from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

TARGET_COUNTIES = [
    "Ventura",
    "Santa Barbara",
    "San Luis Obispo",
    "Orange",
]
YEAR_START = 2015
YEAR_END = 2024

ELECTRICITY_FILENAME = "AGG_CONSUMPTION_ELEC_COUNTY_TBL_ada.xlsx"
POPULATION_FILENAMES = [
    "E-6_Report_July_2010-2019_w.xlsx",
    "E-6_Report_July_2020-2025_Feb26_w.xlsx",
]


def resolve_input_file(filename: str) -> Path:
    candidates = [
        BASE_DIR / filename,
        DATA_DIR / "raw" / filename,
    ]
    for path in candidates:
        if path.exists():
            return path
    searched = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Could not find {filename}. Searched: {searched}")


def normalize_county_name(value: object) -> str | None:
    if pd.isna(value):
        return None
    text = str(value).strip()
    if not text:
        return None
    return text.title()


def load_electricity() -> pd.DataFrame:
    path = resolve_input_file(ELECTRICITY_FILENAME)
    df = pd.read_excel(path)
    df = df.rename(
        columns={
            "YEAR": "year",
            "COUNTY_NAME": "county",
            "SECTOR": "sector",
            "GWH": "gwh",
        }
    )
    df["county"] = df["county"].map(normalize_county_name)
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["gwh"] = pd.to_numeric(df["gwh"], errors="coerce")

    df = df[
        df["county"].isin(TARGET_COUNTIES)
        & df["year"].between(YEAR_START, YEAR_END)
        & df["gwh"].notna()
    ][["year", "county", "sector", "gwh"]].copy()

    return df


def load_population_file(path: Path) -> pd.DataFrame:
    workbook = pd.ExcelFile(path)
    report_sheet = next(
        sheet_name for sheet_name in workbook.sheet_names if "Report" in sheet_name
    )
    df = pd.read_excel(path, sheet_name=report_sheet, header=None)

    records: list[dict[str, object]] = []
    current_county: str | None = None
    continuation_fragment: str | None = None

    for idx, row in enumerate(df.itertuples(index=False)):
        county_cell = normalize_county_name(row[0])
        year_label = str(row[1]).strip() if not pd.isna(row[1]) else ""

        next_county_cell = None
        next_year_label = ""
        if idx + 1 < len(df):
            next_county_cell = normalize_county_name(df.iat[idx + 1, 0])
            next_year_label = str(df.iat[idx + 1, 1]).strip() if not pd.isna(df.iat[idx + 1, 1]) else ""

        if county_cell:
            combined_county = None
            if (
                year_label.startswith("Census")
                and next_county_cell
                and next_year_label.startswith("Apr-Jun")
            ):
                candidate = f"{county_cell} {next_county_cell}"
                if candidate in TARGET_COUNTIES:
                    combined_county = candidate

            if combined_county:
                current_county = combined_county
                continuation_fragment = next_county_cell
            elif continuation_fragment and county_cell == continuation_fragment and year_label.startswith("Apr-Jun"):
                pass
            else:
                current_county = county_cell
                continuation_fragment = None

        if current_county not in TARGET_COUNTIES:
            continue

        year_match = re.search(r"(\d{4})$", year_label)
        if not year_match:
            continue

        population = pd.to_numeric(row[2], errors="coerce")
        if pd.isna(population):
            continue

        records.append(
            {
                "county": current_county,
                "year": int(year_match.group(1)),
                "population": int(population),
            }
        )

    if not records:
        raise ValueError(f"No population rows parsed from {path.name}")

    return pd.DataFrame.from_records(records)


def load_population() -> pd.DataFrame:
    frames = [load_population_file(resolve_input_file(name)) for name in POPULATION_FILENAMES]
    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(subset=["county", "year"], keep="last")
    df = df[df["year"].between(YEAR_START, YEAR_END)].copy()
    return df


def build_dataset() -> pd.DataFrame:
    electricity = load_electricity()
    population = load_population()

    merged = electricity.merge(population, on=["county", "year"], how="left", validate="many_to_one")
    missing_population = merged["population"].isna().sum()
    if missing_population:
        raise ValueError(f"{missing_population} electricity rows are missing population values.")

    merged["gwh_per_capita"] = merged["gwh"] / merged["population"]
    merged = merged.sort_values(["county", "year", "sector"]).reset_index(drop=True)

    return merged


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DIR / "county_energy_population.csv"

    dataset = build_dataset()
    dataset.to_csv(output_path, index=False)

    county_totals = (
        dataset.groupby(["county", "year"], as_index=False)
        .agg(gwh=("gwh", "sum"), population=("population", "first"))
        .assign(kwh_per_capita=lambda frame: frame["gwh"] * 1_000_000 / frame["population"])
    )

    latest_year = int(county_totals["year"].max())
    latest = county_totals[county_totals["year"] == latest_year].sort_values("county")

    print(f"Wrote {len(dataset):,} rows to {output_path}")
    print(f"Years: {int(dataset['year'].min())}-{int(dataset['year'].max())}")
    print("Latest county totals:")
    print(latest.to_string(index=False))


if __name__ == "__main__":
    main()

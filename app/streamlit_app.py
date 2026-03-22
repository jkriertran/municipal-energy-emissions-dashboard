from __future__ import annotations
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
BASE_DIR = APP_DIR.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "county_energy_population.csv"

COLOR_PRIMARY = "#0f5c5a"
COLOR_ACCENT = "#b55a30"
COLOR_SOFT = "#edf3f0"
COLOR_TEXT = "#132628"
COLOR_MUTED = "#3f5558"
COLOR_CARD = "#ffffff"
COLOR_BORDER = "rgba(19, 38, 40, 0.14)"
COLOR_GRID = "rgba(19, 38, 40, 0.18)"
COLOR_PLOT_BG = "#fbfcfa"
COLOR_SIDEBAR_BG = "#f7faf8"
COLOR_FIELD_BG = "#ffffff"
COLOR_FIELD_ALT = "#e8efeb"
COLOR_CHIP_BG = "#d9e6df"
CHART_FONT_FAMILY = "Arial, Helvetica, sans-serif"
CHART_TITLE_FONT_FAMILY = "Arial Black, Arial, Helvetica, sans-serif"
TOP_CHART_HEIGHT = 500


st.set_page_config(
    page_title="Municipal Energy & Emissions Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

st.markdown(
    f"""
    <style>
      .stApp {{
        font-family: {CHART_FONT_FAMILY};
        background:
          radial-gradient(circle at top left, rgba(15, 92, 90, 0.08), transparent 26%),
          radial-gradient(circle at top right, rgba(181, 90, 48, 0.06), transparent 22%),
          linear-gradient(180deg, #f7f7f4 0%, #f3f7f4 52%, #eef4f2 100%);
        color: {COLOR_TEXT};
      }}
      .stApp, .stApp p, .stApp label, .stApp span, .stApp div {{
        color: {COLOR_TEXT};
      }}
      .block-container {{
        padding-top: 2.25rem;
        padding-bottom: 2rem;
        padding-left: 1.35rem;
        padding-right: 1.35rem;
        max-width: 1400px;
      }}
      section[data-testid="stSidebar"] {{
        background: {COLOR_SIDEBAR_BG};
        border-right: 1px solid {COLOR_BORDER};
      }}
      section[data-testid="stSidebar"] > div {{
        background: {COLOR_SIDEBAR_BG};
      }}
      section[data-testid="stSidebar"] * {{
        color: {COLOR_TEXT} !important;
      }}
      section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
        padding-top: 0.4rem;
      }}
      section[data-testid="stSidebar"] h2 {{
        color: {COLOR_TEXT} !important;
        letter-spacing: -0.02em;
      }}
      section[data-testid="stSidebar"] label,
      section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
        color: {COLOR_MUTED} !important;
        font-weight: 600;
      }}
      section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background: {COLOR_FIELD_BG} !important;
        border: 1px solid rgba(19, 38, 40, 0.16) !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 24px rgba(19, 38, 40, 0.05) !important;
        min-height: 56px;
      }}
      section[data-testid="stSidebar"] [data-baseweb="select"] input,
      section[data-testid="stSidebar"] [data-baseweb="select"] div,
      section[data-testid="stSidebar"] [data-baseweb="select"] span {{
        color: {COLOR_TEXT} !important;
      }}
      section[data-testid="stSidebar"] [data-baseweb="select"] svg {{
        fill: {COLOR_TEXT} !important;
        color: {COLOR_TEXT} !important;
      }}
      section[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="tag"] {{
        background: {COLOR_CHIP_BG} !important;
        border: 1px solid rgba(15, 92, 90, 0.14) !important;
        border-radius: 12px !important;
        padding: 0.15rem 0.35rem !important;
      }}
      section[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="tag"] span {{
        color: {COLOR_TEXT} !important;
        font-weight: 600;
      }}
      section[data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="tag"] svg {{
        fill: {COLOR_TEXT} !important;
      }}
      section[data-testid="stSidebar"] [data-baseweb="popover"] {{
        background: {COLOR_FIELD_BG} !important;
      }}
      section[data-testid="stSidebar"] button[kind="secondary"] {{
        background: {COLOR_FIELD_ALT} !important;
        border: 1px solid rgba(19, 38, 40, 0.14) !important;
      }}
      section[data-testid="stSidebar"] button[kind="secondary"]:hover {{
        background: {COLOR_CHIP_BG} !important;
      }}
      header[data-testid="stHeader"] {{
        background: rgba(19, 38, 40, 0.96) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      }}
      header[data-testid="stHeader"] [data-testid="stToolbar"] {{
        color: #f8fbfc !important;
      }}
      header[data-testid="stHeader"] *,
      header[data-testid="stHeader"] a,
      header[data-testid="stHeader"] span,
      header[data-testid="stHeader"] button {{
        color: #f8fbfc !important;
      }}
      header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
      header[data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
      header[data-testid="stHeader"] button[data-testid="stBaseButton-headerNoPadding"],
      header[data-testid="stHeader"] button[data-testid="stBaseButton-header"] {{
        color: #f8fbfc !important;
        border-radius: 10px !important;
      }}
      header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"]:hover,
      header[data-testid="stHeader"] [data-testid="stSidebarCollapseButton"]:hover,
      header[data-testid="stHeader"] button[data-testid="stBaseButton-headerNoPadding"]:hover,
      header[data-testid="stHeader"] button[data-testid="stBaseButton-header"]:hover {{
        background: rgba(255, 255, 255, 0.10) !important;
      }}
      header[data-testid="stHeader"] [data-testid="stIconMaterial"] {{
        color: #f8fbfc !important;
      }}
      header[data-testid="stHeader"] svg,
      header[data-testid="stHeader"] button svg {{
        fill: #f8fbfc !important;
        color: #f8fbfc !important;
      }}
      [data-testid="stToolbar"] button {{
        color: #f8fbfc !important;
      }}
      [data-testid="stToolbar"] button:hover {{
        background: rgba(255, 255, 255, 0.08) !important;
      }}
      .hero {{
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(19, 38, 40, 0.10);
        border-radius: 28px;
        padding: 1.5rem 1.6rem 1.3rem;
        box-shadow: 0 18px 44px rgba(19, 38, 40, 0.07);
        backdrop-filter: blur(10px);
      }}
      .eyebrow {{
        color: {COLOR_PRIMARY};
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
      }}
      .hero h1 {{
        color: {COLOR_TEXT};
        font-size: 2.35rem;
        line-height: 1.02;
        margin: 0 0 0.5rem;
      }}
      .hero p {{
        font-size: 1rem;
        max-width: 62ch;
        color: rgba(19, 38, 40, 0.85);
        margin: 0;
      }}
      .metric-card {{
        background: {COLOR_CARD};
        border: 1px solid {COLOR_BORDER};
        border-radius: 22px;
        padding: 1rem 1.1rem 0.95rem;
        min-height: 196px;
        box-shadow: 0 16px 36px rgba(19, 38, 40, 0.06);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        gap: 0.8rem;
      }}
      .metric-top {{
        min-height: 2.6rem;
      }}
      .metric-label {{
        font-size: 0.92rem;
        color: {COLOR_MUTED};
        line-height: 1.35;
      }}
      .metric-main {{
        min-height: 4.9rem;
      }}
      .metric-value {{
        font-size: clamp(2rem, 2.2vw, 2.45rem);
        line-height: 1;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: {COLOR_TEXT};
      }}
      .metric-secondary {{
        font-size: 0.94rem;
        font-weight: 600;
        color: {COLOR_PRIMARY};
        margin-top: 0.32rem;
      }}
      .metric-caption {{
        font-size: 0.91rem;
        line-height: 1.45;
        color: {COLOR_MUTED};
        min-height: 2.7rem;
      }}
      .insights-panel {{
        background: rgba(255, 255, 255, 0.94);
        border: 1px solid {COLOR_BORDER};
        border-radius: 24px;
        padding: 1.15rem 1.2rem 1.05rem;
        box-shadow: 0 16px 36px rgba(19, 38, 40, 0.06);
        margin-top: 1rem;
      }}
      .insights-title {{
        color: {COLOR_TEXT};
        font-size: 1.08rem;
        font-weight: 700;
        letter-spacing: -0.01em;
        margin-bottom: 0.75rem;
      }}
      .insights-grid {{
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.75rem;
      }}
      .insight-item {{
        background: {COLOR_SOFT};
        border: 1px solid rgba(15, 92, 90, 0.10);
        border-radius: 18px;
        padding: 0.9rem 0.95rem;
      }}
      .insight-label {{
        color: {COLOR_MUTED};
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
      }}
      .insight-text {{
        color: {COLOR_TEXT};
        font-size: 0.96rem;
        line-height: 1.45;
      }}
      .section-heading {{
        margin: 0 0 0.35rem;
      }}
      .section-spacer {{
        height: 1.9rem;
      }}
      .chart-header {{
        padding-top: 0.55rem;
        margin-bottom: 0.2rem;
      }}
      .chart-kicker {{
        color: {COLOR_MUTED};
        font-size: 0.88rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
      }}
      .chart-title {{
        color: {COLOR_TEXT};
        font-size: 1.55rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        line-height: 1.08;
        min-height: 3.4rem;
        margin: 0 0 0.85rem;
      }}
      div[data-testid="stPlotlyChart"] {{
        background: {COLOR_CARD};
        border: 1px solid {COLOR_BORDER};
        border-radius: 24px;
        padding: 0.7rem 0.7rem 0.25rem;
        box-shadow: 0 16px 36px rgba(19, 38, 40, 0.06);
      }}
      div[data-testid="stPlotlyChart"] > div {{
        border-radius: 18px;
      }}
      h3 {{
        color: {COLOR_TEXT} !important;
      }}
      .note {{
        background: #eef4f2;
        border-left: 4px solid {COLOR_PRIMARY};
        padding: 0.9rem 1rem;
        border-radius: 12px;
        font-size: 0.95rem;
      }}
      @media (max-width: 1100px) {{
        .insights-grid {{
          grid-template-columns: 1fr;
        }}
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing processed dataset at {DATA_PATH}. Run scripts/build_county_energy_population.py first."
        )

    df = pd.read_csv(DATA_PATH)
    df["year"] = df["year"].astype(int)
    df["gwh"] = pd.to_numeric(df["gwh"], errors="coerce")
    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    df["gwh_per_capita"] = pd.to_numeric(df["gwh_per_capita"], errors="coerce")
    return df


def build_totals(df: pd.DataFrame) -> pd.DataFrame:
    totals = (
        df.groupby(["county", "year"], as_index=False)
        .agg(gwh=("gwh", "sum"), population=("population", "first"))
        .assign(
            kwh_per_capita=lambda frame: frame["gwh"] * 1_000_000 / frame["population"],
            mwh_per_capita=lambda frame: frame["gwh"] * 1_000 / frame["population"],
        )
    )
    return totals


def display_metric_card(
    column: st.delta_generator.DeltaGenerator,
    label: str,
    value: str,
    secondary: str,
    caption: str,
) -> None:
    column.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-top">
            <div class="metric-label">{label}</div>
          </div>
          <div class="metric-main">
            <div class="metric-value">{value}</div>
            <div class="metric-secondary">{secondary}</div>
          </div>
          <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def latest_snapshot(county_df: pd.DataFrame, sector_df: pd.DataFrame) -> dict[str, float]:
    latest_year = int(county_df["year"].max())
    latest_row = county_df[county_df["year"] == latest_year].iloc[0]
    first_row = county_df[county_df["year"] == int(county_df["year"].min())].iloc[0]
    latest_sectors = sector_df[sector_df["year"] == latest_year].copy()
    latest_sectors["share"] = latest_sectors["gwh"] / latest_sectors["gwh"].sum()
    largest_sector = latest_sectors.sort_values("share", ascending=False).iloc[0]

    return {
        "latest_year": latest_year,
        "latest_gwh": float(latest_row["gwh"]),
        "first_gwh": float(first_row["gwh"]),
        "kwh_per_capita": float(latest_row["kwh_per_capita"]),
        "largest_sector_share": float(largest_sector["share"]),
        "largest_sector_name": str(largest_sector["sector"]),
    }


def build_key_insights(
    selected_county: str,
    county_df: pd.DataFrame,
    compare_df: pd.DataFrame,
    snapshot: dict[str, float],
) -> list[tuple[str, str]]:
    latest_year = int(snapshot["latest_year"])
    first_year = int(county_df["year"].min())
    change_pct = (snapshot["latest_gwh"] - snapshot["first_gwh"]) / snapshot["first_gwh"] * 100
    change_direction = "down" if change_pct < 0 else "up"

    insights: list[tuple[str, str]] = [
        (
            "Trend",
            f"{selected_county} used {snapshot['latest_gwh']:,.0f} GWh in {latest_year}, {change_direction} "
            f"{abs(change_pct):.1f}% since {first_year}.",
        ),
        (
            "Sector Mix",
            f"{snapshot['largest_sector_name']} is the largest sector in {latest_year}, accounting for "
            f"{snapshot['largest_sector_share'] * 100:.1f}% of county electricity use.",
        ),
    ]

    latest_compare = compare_df[compare_df["year"] == latest_year].copy()
    peer_compare = latest_compare[latest_compare["county"] != selected_county].copy()

    if not peer_compare.empty:
        peer_average = float(peer_compare["kwh_per_capita"].mean())
        diff_pct = (snapshot["kwh_per_capita"] - peer_average) / peer_average * 100
        relative_position = "above" if diff_pct > 0 else "below"
        insights.append(
            (
                "Benchmark",
                f"In {latest_year}, {selected_county} per-capita use was {abs(diff_pct):.1f}% {relative_position} "
                f"the selected peer average.",
            )
        )
    else:
        insights.append(
            (
                "Per Capita",
                f"{selected_county} recorded {snapshot['kwh_per_capita']:,.0f} kWh per resident in {latest_year}.",
            )
        )

    return insights


def year_tick_values(years: list[int]) -> list[int]:
    unique_years = sorted({int(year) for year in years})
    if len(unique_years) <= 6:
        return unique_years

    ticks = [year for year in unique_years if year % 2 == 0]
    if unique_years[-1] not in ticks:
        ticks.append(unique_years[-1])
    return ticks


def render_chart_header(column: st.delta_generator.DeltaGenerator, county_name: str, title: str) -> None:
    column.markdown(
        f"""
        <div class="chart-header">
          <div class="chart-kicker">{county_name} County</div>
          <div class="chart-title">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_chart_theme(fig, *, height: int, legend_orientation: str = "h", legend_y: float = -0.22) -> None:
    fig.update_layout(
        height=height,
        margin=dict(l=28, r=34, t=16, b=104 if legend_orientation == "h" else 18),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=COLOR_PLOT_BG,
        font=dict(color=COLOR_TEXT, size=15, family=CHART_FONT_FAMILY),
        hoverlabel=dict(bgcolor="#ffffff", font_color=COLOR_TEXT),
        legend=dict(
            orientation=legend_orientation,
            yanchor="top" if legend_orientation == "h" else "middle",
            y=legend_y if legend_orientation == "h" else 0.5,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(color=COLOR_TEXT, size=12, family=CHART_FONT_FAMILY),
            title_font=dict(color=COLOR_TEXT, size=12, family=CHART_FONT_FAMILY),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(color=COLOR_TEXT, size=15, family=CHART_FONT_FAMILY),
        title_font=dict(color=COLOR_TEXT, size=21, family=CHART_TITLE_FONT_FAMILY),
        linecolor=COLOR_BORDER,
        tickcolor=COLOR_BORDER,
        zeroline=False,
        showline=True,
        automargin=True,
        title_standoff=18,
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=COLOR_GRID,
        tickfont=dict(color=COLOR_TEXT, size=15, family=CHART_FONT_FAMILY),
        title_font=dict(color=COLOR_TEXT, size=21, family=CHART_TITLE_FONT_FAMILY),
        tickcolor=COLOR_BORDER,
        zeroline=False,
        automargin=True,
        title_standoff=18,
    )


try:
    raw_df = load_data()
except Exception as exc:
    st.error(str(exc))
    st.stop()


totals_df = build_totals(raw_df)
counties = sorted(totals_df["county"].unique().tolist())
default_county = "Ventura" if "Ventura" in counties else counties[0]
default_peers = [county for county in counties if county != default_county]

with st.sidebar:
    st.header("Filters")
    selected_county = st.selectbox("Focus county", counties, index=counties.index(default_county))
    selected_peers = st.multiselect(
        "Benchmark counties",
        options=[county for county in counties if county != selected_county],
        default=[county for county in default_peers if county != selected_county],
    )

county_totals = totals_df[totals_df["county"] == selected_county].copy()
county_sectors = raw_df[raw_df["county"] == selected_county].copy()
compare_totals = totals_df[totals_df["county"].isin([selected_county, *selected_peers])].copy()
snapshot = latest_snapshot(county_totals, county_sectors)
key_insights = build_key_insights(selected_county, county_totals, compare_totals, snapshot)

sector_labels = {
    "Agriculture and Water Pumping": "Agriculture & Water",
    "Commercial": "Commercial",
    "Industrial": "Industrial",
    "Mining": "Mining",
    "Residential": "Residential",
    "Streetlighting": "Streetlighting",
    "Transportation, Communications, & Utilities": "Transport / Utilities",
}
county_sectors["sector_display"] = county_sectors["sector"].map(sector_labels).fillna(county_sectors["sector"])
trend_year_ticks = year_tick_values(county_totals["year"].tolist())
sector_year_ticks = year_tick_values(county_sectors["year"].tolist())
benchmark_year_ticks = year_tick_values(compare_totals["year"].tolist())

sector_colors = {
    "Agriculture & Water": "#124c5b",
    "Commercial": "#1d7874",
    "Industrial": "#78a6a3",
    "Mining": "#d19a1f",
    "Residential": "#b85c38",
    "Streetlighting": "#7c3f2c",
    "Transport / Utilities": "#5d6d7e",
}
sector_total_by_year = county_sectors.groupby("year", as_index=False)["gwh"].sum()
sector_y_max = float(sector_total_by_year["gwh"].max())
sector_y_upper = sector_y_max * 1.12

st.markdown(
    f"""
    <div class="hero">
      <div class="eyebrow">Municipal Energy & Emissions Dashboard</div>
      <h1>{selected_county} County Electricity Benchmark</h1>
      <p>
        A lightweight public-sector dashboard for tracking electricity trends, sector mix, and peer benchmarks
        using public California county data. This first page is designed for fast reporting and interview-ready storytelling.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

st.markdown(
    f"""
    <div class="insights-panel">
      <div class="insights-title">Key Insights</div>
      <div class="insights-grid">
        {''.join(
            f'''
            <div class="insight-item">
              <div class="insight-label">{label}</div>
              <div class="insight-text">{text}</div>
            </div>
            '''
            for label, text in key_insights
        )}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
change_pct = (snapshot["latest_gwh"] - snapshot["first_gwh"]) / snapshot["first_gwh"] * 100

display_metric_card(
    metric_1,
    "Total Electricity Use",
    f"{snapshot['latest_gwh']:,.0f}",
    f"GWh in {snapshot['latest_year']}",
    "Latest annual county electricity demand.",
)
display_metric_card(
    metric_2,
    f"Change Since {int(county_totals['year'].min())}",
    f"{change_pct:,.1f}",
    f"% through {snapshot['latest_year']}",
    f"Net change from {int(county_totals['year'].min())} to {snapshot['latest_year']}.",
)
display_metric_card(
    metric_3,
    "Per-Capita Use",
    f"{snapshot['kwh_per_capita']:,.0f}",
    f"kWh per resident in {snapshot['latest_year']}",
    "Electricity demand normalized by population.",
)
display_metric_card(
    metric_4,
    "Largest Sector Share",
    f"{snapshot['largest_sector_share'] * 100:,.1f}",
    f"% {snapshot['largest_sector_name']}",
    "Largest contributor in the latest year.",
)

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)

chart_left, chart_right = st.columns(2, gap="large")

with chart_left:
    render_chart_header(chart_left, selected_county, "Total Electricity Trend")
    trend_fig = px.line(
        county_totals,
        x="year",
        y="gwh",
        markers=True,
        color_discrete_sequence=[COLOR_PRIMARY],
    )
    trend_fig.update_traces(line_width=3, marker_size=8)
    apply_chart_theme(trend_fig, height=TOP_CHART_HEIGHT, legend_orientation="h", legend_y=-0.22)
    trend_fig.update_layout(showlegend=False, yaxis_title="GWh", xaxis_title="Year")
    trend_fig.update_xaxes(
        tickmode="array",
        tickvals=trend_year_ticks,
        ticktext=[str(year) for year in trend_year_ticks],
        range=[county_totals["year"].min() - 0.25, county_totals["year"].max() + 0.45],
    )
    st.plotly_chart(trend_fig, width="stretch")

with chart_right:
    render_chart_header(chart_right, selected_county, "Sector Mix Over Time")
    sector_fig = px.area(
        county_sectors,
        x="year",
        y="gwh",
        color="sector_display",
        color_discrete_map=sector_colors,
    )
    sector_fig.update_traces(mode="lines", line={"width": 1.8})
    apply_chart_theme(sector_fig, height=TOP_CHART_HEIGHT, legend_orientation="h", legend_y=-0.17)
    sector_fig.update_layout(yaxis_title="GWh", xaxis_title="Year", showlegend=True, legend_title_text="")
    sector_fig.update_xaxes(
        tickmode="array",
        tickvals=sector_year_ticks,
        ticktext=[str(year) for year in sector_year_ticks],
        range=[county_sectors["year"].min() - 0.25, county_sectors["year"].max() + 0.55],
    )
    sector_fig.update_yaxes(
        range=[0, sector_y_upper],
        nticks=6,
    )
    st.plotly_chart(sector_fig, width="stretch")

st.subheader("Peer Benchmark: Per-Capita Electricity Use")
benchmark_fig = px.line(
    compare_totals,
    x="year",
    y="kwh_per_capita",
    color="county",
    markers=True,
    color_discrete_map={
        selected_county: COLOR_PRIMARY,
        "Santa Barbara": "#d99058",
        "San Luis Obispo": "#7d8f69",
        "Orange": "#5d6f8a",
    },
)
benchmark_fig.update_traces(line_width=3, marker_size=7)
apply_chart_theme(benchmark_fig, height=405, legend_orientation="h", legend_y=-0.22)
benchmark_fig.update_layout(
    yaxis_title="kWh per resident",
    xaxis_title="Year",
    legend_title_text="County",
)
benchmark_fig.update_xaxes(
    tickmode="array",
    tickvals=benchmark_year_ticks,
    ticktext=[str(year) for year in benchmark_year_ticks],
    range=[compare_totals["year"].min() - 0.25, compare_totals["year"].max() + 0.45],
)
st.plotly_chart(benchmark_fig, width="stretch")

st.markdown(
    """
    <div class="note">
      Source note: this page combines California Energy Commission county electricity consumption data with
      California Department of Finance county population estimates. The latest shared year in this MVP is 2024.
    </div>
    """,
    unsafe_allow_html=True,
)

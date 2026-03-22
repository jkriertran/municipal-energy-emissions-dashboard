# Municipal Energy & Emissions Dashboard

A lightweight Streamlit portfolio project for municipal sustainability and public works analytics roles.

This dashboard uses public California data to show how a county can track:
- annual electricity use
- per-capita electricity demand
- sector mix over time
- peer benchmarking across nearby counties

The current MVP is centered on Ventura County and compares it with Santa Barbara, San Luis Obispo, and Orange County.

## Why this project works for a portfolio

- It is directly relevant to municipal sustainability, reporting, KPI tracking, and benchmarking.
- It uses public-sector style analysis instead of flashy but low-value ML.
- It is explainable to non-technical stakeholders.
- It is small enough to finish, demo, and discuss clearly in interviews.

## App preview

The app currently includes:
- KPI scorecards for latest electricity use, change over time, per-capita use, and largest sector share
- electricity trend chart
- sector mix chart
- peer benchmark chart

## Tech stack

- Python
- Streamlit
- pandas
- Plotly
- openpyxl

## Project structure

```text
.
├── app/
│   └── streamlit_app.py
├── data/
│   └── processed/
│       └── county_energy_population.csv
├── scripts/
│   └── build_county_energy_population.py
├── requirements.txt
└── README.md
```

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the app:

```bash
streamlit run streamlit_app.py
```

You can still run the original module directly if you prefer:

```bash
streamlit run app/streamlit_app.py
```

## Deploy on Streamlit Community Cloud

Use these settings when you create the app:

- Repository: `jkriertran/municipal-energy-emissions-dashboard`
- Branch: `main`
- Main file path: `streamlit_app.py`
- Python version: `3.12` or current default

Community Cloud requires you to choose the repository, branch, and entrypoint file path explicitly. Keeping a root-level `streamlit_app.py` makes deployment more reliable and avoids path confusion when the app code lives in a subfolder.

## Rebuild the processed dataset

The repo includes the processed dataset needed to run the app.

If you want to rebuild it from source workbooks, place these local raw files in the project root or `data/raw/`:

- `AGG_CONSUMPTION_ELEC_COUNTY_TBL_ada.xlsx`
- `E-6_Report_July_2010-2019_w.xlsx`
- `E-6_Report_July_2020-2025_Feb26_w.xlsx`

Then run:

```bash
python scripts/build_county_energy_population.py
```

## Data sources

- California Energy Commission county electricity consumption data
- California Department of Finance county population estimates

Official source pages:
- https://www.energy.ca.gov/files/energy-consumption-data-files
- https://dof.ca.gov/forecasting/demographics/estimates/

## Next planned additions

- facility emissions page using Ventura County regulated emissions data
- deployment configuration for a public demo link
- final README screenshots and resume-ready summary

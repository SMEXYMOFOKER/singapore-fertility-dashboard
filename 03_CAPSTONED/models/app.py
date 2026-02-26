import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Singapore Fertility Intelligence", layout="wide")

theme_base = st.get_option("theme.base")
plotly_template = "plotly_dark" if theme_base == "dark" else "plotly"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data_cleaned")

TFR_CSV = os.path.join(DATA_DIR, "tfr_cleaned.csv")
BIRTHS_CSV = os.path.join(DATA_DIR, "births_cleaned.csv")
HDB_CSV = os.path.join(DATA_DIR, "hdb_annual_cleaned.csv")


@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def ensure_columns(df: pd.DataFrame, rename_map: dict) -> pd.DataFrame:
    df = df.copy()
    for desired, candidates in rename_map.items():
        if desired in df.columns:
            continue
        for c in candidates:
            if c in df.columns:
                df = df.rename(columns={c: desired})
                break
    return df


try:
    tfr = load_csv(TFR_CSV)
    births = load_csv(BIRTHS_CSV)
    hdb = load_csv(HDB_CSV)
except FileNotFoundError as e:
    st.error(f"Missing file: {e}")
    st.stop()


tfr = ensure_columns(
    tfr,
    {
        "Year": ["year", "YEAR"],
        "Total_Fertility_Rate": [
            "TFR",
            "tfr",
            "Total Fertility Rate",
            "Total_FertilityRate",
        ],
    },
)

births = ensure_columns(
    births,
    {
        "Year": ["year", "YEAR"],
        "Birth_Count": [
            "births",
            "Births",
            "Resident_Live_Births",
            "Resident_Births",
            "value",
            "Value",
        ],
        "Data Series": [
            "DataSeries",
            "data_series",
            "Series",
            "Birth_Order",
            "Birth Order",
        ],
    },
)

hdb = ensure_columns(
    hdb,
    {
        "Year": ["year", "YEAR"],
        "HDB_Resale_Index": [
            "HDB Index",
            "HDB_Index",
            "Resale_Index",
            "hdb_index",
            "value",
            "Value",
        ],
    },
)


for df_ in (tfr, births, hdb):
    df_["Year"] = pd.to_numeric(df_["Year"], errors="coerce")

tfr = tfr.dropna(subset=["Year"]).copy()
births = births.dropna(subset=["Year"]).copy()
hdb = hdb.dropna(subset=["Year"]).copy()

tfr["Year"] = tfr["Year"].astype(int)
births["Year"] = births["Year"].astype(int)
hdb["Year"] = hdb["Year"].astype(int)

births["Birth_Count"] = pd.to_numeric(births["Birth_Count"], errors="coerce")


births = births.copy()
births["Year"] = pd.to_numeric(births["Year"], errors="coerce")
births["Birth_Count"] = pd.to_numeric(births["Birth_Count"], errors="coerce")
births = births.dropna(subset=["Year"]).copy()
births["Year"] = births["Year"].astype(int)

if "Data Series" in births.columns:
    births["Data Series"] = births["Data Series"].astype(str).str.strip()

    total_labels = {
        "Resident Live-Births By Birth Order",
        "Resident Live Births By Birth Order",
        "Resident Live-Births",
        "Resident Live Births",
        "Total",
        "TOTAL",
    }
    births_orders = births[~births["Data Series"].isin(total_labels)].copy()
else:
    births_orders = births.copy()
    births_orders["Data Series"] = "Births"

births_total = (
    births.dropna(subset=["Birth_Count"])
    .groupby("Year", as_index=False)
    .agg(Birth_Count_Total=("Birth_Count", "sum"))
)

merged = tfr.merge(births_total, on="Year", how="left").merge(
    hdb[["Year", "HDB_Resale_Index"]], on="Year", how="left"
)

st.sidebar.header("Dashboard Controls")

min_year = int(merged["Year"].min())
max_year = int(merged["Year"].max())

year_range = st.sidebar.slider(
    "Select Year Range", min_year, max_year, (min_year, max_year)
)
show_replacement = st.sidebar.checkbox(
    "Show replacement level (2.1) on TFR chart", value=True
)

if st.sidebar.button("Refresh data"):
    st.cache_data.clear()
    st.rerun()

df = merged[
    (merged["Year"] >= year_range[0]) & (merged["Year"] <= year_range[1])
].copy()
births_anim = births_orders[
    (births_orders["Year"] >= year_range[0]) & (births_orders["Year"] <= year_range[1])
].copy()

can_delta = len(df) >= 2


st.title("Singapore Fertility Dashboard")
st.caption("TFR, resident births (by birth order), HDB resale index")


df_sorted = df.sort_values("Year")
latest = df_sorted.iloc[-1]
prev = df_sorted.iloc[-2] if can_delta else latest

latest_tfr = latest.get("Total_Fertility_Rate")
latest_births = latest.get("Birth_Count_Total")
latest_hdb = latest.get("HDB_Resale_Index")

prev_tfr = prev.get("Total_Fertility_Rate")
prev_births = prev.get("Birth_Count_Total")
prev_hdb = prev.get("HDB_Resale_Index")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Latest TFR",
    "—" if pd.isna(latest_tfr) else f"{latest_tfr:.2f}",
    (
        None
        if (not can_delta or pd.isna(latest_tfr) or pd.isna(prev_tfr))
        else f"{latest_tfr - prev_tfr:+.3f}"
    ),
)

c2.metric(
    "Latest resident births",
    "—" if pd.isna(latest_births) else f"{int(latest_births):,}",
    (
        None
        if (not can_delta or pd.isna(latest_births) or pd.isna(prev_births))
        else f"{int(latest_births - prev_births):+d}"
    ),
)

c3.metric(
    "Latest HDB resale index",
    "—" if pd.isna(latest_hdb) else f"{latest_hdb:.1f}",
    (
        None
        if (not can_delta or pd.isna(latest_hdb) or pd.isna(prev_hdb))
        else f"{latest_hdb - prev_hdb:+.1f}"
    ),
)

st.markdown("---")


tab1, tab2, tab3 = st.tabs(["Trends", "Housing vs fertility", "Model evaluation"])


with tab1:
    st.subheader("Long-term trends")

    left, right = st.columns(2)

    with left:
        fig_tfr = px.line(
            df,
            x="Year",
            y="Total_Fertility_Rate",
            markers=True,
            title="Total fertility rate (TFR)",
        )
        if show_replacement:
            fig_tfr.add_hline(
                y=2.1, line_dash="dash", annotation_text="Replacement level (2.1)"
            )
        fig_tfr.update_layout(template=plotly_template, hovermode="x unified")
        st.plotly_chart(fig_tfr, use_container_width=True)

    with right:
        st.subheader("Resident live births by birth order")

        births_anim = births_anim.dropna(subset=["Birth_Count"]).copy()
        births_anim["Birth_Count"] = births_anim["Birth_Count"].fillna(0)

        keep_keywords = (
            "1",
            "2",
            "3",
            "4",
            "5",
            "first",
            "second",
            "third",
            "fourth",
            "fifth",
            "order",
        )
        births_anim = births_anim[
            births_anim["Data Series"]
            .astype(str)
            .str.lower()
            .str.contains("|".join(keep_keywords), na=False)
        ].copy()

        births_anim["Birth_Order"] = births_anim["Data Series"]

        if births_anim.empty:
            st.info("No birth-order rows found in this year range.")
        else:
            fig_bubbles = px.scatter(
                births_anim,
                x="Birth_Order",
                y="Birth_Count",
                size="Birth_Count",
                color="Birth_Order",
                animation_frame="Year",
                hover_name="Birth_Order",
                hover_data={"Birth_Count": ":,.0f", "Year": True},
                size_max=60,
            )
            fig_bubbles.update_layout(
                template=plotly_template, xaxis_title="", yaxis_title="Birth count"
            )
            fig_bubbles.update_traces(marker=dict(opacity=0.75))
            st.plotly_chart(fig_bubbles, use_container_width=True)

    st.subheader("HDB resale index")

    fig_hdb = px.line(
        df,
        x="Year",
        y="HDB_Resale_Index",
        markers=True,
        title="HDB resale price index",
    )
    fig_hdb.update_layout(template=plotly_template, hovermode="x unified")
    st.plotly_chart(fig_hdb, use_container_width=True)


with tab2:
    st.subheader("Housing vs fertility")

    fig_scatter = px.scatter(
        df.dropna(subset=["Total_Fertility_Rate", "HDB_Resale_Index"]),
        x="HDB_Resale_Index",
        y="Total_Fertility_Rate",
        hover_data=["Year"],
        title="TFR vs HDB resale index",
    )
    fig_scatter.update_layout(template=plotly_template)
    st.plotly_chart(fig_scatter, use_container_width=True)

    tmp = df[["Total_Fertility_Rate", "HDB_Resale_Index"]].dropna()
    if len(tmp) >= 3:
        corr = tmp["Total_Fertility_Rate"].corr(tmp["HDB_Resale_Index"])
        st.info(f"Correlation in selected range: r = {corr:.3f}")
    else:
        st.info("Not enough data in the selected range.")


with tab3:
    st.subheader("Model metrics")

    model_comparison = pd.DataFrame(
        {
            "Model": [
                "Naïve lag-1 baseline",
                "Lag regression model",
                "Extended model (lag + HDB index)",
            ],
            "MAE": [0.0320, 0.0394, 0.1623],
            "RMSE": [0.0412, 0.0477, 0.1676],
            "R²": [0.7689, 0.6901, -2.8166],
        }
    )

    st.dataframe(model_comparison, use_container_width=True)

    st.markdown(
        """
- Lag-1 baseline performs best.
- Lag regression does not improve accuracy.
- Adding HDB index worsens accuracy.
"""
    )


st.caption("Data: 03_CAPSTONED/data_cleaned | Streamlit + Plotly")
# streamlit run /Users/smexymofoker/Documents/PYTHON/03_CAPSTONED/models/app.py

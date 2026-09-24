import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Vaccination Data Dashboard", layout="wide")

engine = create_engine('postgresql://postgres:postgres@localhost:5432/vaccination_db')

st.title("🌍 Global Vaccination Data Dashboard")

# --- Load data ---
@st.cache_data
def load_coverage():
    query = """
    SELECT c.year, c.coverage, co.iso_3_code, co.country_name, co.who_region, v.vaccine_description
    FROM coverage c
    JOIN countries co ON c.iso_3_code = co.iso_3_code
    JOIN vaccines v ON c.vaccine_code = v.vaccine_code
    WHERE c.coverage IS NOT NULL AND c.coverage <= 100
    """
    return pd.read_sql(query, engine)

@st.cache_data
def load_incidence():
    query = """
    SELECT i.year, i.incidence_rate, co.iso_3_code, co.country_name, co.who_region, d.disease_description
    FROM incidence i
    JOIN countries co ON i.iso_3_code = co.iso_3_code
    JOIN diseases d ON i.disease_code = d.disease_code
    WHERE i.incidence_rate IS NOT NULL
    """
    return pd.read_sql(query, engine)

coverage_df = load_coverage()
incidence_df = load_incidence()

# --- Sidebar filters (slicers) ---
st.sidebar.header("Filters")

regions = ["All"] + sorted(coverage_df["who_region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("WHO Region", regions)

vaccines_list = sorted(coverage_df["vaccine_description"].dropna().unique().tolist())
selected_vaccine = st.sidebar.selectbox("Vaccine", ["All"] + vaccines_list)

year_min, year_max = int(coverage_df["year"].min()), int(coverage_df["year"].max())
year_range = st.sidebar.slider("Year Range", year_min, year_max, (year_min, year_max))

# --- Apply filters ---
filtered = coverage_df.copy()
if selected_region != "All":
    filtered = filtered[filtered["who_region"] == selected_region]
if selected_vaccine != "All":
    filtered = filtered[filtered["vaccine_description"] == selected_vaccine]
filtered = filtered[(filtered["year"] >= year_range[0]) & (filtered["year"] <= year_range[1])]

# --- KPI cards ---
col1, col2, col3 = st.columns(3)
col1.metric("Records Shown", f"{len(filtered):,}")
col2.metric("Average Coverage", f"{filtered['coverage'].mean():.1f}%" if len(filtered) else "N/A")
high_coverage_pct = (filtered["coverage"] >= 95).mean() * 100 if len(filtered) else 0
col3.metric("% Records ≥95% Coverage", f"{high_coverage_pct:.1f}%")

# --- Trend line ---
st.subheader("Vaccination Coverage Over Time")
yearly = filtered.groupby("year")["coverage"].mean().reset_index()
fig1 = px.line(yearly, x="year", y="coverage")
st.plotly_chart(fig1, use_container_width=True)

# --- Geographic heatmap ---
st.subheader("Coverage by Country (Latest Year in Range)")
latest_year = filtered["year"].max()
map_data = filtered[filtered["year"] == latest_year].groupby(["iso_3_code", "country_name"])["coverage"].mean().reset_index()
fig2 = px.choropleth(
    map_data, locations="iso_3_code", color="coverage", hover_name="country_name",
    color_continuous_scale="Viridis", range_color=(0, 100)
)
st.plotly_chart(fig2, use_container_width=True)

# --- Scatter plot: coverage vs incidence ---
st.subheader("Coverage vs. Disease Incidence")
cov_by_country_year = filtered.groupby(["iso_3_code", "year"])["coverage"].mean().reset_index()
inc_by_country_year = incidence_df.groupby(["iso_3_code", "year"])["incidence_rate"].mean().reset_index()
merged = pd.merge(cov_by_country_year, inc_by_country_year, on=["iso_3_code", "year"])
fig3 = px.scatter(merged, x="coverage", y="incidence_rate", opacity=0.5,
                   labels={"coverage": "Coverage %", "incidence_rate": "Incidence Rate"})
st.plotly_chart(fig3, use_container_width=True)

# --- Top/bottom countries bar chart ---
st.subheader("Top and Bottom 10 Countries by Average Coverage")
country_avg = filtered.groupby("country_name")["coverage"].mean().dropna().sort_values()
col_a, col_b = st.columns(2)
with col_a:
    fig4 = px.bar(country_avg.tail(10), orientation="h", title="Top 10")
    st.plotly_chart(fig4, use_container_width=True)
with col_b:
    fig5 = px.bar(country_avg.head(10), orientation="h", title="Bottom 10")
    st.plotly_chart(fig5, use_container_width=True)
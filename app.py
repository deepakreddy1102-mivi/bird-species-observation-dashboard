import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Bird Species Observation Dashboard",
    layout="wide"
)

# --------------------------------------------------
# Title & description
# --------------------------------------------------
st.title("Bird Species Observation Dashboard")
st.markdown(
    "Interactive analysis of bird observations across forest and grassland ecosystems."
)

# --------------------------------------------------
# Load cleaned data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Data/Processed/cleaned_bird_observations.csv")

df = load_data()

# --------------------------------------------------
# Sidebar - Interactive Filters
# --------------------------------------------------
st.sidebar.header("🔎 Filter Observations")

ecosystem_options = ["All"] + sorted(df["Ecosystem"].dropna().unique().tolist())
selected_ecosystem = st.sidebar.selectbox("Select Ecosystem", ecosystem_options)

year_options = ["All"] + sorted(df["Year"].dropna().unique().tolist())
selected_year = st.sidebar.selectbox("Select Year", year_options)

species_options = ["All"] + sorted(df["Common_Name"].dropna().unique().tolist())
selected_species = st.sidebar.selectbox("Select Species", species_options)

# --------------------------------------------------
# Apply filters
# --------------------------------------------------
filtered_df = df.copy()

if selected_ecosystem != "All":
    filtered_df = filtered_df[filtered_df["Ecosystem"] == selected_ecosystem]

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]

if selected_species != "All":
    filtered_df = filtered_df[filtered_df["Common_Name"] == selected_species]

# --------------------------------------------------
# Dataset Overview (KPIs)
# --------------------------------------------------
st.subheader("📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Observations", len(filtered_df))

with col2:
    st.metric("Unique Species", filtered_df["Common_Name"].nunique())

with col3:
    st.metric("Ecosystems", filtered_df["Ecosystem"].nunique())

# ==================================================
# STEP 11A.3 – ADVANCED VISUALIZATIONS
# ==================================================

# --------------------------------------------------
# 1. Observation Count by Ecosystem
# --------------------------------------------------
st.subheader("Observation Count by Ecosystem")

eco_counts = (
    filtered_df["Ecosystem"]
    .value_counts()
    .reset_index()
)
eco_counts.columns = ["Ecosystem", "Observations"]

fig_eco = px.bar(
    eco_counts,
    x="Ecosystem",
    y="Observations",
    text="Observations",
    title="Observation Count by Ecosystem",
)
st.plotly_chart(fig_eco, use_container_width=True)

# --------------------------------------------------
# 2. Top 10 Most Observed Species
# --------------------------------------------------
st.subheader("Top 10 Most Observed Bird Species")

species_counts = (
    filtered_df["Common_Name"]
    .value_counts()
    .head(10)
    .reset_index()
)
species_counts.columns = ["Species", "Observations"]

fig_species = px.bar(
    species_counts,
    x="Species",
    y="Observations",
    text="Observations",
    title="Top 10 Most Observed Species",
)
st.plotly_chart(fig_species, use_container_width=True)

# --------------------------------------------------
# 3. Visit-wise Observation Trend
# --------------------------------------------------
st.subheader("🔁 Observation Count by Visit")

visit_counts = (
    filtered_df["Visit"]
    .value_counts()
    .sort_index()
    .reset_index()
)
visit_counts.columns = ["Visit", "Observations"]

fig_visit = px.bar(
    visit_counts,
    x="Visit",
    y="Observations",
    text="Observations",
    title="Observation Count by Visit",
)
st.plotly_chart(fig_visit, use_container_width=True)

# --------------------------------------------------
# 4. Species Richness by Ecosystem
# --------------------------------------------------
st.subheader("🌿 Species Richness by Ecosystem")

richness_ecosystem = (
    filtered_df.groupby("Ecosystem")["Common_Name"]
    .nunique()
    .reset_index()
)
richness_ecosystem.columns = ["Ecosystem", "Unique Species"]

fig_rich_eco = px.bar(
    richness_ecosystem,
    x="Ecosystem",
    y="Unique Species",
    text="Unique Species",
    title="Species Richness by Ecosystem",
)
st.plotly_chart(fig_rich_eco, use_container_width=True)

# --------------------------------------------------
# 5. Species Richness Across Visits
# --------------------------------------------------
st.subheader("📈 Species Richness Across Visits")

richness_visit = (
    filtered_df.groupby("Visit")["Common_Name"]
    .nunique()
    .reset_index()
)
richness_visit.columns = ["Visit", "Unique Species"]

fig_rich_visit = px.line(
    richness_visit,
    x="Visit",
    y="Unique Species",
    markers=True,
    title="Species Richness Across Visits",
)
st.plotly_chart(fig_rich_visit, use_container_width=True)

# --------------------------------------------------
# 6. Conservation Priority (PIF Watchlist)
# --------------------------------------------------
st.subheader("🛑 PIF Watchlist Species Distribution")

pif_counts = (
    filtered_df["PIF_Watchlist_Status"]
    .value_counts()
    .reset_index()
)
pif_counts.columns = ["PIF Watchlist Status", "Observations"]

fig_pif = px.pie(
    pif_counts,
    names="PIF Watchlist Status",
    values="Observations",
    title="PIF Watchlist Observation Distribution",
)
st.plotly_chart(fig_pif, use_container_width=True)

# --------------------------------------------------
# 7. Disturbance Impact
# --------------------------------------------------
st.subheader("Observation Count by Disturbance Level")

disturbance_counts = (
    filtered_df["Disturbance"]
    .value_counts()
    .reset_index()
)
disturbance_counts.columns = ["Disturbance Level", "Observations"]

fig_disturb = px.bar(
    disturbance_counts,
    x="Disturbance Level",
    y="Observations",
    text="Observations",
    title="Observation Count by Disturbance Level",
)
st.plotly_chart(fig_disturb, use_container_width=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.markdown(
    "**Project:** Bird Species Observation Analysis  \n"
    "**Tools:** Python, Pandas, Plotly, Streamlit"
)

import streamlit as st
import pandas as pd
import plotly.express as px

from model import load_data

st.set_page_config(page_title="Exo Galaxy Explorer", layout="wide")

st.title("🌌 Exoplanet 3D Galaxy Explorer (LIVE NASA DATA)")

# Load live data
df = load_data()

# rename for clarity
df = df.rename(columns={
    "pl_orbper": "orbital_period",
    "pl_rade": "radius",
    "pl_bmasse": "mass"
})

# drop missing
df = df.dropna()

# 3D plot
fig = px.scatter_3d(
    df,
    x="orbital_period",
    y="radius",
    z="mass",
    hover_name="pl_name",
    color="radius",
    title="Real Exoplanets in 3D Space"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📊 Dataset Snapshot")
st.write(df.head())

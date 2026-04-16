import streamlit as st
from universe import render_universe

st.set_page_config(page_title="ExoGalaxy", layout="wide")

st.title("🌌 ExoGalaxy 3D Universe")

st.markdown("A cinematic space simulation with anomalies and exoplanet signals.")

render_universe()

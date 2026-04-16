import streamlit as st
from universe import render_universe

# Page config (full screen vibe)
st.set_page_config(
    page_title="ExoGalaxy Universe",
    layout="wide"
)

# Header (minimal cinematic style)
st.title("🌌 ExoGalaxy 3D Universe Explorer")
st.markdown("A cinematic space simulation inspired by exoplanet data patterns.")

# Load 3D universe
render_universe()

import streamlit as st
from universe import render_universe

st.set_page_config(
    page_title="ExoGalaxy v2",
    layout="wide"
)

st.title("🌌 ExoGalaxy v2 — Cosmic Intelligence System")

st.markdown("""
### 🧠 What you're seeing:
- 🟡 Sun system (reference star)
- 🌍 Planets (stable exoplanets)
- 🪐 Exoplanets (detected orbital bodies)
- 🔴 Anomalies (unusual TCE signals)
- ⭐ Star field (galactic background)

This visualization represents **Kepler-style transit detection patterns** mapped into a 3D universe.
""")

render_universe()

import streamlit as st
import model
from space_scene import create_cinematic_galaxy

st.set_page_config(
    page_title="ExoGalaxy",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 FULL BLACK HOLE UI
st.markdown("""
<style>
    body {
        background-color: black;
    }

    .main {
        background-color: black;
    }

    h1 {
        color: white;
        text-align: center;
        font-size: 42px;
        letter-spacing: 3px;
    }
</style>
""", unsafe_allow_html=True)

# 🌌 TITLE
st.title("🌌 EXOGALAXY — CINEMATIC SPACE AI")

st.markdown("""
<div style="
    text-align:center;
    color:#00ffcc;
    font-size:14px;
    margin-bottom:20px;
">
LIVE SIMULATION • DEEP SPACE ML ENGINE • ANOMALY DETECTION SYSTEM
</div>
""", unsafe_allow_html=True)

# ⏳ LOADING FEEL
with st.spinner("Initializing cosmic neural grid..."):
    df = model.generate_space_data(2500)

# 🌠 GENERATE SPACE
fig = create_cinematic_galaxy(df)

st.plotly_chart(fig, use_container_width=True)

# 🧠 INSIGHTS PANEL
st.markdown("## 🧠 Mission Control")
st.write("• White dots = background stars (deep space field)")
st.write("• Colored clusters = exoplanet-like systems detected via ML")
st.write("• Red X = cosmic anomalies (Isolation Forest outliers)")
st.write("• Data is fully synthetic but modeled on Kepler-style structure")

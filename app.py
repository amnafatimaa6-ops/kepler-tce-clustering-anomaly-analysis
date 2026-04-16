import streamlit as st
import model
from space_scene import create_cinematic_galaxy

st.set_page_config(page_title="ExoGalaxy", layout="wide")

# FULL BLACK HOLE MODE UI
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
        font-size: 40px;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌌 EXOGALAXY — CINEMATIC SPACE AI")

# loading animation feel
with st.spinner("Scanning deep space signals..."):
    df = model.generate_space_data(2500)

fig = create_cinematic_galaxy(df)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🧠 Mission Control Insights")
st.write("• White particles = background stars in deep space")
st.write("• Colored clusters = gravitationally similar exoplanet systems")
st.write("• Red X points = cosmic anomalies (rare ML-detected outliers)")

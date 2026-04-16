import streamlit as st
from model import generate_space_data
from space_scene import create_galaxy

st.set_page_config(page_title="ExoGalaxy", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌌 ExoGalaxy 3D Universe Explorer")

# load live synthetic universe
df = generate_space_data(2500)

fig = create_galaxy(df)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🧠 Legend")
st.write("- Colored clusters = different exoplanet signal regimes")
st.write("- Red X points = anomalies (rare cosmic events)")
st.write("- This is a simulated NASA-like ML space model")

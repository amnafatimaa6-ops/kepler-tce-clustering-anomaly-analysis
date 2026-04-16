import streamlit as st
import sys, os

# fix import issues on cloud
sys.path.append(os.path.dirname(__file__))

import model
from space_scene import create_galaxy

st.set_page_config(
    page_title="ExoGalaxy 3D",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🌌 dark space UI
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background: radial-gradient(circle at center, #000010, #000000);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌌 ExoGalaxy 3D Universe Explorer")

st.write("Simulated cosmic ML universe — clusters + anomalies + galaxy structure")

# generate universe
df = model.generate_space_data(2500)

# build 3D galaxy
fig = create_galaxy(df)

# render full screen
st.plotly_chart(fig, use_container_width=True)

# legend
st.markdown("""
### 🧠 Universe Legend
- 🌟 Colored points → Galaxy clusters (different exoplanet regimes)  
- ☄️ Red X → Anomalies (rare / extreme signals)  
- 🌌 Space = simulated astrophysical coordinate system  
""")

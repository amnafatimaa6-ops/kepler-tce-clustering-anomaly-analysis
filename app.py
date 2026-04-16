import streamlit as st
from model import generate_galaxy
from universe import render_universe

st.set_page_config(page_title="ExoGalaxy Explorer", layout="wide")

st.title("🌌 ExoGalaxy 3D Universe Explorer")

df = generate_galaxy()

st.markdown("### 🧠 Dataset simulated from astrophysical signal logic")

st.write(df.head())

html = render_universe(df)

st.components.v1.html(html, height=800)

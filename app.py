import streamlit as st
from model import generate_galaxy
from universe import render_universe

st.set_page_config(page_title="ExoGalaxy Explorer", layout="wide")

st.title("🌌 ExoGalaxy 3D Universe Explorer")

df = generate_galaxy(800)  # keep smaller for stability

html = render_universe(df)

st.components.v1.html(html, height=850, scrolling=False)

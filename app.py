import streamlit as st
from model import generate_galaxy
from universe import render_universe

st.set_page_config(layout="wide")

st.title("🌌 ExoGalaxy Explorer")

df = generate_galaxy(600)  # IMPORTANT: keep moderate size

html = render_universe(df)

st.components.v1.html(html, height=900, scrolling=False)

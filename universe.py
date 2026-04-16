import streamlit as st
import streamlit.components.v1 as components

def render_universe():
    # Open the 3D universe HTML file
    with open("static/index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Render inside Streamlit
    components.html(
        html,
        height=900,
        scrolling=False
    )

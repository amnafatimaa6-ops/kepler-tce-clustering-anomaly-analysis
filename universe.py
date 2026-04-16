import streamlit as st
import streamlit.components.v1 as components
import os

def render_universe():

    file_path = "universe_html.txt"

    if not os.path.exists(file_path):
        st.error("❌ universe_html.txt not found in repo")
        st.stop()

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    components.html(html, height=900, scrolling=False)

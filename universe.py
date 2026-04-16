import streamlit as st
import streamlit.components.v1 as components

def render_universe():
    with open("universe_html.txt", "r", encoding="utf-8") as f:
        html = f.read()

    components.html(html, height=900, scrolling=False)

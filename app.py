import streamlit as st
import universe as uni
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# 🌌 FORCE FULL BLACK SCREEN (IMPORTANT)
st.markdown("""
<style>
    html, body, [class*="css"]  {
        background-color: black !important;
        color: white;
    }

    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
        max-width: 100%;
    }

    header, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# 🌌 GENERATE UNIVERSE
df = uni.generate_universe()

fig = go.Figure()

# 🌞 SUN
sun = df[df["type"] == "sun"]
fig.add_trace(go.Scatter3d(
    x=sun["x"], y=sun["y"], z=sun["z"],
    mode="markers",
    marker=dict(size=20, color="yellow"),
    name="Sun"
))

# 🪐 PLANETS (orbits)
for planet in ["Mercury", "Venus", "Earth", "Mars", "Jupiter"]:
    p = df[df["type"] == planet]
    fig.add_trace(go.Scatter3d(
        x=p["x"], y=p["y"], z=p["z"],
        mode="lines",
        line=dict(width=2),
        name=planet
    ))

# ☄ ASTEROIDS (background space dust)
a = df[df["type"] == "asteroid"]
fig.add_trace(go.Scatter3d(
    x=a["x"], y=a["y"], z=a["z"],
    mode="markers",
    marker=dict(size=1, color="white", opacity=0.2),
    name="Asteroids"
))

# ⚠ ANOMALIES (exoplanets)
an = df[df["type"] == "anomaly"]
fig.add_trace(go.Scatter3d(
    x=an["x"], y=an["y"], z=an["z"],
    mode="markers",
    marker=dict(size=3, color="red"),
    name="Anomalies"
))

# 🌌 MAKE IT FULL IMMERSIVE SPACE
fig.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black",

    margin=dict(l=0, r=0, t=0, b=0),

    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor="black",
        aspectmode="manual",
        aspectratio=dict(x=1, y=1, z=1)
    ),

    showlegend=False
)

# 🚀 FULL WIDTH + FULL HEIGHT FEEL
st.plotly_chart(fig, use_container_width=True)

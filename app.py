import streamlit as st
import plotly.graph_objects as go

from data import load_nasa_data
from model import process_data

st.set_page_config(page_title="ExoGalaxy", layout="wide")

st.title("🌌 ExoGalaxy 3D Universe Explorer")

# Load live NASA data
df = load_nasa_data(limit=200)
df, X = process_data(df)

# 🎯 3D Mapping (SPACE TRANSFORMATION)
df["x"] = df["period"] * 0.02
df["y"] = df["radius"] * 20
df["z"] = df["temp"] * 0.1

# 🎨 Colors
colors = []
sizes = []

for a, r, s in zip(df["anomaly"], df["radius"], df["temp"]):
    if a == -1:
        colors.append("red")     # anomaly = dangerous star
        sizes.append(6)
    else:
        colors.append("white")   # normal star
        sizes.append(3)

# 🌌 FIGURE
fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=df["x"],
    y=df["y"],
    z=df["z"],
    mode="markers",
    marker=dict(
        size=sizes,
        color=colors,
        opacity=0.85
    ),
    text=df["name"],
    hovertemplate="""
    <b>%{text}</b><br>
    Orbit: %{x:.2f}<br>
    Size: %{y:.2f}<br>
    Temp: %{z:.2f}<extra></extra>
    """
))

# 🪐 Styling = space vibe
fig.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black",
    margin=dict(l=0, r=0, t=0, b=0),
    scene=dict(
        xaxis=dict(title="Orbit Distance", color="white"),
        yaxis=dict(title="Planet Radius", color="white"),
        zaxis=dict(title="Temperature", color="white"),
        bgcolor="black"
    ),
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="NASA Mission Control V3.2",
    layout="wide"
)

# -----------------------------
# 🌌 GLOWING HUD THEME (DO NOT REMOVE)
# -----------------------------
st.markdown("""
<style>

body {
    background-color: #050814;
    color: #00ffe1;
}

.stApp {
    background: radial-gradient(circle at top, #0a0f2c, #000000);
}

h1, h2, h3 {
    color: #00ffe1;
    text-shadow: 0 0 12px #00ffe1;
    animation: glow 2s infinite;
}

@keyframes glow {
  0% { text-shadow: 0 0 5px #00ffe1; }
  50% { text-shadow: 0 0 20px #00ffe1; }
  100% { text-shadow: 0 0 5px #00ffe1; }
}

div[data-testid="stMetricValue"] {
    font-size: 28px;
    color: #00ffe1;
    text-shadow: 0 0 12px #00ffe1;
    animation: glow 1.8s infinite;
}

.telemetry {
    font-family: monospace;
    color: #7df9ff;
    background: rgba(0,255,255,0.05);
    padding: 12px;
    border-radius: 12px;
    border: 1px solid rgba(0,255,255,0.3);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("🛰️ NASA MISSION CONTROL — V3.2")
st.subheader("Exoplanet Intelligence System | AI Pattern Mining | Orbital Simulation Engine")

# -----------------------------
# FAKE DATA GENERATION
# -----------------------------
@st.cache_data
def generate_data(n=2500):
    np.random.seed(42)
    df = pd.DataFrame({
        "tce_period": np.random.exponential(50, n),
        "tce_depth": np.random.gamma(2, 5000, n),
        "tce_duration": np.random.normal(5, 2, n).clip(0.5, 20),
        "tce_snr": np.random.exponential(10, n)
    })
    return df

df = generate_data()

features = ["tce_period", "tce_depth", "tce_duration", "tce_snr"]

# -----------------------------
# ML PIPELINE
# -----------------------------
X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

iso = IsolationForest(contamination=0.05, random_state=42)
anomaly = iso.fit_predict(X_scaled)

df["cluster"] = clusters
df["anomaly"] = anomaly

# -----------------------------
# PCA
# -----------------------------
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df["pc1"] = X_pca[:, 0]
df["pc2"] = X_pca[:, 1]

# -----------------------------
# METRICS PANEL
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Signals", len(df))
col2.metric("Anomalies", int((anomaly == -1).sum()))
col3.metric("Clusters", len(np.unique(clusters)))

# -----------------------------
# SYSTEM STATUS
# -----------------------------
anomaly_rate = (df["anomaly"] == -1).mean()

if anomaly_rate < 0.05:
    status = "🟢 STABLE ORBITAL GRID"
elif anomaly_rate < 0.1:
    status = "🟠 MODERATE DISTURBANCE"
else:
    status = "🔴 HIGH COSMIC INSTABILITY"

st.subheader("⚠ SYSTEM STATUS")
st.write(status)

# -----------------------------
# LIVE TELEMETRY STREAM (CINEMATIC)
# -----------------------------
st.markdown("## 📡 LIVE TELEMETRY FEED")

telemetry_box = st.empty()

messages = [
    "Mapping exoplanet probability lattice...",
    "Filtering deep space interference...",
    "Recalibrating anomaly thresholds...",
    "Synchronizing AI detection nodes...",
    "Scanning stellar resonance patterns...",
    "Updating orbital trajectory models..."
]

logs = []

for t in range(25):
    logs.append(f"🛰️ {np.random.choice(messages)} | T+ {t}")

    telemetry_box.markdown(
        "<div class='telemetry'>" +
        "<br>".join(logs[-8:]) +
        "</div>",
        unsafe_allow_html=True
    )

    time.sleep(0.12)

# -----------------------------
# PCA VISUALIZATION
# -----------------------------
st.markdown("## 🧠 SIGNAL INTELLIGENCE GRID (PCA)")

fig1 = px.scatter(
    df,
    x="pc1",
    y="pc2",
    color="cluster",
    opacity=0.6,
    title="Exoplanet Signal Clusters (PCA SPACE)"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# ANOMALY RADAR
# -----------------------------
st.markdown("## 🚨 ANOMALY RADAR")

fig2 = px.scatter(
    df,
    x="pc1",
    y="pc2",
    color=df["anomaly"].map({1: "Normal", -1: "Anomaly"}),
    opacity=0.6,
    title="Isolation Forest Anomaly Detection"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 3D ORBIT SIMULATION
# -----------------------------
st.markdown("## 🪐 ORBITAL SIGNAL FIELD — 3D SPACE")

fig3 = go.Figure(data=[go.Scatter3d(
    x=df["pc1"],
    y=df["pc2"],
    z=df["tce_depth"],
    mode='markers',
    marker=dict(
        size=3,
        color=clusters,
        colorscale='Viridis',
        opacity=0.7
    )
)])

fig3.update_layout(
    paper_bgcolor="black",
    scene=dict(
        xaxis=dict(backgroundcolor="black"),
        yaxis=dict(backgroundcolor="black"),
        zaxis=dict(backgroundcolor="black")
    ),
    margin=dict(l=0, r=0, t=30, b=0),
    scene_camera=dict(eye=dict(x=1.6, y=1.6, z=1.2))
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# INSIGHT PANEL
# -----------------------------
st.markdown("## 🧠 MISSION INTERPRETATION")

st.write("""
- Signal space forms structured orbital clusters
- Dense regions = stable astrophysical populations
- Sparse regions = rare anomaly candidates
- PCA reveals hidden geometry of exoplanet detection space
- Isolation Forest identifies non-conforming cosmic signals
""")

st.success("MISSION CONTINUING — DEEP SPACE ANALYSIS ACTIVE 🚀")

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
# PAGE CONFIG (NASA HUD STYLE)
# -----------------------------
st.set_page_config(
    page_title="NASA Mission Control V3.1",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# COSMIC THEME (CSS HUD GLOW)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #050814;
    color: #00ffe1;
}

h1, h2, h3 {
    color: #00ffe1;
    text-shadow: 0px 0px 12px #00ffe1;
}

.stApp {
    background: radial-gradient(circle at top, #0a0f2c, #000000);
}

div[data-testid="stMetricValue"] {
    font-size: 28px;
    color: #00ffe1;
    text-shadow: 0 0 10px #00ffe1;
}

.block-container {
    padding-top: 2rem;
}

.telemetry {
    font-family: monospace;
    color: #7df9ff;
    background: rgba(0,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
    border: 1px solid rgba(0,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE HEADER
# -----------------------------
st.title("🛰️ NASA MISSION CONTROL — V3.1")
st.subheader("Exoplanet Intelligence System | AI Pattern Mining | Orbital Simulation Engine")

# -----------------------------
# SIDEBAR CONTROL PANEL
# -----------------------------
st.sidebar.title("📡 CONTROL PANEL")
mode = st.sidebar.radio("System Mode", ["LIVE ORBIT SIMULATION", "ANALYTICS GRID"])

# -----------------------------
# FAKE EXOPLANET DATA (NO FILE NEEDED)
# -----------------------------
@st.cache_data
def generate_data(n=2500):
    np.random.seed(42)
    data = pd.DataFrame({
        "tce_period": np.random.exponential(50, n),
        "tce_depth": np.random.gamma(2, 5000, n),
        "tce_duration": np.random.normal(5, 2, n).clip(0.5, 20),
        "tce_snr": np.random.exponential(10, n)
    })
    return data

df = generate_data()

features = ["tce_period", "tce_depth", "tce_duration", "tce_snr"]

# -----------------------------
# PREPROCESSING
# -----------------------------
X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# -----------------------------
# ML MODELS
# -----------------------------
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

iso = IsolationForest(contamination=0.05, random_state=42)
anomaly = iso.fit_predict(X_scaled)

df["cluster"] = clusters
df["anomaly"] = anomaly

# -----------------------------
# PCA REDUCTION
# -----------------------------
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df["pc1"] = X_pca[:, 0]
df["pc2"] = X_pca[:, 1]

# -----------------------------
# HUD METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Signals", len(df))
col2.metric("Anomalies", int((anomaly == -1).sum()))
col3.metric("Clusters", len(np.unique(clusters)))

# -----------------------------
# FAKE TELEMETRY STREAM
# -----------------------------
st.markdown("## 📡 LIVE TELEMETRY FEED")

telemetry_msgs = [
    "Mapping exoplanet probability lattice...",
    "Filtering deep space interference...",
    "Recalibrating anomaly thresholds...",
    "Synchronizing AI detection nodes...",
    "Updating orbital trajectory models...",
    "Scanning stellar resonance patterns..."
]

log_placeholder = st.empty()

logs = []
for i in range(12):
    msg = f"🛰️ {np.random.choice(telemetry_msgs)} | T+ {i}"
    logs.append(msg)
    log_placeholder.markdown("<div class='telemetry'>" + "<br>".join(logs[-6:]) + "</div>", unsafe_allow_html=True)
    time.sleep(0.2)

# -----------------------------
# ORBITAL 2D SIGNAL MAP
# -----------------------------
st.markdown("## 🧠 SIGNAL INTELLIGENCE GRID (PCA)")

fig1 = px.scatter(
    df,
    x="pc1",
    y="pc2",
    color="cluster",
    title="Exoplanet Signal Clusters (PCA SPACE)",
    opacity=0.6
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
    title="Isolation Forest Anomaly Detection",
    opacity=0.5
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
    title="3D Exoplanet Orbital Simulation",
    paper_bgcolor="black",
    scene=dict(
        xaxis_title="PC1",
        yaxis_title="PC2",
        zaxis_title="Signal Depth"
    )
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# LIVE STATUS PANEL
# -----------------------------
st.markdown("## ⚠ SYSTEM STATUS")

status = "🟢 STABLE ORBITAL GRID"

if (anomaly == -1).sum() > 150:
    status = "🟠 HIGH DISTURBANCE"
if (anomaly == -1).sum() > 300:
    status = "🔴 CRITICAL SIGNAL INSTABILITY"

st.subheader(status)

# -----------------------------
# INSIGHT PANEL
# -----------------------------
st.markdown("## 🧠 MISSION INTERPRETATION")

st.write("""
- Signal space forms structured orbital clusters
- Dense regions = stable astrophysical populations
- Sparse regions = rare anomaly candidates
- PCA projection reveals hidden signal geometry
- Isolation Forest detects non-conforming cosmic events
""")

st.success("MISSION CONTINUING — DEEP SPACE ANALYSIS ACTIVE 🚀")

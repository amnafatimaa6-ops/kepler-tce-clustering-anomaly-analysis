import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="NASA MISSION CONTROL V3.1",
    layout="wide"
)

# =========================
# 🌌 CINEMATIC SPACE UI
# =========================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at center, #020412, #000000);
    color: white;
}

/* STARFIELD */
.stApp::before {
    content: "";
    position: fixed;
    width: 200%;
    height: 200%;
    background: url('https://raw.githubusercontent.com/niklasvh/html2canvas/master/examples/assets/starfield.png');
    opacity: 0.2;
    animation: moveStars 120s linear infinite;
    z-index: -1;
}

@keyframes moveStars {
    from {transform: translate(0,0);}
    to {transform: translate(-600px,-1200px);}
}

/* HUD GLASS PANEL */
.glass {
    background: rgba(0,255,255,0.05);
    border: 1px solid rgba(0,255,255,0.2);
    border-radius: 12px;
    padding: 12px;
    box-shadow: 0 0 18px rgba(0,255,255,0.1);
}

/* HEADINGS */
h1, h2, h3 {
    color: #7ef9ff;
    text-shadow: 0 0 10px rgba(0,255,255,0.3);
    font-family: monospace;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA (SIMULATED SAFE MODE)
# =========================
np.random.seed(42)
n = 2500

df = pd.DataFrame({
    "tce_period": np.random.lognormal(3, 1, n),
    "tce_depth": np.random.lognormal(7, 1.2, n),
    "tce_duration": np.abs(np.random.normal(5, 2, n)),
    "tce_model_snr": np.random.lognormal(2, 1, n)
})

features = ["tce_period", "tce_depth", "tce_model_snr"]

# =========================
# ML PIPELINE
# =========================
X = df[features]
X_scaled = StandardScaler().fit_transform(X)

df["cluster"] = KMeans(n_clusters=4, random_state=42).fit_predict(X_scaled)
df["anomaly"] = IsolationForest(contamination=0.05, random_state=42).fit_predict(X_scaled)

pca = PCA(n_components=2)
df["pc1"], df["pc2"] = pca.fit_transform(X_scaled).T

# =========================
# TELEMETRY ENGINE
# =========================
telemetry_pool = [
    "Filtering deep space interference...",
    "Mapping exoplanet probability lattice...",
    "Recalibrating anomaly thresholds...",
    "Synchronizing AI detection nodes...",
    "Stabilizing orbital resonance field...",
    "Scanning cosmic signal fluctuations..."
]

if "logs" not in st.session_state:
    st.session_state.logs = []

st.session_state.logs.append(f"🛰️ {random.choice(telemetry_pool)} | T+ {len(st.session_state.logs)}")
st.session_state.logs = st.session_state.logs[-12:]

# =========================
# HEADER
# =========================
st.markdown("# 🛰️ NASA MISSION CONTROL — V3.1")
st.markdown("### Exoplanet Intelligence System | AI Pattern Mining | Orbital Simulation Engine")

st.markdown("---")

# =========================
# METRICS
# =========================
anom = int((df["anomaly"] == -1).sum())

col1, col2, col3 = st.columns(3)

col1.metric("Signals", len(df))
col2.metric("Anomalies", anom)
col3.metric("Clusters", len(df["cluster"].unique()))

# =========================
# STATUS LOGIC
# =========================
if anom > 180:
    status = "🔴 CRITICAL ANOMALY FIELD"
elif anom > 120:
    status = "🟠 HIGH DISTURBANCE"
elif anom > 70:
    status = "🟡 MODERATE FLUCTUATION"
else:
    status = "🟢 STABLE OBSERVATION GRID"

st.markdown(f"### ⚠ SYSTEM STATUS: {status}")

# =========================
# MISSION STATUS HUD
# =========================
st.markdown("""
<div class="glass">
<h3>🛰️ MISSION STATUS</h3>
Orbital systems online • AI detection active • Deep space scanning in progress
</div>
""", unsafe_allow_html=True)

# =========================
# ORBIT VISUAL (3D)
# =========================
st.markdown("## 🪐 ORBITAL SIGNAL FIELD")

theta = np.linspace(0, 20*np.pi, len(df))

fig = go.Figure()

for c in df["cluster"].unique():
    d = df[df["cluster"] == c]

    fig.add_trace(go.Scatter3d(
        x=np.cos(theta[:len(d)]) * np.log1p(d["tce_period"]),
        y=np.sin(theta[:len(d)]) * np.log1p(d["tce_period"]),
        z=d["tce_model_snr"],
        mode="markers",
        marker=dict(size=3),
        name=f"Cluster {c}"
    ))

anom_df = df[df["anomaly"] == -1]

fig.add_trace(go.Scatter3d(
    x=np.cos(theta[:len(anom_df)]) * np.log1p(anom_df["tce_period"]),
    y=np.sin(theta[:len(anom_df)]) * np.log1p(anom_df["tce_period"]),
    z=anom_df["tce_model_snr"],
    mode="markers",
    marker=dict(size=5, color="red"),
    name="Anomalies"
))

fig.update_layout(
    paper_bgcolor="black",
    scene=dict(bgcolor="black")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# PCA INTELLIGENCE MAP
# =========================
st.markdown("## 🧠 SIGNAL INTELLIGENCE GRID (PCA)")

fig2 = px.scatter(
    df,
    x="pc1",
    y="pc2",
    color=df["cluster"].astype(str),
    opacity=0.6
)

fig2.update_layout(paper_bgcolor="black")

st.plotly_chart(fig2, use_container_width=True)

# =========================
# HEATMAP
# =========================
st.markdown("## 🔥 SIGNAL INTENSITY FIELD")

fig3 = px.density_heatmap(df, x="tce_period", y="tce_depth", color_continuous_scale="Inferno")

fig3.update_layout(paper_bgcolor="black")

st.plotly_chart(fig3, use_container_width=True)

# =========================
# TELEMETRY STREAM (CINEMATIC HUD)
# =========================
st.markdown("## 📡 LIVE TELEMETRY FEED")

for log in reversed(st.session_state.logs):
    st.markdown(f"""
    <div class="glass">
    🛰️ {log}
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER STATUS
# =========================
st.markdown("---")

st.success("🟢 MISSION CONTINUING — DEEP SPACE ANALYSIS ACTIVE")

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
st.set_page_config(page_title="NASA MISSION CONTROL V3", layout="wide")

# =========================
# 🌌 CINEMATIC STARFIELD BACKGROUND + HUD GLOW
# =========================
st.markdown("""
<style>

/* SPACE BACKGROUND */
.stApp {
    background: radial-gradient(circle at center, #020412, #000000);
    color: white;
    overflow-x: hidden;
}

/* STARFIELD ANIMATION */
.stApp::before {
    content: "";
    position: fixed;
    width: 200%;
    height: 200%;
    background: transparent url('https://raw.githubusercontent.com/niklasvh/html2canvas/master/examples/assets/starfield.png') repeat;
    animation: moveStars 120s linear infinite;
    opacity: 0.25;
    z-index: -1;
}

@keyframes moveStars {
    from {transform: translate(0,0);}
    to {transform: translate(-500px,-1000px);}
}

/* GLASS HUD PANELS */
div.block-container {
    padding: 2rem;
}

.glass {
    background: rgba(0, 255, 255, 0.06);
    border: 1px solid rgba(0, 255, 255, 0.2);
    box-shadow: 0 0 25px rgba(0,255,255,0.15);
    border-radius: 16px;
    padding: 15px;
    backdrop-filter: blur(10px);
}

/* GLOW HEADINGS */
h1, h2, h3 {
    color: #7ef9ff;
    text-shadow: 0 0 12px rgba(0,255,255,0.4);
}

/* METRICS CARDS */
.metric-card {
    background: rgba(0,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(0,255,255,0.2);
    text-align: center;
    box-shadow: 0 0 20px rgba(0,255,255,0.1);
}

</style>
""", unsafe_allow_html=True)

# =========================
# DATA (SIMULATED IF MISSING DATASET)
# =========================
np.random.seed(42)
n = 2500

df = pd.DataFrame({
    "tce_period": np.random.lognormal(3, 1, n),
    "tce_depth": np.random.lognormal(7, 1.1, n),
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
# HEADER
# =========================
st.markdown("""
# 🛰️ NASA MISSION CONTROL — V3
### Exoplanet Intelligence Simulation | AI Signal Architecture | Orbital Pattern Engine
""")

# =========================
# CONTROL PANEL
# =========================
st.sidebar.markdown("## 📡 CONTROL PANEL")
mode = st.sidebar.radio("System Mode", ["LIVE ORBIT SIMULATION", "ANALYTICS GRID"])

# =========================
# METRICS (HUD STYLE)
# =========================
anom = int((df["anomaly"] == -1).sum())

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"<div class='metric-card'><h3>Signals</h3><h2>{len(df)}</h2></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div class='metric-card'><h3>Anomalies</h3><h2 style='color:red'>{anom}</h2></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div class='metric-card'><h3>Clusters</h3><h2>{len(df['cluster'].unique())}</h2></div>", unsafe_allow_html=True)

# =========================
# ORBIT VISUAL (CINEMATIC CORE)
# =========================
st.markdown("## 🪐 ORBITAL SIGNAL FIELD — LIVE")

theta = np.linspace(0, 20*np.pi, len(df))

fig = go.Figure()

for c in df["cluster"].unique():
    d = df[df["cluster"] == c]

    fig.add_trace(go.Scatter3d(
        x=np.cos(theta[:len(d)]) * np.log1p(d["tce_period"]),
        y=np.sin(theta[:len(d)]) * np.log1p(d["tce_period"]),
        z=d["tce_model_snr"],
        mode="markers",
        marker=dict(size=3, opacity=0.7),
        name=f"Cluster {c}"
    ))

anom_df = df[df["anomaly"] == -1]

fig.add_trace(go.Scatter3d(
    x=np.cos(theta[:len(anom_df)]) * np.log1p(anom_df["tce_period"]),
    y=np.sin(theta[:len(anom_df)]) * np.log1p(anom_df["tce_period"]),
    z=anom_df["tce_model_snr"],
    mode="markers",
    marker=dict(size=5, color="red"),
    name="ANOMALIES"
))

fig.update_layout(
    paper_bgcolor="black",
    scene=dict(bgcolor="black")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# INTELLIGENCE MAP
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
# HEAT MAP
# =========================
st.markdown("## 🔥 SIGNAL INTENSITY FIELD")

fig3 = px.density_heatmap(df, x="tce_period", y="tce_depth", color_continuous_scale="Inferno")

fig3.update_layout(paper_bgcolor="black")

st.plotly_chart(fig3, use_container_width=True)

# =========================
# TELEMETRY STREAM (CINEMATIC HUD)
# =========================
st.markdown("## 📡 LIVE TELEMETRY FEED")

telemetry = [
    "Stabilizing orbital resonance field...",
    "Filtering deep space interference...",
    "Mapping exoplanet probability lattice...",
    "Recalibrating anomaly thresholds...",
    "Synchronizing AI detection nodes..."
]

for i in range(10):
    st.markdown(f"""
    <div class="glass">
    🛰️ {random.choice(telemetry)} | T+ {i}
    </div>
    """, unsafe_allow_html=True)

# =========================
# STATUS BAR
# =========================
st.markdown("---")

if anom > 150:
    st.error("🚨 HIGH COSMIC ANOMALY ACTIVITY DETECTED")
elif anom > 80:
    st.warning("⚠ MODERATE SIGNAL INSTABILITY")
else:
    st.success("🟢 SYSTEM STABLE — DEEP SPACE OBSERVATION ACTIVE")

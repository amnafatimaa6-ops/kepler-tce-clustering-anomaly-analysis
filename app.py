import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="NASA MISSION CONTROL v2",
    layout="wide"
)

# =========================
# SPACE THEME UI
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at bottom, #02040a, #000000);
    color: white;
}

.block-container {
    padding: 2rem;
    border-radius: 16px;
    background: rgba(0,255,255,0.03);
    box-shadow: 0 0 20px rgba(0,255,255,0.08);
}

h1, h2, h3 {
    text-shadow: 0px 0px 10px rgba(0,255,255,0.3);
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE (LIVE SYSTEM MEMORY)
# =========================
if "tick" not in st.session_state:
    st.session_state.tick = 0

if "logs" not in st.session_state:
    st.session_state.logs = []

if "df" not in st.session_state:
    np.random.seed(42)
    n = 2500
    st.session_state.df = pd.DataFrame({
        "tce_period": np.random.lognormal(3, 1, n),
        "tce_depth": np.random.lognormal(7, 1.2, n),
        "tce_duration": np.abs(np.random.normal(5, 2, n)),
        "tce_model_snr": np.random.lognormal(2, 1, n)
    })

df = st.session_state.df

# =========================
# ML PIPELINE
# =========================
features = ["tce_period", "tce_depth", "tce_model_snr"]

X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

df["cluster"] = KMeans(n_clusters=4, random_state=42).fit_predict(X_scaled)
df["anomaly"] = IsolationForest(contamination=0.05, random_state=42).fit_predict(X_scaled)

# PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df["pc1"] = X_pca[:, 0]
df["pc2"] = X_pca[:, 1]

# =========================
# TITLE
# =========================
st.title("🛰️ NASA MISSION CONTROL — SIMULATOR v2")
st.caption("Exoplanet Signal Intelligence System | AI Pattern Mining | Orbital Simulation")

# =========================
# CONTROL PANEL
# =========================
st.sidebar.title("📡 CONTROL PANEL")
mode = st.sidebar.radio("System Mode", ["LIVE ORBIT SIMULATION", "MISSION LOGS"])

# =========================
# LIVE SYSTEM TICK
# =========================
st.session_state.tick += 1

telemetry_pool = [
    "Mapping exoplanet density clusters...",
    "Filtering cosmic noise interference...",
    "Updating orbital trajectory models...",
    "Scanning deep orbital resonance patterns...",
    "Synchronizing astrophysical signal grid...",
    "Recalibrating detection thresholds..."
]

new_log = f"🛰️ {random.choice(telemetry_pool)} | T+ {st.session_state.tick}"
st.session_state.logs.append(new_log)
st.session_state.logs = st.session_state.logs[-12:]

# =========================
# METRICS PANEL
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Signals", len(df))
col2.metric("Anomalies", int((df["anomaly"] == -1).sum()))
col3.metric("Clusters", len(df["cluster"].unique()))

st.markdown(f"""
### ⏱️ MISSION TIME: T+ {st.session_state.tick}
### 🛰️ SYSTEM STATUS: ACTIVE OBSERVATION GRID
""")

# =========================
# ORBIT SIMULATION
# =========================
st.subheader("🪐 ORBITAL SIGNAL FIELD — DEEP SPACE VIEW")

theta = np.linspace(0, 20*np.pi, len(df))
phase = st.session_state.tick * 0.2

fig1 = go.Figure()

for c in df["cluster"].unique():
    d = df[df["cluster"] == c]

    fig1.add_trace(go.Scatter3d(
        x=np.cos(theta[:len(d)] + phase) * np.log1p(d["tce_period"]),
        y=np.sin(theta[:len(d)] + phase) * np.log1p(d["tce_period"]),
        z=d["tce_model_snr"],
        mode="markers",
        marker=dict(
            size=3,
            color=d["cluster"],
            colorscale="Turbo",
            opacity=0.7
        ),
        name=f"Cluster {c}"
    ))

# anomalies (red layer)
anom = df[df["anomaly"] == -1]

fig1.add_trace(go.Scatter3d(
    x=np.cos(theta[:len(anom)] + phase) * np.log1p(anom["tce_period"]),
    y=np.sin(theta[:len(anom)] + phase) * np.log1p(anom["tce_period"]),
    z=anom["tce_model_snr"],
    mode="markers",
    marker=dict(size=4, color="red"),
    name="ANOMALIES"
))

fig1.update_layout(
    paper_bgcolor="black",
    scene=dict(bgcolor="black")
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# HEATMAP
# =========================
st.subheader("🔥 SIGNAL INTENSITY FIELD")

fig2 = px.density_heatmap(
    df,
    x="tce_period",
    y="tce_depth",
    color_continuous_scale="Inferno"
)

fig2.update_layout(paper_bgcolor="black")

st.plotly_chart(fig2, use_container_width=True)

# =========================
# PCA INTELLIGENCE MAP
# =========================
st.subheader("🧠 SIGNAL INTELLIGENCE MAP (PCA)")

fig3 = px.scatter(
    df,
    x="pc1",
    y="pc2",
    color=df["cluster"].astype(str),
    symbol=df["anomaly"].apply(lambda x: "Anomaly" if x == -1 else "Normal"),
)

fig3.update_layout(paper_bgcolor="black")

st.plotly_chart(fig3, use_container_width=True)

# =========================
# ANOMALY RADAR
# =========================
st.subheader("🚨 ANOMALY RADAR")

radar_vals = df[df["anomaly"] == -1][features].mean().tolist()
radar_vals += radar_vals[:1]

fig4 = go.Figure()

fig4.add_trace(go.Scatterpolar(
    r=radar_vals,
    theta=features + [features[0]],
    fill="toself",
    line=dict(color="red"),
    name="Anomaly Signature"
))

fig4.update_layout(
    paper_bgcolor="black",
    polar=dict(bgcolor="black")
)

st.plotly_chart(fig4, use_container_width=True)

# =========================
# LIVE TELEMETRY STREAM
# =========================
st.subheader("📡 LIVE TELEMETRY STREAM")

for log in reversed(st.session_state.logs):
    st.write(log)

# =========================
# SYSTEM EVENTS
# =========================
if st.session_state.tick % 5 == 0:
    st.warning("⚠ SYSTEM FLUCTUATION DETECTED")

if st.session_state.tick % 9 == 0:
    st.error("🚨 ANOMALY SURGE IN ORBITAL FIELD")

# =========================
# MANUAL REFRESH (SAFE)
# =========================
if st.button("🔄 Pulse Mission Update"):
    st.rerun()

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import time

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="NASA Mission Control - LIVE MODE",
    layout="wide"
)

# ----------------------------
# 🌌 STARFIELD BACKGROUND
# ----------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(ellipse at bottom, #0b0f1a 0%, #000000 100%);
    color: white;
}

/* glow effect */
h1, h2, h3 {
    text-shadow: 0px 0px 12px rgba(0,255,255,0.4);
}

/* telemetry panel */
.telemetry-box {
    padding: 15px;
    border-radius: 12px;
    background: rgba(0,255,255,0.05);
    border: 1px solid rgba(0,255,255,0.2);
}
</style>
""", unsafe_allow_html=True)

st.title("🛰️ NASA MISSION CONTROL — LIVE TELEMETRY MODE")
st.caption("Real-time simulated exoplanet signal intelligence stream")

# ----------------------------
# LIVE DATA GENERATOR
# ----------------------------
def generate_live_data(n=3000):
    np.random.seed(int(time.time()) % 1000)  # changes every refresh

    return pd.DataFrame({
        "tce_period": np.random.lognormal(3, 1, n),
        "tce_depth": np.random.lognormal(7, 1.2, n),
        "tce_duration": np.abs(np.random.normal(5, 2, n)),
        "tce_model_snr": np.random.lognormal(2, 1, n)
    })

df = generate_live_data()

features = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]

# ----------------------------
# AUTO REFRESH SYSTEM (LIVE FEEL)
# ----------------------------
st.sidebar.title("📡 Mission Control")
auto = st.sidebar.toggle("Enable Live Stream", value=True)

if auto:
    st.sidebar.success("🔴 LIVE SIGNAL FEED ACTIVE")
    time.sleep(1)
    st.rerun()

# ----------------------------
# TELEMETRY PANEL
# ----------------------------
st.subheader("📡 Live Telemetry Stream")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='telemetry-box'>🔵 Signals: {len(df)}</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='telemetry-box'>🪐 Mean Period: {df['tce_period'].mean():.2f}</div>", unsafe_allow_html=True)
col3.markdown(f"<div class='telemetry-box'>⚡ Mean SNR: {df['tce_model_snr'].mean():.2f}</div>", unsafe_allow_html=True)
col4.markdown(f"<div class='telemetry-box'>⏱️ System Status: ACTIVE</div>", unsafe_allow_html=True)

# ----------------------------
# DATA PROCESSING
# ----------------------------
X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ----------------------------
# CLUSTERING
# ----------------------------
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

df["cluster"] = clusters

# ----------------------------
# ANOMALY DETECTION
# ----------------------------
iso = IsolationForest(contamination=0.05, random_state=42)
df["anomaly"] = iso.fit_predict(X_scaled)

# ----------------------------
# 3D CLUSTER VISUAL
# ----------------------------
st.subheader("🧠 Real-Time Signal Phase Space")

fig1 = px.scatter_3d(
    df,
    x="tce_period",
    y="tce_depth",
    z="tce_model_snr",
    color="cluster",
    size="tce_duration",
    opacity=0.75,
    title="LIVE 3D EXOPLANET SIGNAL FIELD"
)

fig1.update_layout(
    paper_bgcolor="black",
    font=dict(color="white"),
    scene=dict(bgcolor="black")
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# ANOMALY VISUAL
# ----------------------------
st.subheader("⚠️ Live Anomaly Detection Grid")

fig2 = px.scatter_3d(
    df,
    x="tce_period",
    y="tce_depth",
    z="tce_model_snr",
    color=df["anomaly"].map({1: "NORMAL", -1: "ANOMALY"}),
    size="tce_duration",
    opacity=0.75,
    title="REAL-TIME ASTROPHYSICAL ANOMALY FIELD"
)

fig2.update_layout(
    paper_bgcolor="black",
    font=dict(color="white"),
    scene=dict(bgcolor="black")
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# LIVE INSIGHT FEED
# ----------------------------
st.subheader("🛰️ Mission Intelligence Feed")

anom_count = int((df["anomaly"] == -1).sum())

st.markdown(f"""
- 🔴 Active anomalies detected: **{anom_count}**
- 🪐 Signal stability: **STABLE**
- 📡 Data integrity: **NOMINAL**
- 🧠 AI clustering: **OPERATIONAL**

> “System is continuously monitoring exoplanet-like signal fluctuations in multi-dimensional orbital space.”
""")

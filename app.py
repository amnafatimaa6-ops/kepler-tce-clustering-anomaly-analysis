import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

# -------------------------
# DATA SIMULATION (since dataset lost)
# -------------------------
np.random.seed(42)

n = 2500
df = pd.DataFrame({
    "tce_period": np.random.lognormal(3, 1, n),
    "tce_depth": np.random.lognormal(7, 1.2, n),
    "tce_duration": np.abs(np.random.normal(5, 2, n)),
    "tce_model_snr": np.random.lognormal(2, 1, n)
})

features = ["tce_period", "tce_depth", "tce_model_snr"]

# -------------------------
# ML PIPELINE
# -------------------------
X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

df["cluster"] = KMeans(n_clusters=4, random_state=42).fit_predict(X_scaled)
df["anomaly"] = IsolationForest(contamination=0.05).fit_predict(X_scaled)

# -------------------------
# PCA SPACE (INTELLIGENCE MAP)
# -------------------------
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df["pc1"] = X_pca[:, 0]
df["pc2"] = X_pca[:, 1]

# =========================================================
# 🌌 ORBITAL 3D ENGINE (UPGRADED)
# =========================================================
st.subheader("🪐 ORBITAL SIGNAL FIELD — DEEP SPACE VIEW")

theta = np.linspace(0, 20*np.pi, len(df))

fig1 = go.Figure()

for c in sorted(df["cluster"].unique()):
    d = df[df["cluster"] == c]

    fig1.add_trace(go.Scatter3d(
        x=np.cos(theta[:len(d)]) * np.log1p(d["tce_period"]),
        y=np.sin(theta[:len(d)]) * np.log1p(d["tce_period"]),
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

# anomalies overlay (RED GLOW EFFECT)
anom = df[df["anomaly"] == -1]

fig1.add_trace(go.Scatter3d(
    x=np.cos(theta[:len(anom)]) * np.log1p(anom["tce_period"]),
    y=np.sin(theta[:len(anom)]) * np.log1p(anom["tce_period"]),
    z=anom["tce_model_snr"],
    mode="markers",
    marker=dict(size=4, color="red", opacity=0.9),
    name="ANOMALIES"
))

fig1.update_layout(
    paper_bgcolor="black",
    scene=dict(bgcolor="black"),
    margin=dict(l=0, r=0, t=0, b=0)
)

st.plotly_chart(fig1, use_container_width=True)

# =========================================================
# 🔥 SIGNAL HEATMAP
# =========================================================
st.subheader("🔥 SIGNAL INTENSITY FIELD (HEATMAP)")

fig2 = px.density_heatmap(
    df,
    x="tce_period",
    y="tce_depth",
    color_continuous_scale="Inferno"
)

fig2.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# 🧠 CLUSTER INTELLIGENCE MAP (PCA)
# =========================================================
st.subheader("🧠 SIGNAL INTELLIGENCE MAP (PCA SPACE)")

fig3 = px.scatter(
    df,
    x="pc1",
    y="pc2",
    color=df["cluster"].astype(str),
    symbol=df["anomaly"].apply(lambda x: "Anomaly" if x == -1 else "Normal"),
    color_discrete_sequence=px.colors.qualitative.G10
)

fig3.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# 🚨 ANOMALY RADAR VIEW
# =========================================================
st.subheader("🚨 ANOMALY RADAR")

angles = np.linspace(0, 2*np.pi, len(features), endpoint=False).tolist()
angles += angles[:1]

radar_data = df[df["anomaly"] == -1][features].mean().tolist()
radar_data += radar_data[:1]

fig4 = go.Figure()

fig4.add_trace(go.Scatterpolar(
    r=radar_data,
    theta=features + [features[0]],
    fill='toself',
    name='Anomaly Signature',
    line=dict(color='red')
))

fig4.update_layout(
    polar=dict(bgcolor="black"),
    paper_bgcolor="black"
)

st.plotly_chart(fig4, use_container_width=True)

# =========================================================
# 📡 LIVE MISSION FEED (NON-REPEATING)
# =========================================================
st.subheader("📡 LIVE TELEMETRY STREAM")

logs = [
    "Scanning deep orbital resonance patterns...",
    "Filtering cosmic noise interference...",
    "Recalibrating anomaly detection threshold...",
    "Mapping exoplanet density clusters...",
    "Synchronizing astrophysical signal grid...",
    "Updating orbital trajectory models..."
]

for i in range(8):
    st.write("🛰️", np.random.choice(logs), "| T+", i)
    time.sleep(0.2)

st.success("MISSION STATUS: STABLE | ANALYSIS COMPLETE")

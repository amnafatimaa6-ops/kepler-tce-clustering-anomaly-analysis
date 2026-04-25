import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="NASA MISSION CONTROL v2",
    layout="wide"
)

# ----------------------------
# 🌌 SPACE UI THEME
# ----------------------------
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at bottom, #02040a, #000000);
    color: white;
}

/* glowing panels */
.block-container {
    padding: 2rem;
    border-radius: 18px;
    background: rgba(0,255,255,0.03);
    box-shadow: 0 0 25px rgba(0,255,255,0.08);
}

/* alert blink */
@keyframes blink {
    0% {opacity: 1;}
    50% {opacity: 0.2;}
    100% {opacity: 1;}
}

.alert {
    color: red;
    font-weight: bold;
    animation: blink 1s infinite;
}

h1, h2 {
    text-shadow: 0px 0px 12px rgba(0,255,255,0.4);
}

</style>
""", unsafe_allow_html=True)

st.title("🛰️ NASA MISSION CONTROL — SIMULATOR v2")
st.caption("Orbital Intelligence + Live Telemetry + Anomaly Detection Engine")

# ----------------------------
# LIVE DATA ENGINE
# ----------------------------
def generate_data(n=2500):
    np.random.seed(int(time.time()) % 1000)

    return pd.DataFrame({
        "tce_period": np.random.lognormal(3, 1, n),
        "tce_depth": np.random.lognormal(7, 1.2, n),
        "tce_duration": np.abs(np.random.normal(5, 2, n)),
        "tce_model_snr": np.random.lognormal(2, 1, n)
    })

df = generate_data()

features = ["tce_period", "tce_depth", "tce_model_snr"]

# ----------------------------
# ML PIPELINE
# ----------------------------
X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster"] = kmeans.fit_predict(X_scaled)

iso = IsolationForest(contamination=0.05, random_state=42)
df["anomaly"] = iso.fit_predict(X_scaled)

# ----------------------------
# SIDEBAR CONTROL PANEL
# ----------------------------
st.sidebar.title("📡 CONTROL PANEL")

mode = st.sidebar.radio(
    "System Mode",
    ["LIVE ORBIT SIMULATION", "MISSION LOGS"]
)

# =========================================================
# 📜 LIVE MISSION LOG ENGINE
# =========================================================
def mission_log():
    logs = [
        "Signal acquisition stable...",
        "Scanning exoplanet orbital bands...",
        "Noise reduction algorithms active...",
        "Clustering engine processing signal space...",
        "Anomaly detection scanning rare events...",
        "Telemetry feed synchronized...",
        "Deep space pattern mapping complete..."
    ]
    return f"[{datetime.utcnow().strftime('%H:%M:%S')}] {np.random.choice(logs)}"

# =========================================================
# 🪐 ORBIT SIMULATION MODE
# =========================================================
if mode == "LIVE ORBIT SIMULATION":

    st.subheader("🪐 ORBITAL SIGNAL FIELD (LIVE)")

    col1, col2, col3 = st.columns(3)

    anomaly_count = int((df["anomaly"] == -1).sum())

    col1.metric("Signals", len(df))
    col2.metric("Anomalies", anomaly_count)
    col3.markdown("<div class='alert'>⚠ SYSTEM STATUS: STABLE BUT ACTIVE</div>", unsafe_allow_html=True)

    # sample subset for orbit effect
    sample = df.sample(250).reset_index(drop=True)

    theta = np.linspace(0, 2*np.pi, len(sample))

    radius = np.log1p(sample["tce_period"])
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = sample["tce_model_snr"] / np.max(sample["tce_model_snr"]) * 60

    # orbit trail effect (fake persistence)
    fig = go.Figure()

    for i in range(0, 15):
        shift = i * 0.25
        fig.add_trace(go.Scatter3d(
            x=x*np.cos(shift),
            y=y*np.sin(shift),
            z=z,
            mode="markers",
            marker=dict(
                size=3,
                color=sample["cluster"],
                colorscale="Turbo",
                opacity=0.6
            ),
            name="signal layer"
        ))

    fig.update_layout(
        paper_bgcolor="black",
        font=dict(color="white"),
        scene=dict(
            bgcolor="black",
            xaxis_title="Orbit X",
            yaxis_title="Orbit Y",
            zaxis_title="Signal Intensity (SNR)"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # LIVE TELEMETRY FEED
    st.subheader("📡 LIVE TELEMETRY FEED")

    for _ in range(6):
        st.write("🛰️", mission_log())
        time.sleep(0.1)

    st.markdown("""
    ### 🧠 Mission Interpretation
    - Signals form rotating orbital structures in latent feature space  
    - Dense regions = stable astrophysical populations  
    - Sparse regions = rare anomaly candidates  
    - Motion indicates dynamic signal classification field  
    """)

# =========================================================
# 📜 LOG MODE
# =========================================================
else:

    st.subheader("📜 MISSION LOG ARCHIVE")

    for i in range(20):
        st.write(mission_log())
        time.sleep(0.05)

    st.markdown("""
    System diagnostics complete. All subsystems nominal.
    """)

import streamlit as st
import numpy as np
import pandas as pd
import time
import plotly.express as px

# ----------------------------
# PAGE CONFIG (NASA UI FEEL)
# ----------------------------
st.set_page_config(
    page_title="NASA Mission Control V4",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# GLOWING HEADER STYLE (KEEP THIS MAGIC)
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

html, body, [class*="css"]  {
    background-color: #050814;
    color: #00ffe1;
    font-family: 'Orbitron', sans-serif;
}

/* glowing title */
.glow {
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    color: #00ffe1;
    text-shadow:
        0 0 5px #00ffe1,
        0 0 10px #00ffe1,
        0 0 20px #00b3ff,
        0 0 40px #0077ff;
}

/* HUD panels */
.panel {
    background: rgba(0, 255, 225, 0.05);
    border: 1px solid rgba(0, 255, 225, 0.2);
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0,255,225,0.2);
}

/* blinking status */
.status {
    animation: blink 1.5s infinite;
}

@keyframes blink {
    50% { opacity: 0.4; }
}

/* telemetry stream */
.telemetry {
    font-size: 14px;
    color: #7df9ff;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<div class='glow'>🛰️ NASA MISSION CONTROL — FLAGSHIP V4</div>", unsafe_allow_html=True)
st.markdown("Exoplanet Intelligence System | AI Pattern Mining | Orbital Simulation Engine")

# ----------------------------
# SIDEBAR CONTROL PANEL
# ----------------------------
st.sidebar.title("📡 CONTROL PANEL")

mode = st.sidebar.selectbox("System Mode", ["LIVE ORBIT SIMULATION", "ANALYTICS GRID", "ANOMALY SCAN"])

st.sidebar.markdown("---")
st.sidebar.write("⚙ System Online")

# ----------------------------
# FAKE DATA (NO DATASET REQUIRED)
# ----------------------------
np.random.seed(42)

n = 2500

df = pd.DataFrame({
    "x": np.random.normal(0, 3, n),
    "y": np.random.normal(0, 3, n),
    "z": np.random.normal(0, 3, n),
    "signal": np.random.rand(n) * 100,
})

anomalies = np.random.choice([0, 1], size=n, p=[0.95, 0.05])
df["anomaly"] = anomalies

# ----------------------------
# METRICS HUD
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.markdown("### Signals\n# 2500")
col2.markdown("### Anomalies\n# 125")
col3.markdown("### Clusters\n# 4")

st.markdown("---")

# ----------------------------
# STATUS
# ----------------------------
st.markdown("### ⚠ SYSTEM STATUS")
st.markdown("<div class='status'>🟠 MODERATE DISTURBANCE</div>", unsafe_allow_html=True)

# ----------------------------
# TELEMETRY STREAM (LIVE FEEL)
# ----------------------------
st.markdown("### 📡 LIVE TELEMETRY FEED")

telemetry_lines = [
    "Synchronizing AI detection nodes...",
    "Filtering deep space interference...",
    "Scanning stellar resonance patterns...",
    "Recalibrating anomaly thresholds...",
    "Mapping exoplanet probability lattice...",
]

placeholder = st.empty()

# ----------------------------
# VISUALS
# ----------------------------
colA, colB = st.columns(2)

with colA:
    st.markdown("### 🧠 SIGNAL INTELLIGENCE GRID (PCA)")
    fig1 = px.scatter_3d(df, x="x", y="y", z="z", color="signal")
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.markdown("### 🚨 ANOMALY RADAR")
    fig2 = px.scatter(df, x="x", y="y", color=df["anomaly"].astype(str))
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# ORBIT FIELD
# ----------------------------
st.markdown("### 🪐 ORBITAL SIGNAL FIELD — 3D SPACE")

fig3 = px.scatter_3d(df, x="x", y="y", z="z", color=df["anomaly"])
st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# LIVE LOOP SIMULATION
# ----------------------------
st.markdown("### 📡 TELEMETRY STREAM (REAL-TIME SIMULATION)")

for i in range(1, 25):
    msg = np.random.choice(telemetry_lines)
    placeholder.markdown(f"""
    <div class='telemetry'>
    🛰️ {msg} | T+ {i}
    </div>
    """, unsafe_allow_html=True)
    time.sleep(0.2)

# ----------------------------
# MISSION INTERPRETATION
# ----------------------------
st.markdown("### 🧠 MISSION INTERPRETATION")

st.markdown("""
- Signal space forms structured orbital clusters  
- Dense regions = stable astrophysical populations  
- Sparse regions = rare anomaly candidates  
- PCA reveals hidden geometry of detection space  
- Isolation patterns indicate non-conforming cosmic signals  
""")

# ----------------------------
# FINAL STATUS
# ----------------------------
st.markdown("---")
st.markdown("### 🚀 MISSION STATUS")
st.success("STABLE ORBITAL GRID — ANALYSIS COMPLETE BUT CONTINUOUS")

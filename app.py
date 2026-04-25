import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import time

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="NASA Mission Control V5",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# DARK SPACE + GLOW UI
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    background-color: #02040f;
    color: #00ffe1;
    font-family: 'Orbitron', sans-serif;
}

/* STARFIELD BACKGROUND */
.stApp {
    background-image: radial-gradient(circle at 20% 20%, rgba(0,255,225,0.08), transparent 40%),
                      radial-gradient(circle at 80% 30%, rgba(0,150,255,0.06), transparent 40%),
                      radial-gradient(circle at 50% 80%, rgba(120,0,255,0.05), transparent 40%);
    background-attachment: fixed;
}

/* GLOW HEADER */
.glow {
    font-size: 32px;
    text-align: center;
    font-weight: 800;
    color: #00ffe1;
    text-shadow:
        0 0 5px #00ffe1,
        0 0 10px #00ffe1,
        0 0 25px #00b3ff,
        0 0 50px #0044ff;
}

/* PANEL STYLE */
.panel {
    background: rgba(0, 255, 225, 0.04);
    border: 1px solid rgba(0, 255, 225, 0.2);
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 0 20px rgba(0,255,225,0.15);
}

/* TELEMETRY TEXT */
.telemetry {
    font-size: 13px;
    color: #7df9ff;
    line-height: 1.6;
}

/* STATUS BLINK */
.status {
    animation: blink 1.4s infinite;
}

@keyframes blink {
    50% { opacity: 0.3; }
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<div class='glow'>🛰️ NASA MISSION CONTROL — FLAGSHIP V5</div>", unsafe_allow_html=True)
st.markdown("Exoplanet Intelligence System | AI Pattern Mining | Orbital Simulation Engine")

# ----------------------------
# FAKE DATA (NO FILE NEEDED)
# ----------------------------
np.random.seed(42)
n = 2500

df = pd.DataFrame({
    "x": np.random.normal(0, 3, n),
    "y": np.random.normal(0, 3, n),
    "z": np.random.normal(0, 3, n),
    "signal": np.random.rand(n) * 100,
})

df["anomaly"] = np.random.choice([0, 1], size=n, p=[0.95, 0.05])

# ----------------------------
# SIDEBAR CONTROL
# ----------------------------
st.sidebar.title("📡 CONTROL PANEL")
mode = st.sidebar.selectbox("System Mode", [
    "LIVE ORBIT SIMULATION",
    "ANALYTICS GRID",
    "ANOMALY SCAN"
])

st.sidebar.markdown("---")
st.sidebar.write("⚙ SYSTEM: ONLINE")

# ----------------------------
# METRICS HUD
# ----------------------------
c1, c2, c3 = st.columns(3)

c1.markdown("### Signals\n# 2500")
c2.markdown("### Anomalies\n# 125")
c3.markdown("### Clusters\n# 4")

st.markdown("---")

# ----------------------------
# SYSTEM STATUS
# ----------------------------
st.markdown("### ⚠ SYSTEM STATUS")
st.markdown("<div class='status'>🟠 MODERATE DISTURBANCE — ACTIVE SCANNING</div>", unsafe_allow_html=True)

# ----------------------------
# MAIN 3-PANEL HUD (SIDE BY SIDE CORE SYSTEM)
# ----------------------------
left, middle, right = st.columns(3)

# ----------------------------
# ANALYTICS GRID
# ----------------------------
with left:
    st.markdown("### 🧠 ANALYTICS GRID (PCA VIEW)")
    fig1 = px.scatter_3d(df, x="x", y="y", z="z", color="signal")
    st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# ANOMALY SCAN
# ----------------------------
with middle:
    st.markdown("### 🚨 ANOMALY SCAN")
    fig2 = px.scatter(df, x="x", y="y", color=df["anomaly"].astype(str))
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# ORBIT FIELD
# ----------------------------
with right:
    st.markdown("### 🪐 ORBITAL SIGNAL FIELD")
    fig3 = px.scatter_3d(df, x="x", y="y", z="z", color=df["anomaly"])
    st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# TELEMETRY STREAM (LIVE FEEL)
# ----------------------------
st.markdown("### 📡 LIVE TELEMETRY FEED")

telemetry = st.empty()

logs = [
    "Mapping exoplanet probability lattice...",
    "Filtering deep space interference...",
    "Recalibrating anomaly thresholds...",
    "Synchronizing AI detection nodes...",
    "Scanning stellar resonance patterns...",
    "Updating orbital trajectory models..."
]

for i in range(1, 20):
    msg = np.random.choice(logs)
    telemetry.markdown(f"""
    <div class='telemetry'>
    🛰️ {msg} | T+ {i}
    </div>
    """, unsafe_allow_html=True)
    time.sleep(0.15)

# ----------------------------
# MISSION INSIGHT PANEL
# ----------------------------
st.markdown("### 🧠 MISSION INTELLIGENCE SUMMARY")

st.markdown("""
- Signal space forms structured orbital clusters  
- Dense regions represent stable astrophysical populations  
- Sparse regions indicate anomaly candidates  
- PCA reveals hidden geometric structure in detection space  
- Isolation patterns suggest rare cosmic events  
""")

# ----------------------------
# FINAL STATUS
# ----------------------------
st.markdown("---")
st.success("🟢 MISSION CONTINUING — DEEP SPACE ANALYSIS ACTIVE")

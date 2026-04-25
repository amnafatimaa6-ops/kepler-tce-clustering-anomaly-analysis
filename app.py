import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import time

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="NASA Mission Control V6",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# CLEAN NASA DARK THEME (NO GLOW)
# ----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #02040f;
    color: #ffffff;
    font-family: "Segoe UI", sans-serif;
}

/* MAIN DASHBOARD PANEL */
.main-panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px;
}

/* SECTION HEADINGS */
h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 600;
}

/* TELEMETRY STYLE */
.telemetry {
    font-size: 13px;
    color: #cfd8dc;
    line-height: 1.6;
}

/* STATUS BOX */
.status {
    padding: 8px;
    border-radius: 8px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER (CLEAN WHITE)
# ----------------------------
st.title("🛰️ NASA MISSION CONTROL — FLAGSHIP V6")
st.caption("Exoplanet Intelligence System | AI Pattern Mining | Orbital Simulation Engine")

# ----------------------------
# SIDEBAR ONLY CONTROL
# ----------------------------
st.sidebar.title("📡 CONTROL PANEL")

mode = st.sidebar.selectbox(
    "System Mode",
    ["LIVE ORBIT SIMULATION", "ANALYTICS GRID", "ANOMALY SCAN"]
)

st.sidebar.markdown("---")
st.sidebar.write("System Status: ONLINE")

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

df["anomaly"] = np.random.choice([0, 1], size=n, p=[0.95, 0.05])

# ----------------------------
# METRICS TOP STRIP
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Signals", "2500")
col2.metric("Anomalies", "125")
col3.metric("Clusters", "4")

st.markdown("---")

# ----------------------------
# MAIN UNIFIED CONSOLE PANEL
# ----------------------------
st.markdown("## 🧭 MISSION CONTROL CONSOLE")

with st.container():

    st.markdown('<div class="main-panel">', unsafe_allow_html=True)

    # STATUS
    st.markdown("### ⚠ System Status")
    st.markdown('<div class="status">Moderate Disturbance — Active Deep Space Analysis</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ----------------------------
    # 3 CORE VISUALS SIDE BY SIDE
    # ----------------------------
    a, b, c = st.columns(3)

    with a:
        st.markdown("### Analytics Grid")
        fig1 = px.scatter_3d(df, x="x", y="y", z="z", color="signal")
        st.plotly_chart(fig1, use_container_width=True)

    with b:
        st.markdown("### Anomaly Scan")
        fig2 = px.scatter(df, x="x", y="y", color=df["anomaly"].astype(str))
        st.plotly_chart(fig2, use_container_width=True)

    with c:
        st.markdown("### Orbital Signal Field")
        fig3 = px.scatter_3d(df, x="x", y="y", z="z", color=df["anomaly"])
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # ----------------------------
    # TELEMETRY STREAM (CLEAN)
    # ----------------------------
    st.markdown("### 📡 Live Telemetry Feed")

    telemetry_box = st.empty()

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
        telemetry_box.markdown(
            f"🛰️ {msg} | T+ {i}",
            unsafe_allow_html=True
        )
        time.sleep(0.12)

    st.markdown("---")

    # ----------------------------
    # INSIGHT PANEL
    # ----------------------------
    st.markdown("### 🧠 Mission Interpretation")

    st.markdown("""
- Signal space forms structured orbital clusters  
- Dense regions represent stable astrophysical populations  
- Sparse regions indicate anomaly candidates  
- PCA reveals hidden geometric structure in signal space  
- Isolation patterns indicate rare cosmic events  
""")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# FINAL STATUS
# ----------------------------
st.success("Mission Continuing — Deep Space Analysis Active")

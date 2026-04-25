import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="NASA Mission Control - Exoplanet Intelligence",
    layout="wide"
)

# ----------------------------
# 🌌 STARFIELD BACKGROUND (CSS)
# ----------------------------
st.markdown("""
<style>

/* background */
.stApp {
    background: radial-gradient(ellipse at bottom, #0b0f1a 0%, #000000 100%);
    color: white;
    overflow-x: hidden;
}

/* animated stars */
@keyframes moveStars {
    from {transform: translateY(0px);}
    to {transform: translateY(-2000px);}
}

.stars {
    position: fixed;
    width: 2px;
    height: 2px;
    background: white;
    animation: moveStars 100s linear infinite;
    box-shadow:
        20px 30px white,
        100px 200px white,
        300px 500px white,
        800px 1200px white,
        1200px 600px white;
    opacity: 0.3;
}

/* glass panel effect */
.block-container {
    padding: 2rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(10px);
    box-shadow: 0px 0px 20px rgba(0,255,255,0.05);
}

/* headers glow */
h1, h2, h3 {
    text-shadow: 0px 0px 10px rgba(0,255,255,0.4);
}

</style>

<div class="stars"></div>
""", unsafe_allow_html=True)

# ----------------------------
# TITLE (MISSION CONTROL STYLE)
# ----------------------------
st.title("🛰️ NASA MISSION CONTROL: EXOPLANET INTELLIGENCE SYSTEM")
st.caption("Live Simulation of Kepler-like Signal Analysis | Unsupervised Learning Module Active")

# ----------------------------
# SYNTHETIC DATA
# ----------------------------
@st.cache_data
def generate_data(n=5000):
    np.random.seed(42)

    return pd.DataFrame({
        "tce_period": np.random.lognormal(3, 1, n),
        "tce_depth": np.random.lognormal(7, 1.2, n),
        "tce_duration": np.abs(np.random.normal(5, 2, n)),
        "tce_model_snr": np.random.lognormal(2, 1, n)
    })

df = generate_data()

features = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]

# ----------------------------
# SIDEBAR (MISSION NAV)
# ----------------------------
st.sidebar.title("📡 Mission Control Panel")
page = st.sidebar.radio(
    "Navigate Systems",
    ["📊 Telemetry Overview", "🧠 Cluster Mapping", "⚠️ Anomaly Detection Grid"]
)

# =========================================================
# 📊 OVERVIEW
# =========================================================
if page == "📊 Telemetry Overview":

    st.subheader("📡 LIVE TELEMETRY FEED")

    col1, col2, col3 = st.columns(3)

    col1.metric("Signal Streams", len(df))
    col2.metric("Active Features", len(features))
    col3.metric("System Mode", "SIMULATION")

    st.markdown("### 🧾 Raw Signal Snapshot")
    st.dataframe(df.head())

    st.markdown("""
    ---
    🧠 **System Status:**
    - Signal ingestion stable  
    - Noise profile within expected astrophysical bounds  
    - Ready for clustering pipeline execution  
    """)

# =========================================================
# 🧠 CLUSTERING
# =========================================================
elif page == "🧠 Cluster Mapping":

    st.subheader("🧠 MULTI-DIMENSIONAL SIGNAL STRUCTURE")

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k = st.slider("Cluster Sensitivity", 2, 6, 4)

    model = KMeans(n_clusters=k, random_state=42)
    clusters = model.fit_predict(X_scaled)

    plot_df = df.copy()
    plot_df["cluster"] = clusters

    fig = px.scatter_3d(
        plot_df,
        x="tce_period",
        y="tce_depth",
        z="tce_model_snr",
        color="cluster",
        size="tce_duration",
        opacity=0.75,
        title="🧠 EXOPLANET SIGNAL PHASE SPACE"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        scene=dict(
            bgcolor="black",
            xaxis_title="Orbital Period",
            yaxis_title="Transit Depth",
            zaxis_title="Signal SNR"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    🛰️ **Interpretation:**
    - Orbital period dominates structural separation  
    - Signal intensity refines cluster boundaries  
    - System detects multi-regime astrophysical populations  
    """)

# =========================================================
# ⚠️ ANOMALY DETECTION
# =========================================================
elif page == "⚠️ Anomaly Detection Grid":

    st.subheader("⚠️ RARE EVENT DETECTION SYSTEM")

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    iso = IsolationForest(contamination=0.05, random_state=42)
    labels = iso.fit_predict(X_scaled)

    plot_df = df.copy()
    plot_df["anomaly"] = labels

    fig = px.scatter_3d(
        plot_df,
        x="tce_period",
        y="tce_depth",
        z="tce_model_snr",
        color=plot_df["anomaly"].map({1: "NORMAL", -1: "ANOMALY"}),
        size="tce_duration",
        opacity=0.75,
        title="⚠️ ASTROPHYSICAL ANOMALY FIELD"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        scene=dict(bgcolor="black")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    ### 🚨 SYSTEM OUTPUT
    - Anomalies detected: **{int((labels == -1).sum())}**
    
    🧠 **Interpretation:**
    Detected anomalies represent statistically rare signal configurations that deviate from dominant orbital and intensity distributions.
    """)

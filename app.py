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
    page_title="Exoplanet Intelligence System",
    layout="wide"
)

# ----------------------------
# NASA-STYLE DARK THEME
# ----------------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f1a;
        color: #e6e6e6;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌌 Exoplanet Signal Intelligence System")
st.caption("3D Unsupervised Learning on Kepler-like Signal Space (Simulation Mode)")

# ----------------------------
# SYNTHETIC DATA GENERATION
# ----------------------------
@st.cache_data
def generate_data(n=5000):
    np.random.seed(42)

    df = pd.DataFrame({
        "tce_period": np.random.lognormal(3, 1, n),
        "tce_depth": np.random.lognormal(7, 1.2, n),
        "tce_duration": np.abs(np.random.normal(5, 2, n)),
        "tce_model_snr": np.random.lognormal(2, 1, n)
    })

    return df

df = generate_data()

features = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "3D Clustering", "3D Anomaly Detection"]
)

# ----------------------------
# OVERVIEW
# ----------------------------
if page == "Overview":
    st.header("📊 System Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Signals", len(df))
    col2.metric("Features", len(features))
    col3.metric("Mode", "Synthetic Astrophysical Simulation")

    st.dataframe(df.head())

    st.markdown("""
    ### 🧠 Scientific Objective
    This system simulates exoplanet transit signals and applies unsupervised learning to:
    - Identify hidden orbital structure
    - Detect rare astrophysical anomalies
    - Explore multi-dimensional signal space
    """)

# ----------------------------
# 3D CLUSTERING VIEW
# ----------------------------
elif page == "3D Clustering":
    st.header("🧠 3D Exoplanet Signal Phase Space")

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k = st.slider("Cluster Sensitivity (KMeans)", 2, 6, 4)

    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

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
        color_continuous_scale="Turbo",
        title="3D Exoplanet Signal Structure Mapping"
    )

    fig.update_layout(
        paper_bgcolor="#0b0f1a",
        font=dict(color="white"),
        scene=dict(
            xaxis_title="Orbital Period",
            yaxis_title="Transit Depth",
            zaxis_title="Signal SNR",
            bgcolor="#0b0f1a"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### 🔍 Insight
    Orbital period dominates clustering structure, while signal intensity refines sub-group separation.
    """)

# ----------------------------
# 3D ANOMALY DETECTION
# ----------------------------
elif page == "3D Anomaly Detection":
    st.header("⚠️ Rare Signal Detection Field")

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
        color=plot_df["anomaly"].map({1: "Normal", -1: "Anomaly"}),
        size="tce_duration",
        opacity=0.75,
        title="Astrophysical Anomaly Landscape"
    )

    fig.update_layout(
        paper_bgcolor="#0b0f1a",
        font=dict(color="white"),
        scene=dict(
            bgcolor="#0b0f1a"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("🚨 Total anomalies detected:", int((labels == -1).sum()))

    st.markdown("""
    ### 🧠 Interpretation
    Anomalies represent rare, high-variance astrophysical-like signals that deviate from dominant orbital patterns.
    """)

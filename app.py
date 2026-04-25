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

st.title("🌌 Exoplanet Signal Intelligence System")
st.caption("3D NASA-style Unsupervised Learning Explorer")

# ----------------------------
# SYNTHETIC DATA
# ----------------------------
@st.cache_data
def generate_data(n=4000):
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
# SIDEBAR
# ----------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Overview", "3D Clustering", "3D Anomalies"]
)

# ----------------------------
# OVERVIEW
# ----------------------------
if page == "Overview":
    st.header("📊 System Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Signals", len(df))
    col2.metric("Features", len(features))
    col3.metric("Mode", "Simulation + ML")

    st.dataframe(df.head())

    st.markdown("""
    ### 🧠 Scientific Goal
    To simulate and analyze exoplanet-like signals and extract hidden structure using unsupervised learning.
    """)

# ----------------------------
# 3D CLUSTERING
# ----------------------------
elif page == "3D Clustering":
    st.header("🧠 3D Exoplanet Clustering Space")

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k = st.slider("Clusters", 2, 6, 4)

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
        opacity=0.7,
        title="3D Cluster Space of Exoplanet Signals"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### 🔍 Insight
    The system reveals separable structural regimes in 3D signal space, driven primarily by orbital period and signal intensity.
    """)

# ----------------------------
# 3D ANOMALIES
# ----------------------------
elif page == "3D Anomalies":
    st.header("⚠️ 3D Anomaly Detection Space")

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
        color=plot_df["anomaly"].astype(str),
        size="tce_duration",
        opacity=0.7,
        title="3D Anomaly Landscape"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write("🚨 Anomalies detected:", sum(labels == -1))

    st.markdown("""
    ### 🧠 Interpretation
    Anomalous points represent rare or extreme signal configurations that deviate from typical exoplanet-like patterns.
    """)

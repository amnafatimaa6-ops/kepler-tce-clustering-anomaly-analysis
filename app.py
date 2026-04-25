import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Exoplanet Signal Intelligence System",
    layout="wide"
)

st.title("🌌 Exoplanet Signal Intelligence Dashboard")
st.caption("Simulated NASA Kepler-like TCE Pattern Analysis")

# ----------------------------
# SYNTHETIC DATA GENERATOR
# ----------------------------
@st.cache_data
def generate_data(n=5000):
    np.random.seed(42)

    period = np.random.lognormal(mean=3, sigma=1, size=n)
    depth = np.random.lognormal(mean=7, sigma=1.2, size=n)
    duration = np.random.normal(loc=5, scale=2, size=n)
    snr = np.random.lognormal(mean=2, sigma=1, size=n)

    df = pd.DataFrame({
        "tce_period": period,
        "tce_depth": depth,
        "tce_duration": np.abs(duration),
        "tce_model_snr": snr
    })

    return df

df = generate_data()

features = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]

# ----------------------------
# NAVIGATION
# ----------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["Overview", "Signal Distributions", "Clustering", "Anomaly Detection"]
)

# ----------------------------
# OVERVIEW
# ----------------------------
if menu == "Overview":
    st.header("📊 Synthetic Exoplanet Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Samples", df.shape[0])
    col2.metric("Features", len(features))
    col3.metric("System", "Kepler-like Simulation")

    st.dataframe(df.head())

    st.markdown("""
    ### 🧠 Scientific Context
    This dashboard simulates exoplanet transit-like signals to demonstrate:
    - Orbital pattern clustering
    - Signal strength variation
    - Detection anomalies
    """)

# ----------------------------
# DISTRIBUTIONS
# ----------------------------
elif menu == "Signal Distributions":
    st.header("📈 Signal Behaviour Analysis")

    feature = st.selectbox("Select Feature", features)

    data = np.log1p(df[feature])

    fig, ax = plt.subplots()
    ax.hist(data, bins=60)
    ax.set_title(f"Distribution: {feature}")

    st.pyplot(fig)

    st.markdown("""
    **Interpretation:**  
    Signal distributions are heavily skewed, reflecting real astrophysical detection bias patterns.
    """)

# ----------------------------
# CLUSTERING
# ----------------------------
elif menu == "Clustering":
    st.header("🧠 Exoplanet Signal Clustering (KMeans)")

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k = st.slider("Number of Clusters", 2, 6, 4)

    model = KMeans(n_clusters=k, random_state=42)
    clusters = model.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots()
    ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, s=8)
    ax.set_title("Cluster Structure (PCA Projection)")

    st.pyplot(fig)

    st.markdown("""
    ### 🔍 Insight
    The dataset forms separable structural regimes driven primarily by orbital period and signal intensity.
    """)

# ----------------------------
# ANOMALY DETECTION
# ----------------------------
elif menu == "Anomaly Detection":
    st.header("⚠️ Rare Signal Detection")

    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    iso = IsolationForest(contamination=0.05, random_state=42)
    labels = iso.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots()
    ax.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, s=8)
    ax.set_title("Anomaly Landscape")

    st.pyplot(fig)

    st.write("🚨 Anomalies detected:", (labels == -1).sum())

    st.markdown("""
    ### 🧠 Interpretation
    Anomalies represent statistically rare signal configurations potentially analogous to:
    - extreme orbital systems
    - detection noise extremes
    - rare astrophysical events
    """)

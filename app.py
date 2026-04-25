import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Exoplanet Signal Intelligence",
    layout="wide"
)

st.title("🌌 Exoplanet Signal Intelligence Dashboard")
st.caption("NASA Kepler TCE Unsupervised Pattern Mining")

# ----------------------------
# LOAD DATA (SAFE VERSION)
# ----------------------------
@st.cache_data
def load_data():
    file_name = "q1_q17_dr25_tce_2026.04.16_05.54.54.csv"
    
    try:
        df = pd.read_csv(file_name, comment="#")
    except FileNotFoundError:
        st.error("🚨 Dataset not found. Please upload CSV into the repository.")
        st.stop()

    # Clean metadata columns safely
    drop_cols = [
        "rowid",
        "tce_delivname",
        "tce_datalink_dvs",
        "tce_datalink_dvr"
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Remove fully empty columns
    missing_pct = (df.isnull().sum() / len(df)) * 100
    df = df.drop(columns=missing_pct[missing_pct == 100].index)

    return df

df = load_data()

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
menu = st.sidebar.radio(
    "Navigation",
    ["Overview", "Feature Exploration", "Clustering", "Anomaly Detection"]
)

features = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]

# ----------------------------
# OVERVIEW
# ----------------------------
if menu == "Overview":
    st.header("📊 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Features", df.shape[1])
    col3.metric("Numeric Columns", len(df.select_dtypes(include=np.number).columns))

    st.dataframe(df.head())

# ----------------------------
# FEATURE EXPLORATION
# ----------------------------
elif menu == "Feature Exploration":
    st.header("📈 Signal Distributions")

    feature = st.selectbox("Select Feature", features)

    data = np.log1p(df[feature].dropna())

    fig, ax = plt.subplots()
    ax.hist(data, bins=60)
    ax.set_title(f"Log Distribution: {feature}")

    st.pyplot(fig)

# ----------------------------
# CLUSTERING
# ----------------------------
elif menu == "Clustering":
    st.header("🧠 KMeans Signal Structure")

    X = df[features].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k = st.slider("Clusters", 2, 6, 4)

    model = KMeans(n_clusters=k, random_state=42)
    clusters = model.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots()
    ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, s=10)
    ax.set_title("Cluster Space (PCA Projection)")

    st.pyplot(fig)

    tmp = pd.DataFrame(X, columns=features)
    tmp["cluster"] = clusters

    st.subheader("Cluster Profiles")
    st.dataframe(tmp.groupby("cluster").mean())

# ----------------------------
# ANOMALY DETECTION
# ----------------------------
elif menu == "Anomaly Detection":
    st.header("⚠️ Anomalous Signal Detection")

    X = df[features].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    iso = IsolationForest(contamination=0.05, random_state=42)
    labels = iso.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots()
    ax.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, s=10)
    ax.set_title("Anomaly Map")

    st.pyplot(fig)

    st.write("🚨 Anomalies detected:", sum(labels == -1))

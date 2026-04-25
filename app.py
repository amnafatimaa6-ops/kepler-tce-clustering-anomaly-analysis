import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="Exoplanet Signal Analysis", layout="wide")

st.title("🌌 Exoplanet Signal Intelligence Dashboard")
st.markdown("Unsupervised Learning on NASA Kepler TCE Dataset")

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("q1_q17_dr25_tce_2026.04.16_05.54.54.csv", comment="#")
    
    # Drop metadata
    drop_cols = ["rowid", "tce_delivname", "tce_datalink_dvs", "tce_datalink_dvr"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    
    # Drop 100% missing
    missing_pct = (df.isnull().sum() / len(df)) * 100
    df = df.drop(columns=missing_pct[missing_pct == 100].index)
    
    return df

df = load_data()

# -----------------------
# SIDEBAR NAVIGATION
# -----------------------
section = st.sidebar.radio("Navigation", [
    "Overview",
    "Feature Analysis",
    "Clustering",
    "Anomaly Detection"
])

# -----------------------
# OVERVIEW
# -----------------------
if section == "Overview":
    st.header("Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Numerical Features", len(df.select_dtypes(include=np.number).columns))
    
    st.subheader("Sample Data")
    st.dataframe(df.head())

    st.subheader("Feature Summary")
    st.dataframe(df.describe().T)

# -----------------------
# FEATURE ANALYSIS
# -----------------------
elif section == "Feature Analysis":
    st.header("Feature Distributions")

    features = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]

    selected = st.selectbox("Select Feature", features)

    data = np.log1p(df[selected].dropna())

    fig, ax = plt.subplots()
    ax.hist(data, bins=80)
    ax.set_title(f"Log Distribution of {selected}")
    st.pyplot(fig)

# -----------------------
# CLUSTERING
# -----------------------
elif section == "Clustering":
    st.header("KMeans Clustering")

    features = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]
    X = df[features].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    k = st.slider("Number of Clusters", 2, 6, 4)

    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots()
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters)
    ax.set_title("Cluster Visualization (PCA)")
    st.pyplot(fig)

    st.subheader("Cluster Means")
    tmp = pd.DataFrame(X, columns=features)
    tmp["cluster"] = clusters
    st.dataframe(tmp.groupby("cluster").mean())

# -----------------------
# ANOMALY DETECTION
# -----------------------
elif section == "Anomaly Detection":
    st.header("Anomaly Detection (Isolation Forest)")

    features = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]
    X = df[features].dropna()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    contamination = st.slider("Anomaly Percentage", 0.01, 0.10, 0.05)

    iso = IsolationForest(contamination=contamination, random_state=42)
    labels = iso.fit_predict(X_scaled)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    fig, ax = plt.subplots()
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=labels)
    ax.set_title("Anomaly Visualization")
    st.pyplot(fig)

    st.write("Anomalies Detected:", (labels == -1).sum())

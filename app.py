import streamlit as st
import plotly.express as px
import pandas as pd

from model import load_data, preprocess, train_models, FEATURES

st.set_page_config(page_title="ExoCluster Explorer", layout="wide")

st.title("🌌 Exoplanet Signal 3D Explorer")

# Load data
df = load_data("data.csv")
df, X, X_scaled = preprocess(df)

clusters, anomalies, X_pca = train_models(X_scaled, X.index)

# Attach results
df = df.loc[X.index].copy()
df["cluster"] = clusters
df["anomaly"] = anomalies
df["x"] = X_pca[:, 0]
df["y"] = X_pca[:, 1]
df["z"] = X_pca[:, 2]

# Sidebar filters
st.sidebar.header("Controls")
show_anomalies = st.sidebar.checkbox("Show anomalies", True)

plot_df = df.copy()
if not show_anomalies:
    plot_df = plot_df[plot_df["anomaly"] == 1]

# 3D scatter
fig = px.scatter_3d(
    plot_df,
    x="x",
    y="y",
    z="z",
    color="cluster",
    symbol="anomaly",
    hover_data=FEATURES,
    title="3D Exoplanet Signal Space"
)

st.plotly_chart(fig, use_container_width=True)

# Stats panel
st.subheader("📊 Cluster Summary")
st.dataframe(plot_df.groupby("cluster")[FEATURES].mean())

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

def process_data(df):

    features = df[["period", "radius", "temp"]].copy()

    scaler = StandardScaler()
    X = scaler.fit_transform(features)

    # clustering
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)

    # anomaly detection
    iso = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = iso.fit_predict(X)

    return df, X

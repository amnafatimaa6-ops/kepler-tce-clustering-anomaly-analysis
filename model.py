import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

FEATURES = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]

def load_data(path):
    df = pd.read_csv(path, comment="#")
    return df

def preprocess(df):
    df = df.copy()
    
    X = df[FEATURES].dropna()
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return df, X, X_scaled

def train_models(X_scaled, df_index):
    # Clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    # Anomaly detection
    iso = IsolationForest(contamination=0.05, random_state=42)
    anomalies = iso.fit_predict(X_scaled)

    # PCA for 3D/2D projection
    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_scaled)

    return clusters, anomalies, X_pca

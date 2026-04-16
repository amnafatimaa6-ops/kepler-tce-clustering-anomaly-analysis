import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans

def generate_space_data(n=2500):
    np.random.seed(42)

    df = pd.DataFrame({
        "x": np.random.normal(0, 150, n),
        "y": np.random.normal(0, 150, n),
        "z": np.random.normal(0, 150, n),

        "tce_period": np.random.lognormal(3, 1, n),
        "tce_depth": np.random.lognormal(5, 2, n),
        "tce_duration": np.random.lognormal(1, 0.6, n),
        "tce_model_snr": np.random.lognormal(2, 1, n)
    })

    features = ["tce_period", "tce_depth", "tce_duration", "tce_model_snr"]

    scaler = StandardScaler()
    X = scaler.fit_transform(df[features])

    # ML MODELS
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)

    iso = IsolationForest(contamination=0.05, random_state=42)
    df["anomaly"] = iso.fit_predict(X)

    return df

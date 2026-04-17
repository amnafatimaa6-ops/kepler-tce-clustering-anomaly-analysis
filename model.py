import numpy as np
import pandas as pd

def generate_galaxy(n=800, seed=42):
    np.random.seed(seed)

    x = np.random.normal(0, 1, n)
    y = np.random.normal(0, 1, n)
    z = np.random.normal(0, 1, n)

    period = np.abs(np.random.normal(50, 80, n))
    depth = np.abs(np.random.normal(1000, 5000, n))
    snr = np.abs(np.random.normal(10, 50, n))
    duration = np.abs(np.random.normal(5, 3, n))

    anomaly = (snr > 80) | (depth > 12000)

    return pd.DataFrame({
        "x": x, "y": y, "z": z,
        "period": period,
        "depth": depth,
        "snr": snr,
        "duration": duration,
        "anomaly": anomaly.astype(int)
    })

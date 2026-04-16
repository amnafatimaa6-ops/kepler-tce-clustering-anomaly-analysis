import pandas as pd
import requests
from io import StringIO
import numpy as np

def fallback_data(n=200):
    return pd.DataFrame({
        "name": [f"Star-{i}" for i in range(n)],
        "period": np.random.uniform(0.5, 500, n),
        "radius": np.random.uniform(0.5, 20, n),
        "temp": np.random.uniform(200, 3000, n)
    })

def load_nasa_data(limit=200):
    try:
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

        query = f"""
        SELECT pl_name, pl_orbper, pl_rade, pl_eqt
        FROM ps
        WHERE pl_orbper IS NOT NULL
        LIMIT {limit}
        """

        response = requests.get(
            url,
            params={"query": query, "format": "csv"},
            timeout=10
        )

        # if bad response → fallback
        if response.status_code != 200 or len(response.text.strip()) < 10:
            return fallback_data(limit)

        df = pd.read_csv(StringIO(response.text))

        # safety rename
        df.columns = [c.strip().lower() for c in df.columns]

        df = df.rename(columns={
            "pl_name": "name",
            "pl_orbper": "period",
            "pl_rade": "radius",
            "pl_eqt": "temp"
        })

        required = ["name", "period", "radius", "temp"]
        df = df[[c for c in required if c in df.columns]]

        df = df.dropna()

        # if empty after cleaning → fallback
        if len(df) == 0:
            return fallback_data(limit)

        return df

    except Exception as e:
        print("NASA API failed:", e)
        return fallback_data(limit)

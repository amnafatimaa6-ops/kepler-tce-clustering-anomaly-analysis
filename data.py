import pandas as pd
import requests
from io import StringIO

def load_nasa_data(limit=200):
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

    query = f"""
    SELECT pl_name, pl_orbper, pl_rade, pl_eqt
    FROM ps
    WHERE pl_orbper IS NOT NULL
    LIMIT {limit}
    """

    response = requests.get(url, params={
        "query": query,
        "format": "csv"
    })

    # 🧠 safety check
    if response.status_code != 200 or len(response.text.strip()) == 0:
        raise ValueError("NASA API failed or returned empty data")

    df = pd.read_csv(StringIO(response.text))

    # 🧼 clean column names safely
    df.columns = [c.strip().lower() for c in df.columns]

    # 🧠 rename only if columns exist
    rename_map = {
        "pl_name": "name",
        "pl_orbper": "period",
        "pl_rade": "radius",
        "pl_eqt": "temp"
    }

    df = df.rename(columns=rename_map)

    # keep only required columns safely
    required = ["name", "period", "radius", "temp"]
    df = df[[c for c in required if c in df.columns]]

    # drop missing
    df = df.dropna()

    return df

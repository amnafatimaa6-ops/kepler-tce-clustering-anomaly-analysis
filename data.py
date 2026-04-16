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

    df = pd.read_csv(StringIO(response.text))

    df.columns = ["name", "period", "radius", "temp"]

    # clean
    df = df.dropna()
    return df

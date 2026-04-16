import pandas as pd
import requests

FEATURES = ["pl_orbper", "pl_rade", "pl_bmasse"]

def load_data():
    url = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?"
        "query=select+top+2000+pl_name,pl_orbper,pl_rade,pl_bmasse+from+ps&format=csv"
    )

    df = pd.read_csv(url)

    # clean
    df = df.dropna()

    return df


def get_features(df):
    X = df[FEATURES]
    return X

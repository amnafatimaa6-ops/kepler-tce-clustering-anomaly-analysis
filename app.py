import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="NASA Mission Control - Orbital Mode",
    layout="wide"
)

# ----------------------------
# SPACE THEME
# ----------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at bottom, #050814, #000000);
    color: white;
}
h1, h2 {
    text-shadow: 0px 0px 10px rgba(0,255,255,0.4);
}
</style>
""", unsafe_allow_html=True)

st.title("🛰️ NASA MISSION CONTROL — ORBITAL LIVE SYSTEM")
st.caption("Exoplanet Signal Intelligence + Orbital Simulation Engine")

# ----------------------------
# LIVE SYNTHETIC DATA
# ----------------------------
def generate_data(n=2000):
    np.random.seed(int(time.time()) % 1000)

    return pd.DataFrame({
        "tce_period": np.random.lognormal(3, 1, n),
        "tce_depth": np.random.lognormal(7, 1.2, n),
        "tce_duration": np.abs(np.random.normal(5, 2, n)),
        "tce_model_snr": np.random.lognormal(2, 1, n)
    })

df = generate_data()

features = ["tce_period", "tce_depth", "tce_model_snr"]

# ----------------------------
# ML PROCESSING
# ----------------------------
X = df[features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

iso = IsolationForest(contamination=0.05, random_state=42)
anomaly = iso.fit_predict(X_scaled)

df["cluster"] = clusters
df["anomaly"] = anomaly

# ----------------------------
# SIDEBAR CONTROL
# ----------------------------
st.sidebar.title("📡 Mission Control Panel")

mode = st.sidebar.radio(
    "System Mode",
    ["Live Orbit Simulation", "Static Analysis View"]
)

# =========================================================
# 🪐 ORBIT SIMULATION MODE
# =========================================================
if mode == "Live Orbit Simulation":

    st.subheader("🪐 ORBITAL SIGNAL TRAJECTORY FIELD")

    # pick subset for clarity
    n = 200
    sim = df.sample(n).reset_index(drop=True)

    # create orbit angles
    theta = np.linspace(0, 2*np.pi, n)

    # fake orbital radii based on signal strength
    radius = np.log1p(sim["tce_period"])

    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = sim["tce_model_snr"] / np.max(sim["tce_model_snr"]) * 50

    frames = []
    for i in range(0, 20):
        shift = i * 0.3
        frames.append(go.Frame(
            data=[
                go.Scatter3d(
                    x=x*np.cos(shift),
                    y=y*np.sin(shift),
                    z=z,
                    mode='markers',
                    marker=dict(
                        size=4,
                        color=sim["cluster"],
                        colorscale="Turbo",
                        opacity=0.8
                    )
                )
            ]
        ))

    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode='markers',
                marker=dict(
                    size=4,
                    color=sim["cluster"],
                    colorscale="Turbo",
                    opacity=0.8
                )
            )
        ],
        frames=frames
    )

    fig.update_layout(
        title="🪐 Simulated Orbital Motion of Exoplanet Signals",
        paper_bgcolor="black",
        font=dict(color="white"),
        scene=dict(
            bgcolor="black",
            xaxis_title="Orbit X",
            yaxis_title="Orbit Y",
            zaxis_title="Signal Strength (SNR)"
        ),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(label="▶ Play Orbit",
                     method="animate",
                     args=[None, {"frame": {"duration": 150, "redraw": True}}])
            ]
        )]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### 🛰️ Mission Interpretation
    - Signals behave like orbital trajectories in latent feature space  
    - Stronger signals appear at higher orbital elevation (SNR axis)  
    - Clustering reveals grouped orbital regimes (stable astrophysical families)
    """)

# =========================================================
# STATIC VIEW
# =========================================================
else:

    st.subheader("📊 Static Mission Telemetry")

    st.write("Anomaly count:", int((df["anomaly"] == -1).sum()))

    st.markdown("""
    System is in diagnostic mode. Orbit simulation disabled.
    """)

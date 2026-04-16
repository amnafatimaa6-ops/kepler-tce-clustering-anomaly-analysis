import plotly.graph_objects as go
import numpy as np

def create_cinematic_galaxy(df):

    fig = go.Figure()

    # 🌟 STAR FIELD BACKGROUND
    n_stars = 1200
    fig.add_trace(go.Scatter3d(
        x=np.random.normal(0, 400, n_stars),
        y=np.random.normal(0, 400, n_stars),
        z=np.random.normal(0, 400, n_stars),
        mode="markers",
        marker=dict(size=1, color="white", opacity=0.15),
        name="Star Field"
    ))

    # 🪐 CLUSTERS (galaxies / systems)
    colors = ["cyan", "magenta", "yellow", "lime"]

    for c in df["cluster"].unique():
        d = df[df["cluster"] == c]

        fig.add_trace(go.Scatter3d(
            x=d["x"],
            y=d["y"],
            z=d["z"],
            mode="markers",
            marker=dict(
                size=2.5,
                color=colors[c % len(colors)],
                opacity=0.75
            ),
            name=f"System {c}"
        ))

    # ⚠ ANOMALIES (cosmic events)
    anomaly = df[df["anomaly"] == -1]

    fig.add_trace(go.Scatter3d(
        x=anomaly["x"],
        y=anomaly["y"],
        z=anomaly["z"],
        mode="markers",
        marker=dict(
            size=6,
            color="red",
            symbol="x",
            opacity=0.9
        ),
        name="Cosmic Anomaly"
    ))

    # 🌌 DARK SPACE STYLE
    fig.update_layout(
        paper_bgcolor="black",
        plot_bgcolor="black",
        margin=dict(l=0, r=0, t=0, b=0),

        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="black"
        ),

        title="🌌 EXOGALAXY — CINEMATIC AI UNIVERSE",
        font=dict(color="white")
    )

    return fig

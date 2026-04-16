import plotly.graph_objects as go

def create_galaxy(df):

    colors = ["cyan", "magenta", "yellow", "lime"]

    fig = go.Figure()

    # normal stars
    for c in df["cluster"].unique():
        d = df[df["cluster"] == c]

        fig.add_trace(go.Scatter3d(
            x=d["x"],
            y=d["y"],
            z=d["z"],
            mode="markers",
            marker=dict(size=2, color=colors[c % len(colors)]),
            name=f"Cluster {c}"
        ))

    # anomalies (red supernova vibes)
    anomaly = df[df["anomaly"] == -1]

    fig.add_trace(go.Scatter3d(
        x=anomaly["x"],
        y=anomaly["y"],
        z=anomaly["z"],
        mode="markers",
        marker=dict(size=5, color="red", symbol="x"),
        name="Anomalies"
    ))

    fig.update_layout(
        paper_bgcolor="black",
        plot_bgcolor="black",
        margin=dict(l=0, r=0, t=0, b=0),
        scene=dict(
            xaxis=dict(backgroundcolor="black"),
            yaxis=dict(backgroundcolor="black"),
            zaxis=dict(backgroundcolor="black"),
        ),
        title="🌌 ExoGalaxy 3D Universe Explorer"
    )

    return fig

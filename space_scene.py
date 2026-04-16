
import plotly.graph_objects as go

def create_galaxy(df):

    colors = ["cyan", "magenta", "yellow", "lime"]

    fig = go.Figure()

    # 🌟 normal galaxy clusters
    for c in sorted(df["cluster"].unique()):
        d = df[df["cluster"] == c]

        fig.add_trace(go.Scatter3d(
            x=d["x"],
            y=d["y"],
            z=d["z"],
            mode="markers",
            marker=dict(
                size=2,
                color=colors[c % len(colors)],
                opacity=0.7
            ),
            name=f"Cluster {c}"
        ))

    # ☄️ anomalies (rare cosmic events)
    anomaly = df[df["anomaly"] == -1]

    fig.add_trace(go.Scatter3d(
        x=anomaly["x"],
        y=anomaly["y"],
        z=anomaly["z"],
        mode="markers",
        marker=dict(
            size=5,
            color="red",
            symbol="x",
            opacity=0.9
        ),
        name="Anomalies"
    ))

    fig.update_layout(
        paper_bgcolor="black",
        plot_bgcolor="black",
        margin=dict(l=0, r=0, t=0, b=0),

        scene=dict(
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(showbackground=False),
        ),

        title="🌌 ExoGalaxy 3D Universe Explorer"
    )

    return fig

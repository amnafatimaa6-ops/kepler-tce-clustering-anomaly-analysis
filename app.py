import streamlit as st
import numpy as np
import time
import plotly.graph_objects as go

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="NASA Mission Control V5",
    layout="wide",
)

# ----------------------------
# 🌌 STARFIELD BACKGROUND (REAL ANIMATION)
# ----------------------------
st.markdown("""
<style>
body {
    margin: 0;
    overflow-x: hidden;
    background: black;
}

/* canvas starfield */
#stars {
    position: fixed;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: radial-gradient(ellipse at bottom, #0d1d31 0%, #000 100%);
}

/* warp flash effect */
.warp {
    animation: warpFlash 1.5s ease-in-out infinite alternate;
}

@keyframes warpFlash {
    0% { filter: brightness(1); }
    100% { filter: brightness(2) contrast(1.3); }
}

/* HUD glow */
.glow {
    color: #00ffe1;
    text-shadow: 0 0 10px #00ffe1, 0 0 30px #00bfff;
    font-size: 26px;
    text-align: center;
}
</style>

<canvas id="stars"></canvas>

<script>
const canvas = document.getElementById("stars");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let stars = Array(400).fill().map(() => {
    return {
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        z: Math.random() * canvas.width
    };
});

function draw() {
    ctx.fillStyle = "black";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    for (let s of stars) {
        s.z -= 2;

        if (s.z <= 0) {
            s.x = Math.random() * canvas.width;
            s.y = Math.random() * canvas.height;
            s.z = canvas.width;
        }

        let k = 128.0 / s.z;
        let px = s.x * k + canvas.width / 2;
        let py = s.y * k + canvas.height / 2;

        if (px >= 0 && px < canvas.width && py >= 0 && py < canvas.height) {
            let size = (1 - s.z / canvas.width) * 3;
            ctx.fillStyle = "white";
            ctx.fillRect(px, py, size, size);
        }
    }

    requestAnimationFrame(draw);
}

draw();
</script>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<div class='glow warp'>🛰️ NASA MISSION CONTROL — V5 ORBITAL SIMULATION</div>", unsafe_allow_html=True)

# ----------------------------
# KEPLER ORBIT PHYSICS (REAL MATH)
# ----------------------------
st.markdown("## 🪐 Kepler Orbit Simulation (True Physics)")

# semi-major axis
a = 3
e = 0.6  # eccentricity

theta = np.linspace(0, 2*np.pi, 500)

# Kepler ellipse equation
r = (a * (1 - e**2)) / (1 + e * np.cos(theta))

x = r * np.cos(theta)
y = r * np.sin(theta)

fig = go.Figure()

# orbit path
fig.add_trace(go.Scatter(
    x=x, y=y,
    mode="lines",
    line=dict(color="cyan", width=2),
    name="Orbit Path"
))

# focus (star)
fig.add_trace(go.Scatter(
    x=[0], y=[0],
    mode="markers",
    marker=dict(size=12, color="yellow"),
    name="Star"
))

fig.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black",
    font=dict(color="cyan"),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# LIVE WARP SIMULATION FEED
# ----------------------------
st.markdown("## ⚡ Warp-Speed Telemetry")

telemetry = [
    "Entering orbital resonance field...",
    "Warp bubble stabilizing...",
    "Gravitational lensing detected...",
    "Signal coherence increasing...",
    "Deep space anomaly scan active..."
]

placeholder = st.empty()

for i in range(15):
    msg = np.random.choice(telemetry)
    placeholder.markdown(f"""
    <div style='color:#00ffe1; font-family:monospace; font-size:14px'>
    🛰️ {msg} | T+ {i}
    </div>
    """, unsafe_allow_html=True)
    time.sleep(0.15)

# ----------------------------
# FINAL MISSION STATE
# ----------------------------
st.markdown("---")
st.success("🟢 ORBIT STABLE — KEPLER SYSTEM LOCKED — STARFIELD SYNCHRONIZED")

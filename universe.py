import json

def render_universe(df):
    data_json = json.dumps(df.to_dict(orient="records"))

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                overflow: hidden;
                background: black;
            }}
            #info {{
                position: absolute;
                top: 10px;
                left: 10px;
                color: white;
                z-index: 10;
                font-family: Arial;
                background: rgba(0,0,0,0.5);
                padding: 10px;
                border-radius: 8px;
            }}
        </style>
    </head>

    <body>
    <div id="info">
        🌌 ExoGalaxy Live<br>
        🔴 Anomalies | 🔵 Normal Signals
    </div>

    <script src="https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.min.js"></script>

    <script>
        const scene = new THREE.Scene();

        const camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth/window.innerHeight,
            0.1,
            2000
        );

        // ⭐ IMPORTANT FIX: move camera back MORE
        camera.position.z = 120;

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // 🌟 STAR FIELD (bigger visibility)
        for (let i = 0; i < 3000; i++) {{
            const star = new THREE.Mesh(
                new THREE.SphereGeometry(0.2, 6, 6),
                new THREE.MeshBasicMaterial({{ color: 0xffffff }})
            );

            star.position.set(
                (Math.random() - 0.5) * 800,
                (Math.random() - 0.5) * 800,
                (Math.random() - 0.5) * 800
            );

            scene.add(star);
        }}

        const data = {data_json};

        data.forEach(p => {{
            const isAnomaly = p.anomaly === 1;

            const color = isAnomaly ? 0xff0033 : 0x00ffff;

            const planet = new THREE.Mesh(
                new THREE.SphereGeometry(isAnomaly ? 1.5 : 1.0, 10, 10),
                new THREE.MeshBasicMaterial({{ color: color }})
            );

            // 🔥 IMPORTANT FIX: spread points wider
            planet.position.x = p.x * 40;
            planet.position.y = p.y * 40;
            planet.position.z = p.z * 40;

            scene.add(planet);
        }});

        function animate() {{
            requestAnimationFrame(animate);

            scene.rotation.y += 0.001;
            scene.rotation.x += 0.0004;

            renderer.render(scene, camera);
        }}

        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth/window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>

    </body>
    </html>
    """

    return html

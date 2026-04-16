

import json

def render_universe(df):
    data = df.to_dict(orient="records")
    data_json = json.dumps(data)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                overflow: hidden;
                background: radial-gradient(circle at center, #000010, #000000);
            }}

            #info {{
                position: absolute;
                color: white;
                top: 10px;
                left: 10px;
                font-family: Arial;
                z-index: 10;
                background: rgba(0,0,0,0.4);
                padding: 10px;
                border-radius: 8px;
            }}
        </style>
    </head>

    <body>
    <div id="info">
        🌌 ExoGalaxy Explorer<br>
        🔴 Red = Anomaly<br>
        🔵 Cyan = Normal Signal
    </div>

    <script src="https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.min.js"></script>

    <script>
        const scene = new THREE.Scene();

        const camera = new THREE.PerspectiveCamera(
            75,
            window.innerWidth / window.innerHeight,
            0.1,
            1000
        );
        camera.position.z = 6;

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // 🌟 STAR FIELD
        for (let i = 0; i < 1500; i++) {{
            const star = new THREE.Mesh(
                new THREE.SphereGeometry(0.01, 6, 6),
                new THREE.MeshBasicMaterial({{ color: 0xffffff }})
            );

            star.position.set(
                (Math.random() - 0.5) * 60,
                (Math.random() - 0.5) * 60,
                (Math.random() - 0.5) * 60
            );

            scene.add(star);
        }}

        // 🌍 DATA
        const data = {data_json};

        data.forEach(p => {{
            const color = p.anomaly === 1 ? 0xff0033 : 0x00ffff;

            const planet = new THREE.Mesh(
                new THREE.SphereGeometry(p.anomaly ? 0.06 : 0.03, 10, 10),
                new THREE.MeshBasicMaterial({{ color: color }})
            );

            planet.position.x = p.x * 4;
            planet.position.y = p.y * 4;
            planet.position.z = p.z * 4;

            scene.add(planet);
        }});

        // 🌌 ANIMATION (cinematic drift)
        function animate() {{
            requestAnimationFrame(animate);
            scene.rotation.y += 0.0006;
            scene.rotation.x += 0.0002;
            renderer.render(scene, camera);
        }}

        animate();

        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>

    </body>
    </html>
    """

    return html

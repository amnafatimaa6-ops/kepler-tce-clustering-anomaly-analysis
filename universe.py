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
        </style>
    </head>

    <body>
    <script src="https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.min.js"></script>

    <script>
        const scene = new THREE.Scene();

        const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 5000);
        camera.position.z = 200;

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        // 🌟 STARFIELD (MILKY WAY STYLE)
        const starGeo = new THREE.BufferGeometry();
        const starCount = 5000;

        const positions = [];

        for (let i = 0; i < starCount; i++) {{
            positions.push((Math.random() - 0.5) * 2000);
            positions.push((Math.random() - 0.5) * 2000);
            positions.push((Math.random() - 0.5) * 2000);
        }}

        starGeo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

        const starMat = new THREE.PointsMaterial({{
            color: 0xffffff,
            size: 1
        }});

        const stars = new THREE.Points(starGeo, starMat);
        scene.add(stars);

        // ☀️ SUN (glowing)
        const sun = new THREE.Mesh(
            new THREE.SphereGeometry(10, 32, 32),
            new THREE.MeshBasicMaterial({{ color: 0xffcc00 }})
        );
        scene.add(sun);

        // 🪐 PLANETS ORBITING
        const planets = [];

        for (let i = 0; i < 5; i++) {{
            const planet = new THREE.Mesh(
                new THREE.SphereGeometry(2 + Math.random(), 16, 16),
                new THREE.MeshBasicMaterial({{
                    color: new THREE.Color(`hsl(${{Math.random()*360}}, 70%, 50%)`)
                }})
            );

            planet.userData = {{
                radius: 30 + i * 15,
                speed: 0.002 + Math.random() * 0.003,
                angle: Math.random() * Math.PI * 2
            }};

            scene.add(planet);
            planets.push(planet);
        }}

        // 🌍 EXOPLANET DATA
        const data = {data_json};

        data.forEach(p => {{
            const isAnomaly = p.anomaly === 1;

            const planet = new THREE.Mesh(
                new THREE.SphereGeometry(isAnomaly ? 2 : 1.2, 12, 12),
                new THREE.MeshBasicMaterial({{
                    color: isAnomaly ? 0xff0033 : 0x00ffff
                }})
            );

            planet.position.set(
                p.x * 100,
                p.y * 100,
                p.z * 100
            );

            scene.add(planet);
        }});

        // 🎬 ANIMATION LOOP
        function animate() {{
            requestAnimationFrame(animate);

            // orbit planets
            planets.forEach(p => {{
                p.userData.angle += p.userData.speed;
                p.position.x = Math.cos(p.userData.angle) * p.userData.radius;
                p.position.z = Math.sin(p.userData.angle) * p.userData.radius;
            }});

            // slow galaxy drift
            scene.rotation.y += 0.0005;

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

import streamlit as st
import streamlit.components.v1 as components

def render_universe():

    html = """
<!DOCTYPE html>
<html>
<head>
<style>
body { margin:0; overflow:hidden; background:black; }
canvas { display:block; }
#hud{
  position:absolute;
  top:10px;
  left:10px;
  color:white;
  font-family:Arial;
  background:rgba(0,0,0,0.6);
  padding:12px;
  border-radius:12px;
  font-size:14px;
}
</style>
</head>

<body>

<div id="hud">
🌌 ExoGalaxy Realistic Mode<br>
🟡 Sun = light source<br>
🌍 Planets = orbiting bodies<br>
🔴 Red = anomalies (ML outliers)
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.155.0/build/three.min.js"></script>

<script>

// ======================
// 🌌 SCENE
// ======================
const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth/window.innerHeight,
  0.1,
  5000
);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

camera.position.z = 200;

// ======================
// ⭐ STAR BACKGROUND
// ======================
function stars(){
  const geo = new THREE.BufferGeometry();
  const pos = [];

  for(let i=0;i<20000;i++){
    pos.push(
      (Math.random()-0.5)*4000,
      (Math.random()-0.5)*4000,
      (Math.random()-0.5)*4000
    );
  }

  geo.setAttribute("position", new THREE.Float32BufferAttribute(pos,3));

  const mat = new THREE.PointsMaterial({
    color:0xffffff,
    size:0.7,
    transparent:true
  });

  scene.add(new THREE.Points(geo,mat));
}
stars();


// ======================
// ☀️ SUN (REAL LIGHT SOURCE)
// ======================
const sunGeo = new THREE.SphereGeometry(18, 64, 64);

const sunMat = new THREE.MeshBasicMaterial({
  color: 0xffcc33
});

const sun = new THREE.Mesh(sunGeo, sunMat);
scene.add(sun);

// REAL LIGHT FROM SUN
const light = new THREE.PointLight(0xffffff, 3, 2000);
light.position.set(0,0,0);
scene.add(light);


// ======================
// 🌍 PLANET FUNCTION (REALISTIC)
// ======================
function createPlanet(size, color, distance, speed, name){

  const geo = new THREE.SphereGeometry(size, 64, 64);

  const mat = new THREE.MeshStandardMaterial({
    color: color,
    roughness: 0.7,
    metalness: 0.1
  });

  const mesh = new THREE.Mesh(geo, mat);

  const pivot = new THREE.Object3D();
  scene.add(pivot);

  mesh.position.x = distance;
  pivot.add(mesh);

  return {mesh, pivot, speed, name};
}


// ======================
// 🌍 NORMAL PLANETS
// ======================
const earth = createPlanet(5, 0x2a6cff, 60, 0.01, "Earth");
const venus = createPlanet(4, 0xff9966, 90, 0.008, "Venus");
const mars  = createPlanet(4.5, 0xff5533, 120, 0.006, "Mars");


// ======================
// 🌙 MOON (EARTH)
// ======================
const moon = createPlanet(1.5, 0xaaaaaa, 10, 0.03, "Moon");
earth.mesh.add(moon.mesh);


// ======================
// 🔴 ANOMALIES (ML OUTLIERS)
// ======================
const anomaly1 = createPlanet(6, 0xff0033, 160, 0.004, "Anomaly-1");
const anomaly2 = createPlanet(7, 0xff00aa, 210, 0.003, "Anomaly-2");


// ======================
// 🌌 ANIMATION LOOP
// ======================
function animate(){

  requestAnimationFrame(animate);

  // planet orbits
  earth.pivot.rotation.y += earth.speed;
  venus.pivot.rotation.y += venus.speed;
  mars.pivot.rotation.y += mars.speed;

  anomaly1.pivot.rotation.y += anomaly1.speed;
  anomaly2.pivot.rotation.y += anomaly2.speed;

  // slow galaxy rotation
  scene.rotation.y += 0.0003;

  renderer.render(scene,camera);
}

animate();


// ======================
// 📱 RESPONSIVE
// ======================
window.addEventListener("resize",()=>{
  camera.aspect = window.innerWidth/window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth,window.innerHeight);
});

</script>

</body>
</html>
"""

    components.html(html, height=900, scrolling=False)

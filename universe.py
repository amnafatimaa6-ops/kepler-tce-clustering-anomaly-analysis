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
#info {
  position:absolute;
  top:10px;
  left:10px;
  color:white;
  font-family:Arial;
  background:rgba(0,0,0,0.5);
  padding:10px;
  border-radius:10px;
}
</style>
</head>

<body>

<div id="info">
<b>ExoGalaxy System</b><br>
Click + observe cosmic structure<br>
</div>

<script src="https://cdn.jsdelivr.net/npm/three@0.155.0/build/three.min.js"></script>

<script>

// ======================
// 🌌 SCENE SETUP
// ======================
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth/window.innerHeight,
  0.1,
  3000
);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

camera.position.z = 120;

// ======================
// ⭐ STAR FIELD (GALAXY)
// ======================
function createStars(){
  const geo = new THREE.BufferGeometry();
  const pos = [];

  for(let i=0;i<15000;i++){
    pos.push(
      (Math.random()-0.5)*2500,
      (Math.random()-0.5)*2500,
      (Math.random()-0.5)*2500
    );
  }

  geo.setAttribute("position", new THREE.Float32BufferAttribute(pos,3));

  const mat = new THREE.PointsMaterial({
    color:0xffffff,
    size:1.0
  });

  scene.add(new THREE.Points(geo,mat));
}
createStars();


// ======================
// 🪐 CELESTIAL OBJECTS
// ======================
function planet(x,y,z,color,size,name,type){

  const geo = new THREE.SphereGeometry(size,32,32);
  const mat = new THREE.MeshBasicMaterial({color:color});
  const mesh = new THREE.Mesh(geo,mat);

  mesh.position.set(x,y,z);
  mesh.userData = {name,type};

  scene.add(mesh);
}

// ======================
// ☀️ STAR SYSTEM
// ======================
planet(0,0,0,0xffff00,10,"Sun","star");

// 🌍 PLANETS (NORMAL EXOPLANETS)
planet(40,10,-80,0x00aaff,3,"Kepler-22b","planet");
planet(-60,-20,-120,0x00ffcc,2.5,"Kepler-69c","planet");

// 🌙 MOON SYSTEM
planet(50,15,-85,0x888888,1,"Moon-1","moon");

// ======================
// 🔴 ANOMALIES (YOUR ML OUTPUT)
// ======================
// These represent:
// - extreme depth
// - abnormal SNR
// - unusual orbital period

planet(-80,30,-150,0xff0000,3,"ANOMALY-1","anomaly");
planet(90,-40,-200,0xff0066,4,"ANOMALY-2","anomaly");
planet(-120,60,-260,0xff3300,2.5,"ANOMALY-3","anomaly");


// ======================
// 🌀 ROTATION (GALAXY FEEL)
// ======================
function animate(){
  requestAnimationFrame(animate);

  scene.rotation.y += 0.0008;

  renderer.render(scene,camera);
}
animate();


// ======================
// 📱 RESIZE
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

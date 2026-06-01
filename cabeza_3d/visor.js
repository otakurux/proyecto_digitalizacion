import * as THREE from "three";

import { OrbitControls }
from "https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js";

import { FBXLoader }
from "https://unpkg.com/three@0.160.0/examples/jsm/loaders/FBXLoader.js";

const viewer =
document.getElementById("viewer");

const loading =
document.getElementById("loading");

const errorPanel =
document.getElementById("errorPanel");

const scene =
new THREE.Scene();

scene.background =
new THREE.Color(0xe5e5e5);

const camera =
new THREE.PerspectiveCamera(
60,
window.innerWidth/window.innerHeight,
0.01,
10000
);

camera.position.set(
0,
2,
5
);

const renderer =
new THREE.WebGLRenderer({
    antialias:true
});

renderer.setPixelRatio(
window.devicePixelRatio
);

renderer.setSize(
window.innerWidth,
window.innerHeight
);

viewer.appendChild(
renderer.domElement
);

const controls =
new OrbitControls(
camera,
renderer.domElement
);

controls.enableDamping = true;

controls.dampingFactor = 0.05;

controls.minDistance = 0.1;
controls.maxDistance = 1000;

/* ======================
   GRID
====================== */

const grid =
new THREE.GridHelper(
20,
20
);

scene.add(grid);

/* ======================
   EJES XYZ
====================== */

const axes =
new THREE.AxesHelper(5);

scene.add(axes);

/* ======================
   LUCES
====================== */

const ambient =
new THREE.AmbientLight(
0xffffff,
2
);

scene.add(ambient);

const directional =
new THREE.DirectionalLight(
0xffffff,
3
);

directional.position.set(
5,
10,
5
);

scene.add(directional);

const directional2 =
new THREE.DirectionalLight(
0xffffff,
2
);

directional2.position.set(
-5,
5,
-5
);

scene.add(directional2);

/* ======================
   CUBO TEST
====================== */

const cube =
new THREE.Mesh(

    new THREE.BoxGeometry(
        0.5,
        0.5,
        0.5
    ),

    new THREE.MeshNormalMaterial()

);

cube.position.set(
-2,
0.25,
0
);

scene.add(cube);

/* ======================
   CARGA FBX
====================== */

const loader =
new FBXLoader();

loader.load(

"/visor3d/cabeza.fbx",

function(model){

    console.log(
        "Modelo cargado"
    );

    loading.innerHTML =
    "Modelo cargado";

    scene.add(model);

    const box =
    new THREE.Box3()
    .setFromObject(model);

    const center =
    box.getCenter(
        new THREE.Vector3()
    );

    const size =
    box.getSize(
        new THREE.Vector3()
    );

    console.log(
        "Tamaño:",
        size
    );

    model.position.x = 0;
    model.position.y = 0;
    model.position.z = 0;

    const maxAxis =
    Math.max(
        size.x,
        size.y,
        size.z
    );

    const scale =
    3 / maxAxis;

    model.scale.set(
        scale,
        scale,
        scale
    );

    const distance = 10;

    camera.position.set(
        distance,
        distance,
        distance
    );

    controls.target.set(
        0,
        0,
        0
    );

    controls.update();

},

function(xhr){

    if(xhr.total){

        const percent =
        (
            xhr.loaded /
            xhr.total
        ) * 100;

        loading.innerHTML =
        "Cargando: "
        + percent.toFixed(1)
        + "%";
    }

},

function(error){

    console.error(error);

    errorPanel.innerHTML =
    "Error al cargar FBX";

}

);

/* ======================
   RENDER
====================== */

function animate(){

    requestAnimationFrame(
        animate
    );

    cube.rotation.y += 0.01;

    controls.update();

    renderer.render(
        scene,
        camera
    );
}

animate();

/* ======================
   RESIZE
====================== */

window.addEventListener(
"resize",
()=>{

    camera.aspect =
    window.innerWidth /
    window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

});
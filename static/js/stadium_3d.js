// Three.js 3D Stadium Visualization

let scene, camera, renderer, controls;
let stadiumGroup;
let raycaster, mouse;
let interactiveObjects = [];

// Color status mappings
const STATUS_COLORS = {
    'Green': 0x39ff14,
    'Yellow': 0xffff00,
    'Orange': 0xff9e00,
    'Red': 0xff0055
};

const DEFAULT_COLOR = 0x1e293b;

function init3DStadium() {
    const container = document.getElementById('canvas3d');
    if (!container) return;

    const width = container.clientWidth;
    const height = container.clientHeight;

    // 1. Create Scene & Camera
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x060913, 0.015);

    camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.set(0, 45, 60);

    // 2. Create Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // 3. Add Orbit Controls
    if (typeof THREE.OrbitControls !== 'undefined') {
        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.maxPolarAngle = Math.PI / 2 - 0.05; // don't go below ground
        controls.minDistance = 20;
        controls.maxDistance = 150;
    }

    // 4. Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0x00f0ff, 0.8);
    dirLight1.position.set(20, 40, 20);
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x9d4edd, 0.6);
    dirLight2.position.set(-20, 30, -20);
    scene.add(dirLight2);

    stadiumGroup = new THREE.Group();
    scene.add(stadiumGroup);

    // 5. Build Stadium Meshes
    buildPitch();
    buildStands();
    buildGates();
    buildParkingAndTransit();

    // Raycaster for click events
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    container.addEventListener('click', onStadiumClick, false);
    window.addEventListener('resize', onWindowResize, false);

    animate();
}

// Draw soccer pitch in center
function buildPitch() {
    // Pitch base
    const pitchGeo = new THREE.BoxGeometry(22, 0.5, 14);
    const pitchMat = new THREE.MeshPhongMaterial({
        color: 0x052e16,
        emissive: 0x064e3b,
        emissiveIntensity: 0.2,
        flatShading: true
    });
    const pitch = new THREE.Mesh(pitchGeo, pitchMat);
    pitch.position.y = 0.25;
    stadiumGroup.add(pitch);

    // Pitch lines
    const lineMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    const centerCircleGeo = new THREE.RingGeometry(2.5, 2.6, 32);
    const centerCircle = new THREE.Mesh(centerCircleGeo, lineMat);
    centerCircle.rotation.x = -Math.PI / 2;
    centerCircle.position.y = 0.51;
    stadiumGroup.add(centerCircle);
}

// Build ring stands (Lower, Middle, Upper Tiers)
function buildStands() {
    const tiers = [
        { id: 'stand_lower', radius: 16, height: 2, depth: 3, name: 'Lower Tier Stands' },
        { id: 'stand_middle', radius: 21, height: 4, depth: 4, name: 'Mid Tier Stands' },
        { id: 'stand_upper', radius: 27, height: 7, depth: 5, name: 'Upper Tier Stands' }
    ];

    tiers.forEach((tier, index) => {
        // Draw stands using cylinder geometries with hollow centers
        const radialSegments = 32;
        const geom = new THREE.CylinderGeometry(
            tier.radius + tier.depth, 
            tier.radius, 
            tier.height, 
            radialSegments, 
            1, 
            true
        );
        
        // Materials (Glassmorphic neon edges look)
        const mat = new THREE.MeshPhongMaterial({
            color: DEFAULT_COLOR,
            transparent: true,
            opacity: 0.75,
            side: THREE.DoubleSide,
            shininess: 80,
            flatShading: true
        });

        const standMesh = new THREE.Mesh(geom, mat);
        standMesh.position.y = (tier.height / 2) + 0.1;
        standMesh.userData = { 
            id: tier.id, 
            name: tier.name, 
            type: 'stand',
            defaultColor: DEFAULT_COLOR
        };
        
        stadiumGroup.add(standMesh);
        interactiveObjects.push(standMesh);
    });
}

// Build Gates around the stands
function buildGates() {
    const gateData = [
        { id: 'gate_a', name: 'Gate A (North)', angle: 0, radius: 34 },
        { id: 'gate_b', name: 'Gate B (East)', angle: Math.PI / 2, radius: 34 },
        { id: 'gate_c', name: 'Gate C (West)', angle: -Math.PI / 2, radius: 34 },
        { id: 'vip_entrance', name: 'VIP Club Entrance', angle: Math.PI, radius: 34 }
    ];

    gateData.forEach(g => {
        const geom = new THREE.BoxGeometry(4, 3, 4);
        const mat = new THREE.MeshPhongMaterial({
            color: 0x0f172a,
            emissive: 0x0f172a,
            shininess: 100
        });
        const gateMesh = new THREE.Mesh(geom, mat);
        
        // Arrange circularly
        gateMesh.position.x = Math.cos(g.angle) * g.radius;
        gateMesh.position.z = Math.sin(g.angle) * g.radius;
        gateMesh.position.y = 1.5;
        
        gateMesh.userData = {
            id: g.id,
            name: g.name,
            type: 'entrance',
            defaultColor: 0x0f172a
        };

        stadiumGroup.add(gateMesh);
        interactiveObjects.push(gateMesh);
    });
}

// Outer parking lots & Transit stations
function buildParkingAndTransit() {
    const items = [
        { id: 'parking_east', name: 'Parking Lot East', x: 45, z: 25, color: 0x334155, type: 'parking' },
        { id: 'parking_west', name: 'Parking Lot West', x: -45, z: 25, color: 0x334155, type: 'parking' },
        { id: 'parking_vip', name: 'VIP Parking Lot', x: 0, z: -48, color: 0x475569, type: 'parking' },
        { id: 'metro_station', name: 'Metro Transit Hub', x: 45, z: -30, color: 0x0284c7, type: 'transit' },
        { id: 'bus_stop', name: 'Stadium Bus Terminal', x: -45, z: -30, color: 0x0f766e, type: 'transit' }
    ];

    items.forEach(it => {
        const geom = new THREE.BoxGeometry(10, 0.4, 10);
        const mat = new THREE.MeshPhongMaterial({ color: it.color, transparent: true, opacity: 0.8 });
        const mesh = new THREE.Mesh(geom, mat);
        mesh.position.set(it.x, 0.2, it.z);
        mesh.userData = {
            id: it.id,
            name: it.name,
            type: it.type,
            defaultColor: it.color
        };
        stadiumGroup.add(mesh);
        interactiveObjects.push(mesh);
        
        // Add a small pole light on top of transit zones
        if (it.type === 'transit') {
            const poleGeo = new THREE.CylinderGeometry(0.2, 0.2, 4);
            const poleMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
            const pole = new THREE.Mesh(poleGeo, poleMat);
            pole.position.set(it.x, 2, it.z);
            stadiumGroup.add(pole);
        }
    });
}

// WebSockets push updates color matching
function update3DStadiumColors(zonesArray) {
    if (!zonesArray) return;
    
    zonesArray.forEach(z => {
        const mesh = interactiveObjects.find(obj => obj.userData.id === z.id);
        if (mesh) {
            const status = z.status; // Green, Yellow, Orange, Red
            const targetColor = STATUS_COLORS[status] || mesh.userData.defaultColor;
            
            // Perform color transition / update material
            mesh.material.color.setHex(targetColor);
            if (status !== 'Green') {
                mesh.material.emissive.setHex(targetColor);
                mesh.material.emissiveIntensity = 0.35;
            } else {
                mesh.material.emissive.setHex(0x000000);
            }
        }
    });
}

// Click Raycast Handler
function onStadiumClick(event) {
    const container = document.getElementById('canvas3d');
    const rect = container.getBoundingClientRect();
    
    mouse.x = ((event.clientX - rect.left) / container.clientWidth) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / container.clientHeight) * 2 + 1;

    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(interactiveObjects);

    if (intersects.length > 0) {
        const clickedObj = intersects[0].object;
        console.log("Clicked 3D Zone:", clickedObj.userData.id);
        
        // Trigger UI callback
        if (window.selectStadiumZone) {
            window.selectStadiumZone(clickedObj.userData.id);
        }
        
        // Visual indicator flash
        const origColor = clickedObj.material.color.getHex();
        clickedObj.material.color.setHex(0xffffff);
        setTimeout(() => {
            clickedObj.material.color.setHex(origColor);
        }, 150);
    }
}

function onWindowResize() {
    const container = document.getElementById('canvas3d');
    if (!container) return;
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

let pulseTime = 0;
function animate() {
    requestAnimationFrame(animate);
    
    pulseTime += 0.03;
    
    // Gentle pulse animation for active neon glowing sectors
    interactiveObjects.forEach(mesh => {
        if (mesh.material.emissive && mesh.material.emissive.getHex() !== 0x000000) {
            mesh.material.emissiveIntensity = 0.25 + Math.sin(pulseTime) * 0.15;
        }
    });
    
    // Rotate stadium very slowly for dynamic view
    if (stadiumGroup && (!controls || controls.state === -1)) {
        stadiumGroup.rotation.y += 0.0006;
    }
    
    if (controls) controls.update();
    renderer.render(scene, camera);
}

// Global hook
window.init3DStadium = init3DStadium;
window.update3DStadiumColors = update3DStadiumColors;

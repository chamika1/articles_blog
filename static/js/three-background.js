// Enhanced Three.js background with interactive effects
let scene, camera, renderer, particlesMesh, clock;
let mouseX = 0, mouseY = 0;
let targetX = 0, targetY = 0;
let windowHalfX = window.innerWidth / 2;
let windowHalfY = window.innerHeight / 2;

// Initialize Three.js scene
function initThreeJS() {
    // Setup
    clock = new THREE.Clock();
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 3;
    
    // Renderer
    const canvas = document.getElementById('bg-canvas');
    renderer = new THREE.WebGLRenderer({ 
        canvas, 
        alpha: true,
        antialias: true 
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);
    
    // Create particle system
    createParticles();
    
    // Add floating objects
    addFloatingObjects();
    
    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
    scene.add(ambientLight);
    
    // Add point lights
    addPointLights();
    
    // Event listeners
    document.addEventListener('mousemove', onMouseMove);
    window.addEventListener('resize', onWindowResize);
    
    // Start animation loop
    animate();
}

// Create particle system
function createParticles() {
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 2000;
    
    const posArray = new Float32Array(particlesCount * 3);
    const colorsArray = new Float32Array(particlesCount * 3);
    
    for(let i = 0; i < particlesCount * 3; i += 3) {
        // Position
        posArray[i] = (Math.random() - 0.5) * 10;
        posArray[i+1] = (Math.random() - 0.5) * 10;
        posArray[i+2] = (Math.random() - 0.5) * 10;
        
        // Color - blue/purple gradient
        colorsArray[i] = Math.random() * 0.2 + 0.1; // R
        colorsArray[i+1] = Math.random() * 0.2 + 0.3; // G
        colorsArray[i+2] = Math.random() * 0.5 + 0.5; // B
    }
    
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorsArray, 3));
    
    const particlesMaterial = new THREE.PointsMaterial({
        size: 0.01,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        sizeAttenuation: true
    });
    
    particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
    scene.add(particlesMesh);
}

// Add floating geometric objects
function addFloatingObjects() {
    // Create several geometric objects
    const geometries = [
        new THREE.TorusGeometry(0.3, 0.1, 16, 100),
        new THREE.OctahedronGeometry(0.3, 0),
        new THREE.TetrahedronGeometry(0.3, 0),
        new THREE.IcosahedronGeometry(0.3, 0)
    ];
    
    // Materials with different colors
    const materials = [
        new THREE.MeshStandardMaterial({ color: 0x3b82f6, wireframe: true }),
        new THREE.MeshStandardMaterial({ color: 0x8b5cf6, wireframe: true }),
        new THREE.MeshStandardMaterial({ color: 0x06b6d4, wireframe: true }),
        new THREE.MeshStandardMaterial({ color: 0x6366f1, wireframe: true })
    ];
    
    // Create and position objects
    for (let i = 0; i < 8; i++) {
        const index = Math.floor(Math.random() * geometries.length);
        const mesh = new THREE.Mesh(geometries[index], materials[index % materials.length]);
        
        // Random position
        mesh.position.x = (Math.random() - 0.5) * 10;
        mesh.position.y = (Math.random() - 0.5) * 10;
        mesh.position.z = (Math.random() - 0.5) * 10;
        
        // Random rotation
        mesh.rotation.x = Math.random() * Math.PI;
        mesh.rotation.y = Math.random() * Math.PI;
        
        // Random scale
        const scale = Math.random() * 0.5 + 0.5;
        mesh.scale.set(scale, scale, scale);
        
        // Add custom properties for animation
        mesh.userData = {
            rotationSpeed: {
                x: (Math.random() - 0.5) * 0.002,
                y: (Math.random() - 0.5) * 0.002,
                z: (Math.random() - 0.5) * 0.002
            },
            floatSpeed: Math.random() * 0.002 + 0.001,
            floatDistance: Math.random() * 0.5 + 0.5,
            initialY: mesh.position.y
        };
        
        scene.add(mesh);
    }
}

// Add dynamic point lights
function addPointLights() {
    const colors = [0x3b82f6, 0x8b5cf6, 0x06b6d4];
    
    for (let i = 0; i < 3; i++) {
        const light = new THREE.PointLight(colors[i], 1, 10);
        light.position.set(
            (Math.random() - 0.5) * 10,
            (Math.random() - 0.5) * 10,
            (Math.random() - 0.5) * 5
        );
        
        // Add custom properties for animation
        light.userData = {
            moveSpeed: {
                x: (Math.random() - 0.5) * 0.01,
                y: (Math.random() - 0.5) * 0.01,
                z: (Math.random() - 0.5) * 0.01
            },
            intensity: {
                min: 0.5,
                max: 1.5,
                current: 1,
                speed: Math.random() * 0.01 + 0.005,
                increasing: Math.random() > 0.5
            }
        };
        
        scene.add(light);
    }
}

// Handle mouse movement
function onMouseMove(event) {
    mouseX = (event.clientX - windowHalfX) / 100;
    mouseY = (event.clientY - windowHalfY) / 100;
}

// Handle window resize
function onWindowResize() {
    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;
    
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    
    const elapsedTime = clock.getElapsedTime();
    
    // Smooth mouse movement
    targetX = mouseX * 0.5;
    targetY = mouseY * 0.5;
    
    // Rotate particle system
    particlesMesh.rotation.x += 0.0003;
    particlesMesh.rotation.y += 0.0005;
    
    // Rotate camera based on mouse position (subtle effect)
    camera.position.x += (targetX - camera.position.x) * 0.05;
    camera.position.y += (-targetY - camera.position.y) * 0.05;
    camera.lookAt(scene.position);
    
    // Animate all objects in the scene
    scene.children.forEach(object => {
        // Only animate meshes and lights with userData
        if ((object instanceof THREE.Mesh || object instanceof THREE.PointLight) && object.userData) {
            // For meshes with rotation data
            if (object.userData.rotationSpeed) {
                object.rotation.x += object.userData.rotationSpeed.x;
                object.rotation.y += object.userData.rotationSpeed.y;
                object.rotation.z += object.userData.rotationSpeed.z;
            }
            
            // For meshes with float animation
            if (object.userData.floatSpeed) {
                object.position.y = object.userData.initialY + 
                    Math.sin(elapsedTime * object.userData.floatSpeed * Math.PI) * 
                    object.userData.floatDistance;
            }
            
            // For lights with intensity animation
            if (object.userData.intensity) {
                const intensity = object.userData.intensity;
                
                if (intensity.increasing) {
                    intensity.current += intensity.speed;
                    if (intensity.current >= intensity.max) {
                        intensity.increasing = false;
                    }
                } else {
                    intensity.current -= intensity.speed;
                    if (intensity.current <= intensity.min) {
                        intensity.increasing = true;
                    }
                }
                
                object.intensity = intensity.current;
            }
            
            // For lights with movement
            if (object.userData.moveSpeed) {
                object.position.x += object.userData.moveSpeed.x;
                object.position.y += object.userData.moveSpeed.y;
                object.position.z += object.userData.moveSpeed.z;
                
                // Bounce off boundaries
                if (Math.abs(object.position.x) > 5) {
                    object.userData.moveSpeed.x *= -1;
                }
                if (Math.abs(object.position.y) > 5) {
                    object.userData.moveSpeed.y *= -1;
                }
                if (Math.abs(object.position.z) > 3) {
                    object.userData.moveSpeed.z *= -1;
                }
            }
        }
    });
    
    renderer.render(scene, camera);
}

// Initialize when DOM is loaded
window.addEventListener('load', initThreeJS);
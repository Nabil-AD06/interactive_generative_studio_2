(function () {
  var hero3d = document.getElementById('hero-3d');
  if (!hero3d) return;

  var scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x050a14, 0.002);

  var camera = new THREE.PerspectiveCamera(60, hero3d.clientWidth / hero3d.clientHeight, 1, 1000);
  camera.position.set(0, 0, 12);

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(hero3d.clientWidth, hero3d.clientHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.2;
  hero3d.appendChild(renderer.domElement);

  // ---- Lights ----
  var ambient = new THREE.AmbientLight(0x404060, 0.5);
  scene.add(ambient);

  var dirLight = new THREE.DirectionalLight(0x34d399, 2);
  dirLight.position.set(1, 2, 3);
  scene.add(dirLight);

  var dirLight2 = new THREE.DirectionalLight(0x0d9488, 1.5);
  dirLight2.position.set(-2, -1, 2);
  scene.add(dirLight2);

  var pointLight = new THREE.PointLight(0xf59e0b, 1, 20);
  pointLight.position.set(0, 0, 5);
  scene.add(pointLight);

  // ---- Materials with emerald/teal/amber palette ----
  var materials = {
    emerald: new THREE.MeshPhysicalMaterial({
      color: 0x10b981,
      metalness: 0.3,
      roughness: 0.4,
      emissive: 0x10b981,
      emissiveIntensity: 0.05,
      clearcoat: 0.3,
      clearcoatRoughness: 0.4,
    }),
    teal: new THREE.MeshPhysicalMaterial({
      color: 0x0d9488,
      metalness: 0.4,
      roughness: 0.3,
      emissive: 0x0d9488,
      emissiveIntensity: 0.05,
      clearcoat: 0.2,
      clearcoatRoughness: 0.3,
    }),
    amber: new THREE.MeshPhysicalMaterial({
      color: 0xf59e0b,
      metalness: 0.2,
      roughness: 0.5,
      emissive: 0xf59e0b,
      emissiveIntensity: 0.03,
      clearcoat: 0.4,
      clearcoatRoughness: 0.5,
    }),
    lightTeal: new THREE.MeshPhysicalMaterial({
      color: 0x5eead4,
      metalness: 0.1,
      roughness: 0.6,
      transparent: true,
      opacity: 0.8,
      emissive: 0x5eead4,
      emissiveIntensity: 0.02,
    }),
    glass: new THREE.MeshPhysicalMaterial({
      color: 0xffffff,
      metalness: 0,
      roughness: 0.1,
      transparent: true,
      opacity: 0.15,
      envMapIntensity: 1,
      clearcoat: 1,
      clearcoatRoughness: 0.1,
    }),
  };

  // ---- Objects ----
  var objects = [];

  var torusKnot = new THREE.Mesh(new THREE.TorusKnotGeometry(1.2, 0.35, 128, 16), materials.emerald);
  torusKnot.position.set(-2.5, 0.5, 0);
  scene.add(torusKnot);
  objects.push({ mesh: torusKnot, speed: 0.4, rotX: 0.3, rotY: 0.5 });

  var icosahedron = new THREE.Mesh(new THREE.IcosahedronGeometry(1.1, 0), materials.teal);
  icosahedron.position.set(2.8, -0.3, -1);
  scene.add(icosahedron);
  objects.push({ mesh: icosahedron, speed: 0.3, rotX: 0.5, rotY: 0.3 });

  var torus = new THREE.Mesh(new THREE.TorusGeometry(1.4, 0.4, 32, 64), materials.amber);
  torus.position.set(0, 1.8, -2);
  scene.add(torus);
  objects.push({ mesh: torus, speed: 0.5, rotX: 0.7, rotY: 0.2 });

  var octahedron = new THREE.Mesh(new THREE.OctahedronGeometry(0.9, 0), materials.lightTeal);
  octahedron.position.set(-1.5, -1.2, -1.5);
  scene.add(octahedron);
  objects.push({ mesh: octahedron, speed: 0.35, rotX: 0.4, rotY: 0.6 });

  var dodecahedron = new THREE.Mesh(new THREE.DodecahedronGeometry(0.8, 0), materials.glass);
  dodecahedron.position.set(1.8, 1.5, -1);
  scene.add(dodecahedron);
  objects.push({ mesh: dodecahedron, speed: 0.25, rotX: 0.6, rotY: 0.4 });

  // ---- Particles ----
  var particleCount = 1200;
  var particleGeo = new THREE.BufferGeometry();
  var positions = new Float32Array(particleCount * 3);
  var sizes = new Float32Array(particleCount);

  for (var i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 40;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 30;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 30 - 5;
    sizes[i] = Math.random() * 2 + 0.5;
  }

  particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  particleGeo.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

  var particleMat = new THREE.PointsMaterial({
    color: 0x34d399,
    size: 0.06,
    transparent: true,
    opacity: 0.6,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true,
  });

  var particles = new THREE.Points(particleGeo, particleMat);
  scene.add(particles);

  // ---- Mouse ----
  var mouseTarget = { x: 0, y: 0 };
  var mouseCurrent = { x: 0, y: 0 };

  document.addEventListener('mousemove', function (e) {
    var rect = hero3d.getBoundingClientRect();
    mouseTarget.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
    mouseTarget.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
  });

  hero3d.addEventListener('touchmove', function (e) {
    var touch = e.touches[0];
    var rect = hero3d.getBoundingClientRect();
    mouseTarget.x = ((touch.clientX - rect.left) / rect.width) * 2 - 1;
    mouseTarget.y = -((touch.clientY - rect.top) / rect.height) * 2 + 1;
  }, { passive: true });

  // ---- Resize ----
  function resize() {
    var w = hero3d.clientWidth;
    var h = hero3d.clientHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  }

  window.addEventListener('resize', resize);

  // ---- Animation ----
  var clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);

    var elapsed = clock.getElapsedTime();

    // Smooth mouse follow
    mouseCurrent.x += (mouseTarget.x - mouseCurrent.x) * 0.05;
    mouseCurrent.y += (mouseTarget.y - mouseCurrent.y) * 0.05;

    // Rotate objects
    objects.forEach(function (obj, index) {
      obj.mesh.rotation.x += obj.rotX * obj.speed * 0.008;
      obj.mesh.rotation.y += obj.rotY * obj.speed * 0.008;

      // Floating motion
      obj.mesh.position.y += Math.sin(elapsed * obj.speed + index * 2) * 0.002;
    });

    // Mouse parallax on objects
    objects.forEach(function (obj) {
      obj.mesh.rotation.x += mouseCurrent.y * 0.002;
      obj.mesh.rotation.y += mouseCurrent.x * 0.002;
    });

    // Camera orbit slightly
    camera.position.x = Math.sin(elapsed * 0.05) * 1.5 + mouseCurrent.x * 1.5;
    camera.position.y = Math.sin(elapsed * 0.03) * 0.8 + mouseCurrent.y * 1;
    camera.lookAt(0, 0, 0);

    // Pulse light
    pointLight.intensity = 0.8 + Math.sin(elapsed * 0.5) * 0.3;

    // Rotate particles slowly
    particles.rotation.y = elapsed * 0.01;

    renderer.render(scene, camera);
  }

  animate();
})();

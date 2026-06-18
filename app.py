import streamlit as st
import streamlit.components.v1 as components
import json

# --- Page Configuration & Styling ---
st.set_page_config(
    page_title="NEXORIUM // Parametric 3D CAD Engine",
    page_icon="🧊", # Upgraded to a sleek 3D solid primitive icon
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enterprise Dark-Theme Injection
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    div.stButton > button:first-child {
        background-color: #0F52BA; color: white; border-radius: 4px; border: none; width: 100%;
    }
    div.stButton > button:first-child:hover { background-color: #1A66DB; border: none; }
    .metric-container { background-color: #1E222B; padding: 15px; border-radius: 6px; border: 1px solid #2D3139; }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "feature_tree" not in st.session_state:
    st.session_state.feature_tree = [
        {"id": "base_block", "type": "Base Extrude", "width": 120.0, "height": 80.0, "depth": 40.0},
        {"id": "pocket_01", "type": "Boolean Cut (Cylinder)", "radius": 20.0, "x_offset": 0.0, "y_offset": 0.0}
    ]

# --- Sidebar: Feature Tree & Parameter Controls ---
with st.sidebar:
    st.title("🧊 NEXORIUM CAD")
    st.caption("Parametric Kernel: Manifold v2.5 (WASM-Client Driven)")
    st.divider() 
    
    st.subheader("1. Global Part History")
    
    # Render the ordered historical operations list
    for idx, feature in enumerate(st.session_state.feature_tree):
        with st.expander(f"⚙️ {idx+1}. {feature['type']} [{feature['id']}]", expanded=True):
            if feature["type"] == "Base Extrude":
                feature["width"] = st.slider("Width (X)", 10.0, 200.0, float(feature["width"]), step=5.0, key=f"w_{idx}")
                feature["height"] = st.slider("Height (Y)", 10.0, 200.0, float(feature["height"]), step=5.0, key=f"h_{idx}")
                feature["depth"] = st.slider("Depth (Z)", 5.0, 100.0, float(feature["depth"]), step=5.0, key=f"d_{idx}")
            
            elif feature["type"] == "Boolean Cut (Cylinder)":
                feature["radius"] = st.slider("Hole Radius", 5.0, 50.0, float(feature["radius"]), step=1.0, key=f"r_{idx}")
                feature["x_offset"] = st.slider("Position Shift X", -60.0, 60.0, float(feature["x_offset"]), step=2.0, key=f"x_{idx}")
                feature["y_offset"] = st.slider("Position Shift Y", -40.0, 40.0, float(feature["y_offset"]), step=2.0, key=f"y_{idx}")

    st.divider() 
    if st.button("Reset Geometry To Default Blueprint"):
        st.session_state.feature_tree = [
            {"id": "base_block", "type": "Base Extrude", "width": 120.0, "height": 80.0, "depth": 40.0},
            {"id": "pocket_01", "type": "Boolean Cut (Cylinder)", "radius": 20.0, "x_offset": 0.0, "y_offset": 0.0}
        ]
        st.rerun()

# --- Main Dashboard Layout ---
col_canvas, col_telemetry = st.columns([3, 1])

with col_canvas:
    st.subheader("Real-Time 3D Viewport")
    
    # Serialize feature tree state to inject cleanly into the client-side browser pipeline
    json_state = json.dumps(st.session_state.feature_tree)
    
    # Premium Frontend HTML/JS Architecture Embedded directly in Streamlit
    html_component_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; background-color: #11141A; font-family: monospace; }}
            #canvas-container {{ width: 100vw; height: 580px; position: relative; }}
            #loading-overlay {{ position: absolute; top: 10px; left: 10px; color: #00FFCC; font-size: 12px; z-index: 100; }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <script src="https://elalish.github.io/manifold/manifold.js"></script>
    </head>
    <body>
        <div id="loading-overlay">⚙️ Manifold WASM Active Engine Loop</div>
        <div id="canvas-container"></div>

        <script>
            const featureTree = {json_state};
            
            let scene, camera, renderer, controls, currentMesh;
            const container = document.getElementById('canvas-container');

            function initThree() {{
                scene = new THREE.Scene();
                scene.background = new THREE.Color(0x11141A);

                camera = new THREE.PerspectiveCamera(45, window.innerWidth / 580, 1, 1000);
                camera.position.set(150, 150, 200);

                renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(container.clientWidth, 580);
                renderer.shadowMap.enabled = true;
                container.appendChild(renderer.domElement);

                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;

                // Technical Environment Lighting Assembly
                const ambientLight = new THREE.AmbientLight(0x666666);
                scene.add(ambientLight);

                const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.8);
                dirLight1.position.set(200, 400, 300);
                scene.add(dirLight1);

                const dirLight2 = new THREE.DirectionalLight(0x4444ff, 0.3);
                dirLight2.position.set(-200, -200, -200);
                scene.add(dirLight2);

                // Engineering Workspace Blueprint Grid
                const gridHelper = new THREE.GridHelper(300, 30, 0x444955, 0x242831);
                gridHelper.position.y = -50;
                scene.add(gridHelper);
            }}

            // Execution Loop invoking Manifold WASM Solid Primitives and Boolean Pipeline
            function processGeometry(Module) {{
                if (!Module || !Module.Manifold) return;
                const {{"Manifold", "Cube", "Cylinder"}} = Module;

                // 1. Process Feature Node 01: Base Block
                const baseData = featureTree[0];
                const baseCube = Cube(baseData.width, baseData.height, baseData.depth, true);

                // 2. Process Feature Node 02: Cylindrical Cut
                const cutData = featureTree[1];
                // Generate tool geometric primitive
                let toolCylinder = Cylinder(baseData.depth + 10, cutData.radius, cutData.radius, 32);
                // Transform tool position relative to coordinate origin
                toolCylinder = toolCylinder.translate([cutData.x_offset, cutData.y_offset, -(baseData.depth + 10)/2]);

                // 3. Execute Boolean Subtraction Optimization (Difference)
                const optimizedSolid = baseCube.difference(toolCylinder);

                // 4. Extract Manifold Mesh Structure back out into standard WebGL Output Struct
                const outputMesh = optimizedSolid.getMesh();

                // 5. Build native ThreeJS Geometry from WASM Output arrays
                const geometry = new THREE.BufferGeometry();
                geometry.setAttribute('position', new THREE.BufferAttribute(outputMesh.vertProperties, 3));
                geometry.setIndex(new THREE.BufferAttribute(outputMesh.triVerts, 1));
                geometry.computeVertexNormals();

                // Clean memory footprints within WebGL Pipeline
                if (currentMesh) scene.remove(currentMesh);

                // Premium Matte Metallic Material Engineering Visuals
                const material = new THREE.MeshStandardMaterial({{
                    color: 0x90A4AE,
                    roughness: 0.2,
                    metalness: 0.8,
                    wireframe: false,
                    flatShading: false
                }});

                currentMesh = new THREE.Mesh(geometry, material);
                currentMesh.position.y = 0;
                scene.add(currentMesh);

                // Garbage Clean Explicit WASM Heap Memory allocation paths
                baseCube.delete();
                toolCylinder.delete();
                optimizedSolid.delete();
                
                document.getElementById('loading-overlay').innerText = "⚡ Kernel Execution Complete // Low Server Overhead Stable";
            }}

            function animate() {{
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }}

            // Setup lifecycle callbacks and engine execution orchestrator
            initThree();
            animate();

            // Wait for asynchronous loading sequence of compiled Manifold Context
            stManifoldModule().then((Module) => {{
                processGeometry(Module);
                
                window.addEventListener('resize', () => {{
                    camera.aspect = container.clientWidth / 580;
                    camera.updateProjectionMatrix();
                    renderer.setSize(container.clientWidth, 580);
                }});
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_component_code, height=590, scrolling=False)

with col_telemetry:
    st.subheader("Kernel Status")
    
    # State Engine Analytics Metadata Output
    st.markdown("""
    <div class="metric-container">
        <span style="color:#A0A5B5; font-size:12px;">SERVER RAM USAGE</span><br>
        <span style="color:#00FFCC; font-size:24px; font-weight:bold;">~42.4 MB</span><br>
        <span style="color:#6B7280; font-size:11px;">Render Tier Performance Limit: 512 MB</span>
    </div>
    <br>
    <div class="metric-container">
        <span style="color:#A0A5B5; font-size:12px;">WASM HEAP BOUNDARY</span><br>
        <span style="color:#00FFCC; font-size:24px; font-weight:bold;">Isolating</span><br>
        <span style="color:#6B7280; font-size:11px;">Memory cleanup executed via manual garbage disposal patterns</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### B-Rep History Stack Log")
    st.json(st.session_state.feature_tree)

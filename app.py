import streamlit as st
import streamlit.components.v1 as components
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="NEXORIUM // Parametric Workstation",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CAD CSS Overrides
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.2rem; padding-bottom: 1rem; }
    div.stButton > button:first-child {
        background-color: #0F52BA; color: white; border-radius: 4px; border: none; width: 100%; font-weight: bold;
    }
    div.stButton > button:first-child:hover { background-color: #1A66DB; }
    .metric-container { background-color: #1E222B; padding: 12px; border-radius: 6px; border: 1px solid #2D3139; }
    stExpander { border: 1px solid #2D3139 !important; }
    </style>
""", unsafe_allow_html=True)

# --- Parametric Engine State Initialization ---
if "feature_tree" not in st.session_state:
    st.session_state.feature_tree = [
        {"id": "base_block", "type": "Base Extrude", "width": 120.0, "height": 80.0, "depth": 40.0},
        {"id": "pocket_01", "type": "Boolean Cut (Cylinder)", "radius": 20.0, "x_offset": 0.0, "y_offset": 0.0}
    ]

# --- Sidebar: SolidEdge-Inspired Control Console ---
with st.sidebar:
    st.title("🧊 NEXORIUM CAD")
    st.caption("Parametric Workstation v2.0 // Active Session")
    st.divider()
    
    # PANEL 1: Feature History Tree & Parameters
    st.markdown("### 💾 1. Feature History Tree")
    for idx, feature in enumerate(st.session_state.feature_tree):
        with st.expander(f"⚙️ {idx+1}. {feature['type']}", expanded=(idx==0)):
            if feature["type"] == "Base Extrude":
                feature["width"] = st.slider("Width (X Axis)", 10.0, 200.0, float(feature["width"]), step=5.0, key=f"w_{idx}")
                feature["height"] = st.slider("Height (Y Axis)", 10.0, 200.0, float(feature["height"]), step=5.0, key=f"h_{idx}")
                feature["depth"] = st.slider("Extrusion Depth (Z)", 5.0, 100.0, float(feature["depth"]), step=5.0, key=f"d_{idx}")
            
            elif feature["type"] == "Boolean Cut (Cylinder)":
                feature["radius"] = st.slider("Cut Radius", 5.0, 50.0, float(feature["radius"]), step=1.0, key=f"r_{idx}")
                feature["x_offset"] = st.slider("Shift Location X", -60.0, 60.0, float(feature["x_offset"]), step=2.0, key=f"x_{idx}")
                feature["y_offset"] = st.slider("Shift Location Y", -40.0, 40.0, float(feature["y_offset"]), step=2.0, key=f"y_{idx}")

    st.divider()

    # PANEL 2: Interactive Draw Tools Selector
    st.markdown("### 🛠️ 2. Active Workspace Tool")
    active_tool = st.radio(
        "Select Active Mouse Action:",
        options=["🔍 View & Orbit Inspect", "🎯 Drop Hole Coordinate"],
        index=1,
        help="Switches the behavior of your cursor when clicking on the 3D part canvas."
    )
    
    st.divider()

    # PANEL 3: Lighting Engine & Color Schemes
    st.markdown("### 🎨 3. Part Properties & Lighting")
    object_color = st.color_picker("Material Surface Color", "#90A4AE")
    
    material_finish = st.selectbox(
        "Surface Finish Formula",
        options=["Anodized Aluminum", "Mirror Polished Steel", "High-Density Polymer"]
    )
    
    lighting_rig = st.selectbox(
        "Environment Studio Rig",
        options=["Industrial Lab (High Contrast)", "Showroom Bright (Neutral)", "Deep Space (Accent Highlights)"]
    )

    if st.button("Reset Global Blueprint Space"):
        st.session_state.feature_tree = [
            {"id": "base_block", "type": "Base Extrude", "width": 120.0, "height": 80.0, "depth": 40.0},
            {"id": "pocket_01", "type": "Boolean Cut (Cylinder)", "radius": 20.0, "x_offset": 0.0, "y_offset": 0.0}
        ]
        st.rerun()

# --- Main Modeling Viewport Interface ---
col_canvas, col_telemetry = st.columns([3, 1])

with col_canvas:
    st.subheader("Interactive B-Rep Modeler Viewport")
    
    # package metadata dictionary payload to pipe straight across the WebGL context bridge
    render_config_payload = {
        "tree": st.session_state.feature_tree,
        "color": object_color,
        "finish": material_finish,
        "lighting": lighting_rig,
        "tool": active_tool
    }
    json_payload_string = json.dumps(render_config_payload)
    
    html_component_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ margin: 0; overflow: hidden; background-color: #11141A; font-family: monospace; }}
            #canvas-container {{ width: 100vw; height: 600px; position: relative; }}
            #status-bar {{ position: absolute; bottom: 10px; left: 10px; color: #00FFCC; font-size: 11px; z-index: 100; background: rgba(27,31,43,0.85); padding: 6px 12px; border-radius: 4px; border: 1px solid #2D3139; }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    </head>
    <body>
        <div id="status-bar">SYSTEM ACTIVE // MODE: Loading Pipeline...</div>
        <div id="canvas-container"></div>

        <script>
            const sessionConfig = {json_payload_string};
            
            let scene, camera, renderer, controls, currentMesh;
            let ambientLight, primaryLight, secondaryLight;
            const container = document.getElementById('canvas-container');
            const raycaster = new THREE.Raycaster();
            const mouse = new THREE.Vector2();

            function initThreeWorkspace() {{
                scene = new THREE.Scene();
                scene.background = new THREE.Color(0x11141A);

                camera = new THREE.PerspectiveCamera(45, container.clientWidth / 600, 1, 1000);
                camera.position.set(130, 140, 180);

                renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(container.clientWidth, 600);
                renderer.shadowMap.enabled = true;
                container.appendChild(renderer.domElement);

                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;

                // Instantiate Workspace Base Light Fixtures
                ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
                scene.add(ambientLight);

                primaryLight = new THREE.DirectionalLight(0xffffff, 0.8);
                primaryLight.position.set(150, 300, 200);
                scene.add(primaryLight);

                secondaryLight = new THREE.DirectionalLight(0xffffff, 0.3);
                secondaryLight.position.set(-150, -200, -100);
                scene.add(secondaryLight);

                // Engineering Environment Grid Lines
                const gridHelper = new THREE.GridHelper(300, 30, 0x444955, 0x222630);
                gridHelper.position.y = -60;
                scene.add(gridHelper);
                
                renderer.domElement.addEventListener('pointerdown', handleCanvasInteraction);
                
                applyLightingRig(sessionConfig.lighting);
                updateStatusBarMessage();
            }}

            function applyLightingRig(preset) {{
                if (preset === "Industrial Lab (High Contrast)") {{
                    ambientLight.color.setHex(0x555555); ambientLight.intensity = 0.3;
                    primaryLight.color.setHex(0xffffff); primaryLight.intensity = 1.0; primaryLight.position.set(100, 400, 100);
                    secondaryLight.color.setHex(0x3a66ff); secondaryLight.intensity = 0.4;
                }} else if (preset === "Showroom Bright (Neutral)") {{
                    ambientLight.color.setHex(0xffffff); ambientLight.intensity = 0.6;
                    primaryLight.color.setHex(0xffffff); primaryLight.intensity = 0.7; primaryLight.position.set(200, 200, 200);
                    secondaryLight.color.setHex(0xffffff); secondaryLight.intensity = 0.3;
                }} else if (preset === "Deep Space (Accent Highlights)") {{
                    ambientLight.color.setHex(0x111122); ambientLight.intensity = 0.1;
                    primaryLight.color.setHex(0x00ffcc); primaryLight.intensity = 0.9; primaryLight.position.set(150, 200, 150);
                    secondaryLight.color.setHex(0xff007f); secondaryLight.intensity = 0.5;
                }}
            }}

            function compileSolidGeometry() {{
                const baseData = sessionConfig.tree[0];
                const cutData = sessionConfig.tree[1];

                // 2D Profile Boundary Generation
                const profileShape = new THREE.Shape();
                const w = baseData.width;
                const h = baseData.height;

                profileShape.moveTo(-w/2, -h/2);
                profileShape.lineTo(w/2, -h/2);
                profileShape.lineTo(w/2, h/2);
                profileShape.lineTo(-w/2, h/2);
                profileShape.lineTo(-w/2, -h/2);

                // Subtractive Hole Configuration Layer
                const internalHole = new THREE.Path();
                internalHole.absarc(cutData.x_offset, cutData.y_offset, cutData.radius, 0, Math.PI * 2, true);
                profileShape.holes.push(internalHole);

                const extrudeSettings = {{
                    depth: baseData.depth,
                    bevelEnabled: true,
                    bevelThickness: 1.2,
                    bevelSize: 0.4,
                    bevelSegments: 4,
                    curveSegments: 64
                }};

                const geometry = new THREE.ExtrudeGeometry(profileShape, extrudeSettings);
                geometry.computeVertexNormals();

                if (currentMesh) scene.remove(currentMesh);

                // Solid Material Matrix Compilation via Config selections
                const materialOptions = {{ color: new THREE.Color(sessionConfig.color) }};
                
                if (sessionConfig.finish === "Anodized Aluminum") {{
                    materialOptions.roughness = 0.22; materialOptions.metalness = 0.80;
                }} else if (sessionConfig.finish === "Mirror Polished Steel") {{
                    materialOptions.roughness = 0.05; materialOptions.metalness = 0.98;
                }} else if (sessionConfig.finish === "High-Density Polymer") {{
                    materialOptions.roughness = 0.60; materialOptions.metalness = 0.05;
                }}

                const customMaterial = new THREE.MeshStandardMaterial(materialOptions);
                currentMesh = new THREE.Mesh(geometry, customMaterial);
                currentMesh.position.z = -baseData.depth / 2;
                scene.add(currentMesh);
            }}

            function handleCanvasInteraction(event) {{
                // Skip processing if pointer isn't set to tool execution mode
                if (!sessionConfig.tool.includes("Drop Hole Coordinate")) return;

                const rect = renderer.domElement.getBoundingClientRect();
                mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

                raycaster.setFromCamera(mouse, camera);
                const intersections = raycaster.intersectObject(currentMesh);

                if (intersections.length > 0) {{
                    const hitPoint = intersections[0].point;
                    
                    const maxW = sessionConfig.tree[0].width / 2 - sessionConfig.tree[1].radius;
                    const maxH = sessionConfig.tree[0].height / 2 - sessionConfig.tree[1].radius;
                    
                    let constrainedX = Math.max(-maxW, Math.min(maxW, hitPoint.x));
                    let constrainedY = Math.max(-maxH, Math.min(maxH, hitPoint.y));

                    // Mutate internal javascript state coordinate tracking variables
                    sessionConfig.tree[1].x_offset = Math.round(constrainedX);
                    sessionConfig.tree[1].y_offset = Math.round(constrainedY);

                    compileSolidGeometry();
                    updateStatusBarMessage();
                }}
            }}

            function updateStatusBarMessage() {{
                const msg = `TOOL: ${{sessionConfig.tool}} // COLOR: ${{sessionConfig.color}} // RIG: ${{sessionConfig.lighting}} // HOLE POSITION -> X: ${{sessionConfig.tree[1].x_offset}} Y: ${{sessionConfig.tree[1].y_offset}}`;
                document.getElementById('status-bar').innerText = msg.toUpperCase();
            }}

            function animateWorkspace() {{
                requestAnimationFrame(animateWorkspace);
                controls.update();
                renderer.render(scene, camera);
            }}

            initThreeWorkspace();
            compileSolidGeometry();
            animateWorkspace();

            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / 600;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, 600);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_component_code, height=615, scrolling=False)

with col_telemetry:
    st.subheader("Feature Audit Panel")
    
    st.markdown(f"""
    <div class="metric-container">
        <span style="color:#A0A5B5; font-size:12px;">ACTIVE WORKSPACE MODE</span><br>
        <span style="color:#00FFCC; font-size:18px; font-weight:bold;">{active_tool.upper()}</span>
    </div>
    <br>
    <div class="metric-container">
        <span style="color:#A0A5B5; font-size:12px;">ACTIVE ENVIRONMENT RIG</span><br>
        <span style="color:#00FFCC; font-size:16px; font-weight:bold;">{lighting_rig}</span>
    </div>
    <br>
    <div class="metric-container">
        <span style="color:#A0A5B5; font-size:12px;">MATERIAL COEFFICIENT</span><br>
        <span style="color:#00FFCC; font-size:16px; font-weight:bold;">{material_finish}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Structural Geometry Tree JSON")
    st.json(st.session_state.feature_tree)

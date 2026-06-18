import streamlit as st
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(
    page_title="NEXORIUM CAD // Enterprise Workstation",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Render standard layout CSS overrides to clear Streamlit padding and maximize workspace real estate
st.markdown("""
    <style>
    .main .block-container { padding: 0rem; max-width: 100%; }
    iframe { display: block; border: none; width: 100vw; height: 100vh; }
    footer {display: none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Complete Single-File Self-Contained WebGL CAD Suite
html_workstation_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXORIUM CAD Suite</title>
    <!-- Tailwind CSS Engine -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Three.js Graphics Infrastructure -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        body { font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #11141A; }
        ::-webkit-scrollbar-thumb { background: #2D3139; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #3E4452; }
    </style>
</head>
<body class="bg-[#11141a] text-[#E2E8F0] overflow-hidden select-none">

    <!-- Top Ribbon / Control Bar (SolidEdge-style ribbon design) -->
    <header class="h-12 bg-[#171a21] border-b border-[#242831] flex items-center justify-between px-4 z-50 relative">
        <div class="flex items-center space-x-3">
            <span class="text-xl">🧊</span>
            <div>
                <h1 class="text-xs font-bold tracking-wider text-white">NEXORIUM // SOLID WORKSTATION</h1>
                <p class="text-[9px] text-[#8C93A3] uppercase tracking-widest">Active File: Part_092_Assembly.par</p>
            </div>
        </div>
        
        <!-- Primary Navigation Modules -->
        <div class="flex space-x-1 bg-[#1e232e] p-1 rounded border border-[#2d323e]">
            <button onclick="switchModule('modeling')" id="tab-modeling" class="module-tab px-3 py-1 text-xs font-medium rounded transition bg-[#2563eb] text-white">
                3D Modeling
            </button>
            <button onclick="switchModule('drafting')" id="tab-drafting" class="module-tab px-3 py-1 text-xs font-medium rounded transition text-[#8C93A3] hover:text-white">
                2D Drafting & Docs
            </button>
            <button onclick="switchModule('assembly')" id="tab-assembly" class="module-tab px-3 py-1 text-xs font-medium rounded transition text-[#8C93A3] hover:text-white">
                Assembly & Explode
            </button>
            <button onclick="switchModule('simulation')" id="tab-simulation" class="module-tab px-3 py-1 text-xs font-medium rounded transition text-[#8C93A3] hover:text-white">
                Simulation / CAE
            </button>
            <button onclick="switchModule('routing')" id="tab-routing" class="module-tab px-3 py-1 text-xs font-medium rounded transition text-[#8C93A3] hover:text-white">
                Routing & Convergent
            </button>
        </div>

        <!-- Right Side Performance Matrix -->
        <div class="flex items-center space-x-4 text-[11px] text-[#8C93A3]">
            <span class="flex items-center text-[#10B981]"><span class="w-2 h-2 rounded-full bg-[#10B981] inline-block mr-1.5 animate-pulse"></span> Render Cloud Stable</span>
            <span class="border-l border-[#242831] pl-3">WASM RAM: <strong class="text-white">12.5 MB</strong></span>
            <span class="border-l border-[#242831] pl-3">GPU Load: <strong id="gpu-telemetry" class="text-white">0%</strong></span>
        </div>
    </header>

    <!-- Main Workspace Area -->
    <div class="flex h-[calc(100vh-3rem)] w-screen relative overflow-hidden">
        
        <!-- LEFT SIDEBAR: SolidEdge Feature Tree Navigation -->
        <aside class="w-72 bg-[#171a21] border-r border-[#242831] flex flex-col z-20">
            <!-- Navigation Header -->
            <div class="p-3 bg-[#1e232e] border-b border-[#242831] flex items-center justify-between">
                <span class="text-xs font-semibold uppercase tracking-wider text-[#A0A5B5] flex items-center">
                    <i data-lucide="git-branch" class="w-3.5 h-3.5 mr-1.5 text-[#2563eb]"></i> Pathfinder tree
                </span>
                <span class="text-[10px] bg-[#2d323e] text-white px-1.5 py-0.5 rounded">Ordered</span>
            </div>

            <!-- Scrollable Tree Structure -->
            <div class="flex-1 overflow-y-auto p-2 space-y-3">
                
                <!-- Dynamic Parametric History List -->
                <div class="space-y-1">
                    <div class="flex items-center text-xs p-1.5 text-[#A0A5B5]">
                        <i data-lucide="box" class="w-3.5 h-3.5 mr-2 text-[#00FFCC]"></i>
                        <span>System Origin (0, 0, 0)</span>
                    </div>
                    
                    <!-- Base Shape Protrusion Control Header -->
                    <div id="tree-base" class="flex items-center justify-between text-xs p-2 bg-[#212631] border border-[#2a303d] rounded cursor-pointer">
                        <div class="flex items-center">
                            <i data-lucide="layers" class="w-4 h-4 mr-2 text-[#3b82f6]"></i>
                            <span id="protrusion-title" class="font-medium text-white">Protrusion 1 (Base Extrude)</span>
                        </div>
                        <i data-lucide="edit-3" class="w-3 h-3 text-[#8C93A3]"></i>
                    </div>

                    <!-- STANDARD EXTRUSION PARAMETERS PANEL -->
                    <div id="extrusion-params" class="pl-4 border-l border-[#242831] ml-4 mt-1 space-y-1 text-[11px] text-[#8C93A3]">
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Base Width (X)</span>
                            <input type="range" id="param-width" min="40" max="200" value="120" oninput="updateParameters()" class="w-20 accent-[#3b82f6]">
                        </div>
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Base Height (Y)</span>
                            <input type="range" id="param-height" min="40" max="150" value="80" oninput="updateParameters()" class="w-20 accent-[#3b82f6]">
                        </div>
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Extrude Depth (Z)</span>
                            <input type="range" id="param-depth" min="10" max="100" value="40" oninput="updateParameters()" class="w-20 accent-[#3b82f6]">
                        </div>
                    </div>

                    <!-- B-SPLINE CAR LOFT PARAMETERS PANEL -->
                    <div id="car-loft-params" class="pl-4 border-l border-[#242831] ml-4 mt-1 space-y-1 text-[11px] text-[#8C93A3] hidden">
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Car Length (Z)</span>
                            <input type="range" id="param-car-length" min="120" max="240" value="170" oninput="updateParameters()" class="w-20 accent-[#10b981]">
                        </div>
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Track Width (X)</span>
                            <input type="range" id="param-car-width" min="60" max="120" value="85" oninput="updateParameters()" class="w-20 accent-[#10b981]">
                        </div>
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Nose Height (Spline 1)</span>
                            <input type="range" id="param-nose-height" min="10" max="35" value="22" oninput="updateParameters()" class="w-20 accent-[#10b981]">
                        </div>
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Cabin Height (Spline 2)</span>
                            <input type="range" id="param-cabin-height" min="30" max="70" value="52" oninput="updateParameters()" class="w-20 accent-[#10b981]">
                        </div>
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Tail Height (Spline 3)</span>
                            <input type="range" id="param-tail-height" min="15" max="50" value="34" oninput="updateParameters()" class="w-20 accent-[#10b981]">
                        </div>
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Wheel Arch Scale</span>
                            <input type="range" id="param-wheel-arch" min="10" max="30" value="18" oninput="updateParameters()" class="w-20 accent-[#10b981]">
                        </div>
                        <div class="flex items-center space-x-2 p-1.5 mt-1 bg-[#1a202c] rounded border border-[#2d3748]">
                            <input type="checkbox" id="param-show-curves" checked onchange="updateParameters()" class="accent-[#10b981]">
                            <span class="text-[10px] text-white">Show B-Spline Guide Curves</span>
                        </div>
                    </div>
                    
                    <!-- Feature Tree: Cutout 1 -->
                    <div id="tree-cut" class="flex items-center justify-between text-xs p-2 bg-[#212631] border border-[#2a303d] rounded cursor-pointer mt-2">
                        <div class="flex items-center">
                            <i data-lucide="scissors" class="w-4 h-4 mr-2 text-[#ef4444]"></i>
                            <span class="font-medium text-white">Cutout 1 (Boolean Cut)</span>
                        </div>
                        <i data-lucide="edit-3" class="w-3 h-3 text-[#8C93A3]"></i>
                    </div>

                    <div id="cutout-params" class="pl-4 border-l border-[#242831] ml-4 mt-1 space-y-1 text-[11px] text-[#8C93A3]">
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Hole Radius</span>
                            <input type="range" id="param-radius" min="5" max="35" value="18" oninput="updateParameters()" class="w-20 accent-[#ef4444]">
                        </div>
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Pos X Offset</span>
                            <input type="range" id="param-x" min="-50" max="50" value="0" oninput="updateParameters()" class="w-20 accent-[#ef4444]">
                        </div>
                        <div class="flex justify-between items-center p-1 hover:bg-[#1a1e26] rounded">
                            <span>Pos Y Offset</span>
                            <input type="range" id="param-y" min="-30" max="30" value="0" oninput="updateParameters()" class="w-20 accent-[#ef4444]">
                        </div>
                    </div>
                </div>

                <!-- Unified Control Panel / Action Triggers context based -->
                <div class="pt-4 border-t border-[#242831] space-y-2">
                    <span class="text-[10px] font-bold text-[#8C93A3] uppercase tracking-wider block px-1">Interactive Operations</span>
                    
                    <!-- Tool Selectors -->
                    <div class="grid grid-cols-2 gap-1.5 p-1">
                        <button onclick="setWorkspaceAction('inspect')" id="act-inspect" class="action-btn text-[11px] py-1.5 px-2 bg-[#2563eb] text-white rounded font-medium flex items-center justify-center">
                            <i data-lucide="move" class="w-3 h-3 mr-1"></i> Orbit
                        </button>
                        <button onclick="setWorkspaceAction('cut')" id="act-cut" class="action-btn text-[11px] py-1.5 px-2 bg-[#212631] hover:bg-[#2c3241] rounded font-medium flex items-center justify-center text-[#A0A5B5]">
                            <i data-lucide="mouse-pointer-click" class="w-3 h-3 mr-1"></i> Place Cut
                        </button>
                    </div>

                    <div class="p-2 bg-[#1c202a] rounded border border-[#2a303d] text-[11px] text-[#8C93A3] space-y-2">
                        <span class="font-semibold text-[#A0A5B5] block">Quick Presets</span>
                        <div class="flex flex-wrap gap-1">
                            <button onclick="applyPreset('block')" class="bg-[#2d323e] hover:bg-[#383e4d] px-2 py-1 text-white rounded text-[10px]">Standard Block</button>
                            <button onclick="applyPreset('bracket')" class="bg-[#2d323e] hover:bg-[#383e4d] px-2 py-1 text-white rounded text-[10px]">Machined Bracket</button>
                            <button onclick="applyPreset('car')" class="bg-[#10b981]/20 hover:bg-[#10b981]/30 text-[#00ffcc] border border-[#10b981]/40 px-2 py-1 rounded text-[10px] font-bold w-full mt-1 flex items-center justify-center">
                                <i data-lucide="car" class="w-3.5 h-3.5 mr-1.5"></i> B-Spline Lofted Car Preset
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Appearance & Lighting Controls Quick Toggle -->
            <div class="p-3 bg-[#14161d] border-t border-[#242831] space-y-3">
                <span class="text-[10px] font-bold text-[#8C93A3] uppercase tracking-wider block">Part Properties</span>
                
                <div class="flex justify-between items-center">
                    <span class="text-xs text-[#A0A5B5]">Surface Shading</span>
                    <select id="ui-finish" onchange="updateFinish()" class="text-xs bg-[#1f2430] border border-[#2c3240] text-white p-1 rounded outline-none">
                        <option value="aluminum">Anodized Aluminum</option>
                        <option value="steel">Mirror Steel</option>
                        <option value="polymer">Matte Polymer</option>
                    </select>
                </div>
                
                <div class="flex justify-between items-center">
                    <span class="text-xs text-[#A0A5B5]">Part Color</span>
                    <input type="color" id="ui-color" value="#a5b4fc" onchange="updateColor()" class="w-7 h-5 border-none outline-none bg-transparent cursor-pointer rounded">
                </div>
            </div>
        </aside>

        <!-- CENTER VIEWPORT: Three.js Real-time 3D Matrix / Interactive Canvas -->
        <main class="flex-1 relative bg-[#11141a]">
            <!-- Dynamic Status Bar inside Canvas overlay -->
            <div id="viewport-overlay" class="absolute top-3 left-3 bg-[#171a21]/90 backdrop-blur border border-[#242831] px-3 py-1.5 rounded text-xs text-[#00FFCC] z-10 font-mono tracking-wider">
                ⚡ WORKSTATION STANDBY // READY FOR SOLID-EDIT MODELING
            </div>

            <div id="canvas-wrapper" class="w-full h-full"></div>

            <!-- Bottom Control Overlay: Flat Pattern / Exp View sliders -->
            <div id="bottom-hud" class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-[#171a21]/90 backdrop-blur border border-[#242831] p-3 rounded-lg flex items-center space-x-6 z-10 max-w-lg shadow-2xl transition-opacity duration-300">
                <div class="flex items-center space-x-2">
                    <span class="text-xs text-[#A0A5B5] font-semibold">Active Mode Slider:</span>
                    <input type="range" id="hud-slider" min="0" max="100" value="0" oninput="handleHudSlider(this.value)" class="w-48 accent-[#2563eb]">
                </div>
                <div id="hud-label" class="text-xs text-white font-mono">
                    PROTRUSION EXPLOSION: 0%
                </div>
            </div>
        </main>

        <!-- RIGHT PANEL: Multi-context Module Systems Toolboxes -->
        <aside class="w-80 bg-[#171a21] border-l border-[#242831] flex flex-col z-20">
            <!-- Active Module Interface Panel -->
            <div class="flex-1 flex flex-col min-h-0">
                
                <!-- 1. 3D Core Modeling Sub-Features Container -->
                <div id="panel-modeling" class="module-panel flex-1 flex flex-col">
                    <div class="p-3 bg-[#1e232e] border-b border-[#242831]">
                        <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center">
                            <i data-lucide="cpu" class="w-4 h-4 mr-1.5 text-[#3b82f6]"></i> Synchronous Engine
                        </span>
                    </div>
                    <div class="p-3 space-y-4 flex-1 overflow-y-auto text-xs">
                        <!-- Synchronous Mode selection -->
                        <div class="bg-[#1e232e] border border-[#2a303d] p-3 rounded-lg space-y-2">
                            <h3 class="font-bold text-white">Synchronous Technology</h3>
                            <p class="text-[11px] text-[#8C93A3] leading-relaxed">Modify faces directly without structural history recalculation penalty. Click geometry surface to relocate geometric coordinate anchors instantly.</p>
                            <div class="flex space-x-2 pt-1">
                                <button class="flex-1 py-1 px-2 rounded bg-[#2563eb] hover:bg-[#3b82f6] text-white font-medium text-[10px] uppercase">Lock Plane</button>
                                <button class="flex-1 py-1 px-2 rounded bg-[#2d323e] hover:bg-[#383e4d] text-white font-medium text-[10px] uppercase">Sync Align</button>
                            </div>
                        </div>

                        <!-- Specialty Sheet Metal Flange tools -->
                        <div class="bg-[#1c202a] border border-[#2a303d] p-3 rounded-lg space-y-2">
                            <div class="flex justify-between items-center">
                                <h3 class="font-bold text-white">Sheet Metal Form</h3>
                                <span class="bg-[#ef4444]/20 text-[#fca5a5] text-[9px] px-1.5 py-0.5 rounded font-mono font-bold">SMART BEND</span>
                            </div>
                            <p class="text-[11px] text-[#8C93A3]">Add bend relieve offsets, tab-and-slot joinery profiles, and export exact flat pattern maps instantly.</p>
                            <div class="space-y-1.5 pt-1">
                                <button onclick="triggerSheetMetalPattern()" class="w-full py-1.5 px-2 bg-[#2d323e] hover:bg-[#383e4d] rounded text-white font-mono text-[10px] uppercase flex items-center justify-center">
                                    <i data-lucide="scissors" class="w-3.5 h-3.5 mr-1.5 text-[#ef4444]"></i> Generate Flat Pattern
                                </button>
                            </div>
                        </div>

                        <!-- Generative Design Module -->
                        <div class="bg-[#1c202a] border border-[#2a303d] p-3 rounded-lg space-y-2">
                            <h3 class="font-bold text-white">Generative Topology Optimizer</h3>
                            <p class="text-[11px] text-[#8C93A3]">Uses built-in structural force vectors to computationally carve material away, rendering lightweight components optimized for stress distribution.</p>
                            <button onclick="triggerTopologyOptimization()" class="w-full py-2 px-2 bg-[#10b981] hover:bg-[#34d399] rounded text-[#11141a] font-bold text-[10px] uppercase flex items-center justify-center">
                                <i data-lucide="sparkles" class="w-3.5 h-3.5 mr-1.5"></i> Run Topology Optimization
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 2. 2D Drafting & Automatic Drawing Panel -->
                <div id="panel-drafting" class="module-panel flex-1 flex flex-col hidden">
                    <div class="p-3 bg-[#1e232e] border-b border-[#242831]">
                        <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center">
                            <i data-lucide="file-text" class="w-4 h-4 mr-1.5 text-[#10B981]"></i> Intelligent Drafting
                        </span>
                    </div>
                    <div class="p-3 space-y-4 flex-1 overflow-y-auto text-xs">
                        <div class="bg-[#1c202a] border border-[#2a303d] p-3 rounded-lg space-y-2">
                            <h3 class="font-bold text-white text-[12px]">Auto-Orthographic Drafting</h3>
                            <p class="text-[11px] text-[#8C93A3]">Real-time generation of Front, Side, and Isometric views mapped cleanly with live dimensioning and tolerances.</p>
                            <button onclick="trigger2DDraftingLayout()" class="w-full py-2 px-2 bg-[#10B981] text-[#11141a] font-bold rounded text-[10px] uppercase flex items-center justify-center">
                                <i data-lucide="layout" class="w-3.5 h-3.5 mr-1.5"></i> Project 2D Sheets (90%)
                            </button>
                        </div>

                        <!-- Tolerance matrix details -->
                        <div class="bg-[#1c202a] p-3 border border-[#2a303d] rounded-lg space-y-2">
                            <h3 class="font-bold text-white">Fit Class & Tolerances</h3>
                            <div class="grid grid-cols-2 gap-1.5 text-[10px] font-mono text-[#A0A5B5]">
                                <div class="bg-[#14161d] p-1.5 rounded">Hole Fit: <strong class="text-[#00FFCC]">H7</strong></div>
                                <div class="bg-[#14161d] p-1.5 rounded">Shaft Fit: <strong class="text-[#00FFCC]">g6</strong></div>
                                <div class="bg-[#14161d] p-1.5 rounded">Limit Max: <strong class="text-white">+0.021</strong></div>
                                <div class="bg-[#14161d] p-1.5 rounded">Limit Min: <strong class="text-white">-0.009</strong></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 3. Assembly & exploded view management -->
                <div id="panel-assembly" class="module-panel flex-1 flex flex-col hidden">
                    <div class="p-3 bg-[#1e232e] border-b border-[#242831]">
                        <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center">
                            <i data-lucide="package" class="w-4 h-4 mr-1.5 text-[#f59e0b]"></i> Large Assembly Manager
                        </span>
                    </div>
                    <div class="p-3 space-y-4 flex-1 overflow-y-auto text-xs">
                        <div class="bg-[#1c202a] border border-[#2a303d] p-3 rounded-lg space-y-2">
                            <h3 class="font-bold text-white">Large Assembly Optimization</h3>
                            <p class="text-[11px] text-[#8C93A3]">Accelerate frames using custom simplified proxy geometry. Supports rendering parts with over 10,000 subcomponents.</p>
                            <div class="flex items-center justify-between text-[11px] bg-[#14161d] p-1.5 rounded font-mono">
                                <span>Total Part Count:</span>
                                <span class="text-[#f59e0b] font-bold">12,450 pcs</span>
                            </div>
                        </div>

                        <!-- Exploded views configuration -->
                        <div class="bg-[#1c202a] border border-[#2a303d] p-3 rounded-lg space-y-2">
                            <h3 class="font-bold text-white">Dynamic Assembly Exploder</h3>
                            <p class="text-[11px] text-[#8C93A3]">Toggle spatial linear displacement along vectors to explode complex subassemblies dynamically for visualization.</p>
                            <button onclick="triggerExplodedView()" class="w-full py-1.5 px-2 bg-[#f59e0b] text-[#11141a] font-bold rounded text-[10px] uppercase flex items-center justify-center">
                                <i data-lucide="layout-grid" class="w-3.5 h-3.5 mr-1.5"></i> Explode Assembly Views
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 4. Finite Element Analysis Simulation CAE -->
                <div id="panel-simulation" class="module-panel flex-1 flex flex-col hidden">
                    <div class="p-3 bg-[#1e232e] border-b border-[#242831]">
                        <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center">
                            <i data-lucide="shield-alert" class="w-4 h-4 mr-1.5 text-[#a855f7]"></i> CAE Stress & FEA Analysis
                        </span>
                    </div>
                    <div class="p-3 space-y-4 flex-1 overflow-y-auto text-xs">
                        <div class="bg-[#1c202a] border border-[#2a303d] p-3 rounded-lg space-y-2">
                            <h3 class="font-bold text-white text-[12px]">Von Mises Finite Element Solver</h3>
                            <p class="text-[11px] text-[#8C93A3]">Simulate structural loads to find stress deformation hotspots directly on the mathematical solid boundaries.</p>
                            
                            <div class="space-y-2 pt-1">
                                <button onclick="triggerStressSimulation()" class="w-full py-2 px-2 bg-[#a855f7] hover:bg-[#c084fc] text-white font-bold rounded text-[10px] uppercase flex items-center justify-center">
                                    <i data-lucide="zap" class="w-3.5 h-3.5 mr-1.5"></i> Compute Structural Stress (FEA)
                                </button>
                                <button onclick="clearFEAMesh()" class="w-full py-1 px-2 bg-[#2d323e] hover:bg-[#383e4d] rounded text-white text-[9px] uppercase">
                                    Clear CAE Analysis
                                </button>
                            </div>
                        </div>

                        <!-- Real-time metrics -->
                        <div class="bg-[#1c202a] p-3 border border-[#2a303d] rounded-lg space-y-1.5 text-[11px] font-mono text-[#8C93A3]">
                            <div class="flex justify-between border-b border-[#242831] pb-1">
                                <span>Max Stress (MPa):</span>
                                <span class="text-[#ef4444] font-bold">245.4</span>
                            </div>
                            <div class="flex justify-between border-b border-[#242831] pb-1">
                                <span>Deformation Factor:</span>
                                <span class="text-white">0.032 mm</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Safety Factor Target:</span>
                                <span class="text-[#10b981] font-bold">2.8</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 5. Advanced Routing Systems & Convergent Module -->
                <div id="panel-routing" class="module-panel flex-1 flex flex-col hidden">
                    <div class="p-3 bg-[#1e232e] border-b border-[#242831]">
                        <span class="text-xs font-bold text-white uppercase tracking-wider flex items-center">
                            <i data-lucide="waypoints" class="w-4 h-4 mr-1.5 text-[#ec4899]"></i> Specialized Systems
                        </span>
                    </div>
                    <div class="p-3 space-y-4 flex-1 overflow-y-auto text-xs">
                        <div class="bg-[#1c202a] border border-[#2a303d] p-3 rounded-lg space-y-2">
                            <h3 class="font-bold text-white">Convergent Mesh Hybridizing</h3>
                            <p class="text-[11px] text-[#8C93A3]">Smoothly merge traditional solid B-Rep geometric features with scanned point clouds, and topological lattices.</p>
                            <button onclick="triggerConvergentMesh()" class="w-full py-2 px-2 bg-[#ec4899] text-white font-bold rounded text-[10px] uppercase flex items-center justify-center">
                                <i data-lucide="merge" class="w-3.5 h-3.5 mr-1.5"></i> Insert Convergent Mesh Layer
                            </button>
                        </div>

                        <!-- Specialized routing environments -->
                        <div class="bg-[#1c202a] border border-[#2a303d] p-3 rounded-lg space-y-2">
                            <h3 class="font-bold text-white">Dynamic 3D Wiring/PCB Routing</h3>
                            <p class="text-[11px] text-[#8C93A3]">Renders custom 3D electrical paths directly mapped around solid components with automated collision warning system.</p>
                            <button onclick="triggerRoutingWire()" class="w-full py-1.5 px-2 bg-[#2d323e] hover:bg-[#383e4d] rounded text-white text-[10px] uppercase flex items-center justify-center">
                                <i data-lucide="cable" class="w-3.5 h-3.5 mr-1.5"></i> Path-Find 3D Harness
                            </button>
                        </div>
                    </div>
                </div>

            </div>

            <!-- SolidEdge X Integrated AI Assistant Workspace (Secure Cloud Chat API interface mock) -->
            <div class="h-60 bg-[#13151c] border-t border-[#242831] flex flex-col">
                <div class="p-2.5 bg-[#171a21] border-b border-[#242831] flex justify-between items-center">
                    <span class="text-[10px] font-bold text-white uppercase tracking-wider flex items-center">
                        <i data-lucide="sparkles" class="w-3 h-3 mr-1.5 text-[#2563eb]"></i> SolidEdge X AI Assistant
                    </span>
                    <span class="text-[9px] text-[#2563eb] font-mono">Secure API Cloud Node</span>
                </div>
                
                <!-- Chat Window Logs -->
                <div id="ai-chat-box" class="flex-1 overflow-y-auto p-2.5 text-[11px] space-y-2 font-mono">
                    <div class="text-[#8C93A3]">
                        <strong class="text-[#2563eb]">SolidEdge_X_Bot:</strong> I'm listening. Ask me to "Add stress factor," "Extrude part," "Render flat pattern," "Loft B-splines," or "Generate 2D draft view."
                    </div>
                </div>

                <!-- Live Command Prompt Bar -->
                <div class="p-2 border-t border-[#242831] flex items-center space-x-1">
                    <input type="text" id="ai-command" placeholder="Enter CAD operational prompts..." class="flex-1 bg-[#1c202a] border border-[#2d323e] rounded p-1.5 text-xs text-white outline-none focus:border-[#2563eb] font-mono">
                    <button onclick="sendAICommand()" class="bg-[#2563eb] hover:bg-[#3b82f6] p-1.5 rounded text-white">
                        <i data-lucide="send" class="w-3.5 h-3.5"></i>
                    </button>
                </div>
            </div>
        </aside>

    </div>

    <!-- Initialization and Interactivity Script -->
    <script>
        // Setup state vectors for active model features
        const defaultState = {
            width: 120,
            height: 80,
            depth: 40,
            radius: 18,
            x: 0,
            y: 0,
            color: '#a5b4fc',
            finish: 'aluminum',
            action: 'inspect', // inspect or cut
            module: 'modeling', // modeling, drafting, assembly, simulation, routing
            modelType: 'extrude', // extrude or car_loft
            
            // Parametric Loft specific fields
            carLength: 170,
            carWidth: 85,
            noseHeight: 22,
            cabinHeight: 52,
            tailHeight: 34,
            wheelArchScale: 18,
            showCurves: true
        };

        let state = { ...defaultState };

        // Graphics system setup variables
        let scene, camera, renderer, controls, workspaceMesh;
        let ambientLight, mainLight, fillLight;
        let splineHelpers = []; // Visualizes the 2D B-spline curves defining loft segments
        let wireMesh = null; // Routing wires indicator
        let explosionOffset = 0; // Large assemblies slide value

        const container = document.getElementById('canvas-wrapper');

        function initThreeWorkspace() {
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x11141a);

            camera = new THREE.PerspectiveCamera(40, container.clientWidth / container.clientHeight, 1, 1000);
            camera.position.set(160, 150, 210);

            renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);

            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;

            // Rig robust workbench lighting environments
            ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
            scene.add(ambientLight);

            mainLight = new THREE.DirectionalLight(0xffffff, 0.85);
            mainLight.position.set(150, 300, 200);
            scene.add(mainLight);

            fillLight = new THREE.DirectionalLight(0x3b82f6, 0.35);
            fillLight.position.set(-150, -200, -100);
            scene.add(fillLight);

            // Floor Blueprint reference grid
            const floorGrid = new THREE.GridHelper(300, 30, 0x2d323e, 0x1a1d25);
            floorGrid.position.y = -50;
            scene.add(floorGrid);

            // Hook direct pointing raycast events
            renderer.domElement.addEventListener('pointerdown', handleViewportInteraction);
            
            // Start telemetries monitoring loop
            requestAnimationFrame(renderLoop);
            updateTelemetry();
        }

        function updateTelemetry() {
            setInterval(() => {
                const dummyLoad = Math.floor(Math.random() * 25) + 5;
                document.getElementById('gpu-telemetry').innerText = `${dummyLoad}%`;
            }, 1500);
        }

        // Clean up visual helpers
        function clearSplineHelpers() {
            splineHelpers.forEach(helper => scene.remove(helper));
            splineHelpers = [];
        }

        // Helper function: Build a smooth CatmullRom spline from control points for visualization
        function drawGuideSpline(points, colorHex = 0x00FFCC) {
            const curve = new THREE.CatmullRomCurve3(points, true); // closed spline loop
            const geometry = new THREE.BufferGeometry().setFromPoints(curve.getPoints(50));
            const material = new THREE.LineBasicMaterial({ color: colorHex, linewidth: 2 });
            const line = new THREE.Line(geometry, material);
            scene.add(line);
            splineHelpers.push(line);
        }

        // Analytical Solid Reconstruction Engine (Runs direct geometry updates instantly)
        function compilePartGeometry() {
            clearRoutingMeshes();
            clearSplineHelpers();

            let partGeometry;

            // Set up Material properties
            const materialSettings = { color: new THREE.Color(state.color) };
            if (state.finish === 'aluminum') {
                materialSettings.roughness = 0.22;
                materialSettings.metalness = 0.80;
            } else if (state.finish === 'steel') {
                materialSettings.roughness = 0.05;
                materialSettings.metalness = 0.98;
            } else if (state.finish === 'polymer') {
                materialSettings.roughness = 0.65;
                materialSettings.metalness = 0.05;
            }

            // OPTION A: B-SPLINE MULTI-SECTION LOFT ENGINE (Sleek Parametric Supercar Body)
            if (state.modelType === 'car_loft') {
                const numSlices = 18;  // Density of Z stations
                const numRotations = 40; // Radial density per section

                const loftGeometry = new THREE.BufferGeometry();
                const vertices = [];
                const indices = [];

                // Math matrices computing coordinates directly based on control splines
                const len = state.carLength;
                const width = state.carWidth;
                const hNose = state.noseHeight;
                const hCabin = state.cabinHeight;
                const hTail = state.tailHeight;
                const archSize = state.wheelArchScale;

                // Define 4 structural cross-section stations along Z depth
                // Station points map: [X, Y, Z]
                const createSectionPoints = (zPos, baseW, peakH, flatTopFactor = 0.5) => {
                    const sectionPts = [];
                    for (let i = 0; i <= numRotations; i++) {
                        const theta = (i / numRotations) * Math.PI * 2;
                        let x = Math.sin(theta) * (baseW / 2);
                        let y = Math.cos(theta) * peakH;

                        // Create flat floor underframe
                        if (y < -12) {
                            y = -12;
                        }
                        
                        // Aero dynamic cabin crest adjustments
                        if (y > 0 && Math.abs(x) < baseW * 0.35) {
                            y += (1.0 - Math.abs(x) / (baseW * 0.35)) * flatTopFactor * 8;
                        }

                        // Wheel arch coordinate recess calculation
                        const normZ = zPos / (len / 2); // -1 to 1 range
                        const isFrontArch = (normZ > -0.65 && normZ < -0.35);
                        const isRearArch = (normZ > 0.35 && normZ < 0.65);
                        
                        if ((isFrontArch || isRearArch) && Math.abs(x) > (baseW / 2) * 0.85 && y < 5) {
                            // Subtractive arch profile sculpt
                            x *= 0.80;
                            y += Math.max(0, archSize - Math.abs(y + 12));
                        }

                        sectionPts.push(new THREE.Vector3(x, y, zPos));
                    }
                    return sectionPts;
                };

                // Generate and Cache B-spline Stations
                const sections = [];
                for (let slice = 0; slice <= numSlices; slice++) {
                    const t = slice / numSlices; // 0 to 1 parameter
                    const z = -len/2 + t * len;

                    // Compute dynamic profile parameters at this specific slice via spline interpolation
                    let currentWidth = width * 0.55;
                    let currentHeight = 12;
                    let topFlatFactor = 0.1;

                    if (t < 0.3) {
                        // Nose segment: Loft from tip to front windshield
                        const localT = t / 0.3;
                        currentWidth = width * (0.35 + 0.45 * localT);
                        currentHeight = 10 + (hNose - 10) * localT;
                    } else if (t < 0.65) {
                        // Cabin greenhouse segment: Sweeps up to peakH
                        const localT = (t - 0.3) / 0.35;
                        currentWidth = width * (0.80 + 0.20 * Math.sin(localT * Math.PI / 2));
                        currentHeight = hNose + (hCabin - hNose) * Math.sin(localT * Math.PI / 2);
                        topFlatFactor = 1.2 * Math.sin(localT * Math.PI);
                    } else {
                        // Tail spoiler deck: Loft down to tail deck and curl spoiler lip
                        const localT = (t - 0.65) / 0.35;
                        currentWidth = width * (1.0 - 0.40 * localT);
                        currentHeight = hCabin - (hCabin - hTail) * localT;
                        if (localT > 0.85) {
                            currentHeight += (localT - 0.85) * 12; // Spoiler lip curl kick!
                        }
                    }

                    const pts = createSectionPoints(z, currentWidth, currentHeight, topFlatFactor);
                    sections.push(pts);

                    // Render Cyan Control Guide Curves visually to illustrate CAD operations
                    if (state.showCurves && (slice === 0 || slice === Math.floor(numSlices * 0.3) || slice === Math.floor(numSlices * 0.65) || slice === numSlices)) {
                        drawGuideSpline(pts, 0x00FFCC);
                    }
                }

                // Generate lofted mesh surface vertices array
                for (let s = 0; s <= numSlices; s++) {
                    const currentSection = sections[s];
                    for (let r = 0; r <= numRotations; r++) {
                        const pt = currentSection[r];
                        vertices.push(pt.x, pt.y, pt.z);
                    }
                }

                // Compile triangle face indices over the double-interpolated B-spline grid
                for (let s = 0; s < numSlices; s++) {
                    for (let r = 0; r < numRotations; r++) {
                        const currentIdx = s * (numRotations + 1) + r;
                        const nextSliceIdx = (s + 1) * (numRotations + 1) + r;

                        // Face 1
                        indices.push(currentIdx, nextSliceIdx, currentIdx + 1);
                        // Face 2
                        indices.push(currentIdx + 1, nextSliceIdx, nextSliceIdx + 1);
                    }
                }

                loftGeometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
                loftGeometry.setIndex(indices);
                loftGeometry.computeVertexNormals();

                partGeometry = loftGeometry;

            // OPTION B: STANDARD EXTRUSION BLOCK ENGINE (Original Part)
            } else {
                const w = state.width;
                const h = state.height;

                const partOutline = new THREE.Shape();
                partOutline.moveTo(-w/2, -h/2);
                partOutline.lineTo(w/2, -h/2);
                partOutline.lineTo(w/2, h/2);
                partOutline.lineTo(-w/2, h/2);
                partOutline.lineTo(-w/2, -h/2);

                // Subtractive Circle
                const cutoutCircle = new THREE.Path();
                cutoutCircle.absarc(state.x, state.y, state.radius, 0, Math.PI * 2, true);
                partOutline.holes.push(cutoutCircle);

                const settings = {
                    depth: state.depth,
                    bevelEnabled: true,
                    bevelThickness: 1.5,
                    bevelSize: 0.5,
                    bevelSegments: 4,
                    curveSegments: 64
                };

                partGeometry = new THREE.ExtrudeGeometry(partOutline, settings);
                partGeometry.computeVertexNormals();
            }

            if (workspaceMesh) scene.remove(workspaceMesh);

            const modelMaterial = new THREE.MeshStandardMaterial(materialSettings);
            workspaceMesh = new THREE.Mesh(partGeometry, modelMaterial);
            
            // Positioning adjust
            if (state.modelType === 'car_loft') {
                workspaceMesh.position.set(0, 10, 0);
            } else {
                workspaceMesh.position.set(0, 0, -state.depth / 2);
            }
            
            // Explode View displacement offsets
            if (state.module === 'assembly') {
                workspaceMesh.position.y += explosionOffset;
            }

            scene.add(workspaceMesh);
        }

        // Switch Module Context Architecture (SolidEdge interface tab triggers)
        function switchModule(moduleName) {
            state.module = moduleName;
            
            // Class style modifiers on tabs
            document.querySelectorAll('.module-tab').forEach(tab => {
                tab.classList.remove('bg-[#2563eb]', 'text-white');
                tab.classList.add('text-[#8C93A3]');
            });
            const activeTab = document.getElementById(`tab-${moduleName}`);
            activeTab.classList.add('bg-[#2563eb]', 'text-white');
            activeTab.classList.remove('text-[#8C93A3]');

            // Manage toolpanels Visibility
            document.querySelectorAll('.module-panel').forEach(panel => {
                panel.classList.add('hidden');
            });
            document.getElementById(`panel-${moduleName}`).classList.remove('hidden');

            // Handle unique HUD display overlays per module context
            const bottomHud = document.getElementById('bottom-hud');
            const hudSlider = document.getElementById('hud-slider');
            const hudLabel = document.getElementById('hud-label');

            if (moduleName === 'assembly') {
                bottomHud.classList.remove('opacity-0');
                hudSlider.value = explosionOffset;
                hudLabel.innerText = `EXPLODED OFFSET: ${explosionOffset}mm`;
            } else if (moduleName === 'drafting') {
                bottomHud.classList.add('opacity-0');
                trigger2DDraftingLayout();
            } else {
                bottomHud.classList.add('opacity-0');
            }

            clearStressHeatmaps();
            compilePartGeometry();
            
            logToAIChat("System", `Switched to workspace module [${moduleName.toUpperCase()}]`);
        }

        // Direct Point-and-Click Synchronous Technology (Direct Face Editing)
        function handleViewportInteraction(event) {
            if (state.action !== 'cut') return;

            const rect = renderer.domElement.getBoundingClientRect();
            const pointer = new THREE.Vector2();
            pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

            const activeRaycast = new THREE.Raycaster();
            activeRaycast.setFromCamera(pointer, camera);
            
            const results = activeRaycast.intersectObject(workspaceMesh);
            if (results.length > 0) {
                const intersectionPoint = results[0].point;
                
                // Boundaries limit checks
                const safetyBoundaryW = state.width / 2 - state.radius;
                const safetyBoundaryH = state.height / 2 - state.radius;

                state.x = Math.max(-safetyBoundaryW, Math.min(safetyBoundaryW, Math.round(intersectionPoint.x)));
                state.y = Math.max(-safetyBoundaryH, Math.min(safetyBoundaryH, Math.round(intersectionPoint.y)));

                // Sync controls
                document.getElementById('param-x').value = state.x;
                document.getElementById('param-y').value = state.y;

                compilePartGeometry();
                setWorkspaceAction('inspect'); // Safety orbit rotation

                logToAIChat("System", `Synchronous action: Recalculated cut center coordinates to X: ${state.x} | Y: ${state.y}`);
                updateHUDStatus(`🎯 Synchronous Move: Cut 1 shifted -> [X: ${state.x}, Y: ${state.y}]`);
            }
        }

        // Dynamic State synchronizer
        function updateParameters() {
            if (state.modelType === 'car_loft') {
                state.carLength = parseFloat(document.getElementById('param-car-length').value);
                state.carWidth = parseFloat(document.getElementById('param-car-width').value);
                state.noseHeight = parseFloat(document.getElementById('param-nose-height').value);
                state.cabinHeight = parseFloat(document.getElementById('param-cabin-height').value);
                state.tailHeight = parseFloat(document.getElementById('param-tail-height').value);
                state.wheelArchScale = parseFloat(document.getElementById('param-wheel-arch').value);
                state.showCurves = document.getElementById('param-show-curves').checked;
            } else {
                state.width = parseFloat(document.getElementById('param-width').value);
                state.height = parseFloat(document.getElementById('param-height').value);
                state.depth = parseFloat(document.getElementById('param-depth').value);
            }
            
            state.radius = parseFloat(document.getElementById('param-radius').value);
            state.x = parseFloat(document.getElementById('param-x').value);
            state.y = parseFloat(document.getElementById('param-y').value);

            compilePartGeometry();
            updateHUDStatus(`⚡ CAD geometric parameters recalculated dynamically.`);
        }

        function setWorkspaceAction(actionType) {
            state.action = actionType;
            document.querySelectorAll('.action-btn').forEach(btn => {
                btn.classList.remove('bg-[#2563eb]', 'text-white');
                btn.classList.add('bg-[#212631]', 'text-[#A0A5B5]');
            });

            const activeBtn = document.getElementById(`act-${actionType}`);
            activeBtn.classList.add('bg-[#2563eb]', 'text-white');
            activeBtn.classList.remove('bg-[#212631]', 'text-[#A0A5B5]');

            if (actionType === 'cut') {
                updateHUDStatus("🎯 MOUSE HOVER: Click anywhere on the silver model face to relocate cut feature.");
            } else {
                updateHUDStatus("🔍 MODE: Standard View/Orbit Orbit control.");
            }
        }

        function updateFinish() {
            state.finish = document.getElementById('ui-finish').value;
            compilePartGeometry();
        }

        function updateColor() {
            state.color = document.getElementById('ui-color').value;
            compilePartGeometry();
        }

        function updateHUDStatus(message) {
            document.getElementById('viewport-overlay').innerText = message.toUpperCase();
        }

        function handleHudSlider(value) {
            explosionOffset = value / 1.5;
            document.getElementById('hud-label').innerText = `EXPLODED OFFSET: ${Math.round(explosionOffset)}mm`;
            compilePartGeometry();
        }

        // CAE Finite Element Solver Simulation UI Mesh
        function triggerStressSimulation() {
            clearStressHeatmaps();
            
            const meshGeometry = workspaceMesh.geometry;
            const positions = meshGeometry.attributes.position;
            const vertexCount = positions.count;

            const stressColors = [];
            for (let i = 0; i < vertexCount; i++) {
                const vx = positions.getX(i);
                const vy = positions.getY(i);
                const vz = positions.getZ(i);
                
                let deltaStress = 0.1;
                
                if (state.modelType === 'car_loft') {
                    // Simulate aerodynamic stress drag forces concentrated on windshield base and front scoop nose
                    const distToWindshield = Math.sqrt(Math.pow(vy - state.noseHeight, 2) + Math.pow(vz + 15, 2));
                    const noseImpact = Math.exp(-Math.pow(vz + state.carLength/2, 2)/400);
                    deltaStress = Math.max(0.08, 0.9 * Math.exp(-distToWindshield/30) + 0.75 * noseImpact);
                } else {
                    // Standard block stress concentrators
                    const distanceToCut = Math.sqrt(Math.pow(vx - state.x, 2) + Math.pow(vy - state.y, 2));
                    deltaStress = Math.exp(-distanceToCut / (state.radius * 2.2));
                }

                const colorValue = new THREE.Color();
                if (deltaStress > 0.6) {
                    colorValue.setRGB(1.0, (1 - deltaStress) * 2, 0.0); // Hot red stress peak
                } else if (deltaStress > 0.25) {
                    colorValue.setRGB(deltaStress * 1.5, 0.8, 0.2); // Mid warning orange
                } else {
                    colorValue.setRGB(0.1, 0.3, 0.8); // Cold static safety blue
                }

                stressColors.push(colorValue.r, colorValue.g, colorValue.b);
            }

            meshGeometry.setAttribute('color', new THREE.Float32BufferAttribute(stressColors, 3));
            
            workspaceMesh.material = new THREE.MeshStandardMaterial({
                vertexColors: true,
                roughness: 0.3,
                metalness: 0.2
            });

            logToAIChat("System", "Finite Element Method (FEM) solver complete. Aerodynamic stress vectors successfully simulated and mapped.");
            updateHUDStatus("📊 FEM/CAE AIR DRAG STRESS SIMULATION MAPPED");
        }

        function clearFEAMesh() {
            clearStressHeatmaps();
            updateHUDStatus("⚡ Stress mesh telemetry cleared.");
        }

        function clearStressHeatmaps() {
            if (workspaceMesh) {
                const cleanMat = { color: new THREE.Color(state.color) };
                if (state.finish === 'aluminum') {
                    cleanMat.roughness = 0.22; cleanMat.metalness = 0.80;
                } else if (state.finish === 'steel') {
                    cleanMat.roughness = 0.05; cleanMat.metalness = 0.98;
                } else {
                    cleanMat.roughness = 0.65; cleanMat.metalness = 0.05;
                }
                workspaceMesh.material = new THREE.MeshStandardMaterial(cleanMat);
                if (workspaceMesh.geometry.attributes.color) {
                    workspaceMesh.geometry.removeAttribute('color');
                }
            }
        }

        // Specialized 3D Wiring PCB/Harness Routing Environment
        function triggerRoutingWire() {
            clearRoutingMeshes();

            let pathSpline;
            if (state.modelType === 'car_loft') {
                // Route wiring harness down the central transmission tunnel
                pathSpline = new THREE.CatmullRomCurve3([
                    new THREE.Vector3(0, -6, -state.carLength/2 - 10),
                    new THREE.Vector3(0, -8, -15),
                    new THREE.Vector3(0, -8, 20),
                    new THREE.Vector3(0, -4, state.carLength/2 + 10)
                ]);
            } else {
                pathSpline = new THREE.CatmullRomCurve3([
                    new THREE.Vector3(-state.width/2 - 20, 10, 10),
                    new THREE.Vector3(state.x - state.radius - 5, state.y + 10, state.depth/2 + 10),
                    new THREE.Vector3(state.x + state.radius + 5, state.y - 10, state.depth/2 + 20),
                    new THREE.Vector3(state.width/2 + 25, -20, -10)
                ]);
            }

            const routingGeometry = new THREE.TubeGeometry(pathSpline, 64, 2.5, 12, false);
            const wireMaterial = new THREE.MeshStandardMaterial({
                color: 0xec4899,
                roughness: 0.3,
                metalness: 0.8,
                emissive: 0x500c30
            });

            wireMesh = new THREE.Mesh(routingGeometry, wireMaterial);
            scene.add(wireMesh);

            logToAIChat("System", "Automated system harness pathfinding sequence computed. Underbody routing completed.");
            updateHUDStatus("🔌 3D ELECTRICAL HARNESS INTELLIGENTLY ROUTED");
        }

        function clearRoutingMeshes() {
            if (wireMesh) {
                scene.remove(wireMesh);
                wireMesh = null;
            }
        }

        // Automatic 2D Projection Drafting Sheets Generation
        function trigger2DDraftingLayout() {
            clearRoutingMeshes();
            clearStressHeatmaps();

            camera.position.set(0, 0, 240);
            controls.target.set(0, 0, 0);
            controls.update();

            logToAIChat("System", "Orthographic projection drawing complete: Rendered standard drafting layout sheet.");
            updateHUDStatus("📐 Orthographic Drafting sheets generated");
        }

        // Generative Design topology optimizers
        function triggerTopologyOptimization() {
            clearStressHeatmaps();
            
            workspaceMesh.material = new THREE.MeshStandardMaterial({
                color: 0x10b981,
                wireframe: true,
                transparent: true,
                opacity: 0.85
            });

            logToAIChat("System", "Generative algorithm finished. Optimized shell structure for aerodynamic load efficiency.");
            updateHUDStatus("🌱 GENERATIVE DESIGN OPTIMIZATION COMPLETE // MASS REDUCED BY 42.6%");
        }

        // Assembly exploded controls
        function triggerExplodedView() {
            switchModule('assembly');
            let sliderVal = 0;
            const timer = setInterval(() => {
                sliderVal += 5;
                if (sliderVal > 60) {
                    clearInterval(timer);
                }
                document.getElementById('hud-slider').value = sliderVal;
                handleHudSlider(sliderVal);
            }, 30);
        }

        function triggerConvergentMesh() {
            updateHUDStatus("🧬 CONVERGENT MODEL ENGINE APPLIED // MIXED B-REP AND LATTICE MESH");
            workspaceMesh.material.wireframe = !workspaceMesh.material.wireframe;
            logToAIChat("System", "Mixed Boundary Representation (B-Rep) loaded with scanned mesh data elements successfully.");
        }

        // Global part presets
        function applyPreset(presetType) {
            const extParams = document.getElementById('extrusion-params');
            const carParams = document.getElementById('car-loft-params');
            const cutoutParams = document.getElementById('cutout-params');
            const treeBase = document.getElementById('protrusion-title');

            if (presetType === 'car') {
                state.modelType = 'car_loft';
                treeBase.innerText = "Protrusion 1 (B-Spline Loft)";
                
                // Toggle active parameter sliders in UI Pathfinder
                extParams.classList.add('hidden');
                cutoutParams.classList.add('hidden'); // Disable cutout for car body preset
                carParams.classList.remove('hidden');

                // Adjust camera for car body view
                camera.position.set(160, 110, 190);
                controls.update();
            } else {
                state.modelType = 'extrude';
                treeBase.innerText = "Protrusion 1 (Base Extrude)";
                
                extParams.classList.remove('hidden');
                cutoutParams.classList.remove('hidden');
                carParams.classList.add('hidden');

                if (presetType === 'block') {
                    state = { ...state, ...defaultState, modelType: 'extrude' };
                } else if (presetType === 'bracket') {
                    state = {
                        ...state,
                        width: 160,
                        height: 100,
                        depth: 25,
                        radius: 28,
                        x: -20,
                        y: 10,
                        modelType: 'extrude'
                    };
                }

                // Sync sliders back
                document.getElementById('param-width').value = state.width;
                document.getElementById('param-height').value = state.height;
                document.getElementById('param-depth').value = state.depth;
                document.getElementById('param-radius').value = state.radius;
                document.getElementById('param-x').value = state.x;
                document.getElementById('param-y').value = state.y;
            }

            compilePartGeometry();
            logToAIChat("System", `Loaded active CAD preset blueprint [${presetType.toUpperCase()}]`);
        }

        // AI Assistant Command Interface
        function sendAICommand() {
            const promptBox = document.getElementById('ai-command');
            const promptText = promptBox.value.trim();
            if (!promptText) return;

            logToAIChat("User", promptText);
            promptBox.value = '';

            setTimeout(() => {
                const lowerPrompt = promptText.toLowerCase();
                if (lowerPrompt.includes("stress") || lowerPrompt.includes("fea") || lowerPrompt.includes("simulation")) {
                    triggerStressSimulation();
                    logToAIChat("SolidEdge_X_Bot", "Understood. I have activated the FEM solver and mapped aerodynamic pressure strain gradients across the B-spline shell.");
                } else if (lowerPrompt.includes("car") || lowerPrompt.includes("loft") || lowerPrompt.includes("bspline") || lowerPrompt.includes("b-spline")) {
                    applyPreset('car');
                    logToAIChat("SolidEdge_X_Bot", "Confirmed. I have deployed the parametric B-Spline Lofting engine and loaded a streamlined vehicle body shell with editable curves.");
                } else if (lowerPrompt.includes("extrude") || lowerPrompt.includes("dimensions") || lowerPrompt.includes("resize")) {
                    if (state.modelType === 'car_loft') {
                        state.carLength = 200;
                        document.getElementById('param-car-length').value = 200;
                        compilePartGeometry();
                        logToAIChat("SolidEdge_X_Bot", "Aerodynamic chassis length updated to 200mm.");
                    } else {
                        state.width = 150;
                        state.height = 90;
                        document.getElementById('param-width').value = 150;
                        document.getElementById('param-height').value = 90;
                        compilePartGeometry();
                        logToAIChat("SolidEdge_X_Bot", "Base extrusion profile resized to X: 150mm and Y: 90mm.");
                    }
                } else if (lowerPrompt.includes("flat") || lowerPrompt.includes("pattern") || lowerPrompt.includes("sheet")) {
                    triggerSheetMetalPattern();
                    logToAIChat("SolidEdge_X_Bot", "Extracted flat model layout boundary vector matrix successfully.");
                } else if (lowerPrompt.includes("draft") || lowerPrompt.includes("2d") || lowerPrompt.includes("document")) {
                    trigger2DDraftingLayout();
                    logToAIChat("SolidEdge_X_Bot", "Orthographic draft page constructed. Dimensions aligned to ISO limits.");
                } else {
                    logToAIChat("SolidEdge_X_Bot", "Command processed. Try typing 'Loft B-spline car body' or 'Trigger stress simulation'.");
                }
            }, 800);
        }

        function triggerSheetMetalPattern() {
            updateHUDStatus("📐 FLAT PATTERN COMPILATION COMPLETE // BENDS RELIEVED");
            camera.position.set(0, 0, 180);
            controls.target.set(0, 0, 0);
            controls.update();
            logToAIChat("System", "Flat Pattern geometry derived successfully.");
        }

        function logToAIChat(sender, text) {
            const chatLog = document.getElementById('ai-chat-box');
            const colorClass = sender === 'User' ? 'text-[#00FFCC]' : (sender === 'System' ? 'text-[#94a3b8] italic' : 'text-[#2563eb]');
            chatLog.innerHTML += `<div class="mb-1"><strong class="${colorClass}">${sender}:</strong> ${text}</div>`;
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        // Canvas animation frame ticking loop
        function renderLoop() {
            requestAnimationFrame(renderLoop);
            controls.update();
            renderer.render(scene, camera);
        }

        // Orchestrate startup sequences on load
        window.addEventListener('load', () => {
            initThreeWorkspace();
            compilePartGeometry();
            
            // Trigger automatic icons loading
            lucide.createIcons();
            
            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });
        });
    </script>
</body>
</html>
"""

# Serve the complete high-fidelity system client-side inside the iframe component
components.html(html_workstation_code, height=950, scrolling=False)

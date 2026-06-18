# NEXORIUM Parametric 3D CAD Modeler

An enterprise-grade, lightweight 3D parametric CAD modeling design platform engineered explicitly for high-performance deployment on constraint-bound server instances (such as Render.com Free/Starter Tiers).

## Architectural Strategy: Zero-RAM Server footprint

Traditional server-side solid-modeling kernels (e.g., standard C++ OpenCascade wrappers or heavy native mesh manipulation engines) cause immediate Out-Of-Memory (OOM) fatal crashes when serving concurrent 3D transformations within constrained 512MB instances. 

To maximize system scalability, this application utilizes a **Heavy-Client / Stateless-Server architecture**:
1. **The Backend Framework (Python + Streamlit):** Orchestrates the UI shell, acts as the central state controller, and compiles the linear parameter changes into a compact, light JSON feature tree structure (< 1KB).
2. **The Geometric Engine (Google Manifold WASM):** Handled directly inside the client's WebGL browser context. When a slider changes, the raw mathematical calculations, shape derivations, and constructive solid geometries (CSG) execute directly via WebAssembly on the user's processor.
3. **The Rendering Layer (Three.js):** Translates the raw topology metrics output by Manifold into high-performance, responsive viewport matrices dynamically.

## Installation & Local Execution

Ensure you have Python 3.10+ installed locally on your system.

```bash
# Clone the codebase repository
git clone [https://github.com/your-organization/nexorium-cad.git](https://github.com/your-organization/nexorium-cad.git)
cd nexorium-cad

# Install the minimal dependencies
pip install -r requirements.txt

# Boot the local application server instance
streamlit run app.py

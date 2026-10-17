---
name: ai-3d-mesh-generation
description: AI-powered text-to-3D and image-to-3D generation pipelines using Tripo3D API, automatic retopology, PBR texture baking, format conversion (GLB, FBX, OBJ), and offline Blender procedural fallback.
---

# AI 3D Mesh Generation & Tripo3D Pipeline

This skill automates the creation of 3D assets from text prompts and reference images using the Tripo3D API (and open-source 3D models), delivering game-ready, textured `.glb` and `.fbx` models.

---

## ⚡ 1. The Tripo3D Generation Pipeline

```
[Text / Image Prompt] ──> [Tripo3D API] ──> [Draft Mesh (10s)] ──> [PBR Refinement] ──> [.glb Export]
```

1. **Text-to-3D:** Generates 3D models from descriptive text prompts with built-in retopology and unwrapped UVs.
2. **Image-to-3D:** Reconstructs full 360-degree 3D meshes from a single 2D concept image or photo.
3. **Format Standards:** Exports industry-standard binary glTF (`.glb`), FBX, or Wavefront OBJ.
4. **Offline Procedural Fallback:** When offline or without API keys, generates clean low-poly procedural assets using Python and Blender `bpy`.

---

## 🛠️ 2. Universal 3D Generator Script (`generate_3d.py`)

Run the automated CLI runner located in `scripts/generate_3d.py`:

```bash
# Text-to-3D generation via Tripo3D API (requires TRIPO_API_KEY)
python3 scripts/generate_3d.py --backend tripo --prompt "A medieval fantasy treasure chest, stylized, wooden planks, iron braces" --output chest.glb

# Image-to-3D generation via Tripo3D API
python3 scripts/generate_3d.py --backend tripo --image reference.png --output character.glb

# Zero-API Offline Procedural Mode (generates a textured primitive crate)
python3 scripts/generate_3d.py --backend offline-box --output sci_fi_crate.glb
```

---

## 🎮 3. Game Engine Integration Standards

* **Godot 4.x:** Save `.glb` directly into your Godot project root (e.g. `res://assets/models/`). Godot automatically imports materials and collision shapes.
* **Unity:** Import `.glb` or `.fbx` with standard PBR Metallic/Roughness shader assignment.
* **Unreal Engine 5:** Import as `StaticMesh` with Nanite enabled for high-poly Tripo meshes.

---

## 🔄 Interoperability & Handoffs

* **2D Drawn Image to High-Detail 3D (`concept-art-sketch-to-3d-sculptor`):** When starting from a 2D drawing or character refsheet, extract mathematical contour slices and verify Silhouette IoU (`>= 0.85`) via `silhouette_iou_profiler.py`.
* **Autonomous Online Anatomy & Blueprint Research (`autonomous-3d-reference-researcher`):** Search the web for exact real-world skeletal proportions, mechanical dimensions, and Blender 5.2+ `bpy` shader recipes before sculpting.
* **Sub-Second RTX 5060 GPU Baking (`rtx-optix-gpu-baker-denoiser`):** Accelerate normal/AO baking and 2x2 contact sheet renders via NVIDIA OptiX + AI Denoising in `/dev/shm` (`ramdisk-tmpfs-build-bake-accelerator`).
* **Handoff to `threejs-webgl-engineering`:** Immediately loads the generated `.glb` into a live browser viewport for 360-degree orbit inspection.
* **Handoff to `blender-3d-engineering` & `blender-sdf-organic-remeshing`:** For SDF voxel fusion, QuadriFlow retopology, LOD generation, or bone rigging.
* **Handoff to `cross-engine-3d-import-export-bridge`:** Export to Godot 4, Unity, Unreal Engine 5, or S.T.A.L.K.E.R. OGSR (`.ogf`/`.dm`).

## Windows 10/11 & Cross-Platform Blender 5.2+ Parity (`windows-linux-cross-os-runtime-bridge`)
- **Executable Discovery:** Resolve Blender via `shutil.which("blender")` or fallback on Windows to `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe -b --factory-startup`.
- **Cross-OS Scratch & OptiX Baking:** Stage intermediate `.blend`, `.png`, and `.ogf`/`.glb` exports in `Path(tempfile.gettempdir())` (`%TEMP%` on Windows, `/dev/shm` on Linux) and enable `compute_device_type = "OPTIX"` on both Windows WDDM 3.2 and Linux NVIDIA drivers.

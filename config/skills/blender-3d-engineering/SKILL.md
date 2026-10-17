---
name: blender-3d-engineering
description: High-efficiency, quota-saving 3D modeling and procedural asset generation with Blender (bpy). Use when creating 3D models, procedural geometry, game-ready assets (glTF, FBX, OBJ), modifier stacks, or running headless Blender automation.
---

# Blender 3D Engineering & Quota-Saving Guide

This skill governs 3D modeling, asset generation, and procedural workflows in Blender via the Python API (`bpy`). It is specifically optimized to **minimize LLM token/quota usage** while producing professional, game-ready 3D models.

---

## 1. Quota & Context Economy Discipline

### Why LLMs Waste Quota on 3D Modeling
- Generating raw vertex/face coordinate lists in chat bloats context windows with tens of thousands of tokens and frequently creates non-manifold geometry, leading to expensive 5-10 turn repair loops.
- Asking for viewport screenshot renders after every minor tweak consumes massive image tokens.

### Core Quota Safeguards
1. **Headless Script Execution:**
   - Always author self-contained Python scripts (`.py`) written to disk (e.g. scratch directory) and execute them via Blender CLI:
     ```bash
     blender --background --python script.py
     ```
2. **Self-Validating Scripts:**
   - Embed automated topology checks (manifold validation, normal orientation, polycount, bounding box) directly in the script. The script should only return `SUCCESS` or a concise failure diagnosis—preventing hallucination loops.
3. **Milestone-Only Renders:**
   - Generate a preview render (turntable or clay/wireframe image) **only** at major task milestones or final delivery, never after every minor transform.

---

## 2. Modeling Architecture: Modifier Stacks & BMesh

Avoid hardcoding vertex tables. Build models procedurally using parameter-driven primitives and non-destructive modifier stacks:

### A. Primitive Assembly & Modifiers
- Start with basic primitives (`bpy.ops.mesh.primitive_cube_add`, `primitive_cylinder_add`).
- Stack non-destructive modifiers:
  - **Boolean:** Carve cutouts and merge forms (`modifier.operation = 'DIFFERENCE' / 'UNION'`).
  - **Bevel:** Soften hard edges and catch highlights (`width=0.01`, `segments=2`, `limit_method='ANGLE'`).
  - **Mirror:** Build symmetrical assets with clipping enabled to save half the modeling logic.
  - **Solidify / Array:** Add thickness or repeat modular elements.
  - **Subdivision Surface:** Refine curved surfaces when quad topology is clean.

### B. Precision BMesh Operations
Use `bmesh` for direct, memory-efficient mesh manipulation:
```python
import bpy, bmesh

def refine_mesh(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Recalculate normals to face outward
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    # Dissolve degenerate zero-area faces / double vertices
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
```

---

## 3. Game-Ready Asset Pipeline & Verification

Before exporting to game engines (Godot, Unreal, Unity, S.T.A.L.K.E.R.):

1. **Apply Transforms:**
   - Freezing transforms is mandatory. Position must be centered at origin, rotation `(0, 0, 0)`, scale `(1, 1, 1)`:
     ```python
     bpy.ops.object.select_all(action='SELECT')
     bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
     ```
2. **Set Origin Point:**
   - Props/weapons: Center of mass or grip point.
   - Buildings/props placed on ground: Base bottom center (`z = 0`).
3. **Automated UV Unwrapping:**
   ```python
   bpy.ops.object.mode_set(mode='EDIT')
   bpy.ops.mesh.select_all(action='SELECT')
   bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
   bpy.ops.object.mode_set(mode='OBJECT')
   ```
4. **Targeted Export Standards:**
   - **Godot / Web:** glTF 2.0 (`.glb` / `.gltf`) with embedded PBR materials.
   - **Unreal / Unity:** FBX (`+Y Up`, `-Z Forward`, unit scale `1.0`).
   - **S.T.A.L.K.E.R. / X-Ray:** OBJ or `.object` via X-Ray plugin with strict metric scale.

---

## 4. Specialized 3D Subsystem Delegation

For advanced modeling, baking, and character workflows, route to the dedicated domain skills:

* **High-to-Low Normal & AO Baking (`blender-high-to-low-baking`):** Bake tangent-space normal maps, ambient occlusion, and curvature maps from high-poly sculpts onto low-poly cages.
* **Engine Budget & LOD Profiling (`game-engine-3d-budget-profiler`):** Enforce triangle budgets, generate LOD0–LOD3 decimation cascades, and build simplified `UCX_` convex collision hulls.
* **PBR Texture Channel Packing (`blender-pbr-texture-packager`):** Pack ORM (Occlusion/Roughness/Metallic) textures, enforce texel density ($px/cm$), and orient normal maps (DirectX $Y-$ vs OpenGL $Y+$).
* **Organic Character & Animal Anatomy (`character-creature-anatomy-modeling`):** Model biped and quadruped creatures with deformation-friendly quad loops, digitigrade leg landmarks, and automated retopology setup.
* **SDF Voxel Fusion & Anti-Cartoon Organic Remeshing (`blender-sdf-organic-remeshing`):** Fuse overlapping primitives via `voxel_remesh()` + `LAPLACIANSMOOTH` and bake procedural fur cards.
* **Geometry Nodes & Procedural Worlds (`blender-geometry-nodes-procedural-worlds`):** Author Blender 5.2 `GeometryNodeTree` splines, buildings, and Poisson biome scatter with `Realize Instances`.
* **Hard-Surface Weapons, Vehicles & Props (`blender-hard-surface-cad-weapons-props`):** Non-destructive Boolean + Bevel + Weighted Normal stack and FPS weapon bone rigging.
* **UV Unwrapping, UDIMs & Lightmap UV2 (`blender-uv-udim-lightmap-architect`):** Automated seam marking, texel density normalization, UDIM tiles (`1001–1008`), and engine Lightmap UV2 gutters.
* **Animation Retargeting & Vertex Animation Textures (`blender-animation-nla-retargeting-vat`):** NLA visual baking, quaternion loop locking, and `float16 EXR` VAT textures for GPU crowds/destruction.
* **Cross-Engine Export Bridge (`cross-engine-3d-import-export-bridge`):** Unified scale/axis/collision export recipes for Unreal 5, Godot 4, Unity, S.T.A.L.K.E.R. OGSR, and Three.js/WebGPU.
* **Android & Mobile TBDR 3D Optimizer (`android-mobile-3d-asset-optimizer`):** Adreno/Mali micro-triangle pruning, `<=4` bone skinning sanitizer, `fp16` quantization, and ASTC/KTX2 packing.
* **Gaussian Splatting & Scan Cleanup (`blender-gaussian-splatting-photogrammetry-cleanup`):** Retopologize and delight 3D Gaussian Splats, photogrammetry scans, and AI 3D meshes into game-ready PBR assets.
* **3D Printing & CAD Manifold Engineering (`blender-3d-printing-cad-manifold-prep`):** Watertight `bmesh` manifold repair, millimeter snap-fit clearances (`0.15–0.25mm`), and C++ `.stl`/`.3mf` export.
* **S.T.A.L.K.E.R. X-Ray `.ogf` & `.dm` Binary Export (`xray-ogf-dm-blender-pipeline`):** Compile `.ogf` v4 and `.dm` grass/flora binary files directly from Blender.
* **UE5 Foliage to OGSR Transpiler (`ue5-foliage-mesh-to-ogsr-transpiler`):** Decimate S.T.A.L.K.E.R. 2 trees/foliage and preserve mipmap alpha coverage.
* **Rigging & Armature Skinning (`rigging-weight-painting-pipeline`):** Construct bone hierarchies, clamp bone limits ($\le 64$ mobile, $\le 128$ desktop), and normalize vertex weights.
* **Token & Quota Protection (`blender-headless-token-shield`):** Prevent raw vertex/face coordinate dumping in chat, extract compact 3-line CLI telemetry, and gate visual renders to milestones.

## 5. Blender 5.2+ LTS Headless API & Multi-Angle Contact Sheet Rules
1. **Context Override API (`bpy.context.temp_override`):** Never pass legacy dictionary overrides (`bpy.ops.object.mode_set(ctx_dict, ...)`), which raise `TypeError` in Blender 4.0+/5.2+. Always use `with bpy.context.temp_override(window=window, area=area, region=region):`.
2. **Render Engine Identifiers:** In Blender 5.2 LTS, use `scene.render.engine = 'BLENDER_EEVEE_NEXT'` (or `'CYCLES'` with `preferences.compute_device_type = 'OPTIX'`) for headless preview renders.
3. **Mandatory 2x2 Multi-Angle Contact Sheet (`argon-multimodal-vision-grounding`):** Before finalizing any procedural character, creature, or tree asset, render a single `1024x1024` 2x2 grid (`Front, Side, 3/4 Perspective, Clay Silhouette`) and inspect via `view_file` to catch disconnected limbs, primitive seams, or proportion errors in one vision pass.

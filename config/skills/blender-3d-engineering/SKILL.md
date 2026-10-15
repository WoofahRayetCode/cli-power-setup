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

---
name: android-mobile-3d-asset-optimizer
description: Android NDK, Vulkan, and OpenGL ES 3.2 mobile 3D asset optimization in Blender 5.2+. Enforces Adreno/Mali Tile-Based Deferred Rendering (TBDR) triangle budgets, <=4 bone skinning weights, fp16 vertex quantization, and ASTC/KTX2 BasisU texture compression.
---

# Android & Mobile GPU 3D Asset Optimizer (`android-mobile-3d-asset-optimizer`)

## When to Use
- Preparing 3D characters, environments, weapons, and UI 3D models in Blender 5.2+ for **Android** games (Native C++ NDK Vulkan/GLES3, Godot 4 Mobile Renderer, Unity URP Mobile, or Unreal 5 Android).
- Optimizing meshes and textures for mobile **Tile-Based Deferred Renderers (TBDR)** (Qualcomm Adreno, ARM Mali, Samsung Xclipse) to prevent thermal throttling and VRAM bandwidth stalls.

---

## 1. Mobile TBDR Geometry & Micro-Triangle Rules
Mobile GPUs split the screen into $16\times16$ or $32\times32$ pixel tiles in on-chip SRAM. High vertex density and tiny triangles choke the hardware tile binner before fragment shading even begins:

| Asset Category | Android Mobile Triangle Budget | Max Draw Calls / Materials | Max Bone Influences |
| :--- | :--- | :--- | :--- |
| **Hero Character / Player** | `4,500 – 12,000 tris` | `1 – 2 materials` (atlas PBR) | `4 weights/vert`, `<= 64 bones` |
| **NPC / Enemy / Companion** | `2,000 – 6,000 tris` | `1 material` | `2 – 4 weights/vert`, `<= 45 bones` |
| **First-Person Weapon** | `3,500 – 8,000 tris` | `1 – 2 materials` | `1 weight/vert` (rigid bone links) |
| **Props / Vehicles / Trees** | `300 – 2,500 tris` | `1 material` (tight alpha cutout hull) | Static or vertex-shader wind |

- **Eliminate Micro-Triangles (`< 4 px` screen area):** Never export raw Subsurf/Remesh meshes to Android. Run `bmesh.ops.dissolve_degenerate(bm, dist=0.002)` and `DECIMATE` (`COLLAPSE`) so every triangle covers at least several screen pixels.
- **Tight Alpha-Cutout Hulls Over Transparent Quads:** On mobile TBDR, `ALPHA_BLEND` or `ALPHA_CLIP` forces tiles out of Early-Z fast-path (`late ZS update`). Cut mesh geometry tightly around leaf/hair silhouettes so $<15\%$ of the polygon area is transparent empty space.

---

## 2. Mobile GPU Skinning Sanitizer (`bpy`)
Mobile Vulkan/GLES uniform buffers clamp bone matrices per draw call (often `64` `mat4` or `128` `vec4` dual-quaternions) and support at most **4 bone weights per vertex**:

```python
import bpy

def sanitize_mobile_skinning(obj: bpy.types.Object, max_influences: int = 4):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
    # Clamp to top 4 bone weights per vertex and normalize to 1.0
    bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=max_influences)
    bpy.ops.object.vertex_group_clean(group_select_mode='ALL', limit=0.01)
    bpy.ops.object.vertex_group_normalize_all(lock_active=False)
    bpy.ops.object.mode_set(mode='OBJECT')
```

---

## 3. Vertex Quantization (`EXT_mesh_quantization`) & KTX2 / ASTC Textures
1. **16-Bit Vertex Attribute Quantization (`fp16` / `int16`):**
   - Full `float32` `POSITION` (`12B`), `NORMAL` (`12B`), `TANGENT` (`16B`), and `TEXCOORD_0` (`8B`) consume `48 bytes/vertex`.
   - Exporting `.glb` with `KHR_mesh_quantization` / `gltfpack -cc` packs positions into `int16` (`8B`), normals/tangents into `int8` octahedral (`4B`), and UVs into `fp16` (`4B`)—slashing mobile memory bandwidth by **66%** (`16 bytes/vertex`).
2. **ASTC 4x4 / 6x6 & KTX2 Supercompression:**
   - Never ship uncompressed `.png` or desktop `BC7/DXT5` textures inside an Android `.apk`/`.aab`.
   - Pack Occlusion (`R`), Roughness (`G`), and Metallic (`B`) into a single **ORM** map (`blender-pbr-texture-packager`) and encode to **ASTC 4x4** (normals/hero albedo) and **ASTC 6x6** (environment/ORM) inside `.ktx2` containers (`toktx --t2 --encode uastc --zcmp 18`).

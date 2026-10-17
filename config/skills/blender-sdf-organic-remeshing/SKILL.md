---
name: blender-sdf-organic-remeshing
description: Eliminates the 'cartoony balloon-animal' look in procedural Blender 5.x organic modeling using Voxel SDF Remeshing, Volume-Preserving Laplacian Smoothing, Anatomical Plane Flattening, and QuadriFlow Retopology.
---

# Blender 5.x SDF Organic Remeshing & Anti-Cartoon Sculpting (`blender-sdf-organic-remeshing`)

When LLMs generate organic characters, creatures, or animals (such as felines, canines, or NPCs) in Blender by placing `create_uvsphere` ellipsoids and spline tubes together, the resulting mesh looks like a **"cartoony balloon animal"** due to:
1. **Unblended Primitive Intersections:** Hard V-shaped pinching creases where spheres and cylinders overlap.
2. **Uniformly Round Cross-Sections:** Real anatomy has flat bony planes (nasal bridge, scapula, tibia, cheek zygomatic arch) and taut tendon hollows—not inflated spherical tubes.
3. **UV Seam Sawtoothing:** Painting colours per-vertex or across un-retopologized primitive seams creates jagged stair-stepped markings.

This skill replaces raw primitive assembly with a **Signed Distance Field (SDF) Voxel Remesh + Anatomical Plane Carving + QuadriFlow Retopology** pipeline in Blender 5.2+.

---

## 1. The 5-Stage Anti-Cartoon Organic Pipeline

```
[1. Anatomical Blockout]
  - Use metaballs (bpy.data.metaballs) or bmesh primitives with flat-plane scaling
        │
        ▼
[2. Voxel SDF Fusion (bpy.ops.object.voxel_remesh)]
  - Fuses all overlapping limbs, torso, and head into a single watertight manifold
  - Eliminates 100% of internal faces and intersection creases
        │
        ▼
[3. Volume-Preserving Laplacian Smooth (MOD_LAPLACIANSMOOTH)]
  - Relaxes surface tension at joints (shoulder, hip, muzzle) without shrinking volume
        │
        ▼
[4. Anatomical Plane & Hollow Carving (Bony Landmarks)]
  - Flatten nasal bridge, carve pre-orbital eye sockets, hollow flank/tuck, pinch ear pinna
        │
        ▼
[5. QuadriFlow / Decimate Retopology + Smart UV Project]
  - Clean game-ready triangles (< 8,000 tris) + continuous 2048x2048 baked texture
```

---

## 2. Metaball SDF Blockout vs. Raw UV Spheres

Instead of `bmesh.ops.create_uvsphere` (which leaves hard seams), use **Blender Metaballs (`MBALL`)** or **Voxel Remesh** so adjacent muscles blend organically like clay:

```python
import bpy, bmesh
from mathutils import Vector

def fuse_and_remesh_organic(obj, voxel_size=0.006, target_faces=5000):
    """Fuse overlapping primitive parts into a seamless organic mesh in Blender 5.2+."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # 1. Voxel SDF Remesh: melts away balloon intersections into continuous skin
    obj.data.remesh_voxel_size = voxel_size
    obj.data.use_remesh_fix_poles = True
    obj.data.use_remesh_preserve_volume = True
    bpy.ops.object.voxel_remesh()

    # 2. Laplacian Smooth: softens transitions while preserving bony volume
    lap = obj.modifiers.new(name="LaplacianRelax", type='LAPLACIANSMOOTH')
    lap.iterations = 4
    lap.lambda_factor = 0.35
    lap.lambda_border = 0.0
    lap.use_volume_preserve = True
    bpy.ops.object.modifier_apply(modifier=lap.name)

    # 3. Clean game-engine polygon budget via QuadriFlow or Collapse Decimate
    dec = obj.modifiers.new(name="GameBudget", type='DECIMATE')
    dec.decimate_type = 'COLLAPSE'
    dec.ratio = min(1.0, target_faces / max(1, len(obj.data.polygons)))
    bpy.ops.object.modifier_apply(modifier=dec.name)

    # 4. Enable smooth shading
    for poly in obj.data.polygons:
        poly.use_smooth = True
```

---

## 3. Anatomical Anti-Cartoon Rules (Feline / Quadruped / Creature)

To make a quadruped or feline look **realistic instead of cartoony**:

| Feature | Cartoony Mistake (Avoid) | Realistic Anatomical Fix (Enforce) |
| :--- | :--- | :--- |
| **Cranium & Muzzle** | Round ball head + stuck-on cylinder snout | **Wedge pyramid:** Flat dorsal nasal plane from forehead to nose tip (`z` tapers linearly with `y`); wide zygomatic cheek arches; defined chin pad. |
| **Eyes** | Giant spheres sitting on top of the face | **Recessed orbital sockets:** Carve a concave socket *before* placing the cornea; wrap upper and lower eyelid folds (`eyelid crease`) around the eyeball. |
| **Ears (Pinnae)** |Thick cones pointing straight up | **Thin conch shell (< 3mm wall):** Deep anterior hollow cavity, tilted 18° forward and 15° outward, wider base wrapping the temporal skull. |
| **Scapula & Spine** | Cylinder tube torso | **S-curve dorsal line:** Prominent shoulder blades (withers) rising above the thoracic spine, dipping slightly at the back, rising at the iliac crest (croup), and tucking up at the inguinal flank. |
| **Limbs & Paws** | Straight vertical cylinders + ball feet | **Angulated digitigrade zig-zag:** Scapula ($45^\circ$) $\rightarrow$ Humerus $\rightarrow$ Elbow $\rightarrow$ Vertical radius $\rightarrow$ Angled carpal pastern $\rightarrow$ Flat, splayed 4-toed cushion pad resting flush on `Z = 0`. |

---

## 4. Separate Sub-Meshes Only for Hard/Glossy Materials

- **Fuse into the SDF Skin Mesh:** Cranium, muzzle, lips, ears, neck, torso, tail, legs, and paws MUST be fused into a single continuous voxel-remeshed skin surface so no polygon seams exist.
- **Keep as Separate Sharp Sub-Meshes:** Eyeballs (glossy wet cornea), collar strap, metal bell, claws, and thin vibrissae (whiskers)—joined *after* `fuse_and_remesh_organic()` completes.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`blender-gaussian-splatting-photogrammetry-cleanup`**: Converts raw 3D Gaussian Splatting (.ply), NeRF, photogrammetry scans, and AI-generated 3D meshes (Tripo3D/Hun...
- **`blender-uv-udim-lightmap-architect`**: Automated headless UV unwrapping in Blender 5.2+ (SLIM Minimum Stretch, Angle-Based, Conformal), texel density...
- **`blender-geometry-nodes-procedural-worlds`**: Headless Blender 5.2+ Geometry Nodes (bpy.types.GeometryNodeTree) procedural worldbuilding, spline generators ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

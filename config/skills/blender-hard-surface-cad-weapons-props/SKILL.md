---
name: blender-hard-surface-cad-weapons-props
description: Non-destructive hard-surface 3D modeling in Blender 5.2+ for weapons, firearms, vehicles, mechs, and sci-fi props using Boolean + Bevel + Weighted Normals, MikkTSpace tangents, and FPS kinematic weapon bone rigging.
---

# Blender Hard-Surface CAD, Weapons & Props (`blender-hard-surface-cad-weapons-props`)

## When to Use
- Modeling realistic firearms, weapon attachments (scopes, suppressors, magazines, Picatinny rails), vehicles, mechs, electronics, or industrial props in Blender 5.2+.
- Eliminating shading artifacts on flat milled-metal surfaces using **Bevel + Weighted Normals** instead of expensive subdivision surfaces.
- Rigging FPS/TPS weapons for S.T.A.L.K.E.R. OGSR (`wpn_*`), Unreal Engine 5, Godot 4, or Unity.

---

## 1. The AAA Non-Destructive Hard-Surface Modifier Stack
Never use raw `SUBSURF` on machined metal—it turns crisp weapon receivers into melted soap. Use the **Boolean -> Bevel -> Weighted Normal** stack:

```python
import bpy

def apply_hardsurface_stack(obj: bpy.types.Object, bevel_width: float = 0.0015, segments: int = 2):
    # Enable smooth shading; Blender 5.2 uses Smooth by Angle or Weighted Normals
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()

    # 1. Bevel Modifier (chamfers sharp >30 deg edges)
    bev = obj.modifiers.new(name="HS_Bevel", type='BEVEL')
    bev.limit_method = 'ANGLE'
    bev.angle_limit = 0.523599  # 30 degrees
    bev.width = bevel_width
    bev.segments = segments
    bev.harden_normals = False  # Handled by Weighted Normal below
    bev.use_clamp_overlap = True

    # 2. Weighted Normal Modifier (forces large flat faces to stay 100% flat)
    wn = obj.modifiers.new(name="HS_WeightedNormal", type='WEIGHTED_NORMAL')
    wn.mode = 'FACE_AREA_WITH_ANGLE'
    wn.weight = 50
    wn.keep_sharp = True
```

---

## 2. Clean Boolean Cutter Discipline (`SOLVER_MANIFOLD` / `EXACT`)
1. **Blender 5.2 Boolean Solver:** Set `bool_mod.solver = 'MANIFOLD'` (or `'EXACT'`) to avoid non-manifold slivers on coplanar cuts (e.g., ejection ports, cooling vents, Picatinny rail slots).
2. **Support Edge Cleanup:** After applying booleans for game export, run `bmesh.ops.dissolve_limit(bm, angle_limit=0.017)` to remove collinear stray vertices along flat faces, then triangulate Ngons (`MOD_TRIANGULATE`, `keep_custom_normals=True`) **before** baking normal maps so MikkTSpace tangents match 1:1 in-engine.

---

## 3. FPS Kinematic Weapon Rigging Standard
Every interactive firearm or mechanical prop must separate moving sub-parts by vertex group (`1.0` rigid weight per mechanical part) bound to a clean armature hierarchy:

| Bone Name | Parent | Function & Axis Convention |
| :--- | :--- | :--- |
| `root` / `wpn_body` | *(None)* | Receiver / main frame anchored at weapon grip/pivot `(0, 0, 0)`. |
| `mag` / `wpn_mag` | `wpn_body` | Detachable magazine pivot at magwell catch. |
| `bolt` / `wpn_bolt` | `wpn_body` | Reciprocating bolt carrier group sliding strictly along local longitudinal axis. |
| `trigger` | `wpn_body` | Trigger pivot pin. |
| `safety` / `fire_mode` | `wpn_body` | Selector lever pivot. |
| `scope` / `wpn_scope` | `wpn_body` | Optic mount node (can be toggled via bone visibility or child mesh slot). |
| `muzzle` / `gilza` | `wpn_body` | Empty socket bones for muzzle flash particles and brass casing ejection. |

---

## 4. Material & Edge-Wear Realism
- Combine baked **Curvature (`Pointiness`)** and **Ambient Occlusion** masks in the shader tree to drive exposed metallic edge wear along `HS_Bevel` chamfers (`Metallic = 1.0, Roughness = 0.25` on worn edges vs `Roughness = 0.55` on anodized/parkerized flat receiver body).
- Keep total weapon triangle counts within **8,000–22,000 tris** for first-person hero views and **1,500–3,500 tris** for third-person / world pickup LODs.

---
name: rigging-weight-painting-pipeline
description: Character, creature, and animal rigging and skinning in Blender (bpy). Armature hierarchies, bone limits for game engines, automated weight painting normalization, IK/FK solvers, and deformation testing.
---

# Rigging & Weight Painting Pipeline (`rigging-weight-painting-pipeline`)

A 3D character or animal model cannot be animated in a game engine without an optimized skeletal armature and smooth, normalized vertex weight painting. Poor skinning causes mesh collapsing at joints, candy-wrapper twisting on forearms, and game engine bone limit rejections.

This skill governs game-engine-ready armatures, bone hierarchies, and automated skinning verification in Blender via `bpy`.

---

## 1. Game Engine Skeletal Armature Constraints

| Platform / Engine | Max Bones per Mesh | Max Vertex Influences | Root Bone Standard |
| :--- | :--- | :--- | :--- |
| **Mobile / Web (glTF)** | $\le$ 64 bones | 4 bones per vertex | Single `root` at $(0, 0, 0)$ |
| **Standard Game Engine (Unreal/Unity/Godot)**| $\le$ 128 – 256 bones | 4 – 8 bones per vertex | Single `root` $\rightarrow$ `pelvis`/`hips` |
| **S.T.A.L.K.E.R. OGSR (X-Ray)** | Vanilla X-Ray skeleton hierarchy | 2 – 4 bones per vertex | `bip01_root` at origin |

---

## 2. Automated Skinning & Weight Normalization (`bpy`)

Bind a character mesh to an armature and ensure all vertex weights are strictly normalized to $1.0$:

```python
import bpy

def bind_and_normalize_skin(mesh_name, armature_name):
    mesh_obj = bpy.data.objects[mesh_name]
    arm_obj = bpy.data.objects[armature_name]
    
    # Parent mesh to armature with automatic weights
    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    arm_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
    
    # Select mesh and normalize all vertex groups
    bpy.context.view_layer.objects.active = mesh_obj
    bpy.ops.object.vertex_group_normalize_all(group_select_mode='ALL', lock_active=False)
    
    # Clean tiny stray weights (< 0.01) to optimize performance
    bpy.ops.object.vertex_group_clean(group_select_mode='ALL', limit=0.01)
    
    # Limit influences to 4 per vertex for game engine compatibility
    bpy.ops.object.vertex_group_limit_total(group_select_mode='ALL', limit=4)
    print(f"Skinning normalized and clamped to 4 influences: {mesh_name}")
```

---

## 3. Quadruped vs. Biped Armature Hierarchy

- **Biped:**
  `root` $\rightarrow$ `hips` $\rightarrow$ `spine_01` $\rightarrow$ `spine_02` $\rightarrow$ `neck` $\rightarrow$ `head`.
  Legs: `thigh` $\rightarrow$ `calf` $\rightarrow$ `foot` $\rightarrow$ `toe`.
- **Quadruped (Animal / Creature):**
  `root` $\rightarrow$ `pelvis` $\rightarrow$ `spine_lumbar` $\rightarrow$ `spine_thoracic` $\rightarrow$ `neck` $\rightarrow$ `head`.
  Hind legs (Digitigrade): `thigh` $\rightarrow$ `shin` $\rightarrow$ `hock` $\rightarrow$ `paw` $\rightarrow$ `toes`.
  Front legs: `scapula` $\rightarrow$ `humerus` $\rightarrow$ `radius` $\rightarrow$ `wrist` $\rightarrow$ `paw`.

---

## 4. Deformation Range Verification

Before export, test extreme poses to verify joint integrity:
- Elbow / Knee 120° flexion: ensure no volume collapse or self-intersecting quads.
- Shoulder 90° abduction: ensure armpit does not stretch or collapse inwards.

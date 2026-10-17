---
name: game-engine-3d-budget-profiler
description: Enforces game engine 3D performance budgets, automated LOD0-LOD3 generation, convex collision hull generation (UCX), and draw-call material audits in Blender.
---

# Game Engine 3D Budget Profiler (`game-engine-3d-budget-profiler`)

Game engines cannot maintain 60–144 FPS if models exceed GPU triangle throughput or generate excessive draw calls. A model must balance visual fidelity with strict engine memory and rasterization budgets.

This skill establishes automated budget auditing, LOD generation, and collision hull creation via Blender Python (`bpy`).

---

## 1. Standard Engine Triangle & Draw Call Budgets

| Asset Category | Target Triangle Budget | Maximum Materials | Draw Call Target |
| :--- | :--- | :--- | :--- |
| **FPS Viewmodel (Hero Weapon)** | 25,000 – 45,000 tris | 1 – 2 materials | 1 – 2 calls |
| **Hero Character / Boss NPC** | 20,000 – 40,000 tris | 2 – 3 materials | 2 – 3 calls |
| **Standard NPC / Enemy** | 8,000 – 18,000 tris | 1 – 2 materials | 1 – 2 calls |
| **Large Architecture / Hero Prop** | 6,000 – 15,000 tris | 1 – 2 materials | 1 call |
| **Small Prop / Debris / Item** | 300 – 2,500 tris | 1 shared atlas | 1 call |

---

## 2. Automated LOD0 – LOD3 Cascade Generation

Generate progressive Level of Detail (LOD) meshes with quad-preserving edge collapse decimation:

```python
import bpy

def generate_lod_cascade(obj_name, ratios=[0.5, 0.25, 0.10]):
    base_obj = bpy.data.objects[obj_name]
    lods = [base_obj]
    
    for i, ratio in enumerate(ratios, start=1):
        lod = base_obj.copy()
        lod.data = base_obj.data.copy()
        lod.name = f"{base_obj.name}_LOD{i}"
        bpy.context.collection.objects.link(lod)
        
        # Add Decimate modifier
        dec = lod.modifiers.new(name="Decimate", type='DECIMATE')
        dec.decimate_type = 'COLLAPSE'
        dec.ratio = ratio
        dec.use_collapse_triangulate = True
        
        # Apply modifier
        bpy.context.view_layer.objects.active = lod
        bpy.ops.object.modifier_apply(modifier=dec.name)
        lods.append(lod)
        print(f"Generated {lod.name}: {len(lod.data.polygons)} faces ({ratio*100:.0f}%)")
        
    return lods
```

---

## 3. Simplified Convex Collision Mesh Generation (`UCX_`)

Never allow real-time game physics engines to evaluate detailed visual meshes. Generate simplified convex hulls:

```python
def generate_convex_collision(obj_name):
    obj = bpy.data.objects[obj_name]
    col = obj.copy()
    col.data = obj.data.copy()
    col.name = f"UCX_{obj.name}"
    bpy.context.collection.objects.link(col)
    
    # Decimate heavily to create a simplified convex representation
    dec = col.modifiers.new(name="CollisionDecimate", type='DECIMATE')
    dec.decimate_type = 'COLLAPSE'
    dec.ratio = 0.05  # 5% polycount for physics hull
    
    bpy.context.view_layer.objects.active = col
    bpy.ops.object.modifier_apply(modifier=dec.name)
    return col
```

---

## 4. Weighted Normal Modifier for Pristine Shading

Eliminate distorted shading gradients on flat mechanical surfaces:
```python
def apply_weighted_normals(obj):
    mod = obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
    mod.keep_sharp = True
    mod.weight = 50
    obj.data.use_auto_smooth = True
```

---

## 5. Steam Library Per-Engine Polygon & Index Buffer Ceilings

| Engine / Steam Games | Hard Index Buffer Limit per Submesh | Recommended Hero Character / Weapon Tris | Recommended Prop / Foliage Tris |
| :--- | :--- | :--- | :--- |
| **S.T.A.L.K.E.R. X-Ray / EE / OGSR** | **`65,535` verts (`uint16`)** per `.ogf` child or `.dm` | `12,000 – 28,000 tris` | `4,000 – 12,000` (tree `.ogf`), `12 – 64` (grass `.dm`) |
| **UE5 IoStore** (*S.T.A.L.K.E.R. 2*, *Borderlands 4*, *AC Rally*) | `uint32` (Nanite static) / `65k` per skeletal LOD section | `35,000 – 85,000 tris` (Skeletal LOD0) | `5,000 – 50,000 tris` (Nanite handles LODs) |
| **Bethesda Creation Engine** (*Skyrim SE*, *FO3/NV/4*, *Starfield*) | **`65,535` verts (`uint16`)** per `BSTriShape` (`Starfield` uses meshlets) | `15,000 – 35,000 tris` | `500 – 8,000 tris` (`bhkCollisionObject <= 64` verts) |
| **Valve Source & KEX** (*HL2*, *Black Mesa*, *GMod*, *L4D2*, *SiN*) | **`32,767`–`65,535` verts** per `.mdl` bodygroup | `8,000 – 20,000 tris` | `300 – 4,500 tris` (`<=32` VPhysics convex pieces) |
| **Project Zomboid & Classic GTA** (*Zomboid* `108600`, *GTA III/VC/SA*) | `uint16` | `800 – 2,500 tris` (Zomboid/GTA III-SA) | `100 – 1,200 tris` |

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`android-mobile-3d-asset-optimizer`**: Android NDK, Vulkan, and OpenGL ES 3.2 mobile 3D asset optimization in Blender 5.2+. Enforces Adreno/Mali Tile...
- **`game-asset-streaming-lod-governor`**: Real-time asynchronous asset streaming, distance-based LOD hierarchies (LOD0-LOD3), virtual texturing, and LRU...
- **`game-performance-overlay-telemetry`**: In-game HUD performance metrics and telemetry profiling (MangoHud, DXVK HUD, PresentMon). Configures FPS, fram...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

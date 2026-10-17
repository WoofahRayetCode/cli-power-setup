---
name: blender-high-to-low-baking
description: Automated high-to-low poly baking pipeline in Blender (bpy). Bakes tangent-space normal maps, ambient occlusion (AO), curvature/cavity, and material ID masks from multi-million polygon sculpts onto game-ready low-poly meshes.
---

# Blender High-to-Low Poly Baking (`blender-high-to-low-baking`)

Achieving AAA visual fidelity in real-time game engines requires baking the surface details of a high-resolution sculpt (millions of polygons) onto an optimized, game-ready low-poly cage (thousands of polygons).

This skill standardizes headless `bpy` baking workflows to deliver cinematic edge highlights and micro-crevice depth with zero real-time geometry cost.

---

## 1. High-Poly to Low-Poly Cage Setup

Before baking, both meshes must align perfectly at the origin:

```python
import bpy

def setup_bake_objects(high_poly_name, low_poly_name, cage_extrusion=0.015):
    high_obj = bpy.data.objects[high_poly_name]
    low_obj = bpy.data.objects[low_poly_name]
    
    # Ensure transforms are applied
    for obj in [high_obj, low_obj]:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        obj.select_set(False)
        
    return high_obj, low_obj
```

---

## 2. Headless Tangent-Space Normal Map Baking

Bake high-resolution geometric details into 16-bit or 8-bit normal maps:

```python
def bake_normal_map(high_obj, low_obj, output_path, resolution=2048):
    # Setup Cycles with NVIDIA RTX 5060 OptiX GPU acceleration (rtx-optix-gpu-baker-denoiser)
    bpy.context.scene.render.engine = 'CYCLES'
    cprefs = bpy.context.preferences.addons['cycles'].preferences
    cprefs.compute_device_type = 'OPTIX'
    cprefs.get_devices()
    for dev in cprefs.devices:
        dev.use = (dev.type in {'OPTIX', 'CUDA'})
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 8
    bpy.context.scene.cycles.bake_type = 'NORMAL'
    bpy.context.scene.render.bake.use_selected_to_active = True
    bpy.context.scene.render.bake.cage_extrusion = 0.02
    bpy.context.scene.render.bake.normal_space = 'TANGENT'
    
    # Create target texture image
    img = bpy.data.images.new("Baked_Normal", width=resolution, height=resolution, alpha=False, float_buffer=True)
    img.colorspace_settings.name = 'Non-Color'
    
    # Create temporary material and texture node on low-poly
    mat = bpy.data.materials.new(name="Bake_Mat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    nodes.active = tex_node
    
    low_obj.data.materials.clear()
    low_obj.data.materials.append(mat)
    
    # Select high-poly, then low-poly (active)
    bpy.ops.object.select_all(action='DESELECT')
    high_obj.select_set(True)
    low_obj.select_set(True)
    bpy.context.view_layer.objects.active = low_obj
    
    # Execute bake
    bpy.ops.object.bake(type='NORMAL')
    img.filepath_raw = output_path
    img.file_format = 'PNG'
    img.save()
    print(f"Normal map baked to: {output_path}")
```

---

## 3. Ambient Occlusion (AO) & Cavity Baking

Bake contact shadows into crevice masks for PBR shading:
- Set `bpy.context.scene.cycles.bake_type = 'AO'`.
- Use a normalized distance parameter (`distance=1.0m`) to prevent interior geometry from casting pitch-black shadows across exterior surfaces.
- Save as a grayscale 8-bit texture for packing into ORM channel maps.

---

## 4. Hard Edge & UV Seam Alignment Rule

To eliminate black seam line artifacts when rendering baked normal maps in game engines:
1. **Rule:** Every UV island boundary **must** be marked as a **Sharp Edge** (`mesh.edges[i].use_seam == True -> mesh.edges[i].use_edge_sharp = True`).
2. **Padding:** Use a minimum bake margin of **16 pixels** (`bpy.context.scene.render.bake.margin = 16`) for 2048x2048 textures to prevent mipmap bleed.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`blender-uv-udim-lightmap-architect`**: Automated headless UV unwrapping in Blender 5.2+ (SLIM Minimum Stretch, Angle-Based, Conformal), texel density...
- **`blender-gaussian-splatting-photogrammetry-cleanup`**: Converts raw 3D Gaussian Splatting (.ply), NeRF, photogrammetry scans, and AI-generated 3D meshes (Tripo3D/Hun...
- **`blender-hard-surface-cad-weapons-props`**: Non-destructive hard-surface 3D modeling in Blender 5.2+ for weapons, firearms, vehicles, mechs, and sci-fi pr...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

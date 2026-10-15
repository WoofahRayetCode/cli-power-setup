"""
Headless Blender 3D Asset Builder Template
Optimized for Antigravity: Token-efficient, self-validating, game-ready.
Usage: blender --background --python asset_builder_template.py -- [options]
"""

import sys
import bpy
import bmesh
import math

def clean_scene():
    """Wipe default cube, lights, and cameras."""
    bpy.ops.wm.read_factory_settings(use_empty=True)

def apply_all_transforms(obj):
    """Freeze location, rotation, and scale."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def validate_topology(obj):
    """Verify mesh manifoldness, normals, and clean geometry."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Clean duplicates and orient normals outward
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    
    # Check non-manifold edges
    non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
    poly_count = len(bm.faces)
    vert_count = len(bm.verts)
    
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    
    status = {
        "vertices": vert_count,
        "polygons": poly_count,
        "non_manifold_edges": len(non_manifold_edges),
        "is_manifold": len(non_manifold_edges) == 0
    }
    return status

def unwrap_mesh(obj, island_margin=0.02):
    """Auto UV unwrap using Smart UV Project."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=island_margin)
    bpy.ops.object.mode_set(mode='OBJECT')

def export_gltf(filepath, obj):
    """Export asset to glTF 2.0 / GLB."""
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        use_selection=True,
        export_format='GLB',
        export_apply=True
    )

if __name__ == "__main__":
    print("--- Blender Asset Builder Initialized ---")
    clean_scene()
    
    # Example: Create a bevelled sci-fi crate / container
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0, 0, 1.0))
    crate = bpy.context.active_object
    crate.name = "GameAsset"
    
    # Add Bevel Modifier
    bevel = crate.modifiers.new(name="Bevel", type='BEVEL')
    bevel.width = 0.05
    bevel.segments = 2
    bevel.limit_method = 'ANGLE'
    
    apply_all_transforms(crate)
    stats = validate_topology(crate)
    unwrap_mesh(crate)
    
    print(f"Asset Created: {crate.name}")
    print(f"Topology Status: {stats}")
    print("--- Build Finished Successfully ---")

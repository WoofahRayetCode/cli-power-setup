---
name: blender-headless-token-shield
description: Quota and context token protector for 3D modeling and Blender workflows. Prohibits dumping raw vertex coordinate tables into chat, enforces headless Python script execution with compact CLI telemetry, and gates renders to major task milestones.
---

# Blender Headless Token Shield (`blender-headless-token-shield`)

3D modeling tasks are among the most dangerous vectors for LLM context inflation and quota burn. An agent that outputs raw 3D mesh arrays (e.g. lists of 10,000 vertices and face indices) burns **15,000 to 40,000 tokens in a single turn**, quickly exhausting hourly rate limits and degrading reasoning context.

This skill establishes hard token-saving barriers for all 3D modeling operations.

---

## 1. Hard Prohibitions (Zero Coordinate Dumping)

- **Strictly Prohibited:** Outputting raw vertex coordinates, polygon index lists, OBJ string dumps, or glTF JSON blocks directly into chat.
- **Enforced Pattern:** Always write procedural geometry generation logic to a standalone Python script in `scratch/` or `/tmp/` and execute it headlessly via Blender:
  ```bash
  blender --background --python /tmp/generate_mesh.py
  ```

---

## 2. High-Density CLI Telemetry Extraction

Instead of returning verbose Blender engine logs, the script must calculate and output a compact **3-line diagnostic signature**:

```python
# In generate_mesh.py:
mesh = obj.data
print("=== 3D MESH TELEMETRY ===")
print(f"Verts: {len(mesh.vertices)} | Tris: {sum(len(p.vertices) - 2 for p in mesh.polygons)} | Manifold: {mesh.is_manifold}")
print(f"Dimensions: X={obj.dimensions.x:.2f}m, Y={obj.dimensions.y:.2f}m, Z={obj.dimensions.z:.2f}m")
print(f"Status: PASS (Transforms frozen, normals recalculated)")
```

- **Token Cost:** **< 40 tokens** in context vs 25,000+ tokens for raw geometry.

---

## 3. Milestone-Only Visual Verification

- **Never render after every transform:** Do not request screenshot renders for minor rotations, extrusions, or scale adjustments.
- **Render Policy:** Produce a clay wireframe or turntable preview render **only** when a major milestone contract is fulfilled (e.g. high-poly sculpt completed, low-poly retopology verified, or final baked material delivered).
- **Format:** Low-resolution web-optimized preview (e.g. 512x512 PNG, 50 samples with OptiX denoiser) to minimize multimodal token ingestion.

## Windows 10/11 & Cross-Platform Blender 5.2+ Parity (`windows-linux-cross-os-runtime-bridge`)
- **Executable Discovery:** Resolve Blender via `shutil.which("blender")` or fallback on Windows to `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe -b --factory-startup`.
- **Cross-OS Scratch & OptiX Baking:** Stage intermediate `.blend`, `.png`, and `.ogf`/`.glb` exports in `Path(tempfile.gettempdir())` (`%TEMP%` on Windows, `/dev/shm` on Linux) and enable `compute_device_type = "OPTIX"` on both Windows WDDM 3.2 and Linux NVIDIA drivers.

---
name: xray-ogf-dm-blender-pipeline
description: Direct binary compilation and export of S.T.A.L.K.E.R. X-Ray and OGSR 3D meshes (.ogf v4 rigid/skinned models and .dm Detail Model grass/flora) from Blender 5.2+ without third-party plugins.
---

# X-Ray `.ogf` & `.dm` Binary Blender Pipeline (`xray-ogf-dm-blender-pipeline`)

## When to Use
- Exporting custom 3D weapons, props, characters, creatures (e.g., Aisha cat companion), or trees from Blender 5.2+ directly into S.T.A.L.K.E.R. Shadow of Chernobyl / OGSR Engine `.ogf` v4 binary format.
- Compiling custom grass blades, flowers, bushes, or ground cover into X-Ray `.dm` (Detail Model) binary files for `level.details`.
- Bypassing broken GUI-only Blender X-Ray addons during headless CLI automation (`blender -b -P`).

---

## 1. Coordinate System & Tangent Basis Conversion
Blender uses a **Right-Handed Z-Up** coordinate system (`+X Right, +Y Forward, +Z Up`), whereas X-Ray / OGSR uses **Left-Handed Y-Up** (`+X Right, +Y Up, +Z Forward`, DirectX convention).

- **Position / Normal / Tangent Transformation:**
  ```python
  # Blender (x, y, z) -> X-Ray (x, z, y)
  xray_pos = (b_pos.x, b_pos.z, b_pos.y)
  xray_norm = (b_norm.x, b_norm.z, b_norm.y)
  ```
- **UV Coordinate Flip:**
  - DirectX / X-Ray `.dds` textures use top-left `(0, 0)` origin:
  ```python
  xray_u, xray_v = b_u, 1.0 - b_v
  ```
- **Triangle Winding Reversal:**
  - Because swapping `Y` and `Z` flips handedness, reverse triangle index winding `(i0, i1, i2) -> (i0, i2, i1)` so normals face outward in-engine.

---

## 2. X-Ray `.dm` (Detail Model Grass/Flora) Binary Spec
Detail models (`gamedata/meshes/dm/*.dm`) are ultra-fast instanced foliage meshes with a flat, chunkless binary layout:

```python
import struct

def write_xray_dm(path: str, shader: str, texture: str, verts: list, indices: list,
                  flags: int = 0, min_scale: float = 0.5, max_scale: float = 1.2):
    """
    verts: list of (x, y, z, u, v) in X-Ray Left-Handed Y-Up space
    indices: list of uint16 triangle indices (len must be multiple of 3, max 65535)
    flags: 0 = standard waving grass, 1 = no waving (pebbles/twigs)
    """
    assert len(verts) <= 65535 and len(indices) <= 65535, "Exceeds uint16 DM limit"
    with open(path, "wb") as f:
        f.write(shader.encode("ascii") + b"\x00")
        f.write(texture.encode("ascii") + b"\x00")
        f.write(struct.pack("<IffII", flags, min_scale, max_scale, len(verts), len(indices)))
        for x, y, z, u, v in verts:
            f.write(struct.pack("<5f", x, y, z, u, v))
        for idx in indices:
            f.write(struct.pack("<H", idx))
```
- **Mandatory Shader for Grass/Foliage:** Use `details\blend` or `details\lod` so the OGSR wind vertex shader (`s_details`) animates blade sway cleanly.

---

## 3. X-Ray `.ogf` v4 Binary Chunk Specification
OGF v4 files use sequential little-endian chunks (`struct.pack("<II", chunk_id, len(payload)) + payload`):

| Chunk ID | Name | Structure & Requirements |
| :--- | :--- | :--- |
| `0x0001` | `OGF_HEADER` | `version=4 (B)`, `model_type (B)` (`0x0a` = `MT_SKELETON_RIGID`, `0x03` = `MT_SKELETON_ANIM`), `shader_id=0 (H)`, `bbox (6f)`, `bsphere (4f)` (44 bytes total). |
| `0x0002` | `OGF_TEXTURE` | `texture_path\0` + `shader_name\0` (e.g., `models\model`). |
| `0x0003` | `OGF_VERTICES` | `vertex_format (I)` (`0x12071980` = 1-bone link, 60B/vert) + `num_verts (I)` + per-vertex `<3f 3f 3f 3f 2f I` (`pos, norm, tan, binorm, uv, bone_id`). |
| `0x0004` | `OGF_INDICES` | `num_indices (I)` + `num_indices * <H` (`uint16`). **Hard limit: 65,535 vertices per child submesh.** Split larger meshes into multiple children in Chunk `0x0009`. |
| `0x0006` | `OGF_SWIDATA` | `16 zero bytes` + `struct.pack("<IIHH", 1, 0, num_tris, num_verts)`. |
| `0x0009` | `OGF_CHILDREN` | Nested sub-chunks (`0, 1, 2...`), each containing a complete child submesh (`0x01, 0x02, 0x03, 0x04, 0x06`). |
| `0x000D` | `OGF_S_BONE_NAMES` | `num_bones (I)` + per-bone `name\0`, `parent_name\0`, and 60-byte OBB (`rot 9f, translate 3f, halfsize 3f`). |
| `0x0010` | `OGF_S_IKDATA` | Per-bone version `4 (I)`, `game_mtl\0` (`default_object`), 112B `SBoneShape` (`type=1` box), 76B `SJointIKData`, `bind_rot (3f)`, `bind_pos (3f)`, `mass (f)`, `center_of_mass (3f)`. |

---

## 4. Pre-Export Verification Checklist
1. **uint16 Vertex Buffer Ceiling:** Always verify `len(vertices) <= 65535` per material slot/child. If higher, either decimate or partition into multiple `OGF_CHILDREN` sub-chunks.
2. **Bone Weight Normalization:** Every vertex must have valid bone index assignments (`0 <= bone_id < num_bones`) and non-NaN tangents (`mesh.calc_tangents()`).
3. **Binary Magic Verification:** Run a quick Python unpack verify script on the written `.ogf` or `.dm` file to assert chunk lengths sum exactly to `os.path.getsize(path)`.

---

## Promoted Executable Tool (`write_ogf.py`)
- **Location:** `~/.gemini/config/skills/xray-ogf-dm-blender-pipeline/scripts/write_ogf.py`
- **Invocation:** `~/.gemini/config/skills/xray-ogf-dm-blender-pipeline/scripts/write_ogf.py`

## Windows 10/11 & Cross-Platform Blender 5.2+ Parity (`windows-linux-cross-os-runtime-bridge`)
- **Executable Discovery:** Resolve Blender via `shutil.which("blender")` or fallback on Windows to `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe -b --factory-startup`.
- **Cross-OS Scratch & OptiX Baking:** Stage intermediate `.blend`, `.png`, and `.ogf`/`.glb` exports in `Path(tempfile.gettempdir())` (`%TEMP%` on Windows, `/dev/shm` on Linux) and enable `compute_device_type = "OPTIX"` on both Windows WDDM 3.2 and Linux NVIDIA drivers.

---
name: ue5-foliage-mesh-to-ogsr-transpiler
description: Extracts S.T.A.L.K.E.R. 2 (UE5 IoStore) 3D trees, bushes, and grass meshes and transpiles them into 64-bit S.T.A.L.K.E.R. OGSR (.ogf and .dm) formats with uint16 submesh partitioning and alpha-coverage mipmaps.
---

# UE5 Foliage & Tree Mesh to OGSR Transpiler (`ue5-foliage-mesh-to-ogsr-transpiler`)

## When to Use
- Porting 3D trees, pine/birch/oak branches, bushes, and grass foliage from **S.T.A.L.K.E.R. 2: Heart of Chornobyl (UE5.1)** into **S.T.A.L.K.E.R. OGSR Engine**.
- Converting high-poly UE5 Nanite/LOD0 static meshes (`UStaticMesh`) into X-Ray `.ogf` tree visuals (`gamedata/meshes/trees/*.ogf`) or `.dm` instanced ground foliage (`gamedata/meshes/dm/*.dm`).
- Preventing disappearing leaf cards at distance by preserving alpha-test mipmap coverage in `.dds` foliage textures.

---

## 1. End-to-End Extraction & Transpilation Pipeline

### Step 1: Extract UE5 Foliage Assets from IoStore (`.utoc` / `.ucas`)
1. Use `retoc` to convert S.T.A.L.K.E.R. 2 IoStore containers containing `Content/Environment/Foliage/` or `Content/Environment/Trees/` into legacy `.pak` or extract raw `.uasset`/`.ubulk`:
   ```bash
   retoc to-legacy --filter "Foliage|Trees" "/path/to/Stalker2/Content/Paks" /tmp/s2_foliage_legacy.pak
   ```
2. Export static meshes as `.gltf` / `.pskx` and textures as `.png` / `.tga` using CLI asset dumpers (`UEcastoc` / `FModel` CLI / Python `pyuepak` + `uasset` parser).
   - **Tip:** Prefer extracting **LOD1 or LOD2** from UE5 `UStaticMesh` if available, as LOD0 Nanite meshes often exceed 150,000 triangles and require heavy decimation.

---

### Step 2: Headless Blender 5.2 Decimation & Submesh Partitioning
X-Ray `.ogf` v4 and `.dm` files use **16-bit unsigned integer indices (`uint16`, max `65,535` vertices per child submesh)**. Furthermore, OGSR levels render thousands of tree instances, so each tree `.ogf` should target **4,000–12,000 triangles**.

Run a headless Blender 5.2 script (`blender -b -P transpile_foliage.py`) that performs:
1. **Separate Trunk & Canopy Materials:**
   - Assign `models\tree_trunk` (or `default`) shader to solid bark geometry.
   - Assign `trees\trees_fu` (or `models\transparent` / `def_aref`) shader to alpha-tested leaf cards so OGSR applies wind canopy sway and alpha-testing (`alpha_ref = 128`).
2. **Planar / Collapse Decimation (`DECIMATE`):**
   - Apply `DECIMATE` (`decimate_type='COLLAPSE'`, `ratio=target_tris / current_tris`, `use_collapse_triangulate=True`) to bark trunks while locking UV seams (`delimit={'UV'}`).
3. **Vertex Normal Transfer for Fluffy Leaf Canopies:**
   - Leaf cards look flat and harsh unless their vertex normals point radially outward from the canopy center. Add a proxy UV sphere around the tree crown and apply a `DATA_TRANSFER` modifier (`data_types_loops={'CUSTOM_NORMAL'}`) from the sphere to the leaf cards before exporting to `.ogf`.

---

### Step 3: Alpha-Coverage Preserving `.dds` Mipmap Generation
Standard downsampling averages transparent background pixels (`alpha = 0`) with leaf pixels (`alpha = 255`), causing upper mipmaps to drop below X-Ray's `def_aref` threshold (`128`) so tree leaves vanish into bare sticks at 50 meters.

- **Fix — Dilate RGB & Boost Mipmap Alpha Coverage:**
  ```python
  import numpy as np
  from PIL import Image

  def boost_mipmap_alpha_coverage(rgba: np.ndarray, cutoff: float = 0.5, target_coverage: float = None) -> np.ndarray:
      """Scales mipmap alpha channel so the fraction of pixels > cutoff matches LOD0."""
      alpha = rgba[..., 3].astype(np.float32) / 255.0
      if target_coverage is None:
          return rgba
      lo, hi = 0.0, 4.0
      for _ in range(12):
          mid = (lo + hi) * 0.5
          cov = np.mean((alpha * mid) > cutoff)
          if cov < target_coverage:
              lo = mid
          else:
              hi = mid
      rgba[..., 3] = np.clip(alpha * ((lo + hi) * 0.5) * 255.0, 0, 255).astype(np.uint8)
      return rgba
  ```
- Compress final foliage textures to **BC3 / DXT5** (or **BC1a / DXT1 with 1-bit alpha** for crisp `def_aref` cutouts) and generate accompanying `_bump.dds` (swizzled `X-Ray` normal/spec/height) + `.thm` metadata descriptor.

---

### Step 4: Binary Export to `.ogf` or `.dm`
- Invoke the binary writers from `xray-ogf-dm-blender-pipeline`:
  - **Trees & Bushes:** Export as `MT_SKELETON_RIGID` (`0x0a`) `.ogf` with a single `root` bone at `(0, 0, 0)` and separate child chunks for bark and leaves.
  - **Grass & Ground Cover:** Export as `.dm` (`details\blend` shader) with vertex `Y >= 0.0` so grass blades sit flush on terrain heightmaps.

## Windows 10/11 & Cross-Platform Game Modding Parity (`windows-linux-cross-os-runtime-bridge`)
- **Native Windows vs. Linux Wine/Proton:** On Windows 10/11, execute `xrEngine.exe` and mod tools natively via DirectX 11/12 without Wine overhead. On Linux, route through Proton/Wine and DXVK/VKD3D.
- **LLP64 vs. LP64 64-Bit C++ Safety:** On Windows x64 MSVC/Clang-CL (LLP64), `long` and `unsigned long` (`DWORD`) are **32-bit (4 bytes)** whereas on Linux x86_64 (LP64) `long` is 64-bit. Never cast pointers to `long` or `DWORD`—always use `uintptr_t`, `intptr_t`, or `size_t`.
- **Crash Modal Interception & WER Dumps:** On Windows, `xray_crash_handler.py sweep` queries WMI (`Win32_Process`) and terminates lingering `notepad.exe`/`WerFault.exe` popups via `taskkill /F /PID`, reading logs from `%USERPROFILE%\Documents\STALKER-SHOC\logs` and `_appdata_\logs`.
- **Native Win32 Playtest Input & Window Capture:** When `sys.platform == "win32"`, `game_playtest_controller.py` automatically dispatches Win32 `keybd_event` / `mouse_event` (`SendInput`), `ClipCursor`, and `PIL.ImageGrab` instead of Linux `/dev/uinput` and `spectacle`.
- **Steam Library Auto-Discovery:** `steam-mod-scanner` automatically reads `HKCU\Software\Valve\Steam\SteamPath` and `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` on Windows alongside `~/.local/share/Steam` on Linux.

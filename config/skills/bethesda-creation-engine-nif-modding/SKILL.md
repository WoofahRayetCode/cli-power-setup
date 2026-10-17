---
name: bethesda-creation-engine-nif-modding
description: Modding pipeline for Bethesda Creation Engine & Gamebryo games owned in Steam library (Morrowind, Oblivion, Skyrim/SE, Fallout 3, Fallout New Vegas, Fallout 4, Starfield). Covers ESM/ESP/ESL binary plugin records, BSA/BA2 archives, NIF 3D meshes, Papyrus scripting, and SKSE/F4SE/NVSE C++ DLLs.
---

# Bethesda Creation Engine & NIF Modding (`bethesda-creation-engine-nif-modding`)

## When to Use
- Modding any Bethesda title in your Steam library:
  - **Elder Scrolls:** *Morrowind* (`22320`), *Oblivion* (`22330`), *Skyrim* (`72850`), *Skyrim Special Edition* (`489830`).
  - **Fallout & Sci-Fi:** *Fallout 3 / GOTY* (`22300`/`22370`), *Fallout: New Vegas* (`22380`), *Fallout 4* (`377160`), *Fallout 76* (`1151340`), *Starfield* (`1716740`).
- Creating or patching `.esp`/`.esm`/`.esl` binary record plugins, packing `.bsa`/`.ba2` archives, exporting `.nif` meshes from Blender 5.2+, or writing Papyrus `.psc` scripts and `SKSE64`/`F4SE`/`NVSE` C++ native plugins.

---

## 1. Binary Plugin Architecture (`.esm` / `.esp` / `.esl`)
Creation Engine plugins consist of nested **Record (`TES4`, `WEAP`, `ARMO`, `NPC_`, `CELL`, `WRLD`, `QUST`)** and **Group (`GRUP`)** binary chunks (`24-byte header` in Skyrim/FO4; `20-byte header` in Oblivion):
- **FormID Load Order Prefix (`0xFE` Light Plugins):**
  - Standard `.esp`/`.esm` plugins occupy slots `0x00–0xFD` (max 254 active plugins).
  - **ESL-Flagged Light Plugins (`.esl` / `.esp` with header flag `0x0200`)** map into slot `0xFEzzzxxx` (up to `4,096` plugins with max `2,048` new records `'0x800..0xFFF'` each). Always flag small weapon/armor/patch mods as `ESL`!
- **Rule of One Conflict Resolution:** The last plugin in `plugins.txt` touching a FormID overwrites the entire record (e.g., an NPC's inventory or a cell's lighting), unless merged via record delta patchers.

---

## 2. Archive Containers (`.bsa` & `.ba2`)
- **Morrowind / Oblivion / FO3 / FNV / Skyrim SE (`.bsa`):** Magic `BSA\x00` (version `103` FO3/FNV/TES4, `104` TES5, `105` SSE using LZ4 compression).
- **Fallout 4 / 76 / Starfield (`.ba2`):** Magic `BTDX` (`GNRL` for meshes/scripts/sounds using zlib/LZ4; `DX10` for DirectX BC1–BC7 texture mipmap streams so the engine streams only needed mip levels directly into VRAM).
- **Critical Audio Rule:** Never compress `.xwm` / `.fuz` voice files inside a compressed `.bsa` in Skyrim/FNV, or NPC dialogue will stutter or fail to play. Keep audio archives uncompressed (`0x0004` compress flag off).

---

## 3. Blender 5.2+ to `.nif` Mesh & Collision Pipeline
1. **Coordinate System:** NetImmerse/Creation Engine uses **Right-Handed Z-Up** (same as Blender!), where `1 Blender meter = 69.9912 Creation Engine units` (`~70 units/m`, or `1.428 cm/unit`).
2. **`BSLightingShaderProperty` & PBR/ORM:**
   - *FO3/FNV/Skyrim SE:* `_d.dds` (Diffuse), `_n.dds` (Normal with Specular in Alpha channel!), `_s.dds` / `_m.dds` (Environment mask).
   - *Fallout 4:* `_d.dds` (BC1/BC7), `_n.dds` (BC5 2-channel normal), `_s.dds` (BC5 Smoothness in Red + Metallic in Green).
   - *Starfield:* `.mat` layered material files + `_color.dds`, `_normal.dds`, `_rough.dds`, `_metal.dds`, `_ao.dds` in `DX10` `.ba2`.
3. **Havok Collision (`bhkCollisionObject`):** Always generate a simplified convex hull (`<= 64` vertices, `blender-3d-engineering`) rather than raw high-poly `bhkNiTriStripsShape` on movable clutter props to prevent Havok physics explosions.

## Windows 10/11 & Cross-Platform Game Modding Parity (`windows-linux-cross-os-runtime-bridge`)
- **Native Windows vs. Linux Wine/Proton:** On Windows 10/11, execute `xrEngine.exe` and mod tools natively via DirectX 11/12 without Wine overhead. On Linux, route through Proton/Wine and DXVK/VKD3D.
- **LLP64 vs. LP64 64-Bit C++ Safety:** On Windows x64 MSVC/Clang-CL (LLP64), `long` and `unsigned long` (`DWORD`) are **32-bit (4 bytes)** whereas on Linux x86_64 (LP64) `long` is 64-bit. Never cast pointers to `long` or `DWORD`—always use `uintptr_t`, `intptr_t`, or `size_t`.
- **Crash Modal Interception & WER Dumps:** On Windows, `xray_crash_handler.py sweep` queries WMI (`Win32_Process`) and terminates lingering `notepad.exe`/`WerFault.exe` popups via `taskkill /F /PID`, reading logs from `%USERPROFILE%\Documents\STALKER-SHOC\logs` and `_appdata_\logs`.
- **Native Win32 Playtest Input & Window Capture:** When `sys.platform == "win32"`, `game_playtest_controller.py` automatically dispatches Win32 `keybd_event` / `mouse_event` (`SendInput`), `ClipCursor`, and `PIL.ImageGrab` instead of Linux `/dev/uinput` and `spectacle`.
- **Steam Library Auto-Discovery:** `steam-mod-scanner` automatically reads `HKCU\Software\Valve\Steam\SteamPath` and `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` on Windows alongside `~/.local/share/Steam` on Linux.

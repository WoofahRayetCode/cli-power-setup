---
name: source-idtech-kex-engine-modding
description: Modding pipeline for Valve Source/Source 2, GoldSrc, id Tech (Quake II/III, DOOM 3), and Nightdive KEX Engine games in your Steam library (SiN Reloaded, Half-Life 1/2, Black Mesa, Garry's Mod, Left 4 Dead 1/2, Portal 1/2, CS2, TF2).
---

# Valve Source, id Tech & Nightdive KEX Engine Modding (`source-idtech-kex-engine-modding`)

## When to Use
- Modding any **Nightdive KEX**, **Valve Source / GoldSrc**, or **id Tech** title in your Steam library:
  - **Currently Installed (`/mnt/games/SteamLibrary`):** *SiN Reloaded* (`632950`, Nightdive KEX Engine + `Common.kpf` + `game_x64.dll`).
  - **Owned Valve & id Tech Library:** *Half-Life 1 & 2* (`70`, `220`), *Black Mesa* (`362890`), *Garry's Mod* (`4000`), *Left 4 Dead 1 & 2* (`500`, `550`), *Portal 1 & 2* (`400`, `620`), *Counter-Strike: Source & CS2* (`240`, `730`), *Team Fortress 2* (`440`), *Quake II & III Arena* (`2320`, `2200`), *DOOM 3* (`9050`).

---

## 1. Nightdive KEX Engine & *SiN Reloaded* (`632950`) Pipeline
Located at `/mnt/games/SteamLibrary/steamapps/common/SiN Reloaded/`:
1. **`.kpf` (KEX Package File) Containers:**
   - `Common.kpf` and mod `.kpf` archives are standard **ZIP (Deflate/Store)** containers! Inspect and extract into `/dev/shm` without modifying `Common.kpf`:
     ```bash
     unzip -l "/mnt/games/SteamLibrary/steamapps/common/SiN Reloaded/Common.kpf" | token-guard 60
     ```
2. **`base/` Override Directory & `game_x64.dll`:**
   - SiN Reloaded blends id Tech 2 (`Ritual Entertainment` extended Quake II `.sin`/`.pak` archives, `.bsp` levels, `.def`/`.scr` scripts, `.sam`/`.swl` animations) with Nightdive's 64-bit KEX wrapper (`SDL3.dll`, `game_x64.dll`).
   - Place loose override assets inside `base/` (or a custom `-game <mod_folder>` directory) or pack into a load-ordered `.kpf` archive.

---

## 2. Valve Source Engine (`VPK`, `.mdl` StudioMDL, `.vtf`/`.vmt`, GMod Lua)
1. **VPK (`Valve Pak`) Multi-Chunk Archives (`_dir.vpk` + `_000.vpk`):**
   - Extract or pack using `vpk` CLI (`pip install vpk` or Valve `bin/vpk_linux32`):
     ```bash
     vpk -x /dev/shm/vpk_out pak01_dir.vpk
     ```
2. **Blender 5.2+ to Source `.mdl` (`studiomdl` `.qc` Script):**
   - Export reference mesh and skeletal animations from Blender as `.smd` or `.dmx` (Source uses **Right-Handed Z-Up**, `1 inch = 1 Hammer unit`, `1 meter = 39.37 units` or `52.49 units` for character eye-height scale).
   - Author a compact `.qc` compilation manifest with `$modelname`, `$bodygroup`, `$surfaceprop`, `$cdmaterials`, `$sequence`, and `$collisionmodel` (max `32` convex hulls for VPhysics).
3. **VTF Texture & VMT Shader Material Pairs:**
   - Every `.vtf` texture requires a matching `.vmt` key-value shader descriptor (`"VertexLitGeneric"` for models/weapons/characters, `"LightmappedGeneric"` for BSP brush world geometry).

---

## 3. id Tech 2 / 3 / 4 (`.pak`, `.pk3`, `.pk4`, `.md2`/`.md3`/`.md5mesh`)
- **Quake II (`2320`) `.pak`:** Uncompressed `PACK` header (`12B`: magic `"PACK"`, `dir_offset`, `dir_length` where each entry is `56B` filename + `offset` + `size`).
- **Quake III (`2200`) `.pk3` & DOOM 3 (`9050`) `.pk4`:** Standard ZIP archives mounted alphabetically (`z_mymod.pk3` overrides `pak0.pk3`).
- **DOOM 3 `.md5mesh` / `.md5anim`:** Plain-text ASCII skeletal mesh and quaternion keyframe formats—can be generated directly from Python/Blender without binary compilers!

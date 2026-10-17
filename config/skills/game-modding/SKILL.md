---
name: game-modding
description: Specialized workflows, format rules, and safety checks for game modding, focusing on S.T.A.L.K.E.R. Legends of the Zone Trilogy EE (ZoneForge), LTX configurations, XDB pack archives, DDS textures, and engine-safe audio.
---

# Game Modding & S.T.A.L.K.E.R. EE Workflows

This skill guides game modding, with specialized domain knowledge for **S.T.A.L.K.E.R.: Legends of the Zone Trilogy – Enhanced Edition** (Steam / CachyOS Linux) using **ZoneForge**, as well as console and binary modding.

---

## 1. S.T.A.L.K.E.R. EE & ZoneForge Best Practices

### A. Game Configuration (LTX Files)
- **Directory Layout:** Mod configs must mirror vanilla `gamedata/` layout. Note: use `config/` (singular), not `configs/`, for Enhanced Edition.
- **Section Syntax:** Sections follow `[section_name]` or inheritance `[child_section]:parent_section`.
- **Syntax Discipline:**
  - Case-sensitivity is strict in the X-Ray Engine.
  - Do not introduce trailing commas or invalid whitespace in key-value pairs (`parameter = value`).
  - Never guess section names: inspect the unpacked vanilla reference (e.g. `unpacked/config/system.ltx` or `unpacked/config/weapons/...`) before authoring tweaks.

### B. Texture Assets (DDS Format & UI Sheets)
- **Compression Modes:**
  - Use **DXT1** for fully opaque textures or 1-bit binary transparency.
  - Use **DXT5** for smooth interpolated alpha channels.
  - Preserve mipmap generation matching vanilla assets.
- **UI Atlas Sheets:**
  - Most menu and HUD art is packed into shared texture sheets (e.g. `ui_menu_backgraund`).
  - Never replace the entire sheet if only changing one element—use ZoneForge's region replacement (`zoneforge asset replace-region ...`) to paste the customized region while keeping surrounding icons and coords intact.

### C. Audio Assets (OGG Vorbis & GSC Binary Headers)
- **Engine Comment Header Safeguard:**
  - S.T.A.L.K.E.R. stores proprietary binary game engine parameters in a custom binary chunk inside the Ogg Vorbis comment header (controlling hearing distance, min/max volume, and AI awareness).
  - **CRITICAL:** Standard audio tools (Audacity, generic ffmpeg taggers) strip this binary chunk, rendering sounds silent or breaking AI audio perception.
  - Always convert or replace sounds using ZoneForge (`zoneforge asset export` / `zoneforge asset replace`), which copies the GSC binary engine chunk byte-for-byte into the new OGG.

### D. Archive & Pack Lifecycle
- **Vanilla References:** Keep unpacked vanilla game files in `unpacked/` untouched as a read-only baseline for diffs.
- **Packing:** Pack mods using ZoneForge's native packer into `.pack` format (`zoneforge pack`).
- **Steam Workshop Uploads:** Workshop items are configured via `zoneforge.toml` (visibility `2` = private by default). Test locally in-game before promoting to public.

### E. Dialogue & Conversation UI (`game-dialogue-ui-localization`)
- Validate and repair string table XMLs (`gamedata/config/text/`), resolve dead-end dialogue trees, and fix text clipping in `talk.xml`/`talk_16.xml` using `game-dialogue-tool`.

### F. Dynamic Weather & Lighting FX (`game-weather-lighting-fx`)
- Tune ambient light levels, sun shafts/god rays, skybox balance, and tonemapping curves with `weather-lighting-tuner` to prevent overexposure or washed-out shadows.

### G. Weapon Ballistics & Mechanics (`game-weapon-ballistics-mechanics`)
- Configure authentic ballistic physics, dispersion patterns, condition wear (`condition_shot_dec`), and ammo class tables.

### H. Quality-of-Life Gameplay Scripting (`game-qol-gameplay-scripting`)
- Architect clean, event-driven QoL features (carry weight scaling, sprint stamina recovery, field weapon repair kits, zone transition autosaves) without modifying fragile core engine scripts.

---

## 2. Steam Library Multi-Engine Modding Matrix (`steam-mod-scanner`)

Run `steam-mod-scanner` at any time to fingerprint all installed games in `/mnt/games/SteamLibrary` and `~/.local/share/Steam`. Route modding tasks to the matching specialized engine skill:

- **S.T.A.L.K.E.R. Classic Trilogy (`4500`, `20510`, `41700`), Enhanced Edition (`2427410`, `2427420`, `2427430`) & OGSR:**
  - Use `game-modding`, `stalker-ogsr-migration`, `xray-ogf-dm-blender-pipeline` (`write_ogf.py`), and `xray-lua-scripting`.
- **Unreal Engine 5 IoStore Titles (*S.T.A.L.K.E.R. 2* `1643320`, *Borderlands 4* `1285190`, *Assetto Corsa Rally* `3917090`):**
  - Use `ue5-redengine-rage-library-modding`, `stalker2-modding`, and `ue5-foliage-mesh-to-ogsr-transpiler` with `retoc` + `repak` (staging in `/dev/shm` via `ramdisk-tmpfs-build-bake-accelerator`).
- **Nightdive KEX, Valve Source & id Tech (*SiN Reloaded* `632950`, *Half-Life 1/2*, *Black Mesa* `362890`, *Garry's Mod* `4000`, *L4D2* `550`, *Quake II/III*, *DOOM 3*):**
  - Use `source-idtech-kex-engine-modding` (`.kpf` ZIP containers, `.vpk`, StudioMDL `.mdl`/`.qc`, `.vtf`/`.vmt`, `.pk3`/`.pk4`).
- **Bethesda Creation Engine (*Morrowind* `22320`, *Oblivion* `22330`, *Skyrim / SE* `489830`, *Fallout 3 / NV / 4* `22380`/`377160`, *Starfield* `1716740`):**
  - Use `bethesda-creation-engine-nif-modding` (`.esm`/`.esp`/`.esl` light plugins, `.bsa`/`.ba2`, `.nif` meshes, Papyrus `.psc`, SKSE/F4SE/NVSE).
- **Rockstar GTA (*GTA 1* `12170`, *GTA III/VC/SA/IV/V*), *Cyberpunk 2077* (`1091500`), *Witcher 3* (`292030`), *Baldur's Gate 3* (`1086940`) & *Project Zomboid* (`108600`):**
  - Use `ue5-redengine-rage-library-modding`.
- **Vanilla Backups & Reverse Engineering Delegation:** Always preserve read-only vanilla archives and delegate binary disassembly to `rea` MCP tools (`rea-mcp-obligation-ledger-orchestrator`).

---

## 3. Autonomous Hands-Free Playtesting & Closed-Loop Vision Control

When verifying game mods, engine ports, or visual assets, **do not remain idle if the user provides no live controller/keyboard input**. Autonomously assume active control of the game to thoroughly exercise level geometry, physics, and rendering:

1. **Kernel Input Injection (`game-qa-playtest-controller`):**
   - Automatically launch `game_playtest_controller.py` in the background with varied locomotion patterns:
     - `wander`: Autonomous level navigation to verify obstacle colliders, navmeshes, and map bounds.
     - `orbit`: Circle-strafing around key landmarks to test dynamic lighting, normal map reflections, and shadow cascades.
     - `sweep`: 360° panoramic camera sweeps with pitch oscillation to inspect skyboxes, horizon LODs, and distant foliage.
     - `stress-locomotion` & `action-cycle`: Rapid sprint/jump/crouch transitions and weapon swap/fire/reload/inventory cycles to stress animation blend trees and HUD scripts.
2. **Concurrent Screen Telemetry (`game-screen-telemetry-monitor`):**
   - Continuously capture frames in the background to detect:
     - Missing textures (`#FF00FF` magenta or unmapped UVs).
     - GPU pipeline freezes, blackouts, or frametime lockups.
3. **Agentic Perception & Visual Diffing (`agentic-visual-perception`):**
   - Use `agent_visual_grounding.py diff` (SSIM comparison) between pre- and post-action frames to verify that actions (e.g. inventory toggle, weapon discharge) actually mutated visual state on screen.
4. **Autonomous Crash Extraction (`visual-document-ocr-intelligence`):**
   - If an engine crash dialog or BugTrap modal appears, automatically capture the modal, binarize with `document_ocr_pipeline.py preprocess`, and run local OCR (`document_ocr_pipeline.py ocr`) to extract the exact faulting line, file, and expression without human intervention.
5. **Loading Screen Dismissal & Testing Cheats (`game-qa-playtest-controller`):**
   - Automatically dismiss "Press any key to play/continue" loading screen prompts (`game_playtest_controller.py press-any-key --key SPACE`).
   - Enable invulnerability god mode and infinite ammo (`game_playtest_controller.py enable-cheats --god-mode --infinite-ammo`) to ensure uninterrupted, crash-free exploration.
6. **Cursor Confinement & Focus Trapping (`linux-game-window-input-capture`):**
   - Run `game-window-helper lock` to confine mouse inputs inside the game window and eliminate accidental desktop or multi-monitor focus loss.
7. **Waypoint Navigation Replay (`game-autonomous-navigation-ai`):**
   - Replay deterministic route graphs via `nav-graph-recorder replay` to systematically validate level geometry and avoid getting trapped.
8. **Self-Improving Regression Tests (`game-self-improving-qa-pipeline`):**
   - Run `self-improving-qa` to automatically turn crash logs and telemetry anomalies into permanent regression test cases.

---

## 4. Automated Release Packaging & Hardening (`game-mod-release-packager`)

Once mod changes and playtests pass:
1. **Strip Binaries:** Strip non-essential symbols from custom DLLs with `objcopy --strip-debug`.
2. **Pack Game Archives:** Pack loose `gamedata/` directories into `.pack` or `.xdb` archives with optimal zstd compression.
3. **Verify Hashes:** Generate cryptographic `SHA256SUMS.txt` and `RELEASE_INFO.json` manifests for release on Steam Workshop, ModDB, or GitHub Releases.




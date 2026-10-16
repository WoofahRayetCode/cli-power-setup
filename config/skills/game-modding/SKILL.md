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

---

## 2. General Game & Console Modding (GTA PC, Switch, Emulators)

- **Vanilla Backups:** Always preserve a clean backup copy before modifying game binaries, scripts, or archives.
- **Format Verification:** For archive files (PFS0/NSP/NSZ, ZIP, TAR), check header magic, block alignment, and checksums before writing.
- **Reverse Engineering Delegation:** When disassembling or analyzing unfamiliar binary structures, delegate the research to the `rea` tools or an isolated subagent to keep the main context clean.

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



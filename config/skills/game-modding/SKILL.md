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

## 3. Automated Visual & Screen Telemetry Quality Gate (`game-screen-telemetry-monitor`)

- **Automatic Visual Verification:** When testing modded assets, UI textures, or engine ports in-game, automatically run `game_screen_monitor.py` to inspect the screen.
- **Magenta Artifact Sniffing:** Automatically detect unmapped missing textures (`#FF00FF`) or corrupted alpha blending without waiting for the user to report visual bugs.
- **Crash Dialog OCR:** If the mod triggers an engine crash dialog on screen, automatically run `game_screen_monitor.py ocr` to extract the crash stack trace from the desktop modal immediately.


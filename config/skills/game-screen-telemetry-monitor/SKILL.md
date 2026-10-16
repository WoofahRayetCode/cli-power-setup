---
name: game-screen-telemetry-monitor
description: Real-time in-game screen telemetry monitoring, visual anomaly detection (missing textures, freezes, blackouts), and automated crash dialog OCR for game modding, engine porting, and QA testing.
---

# Game Screen Telemetry Monitor

The **Game Screen Telemetry Monitor** provides automated visual surveillance, anomaly detection, and crash dialog OCR for running games and game engine ports across Linux (Wayland/X11), Valve Proton, and Windows.

It is specifically tuned for mod migrations (such as porting legacy **S.T.A.L.K.E.R. Complete** or AMK mods to the 64-bit **OGSR Engine**), runtime QA playtesting, and continuous visual validation.

---

## 🎯 When to Activate

* **Engine Porting QA (e.g. S.T.A.L.K.E.R. Complete to OGSR):**
  - Detecting missing textures (rendered as unmapped magenta `#FF00FF` / `#FF0080` grids).
  - Validating HUD/UI XML aspect ratio adaptation (catching 4:3 elements clipped on 16:9 / 21:9 monitors).
  - Capturing and OCR-transcribing on-screen crash dialogs (`FATAL ERROR`, `Expression : ...`, `BugTrap`).
* **Runtime Crash & Hang Diagnostics:**
  - Diagnosing engine lockups, D3D device resets, and Vulkan GPU hangs (all-black or frozen frames).
  - Reading in-game developer consoles and Lua script stack traces in real time.
* **Continuous Playtest Monitoring:**
  - Running a background watcher that alerts on visual glitches, fps stutter, or sudden crashes while the user tests gameplay.

---

## 🛠️ CLI Tooling (`game_screen_monitor.py`)

The skill includes a standalone monitoring engine located at `scripts/game_screen_monitor.py`.

### 1. Single Screenshot Capture
Captures the display headlessly (KDE Wayland via `spectacle`, or X11/Pillow fallback) and automatically downscales to 1280px to protect model vision token quotas:
```bash
python3 config/skills/game-screen-telemetry-monitor/scripts/game_screen_monitor.py capture --output /tmp/game_frame.png
```

### 2. On-Screen Crash OCR
Transcribes on-screen error dialogs, console messages, and stack traces using `tesseract`:
```bash
python3 config/skills/game-screen-telemetry-monitor/scripts/game_screen_monitor.py ocr /tmp/game_frame.png
```

### 3. Visual Glitch & Anomaly Detection
Scans the captured frame for missing texture magenta (`#FF00FF`), full black screens (GPU crash/hang), or blown-out whiteout rendering:
```bash
python3 config/skills/game-screen-telemetry-monitor/scripts/game_screen_monitor.py glitch /tmp/game_frame.png
```

### 4. Continuous In-Game Monitoring Loop
Polls the screen every $N$ seconds, detecting visual glitches and auto-triggering OCR if an error dialog is suspected:
```bash
python3 config/skills/game-screen-telemetry-monitor/scripts/game_screen_monitor.py monitor --interval 2 --duration 30 --out-dir /tmp/game_telemetry
```

---

## 🔬 S.T.A.L.K.E.R. Complete -> OGSR Porting Workflow

When porting legacy 32-bit Shadow of Chernobyl mods (Complete 2009, AMK 1.4) to 64-bit OGSR Engine:

1. **Launch the Game under Wine/Proton:**
   - Run the game in borderless window or fullscreen mode.
2. **Execute In-Game Screen Watcher:**
   - Launch `game_screen_monitor.py monitor --interval 2 --duration 60 --out-dir /tmp/stalker_port_test`.
3. **Trigger Crash / Glitch Scenarios:**
   - Enter problem levels (e.g. Cordon, Garbage, Dark Valley), spawn customized weapons, or open modded inventory interfaces.
4. **Automated Triage:**
   - **Magenta Detection:** Pinpoints missing `.dds` texture paths or incorrect bump map (`_bump.dds`) references in `textures.ltx`.
   - **Crash Dialog OCR:** Captures the exact line:
     ```text
     FATAL ERROR
     [error]Expression : xml_doc.NavigateToNode(path, index)
     [error]Function   : CUIXmlInit::InitStatic
     [error]File       : ui\UIXmlInit.cpp
     [error]Line       : 75
     [error]Description: XML node not found in file
     ```
   - **Actionable Remediation:** Directly maps the OCR error to the missing UI element in `config/ui/ui_custom_msgs.xml` or script callback.

---

## 🛡️ Token Economy & Privacy Protocol

* **Vision Token Capping:** Every captured frame is constrained to a maximum dimension of 1280px, avoiding the consumption of thousands of tokens per image.
* **Artifact Offloading:** Telemetry monitoring session logs, frame sequences, and raw OCR outputs must be written directly to `.agents/telemetry/` or `/tmp/` rather than pasted wholesale into chat.
* **Local Processing:** Screen grabs and OCR occur 100% locally via `spectacle` and `tesseract` with zero cloud transmission.

---

## 5. Overlay & Capture Coordination

- **MangoHud Telemetry Sync (`game-performance-overlay-telemetry`):** Configure non-overlapping HUD metrics (`mangohud-configurator`) so live stats don't obscure in-game error popups, dialogues, or HUD notification areas.
- **Windowed Capture Isolation (`linux-game-window-input-capture`):** Pair with `game-window-helper` to isolate window coordinates by process name, capturing and analyzing strictly the game viewport without clutter from desktop backgrounds or secondary monitors.


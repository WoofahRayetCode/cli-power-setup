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

## Windows 10/11 & Cross-Platform Game Modding Parity (`windows-linux-cross-os-runtime-bridge`)
- **Native Windows vs. Linux Wine/Proton:** On Windows 10/11, execute `xrEngine.exe` and mod tools natively via DirectX 11/12 without Wine overhead. On Linux, route through Proton/Wine and DXVK/VKD3D.
- **LLP64 vs. LP64 64-Bit C++ Safety:** On Windows x64 MSVC/Clang-CL (LLP64), `long` and `unsigned long` (`DWORD`) are **32-bit (4 bytes)** whereas on Linux x86_64 (LP64) `long` is 64-bit. Never cast pointers to `long` or `DWORD`—always use `uintptr_t`, `intptr_t`, or `size_t`.
- **Crash Modal Interception & WER Dumps:** On Windows, `xray_crash_handler.py sweep` queries WMI (`Win32_Process`) and terminates lingering `notepad.exe`/`WerFault.exe` popups via `taskkill /F /PID`, reading logs from `%USERPROFILE%\Documents\STALKER-SHOC\logs` and `_appdata_\logs`.
- **Native Win32 Playtest Input & Window Capture:** When `sys.platform == "win32"`, `game_playtest_controller.py` automatically dispatches Win32 `keybd_event` / `mouse_event` (`SendInput`), `ClipCursor`, and `PIL.ImageGrab` instead of Linux `/dev/uinput` and `spectacle`.
- **Steam Library Auto-Discovery:** `steam-mod-scanner` automatically reads `HKCU\Software\Valve\Steam\SteamPath` and `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` on Windows alongside `~/.local/share/Steam` on Linux.

## Related & Interoperating Skills
- **`game-self-improving-qa-pipeline`**: Closed-loop self-improving game QA test harness: automated loading screen dismissal, 88% loading stall watchdo...
- **`xray-crash-log-diagnostician`**: Triages and diagnoses S.T.A.L.K.E.R. X-Ray and OGSR engine crashes, BugTrap logs, and Wine/Proton stack traces...
- **`game-runtime-diagnostics`**: Cross-platform game crash diagnostics, performance tuning, and compatibility triage across Windows (DirectX, E...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

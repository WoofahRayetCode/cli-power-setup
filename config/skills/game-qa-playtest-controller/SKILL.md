---
name: game-qa-playtest-controller
description: Autonomous multi-axis game testing locomotion controller using Linux /dev/uinput and evdev. Injects dynamic character movement patterns (circle-strafing orbit, 360° panoramic camera sweeps, obstacle wandering, sprint/jump/crouch stress locomotion, and action cycles) for automated game QA and crash reproduction.
---

# Game QA Playtest Locomotion Controller (`game-qa-playtest-controller`)

The `game-qa-playtest-controller` skill provides programmatic, hardware-level kernel input injection (`/dev/uinput` via `evdev`) to automate complex character locomotion and camera behavior during game testing, mod validation, and engine crash reproduction.

Unlike simplistic linear macros that only hold down single movement keys, `game-qa-playtest-controller` implements non-linear kinematic locomotion: circle-strafing around focal points, full 360° panoramic horizon sweeps with vertical pitch oscillation, autonomous wandering with obstacle bounce-back, rapid state-transition stress testing (sprint/jump/crouch spam), and continuous action-cycling (weapon draw, fire, reload, inventory).

---

## 1. Architecture & Hardware Input Pipeline

```
+---------------------------------------------------------------+
|      Autonomous Game QA Controller (Python CLI)               |
|      (orbit, sweep, wander, stress-locomotion, action-cycle)   |
+---------------------------------------------------------------+
                               |
                               v
                     Linux /dev/uinput (evdev)
        (Virtual Keyboard & Relative Mouse Device Nodes)
                               |
                               v
+---------------------------------------------------------------+
|  Linux Kernel Input Subsystem (evdev input event stream)      |
+---------------------------------------------------------------+
                               |
          +--------------------+--------------------+
          |                                         |
          v                                         v
Native Linux Games / Emulators              Wine / Proton Subsystem
  (SDL2/SDL3, Wayland/X11)              (winex11 / winewayland driver)
          |                                         |
          v                                         v
   In-Game Engine                           DirectInput / RawInput
(Camera & Character Physics)             (Windows Game Executable)
```

### Why `/dev/uinput` Over Synthetic Window Events (`XTest` / `SendInput`)?
1. **DirectInput / RawInput Compatibility**: Modern PC and Wine/Proton games bypass standard window message queues (`WM_KEYDOWN`) and poll raw hardware input directly. Virtual kernel devices created via `/dev/uinput` generate genuine Linux kernel input packets indistinguishable from physical mice and keyboards.
2. **Relative Mouse Motion (`REL_X`, `REL_Y`)**: First-person and third-person camera look handlers require relative mouse deltas rather than absolute screen coordinates. `game_playtest_controller.py` injects smooth sub-pixel mouse steps.
3. **Proton / Steam Deck Parity**: Operates seamlessly across desktop Linux and Steam Deck environments under native X11, XWayland, and pure Wayland without display server permission hacks.

---

## 2. CLI Tool Reference (`game_playtest_controller.py`)

Helper script location: `config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py` (installed to `~/.gemini/config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py` and `~/.claude/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py`).

### Global Flags
- `--dry-run`: Runs locomotion calculations and timing loops in simulation mode without writing to `/dev/uinput` (useful for syntax checks or CI/headless validation).

### Subcommands & Locomotion Patterns

#### 1. Circle-Strafe Orbit (`orbit`)
Holds lateral strafe (`KEY_D` or `KEY_A`) while continuously rotating the camera in counter-yaw (`REL_X`), orbiting a focal target or landmark to inspect 3D model seams, lighting LODs, and geometry clipping.
```bash
# Orbit clockwise for 10 seconds
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py orbit --duration 10.0 --direction right --mouse-speed 12

# Orbit counter-clockwise for 6 seconds
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py orbit --duration 6.0 --direction left
```

#### 2. 360° Panoramic Camera Sweep (`sweep`)
Performs smooth, continuous yaw rotation across full 360° arcs with optional sinusoidal vertical pitch oscillation to sweep the skybox, terrain horizon, and ground planes for missing textures or shader compilation stutters.
```bash
# Sweep horizon for 8 seconds
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py sweep --duration 8.0 --speed 15

# Sweep with vertical pitch oscillation (look up and down while spinning)
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py sweep --duration 12.0 --pitch
```

#### 3. Autonomous Wandering (`wander`)
Navigates the character across game environments using forward sprint thrust with stochastic angle deviations and automatic 180° reverse-turn obstacle recovery when encountering walls, geometry boundaries, or anomalies.
```bash
# Autonomous exploration walk for 30 seconds
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py wander --duration 30.0
```

#### 4. Locomotion State Stress Test (`stress-locomotion`)
Stresses the character controller animation state machine by rapidly interleaving sprint bursts, bunny-hopping (`KEY_SPACE`), tactical crouch toggle/hold (`KEY_LEFTCTRL` / `KEY_C`), and sharp 90° vector snaps.
```bash
# Stress character physics and animation blend trees for 15 seconds
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py stress-locomotion --duration 15.0
```

#### 5. Full Action Cycle (`action-cycle`)
Executes end-to-end combat and inventory cycles: weapon swapping (`KEY_1`, `KEY_2`), primary attack (`BTN_LEFT`), weapon reload (`KEY_R`), world interaction (`KEY_F`), and inventory inspection toggle (`KEY_TAB`).
```bash
# Run 5 consecutive action sequences
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py action-cycle --cycles 5
```

#### 6. Hybrid Dual-Input Stress (`hybrid-stress`)
Simultaneously and intermittently injects both Gamepad controller (analog thumbstick locomotion, right-stick sweep, trigger fire) and Keyboard + Mouse (WASD sprint, sub-pixel mouse look, left-click). Tests if the game engine crashes or desyncs when handling dual-input devices or auto-switching UI button glyphs:
```bash
# Stress dual input devices for 10 seconds
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py hybrid-stress --duration 10.0 --cycles 3
```

#### 7. Visual Target Cursor Clicker (`click-target`)
Bridges visual grounding (`agentic-visual-perception`) directly into mouse cursor actions. Reads screen coordinates or grounding centroids from JSON and executes pinpoint mouse clicks on UI elements (e.g. dialogue responses, inventory items, "Load Game" buttons):
```bash
# Click visual target from agent_visual_grounding.py output
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py click-target --grounding-json /tmp/grounding_result.json

# Click explicit screen coordinates
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py click-target --x 960 --y 540
```

#### 7. NPC Character Dialogue & Talk UI Interaction (`interact-character`)
Triggers the USE action (`KEY_F`), pauses for character dialogue window presentation (`talk.xml`), navigates conversation response choices via numbered hotkeys and mouse targeting, tests Trade UI toggling, and cleanly exits dialogue.
```bash
# Interact with character, navigate 2 dialogue options, test trade, and exit cleanly
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py \
  interact-character --key F --choices 2 --trade
```

---

## 3. Autonomous QA Playtesting Symbiosis

`game-qa-playtest-controller` is designed to run in background tasks alongside visual monitoring tools like `game-screen-telemetry-monitor`:

```
+------------------------------------------------------------------------+
|                      Automated QA Test Session                         |
+------------------------------------------------------------------------+
|                                                                        |
|  [Background Task 1]                  [Background Task 2]              |
|  game_playtest_controller.py          game_screen_monitor.py           |
|  -> wander / orbit locomotion         -> captures screen every 2s      |
|  -> injects movement vectors          -> scans for #FF00FF magenta     |
|                                       -> detects crash dialog OCR      |
|                                                                        |
|                             |                                          |
|                             v                                          |
|      Triangulates Exact Geometry Coordinate or Asset Fault            |
+------------------------------------------------------------------------+
```

### Example Co-Execution Workflow
```bash
# Step 1: Launch screen telemetry monitor in background
python3 config/skills/game-screen-telemetry-monitor/scripts/game_screen_monitor.py \
  --interval 2.0 --output-dir .agents/qa/telemetry &
MONITOR_PID=$!

# Step 2: Run dynamic multi-axis exploration
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py \
  wander --duration 45.0

# Step 3: Run stress action cycle
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py \
  action-cycle --cycles 3

# Step 4: Stop monitor and inspect results
kill -SIGINT $MONITOR_PID
```

### Hands-Free Game Porting Recipe (e.g. S.T.A.L.K.E.R. Complete to OGSR)
When the user is hands-off during mod ports:
1. **Pre-flight Lint:** `python3 config/skills/local-ast-compiler-engine/scripts/local_ast_compiler.py check-syntax --path gamedata/scripts/`
2. **Launch Game + Watcher:** Start `bin_x64/xrEngine.exe` and `game_screen_monitor.py monitor` in detached background tasks.
3. **Execute Non-Linear Test:** Execute `sweep --pitch` -> `orbit` -> `wander` -> `stress-locomotion` -> `action-cycle`.
4. **Verify Action Mutated Screen:** Verify UI mutation via `python3 config/skills/agentic-visual-perception/scripts/agent_visual_grounding.py diff`.
5. **Auto-Recover Crash:** If a crash modal appears, run `document_ocr_pipeline.py ocr` on the modal and `local_model_coprocessor.py summarize-log` on `_appdata_/logs/xrEngine.log` to patch configs and retry.

---

## 4. Permission & Environment Setup

Kernel uinput injection requires access to `/dev/uinput`. On standard Linux distributions (Arch, CachyOS, Ubuntu, Fedora):

```bash
# Verify input group membership
groups | grep -E "input|uinput"

# If permission denied, ensure udev rule exists:
# /etc/udev/rules.d/99-uinput.rules:
# KERNEL=="uinput", MODE="0660", GROUP="input", OPTIONS+="static_node=uinput"
sudo usermod -aG input $USER
```

If run in unprivileged container environments or CI runners without `/dev/uinput`, pass `--dry-run` to execute full kinematic simulation loops without hardware failure.

---

## 5. Anti-Stuck & Anti-Hang Watchdog Protocol (`game-test-watchdog`)

Automated game playtests frequently encounter deadlocks, infinite level-load transitions, repeating script loops, or unhandled crash windows (`notepad.exe` / BugTrap) that stall AI test harnesses indefinitely.

The `game-test-watchdog` utility (`game_test_watchdog.py`) actively supervises running game tests to guarantee autonomous forward momentum.

### Watchdog Capabilities
1. **Log Stagnation Trapping:** Automatically flags and aborts when game engine logs stop updating for > 60 seconds (customizable via `--timeout`).
2. **Infinite Loop Detection:** Detects repeated identical log lines or action cycles (e.g. repeated teleports or recursion loops > 5 occurrences) and terminates the process before quota/time is wasted.
3. **Modal Window Interception:** Sweeps Wine Notepad windows (`xray_*.log - Notepad`) and error dialogs so background tests never hang waiting for manual clicks.
4. **Autonomous Cleanup & Triage:** Automatically captures a diagnostic window screenshot, extracts the tail of the log/stack trace, and terminates the hung process tree (`SIGTERM` -> `SIGKILL`).
5. **Orphaned Process Sweeper:** `game-test-watchdog sweep` cleanly kills lingering background game instances so subsequent tests never hit "already running; refusing".

### CLI Usage
```bash
# Monitor a running game test harness and terminate if frozen or stuck in a loop
game-test-watchdog watch --pattern "xrEngine" --log-file _appdata_/logs/xrEngine.log --timeout 60 --max-loops 5

# Cleanly terminate any lingering or orphaned game processes & Wine modals
game-test-watchdog sweep

# Check status, CPU %, and memory of active game test processes
game-test-watchdog status
```

---

## 6. Powerhouse QA Toolchain Ecosystem

`game-qa-playtest-controller` acts as the kinematic core of a unified autonomous QA stack:

| Skill | Companion CLI | Integration Role |
| :--- | :--- | :--- |
| **`linux-game-window-input-capture`** | `game-window-helper` | Locks mouse cursor and isolates window focus so `/dev/uinput` relative motion never escapes the game viewport across multi-monitor setups. |
| **`game-autonomous-navigation-ai`** | `nav-graph-recorder` | Records and replays deterministic waypoint patrol paths across game levels, replacing purely random wandering with targeted route validation. |
| **`game-self-improving-qa-pipeline`** | `self-improving-qa` | Continuously analyzes playtest telemetry and crash logs to synthesize new regression test scripts and auto-repair broken locators. |
| **`game-dynamic-stress-orchestrator`** | `game-stress-orchestrator` | Injects synthetic chaos (CPU core saturation, frame pacing spikes, network packet loss) during locomotion to verify engine resilience. |
| **`game-performance-overlay-telemetry`** | `mangohud-configurator` | Configures zero-collision MangoHud telemetry overlays and logs frametimes, 1% lows, and VRAM usage throughout playtests. |

## Windows 10/11 & Cross-Platform Game Modding Parity (`windows-linux-cross-os-runtime-bridge`)
- **Native Windows vs. Linux Wine/Proton:** On Windows 10/11, execute `xrEngine.exe` and mod tools natively via DirectX 11/12 without Wine overhead. On Linux, route through Proton/Wine and DXVK/VKD3D.
- **LLP64 vs. LP64 64-Bit C++ Safety:** On Windows x64 MSVC/Clang-CL (LLP64), `long` and `unsigned long` (`DWORD`) are **32-bit (4 bytes)** whereas on Linux x86_64 (LP64) `long` is 64-bit. Never cast pointers to `long` or `DWORD`—always use `uintptr_t`, `intptr_t`, or `size_t`.
- **Crash Modal Interception & WER Dumps:** On Windows, `xray_crash_handler.py sweep` queries WMI (`Win32_Process`) and terminates lingering `notepad.exe`/`WerFault.exe` popups via `taskkill /F /PID`, reading logs from `%USERPROFILE%\Documents\STALKER-SHOC\logs` and `_appdata_\logs`.
- **Native Win32 Playtest Input & Window Capture:** When `sys.platform == "win32"`, `game_playtest_controller.py` automatically dispatches Win32 `keybd_event` / `mouse_event` (`SendInput`), `ClipCursor`, and `PIL.ImageGrab` instead of Linux `/dev/uinput` and `spectacle`.
- **Steam Library Auto-Discovery:** `steam-mod-scanner` automatically reads `HKCU\Software\Valve\Steam\SteamPath` and `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` on Windows alongside `~/.local/share/Steam` on Linux.

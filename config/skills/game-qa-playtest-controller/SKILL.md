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

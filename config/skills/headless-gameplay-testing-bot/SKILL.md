---
name: headless-gameplay-testing-bot
description: Autonomous cross-platform gameplay testing bot, synthetic input replay (uinput, adb input), regression fuzzing, and telemetry invariant assertions.
---

# Headless Gameplay Testing Bot (`headless-gameplay-testing-bot`)

Validating game stability, memory leaks, and gameplay regressions requires hours of continuous playtesting. Manual human testing cannot practically run on every CI commit or overnight test cycle.

This skill governs engine-agnostic automated playtesting, synthetic input injection via Linux `/dev/uinput` and Android `adb shell input`, and automated state invariant assertions.

---

## 1. Automated Testing Architecture

```
+-------------------------------------------------------------+
| Test Controller (Python / Bash Automation)                  |
+-------------------------------------------------------------+
       |                                              ^
       | Synthetic Inputs (uinput / adb input)        | Screen Telemetry & Logs
       v                                              |
+-------------------------------------------------------------+
| Running Game Instance (Godot, Unity, OGSR, C++ Vulkan Engine)|
+-------------------------------------------------------------+
       |
       v
+-------------------------------------------------------------+
| Invariant Watchdog:                                         |
| - Frametime P99 < 33.3ms (no freezes)                       |
| - VRAM / RAM growth < 50MB/hour (no memory leaks)           |
| - Player position within level navmesh (no fall-through)    |
| - Zero segfaults / BugTrap / SIGSEGV terminations           |
+-------------------------------------------------------------+
```

---

## 2. Input Injection Commands

### Linux Desktop (`/dev/uinput`):
```bash
# Inject 30 seconds of automated WASD movement and mouse sweep
python3 -c '
import time, evdev
from evdev import uinput, ecodes as e

ui = uinput.UInput({e.EV_KEY: [e.KEY_W, e.KEY_A, e.KEY_S, e.KEY_D, e.KEY_SPACE]})
for _ in range(10):
    ui.write(e.EV_KEY, e.KEY_W, 1); ui.syn(); time.sleep(1.0)
    ui.write(e.EV_KEY, e.KEY_SPACE, 1); ui.syn(); time.sleep(0.1)
    ui.write(e.EV_KEY, e.KEY_SPACE, 0); ui.syn()
    ui.write(e.EV_KEY, e.KEY_W, 0); ui.syn()
ui.close()
'
```

### Android ADB (`adb shell input`):
```bash
# Inject touch drag / movement joystick on Android
adb shell input swipe 300 1500 300 1200 1000
```

---

## 3. Invariant Assertion Contract

At the conclusion of an automated test run, verify:
1. **Process Exit Code:** Must be `0` (clean shutdown, not killed by OOM or SIGSEGV).
2. **Crash Log Cleanliness:** No `fatal error`, `assertion failed`, or unhandled exception in the game log.
3. **Framerate Telemetry:** P99 framerate above target minimum threshold.

---
name: game-self-improving-qa-pipeline
description: Closed-loop self-improving game QA test harness: automated loading screen dismissal, 88% loading stall watchdog, crash log harvesting, regression database tracking, and area test countdown timers.
---

# Self-Improving Game QA Pipeline (`game-self-improving-qa-pipeline`)

The `game-self-improving-qa-pipeline` skill provides an autonomous, closed-loop quality assurance framework for game development, engine porting, and mod playtesting (specialized for **S.T.A.L.K.E.R. X-Ray / OGSR / S.T.A.L.K.E.R. 2** and PC game testing under Wine/Proton and Linux).

---

## 1. Closed-Loop Self-Improving Architecture

Traditional QA testing simply records whether a game crashed or not. The **Self-Improving QA Pipeline** closes the loop:

```
[Autonomous Playtest] ──► [Failure Detected (Crash / Stall / Geometry Hole)]
          ▲                                 │
          │                                 ▼
[Regression Test Synthesis] ◄── [Regression DB (.agents/qa/regression_db.json)]
          │                                 │
          ▼                                 ▼
[Candidate Fix Applied] ◄──────── [Automated Root Cause Diagnosis]
```

1. **Failure Interception:** The pipeline traps crashes, freezes, and loading stalls.
2. **Regression Logging:** Logs world coordinates `(x, y, z)`, level vertex, and recent action sequence.
3. **Targeted Reproduction:** On subsequent test runs, the system replays the exact failure sequence to verify if candidate patches fix the bug without manual supervision.

---

## 2. Automated Loading Screen Flow & Watchdogs

### A. "Press Any Key to Play" Auto-Dismissal
- **Problem:** Many game engines pause at 100% loading progress and require a keyboard or mouse click to transition into gameplay (`Press any key to continue...`). In unattended testing, this stalls test execution indefinitely.
- **Solution:** Automatically detects when the loading bar completes and injects a simulated `Space` or `Return` keystroke via `xdotool` or `/dev/uinput`.

### B. The 88% Loading Stall Watchdog
- **Problem:** In S.T.A.L.K.E.R. X-Ray / OGSR, level loading often hangs at **88%** (during "Creating new game" or "Synchronizing...").
- **Root Cause:**
  - Missing spawn section in `all.spawn` or missing model texture (`.dds`).
  - Thread deadlock in dynamic shader compilation or audio device enumeration.
- **Action:** If the loading bar stays frozen at 88% for $> 60\text{s}$, the watchdog harvests the recent lines from `xray_<user>.log`, terminates the hung process, and records the offending spawn ID.

---

## 3. Crash Interception & Modal Dismissal

When X-Ray or PC games crash under Wine/Proton, they often spawn a modal error dialog (`xray_*.log - Notepad` or `BugTrap.dll`). While this window is open, the game process stays half-alive, blocking CI pipelines.

```bash
# Sweep and terminate hung crash windows:
python3 config/skills/game-self-improving-qa-pipeline/scripts/self_improving_qa.py sweep-crashes
```

---

## 4. Test Duration & Countdown HUD

When conducting soak tests or profiling performance across different levels (e.g. 5 minutes in Cordon, 5 minutes in Garbage, 5 minutes in Underground):

```bash
# Run 5-minute countdown for Cordon:
python3 config/skills/game-self-improving-qa-pipeline/scripts/self_improving_qa.py countdown --seconds 300 --area "Cordon"
```

---

## 5. Helper Script Reference: `self-improving-qa`

| Command | Action |
| :--- | :--- |
| **`dismiss-loading`** | Injects keypress to advance past 'Press any key to play' screens |
| **`sweep-crashes`** | Sweeps and kills blocking Notepad / BugTrap dialogs |
| **`countdown`** | Runs live terminal timer for area soak tests |
| **`log-flaw`** | Stores failure telemetry into the central regression database |

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`game-autonomous-navigation-ai`**: Autonomous AI player navigation, level vertex/waypoint graph mapping, route recording & playback, obstacle/inv...
- **`game-exploratory-fuzzing`**: Evolutionary input fuzzing, novelty-guided action mutation, and crash delta minimization for automated game QA...
- **`game-screen-telemetry-monitor`**: Real-time in-game screen telemetry monitoring, visual anomaly detection (missing textures, freezes, blackouts)...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

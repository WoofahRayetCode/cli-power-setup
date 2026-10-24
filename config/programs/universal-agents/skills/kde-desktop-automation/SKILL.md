---
name: kde-desktop-automation
description: KDE Plasma 6 KWin window scripting, multi-monitor layouts, Kitty terminal sockets, focus protection, and desktop service menus.
---

# KDE Desktop & Window Automation (`kde-desktop-automation`)

Governs KDE Plasma 6, KWin window management, dual-screen terminal layouts, and desktop shell integration for developer productivity and game test automation.

## Core Capabilities

- **KWin Window Rules (`kwinrulesrc`):**
  - Extreme focus-stealing prevention for headless/game binaries (`kwinrule_*.ini`).
  - Stacking order enforcement: keeping game windows top-left and terminal windows underneath without focus-stealing collisions.
- **Dynamic Multi-Monitor Layouts:**
  - Automated detection of single-panel vs. dual-screen setups (`eDP-1` + `HDMI-A-1`).
  - KWin JavaScript engine scripting (`workspace.clientArea`, `frameGeometry`, `keepAbove`).
  - Real-time window re-fitting when targets change resolution or restart.
- **Kitty Terminal Sockets & Automation:**
  - Remote control via Unix domain sockets (`--listen-on unix:/tmp/kitty-yolo`).
  - Seamless clipboard integration with Wayland (`wl-clipboard`, `smart_paste.py`).
  - Font scaling and dedicated status panes (`stalker-status`, `stalker-ops`).
- **Desktop Entry Integration:**
  - Application launchers (`.desktop`) with `--hold` parameterization for terminal visibility during debugging.
  - Dolphin file manager contextual service menus (`~/.local/share/kio/servicemenus/`).
- **Power & DPMS Automation:**
  - `powerdevilrc` profile adjustments (`kwriteconfig6`) for automated screen timeout controls.
  - Non-destructive display wake hooks (`dpms.py`).

## Key Tools & References
- Layout definition: `LAYOUT.md`
- KWin scripts: `config/system-tweaks/kwin/`
- Rule installer: `scripts/restore-system-tweaks.sh`
- Window dimmer: `config/ogsr-port-tools/dimmer.py`

## Related Skills
- **`linux-systems-engineering`**: Linux systems programming, POSIX, and systemd.
- **`autonomous-game-qa-playtesting`**: Nav-graph execution and headless window testing.

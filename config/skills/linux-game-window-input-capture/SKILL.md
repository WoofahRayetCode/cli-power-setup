---
name: linux-game-window-input-capture
description: Linux game window containment, mouse grab/confinement, focus isolation, and dual-monitor multitasking under Wine/Proton, Gamescope, Wayland, and X11.
---

# Linux Game Window & Input Capture (`linux-game-window-input-capture`)

The `linux-game-window-input-capture` skill provides configurations, scripts, and runtime recipes for managing mouse capture, cursor confinement, borderless windowing, and focus-stealing prevention during game development and automated testing on Linux (Wine, Proton, Gamescope, Wayland, X11).

---

## 1. Core Windowing & Input Challenges

When running games under Wine/Proton while concurrently working in Claude Code CLI or IDEs, three common failure modes occur:

1. **Mouse Escapes Game Viewport:** Moving the camera rapidly throws the cursor onto a secondary monitor or into the desktop taskbar, causing accidental clicks outside the game window.
2. **Cursor Trapped on Alt-Tab:** The game refuses to release mouse focus when Alt-Tabbing, preventing the developer from clicking or typing in the terminal.
3. **Focus Stealing:** The game window repeatedly grabs keyboard focus back from the terminal, interrupting commands typed into Claude Code.

---

## 2. Pointer Grab & Mouse Confinement Solutions

### A. Gamescope Sandboxing (Recommended)
Gamescope creates an isolated micro-compositor where cursor confinement is handled at the Wayland compositor level, completely preventing mouse drift:

```bash
# Launch with explicit cursor grab and borderless window:
gamescope -W 1920 -H 1080 -b --grab --force-grab-cursor --mangoapp -- wine bin/x64/xrEngine.exe
```
- Pressing `Super + S` or standard `Alt + Tab` cleanly releases cursor confinement back to the host desktop without minimizing the game.

### B. Wine Registry Pointer Clipping
To enforce strict viewport confinement inside standard Wine:

```ini
; HKCU\Software\Wine\X11 Driver
"GrabPointer"="Y"

; HKCU\Software\Wine\DirectInput
"MouseWarpOverride"="enable"
```

Command-line application:
```bash
wine reg add "HKCU\Software\Wine\X11 Driver" /v GrabPointer /t REG_SZ /d "Y" /f
wine reg add "HKCU\Software\Wine\DirectInput" /v MouseWarpOverride /t REG_SZ /d "enable" /f
```

---

## 3. Borderless Windowing vs Fullscreen

To prevent GPU display mode resets and flickering when switching between terminal and game:

- **S.T.A.L.K.E.R. / OGSR user.ltx:**
  ```ini
  rs_fullscreen off     ; Enables windowed mode
  ```
- **CLI Launch Arguments:**
  ```bash
  wine bin/x64/xrEngine.exe -windowed -center_screen
  ```

---

## 4. Focus-Stealing Prevention

To stop a running game process from interrupting active typing in the terminal:

### KDE Plasma / KWin
```bash
# Set Focus Stealing Prevention to High
kwriteconfig5 --file kwinrc --group Windows --key FocusStealingPrevention 3
# Or on Plasma 6:
kwriteconfig6 --file kwinrc --group Windows --key FocusStealingPrevention 3
```

### Gamescope Sandbox
Gamescope naturally encapsulates window activation signals (`_NET_ACTIVE_WINDOW`), preventing any child Windows executable from asserting focus over native host terminal emulators (Alacritty, Kitty, Konsole).

---

## 5. Helper Script: `game-window-helper`

Use `game_window_helper.sh` for one-command fixes:

```bash
# Run game sandboxed with locked cursor and MangoHud:
config/skills/linux-game-window-input-capture/scripts/game_window_helper.sh run-gamescope wine xrEngine.exe

# Configure pointer grab in Wineprefix:
config/skills/linux-game-window-input-capture/scripts/game_window_helper.sh configure-wine-mouse ~/.wine

# Toggle game between fullscreen and windowed in user.ltx:
config/skills/linux-game-window-input-capture/scripts/game_window_helper.sh toggle-windowed gamedata/user.ltx
```

---
name: linux-gaming-proton-optimization
description: Optimizing and fixing games under Linux, Wine, Steam Proton, and Steam Deck. Covers GE-Proton switching, dxvk.conf tuning, async shader compilation, GameMode, Gamescope micro-compositing, Winetricks prefix repair, Media Foundation cutscene codec fixes, and anti-cheat compatibility triage.
---

# Linux Gaming, Steam Proton & Steam Deck Optimization

This skill provides an advanced optimization and repair protocol for running Windows games on Linux distributions (CachyOS, Arch, Fedora, Ubuntu) and Steam Deck via Valve's Proton and Wine.

---

## 1. Proton Wine Prefix Troubleshooting Architecture

Proton creates an isolated simulated Windows filesystem for each game in:
`~/.steam/steam/steamapps/compatdata/<appid>/pfx/`

### A. Non-Destructive Prefix Repair
When a game fails after an update or crashes with missing DLL errors:
```bash
# 1. Update wineprefix registry & recreate system directories without losing save states
protontricks -c "wineboot -u" <appid>

# 2. Install missing Microsoft Visual C++ redistributables & DirectX runtimes
protontricks <appid> vcrun2022 d3dcompiler_47 d3dx9

# 3. Fix missing Windows Media Foundation video playback (black video cutscenes)
protontricks <appid> mfplat
```

### B. Proton-GE (GloriousEggroll) Integration
Proton-GE includes upstream Wine patches, ffmpeg cutscene decoding, and FSR/DLSS enhancements not yet included in Valve's Proton Experimental.
- When games show video test screens or crash on opening cutscenes, select **GE-Proton** in Steam Game Properties -> Compatibility -> Force the use of a specific Steam Play compatibility tool.

---

## 2. DXVK & VKD3D-Proton Performance Tuning

Create or edit `dxvk.conf` in the directory containing the game's executable (`.exe`):

```ini
# Asynchronous pipeline compilation (eliminates shader compilation micro-stutters)
dxvk.enableAsync = true
dxvk.numCompilerThreads = 12

# Max frame latency (reduces mouse input lag to 1 frame)
dxvk.maxFrameLatency = 1

# Limit frame rate cleanly within the Vulkan presentation queue
dxvk.maxFrameRate = 144

# Expose AMD or Nvidia GPU vendor ID to bypass broken vendor checks
# dxvk.customDeviceId = 10de  # NVIDIA
# dxvk.customVendorId = 1002  # AMD
```

---

## 3. High-Performance Launch Command Recipes

Use these specialized launch options in Steam Properties (`%command%` syntax):

### A. The Ultimate Low-Latency & Performance Stack
Combines Feral GameMode (CPU governor, I/O priority), MangoHud, and Gamescope micro-compositor:
```bash
gamemoderun mangohud gamescope -W 2560 -H 1440 -r 144 --adaptive-sync --fsr -e -- %command%
```

### B. Custom Native DLL Override (Mods & ASI Loaders)
When using mods, ENB, ReShade, or custom `.dll` wrappers (`dinput8.dll`, `version.dll`, `dxgi.dll`):
```bash
WINEDLLOVERRIDES="dinput8=n,b;version=n,b;dxgi=n,b" %command%
```
*(Tells Wine to load the local 'native' mod DLL first, falling back to 'builtin' Wine libraries only if missing).*

### C. Steam Deck Power & Battery Tuning
For battery-efficient 40Hz/40FPS or 45Hz/45FPS locked gameplay:
```bash
MANGOHUD_CONFIG=fps_limit=45,no_display gamemoderun %command%
```

### D. MangoHud Performance Telemetry (`game-performance-overlay-telemetry`)
Use `mangohud-configurator` to generate custom HUD layouts, frametime graphs, and non-overlapping positioning:
```bash
mangohud-configurator apply --preset competitive --position top-right
```

---

## 4. Anti-Cheat Compatibility Triage (Easy Anti-Cheat / BattlEye)

Before troubleshooting network or kick errors, verify anti-cheat Linux support:
1. **Easy Anti-Cheat (EAC):**
   - Requires developers to enable the EAC Linux runtime module (`easyanticheat_x64.so`).
   - If missing from game directory, install Steam's "Proton EasyAntiCheat Runtime".
2. **BattlEye:**
   - Requires "Proton BattlEye Runtime" installed via Steam client.
3. **Kernel-Level Anti-Cheats (Vanguard, Ricochet, EA AntiCheat):**
   - Strictly incompatible with Linux / Wine due to ring-0 kernel driver dependencies. Guide user toward dual-boot or Windows VM with GPU passthrough.

---

## 5. Dual-Monitor Cursor Confinement & Window Capture (`linux-game-window-input-capture`)

Games running under Proton or Wine on multi-monitor setups often suffer from cursor drift—where fast mouse flicks escape the game window onto a secondary screen, causing inadvertent window defocus or accidental clicks.

Use `game-window-helper` to lock the cursor and isolate window focus:
```bash
# Lock cursor and capture focus to active Proton game window
game-window-helper lock --pattern "steam_app" --borderless

# Release mouse confinement on exit
game-window-helper release
```


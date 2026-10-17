---
name: steamdeck-proton-hardware-tuning
description: Steam Deck & handheld Linux hardware optimization for Proton games. Covers 15W TDP power budgets, 40Hz/45Hz refresh rate frame pacing, 1280x800 16:10 aspect ratio handling, font readability scaling, and battery longevity tuning.
---

# Steam Deck & Handheld Linux Proton Hardware Tuning

This skill guides game development and engine tuning to achieve optimal performance, battery life, and visual legibility on handheld Linux devices (Steam Deck OLED/LCD, ROG Ally on Bazzite/CachyOS, Legion Go).

---

## 1. Handheld Power Budgets & Frame Pacing

On handheld devices, power consumption is constrained to a 15W APU TDP envelope (CPU + GPU combined):

### A. 40Hz / 45Hz Frame Rate Targets
* Running games at 60 FPS consumes significantly more power and causes thermal throttling on handheld APUs.
* **The 40Hz / 25ms Sweet Spot:**
  - 60 FPS = 16.6ms frametime (high battery burn, ~1.5 hours runtime).
  - 30 FPS = 33.3ms frametime (sluggish input response).
  - **40 FPS @ 40Hz = 25.0ms frametime:** Delivers smooth input latency exactly halfway between 30 and 60 FPS, while cutting GPU load by ~33% and extending battery life to 3.5+ hours.

### B. Frame Pacing & Latency Control
Avoid internal frame accumulators that cause stutter when handheld screen refresh rates change:
```ini
# Recommended dxvk.conf for handheld targets
dxvk.maxFrameLatency = 1
dxvk.tearFree = false
```

---

## 2. 16:10 Display Aspect Ratio & Font Legibility

### A. 1280x800 Native Resolution
* The Steam Deck uses a native 1280x800 (16:10) display panel.
* If a game only renders in 16:9 (1280x720), letterboxing (black bars on top and bottom) occurs.
* **Requirement:** Expose full 16:10 resolutions natively, adjusting camera vertical FOV rather than horizontally cropping UI.

### B. Small Screen Font Scaling (Deck Verified Rule)
* On a 7-inch or 7.4-inch screen held at 30–40cm distance, standard 1080p desktop fonts become completely illegible.
* **The Rule:** Any UI text, subtitles, or inventory item tooltips must render with a minimum physical height equivalent to **28 pixels at 1280x800** (or ~9.2mm on screen). Provide an in-game "Large UI / Handheld Mode" toggle.

---

## 3. Storage I/O Optimization (MicroSD Cards)

Many Steam Deck users install games onto MicroSD cards (UHS-I / ~100MB/s sequential read):
* Uncompressed loose assets result in thousands of seek operations that stutter gameplay during streaming.
* Pack game assets into chunked compressed virtual containers (`game-asset-pack-archive-engineering`) using **zstd level 3** compression to minimize storage bus bottlenecks.

## Windows 10/11 & Cross-Platform Game Modding Parity (`windows-linux-cross-os-runtime-bridge`)
- **Native Windows vs. Linux Wine/Proton:** On Windows 10/11, execute `xrEngine.exe` and mod tools natively via DirectX 11/12 without Wine overhead. On Linux, route through Proton/Wine and DXVK/VKD3D.
- **LLP64 vs. LP64 64-Bit C++ Safety:** On Windows x64 MSVC/Clang-CL (LLP64), `long` and `unsigned long` (`DWORD`) are **32-bit (4 bytes)** whereas on Linux x86_64 (LP64) `long` is 64-bit. Never cast pointers to `long` or `DWORD`—always use `uintptr_t`, `intptr_t`, or `size_t`.
- **Crash Modal Interception & WER Dumps:** On Windows, `xray_crash_handler.py sweep` queries WMI (`Win32_Process`) and terminates lingering `notepad.exe`/`WerFault.exe` popups via `taskkill /F /PID`, reading logs from `%USERPROFILE%\Documents\STALKER-SHOC\logs` and `_appdata_\logs`.
- **Native Win32 Playtest Input & Window Capture:** When `sys.platform == "win32"`, `game_playtest_controller.py` automatically dispatches Win32 `keybd_event` / `mouse_event` (`SendInput`), `ClipCursor`, and `PIL.ImageGrab` instead of Linux `/dev/uinput` and `spectacle`.
- **Steam Library Auto-Discovery:** `steam-mod-scanner` automatically reads `HKCU\Software\Valve\Steam\SteamPath` and `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` on Windows alongside `~/.local/share/Steam` on Linux.

## Related & Interoperating Skills
- **`mobile-thermal-frame-pacing`**: Mobile thermal management, Android Swappy frame pacing, dynamic resolution scaling (DRS), and battery efficien...
- **`game-performance-overlay-telemetry`**: In-game HUD performance metrics and telemetry profiling (MangoHud, DXVK HUD, PresentMon). Configures FPS, fram...
- **`cross-platform-game-compatibility`**: Diagnosing and repairing legacy and modern PC games to run smoothly across Windows and Linux. Covers DirectX l...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

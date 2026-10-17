---
name: dxvk-vkd3d-proton-pipeline-profiler
description: Diagnoses and eliminates DXVK and VKD3D-Proton shader compilation stutter, descriptor heap stalls, and VRAM staging bottlenecks for DX11/DX12 games running on Linux.
---

# DXVK & VKD3D-Proton Pipeline Profiler (`dxvk-vkd3d-proton-pipeline-profiler`)

When running DirectX 11 (e.g. S.T.A.L.K.E.R. OGSR) or DirectX 12 (e.g. S.T.A.L.K.E.R. 2) games on Linux via Wine/Proton, severe framerate drops (e.g. 120 FPS dropping to 10 FPS on save load) are frequently caused by the translation layer rather than CPU game logic:
- Synchronous `VkPipeline` compilation blocking the render thread.
- Dynamic constant buffer / staging buffer reallocation (`D3D11_USAGE_DYNAMIC` thrashing).
- VRAM oversubscription pushing textures into system RAM over PCIe.

This skill provides automated telemetry extraction and `dxvk.conf` optimization for Gemini.

---

## 1. Automated DXVK Telemetry Extraction

Launch the game with telemetry logging enabled and extract the bottleneck summary:

```bash
# Run test with DXVK log and HUD telemetry
DXVK_LOG_LEVEL=info DXVK_LOG_PATH=/tmp/dxvk_logs \
DXVK_HUD=devinfo,fps,frametimes,submissions,drawcalls,pipelines,memory,gpuload,compiler \
./tools/save_fps.sh xrEngine.exe test_save 30 25

# Inspect DXVK log for pipeline stalls or memory warnings
grep -iE "warn|err|Compiling|allocated|evicted" /tmp/dxvk_logs/*.log | head -n 30
```

---

## 2. Diagnostic Signatures & High-Performance `dxvk.conf` Fixes

| Observed Symptom | Root Cause in Translation Layer | `dxvk.conf` Surgical Fix |
| :--- | :--- | :--- |
| **Massive stutter when loading save or spawning NPCs** | Synchronous shader compilation blocking main render queue | `dxvk.enableGraphicsPipelineLibrary = True`<br>`dxvk.numCompilerThreads = 8` |
| **10 FPS with low GPU load & high draw-call overhead** | Engine mapping/unmapping constant buffers every draw call | `d3d11.cachedDynamicResources = a`<br>`d3d11.maxImplicitDiscardSize = 256` |
| **Framerate collapses after 2nd level load** | VRAM fragmentation / un-evicted staging buffers | `dxvk.maxChunkSize = 64`<br>`d3d11.relaxedBarriers = True` |
| **High frame latency / input lag on Wayland** | FIFO vs Immediate mailbox presentation mismatch | `dxvk.tearFree = False`<br>`d3d11.syncInterval = 0` |

---

## 3. Production `dxvk.conf` Template for X-Ray / OGSR Engine

Place in the game executable directory alongside `xrEngine.exe`:

```ini
# High-velocity OGSR / X-Ray DX11 -> Vulkan configuration
dxvk.enableGraphicsPipelineLibrary = True
dxvk.trackPipelineLifetime = True
d3d11.cachedDynamicResources = a
d3d11.relaxedBarriers = True
d3d11.ignoreGraphicsBarriers = True
d3d11.maxTessFactor = 16
dxvk.numCompilerThreads = 0
```

## Windows 10/11 & Cross-Platform Game Modding Parity (`windows-linux-cross-os-runtime-bridge`)
- **Native Windows vs. Linux Wine/Proton:** On Windows 10/11, execute `xrEngine.exe` and mod tools natively via DirectX 11/12 without Wine overhead. On Linux, route through Proton/Wine and DXVK/VKD3D.
- **LLP64 vs. LP64 64-Bit C++ Safety:** On Windows x64 MSVC/Clang-CL (LLP64), `long` and `unsigned long` (`DWORD`) are **32-bit (4 bytes)** whereas on Linux x86_64 (LP64) `long` is 64-bit. Never cast pointers to `long` or `DWORD`—always use `uintptr_t`, `intptr_t`, or `size_t`.
- **Crash Modal Interception & WER Dumps:** On Windows, `xray_crash_handler.py sweep` queries WMI (`Win32_Process`) and terminates lingering `notepad.exe`/`WerFault.exe` popups via `taskkill /F /PID`, reading logs from `%USERPROFILE%\Documents\STALKER-SHOC\logs` and `_appdata_\logs`.
- **Native Win32 Playtest Input & Window Capture:** When `sys.platform == "win32"`, `game_playtest_controller.py` automatically dispatches Win32 `keybd_event` / `mouse_event` (`SendInput`), `ClipCursor`, and `PIL.ImageGrab` instead of Linux `/dev/uinput` and `spectacle`.
- **Steam Library Auto-Discovery:** `steam-mod-scanner` automatically reads `HKCU\Software\Valve\Steam\SteamPath` and `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` on Windows alongside `~/.local/share/Steam` on Linux.

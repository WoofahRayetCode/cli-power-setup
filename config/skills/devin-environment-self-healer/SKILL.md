---
name: devin-environment-self-healer
description: Emulates Cognition Devin autonomous environment self-healing. Automatically diagnoses missing host dependencies, dynamic libraries (.so), and compiler toolchains on Linux (CachyOS/Arch).
---

# Devin Environment Self-Healer (`devin-environment-self-healer`)

Cognition Devin's hallmark is autonomous recovery from environment and tooling failures. When a build or test fails due to missing shared libraries, outdated packages, or missing header packages, it diagnoses the missing system dependency and restores the environment instead of halting.

This skill equips Gemini 4 Argon with self-healing capabilities on Linux (CachyOS / Arch Linux).

---

## 1. Automated Diagnosis Patterns

| Error Output Signature | Root Cause | Self-Healing Resolution |
| :--- | :--- | :--- |
| `fatal error: vulkan/vulkan.h: No such file` | Missing Vulkan development headers | Check `pacman -Q vulkan-headers` or install via host |
| `error while loading shared libraries: libX.so` | Missing runtime dynamic library | Run `find /usr/lib -name "libX*"` or resolve package via `pacman -F` |
| `CMake Error: Could not find package X` | Missing CMake find module or pkg-config | Query `pkg-config --modversion X` |
| `ModuleNotFoundError: No module named 'X'` | Missing Python automation dependency | Check `python3 -m pip show X` |

---

## 2. Invariant Safety Guardrails

1. **Non-Interactive Verification First:** Always verify package status non-destructively:
   ```bash
   pacman -Q <package_name> 2>/dev/null || true
   ```
2. **Never Run Dangerous Root Commands:** Never execute destructive operations (`rm -rf`, raw forced package overwrites).
3. **Local Tooling First:** Look in `~/.local/bin/` or virtual environments before modifying system packages.

## Windows 10/11 Native Counterparts (`windows-linux-cross-os-runtime-bridge`)
- **Packages & Toolchains:** Use `winget` / `scoop` / `choco` and `vswhere.exe` (MSVC / Clang-CL) on Windows in place of `pacman` / `yay`. For desktop packaging on Windows, target MSIX / WiX / WinGet manifests (`windows-app-engineering`).
- **Profiling & Time-Travel Debugging:** On Windows 10/11, use **Windows Performance Recorder (`wpr -start GeneralProfile` / `wpa.exe`)** in place of Linux `perf`, and **WinDbg Preview Time-Travel Debugging (`ttd.exe -launch <app.exe>`)** in place of Mozilla `rr`.
- **Hardware, Thermal & Power Profiles:** Query sensors via WMI/CIM (`Get-CimInstance -Namespace root/wmi MSAcpi_ThermalZoneTemperature`, `nvidia-smi`) and switch power plans via `powercfg /setactive` on Windows.
- **File System Hot-Reload & ADB:** Use `.NET System.IO.FileSystemWatcher` (`Register-ObjectEvent`) on Windows in place of `inotifywait`, and resolve `adb.exe` from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`.

## Related & Interoperating Skills
- **`grok-realtime-telemetry-scout`**: Emulates xAI Grok real-time live search on Gemini 4 Argon. Scouts bleeding-edge git commits, pull requests, is...
- **`game-runtime-diagnostics`**: Cross-platform game crash diagnostics, performance tuning, and compatibility triage across Windows (DirectX, E...
- **`cachyos-arch-packaging`**: Arch Linux and CachyOS packaging standards, PKGBUILD authoring, DKMS kernel module builds, and systemd service...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

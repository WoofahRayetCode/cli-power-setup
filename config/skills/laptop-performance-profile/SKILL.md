---
name: laptop-performance-profile
description: Laptop performance tuning, thermal management, and acoustic control. Integrates OMEN Space (omen-cli / omen-space-daemon), ACPI/WMI sysfs, and power-profiles-daemon for whisper-quiet night runs, balanced daily operation, and turbo boost execution.
---

# Laptop Performance & Thermal Profile Engineering

This skill governs laptop hardware performance states, thermal throttling limits, fan acoustic tiers, and battery care policies. It features primary integration with **OMEN Space** (`omen-cli` / `omen-space-daemon`) for HP OMEN / Victus laptops, and automatic fallback to Linux `power-profiles-daemon` and kernel sysfs.

---

## 🎛️ 1. Performance Tiers & Acoustic Profiles

| Profile | Target PL1/PL2 | Fan Curve Profile | Acoustic Profile | Best Used For |
| :--- | :--- | :--- | :--- | :--- |
| **`quiet` / `power-saver`** | 25W - 35W | Sub-silent (< 2500 RPM) | Whisper quiet (< 28 dBA) | Overnight agent runs, user sleeping, low-power background jobs |
| **`balanced`** | 45W / 80W | Dynamic Auto Curve | Moderate (35 - 42 dBA) | Standard coding, git operations, browser browsing, chat |
| **`performance` / `turbo`** | 80W+ / Max TGP | Aggressive / Max Fan | Loud / Maximum Cooling | Heavy C++/Rust compilation, 3D rendering, game QA playtests |

---

## 💻 2. OMEN Space Architecture & CLI Control

The host laptop utilizes **OMEN Space** (`omen-cli` / `omen-space-daemon`) backed by the `omen-acpi` driver:

```bash
# Display full system, thermal, fan RPM, and power limit summary
omen-cli fetch

# Power profile switching
omen-cli power set-profile power-saver
omen-cli power set-profile balanced
omen-cli power set-profile performance

# Fan mode override
omen-cli fan set-mode auto
omen-cli fan set-mode max

# Battery Care (Limit charging to 80% to protect battery longevity)
omen-cli system battery-care 80
```

---

## 🌙 3. Sleep, Lid-Closed (`clamshell-3d`) & Night-Time Acoustic Governance

When the user is resting, napping, or closes the laptop lid during autonomous 3D / coding runs:
* **Rule:** Never allow background tasks to spin fans up to maximum RPM or heat-soak the closed keyboard deck against the OLED/IPS screen panel.
* **Lid-Closed 3D Blender / OptiX Mode (`clamshell-3d`):**
  ```bash
  laptop-perf clamshell-3d
  # (or: python3 scripts/laptop_performance_controller.py clamshell-3d)
  ```
  - Acquires a detached `systemd-inhibit --what=handle-lid-switch:sleep:idle` block lock (`~/.cache/agy_lid_inhibit.pid`) on top of KDE PowerDevil's `LidAction=64` (Turn Off Screen), guaranteeing the laptop **never suspends** when the lid is closed.
  - Caps CPU PL1/PL2 to `power-saver` (`25W–35W`) with `auto` fans (`< 28 dBA`) so the top keyboard deck stays cool (`< 68°C`) while closed.
  - Keeps the **NVIDIA RTX 5060 GPU** fully available for headless Blender 5.2+ (`blender -b -E CYCLES -- --cycles-device OPTIX`) and offscreen EGL EEVEE rendering, which operate 100% without an active display.
* **Wake / Daytime Restoration (`wake-mode`):**
  ```bash
  laptop-perf wake-mode
  ```
  - Releases the lid-switch inhibitor lock and restores the `balanced` profile.

---

## 🚀 4. Transient Boost & Context Manager

For heavy bursts of compute (e.g. compiling large C++ projects with `-j$(nproc)`, building wine/proton binaries, or running 3D playtest sessions), scale up temporarily and revert cleanly.

### CLI Boost Wrapper:
```bash
python3 scripts/laptop_performance_controller.py boost-exec cargo build --release -j$(nproc)
```

### Python Context Manager API:
```python
from laptop_performance_controller import PerformanceContext, get_thermal_telemetry

# Inspect current thermal state
telemetry = get_thermal_telemetry()
print(f"CPU: {telemetry['cpu_temp']}, GPU: {telemetry['gpu_temp']}")

# Temporarily boost to performance mode, auto-reverting when done
with PerformanceContext("performance"):
    run_heavy_compilation_or_playtest()
# Profile automatically restored to previous state
```

---

## 🛡️ 5. Thermal Telemetry & Fallback Chain

`laptop_performance_controller.py` implements a resilient 3-layer discovery chain:
1. **Tier 1 (OMEN Space):** `omen-cli` queries embedded controller and ACPI daemon.
2. **Tier 2 (Freedesktop PPD):** `powerprofilesctl` for GNOME / generic Linux laptops.
3. **Tier 3 (Hardware Telemetry):** `nvidia-smi` and `lm_sensors` (`k10temp`, `amdgpu`, `acpitz`) for real-time temperature verification.

## Windows 10/11 Native Counterparts (`windows-linux-cross-os-runtime-bridge`)
- **Packages & Toolchains:** Use `winget` / `scoop` / `choco` and `vswhere.exe` (MSVC / Clang-CL) on Windows in place of `pacman` / `yay`. For desktop packaging on Windows, target MSIX / WiX / WinGet manifests (`windows-app-engineering`).
- **Profiling & Time-Travel Debugging:** On Windows 10/11, use **Windows Performance Recorder (`wpr -start GeneralProfile` / `wpa.exe`)** in place of Linux `perf`, and **WinDbg Preview Time-Travel Debugging (`ttd.exe -launch <app.exe>`)** in place of Mozilla `rr`.
- **Hardware, Thermal & Power Profiles:** Query sensors via WMI/CIM (`Get-CimInstance -Namespace root/wmi MSAcpi_ThermalZoneTemperature`, `nvidia-smi`) and switch power plans via `powercfg /setactive` on Windows.
- **File System Hot-Reload & ADB:** Use `.NET System.IO.FileSystemWatcher` (`Register-ObjectEvent`) on Windows in place of `inotifywait`, and resolve `adb.exe` from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`.

## Related & Interoperating Skills
- **`linux-hardware-acpi`**: Linux kernel ACPI module development, DSDT/SSDT table analysis, hwmon sensor interfaces, thermal fan curves, a...
- **`hardware-tool-engineering`**: Architect, build, and update hardware management tools, system daemons, sensors, and thermal controllers with ...
- **`mobile-thermal-frame-pacing`**: Mobile thermal management, Android Swappy frame pacing, dynamic resolution scaling (DRS), and battery efficien...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

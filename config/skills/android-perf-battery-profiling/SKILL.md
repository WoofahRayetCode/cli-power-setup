---
name: android-perf-battery-profiling
description: Low-level Android performance profiling, frame rate/jank diagnosis (dumpsys gfxinfo), battery consumption analysis (dumpsys batterystats), Perfetto system tracing, memory leak detection (heap dump triage), and StrictMode violation traps. Use when diagnosing Android app slowness, frame drops, or battery drain.
---

# Android Performance, Frame Rate & Battery Profiling

This skill provides methodologies and automated tools for analyzing frame rendering performance, CPU utilization, battery drain, and memory leaks on Android devices over ADB.

---

## 1. Frame Rate & Jank Diagnosis (`gfxinfo`)

Android apps target 60Hz (16.6ms), 90Hz (11.1ms), or 120Hz (8.3ms) frame deadlines.
* Inspect frame timing histograms directly over ADB:
  ```bash
  adb shell dumpsys gfxinfo <package_name> framestats
  ```
* **Key Metrics:**
  * **Janky Frames:** Percentage of frames that missed the VSYNC deadline. Target: $< 1.0\%$.
  * **90th / 95th / 99th Percentile Render Time:** Identifies tail latency spikes during list scrolling or navigation animations.

Run the included performance analyzer script:
```bash
python3 scripts/android_perf_inspector.py --package com.example.app --jank
```

---

## 2. Battery Consumption & Wake Lock Profiling

Runaway background services and unreleased wake locks drain device batteries rapidly:
1. **Reset Battery Stats:**
   ```bash
   adb shell dumpsys batterystats --reset
   ```
2. **Exercise the App:** Run workflows or let the device idle.
3. **Dump Battery Analytics:**
   ```bash
   adb shell dumpsys batterystats <package_name> | head -n 40
   ```
   * Inspect **WakeLocks:** Partial wake lock count and total duration.
   * Inspect **Alarms:** Wakeup alarm frequencies.
   * Inspect **JobScheduler:** Execution frequency and radio power usage.

---

## 3. Memory Leaks & Heap Dump Triage

To diagnose out-of-memory errors (`OutOfMemoryError`) or activity leaks:
1. **Trigger Garbage Collection & Dump Heap:**
   ```bash
   adb shell am dumpheap <package_name> /data/local/tmp/app_heap.hprof
   adb pull /data/local/tmp/app_heap.hprof ./app_heap.hprof
   ```
2. **Convert to Standard HPROF:**
   ```bash
   hprof-conv app_heap.hprof app_heap_converted.hprof
   ```
3. Open in Eclipse MAT, Android Studio Profiler, or inspect dominator trees to find retained instances of destroyed `Activity` or `Context` references.

---

## 4. Main-Thread StrictMode Enforcement

Enable `StrictMode` in debug builds to crash immediately when disk reads, network operations, or leaked closable objects occur on the UI main thread:
```kotlin
if (BuildConfig.DEBUG) {
    StrictMode.setThreadPolicy(
        StrictMode.ThreadPolicy.Builder()
            .detectDiskReads()
            .detectDiskWrites()
            .detectNetwork()
            .penaltyLog()
            .penaltyDeath()
            .build()
    )
}
```

## Windows 10/11 Native Counterparts (`windows-linux-cross-os-runtime-bridge`)
- **Packages & Toolchains:** Use `winget` / `scoop` / `choco` and `vswhere.exe` (MSVC / Clang-CL) on Windows in place of `pacman` / `yay`. For desktop packaging on Windows, target MSIX / WiX / WinGet manifests (`windows-app-engineering`).
- **Profiling & Time-Travel Debugging:** On Windows 10/11, use **Windows Performance Recorder (`wpr -start GeneralProfile` / `wpa.exe`)** in place of Linux `perf`, and **WinDbg Preview Time-Travel Debugging (`ttd.exe -launch <app.exe>`)** in place of Mozilla `rr`.
- **Hardware, Thermal & Power Profiles:** Query sensors via WMI/CIM (`Get-CimInstance -Namespace root/wmi MSAcpi_ThermalZoneTemperature`, `nvidia-smi`) and switch power plans via `powercfg /setactive` on Windows.
- **File System Hot-Reload & ADB:** Use `.NET System.IO.FileSystemWatcher` (`Register-ObjectEvent`) on Windows in place of `inotifywait`, and resolve `adb.exe` from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`.

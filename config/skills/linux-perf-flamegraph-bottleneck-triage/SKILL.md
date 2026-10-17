---
name: linux-perf-flamegraph-bottleneck-triage
description: Hardware performance counter profiling (perf record/report) and folded stack Flamegraph bottleneck triage for native Linux and Wine/Proton games. Pinpoints exact C++ functions causing severe FPS drops in seconds without blind bisecting.
---

# Linux Perf & Flamegraph Bottleneck Triage (`linux-perf-flamegraph-bottleneck-triage`)

When a game engine or application suffers from severe framerate degradation (e.g. dropping from 128 FPS to 10 FPS on save load), blind code bisection and recompilation loops waste hours of wall-clock time and hundreds of thousands of tokens.

This skill uses Linux kernel hardware performance counters (`perf`) to sample the live process for 5 seconds and extract the exact top-5 CPU hotspot functions into a compact, 20-line folded call-graph summary for Gemini.

---

## 1. 5-Second Live Hotspot Capture

Run while the game or application is exhibiting the slowdown:

```bash
# 1. Sample the running process (native or Wine/Proton) at 99Hz for 5 seconds
TARGET_PID=$(pgrep -n "xrEngine|game_bin")
perf record -F 99 -p "${TARGET_PID}" -g --call-graph dwarf -o /tmp/perf_hotspot.data -- sleep 5

# 2. Extract top-15 self-time and children-time symbols (clamped for token economy)
perf report -i /tmp/perf_hotspot.data --stdio --no-children -n --percent-limit 1.0 | grep -v "^#" | head -n 25
```

---

## 2. Folded Call-Stack Summary (SentencePiece Optimal)

To feed a complete Flamegraph hierarchy into Gemini using under 100 tokens, collapse the stack traces:

```bash
perf script -i /tmp/perf_hotspot.data | awk '
  /^[^\t]/ { func_chain="" }
  /^\t/ { gsub(/^[ \t]+/, ""); split($0, a, " "); func_chain = a[2] ";" func_chain }
  /^$/ { if (func_chain != "") count[func_chain]++ }
  END { for (k in count) print count[k] "|" k }
' | sort -t'|' -k1 -nr | head -n 15
```

### Example Output Read by Gemini:
```text
samples|call_chain
412|xrEngine.exe!CRender::Render;xrGame.dll!CPHWorld::Step;xrPhysics.dll!dInternalStepIsland_x2;
38|xrEngine.exe!CObjectList::Update;xrGame.dll!CInventoryOwner::UpdateInventory;
```
- **Immediate Diagnosis:** 91% of CPU time is trapped inside `CPHWorld::Step` (`dInternalStepIsland_x2` — physics island solver thrashing on colliding ragdolls/objects upon save load).
- **Time to Root Cause:** **5 seconds** instead of 2 hours of blind engine patch bisecting.

---

## 3. Wine / Proton Symbol Resolution

When profiling Windows PE binaries (`.exe` / `.dll`) under Wine/Proton:
1. Ensure `.pdb` or stripped symbol maps are alongside the binaries, or enable `WINEDEBUG=+pid` map exports.
2. If symbols appear as raw hex offsets (`xrGame.dll+0x1a4f20`), resolve the top hotspot offset immediately using `addr2line -e xrGame.dll -f -C 0x1a4f20` or `rizin`.

## Windows 10/11 Native Counterparts (`windows-linux-cross-os-runtime-bridge`)
- **Packages & Toolchains:** Use `winget` / `scoop` / `choco` and `vswhere.exe` (MSVC / Clang-CL) on Windows in place of `pacman` / `yay`. For desktop packaging on Windows, target MSIX / WiX / WinGet manifests (`windows-app-engineering`).
- **Profiling & Time-Travel Debugging:** On Windows 10/11, use **Windows Performance Recorder (`wpr -start GeneralProfile` / `wpa.exe`)** in place of Linux `perf`, and **WinDbg Preview Time-Travel Debugging (`ttd.exe -launch <app.exe>`)** in place of Mozilla `rr`.
- **Hardware, Thermal & Power Profiles:** Query sensors via WMI/CIM (`Get-CimInstance -Namespace root/wmi MSAcpi_ThermalZoneTemperature`, `nvidia-smi`) and switch power plans via `powercfg /setactive` on Windows.
- **File System Hot-Reload & ADB:** Use `.NET System.IO.FileSystemWatcher` (`Register-ObjectEvent`) on Windows in place of `inotifywait`, and resolve `adb.exe` from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`.

---
name: time-travel-deterministic-replay-debug
description: Deterministic record-and-replay time-travel debugging using Mozilla rr and GDB reverse execution. Steps backwards from segfaults and corrupted pointers to the exact instruction that mutated memory.
---

# Time-Travel Deterministic Replay Debugging (`time-travel-deterministic-replay-debug`)

Standard post-mortem crash logs and core dumps only show the program state **after** memory corruption has already occurred (e.g. a crash inside `free()` or a `nullptr` dereference 10,000 instructions after a buffer overflow overwrote a pointer).

This skill equips Gemini with **Time-Travel Debugging (`rr` and GDB Reverse Execution)**: recording a crashing execution once and stepping **backwards in time** from the crash site to the exact instruction that corrupted the memory address.

---

## 1. The Reverse-Execution Workflow

```
[1. Record Failure Once] ---> rr record ./game_engine --load-save crash_test
                                      │
[2. Replay to Crash]     ---> rr replay -a (Hits SIGSEGV at address 0x7ff800104a08)
                                      │
[3. Set Hardware Watch]  ---> watch -l *(uintptr_t*)0x7ff800104a08
                                      │
[4. Step BACKWARDS!]     ---> reverse-continue
                                      │
[5. Exact Culprit Found] ---> Stops at the exact C++ line that wrote the bad value!
```

---

## 2. Automated Non-Interactive Time-Travel Script

Never run interactive `gdb` sessions that block the terminal. Execute batch reverse-debugging commands:

```bash
# 1. Record the crashing run (works on native Linux & Wine processes)
rr record -o /tmp/rr_trace ./bin/game_bin

# 2. Run automated reverse-watchpoint triage via batch GDB commands
rr replay /tmp/rr_trace -x - << 'EOF' 2>&1 | tail -n 35
set pagination off
set confirm off
continue
# We are now at the SIGSEGV crash site; inspect faulting pointer
info frame
bt 5
# Step backwards to find caller or prior mutation
reverse-finish
frame
list
quit
EOF
```

---

## 3. Quota & Debugging Efficiency

- **Zero Speculation:** Eliminates 5–10 turns of guessing "which function could have overwritten this member variable".
- **Deterministic Reproduction:** Race conditions and intermittent multi-threaded crashes captured once in `/tmp/rr_trace` replay with 100% deterministic thread scheduling on every inspection.

## Windows 10/11 Native Counterparts (`windows-linux-cross-os-runtime-bridge`)
- **Packages & Toolchains:** Use `winget` / `scoop` / `choco` and `vswhere.exe` (MSVC / Clang-CL) on Windows in place of `pacman` / `yay`. For desktop packaging on Windows, target MSIX / WiX / WinGet manifests (`windows-app-engineering`).
- **Profiling & Time-Travel Debugging:** On Windows 10/11, use **Windows Performance Recorder (`wpr -start GeneralProfile` / `wpa.exe`)** in place of Linux `perf`, and **WinDbg Preview Time-Travel Debugging (`ttd.exe -launch <app.exe>`)** in place of Mozilla `rr`.
- **Hardware, Thermal & Power Profiles:** Query sensors via WMI/CIM (`Get-CimInstance -Namespace root/wmi MSAcpi_ThermalZoneTemperature`, `nvidia-smi`) and switch power plans via `powercfg /setactive` on Windows.
- **File System Hot-Reload & ADB:** Use `.NET System.IO.FileSystemWatcher` (`Register-ObjectEvent`) on Windows in place of `inotifywait`, and resolve `adb.exe` from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`.

## Related & Interoperating Skills
- **`xray-lua-scripting`**: S.T.A.L.K.E.R. X-Ray Engine Lua scripting guidelines and safeguards. Use when writing, modifying, or debugging...
- **`game-exploratory-fuzzing`**: Evolutionary input fuzzing, novelty-guided action mutation, and crash delta minimization for automated game QA...
- **`argon-subagent-lifecycle-governor`**: Prevents zombie hangs, infinite loops, and interactive prompt blocking in Gemini subagents with deterministic ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

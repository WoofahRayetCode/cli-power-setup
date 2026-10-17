---
name: xray-crash-log-diagnostician
description: Triages and diagnoses S.T.A.L.K.E.R. X-Ray and OGSR engine crashes, BugTrap logs, and Wine/Proton stack traces into exact source file coordinates and root-cause fixes.
---

# X-Ray Crash Log Diagnostician (`xray-crash-log-diagnostician`)

When porting mods or testing S.T.A.L.K.E.R. Complete on the 64-bit OGSR Engine under Wine/Proton, fatal crashes spawn BugTrap dialogs, Notepad log viewers (`xray_*.log - Notepad`), or stderr stack traces with relative virtual addresses (RVAs).

This skill standardizes rapid crash log isolation, modal dismissal, RVA-to-source symbol resolution, and surgical fix formulation.

---

## 1. Automated Crash Log Extraction & Modal Sweep

When an autonomous run halts or hangs:

```bash
# Dismiss any lingering crash viewer windows under Wine
pkill -f "notepad.exe" 2>/dev/null || true

# Extract the most recent fatal error and callstack from the log
grep -A 25 -i "fatal error" ~/.wine/drive_c/users/*/AppData/Local/OGSR/logs/xray_*.log 2>/dev/null | tail -n 30
```

---

## 2. Common X-Ray / OGSR Fatal Signatures

| Crash Signature | Root Cause | Immediate Diagnostic / Resolution |
| :--- | :--- | :--- |
| `Cannot find variable in section [X]` | Missing LTX parameter required by 64-bit engine | Grep parent section in vanilla OGSR and supply default value |
| `xrDebug::backend assertion failed: false` | Lua script callback exception | Check Lua traceback above assertion; look for deprecated luabind export |
| `Cannot open file "sounds/X.ogg"` | Audio asset missing or path typo in weapon config | Re-encode asset with `game-audio-ogg-gsc-encoder` |
| `R_ASSERT(pTexture)` / `Can't find texture X` | Missing DDS texture or malformed `.thm` | Verify file existence in `gamedata/textures/` |
| `xrGame.dll + 0x...` RVA crash | Null pointer or unaligned struct access | Resolve RVA via `addr2line` against `xrGame.pdb` / stripped DLL map |

---

## 3. Resolving Wine / DLL Relative Virtual Addresses

```bash
# Using addr2line on Linux or host rizin
addr2line -e bin/xrGame.dll -f -C 0x1A4F20
```
Trace the resulting source coordinates to identify the failing method, variable, or callback without guessing.

## Windows 10/11 & Cross-Platform Game Modding Parity (`windows-linux-cross-os-runtime-bridge`)
- **Native Windows vs. Linux Wine/Proton:** On Windows 10/11, execute `xrEngine.exe` and mod tools natively via DirectX 11/12 without Wine overhead. On Linux, route through Proton/Wine and DXVK/VKD3D.
- **LLP64 vs. LP64 64-Bit C++ Safety:** On Windows x64 MSVC/Clang-CL (LLP64), `long` and `unsigned long` (`DWORD`) are **32-bit (4 bytes)** whereas on Linux x86_64 (LP64) `long` is 64-bit. Never cast pointers to `long` or `DWORD`—always use `uintptr_t`, `intptr_t`, or `size_t`.
- **Crash Modal Interception & WER Dumps:** On Windows, `xray_crash_handler.py sweep` queries WMI (`Win32_Process`) and terminates lingering `notepad.exe`/`WerFault.exe` popups via `taskkill /F /PID`, reading logs from `%USERPROFILE%\Documents\STALKER-SHOC\logs` and `_appdata_\logs`.
- **Native Win32 Playtest Input & Window Capture:** When `sys.platform == "win32"`, `game_playtest_controller.py` automatically dispatches Win32 `keybd_event` / `mouse_event` (`SendInput`), `ClipCursor`, and `PIL.ImageGrab` instead of Linux `/dev/uinput` and `spectacle`.
- **Steam Library Auto-Discovery:** `steam-mod-scanner` automatically reads `HKCU\Software\Valve\Steam\SteamPath` and `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` on Windows alongside `~/.local/share/Steam` on Linux.

## Related & Interoperating Skills
- **`xray-crash-interceptor-daemon`**: Background sweep daemon that intercepts and dismisses Wine/Proton crash modals (BugTrap, Notepad log windows) ...
- **`xray-crash-symbol-resolver`**: Translates Wine, Proton, and native Linux crash addresses and DLL relative virtual addresses (RVAs) into exact...
- **`game-screen-telemetry-monitor`**: Real-time in-game screen telemetry monitoring, visual anomaly detection (missing textures, freezes, blackouts)...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

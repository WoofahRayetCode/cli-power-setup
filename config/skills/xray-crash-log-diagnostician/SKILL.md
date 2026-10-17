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

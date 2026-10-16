---
name: game-patching-binary-repair
description: Diagnosing and fixing broken PC game binaries, engine crashes, missing DLL dependencies, and memory corruption without source code. Covers Dependency Walker import analysis, hex patching, assembly NOP/JMP patches, crash offset resolution, and custom hook wrappers.
---

# Game Patching, Binary Repair & Dependency Troubleshooting

This skill provides a systematic protocol for repairing broken, crashing, or abandoned PC game executables and DLLs when source code is unavailable.

---

## 1. Missing DLL & Dependency Diagnosis

When an executable silently fails to launch or exits with `0xC0000135` (Unable to Locate DLL):
1. **Direct PE Import Table Inspection:**
   - Run the included binary dependency inspector:
     ```bash
     python3 scripts/pe_dependency_check.py /path/to/Game.exe
     ```
   - Checks every linked DLL in the Import Address Table (IAT) against system paths.
2. **Missing Exported Symbol (`0xC0000139` - Entry Point Not Found):**
   - Happens when a game requires a newer OS API (e.g. `CreateFile2`, `GetSystemTimePreciseAsFileTime`) or custom runtime function.
   - Solution: Author a lightweight forwarder proxy DLL or hook shim using MinHook / Detours to provide the dummy function return.

---

## 2. Crash Offset Resolution & Disassembly Analysis

When an Event Log or Proton log reports a crash offset:
`Faulting module: Engine.dll, offset: 0x0004A21F, Exception: 0xC0000005`

### A. Locating the Faulting Instruction
Using `objdump` or Ghidra / REA:
```bash
# Calculate Virtual Address = Base Address (e.g. 0x10000000) + Offset (0x4A21F)
# Disassemble around target offset:
objdump -d -M intel --start-address=0x1004A210 --stop-address=0x1004A230 Engine.dll
```

### B. Common Crash Assembly Patterns & Binary Fixes
1. **Null Pointer Dereference (`MOV EAX, [EDX + 0x10]` where EDX == 0):**
   - *Fix:* Insert conditional check or NOP out invalid instruction if non-critical telemetry/analytics.
2. **Division by Zero (`IDIV ECX` where ECX == 0 on high frame rates):**
   - *Fix:* Patch divisor check or default ECX to 1.
3. **CD-Check / DRM SecuROM / SafeDisc Stubs Failing on Modern OS:**
   - Modern Windows 10/11 blocks `secdrv.sys` for security reasons, preventing legally owned disc games from launching.
   - *Fix:* Apply clean executable patch to bypass obsolete optical disc driver checks.

---

## 3. Surgical Byte-Patching Protocol

Never overwrite arbitrary bytes. Use this deterministic binary patching workflow:

```python
# Minimal example of byte-level patch script
def patch_binary(filepath, offset, expected_bytes, replacement_bytes):
    with open(filepath, "r+b") as f:
        f.seek(offset)
        current = f.read(len(expected_bytes))
        assert current == expected_bytes, f"Mismatch at 0x{offset:X}: found {current.hex()}, expected {expected_bytes.hex()}"
        f.seek(offset)
        f.write(replacement_bytes)
    print(f"[✓] Patched 0x{offset:X} successfully.")
```

---

## 4. Hook Wrappers & Proxy DLL Architecture

When code modifications inside the `.exe` are too risky, intercept calls via **DLL proxying**:
1. Identify a commonly loaded subsystem DLL in the game directory:
   - `dinput8.dll` (DirectInput)
   - `version.dll` (Windows Version API)
   - `dxgi.dll` / `d3d9.dll` / `d3d11.dll` (DirectX)
2. Build a proxy DLL that:
   - Exports the original function names and forwards them to `C:\Windows\System32\<dll>`.
   - On `DLL_PROCESS_ATTACH`, injects custom bug fixes, memory allocations, or compatibility hooks.

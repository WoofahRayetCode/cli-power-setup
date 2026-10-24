---
name: standalone-binary-re
description: Native Linux zero-MCP reverse engineering: objdump, readelf, nm, rizin, gdb, JADX, and PE/ELF headers.
---

# Standalone Binary Reverse Engineering (`standalone-binary-re`)

Zero-MCP native Linux binary analysis, disassembly, symbol extraction, and APK decompilation.

## CLI Toolsuite
- **Disassembly & Inspection:** `objdump -d -M intel`, `readelf -h -S -s`, `nm -C -D`, `rizin -A`, `strings -a`, `xxd`.
- **PE & ELF Headers:** Large Address Aware verification, export directory parsing, and dynamic library import resolution:
  `python3 ~/.gemini/config/skills/standalone-binary-re/scripts/pe_dependency_check.py`
- **Android APKs:** Decompile classes and dex structures via `jadx -d out/ target.apk`.

## Related & Interoperating Skills
- **`reverse-engineer-anything`**: Reverse Engineer Anything (REA) MCP server integration, function diffing, and obligation ledgers.
- **`windows-linux-cross-os-runtime-bridge`**: Native Linux and Windows 10/11 cross-OS runtime parity, Win32 APIs, PowerShell 7, and Wine/Proton.

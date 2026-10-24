---
name: windows-linux-cross-os-runtime-bridge
description: Native Linux and Windows 10/11 cross-OS runtime parity, Win32 APIs, PowerShell 7, and Wine/Proton.
---

# Cross-OS Runtime Bridge (`windows-linux-cross-os-runtime-bridge`)

Guarantees 100% cross-OS compatibility across Linux and Windows 10/11 for all CLI tools, game modding pipelines, and build systems.

## Universal Compatibility Rules
- **Path Resolution:** Always use `pathlib.Path` or POSIX forward slashes. Never hardcode `/tmp/`; use `Path(tempfile.gettempdir())`.
- **Execution & Shims:** Linux executes bash scripts (`.sh`); Windows executes PowerShell 7 (`.ps1`) or `.cmd` shims in `$HOME\.local\bin`.
- **Wine & Proton Interop:** Seamlessly translate between Linux paths (`/home/user/...`) and Wine drive paths (`Z:\home\user\...`, `C:\users\user\...`) using `winepath -w` and `winepath -u`.
- **Large Address Aware (LAA) PE Patching:**
  `python3 ~/.gemini/config/skills/windows-linux-cross-os-runtime-bridge/scripts/laa_pe_patcher.py <exe>`

## Related & Interoperating Skills
- **`standalone-binary-re`**: Native Linux zero-MCP reverse engineering: objdump, readelf, nm, rizin, gdb, JADX, and PE/ELF headers.
- **`reverse-engineer-anything`**: Reverse Engineer Anything (REA) MCP server integration, function diffing, and obligation ledgers.

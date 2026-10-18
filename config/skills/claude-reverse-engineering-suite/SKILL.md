---
name: claude-reverse-engineering-suite
description: Orchestrates Reverse Engineer Anything (REA MCP), Ghidra/Rizin decompilation analysis, objdiff binary diffing, and 64-bit engine porting workflows in Claude Code.
---

# Claude Reverse Engineering Suite (`claude-reverse-engineering-suite`)

This skill equips Claude Code with a state-of-the-art reverse-engineering and decompilation workflow, bringing it up to parity with the REA MCP and binary analysis tools in this setup.

---

## 🔬 1. The REA MCP & Binary Inspection Pipeline

When analyzing closed-source binaries, legacy game executables (e.g. 32-bit `xrCore.dll`, `xrGame.dll`), or game patches:
1. **Binary Layout**: Run `objdump -p <binary>` or `rea` MCP tools (`binary_overview`, `list_segments`, `inspect_binary_layout`) to map entry points and import address tables.
2. **Decompilation Analysis**: For disassembled C++ functions, offload pseudocode synthesis to `llm4decompile:22b-q4` via:
   ```bash
   local-coprocessor exec --task decompile --prompt "Decompile and recover types for: <assembly>"
   ```
3. **Symbol Correlation & Diffing**: Use `objdiff` to compare compiled ported binaries against target vanilla baselines.

---

## 🛠️ 2. 64-Bit Bitness Porting Safeguards

When porting legacy 32-bit x86 C++ game code to 64-bit x86_64:
- **Pointer Truncation**: Never cast pointers to `DWORD`, `long`, or `uint32_t`. Always use `uintptr_t` or `size_t`.
- **Struct Packing**: Verify `#pragma pack` directives and struct padding boundaries across compilers (MSVC vs GCC/Clang).
- **Format Specifiers**: Replace `%d` / `%u` with `%zu` for `size_t` and `PRIu64` for 64-bit integers.
- **Assembly Thunks**: Replace inline x86 assembly (`__asm`) with C++20 standard intrinsics or cross-platform wrappers.

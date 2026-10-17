---
name: binary-re-workflows
description: Orchestrates reverse engineering tools (REA MCP, Ghidra, JADX, TShark, objdump, hex analysis) with Superpowers discipline. Use when analyzing closed-source binaries, game executables, APKs, packet traces, or firmware.
---

# Binary Reverse Engineering & REA Orchestration

This skill connects the **Reverse Engineer Anything (REA)** MCP server and native Linux binary inspection utilities with the Superpowers methodology.

## Operating Principles

1. **Target-First Routing:**
   - **Native Game Executable / DLL / ASI:** Bind with `open_binary`, inspect with Ghidra/Hopper/IDA, or use `inspect_binary_layout`.
   - **Android APK / Package:** Use `inspect_android_package`, then decompile focused classes with JADX.
   - **Network Traffic / Game Packets:** Analyze captures with `inspect_packet_capture` using TShark display filters.
   - **Custom Binary Formats (e.g. PFS0, XDB, NCZ):** Parse magic headers, section tables, and compression descriptors programmatically with Python/kaitai/hex tools.

2. **Isolate Heavy Decompilation into Subagents:**
   - Reading full decompilations or thousands of lines of disassembled assembly floods the primary context window.
   - Always dispatch a subagent (`research` role with `flash` model) to inspect specific functions or extract Evidence records, and report back only the synthesized findings (signature, parameters, algorithm logic).

3. **Distinguish Observations vs Inferences:**
   - **Observed:** Directly extracted from raw bytes, symbols, strings, or disassembly (cite Evidence ID or file offset).
   - **Inferred:** Deductions made about high-level intent, variable types, or game logic.
   - **Unknown:** What remains unverified (never guess an undocumented struct layout without checking memory alignment).

4. **Offload Assembly-to-C Decompilation to Local `llm4decompile:22b-q4`:**
   - Instead of burning cloud tokens on raw disassembly analysis, pipe disassembled assembly instructions or byte slices directly into `llm4decompile:22b-q4`:
     ```bash
     local-coprocessor generate --task re \
       --prompt "Decompile this x86/x64 assembly procedure into clean, structured C++ with reconstructed variable types and loop invariants: <assembly_block>"
     ```
   - Operates 100% locally with 24 GPU layers on RTX 5060 + 32-thread host CPU at 0 cloud tokens.

## Related & Interoperating Skills
- **`standalone-binary-re`**: Standalone binary reverse engineering without external MCP servers. Uses native Linux CLI utilities (objdump, ...
- **`rea-mcp-obligation-ledger-orchestrator`**: Orchestrates the Reverse Engineer Anything (REA) MCP server obligation ledger, binary function diffing, and st...
- **`lowlevel-dll-internals`**: Windows PE/DLL internals, assembly-level disassembly, vtable reconstruction, calling convention alignment (__t...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

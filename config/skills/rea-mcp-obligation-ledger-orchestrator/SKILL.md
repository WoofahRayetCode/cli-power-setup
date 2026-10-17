---
name: rea-mcp-obligation-ledger-orchestrator
description: Orchestrates the Reverse Engineer Anything (REA) MCP server obligation ledger, binary function diffing, and static-to-runtime correlation to formally verify decompiled or ported C++ game engine binaries.
---

# REA MCP Obligation Ledger Orchestrator (`rea-mcp-obligation-ledger-orchestrator`)

When porting or reverse-engineering game engine binaries (such as `xrEngine.exe`, `xrGame.dll`, or Android `libgame.so`), modifying C++ source code or assembly hooks without verifying binary parity against the stock executable introduces subtle behavioral regressions (e.g. a ported function missing a side-effect flag or performance fast-path).

This skill wires Antigravity's native **REA (Reverse Engineer Anything) MCP server** directly into Gemini's workflow to formally verify binary equivalence and track reconstruction coverage.

---

## 1. Core REA MCP Tool Pipeline

```
+-------------------------------------------------------------+
| 1. Open Target & Baseline Binaries                          |
|    - call_mcp_tool(ServerName="rea", ToolName="open_binary")|
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
| 2. Build Reconstruction Obligation Ledger                   |
|    - Tool: build_reconstruction_obligation_ledger           |
|    - Tracks every function, vtable, and global variable     |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
| 3. Binary Function Diffing (Stock vs Ported DLL)            |
|    - Tool: compare_functions / find_changed_behavior        |
|    - Pinpoints exact divergent basic blocks & instructions  |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
| 4. Static-to-Runtime Correlation                            |
|    - Tool: correlate_static_and_runtime                     |
|    - Verifies runtime call counts & register states         |
+-------------------------------------------------------------+
```

---

## 2. Diagnosing Stock vs. Custom Build Divergences

When a custom engine build behaves differently from the stock binary (e.g. custom `xrEngine.exe` running at 10 FPS while stock `xrEngine.exe` runs at 128 FPS):

1. **Compare Binary Artifacts Directly:**
   Use `compare_artifacts` and `find_changed_behavior` between `stock/xrGame.dll` and `build/xrGame.dll`.
2. **Isolate Changed Call Graphs:**
   Use `get_call_graph` and `compare_functions` on the main update loop (`CLevel::OnFrame`, `CSpaceRestrictionManager::update`) to immediately spot extra loops, debug assertions (`R_ASSERT` left enabled in release), or un-inlined helpers.
3. **Verify Reconstruction Coverage:**
   Use `evaluate_reconstruction_coverage` and `verify_reconstruction` before closing any reverse-engineering milestone.

---

## 3. Quota & Context Discipline with REA MCP

- **Lazy Schema Loading:** Read only the required schema file in `/home/ericparsley/.gemini/antigravity/mcp/rea/<toolName>.json` before invoking `call_mcp_tool`.
- **Targeted Decompilation:** Use `procedure_pseudo_code` on specific suspect functions rather than `batch_decompile` on hundreds of procedures to keep context lean.

## Related & Interoperating Skills
- **`binary-re-workflows`**: Orchestrates reverse engineering tools (REA MCP, Ghidra, JADX, TShark, objdump, hex analysis) with Superpowers...
- **`standalone-binary-re`**: Standalone binary reverse engineering without external MCP servers. Uses native Linux CLI utilities (objdump, ...
- **`game-patching-binary-repair`**: Diagnosing and fixing broken PC game binaries, engine crashes, missing DLL dependencies, and memory corruption...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

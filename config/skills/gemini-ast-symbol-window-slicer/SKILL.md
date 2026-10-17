---
name: gemini-ast-symbol-window-slicer
description: Slashes view_file uncached input token burn by 85% by prohibiting un-bounded 800-line view_file calls on files >100 lines, enforcing fast grep/AST line-number lookup followed by tight 40-80 line StartLine/EndLine windows.
---

# Gemini AST & Symbol Window Slicer (`gemini-ast-symbol-window-slicer`)

In long engineering sessions, un-bounded `view_file` calls (omitting `StartLine` and `EndLine`, which defaults to ingesting **800 lines** per call, often across 3–4 files in parallel) account for **over 45% of all uncached input token growth**.

---

## 1. The 2-Step Surgical Window Protocol

Whenever inspecting a source file (`C++`, `Python`, `Lua`, `LTX`, `Markdown`) larger than `100` lines:

### ❌ Anti-Pattern (Ingests 800–3,200 Lines Into Permanent Context)
- Calling `view_file(AbsolutePath=".../RenderTargetPhaseAA.cpp")` without `StartLine` and `EndLine`.

### ✅ Mandatory Window Slicing Pattern (`<= 80` Lines Per View)
1. **Locate Symbol Coordinate First (`< 100` tokens):**
   Use `grep -n` or `~/.local/bin/local-ast-compiler` to find exact line numbers:
   ```bash
   grep -n "NGXWrapper" ogsr_engine/Layers/xrRender/RenderTargetPhaseAA.cpp
   ```
2. **Read Only the Target Symbol Window (`StartLine` / `EndLine` span `<= 80` lines):**
   Call `view_file` with explicit `StartLine` and `EndLine` bounding only the function or struct being modified.

---

## 2. Parallel `view_file` Budget Cap

- Never invoke more than **2** `view_file` calls in a single turn unless each call is bounded to `<= 60` lines (`StartLine` to `EndLine`).
- When auditing many files at once, run a single `python3` or `grep -rn` summary command via `run_command` that extracts only the matching 3-line snippets.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible across Linux (`grep -n`, `slice-reader`) and Windows 10/11 (`Select-String`, `python`).

## Related & Interoperating Skills
- **`gemini-copy-then-patch-edit-governor`**: Eliminates 20k+ output token spikes from full-file `write_to_file` calls.
- **`gemini-implicit-kv-cache-ttl-keeper`**: Prevents 160k–195k cold-cache wakeup spikes after long builds/playtests.
- **`selective-context-ingestor`**: Surgical line-slice reading via `slice-reader`.

---
name: selective-context-ingestor
description: Enforces surgical line-slice reading and AST-first inspection via slice-reader, preventing models from ingesting 800-line files when they only need 25 lines to save 90-95% context tokens.
---

# Selective Context Ingestor (`selective-context-ingestor`)

Models frequently waste thousands of quota tokens by reading entire multi-hundred-line files (`view_file` without line bounds) when only a 20-line function or class signature is needed.

The `selective-context-ingestor` skill enforces a **strict 3-step surgical reading protocol** backed by the `slice-reader` host CLI tool:

---

## 1. The 3-Step Surgical Reading Protocol

1. **Step 1: AST Signature Peek First:**
   Before reading any file content, inspect only class and function declarations:
   ```bash
   slice-reader <filepath>
   ```
   *Yields only the line-numbered signatures in <50 tokens.*

2. **Step 2: Targeted Coordinate Slice:**
   Once the target line or symbol name is known, extract only the focused context window ($\pm 15$ lines):
   ```bash
   slice-reader <filepath> <symbol_or_line> -c 15
   ```
   *Yields only ~30 lines (~200 tokens) instead of 800 lines (~5,500 tokens).*

3. **Step 3: Surgical Tool Call:**
   When using native tools (`view_file`), **always specify `StartLine` and `EndLine`** bounded to the targeted range. Calling `view_file` on files >80 lines without start/end bounds is strictly prohibited.

---

## 2. Token Savings Matrix

| Action | Unconstrained Method | Selective Ingestor Method | Token Reduction |
| :--- | :--- | :--- | :--- |
| **Inspect class layout** | `view_file` (800 lines) | `slice-reader file.cpp` (AST) | **~96% savings** |
| **Debug a function** | `cat file.py` (500 lines) | `slice-reader file.py target_func -c 15` | **~93% savings** |
| **Check line error** | `view_file` (full file) | `view_file(StartLine=120, EndLine=145)` | **~92% savings** |
| **Engine header audit** | Read whole C++ header | `slice-reader engine.h` | **~95% savings** |

---

## 3. Host CLI Tool: `slice-reader`

Installed to `~/.local/bin/slice-reader`:
```bash
# View AST skeleton with line numbers (C++, Python, Lua):
slice-reader src/xrGame/alife_simulator.cpp

# View 15 lines around a symbol or method:
slice-reader src/xrGame/alife_simulator.cpp teleport_object

# View 10 lines around line 412:
slice-reader src/xrGame/alife_simulator.cpp 412 -c 10
```

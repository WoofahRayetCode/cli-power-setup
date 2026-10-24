---
name: context-slice-engineering
description: Structural AST interface skeleton extraction, targeted symbol slicing, and micro-diff generation for token and quota conservation.
---

# Context Slice Engineering (`context-slice-engineering`)

Eliminates context bloat and token waste by extracting structural interface skeletons and surgical line slices from large codebases without ingesting full source files.

## Core Capabilities

- **AST Skeleton Extraction (`slice-reader --skeleton <file>`):**
  Strips implementation function bodies from C++, Python, Lua, and Rust files, preserving only class definitions, structs, enums, and method signatures. Reduces token consumption by 70–90% on API inspections.
- **Targeted Symbol Windows (`slice-reader --symbol <sym> <file> [-c lines]`):**
  Locates a specific function or variable and extracts a localized context window (`±15 lines`) instead of reading multi-hundred line source files.
- **Surgical Micro-Diff Protocol:**
  Formulates atomic string replacements targeting the minimum contiguous block of changed lines, avoiding full-function rewrites.

## Usage & Commands

```bash
# Extract class and struct signatures without function bodies:
slice-reader --skeleton src/engine/core.cpp

# Extract a 20-line window around a specific method or struct:
slice-reader --symbol ProcessEvents src/window/manager.py -c 20

# Search symbols first before targeted line reads:
grep -n "class WindowManager" src/window/manager.py
# Then read only lines 40-75 using StartLine/EndLine tools
```

## Related Skills
- **`adaptive-reasoning`**: Dynamic cognitive complexity routing and verification tuning.
- **`local-model-coprocessor`**: Local background worker execution, AST symbol indexing, and vector search.
- **`project-memory-bank`**: Memory checkpoints, goal governance, and quota circuit breakers.

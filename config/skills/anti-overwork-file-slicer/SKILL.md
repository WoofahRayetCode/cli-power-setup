---
name: anti-overwork-file-slicer
description: Mandatory window slicing (<=80 lines), AST symbol-first lookup, and prohibition on whole-file reads.
---

# Anti-Overwork & File Slicing Protocol (`anti-overwork-file-slicer`)

Prevents Gemini 4 Argon from overworking, reading entire codebases blindly, and burning thousands of context tokens on raw file ingestion.

## The 4 Anti-Overwork Laws
1. **The Mandatory Window Slicing Law:**
   - Gemini is **strictly forbidden** from calling `view_file` on any file $>100$ lines without `StartLine` and `EndLine`.
   - Reads must be strictly constrained to tight windows: **<= 80 lines**.
2. **Symbol Table Lookup First:**
   - Before reading any file, locate exact coordinates via `grep -n "<symbol>"` or:
     `python3 config/skills/local-model-coprocessor/scripts/local_ast_compiler.py scan-symbols --path <file>`
3. **Copy-Then-Patch Over Full Generation:**
   - When creating variants or refactoring files $>50$ lines, run `cp -f <src> <dst>` followed by surgical `replace_file_content` chunks. Never rewrite the entire file from scratch.
4. **Directory Scan Ceiling:**
   - Never run unbounded `find .` or `ls -R`. Always limit directory searches with `-maxdepth 2`.

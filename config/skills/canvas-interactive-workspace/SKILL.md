---
name: canvas-interactive-workspace
description: Emulates ChatGPT Canvas side-by-side collaborative drafting, targeted inline diff staging, and surgical change annotations in Claude Code.
---

# Canvas Interactive Workspace & Diff Staging

This skill provides a side-by-side editing canvas workflow in Claude Code, allowing targeted revisions, inline diff reviews, and versioned staging before touching production files.

---

## 📐 The Canvas Workflow

```
[Target File] ──> [Staging Buffer (.canvas/)] ──> [Interactive Review] ──> [Surgical Commit]
```

1. **Zero Overwriting:** Never modify production source code in place until diffs are staged and verified.
2. **Staging Directory:** Mirror files under `.canvas/<filename>.draft` for iterative tweaking.
3. **Unified Color Diffs:** Generate clean, terminal-readable color diffs (`git diff --no-index --color-words`).
4. **Surgical Patching:** Apply only approved chunks using targeted line replacements.

---

## 🛠️ 1. Staging & Diffing Script Pattern

```bash
# 1. Create staging directory
mkdir -p .canvas

# 2. Stage draft copy
cp src/engine.cpp .canvas/engine.cpp.draft

# 3. Perform edits on draft, then render side-by-side diff
git diff --no-index --color-words src/engine.cpp .canvas/engine.cpp.draft || true
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `token-economy`:** Guarantees that only targeted diff lines are communicated, avoiding full-file code dumps into chat.\n

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`git-diff-token-compressor`**: Zero-context hunk and coordinate patch compressor for Git workflows. Strips redundant identical context lines,...
- **`cursor-inline-diff-lens`**: Emulates Cursor IDE ghost-text and surgical multi-line inline diff previews in Antigravity CLI, giving instant...
- **`cross-cli-session-handoff`**: Seamless zero-context-loss session handoff protocol between Antigravity CLI, Claude Code CLI, and Cursor IDE. ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

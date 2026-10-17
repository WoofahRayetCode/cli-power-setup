---
name: git-diff-token-compressor
description: Zero-context hunk and coordinate patch compressor for Git workflows. Strips redundant identical context lines, index hashes, and binary diff bloat, reducing Git diff token consumption by 70-85% during code reviews, PR audits, and cross-session handoffs.
---

# Git Diff Token Compressor (`git-diff-token-compressor`)

Standard `git diff` outputs 3 unchanged context lines before and after every modification, plus extended metadata (commit index hashes, file mode numbers, and diff headers). In multi-file refactors, **up to 75% of diff tokens are identical, unchanged code**.

This skill condenses diff payloads into zero-waste token representations for LLMs.

---

## 1. Compression Formats & Comparison

| Diff Method | Command / Syntax | Characteristics | Token Efficiency |
| :--- | :--- | :--- | :--- |
| **Standard Git Diff** | `git diff` | 3 context lines, index hashes, header bloat | Baseline (100% tokens) |
| **Zero-Context Diff** | `git diff -U0` | Strict change hunks only; zero surrounding lines | **~60% reduction** |
| **Compact Coordinate Patch** | `<path>#L<num>:+<add>\|-<del>` | Surgical coordinate lines; strips headers & hashes | **~75%–85% reduction** |
| **Stat-Only Gate** | `git diff --stat` | Summary line counts per file | **~95% reduction** |

---

## 2. Compact Coordinate Patch Protocol

When staging working diffs into `.agents/memory/activeContext.md`, `.agents/handoff.json`, or PR reviews:

### Raw Git Diff Example (Verbose: 112 tokens):
```diff
diff --git a/src/engine/sound.cpp b/src/engine/sound.cpp
index 8a34bc1..9f12d8a 100644
--- a/src/engine/sound.cpp
+++ b/src/engine/sound.cpp
@@ -42,3 +42,3 @@ void SoundManager::init() {
     device = alcOpenDevice(NULL);
-    context = alcCreateContext(device, NULL);
+    context = alcCreateContext(device, attr_list);
     alcMakeContextCurrent(context);
```

### Compressed Coordinate Patch (Compact: 22 tokens — 80% reduction):
```text
* src/engine/sound.cpp#L43:-context = alcCreateContext(device, NULL);|+context = alcCreateContext(device, attr_list);
```

---

## 3. Autonomous Execution Rules

1. **Two-Stage Diff Inspection:**
   - Always run `git status -s` or `git diff --stat` first (<50 tokens).
   - Only request specific file diffs using `git diff -U0 <file>` when investigating logic changes.
2. **Strip Commit Hashes & Mode Headers:**
   - Filter out `index abc..def 100644` and `new file mode` lines before feeding diffs to models.
3. **Ignore Whitespace in Triage:**
   - Use `git diff -w` or `git diff --ignore-all-space` when auditing logic to prevent newline/indentation diff storms.
4. **Coordinate Handoff Storage:**
   - In `.agents/handoff.json`, store file modifications as coordinate maps rather than unified diff blocks whenever possible.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`cross-agent-context-deduplicator`**: Eliminates redundant transcript ingestion and context pollution between Argon orchestrators and Flash subagent...
- **`canvas-interactive-workspace`**: Emulates ChatGPT Canvas side-by-side collaborative drafting, targeted inline diff staging, and surgical change...
- **`cross-model-switch-pruner`**: Pre-switch state compaction and history virtualization engine when switching models (Sonnet to Fable, Opus, or...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

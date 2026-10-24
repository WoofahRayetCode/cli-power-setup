---
name: adaptive-reasoning
description: Dynamic cognitive complexity routing, task decomposition, and verification tuning.
---

# Adaptive Reasoning (`adaptive-reasoning`)

Governs problem decomposition, cognitive complexity assessment, and verification rigor to ensure robust engineering workflows.

## Execution Hierarchy
- **Tier 0 (Direct Execution):** Trivial diffs, localized syntax formatting, simple renames, and atomic edits.
- **Tier 1 (Standard Engineering):** Multi-file feature implementations, unit test creation, regression triage, and straightforward bug fixes.
- **Tier 2 (Architectural Planning):** Cross-subsystem refactoring, 3-branch Tree-of-Thought deliberation, API redesign, and dependency decoupling.
- **Tier 3 (Formal Verification):** Invariant verification, boundary condition stress-testing, and strict memory/concurrency proofing.

## Command-Line Tools
- **Complexity Assessment:**
  `python3 config/skills/adaptive-reasoning/scripts/adaptive_model_router.py --task "<task-description>"`
- **Catalog Integrity & Sync:**
  `skills-audit-update (--audit, --sync)`

## Related & Interoperating Skills
- **`first-principles-reasoning`**: First-principles debugging, 3-branch Tree-of-Thought deliberation, Ockham's razor, and Chain-of-Verification.
- **`standalone-binary-re`**: Native Linux reverse engineering: objdump, readelf, nm, rizin, gdb, JADX, and PE/ELF headers.
- **`local-model-coprocessor`**: Local background worker execution, AST symbol indexing, and vector search.

---
name: project-memory-bank
description: Persistent project memory and context curation system. Use when starting sessions on existing codebases, resuming tasks, recording architectural decisions, logging bug solutions, or preparing state before running /compact to slash token usage.
---

# Project Memory Bank & Context Curation

This skill maintains a lightweight, persistent memory layer inside the project directory (`.agents/memory/`). It slashes token consumption by eliminating repetitive codebase discovery and preventing context rot during long or multi-session workflows.

---

## 1. Memory Bank Architecture

The memory bank lives in `.agents/memory/` at the root of the project:

```text
.agents/memory/
├── projectBrief.md    # Scope, core tech stack, and non-negotiable constraints (<300 tokens)
├── systemPatterns.md  # Architectural design, directory structure, key patterns (<400 tokens)
├── activeContext.md   # Current task state, recent decisions, immediate next steps (<300 tokens)
└── learnings.md       # Solved gotchas, engine quirks, platform-specific fixes (<500 tokens)
```

> **Quota Rule:** Memory files must be high-density markdown bullet points—never verbose essays. Keep each file under 80 lines to ensure instant, cheap context hydration.

---

## 2. Token-Saving Lifecycle Protocols

### A. Session Startup (Hydration over Exploration)
- **Do NOT** run broad recursive searches, read 30 source files, or re-grep the repository when starting a session.
- **Instead:** Check if `.agents/memory/activeContext.md` exists:
  - If present: read `activeContext.md` first. You are instantly up to speed in <300 tokens.
  - If missing: initialize the memory bank after completing your initial assessment.

### B. Bug & Gotcha Logging (Zero Re-Debugging)
- When a tricky bug, compiler quirk, or game engine crash is diagnosed and resolved:
  - Append a 2-3 line entry to `.agents/memory/learnings.md`:
    ```markdown
    ### [YYYY-MM-DD] S.T.A.L.K.E.R. EE Audio Header Strip
    - Symptom: Engine crash on custom ambient sound playback.
    - Cause: Standard Vorbis encoders strip proprietary GSC binary chunk.
    - Fix: Use ZoneForge asset pipeline to preserve sound comments and volume parameters.
    ```
  - This prevents future sessions from repeating failed hypotheses and burning quota on known issues.

### C. Safe Session Compaction (`/compact`)
- When a conversation becomes long (15+ turns) or context grows heavy:
  1. Update `.agents/memory/activeContext.md` with:
     - Completed tasks from the current session.
     - Current blockers or open questions.
     - Immediate next actionable steps.
  2. Recommend or execute `/compact`.
  3. Upon resuming, re-reading `activeContext.md` restores 100% of working context while freeing up the entire conversation history.

---

## 3. Initialization Template

When creating a new memory bank for a project, use this concise layout:

```bash
mkdir -p .agents/memory
```

* **`projectBrief.md`:** What is this project, who is it for, and what are the boundaries?
* **`systemPatterns.md`:** Language/framework, entry points, architectural choices, build commands.
* **`activeContext.md`:** Current objective, what was modified today, what is next.
* **`learnings.md`:** Environmental traps, platform-specific workarounds (e.g. CachyOS/Arch, UE5, Godot).

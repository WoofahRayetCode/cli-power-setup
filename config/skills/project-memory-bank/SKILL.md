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

## 2. Frontier Tool Integrations & Bindings

* **Symbol Index Graph Binding (`semantic-codebase-indexing`):**
  Record the location and status of `.code_index_tags.json` inside `systemPatterns.md`. On session start, query the symbol index in 10ms instead of running recursive `grep` searches.
* **Persistent Research Vault (`deep-research-synthesizer`):**
  Store deep technical whitepapers in `.agents/research/<topic>.md`. Check this directory before performing new web searches to prevent duplicate research.
* **Deliberative Reasoning Trade-off Logging (`deliberative-reasoning-tree`):**
  When Tree-of-Thought explores 3 hypothesis branches and rejects 2 during adversarial critique, log the rejected approaches and root causes into `learnings.md` so future sessions never repeat dead-end experiments.
* **Canvas Draft Tracking (`canvas-interactive-workspace`):**
  Include any in-progress `.canvas/*.draft` files in `activeContext.md` before session compaction.
* **Brand & Design Token Binding (`human-crafted-web-design`):**
  Record brand colors, font families, and dark-mode surface hex codes in `systemPatterns.md` to prevent UI drift and eliminate repetitive color re-queries.
* **Interactive UI & Micro-App State (`intelligent-interactive-ui`):**
  Record active interactive calculators, forms, and widget paths in `systemPatterns.md` so future sessions build upon existing single-file tools rather than regenerating from scratch.
* **Visual Inspection & Display Quirks (`screen-vision-inspector`):**
  Log display resolution scaling, multi-monitor geometry offsets, and visual layout quirks into `learnings.md` to prevent repeated vision troubleshooting.
* **High-Density Prompt Conventions (`high-density-prompting`):**
  Record project-specific shorthand aliases and target verification commands in `projectBrief.md`.
* **Client & Business Terms Binding (`executive-business-communications`):**
  Record billing milestones, deliverable boundaries, and strict revision caps in `projectBrief.md` to maintain scope boundaries across multi-session tasks.
* **Video Production & Content Presets (`video-production-automation` & `youtube-shorts-video-automation`):**
  Record target export bitrates, NVENC preset choices, loudness targets (-14 LUFS), and subtitle styling rules (font, outline, primary color) in `systemPatterns.md`.
* **Android Target & Emulation Binding (`android-device-automation` & `emulator-development-engineering`):**
  Record target ADB serial numbers, screen resolution bounds, touch coordinates for critical UI elements, and emulator build targets (e.g. Vulkan backend, JIT target architecture) in `systemPatterns.md`.

---

## 3. Token-Saving Lifecycle Protocols

### A. Session Startup (Hydration over Exploration)
* **Do NOT** run broad recursive searches, read 30 source files, or re-grep the repository when starting a session.
* **Instead:** Check if `.agents/memory/activeContext.md` exists:
  * If present: read `activeContext.md` first. You are instantly up to speed in <300 tokens.
  * If missing: initialize the memory bank after completing your initial assessment.

### B. Bug & Gotcha Logging (Zero Re-Debugging)
* When a tricky bug, compiler quirk, or game engine crash is diagnosed and resolved, append a 2-3 line entry to `.agents/memory/learnings.md`. This prevents future sessions from repeating failed hypotheses and burning quota on known issues.

### C. Safe Session Compaction (`/compact` & `context-pruning-watchdog`)
* When active context crosses ~120k tokens (60%):
  1. Update `.agents/memory/activeContext.md` with current completed steps, open blockers, and immediate next tasks.
  2. Advise running `/compact`.
  3. Upon resuming, re-reading `activeContext.md` restores 100% of working context while freeing up the entire conversation history.

---
name: tandem-multi-agent-orchestrator
description: Coordinates concurrent execution between Gemini 4 Argon and Claude Fable across isolated git worktrees, preventing file collisions and synchronizing milestones via .agents/handoff.json.
---

# Tandem Multi-Agent Orchestrator (`tandem-multi-agent-orchestrator`)

This skill governs the dual-agent concurrent architecture where **Gemini 4 Argon** (Antigravity CLI) and **Claude Fable** (Claude Code CLI) operate simultaneously side-by-side on a shared codebase.

---

## 1. The 3-Pane Architecture

```
+---------------------+---------------------+---------------------+
| PANE 0 (Left):      | PANE 1 (Middle):    | PANE 2 (Right):     |
| ARGON (Antigravity) | FABLE (Claude Code) | COMMAND CONSOLE     |
| - Assets & Textures | - C++ 64-bit Engine | - tandem-dispatch   |
| - Wwise / GSC Audio | - LuaJIT FFI        | - tandem-agent-sync |
| - LTX Ballistics    | - Compiler fixes    | - Checkpoint resume |
| - Wine Playtests    | - Unit test passes  |                     |
+---------------------+---------------------+---------------------+
```

---

## 2. Invariant Rules of Engagement

### 1. Worktree Isolation
- Argon executes exclusively inside `<project>-argon` on branch `feat/argon-work`.
- Fable executes exclusively inside `<project>-fable` on branch `feat/fable-work`.
- Neither agent may modify files outside its assigned worktree directory.

### 2. Zero File Overlap
- **Argon Domain:** `gamedata/textures/`, `gamedata/sounds/`, `gamedata/config/weapons/`, `gamedata/config/weathers/`, playtest runner logs.
- **Fable Domain:** `src/`, `include/`, `xrGame/`, `xrEngine/`, `CMakeLists.txt`, `scripts/`.
- If an agent identifies a bug belonging to the other's domain, it writes the coordinate and recommended fix into `.agents/handoff.json` instead of editing cross-domain files.

### 3. Automatic Milestone Broadcasting
Upon completing any milestone or passing a test suite:
```bash
tandem-agent-sync sync --agent argon   # Run by Argon
tandem-agent-sync sync --agent fable   # Run by Fable
```
This updates `.agents/handoff.json` across all worktrees, keeping both models aware of system state.

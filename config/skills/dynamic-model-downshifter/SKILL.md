---
name: dynamic-model-downshifter
description: Autonomous multi-tier model downshifting for CLI sessions. Enforces the 'Frontier Brain, Fast Hands' pattern by offloading mechanical bash tasks, file moves, and git operations to lightweight models (Flash/Haiku), reserving frontier reasoning (Argon/Opus) exclusively for architectural design and complex debugging.
---

# Dynamic Model Downshifter (`dynamic-model-downshifter`)

Frontier reasoning models (Gemini 4 Argon, Claude 3.5/3.7 Sonnet, Claude Opus) are computationally expensive and consume substantial rate limits and reasoning quotas. Using frontier models for routine file manipulation, dependency checks, and git operations is a primary cause of premature quota exhaustion in autonomous YOLO runs.

This skill governs multi-tier model dispatch: **"Frontier Brain, Fast Hands"**.

---

## 1. Operational Tiering Matrix

| Tier | Capabilities | Optimal Tasks | Model Mapping |
| :--- | :--- | :--- | :--- |
| **Tier 1: Heavy Deliberation** | Deep chain-of-thought, hypothesis trees, crash dump triage | Architecture planning, multi-file refactor design, reverse-engineering, subtle race condition debugging | `gemini-4-argon-high`<br>`claude-3-opus`<br>`claude-3-7-sonnet` (extended thinking) |
| **Tier 2: Code Implementation** | High code generation accuracy, fast syntax matching | Writing features from spec, implementing unit tests, targeted diff replacements | `gemini-4-argon-medium`<br>`claude-3-5-sonnet` |
| **Tier 3: Fast Hands (Mechanical)** | Sub-second latency, zero reasoning overhead, near-zero cost | Git staging/commits, running test suites, inspecting directory listings, moving/renaming files, grep/find | `gemini-3.8-flash`<br>`claude-3-5-haiku` |

---

## 2. Autonomous Subagent Delegation Protocol

When operating under an autonomous parent agent, offload Tier 3 mechanical work to lightweight subagents:

```python
# Launching mechanical work via Flash subagent
invoke_subagent(
    TypeName="research",
    Role="Mechanical Runner",
    Model="flash",
    Prompt="Run pytest -q on tests/test_core.py and report only the failure lines if any."
)
```

- **Quota Savings:** Preserves the parent agent's weekly frontier quota while burning lightweight tokens that replenish every 5 hours.
- **Context Isolation:** Leaves noisy command outputs inside the subagent transcript, keeping the parent context lean and fully cached.

---

## 3. Interactive CLI Model Switching Shortcuts

When using interactive CLI sessions, use model toggle commands when transitioning from planning to execution:

- **Antigravity CLI:** Drop effort level after planning is approved:
  - Planning: `--effort high`
  - Execution: `--effort low` / switch model to Flash
- **Claude Code CLI:**
  - Shift between `/model claude-3-5-sonnet` and `/model claude-3-5-haiku` for routine maintenance.
- **Live Terminal Cheat Sheet (`dynamic-repo-model-cheatsheet`):**
  - Run `cs` (`agy-cheatsheet`) or check `🎯 Rec: ...` in the statusline to see when dirty `.cpp`/`.hlsl` files have been committed via `repo-auto-sync --checkpoint` and the workspace is ready to downshift back to `Flash • Low`.


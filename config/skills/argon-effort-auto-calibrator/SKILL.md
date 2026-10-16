---
name: argon-effort-auto-calibrator
description: Dynamically calibrates Gemini 4 Argon reasoning effort (--effort low/medium/high) turn-by-turn based on cognitive task complexity, slashing thinking token burn by up to 85% on routine tool execution.
---

# Argon Effort Auto-Calibrator (`argon-effort-auto-calibrator`)

Gemini 4 Argon provides industry-leading reasoning capabilities, but under `--effort high` or `max`, it generates **4,000 to 12,000 internal thinking tokens per turn**. Using high-effort reasoning for mechanical tasks (e.g. running bash commands, applying pre-planned file diffs, inspecting directories) burns through weekly Argon quota prematurely.

This skill dynamically scales Argon's thinking budget turn-by-turn to match the precise cognitive demand of the current step.

---

## 1. Dynamic Effort Calibration Matrix

| Cognitive Complexity | Optimal Argon Effort | Internal Reasoning Budget | Appropriate Task Scope |
| :--- | :--- | :--- | :--- |
| **Level 0: Mechanical** | `--effort low` | < 300 thinking tokens | Git commits, file moves, running tests, statusline checks, reading 1 file |
| **Level 1: Surgical Diff** | `--effort low` | < 500 thinking tokens | Applying planned chunk replacements (`replace_file_content`), typo fixes |
| **Level 2: Standard Feature** | `--effort medium` | 1,000 – 2,000 tokens | Implementing unit tests, adding a new config section, standard Lua callback |
| **Level 3: Deep Architecture**| `--effort high` | 4,000 – 8,000 tokens | Formulating `/plan`, 64-bit struct padding proofs, reverse engineering disassembly |
| **Level 4: Fatal Crash Triage**| `--effort high` | 8,000 – 12,000 tokens | Unknown memory corruption, multi-threaded deadlocks, segfault callstack triage |

---

## 2. Turn-by-Turn Escalation & De-Escalation Rules

1. **Start Low on Execution:**
   Once an architectural plan is approved, drop to `--effort low` immediately for code modifications and test executions.
2. **Escalate Only on Resistance:**
   If a test fails or a compiler emits an unexpected error:
   - *Attempt 1:* Escalate to `--effort medium` to diagnose the error.
   - *Attempt 2+ (Persistent Failure):* Escalate to `--effort high` to explore alternative hypotheses (`deliberative-reasoning-tree`).
3. **Instant De-Escalation on Pass:**
   The moment tests pass, immediately de-escalate back to `--effort low` for the next routine task.

---

## 3. Direct Tool Dispatch Anchor

When invoking tools under Argon, enforce direct action:
```text
"Direct Action Mode: Execute tool call immediately without preamble, repetitive restatements, or speculative internal monologue. Let tool results provide the evidence."
```

---
name: argon-thinking-governor
description: Gemini 4 Argon internal chain-of-thought (CoT) and reasoning token governor. Clamps speculative reasoning bloat during routine tool execution and enforces the hybrid 'Argon Brain, Flash Hands' dispatch pattern.
---

# Gemini 4 Argon Thinking Governor (`argon-thinking-governor`)

Gemini 4 Argon provides industry-leading reasoning and a 1M token context window, but under `--effort high` or `max`, it can generate **4,000 to 12,000 internal thinking tokens per turn** on routine tool calls.

This skill eliminates thinking token inflation, enforcing zero-monologue tool calls and the **"Argon Brain, Flash Hands"** hybrid execution pattern.

---

## Core Governance Directives

### 1. Direct Tool Invocation (Zero Monologue)
- **The Rule:** When an action requires calling a tool (`view_file`, `replace_file_content`, `run_command`, `write_to_file`), emit the tool call **immediately**.
- **Prohibited:** Speculating in internal reasoning about what the file might contain, reciting file lines in chain-of-thought, or justifying obvious edits before making them.
- **Execution Principle:** Let the tool result provide the evidence.

### 2. The "Argon Brain, Flash Hands" Protocol
- **Heavy Planning & Triage:** Run Argon (`--effort high` or `--model gemini-4-argon-high`) or dispatch an Argon subagent (`invoke_subagent(Model="pro")`) exclusively for:
  - Root cause analysis on engine crashes and segfaults.
  - Initial architectural plan formulation (`writing-plans` / `/plan`).
  - Complex reverse-engineering disassembly analysis.
- **Execution & Diffing:** Once the plan is established, drop to **Gemini 3.8 Flash** or `--effort low` to execute the code modifications, unit tests, and file creations.
- **Quota Impact:** Reduces total session token burn by **75% to 85%**.

### 3. Reasoning Effort Matrix

| Task Category | Optimal Argon Effort | Recommended Model Tier | Expected CoT Overhead |
| :--- | :--- | :--- | :--- |
| **Typo / Single File Edit** | `--effort low` | `gemini-3.8-flash-low` | < 250 tokens |
| **Standard Feature / TDD** | `--effort medium` | `gemini-4-argon-medium` | ~1,000 tokens |
| **Architecture / Plan / RE**| `--effort high` | `gemini-4-argon-high` | ~4,000–8,000 tokens |
| **Extreme Multi-Crash Loop**| `--effort max` | `gemini-4-argon-high` | Full deliberation |

---

## Prompt Injection Anchor

When launching `agy` sessions where Argon is active, include this anchor directive:

```text
"Direct Action Mode: Execute tools immediately without preamble, repetitive restatements, or speculative internal monologue. Let tool results provide the evidence."
```

## Related & Interoperating Skills
- **`argon-subagent-dispatch-routing`**: Implements the 'Argon Brain, Flash Hands' subagent swarm dispatch pattern to offload high-volume read, search,...
- **`claude-thinking-budget-governor`**: Extended thinking token budget governor for Claude 3.7+ Sonnet and Opus. Clamps internal reasoning tokens duri...
- **`argon-effort-auto-calibrator`**: Dynamically calibrates Gemini 4 Argon reasoning effort (--effort low/medium/high) turn-by-turn based on cognit...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

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
| **Tier 0: Local Fleet Offload** | Offline open-weights models (34 models in VRAM/RAM including 70B/72B Titans & Specialists), zero cloud billing | Docstrings, commit messages, boilerplate, ODE math, 32-to-64-bit pointers, CAD bpy scripts, RE decompilation, formal padding proofs | `local-coprocessor`<br>(`qwen2.5:72b`, `deepseek-r1:70b`, `llm4decompile:22b`, `blenderllm:7b`) |
| **Tier 1: Fast Hands (Mechanical)** | Sub-second latency, zero reasoning overhead, minimal token burn | Applying planned file diffs, running test suites, git staging/commits, status reports | `gemini-3.8-flash` (`--effort low`)<br>`claude-3-5-haiku` |
| **Tier 2: Code Implementation** | High code generation accuracy, fast syntax matching | Writing features from spec, implementing unit tests, targeted diff replacements | `gemini-3.8-flash` (`--effort medium`)<br>`gemini-4-argon` (`low`) |
| **Tier 3: Heavy Deliberation** | Deep chain-of-thought, hypothesis trees, crash dump triage | Architecture planning, multi-file refactor design, reverse-engineering, fatal crash triage | `gemini-4-argon` (`--effort high`)<br>`claude-3-7-sonnet` (extended thinking) |

---

## 2. 50% Weekly Quota Safe Reserve Offload Policy

When the weekly quota reaches or drops to **50% remaining** (`weekly <= 50%`):
1. **Aggressive Tier 0 Diversion:** Automatically divert code generation, C++ refactoring, LTX configs, and planning from cloud models to the local fleet (`qwen2.5:72b-iq2`, `deepseek-coder-v2:16b`, `deepseek-r1:70b-iq2`, `qwen2.5-coder:32b`).
2. **Sub-4B Rapid Offload Acceleration:** Route sub-second mechanical edits, docstrings, regex, and sanity checks through ultra-compact local models (`deepseek-r1:1.5b`, `smollm2:1.7b`, `phi3.5:latest`, `qwen2.5-coder:1.5b`, `llama3.2:3b`) running at 100–140 tok/s in VRAM.
3. **Cloud Reserve Lock:** Conserves the remaining 50% weekly cloud quota exclusively for final verification gates, complex unresolved compiler cascades, or production sign-offs, guaranteeing the quota lasts seamlessly until the new week reset.

---

## 3. Autonomous Subagent Delegation Protocol

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

## 4. Interactive CLI Model Switching Shortcuts

When using interactive CLI sessions, use model toggle commands when transitioning from planning to execution:

- **Antigravity CLI:** Drop effort level after planning is approved:
  - Planning: `--effort high`
  - Execution: `--effort low` / switch model to Flash
- **Claude Code CLI:**
  - Shift between `/model claude-3-5-sonnet` and `/model claude-3-5-haiku` for routine maintenance.
- **Live Terminal Cheat Sheet (`dynamic-repo-model-cheatsheet`):**
  - Run `cs` (`agy-cheatsheet`) or check `🎯 Rec: ...` in the statusline to see when dirty `.cpp`/`.hlsl` files have been committed via `repo-auto-sync --checkpoint` and the workspace is ready to downshift back to `Flash • Low`.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`claude-opus-plan-sonnet-exec`**: Three-tier model routing architecture for Anthropic Claude ('Opus Plan, Sonnet Code, Haiku Hands'). Preserves ...
- **`argon-effort-auto-calibrator`**: Dynamically calibrates Gemini 4 Argon reasoning effort (--effort low/medium/high) turn-by-turn based on cognit...
- **`claude-thinking-budget-governor`**: Extended thinking token budget governor for Claude 3.7+ Sonnet and Opus. Clamps internal reasoning tokens duri...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

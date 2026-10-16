---
name: adaptive-reasoning
description: Automatic reasoning effort selection and cognitive complexity routing. Automatically scales between instant-speed execution on Flash and deep-reasoning planning on Argon based on prompt complexity.
---

# Adaptive Reasoning & Cognitive Complexity Routing

This skill governs automatic reasoning selection and model escalation to maximize response speed and minimize quota consumption.

---

## Cognitive Complexity Tiers

Before beginning work on any user request, evaluate the prompt's structural complexity:

### Tier 1: Trivial / Direct Execution
* **Triggers:** Single-line fixes, simple typo corrections, direct shell commands, asking for file locations, formatting, or quick status checks.
* **Reasoning Strategy:**
  * Zero extended deliberation.
  * Apply immediate pinpoint diffs via `replace_file_content` or execute terminal commands directly.
  * Run with standard/low thinking latency (keeps streaming instant and saves quota).

### Tier 2: Standard Engineering & Implementation
* **Triggers:** Implementing a specific function, refactoring a single module, writing unit tests, or fixing a verified bug.
* **Reasoning Strategy:**
  * When incoming requests are verbose or conversational, activate `high-density-prompting` to distill into a 4-part surgical directive.
  * When the user requests calculators, data models, or parameter tuning, route to `intelligent-interactive-ui` to generate a reactive single-file micro-app.
  * Follow Test-Driven Development (`test-driven-development`) or targeted debugging (`systematic-debugging`).
  * Sanitize tool outputs using `log-output-sanitizer`.
  * Rely on compiler/linter feedback (e.g. `cargo check`, `ruff`, `clang-tidy`, `pytest`).
  * Execute directly on Gemini 3.8 Flash using surgical diffs.

### Tier 3: Deep Architectural & Multi-System Design
* **Triggers:** Designing new mods, multi-file refactoring, kernel modules (`omen-acpi`), reverse engineering unfamiliar binaries, visual layout diagnostics, or full game architectures.
* **Reasoning Strategy:**
  * Activate `deliberative-reasoning-tree` to explore 3 branching hypothesis paths and conduct adversarial self-critique before writing code.
  * For live visual layout glitches, GUI rendering anomalies, or game HUD overlaps, route desktop/window capture to `screen-vision-inspector`.
  * Route deep external inquiries into unfamiliar APIs to `deep-research-synthesizer`.
  * Route exact mathematical formulas, DSP biquad filter calculations, and log analytics to `sandbox-code-interpreter`.
  * Automatically escalate the architecture and plan drafting phase to a **`pro` (Gemini 4 Argon)** subagent via `invoke_subagent`.
  * Once the plan artifact is created and approved, route all execution back to **Flash** for quota-efficient task completion.

---
name: adaptive-reasoning
description: Dynamic cognitive complexity routing and reasoning effort tuning between Flash and Argon (adaptive_model_router).
---

# Adaptive Reasoning & Model Effort Router (`adaptive-reasoning`)

Governs model escalation and reasoning effort tuning to maximize response speed and minimize quota burn.

## Hierarchy
- **Tier 0:** Zero-Quota Local Fleet Offload (`local-coprocessor`, 34 Ollama models).
- **Tier 1:** Trivial / Direct Execution (Flash, instant streaming, surgical diffs).
- **Tier 2:** Standard Engineering (Flash medium reasoning, test verification).
- **Tier 3:** Deep Architecture & Planning (Argon high reasoning, 3-branch ToT).
- **Router CLI:**
  `python3 config/skills/adaptive-reasoning/scripts/adaptive_model_router.py route --error "<error>" --attempts <N>`
- **Auditor & Updater:**
  `skills-audit-update (--audit, --sync, --fix)`

## Related & Interoperating Skills
- **`local-model-coprocessor`**: Zero-quota offload to 32-thread CPU + RTX 5060 Ollama fleet (34 local models, local AST, and local RAG).
- **`first-principles-reasoning`**: First-principles debugging, 3-branch Tree-of-Thought deliberation, Ockham's razor, and Chain-of-Verification.
- **`standalone-binary-re`**: Native Linux zero-MCP reverse engineering: objdump, readelf, nm, rizin, gdb, JADX, and PE/ELF headers.
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

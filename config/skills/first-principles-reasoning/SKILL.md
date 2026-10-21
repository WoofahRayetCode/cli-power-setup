---
name: first-principles-reasoning
description: First-principles debugging, 3-branch Tree-of-Thought deliberation, Ockham's razor, and Chain-of-Verification.
---

# First-Principles Reasoning (`first-principles-reasoning`)

Eliminates trial-and-error debugging and cognitive overburn through structured Tree-of-Thought exploration and mathematical proofing.

## Deliberation Protocol
1. **Branching Hypotheses:** Formulate 3 distinct candidate root causes (Branch A, Branch B, Branch C).
2. **Adversarial Red-Teaming:** Critique each branch against engine constraints, callstacks, and memory bounds.
3. **Formal Backtracking:** If an approach reveals fatal contradictions, explicitly backtrack before touching code.
4. **Selected Convergence:** Implement only the provably sound fix.
5. **Truth Auditor Tool:**
   `python3 config/skills/first-principles-reasoning/scripts/grok_truth_auditor.py`

## Related & Interoperating Skills
- **`adaptive-reasoning`**: Dynamic cognitive complexity routing and reasoning effort tuning between Flash and Argon (adaptive_model_route...
- **`reverse-engineer-anything`**: Reverse Engineer Anything (REA) MCP server integration, function diffing, and obligation ledgers.
- **`argon-adversarial-verification-gate`**: Formal 4-stage pre-completion adversarial self-critique and boundary-condition proofing for Argon and Claude.
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

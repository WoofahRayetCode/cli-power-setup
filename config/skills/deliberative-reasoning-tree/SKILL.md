---
name: deliberative-reasoning-tree
description: DeepSeek R1 and OpenAI o1-style Tree-of-Thought reasoning, exploring 3 branching hypothesis paths, adversarial self-critique, and formal backtracking before code modification.
---

# Deliberative Reasoning Tree & Adversarial Self-Critique

This skill implements advanced deliberative reasoning (Tree-of-Thought), forcing the AI to explore branching solution paths, attack its own logic from an adversary's perspective, and backtrack before writing code.

---

## 🌲 Tree-of-Thought (ToT) Protocol

```
                 [Problem Statement]
                /         |         \
         [Path A]      [Path B]     [Path C]
       (Naive Fix)   (Deep Refactor) (Proxy/Hook)
            |             |             |
       [Critique]    [Critique]    [Critique]
         (Fails)       (Selected)   (High Risk)
```

1. **Branching Exploration:** Formulate 3 distinct technical architectures or hypotheses.
2. **Adversarial Red-Teaming:** Critique each path for:
   * Edge cases (empty inputs, null pointers, integer overflows).
   * Concurrency & race conditions (deadlocks, thread safety).
   * Memory & quota costs (allocations, cache misses, complexity).
3. **Formal Backtracking:** If an approach reveals fatal flaws during critique, explicitly backtrack and explain why it was abandoned.
4. **Selected Convergence:** Proceed only with the provably superior path.

---

## 🔄 Interoperability & Handoffs

* **Handoff to `adaptive-reasoning`:** Activates automatically when prompt complexity warrants deep deliberative reasoning.
* **Handoff to `superpowers`:** Feeds the selected path directly into `writing-plans`.\n

## Related & Interoperating Skills
- **`argon-adversarial-verification-gate`**: Harnesses Gemini 4 Argon's deep reasoning capacity for formal adversarial self-critique, boundary-condition pr...
- **`chatgpt-o1-hypothesis-tree`**: Emulates ChatGPT o1/o3-mini Tree-of-Thought deliberation on Gemini 4 Argon. Branches into 3 competing hypothes...
- **`claude-thinking-budget-governor`**: Extended thinking token budget governor for Claude 3.7+ Sonnet and Opus. Clamps internal reasoning tokens duri...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

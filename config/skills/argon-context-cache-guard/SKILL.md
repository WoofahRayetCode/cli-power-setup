---
name: argon-context-cache-guard
description: Anchors and stabilizes Gemini 4 Argon context to ensure sessions cross and maintain the 32,768-token cache threshold for maximum 95% KV prompt caching discounts.
---

# Argon Context Cache Guard (`argon-context-cache-guard`)

Gemini 4 Argon offers an industry-leading **95% prompt caching discount** ($0.10/1M cached input vs $2.00/1M uncached input), but this discount requires crossing a strict **32,768-token floor** and maintaining 100% prefix invariance.

If a session hovers under 32k tokens, or if dynamic tokens (timestamps, ephemeral random seeds) are placed at the beginning of the prompt, the entire context misses cache and pays full price.

This skill ensures sessions cross the 32k floor cleanly and locks the prefix to guarantee 95% savings on every turn.

---

## 1. Argon Caching Mechanics

| Parameter | Specification | Impact |
| :--- | :--- | :--- |
| **Caching Floor** | **32,768 tokens** | Turns below 32k pay 100% uncached rate ($2.00/MTok). Turns above 32k pay $0.10/MTok. |
| **Cache Read Discount**| **95% discount** | 20x cost reduction on prompt tokens. |
| **Incremental Granularity** | Continuous sliding | Any new tokens beyond the cached prefix cost standard rate; the prefix stays discounted. |
| **Cache Lifetime (TTL)** | Rolling session / 1 hr | Kept alive by turn activity within the active session. |

---

## 2. Floor Crossing Strategy

To avoid paying full price across dozens of short introductory turns:
1. **Upfront Rule Anchoring:** Always include full workspace rules (`RULE[user_global]`), tool definitions, and skill indices in the system block. This naturally lifts standard Antigravity sessions above the 32k floor right away.
2. **Deterministic Context Padding:** If a session is at 28k–30k tokens, pulling in relevant reference documentation or AST skeletons immediately pushes the context over 32,768 tokens, locking in the 95% discount for all subsequent turns.
3. **Avoid Premature Truncation:** Do not run `/compact` prematurely when context is between 33k and 80k tokens. Staying comfortably above 32k ensures you maintain the 95% discount without falling below the floor.

---

## 3. Strict Prefix Invariance Rules

To prevent breaking the KV cache on Argon:
1. **Never Put Timestamps in System Prompts:** Dynamic dates and current times must strictly reside in trailing user message blocks (e.g. `<ADDITIONAL_METADATA>`), never in system rules.
2. **Frozen Tool Schemas:** Never dynamically alter tool definitions mid-session.
3. **Static System Directives:** Ensure behavioral guidelines and project instructions remain byte-for-byte identical turn-over-turn.

## Related & Interoperating Skills
- **`multi-model-cache-harmonizer`**: Prompt cache prefix stabilization and alignment engine across Claude, Gemini, OpenAI, and Grok. Aligns static ...
- **`gemini-flash-cache-aligner`**: Maximizes Gemini 3.8 Flash prompt caching discounts (>90% savings) through strict prefix stabilization, 4,096-...
- **`agy-context-telemetry`**: Deep context window utilization and token cost inspector for Antigravity CLI (parity with claude /context and ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

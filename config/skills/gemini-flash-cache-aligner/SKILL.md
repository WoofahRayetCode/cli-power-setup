---
name: gemini-flash-cache-aligner
description: Maximizes Gemini 3.8 Flash prompt caching discounts (>90% savings) through strict prefix stabilization, 4,096-token floor anchoring, and dynamic variable isolation.
---

# Gemini Flash Cache Aligner (`gemini-flash-cache-aligner`)

Gemini 3.8 Flash features an automatic implicit prompt caching tier that provides a **90% discount** on cached input tokens, but requires a strict **4,096-token minimum prefix threshold** and **exact character-level prefix invariance**. Modifying a single character high in the prompt invalidates the Key-Value (KV) attention chain and forfeits the 90% discount.

This skill governs prompt prefix structure and caching discipline for all Gemini Flash operations.

---

## 1. The 4,096-Token Floor Rule

- **The Threshold:** Prompts with fewer than 4,096 tokens are **billed at 100%** with zero cache discount.
- **Optimization Strategy:**
  - On new sessions, front-load essential static project definitions, interface types, and tool schemas so the prompt prefix immediately crosses the 4,096-token boundary.
  - Once across 4,096 tokens, every subsequent turn reuses the precomputed KV cache at the **90% discount rate** (0.1x compute cost).

---

## 2. Prefix Invariance & Dynamic Isolation

To prevent cache invalidation during multi-turn sessions:

```text
┌────────────────────────────────────────────────────────────────────────┐
│  STATIC PREFIX (100% IMMUTABLE -> CACHED AT 90% DISCOUNT)             │
│  - System instructions & coding standards                              │
│  - Tool definitions & CLI environment capabilities                     │
│  - Project architecture map & unchanging interface types               │
├────────────────────────────────────────────────────────────────────────┤
│  DYNAMIC TAIL (APPEND-ONLY -> RECOMPUTED EACH TURN)                    │
│  - Incremental tool call execution outputs                             │
│  - Targeted line diffs (replace_file_content)                          │
│  - User requests and model responses                                   │
└────────────────────────────────────────────────────────────────────────┘
```

### Prohibited Behaviors:
- **Never inject dynamic timestamps** into system prompts or rules.
- **Never modify global `.md` rule headers mid-session**.
- **Never rewrite entire files** when only modifying a few lines; full-file replacements generate large diffs that disrupt downstream attention caching.

---

## 3. High-Density Diffing Protocol

When modifying existing code under Gemini Flash:
1. Always prefer **surgical chunk replacements** (`replace_file_content`) over full rewrites.
2. Keep edits focused to $\le$ 30 lines per replacement.
3. Keep the conversation transcript lean so cache retrieval latency remains sub-second.

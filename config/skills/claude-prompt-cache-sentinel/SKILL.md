---
name: claude-prompt-cache-sentinel
description: Maximizes Anthropic Prompt Caching discounts (90% savings) through strict 1,024-token boundary alignment blocks, prefix freezing, and 5-minute ephemeral TTL protection.
---

# Claude Prompt Cache Sentinel (`claude-prompt-cache-sentinel`)

Anthropic offers a **90% discount** on prompt tokens that hit the KV cache (`cache_read_input_tokens`) compared to uncached input tokens. However, the cache is easily broken by small non-deterministic shifts in the conversation prefix or by crossing the 5-minute ephemeral TTL window during long compilations.

This skill aligns Claude Code sessions to Anthropic's caching architecture to guarantee maximum savings.

---

## ⚡ 1. The 1,024-Token Boundary Block Principle

Anthropic cuts prompt caching blocks into **1,024-token increments**.
- To qualify for caching, the cached prefix must exceed **1,024 tokens** (Sonnet 3.5/3.7) or **2,048 tokens** (Opus).
- Any change in the prefix invalidates *all subsequent blocks* in the prompt cache.

### Core Rules for Prefix Stability:
1. **Never Insert Volatile Preamble**: Never place dynamic timestamps, battery percentages, or fluctuating host temperatures at the start of prompts.
2. **Anchor Global Instructions**: Keep `CLAUDE.md` and system rules frozen at the very beginning of the context.
3. **Group Static Tool Definitions**: Ensure tool declarations and static schemas precede dynamic user messages.

---

## ⏱️ 2. The 5-Minute TTL Protection Protocol

Anthropic prompt caches are ephemeral with a **5-minute Time-To-Live (TTL)**.
- If a build, test suite, or long-running game playtest takes **> 300 seconds** before the next interaction, the entire KV cache expires, forcing a full-cost re-billing of all context tokens.
- **Pre-Wait Compaction**: Before launching any job expected to take `> 60s`, if active context exceeds 40,000–50,000 tokens, stage state to `.agents/memory/activeContext.md` and run `/compact`.
- **Log Tail Redirection**: Pipe noisy stdout to `/dev/shm/<job>.log` and only read `tail -n 25` to avoid loading megabytes of text that would dirty the prompt cache.

---

## 🔗 Related & Interoperating Skills
- **`claude-ultimate-quota-sentinel`**: Master 6-pillar quota and rate-limit preservation engine for Claude Code.
- **`fable-planning-token-compressor`**: 5-tier planning compression pipeline for Claude Fable 5.1.
- **`claude-context-rot-shield`**: Proactive 40k–50k compaction boundaries and attention protection.
- **`claude-eco`**: Launcher setting `--effort low` with low thinking budget and prompt cache alignment.

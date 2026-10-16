---
name: prompt-cache-context-optimizer
description: Emulates 1M+ context windows and maximizes Anthropic prompt caching discounts (>90% savings) through strict prefix ordering, hierarchical AST compression, and cache stabilization.
---

# Prompt Cache & Massive Context Optimizer

This skill establishes prompt structuring techniques, context cache stabilization, and hierarchical AST compression to emulate an infinite context window in Claude Code while slashing input token costs by up to 90%.

---

## ⚡ How Anthropic Prompt Caching Works

Anthropic prompt caching triggers on exact prefix matches of 1,024+ tokens. Any change to a single character in the beginning of a prompt invalidates the cache for all subsequent tokens.

### Optimization Rules:
1. **Static Rules First:** Keep system rules (`CLAUDE.md`, `GEMINI.md`) and tool definitions completely static at the prompt prefix.
2. **Deterministic Context Ordering:** Never interleave dynamic files between static project instructions. Order: `System Rules -> Project Brief -> Architecture -> Active Code -> Dynamic User Prompt`.
3. **5-Minute Cache TTL Refresh:** When running long workflows, periodic lightweight pings keep the 5-minute cache alive, preventing full re-reading fees.

---

## 🧠 1. Emulating Massive Context Windows (1M+ Tokens)

When working on massive codebases that exceed 200k tokens:

* **Hierarchical AST Summaries:** Instead of reading 50 full files into context, generate a 2-level structural index:
  ```json
  {
    "file": "src/core/engine.cpp",
    "classes": ["Engine", "RenderPipeline"],
    "methods": ["Init()", "RenderFrame()", "Shutdown()"],
    "dependencies": ["glad/glad.h", "GLFW/glfw3.h"]
  }
  ```
* **Rolling Context Snapshots:** Store solved state in `.agents/memory/activeContext.md` and instruct the user or CLI to run `/compact`. Resume from the compacted snapshot with zero loss of architecture.

---

## 📉 Token Economy Visibility

* Reading a 150k token repo 10 times un-cached: **1,500,000 billed input tokens**.
* Reading with stabilized prompt caching (>90% discount): **~165,000 effective input tokens**.\n
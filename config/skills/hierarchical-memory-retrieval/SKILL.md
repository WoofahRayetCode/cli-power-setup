---
name: hierarchical-memory-retrieval
description: Multi-tiered query-driven memory retrieval across working context, episodic logs (.agents/episodes/), semantic project patterns (.agents/memory/), and archival records with BM25 ranking.
---

# Hierarchical Memory Retrieval & Semantic Context Extraction

When working in long-lived repositories with dozens of past sessions and 129+ agent skills, blindly re-reading full memory files (`systemPatterns.md`, `techContext.md`, `activeContext.md`, and past episode logs) consumes **5,000–15,000 input tokens** every session startup.

**`hierarchical-memory-retrieval`** establishes a 4-tier cognitive memory architecture with query-driven BM25 search, extracting only pinpoint relevant memory sections (<250 tokens) in under 15ms.

---

## 🏛️ The 4-Tier Memory Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│ Tier 1: L1 Scratchpad / Working Memory                      │
│ Active prompt, tool results, in-flight diffs (<2,000 tokens)│
├─────────────────────────────────────────────────────────────┤
│ Tier 2: L2 Semantic Project Memory                          │
│ .agents/memory/ (activeContext, systemPatterns, learnings)  │
├─────────────────────────────────────────────────────────────┤
│ Tier 3: L3 Episodic Narrative Log                           │
│ .agents/episodes/*.md (Chronological ADRs & milestone paths)│
├─────────────────────────────────────────────────────────────┤
│ Tier 4: L4 Archival Repository Memory                       │
│ Git history, changelogs, architecture RFCs, release tags    │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚡ 1. Instant Memory Search CLI

Query project memory and past episode logs without loading the files:

```bash
# Query memory with BM25 ranking (top 3 snippets)
python3 config/skills/hierarchical-memory-retrieval/scripts/memory_retriever.py "Vulkan descriptor set binding"

# Search specific directories with JSON output
python3 config/skills/hierarchical-memory-retrieval/scripts/memory_retriever.py "Proton audio desync" --dirs .agents/memory .agents/episodes --top 2 --json
```

### Output Example:
```text
🔍 Top 2 Memory Matches for: 'Proton audio desync'
------------------------------------------------------------
[1] .agents/memory/learnings.md > Audio Latency in Wine (Relevance: 3.84)
    Excerpt: Setting PULSE_LATENCY_MSEC=60 in Proton game launch prevents buffer underrun crackling...
[2] .agents/episodes/20261014_audio_subsystem.md > OpenAL Soft Buffer Fix (Relevance: 2.45)
    Excerpt: Fixed AL_BUFFER_SIZE allocation desync by clamping source sample rates to 48kHz...
```

---

## 🧠 2. Selective Hydration Protocol (Sub-300 Tokens)

1. **Do NOT** blindly read all files in `.agents/memory/` or `.agents/episodes/`.
2. When answering a specific domain question or debugging a recurring error:
   - Run `memory_retriever.py "<keyword>"` first.
   - If a high-confidence match ($>2.0$ score) is found, read only the target section lines using `view_file` with `StartLine`/`EndLine`.
   - Never inject irrelevant memory files into active context.

---

## 🔄 Interoperability & Handoffs

* **Handoff to `project-memory-bank`:** Indexes and retrieves data maintained in `.agents/memory/`.
* **Handoff to `session-episodic-memory`:** Searches chronological milestones and ADRs in `.agents/episodes/`.
* **Handoff to `token-economy`:** Cuts memory hydration cost from ~10,000 tokens to <250 tokens per turn.

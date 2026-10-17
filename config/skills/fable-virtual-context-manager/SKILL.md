---
name: fable-virtual-context-manager
description: Virtualized context paging and hierarchical indexing for Claude Fable (1M-token context). Prevents full 1M-token re-billing by paging active 30k-token subsystem slices from a disk-backed knowledge graph into working memory.
---

# Fable Virtual Context Manager (`fable-virtual-context-manager`)

Claude Fable features a **1-million-token context window**, designed for multi-day, long-horizon software engineering. However, ingesting 500,000+ tokens of raw source files into working memory across every turn incurs severe input token re-billing and attention drift.

This skill establishes a disk-backed **virtualized context paging architecture** that allows Fable to reason over massive codebases with the token efficiency of a lightweight session.

---

## 1. Virtualized Context Architecture

Instead of holding entire multi-gigabyte source trees in active context, Fable maintains a disk-backed knowledge graph:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ MASTER KNOWLEDGE GRAPH (.agents/fable_index.json on disk)              │
│ - Complete symbol dependency map across all engine subsystems          │
│ - Full call-graph links, struct layouts, and interface contracts       │
├────────────────────────────────────────────────────────────────────────┤
│ ACTIVE WORKING WINDOW (In-Prompt: ~25k to 40k tokens)                  │
│ - Paged Subsystem Slice: ONLY current focus (e.g. xrRender shaders)    │
│ - Pinned Static Prefix: Coding standards, tool specs, core types       │
│ - Active Hypothesis & Current Blocker (activeContext.md)               │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. On-Demand Subsystem Paging Protocol

When transitioning across architectural boundaries (e.g. from C++ physics in `xrPhysics` to Lua scripts in `gamedata/scripts/`):
1. **Flush Inactive Slice:** Unload detailed implementation files of the completed subsystem from the working context.
2. **Page Active Slice:** Load only the interface headers and symbol references of the target subsystem:
   ```bash
   # Extract only the active subsystem slice from the master index
   python3 -c "import json; idx = json.load(open('.agents/fable_index.json')); print(idx['xrRender']['interfaces'])"
   ```
3. **Token Savings:** Reduces turn input billing from **600,000 tokens down to ~30,000 tokens** (95% reduction), while preserving full architectural coherence.

---

## 3. Pinned Cache Invariance for 1M Context

- Maintain exact character-level invariance in the prompt prefix.
- Never inject fluctuating timestamps, live clock counters, or random seeds into system instructions.
- Ensure that the static foundation remains pinned in Anthropic's prompt cache for up to 24 hours, guaranteeing the **90% prompt caching discount**.

---

## 4. Automated Host Slice Extraction (`fable_slice_extractor.py`)

Run the automated host slice extractor before ingesting any subsystem:
```bash
./scripts/fable_slice_extractor.py <subsystem_dir> --format xml --max-files 50
```
- **Zero Hallucination:** Directly parses C++ classes, methods, inheritance, and Lua functions into line-anchored `<fn L="...">` tags.
- **Sub-Second Speed:** Parses 50 files in <30ms on host CPU with zero LLM API calls.
- **Guaranteed Compression:** Replaces 50,000–100,000 lines of implementation code with a 1,500-token interface skeleton.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`fable-atomic-diff-sequencer`**: Multi-file refactor execution coordinator for Claude Fable 5.1. Regulates Fable's 128k output capacity by brea...
- **`claude-fable-engine-governor`**: Autonomous context, token, and quota governor for Anthropic's Claude Fable model during large-scale game engin...
- **`local-vector-rag-engine`**: Local vector embeddings and dense semantic search engine running on host CPU/GPU/RAM. Replaces context-stuffin...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

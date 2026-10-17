---
name: semantic-codebase-indexing
description: Cursor and Windsurf-style AST symbol indexing, call-graph tracing, and ctags/tree-sitter repository mapping for instant token-efficient code navigation.
---

# Semantic Codebase Indexing & AST Symbol Graphs

This skill brings Cursor and Windsurf-style instant codebase symbol intelligence to Claude Code, maintaining a lightweight AST index to trace classes, functions, and callers in milliseconds.

---

## 🗺️ Why Semantic Indexing Saves Quota

* Traditional AI search: Greps across 200 files and reads 50 full source files into context (**>30,000 tokens**).
* Semantic Symbol Index: Queries a 50KB pre-built symbol map to locate exact function definitions and callers in 10ms (**<300 tokens**).

---

## 🛠️ 1. Lightweight Symbol Index Generation

Generate a fast JSON symbol map using Universal Ctags or Python AST:

```bash
# Generate compact JSON tags for all symbols
ctags -R --output-format=json --fields=+n+K -f .code_index_tags.json src/ 2>/dev/null || true
```

Query symbols instantly:
```bash
# Find exact function definition without reading the whole file
jq -r 'select(.name=="RenderFrame") | "\(.path):\(.line) [\(.kind)]"' .code_index_tags.json
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `prompt-cache-context-optimizer`:** Provides the AST summaries needed to emulate 1M+ context windows.
* **Handoff to `token-economy`:** Drastically reduces input token consumption by targeting exact file lines.\n

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`qwen-polyglot-ast-cartographer`**: Emulates Qwen 2.5 Coder polyglot AST cartography. Generates instant symbol call-graphs, inheritance trees, and...
- **`local-vector-rag-engine`**: Local vector embeddings and dense semantic search engine running on host CPU/GPU/RAM. Replaces context-stuffin...
- **`stalker-spawn-entity-indexer`**: High-performance local indexer and query engine for S.T.A.L.K.E.R. unpacked all.spawn and game.graph archives....
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

---
name: local-research-scout
description: Autonomous zero-quota multi-source web search, documentation scraping, and technical query synthesis. Sources across DuckDuckGo HTML, GitHub API, StackOverflow, and direct page scraping, ranking evidence with local embeddings (bge-m3) and synthesizing answers using local LLMs (deepseek-coder-v2:16b, deepseek-r1:14b, qwen2.5:32b).
---

# Local Research Scout (`local-research-scout`)

Zero-quota, multi-source technical web search and RAG synthesis engine. Runs entirely on host CPU and RTX 5060 GPU with zero external cloud API keys and 0 tokens billed to Gemini or Claude.

## Key Capabilities

1. **Federated Multi-Source Search**:
   - **DuckDuckGo HTML Engine**: Natural language search across documentation, modding forums, ModDB, Reddit, and wikis.
   - **GitHub Repositories API**: Open-source game engines (OGSR, X-Ray, Godot), shaders, forks, and release assets.
   - **StackOverflow / StackExchange API**: Compiler errors, 64-bit migration traps, pointer truncation fixes, and Linux system API solutions.
2. **Local RAG & Dense Retrieval**:
   - Embeds query and documentation snippets using local `bge-m3` or `nomic-embed-text`.
   - Computes cosine similarity to select the top-k most relevant evidence blocks.
3. **Specialized Local Synthesis**:
   - **Game Engine Porting / C++ / HLSL**: Synthesized by `deepseek-coder-v2:16b` (128k context, MoE architecture).
   - **Math, Physics, Root-Cause Debugging**: Synthesized by `deepseek-r1:14b` / `deepseek-r1:32b` (deep Chain-of-Thought reasoning).
   - **Modern Web / Tailwind / Frameworks**: Synthesized by `qwen2.5-coder:14b`.
   - **Dialogue / Translations**: Synthesized by `aya:8b`.

## CLI Usage

```bash
# Multi-source technical search with LLM synthesis (0 Cloud Tokens)
local-research-scout "OGSR engine 64-bit cmake build instructions"

# Search with deep page scraping and bge-m3 local RAG ranking
local-research-scout "c++ pointer truncation 64 bit x86_64 fix" --scrape --rag

# Raw search mode (fast link and snippet extraction without LLM synthesis)
local-research-scout "godot 4 compute shader buffer synchronization" --raw-search

# GitHub repositories only
local-research-scout "X-Ray engine 64-bit" --github-only

# StackOverflow only
local-research-scout "linux uinput virtual keyboard permissions" --so-only

# Save research report artifact to .agents/research/
local-research-scout "S.T.A.L.K.E.R. LTX weapon ballistics formulas" --save-artifact
```

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`local-vector-rag-engine`**: Local vector embeddings and dense semantic search engine running on host CPU/GPU/RAM. Replaces context-stuffin...
- **`local-model-coprocessor`**: Offloads low-complexity tasks (docstrings, commit messages, log summarization, regex, boilerplate) to local SL...
- **`adaptive-reasoning`**: Automatic reasoning effort selection and cognitive complexity routing. Automatically scales between instant-sp...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

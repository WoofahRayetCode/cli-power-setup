---
name: claude-local-fleet-offloader
description: Offloads low-complexity and repetitive engineering tasks from Claude Code to the 42-model local Ollama fleet, automatically activating 50% weekly quota Safe Mode to preserve Anthropic cloud tokens.
---

# Claude Local Fleet Offloader (`claude-local-fleet-offloader`)

Claude 3.7 Sonnet and Opus are world-class reasoning models, but using cloud tokens for mechanical symbol searches, boilerplate generation, decompilation analysis, and unit test logs burns expensive rate limits and exhausts weekly quotas rapidly.

This skill equips Claude Code with an automated **Zero-Quota Local Offload Pipeline**, routing specialized engineering tasks to the local 42-model Ollama fleet running on the host AMD Ryzen 9 (32 threads) and NVIDIA GeForce RTX 5060 Laptop GPU (8GB GDDR7 VRAM).

---

## 🛡️ 1. The 50% Weekly Quota Safe Mode

When Claude Code's weekly quota drops to **$\le 50\%$**, this skill automatically engages **Safe Mode**:
- **Divert Code Generation**: Divert repetitive boilerplate, CRUD, LTX configs, and test fixtures to local models via `local-coprocessor` or `agy-omni-mode --exec`.
- **Divert C++ Decompilation**: Offload disassembly analysis and pseudocode reconstruction to `llm4decompile:22b-q4`.
- **Divert Math & Physics**: Route ballistics curves and matrix proofs to `deepseek-r1:70b-iq2` or `mathstral:7b`.
- **Divert 3D Blender Automation**: Route procedural geometry and shader scripts to `blender-architect` or `blenderllm:7b-q4`.
- **Preserve Claude Quota**: Reserve the remaining 50% cloud quota strictly for high-level architectural decisions and difficult debugging until the weekly reset.

---

## 🤖 2. Complete 42-Model Local Fleet Catalog & Routing Matrix

Claude Code can route any engineering task to host CPU/GPU/RAM via `local-coprocessor exec` or `claude-omni-mode --exec`:

### Tier 1: Ultra-Large Titans (70B-72B) — Safe Mode Primary Drivers
| Model | Size / VRAM | Primary Specialization | Invocation Command |
| :--- | :--- | :--- | :--- |
| `qwen2.5:72b-iq2` | 25 GB / RAM+VRAM | Deep systems C++, large-scale refactors, 64-bit engine ports | `local-coprocessor exec --task titan-code --prompt "..."` |
| `llama3.3:70b-iq2` | 19 GB / RAM+VRAM | Swarm orchestration, autonomous tool-calling, agent workflows | `local-coprocessor exec --task titan-agent --prompt "..."` |
| `deepseek-r1:70b-iq2` | 19 GB / RAM+VRAM | Formal mathematical verification, struct padding, deep CoT | `local-coprocessor exec --task titan-reason --prompt "..."` |

### Tier 2: 24B-47B Heavyweights & Mixture-of-Experts
| Model | Size / VRAM | Primary Specialization | Invocation Command |
| :--- | :--- | :--- | :--- |
| `mixtral:8x7b` | 26 GB / RAM+VRAM | High-capacity sparse MoE, complex polyglot reasoning | `local-coprocessor exec --task moe-heavy --prompt "..."` |
| `command-r:35b` | 18 GB / RAM+VRAM | Enterprise agentic RAG, citation grounding, tool calling | `local-coprocessor exec --task enterprise-agent --prompt "..."` |
| `qwen2.5-coder:32b` | 19 GB / RAM+VRAM | Multi-file SWE-bench code architecture, full test suites | `local-coprocessor exec --task code-frontier --prompt "..."` |
| `deepseek-r1:32b` | 19 GB / RAM+VRAM | Complex algorithm verification, 32B deep chain-of-thought | `local-coprocessor exec --task reason-32b --prompt "..."` |
| `qwen2.5:32b` | 19 GB / RAM+VRAM | General synthesis, polyglot software design, doc generation | `local-coprocessor exec --task general-synthesis --prompt "..."` |
| `mistral-small:24b` | 14 GB / RAM+VRAM | Dense reasoning, large context technical synthesis | `local-coprocessor exec --task mistral-small --prompt "..."` |

### Tier 3: Binary Decompilation & MoE Code Engines (16B-22B)
| Model | Size / VRAM | Primary Specialization | Invocation Command |
| :--- | :--- | :--- | :--- |
| `llm4decompile:22b-q4` | 13 GB / RAM+VRAM | Assembly decompilation, Ghidra/Rizin pseudocode reconstruction | `local-coprocessor exec --task decompile --prompt "..."` |
| `deepseek-coder-v2:16b` | 8.9 GB / RAM+VRAM | Cross-engine shader transpilation, SPIR-V/HLSL, MoE coding | `local-coprocessor exec --task shader --prompt "..."` |

### Tier 4: Mid-Weight Domain Specialists (9B-14B)
| Model | Size / VRAM | Primary Specialization | Invocation Command |
| :--- | :--- | :--- | :--- |
| `phi4:14b` | 9.1 GB / 8GB VRAM | Physics engines, ODEs, numerical ballistics math | `local-coprocessor exec --task physics --prompt "..."` |
| `deepseek-r1:14b` | 9.0 GB / 8GB VRAM | Fast CoT reasoning, algorithm assertions, logic proofs | `local-coprocessor exec --task reason-14b --prompt "..."` |
| `qwen2.5-coder:14b` | 9.0 GB / 8GB VRAM | Modular C++/Python refactoring, API integration | `local-coprocessor exec --task code-14b --prompt "..."` |
| `mistral-nemo:12b` | 7.1 GB / 8GB VRAM | 128k long-context analysis, full build log summarization | `local-coprocessor exec --task long --prompt "..."` |
| `codegeex4:9b` | 5.5 GB / 8GB VRAM | Whole-repo AST search, 128k context symbol call-graph | `local-coprocessor exec --task code-repo --prompt "..."` |
| `gemma2:9b` | 5.4 GB / 8GB VRAM | Executive communications, proposals, technical reports | `local-coprocessor exec --task business --prompt "..."` |

### Tier 5: Workhorse Domain Specialists (6.7B-8B) — 100% VRAM Resident
| Model | Size / VRAM | Primary Specialization | Invocation Command |
| :--- | :--- | :--- | :--- |
| `blenderllm:7b-q4` | 4.7 GB / VRAM | Blender 3D bpy scripts, procedural geometry, modifiers | `local-coprocessor exec --task blender --prompt "..."` |
| `blender-architect:latest` | 4.7 GB / VRAM | Blender SDF remeshing, game-ready assets, OGF/DM exports | `local-coprocessor exec --task blender-arch --prompt "..."` |
| `qwen2.5-coder:7b` | 4.7 GB / VRAM | Everyday C++/Python coding, unit test implementation | `local-coprocessor exec --task test --prompt "..."` |
| `qwen2.5:7b` | 4.7 GB / VRAM | Modern web frontend, Tailwind CSS, HTML UI layouts | `local-coprocessor exec --task web --prompt "..."` |
| `hermes3:8b` | 4.7 GB / VRAM | Function calling, JSON schema compliance, structured tools | `local-coprocessor exec --task tool --prompt "..."` |
| `llama3.1:8b` | 4.9 GB / VRAM | General conversation, interactive brainstorming, dialogues | `local-coprocessor exec --task conversation --prompt "..."` |
| `deepseek-r1:8b` | 5.2 GB / VRAM | Boundary condition assertions, unit test logic proofs | `local-coprocessor exec --task reason-8b --prompt "..."` |
| `aya:8b` | 4.8 GB / VRAM | Game localization, S.T.A.L.K.E.R. string table XML translation | `local-coprocessor exec --task translate --prompt "..."` |
| `granite-code:8b` | 4.6 GB / VRAM | C#, .NET 8/9, Avalonia UI, XAML GUI components | `local-coprocessor exec --task csharp --prompt "..."` |
| `starcoder2:7b` | 4.0 GB / VRAM | Rust systems programming, Cargo, borrow checker fixes | `local-coprocessor exec --task rust --prompt "..."` |
| `codellama:7b-python` | 3.8 GB / VRAM | Python automation scripts, pytest suites, data pipelines | `local-coprocessor exec --task python --prompt "..."` |
| `deepseek-coder:6.7b-instruct`| 3.8 GB / VRAM | Linux kernel, POSIX APIs, low-level C systems | `local-coprocessor exec --task systems-posix --prompt "..."` |
| `mathstral:7b` | 4.1 GB / VRAM | Quaternion SLERP, linear algebra, 3D math | `local-coprocessor exec --task math --prompt "..."` |
| `wizard-math:7b` | 4.1 GB / VRAM | Matrix transformations, competition math proofs | `local-coprocessor exec --task competition-math --prompt "..."` |
| `sqlcoder:7b` | 4.1 GB / VRAM | SQLite schemas, SQL query tuning, DDL migrations | `local-coprocessor exec --task sql --prompt "..."` |

### Tier 6: Multimodal Vision Engines (VRAM Resident)
| Model | Size / VRAM | Primary Specialization | Invocation Command |
| :--- | :--- | :--- | :--- |
| `llava:13b` | 8.0 GB / VRAM | High-accuracy UI layout audit, architecture diagrams | `local-coprocessor exec --task vision-13b --image <path>` |
| `minicpm-v:8b` | 5.5 GB / VRAM | In-game screen telemetry, HUD verification, visual diffs | `local-coprocessor exec --task vision --image <path>` |
| `moondream:latest` | 1.7 GB / VRAM | Sub-second bounding box checks, fast image QA | `local-coprocessor exec --task fast-vision --image <path>` |

### Tier 7: Compact & Sub-Second Edge Engines (1.5B-3.8B)
| Model | Size / VRAM | Primary Specialization | Invocation Command |
| :--- | :--- | :--- | :--- |
| `llama3.2:3b` | 2.0 GB / VRAM | Quick status notifications, brief draft responses | `local-coprocessor exec --task status-report --prompt "..."` |
| `phi3.5:latest` | 2.2 GB / VRAM | 128k mini-logic, fast math, rapid text evaluation | `local-coprocessor exec --task mini-logic --prompt "..."` |
| `smollm2:1.7b` | 1.8 GB / VRAM | Sub-second docstrings, code formatting, commit notes | `local-coprocessor exec --task docstring --prompt "..."` |
| `qwen2.5-coder:1.5b` | 986 MB / VRAM | Regex generation, boilerplate bridges, syntax snippets | `local-coprocessor exec --task regex --prompt "..."` |
| `deepseek-r1:1.5b` | 1.1 GB / VRAM | Sub-second sanity proofs, micro CoT validation | `local-coprocessor exec --task fast-reason --prompt "..."` |

### Tier 8: Local Vector Embedding Engines
| Model | Size / VRAM | Primary Specialization | Invocation Command |
| :--- | :--- | :--- | :--- |
| `bge-m3:latest` | 1.2 GB / VRAM | Multilingual dense embeddings, hybrid search | `local-coprocessor exec --task embed-dense --prompt "..."` |
| `nomic-embed-text:latest`| 274 MB / VRAM | Fast code embeddings, semantic repository retrieval | `local-coprocessor exec --task embed --prompt "..."` |

---

## ⚡ 3. Terminal Offload CLI Helpers for Claude Code

When working on any repository, invoke local models directly via the native Bash tool:
1. **Direct Model Invocation**: `local-coprocessor exec --model <model-name> --prompt "<prompt>"`
2. **Task-Driven Routing**: `local-coprocessor exec --task <task-name> --prompt "<prompt>"`
3. **Dynamic Fleet Orchestration**: `claude-omni-mode --exec --task <task> --prompt "<prompt>"`
4. **Token Savings & VRAM Headroom**: `local-coprocessor status` (inspect lifetime saved tokens)
5. **Symbol & Slice Inspection**: `slice-reader <file> <start> <end>` or `token-guard grep -n "pattern"`


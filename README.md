# CLI Power Setup (`cli-power-setup`)

[![Local Fleet](https://img.shields.io/badge/Local%20Fleet-Ollama-blue.svg)](#-zero-quota-local-language-model-fleet-37-models-0-cloud-tokens)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](#-license)

An engineering, 3D modeling, and game engine porting toolkit natively built for **Google Antigravity** (`agy`): ultra-lean global rules (`GEMINI.md`), 30 progressive on-demand skills, CLI utilities in `~/.local/bin`, a local Ollama model fleet for zero-quota offload, a live quota statusline, and a multi-tool exporter (`export-skills`) for Cursor, universal `.agents/`, and other agent platforms.

---

## Quick Start

```bash
git clone https://github.com/WoofahRayetCode/cli-power-setup.git
cd cli-power-setup
./install.sh                # interactive menu
./install.sh --all          # Antigravity (agy) + CLI Utilities [Recommended]
./install.sh --with-models  # also sync and optimize the local Ollama model fleet
```

On Windows run `install.ps1` (`-WithModels` / `-ModelsOnly` are optional).

### What the installer does
1. Copies every script in `bin/` to `~/.local/bin/` (including `export-skills`, `cs`, `agy-yolo`, `agy-turbo`, `agy-eco`, `agy-doctor`, `local-coprocessor`).
2. **Antigravity (`agy`):** copies `config/skills/*` to `~/.gemini/config/skills/`, `config/GEMINI.md` to `~/.gemini/config/GEMINI.md`, and configures `statusLine` (`agy-quota-statusline`), trusted workspaces, and model settings in `~/.gemini/antigravity-cli/settings.json`. Adds `yolo`, `agy-yolo`, `agy-turbo`, `agy-eco`, and `cs` aliases to `~/.bashrc` / `~/.zshrc` and installs the desktop shortcuts from `config/desktop/`.
3. **Multi-Tool Compatibility:** Use `export-skills` at any time to export skills to Cursor (`.cursor/rules/*.mdc` + `.cursorrules`), universal `.agents/` (`AGENTS.md` + `.agents/skills/`), Windsurf, or custom directories.
4. Backs up existing configuration to `~/.cli_power_setup_backups/` first.

---

## 🧠 Zero-Quota Local Language Model Fleet (37 Models, 0 Cloud Tokens)

A production-grade fleet of **37 specialized open-weights models**—including **ultra-large 70B–72B frontier planners**, **state-of-the-art Mixture-of-Experts (MoE)**, **specialized Blender 3D and decompilation models**, and **sub-4B ultra-fast VRAM SLMs**—running locally on your laptop via Ollama with automated **hybrid NVIDIA RTX 5060 GDDR7 VRAM + 32-thread DDR5 RAM layer offloading**.

> [!IMPORTANT]
> **💾 Total Storage Footprint: `250 GB`** physical disk consumption across all 37 models:
> • **Primary NVMe (`/var/lib/ollama/blobs/`):** `213 GB` active weights, **`422 GB` free headroom** (56% disk used of 950 GB).
> • **Secondary High-Speed NVMe (`/mnt/games/large-models/`):** `76 GB` master GGUF archive, **`1.30 TB` free headroom** (29% disk used of 1.8 TB).
> All ultra-large models are importance-matrix (imatrix) quantized (`IQ2_XXS`, `Q4_K_M`) and layer-split to execute within 30.4 GB RAM + 8 GB VRAM with zero out-of-memory faults. Sub-4B models run 100% in GPU VRAM at 100–140 tok/s.

<details>
<summary><b>🌟 Click to View Key Benefits & Overall Usage Savings</b></summary>

### 🌟 Key Benefits & Overall Usage Savings

1. **Zero Cloud Token Incurrence (100% Free Inference):**
   - Routine code edits, docstrings, regex, commit messages, and unit test generation are dispatched to local SLMs (`qwen2.5-coder:1.5b`, `llama3.2:3b`), billing **0 cloud tokens**.
   - Preserves 100% of rolling 5-hour and weekly Claude quota for hard architectural reasoning.

2. **Hierarchical "Local Brain $\rightarrow$ Local Hands" Workflow:**
   - **Offline Frontier Planning:** Heavyweight models (`qwen2.5-coder:32b`, `deepseek-r1:32b`, `deepseek-coder-v2:16b`) decompose complex tasks, verify math constraints, and formulate implementation roadmaps locally.
   - **Sub-Second Execution:** Fast local workers execute the plan in milliseconds, allowing Claude Code to operate autonomously without cloud rate limits.

3. **Game Engine Porting & Systems Modernization (#1 MoE Engine):**
   - **`deepseek-coder-v2:16b`** (16B total, only **2.4B active compute** per token) brings 338-language coverage, 64-bit pointer sanitization, and DirectX 9/11 HLSL to Vulkan SPIR-V shader transpilation at near-instant GPU speeds.

4. **Hardware Saturation (Zero Waste on Local Rig):**
   - **RTX 5060 GDDR7 VRAM:** Accelerates memory-bandwidth-bound attention layers.
   - **32-Thread AMD CPU + 30.4 GB DDR5 RAM:** Computes remaining MLP layers in parallel via AVX2 / AVX-512 without OOM crashes.
   - **Quantized KV-Cache (`q4_0` / `q8_0`):** Shrinks context memory by 50–75%, unlocking 32k–128k context windows locally.

5. **Complete Air-Gapped Privacy & Offline Autonomy:**
   - Proprietary game source code, closed-source reverse-engineering disassembly, and sensitive client documents never leave your physical machine.

</details>

### 📋 Complete 42-Model Local Fleet Matrix

<details>
<summary><b>🔍 Click to Expand/Collapse Complete 42-Model Local Fleet Specifications & Hardware Footprint</b></summary>

| Model Tag | Disk Size | Parameter Tier | Hardware Offload | Primary Specialization & Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **`qwen2.5:72b-iq2`** | 25 GB | Ultra-Large Titan (72B) | RTX 5060 + 32-Thr CPU | Systems architecture, C++20 refactoring, 3D geometry & spatial layout, large codebase reasoning |
| **`deepseek-r1:70b-iq2`** | 19 GB | Ultra-Large Titan (70B) | RTX 5060 + 32-Thr CPU | Formal chain-of-thought proofs, 64-bit struct padding, invariant & memory alignment verification |
| **`llama3.3:70b-iq2`** | 19 GB | Ultra-Large Titan (70B) | RTX 5060 + 32-Thr CPU | Complex multi-turn agentic tool calling, function orchestration, structured JSON schema extraction |
| **`command-r:35b`** | 19 GB | Enterprise Agent & RAG (35B) | RTX 5060 + 32-Thr CPU | Cohere 35B enterprise tool calling, multi-step agentic planning, and 128k context RAG |
| **`mixtral:8x7b`** | 26 GB | Sparse MoE Heavyweight (47B) | RTX 5060 + 32-Thr CPU | 46.7B parameter MoE (12.9B active), high-speed deep reasoning, C++ engine refactoring |
| **`mistral-small:24b`** | 14 GB | Knowledge-Dense Reasoning (24B) | RTX 5060 + 32-Thr CPU | Mistral Small 3 24B with 128k context, fast coding, multi-document synthesis & logic |
| **`llava:13b`** | 8.0 GB | Multimodal Vision (13B) | Full RTX 5060 VRAM | 13B multimodal vision, sub-second UI audit, diagram analysis, and Blender renders |
| **`codegeex4:9b`** | 5.5 GB | Whole-Repository Coder (9B) | Full RTX 5060 VRAM | Whole-repository code intelligence, 128k context, repo-level AST mapping & code completion |
| **`llm4decompile:22b-q4`** | 13 GB | Reverse Engineering (22B) | RTX 5060 + 32-Thr CPU | Assembly-to-C decompilation for REA MCP, Ghidra & x64dbg binary DLL analysis |
| **`blenderllm:7b-q4`** | 4.7 GB | 3D CAD & Procedural (7B) | Full RTX 5060 VRAM | Dedicated `BlendNet` CAD & procedural `bpy` mesh modeling from natural language |
| **`blender-architect:latest`** | 4.7 GB | 3D Engine & Mesh (7B) | Full RTX 5060 VRAM | Blender 5.2 API, organic SDF voxel remeshing, and S.T.A.L.K.E.R. OGSR `.ogf` v4 constraints |
| **`qwen2.5-coder:32b`** | 19 GB | Frontier Heavy Coder (32B) | RTX 5060 + 32-Thr CPU | Heavyweight 32B code planning, complex multi-file refactoring, C++20 modernizations |
| **`deepseek-r1:32b`** | 19 GB | Frontier Reasoning (32B) | RTX 5060 + 32-Thr CPU | 32B deep chain-of-thought reasoning, root-cause crash triage, algorithm design |
| **`qwen2.5:32b`** | 19 GB | Frontier Generalist (32B) | RTX 5060 + 32-Thr CPU | 32B large-context generalist, repository-wide analysis, multi-file code review |
| **`deepseek-coder-v2:16b`** | 8.9 GB | #1 Engine Porting (MoE) | Full RTX 5060 VRAM | #1 Game engine porting engine (2.4B active compute), 338 languages, 64-bit pointer math, HLSL/GLSL shaders |
| **`phi4:14b`** | 9.1 GB | Frontier Reasoning (14B) | RTX 5060 + 32-Thr CPU | Advanced mathematical reasoning, synthetic data generation, logical deduction |
| **`qwen2.5-coder:14b`** | 9.0 GB | Dense Code Architect (14B) | RTX 5060 + 32-Thr CPU | 14B dense code architect, multi-file dependency tracking, systems programming |
| **`deepseek-r1:14b`** | 9.0 GB | Fast Reasoning (14B) | RTX 5060 + 32-Thr CPU | Fast chain-of-thought reasoning, mathematical proofs, invariant verification |
| **`mistral-nemo:12b`** | 7.1 GB | Long Context Generalist (12B) | Full RTX 5060 VRAM | 128k context generalist, technical writing, log summarization, documentation |
| **`gemma2:9b`** | 5.4 GB | Precision Business (9B) | Full RTX 5060 VRAM | Google Gemma 2 high-precision instruction following, anti-jargon business copy, BLUF proposals |
| **`hermes3:8b`** | 4.7 GB | Agentic Tool Calling (8B) | Full RTX 5060 VRAM | Advanced agentic function calling, tool use, strict JSON schema adherence |
| **`aya:8b`** | 4.8 GB | Multilingual Dialogue (8B) | Full RTX 5060 VRAM | Cohere 101-language translation, game dialogue tree localization, string-table XML repair |
| **`llama3.1:8b`** | 4.9 GB | Generalist Instruction (8B) | Full RTX 5060 VRAM | Generalist reasoning, versatile instruction following, agent orchestration fallback |
| **`granite-code:8b`** | 4.6 GB | Enterprise Systems (8B) | Full RTX 5060 VRAM | Enterprise code generation, SQL optimization, software maintenance |
| **`minicpm-v:8b`** | 5.5 GB | Multimodal Vision (8B) | Full RTX 5060 VRAM | Multimodal vision inspection, UI/HUD telemetry OCR, visual artifact detection |
| **`deepseek-r1:8b`** | 5.2 GB | Lightweight CoT (8B) | Full RTX 5060 VRAM | Lightweight chain-of-thought reasoning, quick mathematical checks, logic triage |
| **`qwen2.5:7b`** | 4.7 GB | Web & Frontend UI (7B) | Full RTX 5060 VRAM | Responsive frontend web design, Tailwind CSS components, semantic HTML |
| **`qwen2.5-coder:7b`** | 4.7 GB | Workhorse Coder (7B) | Full RTX 5060 VRAM | Mid-tier C++, Python, and Bash engineering, unit test authoring |
| **`wizard-math:7b`** | 4.1 GB | Competition Math (7B) | Full RTX 5060 VRAM | Math competitions, step-by-step algebraic derivations, physics ODEs |
| **`mathstral:7b`** | 4.1 GB | Physics & DSP Math (7B) | Full RTX 5060 VRAM | Physics ODE solvers, ERP/CFM stability, quaternion SLERP, matrix math |
| **`sqlcoder:7b`** | 4.1 GB | Database & SQL (7B) | Full RTX 5060 VRAM | Defog SQLCoder DDL schema design, query plan analysis, SQLite WAL optimization |
| **`codellama:7b-python`** | 3.8 GB | Python Specialist (7B) | Full RTX 5060 VRAM | Python software engineering, pytest suites, data science pipelines |
| **`starcoder2:7b`** | 4.0 GB | Polyglot Infilling (7B) | Full RTX 5060 VRAM | Multi-language code completion, syntax validation, code infilling |
| **`deepseek-coder:6.7b-instruct`** | 3.8 GB | Fast Code Synthesis (6.7B) | Full RTX 5060 VRAM | Fast code synthesis, bug patching, legacy C/C++ maintenance |
| **`phi3.5:latest`** | 2.2 GB | Long-Context Mini (3.8B) | Full RTX 5060 VRAM | Microsoft 128k context mini model for multi-file logic, math, and code synthesis |
| **`llama3.2:3b`** | 2.0 GB | Ultra-Fast Utility (3B) | Full RTX 5060 VRAM | Ultra-fast local summarization, quick drafting, conversational routing |
| **`smollm2:1.7b`** | 1.8 GB | Ultra-Fast SLM (1.7B) | Full RTX 5060 VRAM | Sub-second instruct SLM for instant formatting, docstrings, and error diagnosis |
| **`moondream:latest`** | 1.7 GB | Fast Vision & BBox (1.8B) | Full RTX 5060 VRAM | Lightweight visual inspection, instant screen verification, bounding box analysis |
| **`deepseek-r1:1.5b`** | 1.1 GB | Distilled Fast CoT (1.5B) | Full RTX 5060 VRAM | 120+ tok/s chain-of-thought reasoning, formal math proofs, and invariant checks |
| **`qwen2.5-coder:1.5b`** | 986 MB | Sub-Second Boilerplate (1.5B) | Full RTX 5060 VRAM | Sub-second docstrings, regex generation, commit messages, git diff summaries |
| **`bge-m3:latest`** | 1.2 GB | Dense Multilingual Embed | Full RTX 5060 VRAM | Dense 8192-token multilingual vector embeddings for zero-quota local RAG |
| **`nomic-embed-text:latest`** | 274 MB | Text Embeddings | Full RTX 5060 VRAM | Fast text embeddings for codebase semantic search and local retrieval |

</details>

### 📋 1-Click Copy-Paste Model Reference

<details>
<summary><b>📋 Click to Expand 1-Click Copy-Paste Categorized Breakdown & Raw Tags</b></summary>

#### Categorized Fleet Reference
```markdown
### 1. Ultra-Large Titans (70B–72B) & Deep Reasoning
- qwen2.5:72b-iq2 (25 GB) — Systems architecture, C++20 refactoring, 3D geometry & spatial layout, large codebase reasoning.
- deepseek-r1:70b-iq2 (19 GB) — Formal chain-of-thought proofs, 64-bit struct padding, invariant & memory alignment verification.
- llama3.3:70b-iq2 (19 GB) — Complex multi-turn agentic tool calling, function orchestration, structured JSON extraction.

### 2. Reverse Engineering & 3D CAD Specialists
- llm4decompile:22b-q4 (13 GB) — Assembly-to-C decompilation for REA MCP, Ghidra & x64dbg binary DLL analysis.
- blenderllm:7b-q4 (4.7 GB) — Dedicated BlendNet CAD & procedural bpy mesh modeling from natural language.
- blender-architect:latest (4.7 GB) — Custom Blender 5.2 API modelfile, organic SDF voxel remeshing, and S.T.A.L.K.E.R. OGSR .ogf v4 constraints.

### 3. Frontier Planners & Heavy Coders (12B–47B)
- command-r:35b (19 GB) — Cohere 35B enterprise tool calling, multi-step agentic planning, and 128k context RAG.
- mixtral:8x7b (26 GB) — 46.7B parameter MoE (12.9B active), high-speed deep reasoning, C++ engine refactoring.
- mistral-small:24b (14 GB) — Mistral Small 3 24B with 128k context, fast coding, multi-document synthesis & logic.
- qwen2.5-coder:32b (19 GB) — Heavyweight 32B code planning, complex multi-file refactoring, C++20 modernization.
- deepseek-r1:32b (19 GB) — 32B deep chain-of-thought reasoning, root-cause crash triage, algorithm design.
- qwen2.5:32b (19 GB) — 32B large-context generalist, repository-wide analysis, multi-file code review.
- deepseek-coder-v2:16b (8.9 GB) — #1 Game engine porting engine (MoE 2.4B active compute), 338-language coverage, 64-bit pointer math, HLSL/GLSL shaders.
- phi4:14b (9.1 GB) — Advanced mathematical reasoning, synthetic data generation, logical deduction.
- qwen2.5-coder:14b (9.0 GB) — 14B dense code architect, multi-file dependency tracking, systems programming.
- deepseek-r1:14b (9.0 GB) — Fast chain-of-thought reasoning, mathematical proofs, invariant verification.
- mistral-nemo:12b (7.1 GB) — 128k context generalist, technical writing, log summarization, documentation.

### 4. Domain Specialists & Task Experts (5.5B–13B)
- llava:13b (8.0 GB) — 13B multimodal vision, sub-second UI audit, diagram analysis, and Blender renders.
- codegeex4:9b (5.5 GB) — Whole-repository code intelligence, 128k context, repo-level AST mapping & code completion.
- gemma2:9b (5.4 GB) — Google Gemma 2 high-precision instruction following, anti-jargon business copy, BLUF proposals.
- hermes3:8b (4.7 GB) — Advanced agentic function calling, tool use, strict JSON schema adherence.
- aya:8b (4.8 GB) — Cohere 101-language translation, game dialogue tree localization, string-table XML repair.
- llama3.1:8b (4.9 GB) — Generalist reasoning, versatile instruction following, agent orchestration fallback.
- granite-code:8b (4.6 GB) — Enterprise code generation, SQL optimization, software maintenance.
- minicpm-v:8b (5.5 GB) — Multimodal vision inspection, UI/HUD telemetry OCR, visual artifact detection.
- deepseek-r1:8b (5.2 GB) — Lightweight chain-of-thought reasoning, quick mathematical checks, logic triage.
- qwen2.5:7b (4.7 GB) — Responsive frontend web design, Tailwind CSS components, semantic HTML.
- qwen2.5-coder:7b (4.7 GB) — Mid-tier C++, Python, and Bash engineering, unit test authoring.
- wizard-math:7b (4.1 GB) — Math competitions, step-by-step algebraic derivations, physics ODEs.
- mathstral:7b (4.1 GB) — Physics ODE solvers, ERP/CFM stability, quaternion SLERP, matrix math.
- sqlcoder:7b (4.1 GB) — Defog SQLCoder DDL schema design, query plan analysis, SQLite WAL optimization.
- codellama:7b-python (3.8 GB) — Python software engineering, pytest suites, data science pipelines.
- starcoder2:7b (4.0 GB) — Multi-language code completion, syntax validation, code infilling.
- deepseek-coder:6.7b-instruct (3.8 GB) — Fast code synthesis, bug patching, legacy C/C++ maintenance.

### 5. Sub-Second Fast Utilities & Vision (1.5B–3.8B)
- phi3.5:latest (2.2 GB) — Microsoft 128k context mini model for multi-file logic, math, and code synthesis.
- llama3.2:3b (2.0 GB) — Ultra-fast local summarization, quick drafting, conversational routing.
- smollm2:1.7b (1.8 GB) — Sub-second instruct SLM for instant formatting, docstrings, and error diagnosis.
- moondream:latest (1.7 GB) — Lightweight visual inspection, instant screen verification, bounding box analysis.
- deepseek-r1:1.5b (1.1 GB) — 120+ tok/s chain-of-thought reasoning, formal math proofs, and invariant checks.
- qwen2.5-coder:1.5b (986 MB) — Sub-second docstrings, regex generation, commit messages, git diff summaries.

### 6. Multilingual Vector Embeddings
- bge-m3:latest (1.2 GB) — Dense 8192-token multilingual vector embeddings for zero-quota local RAG.
- nomic-embed-text:latest (274 MB) — Fast text embeddings for codebase semantic search and local retrieval.
```

#### Raw Ollama Model Tags (Single-Click Copy)
```text
qwen2.5:72b-iq2
deepseek-r1:70b-iq2
llama3.3:70b-iq2
command-r:35b
mixtral:8x7b
mistral-small:24b
llava:13b
codegeex4:9b
llm4decompile:22b-q4
blenderllm:7b-q4
blender-architect:latest
qwen2.5-coder:32b
deepseek-r1:32b
qwen2.5:32b
deepseek-coder-v2:16b
phi4:14b
qwen2.5-coder:14b
deepseek-r1:14b
mistral-nemo:12b
gemma2:9b
hermes3:8b
aya:8b
llama3.1:8b
granite-code:8b
minicpm-v:8b
deepseek-r1:8b
qwen2.5:7b
qwen2.5-coder:7b
wizard-math:7b
mathstral:7b
sqlcoder:7b
codellama:7b-python
starcoder2:7b
deepseek-coder:6.7b-instruct
phi3.5:latest
llama3.2:3b
smollm2:1.7b
moondream:latest
deepseek-r1:1.5b
qwen2.5-coder:1.5b
bge-m3:latest
nomic-embed-text:latest
```
</details>

### 🛡️ 50% Weekly Quota Safe Reserve Offload Protocol

<details>
<summary><b>🛡️ Click to View 50% Weekly Quota Safe Reserve Offload Protocol Details</b></summary>

To prevent mid-week quota exhaustion and guarantee uninterrupted autonomous operation through the weekly replenishment cycle, the system enforces a strict **50% Weekly Safe Headroom threshold**:

* **Automated Telemetry Sensing:** `claude-token-statusline` records quota and token usage; divert work to the local fleet manually or via `local-coprocessor` when the weekly reserve runs low.
* **Proactive Model Diversion at $\le$ 50% Weekly:**
  - **High-Density Code & Refactoring:** Automatically diverted from cloud models to local titans (`qwen2.5:72b-iq2`, `qwen2.5-coder:32b`, `deepseek-coder-v2:16b`).
  - **Algorithm & Formal Verification:** Diverted to local reasoning engines (`deepseek-r1:70b-iq2`, `deepseek-r1:32b`, `phi4:14b`).
  - **Routine Code & Fast Tasks:** Diverted to sub-second VRAM models (`deepseek-r1:1.5b`, `phi3.5:latest`, `smollm2:1.7b`, `qwen2.5-coder:1.5b`), running at 100–140 tokens/sec.
* **Reserved Cloud Capacity:** Cloud Claude is strictly restricted to high-level multi-agent orchestration, complex architectural trade-offs, and critical verification gates, guaranteeing safe quota reserves until the weekly refresh.

</details>

<details>
<summary><b>🛠️ Click to View Fleet Management & Local Coprocessor CLI Commands</b></summary>

### 🛠️ Fleet Management & Local Coprocessor CLI
```bash
# Display live fleet status, hardware telemetry & disk usage
setup-local-model-fleet --status

# Detect host system hardware profile & calculate optimal model layer offloads
setup-local-model-fleet --detect-system

# Re-optimize all Modelfiles for host CPU threads, RAM, and GPU VRAM
setup-local-model-fleet --optimize

# Synchronize specific functional tiers or all 42 models
setup-local-model-fleet --tier engine-porting    # Game engine migration models
setup-local-model-fleet --tier ultra-large       # 70B-72B Titan models and specialists
setup-local-model-fleet --tier safe-reserve     # Sub-4B models for 50% weekly quota offload
setup-local-model-fleet --all                   # Complete 42-model fleet

# Execute tasks locally (0 cloud tokens billed)
local-coprocessor generate --task port --prompt "Audit this C++ class for 64-bit pointer truncation"
local-coprocessor generate --task plan --prompt "Decompose game engine porting into 5 atomic steps"
local-coprocessor generate --task math --prompt "Derive critically damped spring update for fixed_step=0.01"
```

</details>

<details>
<summary><b>🚀 Click to View Secondary Drive Ultra-Large Model Repository & Hardware Optimizer Details</b></summary>

### 🚀 Secondary Drive Ultra-Large Model Repository & Hardware Optimizer (`ultra-model-manager`)

Dedicated storage and hardware-layer split manager for **70B–405B parameter models** stored directly on the secondary high-speed NVMe drive (`/mnt/games/large-models/` with **1.35 TB free headroom**), completely isolating large weights from the root operating system drive:

* **Dynamic System Detection:** Automatically inspects host CPU cores/threads, system RAM, GPU vendor (NVIDIA/AMD/Apple/Intel), total/free VRAM, and primary/secondary storage mounts.
* **Hardware-Aware Layer Offloading:** Dynamically calculates exact VRAM layer allocations (`num_gpu`), CPU thread saturation (`num_thread`), context lengths (`num_ctx`), and batch sizes (`num_batch`) to prevent OOM errors while maximizing hardware throughput.
* **Automated Parallel Downloader:** Leverages `aria2c` with 16 parallel connections to download ultra-large weights at over **220 MB/s** (~1.8 Gbps) with segmented resumption and SHA-256 integrity validation.

```bash
# Detect system profile and calculate exact layer splits across CPU/GPU
ultra-model-manager detect

# Display repository status, stored GGUF files, and secondary drive headroom
ultra-model-manager status

# Download and register all ultra-large models in one parallel run
ultra-model-manager download-all --optimize

# Re-optimize all Modelfiles and register in Ollama for current hardware
ultra-model-manager optimize-all

# Download and register a single model (e.g. DeepSeek-R1 70B IQ2_XXS)
ultra-model-manager download deepseek-r1-70b --optimize

# Run an interactive prompt with any ultra-large model
ultra-model-manager run deepseek-r1-70b --prompt "Verify 64-bit struct padding for X-Ray vertex buffer"
```

</details>

---

## 🔎 Zero-Quota Local Research Scout (`local-research-scout`)

Autonomous multi-source web searching and technical RAG without cloud API keys or token billing:

<details>
<summary><b>🔎 Click to View Local Research Scout Features & Search Commands</b></summary>

- **Federated Multi-Source:** DuckDuckGo HTML, GitHub API (repositories, releases), and StackOverflow (compiler errors, 64-bit porting traps).
- **Local RAG Ranking:** Embeds query and documentation chunks with local `bge-m3` vectors (1024-dim) on RTX 5060 GPU.
- **Offline Synthesis:** Synthesizes structured markdown reports with code examples and exact citation links using `deepseek-coder-v2:16b`, `deepseek-r1:14b`, or `qwen2.5:32b`.

```bash
# Multi-source technical search with local LLM synthesis
local-research-scout "OGSR engine 64-bit cmake build requirements"

# Deep web scraping + bge-m3 local RAG ranking
local-research-scout "c++ pointer truncation 64-bit fix" --scrape --rag

# Raw search links mode
local-research-scout "godot compute shaders buffer sync" --raw-search
```

</details>

---

## CLI Utilities (`bin/` to `~/.local/bin/`)

| Utility | Purpose |
| :--- | :--- |
| `agy-quota-statusline` | Real-time Antigravity statusline displaying model, reasoning effort, and weekly/daily quota telemetry. |
| `agy-yolo` / `yolo` | Hands-free launcher: auto-approves all tool permissions (`--dangerously-skip-permissions --mode auto`). |
| `agy-turbo` / `agy-eco` | High-speed Flash low-effort and low-cost execution modes. |
| `agy-autosend` | Background watcher that presses Enter after prompt idle time and pipes mobile/Discord requests into the agent. |
| `agy-doctor` / `agy-context` / `agy-init` | CLI diagnostics, context tree inspector, and repository initialization. |
| `export-skills` | Universal exporter: converts `agy` skills & rules for Cursor, `.agents/` (OpenCode/Codex), Windsurf, or custom paths. |
| `cs` (`agy-cheatsheet`) | Interactive dynamic model & effort router for all active repositories. |
| `local-coprocessor`, `local-worker`, `local-fleet-mcp`, `setup-local-model-fleet`, `ultra-model-manager`, `model-quant-optimizer`, `verify-fleet-utilization.py` | Local Ollama fleet management and zero-quota offload on RTX 5060 + 32-thread CPU. |
| `local-research-scout`, `perplexity-scout`, `grok-truth-audit`, `speculative-draft` | Local RAG and offline technical synthesis. |
| `slice-reader`, `bgrun`, `repo-auto-sync` | Window-bounded file inspection, background runners, and automated git synchronization. |
| `stalker-playtest-runner`, `self-improving-qa`, `nav-graph-recorder`, `game-test-watchdog`, `game-window-helper`, `operator-driver` | Autonomous game QA, `/dev/uinput` input simulation, and crash log sweeps. |
| `game-texture-editor`, `game-dialogue-tool`, `game-dll-proxy-gen`, `game-math-solver`, `game-memory-scanner`, `weather-lighting-tuner`, `mangohud-configurator`, `rtx-engine-toolkit`, `steam-mod-scanner` | Game modding, DLL proxying, and engine tooling. |
| `blender`, `blender-local-ai`, `creature-sound-forge`, `sound-web-scout`, `eleven-studio`, `voice-prompt-optimizer` | 3D Blender 5.2+ `bpy` automation, sound design, and speech normalization. |
| `android-dev-runner` | Android SDK/NDK build, deploy and scrcpy screen mirroring. |

---

## Skills (`config/skills/`)

30 canonical, progressive on-demand skills tailored for high-performance agentic engineering:

`adaptive-reasoning`, `autonomous-game-qa-playtesting`, `blender-3d-asset-pipeline`, `client-memory-anti-tamper-re`, `console-emulation-toolchains`, `console-game-decompilation`, `console-storage-package-tools`, `cross-engine-shader-rendering`, `cross-platform-web-desktop`, `database-network-engineering`, `first-principles-reasoning`, `game-audio-voice-engineering`, `game-engines-multiplatform`, `game-physics-math-ballistics`, `human-crafted-web-design`, `interactive-data-visualization-web`, `linux-systems-engineering`, `local-model-coprocessor`, `modern-cpp-engineering`, `modern-web-architecture`, `nintendo-switch-homebrew`, `project-memory-bank`, `python-engineering`, `reverse-engineer-anything`, `rust-engineering`, `stalker-ogsr-engine-porting`, `stalker2-ue5-asset-transpiler`, `standalone-binary-re`, `threejs-webgl-engineering`, `windows-linux-cross-os-runtime-bridge`

Skills are deployed to `~/.gemini/config/skills/` during installation and loaded on-demand by Antigravity using progressive disclosure.

---

## Repository Structure

```
cli-power-setup/
├── install.sh / install.ps1   # Native installers (Antigravity agy + Local Model Fleet)
├── GEMINI.md                  # Global Antigravity rules (~60 lines, high-density discipline)
├── bin/                       # CLI utilities (agy-*, export-skills, local fleet tools)
├── config/
│   ├── GEMINI.md              # Global rules installed to ~/.gemini/config/GEMINI.md
│   ├── skills/                # 30 canonical Antigravity skills
│   ├── desktop/               # agy-yolo desktop shortcuts & Dolphin service menus
│   ├── ogsr-port-tools/       # OGSR 64-bit porting & guardian daemon tools
│   ├── system-tweaks/         # Linux system tweaks
│   └── token_ledger.json      # Lifetime token savings ledger
├── docs/                      # Documentation
└── scripts/                   # Maintenance scripts
```

## Adding or Exporting Skills
1. Create `config/skills/<name>/SKILL.md` (and optional `scripts/`).
2. Run `./install.sh --all` to deploy to `~/.gemini/config/skills/`.
3. To export to other platforms, run `export-skills --target cursor` or `export-skills --target agents`.

---

## 📄 License
MIT License. Free to use, adapt, and distribute for autonomous agent engineering.

## Local AI models: NVIDIA Nemotron in the fleet (2026-10-18)
Tested against the existing local models with validated tasks (`tools/model_eval.py`, `tools/model_eval_hard.py`; results in `docs/learn/`, decisions in `docs/NVIDIA_MODELS.md`). Quality first, speed only as a tie-break.
- **yasserrmd/OpenReasoning-Nemotron:7b** (NVIDIA, 4.4 GB): math, science and reasoning. Scored 6/6 on the maths tests; **replaced wizard-math and mathstral** (4/6, 3/6).
- **nemotron-3-nano:4b** (NVIDIA, 2.8 GB): fast reasoning, agent/tool use, second opinion for code. **Replaced deepseek-r1:8b** (better maths, equal code, 8x faster).
- **minicpm-v:8b** (vision) matched NVIDIA nemotron-3.5-bolt (24 GB) at 15x the speed, so bolt, llava:13b and moondream were removed.
- **gpt-oss:20b** (OpenAI, MXFP4 weights native to RTX 50 cards) is the main general/reasoning/maths/Blender model and **qwen3-coder:30b** the fast code model; they replaced about 25 larger or weaker models after side-by-side tests (docs/NVIDIA_MODELS.md in the port project).
- **NVIDIA Parakeet** (speech to text, `tools/stt.py`) replaces Whisper as the default; faster-whisper is the fallback. Not on Ollama: NVIDIA Magpie TTS (voice cloning), OpenMath, NV-Embed.
- Used by: `local-worker` (candidate lists), `local-coprocessor`, the fleet setup/verify scripts and the model skills. VRAM/CPU sharing with a running game: `tools/llmrun.py`.

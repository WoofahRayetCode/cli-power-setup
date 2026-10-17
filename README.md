# CLI Power Setup (`cli-power-setup`)

[![Active Skills](https://img.shields.io/badge/Skills-314%20Active-brightgreen.svg)](#-categorized-skills-directory-314-skills)
[![Local Fleet](https://img.shields.io/badge/Local%20Fleet-31%20Models%20(Ollama)-blue.svg)](#-zero-quota-local-language-model-fleet-31-models-0-cloud-tokens)
[![Fleet Disk Size](https://img.shields.io/badge/Fleet%20Disk%20Size-198%20GB%20(31%20Models)-blueviolet.svg)](#-zero-quota-local-language-model-fleet-31-models-0-cloud-tokens)
[![Secondary NVMe](https://img.shields.io/badge/Secondary%20NVMe-1.4%20TB%20Headroom%20(/mnt/games)-success.svg)](#-secondary-drive-ultra-large-model-repository--hardware-optimizer)
[![Hardware Offload](https://img.shields.io/badge/Hardware-32T%20CPU%20%2B%20RTX%205060%20CUDA-orange.svg)](#-zero-quota-local-language-model-fleet-31-models-0-cloud-tokens)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](#-license)

A production-grade, quota-optimized engineering, 3D modeling, and game engine porting suite for **Google Antigravity (`agy` — Gemini 4 Argon + Gemini 3.8 Flash Swarm)** and **Cursor IDE** (featuring dedicated multi-model behavioral adaptation for **Gemini 4 Argon/Flash**, **xAI Grok**, **OpenAI GPT/o1/o3**, and **DeepSeek**), backed by **32-thread CPU + NVIDIA RTX 5060 CUDA/OptiX + 30 GB `/dev/shm` RAM-disk hardware offloading**.

This repository organizes **316 autonomous agent skills**, 316 modular Cursor rules (`.cursor/rules/*.mdc`), global engineering discipline rules, a 29-model zero-quota local LLM fleet, an Omni-Auto dynamic routing engine, a floating voice dictation pill (`agy-mic-button`), and a live multi-row telemetry statusline (`agy-quota-statusline`).

---

## 🧭 Quick Navigation

Jump directly to any section of the documentation:

* [⚡ Quick Start & Installation](#-quick-start)
* [🧠 Zero-Quota Local Language Model Fleet (31 Models)](#-zero-quota-local-language-model-fleet-31-models-0-cloud-tokens)
  * [Key Benefits & Token Savings](#-key-benefits--overall-usage-savings)
  * [Local Fleet Matrix (Collapsible Table)](#-complete-31-model-local-fleet-matrix)
  * [Secondary Drive Ultra-Large Model Repository (`ultra-model-manager`)](#-secondary-drive-ultra-large-model-repository--hardware-optimizer)
* [🚀 Dynamic AGY Omni-Auto Mode (`agy-omni-mode`)](#-dynamic-agy-omni-auto-mode-agy-omni-mode)
* [🔎 Zero-Quota Local Research Scout (`local-research-scout`)](#-zero-quota-local-research-scout-local-research-scout)
* [🛠️ CLI Power Tools & Launchers](#️-cli-power-tools--launchers)
* [🎯 Division of Labor: `agy` CLI vs. Cursor IDE](#-division-of-labor-agy-cli-vs-cursor-ide)
* [🧩 Categorized Skills Directory (314 Skills Dropdowns)](#-categorized-skills-directory-314-skills)
  * [1. Cognitive Reasoning, Quota Governance & Token Containment](#1-cognitive-reasoning-quota-governance--token-containment)
  * [2. Game Engine Architecture, Porting & Diagnostics](#2-game-engine-architecture-porting--diagnostics)
  * [3. 3D Assets, Headless Blender 5.2+ & Audio DSP](#3-3d-assets-headless-blender-52--audio-dsp)
  * [4. Systems Engineering, C++, Rust, CMake & Packaging](#4-systems-engineering-c-rust-cmake--packaging)
  * [5. Cyber Security, Anti-Tamper, RE & Cryptography](#5-cyber-security-anti-tamper-re--cryptography)
  * [6. Mobile Android & Handheld Linux Engineering](#6-mobile-android--handheld-linux-engineering)
  * [7. Modern Web Architecture, Full-Stack & UI/UX](#7-modern-web-architecture-full-stack--uiux)
  * [8. Machine Vision, OCR & Visual Intelligence](#8-machine-vision-ocr--visual-intelligence)
  * [9. Automated Testing, QA & Mutation Fuzzing](#9-automated-testing-qa--mutation-fuzzing)
  * [10. Frontier AI, Subagent Swarms & Multi-Model Parity](#10-frontier-ai-subagent-swarms--multi-model-parity)
  * [11. DevOps, Docker, CI/CD & Documentation](#11-devops-docker-cicd--documentation)
* [📊 Real-Time Dual-CLI Quota & Statusline Monitors](#-real-time-dual-cli-quota--statusline-monitors)
* [🛡️ Ultimate Hardening Protocols & Zero-Token Pre-Flight](#️-ultimate-hardening-protocols--zero-token-host-pre-flight)
* [📱 Android 2D & 3D Game & App Workflows](#-android-2d--3d-game--app-development-workflows)
* [📂 Repository Structure](#-repository-structure)
* [🔄 Auto-Synchronized Catalog](#-auto-synchronized-skill--cli-inventory-314-total-active-skills)

---

## ⚡ Quick Start

Clone this repository and run the interactive setup:

```bash
git clone https://github.com/WoofahRayetCode/cli-power-setup.git
cd cli-power-setup
./install.sh
```

### 📋 Interactive Installer Menu
Running `./install.sh` displays an interactive target menu:
```text
CLI Power Setup Installer
Select target environment:
  1) Full Setup (Antigravity & Cursor) [Recommended]
  2) Antigravity only (~/.gemini)
  3) Cursor only (~/.cursor, ~/.cursorrules)
  4) Exit
```

Or pass flags non-interactively in automated scripts:
```bash
./install.sh --all     # Install for Google Antigravity and Cursor IDE
./install.sh --agy     # Install for Google Antigravity only
./install.sh --cursor  # Install for Cursor IDE only
```

### What the Installer Does:
1. **Safety Backup:** Automatically archives existing configurations to `~/.cli_power_setup_backups/`.
2. **Environment Sync:** Deploys all 316 skills to `~/.gemini/config/skills/` and converts them into Cursor `.mdc` rules in `~/.cursor/rules/`.
3. **Global Discipline & Voice Command Routing:** Installs engineering safeguards, Quota Governance, the **Output Token Economy**, Zero-Quota Local CPU/GPU Math Offload rules, and Natural-Language Spoken Command Routing (*"Set a goal..."*, *"Make a plan..."*, *"Use boost..."*) to `~/.gemini/config/GEMINI.md` and `~/.cursorrules`.
4. **Live Multi-Row Telemetry Statusline (`agy-quota-statusline`):** Tracks real-time 5h/weekly quota, 250k compaction gate countdown (`🧹`), active skills in real time (`🛠️ Skills [Live]`), CPU/GPU temperatures & fan RPM (`🌡️`), lid-closed lock state (`🔒Lid-Safe`), RTX 5060 VRAM & `/dev/shm` RAM-disk usage (`🚀`), and active background workloads (`⚙️ 🎨Blender+🔨Build+🎮OGSR/Wine`).
5. **Floating Voice Dictation Pill (`agy-mic-button`):** Launches a draggable, pinnable (`📌`/`📍`) floating `[🎙️ Talk | ⏎ Send | ⚡Auto | 📌Pin]` overlay that triggers `/voice` (`F5`) without keyboard shortcuts and auto-closes when `agy` exits.
6. **Launchers & Self-Optimizing Ecosystem Tools:** Installs `agy-yolo`, `agy-turbo`, `agy-omni-mode`, `local-research-scout`, `game-math-solver`, `skill-evolve`, `skill-optimize`, `laptop-perf`, `repo-auto-sync`, and `setup-local-model-fleet` into `~/.local/bin/`.

---

## 🧠 Zero-Quota Local Language Model Fleet (29 Models, 0 Cloud Tokens)

A production-grade fleet of **29 specialized open-weights models**—including **state-of-the-art Mixture-of-Experts (MoE)** and **heavyweight 14B–32B frontier planners**—running locally on your laptop via Ollama with automated **hybrid NVIDIA RTX 5060 GDDR7 VRAM + 32-thread DDR5 RAM layer offloading**.

> [!IMPORTANT]
> **💾 Total Storage Footprint: `166 GB`** physical disk consumption across all 29 models on NVMe SSD (`/var/lib/ollama/blobs/`), with **`523 GB` free headroom** remaining (46% disk used of 950 GB). Deduplicated GGUF layers are shared between model variants to minimize drive wear.

### 🌟 Key Benefits & Overall Usage Savings

1. **Zero Cloud Token Incurrence (100% Free Inference):**
   - Routine code edits, docstrings, regex, commit messages, and unit test generation are dispatched to local SLMs (`qwen2.5-coder:1.5b`, `llama3.2:3b`), billing **0 cloud tokens**.
   - Preserves 100% of rolling 5-hour and weekly Gemini 4 Argon / Claude 3.7 Sonnet quota for hard architectural reasoning.

2. **Hierarchical "Local Brain $\rightarrow$ Local Hands" Workflow:**
   - **Offline Frontier Planning:** Heavyweight models (`qwen2.5-coder:32b`, `deepseek-r1:32b`, `deepseek-coder-v2:16b`) decompose complex tasks, verify math constraints, and formulate implementation roadmaps locally.
   - **Sub-Second Execution:** Fast local workers execute the plan in milliseconds, allowing `agy` to operate autonomously without cloud rate limits.

3. **Game Engine Porting & Systems Modernization (#1 MoE Engine):**
   - **`deepseek-coder-v2:16b`** (16B total, only **2.4B active compute** per token) brings 338-language coverage, 64-bit pointer sanitization, and DirectX 9/11 HLSL to Vulkan SPIR-V shader transpilation at near-instant GPU speeds.

4. **Hardware Saturation (Zero Waste on Local Rig):**
   - **RTX 5060 GDDR7 VRAM:** Accelerates memory-bandwidth-bound attention layers.
   - **32-Thread AMD CPU + 30.4 GB DDR5 RAM:** Computes remaining MLP layers in parallel via AVX2 / AVX-512 without OOM crashes.
   - **Quantized KV-Cache (`q4_0` / `q8_0`):** Shrinks context memory by 50–75%, unlocking 32k–128k context windows locally.

5. **Complete Air-Gapped Privacy & Offline Autonomy:**
   - Proprietary game source code, closed-source reverse-engineering disassembly, and sensitive client documents never leave your physical machine.

### 📋 Complete 31-Model Local Fleet Matrix

<details>
<summary><b>🔍 Click to View Complete 31-Model Local Fleet Specifications & Memory Footprint</b></summary>

| Functional Tier | Primary Model | Fallback | Memory | Specialization & Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **`ultra-large`** | **`deepseek-r1:70b-iq2`** | `llm4decompile:22b-q4` | ~19.1–22.4 GB VRAM+RAM | **Titan 70B Deep Reasoning.** Secondary NVMe storage (`/mnt/games`), 18-layer VRAM offload (`--task reason`) |
| **`decompile-re`** | **`llm4decompile:22b-q4`** | `deepseek-coder-v2:16b` | ~12.4 GB VRAM+RAM | **Binary Reverse Engineering.** Assembly-to-C decompilation for REA MCP & Ghidra (`--task re`) |
| **`engine-porting`** | **`deepseek-coder-v2:16b`** | `qwen2.5-coder:32b` | ~6.0 GB VRAM + RAM | **#1 Game Engine Porting.** 32-to-64-bit pointer math, struct alignment, HLSL/GLSL shaders (`--task port`) |
| **`frontier-planners`** | **`qwen2.5-coder:32b`** | `deepseek-r1:32b` | ~7.5 GB VRAM + RAM | **Heavyweight 32B Code Planner.** SWE-bench leader, large refactors, C++20 modernizations (`--task plan`) |
| **`reasoning`** | **`deepseek-r1:32b`** | `deepseek-r1:14b` / `8b` | ~5.2–7.5 GB VRAM | **32B Deep Chain-of-Thought.** Architectural verification, invariant proofs, root-cause triage (`--task reason`) |
| **`generalist`** | **`qwen2.5:32b`** | `mistral-nemo:12b` | ~7.1–7.5 GB VRAM | **32B Large Context Generalist.** Repo analysis, modern web architectures, enterprise copy (`--task long`) |
| **`mid-code`** | **`qwen2.5-coder:14b`** | `qwen2.5-coder:7b` | ~4.7–7.0 GB VRAM | **14B Dense Code Architect.** Multi-file dependency tracking and C++20 modernizations (`--task code`) |
| **`stem-math`** | **`mathstral:7b`** | `wizard-math:7b` / `phi4` | ~4.1 GB VRAM | Physics ODEs, Open Dynamics Engine (ODE) ERP/CFM stability, quaternion SLERP (`--task math`) |
| **`dialogue-i18n`** | **`aya:8b`** | `qwen2.5:7b` | ~4.8 GB VRAM | Cohere 101-language translation, Slavic/CJK/FIGS game dialogue trees, XML repair (`--task translate`) |
| **`web-frontend`** | **`qwen2.5:7b`** | `gemma2:9b` | ~4.7 GB VRAM | Modern Tailwind CSS card grids, responsive UI components, semantic HTML (`--task web`) |
| **`business-copy`** | **`gemma2:9b`** | `qwen2.5:7b` | ~5.4 GB VRAM | Google Gemma 2 anti-jargon business copy, BLUF proposals, SOWs (`--task business`) |
| **`database-sql`** | **`sqlcoder:7b`** | `granite-code:8b` | ~4.1 GB VRAM | Defog SQLCoder state-of-the-art DDL schema design & SQLite WAL optimization (`--task sql`) |
| **`agentic-tools`** | **`hermes3:8b`** | `llama3.1:8b` | ~4.7 GB VRAM | Agentic function calling, tool use, strict JSON schema adherence (`--task tool`) |
| **`fast-boilerplate`**| **`qwen2.5-coder:1.5b`**| `llama3.2:3b` | ~1.0 GB VRAM | Sub-second regex, docstrings, commit messages, and unit test boilerplate (`--task fast`) |
| **`vision-ocr`** | **`minicpm-v:8b`** | `moondream:latest` | ~5.5 GB VRAM | Multimodal UI and HUD visual inspection, screen diffing, and local OCR (`--task vision`) |
| **`embeddings`** | **`bge-m3:latest`** | `nomic-embed-text` | ~1.2 GB VRAM | 8192-token dense multilingual vector embeddings for zero-quota local RAG |
| **`blender-3d`** | **`blender-architect:latest`** | `qwen2.5-coder:7b` | ~4.7 GB VRAM | Custom Modelfile fused with Blender 5.2 API & organic SDF voxel remeshing rules (`--task blender`) |

</details>

### 🛠️ Fleet Management & Local Coprocessor CLI
```bash
# Display live fleet status, hardware telemetry & disk usage
setup-local-model-fleet --status

# Synchronize specific functional tiers or all 29 models
setup-local-model-fleet --tier engine-porting    # Game engine migration models
setup-local-model-fleet --tier frontier-planners # 14B-32B offline planners
setup-local-model-fleet --all                   # Complete 29-model fleet

# Execute tasks locally (0 cloud tokens billed)
local-coprocessor generate --task port --prompt "Audit this C++ class for 64-bit pointer truncation"
local-coprocessor generate --task plan --prompt "Decompose game engine porting into 5 atomic steps"
local-coprocessor generate --task math --prompt "Derive critically damped spring update for fixed_step=0.01"
```

### 🚀 Secondary Drive Ultra-Large Model Repository & Hardware Optimizer (`ultra-model-manager`)

Dedicated storage and hardware-layer split manager for **70B–405B parameter models** stored directly on the secondary high-speed NVMe drive (`/mnt/games/large-models/` with **1.35 TB free headroom**), completely isolating large weights from the root operating system drive:

* **Hardware Optimization:** Every model is calibrated with importance-matrix (`IQ2_XXS` / `Q4_K_M`) quantization, 32-thread AMD Zen AVX-512 CPU execution, and automated GDDR7 VRAM layer offloading to the NVIDIA RTX 5060 (leaving safe headroom for desktop rendering and quantized `q4_0` KV cache).
* **Automated Parallel Downloader:** Leverages `aria2c` with 16 parallel connections to download ultra-large weights at over **220 MB/s** (~1.8 Gbps) with segmented resumption and SHA-256 integrity validation.

```bash
# Display repository status, stored GGUF files, and secondary drive headroom
ultra-model-manager status

# Download and register DeepSeek-R1 70B (IQ2_XXS) on secondary storage
ultra-model-manager download deepseek-r1-70b --optimize

# Download and register LLM4Decompile 22B for assembly-to-C reverse engineering
ultra-model-manager download llm4decompile-22b --optimize

# Download and register Qwen 2.5 72B for dense systems architecture and C++ porting
ultra-model-manager download qwen-72b-instruct --optimize

# Run an interactive prompt with any ultra-large model
ultra-model-manager run deepseek-r1-70b --prompt "Verify 64-bit struct padding for X-Ray vertex buffer"
```

---

## 🚀 Dynamic AGY Omni-Auto Mode (`agy-omni-mode`)

The **Omni-Auto Mode** dynamically evaluates every user instruction, workflow lifecycle step, git dirty file types, and rolling 5-hour quota headroom to automatically switch between cloud Gemini models and local Ollama models with zero token waste:

### Step Lifecycle Routing Matrix

| Workflow Lifecycle Step | Engine Target | Model Dispatched | Reasoning / Tool | Cloud Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Intake & Scanning** | Host Local CPU | `local-ast-compiler` / `slice-reader` | AST Symbol Indexing | **0 tokens** |
| **Internet & Web Research** | Host Local Ollama | `local-research-scout` (`deepseek-coder-v2:16b` + `bge-m3`) | Multi-Source RAG Search | **0 tokens** |
| **Architecture & Planning** | Cloud Pro / Local | `gemini-4-pro` (or local `deepseek-r1:32b` if quota < 40%) | `--effort high` | Minimal |
| **Code Generation & Porting**| Local / Cloud Flash | `deepseek-coder-v2:16b` / `qwen2.5-coder:32b` / `flash` | `--effort low` | **0 to minimal** |
| **Math & Physics Derivations**| Host Local RTX 5060 | `mathstral:7b` / `phi4:14b` / `game-math-solver` | CUDA 13.4 / AVX-512 | **0 tokens** |
| **Verification & Testing** | Host CPU/GPU | `pytest` / `cargo test` / `local-preflight-syntax-gate` | Native execution | **0 tokens** |
| **Summarization & Commits** | Host Local Ollama | `mistral-nemo:12b` / `llama3.2:3b` | `local-coprocessor` | **0 tokens** |

```bash
# Evaluate active workspace domain and optimal engine routing
agy-omni-mode

# Evaluate specific prompt with routing rationale
agy-omni-mode "port legacy blenders to DX11 hlsl"

# Auto-execute on local engine if Tier 0
agy-omni-mode --exec "calculate quaternion slerp for camera trajectory"
```

---

## 🔎 Zero-Quota Local Research Scout (`local-research-scout`)

Autonomous multi-source web searching and technical RAG without cloud API keys or token billing:
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

---

## 🛠️ CLI Power Tools & Launchers

A dedicated suite of executable utilities installed directly into `~/.local/bin/` to automate every aspect of autonomous coding, quota monitoring, and local hardware acceleration:

| Utility | Category | Purpose |
| :--- | :--- | :--- |
| **`agy-omni-mode`** | Dynamic Routing | Autonomous model & fleet switcher between Cloud Gemini and local Ollama models. |
| **`local-research-scout`**| Research / RAG | Zero-quota multi-source search (DDG, GitHub, StackOverflow) + `bge-m3` RAG synthesis. |
| **`agy-quota-statusline`**| Telemetry | Live multi-row quota, skills, thermal, VRAM, and git statusline. |
| **`agy-mic-button`** | Voice / Input | Floating draggable & snap-pinnable voice dictation pill for hands-free coding. |
| **`agy-yolo` / `yolo`** | Autonomous | High-autonomy runner for hands-free goal execution (Argon Brain + Flash Hands). |
| **`agy-turbo`** | Speed | Instant turnaround low-effort Gemini 3.8 Flash runner for routine tasks. |
| **`game-math-solver`** | Hardware Math | 32-thread CPU + RTX 5060 CUDA solver for quaternions, ODEs, and ballistics (0 tokens). |
| **`local-coprocessor`** | Offline AI | Task dispatcher to local Ollama fleet (`port`, `plan`, `code`, `math`, `sql`, `web`). |
| **`setup-local-model-fleet`**| Fleet Manager | Local model fleet installer, tier synchronizer, and storage inspector. |
| **`ultra-model-manager`** | Ultra-Large AI | Downloader, hardware layer-offload tuner, and Ollama registrar on secondary NVMe. |
| **`model-quant-optimizer`** | Ultra-Large AI | Hardware budget planner, imatrix (IQ2/IQ3) and AirLLM runner for 70B-405B models. |
| **`gemini-reasoning-tuner`**| Quota / Tuning | Real-time reasoning effort and model tier calibrator for Google Antigravity. |
| **`laptop-perf`** | Hardware | OMEN thermal governor (`clamshell-3d` lid-closed render lock, `sleep-mode`, `boost-exec`). |
| **`repo-auto-sync`** | Git Automation | Autonomous git sync, milestone committer, `.gitignore` hardener, and push manager. |
| **`skill-evolve`** | Skill Evolution | Closed-loop runtime skill synthesizer, script promoter, and hot-patcher. |
| **`slice-reader`** | Context Guard | Surgical line-slice reader and AST skeleton extractor (slashes input tokens by 95%). |
| **`token-guard`** | Context Guard | Intercepts noisy shell output, enforcing hard 30-line ceilings to prevent context floods. |
| **`voice-prompt-optimizer`**| Voice / Context | Cleans conversational filler, normalizes phonetic jargon (C++, OGSR, LTX), saves 50–85% tokens. |

---

## 🎯 Division of Labor: `agy` CLI vs. Cursor IDE

While all 316 skills and CLI utilities are shared across environments, they divide into distinct operational sweet spots:

### 1. Skills That Excel in `agy` CLI (Headless, Voice-Driven & Unattended)
*Best launched via `agy-yolo`, `agy-turbo`, or spoken *"Set a goal..."* via `agy-mic-button`*

* **Autonomous Long-Running Goals & Porting Swarms:** `stalker-ogsr-migration`, `autonomous-goal-governor`, `argon-dynamic-subagent-swarm`. Gemini 4 Argon (`High`) orchestrates architecture while dispatching parallel Gemini 3.8 Flash worker subagents for 85%+ quota savings.
* **Lid-Closed Clamshell 3D Rendering & Baking:** `laptop-performance-profile` (`laptop-perf clamshell-3d`), `rtx-optix-gpu-baker-denoiser`, `ramdisk-tmpfs-build-bake-accelerator`. Blocks systemd lid-suspend while capping CPU boost so headless Blender 5.2+ OptiX GPU renders run safely while you sleep.
* **Zero-Quota Local CPU/GPU Math & Asset Offloading:** `game-3d-linear-algebra-quaternions`, `computational-geometry-mesh-bvh-math`, `physics-ballistics-ode-numerical-math`, `pbr-radiometry-color-dsp-math` (`game-math-solver` on 32-thread AVX-512 CPU + RTX 5060 CUDA 13.4).
* **Game QA & System Watchdogs:** `game-qa-playtest-controller`, `game-test-watchdog`, `stalker-playtest-runner`. Direct access to `/dev/uinput` input injection, headless Wine/Proton processes, and X-Ray crash log window dismissals.

### 2. Skills That Excel in Cursor IDE (Interactive & Visual)
*Best used via Cursor Agent or Composer*

* **Web, UI & Data Visualization:** `creative-web-design-archetypes`, `human-crafted-web-design`, `interactive-data-visualization-web`, `generative_ui`.
* **Side-by-Side Code Review & Triage:** `coderabbit-ai-review`, `canvas-interactive-workspace`.

| Workflow | Recommended Tool | Model & Hardware Routing |
| :--- | :--- | :--- |
| **Overnight engine porting, 3D baking & autonomous QA** | **`agy-yolo`** | **Gemini 4 Argon (High) + Flash Swarm** |
| **Routine edits, repository sync & quick commands** | **`agy-turbo`** | **Gemini 3.8 Flash (Low Effort)** |
| **3D coordinates, ODE physics, ballistics & symbolic proofs** | **`game-math-solver`** | **Local 32-Thread CPU + RTX 5060 CUDA (`0` tokens)** |
| **Interactive UI styling, websites & visual apps** | **Cursor IDE** | **Grok 4.7 / Gemini / o3-mini** |

---

## 🧩 Categorized Skills Directory (314 Skills)

The full collection of 314 skills is organized into 11 functional domains. Click any category below to expand its skills and capabilities:

<details>
<summary><b>🧠 1. Cognitive Reasoning, Quota Governance & Token Containment (38 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`adaptive-reasoning`** | Heuristic reasoning effort selection between Flash and Argon based on cognitive complexity. |
| **`superpowers`** | Core engineering discipline engine, TDD enforcement, and workflow router. |
| **`writing-plans`** | Granular, dependency-ordered, machine-verifiable task lists for complex refactors. |
| **`executing-plans`** | Safe plan execution with test-gated checkpoints and rollback guarantees. |
| **`brainstorming`** | Requirements discovery, design exploration, and architectural trade-off analysis. |
| **`systematic-debugging`** | Root-cause hypothesis testing via engine logs, stack traces, and reproducible test cases. |
| **`test-driven-development`**| Strict Red-Green-Refactor cycle before implementation. |
| **`verification-before-completion`**| Final quality gate collecting concrete execution evidence before declaring tasks done. |
| **`argon-thinking-governor`**| Clamps internal reasoning tokens during routine tool calls; enforces Flash dispatch. |
| **`gemini-dynamic-reasoning-tuner`**| Real-time reasoning effort governor turn-by-turn based on rolling quota headroom. |
| **`gemini-5h-quota-governor`**| Telemetry governor for rolling 5-hour quota windows, pacing autonomous runs. |
| **`gemini-flash-cache-aligner`**| Maximizes Flash prompt caching discounts (>90%) through prefix stabilization. |
| **`gemini-implicit-kv-cache-ttl-keeper`**| Prevents uncached input token spikes during long playtests and C++ builds. |
| **`gemini-ast-symbol-window-slicer`**| Enforces bounded 40–80 line window slicing on `view_file` to save 85% tokens. |
| **`gemini-copy-then-patch-edit-governor`**| Forbids full-file regeneration; enforces `cp` + surgical `replace_file_content`. |
| **`token-economy`** | Output token optimization, zero conversational fluff, and high-density status. |
| **`token-guard`** | Terminal command line ceiling protector, intercepting runaway stdout dumps. |
| **`slice-reader`** | Surgical line-slice reader and AST skeleton extractor. |
| **`prompt-cache-context-optimizer`**| Emulates 1M+ context window and locks in 90%+ Anthropic prompt caching discounts. |
| **`context-pruning-watchdog`**| Live telemetry monitoring of active context consumption and lossless compaction. |
| **`context-window-governor`**| Deterministic token budgeting, turn partitioning, and hard output containment. |
| **`working-memory-checkpointing`**| Atomic snapshotting and 1-command rollback of dirty diffs and active hypotheses. |
| **`first-principles-reasoning`**| First-principles decomposition, Chain-of-Verification (CoVe), and Ockham's razor. |
| **`task-velocity-governor`**| Enforces task completion velocity, 5-step targeted rule, and anti-thrashing bounds. |
| **`deliberative-reasoning-tree`**| Tree-of-Thought (ToT) 3-path branching, adversarial self-critique, and backtracking. |
| **`argon-adversarial-verification-gate`**| Deep reasoning adversarial critique and boundary-condition proofing. |
| **`argon-ast-syntax-gate`**| Pre-flight local compiler and AST syntax verification gate in milliseconds. |
| **`argon-atomic-diff-sequencer`**| Restricts all code changes to surgical <=30 line replacements. |
| **`argon-context-cache-guard`**| Anchors context to cross and maintain the 32,768-token cache threshold. |
| **`argon-effort-auto-calibrator`**| Dynamically scales Argon thinking effort (--effort low/med/high) turn-by-turn. |
| **`argon-long-context-retrieval-anchor`**| Semantic anchoring across 1M context to prevent lost-in-the-middle degradation. |
| **`argon-long-haul-context-compaction-gate`**| Milestone compaction at 250k tokens to maintain sub-second latency. |
| **`fable-virtual-context-manager`**| Virtualizes 1M-token context by paging 30k subsystem slices into memory. |
| **`claude-opus-conciseness-enforcer`**| Enforces <=200 token outputs, strict BLUF, saving up to 75% output tokens. |
| **`claude-context-rot-shield`**| Enforces 80k-token milestone compaction boundaries and cache block alignment. |
| **`claude-thinking-budget-governor`**| Extended thinking token budget governor for Claude 3.7+ Sonnet/Opus. |
| **`autonomous-goal-governor`**| Quota governance, machine-verifiable contracts, and 3-strike circuit breaker. |
| **`universal-token-containment-protocol`**| Enforces zero code repetition, artifact offloading, and strict tool caps. |

</details>

<details>
<summary><b>🎮 2. Game Engine Architecture, Porting & Diagnostics (45 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`game-engine-migration`** | Universal 5-stage engine & mod porting framework (32-to-64 bit, DX9 to DX11/Vulkan). |
| **`stalker-ogsr-migration`** | 32-bit S.T.A.L.K.E.R. mod porting to 64-bit OGSR Engine. |
| **`stalker2-to-ogsr-asset-transpiler`**| Converts S.T.A.L.K.E.R. 2 UE5 IoStore assets into 64-bit OGSR/X-Ray formats. |
| **`ue5-foliage-mesh-to-ogsr-transpiler`**| Extracts UE5 3D foliage and transpiles to OGSR .ogf and .dm formats. |
| **`ue5-redengine-rage-library-modding`**| Modding workflows for UE5 IoStore, Rockstar GTA/RAGE, CDPR REDengine. |
| **`bethesda-creation-engine-nif-modding`**| Skyrim/Fallout/Starfield ESM/ESP plugins, BA2 archives, NIF meshes, SKSE. |
| **`source-idtech-kex-engine-modding`**| Valve Source/Source 2, GoldSrc, id Tech, and Nightdive KEX Engine modding. |
| **`cpp-64bit-engine-port-sanitizer`**| Detects and repairs 64-bit pointer truncation and alignment faults in C++ engines. |
| **`argon-deep-memory-allocator-sanitizer`**| 64-bit pointer, struct padding, and alignment sanitizer for legacy C++ engines. |
| **`godot-game-dev`** | Godot 4.x development, GDScript 2.0 static typing, and headless GUT tests. |
| **`godot-shader-vfx`** | Godot 4 spatial/canvas shaders, vertex wind displacement, and GPU particles. |
| **`unreal-engine-dev`** | Unreal Engine 5 C++, Gameplay Framework, UObject memory management. |
| **`unity-game-dev`** | Unity C#, zero-allocation Span/Memory, ScriptableObjects, UI Toolkit. |
| **`gamemaker-gml-engineering`** | Modern GameMaker (2024+), constructors, structs, FSMs, volatile surfaces. |
| **`game-modding`** | S.T.A.L.K.E.R. EE ZoneForge toolchain, LTX syntax, and engine-safe audio. |
| **`xray-lua-scripting`** | S.T.A.L.K.E.R. X-Ray Engine Lua callbacks, memory safety, and quest scripting. |
| **`stalker-level-ai-graph-triage`**| Cross-level AI spawn graph repair, node traversal, and patrol path alignment. |
| **`stalker-luajit-ffi-migration`**| Migrates legacy Luabind script bindings to high-performance LuaJIT FFI. |
| **`stalker-spawn-entity-indexer`**| Indexes 40k+ line all.spawn into queryable JSON maps for precise entity slicing. |
| **`xray-crash-log-diagnostician`**| Triages X-Ray / OGSR engine crashes and Wine/Proton stack traces to source lines. |
| **`xray-crash-interceptor-daemon`**| Background sweep daemon intercepting Wine/Proton crash modals (BugTrap/Notepad). |
| **`xray-crash-symbol-resolver`**| Translates Wine/Proton crash offsets to exact source lines via addr2line/rizin. |
| **`xray-macro-boilerplate-condenser`**| Condenses legacy GSC macros (IC, Luabind) into semantic C++ signatures. |
| **`game-runtime-diagnostics`** | Cross-platform PC & Steam Deck game crash troubleshooting (Proton, DXVK, TDRs). |
| **`dxvk-vkd3d-proton-pipeline-profiler`**| Diagnoses and eliminates DXVK and VKD3D shader compilation stutter and VRAM stalls. |
| **`dx11-dx12-vulkan-rtx-bridge`**| Zero-copy DX11 to DX12/Vulkan ray-tracing sidecar and DLSS 3/4 Frame Generation. |
| **`nvidia-rtx-dlss-rr-nrd-streamline`**| NVIDIA RTX NGX & Streamline SDK, DLSS 4 Transformer, Ray Reconstruction. |
| **`rtx-compute-bvh-raytracing-ssgi`**| Real-time Ray-Traced Global Illumination (SSGI/SDFGI) in DX11/DX12/Vulkan. |
| **`game-audio-engine-engineering`**| Lock-free audio callbacks, 3D HRTF spatialization, and dynamic ducking. |
| **`game-physics-collision-pipeline`**| Fixed-timestep accumulator loops, state interpolation, and BVH broadphase. |
| **`game-memory-allocator-engineering`**| Linear Arenas, Stack LIFO rollback, Pool free lists, and TLSF alignment. |
| **`game-input-system-abstraction`**| Scaled radial deadzones, sub-pixel mouse smoothing, controller glyph switching. |
| **`game-asset-pack-archive-engineering`**| Virtual File System mount hierarchy, high-performance VPAK containers, zlib mmap. |
| **`game-entity-component-system`**| Archetype & Sparse-Set data layouts, SoA memory alignment, and DAG scheduling. |
| **`game-animation-skeletal-pipeline`**| TRS bone hierarchies, quaternion SLERP/NLERP, and FABRIK/Two-Bone IK. |
| **`game-networking-state-sync`**| Client-side input prediction, server reconciliation, and delta snapshots. |
| **`game-save-state-serialization`**| Endian-safe binary containers, versioned schema migrations, and CRC32 checks. |
| **`game-debug-ui-tools`** | In-engine Dear ImGui integration, immediate 3D DebugDraw, runtime CVars. |
| **`game-weather-lighting-fx`** | Dynamic weather cycles, HDR tonemapping, sun shafts, and glare suppression. |
| **`game-performance-overlay-telemetry`**| MangoHud, DXVK HUD, FPS, 1% lows, GPU/VRAM/power stats, top-right positioning. |
| **`game-weapon-ballistics-mechanics`**| Weapon LTX configs, ballistics physics, projectile radii, anti-jamming. |
| **`game-qol-gameplay-scripting`** | Proximity item radar, auto-loot, faction defense, and sprint anomaly immunity. |
| **`game-autonomous-navigation-ai`**| Autonomous waypoint navigation, route smoothing, and collision trap avoidance. |
| **`game-companion-pet-ai`** | Custom companion pet AI, dynamic torch light in dark, and homing missiles. |
| **`game-config-delta-extractor`**| Game configuration delta extractor and inheritance pruner (LTX, TSCN, YAML). |

</details>

<details>
<summary><b>🎨 3. 3D Assets, Headless Blender 5.2+ & Audio DSP (28 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`blender-3d-engineering`** | High-efficiency headless Blender 5.2+ procedural geometry, modifiers, exports. |
| **`rtx-optix-gpu-baker-denoiser`**| Accelerates Cycles texture baking 10x–20x via RTX 5060 OptiX AI Denoising. |
| **`blender-sdf-organic-remeshing`**| Eliminates balloon-animal looks via Voxel SDF Remeshing and QuadriFlow. |
| **`blender-high-to-low-baking`**| Headless normal, AO, curvature/cavity, and material ID baking via bpy. |
| **`blender-pbr-texture-packager`**| PBR ORM channel packing, texel density enforcement, normal Y-inversion. |
| **`blender-uv-udim-lightmap-architect`**| Headless UV unwrapping (SLIM Minimum Stretch), Trim Sheets, UDIM arrays. |
| **`character-creature-anatomy-modeling`**| Organic biped/quadruped skeletal topology, concentric deformation loops. |
| **`rigging-weight-painting-pipeline`**| Armature bone budgets, automated weight normalization, 4-influence clamping. |
| **`blender-hard-surface-cad-weapons-props`**| Boolean + Bevel + Weighted Normals hard-surface weapons, vehicles, props. |
| **`blender-geometry-nodes-procedural-worlds`**| Spline generators (roads, cables, fences), Poisson-disk biome foliage scattering. |
| **`blender-animation-nla-retargeting-vat`**| NLA action baking, cyclic loop quaternion continuity, Vertex Animation Textures. |
| **`blender-gaussian-splatting-photogrammetry-cleanup`**| Cleans 3D Gaussian Splats (.ply), NeRF, and AI 3D meshes into game-ready PBR. |
| **`concept-art-sketch-to-3d-sculptor`**| Converts 2D concept art into 3D models with Silhouette IoU >= 0.80 verification. |
| **`cross-engine-3d-import-export-bridge`**| Unified Blender export matrix to UE5 (Nanite), Godot (.glb), Unity, and OGSR (.ogf). |
| **`xray-ogf-dm-blender-pipeline`**| Direct binary export of S.T.A.L.K.E.R. .ogf models and .dm flora from Blender 5.2+. |
| **`ai-3d-mesh-generation`** | AI text-to-3D and image-to-3D generation pipelines using Tripo3D API. |
| **`threejs-webgl-engineering`**| Interactive 3D WebGL/WebGPU development, GLTFLoader, OrbitControls, PBR. |
| **`audio-dsp-tuning`** | Studio headset EQ (AutoEq/Harman) & 6-stage broadcast voice chains. |
| **`game-audio-ogg-gsc-encoder`**| Ogg Vorbis encoding with proprietary GSC binary engine comment headers. |
| **`creature-sound-forge`** | CC0 animal audio masterer + Klatt mammalian vocal tract DSP synthesis. |
| **`creature-animal-bioacoustic-audio`**| Realistic animal/mutant vocalization combining field audio and glottal DSP. |
| **`sound-web-scout`** | Autonomous web audio researcher (Wikimedia/Archive) with SNR burst slicing. |
| **`eleven-studio`** | Character neural TTS, timbre cloning, STS voice conversion, GSC v3 Ogg headers. |
| **`elevenlabs-voice-cloning-sts-studio`**| Zero-shot instant voice cloning and speech-to-speech voice conversion. |
| **`elevenlabs-voice-isolator-dubbing-sfx`**| Studio voice isolation, AI cross-language game dubbing, and text-to-SFX. |
| **`voice-speech-audio-synthesis`**| Speech-to-text via Whisper, natural voice generation via Piper/Kokoro/TTS. |
| **`pbr-radiometry-color-dsp-math`**| Cook-Torrance GGX BRDF, sRGB/Linear colorimetry, ACES Filmic tonemapping. |
| **`blender-headless-token-shield`**| Prohibits raw vertex/mesh dumps in chat; enforces headless Python automation. |

</details>

<details>
<summary><b>⚙️ 4. Systems Engineering, C++, Rust, CMake & Packaging (32 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`modern-cpp-engineering`** | Modern C++20/C++23 standards, RAII, smart pointers, Concepts, CMake. |
| **`rust-engineering`** | Compiler-first Rust, lifetimes, borrow checker, zero-cost abstractions, Clippy. |
| **`python-engineering`** | Python 3.10+, strict Mypy type annotations, pytest suites, Ruff optimization. |
| **`csharp-dotnet-engineering`** | Modern C# and .NET 8/9, memory optimization with Span/Memory, async/await. |
| **`cmake-cross-platform`** | Target-centric modern CMake (3.25+), cross-compilation toolchains, CPack. |
| **`linux-systems-engineering`** | POSIX APIs, asynchronous I/O (epoll/io_uring), process/signal management. |
| **`win32-systems-engineering`** | Win32 API, Windows Registry, Windows Services (SCM), Named Pipes, SEH. |
| **`windows-app-engineering`** | WinUI 3, Windows App SDK, WPF (.NET 8/9), C#/WinRT component interop. |
| **`avalonia-cross-platform-dev`**| Cross-platform XAML GUI development with Avalonia UI (.NET 8/9), MVVM. |
| **`tauri-multiplatform-dev`** | Lightweight cross-platform desktop/mobile engineering (Tauri 2.0, Rust). |
| **`electron-desktop-dev`** | Electron desktop apps, IPC security, context isolation, preload scripts. |
| **`bash-posix-automation`** | Defensive Bash/POSIX shell engineering, signal exit traps, ShellCheck. |
| **`powershell-windows-automation`**| Modern PowerShell 7, advanced cmdlet design, CIM/WMI querying, P/Invoke. |
| **`linux-desktop-packaging`** | Flatpak manifests, AppImage bundling, XDG Base Directory, .desktop entries. |
| **`cachyos-arch-packaging`** | Arch/CachyOS PKGBUILD authoring, DKMS kernel module builds, systemd units. |
| **`linux-hardware-acpi`** | Linux kernel ACPI module development, DSDT/SSDT table analysis, hwmon sensors. |
| **`hardware-tool-engineering`**| Hardware management tools, system daemons, sensors, thermal controllers. |
| **`laptop-performance-profile`**| HP OMEN ACPI/WMI sysfs integration, whisper-quiet night runs, boost execution. |
| **`cuda-gpu-acceleration`** | NVIDIA CUDA 13.4 kernel development, nvcc compilation, Tensor Core math. |
| **`vulkan-gpu-compute`** | Cross-vendor GPU compute via Vulkan 1.3/1.4, SPIR-V shaders, headless GPGPU. |
| **`cross-engine-shader-transpiler`**| Universal shader authoring and transpilation using Slang and SPIRV-Cross. |
| **`shader-cross-compilation`** | HLSL/GLSL/SPIR-V translation, clip space mapping, std140/std430 layouts. |
| **`pc-cross-platform-graphics-api`**| Modern C++ graphics Hardware Abstraction Layer (HAL) for DX12, Vulkan, DX11. |
| **`real-time-rendering-pipeline`**| Frame graphs, transient memory aliasing, bindless descriptors, reversed-Z. |
| **`database-sql-engineering`** | SQLite performance tuning (WAL mode, PRAGMAs, indexing), PostgreSQL schema. |
| **`network-protocol-engineering`**| Packet inspection (tshark/tcpdump), Protobuf/FlatBuffers, Linux TUN/TAP. |
| **`network-packet-stream-condenser`**| Flattens verbose packet dissections into high-density 1-line TSV tuples. |
| **`sql-schema-query-condenser`**| Serializes verbose DDL migrations and EXPLAIN trees into compact type notation. |
| **`compiler-error-cascade-isolator`**| Filters compiler template cascades, isolating #1 root-cause failure coordinate. |
| **`time-travel-deterministic-replay-debug`**| Deterministic record-and-replay time-travel debugging using Mozilla rr and GDB. |
| **`windows-linux-cross-os-runtime-bridge`**| Cross-platform runtime bridge between Windows 10/11 and Linux (Arch/CachyOS). |
| **`steamcmd-workshop-pipeline`**| SteamCMD and Steam Workshop publishing pipeline and VDF manifests. |

</details>

<details>
<summary><b>🛡️ 5. Cyber Security, Anti-Tamper, RE & Cryptography (22 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`reverse-engineer-anything`** | Deep multi-target reverse engineering with REA MCP server integration. |
| **`binary-re-workflows`** | Orchestrates Ghidra, JADX, TShark, objdump, and hex diffing workflows. |
| **`standalone-binary-re`** | Zero-MCP CLI reverse engineering (`readelf`, `objdump`, `jadx`, `pefile`). |
| **`open-apk`** | Android APK, XAPK, DEX, and resource loader for JADX headless triage. |
| **`wakaru`** | Production JS bundle unpacker & decompiler (Webpack, Vite, Electron). |
| **`lowlevel-dll-internals`** | Windows PE/DLL internals, vtables, calling conventions, MinHook detours. |
| **`game-security-anti-tamper`** | Memory injection defense, DLL hijacking prevention, save file HMAC integrity. |
| **`client-memory-integrity-anticheat`**| Anti-debugging, memory scanner detection, XOR value obfuscation, heartbeat sync. |
| **`game-memory-scanner`** | Virtual memory inspection, iterative candidate filtering, AOB signature scans. |
| **`game-dll-proxy-generator`** | Automated proxy DLL generator (dinput8, dxgi, version) with export forwarding. |
| **`cryptographic-security-engineering`**| Ed25519 signatures, AES-256-GCM AEAD, HKDF key derivation, constant-time ops. |
| **`security-vulnerability-audit`**| Pre-commit secret scanning (gitleaks), SAST (semgrep), dependency audits. |
| **`devsecops-supply-chain-security`**| Binary compiler hardening (RELRO, Canaries, NX, PIE), SBOMs, supply-chain checks. |
| **`app-security-threat-modeling`**| STRIDE threat modeling, OWASP Top 10 mitigation, memory safety hardening. |
| **`api-network-security-hardening`**| TLS 1.3/certificate pinning, mTLS, token bucket rate limiting, CORS/CSP policies. |
| **`game-patching-binary-repair`**| PE import analysis, crash offset disassembly, missing DLL stubs, byte patching. |
| **`console-game-decompilation`**| PS1/PS2/PS3/Xbox matching decompilations, splat binary splitting, objdiff. |
| **`console-homebrew-engineering`**| Switch Atmosphere/Hekate CFW, FAT32 32KB alignment, NSP/NSZ compression. |
| **`disassembly-token-redactor`**| Strips raw hex opcodes and NOP sleds from objdump, emitting symbolic CFGs. |
| **`rea-mcp-obligation-ledger-orchestrator`**| REA MCP obligation ledger, binary function diffing, static-to-runtime sync. |
| **`autogen-adversarial-redteam-critic`**| Microsoft AutoGen multi-persona red-teaming, attacking candidate fixes. |
| **`game-trainer-engineering`** | Cross-platform memory scanning, pointer chain resolvers, AOB scans, detours. |

</details>

<details>
<summary><b>📱 6. Mobile Android & Handheld Linux Engineering (24 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`android-app-engineering`** | Kotlin, Gradle KTS, foreground services, network VPN APIs, ProGuard/R8. |
| **`android-game-ndk-vulkan`** | Native Android game dev in C++20, Android NDK GameActivity, Vulkan rendering. |
| **`android-mobile-3d-asset-optimizer`**| Tile-Based Deferred Rendering triangle budgets, fp16 vertex quantization, ASTC. |
| **`android-monetization-iap-ads`**| Google Play BillingClient 7.x, receipt cryptographic verification, Integrity API. |
| **`android-rom-os-engineering`** | Custom ROM dev, AOSP/LineageOS device trees, vendor blobs, SELinux sepolicy. |
| **`android-device-automation`** | Real-time device control, scrcpy mirroring, touch automation, carrier debloating. |
| **`android-ndk-jni-engineering`** | C/C++ JNI, zero-copy ByteBuffers, Vulkan/Oboe audio, tombstone symbolization. |
| **`android-compose-ui-ux`** | Jetpack Compose, Material 3, edge-to-edge window insets, recomposition tuning. |
| **`android-architecture-jetpack`**| Clean Architecture, MVI/StateFlow, Room auto-migrations, Navigation DSL. |
| **`android-testing-ci-cd-security`**| Robolectric, Compose UI tests, R8 shrinking, Android Keystore StrongBox. |
| **`android-perf-battery-profiling`**| Jank analysis (dumpsys gfxinfo), batterystats, Perfetto, memory leak heap dumps. |
| **`mobile-gpu-texture-compression`**| ASTC/ETC2 mobile texture compression pipeline, runtime negotiation, mipmaps. |
| **`mobile-thermal-frame-pacing`**| Android Swappy frame pacing, dynamic resolution scaling (DRS), battery efficiency. |
| **`android-dev-runner`** | Android development runner, scrcpy device mirroring, and jank analysis. |
| **`proton-game-dev-linux`** | Target Valve Proton, case-sensitive asset path normalization, open codecs. |
| **`steamdeck-proton-hardware-tuning`**| Steam Deck 15W APU TDP budget, 40Hz frame pacing, 1280x800, 28px font scaling. |
| **`wine-proton-native-interop`** | Win32-to-Linux named pipes, shared memory shims, Wine DLL call thunking. |
| **`linux-game-window-input-capture`**| Pointer grab/confinement, Gamescope sandboxing, borderless windowing. |
| **`linux-gaming-proton-optimization`**| Steam Proton prefix repair, GE-Proton codecs, dxvk.conf tuning, GameMode. |
| **`cross-platform-game-compatibility`**| 4GB LAA memory patching, legacy DirectX wrappers, thread affinity caps. |
| **`game-window-helper`** | Gamescope sandboxing, pointer lock, focus isolation, multi-monitor dual setup. |
| **`mangohud-configurator`** | In-game performance HUD configuration (FPS, frametimes, 1% lows, VRAM, thermals). |
| **`amd-igpu-nvidia-dgpu-hybrid-offload`**| Dual-GPU splitter: AMD Radeon iGPU (display) + NVIDIA RTX 5060 dGPU (compute). |
| **`linux-perf-flamegraph-bottleneck-triage`**| Hardware performance counters and Flamegraph bottleneck triage under Linux/Proton. |

</details>

<details>
<summary><b>🌐 7. Modern Web Architecture, Full-Stack & UI/UX (26 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`human-crafted-web-design`** | Anti-AI heuristics, Linear/Stripe aesthetics, Geist typography, Tailwind CSS. |
| **`creative-web-design-archetypes`**| Neo-Brutalism, Parchment, Cyberpunk HUD, Academic Journal, Glassmorphism. |
| **`static-site-architecture`** | Modern Jamstack architecture (Astro, VitePress, Starlight, Content Collections). |
| **`intelligent-interactive-ui`** | Reactive single-file micro-apps, live calculators, filterable data tables. |
| **`interactive-data-visualization-web`**| D3.js force-directed networks, Vis.js timelines, dynamic entity stat matrices. |
| **`generative-visual-artifacts`**| Self-contained interactive HTML/SVG widgets, KaTeX mathematical formulas. |
| **`canvas-interactive-workspace`**| Collaborative side-by-side editing canvas, targeted inline diff staging. |
| **`cross-browser-extensions`** | Manifest V3 extensions (Chrome, Firefox, Safari) with background workers. |
| **`headless-browser-automation`**| Headless Chromium via Playwright and Puppeteer, dynamic JS, screenshot capture. |
| **`documentation-site-generator`**| Static documentation site generation using VitePress and MkDocs Material. |
| **`humanities-lore-research`** | Cross-disciplinary history, ancient mythology, folklore, entity dossiers. |
| **`executive-business-communications`**| BLUF executive emails, client proposals, Scope of Work (SOW), invoice generation. |
| **`furry-fursona-art-design`** | Furry/fursona character art, multi-view turnaround refsheets, digitigrade anatomy. |
| **`frontier-image-studio`** | Multi-backend AI image generation dispatch (OpenAI, Gemini Imagen, Flux.1, Pillow). |
| **`youtube-shorts-video-automation`**| Automated viral YouTube Shorts/TikToks: 9:16 vertical, hook-first pacing, subtitles. |
| **`video-production-automation`**| FFmpeg hardware NVENC (AV1, HEVC, H.264), multi-track audio mastering (-14 LUFS). |
| **`discord-bot-engineering`** | Discord API v10 slash commands, interactive buttons/modals, voice audio gateway. |
| **`game-dialogue-ui-localization`**| Multi-language conversation UI repair (FIGS, CJK, Slavic, BiDi RTL, Turkish). |
| **`game-dialogue-tool`** | Dialogue XML validation, missing string ID detection, talk dialog formatting. |
| **`game-localization-i18n`** | ICU message formatting, pluralization rules, RTL layout mirroring. |
| **`generative_ui`** | Production-ready generative UI component scaffolding and live widgets. |
| **`weather-lighting-tuner`** | Balances sun shafts, bloom, dynamic skyboxes, and glare suppression. |
| **`game-texture-editing`** | Procedural normal generation, RNM blending, seamless tiling, de-lighting, CAS. |
| **`game-texture-material-pipeline`**| BCn/ASTC/KTX2 compression, normal map Y-inversion, ORM channel packing. |
| **`game-graphics-optimization-profiling`**| Hi-Z occlusion culling, GPU MultiDraw, LODs, TAA, DLSS/FSR integration. |
| **`post-processing-visual-fx`** | ACES/AgX tone mapping, progressive bloom, SSAO/GTAO, CSM shadow cascades. |

</details>

<details>
<summary><b>🔬 8. Machine Vision, OCR & Visual Intelligence (18 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`computer-vision-deep-learning`**| Neural object detection (YOLOv8/v11), instance segmentation (SAM 2), ByteTrack. |
| **`industrial-machine-vision-inspection`**| Camera calibration, sub-pixel dimensioning, Otsu/Sauvola, template matching. |
| **`visual-document-ocr-intelligence`**| Multi-engine OCR (Tesseract/Paddle/Surya), deskewing, table extraction. |
| **`agentic-visual-perception`** | SAHI 4K/8K tiling, natural language visual grounding coordinates, SSIM diffing. |
| **`screen-vision-inspector`** | Autonomous screen/window capture and visual layout debugging (Project Astra). |
| **`argon-multimodal-vision-grounding`**| Game screen telemetry, UI layout audits, rendering artifact triage. |
| **`local-gpu-vision-ocr-preprocessor`**| Pre-processes screenshots locally on host CPU/GPU using perceptual frame diffing. |
| **`game-screen-telemetry-monitor`**| Real-time in-game screen telemetry monitoring, anomaly detection, crash OCR. |
| **`silhouette-iou-profiler`** | Extracts 32-slice mathematical width contours and verifies Silhouette IoU >= 0.80. |
| **`local-vector-rag-engine`** | Local vector embeddings and dense semantic search engine on host CPU/GPU/RAM. |
| **`local-ast-compiler-engine`** | Multithreaded AST parsing (`nproc`), symbol extraction, and syntax checks. |
| **`local-model-coprocessor`** | Offloads docstrings, commit messages, and boilerplate to local Ollama models. |
| **`local-preflight-syntax-gate`**| Zero-token host CPU syntax verification (luac, ruff, cargo, clang). |
| **`semantic-codebase-indexing`**| AST symbol indexing, call-graph tracing, and ctags/tree-sitter repo mapping. |
| **`qwen-polyglot-ast-cartographer`**| Symbol call-graphs, inheritance trees, and signatures across C++, Python, Lua. |
| **`polyglot-ast-interface-pruner`**| Strips function bodies, comments, and private variables for 85–90% context reduction. |
| **`smart-context-packer`** | Compresses multi-file codebases into interface-only AST skeletons. |
| **`selective-context-ingestor`**| Enforces surgical line-slice reading and AST-first inspection via `slice-reader`. |

</details>

<details>
<summary><b>🧪 9. Automated Testing, QA & Mutation Fuzzing (20 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`self-healing-test-automation`**| Resilient locator auto-repair, semantic scoring, visual OCR fallback. |
| **`coverage-guided-mutation-testing`**| AST-based fault injection, mutant survival analysis, and automated test synthesis. |
| **`game-exploratory-fuzzing`** | Evolutionary action mutation, novelty-guided state exploration, crash bisection. |
| **`game-self-improving-qa-pipeline`**| Closed-loop self-improving QA, 'Press any key' dismissal, stall watchdog. |
| **`game-qa-playtest-controller`**| Autonomous multi-axis locomotion (orbit, sweep, wander) via `/dev/uinput`. |
| **`game-test-watchdog`** | Anti-stuck, freeze, and infinite loop supervisor for game QA runs. |
| **`stalker-playtest-runner`** | Hands-free playtesting, cheat injection, locomotion, crash interception. |
| **`self-improving-qa`** | QA controller, screen dismissal, stall monitoring, and crash triage. |
| **`headless-gameplay-testing-bot`**| Synthetic input replay (uinput, adb input), regression fuzzing, invariant assertions. |
| **`headless-game-ci-automation`**| Automated headless compilation, asset baking, CLI test execution (GUT). |
| **`nav-graph-recorder`** | Autonomous level waypoint mapping, route recording, collision trap logging. |
| **`game-dynamic-stress-orchestrator`**| Safe radial wave spawning, multi-faction air/mutant clashes, VRAM profiling. |
| **`game-ai-agent-play`** | Reinforcement learning, Gymnasium, OpenCV computer vision, low-latency input. |
| **`headless-test-condenser`** | Condenses verbose test suite output, reporting only failing assertions. |
| **`log-output-sanitizer`** | Intercepts noisy compiler and package manager terminal output. |
| **`coderabbit-ai-review`** | CodeRabbit-grade autonomous PR code review, sequence diagrams, suggestion diffs. |
| **`subagent-code-reviewer`** | Dispatches an isolated subagent to audit code changes and mod diffs. |
| **`devin-environment-self-healer`**| Diagnoses missing host dependencies, dynamic libraries (.so), and compilers. |
| **`cross-agent-hot-reload-watcher`**| inotifywait observer triggering instant hot-reloading of modified scripts. |
| **`cursor-rules-sync`** | Converts all skills to Cursor `.mdc` rules and synchronizes `.cursorrules`. |

</details>

<details>
<summary><b>🤖 10. Frontier AI, Subagent Swarms & Multi-Model Parity (35 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`agy-omni-mode`** | Dynamic model & fleet orchestrator switching between Gemini and local Ollama. |
| **`local-research-scout`** | Multi-source web search (DuckDuckGo, GitHub, StackOverflow) + `bge-m3` RAG. |
| **`argon-dynamic-subagent-swarm`**| Spawns parallel Flash worker subagents for high-volume asset conversion. |
| **`argon-subagent-dispatch-routing`**| 'Argon Brain, Flash Hands' dispatch pattern offloading high-volume execution. |
| **`argon-subagent-lifecycle-governor`**| Prevents zombie hangs and interactive prompt blocking with timeouts. |
| **`argon-subagent-payload-compressor`**| Enforces high-density return envelopes, reducing parent context inflation by 80%. |
| **`argon-tool-calling-densifier`**| Enforces compact parallel tool invocation and parameter density on Argon. |
| **`argon-sentencepiece-serializer`**| Formats tabular data to optimize density under Google's SentencePiece tokenizer. |
| **`argon-structured-json-schema-enforcer`**| Constrained decoding emitting deterministic, schema-compliant JSON payloads. |
| **`argon-self-contained-autonomous-driver`**| Single-driver workflow unifies planning, C++ refactoring, and QA playtesting. |
| **`subagent-swarm-orchestrator`**| Coordinates parallel subagent swarms in Claude Code using isolated worktrees. |
| **`claude-silent-dispatch`** | Eliminates pre-tool narration and commentary, executing tools directly. |
| **`claude-worktree-tmux`** | Detached background sessions and tmux pane isolation without context pollution. |
| **`claude-opus-plan-sonnet-exec`**| Hierarchical planning on Claude 3.7 Opus and execution on Sonnet 3.7. |
| **`chatgpt-o1-hypothesis-tree`**| Emulates ChatGPT o1/o3-mini Tree-of-Thought deliberation on Gemini 4 Argon. |
| **`codestral-fill-in-the-middle`**| Emulates Mistral Codestral Fill-in-the-Middle (FIM) surgical infilling. |
| **`cohere-provenance-grounding-ledger`**| Emulates Cohere Command R+ grounded provenance citations for config parameters. |
| **`grok-realtime-telemetry-scout`**| Emulates xAI Grok real-time live search, scouting git commits and package feeds. |
| **`meta-llama-kv-prefix-stabilizer`**| Emulates Meta Llama 3.3 KV-cache alignment for 95% prompt cache discounts. |
| **`deepseek-r1-math-verification`**| Emulates DeepSeek-R1 chain-of-verification and self-correcting proofs in CoT. |
| **`cursor-inline-diff-lens`** | Emulates Cursor IDE ghost-text and surgical multi-line inline diff previews. |
| **`windsurf-cascade-flow-tracker`**| Emulates Codeium Windsurf Cascade Flow, tracking multi-file dependency ripples. |
| **`fable-atomic-diff-sequencer`**| Enforces atomic chunk editing on Claude Fable, eliminating full-file rewrites. |
| **`dual-engine-quota-balancer`**| Dynamic telemetry coordination across Argon, Flash subagents, and local offloads. |
| **`dynamic-model-downshifter`**| Telemetry governor downshifting to Flash when quota headroom reaches safe reserve. |
| **`multi-model-cache-harmonizer`**| Harmonizes prompt cache boundaries across Claude, Gemini, OpenAI, and Grok. |
| **`cross-model-switch-pruner`**| Pre-switch state compaction eliminating token re-reads when switching models. |
| **`model-optimal-state-serializer`**| Tokenizer-native serialization (XML-KV for Claude, Pipe-TSV for Gemini). |
| **`dynamic-repo-model-cheatsheet`**| Terminal cheat sheet (`agy-cheatsheet`/`cs`) recommending model/effort per repo. |
| **`cross-cli-session-handoff`** | Serializes state for seamless handoffs between Antigravity, Claude, and Cursor. |
| **`session-episodic-memory`** | Multi-session milestone checkpointing and chronological episode logging. |
| **`session-experience-harvester`**| Mines past session logs, distilling solved CTDs and token savings into memory. |
| **`hierarchical-memory-retrieval`**| Multi-tiered BM25 search across working context, episodes, and semantic patterns. |
| **`project-memory-bank`** | Persistent project memory and context curation system (`.agents/memory/`). |
| **`sandbox-code-interpreter`** | Headless Python scientific computing, data analytics, and mathematical proofs. |

</details>

<details>
<summary><b>📦 11. DevOps, Docker, CI/CD & Documentation (26 Skills)</b></summary>

| Skill | Purpose & Key Capabilities |
| :--- | :--- |
| **`homelab-docker-devops`** | Self-hosted Docker Compose multi-service stacks, Samba permissions, Nextcloud. |
| **`github-actions-cicd`** | Multi-OS GitHub Actions matrix builds, automated release packaging, caching. |
| **`nix-reproducible-environments`**| Hermetic developer environments using Nix Flakes (`flake.nix`, `devShells`). |
| **`static-site-architecture`** | Jamstack architecture with automated GitHub Pages CI/CD deployment pipelines. |
| **`documentation-site-generator`**| Static documentation site generation using VitePress and MkDocs Material. |
| **`skills-updater-and-auditor`**| Audits installed skills, verifies frontmatter, repairs permissions, syncs repos. |
| **`skill-evolve`** | Runtime skill scaffolder, Voyager script promoter, and `<50ms` hot-patcher. |
| **`skill-optimize`** | Autonomous skill ecosystem optimizer, building capability graphs. |
| **`autonomous-skill-ecosystem-optimizer`**| Closed-loop auto-optimizing skill ecosystem harmonizer (`skill_ecosystem_graph.json`). |
| **`self-evolving-skill-synthesizer`**| Closed-loop in-flight skill synthesis, promoting verified scripts into skills. |
| **`autonomous-git-repo-sync-governor`**| Upstream pull/rebase, milestone auto-commit, secret pre-commit filtering. |
| **`repo-auto-sync`** | Autonomous git repo puller, `.gitignore` hardener, README updater, push manager. |
| **`cross-agent-git-rebase-guard`**| Automated git worktree synchronization, non-interactive rebasing, conflict merges. |
| **`using-git-worktrees`** | Manages isolated git worktrees for parallel mod development and risky changes. |
| **`argon-hierarchical-worktree-isolator`**| Sandboxes concurrent subagent file modifications into isolated git worktrees. |
| **`git-diff-token-compressor`** | Zero-context hunks (-U0) and coordinate patches slashing diff tokens by 70–85%. |
| **`ramdisk-tmpfs-build-bake-accelerator`**| Stages Blender bakes, renders, and CMake objects in `/dev/shm` (40 GB/s bandwidth). |
| **`legacy-codebase-cartographer`**| AST-first reverse engineering of legacy repos, extracting control flow graphs. |
| **`agent-error-recovery-sentinel`**| Automatic watchdog catching fatal build breaks, segfaults, and unhandled exceptions. |
| **`game-mod-release-packager`** | Automated mod release packaging, XDB container compression, checksum manifests. |
| **`zoneforge-cloud-sync-governor`**| Google Drive and cloud asset sync, OAuth2 token renewal, resumable transfers. |
| **`steam-mod-scanner`** | Fingerprints installed Steam games by engine and maps them to modding skills. |
| **`agy-codebase-init`** | Autonomous repository intake (parity with `/init`), detecting build systems and linters. |
| **`agy-cli-doctor`** | System diagnostics (parity with `doctor`), verifying database and endpoint health. |
| **`agy-context-telemetry`** | Token cost inspector (parity with `/context` and `/cost`), tracking cache efficiency. |
| **`deep-research-synthesizer`**| Autonomous multi-source web crawling, recursive citation mapping, research synthesis. |

</details>

---

## 📊 Real-Time Dual-CLI Quota & Statusline Monitors

The suite includes **dedicated, tailor-made statusline monitors** for both CLIs:

### 1. Claude Code CLI Dedicated Monitor (`claude-statusline`)
Installed to `~/.local/bin/claude-statusline` and configured in `~/.claude/settings.json`. Intercepts Claude Code's live `stdin` telemetry stream to render model, rate limits, weekly reset countdowns, visual context gauge with token counts, prompt cache savings, session cost, and git worktree:
```text
⚡ Claude [Sonnet 3.7 • Turbo] | 5h: 86% (reset 00:40) | Wk: 96% (reset in 40m) | 🧠 Ctx: [█░░░░░] 22% (44k) | 💾 Saved: 5.2M tok (92% cache) | 💲 $0.06 +45/-12
```

### 2. Antigravity CLI Dedicated Monitor (`agy-quota-statusline`)
Installed to `~/.local/bin/agy-quota-statusline` and configured in `~/.gemini/antigravity-cli/settings.json`:
```text
⚡ Gemini: 5h: 78% (reset 16:00) | Wk: 72% | 💾 Saved: 23.7M tok (Flash)
```
In multi-model sessions:
```text
⚡ Gemini: 5h: 78% | Wk: 72% | 💾 Saved: 23.4M tok (Argon: 12.0M | Flash: 11.4M)
```
* **Context Cache Token Telemetry:** Correlates active session step tokens from `transcript.jsonl` with turn models in `gen_metadata` to display exact prompt tokens saved by context caching.
* **Universal Lifetime Fallback:** When active session cache savings are clean, seamlessly falls back to `~/.cli_power_setup/token_ledger.json` to render the persistent lifetime token benchmark (`1.54B tok`).
* **Zero CLI Lag:** Subprocesses are detached with PID lockfile protection (`/tmp/agy_quota_refresh.lock`), guaranteeing instantaneous prompt rendering (<2ms).

---

## 🛡️ Ultimate Hardening Protocols & Zero-Token Host Pre-Flight

To maximize efficiency and slash token costs when operating heavy-duty frontier models like **Claude Fable 5.1** or **Gemini 4 Argon**, the suite enforces automated host-CPU pre-flighting and strict context containment:

### The Zero-Token Host Pre-flight Arsenal (<30ms Local Execution)
Instead of forcing expensive LLMs to read raw, noisy files into their context windows, 6 specialized Python utilities process data directly on the host CPU in milliseconds with **0 API tokens burned**:

| Pre-flight Utility | Associated Skill | What It Does on Host CPU | Token Savings |
| :--- | :--- | :--- | :--- |
| **`fable_slice_extractor.py`** | `fable-virtual-context-manager` | Strips function bodies, extracting AST class hierarchies and signatures | **~97% input token reduction** |
| **`slice-reader`** | `selective-context-ingestor` | Extracts line-numbered AST skeletons or focused $\pm 15$ line windows | **~92%–95% file reading reduction** |
| **`token-guard`** | `shell-output-token-guard` | Enforces a 30-line ceiling on commands (`grep`, `find`, `git log`) | **Prevents 10k–50k stdout floods** |
| **`compiler_cascade_isolator.py`** | `compiler-error-cascade-isolator` | Filters compiler template cascades, isolating #1 root-cause coordinate | **~95% compiler log reduction** |
| **`xray_crash_resolver.py`** | `xray-crash-symbol-resolver` | Scans 15,000-line crash logs, isolating fatal assertions and RVAs | **~99% crash log reduction** |
| **`config_delta_extractor.py`** | `game-config-delta-extractor` | Compares child config sections with parents, extracting only overrides | **~95% config token reduction** |

---

## 📱 Android 2D & 3D Game & App Development Workflows

The repository provides a dedicated toolchain and automation suite for high-performance 2D and 3D Android development across C++/Vulkan NDK, Godot, Unity, and Jetpack Compose:

1. **High-End 3D Native Game Architecture (C++ / Vulkan NDK):**
   * **Skills:** `android-ndk-jni-engineering` + `vulkan-gpu-compute` + `game-texture-material-pipeline` + `android-perf-battery-profiling`.
   * **Tooling:** Automated NDK builds with CMake, Vulkan validation layers, ASTC texture compression, and zero-copy ByteBuffers.

2. **Cross-Platform Engine Porting (Godot / Unity Android):**
   * **Skills:** `android-app-engineering` + `android-mobile-3d-asset-optimizer` + `mobile-thermal-frame-pacing`.
   * **Optimization:** TBDR tile budget profiling, Swappy frame pacing, and Dynamic Resolution Scaling (DRS).

3. **Modern Jetpack Compose UI & Reactive Apps:**
   * **Skills:** `android-compose-ui-ux` + `android-architecture-jetpack` + `android-testing-ci-cd-security`.
   * **Architecture:** Clean Architecture with MVI/StateFlow, edge-to-edge window insets, StrongBox Keystore security, and Robolectric UI tests.

```bash
# Verify Android SDK/NDK, USB debugging & device screen mirroring
android-dev-runner doctor
android-dev-runner mirror   # Launches high-performance scrcpy mirror
android-dev-runner jank     # Profiles frame rendering drops and 1% lows
```

---

## 📂 Repository Structure

```text
cli-power-setup/
├── install.sh                  # Interactive Linux installer with backup & menu
├── install.ps1                 # Native Windows 10/11 PowerShell installer
├── README.md                   # Comprehensive documentation & categorized reference
├── .cursorrules                # Root-level unified Cursor AI rules & skill index
├── .cursor/
│   └── rules/                  # 316 modular Cursor rules (.mdc) with semantic metadata
├── bin/
│   ├── agy-omni-mode           # Dynamic Gemini & local Ollama model orchestrator
│   ├── local-research-scout    # Zero-quota multi-source search (DDG, GitHub, SO) + RAG
│   ├── agy-quota-statusline    # Live multi-row quota, skills, thermal, VRAM & git statusline
│   ├── agy-mic-button          # Floating draggable/pinnable voice dictation pill for agy
│   ├── agy-yolo                # Autonomous hands-free YOLO mode launcher (Argon + Flash)
│   ├── agy-turbo               # High-speed Flash low-effort Turbo mode launcher
│   ├── agy-cheatsheet          # Dynamic repo-aware model, effort & hardware offload recommender
│   ├── game-math-solver        # 32-thread CPU + RTX 5060 CUDA math, physics & SymPy solver
│   ├── local-coprocessor       # Zero-quota task dispatcher to local Ollama fleet
│   ├── setup-local-model-fleet # Local model fleet installer, tier synchronizer & telemetry
│   ├── gemini-reasoning-tuner  # Automatic model tier and reasoning effort governor
│   ├── laptop-perf             # Hardware acoustic & thermal governor (lid-closed 3D lock)
│   ├── repo-auto-sync          # Autonomous git pull/checkpoint/push & fleet manager
│   ├── skill-evolve            # Closed-loop runtime skill scaffolder & script promoter
│   ├── skill-optimize          # Auto-optimizing skill ecosystem graph harmonizer
│   ├── stalker-playtest-runner # Autonomous hands-free game QA, dialogue & locomotion runner
│   ├── context-watchdog        # Automated background context monitor & pre-compact memory stager
│   ├── token-guard             # Terminal command output line ceiling protector (30-line ceiling)
│   └── slice-reader            # Surgical line-slice reader & AST skeleton extractor
└── config/
    ├── GEMINI.md               # Global engineering discipline, quota governance & voice rules
    ├── skill_ecosystem_graph.json # Auto-optimized capability graph across all skills
    ├── token_ledger.json       # Pure Antigravity (agy) lifetime token savings ledger
    └── skills/                 # 314 specialized skill packages
```

---

<!-- AUTO-SYNC-CATALOG:START -->
## 🔄 Auto-Synchronized Skill & CLI Inventory (316 Total Active Skills)

### Latest CLI Utilities (`bin/` -> `~/.local/bin/`)
| CLI Tool | Purpose |
| :--- | :--- |
| **`agy-mic-button`** | Floating XWayland voice dictation pill (`[🎙️ Talk | ⏎ Send | ⚡Auto | 📌Pin]`) with drag memory, terminal snap-pin, and auto-close on `agy` exit. |
| **`rtx-engine-toolkit`** | NVIDIA RTX/NGX/DLSS 4 engine auditor & code generator (`audit`, `gen-dlss-patch`, `gen-hlsl-ssgi` SM 5.0 compute ray-tracing, `gen-cdb-bvh`, `gen-dx12-bridge`). |
| **`eleven-studio`** | ElevenLabs feature parity CLI: expressive character neural TTS, `--ref-audio` 32-band timbre cloning, STS voice changer (`--pitch`/`--formant`), STFT Voice Isolator, S.T.A.L.K.E.R. radio/gasmask FX, and GSC v3 Ogg headers. |
| **`game-math-solver`** | Zero-quota 32-thread AVX-512 CPU + RTX 5060 CUDA 13.4 GPU math solver (`coord`, `ode`, `ballistics`, `ai-node`, `prove`, `hw-bench`). |
| **`creature-sound-forge`** | Real CC0 animal vocalization masterer + Klatt/Rosenberg mammalian glottal-formant DSP synth + 24-byte GSC X-Ray v3 binary Ogg header injector. |
| **`sound-web-scout`** | Autonomous web audio & SFX researcher (Wikimedia Commons + Internet Archive) with `/dev/shm` SNR scoring, burst slicing, and GSC v3 Ogg mastering. |
| **`blender` (RTX 5060 Wrapper)** | Forces NVIDIA GeForce RTX 5060 PRIME offload for Viewport/EEVEE/Workbench + locks Cycles to `OPTIX` GPU (`force_rtx5060_optix.py`). |
| **`laptop-perf`** | Hardware acoustic & thermal governor (`clamshell-3d` lid-closed 3D render lock, `sleep-mode`, `wake-mode`, `boost-exec`). |
| **`agy-cheatsheet` (`cs`)** | Dynamic repo-aware model, reasoning effort, and hardware offload cheat sheet + live statusline recommender (`~/Documents/GitHub`). |
| **`skill-evolve` & `skill-optimize`** | Closed-loop runtime skill scaffolder, Voyager script promoter, `<50ms` hot-patcher, and automatic ecosystem mesh optimizer (`skill_ecosystem_graph.json`). |
| **`repo-auto-sync`** | Autonomous git repo puller, `.gitignore` hardener, `README.md` updater, milestone committer, and 32-repo fleet manager. |
| **`steam-mod-scanner`** | Fingerprints installed Steam games (`/mnt/games/SteamLibrary`) by engine & archive format and maps to modding skills. |
| **`silhouette-iou-profiler`** | Extracts 32-slice mathematical width contours & hex palettes from 2D drawings and verifies 3D render Silhouette IoU. |
| **`local-coprocessor` / `local-rag` / `local-ast-compiler`** | Zero-quota local CPU/GPU/RAM offload engines for AST syntax checks, BM25/vector RAG, and local LLM summarization. |

### Recently Evolved & SOTA Skills (21 Indexed Automatically)
| Skill Name | Description |
| :--- | :--- |
| **`ai-procedural-audio-generation`** | AI-powered and procedural audio generation for game development, content creation, and applications. Covers procedural DSP synthesis (oscillators, envelopes, noise bursts, chiptune/sfxr), text-to-sound-effect (SFX) models, adaptive game soundtrack layering, UI sound design, and loudness normalization. |
| **`argon-yolo-quota-pacing-watchdog`** | Telemetry governor that paces Gemini 4 Argon autonomous YOLO execution, preventing 5-hour quota exhaustion by staging state and safely sleeping until window refresh. |
| **`autonomous-3d-reference-researcher`** | Autonomous online anatomical, mechanical blueprint, and Blender bpy technique researcher. Searches the web for real-world proportions, skeletal joint ratios, and shader recipes before/during 3D modeling and crystallizes findings into skills via skill-evolve. |
| **`autonomous-audio-sfx-web-researcher`** | Autonomously searches open web audio repositories (Wikimedia Commons, Internet Archive) for real CC0/public-domain sound effects, foley, animal vocalizations, weapons, and ambient audio; ranks candidates acoustically by Signal-to-Noise Ratio (SNR), spectral centroid, and clipping; slices the cleanest audio event in /dev/shm; and exports mastered WAV/OGG with GSC X-Ray v3 binary headers. |
| **`blender-3d-printing-cad-manifold-prep`** | General 3D engineering in Blender 5.2+ for 3D printing (FDM/SLA), CNC machining, watertight manifold repair, wall thickness solidification, mechanical snap-fit clearance tolerances (0.15-0.25mm), overhang analysis, and precision STL/3MF export. |
| **`blender-local-ai-critic-loop`** | Closed-loop local AI 3D modeling, topology auditing, and VLM render critique pipeline (blender-local-ai). Bridges local Ollama models (blender-architect:latest, minicpm-v:8b, deepseek-r1:8b) with installed Blender 5.2+ skills at zero cloud token cost. |
| **`claude-fable-engine-governor`** | Autonomous context, token, and quota governor for Anthropic's Claude Fable model during large-scale game engine ports (e.g. S.T.A.L.K.E.R. OGSR/X-Ray). Enforces 1M-token prompt cache pinning, C++ AST skeletonization, and surgical crash-dump extraction. |
| **`cross-agent-context-deduplicator`** | Eliminates redundant transcript ingestion and context pollution between Argon orchestrators and Flash subagents by clamping sync payloads to strict 15-line symbol diff abstracts. |
| **`cuda-numpy-batch-texture-dsp-processor`** | Saturates all 32 host CPU threads (ProcessPoolExecutor), 30 GB RAM, and NVIDIA CUDA/NumPy SIMD vectorization for massively parallel batch processing of .dds textures, normal map swizzling, alpha-coverage mipmaps, and .ogg audio files. |
| **`dynamic-skill-router`** | High-performance semantic intent matching and capability indexing across 100+ installed skills. Use to instantly discover, rank, and activate the exact 2-3 optimal skills for any complex prompt, eliminating skill choice paralysis and context bloat. |
| **`emulator-development-engineering`** | Video game console emulation architecture, CPU interpreter & JIT dynamic binary translation, cycle-accurate timing, memory-mapped I/O (MMU), Vulkan/OpenGL graphics rendering backends, APU sound emulation, and contributions to open-source emulators (Dolphin, RPCS3, PCSX2, Ryujinx, RetroArch). |
| **`flash-context-compactor`** | Prevents Gemini 3.8 Flash context window inflation through targeted line-slice reading, AST interface skeletons, and proactive state compaction below the 100k-token ceiling. |
| **`game-asset-streaming-lod-governor`** | Real-time asynchronous asset streaming, distance-based LOD hierarchies (LOD0-LOD3), virtual texturing, and LRU memory cache eviction. |
| **`game-engine-3d-budget-profiler`** | Enforces game engine 3D performance budgets, automated LOD0-LOD3 generation, convex collision hull generation (UCX), and draw-call material audits in Blender. |
| **`high-density-prompting`** | Compresses verbose prompts into surgical, quota-saving directives, eliminates speculative reasoning tokens, and enforces deterministic, zero-waste agent outputs. |
| **`speculative-multi-step-drafting`** | Bundles predictable consecutive edits and multi-file modifications into single-turn atomic dispatches, slashing multi-turn reasoning overhead and saving up to 75% input tokens. |
| **`stalker2-modding`** | Modding workflows and tools for S.T.A.L.K.E.R. 2 Heart of Chornobyl (Unreal Engine 5). Use when packaging UE5 IoStore containers (pak, ucas, utoc) with repak, authoring RE-UE4SS C++ and Lua hooks, inspecting assets via FModel, or organizing mod distributions. |
| **`ultra-large-model-quantization-optimizer`** | Hardware-aware model compression, extreme low-bit quantization (imatrix IQ2/IQ3), sparse MoE execution, and layer-wise NVMe SSD streaming (AirLLM). Enables running 70B to 405B parameter language models locally on consumer laptop hardware (30GB RAM + 8GB RTX 5060 VRAM). |
| **`voice-prompt-context-optimizer`** | Autonomous voice-to-text prompt normalizer and context token saver. Eliminates conversational filler, corrects phonetic developer jargon (C++, OGSR, LTX, JSON), translates spoken commands into slash commands, and prevents compounding context bloat across voice-driven AI workflows. |
| **`xray-dx11-shader-modernization`** | Modernizes and adapts legacy DirectX 9 Shader Model 3.0 shaders to DirectX 11 Shader Model 5.0 in S.T.A.L.K.E.R. / OGSR Engine. Enforces 16-byte constant buffer (cbuffer) alignment, registers texture sampler splits, and fixes blown-out dynamic lighting/reflections. |
| **`yolo-autonomous-watchdog`** | Autonomous execution watchdog and quota protector for YOLO modes (claude-yolo, agy-yolo). Prevents infinite retry loops, terminal stdout flooding, oscillating file churn, and runaway context inflation during unattended operation. |

<!-- AUTO-SYNC-CATALOG:END -->

---

## 🛠️ Maintenance & Adding New Skills

### To add a new skill:
1. Create `config/skills/<skill-name>/SKILL.md`.
2. Include standard YAML frontmatter:
   ```markdown
   ---
   name: your-skill-name
   description: Brief description explaining when and why to activate this skill.
   ---
   # Skill Title
   ...
   ```
3. Run `skills-audit-update --sync` (or `./install.sh --all`) to automatically compile and deploy the new skill across **Antigravity**, **Claude Code**, and **Cursor IDE**.

---

## 📄 License
MIT License. Free to use, adapt, and distribute for autonomous agent engineering.

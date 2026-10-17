---
name: local-model-coprocessor
description: Offloads low-complexity tasks (docstrings, commit messages, log summarization, regex, boilerplate) to local SLMs/LLMs running in GPU VRAM or system RAM via Ollama or llama.cpp, saving 100% of cloud quota for hard architectural reasoning.
---

# Local Model Coprocessor (`local-model-coprocessor`)

The `local-model-coprocessor` skill bridges your agent with local small language models (SLMs) and open-weights models running directly on your host GPU (NVIDIA CUDA) or CPU/RAM via Ollama or `llama.cpp`.

By delegating deterministic, low-complexity drafting tasks to local hardware, this skill preserves your 5-hour rolling cloud quota for difficult architectural planning, deep debugging, and multi-file refactoring.

---

## 1. Coprocessor Architecture & Quota Shielding

```
+------------------------------------------------------------------------+
|                          Incoming User Request                         |
+------------------------------------------------------------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
|                 Adaptive Complexity Filter (Tier 1 & 2)                |
+------------------------------------------------------------------------+
            |                                               |
 [Hard Problem: Cloud Model]                 [Boilerplate / Trivial: Local]
 (Argon / Sonnet / Flash)                   (Ollama / llama.cpp / VRAM)
            |                                               |
            v                                               v
 Cloud Reasoning Quota Billed                Host GPU VRAM / Local RAM
 (Architectural Plans, Hard Bugs)             - Docstring generation
                                              - Conventional commit msgs
                                              - Terminal log triage
                                              - Regex & shell one-liners
                                              - 0 Cloud Tokens Billed!
```

---

## 2. Complete 23-Model Local Fleet & Task Matrix

The local fleet is orchestrated via Ollama (`http://localhost:11434`), consuming **85 GB** physical disk space in `/var/lib/ollama/blobs/` on NVMe storage with zero cloud token usage:

| Domain / Task Flag | Primary Model | Fallback | VRAM | Specialization / Routing Target |
| :--- | :--- | :--- | :--- | :--- |
| **`--task code`** | `qwen2.5-coder:7b` | `deepseek-coder:6.7b` | ~4.7 GB | Core multi-language refactoring, AST linting, logic fixes |
| **`--task fast`** | `qwen2.5-coder:1.5b` | `llama3.2:3b` | ~1.0 GB | Sub-second regex, docstrings, unit test boilerplate |
| **`--task cpp`** | `deepseek-coder:6.7b-instruct` | `qwen2.5-coder:7b` | ~3.8 GB | Modern C++20, pointer safety, OGSR/X-Ray engine porting |
| **`--task csharp`** | `granite-code:8b` | `qwen2.5-coder:7b` | ~4.6 GB | C# .NET 8/9, Avalonia, EF Core, enterprise backend |
| **`--task rust`** | `starcoder2:7b` | `qwen2.5-coder:7b` | ~4.0 GB | Rust ownership, borrow checker proofs, zero-cost abstractions |
| **`--task python`** | `codellama:7b-python` | `qwen2.5-coder:7b` | ~3.8 GB | Python 3.10+, scientific computing, pytest test generation |
| **`--task math`** | `mathstral:7b` | `wizard-math:7b` / `phi4:14b` | ~4.1 GB | Physics ODEs, exponential damping, quaternion SLERP |
| **`--task reason`** | `deepseek-r1:8b` | `phi4:14b` | ~5.2 GB | Step-by-step chain-of-thought proofs & algorithmic verification |
| **`--task translate`** | `aya:8b` | `qwen2.5:7b` | ~4.8 GB | Cohere 101-language translation, Slavic/CJK/FIGS game dialogue |
| **`--task web`** | `qwen2.5:7b` | `gemma2:9b` | ~4.7 GB | Web modernization, responsive Tailwind, clean semantic HTML |
| **`--task business`** | `gemma2:9b` | `qwen2.5:7b` | ~5.4 GB | Anti-jargon client proposals, BLUF executive copy, SOWs |
| **`--task sql`** | `sqlcoder:7b` | `granite-code:8b` | ~4.1 GB | State-of-the-art SQL query synthesis, SQLite WAL tuning |
| **`--task tool`** | `hermes3:8b` | `llama3.1:8b` | ~4.7 GB | Function calling, tool use, strict JSON schema compliance |
| **`--task long`** | `mistral-nemo:12b` | `qwen2.5:7b` | ~7.1 GB | 128k context window, long document/repo summarization |
| **`--task vision`** | `minicpm-v:8b` | `moondream:latest` | ~5.5 GB | Game HUD inspection, OCR triage, visual bug analysis |
| **`--task blender`** | `blender-architect:latest` | `qwen2.5-coder:7b` | ~4.7 GB | Custom model fused with Blender 5.2 API & organic SDF rules |
| **Embeddings** | `bge-m3:latest` | `nomic-embed-text` | ~1.2 GB | Dense multilingual vector embeddings for `local-vector-rag` |

---

## 3. CLI Helper Tool Reference (`local-coprocessor` / `setup-local-model-fleet`)

Installed in `~/.local/bin/local-coprocessor` and `~/.local/bin/setup-local-model-fleet`.

### Fleet Management Commands
```bash
# 1. Inspect fleet health, hardware telemetry, and disk storage (85 GB)
setup-local-model-fleet --status

# 2. Sync or verify specific functional tiers
setup-local-model-fleet --tier code     # Polyglot coding models
setup-local-model-fleet --tier math     # Physics & STEM models
setup-local-model-fleet --tier dialogue # Translation & text repair
setup-local-model-fleet --tier web-business # Web modernization & proposals
setup-local-model-fleet --all          # Synchronize all 23 models

# 3. Build or rebuild custom Modelfiles
setup-local-model-fleet --build-custom
```

### Coprocessor Execution Commands
```bash
# 1. Code completion or refactoring via optimal engine
local-coprocessor generate --task cpp --prompt "Refactor raw pointer into std::unique_ptr"

# 2. Mathematical derivation & ODE solutions
local-coprocessor generate --task math --prompt "Derive critically damped spring update for fixed_step=0.01"

# 3. Game dialogue translation preserving tags
local-coprocessor generate --task translate --prompt "Translate string into Russian: <text>Hello stalker</text>"

# 4. Web modernization into Tailwind CSS
local-coprocessor generate --task web --prompt "Convert this legacy HTML table to responsive cards"

# 5. Executive business proposal drafting
local-coprocessor generate --task business --prompt "Draft a BLUF proposal for 3D model asset conversion"

# 6. SQL query synthesis & indexing
local-coprocessor generate --task sql --prompt "Generate optimized SQLite schema for game savegame inventory"

# 7. Auto-injecting installed skill rulebooks into local prompt
local-coprocessor generate --auto-skill --prompt "Write a Blender 5.2 bpy script for voxel remeshing"
```

---

## 4. Host Hardware Optimization

* **VRAM Allocation**: Set `OLLAMA_NUM_PARALLEL=2` and `OLLAMA_MAX_LOADED_MODELS=1` in your environment to prevent VRAM thrashing when sharing GPU with graphical desktop tasks.
* **CPU Fallback**: When GPU is busy running Blender or games, run quantized models (`qwen2.5-coder:1.5b-instruct-q4_K_M`) on host CPU cores with zero GPU memory footprint.

## Windows 10/11 & Cross-OS Hardware Offload Parity (`windows-linux-cross-os-runtime-bridge`)
- **CPU Thread Saturation:** Use `os.cpu_count()` in Python, `$env:NUMBER_OF_PROCESSORS` in PowerShell 7 (`CMAKE_BUILD_PARALLEL_LEVEL=$env:NUMBER_OF_PROCESSORS`, `CARGO_BUILD_JOBS=$env:NUMBER_OF_PROCESSORS`, `msbuild /m`), and `$(nproc)` on Linux.
- **RAM-Disk & Scratch I/O:** Resolve scratch paths via `Path("/dev/shm")` on Linux, an ImDisk/OSFMount RAMDrive (`R:\`) if mounted on Windows, or `Path(tempfile.gettempdir())` (`%LOCALAPPDATA%\Temp`). Never hardcode `/tmp/`.
- **Dual-GPU Selection (RTX 5060 dGPU + Radeon 610M iGPU):** On Windows 10/11, bind executables via Registry `HKCU:\Software\Microsoft\DirectX\UserGpuPreferences` (`GpuPreference=1;` for Power-Saving AMD Radeon iGPU; `GpuPreference=2;` for High-Performance NVIDIA RTX 5060 dGPU) and `CUDA_VISIBLE_DEVICES=0`.
- **Vision & OCR on Windows:** Use `PIL.ImageGrab.grab(all_screens=True)` and resolve `tesseract.exe` via `shutil.which("tesseract")` or `C:\Program Files\Tesseract-OCR\tesseract.exe`.

## Related & Interoperating Skills
- **`local-vector-rag-engine`**: Local vector embeddings and dense semantic search engine running on host CPU/GPU/RAM. Replaces context-stuffin...
- **`dual-engine-quota-balancer`**: Dynamic telemetry coordination across Gemini 4 Argon, Gemini 3.8 Flash subagents, and local CPU/GPU offloads, ...
- **`local-ast-compiler-engine`**: High-performance multithreaded AST analysis, symbol table scanning, and structural linting running across all ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

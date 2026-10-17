---
name: agy-omni-mode
description: Dynamic model & fleet orchestrator for Google Antigravity. Dynamically switches between Gemini models (Pro / Flash) and local Ollama language models based on task complexity, active step lifecycle, referenced project files, and rolling 5-hour quota headroom.
---

# AGY Omni-Auto Mode (`agy-omni-mode`)

Autonomous dynamic routing and execution orchestrator. Seamlessly switches between Cloud Gemini models (`gemini-4-pro`, `gemini-3.8-flash`) and host-local Ollama models (`deepseek-coder-v2:16b`, `deepseek-r1:32b`, `qwen2.5-coder:32b`, `bge-m3`) with zero manual toggling.

## Architecture & Tier Hierarchy

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AGY OMNI-AUTO MODE                              │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
       ┌───────────────────────────┴───────────────────────────┐
       ▼                                                       ▼
 [Tier 0: Local Host & Ollama]                       [Cloud Gemini API]
 (0 Cloud Tokens • Free Host Compute)                (Argon Brain & Flash Hands)
  • Intake & AST: local-ast-compiler                  • Tier 1: Flash Low Effort
  • Search & RAG: local-research-scout (bge-m3)       • Tier 2: Flash Subagents
  • Engine Porting: deepseek-coder-v2:16b             • Tier 3: Gemini 4 Pro (High)
  • Deep Logic / Math: deepseek-r1:14b / mathstral
  • Docs / Commits: mistral-nemo:12b / llama3.2
```

## Step Lifecycle Routing Matrix

| Workflow Step | Engine | Model | Reasoning / Tool | Cloud Cost |
| :--- | :--- | :--- | :--- | :--- |
| **Intake / Scan** | Local CPU | `slice-reader` / `local-ast-compiler` | Symbol indexing | **0 tokens** |
| **Web Research** | Local Ollama | `local-research-scout` (`deepseek-coder-v2:16b` + `bge-m3`) | Multi-source RAG search | **0 tokens** |
| **Architecture / Plan** | Cloud Pro / Local | `gemini-4-pro` (or `deepseek-r1:32b` if quota < 40%) | `--effort high` | Minimal |
| **Code / Porting** | Local / Cloud Flash | `deepseek-coder-v2:16b` / `qwen2.5-coder:32b` / `flash` | `--effort low` | **0 to minimal** |
| **Math / Physics** | Local RTX 5060 | `mathstral:7b` / `phi4:14b` / `game-math-solver` | CUDA / AVX-512 | **0 tokens** |
| **Verification / Tests** | Host CPU/GPU | `pytest` / `cargo test` / `local-preflight-syntax-gate` | Native execution | **0 tokens** |
| **Docs / Commits** | Local Ollama | `mistral-nemo:12b` / `llama3.2:3b` | `local-coprocessor` | **0 tokens** |

## CLI Usage

```bash
# Display live workspace domain, dirty files, and optimal engine recommendation
agy-omni-mode

# Evaluate specific prompt routing with rationale
agy-omni-mode "port X-Ray legacy blenders to DX11 hlsl"

# Return machine-readable JSON for integration into statuslines and scripts
agy-omni-mode --json

# Set active workflow step
agy-omni-mode --set-step plan
agy-omni-mode --set-step execute

# Execute immediately on local engine if Tier 0
agy-omni-mode --exec "calculate quaternion slerp for camera trajectory"
```

## Quota Self-Protection Circuit Breaker
- When rolling 5-hour quota is $\ge 40\%$, routine execution uses Gemini 3.8 Flash for instant turnaround and Gemini 4 Argon for high-complexity architecture.
- When rolling 5-hour quota drops $< 40\%$, the orchestrator automatically clamps cloud dispatches and routes code generation, architecture planning, and debugging to local 32B/16B models (`deepseek-r1:32b`, `qwen2.5-coder:32b`, `deepseek-coder-v2:16b`), guaranteeing **uninterrupted execution without quota lockouts**.

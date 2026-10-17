---
name: argon-subagent-dispatch-routing
description: Implements the 'Argon Brain, Flash Hands' subagent swarm dispatch pattern to offload high-volume read, search, and execution tasks to Gemini Flash while conserving Argon quota.
---

# Argon Subagent Dispatch Routing (`argon-subagent-dispatch-routing`)

Gemini 4 Argon (`pro`) is an exceptionally powerful reasoning model with high per-token quota costs. Utilizing Argon to run routine directory listings, wide code searches, repetitive test executions, or read large text files exhausts weekly Argon quota rapidly.

This skill operationalizes the **"Argon Brain, Flash Hands"** protocol by routing execution workloads to lightweight Flash subagents while keeping Argon in the orchestrator role.

---

## 1. Model Tier Division of Labor

```
+--------------------------------------------------------------+
|                   ARGON (pro / --effort high)                |
|  - System Architecture & Planning (/plan, writing-plans)     |
|  - Multi-hypothesis Crash & Segfault Triage                  |
|  - Final Code Review & Verification Gates                    |
+--------------------------------------------------------------+
                               |
                               | (dispatches via invoke_subagent)
                               v
+--------------------------------------------------------------+
|            FLASH SUBAGENTS (flash / flash_lite)              |
|  - Broad repository grep / file reading                      |
|  - Running unit tests & headless test suites                 |
|  - Applying mechanical edits across multiple files           |
|  - Compiling build outputs & formatting summaries            |
+--------------------------------------------------------------+
```

---

## 2. Dispatch Directives

When Argon is the active primary agent:
1. **Delegating Research:** For wide scans or multi-file inspections, call:
   ```json
   invoke_subagent({
     "Subagents": [{
       "TypeName": "research",
       "Role": "Codebase Investigator",
       "Model": "flash",
       "Prompt": "Search for all usages of X and return only the top 5 file paths and line ranges."
     }]
   })
   ```
2. **Delegating Heavy Builds & Tests:** Offload long compilation logs or full test suites to Flash:
   ```json
   invoke_subagent({
     "Subagents": [{
       "TypeName": "self",
       "Role": "Test Runner",
       "Model": "flash",
       "Prompt": "Execute pytest -q and return only failing test names and line coordinates."
     }]
   })
   ```
3. **Conserving Orchestrator Context:** The subagent's internal thinking tokens and raw command dumps remain isolated in its own subagent context, returning only the synthesized summary back to Argon.

---

## 3. Quota Savings Matrix

| Task Type | Handled By | Quota Impact vs Running on Argon |
| :--- | :--- | :--- |
| **Wide Grep / 20+ File Reads** | Flash subagent | **~90% quota saved** |
| **Full Test Suite Execution** | Flash subagent | **~95% quota saved** |
| **Multi-File Boilerplate Generation** | Flash subagent | **~80% quota saved** |
| **Crash Root-Cause Diagnosis** | Argon primary | High cognitive necessity |

---

## 4. Live Cheat Sheet & Payload Compression Integration
- **Repo-Aware Swarm Routing (`dynamic-repo-model-cheatsheet`):** When `agy-cheatsheet` (`cs`) or the bottom of your statusline displays `Argon•High+Flash` (e.g. on `ogsr-complete-merge`), Argon automatically retains 64-bit C++/DX11 tasks while dispatching parallel Flash subagents (`argon-dynamic-subagent-swarm`) for LTX configs, DDS textures, and Ogg Vorbis audio.
- **Return Envelope Compression (`argon-subagent-payload-compressor` & `cross-agent-context-deduplicator`):** All Flash subagents must return compact $\le 15$-line symbol-coordinate summaries so Argon's 1M context window stays lean.
- **Cross-OS Parity (`windows-linux-cross-os-runtime-bridge`):** Operates identically across Linux and Windows 10/11 (`agy-yolo` / `agy-turbo`).


---
name: dual-engine-quota-balancer
description: Dynamic telemetry coordination across Gemini 4 Argon, Gemini 3.8 Flash subagents, and local CPU/GPU offloads, balancing task allocation to guarantee uninterrupted execution without hitting rolling quota limits.
---

# Multi-Tier & Dual-Engine Quota Balancer (`dual-engine-quota-balancer`)

Balancing workloads between **Gemini 4 Argon (`pro`)**, **Gemini 3.8 Flash (`flash` subagents)**, and **Zero-Quota Local Hardware Offloads** guarantees uninterrupted execution across 5-hour and weekly rolling quota windows.

---

## 1. Model Tier & Quota Economics

| Tier / Engine | Quota Characteristics | Best Use Cases (Maximum ROI) | Throttle Threshold |
| :--- | :--- | :--- | :--- |
| **Gemini 4 Argon (`pro`)** | Rolling 5-Hour & Weekly limits; **95% prompt cache discount** ($0.10/MTok); 1M context. | 64-bit C++ engine porting (`OGSR`), DX11/Vulkan shaders, binary RE (`rea`), crash triage, architecture. | Downshift routine steps to Flash when 5h quota < 25% |
| **Gemini 3.8 Flash (`flash`)** | Ultra-high throughput; ~85% lower quota burn than Argon; parallel subagent execution. | LTX/XML/JSON configs, GDScript UI, wide grep/search, running test suites, batch audio/texture scripts. | Offload to local CPU/GPU tools when batching >100 files |
| **Local Host CPU/GPU/RAM** | **0% Cloud Quota** (Ryzen 9 8940HX 32-Thr + RTX 5060 + 30GB `/dev/shm`). | AST syntax checks (`local-ast-compiler`), BM25/vector search (`local-rag`), OptiX baking, OCR diffing. | Always run first before spending cloud tokens |

---

## 2. Dynamic Workload Rebalancing Rules

1. **Enforce "Argon Brain, Flash Hands" (`argon-subagent-dispatch-routing`):**
   - Keep Argon focused on root-cause debugging, C++ 64-bit alignment proofs, and architectural planning.
   - Dispatch file searches, LTX/DDS asset edits, and test suite runs to parallel Flash subagents (`invoke_subagent(..., Model="flash")`).
2. **Automatic Effort Downshifting (`adaptive-reasoning` & `argon-effort-auto-calibrator`):**
   - Use `Argon • High` only for Tier 3 tasks (64b C++, shaders, kernel ACPI, crashes).
   - Use `Argon • Med` for Blender 3D (`bpy`), Lua quests, and multi-file refactors.
   - Use `Flash • Low` for routine config/UI edits and git synchronization.
3. **5-Hour Rolling Window Protection (`argon-yolo-quota-pacing-watchdog`):**
   - If the rolling 5-hour quota approaches safe reserve limits during an `agy-yolo` run, stage state to `.agents/memory/activeContext.md`, shift mechanical tasks to Flash/local tools, or safely sleep until the recorded reset timestamp passes.
4. **Live Statusline & Repo Cheat Sheet (`dynamic-repo-model-cheatsheet`):**
   - Consult `agy-cheatsheet` (`cs`) or the bottom of your `agy` statusline (`🧭 CS [...]`) for real-time per-repository model and hardware routing (`Argon•High+Flash` for `ogsr-complete-merge`, `Flash • Low` for config/UI repos).
   - Offload syntax validation (`local-ast-compiler`), semantic search (`local-rag`), `/dev/shm` builds (`ramdisk-tmpfs-build-bake-accelerator`), and dual-GPU workloads (`amd-igpu-nvidia-dgpu-hybrid-offload`) locally before spending cloud quota.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

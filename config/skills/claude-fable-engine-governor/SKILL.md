---
name: claude-fable-engine-governor
description: Autonomous context, token, and quota governor for Anthropic's Claude Fable model during large-scale game engine ports (e.g. S.T.A.L.K.E.R. OGSR/X-Ray). Enforces 1M-token prompt cache pinning, C++ AST skeletonization, and surgical crash-dump extraction.
---

# Claude Fable Engine Governor (`claude-fable-engine-governor`)

Anthropic's **Claude Fable** model features a **1-million-token context window**, a **128,000-token maximum output**, and advanced adaptive reasoning. It is specifically designed for long-horizon, multi-file software engineering tasks such as full game engine migrations (e.g. 32-bit legacy X-Ray to 64-bit OGSR Engine).

However, unconstrained use of a 1M-token model risks severe rate limit exhaustion and token inflation. This skill establishes strict governance protocols to maximize Fable's reasoning power while slashing compute costs.

---

## 1. The 1M Pinned Prompt Cache Architecture

To sustain Anthropic's **90% prompt cache discount** across hours of continuous engine porting:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ STATIC PREFIX (PINNED & IMMUTABLE -> CACHED AT 90% DISCOUNT)           │
│ - Engine architecture map & subsystem dependency graph                 │
│ - 64-bit data type definitions & memory alignment standards            │
│ - Tool schemas and strict project coding rules (LTX, C++, Lua)         │
├────────────────────────────────────────────────────────────────────────┤
│ DYNAMIC TAIL (APPEND-ONLY -> RECOMPUTED EACH TURN)                     │
│ - Condensed compiler diagnostics (headless-test-condenser)            │
│ - Targeted 15-frame crash log snippets (xray_*.log)                    │
│ - Surgical file replacements (replace_file_content)                    │
└────────────────────────────────────────────────────────────────────────┘
```

- **Prefix Invariance:** Prohibit dynamic timestamps, clocks, or fluctuating headers in the prefix.
- **Cache Reuse:** By pinning static engine interfaces, a 200,000-token context acts like a 20,000-token input billing event on subsequent turns.

---

## 2. Whole-Engine AST Skeletonization

Never dump raw multi-thousand-line C++ files into Fable when reasoning about engine architecture. Ingest interface skeletons:

```cpp
// Prohibited (Raw implementation bloat: ~1,200 tokens):
class CWeaponAK74 : public CWeaponMagazinedWGrenade {
    // 250 lines of inline firing logic, audio triggers, animations
};

// Enforced (Engine AST Skeleton: ~60 tokens):
class CWeaponAK74 : public CWeaponMagazinedWGrenade {
public:
    virtual void Load(LPCSTR section) override;
    virtual void FireTrace(const Fvector& P, const Fvector& D) override;
    virtual void net_Export(NET_Packet& P) override;
};
```

- **Efficiency Payoff:** Allows Fable to hold the **entire game engine's public interface** across all subsystems (`xrGame`, `xrRender`, `xrCore`, `xrPhysics`) in under 60,000 tokens.

---

## 3. Crash Dump & Stack Trace Slicing

Game engine crash logs (like `xray_*.log` or BugTrap reports) often exceed 15,000 lines of initialization output.

- **Extraction Filter:**
  ```bash
  # Prohibited:
  cat xray_crash.log

  # Enforced: Extract only fault address, assertion, and callstack
  grep -A 25 -B 5 "FATAL ERROR" xray_crash.log || tail -n 35 xray_crash.log
  ```
- **Context Savings:** Ingests $\le$ 35 lines (~350 tokens) instead of 15,000 lines (~120,000 tokens) while preserving 100% of the diagnostic value.

---

## 4. Adaptive Thinking Token Allocation

| Task Scope in Engine Port | Thinking Budget | Operational Mode |
| :--- | :--- | :--- |
| **Crash Diagnosis / Pointer Alignment** | **6,000 – 10,000 tokens** | Deep deliberative reasoning; trace call graph & struct padding |
| **Shader & Render Graph Migration** | **3,000 – 5,000 tokens** | Validate vertex/pixel registers and constant buffer layouts |
| **Lua Script Binding / LTX Syntax** | **$\le$ 1,500 tokens** | Direct interface match; verification against schema |
| **File Edits & Build Verification** | **0 tokens (Disabled)** | Immediate tool invocation; zero speculative monologue |

---

## 5. Three-Tier Delegation Boundary

- **Fable:** Reserved for root-cause crash triage, 64-bit struct padding proofs, and render graph refactoring.
- **Sonnet:** Executes implementation code diffs, builds Lua tables, and modifies weapon LTX configs.
- **Haiku / Flash:** Runs compilers (`ninja`, `cmake`), executes Wine/Proton tests, and checks git diff status.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

## Related & Interoperating Skills
- **`fable-planning-token-compressor`**: Eliminates input and output token bloat during Claude Fable 5.1 planning phases (AST skeletonization, contract-only plans).
- **`claude-5-5-multi-agent-orchestrator`**: Coordinates autonomous parallel subagent swarms for Claude 5.5 and Fable 5.1.
- **`fable-virtual-context-manager`**: Virtualized context paging and hierarchical indexing for Claude Fable (1M-token context). Prevents full 1M-token re-billing.
- **`fable-atomic-diff-sequencer`**: Multi-file refactor execution coordinator for Claude Fable 5.1. Regulates Fable's 128k output capacity.
- **`claude-ultimate-quota-sentinel`**: Unified 6-pillar quota and rate-limit preservation engine for Claude Code.
- **`dynamic-repo-model-cheatsheet` (`claude-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

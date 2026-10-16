---
name: autonomous-goal-governor
description: Quota governance, machine-verifiable contract formulation, circuit breaker enforcement (3-strike rule), and phased milestone compaction during long-running /goal and overnight autonomous agent runs.
---

# Autonomous Goal Governor & Quota Protector

The **Autonomous Goal Governor** protects token quotas and prevents catastrophic context rot during long-running autonomous execution loops triggered by the `/goal` command or multi-step unattended tasks.

It transforms open-ended user requests into machine-verifiable contracts, enforces an automated **3-Strike Circuit Breaker** against trial-and-error doom loops, and orchestrates **Phased Milestone Compaction** to reset context volume between execution phases.

---

## 🎯 When to Activate

* **Initiating `/goal` Runs:** When the user issues `/goal <description>` or asks for an overnight/autonomous execution loop.
* **Open-Ended or Complex Prompts:** Transforming ambiguous goals (*"make this feature work"*, *"port this mod"*) into bounded, machine-verifiable exit assertions.
* **Persistent Test/Compile Failures:** Tripping a circuit breaker when an agent fails 3 consecutive iterations on the same issue, forcing an atomic rollback instead of burning 50,000+ tokens on minor variations.
* **Multi-Hour Tasks:** Splitting large projects into discrete phases with atomic commits and `/compact` checkpoints to prevent the 100k+ token per-turn penalty.

---

## 🛡️ Core Governance Protocols

### 1. Machine-Verifiable Contract Formulation
Never enter an autonomous loop on an ambiguous prompt. Before beginning work, formulate a structured goal contract:
```bash
python3 config/skills/autonomous-goal-governor/scripts/goal_governor.py formulate \
  --goal "Port S.T.A.L.K.E.R. Complete to OGSR" \
  --test-cmd "wine bin_x64/xrEngine.exe -fsltx fsgame.ltx"
```
The contract defines:
* Explicit test or validation commands with machine-verifiable exit codes (`0`).
* Quantitative acceptance criteria (e.g. 0 linter errors, passing test suites).
* Phased milestone schedule (Architecture $\rightarrow$ Implementation $\rightarrow$ Verification).

### 2. Autonomous 3-Strike Circuit Breaker
When an implementation attempt fails compilation, test execution, or visual verification:
```bash
python3 config/skills/autonomous-goal-governor/scripts/goal_governor.py strike --task "dx11_shaders" --reason "Shader compilation failed: E_FAIL"
```
* **Strike 1 & 2:** Review sanitized error logs (`log-output-sanitizer`), apply targeted adjustment.
* **Strike 3 (Circuit Breaker Tripped):** The governor halts further edits and mandates:
  1. Roll back dirty edits via `working-memory-checkpointing`:
     ```bash
     python3 config/skills/working-memory-checkpointing/scripts/state_checkpoint.py rollback
     ```
  2. Log the failed hypothesis and root cause to `.agents/memory/learnings.md`.
  3. Formulate an alternative hypothesis branch before modifying code again.
  4. Reset strikes once the alternative approach is active:
     ```bash
     python3 config/skills/autonomous-goal-governor/scripts/goal_governor.py reset --task "dx11_shaders"
     ```

### 3. Phased Milestone Compaction
Autonomous goals degrade when context reaches 100k+ tokens because each subsequent tool execution incurs massive prompt costs.
* Divide large goals into 3 distinct phases:
  * **Phase 1: Architecture & Scaffolding**
  * **Phase 2: Core Implementation**
  * **Phase 3: Verification & Hardening**
* Upon completing a phase:
  ```bash
  python3 config/skills/autonomous-goal-governor/scripts/goal_governor.py phase-gate
  ```
* The governor verifies phase assertions, creates a milestone git commit, writes active state to `.agents/memory/activeContext.md`, and prompts for `/compact` to reset token overhead before Phase 2 begins.

### 4. Model Tiering Discipline
* **Phase 1 (Decomposition & Planning):** Escalate to deep reasoning (`Argon` / `pro`) to create the architecture and verifiable contract.
* **Phase 2 & 3 (Execution & Fix Loops):** Confine execution to fast, low-cost models (`Flash` / `Turbo`) using surgical chunk replacements (`replace_file_content`).

### 5. Subagent Depth & Concurrency Caps
* **Max Concurrency:** Never spawn more than 2 parallel subagents simultaneously.
* **Zero Nested Subagents:** Subagents are forbidden from spawning recursive subagents during `/goal` runs to prevent exponential token branching.

### 6. Quota Reserve Watchdog (5-Hour & Weekly Safe Reserves)
Autonomous background processes and test runs actively verify available quota reserves:
```bash
python3 config/skills/autonomous-goal-governor/scripts/goal_governor.py quota-guard --min-5h 15 --min-weekly 10
```
* **Real-Time Telemetry:** Inspects live quota windows (`5h: <rem>% (reset HH:MM)` and `Wk: <rem>%`) across Claude Code (`/tmp/claude_quota_state.json`) and Antigravity (`/tmp/agy_quota_cache.txt`).
* **Emergency Circuit Breaker:** When 5-hour or weekly remaining quota drops to or below safe reserve thresholds:
  1. Halts execution loops immediately (exit code `2`).
  2. Auto-stages active progress to `.agents/memory/activeContext.md`.
  3. Preserves remaining quota for the user, preventing exhaustion before they return.

---

## 🛠️ CLI Reference (`goal_governor.py`)

| Command | Action | Quota Benefit |
| :--- | :--- | :--- |
| `formulate --goal "..."` | Creates verifiable contract and phased plan | Prevents infinite evaluator loops |
| `strike --task "..."` | Logs attempt failure; trips at 3 strikes | Halts trial-and-error doom loops |
| `success --task "..."` | Clears strikes on passing tests | Maintains accurate error budgets |
| `phase-gate` | Completes phase and advises `/compact` | Eliminates 100k+ token per-turn overhead |
| `quota-guard` | Enforces 5-hour & weekly safe reserve thresholds | Prevents quota exhaustion when user is away |
| `status` | Reports active goal, phase, and strikes | Instant statusline visibility |

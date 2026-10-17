---
name: task-velocity-governor
description: Enforces task completion velocity, strict timeboxing, step budgeting, anti-thrashing loops, and diminishing returns boundaries. Prevents tasks from taking longer than necessary and halts iterative wheel-spinning.
---

# Task Velocity & Timeboxing Governor

This skill enforces strict execution velocity, timebox discipline, step budgeting, and anti-thrashing heuristics. It guarantees that engineering tasks conclude promptly without falling into endless iterative loops, over-engineering, or speculative scope creep.

---

## ⚡ 1. The Laws of Task Velocity

### 1. The 5-Step Rule (Targeted Fixes & Small Features)
* Any targeted bug fix, script update, or minor feature must be achievable in **$\le$ 5 operational steps**:
  1. `Locate / Inspect` (find root cause file and line).
  2. `TDD / Verification Harness` (write or run failing test).
  3. `Surgical Replacement` (targeted chunk edit with `replace_file_content`).
  4. `Verification Run` (confirm test passes).
  5. `Deploy / Conclude` (clean checklist status).

### 2. The Diminishing Returns Boundary ("Good Enough" Gate)
* Once the functional requirements are met and tests pass, **conclude immediately**.
* **Prohibited:** Speculative refactoring, unsolicited cosmetic reorganizations, premature abstractions, or adding unrequested hypothetical features.

### 3. The 3-Strike Loop Breaker (File Churn Rule)
* If the same file or test is modified **3 times consecutively** without resolving the issue:
  * **Halt immediately:** You are stuck in a trial-and-error cycle.
  * **Pivot:** Step back, review system logs, formulate a fundamentally different hypothesis, or seek user alignment.

### 4. Game QA & Automated Test Anti-Stall Guardrail
* Long-running game playtests, level smoke runs, and engine simulations must never execute without active stuck detection.
* If a game test produces no log writes for > 60 seconds (log stagnation) or repeats identical action lines > 5 times (infinite loop):
  * **Terminate immediately:** Run `game-test-watchdog watch` or `sweep` to capture window diagnostics and kill the hung process group (`SIGTERM` -> `SIGKILL`).
  * **Triage without stalling:** Extract the stack trace, formulate a targeted fix, and never let the AI assistant hang waiting on an orphaned or frozen game binary.

---

## ⏱️ 2. Autonomous Timebox & Velocity Telemetry

Use `task_velocity_guard.py` to bound long-running tasks:

```bash
# 1. Initialize a governed task (e.g. 8 steps max, 10-minute timebox)
python3 config/skills/task-velocity-governor/scripts/task_velocity_guard.py \
  start "migrate_shader_pipeline" --steps 8 --minutes 10

# 2. Record intermediate steps and monitor loop health
python3 config/skills/task-velocity-governor/scripts/task_velocity_guard.py \
  step "patched vertex shader input layout" --file "shaders/r4/deffer_base.ps"

# 3. Check velocity status
python3 config/skills/task-velocity-governor/scripts/task_velocity_guard.py status

# 4. Conclude task and print velocity efficiency score
python3 config/skills/task-velocity-governor/scripts/task_velocity_guard.py finish
```

---

## 🛡️ 3. Integration with High-Density Protocol

* **Direct Action Over Commentary:** Skip verbal preambles ("Now I will..."). Run the tool directly.
* **Surgical Diffs:** Never rewrite a 500-line file when a 4-line patch fixes the root cause.
* **Deterministic Verification:** If the compiler or test suite passes, declare victory and conclude.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`superpowers`**: Core engineering methodology and discipline engine. Use when starting non-trivial tasks to evaluate if brainst...
- **`argon-atomic-diff-sequencer`**: Enforces Claude-grade atomic chunk editing on Gemini 4 Argon. Restricts all code changes to surgical <= 30-lin...
- **`executing-plans`**: Step-by-step execution of approved implementation plans. Use when executing a multi-step plan to track progres...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

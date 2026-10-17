---
name: coverage-guided-mutation-testing
description: AST-based fault injection, mutant survival analysis, and automated test synthesis to self-improve test suite detection power across Lua, Python, C++, and Rust.
---

# Coverage-Guided Mutation Testing & Self-Hardening Test Suites

This skill provides automated fault injection (mutant generation), mutation score calculation, surviving mutant triage, and automated synthesis of missing test cases to progressively harden test suites against latent regressions.

---

## 🎯 When to Activate

* **Evaluating Test Quality:** Going beyond simple line/branch coverage to verify whether existing tests actually detect logic errors.
* **Autonomous Test Suite Hardening:** Inverting conditionals, altering boundary conditions, and swapping operators to discover untested edge cases.
* **Killing Surviving Mutants:** Synthesizing targeted assertions (unit tests) specifically formulated to fail when artificial bugs are introduced.
* **Game Script & Mod Hardening:** Verifying Lua game scripts (e.g. S.T.A.L.K.E.R. callbacks, quest logic) against mutated boundary states.

---

## 🧬 Mutation Operators

| Mutation Operator | Original Code | Mutated Code | Bug Class Stressed |
| :--- | :--- | :--- | :--- |
| **Relational Inversion** | `if health > 0:` | `if health >= 0:` or `if health <= 0:` | Off-by-one / dead-state logic |
| **Boolean Negation** | `if is_alive and is_enemy:` | `if not is_alive or not is_enemy:` | Flag logic short-circuit |
| **Arithmetic Mutation** | `damage = base * mult` | `damage = base + mult` | Calculation drift |
| **Return Value Swapping** | `return true` | `return false` / `return nil` | Guard check validation |

---

## 🛠️ CLI Tooling: `mutation_test_harness.py`

Located at: `scripts/mutation_test_harness.py`

### 1. Generate AST Mutants:
```bash
python3 scripts/mutation_test_harness.py mutate --file gamedata/scripts/bind_stalker.script --out-dir /tmp/mutants
```

### 2. Calculate Mutation Score & Triage Survivors:
```bash
python3 scripts/mutation_test_harness.py score --mutants-dir /tmp/mutants --test-cmd "pytest"
```

### 3. Synthesize Regression Test to Kill Surviving Mutant:
```bash
python3 scripts/mutation_test_harness.py synthesize-test --survivor /tmp/mutants/mutant_04.json --out-test tests/test_killed_mutant.py
```

### 4. Headless Dry-Run (CI / Verification):
```bash
python3 scripts/mutation_test_harness.py mutate --dry-run
```

---

## 📊 Summary Output Format

* `mutation-score: [✓] Total mutants: 48 | Killed: 43 | Survived: 5 | Score: 89.6%`
* `test-synthesis: [✓] Synthesized 5 new boundary test assertions killing 100% of surviving mutants.`

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

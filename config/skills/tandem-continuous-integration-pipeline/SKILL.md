---
name: tandem-continuous-integration-pipeline
description: Automated pre-merge staging pipeline that compiles and smoke-tests unified Argon and Fable branches before merging into main.
---

# Tandem Continuous Integration Pipeline (`tandem-continuous-integration-pipeline`)

When Gemini 4 Argon produces assets and configurations while Claude Fable refactors C++ engine code concurrently, merging both directly into `main` without integration testing can result in broken builds or runtime crashes.

This skill provides an automated, non-interactive integration test gate that compiles the combined branch and executes a fast smoke test before declaring milestones complete.

---

## 1. Staging Workflow Architecture

```
feat/argon-work  ----\
                      +---> staging/tandem-test ---> [ Clean Build & Smoke Test ] ---> main
feat/fable-work  ----/                                (Process Exit Code: 0)
```

---

## 2. Automated Integration Test Script

```bash
# 1. Switch to staging test branch
git checkout -B staging/tandem-test main

# 2. Merge both agent branches non-interactively
git merge feat/argon-work --no-edit -m "ci: merge Argon changes for integration test"
git merge feat/fable-work --no-edit -m "ci: merge Fable changes for integration test"

# 3. Parallel Compilation with all CPU cores
cmake --build build -j$(nproc) 2>&1 | token-guard --lines 30

# 4. Fast 30-Second Headless Smoke Test
timeout 30s ./bin/game_engine -nowait -nosound 2>&1 | tail -n 20 || [ $? -eq 124 ]

# 5. Fast-Forward Main only if smoke test passes
git checkout main
git merge staging/tandem-test --ff-only
git branch -D staging/tandem-test
```

---

## 3. Failure Quarantine Protocol

If the integration build fails:
1. **Never Pollute Main:** The staging branch is kept in quarantine; `main` remains 100% clean and working.
2. **Assign Defect to Responsible Agent:**
   - Compiler syntax/link errors -> Dispatched to Fable (`tandem-dispatch --to fable`).
   - Missing textures, audio path typos, or LTX parsing errors -> Dispatched to Argon (`tandem-dispatch --to argon`).

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

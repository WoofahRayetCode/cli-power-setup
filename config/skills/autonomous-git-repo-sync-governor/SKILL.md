---
name: autonomous-git-repo-sync-governor
description: Autonomous git repository synchronization, upstream pull/rebase, milestone auto-commit, large-binary/secret pre-commit filtering, and multi-repo fleet updates across ~/Documents/GitHub during long sessions and general development.
---

# Autonomous Git Repository Sync & Milestone Governor (`autonomous-git-repo-sync-governor`)

## When to Use
- **During Long Autonomous Sessions (`/goal`, `agy-yolo`, `claude-yolo`, `tandem-yolo`):** Automatically committing and pushing verified milestones so progress is never lost in uncommitted dirty worktrees.
- **General Development & Multi-Repo Workflows:** Keeping the active workspace and dependent repos (e.g., `cli-power-setup`, `ogsr-complete-merge`, `OGSR-Engine`, `zoneforge`, `rea`) synchronized with `origin` without manual git housekeeping.
- **Pre-Compaction & Session Handoff:** Ensuring all verified changes are committed and pushed (or safely checkpointed) before running `/compact`.

---

## 1. Closed-Loop Repo Synchronization Lifecycle

```mermaid
flowchart LR
    A["Start Task / Session"] --> B["repo-auto-sync --pull <repo> (Autostash Rebase)"]
    B --> C["Execute Code / Mod / Skill Changes"]
    C --> D["Verify Build & Tests Pass"]
    D --> E["repo-auto-sync --checkpoint <repo> --push"]
    E --> F{"More Milestones?"}
    F -- "Yes" --> C
    F -- "No / Compaction" --> G["Clean Synced Repo on GitHub"]
```

---

## 2. `repo-auto-sync` CLI Reference (`~/.local/bin/repo-auto-sync`)

| Command | Action |
| :--- | :--- |
| `repo-auto-sync --status [repo]` | Shows branch, ahead/behind remote counts, and dirty file tally. |
| `repo-auto-sync --pull [repo]` | Safely runs `git fetch` + `git pull --rebase --autostash` if behind `origin`. |
| `repo-auto-sync --checkpoint [repo] -m "feat: ..." --push` | Creates/updates `.gitignore`, synchronizes `README.md` skill/tool tables, filters `>50MB` binaries, commits, and pushes to `origin`. |
| `repo-auto-sync --ensure-gitignore [repo]` | Creates or updates `.gitignore` with Python, Blender (`*.blend1`), `.env`, and `>50MB` exclusions. |
| `repo-auto-sync --update-readme [repo]` | Updates `README.md` live skill counts (`301`), CLI tool tables, and auto-indexed skill catalog. |
| `repo-auto-sync --fleet-status` | Scans all 30 repositories in `~/Documents/GitHub/` in parallel (`<0.5s`) showing branch, dirty count, and ahead/behind status. |
| `repo-auto-sync --fleet-pull` | Fast-forwards all clean repositories in `~/Documents/GitHub/` that have upstream updates waiting on GitHub. |

---

## 3. Mandatory Safety, `.gitignore` & `README.md` Guardrails
1. **Automatic `.gitignore` Creation & Oversized File Shield (`50 MB` Hard Cap):**
   - `repo-auto-sync --checkpoint` automatically creates or updates `.gitignore` (`__pycache__/`, `*.py[cod]`, `*.blend1`, `.env`, `.DS_Store`, `.agents/`), unstages any accidental file `> 50 MB` (e.g., `.db`, `.pak`, `.utoc`), and appends its relative path directly to `.gitignore` so it never pollutes `git status` again.
2. **Automatic `README.md` Synchronization:**
   - Every `--checkpoint` automatically updates `README.md` so skill counts (`301`), Cursor rule counts, CLI tool tables, and newly evolved skills are always documented on GitHub without manual editing.
3. **Verify Before Pushing:**
   - Only run `--checkpoint --push` after syntax checks (`local-ast-compiler` / `luac -p` / `py_compile`) or build/test checks succeed.
4. **Detached HEAD Protection:**
   - If a repository is in `detached HEAD` state, `repo-auto-sync` warns and skips blind pushing so worktree branches remain authoritative.

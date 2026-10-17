---
name: cross-agent-git-rebase-guard
description: Automated git worktree synchronization, non-interactive rebasing, and conflict-free merging between concurrent AI agent feature branches.
---

# Cross-Agent Git Rebase Guard (`cross-agent-git-rebase-guard`)

When Gemini 4 Argon dispatches parallel Gemini Flash subagents into isolated git worktrees (`argon-hierarchical-worktree-isolator` with `Workspace="share"` or `Workspace="branch"`), merging feature branches naively can trigger interactive editor prompts, merge conflicts, or dirty working directory locks.

This skill governs non-interactive, automated branch merging and rebase synchronization across Argon and Flash subagent branches.

---

## 1. Clean Synchronization Workflow

```
feat/flash-assets  ----[ Commit A1 ]----[ Commit A2 ]----+
                                                         | (Clean Merge)
main               --------------------------------------+----> [ Unified Main ]
                                                         |
feat/argon-engine  ----[ Commit E1 ]----[ Commit E2 ]----+
```

---

## 2. Non-Interactive Merge Commands

When integrating concurrent subagent work back to `main`:

```bash
# 1. Switch to root repository
cd /path/to/project-root

# 2. Ensure working directory is clean
git status --porcelain

# 3. Merge Flash subagent asset/config branch with automated commit message
git merge feat/flash-assets --no-edit -m "merge: integrate Flash subagent LTX and asset enhancements"

# 4. Merge Argon engine branch
git merge feat/argon-engine --no-edit -m "merge: integrate Argon 64-bit C++ engine refactors"

# 5. Checkpoint, update README/.gitignore, and push unified main to remote
repo-auto-sync . --checkpoint -m "chore(release): sync merged subagent branches" --push
```

---

## 3. Conflict Prevention Guardrails

1. **Commit Early, Commit Atomic (`autonomous-git-repo-sync-governor`):** Each subagent must commit atomic milestones rather than leaving dozens of uncommitted files sitting in working trees.
2. **Rebase Onto Main Post-Merge:**
   Once `main` is updated:
   ```bash
   git fetch origin && git rebase main
   ```
3. **Never Force Push (`--force`):** Always use standard fast-forward or non-interactive merge commits to preserve subagent execution history.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All git sync and worktree commands (`repo-auto-sync`, `agy-cheatsheet` / `cs`) run natively on Windows 10/11 and Linux.


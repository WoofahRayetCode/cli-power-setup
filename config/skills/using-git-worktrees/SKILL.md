---
name: using-git-worktrees
description: Manages isolated git worktrees for parallel mod development, experimenting with risky changes, or testing multiple branches simultaneously without dirtying the working directory.
---

# Git Worktrees for Isolated Modding & Development

Use this skill when developing experimental features, testing conflicting mod configurations, or making changes while keeping the primary workspace untouched.

## Why Use Worktrees for Modding
- Modding often requires building, packing, or testing against live game directories.
- Switching branches in a dirty working directory can overwrite game files or cause stash conflicts.
- Worktrees provide separate filesystem directories linked to the same repository and `.git` database.

## Operating Commands

### 1. Creating a Worktree
```bash
# Create a new branch in a dedicated sibling directory
git worktree add ../<repo-name>-<feature-branch> -b <feature-branch>

# Or check out an existing branch into a worktree
git worktree add ../<repo-name>-<branch> <branch>
```

### 2. Listing Active Worktrees
```bash
git worktree list
```

### 3. Cleaning Up After Verification
Once changes are merged or discarded:
```bash
# Remove the worktree folder
git worktree remove ../<repo-name>-<feature-branch>

# Prune stale administrative records
git worktree prune
```

## Safety Checklist
- Never delete a worktree directory using raw `rm -rf` without running `git worktree remove` or `git worktree prune`.
- Do not run worktrees inside the repository's tracked folders—always place them in sibling directories or `/tmp/`.
- **Automated Worktree Sync & Subagent Isolation (`autonomous-git-repo-sync-governor`, `argon-hierarchical-worktree-isolator` & `dynamic-repo-model-cheatsheet`):**
  - When Argon spawns parallel Flash worker subagents with `Workspace="share"` or `Workspace="branch"`, or when working in sibling feature worktrees, use `repo-auto-sync <worktree> --checkpoint --push` to harden `.gitignore` against `>50 MB` build artifacts and update `agy-cheatsheet` (`cs`) with live model recommendations.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

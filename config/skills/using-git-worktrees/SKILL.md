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
- **Automated Worktree Sync & Cheat Sheet Indexing (`autonomous-git-repo-sync-governor` & `dynamic-repo-model-cheatsheet`):**
  - Use `repo-auto-sync <worktree> --checkpoint --push` inside sibling worktrees (e.g. `ogsr-complete-merge-argon` and `ogsr-complete-merge-fable`) to harden `.gitignore` against `>50 MB` build artifacts and update `agy-cheatsheet` (`cs`) with per-worktree model recommendations.


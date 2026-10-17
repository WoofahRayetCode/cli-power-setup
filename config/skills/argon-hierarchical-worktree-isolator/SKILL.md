---
name: argon-hierarchical-worktree-isolator
description: Sandboxes concurrent subagent file modifications into isolated git worktrees, preventing file lock collisions and allowing atomic integration by Argon.
---

# Argon Hierarchical Worktree Isolator (`argon-hierarchical-worktree-isolator`)

When Gemini 4 Argon dispatches parallel subagents to apply edits or compile assets simultaneously, executing in the shared root repository causes:
- File-write race conditions (subagents clobbering each other's edits).
- Build directory locks (`CMakeCache.txt`, `build.ninja` lock contention).
- Dirty git working trees that prevent clean rollbacks.

This skill governs the automatic provisioning of ephemeral git worktrees for subagents.

---

## 1. Subagent Workspace Architecture

```
+-------------------------------------------------------------+
| Primary Workspace: Argon Orchestrator                       |
+-------------------------------------------------------------+
                 /                           \
(Workspace="branch")                       (Workspace="branch")
               v                               v
+-----------------------------+ +-----------------------------+
| Subagent Workspace A        | | Subagent Workspace B        |
| - Branch: subagent/task-1   | | - Branch: subagent/task-2   |
| - Isolated build/ directory | | - Isolated build/ directory |
| - Independent file edits    | | - Independent file edits    |
+-----------------------------+ +-----------------------------+
                 \                           /
                  \                         /
                   v                       v
+-------------------------------------------------------------+
| Atomic Merge into Orchestrator Branch upon Verification     |
+-------------------------------------------------------------+
```

---

## 2. Invocation Directives

When launching code-modifying subagents via `invoke_subagent`:

```json
{
  "Subagents": [
    {
      "TypeName": "self",
      "Role": "Shader Modernizer",
      "Model": "flash",
      "Workspace": "branch",
      "Prompt": "Port legacy DX9 shaders to DX11 in your isolated branch and verify with spirv-val."
    }
  ]
}
```

- **`Workspace="branch"`:** Creates an isolated git worktree cloned from the parent's current commit.
- **`Workspace="share"`:** Shares repository object storage without duplicating disk space (similar to `git-worktree`), allowing fast branch creation in < 100ms.

---

## 3. Integration & Teardown

1. When the subagent succeeds, it returns the commit hash or diff coordinates in its compressed return envelope.
2. Argon reviews the diff via `argon-adversarial-verification-gate`.
3. Argon performs a fast-forward merge into the primary working tree:
   ```bash
   git merge subagent/task-1 --ff-only
   ```
4. The subagent workspace is deleted automatically upon task completion.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

## Related & Interoperating Skills
- **`cross-agent-git-rebase-guard`**: Automated git worktree synchronization, non-interactive rebasing, and conflict-free merging between concurrent...
- **`argon-dynamic-subagent-swarm`**: Spawns and coordinates parallel Gemini Flash worker subagents to execute high-volume asset conversion, audio p...
- **`argon-subagent-dispatch-routing`**: Implements the 'Argon Brain, Flash Hands' subagent swarm dispatch pattern to offload high-volume read, search,...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

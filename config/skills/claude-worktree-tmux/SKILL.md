---
name: claude-worktree-tmux
description: Native Claude Code background session and tmux pane isolation, running heavy builds, test suites, and long tasks in detached worktrees without context pollution.
---

# Claude Native Worktree & Tmux Session Isolation

This skill leverages Claude Code's native support for git worktrees (`-w, --worktree`), tmux panes (`--tmux`), and background detached agents (`claude --bg`, `claude attach`, `claude logs`) to isolate heavy compilation, long test runs, or complex research tasks outside the primary conversation context.

---

## 🖥️ 1. Native Claude CLI Flags

Claude Code has built-in primitives for parallel task execution:

```bash
# 1. Launch a parallel session in a named git worktree
claude -w feature-physics

# 2. Launch an isolated session inside a native tmux pane
claude -w feature-audio --tmux

# 3. Launch a detached background session for a long task
claude --bg -p "Run full pytest suite and write failures to /tmp/failures.log"
# (Outputs a short ID, e.g. agent-a4f)

# 4. Check background session logs without entering the session
claude logs agent-a4f

# 5. Re-attach to the background session when needed
claude attach agent-a4f
```

---

## 🛡️ 2. Protecting the Main Context Window

When a user requests a heavy, long-running task (e.g. compiling a C++ game engine, unpacking large game archives, or running a 10-minute test suite):

1. **Do NOT run it inline in the main chat:** Dumping 500 lines of terminal output into your main chat permanently pollutes your context window.
2. **Dispatch to a detached background agent:**
   ```bash
   claude --bg -p "cmake --build build --parallel && ctest"
   ```
3. **Monitor via exit status:** Check status or log summary, keeping the primary chat window lean, fast, and responsive.

---

## 🔄 Interoperability & Handoffs

* **Handoff to `subagent-swarm-orchestrator`:** For coordinating multi-agent JSON communication.
* **Handoff to `using-git-worktrees`:** For low-level git worktree pruning and branch removal.
* **Handoff to `token-economy`:** Prevents massive build logs from entering the active transcript.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

---
name: subagent-swarm-orchestrator
description: Coordinates autonomous parallel subagent swarms in Claude Code, leveraging isolated git worktrees, background processes, and parent-child JSON messaging pipelines.
---

# Subagent Swarm Orchestrator

This skill brings Antigravity-style autonomous multi-agent swarms into Claude Code, orchestrating parallel worker tasks across isolated sandboxes.

---

## 🐝 Architecture: Swarm Hierarchy

```
       [Parent Orchestrator (Claude Code)]
            /            |            \
 [Worker 1: Linter] [Worker 2: Tests] [Worker 3: Docs]
   (Worktree A)       (Worktree B)       (Worktree C)
```

---

## 🛠️ 1. Parallel Task Dispatch via Worktrees

To run parallel sub-agents without file collision or git conflicts:

```bash
# 1. Create isolated worker worktrees
git worktree add -b worker-test .worktrees/worker-test
git worktree add -b worker-lint .worktrees/worker-lint

# 2. Launch detached background workers
(cd .worktrees/worker-test && pytest > test_results.json 2>&1) &
PID_TEST=$!

(cd .worktrees/worker-lint && ruff check . > lint_results.json 2>&1) &
PID_LINT=$!

# 3. Non-blocking parent harvest
wait $PID_TEST $PID_LINT
```

---

## 📨 2. JSON IPC Message Schema

Subagents report progress back to the parent orchestrator via standard JSON files:

```json
{
  "worker_id": "worker-unit-tests",
  "status": "COMPLETED",
  "exit_code": 0,
  "summary": "All 42 tests passed in 1.4s",
  "artifacts": [".worktrees/worker-test/report.html"],
  "blockers": []
}
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `using-git-worktrees`:** For low-level worktree lifecycle and branch cleanup.
* **Handoff to `subagent-code-reviewer`:** For dispatching dedicated code-review subagents before merging.\n

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`claude-worktree-tmux`**: Native Claude Code background session and tmux pane isolation, running heavy builds, test suites, and long tas...
- **`cross-agent-git-rebase-guard`**: Automated git worktree synchronization, non-interactive rebasing, and conflict-free merging between concurrent...
- **`argon-subagent-payload-compressor`**: Enforces high-density structured return envelopes on Gemini subagent messages, eliminating conversational fluf...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

---
name: argon-subagent-lifecycle-governor
description: Prevents zombie hangs, infinite loops, and interactive prompt blocking in Gemini subagents with deterministic timeouts and automated process cleanup.
---

# Argon Subagent Lifecycle Governor (`argon-subagent-lifecycle-governor`)

When Gemini 4 Argon dispatches background subagents (`invoke_subagent`), subagents execute asynchronously. If a subagent invokes an interactive command (e.g. `apt-get` waiting for `[Y/n]`, an interactive debugger, or an uncapped `find` command), the subagent can hang indefinitely in the background, consuming memory and failing to return results to the parent orchestrator.

This skill establishes deterministic lifecycle management, timeout bounding, and zombie process cleanup for all subagents.

---

## 1. Subagent Execution Guardrails

1. **Non-Interactive Shell Enforcements:**
   - Every shell invocation within a subagent must set non-interactive environment flags:
     ```bash
     export DEBIAN_FRONTEND=noninteractive
     export PAGER=cat
     export CI=true
     ```
2. **Deterministic Timeouts:**
   - Long-running commands (compilations, archive extractions, test suites) must be wrapped with an explicit `timeout` command:
     ```bash
     timeout 180s ./run_heavy_test.sh || [ $? -eq 124 ]
     ```
3. **State Polling Avoidance:**
   - Argon relies on reactive wakeups. Never loop calling `manage_subagents(Action="list")` in tight circles; let the system message notification resume execution when the subagent completes.

---

## 2. Subagent Heartbeat & Circuit Breaker

If a subagent has not reported back within its allotted operational window:
1. Check subagent health using `manage_subagents(Action="list")`.
2. If state is `errored` or frozen in `waiting_for_input`, terminate the subagent immediately:
   ```json
   manage_subagents({
     "Action": "kill",
     "ConversationIds": ["<hung_subagent_id>"]
   })
   ```
3. Re-route the task with simplified parameters or escalate to direct execution on the parent agent.

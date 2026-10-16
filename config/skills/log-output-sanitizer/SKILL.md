---
name: log-output-sanitizer
description: Intercepts noisy compiler, package manager, and test suite terminal output (cargo, pytest, npm, cmake), passing only actionable errors and compact summaries to preserve context.
---

# Log Output Sanitizer & Terminal Stream Token Filter

This skill prevents runaway terminal output from polluting the conversation history. In raw command executions, tools like `cargo build`, `pytest`, `npm install`, and `cmake` routinely output hundreds of lines of passing checks and progress bars. Once in history, you pay for those tokens on every subsequent turn.

---

## 🛡️ Core Rules

1. **Never Pipe Noisy Unfiltered Commands:** Avoid raw verbose commands when checking build health or running suites.
2. **Compact Flags First:**
   * `pytest`: Use `pytest -q --tb=short` or filter with `-k <test_name>` instead of default verbose tables.
   * `cargo`: Use `cargo check --message-format=short` or `cargo test -- --nocapture` only when debugging specific failures.
   * `npm / yarn`: Append `--silent` or `--loglevel error` to package installations.
   * `cmake / make`: Run with `-s` (silent) or pipe through `grep` when verifying compilation.
3. **Capture & Tail Failures:** When a long command produces 500+ lines of output, pipe to a temporary log file and print only the last 30 lines or targeted errors:
   ```bash
   ./build.sh > /tmp/build.log 2>&1 || tail -n 30 /tmp/build.log
   ```

---

## 📊 Summary Output Format

When reporting command results in chat, summarize into 1-line indicators:
* `cargo check: [✓] 0 errors, 2 warnings (clean)`
* `pytest: [✓] 42 passed, 0 failed in 1.12s`
* `npm install: [✓] 3 packages added, audit clean`

---

## 🔄 Interoperability & Handoffs

* **Handoff to `token-economy`:** Enforces the Silent Tool Success principle across all CLI tool calls.
* **Handoff to `systematic-debugging`:** When a command fails, inspect `/tmp/build.log` targeting only the specific line containing the error or panic backtrace.

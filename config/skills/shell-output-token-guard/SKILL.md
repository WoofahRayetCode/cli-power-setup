---
name: shell-output-token-guard
description: Enforces hard terminal stdout line ceilings using token-guard to intercept noisy commands (find, grep, git log, compiler dumps), truncating runaway output and saving 10k-50k tokens per query.
---

# Shell Output Token Guard (`shell-output-token-guard`)

When executing shell commands (`run_command`, terminal tasks), unconstrained stdout streams (e.g. `grep -rn`, `find`, `git log`, `ls -R`, verbose build logs) can easily dump 1,000 to 10,000 lines of text into the conversation history.

A single 5,000-line terminal dump permanently bloats the active conversation by **~40,000 tokens**, accelerating context degradation and triggering premature 5-hour quota exhaustion.

The `shell-output-token-guard` skill eliminates this risk by mandating output containment via `token-guard`.

---

## 1. The `token-guard` CLI Wrapper

The utility is installed at `~/.local/bin/token-guard`:

```bash
# Wrap any command that might produce unpredictable or voluminous output
token-guard <command> [args...]

# Customize line ceiling (default is 30 lines)
token-guard --max-lines 50 <command>
```

### Behavior:
1. **Preserves Head:** Displays the first 25 lines of output so the agent sees initial matches or startup headers.
2. **Suppresses Mid-Section:** Intercepts and discards repetitive lines.
3. **Preserves Tail:** Retains the final 5 lines containing completion status, error summaries, or exit tallies.
4. **Context Savings Telemetry:** Displays exact lines truncated and estimated tokens saved from context:
   ```text
   [⚠️ token-guard: 3,420 lines truncated | ~27,360 tokens saved from context]
   ```

---

## 2. Command Rules

| Unsafe Direct Execution (Prohibited) | Safe Guarded Execution (Enforced) |
| :--- | :--- |
| `grep -rn "pattern" .` | `token-guard grep -rn "pattern" .` |
| `find . -name "*.ltx"` | `token-guard find . -name "*.ltx"` |
| `git log -p` | `token-guard git log --oneline -n 20` |
| `ctest --output-on-failure` | `token-guard ctest --output-on-failure` |
| `nm -D binary.so` | `token-guard nm -D binary.so` |

---

## 3. High-Density Integration with Agents

- **Zero-Waste Lookups:** When searching wide directories for unknown symbols or files, agents must always prefix exploratory commands with `token-guard`.
- **Targeted Drilling:** If `token-guard` indicates matches were truncated, the agent narrows its search pattern (e.g. adding subdirectory or file extension filters) rather than re-running wide unconstrained queries.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`yolo-autonomous-watchdog`**: Autonomous execution watchdog and quota protector for YOLO modes (claude-yolo, agy-yolo). Prevents infinite re...
- **`log-output-sanitizer`**: Intercepts noisy compiler, package manager, and test suite terminal output (cargo, pytest, npm, cmake), passin...
- **`context-window-governor`**: Deterministic token budgeting, turn-by-turn context partitioning, and hard output containment to prevent tool ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

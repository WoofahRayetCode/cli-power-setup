---
name: agy-context-telemetry
description: Deep context window utilization and token cost inspector for Antigravity CLI (parity with claude /context and claude /cost). Tracks step-by-step cache efficiency, prompt overhead, model token splits, and dollar value savings.
---

# Antigravity Context & Cost Inspector (`agy-context-telemetry`)

Provides complete parity with Claude Code's native `/context` and `/cost` commands. Inspects the active conversation trajectory to reveal exact token distributions, prompt cache hit rates, capacity headroom, and estimated dollar savings.

---

## When to Use

- When monitoring active context growth during complex multi-step refactors or `/goal` runs.
- When determining whether it is time to run `/compact`.
- To audit prompt cache efficiency and verify that prefixes are remaining stable.
- To analyze step-by-step token consumption across tool executions.

---

## Telemetry Capabilities

1. **Step Trajectory Audit:**
   - Displays a breakdown table of recent turns showing uncached input tokens, cached prefix tokens, output tokens, and per-step cache hit rates.
2. **Context Window Saturation:**
   - Tracks current capacity against Gemini 4 Argon's 1,000,000 token window.
   - Flags an automatic warning when context reaches or exceeds 50% capacity.
3. **Monetary Savings Calculation:**
   - Compares standard full-price token billing against the 90% prompt caching discount.
   - Calculates real-time estimated dollar savings.

---

## Quick CLI Execution

```bash
# Inspect current session context and token savings
agy-context

# Show recent 20 steps
agy-context --turns 20

# Output structured JSON for automation
agy-context --json
```

## Live Statusline & Cheat Sheet Integration (`dynamic-repo-model-cheatsheet`)
- Works alongside `agy-quota-statusline`, which renders real-time token/cache metrics on top and the live 2-bar **Model & Reasoning Cheat Sheet** (`🧭 CS [...]` + `📚 Repos: ...`) at the bottom of your terminal.
- Run `agy-cheatsheet` (or `cs`) to inspect the full 32-repository routing matrix across `~/Documents/GitHub/`.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** `agy-context`, `agy-quota-statusline`, and `agy-cheatsheet` (`cs`) run natively on Windows 10/11 (`.cmd` shims in `$HOME\.local\bin`) and Linux.


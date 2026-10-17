---
name: agy-cli-doctor
description: System diagnostics and environment verification for Antigravity CLI (parity with claude doctor). Validates binary health, settings.json permissions, SQLite conversation database integrity, model endpoint connectivity, and quota locks.
---

# Antigravity CLI Doctor & Diagnostics (`agy-cli-doctor`)

Provides complete parity with Claude Code's native `claude doctor` command. Inspects and audits the local runtime, permissions whitelist, conversation persistence databases, and cloud API connectivity.

---

## When to Use

- When encountering runtime errors, unexpected permission prompts, or command execution failures.
- When verifying that Google Cloud Code API endpoints are reachable.
- When checking SQLite database integrity in `~/.gemini/antigravity-cli/conversations/`.
- To clean up stale statusline lock files (`/tmp/agy_quota_refresh.lock`).

---

## Diagnostic Scope

1. **CLI Executable & Environment:**
   - Verifies `agy` location in `$PATH`, subcommands availability, and runtime exit codes.
2. **Settings & Permissions Audit:**
   - Validates `~/.gemini/antigravity-cli/settings.json`.
   - Counts whitelist entries and checks configured model.
3. **SQLite Conversation Database Integrity:**
   - Executes `PRAGMA integrity_check;` across recent session databases to prevent database corruption.
4. **Cloud API Connectivity:**
   - Validates reachability of Gemini 4 Argon, Gemini 3.8 Flash, and Claude Sonnet/Opus model endpoints.
5. **Lock & Cache Self-Healing:**
   - Detects and clears stale quota refresh locks (>60s old) to keep statusline telemetry fresh.

---

## Quick CLI Execution

```bash
# Run complete system health check
agy-doctor
```

## 3. Hardware Offload, Cheat Sheet & Skill Audit Integration
- `agy-doctor` also verifies:
  - `~/.cli_power_setup/repo_cheatsheet.json` (`dynamic-repo-model-cheatsheet` / `cs`) and `~/.cli_power_setup/token_ledger.json` symlinks.
  - Hybrid GPU render nodes (`/dev/dri/renderD128` RTX 5060 dGPU + `/dev/dri/renderD129` Radeon 610M iGPU via `amd-igpu-nvidia-dgpu-hybrid-offload`) and `/dev/shm` tmpfs (`ramdisk-tmpfs-build-bake-accelerator`).
- Pair with `skills-audit-update --audit` and `repo-auto-sync --fleet-status` for full workspace health verification.


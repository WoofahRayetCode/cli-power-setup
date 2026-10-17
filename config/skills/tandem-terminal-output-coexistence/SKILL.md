---
name: tandem-terminal-output-coexistence
description: Prevents runaway terminal scrolling, stdout floods, and pane noise in the 3-column tandem layout using token-guard and compact statuslines.
---

# Tandem Terminal Output Coexistence (`tandem-terminal-output-coexistence`)

In a 3-column side-by-side terminal layout (Argon, Fable, Dispatch Console), if one agent executes a verbose command (e.g. `cmake --build`, `git log`, or raw `retoc unpack` listing 50,000 files), its pane floods with thousands of lines per second.

This runaway output obscures statuslines, strains GPU terminal rendering, and clutters the visual field while the game window is running.

This skill integrates `shell-output-token-guard` directly into the tandem layout to maintain clean, high-density terminal coexistence.

---

## 1. Coexistence Directives

### 1. Mandatory Piping to Token Guard
When running high-volume CLI commands in either agent pane:
```bash
# Bad: Floods 10,000 lines into the 3-column pane
cmake --build build -j$(nproc)

# Good: Clamped to 50 lines max with clear exit status
cmake --build build -j$(nproc) 2>&1 | token-guard --lines 50
```

### 2. Quiet Flag Enforcement
Always pass quiet/compact flags when executing package managers and build tools:
- `ninja` instead of raw `make` (progress ticker on a single line).
- `pytest -q --tb=short` instead of verbose test listings.
- `cargo test -- -q` for Rust tests.
- `retoc unpack ... -q` or redirecting stdout to log files: `retoc unpack ... > /tmp/retoc.log 2>&1`.

---

## 3. High-Density Statusline Protection

Both agent panes run their respective statusline utilities:
- Left Pane (Argon): `agy-quota-statusline` (showing 5h quota, weekly quota, and 95% cache hits).
- Middle Pane (Fable): `claude-statusline` (showing Claude context fuel and token costs).
- Right Pane: Active command prompt for `tandem-dispatch`.

By clamping command noise, both statuslines remain continuously readable at a glance without scrolling.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

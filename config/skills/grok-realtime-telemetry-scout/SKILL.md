---
name: grok-realtime-telemetry-scout
description: Emulates xAI Grok real-time live search on Gemini 4 Argon. Scouts bleeding-edge git commits, pull requests, issue trackers, and package feeds for undocumented Linux and game fixes.
---

# Grok Real-Time Telemetry Scout (`grok-realtime-telemetry-scout`)

xAI Grok's signature strength is its connection to raw, real-time data feeds, allowing it to surface solutions from fresh developer commits, GitHub pull requests, and bleeding-edge forum discussions before they appear in static documentation.

This skill equips Gemini 4 Argon with real-time scout capabilities to discover undocumented fixes for Proton, Wine, Vulkan, and Linux game engine crashes.

---

## 1. Real-Time Scouting Protocol

When standard documentation or code inspection fails to resolve an obscure Linux/Wine defect:

### 1. Upstream GitHub Commit & PR Scouting
Query upstream engine repositories for recent unreleased commits:
```bash
# Search recent commits in upstream OGSR / X-Ray for crash keywords
git log --all --grep="segfault" --grep="crash" -n 5 --oneline

# Search open and closed upstream PRs via gh CLI
gh pr list --state all --search "save crash" --limit 5
```

### 2. Arch Linux AUR & CachyOS Package Diffing
Check bleeding-edge packaging PKGBUILD patches for custom Wine / DXVK overrides:
```bash
# Inspect upstream patch files in AUR or CachyOS repos
curl -s "https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=wine-ge-custom" | grep -iE "patch|export" | head -20
```

---

## 2. Invariant Directives

1. **Focus on Raw Commits Over Opinions:** Prioritize exact code commit diffs and closed issue resolutions over forum opinions.
2. **Token Economy Scrape:** Never dump full HTML pages into context. Pipe web search and curl results through `token-guard` or `grep` to extract only technical patch snippets (< 30 lines).

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

## Related & Interoperating Skills
- **`devin-environment-self-healer`**: Emulates Cognition Devin autonomous environment self-healing. Automatically diagnoses missing host dependencie...
- **`linux-gaming-proton-optimization`**: Optimizing and fixing games under Linux, Wine, Steam Proton, and Steam Deck. Covers GE-Proton switching, dxvk....
- **`autogen-adversarial-redteam-critic`**: Emulates Microsoft AutoGen multi-persona red-teaming. Executes an internal Devil's Advocate audit to aggressiv...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

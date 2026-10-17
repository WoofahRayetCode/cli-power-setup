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

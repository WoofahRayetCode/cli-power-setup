---
name: dynamic-repo-model-cheatsheet
description: Dynamic terminal cheat sheet (agy-cheatsheet / cs) and live statusline recommender that scans ~/Documents/GitHub repositories, uncommitted diffs, recent commits, and error states to recommend the optimal Model + Reasoning Effort + Local Hardware Offload.
---

# Dynamic Repo-Aware Model & Reasoning Cheat Sheet (`dynamic-repo-model-cheatsheet`)

Provides a live, self-updating terminal cheat sheet (`agy-cheatsheet` / `cs`) and statusline indicator (`🎯 Rec: ...`) that inspects all projects in `~/Documents/GitHub/` alongside your active working tree to recommend the exact **Model Tier**, **Reasoning Effort**, and **Local CPU/GPU/RAM Offload** for what you are working on right now.

## 1. How It Works & Dynamically Adapts

Unlike a static reference table, `agy-cheatsheet` recalculates recommendations in real time using four signals:
1. **Active Uncommitted Work (`git status --porcelain` + directory walking):**
   - Inspects the exact file extensions you are modifying right now.
   - Example: Editing `.ltx`, `.xml`, `.dds`, or `.ogg` inside `OGSR-Engine` or `zoneforge` recommends **`Flash • Low`** (saving ~85% quota). The moment you modify `.cpp`, `.h`, `.hlsl`, `.ps`, or `.patch`, it automatically escalates that repo's live recommendation to **`Argon • High`** (64-bit pointer & shader safety).
2. **Recent Commit History (`git diff-tree HEAD` & commit timestamps):**
   - Ranks repositories in `~/Documents/GitHub/` by live dirty count and most recent activity timestamp so the repos you actively work on always float to the top of the cheat sheet.
3. **New Repo & New Stack Auto-Discovery:**
   - Scans all project folders in `~/Documents/GitHub/` (both git and non-git directories) in parallel (`ThreadPoolExecutor`). Adding a new repository or introducing new file types (e.g. `.blend`, `.gd`, `.rs`, `.kt`, `.cs`) automatically profiles the stack and updates [`config/repo_cheatsheet.json`](file:///home/ericparsley/Documents/GitHub/cli-power-setup/config/repo_cheatsheet.json).
4. **Crash & Retry Escalation (`.agents/memory/adaptive_reasoning_state.json`):**
   - If `adaptive-model-router` records a Tier 3 crash or consecutive test failure in a repo, `agy-cheatsheet` immediately flags `⚠️ Recent error/retry escalation` and switches the live recommendation to **`Argon • High`**.

## 2. Where It Appears Automatically

1. **Startup Banner (`agy-yolo`, `agy-turbo`, `claude-yolo`, `claude-turbo`):**
   - Automatically prints the compact 7-line cheat sheet box showing your current workspace's live recommendation + your top 5 most recently active GitHub repositories before launching the agent.
2. **Live Bottom Statusline (`agy-quota-statusline` & `claude-statusline`):**
   - Displays a fast, cached segment (`🎯 Rec: Flash•Low` / `🎯 Rec: Argon•High` / `🎯 Rec: Tandem•Arg+Fab`) directly in your bottom terminal status bar that updates within 30 seconds as you edit different files.
3. **Automatic Git Sync Hook (`repo-auto-sync`):**
   - Every `repo-auto-sync --checkpoint` or `skill-evolve` run calls `agy-cheatsheet --update` to persist your latest repo telemetry into `config/repo_cheatsheet.json` (symlinked at `~/.cli_power_setup/repo_cheatsheet.json`).

## 3. Terminal Commands

```bash
# Show active workspace analysis + top 14 most recently active GitHub repos
agy-cheatsheet
# (or short alias)
cs

# Show all 34+ repositories in ~/Documents/GitHub
agy-cheatsheet --all

# Print the compact startup box banner
agy-cheatsheet --banner

# Fast (<10ms cached) 1-segment recommendation for statuslines
agy-cheatsheet --statusline

# Silently refresh config/repo_cheatsheet.json
agy-cheatsheet --update
```

## 4. Repository Stack Routing Matrix

| Stack / Repository Group | Fast / Routine Mode | Deep / Architecture Mode | Local Hardware Offload |
| :--- | :--- | :--- | :--- |
| **64-Bit C++ Engine & Shaders** (`OGSR-Engine`, `ogsr-complete-merge*`) | `Flash • Low` (`.ltx`/`.dds` configs) | `Argon • High` / `Tandem•Arg+Fab` (`.cpp`/`.h`/`.ps`) | 32-Thread CMake + `/dev/shm` tmpfs |
| **S.T.A.L.K.E.R. Modding Suite** (`zoneforge`) | `Flash • Low` (LTX deltas, audio, DDS) | `Argon • Med` (Lua state, `.ogf`/`.xdb` codecs) | CUDA/NumPy 32-Thread + `/dev/shm` |
| **Binary RE & Native Hooks** (`rea`, `wlfryt-organized-gta-pc-fixes`) | `Flash • Low` (TS glue, `.ini`/`.vdf`) | `Argon • High` (Decompilation, ASI hooks) | REA MCP + `CARGO_BUILD_JOBS=32` |
| **Linux Kernel ACPI & Rust** (`omen-acpi`, `omen-space`) | `Flash • Low` (Systemd, PKGBUILD, UI) | `Argon • High` (EC registers, DKMS, Rust lifetimes) | `CARGO_BUILD_JOBS=32` |
| **Godot 4 Game Fleet** (`BarrelBreaker`, `CargoCamp`, `Warmstead`, etc.) | `Flash • Low` (GDScript UI, `.tscn` signals) | `Argon • Med` (Blender `.glb`, nav graphs, shaders) | RTX 5060 OptiX (`16–32` samples) |
| **C# .NET / Unity / Avalonia** (`PS-Multi-Tools`, `SuperRCProHams`) | `Flash • Low` (AXAML UI, `.meta` configs) | `Argon • Med` (Async/AOT, C# systems) | Parallel `dotnet build` |
| **Android Kotlin & NDK** (`tetherfusenet`, `NSZ-Android`) | `Flash • Low` (XML layouts, Gradle KTS) | `Argon • Med` (VPN/Tethering services, JNI/NDK) | ADB + Radeon 610M iGPU |
| **Crypto & Console Homebrew** (`AegisVault`, `nsz`, `switch-softmod-prep`) | `Flash • Low` (CLI wrappers, JSON feeds) | `Argon • Med` (Cryptographic verification, NSP/NSZ) | 32-Thread `ProcessPool` + `/dev/shm` |
| **AI Skills & Orchestration** (`cli-power-setup`) | `Flash • Low` (Skill sync, docs, `.gitignore`) | `Argon • High` (Multi-agent swarm architecture) | Local AST/RAG + 32-Thread |

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

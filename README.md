# Antigravity Power Setup (`agy-power-setup`)

A production-grade, quota-optimized engineering and game development suite for **Google Antigravity (`agy`)** and **Claude Code CLI**.

This repository organizes a curated set of **27 autonomous agent skills**, global engineering rules, quota-saving protocols, and a real-time CLI statusline monitor.

---

## ⚡ Quick Start

Clone or copy this repository to your target machine and run the installer:

```bash
git clone https://github.com/your-username/agy-power-setup.git
cd agy-power-setup
./install.sh
```

The installer will:
1. **Safely backup** your existing `~/.gemini/config/skills`, `GEMINI.md`, and `settings.json`.
2. **Install all 26 skills** to `~/.gemini/config/skills/`.
3. **Configure global engineering & token economy rules** in `~/.gemini/config/GEMINI.md`.
4. **Install the real-time quota statusline monitor** to `~/.local/bin/agy-quota-statusline`.
5. **Update `~/.gemini/antigravity-cli/settings.json`** to display live quota in the CLI prompt with `stack_with_default: true`.

---

## 📂 Repository Structure

```text
agy-power-setup/
├── install.sh                  # Automated installer with backup & verification
├── README.md                   # Documentation & skill index
├── bin/
│   └── agy-quota-statusline    # Asynchronous real-time quota tracker (Python)
└── config/
    ├── GEMINI.md               # Global engineering discipline & token economy rules
    ├── settings.template.json  # Reference AGY CLI settings configuration
    └── skills/                 # 26 specialized skills
```

---

## 🛠️ Complete Skill Directory

### 🧠 Core Engineering & Cognitive Methodology
| Skill | Description |
| :--- | :--- |
| **`adaptive-reasoning`** | Automatic reasoning effort selection. Scales between instant Flash and deep-reasoning Argon based on prompt complexity. |
| **`superpowers`** | Primary engineering discipline engine: triggers brainstorming, planning, TDD, and debugging workflows. |
| **`writing-plans`** | Breaks down complex tasks into granular, dependency-ordered, verifiable task lists. |
| **`executing-plans`** | Safe step-by-step plan execution with verification checkpoints. |
| **`brainstorming`** | Interactive design exploration and requirements discovery before writing code. |
| **`systematic-debugging`** | Hypothesis-driven root cause analysis via engine logs and reproducible tests before editing. |
| **`test-driven-development`** | Strict TDD workflows: write failing unit tests before feature implementation. |
| **`verification-before-completion`**| Final quality gate: enforces compiler and test verification before closing tasks. |
| **`subagent-code-reviewer`** | Spawns isolated review subagents to audit diffs and security without polluting context. |
| **`using-git-worktrees`** | Manages isolated worktrees for multi-branch experiments without dirtying working copies. |

### 🎮 Game Engines & 3D Asset Engineering
| Skill | Description |
| :--- | :--- |
| **`godot-game-dev`** | Godot 4.x workflows: GDScript 2.0 static typing, scene lifecycle, and headless GUT testing. |
| **`unreal-engine-dev`** | Unreal Engine 5 workflows: Gameplay Framework, UObject memory management, Subsystems. |
| **`unity-game-dev`** | Unity C# workflows: MonoBehaviours, ScriptableObjects, and zero-allocation memory discipline. |
| **`blender-3d-engineering`** | High-efficiency 3D modeling via headless `bpy`, modifier stacks, manifold validation, and game exports. |

### ☢️ Game Modding (S.T.A.L.K.E.R. Ecosystem)
| Skill | Description |
| :--- | :--- |
| **`game-modding`** | Core S.T.A.L.K.E.R. EE workflows: ZoneForge toolchain, LTX syntax safety, DXT textures, and sound preservation. |
| **`xray-lua-scripting`** | S.T.A.L.K.E.R. X-Ray Engine Lua scripting guidelines, callbacks, and memory safeguards. |
| **`stalker2-modding`** | S.T.A.L.K.E.R. 2 Heart of Chornobyl (UE5): repak container packaging and RE-UE4SS C++/Lua hooks. |

### 💻 Systems, Reverse Engineering & Languages
| Skill | Description |
| :--- | :--- |
| **`cachyos-arch-packaging`** | Arch/CachyOS standards: PKGBUILD authoring, DKMS kernel module builds, and systemd units. |
| **`reverse-engineer-anything`** | Multi-target reverse engineering with REA MCP (native, managed, web, firmware, mobile). |
| **`binary-re-workflows`** | Orchestrates REA, Ghidra, JADX, TShark, objdump, and hex analysis. |
| **`steamcmd-workshop-pipeline`**| SteamCMD automated workshop item publishing, VDF manifests, and content depot management. |
| **`python-engineering`** | Modern Python 3.10+ standards: strict typing, pytest suites, Ruff, and Mypy. |
| **`rust-engineering`** | Rust compiler-first workflows: zero-cost abstractions, borrow checker mastery, Clippy, and tests. |
| **`modern-cpp-engineering`** | Modern C++20/C++23 standards: RAII, Concepts, smart pointers, and CMake management. |
| **`csharp-dotnet-engineering`** | .NET 8/9 standards: Span/Memory allocation optimizations, async cancellation, and Roslyn analyzers. |

### 💰 Quota, Memory & Context Engineering
| Skill | Description |
| :--- | :--- |
| **`token-economy`** | Output token optimization: eliminates conversational fluff, uses compact checklist status, and offloads heavy text. |
| **`project-memory-bank`** | Persistent project memory (`.agents/memory/`): eliminates repetitive codebase discovery, logs engine gotchas, and preserves context across `/compact`. |

---

## 📊 Real-Time CLI Quota Statusline

The statusline script (`~/.local/bin/agy-quota-statusline`) displays real-time 5-hour and weekly quota remaining directly at the bottom of the AGY CLI:

```text
⚡ Gemini: 5h: 88% (reset 18:30) | Wk: 94%
```

### Key Technical Features:
- **Non-Blocking & Zero Lag:** Caches quota metrics locally (`/tmp/agy_quota_cache.txt`). Background refreshes are asynchronously spawned with lockfile protection.
- **Stacked Layout:** Uses `stack_with_default: true` in `settings.json` so both the standard model/directory prompt and the live quota bar display cleanly without collisions.

---

## 🔄 Updating or Adding New Skills

To add a new skill to your suite:
1. Create a subdirectory under `config/skills/<skill-name>/`.
2. Add a `SKILL.md` with YAML frontmatter:
   ```markdown
   ---
   name: your-skill-name
   description: 1-2 sentence description explaining when and why to activate this skill.
   ---
   # Your Skill Title
   ...
   ```
3. Run `./install.sh` to deploy the updates.

# Antigravity Power Setup (`agy-power-setup`)

A production-grade, quota-optimized engineering and game development suite for **Google Antigravity (`agy`)** and **Claude Code CLI**.

This repository organizes a curated set of **31 autonomous agent skills**, global engineering rules, quota-saving protocols, and an asynchronous real-time CLI statusline monitor.

---

## ⚡ Quick Start

Clone this repository to your machine and run the installer:

```bash
git clone https://github.com/WoofahRayetCode/agy-power-setup.git
cd agy-power-setup
./install.sh
```

### What the Installer Does:
1. **Safety Backup:** Archives existing configurations to `~/.gemini/backups/`.
2. **Dual-CLI Sync:** Installs all 31 skills to `~/.gemini/config/skills/` and mirrors them to `~/.claude/skills/` if Claude Code is present.
3. **Global Discipline Rules:** Updates `~/.gemini/config/GEMINI.md` with engineering safeguards and the **Output Token Economy**.
4. **Live Quota & Token Monitor:** Installs `agy-quota-statusline` and `agy-turbo` into `~/.local/bin/`.
5. **Prompt Integration:** Configures `~/.gemini/antigravity-cli/settings.json` with `stack_with_default: true` for clean statusline display.

---

## 📂 Repository Structure

```text
agy-power-setup/
├── install.sh                  # Automated installer with backup & verification
├── README.md                   # Comprehensive documentation & skill reference
├── .gitignore                  # Clean git filters
├── bin/
│   ├── agy-quota-statusline    # Asynchronous real-time quota & token savings tracker
│   └── agy-turbo               # High-speed Turbo mode launcher script (hands-free)
└── config/
    ├── GEMINI.md               # Global engineering discipline & token economy rules
    ├── settings.template.json  # Reference AGY CLI settings configuration
    └── skills/                 # 31 specialized skills
```

---

## 🧭 Complete Skill Index

| Skill | Category | Primary Focus |
| :--- | :--- | :--- |
| **`adaptive-reasoning`** | Cognitive | Heuristic reasoning effort selection (Flash vs Argon) |
| **`superpowers`** | Methodology | Core engineering discipline engine & workflow router |
| **`writing-plans`** | Methodology | Granular, dependency-ordered, verifiable task lists |
| **`executing-plans`** | Methodology | Safe plan execution with test-gated checkpoints |
| **`brainstorming`** | Methodology | Requirements discovery and architectural trade-offs |
| **`systematic-debugging`** | Methodology | Root-cause hypothesis testing via logs and traces |
| **`test-driven-development`** | Methodology | Strict Red-Green-Refactor before implementation |
| **`verification-before-completion`** | Methodology | Final quality gate with reproducible evidence |
| **`subagent-code-reviewer`** | Methodology | Isolated subagent code reviews without context bloat |
| **`using-git-worktrees`** | Methodology | Safe branch sandboxes for risky experiments |
| **`godot-game-dev`** | Game Engine | Godot 4.x, GDScript 2.0 static typing, headless GUT |
| **`unreal-engine-dev`** | Game Engine | Unreal Engine 5 C++, Gameplay Framework, GC rules |
| **`unity-game-dev`** | Game Engine | Unity C#, zero-allocation Span/Memory, ScriptableObjects |
| **`blender-3d-engineering`** | 3D Assets | Headless `bpy` modeling, modifier stacks, game exports |
| **`game-modding`** | Modding | S.T.A.L.K.E.R. EE ZoneForge toolchain, LTX & audio rules |
| **`xray-lua-scripting`** | Modding | S.T.A.L.K.E.R. X-Ray Engine Lua callbacks and memory safety |
| **`stalker2-modding`** | Modding | S.T.A.L.K.E.R. 2 UE5 repak containers & RE-UE4SS hooks |
| **`cachyos-arch-packaging`** | Systems | Arch/CachyOS PKGBUILD, DKMS kernel modules, systemd |
| **`reverse-engineer-anything`** | Systems/RE | Deep multi-target analysis with REA MCP |
| **`binary-re-workflows`** | Systems/RE | Ghidra, JADX, TShark, objdump, and hex diffing |
| **`standalone-binary-re`** | Systems/RE | Zero-MCP CLI reverse engineering (`readelf`, `objdump`, `jadx`, `pefile`) |
| **`open-apk`** | Systems/RE | Android APK, XAPK, DEX, and resource loader for JADX headless |
| **`wakaru`** | Systems/RE | Production JS bundle unpacker & decompiler (Webpack, Vite, Electron) |
| **`lowlevel-dll-internals`** | Systems/RE | Windows PE/DLL internals, vtables, calling conventions, MinHook |
| **`steamcmd-workshop-pipeline`** | Systems | Automated Steam Workshop publishing & VDF manifests |
| **`python-engineering`** | Language | Python 3.10+, strict typing (Mypy), pytest, Ruff |
| **`rust-engineering`** | Language | Compiler-first Rust, zero-cost abstractions, Clippy |
| **`modern-cpp-engineering`** | Language | Modern C++20/C++23, RAII, Concepts, CMake |
| **`csharp-dotnet-engineering`** | Language | .NET 8/9, Span/Memory allocation-free patterns, async |
| **`token-economy`** | Quota | Eliminates conversational fluff & echoes; compact status |
| **`project-memory-bank`** | Memory | Persistent `.agents/memory/` context to prevent re-hydration |

---

## 📖 Detailed Skill Reference

### 🧠 Core Engineering & Cognitive Methodology

#### 1. `adaptive-reasoning`
* **Trigger:** Complex refactors, architectural planning, ambiguous bugs, or high-volume rote tasks.
* **Mechanism:** Evaluates user prompt complexity against cognitive heuristics. Directs simple searches, file reads, and template edits to high-speed Flash, while automatically routing architectural breakdowns, debugging, and multi-file diffs to Argon.
* **Quota Advantage:** Eliminates the waste of high-tier reasoning tokens on routine lookups while ensuring difficult tasks receive full reasoning depth.

#### 2. `superpowers`
* **Trigger:** Starting non-trivial engineering tasks, refactors, or new architectures.
* **Mechanism:** Acts as the executive controller for engineering discipline. Evaluates whether a prompt requires brainstorming, structured planning, test-driven development, or systematic debugging before any production code is touched.
* **Quota Advantage:** Prevents costly "vibe coding" loops where models write speculative, broken code and spend 10 turns trying to patch runtime errors.

#### 3. `writing-plans`
* **Trigger:** Multi-file features, complex system refactors, mod architectures.
* **Mechanism:** Deconstructs high-level objectives into self-contained, bite-sized tasks. Each task specifies: exact files modified, expected code diff, verification commands (tests, builds), and rollback checkpoints.
* **Quota Advantage:** Eliminates ambiguous instructions that cause agents to wander, overwrite incorrect files, or thrash between different approaches.

#### 4. `executing-plans`
* **Trigger:** Executing an approved implementation plan.
* **Mechanism:** Enforces step-by-step progress through task plans. Validates each step with concrete evidence (terminal output, compiler status) before advancing. Halts immediately upon failure rather than compounding errors.
* **Quota Advantage:** Guarantees that errors are caught at Step N rather than discovering a foundational failure at Step N+10.

#### 5. `brainstorming`
* **Trigger:** Early-stage project design, architectural choices, feature scoping.
* **Mechanism:** Structured interactive interview protocol. Explores technical trade-offs, constraints, dependencies, and alternatives before committing to an implementation path.
* **Quota Advantage:** Prevents implementing the wrong architecture, saving 100% of the rework token cost.

#### 6. `systematic-debugging`
* **Trigger:** Compiler errors, test failures, runtime crashes, engine fatal exceptions.
* **Mechanism:** Hypothesis-driven debugging protocol:
  1. Capture raw crash logs, stack traces, and environment state.
  2. Formulate a testable root-cause hypothesis.
  3. Create a minimal reproducible test case.
  4. Fix the root cause and verify with tests. **Prohibits speculative value tweaking.**
* **Quota Advantage:** Cuts debugging cycles from 10–15 rambling turns down to 2–3 deterministic turns.

#### 7. `test-driven-development`
* **Trigger:** Authoring parsers, business logic, algorithmic routines, API endpoints, bug fixes.
* **Mechanism:** Enforces strict Red-Green-Refactor:
  1. Author a failing unit test that exercises the expected behavior.
  2. Implement the minimum production code required to turn the test green.
  3. Refactor with test coverage protection.
* **Quota Advantage:** Provides an automated, deterministic verification harness that prevents regression bugs and prompt thrashing.

#### 8. `verification-before-completion`
* **Trigger:** Prior to declaring any task, PR, or mod ready.
* **Mechanism:** Quality gate requiring verifiable evidence: compiler clean passes (`cargo check`, `dotnet build`), full test suite execution, asset syntax checks, and file existence confirmation.
* **Quota Advantage:** Guarantees the agent does not declare victory prematurely, avoiding follow-up user correction prompts.

#### 9. `subagent-code-reviewer`
* **Trigger:** Prior to merging large PRs, committing sensitive security changes, or publishing mods.
* **Mechanism:** Spawns an isolated reviewer subagent that receives only the git diff and review rubric. Analyzes logic bugs, edge cases, memory leaks, and style violations.
* **Quota Advantage:** Audits extensive diffs in an isolated conversation, keeping your primary session transcript clean and compact.

#### 10. `using-git-worktrees`
* **Trigger:** Testing risky changes, running concurrent mod branches, verifying clean builds.
* **Mechanism:** Automates `git worktree add`, directory branching, and cleanup. Keeps experiments fully sandboxed from your working tree.
* **Quota Advantage:** Avoids messy stash/checkout cycles that dirty git index state and force repository re-exploration.

---

### 🎮 Game Engines & 3D Asset Engineering

#### 11. `godot-game-dev`
* **Trigger:** Godot Engine 4.x game logic, UI systems, physics, scene trees.
* **Mechanism:** Enforces strict GDScript 2.0 static typing (`var x: int = 10`), "signals up, functions down" scene tree decoupling, data-driven custom `Resource` definitions, and headless CLI unit testing with the GUT framework.
* **Quota Advantage:** Static typing and headless checks catch script errors via CLI before running the full game window.

#### 12. `unreal-engine-dev`
* **Trigger:** Unreal Engine 5 C++ classes, Gameplay Framework, Subsystems, Blueprints.
* **Mechanism:** Governs UObject lifecycle, `UPROPERTY` garbage collection semantics, Subsystems for persistent game logic, Enhanced Input actions, and headless build compilation.
* **Quota Advantage:** Prevents UE5 GC pointer corruption and dangling references that cause engine crashes and lengthy log analysis.

#### 13. `unity-game-dev`
* **Trigger:** Unity Engine C# scripts, MonoBehaviours, ScriptableObjects, UI Toolkit.
* **Mechanism:** Enforces zero-allocation patterns (avoiding runtime GC spikes), `Span<T>` and `Memory<T>` for buffers, ScriptableObject architectures, and decoupled EventChannel systems.
* **Quota Advantage:** Eliminates garbage collection churn and memory leak debugging cycles.

#### 14. `blender-3d-engineering`
* **Trigger:** Creating 3D models, procedural geometry, hard-surface props, game asset exports.
* **Mechanism:** Headless Python execution via `/usr/bin/blender -b -P script.py`. Constructs assets using parameter-driven primitives and non-destructive modifier stacks (Boolean, Bevel, Mirror, Array, Subsurf). Validates manifold topology in-script and exports clean glTF/FBX.
* **Quota Advantage:** Eliminates the disaster of emitting thousands of raw vertex coordinates into chat, saving 20,000+ tokens per asset while producing clean, manifold meshes.

---

### ☢️ Game Modding (S.T.A.L.K.E.R. Ecosystem)

#### 15. `game-modding`
* **Trigger:** S.T.A.L.K.E.R. Legends of the Zone Trilogy Enhanced Edition (EE) modding.
* **Mechanism:** Operates ZoneForge asset workflows. Enforces read-only baseline protection for unpacked vanilla archives, strict LTX section header and inheritance syntax, DXT1/DXT5 texture standards, and engine-safe OGG audio chunk preservation.
* **Quota Advantage:** Eliminates fatal X-Ray engine crashes caused by missing LTX parent sections or corrupted audio comment headers.

#### 16. `xray-lua-scripting`
* **Trigger:** S.T.A.L.K.E.R. X-Ray Engine Lua scripts, quest logic, inventory hooks, callbacks.
* **Mechanism:** Enforces safe engine callback bindings, memory leak prevention in global Lua states, safe game save serialization, and strict nil-checking on game objects.
* **Quota Advantage:** Prevents silent script freezes and corrupt savegame states.

#### 17. `stalker2-modding`
* **Trigger:** S.T.A.L.K.E.R. 2 Heart of Chornobyl modding (Unreal Engine 5).
* **Mechanism:** Governs UE5 IoStore container packaging (`.pak`, `.ucas`, `.utoc`) using `repak`, RE-UE4SS C++ and Lua hooking workflows, and game asset extraction.
* **Quota Advantage:** Eliminates trial-and-error container packing errors and mismatched compression flags.

---

### 💻 Systems, Reverse Engineering & Languages

#### 18. `cachyos-arch-packaging`
* **Trigger:** CachyOS and Arch Linux PKGBUILD authoring, DKMS modules, systemd services.
* **Mechanism:** Enforces Arch packaging standards, safe DKMS kernel hooks (e.g. `omen-acpi`), systemd unit authoring, `makepkg` verification, and package integrity checks.
* **Quota Advantage:** Prevents broken build chroots and dirty package installations.

#### 19. `reverse-engineer-anything`
* **Trigger:** Reverse engineering native binaries, managed code, Electron apps, APKs, firmware.
* **Mechanism:** Deep integration with REA MCP. Handles static disassembly, decompilation, memory reconstruction, control-flow graphing, and evidence ledger maintenance.
* **Quota Advantage:** Focuses analysis strictly on evidence ledgers rather than dumping raw assembly dumps into chat.

#### 20. `binary-re-workflows`
* **Trigger:** Inspecting compiled binaries, game DLLs, network packets, executables.
* **Mechanism:** Orchestrates REA, Ghidra, JADX, TShark, `objdump`, and hex analysis tools under Superpowers verification standards.
* **Quota Advantage:** Converts opaque binary debugging into deterministic, hypothesis-driven investigation.

#### 21. `standalone-binary-re`
* **Trigger:** Reverse engineering binaries when REA MCP is offline, unavailable, or for fast zero-overhead CLI inspection.
* **Mechanism:** Direct execution of native Linux utilities (`objdump`, `readelf`, `nm`, `jadx`, `gdb`, `strings`, `xxd`) and Python `pefile`. Handles Linux ELF relocations/symbols, Windows PE export/import directories, Android APK Java decompilation, and custom binary formats without MCP dependencies.
* **Quota Advantage:** Zero MCP startup latency; avoids large token-heavy disassembly dumps through targeted function filters.

#### 22. `open-apk`
* **Trigger:** Opening, decompiling, or inspecting Android APK, XAPK, DEX, or JAR files.
* **Mechanism:** Streamlines loading Android packages into JADX headless static analysis, extracting package metadata, searching classes/methods, resolving xrefs, and exporting readable Java source. Supports downloading from APKPure via `apkeep`.
* **Quota Advantage:** Extracts targeted classes rather than dumping hundreds of decompiled Java files into context.

#### 23. `wakaru`
* **Trigger:** Auditing minified production JavaScript, Webpack/Vite/Rollup bundles, Electron apps, or compiled Vue 3 artifacts.
* **Mechanism:** JavaScript bundle unpacker and decompiler. Splits bundled assets into original module structures, reverses transpiler helpers (async/await, classes, JSX, optional chaining), and un-minifies structure deterministically.
* **Quota Advantage:** Turns unreadable single-line 2MB bundles into isolated, readable modules with zero hallucination.

#### 24. `lowlevel-dll-internals`
* **Trigger:** Analyzing Windows PE/DLL binaries, ASI plugins, C++ engine classes, vtables, crash dumps, or writing native detour hooks.
* **Mechanism:** Applies compiler-grade binary heuristics: RVA-to-file offset conversion, 32-bit calling convention stack alignment (`__thiscall` in `ecx`, `__stdcall`, `__cdecl`), 64-bit ABI shadow space rules, virtual method table (VTable) slot indexing, 5-byte relative jump detour blueprints, and memory protection patching.
* **Quota Advantage:** Eliminates trial-and-error memory patching and prevents cryptic `0xC0000005` access violations before code execution.

#### 25. `steamcmd-workshop-pipeline`
* **Trigger:** Publishing, updating, or managing Steam Workshop items via SteamCMD.
* **Mechanism:** Generates valid VDF workshop manifests, manages content depots, sets item visibility, handles preview images, and publishes automated changelogs.
* **Quota Advantage:** Replaces error-prone manual SteamCMD commands with automated, verified scripts.

#### 26. `python-engineering`
* **Trigger:** Python development, API building, test suites, automation scripts.
* **Mechanism:** Enforces Python 3.10+ modern idioms: strict type annotations (`mypy`), fast linting and formatting (`ruff`), pytest test suites with fixtures, and hot-path memory profiling.
* **Quota Advantage:** Static type checks catch bugs instantly before runtime.

#### 27. `rust-engineering`
* **Trigger:** Rust systems development, game tools, CLI applications.
* **Mechanism:** Enforces compiler-first workflows: zero-cost abstractions, idiomatic error handling with `Result` and `Option`, strict borrow checker compliance, and Clippy lint audits.
* **Quota Advantage:** Zero runtime crashes; compiler errors are solved systematically.

#### 28. `modern-cpp-engineering`
* **Trigger:** C++ systems programming, game engine modules, native libraries.
* **Mechanism:** Modern C++20/C++23 standards: RAII memory management, smart pointers (`unique_ptr`, `shared_ptr`), Concepts for template constraints, and CMake modular targets.
* **Quota Advantage:** Eliminates memory leaks, buffer overflows, and undefined behavior debugging.

#### 29. `csharp-dotnet-engineering`
* **Trigger:** Modern .NET 8/9 applications, C# utilities, engine plugins.
* **Mechanism:** Emphasizes memory optimization using `Span<T>` and `Memory<T>`, strict `CancellationToken` propagation across async chains, pattern matching, and Roslyn analyzer enforcement.
* **Quota Advantage:** Guarantees efficient, allocation-conscious code that minimizes GC pauses.

---

### 💰 Quota, Memory & Context Engineering

#### 30. `token-economy`
* **Trigger:** Active in all conversations via `GEMINI.md` and on-demand skill.
* **Mechanism:**
  - **Zero Conversational Fluff:** Drops conversational preambles ("Sure, I can help with that"), fillers, and sign-offs.
  - **High-Density Status:** Uses single-line checklist indicators (`[✓]`, `[→]`, `[!]`) instead of multi-paragraph narratives.
  - **Silent Tool Success:** Suppresses echoing successful terminal outputs; surfaces only errors, diffs, and metrics.
  - **Surgical Edits:** Enforces targeted chunk replacements (`replace_file_content`) over full-file overwrites.
  - **Artifact Offloading:** Offloads extensive plans, logs, and designs to files/artifacts referenced by 1-line clickable links.
  - **Token Economy Visibility:** Concludes multi-step workflows with a single high-density token savings metric line (`📉 Token Economy: ~<N> tokens saved (<breakdown>)`).
* **Quota Advantage:** Directly slashes output token consumption by 40–70% and prevents compounding transcript bloat.

#### 31. `project-memory-bank`
* **Trigger:** Starting work on a repository, multi-session tasks, before running `/compact`.
* **Mechanism:**
  - Maintains persistent markdown files in `.agents/memory/`:
    - `projectBrief.md`: Scope, tech stack, boundaries (<300 tokens).
    - `systemPatterns.md`: Architecture, directory conventions (<400 tokens).
    - `activeContext.md`: Current objective, recent changes, immediate next steps (<300 tokens).
    - `learnings.md`: Solved engine gotchas, compiler traps, environment fixes (<500 tokens).
  - **Instant Hydration:** Reads `activeContext.md` upon session start instead of scanning 30 files.
  - **Lossless Compaction:** Saves state before `/compact`, wiping 100k-token conversation histories while retaining 100% working context.
* **Quota Advantage:** Saves 15,000–50,000 exploration tokens on every new session and eliminates re-debugging known issues.

---

## 📊 Real-Time CLI Quota & Token Savings Statusline

The statusline script (`~/.local/bin/agy-quota-statusline`) displays real-time 5-hour and weekly quota remaining, plus live session prompt tokens saved via Google context caching:

```text
⚡ Gemini: 5h: 78% (reset 16:00) | Wk: 72% | 💾 Saved: 7.6M tok (Flash)
```

In multi-model sessions (e.g. adaptive escalation between Flash and Argon):
```text
⚡ Gemini: 5h: 78% | Wk: 72% | 💾 Saved: 23.4M tok (Argon: 12.0M | Flash: 11.4M)
```

### Technical Design:
* **Context Cache Token Telemetry:** Directly correlates active session step tokens from `transcript.jsonl` with turn models in `gen_metadata`, displaying exact prompt tokens saved by context caching.
* **Per-Model Savings Breakdown:** Automatically disaggregates saved prompt tokens across models when multiple models (e.g. Gemini 3.8 Flash, Gemini 4 Argon, Claude Sonnet) are used in a single session.
* **Asynchronous & Non-Blocking Quota:** Queries `agy -p /usage` and caches the result in `/tmp/agy_quota_cache.txt` with a 2-minute TTL.
* **Zero CLI Lag:** Quota subprocesses are detached with PID lockfile protection (`/tmp/agy_quota_refresh.lock`), guaranteeing instant prompt rendering (<2ms).
* **Clean Stacking:** Configured in `~/.gemini/antigravity-cli/settings.json` with `stack_with_default: true` so the live quota line renders below the default working directory and model status.

---

## 🚀 Antigravity CLI Turbo Mode (`agy-turbo`)

Equivalent to the **Turbo** mode in the Antigravity Desktop App, the `agy-turbo` launcher activates hands-free auto-execution with minimal chain-of-thought latency:

```bash
agy-turbo
```

### Configuration Flags:
* `--model gemini-3.8-flash-low`: Dispatches the ultra-fast low-latency Flash variant.
* `--effort low`: Minimizes chain-of-thought reasoning pauses for instantaneous token streaming.
* `--dangerously-skip-permissions`: Auto-approves tool actions and shell commands without modal stops.
* `--mode auto`: Automatically applies and accepts validated code edits.

> [!TIP]
> **Desktop Shortcut:** On Linux systems, a `.desktop` shortcut (`agy-turbo.desktop`) can be created in `~/Desktop/` to launch `agy-turbo` in Konsole with a single click.

---

## 🛠️ Maintenance & Adding New Skills

### To add a new skill:
1. Create `config/skills/<skill-name>/SKILL.md`.
2. Include standard YAML frontmatter:
   ```markdown
   ---
   name: your-skill-name
   description: Brief description explaining when and why to activate this skill.
   ---
   # Skill Title
   ...
   ```
3. Run `./install.sh` to deploy the new skill across Antigravity and Claude Code environments.

---

## 📄 License
MIT License. Free to use, adapt, and distribute for autonomous agent engineering.

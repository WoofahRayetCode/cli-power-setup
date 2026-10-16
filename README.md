# CLI Power Setup (`cli-power-setup`)

A production-grade, quota-optimized engineering and game development suite for **Google Antigravity (`agy`)** and **Claude Code CLI (`claude`)**.

This repository organizes a curated set of **35 autonomous agent skills**, global engineering discipline rules, quota-saving protocols, a Turbo launcher, and an asynchronous real-time CLI statusline monitor.

---

## ⚡ Quick Start

Clone this repository to your machine and run the installer:

```bash
git clone https://github.com/WoofahRayetCode/cli-power-setup.git
cd cli-power-setup
./install.sh
```

### 📋 Interactive Installer Menu
Running `./install.sh` displays an interactive target menu:
```text
CLI Power Setup Installer
Select target CLI environment:
  1) Dual-CLI (Both Antigravity & Claude Code) [Recommended]
  2) Antigravity only (~/.gemini)
  3) Claude Code only (~/.claude)
  4) Exit
```

Or pass flags non-interactively in automated scripts:
```bash
./install.sh --all     # Install for both Antigravity & Claude Code
./install.sh --agy     # Install for Google Antigravity only
./install.sh --claude  # Install for Claude Code only
```

### What the Installer Does:
1. **Safety Backup:** Automatically archives existing configurations to `~/.cli_power_setup_backups/`.
2. **Dual-CLI Sync:** Deploys all 35 skills to `~/.gemini/config/skills/` and `~/.claude/skills/`.
3. **Global Discipline Rules:** Installs engineering safeguards and the **Output Token Economy** to `~/.gemini/config/GEMINI.md` and `~/.claude/CLAUDE.md`.
4. **Live Quota & Token Monitor:** Installs `agy-quota-statusline` and configures it in both `~/.gemini/antigravity-cli/settings.json` and `~/.claude/settings.json`.
5. **Turbo Mode Launcher:** Installs `agy-turbo` into `~/.local/bin/`.

---

## 📂 Repository Structure

```text
cli-power-setup/
├── install.sh                  # Interactive dual-CLI installer with backup & menu
├── README.md                   # Comprehensive documentation & skill reference
├── .gitignore                  # Clean git filters
├── bin/
│   ├── agy-quota-statusline    # Asynchronous real-time quota & token savings tracker (Gemini)
│   ├── claude-statusline       # Dedicated real-time telemetry & context monitor (Claude Code)
│   └── agy-turbo               # High-speed Turbo mode launcher script (hands-free)
└── config/
    ├── GEMINI.md               # Global engineering discipline & token economy rules
    ├── settings.template.json  # Reference AGY CLI settings configuration
    └── skills/                 # 35 specialized skills
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
| **`game-engine-migration`** | Game Engine | Universal 5-stage engine & mod porting framework (32-to-64 bit, DX9-to-DX11/VK) |
| **`blender-3d-engineering`** | 3D Assets | Headless `bpy` modeling, modifier stacks, game exports |
| **`game-modding`** | Modding | S.T.A.L.K.E.R. EE ZoneForge toolchain, LTX & audio rules |
| **`xray-lua-scripting`** | Modding | S.T.A.L.K.E.R. X-Ray Engine Lua callbacks and memory safety |
| **`stalker2-modding`** | Modding | S.T.A.L.K.E.R. 2 UE5 repak containers & RE-UE4SS hooks |
| **`stalker-ogsr-migration`** | Modding | 32-bit S.T.A.L.K.E.R. mod porting to 64-bit OGSR Engine |
| **`game-runtime-diagnostics`** | Diagnostics | Cross-platform PC & Steam Deck game crash troubleshooting (Proton, DirectX, TDRs) |
| **`audio-dsp-tuning`** | Audio/DSP | Studio headset EQ (AutoEq/Harman) & 6-stage broadcast mic processing (EasyEffects/Equalizer APO) |
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

## 🧩 Architectural Design: Generalist vs. Specialist Skills

To provide maximum flexibility without losing precision, this suite employs a **two-tier skill hierarchy**:
1. **Generalist Blueprints:** Skills like `game-engine-migration` give the AI the universal, battle-tested 5-stage blueprint for porting *any* game or engine from 32-bit to 64-bit and legacy DirectX to modern Vulkan/DX11.
2. **Specialist Experts:** Skills like `stalker-ogsr-migration` handle the exact proprietary quirks, crash signatures, and custom toolchains of specific game engines.
*This ensures the AI never gets stuck when tackling unfamiliar engines, while retaining pinpoint mastery on specialized environments.*

---

## 📖 Detailed Skill Reference

### 🧠 Core Engineering & Cognitive Methodology

#### 1. `adaptive-reasoning`
* **In Simple Terms:** Automatically balances speed and thinking depth so you don't burn through your daily AI quota on easy tasks.
* **When It Kicks In:** On every request—from quick file searches to complex multi-file architectural refactors.
* **How It Works:** Routes simple lookups and quick edits to ultra-fast models (like Flash), while automatically reserving deep reasoning models (like Argon or Claude Extended Thinking) for hard bugs and architectural plans.
* **Why It Saves Quota:** Saves expensive thinking compute for problems that truly require it, keeping routine interactions instantaneous.

#### 2. `superpowers`
* **In Simple Terms:** Acts as a senior staff engineer that stops the AI from recklessly rushing into code before it has thought through the plan and tests.
* **When It Kicks In:** At the start of any new feature, bug fix, or project change.
* **How It Works:** Evaluates whether a prompt requires brainstorming, a structured checklist, a test-first approach, or systematic root-cause debugging before any file is touched.
* **Why It Saves Quota:** Prevents chaotic "vibe coding" loops where an AI writes speculative, broken code and wastes 10 turns trying to patch its own mistakes.

#### 3. `writing-plans`
* **In Simple Terms:** Breaks down massive, overwhelming coding projects into small, bite-sized checklists where each step takes only 2–5 minutes.
* **When It Kicks In:** Whenever a task touches multiple files, requires a refactor, or introduces a new system.
* **How It Works:** Prepares a detailed roadmap listing the exact files to edit, the expected code changes, and the exact commands needed to verify success before writing a single line of production code.
* **Why It Saves Quota:** Prevents the AI from wandering off track, overwriting incorrect files, or thrashing between different designs.

#### 4. `executing-plans`
* **In Simple Terms:** Walks through an approved checklist step-by-step, proving that each step works before moving to the next.
* **When It Kicks In:** Whenever you tell the AI to execute an approved implementation plan.
* **How It Works:** Runs tests or compiler checks after each individual step. If a step fails, it halts immediately and fixes the issue instead of digging a deeper hole.
* **Why It Saves Quota:** Catches mistakes at Step 1 rather than discovering everything is broken at Step 10.

#### 5. `brainstorming`
* **In Simple Terms:** An interactive design interview that asks helpful clarifying questions to ensure the AI builds exactly what you want.
* **When It Kicks In:** Early project planning, when ideas are still loose, or when there are multiple architectural paths.
* **How It Works:** Proposes options, weighs pros and cons, and confirms your preferences before committing to code.
* **Why It Saves Quota:** Prevents building the wrong architecture, saving 100% of the token cost required to tear down and rewrite incorrect work.

#### 6. `systematic-debugging`
* **In Simple Terms:** A scientific detective method for finding bugs using real evidence instead of random guessing.
* **When It Kicks In:** Whenever code crashes, tests fail, or an engine throws an error.
* **How It Works:** Reads the error log, forms a clear hypothesis of the root cause, proves it with a minimal test case, and verifies the fix with tests. Random value-tweaking is strictly forbidden.
* **Why It Saves Quota:** Solves bugs in 2–3 targeted turns instead of 15 rambling rounds of trial-and-error.

#### 7. `test-driven-development`
* **In Simple Terms:** Writes an automated test that proves what the code should do *before* writing the actual code.
* **When It Kicks In:** Writing new functions, business logic, game mechanics, parsers, or bug fixes.
* **How It Works:** Follows the Red-Green-Refactor cycle: (1) write a failing test, (2) write the minimal code to make it pass, (3) clean up the code with confidence that the test will catch any regressions.
* **Why It Saves Quota:** Guarantees code works on the first try and prevents future edits from silently breaking existing features.

#### 8. `verification-before-completion`
* **In Simple Terms:** A mandatory quality gate that double-checks that everything actually compiles and passes tests before declaring "I'm done!"
* **When It Kicks In:** Right before the AI finishes a task or tells you work is complete.
* **How It Works:** Runs real terminal commands (builds, linters, test suites) and inspects output logs to confirm success.
* **Why It Saves Quota:** Eliminates premature victory claims where the AI says a job is finished, but the code won't even compile.

#### 9. `subagent-code-reviewer`
* **In Simple Terms:** Calls in a fresh, objective AI reviewer to inspect code changes from an independent perspective.
* **When It Kicks In:** Before committing major code changes or publishing mods.
* **How It Works:** Dispatches the code diff to an isolated reviewer subagent that checks for security flaws, memory leaks, and logic bugs without cluttering your main chat.
* **Why It Saves Quota:** Audits large diffs in a separate lightweight sandbox, keeping your primary session transcript small and fast.

#### 10. `using-git-worktrees`
* **In Simple Terms:** Creates a private sandbox folder for risky experiments without messing up your main project files.
* **When It Kicks In:** Testing experimental changes, comparing versions, or working on multiple mod branches simultaneously.
* **How It Works:** Uses Git's built-in worktree feature to check out separate branches into distinct folders side-by-side.
* **Why It Saves Quota:** Avoids messy stash/checkout cycles that dirty git state and force the AI to re-scan the whole repository.

---

### 🎮 Game Engines & 3D Asset Engineering

#### 11. `godot-game-dev`
* **In Simple Terms:** Expert guide for building games with the Godot Engine using clean, error-free GDScript 2.0.
* **When It Kicks In:** Writing Godot 4.x game logic, player controllers, UI menus, physics, or scene trees.
* **How It Works:** Enforces strict type safety (`var speed: float = 5.0`), clean signal connections between nodes ("signals up, functions down"), custom `Resource` files for game data, and fast headless testing with the GUT framework.
* **Why It Saves Quota:** Catches typos and script errors instantly via the command line without launching the full game window.

#### 12. `unreal-engine-dev`
* **In Simple Terms:** Best practices for Unreal Engine 5 C++ and Blueprints that prevent game crashes and memory leaks.
* **When It Kicks In:** Developing UE5 games, gameplay actors, user interfaces, or gameplay abilities.
* **How It Works:** Enforces Unreal's memory management rules (`UPROPERTY()`), subsystem architectures, and Enhanced Input systems so the game engine doesn't crash from lost or dangling pointers.
* **Why It Saves Quota:** Prevents cryptic Unreal crashes that usually require digging through massive 100MB log files.

#### 13. `unity-game-dev`
* **In Simple Terms:** High-performance C# guidelines for Unity that keep your game running at a smooth 60+ FPS without lag spikes.
* **When It Kicks In:** Writing Unity scripts, MonoBehaviours, ScriptableObjects, or UI Toolkit components.
* **How It Works:** Eliminates hidden memory allocations that trigger Unity's garbage collector, uses ScriptableObjects for modular data, and decouples game events with EventChannels.
* **Why It Saves Quota:** Prevents performance stutter and memory leaks before they ever reach the game engine.

#### 14. `game-engine-migration`
* **In Simple Terms:** The universal master blueprint for upgrading older games and mods to modern 64-bit systems, new graphics APIs (DirectX 11/Vulkan), and updated engines.
* **When It Kicks In:** Upgrading any 32-bit legacy game or mod to 64-bit, switching rendering pipelines, or modernizing older game engines.
* **How It Works:** Follows a 5-step checklist: checks dependencies, updates memory pointers and data alignment (so memory doesn't get corrupted), modernizes shader code, updates scripting bridges (like Lua), and runs side-by-side comparison tests.
* **Why It Saves Quota:** Replaces weeks of trial-and-error game crashes (`0xC0000005` memory errors) with a reliable, structured conversion recipe.

#### 15. `blender-3d-engineering`
* **In Simple Terms:** Creates 3D game models and props in Blender behind the scenes using automated Python scripts.
* **When It Kicks In:** Generating 3D props, weapons, buildings, or exporting assets to glTF or FBX format.
* **How It Works:** Runs Blender in "headless mode" (no graphic window needed) using Python math and modifiers (like bevel, mirror, and boolean cuts) to produce clean, watertight 3D models.
* **Why It Saves Quota:** Instead of typing out 50,000 raw 3D vertex numbers into the chat (which drains tokens in seconds), it generates a clean 30-line script that builds the mesh in seconds.

---

### ☢️ Game Modding (S.T.A.L.K.E.R. Ecosystem)

#### 16. `game-modding`
* **In Simple Terms:** Safety guardrails for modding games like S.T.A.L.K.E.R. Enhanced Edition, making sure configurations and textures don't break the game.
* **When It Kicks In:** Modding weapons, items, UI menus, textures, or game configurations.
* **How It Works:** Protects original game files by keeping them read-only, checks game configuration text files (LTX) for missing sections, ensures textures use the right compression (DXT1/DXT5), and preserves special audio headers.
* **Why It Saves Quota:** Stops the game engine from crashing on startup due to a single missing bracket or corrupted audio file.

#### 17. `xray-lua-scripting`
* **In Simple Terms:** Specialized scripting rules for the S.T.A.L.K.E.R. X-Ray game engine that prevent savegame corruption and game freezes.
* **When It Kicks In:** Writing quest scripts, inventory logic, NPC behaviors, or custom game mechanics in S.T.A.L.K.E.R.
* **How It Works:** Enforces strict nil-checks (verifying an enemy or item still exists before talking to it), prevents memory leaks in Lua, and ensures game saves stay clean.
* **Why It Saves Quota:** Avoids silent script freezes and prevents corrupted save files that ruin hours of playthroughs.

#### 18. `stalker2-modding`
* **In Simple Terms:** Modding toolkit for S.T.A.L.K.E.R. 2 Heart of Chornobyl (Unreal Engine 5).
* **When It Kicks In:** Creating mods for S.T.A.L.K.E.R. 2, packing game archives, or adding custom C++ and Lua gameplay hooks.
* **How It Works:** Automates packaging UE5 game containers (`.pak`, `.ucas`, `.utoc`) with proper compression using `repak` and sets up RE-UE4SS scripting hooks.
* **Why It Saves Quota:** Eliminates failed container packing and wrong compression settings that cause the game to ignore mods.

#### 19. `stalker-ogsr-migration`
* **In Simple Terms:** The expert specialist for porting older S.T.A.L.K.E.R. mods (like S.T.A.L.K.E.R. Complete 2009) to the modern, 64-bit OGSR Engine.
* **When It Kicks In:** Upgrading 32-bit Shadow of Chernobyl mods to the modern 64-bit OGSR engine.
* **How It Works:** Removes incompatible 32-bit DLL files, removes old DirectX 9 shaders that crash the modern DX11 renderer, updates script callbacks to LuaJIT, and converts level spawn files using ACDC.
* **Why It Saves Quota:** Directly solves the known causes of fatal startup crashes (`FATAL ERROR: Expression: !failed()`) without endless guesswork.

#### 20. `game-runtime-diagnostics`
* **In Simple Terms:** A master doctor for PC games that investigates why games crash, stutter, or refuse to launch on Windows and Linux (Steam Deck / Proton), and fixes them.
* **When It Kicks In:** Whenever a game crashes to desktop, freezes with a DirectX error, suffers from shader compilation stutter, or fails to launch in Steam Proton.
* **How It Works:** On Linux, parses Proton log streams (`PROTON_LOG=1`), configures DXVK async shader compilation, repairs broken Wine prefixes with Winetricks, and sets up DLL overrides. On Windows, reads Event Viewer crash logs (Event ID 1000), fixes GPU driver timeouts (TDRs), and repairs missing DirectX/Visual C++ runtimes.
* **Why It Saves Quota:** Pinpoints the exact missing dependency, broken codec, or corrupted shader cache instantly instead of blindly reinstalling 100GB games.

---

### 🎧 Audio Engineering & DSP

#### 21. `audio-dsp-tuning`
* **In Simple Terms:** Calibrates headphones to sound balanced and clear, and transforms any microphone into a studio-grade broadcast voice without background noise.
* **When It Kicks In:** Tuning headset audio, fixing muddy bass or piercing treble, eliminating microphone background noise (fans, keyboard clicks), or setting up stream audio.
* **How It Works:** Applies acoustic target curves (Harman Target via AutoEq) to headphones and sets up a professional 6-stage microphone processing chain (high-pass filter, AI noise suppression, surgical EQ, vocal compressor, de-esser, and brickwall limiter). Outputs ready-to-use profiles for EasyEffects (Linux) and Equalizer APO / Peace (Windows).
* **Why It Saves Quota:** Eliminates hours of manual trial-and-error audio tweaking and prevents incomprehensible voice audio during multiplayer gaming or calls.

---

### 💻 Systems, Reverse Engineering & Languages

#### 22. `cachyos-arch-packaging`
* **In Simple Terms:** Builds and packages Linux software, kernel drivers, and background services specifically for Arch Linux and CachyOS.
* **When It Kicks In:** Creating Arch/CachyOS packages (`PKGBUILD`), installing kernel drivers (like `omen-acpi`), or setting up systemd background services.
* **How It Works:** Enforces Arch packaging standards, checks integrity hashes, validates build dependencies in isolated chroots, and verifies systemd service files.
* **Why It Saves Quota:** Prevents broken package builds and keeps your Linux system clean, stable, and conflict-free.

#### 23. `reverse-engineer-anything`
* **In Simple Terms:** A deep inspection engine for understanding closed-source software, compiled games, and applications when no source code is available.
* **When It Kicks In:** Analyzing compiled binaries, Windows/Linux executables, Android packages, or web apps.
* **How It Works:** Deeply integrates with REA MCP to perform static disassembly, decompile code, reconstruct data structures, and keep an evidence ledger.
* **Why It Saves Quota:** Tracks findings in structured evidence summaries rather than dumping thousands of lines of raw, unreadable assembly into chat.

#### 24. `binary-re-workflows`
* **In Simple Terms:** Coordinates professional reverse engineering tools (like Ghidra, JADX, and network packet analyzers) under a strict scientific process.
* **When It Kicks In:** Inspecting unfamiliar game DLLs, network packets, or complex binary executables.
* **How It Works:** Combines static analysis and runtime tracing to test hypotheses about how closed-source binaries function.
* **Why It Saves Quota:** Turns confusing binary mysteries into deterministic, step-by-step discoveries.

#### 25. `standalone-binary-re`
* **In Simple Terms:** A fast, zero-setup toolkit for peeking inside binary files using standard Linux terminal tools—no heavy servers required.
* **When It Kicks In:** Inspecting executables, DLLs, or Android APKs when external MCP servers are offline or when you need answers in seconds.
* **How It Works:** Uses built-in Linux tools (`objdump`, `readelf`, `nm`, `strings`, `jadx`, `gdb`) and Python scripts to quickly inspect exported functions, headers, and text.
* **Why It Saves Quota:** Starts up instantly with zero overhead and filters out noise so you only see the functions you care about.

#### 26. `open-apk`
* **In Simple Terms:** Automatically opens, inspects, and decompiles Android mobile app packages (APKs) into readable Java code.
* **When It Kicks In:** Reverse engineering Android apps, mobile games, or APK packages.
* **How It Works:** Unpacks APK and DEX files directly into JADX headless analysis, searches classes and methods, and can download APKs directly via `apkeep`.
* **Why It Saves Quota:** Extracts only the exact Java classes you need instead of dumping hundreds of decompiled files into the chat context.

#### 27. `wakaru`
* **In Simple Terms:** Unpacks and unscrambles messy, minified JavaScript bundles (like from Webpack, Vite, or Electron) back into clean, organized files.
* **When It Kicks In:** Auditing modern web apps, Electron desktop software, or production JavaScript bundles.
* **How It Works:** Separates bundled web assets back into individual source files and translates minified shortcuts back into readable classes, async functions, and JSX.
* **Why It Saves Quota:** Turns a gigantic, unreadable 2MB single-line JavaScript file into clean, modular source files with zero hallucination.

#### 28. `lowlevel-dll-internals`
* **In Simple Terms:** A low-level guide for safely modifying Windows DLLs, game engine classes, and memory patches without crashing the game.
* **When It Kicks In:** Writing game mod plugins (like ASI plugins), hooking engine functions, or analyzing crash dumps.
* **How It Works:** Calculates computer memory offsets, 32-bit calling conventions (`__thiscall` in `ecx`), 64-bit ABI shadow space, and virtual function tables so memory patches don't cause instant crashes.
* **Why It Saves Quota:** Prevents dreaded `0xC0000005` "Access Violation" crashes by calculating memory addresses and calling conventions correctly the first time.

#### 29. `steamcmd-workshop-pipeline`
* **In Simple Terms:** Automates publishing and updating mods on the Steam Workshop from the command line without clicking through confusing web forms.
* **When It Kicks In:** Uploading new mods, pushing updates, setting preview images, or writing changelogs on Steam Workshop.
* **How It Works:** Generates valid Steam VDF configuration manifests, manages content depots, and executes SteamCMD commands automatically.
* **Why It Saves Quota:** Replaces error-prone manual upload attempts with an automated, verified deployment script.

#### 30. `python-engineering`
* **In Simple Terms:** Best practices for writing clean, fast, and bug-free modern Python code (Python 3.10+).
* **When It Kicks In:** Writing Python scripts, web APIs, automation tools, or test suites.
* **How It Works:** Enforces strict type hints (`mypy`), lightning-fast code formatting and linting (`ruff`), and comprehensive test suites (`pytest`).
* **Why It Saves Quota:** Catches bugs before code ever runs, saving countless turns of debugging runtime errors.

#### 31. `rust-engineering`
* **In Simple Terms:** Writes reliable, blazing-fast Rust code by working harmoniously with the Rust compiler.
* **When It Kicks In:** Writing systems software, game tools, performance-critical modules, or CLI utilities in Rust.
* **How It Works:** Follows Rust best practices for memory ownership, zero-cost abstractions, error handling with `Result` and `Option`, and strict Clippy lint checks.
* **Why It Saves Quota:** Eliminates runtime crashes completely—if it compiles cleanly in Rust, it works.

#### 32. `modern-cpp-engineering`
* **In Simple Terms:** Modern C++ (C++20/C++23) standards that eliminate old-school memory bugs, buffer overflows, and crashes.
* **When It Kicks In:** Writing game engine code, native libraries, or performance-critical C++ applications.
* **How It Works:** Uses smart pointers (`unique_ptr`, `shared_ptr`), RAII (automatic cleanup of resources), modern Concepts, and clean CMake build files.
* **Why It Saves Quota:** Prevents memory leaks, buffer overflows, and segmentation faults before they happen.

#### 33. `csharp-dotnet-engineering`
* **In Simple Terms:** High-performance modern C# and .NET (8/9) guidelines focused on zero-allocation and responsive async code.
* **When It Kicks In:** Writing C# backend services, desktop utilities, game plugins, or tools.
* **How It Works:** Uses memory-efficient types (`Span<T>`, `Memory<T>`), proper async cancellation tokens, and Roslyn code analyzers to keep apps fast.
* **Why It Saves Quota:** Prevents memory bloat and keeps background operations responsive and leak-free.

---

### 💰 Quota, Memory & Context Engineering

#### 34. `token-economy`
* **In Simple Terms:** The ultimate quota-saving protocol that eliminates robotic fluff, stops the AI from repeating itself, and stretches your daily AI usage limits by 2x to 3x.
* **When It Kicks In:** Always active in every conversation across Antigravity and Claude Code.
* **How It Works:**
  - **Zero Conversational Fluff:** Drops conversational preambles ("Sure, I can help with that!"), robotic fillers, and sign-offs.
  - **Zero Prompt Restatement:** Never echoes, paraphrases, or summarizes your prompt back to you; leads immediately with actionable technical data.
  - **Zero Code Duplication in Chat:** Once code is created or modified on disk, never re-pastes large code blocks into chat text. Uses file links, line ranges, and a 1-sentence rationale.
  - **High-Density Status:** Uses single-line checklist indicators (`[✓]`, `[→]`, `[!]`) instead of multi-paragraph narratives.
  - **Silent Tool Success:** Suppresses echoing successful terminal outputs; surfaces only actionable errors, diffs, and metrics.
  - **Surgical Edits:** Enforces targeted chunk replacements over full-file rewrites.
  - **Artifact Offloading:** Offloads extensive plans, logs, and designs to separate files referenced by 1-line clickable links.
  - **Token Economy Visibility:** Concludes multi-step workflows with a single high-density token savings metric line (`📉 Token Economy: ~<N> tokens saved (<breakdown>)`).
* **Measured Savings Breakdown (per 10-turn engineering session):**

| Optimization | Typical Unconstrained Waste | Strict Token Economy | Output Tokens Saved |
| :--- | :--- | :--- | :--- |
| **No Code Duplication** | Pasting 4 edited functions into chat (~500 tok ea) | File links & line ranges only | **~2,000 tokens** |
| **Silent Tool Success** | Echoing 2 full test/build logs (~400 tok ea) | 1-line metric tallies | **~800 tokens** |
| **No Prompt Restatements** | Paraphrasing prompt on 10 turns (~75 tok ea) | Direct technical lead | **~750 tokens** |
| **No File Tree Echoes** | Pasting sprawling 30-line `tree` outputs | Changed paths only | **~450 tokens** |
| **Surgical Chunk Edits** | Re-writing whole files to change 3 lines | Targeted diff chunks | **~2,500+ tokens** |
| **Total Session Savings** | | | **~6,500 Output Tokens** |

* **Compounding Context Multiplier:** Because past conversation output tokens are re-ingested as input prompt tokens on every subsequent turn, saving 6,500 output tokens in early turns prevents re-reading **~35,000–60,000 cumulative prompt tokens** across a 15-turn session, extending rolling 5-hour quota limits by **2x to 3x**.

#### 35. `project-memory-bank`
* **In Simple Terms:** A smart project notebook that stores your project's architecture and lessons learned, so the AI never forgets what you're working on across restarts.
* **When It Kicks In:** Starting work on a repository, resuming multi-session tasks, or before running `/compact`.
* **How It Works:**
  - Maintains concise, persistent markdown files in `.agents/memory/`:
    - `projectBrief.md`: Project scope, tech stack, and goals (<300 tokens).
    - `systemPatterns.md`: Code architecture and directory conventions (<400 tokens).
    - `activeContext.md`: Current objective, recent changes, and immediate next steps (<300 tokens).
    - `learnings.md`: Solved engine gotchas, compiler traps, and environment fixes (<500 tokens).
  - **Instant Hydration:** Reads `activeContext.md` upon session start instead of scanning 30 source files.
  - **Lossless Compaction:** Saves state before `/compact`, clearing out 100k-token conversation histories while retaining 100% working context.
* **Why It Saves Quota:** Saves 15,000–50,000 exploration tokens on every new session and prevents the AI from re-debugging known issues.

---

## 📊 Real-Time Dual-CLI Quota & Statusline Monitors

The suite includes **dedicated, tailor-made statusline monitors** for both CLIs:

### 1. Claude Code CLI Dedicated Monitor (`claude-statusline`)
Installed to `~/.local/bin/claude-statusline` and configured in `~/.claude/settings.json`. Intercepts Claude Code's live `stdin` telemetry stream to render model, rate limits, visual context gauge, session cost, and git worktree:
```text
⚡ Claude [Sonnet 3.7] | 5h: 72% (reset 17:00) | Wk: 86% | 🧠 Ctx: [█░░░░░] 22% | 💲 $0.06 +45/-12
```
* **Visual Context Gauge:** Dynamic progress bar showing real-time token consumption of your 200k context window.
* **Rolling Quotas:** Real-time remaining percentages for 5-hour and 7-day limits with exact reset countdowns.
* **Diff & Cost Telemetry:** Real-time session spend in USD alongside cumulative lines added/removed (`+45/-12`).

### 2. Antigravity CLI Dedicated Monitor (`agy-quota-statusline`)
Installed to `~/.local/bin/agy-quota-statusline` and configured in `~/.gemini/antigravity-cli/settings.json`:
```text
⚡ Gemini: 5h: 78% (reset 16:00) | Wk: 72% | 💾 Saved: 23.7M tok (Flash)
```
In multi-model sessions (e.g. adaptive escalation between Flash and Argon):
```text
⚡ Gemini: 5h: 78% | Wk: 72% | 💾 Saved: 23.4M tok (Argon: 12.0M | Flash: 11.4M)
```
* **Context Cache Token Telemetry:** Correlates active session step tokens from `transcript.jsonl` with turn models in `gen_metadata` to display exact prompt tokens saved by context caching.
* **Asynchronous & Non-Blocking Quota:** Queries `agy -p /usage` and caches the result in `/tmp/agy_quota_cache.txt` with a 2-minute TTL.
* **Zero CLI Lag:** Subprocesses are detached with PID lockfile protection (`/tmp/agy_quota_refresh.lock`), guaranteeing instantaneous prompt rendering (<2ms).

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

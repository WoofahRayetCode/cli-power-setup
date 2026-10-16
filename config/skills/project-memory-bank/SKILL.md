---
name: project-memory-bank
description: Persistent project memory and context curation system. Use when starting sessions on existing codebases, resuming tasks, recording architectural decisions, logging bug solutions, or preparing state before running /compact to slash token usage.
---

# Project Memory Bank & Context Curation

This skill maintains a lightweight, persistent memory layer inside the project directory (`.agents/memory/`). It slashes token consumption by eliminating repetitive codebase discovery and preventing context rot during long or multi-session workflows.

---

## 1. Memory Bank Architecture

The memory bank lives in `.agents/memory/` at the root of the project:

```text
.agents/memory/
├── projectBrief.md    # Scope, core tech stack, and non-negotiable constraints (<300 tokens)
├── systemPatterns.md  # Architectural design, directory structure, key patterns (<400 tokens)
├── activeContext.md   # Current task state, recent decisions, immediate next steps (<300 tokens)
└── learnings.md       # Solved gotchas, engine quirks, platform-specific fixes (<500 tokens)
```

> **Quota Rule:** Memory files must be high-density markdown bullet points—never verbose essays. Keep each file under 80 lines to ensure instant, cheap context hydration.

---

## 2. Frontier Tool Integrations & Bindings

* **Symbol Index Graph Binding (`semantic-codebase-indexing`):**
  Record the location and status of `.code_index_tags.json` inside `systemPatterns.md`. On session start, query the symbol index in 10ms instead of running recursive `grep` searches.
* **Persistent Research Vault (`deep-research-synthesizer`):**
  Store deep technical whitepapers in `.agents/research/<topic>.md`. Check this directory before performing new web searches to prevent duplicate research.
* **Deliberative Reasoning Trade-off Logging (`deliberative-reasoning-tree`):**
  When Tree-of-Thought explores 3 hypothesis branches and rejects 2 during adversarial critique, log the rejected approaches and root causes into `learnings.md` so future sessions never repeat dead-end experiments.
* **Canvas Draft Tracking (`canvas-interactive-workspace`):**
  Include any in-progress `.canvas/*.draft` files in `activeContext.md` before session compaction.
* **Brand & Design Token Binding (`human-crafted-web-design`):**
  Record brand colors, font families, and dark-mode surface hex codes in `systemPatterns.md` to prevent UI drift and eliminate repetitive color re-queries.
* **Interactive UI & Micro-App State (`intelligent-interactive-ui`):**
  Record active interactive calculators, forms, and widget paths in `systemPatterns.md` so future sessions build upon existing single-file tools rather than regenerating from scratch.
* **Visual Inspection & Display Quirks (`screen-vision-inspector`):**
  Log display resolution scaling, multi-monitor geometry offsets, and visual layout quirks into `learnings.md` to prevent repeated vision troubleshooting.
* **High-Density Prompt Conventions (`high-density-prompting`):**
  Record project-specific shorthand aliases and target verification commands in `projectBrief.md`.
* **Client & Business Terms Binding (`executive-business-communications`):**
  Record billing milestones, deliverable boundaries, and strict revision caps in `projectBrief.md` to maintain scope boundaries across multi-session tasks.
* **Video Production & Content Presets (`video-production-automation` & `youtube-shorts-video-automation`):**
  Record target export bitrates, NVENC preset choices, loudness targets (-14 LUFS), and subtitle styling rules (font, outline, primary color) in `systemPatterns.md`.
* **Android Target & Emulation Binding (`android-device-automation` & `emulator-development-engineering`):**
  Record target ADB serial numbers, screen resolution bounds, touch coordinates for critical UI elements, and emulator build targets (e.g. Vulkan backend, JIT target architecture) in `systemPatterns.md`.
* **Graphics Pipeline & Shader Bindings (`shader-cross-compilation`, `real-time-rendering-pipeline`, `game-texture-material-pipeline`):**
  Record target graphics API (Vulkan 1.3 / D3D12 / WebGPU), clip space conventions, normal map Y-axis orientation (DirectX Y- vs OpenGL Y+), texture compression formats (BCn vs ASTC), and descriptor binding layouts in `systemPatterns.md`.
* **Skills Health & Synchronization Telemetry (`skills-updater-and-auditor`):**
  Record last-audited skill count, missing host dependencies, and upstream commit sha in `systemPatterns.md` to prevent repetitive dependency rediscovery across sessions.
* **Android Engineering & NDK Stack Binding (`android-app-engineering`, `android-compose-ui-ux`, `android-architecture-jetpack`, `android-ndk-jni-engineering`):**
  Record target Android SDK version (e.g. API 35), minimum SDK, NDK ABI filters (`arm64-v8a`, `armeabi-v7a`), Room database schema version, and Compose compiler metrics in `systemPatterns.md`.
* **Episodic Narrative & Milestone Checkpoints (`session-episodic-memory`):**
  Link active chronological episode logs (`.agents/episodes/<timestamp>_<task>.md`) inside `activeContext.md` before `/compact` to preserve the reasoning trail across compaction cycles.
* **Game Engine Architecture & VFS Bindings (`game-audio-engine-engineering`, `game-physics-collision-pipeline`, `game-memory-allocator-engineering`, `game-input-system-abstraction`, `game-asset-pack-archive-engineering`):**
  Record physics fixed timestep (`fixedDelta = 1/60.0f`), primary memory allocator strategy (Linear Arena vs TLSF), audio sample rate/voice limits, radial deadzone configurations, and VFS pack mount priority hierarchy in `systemPatterns.md`.
* **Gameplay Systems & Networked Runtime Bindings (`game-entity-component-system`, `game-animation-skeletal-pipeline`, `game-networking-state-sync`, `game-save-state-serialization`, `game-debug-ui-tools`):**
  Record ECS storage archetype model (Flecs vs EnTT), skeletal joint limit configurations, network server tick rate / interpolation buffer delay ($60\text{--}100\text{ms}$), save state schema version integer, and registered runtime CVars in `systemPatterns.md`.
* **Discord Bot Architecture & Gateway Bindings (`discord-bot-engineering`):**
  Record bot client runtime (discord.py vs discord.js), required gateway intents bitmask, application ID, test guild IDs, and Redis caching topology in `systemPatterns.md`.
* **Procedural & Generative Audio Bindings (`ai-procedural-audio-generation`):**
  Record target output sample rate (default $48\text{kHz}$), target integrated loudness ($-14\text{ LUFS}$ YouTube / $-16\text{ LUFS}$ Mobile / $-24\text{ LUFS}$ Game Engine), and procedural SFX preset directories in `systemPatterns.md`.
* **Security, Anti-Tamper & Cryptographic Bindings (`game-security-anti-tamper`, `cryptographic-security-engineering`, `devsecops-supply-chain-security`, `app-security-threat-modeling`, `api-network-security-hardening`, `client-memory-integrity-anticheat`):**
  Record binary checksec audit status (RELRO, Canaries, NX, PIE), HMAC signing key rotation cycles, Ed25519 public keys, GitHub Actions SHA pins, STRIDE threat vectors, rate limit thresholds, and memory obfuscation schemes in `systemPatterns.md`.
* **Game Compatibility & Proton Development Bindings (`cross-platform-game-compatibility`, `linux-gaming-proton-optimization`, `game-patching-binary-repair`, `proton-game-dev-linux`, `steamdeck-proton-hardware-tuning`, `wine-proton-native-interop`):**
  Record target Steam AppID, wineprefix path, LAA 4GB PE header status, `dxvk.conf` flags (e.g. `enableAsync`, `maxFrameLatency`), required DLL overrides (`WINEDLLOVERRIDES`), Steam Deck 40Hz/45Hz targets, font scale thresholds, and Wine named pipe paths in `systemPatterns.md` and `learnings.md`.
* **GameMaker & GML Architecture Bindings (`gamemaker-gml-engineering`):**
  Record GameMaker runtime version, YYP project root, target texture page sizes ($2048\times2048$ default), custom texture groups, and active surface IDs in `systemPatterns.md`.
* **Game Trainer & Memory Hook Bindings (`game-trainer-engineering`):**
  Record verified multi-level pointer offsets, base module names, AOB signature byte masks, and detour hook addresses in `systemPatterns.md` and `learnings.md`.
* **Game Localization & Internationalization Bindings (`game-localization-i18n`):**
  Record supported locales (BCP 47 language tags), active translation catalog formats (PO/JSON/CSV), RTL layout mirrors, ICU pluralization rules, and fallback font chains (Noto Sans CJK, Cyrillic) in `systemPatterns.md`.
* **Headless Game CI & Build Automation Bindings (`headless-game-ci-automation`):**
  Record target engine CLI execution flags (`--headless`, `-batchmode -nographics`, `RunUAT.sh`), test runner configurations (Godot GUT, Unity UTF), artifact export paths, and packaging matrices in `systemPatterns.md`.
* **Godot Shader & VFX Material Bindings (`godot-shader-vfx`):**
  Record active Godot 4 shader types (`spatial`, `canvas_item`, `particles`), `hint_screen_texture` sampler usages, compute particle pipeline buffers, and material parameter defaults in `systemPatterns.md`.
* **Hierarchical Memory & Context Retrieval Bindings (`hierarchical-memory-retrieval`):**
  Record active memory directories (`.agents/memory/`, `.agents/episodes/`, `.agents/checkpoints/`), top-k retrieval thresholds, and BM25 search parameters in `systemPatterns.md`.
* **Context Budgeting & Governor Headroom Bindings (`context-window-governor`):**
  Record model-specific context window ceiling (200k vs 1M), turn-level partition budgets (20% rules / 35% code / 25% output / 20% generation), and clamp line thresholds in `systemPatterns.md`.
* **Working Memory State Checkpoint Bindings (`working-memory-checkpointing`):**
  Record active checkpoint retention limit (`--keep 5`), dirty state patch files in `.agents/checkpoints/`, and branch snapshot metadata in `activeContext.md`.
* **CodeRabbit AI Review & PR Gate Bindings (`coderabbit-ai-review`):**
  Record last PR readiness score (0–100), active review reports in `.agents/reviews/`, open blocking critical/major findings, and PR gate status (APPROVE / REQUEST_CHANGES) in `progress.md`.
* **Console Game Decompilation & Binary Split Bindings (`console-game-decompilation`):**
  Record target console platform (PS1/PS2/PS3/Xbox/Xbox360), executable format, base RAM load address, identified compiler toolchain (e.g. GCC 2.7.2, CodeWarrior GC), and active `splat.yaml` configuration in `systemPatterns.md`.
* **Game Screen Telemetry & Anomaly Logging Bindings (`game-screen-telemetry-monitor`):**
  Record target game window title, display capture backend (`spectacle` Wayland / X11), active telemetry session output directory (`.agents/telemetry/` or `/tmp/`), known missing texture false positives, and OCR crash pattern signatures in `systemPatterns.md` and `learnings.md`.
* **Autonomous Goal Contract & Circuit Breaker Bindings (`autonomous-goal-governor`):**
  Record active goal contract ID, verification command, current phase number (1/2/3), active task strike counts, and circuit breaker trip state in `.agents/goals/current_goal.json` and `activeContext.md`.
* **Fursona Profile & Refsheet Asset Bindings (`furry-fursona-art-design`):**
  Record active character profile JSON path, species archetype, digitigrade vs plantigrade configuration, official palette hex codes, and 3D VRChat avatar specs in `.agents/fursonas/` and `systemPatterns.md`.
* **Android ROM & Device Tree Bindings (`android-rom-os-engineering`):**
  Record target OEM vendor, device codename, SoC architecture, `BOARD_SUPER_PARTITION_SIZE` budget, kernel branch/commit, and active device tree path (`device/<vendor>/<codename>/`) in `systemPatterns.md` and `learnings.md`.
* **Game QA Playtest Locomotion & Profile Bindings (`game-qa-playtest-controller`):**
  Record active playtest locomotion pattern (`orbit`, `sweep`, `wander`, `stress-locomotion`, `action-cycle`), mouse yaw sensitivity deltas, uinput device capability state, and test replay logs in `.agents/playtest/` and `systemPatterns.md`.
* **Machine Vision Suite & Calibration Bindings (`computer-vision-deep-learning`, `industrial-machine-vision-inspection`, `visual-document-ocr-intelligence`, `agentic-visual-perception`):**
  Record active vision model weights (ONNX/PyTorch path), inference execution provider (`CUDAExecutionProvider` / TensorRT), camera intrinsic matrix JSON path, optical scale ratio ($px/mm$), OCR language dictionary (`eng`), and SAHI slice dimensions ($640\times640$, 20% overlap) in `systemPatterns.md`.
* **Local Hardware Offloading Bindings (`local-model-coprocessor`, `local-vector-rag-engine`, `local-ast-compiler-engine`):**
  Record active local model name (`qwen2.5-coder:1.5b`), server endpoint (`http://localhost:11434`), RAG vector index path (`.agents/rag/index.json`), host CPU thread saturation count (`nproc`), and AST cache paths in `systemPatterns.md`.
* **Self-Improving Testing Suite Bindings (`game-exploratory-fuzzing`, `self-healing-test-automation`, `coverage-guided-mutation-testing`):**
  Record active QA input corpus path (`.qa_corpus/`), minimal crash reproduction replay scripts, healed locator patch history (`.agents/healed_locators/`), surviving mutant manifests (`.agents/mutants/`), and mutation score percentages in `systemPatterns.md` and `learnings.md`.
* **Cross-CLI Handoff & Session State Bindings (`cross-cli-session-handoff`):**
  Record active `.agents/handoff.json` packet status, source CLI environment (Antigravity / Claude Code / Cursor), git diff snapshot paths (`.agents/checkpoints/handoff_*.diff`), and current blocking task in `activeContext.md` to guarantee zero-loss session transitions.
* **Legacy Engine Cartography & Pruning Bindings (`legacy-codebase-cartographer`):**
  Record active omit manifest path (`.agents/audit/omit_manifest.txt`), excluded build targets, and unreferenced translation units in `systemPatterns.md` to prevent dead-code porting.
* **Autonomous Error Recovery & Crash Archive Bindings (`agent-error-recovery-sentinel`):**
  Record active crash logs (`.agents/crashes/`), modal dismissal counts, cleared lock files, and zombie process recovery metrics in `learnings.md`.
* **Model-Optimal State Serialization Bindings (`model-optimal-state-serializer`):**
  Format `activeContext.md` and compaction snapshots using target tokenizer layouts (XML-KV for Claude BPE, Pipe-TSV for Gemini SentencePiece, compact symbol coordinates `<file>#L<line>:<sig>`) to compress state size by 60–80% (<350 tokens).

---

## 3. Token-Saving Lifecycle Protocols

### A. Session Startup (Hydration over Exploration)
* **Do NOT** run broad recursive searches, read 30 source files, or re-grep the repository when starting a session.
* **Instead:** Check if `.agents/memory/activeContext.md` exists:
  * If present: read `activeContext.md` first. You are instantly up to speed in <300 tokens.
  * If missing: initialize the memory bank after completing your initial assessment.

### B. Bug & Gotcha Logging (Zero Re-Debugging)
* When a tricky bug, compiler quirk, or game engine crash is diagnosed and resolved, append a 2-3 line entry to `.agents/memory/learnings.md`. This prevents future sessions from repeating failed hypotheses and burning quota on known issues.

### C. Safe Session Compaction (`/compact` & `context-pruning-watchdog`)
* When active context crosses ~120k tokens (60%):
  1. Update `.agents/memory/activeContext.md` with current completed steps, open blockers, and immediate next tasks.
  2. Advise running `/compact`.
  3. Upon resuming, re-reading `activeContext.md` restores 100% of working context while freeing up the entire conversation history.

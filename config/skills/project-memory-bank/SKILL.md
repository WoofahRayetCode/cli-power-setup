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
* **Game Compatibility & Proton Tuning Bindings (`cross-platform-game-compatibility`, `linux-gaming-proton-optimization`, `game-patching-binary-repair`):**
  Record target Steam AppID, wineprefix path, LAA 4GB PE header status, `dxvk.conf` flags (e.g. `enableAsync`, `maxFrameLatency`), required DLL overrides (`WINEDLLOVERRIDES`), and custom binary patches in `systemPatterns.md` and `learnings.md`.

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

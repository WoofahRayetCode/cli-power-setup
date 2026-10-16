---
name: adaptive-reasoning
description: Automatic reasoning effort selection and cognitive complexity routing. Automatically scales between instant-speed execution on Flash and deep-reasoning planning on Argon based on prompt complexity.
---

# Adaptive Reasoning & Cognitive Complexity Routing

This skill governs automatic reasoning selection and model escalation to maximize response speed and minimize quota consumption.

---

## Cognitive Complexity Tiers

Before beginning work on any user request, evaluate the prompt's structural complexity:

### Tier 1: Trivial / Direct Execution
* **Triggers:** Single-line fixes, simple typo corrections, direct shell commands, asking for file locations, formatting, quick status checks, inspecting LAA 4GB PE flags (`laa_pe_patcher.py`), semantic skill matching (`dynamic-skill-router`), or skill health audits/sync (`skills-audit-update`).
* **Reasoning Strategy:**
  * Zero extended deliberation.
  * When uncertain which skill to activate among 146+ choices, run `skill_router.py "<prompt>"` in <20ms to pinpoint the exact 2-3 expert skills.
  * Apply immediate pinpoint diffs via `replace_file_content` or execute terminal commands directly.
  * Run with standard/low thinking latency (keeps streaming instant and saves quota).

### Tier 2: Standard Engineering & Implementation
* **Triggers:** Implementing a specific function, refactoring a single module, writing unit tests, fixing a verified bug, session milestone checkpointing (`session-episodic-memory`), video production scripts, vertical shorts generation, Android device automation, Jetpack Compose UI screens, Android architecture/Room flows, Android testing/release hardening, shader translation/validation, PBR texture channel packing, cross-platform input mapping (`game-input-system-abstraction`), VFS container asset packing (`game-asset-pack-archive-engineering`), save state serialization & inspection (`game-save-state-serialization`), in-engine debug UI / CVars (`game-debug-ui-tools`), Discord bot slash commands / UI modals (`discord-bot-engineering`), procedural SFX synthesis & audio normalization (`ai-procedural-audio-generation`), binary hardening checksec audits (`devsecops-supply-chain-security`), cryptographic HMAC signing/verification (`cryptographic-security-engineering`), save file tamper sealing (`game-security-anti-tamper`), game 4GB LAA patching & DirectX legacy wrapping (`cross-platform-game-compatibility`), Proton/Wine prefix repair & dxvk.conf tuning (`linux-gaming-proton-optimization`), binary dependency checking (`game-patching-binary-repair`), STRIDE threat modeling & path traversal defense (`app-security-threat-modeling`), token bucket API rate limiting & certificate pinning (`api-network-security-hardening`), obfuscated value memory protection & anti-debugging (`client-memory-integrity-anticheat`), case-sensitive asset normalization & headless Proton testing (`proton-game-dev-linux`), Steam Deck 40Hz frame pacing & font scaling (`steamdeck-proton-hardware-tuning`), Wine named pipe IPC & DLL thunking (`wine-proton-native-interop`), GameMaker GML constructors/structs & volatile surface management (`gamemaker-gml-engineering`), game trainer memory scanning & mid-function code injection (`game-trainer-engineering`), ICU message format / pluralization (`game-localization-i18n`), headless CI game engine builds / automated testing (`headless-game-ci-automation`), Godot 4 screen-reading shaders / VFX compute particles (`godot-shader-vfx`), BM25 hierarchical memory retrieval (`hierarchical-memory-retrieval`), token budget partitioning & output containment clamping (`context-window-governor`), atomic working state snapshotting & hypothesis rollback (`working-memory-checkpointing`), CodeRabbit PR code review & architectural walkthrough generation (`coderabbit-ai-review`), console game decompilation & matching reverse engineering (`console-game-decompilation`), real-time game screen telemetry monitoring & crash dialog OCR (`game-screen-telemetry-monitor`), autonomous multi-axis game testing locomotion & action cycling (`game-qa-playtest-controller`), autonomous `/goal` execution & 3-strike circuit breaker governance (`autonomous-goal-governor`), fursona/furry character design, turnaround refsheets, digitigrade anatomy prompt translation & palette swatch rendering (`furry-fursona-art-design`), Android custom ROM development, AOSP/LineageOS device tree bring-up, proprietary blob extraction & SELinux sepolicy triage (`android-rom-os-engineering`), neural object detection & segmentation (`computer-vision-deep-learning`), camera calibration & precision metrology (`industrial-machine-vision-inspection`), document OCR & table extraction (`visual-document-ocr-intelligence`), agentic visual grounding & SAHI high-resolution perception (`agentic-visual-perception`), local SLM coprocessor offloading (`local-model-coprocessor`), local vector semantic search RAG (`local-vector-rag-engine`), multithreaded AST syntax inspection (`local-ast-compiler-engine`), or skill lifecycle maintenance.
* **Reasoning Strategy:**
  * When incoming requests are verbose or conversational, activate `high-density-prompting` to distill into a 4-part surgical directive.
  * When logging architectural decisions (ADRs) or preparing for `/compact`, route to `session-episodic-memory` to write a high-density episode record into `.agents/episodes/`.
  * When the user requests calculators, data models, or parameter tuning, route to `intelligent-interactive-ui` to generate a reactive single-file micro-app.
  * When auditing, verifying permissions, or syncing installed skills across CLIs, route to `skills-updater-and-auditor`.
  * When building Android UI, edge-to-edge layouts, or fixing recomposition jank, route to `android-compose-ui-ux`.
  * When architecting Android data layers, Room migrations, Navigation DSL, or WorkManager, route to `android-architecture-jetpack`.
  * When authoring Android tests (JUnit, MockK, Robolectric) or configuring R8 rules, route to `android-testing-ci-cd-security`.
  * When transcoding, clipping, or editing video, route to `video-production-automation` and `youtube-shorts-video-automation` for hardware-accelerated NVENC AV1/HEVC pipelines.
  * When automating mobile device maintenance, debloating, or screen observation, route to `android-device-automation`.
  * When compiling/validating shaders (HLSL/GLSL/SPIR-V) or converting texture channels/normal maps, route to `shader-cross-compilation` and `game-texture-material-pipeline`.
  * When implementing controller deadzones, glyph switching, or mouse delta sub-pixel smoothing, route to `game-input-system-abstraction`.
  * When packing game mod containers or designing virtual file systems, route to `game-asset-pack-archive-engineering`.
  * When inspecting or migrating save file binary containers and schema versions, route to `game-save-state-serialization`.
  * When embedding ImGui debug windows, runtime CVars, or 3D primitive drawing overlays, route to `game-debug-ui-tools`.
  * When developing Discord bot slash commands, buttons, modals, select menus, or calculating permission/intent bitmasks, route to `discord-bot-engineering`.
  * When synthesizing game sound effects, procedural chiptune audio, UI interaction sounds, or normalizing audio to platform LUFS standards, route to `ai-procedural-audio-generation`.
  * When auditing binary compiler hardening (RELRO, Canaries, NX, PIE) or scanning dependencies (SBOM), route to `devsecops-supply-chain-security`.
  * When generating secure entropy keys, verifying HMAC-SHA256 signatures, or deriving subkeys with HKDF, route to `cryptographic-security-engineering`.
  * When sealing save files with HMACs, mitigating DLL hijacking, or checking anti-tamper integrity, route to `game-security-anti-tamper`.
  * When patching 32-bit game PE headers with Large Address Aware, resolving legacy DirectX wrappers, or constraining multi-core thread affinities, route to `cross-platform-game-compatibility`.
  * When repairing Wine prefixes, tuning dxvk.conf, switching to GE-Proton for media codecs, or configuring Gamescope/GameMode, route to `linux-gaming-proton-optimization`.
  * When resolving missing DLL imports, analyzing crash offsets, or applying surgical binary byte patches, route to `game-patching-binary-repair`.
  * When threat modeling application architectures with STRIDE, sanitizing path traversal, or zeroing secret buffers, route to `app-security-threat-modeling`.
  * When configuring TLS 1.3 ciphers, token bucket rate limiters, or verifying webhook signatures, route to `api-network-security-hardening`.
  * When protecting game memory against Cheat Engine scanners (XOR obfuscation) or detecting debuggers/hooks, route to `client-memory-integrity-anticheat`.
  * When architecting Windows games to run smoothly on Proton (case-sensitivity normalization, open media codecs, headless CI Proton runners), route to `proton-game-dev-linux`.
  * When optimizing for Steam Deck / handheld hardware (15W APU TDP budget, 40Hz frame pacing, 1280x800 resolution, legible UI fonts), route to `steamdeck-proton-hardware-tuning`.
  * When bridging Windows and native Linux via Wine named pipes, shared memory, or DLL call thunking, route to `wine-proton-native-interop`.
  * When writing GameMaker GML scripts, lightweight constructors/structs, state machines, volatile surface memory, or texture group batching, route to `gamemaker-gml-engineering`.
  * When developing game trainers, pointer chain resolvers, AOB pattern scans, or mid-function code injection hooks (Windows/Linux/Proton), route to `game-trainer-engineering`.
  * When extracting localization strings, authoring ICU plural rules, configuring BiDi/RTL layout, or validating font fallbacks, route to `game-localization-i18n`.
  * When setting up headless game engine builds, running CLI test suites (Godot GUT, Unity batchmode, UE5 RunUAT), or automating GitHub Actions release packaging, route to `headless-game-ci-automation`.
  * When authoring Godot 4 visual shaders, screen-reading distortion effects, foliage wind vertex displacement, or GPU compute particle shaders, route to `godot-shader-vfx`.
  * When retrieving past architectural decisions or searching episodic logs without loading full files, route to `hierarchical-memory-retrieval`.
  * When budgeting context headroom, clamping verbose command outputs, or estimating token weights, route to `context-window-governor`.
  * When testing speculative fixes or alternative hypotheses during complex refactors, route to `working-memory-checkpointing` to snapshot state before modification.
  * When auditing pull requests, generating architectural sequence diagrams, or reviewing diffs with 1-click GitHub suggestions, route to `coderabbit-ai-review`.
  * When inspecting console executables (PS-X EXE, ELF, XBE, XEX), configuring splat binary splitting, or matching ancient compiler assembly, route to `console-game-decompilation`.
  * When running game QA, validating engine ports (e.g. S.T.A.L.K.E.R. Complete to OGSR), or verifying games without user input, orchestrate `game-qa-playtest-controller` with `game-screen-telemetry-monitor` and `agentic-visual-perception` to autonomously take control of character movement, detect missing textures/freezes, and extract crash dialogs.
  * When automating game testing locomotion, circle-strafing orbits, 360° panoramic camera sweeps, obstacle wandering, or action cycle stress testing, route to `game-qa-playtest-controller`.
  * When executing `/goal` runs or multi-hour autonomous tasks, route to `autonomous-goal-governor` to formulate verifiable exit contracts, enforce 3-strike circuit breaker rollbacks, and guide phased `/compact` milestones.
  * When designing fursonas, generating anthro character refsheets, or formulating model-specific prompts for SDXL/Pony/Midjourney/Flux, route to `furry-fursona-art-design`.
  * When porting AOSP/LineageOS ROMs, configuring device trees, sizing dynamic super partitions, or resolving SELinux avc denials, route to `android-rom-os-engineering`.
  * When designing or deploying neural vision models (YOLO, SAM 2, RT-DETR) or optimizing ONNX/CUDA inference pipelines, route to `computer-vision-deep-learning`.
  * When calibrating camera intrinsics, performing geometric dimensioning (GD&T), or matching templates with normalized cross-correlation, route to `industrial-machine-vision-inspection`.
  * When preprocessing scanned documents, running multi-engine OCR, or extracting structured table grids, route to `visual-document-ocr-intelligence`.
  * When grounding natural language queries into UI screen coordinates, tiling 4K canvases with SAHI, or verifying visual state diffs, route to `agentic-visual-perception`.
  * When generating boilerplate, docstrings, commit messages, or triaging verbose compiler logs, route to `local-model-coprocessor` to run on local GPU/RAM with 0 cloud tokens billed.
  * When searching large codebases or documentation without stuffing thousands of lines into prompt context, route to `local-vector-rag-engine`.
  * When checking syntax, scanning function/class symbol tables, or verifying code structure across all CPU cores in parallel, route to `local-ast-compiler-engine`.
  * When executing evolutionary action mutation, novelty-guided state exploration, or bisecting crash traces to minimal reproduction sequences, route to `game-exploratory-fuzzing`.
  * When repairing broken UI selectors, multi-vector locator matching (role, text, OCR), or mitigating test flakiness, route to `self-healing-test-automation`.
  * When injecting AST fault mutants (conditional/arithmetic/boolean) to evaluate test quality and synthesize regression assertions, route to `coverage-guided-mutation-testing`.
  * Follow Test-Driven Development (`test-driven-development`) or targeted debugging (`systematic-debugging`).
  * Sanitize tool outputs using `log-output-sanitizer`.
  * Rely on compiler/linter feedback (e.g. `cargo check`, `ruff`, `clang-tidy`, `pytest`, `spirv-val`).
  * Execute directly on Gemini 3.8 Flash using surgical diffs.

### Tier 3: Deep Architectural & Multi-System Design
* **Triggers:** Designing new mods, multi-file refactoring, kernel modules (`omen-acpi`), reverse engineering unfamiliar binaries, visual layout diagnostics, console emulator architecture, game AI reinforcement learning agents, Android NDK C++ native engines/JNI bridges, low-level Android battery/jank profiling, modern rendering engine architectures (Vulkan/DX12), frame graph design, graphics optimization/culling, cinematic post-processing pipelines, real-time spatial audio DSP engines, fixed-timestep physics accumulators & narrowphase solvers, custom memory allocators (Arena/Pool/TLSF), ECS Archetype/Sparse-Set architecture (`game-entity-component-system`), skeletal animation dual-quaternion skinning & IK solvers (`game-animation-skeletal-pipeline`), multiplayer client prediction & state synchronization (`game-networking-state-sync`), sharded Discord bot cluster architectures (`discord-bot-engineering`), adaptive multi-stem soundtrack composition (`ai-procedural-audio-generation`), anti-cheat server simulation sanity architectures (`game-security-anti-tamper`), applied cryptographic protocol engineering (`cryptographic-security-engineering`), or multi-camera stereo depth perception and neural vision backbone training (`computer-vision-deep-learning`).
* **Reasoning Strategy:**
  * Activate `deliberative-reasoning-tree` to explore 3 branching hypothesis paths and conduct adversarial self-critique before writing code.
  * For live visual layout glitches, GUI rendering anomalies, or game HUD overlaps, route desktop/window capture to `screen-vision-inspector`.
  * For Android native NDK, JNI memory pinning, Oboe audio, or tombstone symbolization, route to `android-ndk-jni-engineering`.
  * For Android frame jank, dumpsys gfxinfo analysis, or battery wake lock profiling, route to `android-perf-battery-profiling`.
  * For game AI training, state recognition, or input emulation, route to `game-ai-agent-play`.
  * For dynamic binary recompilation (JIT), MMU fastmem, or cycle-accurate timing in emulators, route to `emulator-development-engineering`.
  * For modern rendering architectures, bindless descriptors, and frame graphs, route to `real-time-rendering-pipeline`.
  * For rendering bottlenecks, Hi-Z occlusion culling, and TAA/FSR upscaling, route to `game-graphics-optimization-profiling`.
  * For HDR tone mapping, progressive bloom, and cascaded shadow maps, route to `post-processing-visual-fx`.
  * For lock-free spatial audio callbacks, 3D HRTF convolution, and bus mixing hierarchies, route to `game-audio-engine-engineering`.
  * For deterministic physics loops, render state interpolation, and GJK/EPA continuous collision detection, route to `game-physics-collision-pipeline`.
  * For cache-aligned linear arenas, stack rollbacks, pool free lists, and TLSF two-level allocators, route to `game-memory-allocator-engineering`.
  * For Entity Component System archetype storage, SoA cache alignment, and parallel system DAG scheduling, route to `game-entity-component-system`.
  * For character skeletal hierarchy transforms, quaternion SLERP, dual-quaternion skinning, and FABRIK/Two-Bone IK, route to `game-animation-skeletal-pipeline`.
  * For authoritative multiplayer architecture, client-side input prediction replay, remote entity interpolation, and delta snapshot compression, route to `game-networking-state-sync`.
  * For sharded Discord bot clusters, distributed rate-limit coordination, or low-latency Voice Gateway Opus streaming, route to `discord-bot-engineering`.
  * For dynamic multi-stem vertical soundtrack layering, horizontal music re-sequencing, or deep AI text-to-audio conditioning, route to `ai-procedural-audio-generation`.
  * For anti-cheat state validation, anti-teleport bounds, and memory injection defense, route to `game-security-anti-tamper`.
  * For AEAD authenticated encryption schemes, constant-time side-channel defenses, and hardware-backed key attestation, route to `cryptographic-security-engineering`.
  * For end-to-end supply chain provenance, rootless container security, and minimal-privilege CI/CD enforcement, route to `devsecops-supply-chain-security`.
  * Route deep external inquiries into unfamiliar APIs to `deep-research-synthesizer`.
  * Route exact mathematical formulas, DSP biquad filter calculations, and log analytics to `sandbox-code-interpreter`.
  * Automatically escalate the architecture and plan drafting phase to a **`pro` (Gemini 4 Argon)** subagent via `invoke_subagent`.
  * Once the plan artifact is created and approved, route all execution back to **Flash** for quota-efficient task completion.

---

## Dynamic Difficulty-Triggered Escalation (`adaptive_model_router.py`)

When an agent encounters difficulty getting something to work (e.g. failing unit tests, compilation errors, repeated crash loops), it must **never thrash in low-reasoning trial-and-error loops**.

Invoke the Adaptive Router to dynamically calibrate model and reasoning depth:
```bash
python3 config/skills/adaptive-reasoning/scripts/adaptive_model_router.py route --error "<error snippet>" --attempts <N>
```

### Escalation Hierarchy:
1. **Attempt 0 (Normal Execution):**
   - **Model:** `Flash` / `Turbo`
   - **Reasoning:** `Low` / instant streaming
   - **Strategy:** Surgical pinpoint edits (`replace_file_content`).
2. **Attempt 1 (Difficulty Encountered):**
   - **Model:** `Flash`
   - **Reasoning:** `Medium` / Systematic root-cause diagnosis (`systematic-debugging`).
   - **Strategy:** Read full error stack trace, inspect AST definitions (`local-ast-compiler-engine`), isolate root cause.
3. **Attempt 2+ or Fatal Memory/Crash (Deep Escalation):**
   - **Model:** `pro` (Gemini 4 Argon / Claude Sonnet/Opus) via `invoke_subagent(Model="pro")`
   - **Reasoning:** `High` / Deliberative Tree-of-Thought (`deliberative-reasoning-tree`).
   - **Strategy:** Formulate 3 distinct hypothesis branches, red-team each path, execute provably sound architecture.
4. **Task Verified Passing (`pass`):**
   - Immediate automatic de-escalation back to **`Flash` / Low Reasoning**, restoring 100% quota efficiency.


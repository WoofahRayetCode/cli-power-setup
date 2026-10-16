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
* **Triggers:** Single-line fixes, simple typo corrections, direct shell commands, asking for file locations, formatting, quick status checks, semantic skill matching (`dynamic-skill-router`), or skill health audits/sync (`skills-audit-update`).
* **Reasoning Strategy:**
  * Zero extended deliberation.
  * When uncertain which skill to activate among 100+ choices, run `skill_router.py "<prompt>"` in <20ms to pinpoint the exact 2-3 expert skills.
  * Apply immediate pinpoint diffs via `replace_file_content` or execute terminal commands directly.
  * Run with standard/low thinking latency (keeps streaming instant and saves quota).

### Tier 2: Standard Engineering & Implementation
* **Triggers:** Implementing a specific function, refactoring a single module, writing unit tests, fixing a verified bug, session milestone checkpointing (`session-episodic-memory`), video production scripts, vertical shorts generation, Android device automation, Jetpack Compose UI screens, Android architecture/Room flows, Android testing/release hardening, shader translation/validation, PBR texture channel packing, or skill lifecycle maintenance.
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
  * Follow Test-Driven Development (`test-driven-development`) or targeted debugging (`systematic-debugging`).
  * Sanitize tool outputs using `log-output-sanitizer`.
  * Rely on compiler/linter feedback (e.g. `cargo check`, `ruff`, `clang-tidy`, `pytest`, `spirv-val`).
  * Execute directly on Gemini 3.8 Flash using surgical diffs.

### Tier 3: Deep Architectural & Multi-System Design
* **Triggers:** Designing new mods, multi-file refactoring, kernel modules (`omen-acpi`), reverse engineering unfamiliar binaries, visual layout diagnostics, console emulator architecture, game AI reinforcement learning agents, Android NDK C++ native engines/JNI bridges, low-level Android battery/jank profiling, modern rendering engine architectures (Vulkan/DX12), frame graph design, graphics optimization/culling, or cinematic post-processing pipelines.
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
  * Route deep external inquiries into unfamiliar APIs to `deep-research-synthesizer`.
  * Route exact mathematical formulas, DSP biquad filter calculations, and log analytics to `sandbox-code-interpreter`.
  * Automatically escalate the architecture and plan drafting phase to a **`pro` (Gemini 4 Argon)** subagent via `invoke_subagent`.
  * Once the plan artifact is created and approved, route all execution back to **Flash** for quota-efficient task completion.

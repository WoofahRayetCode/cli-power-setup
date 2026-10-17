# CLI Power Setup (`cli-power-setup`)

A production-grade, quota-optimized engineering, 3D modeling, and game engine porting suite for **Google Antigravity (`agy` — Gemini 4 Argon + Gemini 3.8 Flash Swarm)** and **Cursor IDE** (featuring dedicated multi-model behavioral adaptation for **Gemini 4 Argon/Flash**, **xAI Grok**, **OpenAI GPT/o1/o3**, and **DeepSeek**), backed by **32-thread CPU + NVIDIA RTX 5060 CUDA/OptiX + 30 GB `/dev/shm` RAM-disk hardware offloading**.

This repository organizes **302 autonomous agent skills**, 302 modular Cursor rules (`.cursor/rules/*.mdc`), global engineering discipline rules, a clickable floating voice dictation pill (`agy-mic-button`), a zero-quota CPU/GPU math & physics solver (`game-math-solver`), an auto-optimizing skill ecosystem engine (`skill-optimize`), a clamshell 3D thermal governor (`laptop-perf`), and a live multi-row telemetry statusline (`agy-quota-statusline`).

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
Select target environment:
  1) Full Setup (Antigravity & Cursor) [Recommended]
  2) Antigravity only (~/.gemini)
  3) Cursor only (~/.cursor, ~/.cursorrules)
  4) Exit
```

Or pass flags non-interactively in automated scripts:
```bash
./install.sh --all     # Install for Google Antigravity and Cursor IDE
./install.sh --agy     # Install for Google Antigravity only
./install.sh --cursor  # Install for Cursor IDE only
```

### What the Installer Does:
1. **Safety Backup:** Automatically archives existing configurations to `~/.cli_power_setup_backups/`.
2. **Environment Sync:** Deploys all 302 skills to `~/.gemini/config/skills/` and converts them into Cursor `.mdc` rules in `~/.cursor/rules/`.
3. **Global Discipline & Voice Command Routing:** Installs engineering safeguards, Quota Governance, the **Output Token Economy**, Zero-Quota Local CPU/GPU Math Offload rules, and Natural-Language Spoken Command Routing (*"Set a goal..."*, *"Make a plan..."*, *"Use boost..."*) to `~/.gemini/config/GEMINI.md` and `~/.cursorrules`.
4. **Live Multi-Row Telemetry Statusline (`agy-quota-statusline`):** Tracks real-time 5h/weekly quota, 250k compaction gate countdown (`🧹`), active skills in real time (`🛠️ Skills [Live]`), CPU/GPU temperatures & fan RPM (`🌡️`), lid-closed lock state (`🔒Lid-Safe`), RTX 5060 VRAM & `/dev/shm` RAM-disk usage (`🚀`), and active background workloads (`⚙️ 🎨Blender+🔨Build+🎮OGSR/Wine`).
5. **Floating Voice Dictation Pill (`agy-mic-button`):** Launches a draggable, pinnable (`📌`/`📍`) floating `[🎙️ Talk | ⏎ Send | ⚡Auto | 📌Pin]` overlay that triggers `/voice` (`F5`) without keyboard shortcuts and auto-closes when `agy` exits.
6. **Launchers & Self-Optimizing Ecosystem Tools:** Installs `agy-yolo`, `agy-turbo`, `game-math-solver`, `skill-evolve`, `skill-optimize`, `laptop-perf`, `repo-auto-sync`, and `skills-audit-update` into `~/.local/bin/`.

---

## 📂 Repository Structure

```text
cli-power-setup/
├── install.sh                  # Interactive Linux installer with backup & menu
├── install.ps1                 # Native Windows 10/11 PowerShell installer
├── README.md                   # Comprehensive documentation & skill reference
├── .cursorrules                # Root-level unified Cursor AI rules & skill index
├── .cursor/
│   └── rules/                  # 302 modular Cursor rules (.mdc) with semantic metadata
├── bin/
│   ├── agy-quota-statusline    # Live multi-row quota, skills, thermal, VRAM & git statusline
│   ├── agy-mic-button          # Floating draggable/pinnable voice dictation pill for agy
│   ├── agy-yolo                # Autonomous hands-free YOLO mode launcher (Argon + Flash)
│   ├── agy-turbo               # High-speed Flash low-effort Turbo mode launcher
│   ├── agy-cheatsheet          # Dynamic repo-aware model, effort & hardware offload recommender
│   ├── game-math-solver        # 32-thread CPU + RTX 5060 CUDA 13.4 math, physics & SymPy solver
│   ├── skill-evolve            # Closed-loop runtime skill scaffolder & Voyager script promoter
│   ├── skill-optimize          # Auto-optimizing skill ecosystem graph harmonizer (300 skills)
│   ├── repo-auto-sync          # Autonomous git pull/checkpoint/push & README fleet manager
│   ├── stalker-playtest-runner # Autonomous hands-free game QA, dialogue & locomotion runner
│   ├── context-watchdog        # Automated background context monitor & pre-compact memory stager
│   ├── game-test-watchdog      # Autonomous anti-stuck, freeze & infinite loop supervisor for game QA
│   ├── game-texture-editor     # Procedural normal generation, RNM blend, seamless tiling & DDS transcode
│   ├── game-dialogue-tool      # S.T.A.L.K.E.R. & RPG conversation UI layout repair, string cross-ref & encoding
│   ├── weather-lighting-tuner  # Weather cycle balance, sun glare suppression & HDR tonemapping
│   ├── mangohud-configurator   # In-game performance HUD configurator (FPS, 1% lows, thermals, power, VRAM)
│   ├── game-window-helper      # Gamescope sandboxing, pointer lock & focus-stealing prevention
│   ├── nav-graph-recorder      # Autonomous waypoint navigation, route smoothing & collision trap logging
│   ├── self-improving-qa       # Closed-loop QA controller, 'Press any key' dismissal, stall watchdog & timers
│   ├── cursor-rules-sync       # Converts all skills to Cursor .mdc rules and deploys .cursorrules
│   ├── token-guard             # Terminal command output line ceiling protector (30-line context guard)
│   ├── slice-reader            # Surgical line-slice reader & AST skeleton extractor
│   ├── android-dev-runner      # Android 2D/3D development doctor, scrcpy mirror & jank analyzer
│   └── skills-audit-update     # Health auditor, permissions fixer & multi-environment synchronizer
└── config/
    ├── GEMINI.md                    # Global engineering discipline, quota governance & voice routing rules
    ├── skill_ecosystem_graph.json   # Auto-optimized capability & synergy graph across all 300 skills
    ├── settings.template.json       # Reference AGY CLI settings configuration
    ├── token_ledger.json            # Pure Antigravity (agy) lifetime token savings ledger (1.28B cached tokens)
    ├── cursor/                      # Cursor reference templates and rules
    └── skills/                      # 302 specialized skills
```

---

## 🎯 Where Skills Perform Best: `agy` CLI vs. Cursor IDE (Division of Labor)

While all 302 skills and CLI utilities are shared across environments, they naturally divide into distinct operational sweet spots:

### 1. Skills That Excel in `agy` CLI (Headless, Voice-Driven & Unattended)
*Best launched via `agy-yolo`, `agy-turbo`, or spoken *"Set a goal..."* via `agy-mic-button`*

* **Autonomous Long-Running Goals & Porting Swarms:** `stalker-ogsr-migration`, `autonomous-goal-governor`, `argon-dynamic-subagent-swarm`. Gemini 4 Argon (`High`) orchestrates architecture while dispatching parallel Gemini 3.8 Flash worker subagents for 85%+ quota savings.
* **Lid-Closed Clamshell 3D Rendering & Baking:** `laptop-performance-profile` (`laptop-perf clamshell-3d`), `rtx-optix-gpu-baker-denoiser`, `ramdisk-tmpfs-build-bake-accelerator`. Blocks systemd lid-suspend while capping CPU boost so headless Blender 5.2+ OptiX GPU renders run safely while you sleep.
* **Zero-Quota Local CPU/GPU Math & Asset Offloading:** `game-3d-linear-algebra-quaternions`, `computational-geometry-mesh-bvh-math`, `physics-ballistics-ode-numerical-math`, `pbr-radiometry-color-dsp-math` (`game-math-solver` on 32-thread AVX-512 CPU + RTX 5060 CUDA 13.4).
* **Game QA & System Watchdogs:** `game-qa-playtest-controller`, `game-test-watchdog`, `stalker-playtest-runner`. Direct access to `/dev/uinput` input injection, headless Wine/Proton processes, and X-Ray crash log window dismissals.

### 2. Skills That Excel in Cursor IDE (Interactive & Visual)
*Best used via Cursor Agent or Composer*

* **Web, UI & Data Visualization:** `creative-web-design-archetypes`, `human-crafted-web-design`, `interactive-data-visualization-web`, `generative_ui`.
* **Side-by-Side Code Review & Triage:** `coderabbit-ai-review`, `canvas-interactive-workspace`.

### Recommended Division of Labor

| Workflow | Recommended Tool | Model & Hardware Routing |
| :--- | :--- | :--- |
| **Overnight engine porting, 3D baking & autonomous QA** | **`agy-yolo`** | **Gemini 4 Argon (High) + Flash Swarm** |
| **Routine edits, repository sync & quick commands** | **`agy-turbo`** | **Gemini 3.8 Flash (Low Effort)** |
| **3D coordinates, ODE physics, ballistics & symbolic proofs** | **`game-math-solver`** | **Local 32-Thread CPU + RTX 5060 CUDA (`0` tokens)** |
| **Interactive UI styling, websites & visual apps** | **Cursor IDE** | **Grok 4.7 / Gemini / o3-mini** |

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
| **`threejs-webgl-engineering`** | 3D/WebGL | Interactive 3D browser viewports, GLTFLoader, OrbitControls, PBR |
| **`ai-3d-mesh-generation`** | 3D/AI | Tripo3D text/image-to-3D pipeline, game asset export (GLB/FBX) |
| **`game-modding`** | Modding | S.T.A.L.K.E.R. EE ZoneForge toolchain, LTX & audio rules |
| **`xray-lua-scripting`** | Modding | S.T.A.L.K.E.R. X-Ray Engine Lua callbacks and memory safety |
| **`stalker2-modding`** | Modding | S.T.A.L.K.E.R. 2 UE5 repak containers & RE-UE4SS hooks |
| **`stalker-ogsr-migration`** | Modding | 32-bit S.T.A.L.K.E.R. mod porting to 64-bit OGSR Engine |
| **`game-runtime-diagnostics`** | Diagnostics | Cross-platform PC & Steam Deck game crash troubleshooting (Proton, DirectX, TDRs) |
| **`audio-dsp-tuning`** | Audio/DSP | Studio headset EQ (AutoEq/Harman) & 6-stage broadcast mic processing (EasyEffects/Equalizer APO) |
| **`android-app-engineering`** | Mobile | Modern Android Kotlin, Jetpack Compose, foreground services, Gradle KTS |
| **`console-homebrew-engineering`** | Homebrew | Switch Atmosphere/Hekate CFW, 32KB FAT32 alignment, NSP/NSZ, Obtainium |
| **`electron-desktop-dev`** | Desktop/Web | Secure Electron desktop apps, IPC context bridges, memory optimization |
| **`linux-hardware-acpi`** | Systems/HW | Linux kernel ACPI modules, `/sys/class/hwmon`, D-Bus fan control daemons |
| **`homelab-docker-devops`** | DevOps | Multi-container Docker Compose, Samba POSIX ACLs, Nextcloud, systemd timers |
| **`linux-systems-engineering`** | Systems | POSIX APIs, epoll/io_uring, systemd units, strace & core triage |
| **`bash-posix-automation`** | Automation | Defensive Bash/POSIX scripts, exit traps, argument parsing, ShellCheck |
| **`linux-desktop-packaging`** | Packaging | Flatpak, AppImage, XDG Base Directory, FreeDesktop integration |
| **`win32-systems-engineering`** | Systems | Win32 API, Registry, SCM Windows services, SEH, manifests |
| **`powershell-windows-automation`** | Automation | Modern PowerShell 7, CIM/WMI, Task Scheduler, P/Invoke |
| **`windows-app-engineering`** | UI/Desktop | WinUI 3, WPF, Windows App SDK, C#/WinRT, Fluent UI, MSIX |
| **`cmake-cross-platform`** | Build/Tools | Modern CMake (3.25+), cross-compilation toolchains, CPack |
| **`avalonia-cross-platform-dev`** | UI/Desktop | Avalonia UI (.NET 8/9), MVVM, Native AOT, cross-platform XAML |
| **`tauri-multiplatform-dev`** | UI/Desktop | Lightweight desktop/mobile apps (Tauri 2.0, Rust backend, web frontend) |
| **`cross-browser-extensions`** | Web/Ext | Manifest V3 multi-browser extensions (Chrome, Firefox, Safari) |
| **`prompt-cache-context-optimizer`** | Frontier | Emulates 1M+ context window & >90% Anthropic prompt cache discount |
| **`subagent-swarm-orchestrator`** | Frontier | Autonomous parallel subagent swarms, worktrees & JSON IPC pipelines |
| **`generative-visual-artifacts`** | Frontier | Interactive HTML5/JS/SVG widgets & live browser preview generation |
| **`canvas-interactive-workspace`** | Frontier | Side-by-side editing canvas, targeted diff staging & surgical rollbacks |
| **`deep-research-synthesizer`** | Frontier | Recursive multi-source web crawling & cited technical research whitepapers |
| **`sandbox-code-interpreter`** | Frontier | Headless Python scientific computing, log analytics & chart plotting |
| **`deliberative-reasoning-tree`** | Frontier | Tree-of-Thought (ToT) 3-path branching, adversarial self-critique & backtracking |
| **`semantic-codebase-indexing`** | Frontier | Instant AST symbol graph indexing, ctags/tree-sitter call hierarchy |
| **`frontier-image-studio`** | Frontier | ChatGPT (DALL-E 3) & Gemini (Imagen 3) style generation & dispatch |
| **`claude-silent-dispatch`** | Claude Native | Eliminates pre-tool narration & play-by-plays, executing silently |
| **`claude-worktree-tmux`** | Claude Native | Background detached sessions (`--bg`, `--tmux`) & worktree isolation |
| **`headless-browser-automation`** | Web/Dynamic | Headless Chromium (Playwright/Puppeteer), JS execution & screenshots |
| **`voice-speech-audio-synthesis`** | Audio/Voice | Speech transcription (Whisper) & offline/cloud voice synthesis (Piper/TTS) |
| **`network-protocol-engineering`** | Systems/Net | Packet triage (`tshark`/`pcap`), Protobuf serialization, Linux TUN/TAP |
| **`database-sql-engineering`** | Database | SQLite WAL tuning, PRAGMAs, query execution plans (`EXPLAIN`), PostgreSQL |
| **`github-actions-cicd`** | DevOps | Multi-OS release matrices (Linux, Windows, macOS), automated publishing |
| **`documentation-site-generator`** | Docs | Zero-config VitePress & MkDocs Material sites with GitHub Pages deploy |
| **`security-vulnerability-audit`** | Security | Secret leakage detection (`gitleaks`), SAST (`semgrep`), binary hardening |
| **`nix-reproducible-environments`** | DevOps | Hermetic dev environments & Nix Flakes (`flake.nix`, `devShells`) |
| **`log-output-sanitizer`** | Context/Quota | Filters noisy compiler/test logs before entering chat context |
| **`smart-context-packer`** | Context/Quota | Compresses multi-file codebases into interface-only AST skeletons |
| **`context-pruning-watchdog`** | Context/Quota | Live context telemetry, auto state staging, and lossless compaction |
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
| **`human-crafted-web-design`** | Frontend/Web | Production tactile dark UI, anti-AI heuristics, Geist typography, responsive Tailwind CSS v4 |
| **`executive-business-communications`** | Business | BLUF executive emails, anti-jargon filter, high-conversion proposals, SOWs, invoice generation |
| **`intelligent-interactive-ui`** | Frontier/UI | Reactive single-file micro-apps, forms & live calculators (Astra Intelligent UI) |
| **`screen-vision-inspector`** | Frontier/Vision | Autonomous screen/window capture & visual layout debugging (Project Astra Vision) |
| **`cuda-gpu-acceleration`** | Hardware/GPU | NVIDIA CUDA 13.4, nvcc, Tensor Cores, PyTorch C++ extensions & OptiX |
| **`vulkan-gpu-compute`** | Hardware/GPU | Cross-vendor Vulkan 1.3/1.4 compute, SPIR-V, multi-GPU (NVIDIA, AMD, Intel) |
| **`hardware-tool-engineering`** | Hardware/Dev | System daemons, hwmon, ACPI/fan controllers & CPU SIMD feature dispatch |
| **`video-production-automation`** | Video/Media | NVENC AV1/HEVC hardware transcoding, batch processing, -14 LUFS loudness mastering |
| **`youtube-shorts-video-automation`** | Video/Shorts | 9:16 vertical re-framing, hook-first pacing, kinetic subtitles, split-screen |
| **`game-ai-agent-play`** | Gaming/AI | Reinforcement learning, Gymnasium, OpenCV visual state parsing & low-latency uinput |
| **`android-device-automation`** | Mobile/Auto | ADB/scrcpy real-time screen capture, touch botting, debloating, cache cleaning |
| **`emulator-development-engineering`** | Emulation | Console emulation architecture, JIT dynamic recompilation, fastmem, Vulkan renderers |
| **`shader-cross-compilation`** | Graphics/Shaders | HLSL/GLSL/SPIR-V/WGSL translation, clip space, std140/std430, `glslangValidator` |
| **`game-texture-material-pipeline`** | Graphics/Assets | BCn/ASTC/KTX2 compression, normal map Y-inversion, ORM channel packing, sRGB discipline |
| **`game-texture-editing`** | Graphics/Textures | Procedural normal generation, RNM blending, seamless tiling, de-lighting, alpha edge dilation, CAS sharpening |
| **`real-time-rendering-pipeline`** | Graphics/Engine | Frame graphs, transient memory aliasing, bindless descriptors, reversed-Z, RenderDoc |
| **`game-graphics-optimization-profiling`** | Graphics/Perf | Bottleneck triage, Hi-Z occlusion culling, GPU MultiDraw, LODs, TAA & FSR/DLSS |
| **`post-processing-visual-fx`** | Graphics/PostFX | ACES/AgX tone mapping, progressive dual-filtering bloom, SSAO/GTAO, CSM shadow cascades |
| **`game-audio-engine-engineering`** | Engine/Audio | Lock-free audio callbacks, 3D HRTF spatialization, bus mixing & dynamic ducking |
| **`ai-procedural-audio-generation`** | Audio/SFX | Procedural DSP synthesis, text-to-SFX models, adaptive game music & loudness normalization |
| **`game-physics-collision-pipeline`** | Engine/Physics | Fixed-timestep accumulator loops, state interpolation, BVH broadphase & GJK/EPA CCD |
| **`game-memory-allocator-engineering`** | Engine/Memory | Linear Arenas, Stack LIFO rollback, Pool free lists, TLSF & 64-byte cache alignment |
| **`game-input-system-abstraction`** | Engine/Input | Scaled radial deadzones, sub-pixel mouse smoothing, controller GUID glyph switching |
| **`game-asset-pack-archive-engineering`** | Engine/VFS | Virtual File System mount hierarchy, high-performance VPAK container format & zlib mmap |
| **`game-entity-component-system`** | Engine/ECS | Archetype & Sparse-Set data layouts, SoA memory alignment & multithreaded system DAG scheduling |
| **`game-animation-skeletal-pipeline`** | Engine/Anim | TRS bone hierarchies, quaternion SLERP/NLERP, dual-quaternion skinning & FABRIK/Two-Bone IK |
| **`game-networking-state-sync`** | Engine/Net | Client-side input prediction, server reconciliation, entity interpolation & delta snapshots |
| **`game-save-state-serialization`** | Engine/Save | Endian-safe GSAV binary containers, versioned schema migrations, CRC32 & atomic file replace |
| **`game-debug-ui-tools`** | Engine/Tools | In-engine Dear ImGui integration, immediate 3D DebugDraw, runtime CVars & frame profiler flame charts |
| **`skills-updater-and-auditor`** | Lifecycle/Health | Automated parity audit, YAML frontmatter check, script permission repair & GitHub sync |
| **`discord-bot-engineering`** | Bot/Discord | API v10 slash commands, interactive UI (Buttons, Modals), Gateway intents & voice audio |
| **`game-security-anti-tamper`** | Security/Game | Memory injection defense, DLL hijacking prevention, save file HMAC integrity seals & anti-teleport |
| **`cryptographic-security-engineering`** | Security/Crypto | Ed25519 signatures, AES-256-GCM AEAD, HKDF key derivation & constant-time compare |
| **`devsecops-supply-chain-security`** | Security/DevOps | Checksec binary compiler hardening (RELRO, Canaries, NX, PIE), SBOM & dependency audits |
| **`android-ndk-jni-engineering`** | Mobile/NDK | C/C++ JNI, zero-copy ByteBuffers, Vulkan/Oboe, tombstone symbolization |
| **`android-compose-ui-ux`** | Mobile/UI | Jetpack Compose, Material 3, edge-to-edge window insets, recomposition optimization |
| **`android-architecture-jetpack`** | Mobile/Arch | Clean Architecture, MVI/StateFlow, Room auto-migrations, Navigation DSL, Hilt |
| **`android-testing-ci-cd-security`** | Mobile/DevOps | Robolectric, Compose UI tests, R8 shrinking, Android Keystore StrongBox |
| **`android-perf-battery-profiling`** | Mobile/Perf | Jank analysis (`dumpsys gfxinfo`), batterystats, Perfetto, memory leak heap dumps |
| **`cross-platform-game-compatibility`** | Gaming/Compat | 4GB LAA memory patching, legacy DirectX wrappers (DXVK/dgVoodoo2), thread affinity & frame rate caps |
| **`linux-gaming-proton-optimization`** | Gaming/Linux | Steam Proton/Wine prefix repair, GE-Proton cutscene codecs, dxvk.conf tuning, Gamescope & GameMode |
| **`game-patching-binary-repair`** | Gaming/Binary | PE import analysis, crash offset disassembly, missing DLL stubs & surgical byte-level patching |
| **`app-security-threat-modeling`** | Security/Arch | STRIDE threat modeling, OWASP Top 10 mitigation, path traversal defense, memory zeroing |
| **`api-network-security-hardening`** | Security/Network | TLS 1.3 ciphers, SPKI certificate pinning, token bucket rate limiting, replay defense & CSP |
| **`client-memory-integrity-anticheat`** | Security/Client | XOR value obfuscation, Win32/POSIX anti-debugging, hardware breakpoint traps & state hash |
| **`proton-game-dev-linux`** | Gaming/Proton | Target Valve Proton, case-sensitive asset path normalization, open cutscene codecs & headless CI |
| **`steamdeck-proton-hardware-tuning`** | Gaming/Handheld | Steam Deck 15W APU TDP budget, 40Hz frame pacing, 1280x800 resolution & 28px font scaling |
| **`wine-proton-native-interop`** | Gaming/Interop | Win32-to-Linux named pipe mapping, shared memory shims, Wine DLL call thunking & relay traces |
| **`gamemaker-gml-engineering`** | Gaming/GML | Modern GameMaker (2024+), constructors/structs, FSMs, volatile surfaces, delta timing & batching |
| **`game-trainer-engineering`** | Gaming/Trainer | Cross-platform memory scanning, pointer chain resolvers, AOB scans & mid-function detour hooks |
| **`game-localization-i18n`** | Gaming/i18n | ICU message formatting, pluralization rules, RTL layout mirroring & CJK/Cyrillic font fallbacks |
| **`game-dialogue-ui-localization`** | Gaming/Dialogue | Multi-language conversation UI repair (FIGS, CJK fullwidth, Slavic CP1251/CP1250, BiDi RTL, Turkish), talk.xml overrun & mojibake |
| **`headless-game-ci-automation`** | DevOps/GameCI | Headless engine CLI builds (Godot/Unity/UE5), automated test runners (GUT) & matrix packaging |
| **`godot-shader-vfx`** | Godot/Shaders | Godot 4 screen-reading spatial/canvas shaders, vertex wind displacement & GPU compute particles |
| **`coderabbit-ai-review`** | Review/PR | CodeRabbit-grade PR reviews, architectural Mermaid sequence diagrams, defect triage & GitHub suggestion diffs |
| **`console-game-decompilation`** | Console/Decomp | PS1, PS2, PS3, Xbox, Xbox 360 matching decompilations, splat binary splitting & objdiff |
| **`game-screen-telemetry-monitor`** | Gaming/Vision | Real-time in-game screen monitoring, visual anomaly detection (magenta textures, freezes) & crash OCR |
| **`autonomous-goal-governor`** | Goal/Quota | Machine-verifiable contract formulation, 3-strike circuit breaker & phased `/compact` milestones for `/goal` |
| **`furry-fursona-art-design`** | Creative/Art | Fursona character design, multi-view turnaround refsheets, digitigrade anatomy & palette swatches |
| **`android-rom-os-engineering`** | Mobile/ROM | AOSP & LineageOS device trees, vendor blob extraction, dynamic super partitions & SELinux sepolicy |
| **`game-qa-playtest-controller`** | Gaming/QA | Autonomous multi-axis locomotion (orbit, sweep, wander, stress transitions, action cycles) via uinput |
| **`computer-vision-deep-learning`** | Vision/AI | Neural detection (YOLOv8/v11), instance segmentation (SAM 2), ONNX/CUDA & ByteTrack |
| **`industrial-machine-vision-inspection`** | Vision/Metrology | Camera calibration, GD&T sub-pixel dimensioning, Otsu/Sauvola & template matching |
| **`visual-document-ocr-intelligence`** | Vision/DocAI | Multi-engine OCR (Tesseract/Paddle/Surya), deskewing, Sauvola & table extraction |
| **`agentic-visual-perception`** | Vision/Agent | SAHI 4K/8K tiling, natural language visual grounding coordinates & SSIM diffing |
| **`local-model-coprocessor`** | Hardware/LLM | Offloads docstrings, commit msgs & boilerplate to local Ollama/llama.cpp (0 cloud tokens) |
| **`local-vector-rag-engine`** | Hardware/RAG | Local vector embeddings & dense search, retrieving top-k snippets instead of 50k+ context stuffing |
| **`local-ast-compiler-engine`** | Hardware/AST | Multithreaded AST parsing (`nproc`), symbol extraction & local syntax check before LLM calls |
| **`game-exploratory-fuzzing`** | QA/Self-Improve | Evolutionary action mutation, novelty-guided state exploration & crash delta bisection |
| **`self-healing-test-automation`** | QA/Self-Improve | Resilient locator auto-repair, multi-vector semantic scoring & test auto-patching |
| **`coverage-guided-mutation-testing`** | QA/Self-Improve | AST fault injection (conditionals/arithmetic/booleans), mutant score & test synthesis |
| **`laptop-performance-profile`** | Hardware/Perf | OMEN Space integration, ACPI/WMI sysfs, whisper-quiet night runs & boost execution |
| **`humanities-lore-research`** | Lore/Research | Cross-disciplinary history, ancient mythology, folklore, entity dossiers & relationship graphs |
| **`creative-web-design-archetypes`** | Web/Archetypes | Neo-Brutalism, Parchment, Cyberpunk HUD, Academic Journal, Swiss Modernism & Glassmorphism |
| **`static-site-architecture`** | Web/Jamstack | Jamstack & SSG architecture (Astro, VitePress, Starlight, Content Collections, GitHub Pages CI/CD) |
| **`interactive-data-visualization-web`** | Web/Vis | Zero-build D3.js force-directed networks, Vis.js timelines & dynamic entity stat matrices |
| **`task-velocity-governor`** | Governance/Speed | Task completion velocity, 5-step targeted rule, anti-thrashing loops & diminishing returns bounds |
| **`first-principles-reasoning`** | Reasoning/Core | First-principles decomposition, Chain-of-Verification (CoVe), red-teaming & Ockham's razor ranking |
| **`dynamic-skill-router`** | Context/Router | Semantic intent matching, capability indexing, and sub-second skill activation across 217 skills |
| **`session-episodic-memory`** | Context/Memory | Multi-session milestone checkpointing, chronological episode logging (`.agents/episodes/`), ADR tracking |
| **`hierarchical-memory-retrieval`** | Memory/Recall | Multi-tiered query-driven BM25 search across `.agents/memory/`, episodes & git history |
| **`context-window-governor`** | Context/Budget | Turn-by-turn token budgeting (20/35/25/20%), pre-flight size estimation & hard output clamping |
| **`working-memory-checkpointing`** | Context/State | Atomic snapshotting & 1-command rollback of dirty diffs, hypotheses & test states |
| **`high-density-prompting`** | Quota | Compresses verbose prompts into surgical, zero-waste agent directives |
| **`token-economy`** | Quota | Eliminates conversational fluff & echoes; compact status |
| **`project-memory-bank`** | Memory | Persistent `.agents/memory/` context to prevent re-hydration |
| **`game-weather-lighting-fx`** | Gaming/Weather | Weather cycle tuning, HDR tonemapping, sun shafts/god rays & blinding glare suppression |
| **`game-performance-overlay-telemetry`** | Gaming/HUD | In-game telemetry (MangoHud, DXVK HUD), FPS, 1% lows, VRAM/power stats & top-right HUD positioning |
| **`game-weapon-ballistics-mechanics`** | Gaming/Weapons | Weapon LTX configs, full-auto trigger states, underbarrel launchers, blast physics & anti-jamming |
| **`game-qol-gameplay-scripting`** | Gaming/Scripting | Proximity item radar & smart auto-loot, faction-filtered defense systems, sprint anomaly immunity |
| **`linux-game-window-input-capture`** | Gaming/Linux | Pointer grab/confinement, Gamescope sandboxing, borderless windowing & focus-stealing prevention |
| **`game-autonomous-navigation-ai`** | Gaming/AI | Self-improving waypoint navigation, collision trap blacklisting, and reactive combat aimbot steering |
| **`game-self-improving-qa-pipeline`** | QA/Automation | Closed-loop self-improving QA, 'Press any key' dismissal, 88% stall watchdog, regression DB & timers |
| **`game-companion-pet-ai`** | Gaming/Companion | Custom companion pet AI, god mode status, dynamic torch light in dark, homing mouth missiles & meows |
| **`game-dynamic-stress-orchestrator`** | QA/Stress | Safe radial wave spawning (anti-mesh-drop), multi-faction air/mutant clashes & VRAM saturation profiling |
| **`game-memory-scanner`** | Gaming/Trainer | Virtual memory inspection, iterative candidate filtering (exact/changed), AOB scans & memory freeze |
| **`game-dll-proxy-generator`** | Gaming/Trainer | Automated proxy DLL generator (dinput8, dxgi, version) with export forwarding, MinHook & Proton configs |
| **`agy-codebase-init`** | Workflow/Parity | Claude Code `/init` parity: automatic codebase architecture intake, stack detection & GEMINI.md/CLAUDE.md scaffolding |
| **`agy-cli-doctor`** | DevOps/Parity | Claude Code `doctor` parity: SQLite database integrity check, permissions whitelist audit, model endpoint health |
| **`agy-context-telemetry`** | Token/Parity | Claude Code `/context` & `/cost` parity: step-by-step cache telemetry, model split, token savings & cost estimation |
| **`argon-thinking-governor`** | Token/Cognitive | Gemini 4 Argon internal CoT thinking token clamp, zero-monologue tool execution & hybrid Flash dispatch |
| **`blender-high-to-low-baking`** | 3D/Baking | Headless multi-map baking (normal, AO, curvature/cavity, ID) from multi-million sculpts to low-poly via bpy |
| **`game-engine-3d-budget-profiler`** | 3D/Budget | Game engine 3D performance budget validation, automated LOD0–LOD3 decimation & UCX collision hulls |
| **`blender-pbr-texture-packager`** | 3D/PBR | PBR ORM channel packing (Occlusion, Roughness, Metallic), texel density enforcement & DirectX/OpenGL normal inversion |
| **`character-creature-anatomy-modeling`** | 3D/Anatomy | Biped and quadruped skeletal topology, concentric deformation loops, digitigrade mechanics & retopo cages |
| **`rigging-weight-painting-pipeline`** | 3D/Rigging | Game armature bone budgets, automated weight normalization, 4-influence clamping & IK/FK solvers |
| **`blender-headless-token-shield`** | 3D/Token | Prohibits raw vertex/mesh dumps in chat; enforces headless Python automation with 3-line CLI telemetry |
| **`claude-opus-conciseness-enforcer`** | Token/Opus | Enforces <=200 token outputs, strict BLUF, zero code repetition in chat, saving up to 75% Opus output tokens |
| **`fable-virtual-context-manager`** | Context/Fable | Virtualizes 1M-token context by paging 30k subsystem slices from a disk knowledge graph into working memory |
| **`argon-effort-auto-calibrator`** | Token/Argon | Dynamically scales Argon thinking effort (--effort low/med/high) turn-by-turn to slash reasoning tokens by 85% |
| **`universal-token-containment-protocol`** | Token/Global | Enforces zero chat code duplication, artifact offloading, and strict tool caps across all 217 skills |
| **`model-optimal-state-serializer`** | Token/State | Tokenizer-native state serialization (XML-KV for Claude BPE, Pipe-TSV for Gemini SentencePiece, symbol URIs) |
| **`multi-model-cache-harmonizer`** | Cache/Multi | Static prefix anchoring and boundary alignment across Claude, Gemini, OpenAI, and Grok for 90-95% cache discounts |
| **`git-diff-token-compressor`** | Git/Token | Zero-context hunks (-U0) and coordinate patches (<file>#L<num>:+added|-removed) slashing diff tokens by 70-85% |
| **`polyglot-ast-interface-pruner`** | AST/Context | Strips function bodies, comments, and private variables across C++, C#, Rust, Python, Lua for 85-90% context reduction |
| **`local-preflight-syntax-gate`** | QA/Preflight | Zero-token host CPU syntax verification (luac, ruff, cargo, clang) saving 15k-40k reasoning tokens per typo |
| **`disassembly-token-redactor`** | RE/Token | Strips raw hex opcodes and NOP sleds from objdump/readelf/rizin, condensing disasm into symbolic CFG basic blocks |
| **`game-config-delta-extractor`** | Game/Config | Inheritance delta extractor for S.T.A.L.K.E.R. LTX, Godot TSCN, and YAML, slashing config context by 80-85% |
| **`network-packet-stream-condenser`** | Net/Token | Compresses verbose tshark/tcpdump packet dissections into high-density 1-line TSV telemetry tuples |
| **`sql-schema-query-condenser`** | DB/Token | Serializes verbose DDL and EXPLAIN query plan trees into compact type-bracket notation and operator pipelines |
| **`cross-model-switch-pruner`** | Switch/Token | Pre-switch state compaction and zero-history handoffs to eliminate 80k-150k token re-reads when switching to Fable |
| **`compiler-error-cascade-isolator`** | Build/Compiler | Isolates #1 root-cause C++ compiler error and strips 500+ lines of cascaded template noise (saving 10k-30k tokens) |
| **`xray-crash-symbol-resolver`** | Crash/Symbol | Translates Wine/Proton crash offsets to exact source lines via host addr2line/rizin in 15ms (saving 25k-40k tokens) |
| **`xray-macro-boilerplate-condenser`** | AST/Macros | Condenses legacy GSC macros (IC, Luabind, memory wrappers) into semantic signatures for 70-80% smaller C++ context |
| **`stalker-spawn-entity-indexer`** | Game/Spawn | Indexes 40k+ line all.spawn into queryable JSON maps, returning exact 15-line entity slices (99.5% token reduction) |
| **`fable-atomic-diff-sequencer`** | Fable/Sequencer | Decomposes Fable 128k output refactors into atomic, dependency-ordered chunk executions to prevent tool timeouts |
| **`session-experience-harvester`** | Memory/Ledger | Mines past long-running session logs, tracking multi-billion token savings and distilling solved CTDs into memory |
| **`shell-output-token-guard`** | CLI/Safety | Enforces terminal line ceilings via `token-guard`, preventing 10k-50k stdout context floods |
| **`selective-context-ingestor`** | Ingest/Slicing | Surgical line-slice and AST-first reader via `slice-reader`, cutting file reading context by 90-95% |

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

#### 18. `game-modding`
* **In Simple Terms:** Safety guardrails for modding games like S.T.A.L.K.E.R. Enhanced Edition, making sure configurations and textures don't break the game.
* **When It Kicks In:** Modding weapons, items, UI menus, textures, or game configurations.
* **How It Works:** Protects original game files by keeping them read-only, checks game configuration text files (LTX) for missing sections, ensures textures use the right compression (DXT1/DXT5), and preserves special audio headers.
* **Why It Saves Quota:** Stops the game engine from crashing on startup due to a single missing bracket or corrupted audio file.

#### 19. `xray-lua-scripting`
* **In Simple Terms:** Specialized scripting rules for the S.T.A.L.K.E.R. X-Ray game engine that prevent savegame corruption and game freezes.
* **When It Kicks In:** Writing quest scripts, inventory logic, NPC behaviors, or custom game mechanics in S.T.A.L.K.E.R.
* **How It Works:** Enforces strict nil-checks (verifying an enemy or item still exists before talking to it), prevents memory leaks in Lua, and ensures game saves stay clean.
* **Why It Saves Quota:** Avoids silent script freezes and prevents corrupted save files that ruin hours of playthroughs.

#### 20. `stalker2-modding`
* **In Simple Terms:** Modding toolkit for S.T.A.L.K.E.R. 2 Heart of Chornobyl (Unreal Engine 5).
* **When It Kicks In:** Creating mods for S.T.A.L.K.E.R. 2, packing game archives, or adding custom C++ and Lua gameplay hooks.
* **How It Works:** Automates packaging UE5 game containers (`.pak`, `.ucas`, `.utoc`) with proper compression using `repak` and sets up RE-UE4SS scripting hooks.
* **Why It Saves Quota:** Eliminates failed container packing and wrong compression settings that cause the game to ignore mods.

#### 21. `stalker-ogsr-migration`
* **In Simple Terms:** The expert specialist for porting older S.T.A.L.K.E.R. mods (like S.T.A.L.K.E.R. Complete 2009) to the modern, 64-bit OGSR Engine.
* **When It Kicks In:** Upgrading 32-bit Shadow of Chernobyl mods to the modern 64-bit OGSR engine.
* **How It Works:** Removes incompatible 32-bit DLL files, removes old DirectX 9 shaders that crash the modern DX11 renderer, updates script callbacks to LuaJIT, and converts level spawn files using ACDC.
* **Why It Saves Quota:** Directly solves the known causes of fatal startup crashes (`FATAL ERROR: Expression: !failed()`) without endless guesswork.

#### 22. `game-runtime-diagnostics`
* **In Simple Terms:** A master doctor for PC games that investigates why games crash, stutter, or refuse to launch on Windows and Linux (Steam Deck / Proton), and fixes them.
* **When It Kicks In:** Whenever a game crashes to desktop, freezes with a DirectX error, suffers from shader compilation stutter, or fails to launch in Steam Proton.
* **How It Works:** On Linux, parses Proton log streams (`PROTON_LOG=1`), configures DXVK async shader compilation, repairs broken Wine prefixes with Winetricks, and sets up DLL overrides. On Windows, reads Event Viewer crash logs (Event ID 1000), fixes GPU driver timeouts (TDRs), and repairs missing DirectX/Visual C++ runtimes.
* **Why It Saves Quota:** Pinpoints the exact missing dependency, broken codec, or corrupted shader cache instantly instead of blindly reinstalling 100GB games.

---

### 🎧 Audio Engineering & DSP

#### 23. `audio-dsp-tuning`
* **In Simple Terms:** Calibrates headphones to sound balanced and clear, and transforms any microphone into a studio-grade broadcast voice without background noise.
* **When It Kicks In:** Tuning headset audio, fixing muddy bass or piercing treble, eliminating microphone background noise (fans, keyboard clicks), or setting up stream audio.
* **How It Works:** Applies acoustic target curves (Harman Target via AutoEq) to headphones and sets up a professional 6-stage microphone processing chain (high-pass filter, AI noise suppression, surgical EQ, vocal compressor, de-esser, and brickwall limiter). Outputs ready-to-use profiles for EasyEffects (Linux) and Equalizer APO / Peace (Windows).
* **Why It Saves Quota:** Eliminates hours of manual trial-and-error audio tweaking and prevents incomprehensible voice audio during multiplayer gaming or calls.

---

### 📱 Mobile, Emulation & Console Homebrew

#### 24. `android-app-engineering`
* **In Simple Terms:** Expert guide for writing fast, modern Android applications in Kotlin, managing Gradle builds, and avoiding background battery/network service kills.
* **When It Kicks In:** Developing Android apps, configuring Kotlin Gradle scripts (`build.gradle.kts`), network tethering services, or APK release signing.
* **How It Works:** Enforces modern Jetpack Compose architecture, sets up reliable foreground services that survive Android's Doze battery saver, configures ProGuard/R8 rules so serialization doesn't break, and manages cryptographic keystores.
* **Why It Saves Quota:** Eliminates trial-and-error Gradle build failures and background service termination debugging.

#### 25. `console-homebrew-engineering`
* **In Simple Terms:** A safety-first guide for console softmodding, custom firmware (CFW) setups, payload injectors, and game package management.
* **When It Kicks In:** Setting up Nintendo Switch CFW (Atmosphere/Hekate), SD card formatting, converting/compressing game packages (NSP/NSZ), or managing Obtainium emulator feeds.
* **How It Works:** Enforces strict FAT32 32KB cluster alignment (preventing fatal Switch archive-bit corruption), configures Hekate bootloaders and raw emuMMC partitions, and handles block-compressed zstd NSZ files.
* **Why It Saves Quota:** Prevents bricked consoles, corrupt SD cards, and broken bootloader configuration loops.

---

### 🖥️ Desktop, Kernel & Infrastructure

#### 26. `electron-desktop-dev`
* **In Simple Terms:** Best practices for building secure, lightweight desktop applications with Electron without massive memory bloat.
* **When It Kicks In:** Developing Electron apps, custom Chromium browsers, desktop messaging clients, or system tray utilities.
* **How It Works:** Enforces strict security boundaries (context isolation, disabled node integration in renderers), types IPC communication via `contextBridge`, handles multi-window and tray lifecycles, and packages multi-platform distributions with electron-builder.
* **Why It Saves Quota:** Catches Electron security vulnerabilities and memory leaks before deployment.

#### 27. `linux-hardware-acpi`
* **In Simple Terms:** Guides the development of Linux kernel ACPI modules, hardware fan curves, and system telemetry background services.
* **When It Kicks In:** Developing kernel modules (like `omen-acpi`), controlling laptop fan curves, reading thermal sensors via `/sys/class/hwmon/`, or writing D-Bus hardware daemons.
* **How It Works:** Decompiles ACPI DSDT/SSDT tables (`iasl`), binds Linux WMI drivers to hardware sensors, and implements hysteresis smoothing so fans don't rapidly rev up and down.
* **Why It Saves Quota:** Prevents kernel panics, memory boundary violations in C kernel space, and runaway fan loops.

#### 28. `homelab-docker-devops`
* **In Simple Terms:** Standardizes setting up home servers, Docker containers, Samba network storage, and automated backups on Linux / Raspberry Pi.
* **When It Kicks In:** Managing Raspberry Pi NAS setups, multi-container Docker Compose stacks, network shared folders (Samba), or systemd backup timers.
* **How It Works:** Deploys clean multi-service `docker-compose.yml` configurations with isolated bridge networks, sets proper Samba POSIX group permissions (`0664`/`0775`) to avoid "Permission Denied" errors, and automates daily maintenance with systemd timers.
* **Why It Saves Quota:** Eliminates permission-denied errors and container crash loops through verified configuration templates.

---

### 🐧 Linux Systems & Packaging

#### 29. `linux-systems-engineering`
* **In Simple Terms:** Deep low-level Linux systems programming for building background services, handling high-speed data, and fixing system crashes.
* **When It Kicks In:** Writing Linux services in C/C++/Rust, dealing with file descriptors, sockets, `epoll`/`io_uring`, writing systemd daemons, or analyzing core dumps.
* **How It Works:** Implements non-blocking I/O multiplexing, structures hardened systemd units with watchdog timers and security sandboxing (`ProtectSystem=strict`), and diagnoses crashes with `strace` and `gdb`.
* **Why It Saves Quota:** Prevents silent process hangs, memory leaks, and mysterious daemon crashes with systematic POSIX diagnostics.

#### 30. `bash-posix-automation`
* **In Simple Terms:** A safety shield for writing bulletproof shell scripts that never break, corrupt files, or fail silently.
* **When It Kicks In:** Writing installation scripts, build hooks, or setup tools across Linux and macOS.
* **How It Works:** Enforces strict error trapping (`set -euo pipefail`), signal cleanup (`trap cleanup EXIT INT TERM`), portable argument parsing with `getopts`, atomic temporary files (`mktemp`), and ShellCheck validation.
* **Why It Saves Quota:** Stops script errors before they start and prevents runaway scripts from altering unwanted files.

#### 31. `linux-desktop-packaging`
* **In Simple Terms:** Packages Linux desktop apps so they appear cleanly in app launchers, look great, and run safely on any distribution.
* **When It Kicks In:** Creating `.desktop` launchers, AppStream metadata, sandboxed Flatpak packages, or portable AppImages.
* **How It Works:** Enforces FreeDesktop and XDG standards, builds sandboxed Flatpak manifests with fine-grained portal permissions (Wayland, audio, network), and bundles self-contained AppImages with `linuxdeploy`.
* **Why It Saves Quota:** Eliminates distribution dependency hell and ensures apps launch reliably everywhere on the first try.

---

### 🪟 Windows Systems & Applications

#### 32. `win32-systems-engineering`
* **In Simple Terms:** Low-level Windows native programming for building Windows background services, managing the Windows Registry, and handling crashes.
* **When It Kicks In:** Writing native Windows C++/C# applications, editing the Windows Registry (`.reg`), writing Windows Services (SCM), or reading crash dumps.
* **How It Works:** Handles Win32 kernel objects, synchronizes threads with Mutexes and Events, embeds modern Per-Monitor V2 DPI manifests, and captures instant crash minidumps via Structured Exception Handling (SEH).
* **Why It Saves Quota:** Eliminates blurry Windows scaling quirks, permission errors, and untraceable crash bugs.

#### 33. `powershell-windows-automation`
* **In Simple Terms:** Professional-grade PowerShell scripting for automating Windows tasks, managing services, and configuring environments.
* **When It Kicks In:** Automating Windows administration, running setup scripts on Windows, querying hardware via CIM/WMI, or scheduling tasks.
* **How It Works:** Uses advanced cmdlet design (`[CmdletBinding()]`), pipeline streaming, strict error termination (`$ErrorActionPreference = 'Stop'`), and inline Win32 API calls via `Add-Type` (P/Invoke).
* **Why It Saves Quota:** Prevents broken Windows automation runs and maintains identical CLI argument parity (`--help`, `--dry-run`) with Linux Bash scripts.

#### 34. `windows-app-engineering`
* **In Simple Terms:** Best practices for building beautiful, modern Windows desktop apps using Microsoft's latest UI frameworks (WinUI 3 and WPF).
* **When It Kicks In:** Creating Windows desktop tools, hardware control panels, or utilities with Fluent Design.
* **How It Works:** Implements Windows 11 Mica material and custom draggable titlebars, ensures single-instance execution, integrates with the system tray, and packages clean MSIX installers.
* **Why It Saves Quota:** Prevents common XAML layout bugs, memory leaks, and confusing packaging errors.

---

### 🌐 Multiplatform & Cross-Platform Development

#### 35. `cmake-cross-platform`
* **In Simple Terms:** A universal build system guide for compiling C/C++ projects across Linux, Windows, and macOS without messy build scripts.
* **When It Kicks In:** Managing CMake projects (3.25+), cross-compiling from Linux to Windows (via MinGW-w64 or Clang), or generating installers.
* **How It Works:** Uses clean target-based CMake (`target_link_libraries`), declarative cross-compilation toolchain files, and automates multi-platform installers using CPack (NSIS for Windows, DEB/RPM for Linux).
* **Why It Saves Quota:** Solves compiler and linker errors on the first build and avoids brittle, platform-specific compiler flags.

#### 36. `avalonia-cross-platform-dev`
* **In Simple Terms:** Build high-performance desktop applications that run natively on Windows, Linux, and macOS using a single C# / XAML codebase.
* **When It Kicks In:** Developing multiplatform desktop tools, game backup managers (like `PS-Multi-Tools`), or utilities with .NET 8/9.
* **How It Works:** Employs the MVVM pattern with compiled bindings (`x:DataType`), cross-platform file pickers (`StorageProvider`), system tray integration, and Native Ahead-Of-Time (AOT) compilation for instant startup.
* **Why It Saves Quota:** Eliminates having to rewrite UI code for different operating systems and avoids reflection runtime bugs.

#### 37. `tauri-multiplatform-dev`
* **In Simple Terms:** Builds ultra-lightweight desktop and mobile apps with a web frontend (HTML/CSS/JS) and a fast Rust backend, using a fraction of the memory of Electron.
* **When It Kicks In:** Creating modern desktop tools, lightweight alternatives to Electron apps, or cross-platform utilities.
* **How It Works:** Uses the operating system's built-in web engine (saving over 100MB of RAM per app), provides secure typed IPC commands between Rust and TypeScript, and compiles to Linux, Windows, macOS, Android, and iOS.
* **Why It Saves Quota:** Prevents Electron memory bloat and ensures safe, typed communication between the UI and system hardware.

#### 38. `cross-browser-extensions`
* **In Simple Terms:** Build browser extensions that work simultaneously across Google Chrome, Mozilla Firefox, Microsoft Edge, and Safari using Manifest V3.
* **When It Kicks In:** Building browser extensions, web feed customizers (like `ClutterlessSocial`), content filters, or social media tools.
* **How It Works:** Unifies browser APIs using `webextension-polyfill`, manages background service workers and event pages, handles secure content script messaging, and packages separate store-ready zips and signed XPI files.
* **Why It Saves Quota:** Eliminates having to maintain duplicate codebases for Chrome and Firefox.

---

### 🚀 Frontier Model & Platform Parity (Gemini, ChatGPT, DeepSeek, Cursor)

#### 39. `prompt-cache-context-optimizer`
* **In Simple Terms:** Emulates Gemini's massive 1M–2M context window in Claude Code and guarantees a 90% discount on your AI token bills.
* **When It Kicks In:** Working with large codebases, multi-file refactors, or running long 15+ turn sessions.
* **How It Works:** Re-orders prompts so static system rules and project indexes sit at the front to guarantee Anthropic prompt cache hits (>1,024 tokens, 5-minute TTL), and compresses huge code repositories into lightweight 2-level AST summaries.
* **Why It Saves Quota:** Slashes input prompt costs by **up to 90%** and prevents expensive repetitive repository reads.

#### 40. `subagent-swarm-orchestrator`
* **In Simple Terms:** Gives Claude Code the ability to launch and coordinate a team of autonomous background AI worker agents running in parallel.
* **When It Kicks In:** Running linting, testing, and documentation generation simultaneously, or exploring competing solutions.
* **How It Works:** Uses detached background tasks in isolated git worktrees (`.worktrees/worker-*`), pipes JSON messages between workers and the parent orchestrator, and aggregates completed results.
* **Why It Saves Quota:** Offloads massive exploration and test-log noise into disposable background sandboxes, keeping your main conversation transcript tiny.

#### 41. `generative-visual-artifacts`
* **In Simple Terms:** Generates interactive web widgets, UI mockups, and charts in Claude Code that instantly open in your local web browser.
* **When It Kicks In:** Reviewing UI wireframes, visualizing hardware telemetry, fan curves, or complex math formulas.
* **How It Works:** Builds zero-dependency single-file HTML5/Tailwind/Chart.js/KaTeX artifacts, saves them to temporary previews, and auto-launches them via `xdg-open` or `open`.
* **Why It Saves Quota:** Replaces hundreds of lines of confusing ASCII tables or text descriptions with an instant rendered visual interface.

#### 42. `canvas-interactive-workspace`
* **In Simple Terms:** Brings ChatGPT's Canvas side-by-side editing experience into Claude Code for reviewing and approving exact line diffs.
* **When It Kicks In:** Making delicate code refactors, editing configuration files, or reviewing major modifications.
* **How It Works:** Stages draft modifications in `.canvas/`, renders unified colorized terminal diffs, applies targeted search-and-replace chunks, and logs design rationales.
* **Why It Saves Quota:** Eliminates full-file rewrites and allows reviewing and approving edits in place before touching production files.

#### 43. `deep-research-synthesizer`
* **In Simple Terms:** Brings OpenAI Deep Research and Perplexity Pro investigative capabilities into Claude Code for generating cited technical whitepapers.
* **When It Kicks In:** Researching unfamiliar protocols, complex APIs, kernel subsystems, or open-source libraries.
* **How It Works:** Formulates multi-vector queries, recursively crawls documentation and GitHub issues, rates source credibility, filters SEO spam, and compiles formal cited reports into `.agents/research/`.
* **Why It Saves Quota:** Prevents the user from having to manually guide the AI through 20 separate web search rounds.

#### 44. `sandbox-code-interpreter`
* **In Simple Terms:** An in-chat scientific calculator and data analyst that executes Python in the background to calculate exact numbers, parse data, and plot charts.
* **When It Kicks In:** Calculating audio DSP filter curves, analyzing hardware telemetry logs, verifying math proofs, or parsing CSV/benchmark files.
* **How It Works:** Runs headless Python scripts in an isolated virtual environment with `numpy`, `pandas`, `matplotlib`, and `scipy`, outputting exact numbers and high-res vector charts.
* **Why It Saves Quota:** Eliminates guessing and hallucinated math by calculating exact values programmatically.

#### 45. `deliberative-reasoning-tree`
* **In Simple Terms:** Implements DeepSeek R1 and OpenAI o1-style Tree-of-Thought reasoning, exploring 3 distinct solution paths and attacking its own logic before writing code.
* **When It Kicks In:** High-complexity architectural decisions, concurrency debugging, or performance-critical design.
* **How It Works:** Generates 3 parallel solution paths, runs an adversarial self-critique checking edge cases and memory hazards, explicitly backtracks on flaws, and selects only the proven best path.
* **Why It Saves Quota:** Prevents the AI from pursuing a flawed architectural path that takes hours of trial-and-error to unwind.

#### 46. `semantic-codebase-indexing`
* **In Simple Terms:** Gives Claude Code Cursor and Windsurf-style instant photographic memory of your entire project's classes and functions.
* **When It Kicks In:** Searching for function definitions, callers, or class hierarchies across large multi-file repositories.
* **How It Works:** Maintains a compact Universal Ctags / Tree-sitter symbol index (`.code_index_tags.json`) that Claude queries in 10ms with `jq` without reading whole files into the chat context.
* **Why It Saves Quota:** Replaces multi-file `view_file` calls (which burn 20,000+ tokens) with a 200-token targeted symbol lookup.

#### 47. `frontier-image-studio`
* **In Simple Terms:** Gives Claude Code the ability to generate images in the exact visual styles of ChatGPT (DALL-E 3) and Gemini (Imagen 3), with zero-API local graphics generation.
* **When It Kicks In:** Creating concept art, UI badges, logos, game textures, or generating images via external AI image APIs.
* **How It Works:** Applies specialized prompt engineering formulas (Pixar 3D dioramas for ChatGPT, photorealistic Hasselblad camera lenses for Gemini), includes a multi-backend Python runner (`scripts/generate_image.py`), and can render crisp vector SVGs and procedural game textures locally without any API keys.
* **Why It Saves Quota:** Generates images programmatically and previews them in your local browser, eliminating repetitive trial-and-error prompt iterations.

#### 48. `claude-silent-dispatch`
* **In Simple Terms:** Stops Claude Code from "talking out loud" before running commands, jumping straight to the action to save you tokens.
* **When It Kicks In:** Whenever Claude runs terminal commands, searches files, or applies code edits.
* **How It Works:** Eliminates preambles and explanatory play-by-plays (like *"Verifying missing-API claims..."*), immediately executing the required tool call as the first token of the turn and reporting only compact results.
* **Why It Saves Quota:** Saves **500 to 1,500 output tokens (~15,000+ compounding input tokens)** on every multi-step coding task.

#### 49. `claude-worktree-tmux`
* **In Simple Terms:** Lets Claude Code run heavy builds, tests, or long tasks in a separate background window so your main chat stays clean and responsive.
* **When It Kicks In:** Compiling large C++ engines, unpacking game archives, or running long test suites.
* **How It Works:** Uses Claude Code's native `-w, --worktree`, `--tmux`, and `--bg` flags to dispatch long tasks into detached background panes, checking progress via `claude logs` without dumping hundreds of terminal lines into your main chat.
* **Why It Saves Quota:** Isolates noisy terminal output to background sandboxes so it never enters or bloats your active chat memory.

#### 50. `headless-browser-automation`
* **In Simple Terms:** Runs a real hidden web browser that can click buttons, log into websites, run complex JavaScript, and take full-page screenshots.
* **When It Kicks In:** Scraping dynamic modern websites, testing web apps, extracting data from Single Page Applications (SPAs), or capturing web screenshots.
* **How It Works:** Controls headless Chromium via Playwright and Puppeteer, executes client-side JavaScript, waits for network idle, and saves full-resolution screenshots.
* **Why It Saves Quota:** Eliminates guesswork when scraping dynamic websites by letting the AI see and inspect the exact rendered web page.

#### 51. `voice-speech-audio-synthesis`
* **In Simple Terms:** Transcribes spoken audio into text and generates realistic human voices for game characters, voice memos, and videos.
* **When It Kicks In:** Transcribing meeting recordings, generating game NPC dialogue, creating subtitle files (.srt), or synthesizing voiceovers.
* **How It Works:** Runs high-performance local speech-to-text with `faster-whisper`, and generates neural human voices locally using Piper and Kokoro TTS (zero API fees required).
* **Why It Saves Quota:** Generates speech and transcribes audio completely offline on your computer without paying cloud transcription fees.

#### 52. `network-protocol-engineering`
* **In Simple Terms:** Analyzes network traffic, designs custom communication protocols, and sets up virtual network adapters and VPN tunnels.
* **When It Kicks In:** Troubleshooting connection problems, inspecting network packet traces (`.pcap`), building socket servers, or working on network tethering tools like `tetherfusenet`.
* **How It Works:** Uses command-line `tshark` and `tcpdump` to decode network protocols, serializes binary messages with Protobuf/FlatBuffers, and configures Linux TUN/TAP virtual network interfaces.
* **Why It Saves Quota:** Decodes network issues directly from the terminal without needing to install or launch heavy Wireshark graphical software.

#### 53. `database-sql-engineering`
* **In Simple Terms:** Makes databases run lightning-fast, writes clean SQL, and eliminates "database is locked" errors.
* **When It Kicks In:** Working with SQLite in desktop apps or games, designing PostgreSQL schemas for home servers, or tuning slow database queries.
* **How It Works:** Applies production SQLite tuning (WAL mode, PRAGMAs, indexes), analyzes query execution plans (`EXPLAIN QUERY PLAN`), and manages safe database migrations.
* **Why It Saves Quota:** Prevents database corruptions, write bottlenecks, and slow table-scanning queries that crash applications.

#### 54. `github-actions-cicd`
* **In Simple Terms:** Automates building and publishing your software for Windows, Linux, and Mac every time you push an update to GitHub.
* **When It Kicks In:** Setting up automated testing, building release packages (`.AppImage`, `.exe`, `.dmg`), or publishing updates across your 30+ GitHub projects.
* **How It Works:** Creates multi-OS GitHub Actions matrix pipelines with build caching (`ccache`, `cargo-cache`) and automatically uploads packaged binaries to GitHub Releases when a tag is created.
* **Why It Saves Quota:** Replaces hours of tedious manual compiling and uploading with a fully automated, cloud-hosted release pipeline.

#### 55. `documentation-site-generator`
* **In Simple Terms:** Turns simple markdown notes into gorgeous, searchable documentation websites that look like professional open-source projects.
* **When It Kicks In:** Writing project manuals, API references, or documentation sites for your repositories.
* **How It Works:** Scaffolds zero-dependency VitePress or MkDocs Material sites with full-text search, automatic API extraction, and 1-click deployment to GitHub Pages.
* **Why It Saves Quota:** Builds complete documentation websites in under a minute without manual HTML or CSS styling.

#### 56. `security-vulnerability-audit`
* **In Simple Terms:** A security guard that scans your code before you commit it, ensuring you never accidentally push private passwords or API keys to GitHub.
* **When It Kicks In:** Before committing code, publishing repositories, or auditing open-source dependencies.
* **How It Works:** Runs `gitleaks` to catch exposed API keys and secrets, performs static security analysis (`semgrep`), checks dependencies for vulnerabilities, and verifies binary exploit mitigations.
* **Why It Saves Quota:** Prevents devastating security leaks and accidental public disclosure of expensive API tokens.

#### 57. `nix-reproducible-environments`
* **In Simple Terms:** Creates rock-solid, identical developer environments that work the same on any Linux or Mac computer without Docker overhead.
* **When It Kicks In:** Managing projects with complex dependencies (like `omen-space`), configuring `flake.nix`, or avoiding "works on my machine" bugs.
* **How It Works:** Uses Nix Flakes to declare exact compiler versions, libraries, and tools, launching isolated development shells (`nix develop`) with zero system package clutter.
* **Why It Saves Quota:** Eliminates hours of compiler version conflicts, broken packages, and missing dependency debugging.

---

### 💻 Systems, Reverse Engineering & Languages

#### 58. `cachyos-arch-packaging`
* **In Simple Terms:** Builds and packages Linux software, kernel drivers, and background services specifically for Arch Linux and CachyOS.
* **When It Kicks In:** Creating Arch/CachyOS packages (`PKGBUILD`), installing kernel drivers (like `omen-acpi`), or setting up systemd background services.
* **How It Works:** Enforces Arch packaging standards, checks integrity hashes, validates build dependencies in isolated chroots, and verifies systemd service files.
* **Why It Saves Quota:** Prevents broken package builds and keeps your Linux system clean, stable, and conflict-free.

#### 59. `reverse-engineer-anything`
* **In Simple Terms:** A deep inspection engine for understanding closed-source software, compiled games, and applications when no source code is available.
* **When It Kicks In:** Analyzing compiled binaries, Windows/Linux executables, Android packages, or web apps.
* **How It Works:** Deeply integrates with REA MCP to perform static disassembly, decompile code, reconstruct data structures, and keep an evidence ledger.
* **Why It Saves Quota:** Tracks findings in structured evidence summaries rather than dumping thousands of lines of raw, unreadable assembly into chat.

#### 60. `binary-re-workflows`
* **In Simple Terms:** Coordinates professional reverse engineering tools (like Ghidra, JADX, and network packet analyzers) under a strict scientific process.
* **When It Kicks In:** Inspecting unfamiliar game DLLs, network packets, or complex binary executables.
* **How It Works:** Combines static analysis and runtime tracing to test hypotheses about how closed-source binaries function.
* **Why It Saves Quota:** Turns confusing binary mysteries into deterministic, step-by-step discoveries.

#### 61. `standalone-binary-re`
* **In Simple Terms:** A fast, zero-setup toolkit for peeking inside binary files using standard Linux terminal tools—no heavy servers required.
* **When It Kicks In:** Inspecting executables, DLLs, or Android APKs when external MCP servers are offline or when you need answers in seconds.
* **How It Works:** Uses built-in Linux tools (`objdump`, `readelf`, `nm`, `strings`, `jadx`, `gdb`) and Python scripts to quickly inspect exported functions, headers, and text.
* **Why It Saves Quota:** Starts up instantly with zero overhead and filters out noise so you only see the functions you care about.

#### 62. `open-apk`
* **In Simple Terms:** Automatically opens, inspects, and decompiles Android mobile app packages (APKs) into readable Java code.
* **When It Kicks In:** Reverse engineering Android apps, mobile games, or APK packages.
* **How It Works:** Unpacks APK and DEX files directly into JADX headless analysis, searches classes and methods, and can download APKs directly via `apkeep`.
* **Why It Saves Quota:** Extracts only the exact Java classes you need instead of dumping hundreds of decompiled files into the chat context.

#### 63. `wakaru`
* **In Simple Terms:** Unpacks and unscrambles messy, minified JavaScript bundles (like from Webpack, Vite, or Electron) back into clean, organized files.
* **When It Kicks In:** Auditing modern web apps, Electron desktop software, or production JavaScript bundles.
* **How It Works:** Separates bundled web assets back into individual source files and translates minified shortcuts back into readable classes, async functions, and JSX.
* **Why It Saves Quota:** Turns a gigantic, unreadable 2MB single-line JavaScript file into clean, modular source files with zero hallucination.

#### 64. `lowlevel-dll-internals`
* **In Simple Terms:** A low-level guide for safely modifying Windows DLLs, game engine classes, and memory patches without crashing the game.
* **When It Kicks In:** Writing game mod plugins (like ASI plugins), hooking engine functions, or analyzing crash dumps.
* **How It Works:** Calculates computer memory offsets, 32-bit calling conventions (`__thiscall` in `ecx`), 64-bit ABI shadow space, and virtual function tables so memory patches don't cause instant crashes.
* **Why It Saves Quota:** Prevents dreaded `0xC0000005` "Access Violation" crashes by calculating memory addresses and calling conventions correctly the first time.

#### 65. `steamcmd-workshop-pipeline`
* **In Simple Terms:** Automates publishing and updating mods on the Steam Workshop from the command line without clicking through confusing web forms.
* **When It Kicks In:** Uploading new mods, pushing updates, setting preview images, or writing changelogs on Steam Workshop.
* **How It Works:** Generates valid Steam VDF configuration manifests, manages content depots, and executes SteamCMD commands automatically.
* **Why It Saves Quota:** Replaces error-prone manual upload attempts with an automated, verified deployment script.

#### 66. `python-engineering`
* **In Simple Terms:** Best practices for writing clean, fast, and bug-free modern Python code (Python 3.10+).
* **When It Kicks In:** Writing Python scripts, web APIs, automation tools, or test suites.
* **How It Works:** Enforces strict type hints (`mypy`), lightning-fast code formatting and linting (`ruff`), and comprehensive test suites (`pytest`).
* **Why It Saves Quota:** Catches bugs before code ever runs, saving countless turns of debugging runtime errors.

#### 67. `rust-engineering`
* **In Simple Terms:** Writes reliable, blazing-fast Rust code by working harmoniously with the Rust compiler.
* **When It Kicks In:** Writing systems software, game tools, performance-critical modules, or CLI utilities in Rust.
* **How It Works:** Follows Rust best practices for memory ownership, zero-cost abstractions, error handling with `Result` and `Option`, and strict Clippy lint checks.
* **Why It Saves Quota:** Eliminates runtime crashes completely—if it compiles cleanly in Rust, it works.

#### 68. `modern-cpp-engineering`
* **In Simple Terms:** Modern C++ (C++20/C++23) standards that eliminate old-school memory bugs, buffer overflows, and crashes.
* **When It Kicks In:** Writing game engine code, native libraries, or performance-critical C++ applications.
* **How It Works:** Uses smart pointers (`unique_ptr`, `shared_ptr`), RAII (automatic cleanup of resources), modern Concepts, and clean CMake build files.
* **Why It Saves Quota:** Prevents memory leaks, buffer overflows, and segmentation faults before they happen.

#### 69. `csharp-dotnet-engineering`
* **In Simple Terms:** High-performance modern C# and .NET (8/9) guidelines focused on zero-allocation and responsive async code.
* **When It Kicks In:** Writing C# backend services, desktop utilities, game plugins, or tools.
* **How It Works:** Uses memory-efficient types (`Span<T>`, `Memory<T>`), proper async cancellation tokens, and Roslyn code analyzers to keep apps fast.
* **Why It Saves Quota:** Prevents memory bloat and keeps background operations responsive and leak-free.

---

### 💼 Web Design & Executive Business Communications

#### 73. `human-crafted-web-design`
* **In Simple Terms:** Creates realistic, handcrafted web applications and landing pages that look and feel like they were built by a top-tier design agency, completely avoiding the tacky "AI-generated" aesthetic.
* **When It Kicks In:** Designing web frontends, landing pages, interactive apps, UI dashboards, and responsive portfolios.
* **How It Works:**
  - **Bans Generic AI Tropes:** Enforces strict bans against purple-to-blue neon gradient blur spheres, cheesy floating 3D clay figures, buzzword soup headings (*"Empowering the Future of Synergy"*), and unformatted generic cards.
  - **Tactile Dark Polish:** Uses stacked dark neutral surfaces (`#09090b` canvas, `#121215` cards), 1px subtle borders (`border-neutral-800`), and restrained micro-glow accents (`ring-1 ring-white/10`).
  - **Modern Typography:** Implements clean, modern type scales using Geist Sans or Inter paired with JetBrains Mono for metrics and technical badges.
  - **Ready-to-Use Artifacts:** Includes a responsive Tailwind CSS v4 landing page template ready for production deployment.
* **Why It Saves Quota:** Eliminates endless back-and-forth prompt revisions trying to fix ugly, generic AI layouts.

#### 74. `executive-business-communications`
* **In Simple Terms:** Writes crisp, persuasive business emails, client proposals, contracts, and invoices that sound like a seasoned executive rather than a chatbot.
* **When It Kicks In:** Writing client outreach, business emails, project proposals, Scope of Work (SOW) agreements, payment reminders, or invoices.
* **How It Works:**
  - **BLUF Protocol:** Enforces "Bottom Line Up Front"—delivering the key ask, timeline, and dollar impact in the first 2 sentences.
  - **Anti-Jargon Filter:** Automatically catches and eliminates 50+ robotic corporate clichés (*"I hope this email finds you well"*, *"delve"*, *"tapestry"*, *"game-changer"*, *"testament to"*).
  - **Bulletproof SOWs & Proposals:** Establishes explicit deliverable boundaries, milestone schedules, and strict 2-round revision caps to prevent scope creep.
  - **Printable Invoices:** Ships with a clean, print-optimized HTML invoice template complete with itemized billing, bank wire/SWIFT fields, and tax breakdowns.
* **Why It Saves Quota:** Generates professional, send-ready communications on the first turn without requiring manual prompt engineering to sound human.

---

### 💰 Quota, Memory & Context Engineering

#### 70. `log-output-sanitizer`
* **In Simple Terms:** An automatic muffler for noisy terminal commands that stops hundreds of lines of passing tests and compiler junk from cluttering your chat history.
* **When It Kicks In:** Running `cargo build`, `npm install`, `cmake`, `pytest`, or any test/build pipeline.
* **How It Works:** Applies compact flags (`--quiet`, `--tb=short`, `--message-format=short`) and redirects heavy build streams to `/tmp/build.log`, passing only actionable errors and 1-line summary tallies to the AI's context window.
* **Why It Saves Quota:** Saves **2,000–5,000 input tokens per command execution**, preventing chat history from being flooded with useless progress text.

#### 71. `smart-context-packer`
* **In Simple Terms:** Creates a lightweight "X-ray skeleton" of your code that shows classes and function names without loading thousands of lines of internal loops.
* **When It Kicks In:** Exploring an unfamiliar subsystem, planning a multi-file refactor, or mapping out architecture across 15+ files.
* **How It Works:** Strips out function bodies, comments, and empty lines, preserving only class definitions, public method signatures, and exported types.
* **Why It Saves Quota:** Shrinks a 50,000-token multi-file codebase down to **<4,000 tokens (a 90% reduction)** while giving the AI 100% of the architectural context it needs.

#### 72. `context-pruning-watchdog`
* **In Simple Terms:** An automated context monitor and memory stager that continuously checks prompt volume and safely stages working state into memory before `/compact` is executed.
* **When It Kicks In:** Continuously in the background via `claude-statusline` and `goal_governor.py`. Triggers automatically when context $\ge 50\%$ (~100k tokens), on goal phase-gates, or via manual `context-watchdog check / stage`.
* **How It Works:**
  - Continuously monitors active context percentage and token count from statusline telemetry and conversation logs.
  - Automatically captures dirty git working tree diffs into `.agents/checkpoints/` and compiles current progress, active goals, and next steps into `.agents/memory/activeContext.md`.
  - Flags the statusline (`🧠 Ctx: [====] 52% (104k ⚠️ Staged • Run /compact)`) to alert the user or autonomous agent.
* **Why It Saves Quota:** Eliminates context bloat and catastrophic forgetting. Compacting after staging allows the session to instantly rehydrate in <300 tokens without losing any in-flight code changes or architectural decisions.

#### 75. `token-economy`
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

#### 76. `project-memory-bank`
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

#### 77. `high-density-prompting`
* **In Simple Terms:** A prompt compression engine that turns long, wordy requests into sharp, surgical instructions—stopping the AI from burning thousands of expensive thinking tokens on simple tasks.
* **When It Kicks In:** Whenever you type a prompt, or when you explicitly ask the AI to "distill", "compress", or "optimize" a request.
* **How It Works:**
  - **The 4-Part Directive Formula:** Restructures prompts into `[Target File/Line] + [Action] + [Constraints] + [Verification Command]`.
  - **Suppresses Runaway Thinking Tokens:** Explicitly scopes boundaries so reasoning models (Claude 3.7 Extended Thinking / Gemini Argon) don't speculate across 20 unrelated files or generate 5,000 thinking tokens.
  - **Strips Conversational Overhead:** Eliminates conversational preambles, pleasantries, and requests for conversational walk-throughs that permanently bloat chat history.
  - **Deterministic Output Capping:** Mandates diffs, checklists, or file links instead of 500-word explanations.
* **Why It Saves Quota:** Slashes expensive output reasoning tokens by **75%–90%** and stops prompts from compounding into multi-thousand-token history bloat.

#### 78. `intelligent-interactive-ui`
* **In Simple Terms:** Brings GPT-6 Astra's "Intelligent UI" to your CLI—generating live, reactive mini-apps, calculators, and interactive forms that open in your browser instead of dumping static text tables.
* **When It Kicks In:** Requesting pricing tier estimators, ROI calculators, filterable data tables, or parameter tuning tools.
* **How It Works:** Builds zero-build reactive single-file HTML5 widgets powered by Alpine.js and tactile dark Tailwind CSS. Supports real-time math, dynamic sliders, and one-click JSON/CSV data export buttons.
* **Why It Saves Quota:** Completely replaces back-and-forth conversational calculations with an interactive micro-app you can use indefinitely without burning another API token.

#### 79. `screen-vision-inspector`
* **In Simple Terms:** Gives the AI eyes on your computer screen—autonomously capturing and inspecting your desktop or specific application windows (Project Astra / GPT-6 Astra Vision parity).
* **When It Kicks In:** Diagnosing visual layout bugs, CSS misalignment, broken fonts, game HUD glitches, or terminal rendering issues.
* **How It Works:** Uses local capture utilities (`PIL.ImageGrab`, ImageMagick `import`, `grim`) to grab full screens or bounding boxes (`--bbox`), automatically downscales to 1280px to preserve vision tokens, and stores captures privately in `/tmp/`.
* **Why It Saves Quota:** Eliminates having to manually take screenshots, crop them, upload them to external tools, or guess pixel offsets.

#### 80. `cuda-gpu-acceleration`
* **In Simple Terms:** Direct GPU engineering for NVIDIA GPUs (including your RTX 5060 Blackwell)—compiling CUDA C++ kernels, Tensor Core matrix math, and OptiX ray-tracing.
* **When It Kicks In:** Writing custom CUDA kernels, building PyTorch C++ extensions, GPU memory coalescing, or accelerating local offline AI/3D pipelines.
* **How It Works:** Uses `/opt/cuda/bin/nvcc` with native target flags (`-arch=native`), optimizes shared memory to eliminate DRAM latency, and leverages Tensor Cores (FP16/BF16/FP8).
* **Why It Saves Quota:** Moves heavy numerical tasks and offline 3D rendering to your discrete GPU, executing in milliseconds with zero cloud compute cost.

#### 81. `vulkan-gpu-compute`
* **In Simple Terms:** Cross-vendor GPU compute and modern graphics that run identically across NVIDIA, AMD, and Intel hardware.
* **When It Kicks In:** Writing GPGPU compute shaders, headless data processing, multi-GPU selection, or cross-platform graphics.
* **How It Works:** Compiles GLSL/HLSL compute shaders into portable SPIR-V binaries via `glslangValidator`, selectively dispatches to high-performance discrete GPUs (RTX 5060) or low-power integrated GPUs (Radeon 610M), and debugs synchronization barriers.
* **Why It Saves Quota:** Guarantees universal cross-GPU code compatibility that runs on any modern GPU without vendor lock-in.

#### 82. `hardware-tool-engineering`
* **In Simple Terms:** A specialized guide for building, updating, and maintaining hardware management tools, fan controllers, power governors, and system daemons.
* **When It Kicks In:** Creating hardware utilities (like `omen-acpi`), reading temperature/fan sensors (`hwmon`), managing battery charge thresholds, or detecting CPU SIMD capabilities.
* **How It Works:** Reads Linux `/sys/class/hwmon/` and power supply trees, uses runtime CPU feature detection (`cpuid`) to dispatch AVX-512 or AVX2 SIMD paths, and enforces safe bounds checking before writing to embedded controller registers.
* **Why It Saves Quota:** Prevents kernel panics, permission errors, and hardware crashes through defensive bounds validation and safe udev rules.

### 🎬 Video Production, Gaming AI & Emulation

#### 83. `video-production-automation`
* **In Simple Terms:** Automates video editing, batch transcoding, audio loudness mastering, and color correction with hardware-accelerated NVIDIA NVENC (AV1/HEVC).
* **When It Kicks In:** Transcoding video archives, normalizing audio to broadcast standards (-14 LUFS for YouTube), concatenating clips, or generating proxy files.
* **How It Works:** Uses local FFmpeg with NVENC hardware acceleration (`av1_nvenc`, `hevc_nvenc`, `h264_nvenc`), applying two-pass `loudnorm` audio filters and batch script automation.
* **Why It Saves Quota:** Completely eliminates expensive cloud rendering APIs and GUI video rendering slowdowns by running hardware-accelerated CLI pipelines at hundreds of frames per second.

#### 84. `youtube-shorts-video-automation`
* **In Simple Terms:** Creates viral YouTube Shorts, TikToks, and Instagram Reels from horizontal footage—automatically handling 9:16 vertical re-framing, hook pacing, split-screen gameplay, and animated subtitles.
* **When It Kicks In:** Making YouTube Shorts, cutting vertical clips from long-form content, formatting split-screens (cam + gameplay), or generating word-by-word highlighted captions.
* **How It Works:** Detects aspect ratios, crops or blurs backgrounds to 1080x1920 (9:16), cuts dead silence via audio thresholding, generates styled ASS/SSA animated subtitles, and exports with YouTube-optimized NVENC encoding.
* **Why It Saves Quota:** Generates complete social video assets from a single CLI command without paying for SaaS video generation tools or burning multi-turn prompt tokens on manual layout math.

#### 85. `game-ai-agent-play`
* **In Simple Terms:** Builds AI agents that can observe games, learn game mechanics, and play video games using computer vision and direct input simulation.
* **When It Kicks In:** Training autonomous gaming agents, bot development, reinforcement learning (Gymnasium/Stable-Baselines3), or testing gameplay mechanics automatically.
* **How It Works:** Captures game frames via desktop/screen grabs or window handles, parses visual state with OpenCV (template matching, contour detection, OCR), feeds states to RL policies or state machines, and sends sub-millisecond keyboard/mouse inputs via `/dev/uinput` or `evdev`.
* **Why It Saves Quota:** Enables hands-free, autonomous game testing and robotic gameplay loops without human manual input or cloud gaming server costs.

#### 86. `android-device-automation`
* **In Simple Terms:** Automates Android phone management, real-time screen mirroring (via scrcpy), mobile game botting, app debloating, and cache cleaning.
* **When It Kicks In:** Mirroring Android devices over USB/Wi-Fi, automating repetitive mobile game actions, cleaning junk cache, uninstalling carrier bloatware, or diagnosing device health.
* **How It Works:** Communicates over ADB (`adb shell`) and scrcpy for sub-30ms screen frames, executes touch gestures and swipes via `input tap`/`input swipe`, queries package managers to safely disable bloatware for `user 0`, and analyzes battery/thermal throttling via `dumpsys`.
* **Why It Saves Quota:** Automates tedious phone maintenance and gameplay loops directly over USB/Wi-Fi with zero commercial phone-manager apps or manual tapping.

#### 87. `emulator-development-engineering`
* **In Simple Terms:** A comprehensive engineering handbook for building, debugging, and contributing to video game console emulators (Dolphin, RPCS3, PCSX2, Ryujinx, etc.).
* **When It Kicks In:** Working on emulator codebases, writing CPU interpreters or dynamic binary recompiler (JIT) backends, implementing virtual MMU/fastmem, cycle-accurate bus timing, or Vulkan rendering backends.
* **How It Works:** Architectures guest-to-host register allocation, handles endianness swapping and memory-mapped I/O (MMIO), builds SSA intermediate representations (IR) for JIT compilation, and synchronizes guest audio/video clocks.
* **Why It Saves Quota:** Prevents subtle emulation bugs like timing desyncs, guest crashes, and memory leaks by strictly following proven low-level emulation paradigms.

### 🎮 Real-Time Video Game Graphics & Engine Migration

#### 88. `shader-cross-compilation`
* **In Simple Terms:** Translates, optimizes, and validates game shaders across HLSL, GLSL, SPIR-V, WGSL, and Metal Shading Language (MSL) when modernizing graphics or porting games between engines.
* **When It Kicks In:** Porting DirectX shaders to Vulkan/OpenGL, converting legacy Shader Model 3.0/4.0/5.0 to modern SM 6.x, fixing buffer alignment bugs (`std140` vs `std430`), or resolving Vulkan vs DirectX clip-space and matrix order gotchas.
* **How It Works:** Compiles shaders with `glslangValidator`, optimizes bytecode with `spirv-opt`, validates specification adherence via `spirv-val`, and handles matrix ordering (row-major vs column-major) and clip space Y-inversion.
* **Why It Saves Quota:** Stops endless compile-fail cycles by catching buffer packing violations and dialect incompatibilities before deployment.

#### 89. `game-texture-material-pipeline`
* **In Simple Terms:** Automates game asset texture compression, PBR material channel packing (ORM), and normal map format conversions (DirectX vs OpenGL).
* **When It Kicks In:** Migrating game textures between engines, fixing inverted normal maps (bumps looking like dents), packing separate AO/Roughness/Metallic maps into a single ORM texture, or choosing GPU compression formats (BC1/BC3/BC5/BC7, ASTC, KTX2).
* **How It Works:** Inverts green channels ($Y$) for DirectX/OpenGL normal compatibility, enforces linear color space for data maps and sRGB for albedo, and packs multi-channel textures via automated Python/Pillow pipelines.
* **Why It Saves Quota:** Cuts GPU texture bandwidth in half by combining multiple texture fetches into single samplers and prevents visual material rendering bugs.

#### 90. `game-texture-editing`
* **In Simple Terms:** An autonomous texture editor and repair suite that generates 3D normal maps, blends detail normals mathematically without flattening (RNM), creates seamless repeating tiles, removes baked-in shadows (de-lighting), eliminates dark cutout fringe halos, and sharpens micro-details.
* **When It Kicks In:** Creating or improving game textures, converting heightmaps to tangent normal maps, fixing seam artifacts on repeating terrain/walls, cleaning up ugly dark edges on foliage/sprites, or generating S.T.A.L.K.E.R. `_bump.dds` and `_bump#.dds` pairs.
* **How It Works:** Executes procedural NumPy, Pillow, and ImageMagick algorithms directly via `game-texture-editor` CLI (Scharr gradient normal generation, Reoriented Normal Mapping, Hermite cross-seam blending, alpha color dilation, and frequency-separation de-lighting).
* **Why It Saves Quota:** Eliminates manual GUI photo editor round-trips by performing surgical texture repairs, sharpening, and format conversions automatically via code.

#### 91. `real-time-rendering-pipeline`
* **In Simple Terms:** Architectural guide for modern explicit graphics engines (DirectX 12, Vulkan 1.3+, WebGPU) featuring render graphs, bindless textures, and reversed-Z depth.
* **When It Kicks In:** Building custom renderers, refactoring legacy slot-based drawing to bindless descriptor indexing, eliminating depth fighting in massive outdoor worlds, or analyzing frame captures in RenderDoc.
* **How It Works:** Constructs Directed Acyclic Graph (DAG) render passes with transient memory aliasing, implements unbounded descriptor arrays (`Texture2D g_Textures[]`), and configures floating-point reversed-Z ($[1.0, 0.0]$).
* **Why It Saves Quota:** Eliminates thousands of CPU draw call stalls and state thrashing, enabling 10,000+ objects on screen without frame drops.

#### 91. `game-graphics-optimization-profiling`
* **In Simple Terms:** Detects whether a game is CPU-bound, vertex-bound, pixel-bound, or overdraw-bound, and applies high-performance culling and modern temporal upscaling (TAA, FSR, DLSS).
* **When It Kicks In:** Fixing low framerates, draw call bottlenecks, geometry bottlenecks, implementing Hierarchical-Z (Hi-Z) occlusion culling, or wiring camera jitter and motion vectors for FSR 2/3 and DLSS.
* **How It Works:** Uses GPU multi-draw indirect commands (`vkCmdDrawIndexedIndirect`), sets up Halton sub-pixel camera jitter sequences, generates per-pixel velocity vectors, and configures LOD transition thresholds.
* **Why It Saves Quota:** Pinpoints the exact hardware bottleneck in seconds using empirical profiling rules instead of blindly altering shader math.

#### 92. `post-processing-visual-fx`
* **In Simple Terms:** Implements cinematic visual effects, HDR tone mapping (ACES, AgX), progressive dual-filter bloom, and cascaded shadow maps (CSM).
* **When It Kicks In:** Adding post-processing stacks to a game engine, eliminating highlight burnout in explosions, implementing realistic bloom without GPU lag, or fixing shadow edge shimmering.
* **How It Works:** Applies fitted ACES/AgX tone mapping curves, downsamples and upsamples bloom using 13-tap and 9-tap progressive filters, and calculates logarithmic/uniform split distances for Cascaded Shadow Maps with texel snapping.
* **Why It Saves Quota:** Provides mathematically correct, drop-in shader implementations that eliminate trial-and-error visual tuning.

### 🛡️ Skills Integrity, Health & Lifecycle Management

#### 93. `skills-updater-and-auditor`
* **In Simple Terms:** An automated mechanic that inspects all installed skills across Antigravity and Claude Code—fixing broken permissions, validating YAML frontmatter, checking missing tool dependencies, and pulling updates from GitHub with one command.
* **When It Kicks In:** Whenever you want to check if your skills are up to date, after pulling git changes, when adding new skills, or if a skill script fails to run.
* **How It Works:** Audits all 3 directories (`config/skills/`, `~/.gemini/config/skills/`, `~/.claude/skills/`), runs syntax linters on Python/Bash scripts, auto-applies `chmod +x` to helper scripts, scans for required host CLI tools (`ffmpeg`, `adb`, `glslangValidator`, etc.), and checks `origin/main` for remote updates.
* **Why It Saves Quota:** Eliminates silent agent errors, broken script execution failures, and desynchronized configurations that cause models to fail mid-turn and burn tokens diagnosing setup bugs.

### 📱 Full-Stack Android Engineering & Optimization

#### 94. `android-ndk-jni-engineering`
* **In Simple Terms:** High-performance Android C/C++ development—connecting native code to Kotlin via zero-copy JNI, running Vulkan/Oboe audio pipelines, and decoding native crash dumps.
* **When It Kicks In:** Writing native libraries in C++, porting game engines to Android, optimizing DSP audio, preventing JNI local reference table overflow crashes, or symbolizing native `SIGSEGV` tombstone stack traces.
* **How It Works:** Uses direct ByteBuffers (`GetDirectBufferAddress`) for zero-copy memory transfers, caches `jmethodID`/`jfieldID` lookups in `JNI_OnLoad`, configures Oboe low-latency audio streams (`AAudio`), and symbolizes PC addresses with `addr2line`.
* **Why It Saves Quota:** Stops native crashes and cryptic JNI pointer bugs before they enter endless trial-and-error debugging loops.

#### 95. `android-compose-ui-ux`
* **In Simple Terms:** Advanced Jetpack Compose UI design system—building butter-smooth Material 3 interfaces, edge-to-edge window insets, and eliminating recomposition lag.
* **When It Kicks In:** Creating Android screens in Compose, fixing UI stuttering or dropped frames during scrolling, styling status/navigation bars, handling IME keyboard padding, or designing custom canvas drawings.
* **How It Works:** Enforces `@Immutable` and `@Stable` contracts on UI models, defers state reads to layout/draw phases via lambdas (`Modifier.offset { ... }`), and utilizes modern `enableEdgeToEdge()` APIs.
* **Why It Saves Quota:** Fixes UI rendering lag and recomposition thrashing by structuring state correctly on the first attempt.

#### 96. `android-architecture-jetpack`
* **In Simple Terms:** Architectural blueprint for modern Android apps—connecting ViewModels, Room databases, type-safe Navigation, and WorkManager background tasks using clean Unidirectional Data Flow.
* **When It Kicks In:** Setting up a new Android project, adding Room persistence with schema migrations, switching to type-safe Kotlin DSL Navigation (2.8+), or managing background sync workers.
* **How It Works:** Implements single immutable `StateFlow<UiState>` per screen with `collectAsStateWithLifecycle()`, defines Room DAOs with reactive Flows, and injects dependencies via Dagger Hilt.
* **Why It Saves Quota:** Prevents lifecycle leaks, configuration change data loss, and architecture spaghetti that requires full app rewrites.

#### 97. `android-testing-ci-cd-security`
* **In Simple Terms:** Complete testing, CI/CD automation, and release security suite for Android—testing ViewModels locally on JVM without an emulator, configuring R8 bytecode shrinking, and securing secrets with Android Keystore.
* **When It Kicks In:** Writing unit tests with MockK & Turbine, authoring Compose semantics UI tests, setting up headless Gradle CI builds, preventing reverse engineering with R8, or encrypting sensitive tokens.
* **How It Works:** Runs JVM-speed unit tests with Robolectric, configures strict ProGuard keep rules for JNI and serialization, archives `mapping.txt` for Play Console deobfuscation, and generates hardware-backed AES-256 keys via StrongBox Keystore.
* **Why It Saves Quota:** Validates code health on the fast local JVM in seconds without booting heavy Android emulators or paying cloud CI fees.

#### 98. `android-perf-battery-profiling`
* **In Simple Terms:** Diagnostic toolkit for finding why an Android app is lagging, dropping frames, draining the battery, or leaking memory.
* **When It Kicks In:** Diagnosing missed VSYNC frame deadlines (jank), analyzing battery wake locks, catching main-thread disk/network operations via StrictMode, or debugging OutOfMemoryError crashes.
* **How It Works:** Queries `dumpsys gfxinfo framestats` for 90Hz/120Hz missed deadlines, dumps battery wake lock durations via `dumpsys batterystats`, and extracts/converts heap dumps (`am dumpheap` + `hprof-conv`) to detect leaked Activities.
* **Why It Saves Quota:** Replaces vague guessing about app performance with exact millisecond frame histograms and battery power breakdown logs.

### 🧭 Dynamic Orchestration & Long-Horizon Memory

#### 99. `dynamic-skill-router`
* **In Simple Terms:** An intelligent navigation system for your 105-skill toolkit—analyzing your prompt in milliseconds and finding the exact 2-3 best skills to use, stopping the AI from getting overwhelmed by too many choices.
* **When It Kicks In:** Whenever you give a task that spans multiple disciplines, or when the AI needs to discover which specialized skills apply to an unfamiliar technical problem.
* **How It Works:** Uses a BM25-style inverted keyword index with IDF token weighting and skill name boosting (`scripts/skill_router.py`), scoring all 105 skills in under 20ms and outputting ranked matches with explanations.
* **Why It Saves Quota:** Eliminates the token cost of scanning or loading dozens of skill files into active memory, cutting discovery overhead by up to **95%**.

#### 100. `session-episodic-memory`
* **In Simple Terms:** A chronological journal for your coding sessions—recording what you worked on, why you made specific architectural choices, which approaches failed, and what to do next so the AI never forgets across `/compact` resets or multi-day breaks.
* **When It Kicks In:** Long engineering tasks, complex multi-session projects, or before running `/compact`.
* **How It Works:** Writes structured, timestamped episode snapshots to `.agents/episodes/YYYY-MM-DD_HHMM.md` capturing Objectives, Key Decisions (ADRs), Discarded Alternatives, and Next Tasks.
* **Why It Saves Quota:** Completely prevents circular debugging loops (trying a solution that was already proven broken 2 hours ago) and eliminates having to re-explain the project history after running `/compact`.

### 🕹️ Video Game Engine Architecture & Porting Foundations

#### 101. `game-audio-engine-engineering`
* **In Simple Terms:** Real-time audio engine architecture—enforcing lock-free audio callbacks, 3D HRTF binaural spatialization, bus mixing hierarchies, and sound bank asset pipelines.
* **When It Kicks In:** Building custom audio systems, integrating audio libraries (OpenAL Soft, MiniAudio, FMOD, Wwise), fixing audio crackling/pops caused by thread priority inversions, or implementing dynamic ducking and 3D sound occlusion.
* **How It Works:** Enforces zero-allocation (`malloc`/`free`) and lock-free SPSC queues inside audio threads, implements inverse-distance spatial attenuation with equal-power panning, and applies biquad low-pass filtering for physics-based occlusion.
* **Why It Saves Quota:** Eliminates intermittent, hard-to-reproduce audio crashes and priority inversions that derail game testing sessions.

#### 102. `game-physics-collision-pipeline`
* **In Simple Terms:** Deterministic physics simulation and collision pipeline—eliminating collision tunneling via fixed-timestep accumulator loops and continuous collision detection (CCD).
* **When It Kicks In:** Implementing or porting game physics (Jolt, PhysX, Box2D, custom engine), fixing fast-moving projectiles passing through walls, or resolving visual camera jitter.
* **How It Works:** Decouples variable rendering framerates from fixed physics steps ($1/60\text{s}$) using alpha state interpolation, organizes bounding volumes into dynamic BVH trees, and computes penetration depth/normals using GJK and EPA simplex algorithms.
* **Why It Saves Quota:** Prevents broken physics edge cases and collision tunneling loops before they corrupt game state or require multi-hour debugging.

#### 103. `game-memory-allocator-engineering`
* **In Simple Terms:** Custom game engine memory managers (Linear Arenas, Stack Rollbacks, Pool Free Lists, TLSF)—eliminating memory fragmentation and aligning data to 64-byte CPU cache lines.
* **When It Kicks In:** Porting 32-bit games to 64-bit, eliminating heap fragmentation (`malloc` overhead), enforcing SIMD vector alignment, or building frame-lifetime transient allocators.
* **How It Works:** Uses contiguous pre-allocated byte arenas with pointer bumping for single-frame scratchpads, pooled chunks for uniform entities/particles, and bitmask-indexed TLSF for variable heap allocations, with strict 64-byte cache line alignment.
* **Why It Saves Quota:** Eliminates mysterious OS page fault hitches, memory leaks, and pointer alignment crashes common during 64-bit engine ports.

#### 104. `game-input-system-abstraction`
* **In Simple Terms:** Universal game input abstraction layer—unifying controllers, mice, and keyboards with mathematically correct radial deadzones and dynamic button glyphs.
* **When It Kicks In:** Porting game input across platforms (Windows RawInput, SDL3, Linux evdev, Steam Input), fixing diagonal gamepad aiming drift, or auto-switching UI button prompts between Xbox, PlayStation, and Nintendo.
* **How It Works:** Replaces buggy axial deadzones with normalized Scaled Radial Deadzone math ($D = \frac{\lVert v \rVert - r_{in}}{r_{out} - r_{in}} \cdot \hat{v}$), accumulates sub-pixel mouse deltas for high-DPI mice, and inspects controller vendor/product GUIDs to dynamically render gamepad glyphs.
* **Why It Saves Quota:** Fixes controller drift, sticky diagonal aiming, and broken device hot-plugging on the first implementation pass.

#### 105. `game-asset-pack-archive-engineering`
* **In Simple Terms:** Virtual File System (VFS) and packed game container toolchain—loading assets from compressed archives with memory-mapped I/O (`mmap`) and mod priority hierarchies.
* **When It Kicks In:** Packaging game assets into binary archives, implementing mod override support without altering base game files, or converting loose file disk reads into zero-copy memory-mapped containers.
* **How It Works:** Implements a priority-ordered VFS mount hierarchy (Mod Override $\to$ Patch $\to$ Base Game), serializes chunked binary archives (`VPAK`) with zlib compression, and provides a standalone CLI asset packer (`scripts/vfs_asset_packer.py`).
* **Why It Saves Quota:** Speeds up game asset loading, prevents loose-file disk thrashing, and eliminates broken mod installation paths.

#### 106. `game-entity-component-system`
* **In Simple Terms:** Architectural guide for high-throughput Entity Component Systems (ECS) and Data-Oriented Design (DOD)—organizing game entities into cache-friendly memory streams and scheduling systems across CPU cores.
* **When It Kicks In:** Designing core engine logic, porting slow object-oriented classes to Archetype (Flecs/Bevy) or Sparse-Set (EnTT) patterns, eliminating CPU cache misses, or scheduling multithreaded systems with read/write access bitmasks.
* **How It Works:** Replaces fragmented pointer chasing with contiguous Structure-of-Arrays (SoA) memory pools, implements $O(1)$ component add/remove via swap-and-pop, and prevents pointer bugs using 64-bit generational entity handles.
* **Why It Saves Quota:** Enables 100,000+ entities updating simultaneously without frame drops, eliminating late-stage engine rewrites due to OOP CPU bottlenecks.

#### 107. `game-animation-skeletal-pipeline`
* **In Simple Terms:** Real-time 3D character animation and skeletal deformation—handling bone transforms, quaternion SLERP interpolation, dual-quaternion volume skinning, and inverse kinematics (IK).
* **When It Kicks In:** Adding skeletal character animation to a custom engine, fixing "candy-wrapper" joint volume loss on extreme twists, implementing foot placement IK on uneven terrain, or decoupling root motion for physics controllers.
* **How It Works:** Interpolates bone rotations via shortest-path SLERP/NLERP, preserves joint volumes using Dual Quaternion Skinning, solves joint angles using analytical Two-Bone and multi-link FABRIK IK solvers, and extracts horizontal displacement for physics movement.
* **Why It Saves Quota:** Fixes foot sliding, character mesh twisting glitches, and quaternion flipping bugs on the first implementation attempt.

#### 108. `game-networking-state-sync`
* **In Simple Terms:** Multiplayer networking engine—keeping players in sync across high-ping connections using client-side input prediction, server reconciliation, remote entity interpolation, and delta snapshots.
* **When It Kicks In:** Adding multiplayer to a game, fixing rubber-banding and player jitter, compressing state packets over UDP, or building deterministic rollback networking.
* **How It Works:** Simulates local inputs instantly in an unacknowledged ring buffer, reconciles local errors against authoritative server ticks by replaying inputs, smoothly interpolates remote proxies along Hermite splines, and packs rotations into 32-bit "smallest three" integers.
* **Why It Saves Quota:** Provides mathematically proven lag compensation algorithms, preventing multiplayer desync loops and phantom hit bugs.

#### 109. `game-save-state-serialization`
* **In Simple Terms:** Corruption-proof game save system—saving and loading game worlds with versioned binary chunks, checksum validation, and atomic disk replacement.
* **When It Kicks In:** Implementing save/load checkpoints, porting save files across engine revisions, preventing save file corruption on sudden game crashes, or inspecting binary save containers.
* **How It Works:** Serializes tagged binary chunks (`GSAV`) with CRC32 integrity validation, handles schema version migrations automatically, and writes atomically to `.tmp` files before disk swaps. Includes a standalone inspector CLI (`scripts/save_state_inspector.py`).
* **Why It Saves Quota:** Stops corrupted save files and backwards compatibility breakage from corrupting developer test runs and player data.

#### 110. `game-debug-ui-tools`
* **In Simple Terms:** In-engine developer dashboard and diagnostic toolkit—embedding Dear ImGui menus, 3D debug shapes (rays, boxes, contact points), live console variables (CVars), and real-time CPU/GPU frame profilers.
* **When It Kicks In:** Diagnosing gameplay bugs in real time, tuning physics/graphics variables live without restarting the engine, profiling frame stutter, or visualizing collision hitboxes.
* **How It Works:** Hooks Dear ImGui as a post-tonemap render pass with automatic input capture blocking, provides immediate-mode `DebugDraw` primitive rings, exposes runtime CVars with auto-completion, and records hierarchical RAII scope flame charts.
* **Why It Saves Quota:** Eliminates the cycle of recompiling the game 20 times to test different numbers by letting you tweak values live in-game.

### 🤖 Discord Bot Engineering & Real-Time APIs

#### 111. `discord-bot-engineering`
* **In Simple Terms:** Complete production Discord bot development kit—creating modern slash commands, interactive buttons, modal text forms, select menus, and voice audio streaming in Python (`discord.py`) or TypeScript (`discord.js`).
* **When It Kicks In:** Building or maintaining Discord bots, implementing slash commands, handling modals/buttons/select menus, calculating gateway intent and permission bitmasks, connecting to voice channels with Opus audio, or scaling to thousands of servers with sharding.
* **How It Works:** Enforces sub-3-second deferred interaction discipline, handles route-specific rate-limit buckets, provides clean modular Cog/Command architectures, streams low-latency audio via FFmpeg and PyNaCl, and includes a standalone bitmask calculator (`scripts/discord_bitmask_calculator.py`).
* **Why It Saves Quota:** Stops common Discord pitfalls (failed interaction timeouts, missing privileged intents, unhandled rate-limit 429 loops) before you burn tokens debugging WebSocket errors.

### 🎵 Procedural & Generative Audio Engineering

#### 112. `ai-procedural-audio-generation`
* **In Simple Terms:** Sound effect and music generation workshop—synthesizing game SFX (lasers, explosions, coins, whooshes, UI clicks) offline with pure code, guiding AI text-to-audio models, layering adaptive game music, and mastering loudness.
* **When It Kicks In:** Creating game sound effects, generating UI interaction audio, scoring background music for videos/shorts, implementing multi-stem dynamic combat music, or normalizing sound to YouTube (-14 LUFS) or mobile (-16 LUFS) standards.
* **How It Works:** Uses pure mathematical waveform synthesis (Sine, Square, Sawtooth, White Noise) with ADSR envelope shaping, provides an instant offline SFX synthesis tool (`scripts/procedural_sfx_generator.py`), and engineers prompts for frontier text-to-sound-effect models (ElevenLabs SFX, AudioCraft).
* **Why It Saves Quota:** Generates game-ready sound effects and UI pings locally in milliseconds with zero API costs, zero quotas, and zero external software.

### 🛡️ Cyber Security, Anti-Tamper & Applied Cryptography

#### 113. `game-security-anti-tamper`
* **In Simple Terms:** In-game anti-tamper and anti-cheat guard—protecting game executables against memory injection, blocking DLL proxy hijacking, sealing save files with HMAC signatures, and enforcing server-side anti-teleport physics.
* **When It Kicks In:** Hardening a game client against memory modifications (Cheat Engine), protecting save states from hex editing, preventing malicious proxy DLLs (`version.dll`, `dxgi.dll`), or writing server-side sanity checks for multiplayer movement.
* **How It Works:** Restricts DLL search paths to System32 (`SetDefaultDllDirectories`), seals save files with HMAC-SHA256 signatures verified in constant time, tracks monotonic version counters, and bounds player displacement deltas against physics limits.
* **Why It Saves Quota:** Stops cheat injection vulnerabilities and save file corruption exploits during development before they compromise player economies.

#### 114. `cryptographic-security-engineering`
* **In Simple Terms:** Applied modern cryptography toolkit—verifying Ed25519 digital signatures (Discord bot webhooks, Git commits), encrypting data with AES-256-GCM AEAD, deriving keys with HKDF, and enforcing constant-time comparisons.
* **When It Kicks In:** Handling cryptographic keys, verifying Discord interaction HTTP webhooks, encrypting sensitive local credentials/tokens, deriving domain-separated subkeys, or preventing remote timing side-channel attacks.
* **How It Works:** Uses verified modern primitives (Ed25519, AES-256-GCM, HKDF-SHA256), eliminates timing leaks via constant-time comparisons (`secrets.compare_digest`), and provides a standalone cryptographic utility (`scripts/crypto_guard.py`).
* **Why It Saves Quota:** Eliminates fragile custom crypto implementations and padding oracle vulnerabilities that cause catastrophic security flaws.

#### 115. `devsecops-supply-chain-security`
* **In Simple Terms:** Build-time binary hardening and supply chain inspector—verifying compiler defense flags (Full RELRO, Stack Canaries, NX, PIE via `checksec`), scanning dependencies for CVEs, generating SBOMs, and securing CI/CD pipelines.
* **When It Kicks In:** Packaging production binaries or shared libraries, auditing GitHub Actions workflows for supply chain risks, pinning actions to immutable commit SHAs, or running automated CVE audits (`cargo-audit`, `pip-audit`).
* **How It Works:** Inspects ELF binary headers for RELRO, canary symbols, and non-executable stacks (`scripts/binary_hardening_check.py`), audits dependency vulnerability databases, and enforces least-privilege CI/CD execution.
* **Why It Saves Quota:** Catches missing compiler security flags and vulnerable dependencies automatically at build time before deployment to end users.

### 🎮 Game Compatibility, Portability & Binary Repair

#### 116. `cross-platform-game-compatibility`
* **In Simple Terms:** The universal repair protocol for getting legacy and modern PC games to run smoothly on modern Windows 10/11 and Linux without crashing.
* **When It Kicks In:** 32-bit games running out of RAM (CTD at 2GB), legacy DirectX 1–9 titles stuttering or black-screening, physics going crazy on >60Hz monitors, or games freezing on modern high-core CPUs.
* **How It Works:** Applies 4GB Large Address Aware (LAA) patches to 32-bit PE headers (`scripts/laa_pe_patcher.py`), configures legacy DirectX translation layers (dgVoodoo2, d3d8to9, DXVK), clamps CPU thread affinity to physical performance cores, and sets frame limits.
* **Why It Saves Quota:** Solves 90% of legacy PC game launch failures systematically in 1 turn instead of blindly tweaking random Windows compatibility flags.

#### 117. `linux-gaming-proton-optimization`
* **In Simple Terms:** Dedicated tuning and troubleshooting guide for running Windows games on Linux distributions (CachyOS, Arch, Fedora) and the Steam Deck via Valve's Proton and Wine.
* **When It Kicks In:** Steam games showing black cutscenes or test screens (Media Foundation missing), shader compilation stuttering, prefix dependency corruption, or configuring Gamescope and GameMode.
* **How It Works:** Tunes `dxvk.conf` for asynchronous shader compilation, switches to GE-Proton for proprietary video codecs, repairs broken wineprefixes with non-destructive `protontricks`, and crafts optimized launch commands (`gamemoderun mangohud gamescope`).
* **Why It Saves Quota:** Diagnoses Proton launch failures from log signatures directly rather than deleting and re-downloading entire 50GB game prefixes.

#### 118. `game-patching-binary-repair`
* **In Simple Terms:** Diagnosing and surgically repairing broken, crashing, or abandoned PC game binaries when source code is completely unavailable.
* **When It Kicks In:** Games failing to launch with `0xC0000135` (missing DLL) or `0xC0000139` (entry point not found), opaque crashes at specific memory offsets, or legacy disc checks failing on modern OS.
* **How It Works:** Inspects the executable's Import Address Table (`scripts/pe_dependency_check.py`), disassembles instructions around crash offsets with `objdump`, authors proxy DLL shims (`dinput8.dll`, `version.dll`), and applies safe byte-level hex patches.
* **Why It Saves Quota:** Resolves binary engine crashes through pinpoint offset disassembly and minimal shims rather than trial-and-error mod guessing.

### 🛡️ End-to-End Application & Network Security Hardening

#### 119. `app-security-threat-modeling`
* **In Simple Terms:** Comprehensive application security architecture covering STRIDE threat modeling, OWASP Top 10 defense, path traversal prevention, and memory zeroing for sensitive secrets.
* **When It Kicks In:** Architecting new desktop apps, web services, or backend daemons; preventing IDOR/BOLA authorization bypasses; sanitizing file upload paths; and zeroing cryptographic secrets from memory buffers.
* **How It Works:** Implements STRIDE defense-in-depth matrices, resolves absolute canonical paths against directory climbing attacks, and enforces immediate memory wiping (`memset_s` / `zeroize` / buffer clearing) with `mlock()` to prevent secrets leaking in crash dumps.
* **Why It Saves Quota:** Identifies security flaws systematically during architectural design before expensive post-release penetration test remediation cycles.

#### 120. `api-network-security-hardening`
* **In Simple Terms:** Transport and network boundary defense—TLS 1.3 AEAD cipher hardening, mobile/desktop SPKI certificate pinning, token bucket rate limiting, webhook replay defenses, and modern CSP policies.
* **When It Kicks In:** Protecting API endpoints, game servers, or Discord bots against DDoS floods, credential stuffing, man-in-the-middle (MITM) proxy interception, and webhook replay attacks.
* **How It Works:** Implements sliding-window token bucket algorithms, validates incoming webhook timestamp freshness (<300s window) with HMAC-SHA256, pins SPKI SHA-256 hashes, and applies strict browser isolation HTTP security headers.
* **Why It Saves Quota:** Stops bot spam, API brute-forcing, and replay attacks at the network boundary before they consume backend database and compute quota.

#### 121. `client-memory-integrity-anticheat`
* **In Simple Terms:** Client runtime protection against memory scanners (Cheat Engine), dynamic debuggers (x64dbg, IDA, GDB, Frida), and illegal function hooks.
* **When It Kicks In:** Developing single-player or multiplayer games, desktop software with sensitive license/auth state, or anti-tamper client modules.
* **How It Works:** Encrypts in-memory integers with XOR dynamic masks to hide values from scanner sweeps, queries Win32 PEB / hardware debug registers (DR0–DR3) / Linux `ptrace` anti-attach probes, and verifies periodic state hash heartbeats with authoritative servers.
* **Why It Saves Quota:** Prevents basic cheat engine modifications and memory hacking from breaking game economies and multiplayer simulations.

### 🐧 Proton & Handheld Linux Game Development

#### 122. `proton-game-dev-linux`
* **In Simple Terms:** Guidelines and automated tools for engineering PC games that target Valve's Proton seamlessly from day one—achieving 100% Linux and SteamOS compatibility without maintaining a separate Linux port.
* **When It Kicks In:** Designing cross-platform asset VFS paths (preventing case-sensitivity crashes), selecting video cutscene codecs (WebM/VP9 instead of proprietary Media Foundation), and testing builds headlessly via Proton CLI in CI.
* **How It Works:** Enforces lowercase internal path normalization, specifies open royalty-free video formats (WebM/Opus), and provides a headless continuous integration runner (`proton run Game.exe --headless-tests`).
* **Why It Saves Quota:** Eliminates the hundreds of hours and engineering turns spent porting games to native Linux by leveraging Proton as a first-class deployment target.

#### 123. `steamdeck-proton-hardware-tuning`
* **In Simple Terms:** Handheld hardware optimization for Steam Deck and mobile Linux devices running Proton games.
* **When It Kicks In:** Optimizing games for the Steam Deck's 15W APU TDP envelope, locking 40Hz/45Hz refresh rate frame pacing, supporting native 1280x800 (16:10) resolutions, and ensuring in-game font legibility.
* **How It Works:** Applies 25ms 40Hz frametime pacing for maximum battery longevity, enforces minimum 28px font heights at 800p for handheld reading, and optimizes asset packaging for MicroSD card read throughput.
* **Why It Saves Quota:** Directly achieves Valve "Deck Verified" status on the first submission without multi-round QA rejection cycles.

#### 124. `wine-proton-native-interop`
* **In Simple Terms:** Advanced systems engineering for bridging native Linux host capabilities (system daemons, Unix Domain Sockets, pipe communication, shared memory) with Windows games running inside Proton.
* **When It Kicks In:** Connecting Windows game processes to native Linux companion tools (OBS, Discord RPC, telemetry dashboards) or writing custom Wine thunking libraries to call Linux `.so` libraries directly.
* **How It Works:** Uses Wine's named pipe mapping to bridge into Linux Unix sockets (`\\.\pipe\...` -> `/dosdevices/pipe/...`), utilizes `/dev/shm` for zero-copy memory buffers, and configures `WINEDEBUG=+relay` for API call traces.
* **Why It Saves Quota:** Enables seamless host-to-guest interop without requiring complex networked TCP/UDP overhead or fragile hacks.

#### 125. `gamemaker-gml-engineering`
* **In Simple Terms:** Modern 2D/2.5D game architecture and performance optimization using modern GameMaker (2024+) and GML Code.
* **When It Kicks In:** Authoring GML scripts, creating lightweight constructor structs (eliminating heavy object bloat), finite state machines via method variables, managing volatile surface VRAM lifecycle, avoiding draw batch breaks, and tuning delta timing.
* **How It Works:** Replaces traditional `ds_*` maps/lists with native GC-managed structs and arrays, safeguards dynamic surfaces against alt-tab crashes with automatic recreation logic, batches draw calls by texture group, and implements sub-pixel delta timing.
* **Why It Saves Quota:** Prevents common GameMaker pitfalls (VRAM memory leaks, stuttery frame pacing, object count bloat) before they corrupt runtime performance.

#### 126. `game-trainer-engineering`
* **In Simple Terms:** Cross-platform game trainer, cheat engine, and debug overlay development for PC games on Windows and Linux (native and Steam Proton/Wine).
* **When It Kicks In:** Creating external or internal game trainers, resolving dynamic multi-level pointer chains, scanning memory with wildcard AOB (Array of Bytes) signatures, writing mid-function assembly trampoline detours, or injecting trainers via `WINEDLLOVERRIDES`.
* **How It Works:** Provides cross-platform pointer resolution algorithms, wildcard bytecode pattern scanners, Win32 `ReadProcessMemory` / Linux `/proc/<pid>/mem` handlers, and DirectX/Vulkan ImGui overlay injection techniques.
* **Why It Saves Quota:** Pinpoints exact memory offsets and stable signature masks in 1 turn rather than wasting context on blind trial-and-error memory scanning.

#### 127. `game-localization-i18n`
* **In Simple Terms:** Complete game internationalization (i18n) and localization (L10n) pipeline for games, engines, and interactive applications.
* **When It Kicks In:** Setting up multi-language catalogs (PO, JSON, CSV), handling ICU message format pluralization rules, managing RTL (Right-to-Left) BiDi layout flipping for Arabic/Hebrew, and configuring fallback font chains for CJK and Cyrillic glyphs.
* **How It Works:** Enforces key-based string extraction over hardcoded text, validates ICU plural rules across languages with distinct numeric categories (e.g. Slavic `one/few/many/other`), automates UI bounding box expansion budgets (30%–50% growth for German), and configures runtime font fallback hierarchies.
* **Why It Saves Quota:** Prevents catastrophic broken UI text truncations, missing glyph boxes ("tofu"), and grammar bugs without requiring multi-round localization patch cycles.

#### 128. `headless-game-ci-automation`
* **In Simple Terms:** Headless continuous integration, automated command-line testing, and cross-platform artifact packaging for Godot, Unity, and Unreal Engine.
* **When It Kicks In:** Setting up GitHub Actions, GitLab CI, or local Docker build containers to run game test suites headlessly (Godot GUT, Unity Test Framework, Unreal RunUAT) and export automated release builds.
* **How It Works:** Formats exact headless CLI execution arguments (`--headless`, `-batchmode -nographics`, `RunUAT.sh -nocompileeditor`), handles fake virtual framebuffers (Xvfb) when display servers are missing, parses machine-readable JUnit/XML test reports, and generates versioned zip/tar release archives.
* **Why It Saves Quota:** Automates tedious manual export clicks and catches game regressions in CI before they pollute release builds.

#### 129. `godot-shader-vfx`
* **In Simple Terms:** Specialized visual shaders, screen-space distortion effects, and GPU compute particle systems for Godot Engine 4.
* **When It Kicks In:** Writing Godot 4 `spatial`, `canvas_item`, and `particles` shaders, creating screen-reading distortion effects (heat haze, shockwaves, water refractions), foliage wind vertex displacement, and GPU particle simulations.
* **How It Works:** Uses modern Godot 4 shader syntax with `hint_screen_texture` sampler uniforms, implements custom vertex function world-space displacement, and optimizes particle systems to run on GPU compute pipelines without CPU overhead.
* **Why It Saves Quota:** Delivers production-grade Godot 4 shader code on the first attempt, avoiding obsolete Godot 3 shader syntax errors and runtime compiler warnings.

#### 130. `hierarchical-memory-retrieval`
* **In Simple Terms:** A super-fast search engine for your project memory, finding only the 1–2 relevant sentences from past notes without loading entire files into chat.
* **When It Kicks In:** Whenever the AI needs to check past architectural decisions, bug solutions, or configuration rules across long-running projects.
* **How It Works:** Uses BM25 keyword relevance to search across `.agents/memory/`, `.agents/episodes/`, and documentation, extracting a 3–5 line preview snippet in under 15ms.
* **Why It Saves Quota:** Cuts memory hydration costs from 10,000+ tokens down to under 250 tokens per turn, preventing memory bloat.

#### 131. `context-window-governor`
* **In Simple Terms:** An automatic traffic cop that stops massive command outputs (like 5,000 lines of compiler errors or raw files) from blowing up your conversation limit.
* **When It Kicks In:** On every command execution and file view, estimating token size before loading.
* **How It Works:** Allocates mathematical token budgets per turn (20% rules, 35% code, 25% output, 20% response) and clamps noisy outputs over 50 lines to head+tail previews, saving full raw dumps to `/tmp/`.
* **Why It Saves Quota:** Eliminates catastrophic 40k-token context spikes from a single command, keeping your session running smoothly under the 60% compaction threshold.

#### 132. `working-memory-checkpointing`
* **In Simple Terms:** A quick-save and rewind button for your code and thoughts, so the AI can safely test risky ideas without messing up your workspace.
* **When It Kicks In:** Before trying an unverified bug fix, experimental refactor, or complex multi-file edit.
* **How It Works:** Takes a snapshot of uncommitted git changes and hypothesis notes in `.agents/checkpoints/`. If an experiment fails, a single command restores your clean workspace in milliseconds.
* **Why It Saves Quota:** Prevents the AI from spending 5 rambling turns trying to manually undo broken code, cutting experiment recovery down to 1 command.

#### 133. `coderabbit-ai-review`
* **In Simple Terms:** An autonomous CodeRabbit-grade reviewer that audits pull requests, generates component interaction diagrams, and writes 1-click GitHub fix suggestions.
* **When It Kicks In:** Before committing or submitting pull requests, performing multi-dimensional reviews across correctness, security, performance, and architecture.
* **How It Works:** Analyzes git diffs using static heuristics (checking for leaked secrets, injection risks, resource leaks, missing boundary checks), produces a Mermaid sequence diagram showing component interactions, and outputs a 0–100 readiness score with a formal verdict (`APPROVE` or `REQUEST_CHANGES`).
* **Why It Saves Quota:** Catches defects and security vulnerabilities locally before triggering costly remote CI review cycles or production regressions.

#### 134. `console-game-decompilation`
* **In Simple Terms:** Reverse engineering and matching decompilation toolkit to turn PS1, PS2, PS3, original Xbox, Xbox 360, and GameCube game binaries back into compilable C/C++ source code.
* **When It Kicks In:** Reverse engineering console games for preservation, source ports, or engine modding; inspecting executable containers (PS-X EXE, ELF, XBE, XEX); splitting ROMs with splat; or verifying function matches with `objdiff` and `decomp.me`.
* **How It Works:** Integrates native CLI tools (`objdiff` for visual diffing, `splat` for binary splitting, `m2c` for MIPS/PowerPC assembly-to-C translation, and `rizin`/`rz-ghidra` for headless decompilation) to automate container inspection, section partitioning, and register mismatch diagnosis.
* **Why It Saves Quota:** Eliminates thousands of hours of manual binary analysis by automating container inspection, section partitioning, and register mismatch diagnosis.

#### 135. `game-screen-telemetry-monitor`
* **In Simple Terms:** Real-time in-game visual observer that detects graphics glitches (missing magenta textures, black screens), monitors frame changes, and automatically transcribes crash errors off the screen.
* **When It Kicks In:** Playtesting games, porting mods between game engines (e.g. S.T.A.L.K.E.R. Complete to the 64-bit OGSR Engine), or diagnosing sudden engine freezes and desktop crashes.
* **How It Works:** Uses local headless screen capture (`spectacle` on KDE Wayland, X11/Pillow fallback) downscaled to 1280px to protect quotas, scans pixel histograms for unmapped missing textures (`#FF00FF`) or GPU hangs, and executes local OCR (`tesseract`) to transcribe fatal error dialogs and stack traces.
* **Why It Saves Quota:** Eliminates manual screenshot cropping and typing out crash logs by autonomously extracting the exact engine crash code directly into structured logs.

#### 136. `autonomous-goal-governor`
* **In Simple Terms:** Autonomous supervisor and quota protector for long-running `/goal` commands and overnight agent tasks that prevents infinite error loops, halts on 3 consecutive failures, and manages 5-hour and weekly quota reserves.
* **When It Kicks In:** Running `/goal <description>`, launching overnight autonomous builds, formulating testable completion contracts, monitoring quota reserves, or handling recurring compile/test failures.
* **How It Works:** Turns open-ended prompts into machine-verifiable exit criteria (`goal_governor.py formulate`), enforces an automated 3-strike circuit breaker that rolls back code via `working-memory-checkpointing` after 3 consecutive failures, automatically takes a **smart checkpoint** into `.agents/checkpoints/` when weekly quota drops to 25%, and safely pauses and waits (`--wait-on-5h`) for 5-hour quota replenishment before resuming execution seamlessly.
* **Why It Saves Quota:** Stops the agent from burning 50,000+ tokens in trial-and-error doom loops on a single test, eliminates 100k+ token per-turn accumulation, and guarantees that autonomous tasks never abort prematurely when quota is available or refreshing.

#### 137. `furry-fursona-art-design`
* **In Simple Terms:** Specialized design and generation pipeline for furry and fursona character art, multi-view turnaround reference sheets (refsheets), digitigrade anatomy, and color palette swatches.
* **When It Kicks In:** Designing fursonas, generating character turnaround reference sheets, formulating model-specific prompts for SDXL/Pony/Midjourney/Flux, rendering exact hex color swatches, or preparing 3D VRChat avatar specs.
* **How It Works:** Encodes anthro species taxonomy (canines, felines, scalies, avians, protogens), digitigrade hock joint anatomy, and paw pad structures into structured profiles (`fursona_generator.py build`), generates negative prompt filters against humanized feet or body fusion, renders clean hex color chips with Pillow, and exports VRChat PhysBones/viseme specifications.
* **Why It Saves Quota:** Eliminates dozens of failed image generations, anatomical distortions, and multi-view body blendings by using model-tailored prompt templates and local palette generation.

#### 138. `android-rom-os-engineering`
* **In Simple Terms:** Operating system engineering and porting suite for building AOSP, LineageOS, and custom Android ROMs on target hardware.
* **When It Kicks In:** Bringing up new Android devices, authoring device trees (`BoardConfig.mk`, `device.mk`), extracting proprietary vendor blobs from factory images, sizing dynamic super partitions, or diagnosing bootloops.
* **How It Works:** Automates device tree scaffolding (`android_rom_tools.py scaffold`), translates raw `avc: denied` SELinux audit logs from dmesg into exact `.te` policy allow rules without resorting to permissive mode, validates dynamic partition storage budgets against `BOARD_SUPER_PARTITION_SIZE`, and lints VINTF compatibility matrices.
* **Why It Saves Quota:** Directly resolves the most common causes of device bootloops, missing HAL symbols, and SELinux denial hangs, avoiding endless multi-hour rebuild cycles.

#### 139. `game-qa-playtest-controller`
* **In Simple Terms:** Programmatic game testing locomotion and dialogue controller that injects real multi-axis character movements (circle-strafing, 360° panoramic sweeps, obstacle wandering, sprint/jump transitions, action cycles) and full NPC character dialogue interaction (`talk.xml` navigation, choices traversal, trade testing) via Linux kernel `/dev/uinput`.
* **When It Kicks In:** Autonomous game QA testing, mod validation, testing NPC conversations and trade menus, continuous stress testing, reproducing physics/clip anomalies, or pairing with `game-screen-telemetry-monitor` to explore game levels and detect render errors.
* **How It Works:** Generates hardware-level relative mouse motion (`REL_X`/`REL_Y`) and DirectInput/RawInput keyboard scan codes via Linux `evdev`/`uinput`, executing smooth orbit maneuvers around landmarks, continuous panoramic sky/ground sweeps with vertical pitch oscillation, frontier wandering with obstacle turnarounds, rapid action cycles (weapon fire/reload/inventory), and character talk sequences (`interact-character`) with automatic dialog dismissal.
* **Why It Saves Quota:** Automates tedious manual game locomotion and UI interaction during testing, eliminates hanging modal dialogs, and reproduces physics clipping or rendering faults predictably in repeatable CLI batches.

#### 140. `computer-vision-deep-learning`
* **In Simple Terms:** Modern neural computer vision and high-performance inference engine for real-time object detection, segmentation, and multi-object tracking.
* **When It Kicks In:** Deploying YOLOv8/v11 models, running Segment Anything 2 (SAM 2) zero-shot masks, exporting models to ONNX/TensorRT with FP16 quantization, or tracking moving objects across video feeds with ByteTrack.
* **How It Works:** Orchestrates ONNX Runtime with CUDA/TensorRT execution providers, runs high-throughput batching, performs non-maximum suppression (NMS) bounding box consolidation, and outputs normalized spatial coordinates $[ymin, xmin, ymax, xmax]$.
* **Why It Saves Quota:** Replaces bulky unoptimized PyTorch scripts with pre-compiled ONNX/TensorRT engines running at 60–140 FPS with minimal GPU memory consumption.

#### 141. `industrial-machine-vision-inspection`
* **In Simple Terms:** Classical, deterministic computer vision for pinhole camera calibration, high-precision dimensional metrology, and surface defect inspection.
* **When It Kicks In:** Calibrating camera lenses and removing optical barrel distortion, measuring physical part dimensions down to sub-pixel accuracy, matching templates with normalized cross-correlation, or detecting scratches and voids on surfaces.
* **How It Works:** Computes camera intrinsic matrices ($f_x, f_y, c_x, c_y$) and distortion vectors ($k_1, k_2$) from checkerboards, applies sub-pixel Canny edge detection and minimum bounding rotated rectangles (`minAreaRect`), and converts pixel units directly to calibrated millimeters.
* **Why It Saves Quota:** Delivers mathematically exact measurements and defect triage without burning millions of tokens on heavy generative vision models.

#### 142. `visual-document-ocr-intelligence`
* **In Simple Terms:** Document AI pipeline that straightens crooked scans, removes background shadows, reads text in 100+ languages, and turns tables into clean Markdown or JSON.
* **When It Kicks In:** Digitizing scanned documents, forms, receipts, and invoices; deskewing crooked page images; binarizing yellowed/degraded documents; or parsing multi-column reading orders.
* **How It Works:** Detects orientation skew via Radon/Hough transforms, applies local adaptive Sauvola binarization to eliminate illumination gradients, orchestrates multi-engine OCR (Tesseract, PaddleOCR, Surya), and reconstructs table grid cell boundaries into Markdown tables.
* **Why It Saves Quota:** Solves OCR failure loops caused by poor image quality before feeding clean text into agent context.

#### 143. `agentic-visual-perception`
* **In Simple Terms:** Autonomous AI agent visual reasoning engine that tiles huge 4K/8K images (SAHI) so tiny buttons don't get lost, and translates natural language into exact screen click coordinates.
* **When It Kicks In:** Navigating high-resolution desktops, locating small UI icons without downsampling blur, grounding instructions (*"click the gear icon"*) into screen pixel coordinates, or confirming UI mutations with visual diffs.
* **How It Works:** Implements Slicing Aided Hyper Inference (SAHI) to slice ultra-high-resolution canvases into overlapping tiles, calculates click centroids $(\bar{x}, \bar{y})$ and normalized bounding boxes, and performs structural similarity (SSIM) frame diffing to verify button clicks.
* **Why It Saves Quota:** Prevents missed clicks and hallucinated UI element coordinates on 2K/4K/Retina displays by inspecting full-resolution tiles rather than blurred downscaled images.

#### 144. `local-model-coprocessor`
* **In Simple Terms:** Local hardware shield that sends boilerplate code, function docstrings, regex, and git commit messages to small local models (Ollama / llama.cpp) running in your GPU VRAM, billing zero tokens to your cloud quota.
* **When It Kicks In:** Generating routine docstrings, crafting conventional commit messages from git diffs, formulating regex patterns, or summarizing verbose compiler error logs.
* **How It Works:** Dispatches HTTP requests to local Ollama or llama.cpp endpoints (`qwen2.5-coder:1.5b`, `llama3.2:3b`), using local NVIDIA Tensor Cores or host RAM to return immediate completions without touching external APIs.
* **Why It Saves Quota:** Keeps 100% of your 5-hour rolling cloud quota free for difficult architectural planning and deep debugging.

#### 145. `local-vector-rag-engine`
* **In Simple Terms:** Local semantic search engine that indexes code and documentation on your NVMe/RAM and feeds only the 2–3 exact relevant snippets into the AI prompt instead of dumping 50 full files.
* **When It Kicks In:** Researching unfamiliar libraries, searching large codebases, or referencing extensive API documentation without exceeding context limits.
* **How It Works:** Chunks project files into overlapping windows, builds a local inverted index with term frequency scoring, and performs sub-10ms semantic searches to retrieve pinpoint code excerpts with exact file and line links.
* **Why It Saves Quota:** Slashes input context consumption by 80%–95%, preventing rapid token accumulation and premature `/compact` warnings.

#### 146. `local-ast-compiler-engine`
* **In Simple Terms:** Multithreaded static code engine that uses all your CPU cores to check syntax, scan class/function symbols, and detect code errors in milliseconds before asking the AI.
* **When It Kicks In:** Verifying syntax after edits, mapping function signatures across large codebases, or auditing AST patterns across dozens of files simultaneously.
* **How It Works:** Automatically saturates all CPU threads (`nproc`) to parse Python AST trees concurrently, surfacing line and column errors instantly without guessing.
* **Why It Saves Quota:** Eliminates multiple trial-and-error reasoning turns and prevents the AI from burning output tokens trying to diagnose simple typos or unclosed brackets.

#### 147. `laptop-performance-profile`
* **In Simple Terms:** Laptop hardware performance and acoustic controller that interoperates with OMEN Space and Linux ACPI/WMI sysfs for quiet overnight runs and max-boost compilation.
* **When It Kicks In:** Tuning fan acoustics when the laptop is muted, running overnight background test batches, boosting CPU for parallel C++/Rust builds, or querying live thermals and clock speeds.
* **How It Works:** Bridges `omen-cli` and system ACPI sysfs interfaces (`/sys/devices/platform/hp-wmi`), setting whisper-quiet fan profiles (`laptop_performance_controller.py sleep-mode`), balanced daily operations, and dynamic max-fan boost profiles (`boost-exec`).
* **Why It Saves Quota:** Keeps host temperatures low to prevent thermal CPU throttling during heavy local compilation and playtesting, eliminating frozen timeouts and build stalls.

#### 148. `humanities-lore-research`
* **In Simple Terms:** Cross-disciplinary research engine for world history, ancient mythology, folklore, and complex worldbuilding that compiles structured entity dossiers and timelines ready for web publishing.
* **When It Kicks In:** Researching historical faction backgrounds, mythological archetypes, comparative folklore, artifact origins, and chronological timelines.
* **How It Works:** Organizes cross-cultural entity files with primary source citations, genealogies, historical periods, and entity relationship graphs formatted for direct web integration.
* **Why It Saves Quota:** Prevents speculative historical and mythological hallucinations through structured, evidence-grounded knowledge dossiers.

#### 149. `creative-web-design-archetypes`
* **In Simple Terms:** Visual design and styling system offering curated aesthetics (Neo-Brutalism, Parchment, Cyberpunk HUD, Academic Journal, Swiss Modernism, Glassmorphism).
* **When It Kicks In:** Designing landing pages, mod wikis, lore archives, interactive calculators, or client dashboards.
* **How It Works:** Provides battle-tested CSS variables, typography pairings, color palettes, and component styling rules tailored to distinct aesthetic archetypes.
* **Why It Saves Quota:** Eliminates generic AI-designed interfaces and iterative CSS rework by applying production-grade design tokens on turn one.

#### 150. `static-site-architecture`
* **In Simple Terms:** Modern Jamstack and static site generator (SSG) architecture covering Astro, VitePress, Starlight, and automated GitHub Pages deployment.
* **When It Kicks In:** Creating documentation hubs, project portfolios, mod databases, or blogs with zero server maintenance.
* **How It Works:** Enforces strict Content Collections schemas with Zod validation, zero-JS baseline performance, and turnkey GitHub Actions CI/CD workflows.
* **Why It Saves Quota:** Generates clean, reproducible static architectures without trial-and-error build errors.

#### 151. `interactive-data-visualization-web`
* **In Simple Terms:** Zero-build, browser-native data visualization generating D3.js force-directed networks, Vis.js timelines, and dynamic stat matrices.
* **When It Kicks In:** Visualizing complex character relationships, faction alliances, technological trees, chronological event timelines, and mod dependency graphs.
* **How It Works:** Emits self-contained HTML/JS visualizations with zoom, pan, interactive node filtering, and search capabilities.
* **Why It Saves Quota:** Generates client-side visualizations that run in any web browser without Node.js build pipelines or external hosting.

#### 152. `task-velocity-governor`
* **In Simple Terms:** Task velocity enforcement and anti-thrashing engine that stops iterative wheel-spinning and breaks 3-strike file churn loops.
* **When It Kicks In:** Fixing bugs, refactoring modules, or executing multi-step porting tasks.
* **How It Works:** Enforces a strict 5-step targeted rule, halts immediately once verification tests pass, and flags repeated edits to the same file before token budgets are exhausted.
* **Why It Saves Quota:** Prevents tasks from taking longer than necessary and stops the AI from endlessly polishing passing code.

#### 153. `first-principles-reasoning`
* **In Simple Terms:** Deep reasoning methodology combining First-Principles decomposition, Chain-of-Verification (CoVe), and Ockham's razor hypothesis ranking.
* **When It Kicks In:** Diagnosing elusive bugs, engine crashes, memory leaks, or resolving architectural conflicts.
* **How It Works:** Strips assumptions, decomposes problems into fundamental axioms, generates falsification questions, and ranks hypotheses by simplicity and testability.
* **Why It Saves Quota:** Eliminates confirmation bias and speculative code churn, solving root causes on the first targeted attempt.

#### 154. `game-exploratory-fuzzing`
* **In Simple Terms:** Automated game QA and fuzz testing that uses evolutionary action mutations and novelty search to explore unvisited game states.
* **When It Kicks In:** Stress testing game physics, finding collision boundary holes, discovering memory leaks, or stress-testing AI behaviors.
* **How It Works:** Mutates input sequences (locomotion vectors, weapon toggles, jump/crouch timing) based on screen novelty scores, saving crashing seeds for instant reproduction.
* **Why It Saves Quota:** Finds game crashes and rendering glitches autonomously without requiring hours of manual human playtesting.

#### 155. `self-healing-test-automation`
* **In Simple Terms:** Resilient test automation suite that auto-repairs broken UI selectors, falls back to OCR, and eliminates test flakiness.
* **When It Kicks In:** Web, desktop, and game UI testing where IDs, coordinates, or element hierarchies shift between versions.
* **How It Works:** Combines accessibility trees, visual OCR, and multi-vector semantic locators to locate elements even after layout redesigns.
* **Why It Saves Quota:** Prevents test suites from breaking every time a minor UI element or button text changes.

#### 156. `coverage-guided-mutation-testing`
* **In Simple Terms:** Test suite quality auditor that injects deliberate AST mutations (flipping conditionals, altering operators) to verify if tests actually catch bugs.
* **When It Kicks In:** Hardening critical parsers, game logic, security algorithms, and CI test suites across Lua, Python, C++, and Rust.
* **How It Works:** Injects AST mutants, measures mutant kill rates, and synthesizes missing boundary test cases to plug coverage gaps.
* **Why It Saves Quota:** Ensures tests are truly reliable before shipping code, preventing costly production regressions.

#### 157. `laptop-performance-profile`
* **In Simple Terms:** Thermal and acoustic hardware governor that switches laptop fan curves, CPU power limits, and GPU profiles for whisper-quiet runs or turbo builds.
* **When It Kicks In:** Running long overnight tasks, muted coding sessions, or running heavy parallel compilations (`-j$(nproc)`).
* **How It Works:** Interfaces with OMEN Space daemon, ACPI/WMI sysfs, and power-profiles-daemon to enforce whisper-quiet acoustics or max boost.
* **Why It Saves Quota:** Prevents thermal throttling, hardware degradation, and fan acoustic noise during extended unattended agent runs.

#### 158. `game-dialogue-ui-localization`
* **In Simple Terms:** Specialized game dialogue translation, string table repair, and conversation UI layout engine (S.T.A.L.K.E.R. & RPGs).
* **When It Kicks In:** Fixing dialogue UI text clipping, missing string IDs, CP1251/CP1250/UTF-8 mojibake, or multi-language localization (FIGS, CJK, Slavic, BiDi, Turkish).
* **How It Works:** Validates string tables, cross-references dialogue trees, enforces `complex_mode="1"` multiline wrapping, and calculates visual pixel width across fullwidth CJK glyphs.
* **Why It Saves Quota:** Eliminates game crashes (`xrXMLParser.cpp`), dialogue freezing dead-ends, and unreadable character sets on turn one.

#### 159. `game-weather-lighting-fx`
* **In Simple Terms:** Dynamic game weather cycle tuner, HDR tonemapping calibrator, and sun glare/light-bleed suppressor.
* **When It Kicks In:** When sun shafts (god rays) bleed through solid terrain/geometry, looking at the sun is blindingly overblown, or cutscenes flash unrendered frames.
* **How It Works:** Audits weather LTX files, clamps overblown `sun_color` RGB values, balances `r2_sun_lumscale` and bloom thresholds, and aligns shadow map bias (`r2_sun_bias`).
* **Why It Saves Quota:** Eliminates iterative guessing and testing of lighting CVars by providing calibrated mathematical limits for deferred rendering engines.

#### 160. `game-performance-overlay-telemetry`
* **In Simple Terms:** In-game HUD performance metrics and telemetry profiling suite (MangoHud, DXVK HUD, PresentMon).
* **When It Kicks In:** Profiling FPS, frametimes, 1% lows, GPU/VRAM/RAM saturation, thermals, and power draw during gameplay and engine port QA.
* **How It Works:** Automatically configures MangoHud and DXVK overlays anchored to `top-right` to prevent collision with in-game minimaps and combat HUDs.
* **Why It Saves Quota:** Provides instant visual evidence of frame stutter, VRAM thrashing, and CPU draw-call bottlenecks without requiring external profilers.

#### 161. `game-weapon-ballistics-mechanics`
* **In Simple Terms:** Weapon configuration, ballistics physics, firing cycles, explosive blast radii, underbarrel launchers, and anti-jamming mechanics.
* **When It Kicks In:** Configuring rapid-fire weapons, underbarrel grenade launchers, explosive ordnance, no-reload ammo hooks, and infinite durability.
* **How It Works:** Calibrates `fire_modes = -1`, animation loop states, blast radius vs smoke particle effects (`blast`, `frags`), and zeroes out misfire degradation.
* **Why It Saves Quota:** Prevents weapon animation locks, misfire duds, and weapon script crashes during gameplay testing.

#### 162. `game-qol-gameplay-scripting`
* **In Simple Terms:** Autonomous quality-of-life gameplay scripting: proximity radar scanning, intelligent auto-loot for quest/ammo/health items, and faction-filtered defense.
* **When It Kicks In:** Adding proximity radar auto-loot for quest items, vacuuming needed ammo/medkits, spawning homing counter-measures against enemies, and sprint anomaly repulsion.
* **How It Works:** Implements spatial distance scanning algorithms, faction community goodwill checks (protecting loners/allies), and anomaly immunity hooks.
* **Why It Saves Quota:** Speeds up game testing runs by automating inventory management, protecting key NPCs from premature death, and eliminating tedious backtracking.

#### 163. `linux-game-window-input-capture`
* **In Simple Terms:** Linux game window containment, mouse grab/confinement, focus isolation, and dual-monitor multitasking under Wine/Proton and Gamescope.
* **When It Kicks In:** When the mouse drifts out of the game viewport, the cursor gets trapped on Alt-Tab, or the running game steals focus from the terminal during paired development.
* **How It Works:** Enforces Gamescope sandboxing (`--grab --mangoapp`), configures Wine cursor clipping registry keys, and enables borderless windowed mode.
* **Why It Saves Quota:** Prevents frozen terminals and lost input focus, allowing simultaneous game execution and terminal interaction without disruption.

#### 164. `game-autonomous-navigation-ai`
* **In Simple Terms:** Autonomous character navigation, level vertex/waypoint graph mapping, route recording/replay, and reactive combat aimbot steering.
* **When It Kicks In:** Autonomous playtesting, stress walkthroughs, traversing large game levels hands-free, or testing NPC combat encounters.
* **How It Works:** Navigates via level vertex graphs, injects smoothed mouse-look and sprint vectors via `/dev/uinput`, tracks collision stalls, and blacklists geometry traps.
* **Why It Saves Quota:** Replaces hours of manual human walkthrough testing with autonomous, self-improving path navigation that avoids getting stuck.

#### 165. `game-self-improving-qa-pipeline`
* **In Simple Terms:** Closed-loop self-improving game QA test harness: automated loading dismissal, 88% stall watchdog, crash log harvesting, and countdown timers.
* **When It Kicks In:** Running unattended soak tests, automated regression runs, dismissing 'Press any key to play' screens, and trapping level loading deadlocks.
* **How It Works:** Injects keystrokes when loading hits 100%, traps 88% loading freezes, auto-terminates Notepad crash dialogs, and logs failure coordinates to a central regression database.
* **Why It Saves Quota:** Completely eliminates hung CI/playtest processes and automatically builds regression test cases for candidate bug fixes.

#### 166. `game-companion-pet-ai`
* **In Simple Terms:** Custom companion & pet NPC architecture: state machine behaviors (follow, dynamic speed, guide), god mode status, dynamic lighting, and combat attacks.
* **When It Kicks In:** Implementing immortal pet companions (like cats/dogs), providing player guidance in complex levels, and adding contextual combat support.
* **How It Works:** Implements tether distance following, dynamic speed matching, dynamic torch light emission in dark areas, and homing projectile attacks with vocalization triggers.
* **Why It Saves Quota:** Provides production-ready companion state machines and Blender asset pipelines, avoiding complex trial-and-error AI scripting.

#### 167. `game-dynamic-stress-orchestrator`
* **In Simple Terms:** In-game stress testing and entity orchestration: collision-safe radial wave spawning, multi-faction air/mutant clashes, and performance saturation profiling.
* **When It Kicks In:** Stress testing game engines with massive mutant swarms, testing AI squad combat logic, and profiling minimum 1% low frame pacing.
* **How It Works:** Uses circular ring distribution to prevent physics repulsion explosions (anti-falling under map), orchestrates helicopter vs mutant battles, and cleans up entities dynamically.
* **Why It Saves Quota:** Pushes game engines to their absolute limits safely without corrupting save states or crashing physics solvers.

#### 168. `game-memory-scanner`
* **In Simple Terms:** Dynamic virtual memory inspection, value scanning, candidate filtering, and pointer discovery for PC games on Linux and Wine/Proton.
* **When It Kicks In:** Developing game trainers, finding dynamic entity offsets (health, ammo, coordinates, stamina, currency), scanning AOB byte signatures with wildcards, and freezing live memory addresses.
* **How It Works:** Inspects `/proc/<pid>/maps` across writable regions, performs rapid 4MB chunk pattern scans, iteratively filters candidates across gameplay state changes (`increased`, `decreased`, `changed`, exact), and runs continuous background freeze loops.
* **Why It Saves Quota:** Pinpoints exact memory offsets in real time on the live process, eliminating trial-and-error code patching and dozens of speculative debug turns.

#### 169. `game-dll-proxy-generator`
* **In Simple Terms:** Automated scaffold generator and build pipeline for internal proxy DLLs (DLL hijacking / wrapping).
* **When It Kicks In:** Injecting internal game trainers, MinHook detours, custom Dear ImGui overlays, or binary patches into Windows and Steam Proton / Wine games without external injector tools.
* **How It Works:** Generates complete C++ export forwarding tables for `dinput8.dll`, `version.dll`, `dxgi.dll`, and `winmm.dll`, dynamic system loader fallback, background trainer threads (`DllMain`), modern CMake configs, and one-click MinGW cross-compile scripts.
* **Why It Saves Quota:** Completely automates tedious C++ DLL proxy scaffolding and linker export tables with 100% crash-free stability.

#### 170. `agy-codebase-init`
* **In Simple Terms:** Autonomous repository onboarding and architecture intake for Antigravity (complete parity with Claude Code `/init`).
* **When It Kicks In:** Running `agy` on a new or unconfigured repository, setting up build/test/lint conventions, or scaffolding `GEMINI.md` and `CLAUDE.md`.
* **How It Works:** Recursively inspects project root files (`package.json`, `Cargo.toml`, `pyproject.toml`, `CMakeLists.txt`), discovers entry points and test suites, and generates standardized instructions without manual prompt writing.
* **Why It Saves Quota:** Eliminates 20,000–50,000 tokens of exploratory thrashing on the first turn of any new project.

#### 171. `agy-cli-doctor`
* **In Simple Terms:** System diagnostics, configuration audit, and SQLite database health checker for Antigravity CLI (parity with `claude doctor`).
* **When It Kicks In:** Diagnosing `agy` runtime errors, inspecting `settings.json` permissions whitelist, verifying SQLite database integrity, or clearing stale locks.
* **How It Works:** Runs non-destructive integrity checks on recent session databases in `~/.gemini/antigravity-cli/conversations/`, verifies model API endpoints, and clears stale statusline lock files.
* **Why It Saves Quota:** Prevents failed tool runs and broken session loops by catching environment defects before invoking the LLM.

#### 172. `agy-context-telemetry`
* **In Simple Terms:** Deep context window utilization, step-by-step token trajectory, and dollar savings inspector for Antigravity CLI (parity with `claude /context` & `/cost`).
* **When It Kicks In:** Monitoring token consumption during complex multi-step refactors, auditing prompt cache efficiency, or timing `/compact` milestones.
* **How It Works:** Analyzes active conversation transcripts (`transcript.jsonl`) to compute uncached input, cached prefix tokens, output tokens, per-step hit rates, and estimated dollar savings from the 90% prompt cache discount.
* **Why It Saves Quota:** Pinpoints exact token leakage and warns when context capacity reaches 50% so you compact before rate limits are hit.

#### 173. `argon-thinking-governor`
* **In Simple Terms:** Chain-of-thought (CoT) and internal reasoning token governor for Gemini 4 Argon.
* **When It Kicks In:** Calling routine tools (`view_file`, `replace_file_content`, `run_command`), editing code files, or running multi-turn build/test cycles on Argon.
* **How It Works:** Enforces zero-monologue tool execution (prohibits reciting file lines or speculating about file contents before tool calls) and implements the hybrid "Argon Brain, Flash Hands" dispatch protocol.
* **Why It Saves Quota:** Eliminates 3,000 to 12,000 internal thinking tokens per turn on routine tasks, reducing overall Argon session token burn by 75% to 85%.

#### 174. `yolo-autonomous-watchdog`
* **In Simple Terms:** Autonomous execution watchdog and quota protector for unattended YOLO sessions (`claude-yolo`, `agy-yolo`).
* **When It Kicks In:** Running long, unattended autonomous loops without human prompts.
* **How It Works:** Enforces hard output limits (`head -n 40` on discovery queries), traps 3-strike file oscillation loops, and mandates 12-turn state checkpointing.
* **Why It Saves Quota:** Prevents catastrophic token flooding and halts runaway retry loops.

#### 175. `headless-test-condenser`
* **In Simple Terms:** Test runner output condenser and noise filter for CLI test suites (`pytest`, `cargo test`, `vitest`, `ctest`).
* **When It Kicks In:** Running automated test suites during debugging and TDD cycles.
* **How It Works:** Standardizes low-token flags (`pytest -q --tb=short`, `cargo test -q`, `ctest --output-on-failure`) and isolates re-execution solely to failing targets.
* **Why It Saves Quota:** Strips 95% of passing green test output, saving thousands of context tokens per test run.

#### 176. `dynamic-model-downshifter`
* **In Simple Terms:** Autonomous multi-tier model downshifting for CLI sessions ("Frontier Brain, Fast Hands").
* **When It Kicks In:** Executing mechanical shell tasks, file moves, git commits, or directory checks after architectural plans are finalized.
* **How It Works:** Routes mechanical operations to lightweight models (Flash/Haiku), reserving expensive frontier reasoning (Argon/Opus) exclusively for architectural design and root-cause debugging.
* **Why It Saves Quota:** Prevents wasting scarce hourly rate limits on simple bash tasks.

#### 177. `gemini-flash-cache-aligner`
* **In Simple Terms:** Prompt cache optimizer for Gemini 3.8 Flash.
* **When It Kicks In:** Starting or structuring multi-turn sessions on Gemini Flash.
* **How It Works:** Enforces the 4,096-token minimum prefix floor to unlock the 90% prompt cache discount, ensures character-level prefix invariance, and isolates dynamic variables to prompt tails.
* **Why It Saves Quota:** Guarantees >90% prompt cache discounts across multi-turn sessions.

#### 178. `flash-context-compactor`
* **In Simple Terms:** Context window inflation governor for Gemini Flash.
* **When It Kicks In:** Working in large codebases where sessions risk accumulating hundreds of thousands of tokens.
* **How It Works:** Replaces 500+ line file reads with targeted $\le 50$-line slices, uses AST interface skeletons instead of full bodies, and enforces compaction below 100k tokens.
* **Why It Saves Quota:** Eliminates the 10% residual un-discounted token billing penalty on bloated context windows.

#### 179. `gemini-5h-quota-governor`
* **In Simple Terms:** Real-time telemetry governor for Gemini 3.8 Flash rolling 5-hour quota windows.
* **When It Kicks In:** Monitoring burn rate against reset timestamps during intensive agent workflows.
* **How It Works:** Tracks burn velocity, dynamically throttles verbose tool outputs in the yellow/orange zones, and enforces safe checkpointing and sleep cycles when nearing reserve limits.
* **Why It Saves Quota:** Eliminates unexpected rate-limit lockouts during continuous runs.

#### 180. `claude-opus-plan-sonnet-exec`
* **In Simple Terms:** Three-tier operational routing architecture for Anthropic Claude ("Opus Plan, Sonnet Code, Haiku Hands").
* **When It Kicks In:** Running complex feature implementations or refactors in Claude Code CLI.
* **How It Works:** Confines Opus strictly to Tier 1 architectural design and `/plan` formulation, dropping to Sonnet for code execution and Haiku for mechanical bash operations.
* **Why It Saves Quota:** Stretches Opus availability across the entire week rather than exhausting it in a morning.

#### 181. `claude-thinking-budget-governor`
* **In Simple Terms:** Extended thinking token budget governor for Claude 3.7+ Sonnet and Opus.
* **When It Kicks In:** Using Claude models with hybrid reasoning / extended thinking enabled.
* **How It Works:** Clamps internal reasoning tokens based on task complexity (0 tokens for routine tool execution, $\le 1,500$ for standard coding, up to 6,000 for deep concurrency debugging).
* **Why It Saves Quota:** Saves 3,000 to 10,000 internal thinking tokens per turn on routine tool operations.

#### 182. `claude-context-rot-shield`
* **In Simple Terms:** Context window degradation protector and 1,024-token prompt cache aligner for Claude Code.
* **When It Kicks In:** Context window grows beyond 80,000 tokens during long sessions.
* **How It Works:** Detects attention dilution, stages state to `.agents/memory/activeContext.md`, triggers clean `/compact` boundaries, and aligns static prompts to Anthropic's 1,024-token cache blocks.
* **Why It Saves Quota:** Restores sub-2s response latency and maintains 90% prompt caching discounts.

#### 183. `claude-fable-engine-governor`
* **In Simple Terms:** Autonomous context and quota governor for Anthropic's 1M-token Claude Fable model during large game engine ports.
* **When It Kicks In:** Large-scale C++ game engine migrations (e.g. S.T.A.L.K.E.R. SoC to 64-bit OGSR).
* **How It Works:** Enforces 1M-token prompt cache pinning, whole-engine C++ AST skeletonization (<60k tokens), and surgical 35-line crash log extraction.
* **Why It Saves Quota:** Allows a 1M-token model to reason over entire engine architectures with 90% caching discounts.

#### 184. `cpp-64bit-engine-port-sanitizer`
* **In Simple Terms:** Detects and repairs 64-bit bitness porting defects in C++ game engines.
* **When It Kicks In:** Migrating legacy 32-bit game engines to 64-bit architectures.
* **How It Works:** Audits pointer-to-integer truncations (`uintptr_t`), fixes `#pragma pack(1)` struct padding memory corruption, harmonizes 64-bit calling conventions, and checks vtable alignments.
* **Why It Saves Quota:** Eliminates mysterious heap corruption crashes that cause dozens of failed debugging turns.

#### 185. `stalker-level-ai-graph-triage`
* **In Simple Terms:** Diagnoses and repairs S.T.A.L.K.E.R. and X-Ray/OGSR level AI navmesh and graph defects.
* **When It Kicks In:** Encountering `! Cannot find level vertex` CTDs, broken level changers, or NPC pathfinding deadlocks.
* **How It Works:** Audits `level.ai`, `level.graph`, and `game.graph` point connectivity, cross-referencing ACDC decompiled `all.spawn` entries with level geometry bounds.
* **Why It Saves Quota:** Replaces trial-and-error coordinate guessing with exact mathematical navmesh clamping.

#### 186. `stalker-luajit-ffi-migration`
* **In Simple Terms:** Manages Lua script migration to 64-bit LuaJIT and FFI in OGSR Engine.
* **When It Kicks In:** Porting legacy SoC Lua scripts to modern 64-bit LuaJIT runtimes.
* **How It Works:** Audits deprecated Luabind C++ exports, traps silent nil-pointer dereferences in callbacks, and enforces safe FFI pointer lifetime management.
* **Why It Saves Quota:** Prevents silent script deadlocks and unhandled native C++ thunk crashes.

#### 187. `xray-dx11-shader-modernization`
* **In Simple Terms:** Modernizes legacy DirectX 9 Shader Model 3.0 shaders to DirectX 11 SM 5.0 in OGSR.
* **When It Kicks In:** Migrating visual mods with custom HLSL shaders to DX11 deferred rendering.
* **How It Works:** Decouples texture/sampler registers, enforces strict 16-byte `cbuffer` boundaries, and fixes normal map Y-inversion and blown-out HDR bloom.
* **Why It Saves Quota:** Eliminates cryptic `E_FAIL` shader compilation errors and rendering blackouts.

#### 188. `cross-cli-session-handoff`
* **In Simple Terms:** Seamless zero-context-loss session handoff protocol between Antigravity CLI, Claude Code CLI, and Cursor IDE.
* **When It Kicks In:** Switching between AI coding environments to balance quota or leverage specific model strengths.
* **How It Works:** Exports structured `.agents/handoff.json` packets containing active git diffs, verified milestones, blockers, and next steps for instant resumption in < 300 tokens.
* **Why It Saves Quota:** Eliminates 40,000+ tokens of conversational catch-up when switching CLIs.

#### 189. `legacy-codebase-cartographer`
* **In Simple Terms:** Maps legacy game engine architectures and prunes dead code before porting.
* **When It Kicks In:** Starting a migration on massive legacy codebases with years of accumulated dead code.
* **How It Works:** Constructs reverse-call dependency graphs from core entry points (`WinMain`, `xrGame.dll`) and generates an `omit_manifest.txt` for unreferenced translation units.
* **Why It Saves Quota:** Prunes 25% to 40% of unnecessary files from the port, saving massive context tokens and build times.

#### 190. `agent-error-recovery-sentinel`
* **In Simple Terms:** Autonomous watchdog and runtime error recovery supervisor for unattended playtests.
* **When It Kicks In:** Running autonomous game tests under Wine/Proton that risk freezing on modal dialogs.
* **How It Works:** Intercepts 0% CPU freezes (>90s), dismisses BugTrap/Notepad crash windows, clears stale `.lock`/socket files, and safely auto-resumes test loops.
* **Why It Saves Quota:** Prevents autonomous test sessions from hanging indefinitely in silent failure states.

#### 191. `game-mod-release-packager`
* **In Simple Terms:** Automated game mod release packaging, archive compression, and distribution pipeline.
* **When It Kicks In:** Preparing final mod or engine distributions for public release.
* **How It Works:** Strips debug symbols (`objcopy --strip-debug`), packs game VFS archives (`.xdb`, `.pack`) via ZoneForge with zstd, and generates cryptographic `SHA256SUMS.txt` manifests.
* **Why It Saves Quota:** Eliminates manual release errors and streamlines the build-to-ship pipeline.

#### 192. `blender-high-to-low-baking`
* **In Simple Terms:** Automated high-to-low poly normal and AO texture baking pipeline in Blender (`bpy`).
* **When It Kicks In:** Creating AAA game-ready 3D assets that require film-quality surface detail at low-poly performance.
* **How It Works:** Headlessly aligns high-poly sculpts and low-poly cages, bakes tangent-space normal maps, ambient occlusion, and cavity maps, and enforces sharp edge UV seam alignment.
* **Why It Saves Quota:** Produces cinematic game-ready visual fidelity with zero manual baking mistakes.

#### 193. `game-engine-3d-budget-profiler`
* **In Simple Terms:** Game engine 3D performance budget enforcer, automated LOD generator, and collision hull builder.
* **When It Kicks In:** Verifying that 3D models meet engine triangle budgets and draw-call constraints.
* **How It Works:** Audits polycounts against engine thresholds (FPS viewmodel, NPC, prop), automatically generates LOD0–LOD3 decimation cascades, and builds simplified `UCX_` convex collision hulls.
* **Why It Saves Quota:** Prevents game engine frame drops and eliminates repetitive manual LOD creation.

#### 194. `blender-pbr-texture-packager`
* **In Simple Terms:** PBR texture channel packing (ORM) and normal map orientation standardizer.
* **When It Kicks In:** Packaging materials for game engines (Unreal, Godot, Unity, X-Ray/OGSR).
* **How It Works:** Packs Ambient Occlusion (R), Roughness (G), and Metallic (B) into a single texture via Pillow, standardizes texel density ($px/cm$), and handles DirectX ($Y-$) vs OpenGL ($Y+$) normal green inversion.
* **Why It Saves Quota:** Reduces GPU texture memory footprint by 66% and prevents draw-call stalls.

#### 195. `character-creature-anatomy-modeling`
* **In Simple Terms:** Character, creature, and animal 3D modeling and deformation topology guide in Blender.
* **When It Kicks In:** Sculpting and modeling humans, animals, quadrupeds, or fantasy creatures.
* **How It Works:** Establishes anatomical proportion landmarks (digitigrade hocks, scapula loops), enforces deformation-friendly concentric quad loops around bending joints/eyes/mouths, and automates shrinkwrap retopology setups via `bpy`.
* **Why It Saves Quota:** Eliminates non-deforming topology and pinching artifacts before rigging begins.

#### 196. `rigging-weight-painting-pipeline`
* **In Simple Terms:** Character, creature, and animal skeletal rigging and automated skinning pipeline in Blender.
* **When It Kicks In:** Rigging organic characters and quadrupeds for game engine animation.
* **How It Works:** Constructs standardized bone hierarchies, enforces game engine bone limits ($\le 64$ mobile, $\le 128$ desktop), clamps vertex influences to 4, and normalizes vertex weights automatically via `bpy`.
* **Why It Saves Quota:** Eliminates joint collapsing and candy-wrapper twisting without hours of manual weight painting.

#### 197. `blender-headless-token-shield`
* **In Simple Terms:** Quota and context token protector for 3D modeling and Blender workflows.
* **When It Kicks In:** Authoring or executing 3D geometry manipulation scripts with AI assistants.
* **How It Works:** Strictly prohibits generating raw vertex/polygon coordinate dumps in chat, enforces headless Python script execution with compact 3-line CLI telemetry, and gates visual renders to major milestones.
* **Why It Saves Quota:** Saves 15,000 to 40,000 tokens per turn by eliminating 3D coordinate chat bloat.

#### 198. `claude-opus-conciseness-enforcer`
* **In Simple Terms:** Extreme output conciseness enforcer, BLUF formatter, and hard token cap governor for Claude Opus.
* **When It Kicks In:** Interacting with Claude Opus for architectural planning and root-cause analysis.
* **How It Works:** Enforces a hard output cap of $\le 200$ tokens per response, eliminates conversational preambles/pleasantries, and bans code block re-pasting in chat (confines code strictly to tool calls).
* **Why It Saves Quota:** Slashes expensive Opus output token consumption by up to 75%.

#### 199. `fable-virtual-context-manager`
* **In Simple Terms:** Virtualized context paging and hierarchical indexing for Claude Fable (1M-token context).
* **When It Kicks In:** Multi-day, long-horizon engine migration or whole-codebase engineering tasks on Claude Fable.
* **How It Works:** Maintains a master symbol graph on disk (`.agents/fable_index.json`), dynamically paging only active 30k-token subsystem slices into working memory per turn, and preserves exact character invariance for 90% prompt caching.
* **Why It Saves Quota:** Reduces turn input billing from 600k+ tokens down to ~30k tokens while retaining full architectural coherence.

#### 200. `argon-effort-auto-calibrator`
* **In Simple Terms:** Dynamic reasoning effort calibrator for Gemini 4 Argon (`--effort low/medium/high`).
* **When It Kicks In:** Executing multi-turn tasks on Gemini 4 Argon.
* **How It Works:** Dynamically scales thinking budgets: drops to `--effort low` (<300 tokens) for routine tool calls, file diffs, and git commits; escalates to medium for unit testing; reserves high for unsolved crash triage and `/plan` drafting.
* **Why It Saves Quota:** Eliminates 4,000 to 12,000 internal thinking tokens per turn on routine mechanical steps, cutting Argon session burn by 85%.

#### 201. `universal-token-containment-protocol`
* **In Simple Terms:** Universal cross-model and cross-domain token containment protocol across all 217 skills.
* **When It Kicks In:** Running any engineering task across 3D modeling, reverse engineering, web design, game modding, and test suites.
* **How It Works:** Enforces strict domain rules: caps disassembly dumps to 30 lines, offloads HTML/docs to files/artifacts, mandates surgical chunk diffs, and enforces quiet flags (`pytest -q`, `cargo test -q`).
* **Why It Saves Quota:** Eliminates chat transcript pollution and ensures all large data blocks exist exclusively in tools and disk files.

#### 202. `model-optimal-state-serializer`
* **In Simple Terms:** Tokenizer-native structured state serialization for Claude, Gemini, and Cursor.
* **When It Kicks In:** Saving session state, writing `.agents/memory/activeContext.*`, staging cross-CLI handoffs, or preparing for `/compact`.
* **How It Works:** Serializes memory into tokenizer-optimal layouts: concise XML-KV tags for Claude BPE, flat pipe-delimited TSV tables for Gemini SentencePiece, and compact symbol coordinates (`<file>#L<line>:<sig>`).
* **Why It Saves Quota:** Slashes state hydration token costs by 60%–80% (compressing 500-token verbose JSON blocks into <130 tokens) without losing structural fidelity.

#### 203. `multi-model-cache-harmonizer`
* **In Simple Terms:** Static prefix anchoring and cache boundary alignment engine across Claude, Gemini, OpenAI, and Grok.
* **When It Kicks In:** Formatting system prompts, tools, and multi-turn conversational payloads.
* **How It Works:** Enforces the Three-Zone Hierarchy: aligns frozen static system prefixes to 1,024-token boundaries (Claude/OpenAI) and $\ge 4,096$ tokens (Gemini), isolating ephemeral timestamps and volatile outputs strictly to trailing suffixes.
* **Why It Saves Quota:** Guarantees 90%–95% cache read discounts across interactive turns and stops accidental prompt-cache busts.

#### 204. `git-diff-token-compressor`
* **In Simple Terms:** Zero-context hunk and coordinate patch compressor for Git workflows.
* **When It Kicks In:** Inspecting uncommitted working diffs, code reviews, PR audits, and staging cross-CLI handoffs.
* **How It Works:** Enforces `git diff -U0` and compact coordinate patches (`<file>#L<num>:+added|-removed`), stripping redundant context lines, file mode headers, and commit hashes.
* **Why It Saves Quota:** Slashes diff token consumption by 70%–85% during iterative bug fixes and reviews.

#### 205. `polyglot-ast-interface-pruner`
* **In Simple Terms:** Polyglot AST interface pruner and header skeletonizer across C++, C#, Rust, Python, and Lua.
* **When It Kicks In:** Onboarding onto new repositories, inspecting dependencies, and planning large refactors.
* **How It Works:** Strips implementation bodies, docstrings, and private variables, generating ultra-dense 1-line type signatures.
* **Why It Saves Quota:** Slashes codebase ingestion context by 85%–90% compared to ingesting raw source files.

#### 206. `local-preflight-syntax-gate`
* **In Simple Terms:** Zero-token host-side pre-flight syntax and linter verification gate.
* **When It Kicks In:** Directly after modifying code and before triggering heavy builds or test suites.
* **How It Works:** Runs lightweight native compilers (`luac -p`, `ruff check`, `cargo check`, `clang-format`) in 15ms on the host CPU, repairing syntax errors locally before returning to the model.
* **Why It Saves Quota:** Saves 15,000 to 40,000 expensive frontier model thinking tokens per intercepted syntax typo.

#### 207. `disassembly-token-redactor`
* **In Simple Terms:** Reverse engineering disassembly token redactor and CFG basic-block condenser.
* **When It Kicks In:** Inspecting binaries with `objdump`, `readelf`, `gdb`, or `rizin`.
* **How It Works:** Strips raw hex opcode columns, instruction padding, and linear NOP sleds, retaining only symbolic basic-block branches and call sites.
* **Why It Saves Quota:** Slashes binary disassembly token consumption by 75%–80%.

#### 208. `game-config-delta-extractor`
* **In Simple Terms:** Game configuration delta extractor and inheritance pruner.
* **When It Kicks In:** Auditing or editing S.T.A.L.K.E.R. LTX, Godot TSCN/TRES, and game YAML files.
* **How It Works:** Computes inheritance deltas against parent sections (`[child:parent]`), displaying only overridden key-value pairs.
* **Why It Saves Quota:** Slashes multi-thousand-line weapon/entity config context by 80%–85%.

#### 209. `network-packet-stream-condenser`
* **In Simple Terms:** Network packet stream and PCAP trace condenser.
* **When It Kicks In:** Analyzing network traffic, game packet captures, and API transport logs with `tshark`.
* **How It Works:** Flattens hierarchical dissection trees into single-line TSV telemetry tuples (`#PKT|ID|SRC->DST|PROTO|FLAGS|LEN`).
* **Why It Saves Quota:** Slashes network protocol engineering prompt tokens by 85%–90%.

#### 210. `sql-schema-query-condenser`
* **In Simple Terms:** SQL relational schema and query plan condenser.
* **When It Kicks In:** Inspecting database schemas or profiling SQL queries with `EXPLAIN QUERY PLAN`.
* **How It Works:** Serializes verbose DDL migrations into compact type-bracket notation (`tbl[id:INT*, user:STR!(idx)]`) and flattens query trees into operator pipelines.
* **Why It Saves Quota:** Slashes database context footprint by 65%–75%.

#### 211. `cross-model-switch-pruner`
* **In Simple Terms:** Pre-switch state compaction and history virtualization engine when switching models (Sonnet to Fable, Opus, or Gemini).
* **When It Kicks In:** Mid-session model switches (`/model fable-5.1`) or cross-model handoffs.
* **How It Works:** Intercepts model switching to snapshot diffs, stage model-optimal state (<300 tokens), and run pre-switch compaction or launch zero-history fresh handoff sessions.
* **Why It Saves Quota:** Slashes model switch re-read billing by 98% (reducing 80k–150k token un-cached re-reads down to ~1.5k compacted tokens).

#### 212. `compiler-error-cascade-isolator`
* **In Simple Terms:** C++ template and compiler error cascade isolator.
* **When It Kicks In:** Compiling C++ engines with GCC, Clang, or MSVC.
* **How It Works:** Intercepts raw build outputs, isolates Error #1, and strips hundreds of lines of secondary template instantiation stacks, outputting a 5-line diagnostic tuple.
* **Why It Saves Quota:** Slashes compiler diagnostic context by 90%–95%, saving 10k–30k tokens per build cycle.

#### 213. `xray-crash-symbol-resolver`
* **In Simple Terms:** Translates Wine/Proton crash offsets (`xrGame.dll+0x3b4a12`) into exact source lines via host CPU symbols.
* **When It Kicks In:** Investigating S.T.A.L.K.E.R. / X-Ray engine crashes under Wine/Proton.
* **How It Works:** Runs `addr2line` or `rizin` locally on the host in 15ms to resolve crash offsets directly to source lines (`alife_simulator.cpp#L184`).
* **Why It Saves Quota:** Eliminates 25k–40k tokens of blind multi-file code exploration.

#### 214. `xray-macro-boilerplate-condenser`
* **In Simple Terms:** Strips legacy X-Ray macros, Luabind exports, and allocator boilerplate.
* **When It Kicks In:** Ingesting legacy X-Ray C++ headers and script export bindings.
* **How It Works:** Pre-processes C++ source to condense verbose GSC macros (`IC`, `DECLARE_SCRIPT_...`, chained Luabind defs) into clean functional signatures.
* **Why It Saves Quota:** Reduces C++ file ingestion context by 70%–80%.

#### 215. `stalker-spawn-entity-indexer`
* **In Simple Terms:** Local JSON/SQLite indexer and query tool for unpacked S.T.A.L.K.E.R. `all.spawn` files.
* **When It Kicks In:** Looking up quest entities, smart terrains, level changers, and waypoints.
* **How It Works:** Scans unpacked spawn archives once on the host and retrieves exact 15-line entity slices in milliseconds.
* **Why It Saves Quota:** Saves 35k–50k tokens versus reading raw 40,000-line spawn files.

#### 216. `fable-atomic-diff-sequencer`
* **In Simple Terms:** Multi-file refactor execution coordinator for Claude Fable 5.1.
* **When It Kicks In:** Executing large multi-file engine refactors with Fable's 128k output window.
* **How It Works:** Decomposes whole-subsystem rewrites into dependency-ordered surgical chunk manifests, validating each chunk locally with pre-flight gates.
* **Why It Saves Quota:** Slashes output token waste by 80% and eliminates tool timeouts and catastrophic rollback loops.

#### 217. `session-experience-harvester`
* **In Simple Terms:** Mines completed agent session transcripts, tracking cumulative multi-billion token savings and distilling solved gotchas.
* **When It Kicks In:** Completing long-running sessions, auditing lifetime token savings, or onboarding new sessions onto complex codebases.
* **How It Works:** Scans `.jsonl` session logs, maintains a persistent global ledger (`~/.cli_power_setup/token_ledger.json`) tracking billions of cached tokens, and distills verified CTD solutions into `.agents/memory/learnings.md`.
* **Why It Saves Quota:** Allows new sessions to hydrate thousands of turns of verified engine fixes in <350 tokens, permanently preventing trial-and-error re-discovery.

#### 218. `shell-output-token-guard`
* **In Simple Terms:** Puts an automatic safety guard on terminal commands so noisy scripts don't accidentally dump 5,000 lines into your chat history.
* **When It Kicks In:** Running commands that could have large outputs (`grep`, `find`, `git log`, `ls -R`, builds).
* **How It Works:** Wraps commands with `token-guard`, showing the first 25 lines, omitting repetitive mid-sections, and showing the final 5 lines with an exact token savings count.
* **Why It Saves Quota:** Prevents accidental 20,000–50,000 token terminal dumps that instantly blow through your context window.

#### 219. `selective-context-ingestor`
* **In Simple Terms:** Forces the AI to read only the exact 20 lines it needs instead of blindly reading 800-line files.
* **When It Kicks In:** Whenever the AI inspects a class, investigates a function, or reads a file to understand code.
* **How It Works:** Uses `slice-reader` to extract AST class/method skeletons or targeted $\pm 15$ line windows around symbols, completely stripping out irrelevant implementation bodies.
* **Why It Saves Quota:** Slashes file reading token consumption by 90%–95%, keeping conversations fast and lightweight.

---

## 📊 Real-Time Dual-CLI Quota & Statusline Monitors

The suite includes **dedicated, tailor-made statusline monitors** for both CLIs:

### 1. Claude Code CLI Dedicated Monitor (`claude-statusline`)
Installed to `~/.local/bin/claude-statusline` and configured in `~/.claude/settings.json`. Intercepts Claude Code's live `stdin` telemetry stream to render model, rate limits, weekly reset countdowns, visual context gauge with token counts and compact advisories, prompt cache token savings, session cost, and git worktree:
```text
⚡ Claude [Sonnet 3.7 • Turbo] | 5h: 86% (reset 00:40) | Wk: 96% (reset in 40m) | 🧠 Ctx: [█░░░░░] 22% (44k) | 💾 Saved: 5.2M tok (92% cache) | 💲 $0.06 +45/-12
```
* **Prompt Cache Token Telemetry:** Parses the active session's transcript to compute exact cached tokens (`cache_read_input_tokens`) and cache hit rate, showing your 90% prompt cache discount in real time.
* **Visual Context Gauge with Token Counts:** Dynamic progress bar showing real-time token volume (e.g. `22% (44k)`). When context crosses the 60% threshold, it automatically switches to `(128k ⚠️ Run /compact)`.
* **Turbo Mode Tag:** Confirms at a glance (`• Turbo`) when low-effort thinking caps are active to save reasoning tokens.
* **Dual Rolling Quota & Reset Timers:** Real-time remaining percentages for both 5-hour and 7-day rolling windows, with relative countdowns (e.g. `(reset in 40m)`) when resets are imminent.
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
* **Universal Lifetime Fallback:** When active session cache savings are clean, seamlessly falls back to `~/.cli_power_setup/token_ledger.json` to render the persistent lifetime token benchmark (`1.54B tok`).
* **Asynchronous & Non-Blocking Quota:** Queries `agy -p /usage` and caches the result in `/tmp/agy_quota_cache.txt` with a 2-minute TTL.
* **Zero CLI Lag:** Subprocesses are detached with PID lockfile protection (`/tmp/agy_quota_refresh.lock`), guaranteeing instantaneous prompt rendering (<2ms).

### 3. Universal Lifetime Token Ledger (`~/.cli_power_setup/token_ledger.json`)
The suite maintains a **universal, multi-environment token ledger** that survives session compaction, model switches, and terminal restarts:
* **Cross-CLI Universal Architecture:** Both `claude-statusline` and `agy-quota-statusline` read from this single source of truth. It records sessions from Google Antigravity, Claude Code CLI, and Cursor Agent.
* **Continual Automated Accumulation:** As autonomous tasks complete, [`session-experience-harvester`](#217-session-experience-harvester) mines `.jsonl` transcripts, appending newly cached, uncached, and output tokens to the running lifetime total.
* **Repository Benchmark Backup:** Seeded via `config/token_ledger.json` in the git repository, allowing cloned installations to immediately inherit verified historical benchmarks (e.g. 1.535B tokens saved at 99.5% cache hit rate).

### 4. Quota Governance & Uninterrupted Execution (`goal_governor.py`)
To prevent autonomous tasks, test runners, or overnight builds from abandoning progress prematurely:
* **Never Quit on Available Quota:** Quota numbers (e.g. `5h: 86%`, `Wk: 96%`) represent available headroom. Agents are strictly forbidden from halting when quota is available (> safe reserve limits).
* **5-Hour Exhaustion Wait-for-Refresh:** If rolling 5-hour quota hits safe reserve during an autonomous `/goal` or playtest run, the governor stages active memory to `.agents/memory/activeContext.md`, sleeps until the recorded reset timestamp passes, verifies quota replenishment, and seamlessly resumes execution.
* **Smart Checkpoint at 25% Weekly Quota:** When weekly quota nears 25% remaining, the governor automatically snapshots all uncommitted git diffs, working branch, and active hypothesis context into `.agents/checkpoints/` before proceeding safely.

---

## 🛡️ Ultimate Hardening Protocols: Fable 5.1 & Zero-Token Host Pre-Flight

To maximize efficiency and slash token costs when operating heavy-duty frontier models like **Claude Fable 5.1** or **Gemini 4 Argon**, the suite enforces automated host-CPU pre-flighting and strict context containment:

### 1. Claude Fable 5.1 Hardened Governance Protocol
Claude Fable's 1-million-token context window can easily lead to costly token re-reads if whole repositories are ingested. The suite enforces:
* **Subsystem Slice Virtualization:** Replaces multi-thousand-line source trees with 30k-token interface skeletons generated via [`fable_slice_extractor.py`](file:///home/ericparsley/Documents/GitHub/cli-power-setup/config/skills/fable-virtual-context-manager/scripts/fable_slice_extractor.py).
* **Atomic 30-Line Diff Chunking:** Restricts all code changes to surgical `replace_file_content` chunks $\le$ 30 lines, preventing runaway output token burn and tool timeouts.
* **Thinking Token Clamping:** Caps reasoning effort on routine file edits, syntax checks, and git operations, reserving deep thinking budgets strictly for unsolved crash dumps and pointer alignment proofs.
* **Hard 80k-Token Compaction Boundary:** Automatically stages active state to `.agents/memory/activeContext.md` and triggers `/compact` at 50%–60% context, locking in the 90% prompt cache discount indefinitely.
* **Tokenizer-Native Serialization:** Serializes memory and handoff states in flat XML-KV tags for Claude BPE (saving ~65% tokens) and Pipe-TSV for Gemini SentencePiece (saving ~75% tokens).

### 2. The Zero-Token Host Pre-flight Arsenal (<30ms Local Execution)
Instead of forcing expensive LLMs to read raw, noisy files into their context windows, 6 specialized Python utilities process data directly on the host CPU in milliseconds with **0 API tokens burned**:

| Pre-flight Utility | Associated Skill | What It Does on Host CPU | Token Savings |
| :--- | :--- | :--- | :--- |
| **`fable_slice_extractor.py`** | `fable-virtual-context-manager` | Strips function bodies, extracting AST class hierarchies and Lua export signatures | **~97% input token reduction** |
| **`slice-reader`** | `selective-context-ingestor` | Extracts line-numbered AST skeletons or focused $\pm 15$ line windows around symbols | **~92%–95% file reading reduction** |
| **`token-guard`** | `shell-output-token-guard` | Enforces a 30-line ceiling on commands (`grep`, `find`, `git log`), truncating intermediate noise | **Prevents 10k–50k stdout floods** |
| **`compiler_cascade_isolator.py`** | `compiler-error-cascade-isolator` | Filters compiler template error cascades, isolating the #1 root-cause failure coordinate | **~95% compiler log reduction** |
| **`xray_crash_resolver.py`** | `xray-crash-symbol-resolver` | Scans 15,000-line engine crash logs, isolating fatal assertions and demangling RVAs | **~99% crash log reduction** |
| **`config_delta_extractor.py`** | `game-config-delta-extractor` | Compares child config sections with parents, extracting only overridden keys | **~95% config token reduction** |

---

## 📱 Android 2D & 3D Game & App Development Workflows

The repository provides a dedicated toolchain and automation suite for high-performance 2D and 3D Android development across C++/Vulkan NDK, Godot, Unity, and Jetpack Compose:

### 1. The 3 Primary Android Game & App Workflows

1. **High-End 3D Native Game Architecture (C++ / Vulkan NDK):**
   * **Skills:** `android-ndk-jni-engineering` + `vulkan-gpu-compute` + `game-texture-material-pipeline` + `android-perf-battery-profiling`.
   * **Focus:** Direct zero-copy `DirectByteBuffer` passing across JNI, native Vulkan swapchain rendering, ASTC texture compression, Oboe low-latency audio, and `renderdoccmd` GPU frame inspection over ADB.

2. **Cross-Platform Mobile Engine Pipeline (Godot / Unity 2D & 3D):**
   * **Skills:** `godot-game-dev` (or `unity-game-dev`) + `game-physics-collision-pipeline` + `android-device-automation` + `headless-game-ci-automation`.
   * **Focus:** Headless APK/AAB build automation, CanvasLayer multi-DPI touch scaling, fixed-timestep physics decoupling, and automated APK sideloading.

3. **Modern Reactive 2D Games & UI Applications (Jetpack Compose / Canvas):**
   * **Skills:** `android-compose-ui-ux` + `android-architecture-jetpack` + `android-testing-ci-cd-security`.
   * **Focus:** Hardware-accelerated Compose Canvas drawing, MVI/StateFlow state management, edge-to-edge window insets, R8/ProGuard shrinking, and Keystore hardware encryption.

### 2. Android Development Runner (`android-dev-runner`)
Installed to `~/.local/bin/android-dev-runner`:
* **Environment Diagnostics:** `android-dev-runner doctor` audits Android SDK paths, NDK compilers, CMake, Ninja, Vulkan drivers, and ADB device state.
* **Low-Latency Screen Mirroring:** `android-dev-runner mirror` launches 120fps `scrcpy` display streaming with stay-awake flags for hands-free live playtesting.
* **Frame Rate & Jank Triage:** `android-dev-runner jank --package <pkg>` pulls live VSYNC frame timing histograms directly over ADB.

---

## 🚀 Antigravity Launchers, Voice Dictation Pill & Hardware Offload Savers

### 1. Antigravity YOLO (`agy-yolo` / `yolo`) & Turbo (`agy-turbo`)
* **`agy-yolo` (`yolo`):** Launches Antigravity in hands-free autonomous mode (`--dangerously-skip-permissions --mode auto`) with the dynamic repo-aware cheat sheet banner (`Argon•High+Flash` swarm routing).
* **`agy-turbo`:** Launches Antigravity with `--model gemini-3.8-flash-low --effort low --dangerously-skip-permissions --mode auto` for instantaneous, low-quota execution on routine tasks.

### 2. Floating Voice Dictation Pill (`agy-mic-button`)
Automatically launched alongside `agy` (and automatically closed when all `agy` terminals exit):
* **Controls:** `[⋮⋮ AGY | 🎙️ Talk | ⏎ Send | ⚡Auto | 📌Pin | ×]`
* **Smooth XWayland Drag & Pin (`📌`/`📍`):** Left-drag `⋮⋮ AGY` (or right-drag anywhere) to position; left-click `📌` to lock/pin position on top of the terminal (`🔒 AGY`); right-click `📌` to snap directly to the active terminal's top-right corner and pin.
* **Natural-Language Spoken Command Routing:** Speak *"Set a goal to..."* ($\rightarrow$ `/goal` via `autonomous-goal-governor`), *"Make a plan to..."* ($\rightarrow$ `/plan`), *"Use boost to..."* ($\rightarrow$ `/boost`), or *"Clamshell 3D mode"* ($\rightarrow$ `laptop-perf clamshell-3d`).

### 3. Local 32-Thread CPU + RTX 5060 CUDA 13.4 Math Solver (`game-math-solver`)
Eliminates cloud reasoning token burn on 3D coordinate/quaternion basis transforms (`UE5 <-> X-Ray/OGSR <-> Blender`), ODE `ERP`/`CFM` physics step rescaling, external ballistics trajectories, X-Ray `level.ai` 5-byte `NodePosition` quantization, and SymPy symbolic proofs (`1,000,000` 3D vertices transformed in `16.8 ms` on RTX 5060 CUDA 13.4 with `0` cloud tokens).

---

## 💡 Plain-English Guide & Everyday Command Quick Reference

### Everyday Command Quick Reference

| Command | What It Does | When to Use It |
| :--- | :--- | :--- |
| **`agy-yolo`** / **`yolo`** | Launches Antigravity in hands-free YOLO mode (`--dangerously-skip-permissions --mode auto`) | Autonomous multi-step engineering, 3D asset porting, and overnight `/goal` runs. |
| **`agy-turbo`** | Launches Antigravity with Gemini Flash + low effort | Your fast, quota-saving daily driver for quick edits, syncs, and lookups. |
| **`agy`** | Launches standard Antigravity CLI | Standard interactive sessions with Flash-to-Argon escalation. |
| **`agy-mic-button`** | Launches/manages the floating `[🎙️ Talk \| ⏎ Send \| ⚡Auto \| 📌Pin]` voice pill (`--pin`, `--unpin`, `--stop`) | Click-to-talk voice dictation in `agy` without touching keyboard shortcuts. |
| **`game-math-solver`** | Local 32-thread CPU + RTX 5060 CUDA 13.4 math solver (`coord`, `ode`, `ballistics`, `ai-node`, `prove`, `hw-bench`) | Instant, zero-quota 3D coordinate conversions, ODE physics rescaling, and SymPy proofs. |
| **`laptop-perf`** | Thermal & acoustic governor (`clamshell-3d`, `sleep-mode`, `wake-mode`, `boost-exec`, `status`) | Run `laptop-perf clamshell-3d` to close the laptop lid while 3D rendering/baking continues safely. |
| **`skill-optimize`** | Harmonizes all 300 skills, cross-links synergies, and updates `skill_ecosystem_graph.json` | Automatically run by `skill-evolve` (or manually) to keep all skills working together. |
| **`agy-cheatsheet`** (`cs`) | Scans all GitHub repos and prints live model + effort + hardware recommendations | Anytime you switch repos or want optimal quota/hardware routing advice. |
| **`/compact`** | Compresses long chat history into fresh memory | Whenever the statusline context countdown (`🧹`) reaches the 250k Argon compaction gate. |
| **`game-texture-editor`** | Procedural normal gen, RNM blend, seamless tiles & DDS | Texture repairs, sharpening, alpha bleeding, and bump map generation. |
| **`game-dialogue-tool`** | S.T.A.L.K.E.R. & RPG conversation UI repair, string cross-ref & encoding | When fixing dialogue clipping, missing string IDs, or mojibake in game text. |
| **`game-test-watchdog`** | Autonomous QA supervisor detecting freezes and crashes | Wrap any long-running test to prevent hung processes. |
| **`stalker-playtest-runner`**| Hands-free game QA with input injection & OCR dialog triage | Automated S.T.A.L.K.E.R. / OGSR engine playtesting. |
| **`weather-lighting-tuner`** | Audits weather LTX, clamps sun glare, and balances tonemapping | When sun shafts bleed through world geometry or bloom is blinding. |
| **`mangohud-configurator`** | Generates MangoHud performance HUD profiles (FPS, 1% lows, VRAM) | When benchmarking games or positioning telemetry away from minimaps. |
| **`game-window-helper`** | Sandboxes game in Gamescope, locks mouse pointer, and stops focus stealing | When playtesting games without losing cursor control or terminal focus. |
| **`nav-graph-recorder`** | Records/smoothes routes, avoids invisible walls, and logs collision traps | Autonomous game character navigation and self-improving path routing. |
| **`self-improving-qa`** | Closed-loop QA, dismisses 'Press any key', watchdog for 88% stalls & timers | Unattended playtest runs and automated regression failure logging. |
| **`game-memory-scanner`** | Inspects, scans, filters, and freezes live game memory | Developing cheat trainers, finding dynamic pointers, and scanning AOB signatures. |
| **`game-dll-proxy-gen`** | Generates proxy DLL scaffolds (dinput8, dxgi, version) with export forwarding | Injecting internal trainers, MinHook detours, and ImGui overlays into games. |
| **`token-guard`** | Enforces 30-line terminal ceiling on command executions | Wrap commands (`token-guard <cmd>`) to prevent runaway stdout context floods. |
| **`slice-reader`** | Extracts AST skeletons or $\pm 15$ line slices around symbols | When reading code to view only the target function or class definition. |
| **`android-dev-runner`** | Android 2D/3D development doctor, scrcpy mirror & jank analyzer | Diagnosing Android toolchains, launching 120fps live mirroring, or auditing frame drops. |
| **`cursor-rules-sync`** | Converts all skills to Cursor `.mdc` rules and syncs `.cursorrules` | After modifying skills or when syncing Cursor configuration. |
| **`skills-audit-update --audit`** | Audits health across Antigravity and Cursor | Periodically or when diagnosing missing tools/scripts. |
| **`skills-audit-update --sync`** | Synchronizes all 300 skills across Antigravity and Cursor | After adding or updating any skill in the repository. |
| **`./install.sh --all`** | Re-synchronizes and backs up all 302 skills across Antigravity and Cursor | Whenever you pull updates from the `cli-power-setup` repository. |

---

### 5. Cursor IDE & Multi-Model Integration (xAI Grok, Claude, OpenAI, DeepSeek)

This suite is fully integrated with **Cursor IDE**, supporting all major frontier and open-weight models available in Cursor's model picker:

```
┌─────────────────────────────────────────────────────────────┐
│                       Cursor IDE                            │
├───────────────┬───────────────┬──────────────┬──────────────┤
│   xAI Grok    │Anthropic Claude│ OpenAI o1/4o │ DeepSeek R1  │ Gemini 2.0  │ Meta Llama 3.3│ Qwen 2.5 Coder│
│  (Grok 4.7)   │  (Sonnet 3.7) │  (o3-mini)   │  (V3 / R1)   │ (Flash/Pro) │ (70B / 405B)  │  (32B / 72B)  │
└───────┬───────┴───────┬───────┴──────┬───────┴──────┬───────┴──────┬──────┴───────┬───────┴───────┬───────┘
        ▼               ▼              ▼              ▼              ▼              ▼               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Core Discipline: .cursor/rules/000-cursor-global-discipline.mdc                                    │
│  Universal Model Adaptation Matrix: .cursor/rules/001-multi-model-optimization.mdc                  │
│  217 Modular Skill Rules (.cursor/rules/*.mdc with semantic activation)                             │
│  Unified Root Fallback: ~/.cursorrules                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Universal Model Matrix:
1. **Universal Rules (`alwaysApply: true`):**
   * **`000-cursor-global-discipline.mdc`:** Injected into every prompt. Enforces Output Token Economy (zero fluff, high-density checklists, surgical diffs), S.T.A.L.K.E.R. EE modding integrity, and hardware-aware execution.
   * **`001-multi-model-optimization.mdc`:** Automatically calibrates model behavior based on which engine is selected:
     * **xAI Grok Frontier (`grok-4.7`, `grok-4.7-fast`, `grok-4.5`, `grok-2`):** Multi-hour agentic harness tuning, 500k context governance, reasoning levels (`low` to `xhigh`), zero banter, anti-hallucination LTX/C++ verification.
     * **Anthropic Claude (`claude-3-7-sonnet`, `claude-3-5-sonnet`, `claude-3-5-haiku`):** Prompt cache prefix stabilization (>90% savings), hybrid reasoning alignment, and surgical diff formatting.
     * **OpenAI Reasoning & Standard (`o1`, `o3-mini`, `gpt-4o`, `gpt-4o-mini`):** Silent internal reasoning for o1/o3; verbosity containment and surgical edits for GPT-4o.
     * **Google Gemini (`gemini-2.0-flash`, `gemini-2.0-flash-thinking`, `gemini-1.5-pro`):** Multimodal image/texture grounding, ultra-low latency Flash iterations, 1M+ context handling with AST skeletons.
     * **DeepSeek (`deepseek-r1`, `deepseek-v3`):** English-only code generation, 3-strike circuit breaker on failed debug loops, and strict memory safety checks.
     * **Meta Llama (`llama-3.3-70b`, `llama-3.1-405b/8b`):** Concrete search/replace anchor blocks; context budgeting for 8B/70B local models via RAG.
     * **Qwen & Alibaba (`qwen-2.5-coder-32b/72b`):** Indentation preservation (spaces vs tabs), premier C++/Lua syntax accuracy.
     * **Mistral (`mistral-large-2`, `codestral-2501`):** Fast fill-in-the-middle completions and POSIX/C++ standards compliance.
2. **Modular Skill Rules (`alwaysApply: false`):**
   * All 302 skills are compiled into individual `.cursor/rules/<skill-name>.mdc` files with rich semantic YAML frontmatter descriptions.
   * Cursor's semantic rule matcher automatically pulls the right skill into context only when your prompt or open files require it—**zero prompt bloat and zero token waste**.


3. **Unified Global Fallback (`~/.cursorrules`):**
   * Deployed directly to `$HOME/.cursorrules` and project roots so any folder opened in Cursor inherits this entire suite immediately.

---

<!-- AUTO-SYNC-CATALOG:START -->
## 🔄 Auto-Synchronized Skill & CLI Inventory (302 Total Active Skills)

### Latest CLI Utilities (`bin/` -> `~/.local/bin/`)
| CLI Tool | Purpose |
| :--- | :--- |
| **`agy-mic-button`** | Floating XWayland voice dictation pill (`[🎙️ Talk | ⏎ Send | ⚡Auto | 📌Pin]`) with drag memory, terminal snap-pin, and auto-close on `agy` exit. |
| **`game-math-solver`** | Zero-quota 32-thread AVX-512 CPU + RTX 5060 CUDA 13.4 GPU math solver (`coord`, `ode`, `ballistics`, `ai-node`, `prove`, `hw-bench`). |
| **`laptop-perf`** | Hardware acoustic & thermal governor (`clamshell-3d` lid-closed 3D render lock, `sleep-mode`, `wake-mode`, `boost-exec`). |
| **`agy-cheatsheet` (`cs`)** | Dynamic repo-aware model, reasoning effort, and hardware offload cheat sheet + live statusline recommender (`~/Documents/GitHub`). |
| **`skill-evolve` & `skill-optimize`** | Closed-loop runtime skill scaffolder, Voyager script promoter, `<50ms` hot-patcher, and automatic ecosystem mesh optimizer (`skill_ecosystem_graph.json`). |
| **`repo-auto-sync`** | Autonomous git repo puller, `.gitignore` hardener, `README.md` updater, milestone committer, and 32-repo fleet manager. |
| **`steam-mod-scanner`** | Fingerprints installed Steam games (`/mnt/games/SteamLibrary`) by engine & archive format and maps to modding skills. |
| **`silhouette-iou-profiler`** | Extracts 32-slice mathematical width contours & hex palettes from 2D drawings and verifies 3D render Silhouette IoU. |
| **`local-coprocessor` / `local-rag` / `local-ast-compiler`** | Zero-quota local CPU/GPU/RAM offload engines for AST syntax checks, BM25/vector RAG, and local LLM summarization. |

### Recently Evolved & SOTA Skills (76 Indexed Automatically)
| Skill Name | Description |
| :--- | :--- |
| **`amd-igpu-nvidia-dgpu-hybrid-offload`** | Dual-GPU workload splitter for AMD Radeon 610M iGPU (/dev/dri/renderD129, RADV Vulkan + VA-API VCN + 30GB shared DDR5 RAM) and NVIDIA GeForce RTX 5060 dGPU (/dev/dri/renderD128, 8GB GDDR7 CUDA/OptiX). Prevents background agent tasks from stealing game VRAM. |
| **`android-game-ndk-vulkan`** | Native Android game development using C++20, Android NDK (GameActivity / NativeActivity), Vulkan mobile rendering, touch gesture queues, and pipeline cache serialization. |
| **`android-mobile-3d-asset-optimizer`** | Android NDK, Vulkan, and OpenGL ES 3.2 mobile 3D asset optimization in Blender 5.2+. Enforces Adreno/Mali Tile-Based Deferred Rendering (TBDR) triangle budgets, <=4 bone skinning weights, fp16 vertex quantization, and ASTC/KTX2 BasisU texture compression. |
| **`android-monetization-iap-ads`** | Google Play Billing (BillingClient 7.x), In-App Purchases, server-side receipt cryptographic verification, Play Integrity API, and AdMob/AppLovin mediation. |
| **`argon-adversarial-verification-gate`** | Harnesses Gemini 4 Argon's deep reasoning capacity for formal adversarial self-critique, boundary-condition proofing, and confirmation-bias elimination prior to declaring tasks complete. |
| **`argon-ast-syntax-gate`** | Pre-flight local compiler and AST syntax verification gate for Gemini 4 Argon. Catches syntax, typing, and parsing errors locally in milliseconds before committing changes. |
| **`argon-atomic-diff-sequencer`** | Enforces Claude-grade atomic chunk editing on Gemini 4 Argon. Restricts all code changes to surgical <= 30-line replacements, eliminating full-file rewrites and accidental regressions. |
| **`argon-context-cache-guard`** | Anchors and stabilizes Gemini 4 Argon context to ensure sessions cross and maintain the 32,768-token cache threshold for maximum 95% KV prompt caching discounts. |
| **`argon-deep-memory-allocator-sanitizer`** | Mathematical 64-bit pointer, struct padding, and memory alignment sanitizer for Gemini 4 Argon. Eliminates pointer truncation and alignment faults in legacy C++ game engine ports. |
| **`argon-hierarchical-worktree-isolator`** | Sandboxes concurrent subagent file modifications into isolated git worktrees, preventing file lock collisions and allowing atomic integration by Argon. |
| **`argon-long-context-retrieval-anchor`** | Enforces boundary-edge semantic anchoring across Gemini 4 Argon's 1M-token context window to prevent attention dilution and lost-in-the-middle degradation during massive engineering tasks. |
| **`argon-long-haul-context-compaction-gate`** | Monitors context consumption during long-running Argon YOLO porting runs, triggering atomic milestone compaction at 250k tokens to maintain sub-second latency and 95% cache discounts. |
| **`argon-multimodal-vision-grounding`** | Directs Gemini 4 Argon's native multimodal vision capabilities toward game screen telemetry, UI layout audits, rendering artifact triage, and graphical glitch diagnosis. |
| **`argon-self-contained-autonomous-driver`** | Comprehensive single-driver engineering workflow for Gemini 4 Argon. Unifies planning, asset transpilation, C++ precision refactoring, compilation, and autonomous QA playtesting in a single agent. |
| **`argon-sentencepiece-serializer`** | Formats tabular data, state serializations, and symbol skeletons to optimize token density under Google's SentencePiece tokenizer used by Gemini 4 Argon. |
| **`argon-structured-json-schema-enforcer`** | Leverages Gemini 4 Argon's native constrained decoding to emit deterministic, schema-compliant JSON payloads for automated CLI pipelines and test harnesses. |
| **`argon-subagent-dispatch-routing`** | Implements the 'Argon Brain, Flash Hands' subagent swarm dispatch pattern to offload high-volume read, search, and execution tasks to Gemini Flash while conserving Argon quota. |
| **`argon-subagent-lifecycle-governor`** | Prevents zombie hangs, infinite loops, and interactive prompt blocking in Gemini subagents with deterministic timeouts and automated process cleanup. |
| **`argon-subagent-payload-compressor`** | Enforces high-density structured return envelopes on Gemini subagent messages, eliminating conversational fluff and reducing parent context inflation by up to 80%. |
| **`argon-tool-calling-densifier`** | Enforces compact parallel tool invocation and parameter density on Gemini 4 Argon to minimize output token generation costs and round-trip latency. |
| **`argon-yolo-quota-pacing-watchdog`** | Telemetry governor that paces Gemini 4 Argon autonomous YOLO execution, preventing 5-hour quota exhaustion by staging state and safely sleeping until window refresh. |
| **`autogen-adversarial-redteam-critic`** | Emulates Microsoft AutoGen multi-persona red-teaming. Executes an internal Devil's Advocate audit to aggressively attack candidate fixes before committing code. |
| **`autonomous-3d-reference-researcher`** | Autonomous online anatomical, mechanical blueprint, and Blender bpy technique researcher. Searches the web for real-world proportions, skeletal joint ratios, and shader recipes before/during 3D modeling and crystallizes findings into skills via skill-evolve. |
| **`autonomous-audio-sfx-web-researcher`** | Autonomously searches open web audio repositories (Wikimedia Commons, Internet Archive) for real CC0/public-domain sound effects, foley, animal vocalizations, weapons, and ambient audio; ranks candidates acoustically by Signal-to-Noise Ratio (SNR), spectral centroid, and clipping; slices the cleanest audio event in /dev/shm; and exports mastered WAV/OGG with GSC X-Ray v3 binary headers. |
| **`autonomous-git-repo-sync-governor`** | Autonomous git repository synchronization, upstream pull/rebase, milestone auto-commit, large-binary/secret pre-commit filtering, and multi-repo fleet updates across ~/Documents/GitHub during long sessions and general development. |
| **`autonomous-skill-ecosystem-optimizer`** | Closed-loop auto-optimizing skill ecosystem harmonizer (skill-optimize). Automatically invoked by skill-evolve whenever skills are created or updated to cross-link related skills, enforce Windows/Linux & hardware offload rules, prune dead references, compact tokens, and rebuild the capability graph. |
| **`bethesda-creation-engine-nif-modding`** | Modding pipeline for Bethesda Creation Engine & Gamebryo games owned in Steam library (Morrowind, Oblivion, Skyrim/SE, Fallout 3, Fallout New Vegas, Fallout 4, Starfield). Covers ESM/ESP/ESL binary plugin records, BSA/BA2 archives, NIF 3D meshes, Papyrus scripting, and SKSE/F4SE/NVSE C++ DLLs. |
| **`blender-3d-printing-cad-manifold-prep`** | General 3D engineering in Blender 5.2+ for 3D printing (FDM/SLA), CNC machining, watertight manifold repair, wall thickness solidification, mechanical snap-fit clearance tolerances (0.15-0.25mm), overhang analysis, and precision STL/3MF export. |
| **`blender-animation-nla-retargeting-vat`** | Headless Blender 5.2+ animation authoring, NLA action baking, skeletal retargeting, cyclic loop quaternion continuity, S.T.A.L.K.E.R. .skl/.omf motion export, and Vertex Animation Textures (VAT) for GPU crowd/physics rendering. |
| **`blender-gaussian-splatting-photogrammetry-cleanup`** | Converts raw 3D Gaussian Splatting (.ply), NeRF, photogrammetry scans, and AI-generated 3D meshes (Tripo3D/Hunyuan3D/Trellis) into clean, delighted, quad-retopologized, game-ready PBR assets in headless Blender 5.2+. |
| **`blender-geometry-nodes-procedural-worlds`** | Headless Blender 5.2+ Geometry Nodes (bpy.types.GeometryNodeTree) procedural worldbuilding, spline generators (roads, pipes, cables, fences), modular building assembly, Poisson-disk biome foliage scattering, and Realize Instances game export. |
| **`blender-hard-surface-cad-weapons-props`** | Non-destructive hard-surface 3D modeling in Blender 5.2+ for weapons, firearms, vehicles, mechs, and sci-fi props using Boolean + Bevel + Weighted Normals, MikkTSpace tangents, and FPS kinematic weapon bone rigging. |
| **`blender-sdf-organic-remeshing`** | Eliminates the 'cartoony balloon-animal' look in procedural Blender 5.x organic modeling using Voxel SDF Remeshing, Volume-Preserving Laplacian Smoothing, Anatomical Plane Flattening, and QuadriFlow Retopology. |
| **`blender-uv-udim-lightmap-architect`** | Automated headless UV unwrapping in Blender 5.2+ (SLIM Minimum Stretch, Angle-Based, Conformal), texel density normalization, Trim Sheets, UDIM multi-tile arrays (1001-1008), and non-overlapping UV2 Lightmap generation. |
| **`chatgpt-o1-hypothesis-tree`** | Emulates ChatGPT o1/o3-mini Tree-of-Thought deliberation on Gemini 4 Argon. Branches into 3 competing hypotheses, explores execution paths, and backtracks upon contradiction. |
| **`codestral-fill-in-the-middle`** | Emulates Mistral Codestral Fill-in-the-Middle (FIM) surgical infilling. Anchors prefix and suffix code boundaries to generate exact bridge logic with zero indentation drift or hallucination. |
| **`cohere-provenance-grounding-ledger`** | Emulates Cohere Command R+ grounded provenance citations. Traces every game config parameter and C++ modification to its exact vanilla baseline coordinate to eliminate hallucinated parameters. |
| **`concept-art-sketch-to-3d-sculptor`** | Converts 2D drawn images, character concept art, and reference sketches into high-detail 3D models in Blender 5.2+ using OpenCV/Pillow contour slice profiling, silhouette-locked 3D lofting, iterative Silhouette IoU verification, and camera-projected displacement/texture baking. |
| **`creature-animal-bioacoustic-audio`** | Realistic animal and creature vocalization engineering (cats, dogs, wolves, mutants, wildlife) combining real CC0 acoustic field recordings, Klatt/Rosenberg mammalian glottal-formant vocal tract DSP synthesis (scipy.signal), and automatic GSC X-Ray / OGSR v3 24-byte binary Ogg comment header injection. |
| **`cross-agent-context-deduplicator`** | Eliminates redundant transcript ingestion and context pollution between Argon orchestrators and Flash subagents by clamping sync payloads to strict 15-line symbol diff abstracts. |
| **`cross-agent-git-rebase-guard`** | Automated git worktree synchronization, non-interactive rebasing, and conflict-free merging between concurrent AI agent feature branches. |
| **`cross-agent-hot-reload-watcher`** | Real-time file system observer using inotifywait to trigger instant hot-reloading of modified scripts, configs, and textures in running game instances. |
| **`cross-engine-3d-import-export-bridge`** | Unified Blender 5.2+ to Game Engine 3D export matrix covering Unreal Engine 5 (Nanite/UCX), Godot 4.x (.glb/-col/-loop), Unity (Humanoid/bake_space_transform), S.T.A.L.K.E.R. X-Ray/OGSR (.ogf/.dm), and Three.js/WebGPU (Meshopt/Draco/KTX2). |
| **`cross-engine-shader-transpiler`** | Universal shader authoring and transpilation using Slang and SPIRV-Cross, converting single-source shaders to Vulkan SPIR-V, DX12 HLSL, Metal MSL, and OpenGL GLSL. |
| **`cuda-numpy-batch-texture-dsp-processor`** | Saturates all 32 host CPU threads (ProcessPoolExecutor), 30 GB RAM, and NVIDIA CUDA/NumPy SIMD vectorization for massively parallel batch processing of .dds textures, normal map swizzling, alpha-coverage mipmaps, and .ogg audio files. |
| **`cursor-inline-diff-lens`** | Emulates Cursor IDE ghost-text and surgical multi-line inline diff previews in Antigravity CLI, giving instant visual clarity on code additions and deletions. |
| **`deepseek-r1-math-verification`** | Emulates DeepSeek-R1 chain-of-verification and self-correcting mathematical proofs in Gemini 4 Argon reasoning tokens for memory layouts, offsets, and timing. |
| **`devin-environment-self-healer`** | Emulates Cognition Devin autonomous environment self-healing. Automatically diagnoses missing host dependencies, dynamic libraries (.so), and compiler toolchains on Linux (CachyOS/Arch). |
| **`dual-engine-quota-balancer`** | Dynamic telemetry coordination across Gemini 4 Argon, Gemini 3.8 Flash subagents, and local CPU/GPU offloads, balancing task allocation to guarantee uninterrupted execution without hitting rolling quota limits. |
| **`dxvk-vkd3d-proton-pipeline-profiler`** | Diagnoses and eliminates DXVK and VKD3D-Proton shader compilation stutter, descriptor heap stalls, and VRAM staging bottlenecks for DX11/DX12 games running on Linux. |
| **`dynamic-repo-model-cheatsheet`** | Dynamic terminal cheat sheet (agy-cheatsheet / cs) and live statusline recommender that scans ~/Documents/GitHub repositories, uncommitted diffs, recent commits, and error states to recommend the optimal Model + Reasoning Effort + Local Hardware Offload. |
| **`game-asset-streaming-lod-governor`** | Real-time asynchronous asset streaming, distance-based LOD hierarchies (LOD0-LOD3), virtual texturing, and LRU memory cache eviction. |
| **`game-audio-ogg-gsc-encoder`** | Converts and encodes game audio to Ogg Vorbis while injecting and preserving proprietary GSC binary engine comment chunks (min/max distance, volume, AI perception) required by S.T.A.L.K.E.R. engines. |
| **`grok-realtime-telemetry-scout`** | Emulates xAI Grok real-time live search on Gemini 4 Argon. Scouts bleeding-edge git commits, pull requests, issue trackers, and package feeds for undocumented Linux and game fixes. |
| **`headless-gameplay-testing-bot`** | Autonomous cross-platform gameplay testing bot, synthetic input replay (uinput, adb input), regression fuzzing, and telemetry invariant assertions. |
| **`linux-perf-flamegraph-bottleneck-triage`** | Hardware performance counter profiling (perf record/report) and folded stack Flamegraph bottleneck triage for native Linux and Wine/Proton games. Pinpoints exact C++ functions causing severe FPS drops in seconds without blind bisecting. |
| **`local-gpu-vision-ocr-preprocessor`** | Pre-processes game screenshots, desktop captures, and 3D renders locally on host CPU/GPU using Pillow/NumPy perceptual frame-diffing and local Tesseract OCR, cutting cloud multimodal vision token consumption by 85-95%. |
| **`meta-llama-kv-prefix-stabilizer`** | Emulates Meta Llama 3.3 KV-cache alignment. Enforces strict token-boundary block padding to prevent prompt cache fragmentation and lock in 95% cache discounts. |
| **`mobile-gpu-texture-compression`** | Multi-platform GPU texture compression pipeline covering mobile ASTC/ETC2 and PC BC1-BC7, runtime format negotiation, and mipmap generation. |
| **`mobile-thermal-frame-pacing`** | Mobile thermal management, Android Swappy frame pacing, dynamic resolution scaling (DRS), and battery efficiency algorithms for Android and PC games. |
| **`pc-cross-platform-graphics-api`** | Modern C++ graphics Hardware Abstraction Layer (HAL) supporting DirectX 12, Vulkan, and DirectX 11, Valve Proton compatibility, and RenderDoc telemetry. |
| **`qwen-polyglot-ast-cartographer`** | Emulates Qwen 2.5 Coder polyglot AST cartography. Generates instant symbol call-graphs, inheritance trees, and signatures across C++, Python, Lua, and Rust in under 500 tokens. |
| **`rea-mcp-obligation-ledger-orchestrator`** | Orchestrates the Reverse Engineer Anything (REA) MCP server obligation ledger, binary function diffing, and static-to-runtime correlation to formally verify decompiled or ported C++ game engine binaries. |
| **`self-evolving-skill-synthesizer`** | Closed-loop in-flight skill synthesis, Voyager-style script promotion, and Reflexion self-healing. Automatically creates missing skills, promotes verified one-off scripts into reusable skill tools, and patches stale skill instructions mid-task across Gemini, Claude, and Cursor. |
| **`source-idtech-kex-engine-modding`** | Modding pipeline for Valve Source/Source 2, GoldSrc, id Tech (Quake II/III, DOOM 3), and Nightdive KEX Engine games in your Steam library (SiN Reloaded, Half-Life 1/2, Black Mesa, Garry's Mod, Left 4 Dead 1/2, Portal 1/2, CS2, TF2). |
| **`speculative-multi-step-drafting`** | Bundles predictable consecutive edits and multi-file modifications into single-turn atomic dispatches, slashing multi-turn reasoning overhead and saving up to 75% input tokens. |
| **`stalker2-to-ogsr-asset-transpiler`** | Converts and adapts S.T.A.L.K.E.R. 2 Heart of Chornobyl UE5 IoStore assets (textures, audio, ballistics curves, weather) into 64-bit S.T.A.L.K.E.R. OGSR/X-Ray formats. |
| **`time-travel-deterministic-replay-debug`** | Deterministic record-and-replay time-travel debugging using Mozilla rr and GDB reverse execution. Steps backwards from segfaults and corrupted pointers to the exact instruction that mutated memory. |
| **`ue5-foliage-mesh-to-ogsr-transpiler`** | Extracts S.T.A.L.K.E.R. 2 (UE5 IoStore) 3D trees, bushes, and grass meshes and transpiles them into 64-bit S.T.A.L.K.E.R. OGSR (.ogf and .dm) formats with uint16 submesh partitioning and alpha-coverage mipmaps. |
| **`ue5-redengine-rage-library-modding`** | Multi-engine modding workflows for your installed and owned UE5 IoStore games (Borderlands 4, Assetto Corsa Rally, S.T.A.L.K.E.R. 2), Rockstar GTA (GTA I/III/VC/SA/IV/V), CDPR REDengine (Cyberpunk 2077, Witcher 3), Baldur's Gate 3, Project Zomboid, and No Man's Sky. |
| **`windows-linux-cross-os-runtime-bridge`** | Cross-platform runtime bridge between Windows 10/11 (PowerShell 7, Win32 API, DirectX/DXGI, MSVC, ETW, ImDisk RAMDisk) and Linux (CachyOS/Arch, POSIX/Bash, Vulkan/RADV, Wine/Proton, /dev/shm, /dev/uinput) so all 300+ skills execute natively on both operating systems. |
| **`windsurf-cascade-flow-tracker`** | Emulates Codeium Windsurf Cascade Flow on Gemini 4 Argon. Tracks multi-file dependency ripple effects, symbol references, and cascading changes across C++, Lua, and LTX configurations. |
| **`xray-crash-interceptor-daemon`** | Background sweep daemon that intercepts and dismisses Wine/Proton crash modals (BugTrap, Notepad log windows) during unattended S.T.A.L.K.E.R./OGSR YOLO runs. |
| **`xray-crash-log-diagnostician`** | Triages and diagnoses S.T.A.L.K.E.R. X-Ray and OGSR engine crashes, BugTrap logs, and Wine/Proton stack traces into exact source file coordinates and root-cause fixes. |
| **`xray-ogf-dm-blender-pipeline`** | Direct binary compilation and export of S.T.A.L.K.E.R. X-Ray and OGSR 3D meshes (.ogf v4 rigid/skinned models and .dm Detail Model grass/flora) from Blender 5.2+ without third-party plugins. |
| **`zoneforge-cloud-sync-governor`** | Governs ZoneForge Google Drive and cloud asset synchronization, OAuth2 token refreshment, chunked resumable transfers, and local cache validation for large game mod distributions. |

<!-- AUTO-SYNC-CATALOG:END -->

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
3. Run `skills-audit-update --sync` (or `./install.sh --all`) to automatically compile and deploy the new skill across **Antigravity**, **Claude Code**, and **Cursor IDE**.

---

## 📄 License
MIT License. Free to use, adapt, and distribute for autonomous agent engineering.

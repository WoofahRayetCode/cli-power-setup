---
name: game-engine-migration
description: Universal architectural framework for porting, migrating, and modernizing game engines and legacy mods across bitness (32-bit to 64-bit), graphics APIs (DX9/OpenGL to DX11/DX12/Vulkan), and scripting runtimes.
---

# Universal Game Engine Migration & Porting Framework

This skill establishes the universal 5-stage architectural framework for porting legacy game engines, source ports, custom forks, and game mods across modern hardware architectures, graphics APIs, and operating environments.

---

## 🏛️ The 5-Stage Migration Lifecycle

```
[Phase 1: Architecture Audit]
       │
       ▼
[Phase 2: Bitness & ABI Alignment]
       │
       ▼
[Phase 3: Graphics Pipeline Modernization]
       │
       ▼
[Phase 4: Scripting Runtime & VFS Reconciliation]
       │
       ▼
[Phase 5: Differential Verification & Triage]
```

---

## 🔍 Phase 1: Architecture Audit & Dependency Inventory

Before altering source files or replacing engine binaries:
1. **Catalog Target Bitness & Subsystem Dependencies:**
   - Map all compiled native libraries (`.dll`, `.so`, `.dylib`).
   - Identify 32-bit proprietary binary blobs lacking source code. Any 32-bit closed-source DLL **cannot** link into a 64-bit process space; classify them immediately for re-implementation or Lua/script emulation.
2. **Virtual File System (VFS) & Mount Hierarchy:**
   - Document archive precedence (e.g., loose file overlays vs packed container priority).
   - Verify file-path case sensitivity assumptions (Linux/Wine porting often fails on un-sanitized case-sensitive lookups).
3. **Establish Vanilla / Baseline Checkpoint:**
   - Isolate unmodified legacy baselines in read-only directories (`unpacked/`, `vanilla/`).
   - Capture baseline execution logs, memory footprint, and frame times for differential comparison.

---

## ⚙️ Phase 2: Bitness Transition & Memory Alignment (32-bit to 64-bit)

### 1. Pointer Sizing & Arithmetic
* Replace raw integer casts (`int`, `long`, `DWORD`) holding memory addresses with `uintptr_t` or `size_t`.
* Audit pointer arithmetic and offset calculations:
  ```cpp
  // INCORRECT (Trunctates 64-bit addresses, causing 0xC0000005 crashes)
  DWORD baseAddr = (DWORD)ptr;
  
  // CORRECT (Architecture-agnostic pointer handling)
  uintptr_t baseAddr = reinterpret_cast<uintptr_t>(ptr);
  ```

### 2. Struct Alignment & Padding (`#pragma pack`)
* 32-bit x86 aligns `uint64_t` or `double` on 4-byte boundaries; 64-bit x86_64 aligns them on 8-byte boundaries.
* Binary file formats reading raw structs directly from disk via `fread()` or memory maps will suffer deserialization corruption if struct layout changes.
* Use explicit packing pragmas or fixed-width serializers:
  ```cpp
  #pragma pack(push, 1)
  struct LegacyDiskHeader {
      uint32_t magic;
      uint64_t dataOffset; // Explicit alignment preservation
  };
  #pragma pack(pop)
  ```

### 3. Calling Convention Alignment
* 32-bit engines use explicit conventions (`__thiscall` in `ECX`, `__stdcall`, `__cdecl`, `__fastcall`).
* 64-bit platforms collapse into unified ABIs (Microsoft x64 ABI using `RCX, RDX, R8, R9` with 32-byte shadow space; System V AMD64 using `RDI, RSI, RDX, RCX, R8, R9`).
* Ensure function pointers, engine callbacks, and native detour hooks drop obsolete 32-bit calling convention decorators under 64-bit compilation targets.

---

## 🎨 Phase 3: Graphics Pipeline Modernization

### 1. Legacy Fixed-Function & Early Shaders → Modern Programmable Pipeline
* **DirectX 9 / OpenGL 1.x-2.x:** Rely on implicit render states, fixed texture stages, and implicit uniform updates.
* **DirectX 11 / 12 / Vulkan:** Require explicit Pipeline State Objects (PSOs), explicit render targets, constant buffers, and descriptor sets.
* Strip or convert legacy shader models (SM 2.0 / 3.0). Never load legacy DX9 compiled shaders into modern deferred renderers without transpilation (e.g. via SPIRV-Cross, HLSLcc, or native DX11/12 rewrites).

### 2. Constant Buffer (CBuffer) & Uniform Alignment
* Modern graphics APIs require constant buffer layouts to align on 16-byte boundaries (float4).
* Verify uniform struct padding matches shader-side expectations to avoid matrix distortion or corrupt vertex transformation.

### 3. Vertex Layout Strides
* Ensure vertex declarations match input layouts bit-for-bit.
* Replace deprecated flexible vertex formats (FVF) with explicit vertex input descriptors.

---

## 📜 Phase 4: Scripting Runtime, Host Bridges & VFS

### 1. Embedded Scripting Engine Modernization
* **Lua 5.1 → LuaJIT / C++ Host Bridges:**
  * Ensure 64-bit LuaJIT memory allocation stays within the accessible 32-bit GC address space (or build with `LUAJIT_ENABLE_GC64`).
  * Reconcile callback signatures between engine C++ functions and Lua scripts.
* **Host Callback Lifetimes:**
  * Verify engine game objects exposed to scripts are validated before method invocations (prevent use-after-free or dangling pointers when entities are despawned).

### 2. VFS & Asset Serialization
* **Endianness & Coordinate Swizzling:**
  * When porting between platforms, convert endianness for multi-byte values.
  * Swizzle coordinates when migrating between left-handed (DirectX) and right-handed (OpenGL/Vulkan) coordinate systems.
* **Case Sanitization:**
  * Normalize all asset paths in VFS lookups to lowercase to ensure seamless operation on Linux / Steam Deck filesystems.

---

## 🧪 Phase 5: Differential Verification & Triage

### 1. Telemetry & Log Diffing
* Run identical scenario scripts in the baseline legacy engine and the migrated engine.
* Compare entity spawn counts, inventory inventories, quest state variables, and network synchronization hashes.

### 2. System Crash Classification

| Crash Signature | Root Cause | Remediation Protocol |
| :--- | :--- | :--- |
| `0xC0000005` (Access Violation at `0x00000000`) | Null pointer dereference or missing game entity pointer. | Add strict null guard; inspect host entity lifecycle before call. |
| `0xC0000005` (Access Violation at `0xFFFFFFFF...`) | Pointer truncation caused by casting 64-bit address to 32-bit int. | Audit pointer arithmetic for `DWORD` or `int` casts; replace with `uintptr_t`. |
| `0xC00000FD` (Stack Overflow) | Infinite recursion in engine callback hook or cyclic script event. | Audit hook detours and event dispatch cascades for missing recursion guards. |
| Shader compilation failure (`D3D11 / VK`) | Mismatched constant buffer alignment or missing semantics. | Reconcile cbuffer 16-byte alignment and explicit input layout semantics. |

### 3. Autonomous Closed-Loop Playtest Locomotion & Vision Telemetry
* If hands-on testing by the user is unavailable, **autonomously execute closed-loop locomotion and vision monitoring**:
  - **Input Injection (`game-qa-playtest-controller`):** Inject hardware-level kernel inputs (`/dev/uinput`) running `wander`, `orbit` (circle-strafing), `sweep` (360° panoramic yaw/pitch), and `stress-locomotion` (sprint/jump/crouch) to trigger physics, LOD transitions, and animation blend states.
  - **Screen Surveillance (`game-screen-telemetry-monitor`):** Continuously sample game frames in the background to detect missing shader/texture artifacts (magenta `#FF00FF`), graphics driver hangs, and window freezes.
  - **Action Verification (`agentic-visual-perception`):** Run structural visual diffing (SSIM) between action frames to confirm character responses and UI transitions.
  - **Crash Extraction (`visual-document-ocr-intelligence`):** If a crash occurs, capture the error dialog and run local OCR to extract faulting call stacks instantly.

## 🤖 Local AI Game Engine Porting Coprocessor (`deepseek-coder-v2:16b`, `qwen2.5-coder:32b` via `local-coprocessor`)

To modernize legacy C++ engine classes, audit 32-to-64-bit pointer truncation, and transpile shaders without consuming cloud token quotas, route porting tasks to the local high-end engine porting models:

```bash
# 1. 32-bit to 64-bit pointer sanitization & struct alignment audit
local-coprocessor generate --task port \
  --prompt "Audit this legacy C++ engine class for 32-bit to 64-bit pointer truncation (e.g. DWORD casts) and struct padding mismatches across MSVC x64 vs GCC: <code snippet>"

# 2. Transpile DirectX 9/11 HLSL shader to modern Vulkan SPIR-V / Slang
local-coprocessor generate --task port \
  --prompt "Transpile this DirectX 11 HLSL pixel shader to Vulkan GLSL/SPIR-V. Map cbuffer registers to uniform buffer objects (16-byte alignment), adapt NDC depth range [0, 1] to [-1, 1], and preserve sampler states"

# 3. Modernize legacy C++98/03 OOP code to modern C++20 RAII
local-coprocessor generate --task port --auto-skill \
  --prompt "Refactor this legacy monolithic game engine entity manager to use C++20 std::unique_ptr, std::span, and an Entity-Component-System (ECS) pattern"
```

---

## 🔗 Skill Composition Matrix

* **Local Model Coprocessor (`local-model-coprocessor`):** Dispatches porting tasks directly to `deepseek-coder-v2:16b` and `qwen2.5-coder:32b` locally in VRAM/RAM (0 cloud tokens billed).
* **Low-Level Binaries & VTables:** When reconstructing native C++ classes, combine with `lowlevel-dll-internals`.
* **Zero-MCP CLI Disassembly:** Combine with `standalone-binary-re` for inspecting PE exports, symbols, and relocations.
* **S.T.A.L.K.E.R. Specifics:** When porting to OGSR or Shadow of Chernobyl 64-bit, delegate to `stalker-ogsr-migration`.
* **Hands-Free QA:** Combine `game-qa-playtest-controller` with `game-screen-telemetry-monitor` and `agentic-visual-perception` for autonomous testing.

## Windows 10/11 & Cross-Platform Game Modding Parity (`windows-linux-cross-os-runtime-bridge`)
- **Native Windows vs. Linux Wine/Proton:** On Windows 10/11, execute `xrEngine.exe` and mod tools natively via DirectX 11/12 without Wine overhead. On Linux, route through Proton/Wine and DXVK/VKD3D.
- **LLP64 vs. LP64 64-Bit C++ Safety:** On Windows x64 MSVC/Clang-CL (LLP64), `long` and `unsigned long` (`DWORD`) are **32-bit (4 bytes)** whereas on Linux x86_64 (LP64) `long` is 64-bit. Never cast pointers to `long` or `DWORD`—always use `uintptr_t`, `intptr_t`, or `size_t`.
- **Crash Modal Interception & WER Dumps:** On Windows, `xray_crash_handler.py sweep` queries WMI (`Win32_Process`) and terminates lingering `notepad.exe`/`WerFault.exe` popups via `taskkill /F /PID`, reading logs from `%USERPROFILE%\Documents\STALKER-SHOC\logs` and `_appdata_\logs`.
- **Native Win32 Playtest Input & Window Capture:** When `sys.platform == "win32"`, `game_playtest_controller.py` automatically dispatches Win32 `keybd_event` / `mouse_event` (`SendInput`), `ClipCursor`, and `PIL.ImageGrab` instead of Linux `/dev/uinput` and `spectacle`.
- **Steam Library Auto-Discovery:** `steam-mod-scanner` automatically reads `HKCU\Software\Valve\Steam\SteamPath` and `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` on Windows alongside `~/.local/share/Steam` on Linux.

## Related & Interoperating Skills
- **`game-texture-material-pipeline`**: High-performance asset pipelines for modern PBR and legacy game textures. Use when converting textures across ...
- **`game-asset-pack-archive-engineering`**: Virtual file systems (VFS), game asset pack archive containers (PAK, XDB, AssetBundles), chunked zstd/zlib com...
- **`game-mod-release-packager`**: Automated game mod release packaging, archive compression, and distribution pipeline. Strips debug symbols (st...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

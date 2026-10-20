---
name: console-emulation-toolchains
description: Console homebrew toolchains (devkitPro, libnx, devkitARM), emulator optimization (Ryujinx, RetroArch), and Obtainium.
---

# Console Emulation & Toolchains (`console-emulation-toolchains`)

Homebrew cross-compilation toolchains, native SDKs (libnx), emulator performance tuning, and automated emulator feeds.

## Toolchains & Frameworks
- **devkitPro & libnx:** Cross-compile native Nintendo Switch `.nro` binaries using `aarch64-none-elf-gcc` and libnx APIs.
- **Emulator Performance Tuning:**
  - **Ryujinx & Yuzu/Suyu:** Vulkan backend, SPIR-V shader caching, Host memory mapping (Fastmem), and PPTC profiling.
  - **RetroArch:** Configure run-ahead frame latency mitigation and CRT-Geom shaders.
- **Obtainium Feeds:** Track and auto-update bleeding-edge emulator builds directly from GitHub releases.

## Related & Interoperating Skills
- **`console-storage-package-tools`**: FAT32 32KB cluster alignment, NSP/NSZ compression, XCI trimming, title ID mapping, and hactoolnet extraction.
- **`console-game-decompilation`**: Matching binary decompilation for console ROMs and retro binaries using Splat, m2c, and objdiff.
- **`cross-engine-shader-rendering`**: Slang/SPIRV-Cross shader transpilation (Vulkan, DX12, HLSL, GLSL), Cook-Torrance GGX PBR, and bloom FX.
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

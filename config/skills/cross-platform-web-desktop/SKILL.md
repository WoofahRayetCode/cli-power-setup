---
name: cross-platform-web-desktop
description: Cross-platform desktop and extension development with Tauri 2.0 (Rust), Electron IPC, and Manifest V3.
---

# Cross-Platform Web & Desktop Engineering (`cross-platform-web-desktop`)

Lightweight desktop applications and web extensions using Tauri 2.0, Electron, and Manifest V3.

## Standards
- **Tauri 2.0:** Rust backend commands (`#[tauri::command]`), secure IPC channels, minimal RAM footprint (<40 MB).
- **Electron Security:** `contextIsolation: true`, `nodeIntegration: false`, strict preload script bridging.
- **Manifest V3:** Background service workers, `declarativeNetRequest`, Chrome and Firefox compatibility via `webextension-polyfill`.

## Related & Interoperating Skills
- **`linux-systems-engineering`**: Linux systems programming, POSIX, io_uring, systemd, CachyOS/Arch packaging, and laptop ACPI controls.
- **`cross-engine-shader-rendering`**: Slang/SPIRV-Cross shader transpilation (Vulkan, DX12, HLSL, GLSL), Cook-Torrance GGX PBR, and bloom FX.
- **`rust-engineering`**: Rust development, Cargo builds, borrow checker, lifetimes, zero-cost abstractions, and clippy.

---
name: claude-hardware-acceleration-governor
description: Enforces dynamic 32-thread CPU saturation, 30 GB /dev/shm tmpfs RAM disk builds, and NVIDIA RTX 5060 OptiX GPU acceleration in Claude Code.
---

# Claude Hardware Acceleration Governor (`claude-hardware-acceleration-governor`)

When running on high-performance local hardware (such as this host's AMD Ryzen 9 8940HX with 32 execution threads, 30.4 GB DDR5 RAM, and NVIDIA GeForce RTX 5060 Laptop GPU), Claude Code must never fall back to single-threaded defaults, slow disk operations, or CPU rendering.

This skill governs hardware utilization across compilation, texture processing, and 3D rendering.

---

## ⚡ 1. Dynamic 32-Thread Saturation

Never execute single-threaded compilation or CPU loops. Always saturate all 32 available hardware threads:
- **CMake & Make**: `-j$(nproc)` or `MAKEFLAGS="-j$(nproc)"`
- **Ninja**: Automatically saturates all cores; set `NINJA_STATUS="[%f/%t %r] "`
- **Rust / Cargo**: `CARGO_BUILD_JOBS=$(nproc)`
- **Python Multiprocessing**: `ProcessPoolExecutor(max_workers=os.cpu_count())`

---

## 🚀 2. 30 GB `/dev/shm` tmpfs RAM Disk Accelerator

Stage intermediate builds, texture bakes, game archive unpacks (`.db`/`.pak`), and temporary test artifacts in `/dev/shm` (Linux shared memory tmpfs):
- **Bandwidth**: `~40 GB/s` memory throughput vs NVMe SSD wear.
- **CMake Builds**: `cmake -B /dev/shm/build -S .`
- **Blender Renders**: Save intermediate contact sheet frames to `/dev/shm/render.png`.
- **Cleanup on Exit**: Always remove temporary files from `/dev/shm/` upon task completion.

---

## 🎮 3. NVIDIA RTX 5060 OptiX & CUDA Dispatch

For headless 3D asset generation and rendering in Blender 5.2+ (`bpy`):
- **Hardware Acceleration**: Always activate `compute_device_type = 'OPTIX'` (`scene.cycles.device = 'GPU'`).
- **AI Denoising**: Activate OptiX AI Denoising at `16–32 samples` for sub-second viewport rendering and normal/AO texture baking.
- **Never CPU Fallback**: Do not allow Cycles to fall back to CPU rendering when the RTX 5060 Laptop GPU with 8GB GDDR7 is present.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

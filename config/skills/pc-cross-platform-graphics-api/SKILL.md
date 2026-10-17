---
name: pc-cross-platform-graphics-api
description: Modern C++ graphics Hardware Abstraction Layer (HAL) supporting DirectX 12, Vulkan, and DirectX 11, Valve Proton compatibility, and RenderDoc telemetry.
---

# PC Cross-Platform Graphics API (`pc-cross-platform-graphics-api`)

Modern PC games targeting Windows and Linux (Steam Proton / Steam Deck / native) require a clean Hardware Abstraction Layer (HAL / RHI) that decouples engine gameplay systems from underlying graphics drivers.

This skill establishes unified command list encoding, descriptor management, pipeline state caching, and automated RenderDoc headless frame profiling.

---

## 1. Modern Render Hardware Interface (RHI) Architecture

```
+-------------------------------------------------------------+
| Engine Gameplay Systems (Scene Graph, Render Passes, UI)    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
| Unified RHI Interface (CommandList, Buffer, Texture, PSO)   |
+-------------------------------------------------------------+
        |                                       |
        v                                       v
+-------------------------------+   +-------------------------+
| Vulkan Backend (Linux/Windows)|   | DirectX 12 / 11 Backend |
| - VkCommandBuffer             |   | - ID3D12GraphicsCommandList
| - VkDescriptorSet / PushDesc  |   | - Root Signature / CBV  |
| - SPIR-V Shaders              |   | - DXIL Shaders          |
+-------------------------------+   +-------------------------+
```

---

## 2. Linux & Valve Proton Compatibility Rules

1. **POSIX File Path Invariance:**
   - Linux filesystems (ext4, btrfs) are strictly case-sensitive. Always normalize asset paths to lowercase: `textures/weapons/ak74.dds`, never `Textures/Weapons/AK74.DDS`.
2. **Vulkan Synchronization 2:**
   - Prefer `VK_KHR_synchronization2` over legacy memory barriers to eliminate pipeline stall bubbles and simplify barrier code across both desktop NVIDIA/AMD GPUs and Intel Arc.
3. **Headless RenderDoc Automated Capture:**
   ```bash
   # Capture a single frame from the native or Wine build without UI interaction
   renderdoccmd capture --frame 150 --capture-file capture_frame150.rdc ./build/game_bin
   ```

---

## 3. Shader Cross-Compilation (HLSL to SPIR-V)

Compile HLSL source into both DXIL (DirectX 12) and SPIR-V (Vulkan) from a single master shader:
```bash
# Compile to SPIR-V for Vulkan
glslangValidator -D -e VSMain -S vert -V -o build/shaders/uber_shader.vert.spv src/shaders/uber_shader.hlsl

# Validate SPIR-V bytecode
spirv-val build/shaders/uber_shader.vert.spv
```

---
name: cross-engine-shader-transpiler
description: Universal shader authoring and transpilation using Slang and SPIRV-Cross, converting single-source shaders to Vulkan SPIR-V, DX12 HLSL, Metal MSL, and OpenGL GLSL.
---

# Cross-Engine Shader Transpiler (`cross-engine-shader-transpiler`)

Maintaining separate, redundant shader codebases for Vulkan (SPIR-V), DirectX 12 (DXIL/HLSL), Apple Metal (MSL), and OpenGL/GLES (GLSL) is error-prone and leads to cross-platform visual divergence.

This skill standardizes single-source shader authoring using **Slang** or **SPIRV-Cross** to transpile unified shader code to all target graphics APIs with automated descriptor set, uniform block, and constant buffer alignment.

---

## 1. Universal Transpilation Pipeline

```
+-------------------------------------------------------------+
| Single-Source Shader (Slang or Modern HLSL 2021)            |
+-------------------------------------------------------------+
                              |
              +---------------+---------------+
              |                               |
       (slangc / glslangValidator)            | (spirv-cross)
              v                               v
    +-------------------+           +-------------------+
    | Vulkan SPIR-V     |           | DirectX 12 HLSL   |
    | (PC & Android)    |           | (DXIL / SM 6.6)   |
    +-------------------+           +-------------------+
              |                               |
              +---------------+---------------+
                              |
                              v
    +-------------------+           +-------------------+
    | Apple Metal MSL   |           | OpenGL ES 3.2     |
    | (macOS / iOS)     |           | (Legacy Fallback) |
    +-------------------+           +-------------------+
```

---

## 2. Slang Multi-Target CLI Workflow

```bash
# 1. Compile single shader source to Vulkan SPIR-V
slangc src/shaders/pbr_lighting.slang -target spirv -profile glsl_460 -o build/shaders/pbr_lighting.spv

# 2. Compile to DirectX 12 DXIL
slangc src/shaders/pbr_lighting.slang -target dxil -profile sm_6_6 -o build/shaders/pbr_lighting.dxil

# 3. Transpile SPIR-V to Metal Shading Language (MSL) via spirv-cross
spirv-cross build/shaders/pbr_lighting.spv --msl --output build/shaders/pbr_lighting.metal
```

---

## 3. Layout & Alignment Rules

1. **16-Byte Struct Packing:**
   Ensure all uniform buffers (cbuffers) have struct fields aligned to 16-byte boundaries (e.g. `vec4`, `float4`, or 3-component vectors padded with a scalar float).
2. **Explicit Binding Sets:**
   Use explicit descriptor set and binding qualifiers:
   ```hlsl
   [[vk::binding(0, 0)]] ConstantBuffer<FrameConstants> gFrame : register(b0);
   [[vk::binding(1, 0)]] Texture2D<float4> gAlbedoMap : register(t0);
   [[vk::binding(2, 0)]] SamplerState gSampler : register(s0);
   ```
3. **Automated SPIR-V Validation:**
   Always run `spirv-val` on generated SPIR-V binaries to catch malformed control flows or unsupported memory models before runtime driver submission.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`shader-cross-compilation`**: Cross-compilation, translation, and validation of game shaders across HLSL, GLSL, SPIR-V, WGSL, and MSL. Use w...
- **`vulkan-gpu-compute`**: Cross-vendor GPU compute and modern graphics engineering via Vulkan 1.3/1.4, SPIR-V shader compilation, headle...
- **`pc-cross-platform-graphics-api`**: Modern C++ graphics Hardware Abstraction Layer (HAL) supporting DirectX 12, Vulkan, and DirectX 11, Valve Prot...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

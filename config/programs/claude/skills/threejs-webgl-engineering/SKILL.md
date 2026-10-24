---
name: threejs-webgl-engineering
description: Interactive 3D WebGL and WebGPU engineering with Three.js, OrbitControls, GLTFLoader, and PBR rigs.
---

# Three.js & WebGL Engineering (`threejs-webgl-engineering`)

Interactive browser-based 3D graphics, shader materials, and PBR model inspection.

## Architecture
- **Rendering Setup:** `WebGLRenderer({ antialias: true, powerPreference: 'high-performance' })`, outputColorSpace = `SRGBColorSpace`, ACESFilmicToneMapping.
- **Asset Loading:** Asynchronous GLTFLoader with DRACOLoader decompression and KTX2 texture transcoding.
- **Lighting Rigs:** Three-point studio lighting with directional key, soft ambient sky fill, and subtle rim light.

## Related & Interoperating Skills
- **`cross-engine-shader-rendering`**: Slang/SPIRV-Cross shader transpilation (Vulkan, DX12, HLSL, GLSL), Cook-Torrance GGX PBR, and bloom FX.
- **`interactive-data-visualization-web`**: Browser-based interactive D3.js force graphs, Vis.js timelines, KaTeX, and reactive single-file micro-apps.
- **`linux-systems-engineering`**: Linux systems programming, POSIX, io_uring, systemd, CachyOS/Arch packaging, and laptop ACPI controls.

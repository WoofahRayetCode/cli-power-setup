---
name: game-graphics-optimization-profiling
description: Profiling and optimizing GPU/CPU rendering performance for games and engine ports. Use when identifying vertex, pixel, or bandwidth bottlenecks, implementing draw call batching, designing frustum/occlusion culling, creating LOD systems, or integrating temporal upscaling (TAA, FSR, DLSS).
---

# Game Graphics Optimization & GPU Profiling

This skill governs the identification of rendering bottlenecks, draw call reduction, GPU memory bandwidth optimization, and the integration of modern temporal upscaling technologies.

---

## 1. Identifying the Primary Bottleneck

Before touching rendering code, identify which pipeline stage limits performance:

| Stage | Symptoms | Diagnostic Test | Primary Fixes |
| :--- | :--- | :--- | :--- |
| **CPU Draw / Submission** | Low GPU utilization (<90%), high CPU main thread time | Profile with Tracy / Chrome tracing / CPU counters | Indirect MultiDraw, GPU culling, instancing, state grouping |
| **GPU Vertex / Geometry** | Frame time scales with triangle count, independent of resolution | Halve triangle count or disable geometry stages | Mesh LODs, frustum culling, index buffer cache optimization (Forsyth algorithm) |
| **GPU Pixel / Bandwidth** | Frame time scales directly with screen resolution (4K vs 1080p) | Drop render resolution from 100% to 50% | Early-Z prepass, deferred rendering, half-res postfx, texture compression (BCn) |
| **GPU ROP / Overdraw** | High frame time in transparent foliage, smoke, particles | Render scene in wireframe or overdraw heatmap mode | Sort front-to-back, reduce particle quad bounding boxes, depth bounds testing |

---

## 2. Draw Call Reduction & Culling Hierarchies

### A. Frustum & Occlusion Culling
1. **Frustum Culling:** Test object bounding spheres / AABBs against the 6 camera frustum planes. Reject invisible meshes on CPU or GPU compute.
2. **Hierarchical Z-Buffer (Hi-Z) Occlusion Culling:**
   * Downsample the previous frame's depth buffer into a mip chain storing maximum depth.
   * Project object bounding box onto screen space; test nearest depth against the Hi-Z mip level matching the box's size.
   * Cull occluded geometry before issuing draw calls.

### B. Indirect GPU Multi-Draw
Instead of CPU looping over $N$ meshes:
```cpp
// Vulkan: Single API call draws all visible instances
vkCmdDrawIndexedIndirect(commandBuffer, indirectBuffer, offset, drawCount, sizeof(VkDrawIndexedIndirectCommand));
```
A GPU compute shader runs culling and writes directly to `indirectBuffer`.

---

## 3. Temporal Anti-Aliasing (TAA) & Upscaling Integration

Modern temporal upscalers (AMD FSR 2/3, Intel XeSS, NVIDIA DLSS) require exact engine-provided buffers:

1. **Camera Jittering:** Jitter camera projection matrix sub-pixel offsets using Halton sequence (bases 2 and 3) across 8 to 16 frames:
   $$x_j = \text{Halton}(i, 2) - 0.5, \quad y_j = \text{Halton}(i, 3) - 0.5$$
2. **Motion Vectors (Velocity Buffer):** Per-pixel 2D screen motion from previous frame to current frame:
   $$\text{Velocity} = \text{uv}_{\text{current}} - \text{uv}_{\text{previous}}$$
3. **Linear Depth:** Clean depth without transparency.
4. **Exposure & Reactive Masks:** Mask out particles, UI elements, and alpha-blended geometry from history accumulation to prevent ghosting.

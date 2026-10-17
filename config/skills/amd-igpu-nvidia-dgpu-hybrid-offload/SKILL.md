---
name: amd-igpu-nvidia-dgpu-hybrid-offload
description: Dual-GPU workload splitter for AMD Radeon 610M iGPU (/dev/dri/renderD129, RADV Vulkan + VA-API VCN + 30GB shared DDR5 RAM) and NVIDIA GeForce RTX 5060 dGPU (/dev/dri/renderD128, 8GB GDDR7 CUDA/OptiX). Prevents background agent tasks from stealing game VRAM.
---

# AMD Radeon 610M iGPU + NVIDIA RTX 5060 dGPU Hybrid Offloader (`amd-igpu-nvidia-dgpu-hybrid-offload`)

## When to Use
- Running background video encoding/decoding, playtest screen recording, Vulkan compute shaders, image upscaling, or secondary LLM/embedding inference on the **AMD Radeon 610M iGPU** (`GPU0`, `/dev/dri/renderD129`) so **100% of the NVIDIA RTX 5060 dGPU (8 GB VRAM)** (`GPU1`, `/dev/dri/renderD128`) remains dedicated to the running game or Blender Cycles OptiX bakes.
- Preventing the common Linux hybrid-laptop bug where Vulkan apps accidentally bind to `GPU0` (AMD Radeon 610M) instead of `GPU1` (NVIDIA RTX 5060), or vice versa.

---

## 1. Host Dual-GPU Hardware Topology (CachyOS Linux)

| GPU Device | PCI Address & DRM Render Node | Vulkan Index & Driver | Memory Pool | Ideal Workload Assignment |
| :--- | :--- | :--- | :--- | :--- |
| **AMD Radeon 610M (RDNA2 iGPU)** | `0000:07:00.0` (`/dev/dri/renderD129`, `card2`) | `GPU0` (`radv` Mesa) | Up to **15 GB Shared DDR5 RAM** | Background VA-API H.264/HEVC/AV1 video encode/decode, playtest recording, Vulkan `ncnn`/upscaling, 2D compositor, overflow large-RAM models. |
| **NVIDIA GeForce RTX 5060 Laptop** | `0000:01:00.0` (`/dev/dri/renderD128`, `card1`) | `GPU1` (`NVIDIA` proprietary) | **8,151 MiB Dedicated GDDR7** | Active DXVK/VKD3D-Proton games, Blender 5.2+ Cycles OptiX ray-tracing, CUDA 13.4 kernels, fast 7B Ollama (`qwen2.5-coder:7b`). |

---

## 2. Deterministic GPU Pinning Environment Variables

### A. Pin Heavy 3D Games, DXVK/VKD3D & Blender Cycles to NVIDIA RTX 5060 (`GPU1`)
Because `AMD Radeon 610M` is `GPU0` in `vulkaninfo`, always force high-performance games and 3D renderers onto `GPU1`:
```bash
export __NV_PRIME_RENDER_OFFLOAD=1
export __GLX_VENDOR_LIBRARY_NAME=nvidia
export __VK_LAYER_NV_optimus=NVIDIA_only
export VK_DRIVER_FILES=/usr/share/vulkan/icd.d/nvidia_icd.json
```

### B. Pin Background Compute, Upscalers & Secondary Vulkan Tasks to AMD Radeon 610M iGPU (`GPU0`)
When a game is running on the RTX 5060 and the agent needs GPU compute without touching NVIDIA VRAM or causing frametime spikes:
```bash
export VK_DRIVER_FILES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json
export MESA_VK_DEVICE_SELECT="1002:164e!"
export DRI_PRIME=pci-0000_07_00_0
```

---

## 3. Zero-Nvidia-Load Hardware Video Encode/Decode on AMD iGPU (`VA-API`)
Never use CPU `libx264` or steal RTX 5060 NVENC sessions while playtesting a game. Offload video recording, contact-sheet frame extraction, and transcoding to the **AMD Radeon 610M VCN media engine** (`/dev/dri/renderD129`):

```bash
# Hardware-accelerated H.264 / HEVC encode on AMD Radeon 610M iGPU (0% RTX 5060 impact, <2% CPU)
ffmpeg -vaapi_device /dev/dri/renderD129 \
  -i input.mp4 \
  -vf 'format=nv12,hwupload' \
  -c:v h264_vaapi -qp 22 -y output_igpu.mp4
```

---

## 4. Overflowing Large Local Models (>8 GB) to AMD iGPU + 30 GB DDR5 RAM
- Models `<= 7B–8B Q4_K_M` (`~4.8 GB`) fit 100% inside the **RTX 5060 (8 GB VRAM)** via CUDA.
- If running a larger `14B–32B` model (`9–18 GB`) or running a background embedding daemon while a game occupies RTX 5060 VRAM, run `llama-server` / `ollama` with Vulkan RADV pointed at `GPU0` (`VK_DRIVER_FILES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json`), which seamlessly addresses shared DDR5 system RAM via AMD UMA.

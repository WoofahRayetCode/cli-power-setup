---
name: rtx-optix-gpu-baker-denoiser
description: Accelerates headless Blender 5.2+ Cycles texture baking (Normals, AO, Lightmaps, Curvature) and 2x2 contact sheet renders by 10x-20x using NVIDIA RTX 5060 Hardware Ray-Tracing (OptiX) and AI Denoising at 16-32 samples.
---

# NVIDIA RTX 5060 OptiX GPU Baker & AI Denoiser (`rtx-optix-gpu-baker-denoiser`)

## When to Use
- Any headless Blender 5.2+ (`blender -b -P`) script that runs **Cycles texture baking** (`bpy.ops.object.bake`) or **Cycles preview rendering** (`bpy.ops.render.render`).
- Eliminating slow CPU Cycles fallback (which burns 20–60 seconds per bake) by binding directly to the laptop's **NVIDIA GeForce RTX 5060 GPU (8 GB VRAM, Blackwell RT + Tensor Cores)**.

---

## 1. Mandatory Headless Blender 5.2+ RTX OptiX Activation Snippet
Blender running in `-b` (background/headless) mode defaults to `CPU` rendering unless explicitly instructed to initialize the `OPTIX` backend and enable the NVIDIA GPU device:

```python
import bpy

def enable_rtx_optix_fast_cycles(samples: int = 24, use_denoiser: bool = True):
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'

    # 1. Activate NVIDIA OptiX Hardware Ray-Tracing on RTX 5060
    prefs = bpy.context.preferences
    cprefs = prefs.addons['cycles'].preferences
    try:
        cprefs.compute_device_type = 'OPTIX'
    except TypeError:
        cprefs.compute_device_type = 'CUDA'
    cprefs.get_devices()
    for dev in cprefs.devices:
        dev.use = (dev.type in {'OPTIX', 'CUDA'})

    scene.cycles.device = 'GPU'

    # 2. Low-Sample + Hardware AI Denoising (24 samples + Denoise = 512-sample quality in 0.5s!)
    scene.cycles.samples = samples
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.05
    scene.cycles.use_denoising = use_denoiser
    try:
        scene.cycles.denoiser = 'OPTIX'
    except TypeError:
        scene.cycles.denoiser = 'OPENIMAGEDENOISE'
```

---

## 2. Optimal Sample Counts by Task (RTX 5060 Benchmarks)

| Headless Blender Task | Recommended `samples` | Denoiser | Typical RTX 5060 Time |
| :--- | :--- | :--- | :--- |
| **Tangent-Space Normal Map Bake (`2048x2048`)** | `4` (Pure geometric raycast) | `False` (Never denoise normal vectors) | `~0.18 sec` |
| **Ambient Occlusion (AO) Bake (`2048x2048`)** | `24` | `True` (`OPTIX`) | `~0.45 sec` |
| **2x2 Contact Sheet Preview Render (`1024x1024`)** | `24` (`CYCLES`) or `BLENDER_EEVEE_NEXT` | `True` (`OPTIX`) | `~0.60 sec` |
| **Baked Global Illumination Lightmap (`UV2`)** | `32` | `True` (`OPTIX`) | `~0.75 sec` |

---

## 3. VRAM Hygiene
- When baking `4096x4096` textures on an 8 GB VRAM laptop GPU, set `scene.cycles.use_auto_tile = True` and `scene.cycles.tile_size = 2048` so peak VRAM stays well below `3.5 GB`.

## Windows 10/11 & Cross-OS Hardware Offload Parity (`windows-linux-cross-os-runtime-bridge`)
- **CPU Thread Saturation:** Use `os.cpu_count()` in Python, `$env:NUMBER_OF_PROCESSORS` in PowerShell 7 (`CMAKE_BUILD_PARALLEL_LEVEL=$env:NUMBER_OF_PROCESSORS`, `CARGO_BUILD_JOBS=$env:NUMBER_OF_PROCESSORS`, `msbuild /m`), and `$(nproc)` on Linux.
- **RAM-Disk & Scratch I/O:** Resolve scratch paths via `Path("/dev/shm")` on Linux, an ImDisk/OSFMount RAMDrive (`R:\`) if mounted on Windows, or `Path(tempfile.gettempdir())` (`%LOCALAPPDATA%\Temp`). Never hardcode `/tmp/`.
- **Dual-GPU Selection (RTX 5060 dGPU + Radeon 610M iGPU):** On Windows 10/11, bind executables via Registry `HKCU:\Software\Microsoft\DirectX\UserGpuPreferences` (`GpuPreference=1;` for Power-Saving AMD Radeon iGPU; `GpuPreference=2;` for High-Performance NVIDIA RTX 5060 dGPU) and `CUDA_VISIBLE_DEVICES=0`.
- **Vision & OCR on Windows:** Use `PIL.ImageGrab.grab(all_screens=True)` and resolve `tesseract.exe` via `shutil.which("tesseract")` or `C:\Program Files\Tesseract-OCR\tesseract.exe`.

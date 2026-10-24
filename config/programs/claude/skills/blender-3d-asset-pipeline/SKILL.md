---
name: blender-3d-asset-pipeline
description: Headless Blender 5.2+ bpy automation, hard-surface CAD, SDF remeshing, SLIM UVs, and RTX 5060 OptiX baking.
---

# Blender 3D Asset Pipeline (`blender-3d-asset-pipeline`)

Production 3D asset creation, procedural geometry, organic sculpting, and GPU baking in Blender 5.2+ (`bpy`).

## Hardware & Acceleration
- **NVIDIA RTX 5060 OptiX Ray-Tracing:** Always activate `scene.cycles.device = 'GPU'` and AI OptiX Denoising at 16–32 samples for sub-second baking.
- **30 GB `/dev/shm` tmpfs Accelerator:** Stage intermediate texture bakes and OBJ/FBX exports in `/dev/shm` to eliminate SSD wear.
- **SDF Organic Remeshing:** Eliminate the 'cartoony balloon-animal' look via Voxel SDF Remeshing, Volume-Preserving Laplacian smoothing, and QuadriFlow retopology.
- **Tools:**
  Silhouette verification: `python3 ~/.gemini/config/skills/blender-3d-asset-pipeline/scripts/silhouette_iou_profiler.py`
  Texture editing: `python3 ~/.gemini/config/skills/blender-3d-asset-pipeline/scripts/texture_editor.py`
  PBR channel packing: `python3 ~/.gemini/config/skills/blender-3d-asset-pipeline/scripts/texture_pbr_packer.py`

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`game-engines-multiplatform`**: Modern Godot 4, Unreal Engine 5, Unity, Steamworks publishing, Steam Deck tuning, and Proton game dev.
- **`game-audio-voice-engineering`**: Game audio Ogg Vorbis GSC comment headers, procedural SFX, spatial HRTF, ElevenLabs, and Piper TTS.

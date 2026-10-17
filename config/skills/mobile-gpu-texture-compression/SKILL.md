---
name: mobile-gpu-texture-compression
description: Multi-platform GPU texture compression pipeline covering mobile ASTC/ETC2 and PC BC1-BC7, runtime format negotiation, and mipmap generation.
---

# Mobile GPU Texture Compression (`mobile-gpu-texture-compression`)

Loading uncompressed PNGs or RGBA8 textures on mobile or desktop GPUs exhausts VRAM, destroys memory bandwidth, and triggers aggressive operating system kills. 

Desktop GPUs rely on **BC (Block Compression, BC1–BC7)**, while mobile GPUs (Qualcomm Adreno, ARM Mali, PowerVR) require **ASTC (Adaptive Scalable Texture Compression)** or **ETC2**.

This skill governs the automated dual-target texture compression pipeline and runtime format negotiation.

---

## 1. Cross-Platform Format Matrix

| Asset Type | PC (DirectX 11/12 / Vulkan) | Mobile Android (Vulkan / GLES 3) | Visual Profile |
| :--- | :--- | :--- | :--- |
| **Albedo / Base Color** | `BC7` (sRGB) or `BC1` | `ASTC 6x6` or `ETC2_RGBA8` | sRGB Gamma Corrected |
| **Normal Maps** | `BC5` (RG 2-channel) | `ASTC 5x5` or `EAC_RG11` | Linear / Normalized |
| **Packed ORM (AO/Rough/Metal)**| `BC7` (Linear) | `ASTC 6x6` (Linear) | Linear Raw Values |
| **UI Sprites / Alpha Fonts** | `BC7` or `BC3` | `ASTC 4x4` (High fidelity) | sRGB with Crisp Edges |

---

## 2. Automated Compression CLI Workflow

```bash
# 1. Compress texture for Android via astcenc (ASTC 6x6 block size)
astcenc -cl input_albedo.png output_albedo_astc6x6.astc 6x6 -medium

# 2. Compress normal map for Android (linear, 2-channel normalized)
astcenc -cl input_normal.png output_normal_astc5x5.astc 5x5 -normal -medium

# 3. Compress for PC via DirectXTex / texconv (BC7)
texconv -f BC7_UNORM_SRGB -m 0 -y -o pc_textures/ input_albedo.png
```

---

## 3. Runtime Format Negotiation in Vulkan

```cpp
VkFormatProperties props;
vkGetPhysicalDeviceFormatProperties(physicalDevice, VK_FORMAT_ASTC_6x6_SRGB_BLOCK, &props);

if (props.optimalTilingFeatures & VK_FORMAT_FEATURE_SAMPLED_IMAGE_BIT) {
    // ASTC is natively supported by mobile GPU hardware
    load_astc_texture("textures/albedo.astc");
} else {
    // Fallback to ETC2 for older Android devices
    load_etc2_texture("textures/albedo.pkm");
}
```

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`game-texture-material-pipeline`**: High-performance asset pipelines for modern PBR and legacy game textures. Use when converting textures across ...
- **`blender-pbr-texture-packager`**: PBR texture channel packing (ORM - Occlusion, Roughness, Metallic), texel density enforcement, and normal map ...
- **`android-mobile-3d-asset-optimizer`**: Android NDK, Vulkan, and OpenGL ES 3.2 mobile 3D asset optimization in Blender 5.2+. Enforces Adreno/Mali Tile...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

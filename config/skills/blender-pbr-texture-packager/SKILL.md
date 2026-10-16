---
name: blender-pbr-texture-packager
description: PBR texture channel packing (ORM - Occlusion, Roughness, Metallic), texel density enforcement, and normal map orientation (DirectX vs OpenGL) for game engines.
---

# Blender PBR Texture Packager (`blender-pbr-texture-packager`)

Modern game engines (Unreal, Godot, Unity, X-Ray/OGSR) require channel-packed PBR textures to minimize texture memory footprint and eliminate redundant texture sampler state switches on the GPU.

This skill standardizes ORM packing, texel density metrics, and normal map orientation across game engine targets.

---

## 1. ORM Channel Packing Protocol

Combine individual grayscale maps into a single 3-channel RGB texture:

| Channel | Map Type | Color Space | Role in Engine |
| :--- | :--- | :--- | :--- |
| **Red (R)** | **Ambient Occlusion (AO)** | Linear / Non-Color | Crevice shadows and contact darkening |
| **Green (G)** | **Roughness** | Linear / Non-Color | Surface micro-facet roughness (0 = mirror, 1 = chalk) |
| **Blue (B)** | **Metallic** | Linear / Non-Color | Conductive mask (0 = dielectric/plastic, 1 = raw metal) |

### Headless Packing Script via Pillow:
```python
from PIL import Image

def pack_orm(ao_path, roughness_path, metallic_path, output_path):
    ao = Image.open(ao_path).convert('L')
    rough = Image.open(roughness_path).convert('L')
    metal = Image.open(metallic_path).convert('L')
    
    # Ensure uniform dimensions
    size = ao.size
    rough = rough.resize(size, Image.Resampling.LANCZOS)
    metal = metal.resize(size, Image.Resampling.LANCZOS)
    
    orm = Image.merge('RGB', (ao, rough, metal))
    orm.save(output_path, format='PNG', optimize=True)
    print(f"Packed ORM saved: {output_path} ({size[0]}x{size[1]})")
```

---

## 2. Normal Map Green Channel (`Y`) Inversion

Different graphics APIs interpret the green channel of tangent-space normal maps differently:

- **DirectX / Unreal / S.T.A.L.K.E.R. OGSR:** Uses **Y-** (Green channel inverted, light comes from top-left with negative Y pointing down).
- **OpenGL / Vulkan / Godot / Unity:** Uses **Y+** (Green channel standard, light points up).

### Automated Green Inversion via Pillow:
```python
def invert_normal_green(normal_path, output_path):
    img = Image.open(normal_path).convert('RGBA')
    r, g, b, a = img.split()
    from PIL import ImageOps
    g_inverted = ImageOps.invert(g)
    converted = Image.merge('RGBA', (r, g_inverted, b, a))
    converted.save(output_path)
    print(f"DirectX Y- normal map saved to {output_path}")
```

---

## 3. Texel Density Standardization

To prevent visual jarring where a weapon has crisp 4K pixels next to a muddy 512px hand:
- **Hero First-Person Props:** $20.48\text{ px/cm}$ ($2048\text{ px/m}$)
- **Characters / Third-Person Props:** $10.24\text{ px/cm}$ ($1024\text{ px/m}$)
- **Large World Architecture:** $5.12\text{ px/cm}$ ($512\text{ px/m}$)

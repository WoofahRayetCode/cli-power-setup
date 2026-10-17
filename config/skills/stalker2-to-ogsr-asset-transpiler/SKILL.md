---
name: stalker2-to-ogsr-asset-transpiler
description: Converts and adapts S.T.A.L.K.E.R. 2 Heart of Chornobyl UE5 IoStore assets (textures, audio, ballistics curves, weather) into 64-bit S.T.A.L.K.E.R. OGSR/X-Ray formats.
---

# S.T.A.L.K.E.R. 2 to OGSR Asset Transpiler (`stalker2-to-ogsr-asset-transpiler`)

S.T.A.L.K.E.R. 2 (Unreal Engine 5 IoStore `.utoc` / `.ucas`) contains remastered classic assets, dynamic weather profiles, high-definition audio, and modern weapon ballistics. This skill automates the extraction and transpilation pipeline targeting the 64-bit S.T.A.L.K.E.R. OGSR Engine.

---

## 1. Container Map & Target Assets

| IoStore Container | Content Category | Target OGSR Subsystem | Conversion Toolchain |
| :--- | :--- | :--- | :--- |
| **`pakchunk16`** | 1,736 Weapon & Ballistic Curves | `config/weapons/*.ltx` | Curve transpiler (`retoc export` -> LTX keys) |
| **`pakchunk20` & `pakchunk37`** | 50,000+ Wwise SFX Events | `gamedata/sounds/*.ogg` | Wwise `.wem` -> FFmpeg -> `game-audio-ogg-gsc-encoder` |
| **`pakchunk37`** | `/Game/OLD_Stalker/` PBR Textures | `gamedata/textures/*.dds` | TGA/PNG -> ImageMagick/DirectXTex (BC7/DXT5 + THM) |
| **`pakchunk26` & `pakchunk30`** | Fog & Dynamic Weather Profiles | `config/weathers/*.ltx` | Lighting IES & Fog curves -> OGSR DX11 weather |
| **`Movies/MainMenuVideo/`** | 4K 60fps Bonfire Videos (`.bk2`) | `ui/ui_mm_main.xml` | FFmpeg transcode Bink2 -> OGSR video format |

---

## 2. Extraction Pipeline Commands

```bash
# 1. Unpack specific target pakchunk using retoc
retoc unpack /mnt/games/SteamLibrary/steamapps/common/S.T.A.L.K.E.R.\ 2\ Heart\ of\ Chornobyl/Stalker2/Content/Paks/pakchunk16-Windows.utoc -o /tmp/s2_extracted/

# 2. Inspect manifest with repak
repak list /mnt/games/SteamLibrary/steamapps/common/S.T.A.L.K.E.R.\ 2\ Heart\ of\ Chornobyl/Stalker2/Content/Paks/pakchunk16-Windows.pak | grep -i "AimingWeapon"
```

---

## 3. Ballistic Curve Transpilation Matrix

| S.T.A.L.K.E.R. 2 Curve Property | OGSR LTX Key | Conversion Logic |
| :--- | :--- | :--- |
| `AimingWeaponFOVCurve` | `scope_zoom_factor` | Normalized UE5 FOV translated to X-Ray degrees |
| `AssaultRifleDispersionDefault` | `fire_dispersion_base` | Radial spread converted to radians/degrees |
| `AimingWeaponRecoilPitchCurve` | `cam_dispersion` | Per-shot vertical pitch kick |
| `AimingWeaponRecoilYawCurve` | `cam_dispersion_inc` | Incremental horizontal muzzle drift |

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`ue5-foliage-mesh-to-ogsr-transpiler`**: Extracts S.T.A.L.K.E.R. 2 (UE5 IoStore) 3D trees, bushes, and grass meshes and transpiles them into 64-bit S.T...
- **`stalker2-modding`**: Modding workflows and tools for S.T.A.L.K.E.R. 2 Heart of Chornobyl (Unreal Engine 5). Use when packaging UE5 ...
- **`game-texture-material-pipeline`**: High-performance asset pipelines for modern PBR and legacy game textures. Use when converting textures across ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

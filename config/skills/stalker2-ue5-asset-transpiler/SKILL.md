---
name: stalker2-ue5-asset-transpiler
description: S.T.A.L.K.E.R. 2 UE5 IoStore asset extraction, audio conversion, and vegetation transpilation to OGSR.
---

# S.T.A.L.K.E.R. 2 to OGSR Asset Transpiler (`stalker2-ue5-asset-transpiler`)

Extracts, converts, and transpiles S.T.A.L.K.E.R. 2 Heart of Chornobyl (UE5 IoStore) assets into OGSR / X-Ray formats.

## Pipelines
- **IoStore Extraction:** Inspect and extract `.pak`, `.ucas`, `.utoc` containers via `repak` and `FModel`.
- **3D Meshes (.ogf & .dm):** Convert vegetation, trees, and props into 64-bit OGSR `.ogf` (models) and `.dm` (detail flora):
  `python3 ~/.claude/skills/stalker2-ue5-asset-transpiler/scripts/s2_vegetation_import.py`
  `python3 ~/.claude/skills/stalker2-ue5-asset-transpiler/scripts/write_ogf.py`
- **Asset Vault Management:** Monitor Steam drive space and harvest models/audio automatically.

## Related & Interoperating Skills
- **`stalker-ogsr-engine-porting`**: 64-bit S.T.A.L.K.E.R. OGSR/X-Ray migration, LuaJIT FFI, LTX inheritance, crash triage, and night ops.
- **`cross-engine-shader-rendering`**: Slang/SPIRV-Cross shader transpilation (Vulkan, DX12, HLSL, GLSL), Cook-Torrance GGX PBR, and bloom FX.
- **`standalone-binary-re`**: Native Linux zero-MCP reverse engineering: objdump, readelf, nm, rizin, gdb, JADX, and PE/ELF headers.

---
name: game-mod-release-packager
description: Automated game mod release packaging, archive compression, and distribution pipeline. Strips debug symbols (strip/objcopy), packs game virtual file systems (XDB, PAK, zip), validates SHA-256 checksums, and compiles GitHub / ModDB release distributions using ZoneForge tools.
---

# Game Mod Release Packager (`game-mod-release-packager`)

Once a game mod or engine port successfully passes autonomous testing, compiling the final public release distribution requires several error-prone manual steps: stripping debug symbols, packing assets into engine archives, validating checksums, and authoring release manifests.

This skill automates the complete packaging and distribution pipeline using **ZoneForge** and Linux systems utilities.

---

## 1. Binary Hardening & Debug Symbol Stripping

Releasing unstripped binaries bloats archive downloads by hundreds of megabytes and exposes internal debug paths:

```bash
# Stripping debug symbols while preserving export tables for DLLs:
objcopy --strip-debug bin_x64/xrEngine.exe bin_x64/xrEngine.exe
objcopy --strip-debug bin_x64/xrGame.dll bin_x64/xrGame.dll
objcopy --strip-debug bin_x64/xrRender_R4.dll bin_x64/xrRender_R4.dll

# Verifying binary stripping:
file bin_x64/*.dll | grep -E "(stripped|not stripped)"
```

---

## 2. VFS Archive Packing (ZoneForge & XDB)

Pack loose mod files into engine-native archives (`.xdb`, `.pack`) with optimal chunked compression:

```bash
# Packing mod directory using ZoneForge packaging engine:
zoneforge pack \
    --source ./gamedata \
    --output ./dist/gamedata.db_complete_merge \
    --format xdb \
    --compression zstd-fast \
    --exclude "*.bak,*.tmp,*.log,Thumbs.db"
```

### Packaging Integrity Checks:
- **Audio Headers:** Ensure all `.ogg` files retain the proprietary GSC binary comment header (`OGG_CHUNK_DATA`).
- **LTX Syntax:** Validate that packed `.ltx` configs have no trailing commas or malformed section inheritances.
- **Directory Mirroring:** Verify root paths match engine expectations (`gamedata/config/...`, `gamedata/scripts/...`).

---

## 3. Automated Manifest & Checksum Generation

Generate a cryptographically verifiable release manifest:

```bash
cd ./dist
sha256sum * > SHA256SUMS.txt
md5sum * > MD5SUMS.txt

# Generate high-density release metadata:
cat <<EOF > RELEASE_INFO.json
{
  "mod_name": "S.T.A.L.K.E.R. Complete - 64-bit OGSR Port",
  "version": "1.0.0",
  "build_date": "$(date -u +'%Y-%m-%d %H:%M:%SZ')",
  "target_engine": "OGSR Engine 64-bit (DX11)",
  "compatibility": ["Linux (Proton / Wine)", "Windows 10/11 x64"],
  "archives": [
    $(for f in *.db* *.zip; do [ -f "$f" ] && echo "{\"file\": \"$f\", \"size_mb\": $(du -m "$f" | cut -f1), \"sha256\": \"$(sha256sum "$f" | cut -d' ' -f1)\"},"; done | sed '$ s/,$//')
  ]
}
EOF
```

---

## 4. Distribution Summary

Conclude packaging with a clean release table:
- **Archive Size:** Total packed MB vs unpacked MB (compression efficiency ratio).
- **Checksum Verification:** Verified pass on all SHA-256 signatures.
- **Ready for Deployment:** Instant upload paths for ModDB, Nexus Mods, or Steam Workshop.

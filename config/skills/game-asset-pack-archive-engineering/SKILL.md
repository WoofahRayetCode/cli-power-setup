---
name: game-asset-pack-archive-engineering
description: Virtual file systems (VFS), game asset pack archive containers (PAK, XDB, AssetBundles), chunked zstd/zlib compression, memory-mapped I/O (mmap), and endianness-safe save state serialization. Use when designing asset loaders, porting game archives, or packaging game data distributions.
---

# Game Asset Packaging, Virtual File Systems & VFS Engineering

This skill defines the architecture for game data pack containers, Virtual File Systems (VFS), chunk-based decompression streaming, and cross-platform binary save game serialization.

---

## 1. Virtual File System (VFS) Architecture

A game engine should never call direct OS file APIs (`fopen`, `std::ifstream`) with hardcoded physical disk paths.
* **VFS Mount Point Hierarchy:**
  ```text
  /gamedata/textures/wall.dds
        │
        ├── 1. Mod Override Layer (Physical folder: /mods/hd_textures/) [High Priority]
        ├── 2. Patch Archive Layer (Mounted: patch_01.pak)              [Medium Priority]
        └── 3. Base Game Archive (Mounted: gamedata.pak)               [Base Priority]
  ```
* The VFS searches layers in reverse order of mounting, allowing seamless mod overrides without modifying vanilla files.

---

## 2. High-Performance Archive Container Format (VFS Header)

A production game archive consists of three distinct segments:
```text
┌────────────────────────────────────────────────────────┐
│ Header: Magic ('VPAK'), Version, Flags, TableOffset   │  (32 bytes)
├────────────────────────────────────────────────────────┤
│ Compressed Data Chunks (64KB - 256KB zstd chunks)      │  (Streaming Data)
├────────────────────────────────────────────────────────┤
│ File Index / TOC: [Hash, Offset, CompSize, RawSize]    │  (Table of Contents)
└────────────────────────────────────────────────────────┘
```

* **Chunked Decompression:** Never compress an entire 4GB archive as a single stream. Compress in independent **64KB chunks** so the engine can seek and decompress any asset in $<1\text{ms}$ without loading the entire archive into RAM.
* **Memory-Mapped I/O:** On 64-bit platforms, use `mmap` (Linux) / `MapViewOfFile` (Windows) to map the entire archive into virtual address space, letting the OS kernel handle asynchronous disk paging.

---

## 3. Endianness-Safe Binary Serialization

When porting games between architectures (e.g. big-endian PS3/Xbox 360 to little-endian PC x86-64 / ARM64):
* Always specify explicit fixed-width integer types (`uint32_t`, `int16_t`). Never serialize raw `int` or `long`.
* Implement byte-swapping macros on load:
  ```cpp
  inline uint32_t SwapLE32(uint32_t val) {
  #if __BYTE_ORDER__ == __ORDER_BIG_ENDIAN__
      return __builtin_bswap32(val);
  #else
      return val;
  #endif
  }
  ```

---

## 4. Automated VFS Asset Packer Utility

Run the included VFS pack utility to bundle asset folders into compressed containers:
```bash
python3 scripts/vfs_asset_packer.py --input path/to/assets --output gamedata.vpak --compress
```

---

## 5. Steam Library Archive Format Reference (Stage in `/dev/shm` RAM-Disk)
Always unpack and repack multi-gigabyte archives inside `/dev/shm` (`ramdisk-tmpfs-build-bake-accelerator`) to leverage 30 GB DDR5 RAM (`~40 GB/s`) with zero SSD wear:
- **X-Ray `.db` / `.xdb` / `.pack` (*S.T.A.L.K.E.R.* Trilogy & EE):** `zoneforge pack` / chunked LZHUF or Zstd VFS containers.
- **UE5 Zen IoStore `.utoc` / `.ucas` / `.pak` (*S.T.A.L.K.E.R. 2*, *Borderlands 4*, *Assetto Corsa Rally*):** Extract via `retoc to-legacy` (`liboo2corelinux64.so.9`), repack via `repak pack --compression Zstd` into `Content/Paks/~mods/zzzz_Mod_P.pak`.
- **Nightdive KEX `.kpf` (*SiN Reloaded*) & id Tech `.pk3`/`.pk4` (*Quake III*, *DOOM 3*):** Standard Deflate/Store ZIP containers.
- **Bethesda `.bsa` / `.ba2` (*Morrowind*, *Oblivion*, *Skyrim SE*, *Fallout 3/NV/4*, *Starfield*):** `BSA\x00` (LZ4) and `BTDX` (`GNRL` + `DX10` streamed BC1–BC7 mipmaps). Never set the compress flag on `.bsa` archives containing `.fuz`/`.xwm` voice audio.
- **Valve Source `.vpk` (*Half-Life 2*, *Black Mesa*, *GMod*, *L4D2*, *Portal 2*):** Multi-chunk `_dir.vpk` directory index + `_000.vpk` data chunks.


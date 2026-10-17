---
name: game-save-state-serialization
description: Robust game save system architecture, versioned schema migrations, bit-packed binary serialization, endianness safety, checksum validation, and atomic file replacement. Use when implementing save/load systems, retro game save states, or preventing save corruption.
---

# Game Save State & Serialization Pipeline

This skill defines standards for writing robust, forward-and-backward compatible game save files, memory-mapped checkpoints, and corruption-proof serialization.

---

## 1. Binary Container Layout (`.sav` / `.gstate`)

```text
+---------------------------------------------------------------+
| Magic Header: "GSAV" (4 bytes ASCII: 0x47, 0x53, 0x41, 0x56)   |
+---------------------------------------------------------------+
| Container Version: uint32 (e.g. 1)                            |
+---------------------------------------------------------------+
| Game Schema Version: uint32 (e.g. 104)                        |
+---------------------------------------------------------------+
| Timestamp: int64 (Unix epoch seconds)                         |
+---------------------------------------------------------------+
| Uncompressed Payload Size: uint64                             |
+---------------------------------------------------------------+
| Compressed Payload Size: uint64 (0 if uncompressed)           |
+---------------------------------------------------------------+
| Checksum: uint64 (XXH64 or CRC32 of uncompressed payload)     |
+---------------------------------------------------------------+
| Compression Type: uint8 (0 = None, 1 = Zstd, 2 = Zlib/Deflate)|
+---------------------------------------------------------------+
| Payload Data: Chunked Binary Sections                         |
+---------------------------------------------------------------+
```

---

## 2. Schema Migration & Version Resilience

* **Golden Rule of Backward Compatibility:**
  Never alter existing field order or semantic meanings in published schemas. Append new fields to the end of component chunks with explicit default fallbacks.
* **Chunked Tagged Blocks:**
  Serialize state into independent named or hashed sections:
  ```cpp
  struct ChunkHeader {
      uint32_t tag;    // e.g. 'PLYR', 'WRLD', 'INVT'
      uint32_t version;
      uint64_t byteSize;
  };
  ```
  If a newer save file contains unknown chunk tags, an older engine version safely skips `byteSize` bytes without crashing or corrupting adjacent blocks.

---

## 3. Atomic File Writing & Anti-Corruption Protocol

1. **Write to Temporary File:** Always serialize to `<filename>.tmp` first.
2. **Flush OS Buffers:** Call `fsync()` (Linux/macOS) or `FlushFileBuffers()` (Win32) to guarantee physical disk write.
3. **Atomic Replace:**
   * Linux: `rename(tmpPath, finalPath)` is POSIX-atomic.
   * Windows: `ReplaceFileW(finalPath, tmpPath, backupPath, 0, NULL, NULL)` ensures zero window of corruption if power loss occurs during save.
4. **Backup Ring Buffer:** Maintain `save_slot0.sav`, `save_slot0.sav.bak1`, `save_slot0.sav.bak2`.

---

## 4. Save State Inspector Helper

Use `scripts/save_state_inspector.py` to inspect, validate checksums, and dump chunk metadata from save files.

## Related & Interoperating Skills
- **`game-asset-pack-archive-engineering`**: Virtual file systems (VFS), game asset pack archive containers (PAK, XDB, AssetBundles), chunked zstd/zlib com...
- **`game-security-anti-tamper`**: Game engine runtime security, anti-tamper architectures, memory modification detection, DLL hijacking preventi...
- **`game-engine-migration`**: Universal architectural framework for porting, migrating, and modernizing game engines and legacy mods across ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

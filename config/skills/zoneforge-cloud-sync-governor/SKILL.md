---
name: zoneforge-cloud-sync-governor
description: Governs ZoneForge Google Drive and cloud asset synchronization, OAuth2 token refreshment, chunked resumable transfers, and local cache validation for large game mod distributions.
---

# ZoneForge Cloud Sync Governor (`zoneforge-cloud-sync-governor`)

ZoneForge distributes and synchronizes large S.T.A.L.K.E.R. mod packages, high-resolution texture packs, and virtual file systems (`.xdb`, `.pak`, `.zip`) across local developer workstations and remote Google Drive storage.

This skill provides operational safety for Google Drive integration (`src/zoneforge/drive.py`, `credentials.py`), handling quota limits, OAuth2 refresh tokens, chunked resumable transfers, and hash validation.

---

## 1. Authentication & Credential Architecture

- **Token Storage:** Encrypted or permission-locked (`chmod 600`) credential files in user config (`~/.config/zoneforge/credentials.json`).
- **Headless Refresh:** Automatically refreshes expired OAuth2 access tokens via refresh tokens without prompting for interactive browser authorization in CLI environments.
- **Never Log Secrets:** Client IDs, client secrets, and access tokens must never appear in chat transcripts, git commits, or shell logs.

---

## 2. Resumable Large Asset Transfers

For multi-gigabyte files (e.g. S.T.A.L.K.E.R. 2 texture dumps, packed XDB archives):

1. **Chunked Streaming:** Stream transfers in 8MB–32MB chunks to prevent memory bloat and connection resets.
2. **SHA-256 Checksums:** Compute and verify SHA-256 hashes pre-upload and post-download.
3. **Resumable State:** Persist partial transfer offsets to disk (`.zoneforge_partial_transfer.json`) to allow instant resumption if network drops.

---

## 3. CLI Verification Commands

```bash
# Verify Google Drive connectivity and storage quota
python3 -m zoneforge.cli drive status

# Upload packed mod archive with integrity check
python3 -m zoneforge.cli drive upload --file build/complete_ogsr_remaster.xdb0 --remote-folder "ZoneForge Builds" --verify-hash
```

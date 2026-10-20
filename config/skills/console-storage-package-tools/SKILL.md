---
name: console-storage-package-tools
description: FAT32 32KB cluster alignment, NSP/NSZ compression, XCI trimming, title ID mapping, and hactoolnet extraction.
---

# Console Storage & Package Tools (`console-storage-package-tools`)

MicroSD storage optimization, FAT32 cluster alignment, game package compression (NSP/NSZ/XCI), and cryptographic extraction.

## Critical Storage Invariants
- **FAT32 32KB Cluster Alignment:**
  Nintendo Switch Horizon OS experiences filesystem corruption when using exFAT. Always format SD cards to **FAT32** with **32KB clusters** (`mkfs.vfat -F 32 -s 64 /dev/sdX1` on Linux or `format /FS:FAT32 /A:32K` on Windows).
- **Package Management:**
  - **NSP & NSZ:** Compress Nintendo Submission Packages into compressed NSZ format using `nsz -D` (slashing file sizes by 40-70%).
  - **XCI Trimming:** Strip dummy garbage padding from game card dumps using `NSC_BUILDER`.
  - **Title ID & Ticket Extraction:** Parse and verify cryptographic NCAs using `hactoolnet --keyset prod.keys -t nca`.

## Related & Interoperating Skills
- **`console-emulation-toolchains`**: Console homebrew toolchains (devkitPro, libnx, devkitARM), emulator optimization (Ryujinx, RetroArch), and Obt...
- **`console-game-decompilation`**: Matching binary decompilation for console ROMs and retro binaries using Splat, m2c, and objdiff.
- **`nintendo-switch-homebrew`**: Nintendo Switch Atmosphere CFW, Hekate bootloader, sys-patch, emuMMC setup, RCM payloads, and archive bit fix.
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

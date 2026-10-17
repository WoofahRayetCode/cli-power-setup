---
name: console-homebrew-engineering
description: Console custom firmware (CFW) setups, Nintendo Switch Atmosphere/Hekate bootloaders, FAT32 32KB cluster alignment, NSP/NSZ package compression, and Obtainium emulator feeds.
---

# Console Homebrew Engineering & Softmodding Toolchain

This skill provides safety-critical procedures for gaming console softmodding, custom firmware (CFW) deployment, filesystem cluster alignment, and game package management.

---

## 🎮 1. Nintendo Switch CFW Architecture (Hekate & Atmosphere)

### 1. FAT32 32KB Cluster Formatting (Mandatory)
* **Never use exFAT:** The Nintendo Switch exFAT driver contains a fatal filesystem bug that inevitably corrupts data during homebrew read/write cycles.
* **32KB Cluster Size:** Format SD cards as FAT32 with exact 32KB cluster alignment to prevent "archive bit" corruption and slow boot times:
  ```bash
  # Linux: Format partition to FAT32 with 32KB clusters
  sudo mkfs.vfat -F 32 -s 64 -v /dev/sdX1
  ```

### 2. Bootloader Configuration (`bootloader/hekate_ipl.ini`)
* Maintain clean payload and autoboot configurations:
  ```ini
  [config]
  autoboot=0
  autoboot_list=0
  bootwait=3
  backlight=100
  autohosoff=0
  autonogc=1

  [CFW - emuMMC]
  fss0=atmosphere/package3
  kip1patch=nosigchk
  emummcforce=1
  icon=bootloader/res/icon_payload.bmp

  [Stock - sysMMC]
  fss0=atmosphere/package3
  emummc_force_disable=1
  stock=1
  icon=bootloader/res/icon_switch.bmp
  ```

### 3. emuMMC Raw Partition vs File-Based
* **Raw Partition (Recommended):** Creates an isolated 29.8GB hidden sector partition (`emummc.txt` type `raw_based`), preventing SD card fragmentation.
* **File-Based:** Stored in `/emuMMC/RAW1/eMMC/`; higher risk of file fragmentation on heavy writes.

---

## 📦 2. Package Management: NSP, NSZ, XCI & XCZ

* **NSZ / XCZ Compression:** Uses block-based zstandard (`zstd`) compression to reduce game file size by 40–60% without losing install compatibility.
* **Header & Ticket Verification:** Always verify cryptographic signatures (NCA headers) before installation to prevent boot panics.
* **Ticket Handling:** Ensure title keys are valid and matching console encryption keys (`prod.keys` / `title.keys`).

---

## 🕹️ 3. Emulation & Obtainium Repository Feeds

When managing emulator updates via Obtainium (e.g. `wlfryt-obtainium-emulators`):
* Track upstream GitHub releases using regex asset filters:
  ```json
  {
    "id": "vita3k",
    "url": "https://github.com/Vita3K/Vita3K-Android",
    "filter": "Vita3K.*\\.apk$",
    "versionExtraction": "release"
  }
  ```
* Separate **nightly builds** (unstable, experimental vulkan features) from **stable releases**.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`console-game-decompilation`**: Console game decompilation, matching reverse engineering, and disassembly workflows for PS1, PS2, PS3, origina...
- **`game-modding`**: Specialized workflows, format rules, and safety checks for game modding, focusing on S.T.A.L.K.E.R. Legends of...
- **`database-sql-engineering`**: SQLite performance tuning (WAL mode, PRAGMAs, indexing), PostgreSQL/MySQL schema design, query plan analysis, ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

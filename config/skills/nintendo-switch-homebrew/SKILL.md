---
name: nintendo-switch-homebrew
description: Nintendo Switch Atmosphere CFW, Hekate bootloader, sys-patch, emuMMC setup, RCM payloads, and archive bit fix.
---

# Nintendo Switch Homebrew & CFW (`nintendo-switch-homebrew`)

Custom firmware (CFW) bring-up, bootloader management, signature patching, and system maintenance for the Nintendo Switch.

## Core Architecture
- **Bootloader Configuration (`bootloader/hekate_ipl.ini`):**
  Configure Hekate launch profiles for `Atmosphere FSS0`, `Stock (sysMMC)`, and `emuMMC`. Set `autoboot` and `autohosoff`.
- **Atmosphere Components (`atmosphere/`):**
  - `package3`: Core OS system module loader.
  - `contents/`: Custom sysmodules (Tesla overlay menu, nx-ovlloader, sys-clk overclocking).
  - `hosts/default.txt`: DNS blocking entries (Nintendo telemetry blocklist) to prevent console bans.
- **Signature & System Patches:**
  Deploy `sys-patch` (`atmosphere/contents/420000000007E51A/`) for on-the-fly FS and ES patching.
- **Maintenance & Troubleshooting:**
  - **Archive Bit Fix:** If homebrew apps error after transfer on macOS/Linux, run Hekate's *Tools -> Arch bit -> Fix Archive Bit*.
  - **RCM Payload Injection:** Inject `fusee.bin` or `hekate.bin` via `tegrarcmgui` (Windows) or `fusee-launcher` (Linux).

## Related & Interoperating Skills
- **`modern-cpp-engineering`**: Modern C++20/23 standards, CMake 3.25+, RAII, smart pointers, 64-bit alignment, and memory sanitizers.
- **`console-emulation-toolchains`**: Console homebrew toolchains (devkitPro, libnx, devkitARM), emulator optimization (Ryujinx, RetroArch), and Obt...
- **`console-storage-package-tools`**: FAT32 32KB cluster alignment, NSP/NSZ compression, XCI trimming, title ID mapping, and hactoolnet extraction.
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

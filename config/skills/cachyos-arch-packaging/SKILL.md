---
name: cachyos-arch-packaging
description: Arch Linux and CachyOS packaging standards, PKGBUILD authoring, DKMS kernel module builds, and systemd service units. Use when building, testing, or maintaining packages like omen-acpi on CachyOS/Arch.
---

# Arch Linux & CachyOS Packaging & DKMS Guide

This skill governs package management, `PKGBUILD` creation, and DKMS kernel modules on **CachyOS / Arch Linux**.

## 1. PKGBUILD Standards
- Maintain Arch packaging guidelines:
  - Standard variables: `pkgname`, `pkgver`, `pkgrel`, `pkgdesc`, `arch=('x86_64')`, `license=('GPL-2.0-or-later')`, `depends`, `makedepends`.
  - Use `source=("$pkgname-$pkgver.tar.gz::https://...")` or local git references.
  - Checksums must match: use `sha256sums` or `b2sums`.
- Structure standard packaging functions:
  ```bash
  prepare() { ... }
  build() { ... }
  check() { ... }
  package() { ... }
  ```

## 2. DKMS Kernel Modules (e.g. Omen ACPI)
For out-of-tree Linux kernel drivers (`omen-acpi`):
- Provide `dkms.conf`:
  ```ini
  PACKAGE_NAME="omen-acpi"
  PACKAGE_VERSION="$pkgver"
  BUILT_MODULE_NAME[0]="omen_acpi"
  DEST_MODULE_LOCATION[0]="/kernel/drivers/platform/x86"
  AUTOINSTALL="yes"
  ```
- Install kernel headers dynamically matching the running kernel (`linux-cachyos-headers` or `linux-headers`).
- Test DKMS installation cleanly:
  ```bash
  sudo dkms add -m omen-acpi -v <version>
  sudo dkms build -m omen-acpi -v <version>
  sudo dkms install -m omen-acpi -v <version>
  ```

## 3. Systemd Unit Standards
- Place unit files in `/usr/lib/systemd/system/` for packaged services, or `/etc/systemd/system/` for local overrides.
- Explicitly define `[Unit]`, `[Service]`, and `[Install]` sections.
- Harden daemon services: use `ProtectSystem=full`, `ProtectHome=read-only`, and appropriate user/group privileges where applicable.

## 4. Verification
- Validate with `namcap PKGBUILD` and `namcap <built-package>.pkg.tar.zst`.
- Ensure clean builds in a chroot or local directory without polluting the host root.

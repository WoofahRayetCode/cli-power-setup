---
name: android-rom-os-engineering
description: Android custom ROM development, AOSP and LineageOS device tree bring-up, proprietary vendor blob extraction, kernel defconfigs, dynamic super partition sizing, and SELinux sepolicy denial triage.
---

# Android Custom ROM & OS Engineering

The **Android Custom ROM & OS Engineering** skill guides the architecture, device tree bring-up, proprietary blob extraction, kernel integration, and SELinux policy engineering required to build and port **AOSP**, **LineageOS**, and custom Android operating systems.

---

## 🎯 When to Activate

* **Device Tree Bring-Up:** Scaffolding and configuring `device/<vendor>/<codename>/` (`BoardConfig.mk`, `device.mk`, `AndroidProducts.mk`).
* **Proprietary Vendor Blob Extraction:** Extracting vendor blobs (`.so`, firmware, HALs) from OEM stock firmware (`payload.bin`, `super.img`) and authoring `proprietary-files.txt`.
* **Dynamic Super Partition Allocation:** Calculating dynamic partition group boundaries and sizing `system`, `vendor`, `product`, and `system_ext` against the physical UFS/eMMC `BOARD_SUPER_PARTITION_SIZE`.
* **SELinux Denial Resolution:** Parsing `avc: denied` violations in `logcat`/`dmesg` to author precise `.te` policy allow rules while maintaining an `Enforcing` security posture.
* **Bootloop & HAL Triage:** Debugging initialization failures across SurfaceFlinger, Camera HALs, Audio policy, RIL (telephony), and VINTF compatibility matrices.

---

## 🏗️ The 5 Architectural Pillars

### 1. Build Environment (`repo` & Soong)
* **Manifest Management:** Local device manifests are placed in `.repo/local_manifests/<device>.xml` declaring device, kernel, and vendor repositories.
* **Build Initialization:**
  ```bash
  source build/envsetup.sh
  lunch lineage_<codename>-userdebug
  mka bacon -j$(nproc)
  ```

### 2. Device Tree (`device/<vendor>/<codename>/`)
* **`BoardConfig.mk`:** Hardware constraints, CPU architecture (ARM64 `armv8-a`), bootloader parameters, kernel cmdline, dynamic partition groups, and recovery settings.
* **`device.mk`:** Packages, audio/media XML configs, permission files, and Runtime Resource Overlays (RROs) for notch cutouts, status bar padding, and display refresh rates.
* **`AndroidProducts.mk`:** Product definitions and lunch choice declarations.

### 3. Proprietary Vendor Blobs (`vendor/<vendor>/<codename>/`)
* Extract closed-source silicon libraries (Qualcomm QTI, MediaTek, Exynos) from factory ROMs:
  - Unpack OTA packages: `payload_dumper payload.bin --out dump/`
  - Unpack dynamic partitions: `lpunpack super.img ./super_extracted/`
  - Run Lineage extraction: `./extract-files.sh /path/to/dump`

### 4. Kernel, GKI & DTBOs (`kernel/<vendor>/<soc>/`)
* In modern Android (Android 12/13/14/15+), devices build with **GKI (Generic Kernel Image)** architecture.
* Device-specific logic is isolated into Loadable Kernel Modules (`.ko`), Device Tree Blobs (DTB), and Device Tree Overlays (DTBO) flashed to the `dtbo` partition.

### 5. SELinux & SEPolicy (`sepolicy/vendor/`)
* Never leave ROMs in `Permissive` mode. Enforce strict type enforcement:
  - File contexts: `file_contexts` associates filesystem paths with security labels (`/vendor/bin/hw/android\.hardware\.camera.* u:object_r:hal_camera_default_exec:s0`).
  - Type rules: `camera.te` allows specific operations:
    ```sepolicy
    allow hal_camera_default vendor_persist_camera_file:dir { search read open };
    ```

---

## 🛠️ CLI Toolkit (`android_rom_tools.py`)

The skill includes a dedicated engineering helper at `scripts/android_rom_tools.py`.

### 1. Scaffold a Device Tree Skeleton
Quickly generates the complete file structure and configuration makefiles for a new target device:
```bash
python3 config/skills/android-rom-os-engineering/scripts/android_rom_tools.py scaffold \
  --vendor "xiaomi" \
  --codename "alioth" \
  --soc "qcom" \
  --output device/xiaomi/alioth
```

### 2. Parse AVC Denials into SELinux `.te` Allow Rules
Extracts all `avc: denied` audit entries from a captured logcat or dmesg dump and outputs deduplicated `.te` policy allow statements:
```bash
python3 config/skills/android-rom-os-engineering/scripts/android_rom_tools.py parse-avc \
  --log /tmp/dmesg_boot.txt \
  --output device/xiaomi/alioth/sepolicy/vendor/generated_allow.te
```

### 3. Dynamic Super Partition Budget Calculation
Validates sub-partition sizes against total physical super partition storage to prevent flashing overflow errors:
```bash
python3 config/skills/android-rom-os-engineering/scripts/android_rom_tools.py calc-partitions \
  --super-mb 9126 \
  --system-mb 3500 \
  --vendor-mb 1200 \
  --product-mb 2500 \
  --system-ext-mb 800
```

### 4. VINTF Device Compatibility Linting
Validates that essential HAL providers (audio, camera, composer, sensors, wifi) are properly declared in `manifest.xml`:
```bash
python3 config/skills/android-rom-os-engineering/scripts/android_rom_tools.py vintf-lint \
  --manifest device/xiaomi/alioth/configs/vintf/manifest.xml
```

---

## 🩺 Bootloop Triage Matrix

| Stage | Logcat / dmesg Signature | Root Cause | Exact Resolution |
| :--- | :--- | :--- | :--- |
| **Early Init** | `init: Service '...' exited with status 1` | Daemon failed to start due to missing library or bad permission. | Check `strace` or library dependencies via `readelf -d` on the failing binary. |
| **SELinux** | `avc: denied { read } for comm="surfaceflinger"` | Enforcing mode blocked access to display nodes. | Run `android_rom_tools.py parse-avc` on the log and add missing rule to `sepolicy/`. |
| **SurfaceFlinger** | `E Gralloc: failed to load gralloc HAL` | Missing graphics/EGL proprietary blobs. | Verify `vendor/lib64/hw/gralloc.*.so` exists in `proprietary-files.txt`. |
| **SystemServer** | `VintfObject::checkCompatibility failed` | System framework requires a HAL version that vendor does not declare. | Check `manifest.xml` and update FCM compatibility matrix. |
| **Audio/RIL** | `audioserver: AudioFlinger could not be initialized` | Missing `audio_policy_configuration.xml` or broken vendor audio HAL. | Ensure audio XML routing configs are copied in `device.mk`. |

#!/usr/bin/env python3
"""
Android Custom ROM & OS Engineering Toolkit (android_rom_tools.py)
Automates device tree scaffolding, SELinux avc denial parsing into .te rules,
dynamic partition sizing calculations, and VINTF manifest linting.
"""

import argparse
import os
import re
import sys
from pathlib import Path

def cmd_scaffold(args):
    vendor = args.vendor.lower().strip()
    codename = args.codename.lower().strip()
    soc = args.soc or "qcom"
    out_dir = Path(args.output or f"device/{vendor}/{codename}")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. AndroidProducts.mk
    prod_mk = out_dir / "AndroidProducts.mk"
    prod_mk.write_text(f"""PRODUCT_MAKEFILES := \\
    $(LOCAL_DIR)/lineage_{codename}.mk

COMMON_LUNCH_CHOICES := \\
    lineage_{codename}-user \\
    lineage_{codename}-userdebug \\
    lineage_{codename}-eng
""", encoding="utf-8")

    # 2. lineage_<codename>.mk
    rom_mk = out_dir / f"lineage_{codename}.mk"
    rom_mk.write_text(f"""# Inherit from common AOSP / Lineage products
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Inherit device configurations
$(call inherit-product, device/{vendor}/{codename}/device.mk)

# Device identifier
PRODUCT_NAME := lineage_{codename}
PRODUCT_DEVICE := {codename}
PRODUCT_BRAND := {vendor.capitalize()}
PRODUCT_MODEL := {codename.upper()}
PRODUCT_MANUFACTURER := {vendor.capitalize()}
""", encoding="utf-8")

    # 3. BoardConfig.mk
    board_mk = out_dir / "BoardConfig.mk"
    board_mk.write_text(f"""# Architecture
TARGET_ARCH := arm64
TARGET_ARCH_VARIANT := armv8-a
TARGET_CPU_ABI := arm64-v8a
TARGET_CPU_ABI2 :=
TARGET_CPU_VARIANT := generic

TARGET_2ND_ARCH := arm
TARGET_2ND_ARCH_VARIANT := armv8-a
TARGET_2ND_CPU_ABI := armeabi-v7a
TARGET_2ND_CPU_ABI2 := armeabi
TARGET_2ND_CPU_VARIANT := generic

# Kernel
BOARD_KERNEL_CMDLINE := console=ttyMSM0,115200n8 androidboot.hardware={soc}
BOARD_BOOT_HEADER_VERSION := 2
BOARD_KERNEL_IMAGE_NAME := Image.gz-dtb
TARGET_KERNEL_ARCH := arm64
TARGET_KERNEL_HEADER_ARCH := arm64

# Partitions & Dynamic Super
BOARD_SUPER_PARTITION_SIZE := 9126805504
BOARD_SUPER_PARTITION_GROUPS := {vendor}_dynamic_partitions
BOARD_{vendor.upper()}_DYNAMIC_PARTITIONS_SIZE := 9122611200
BOARD_{vendor.upper()}_DYNAMIC_PARTITIONS_PARTITION_LIST := system vendor product system_ext

BOARD_FLASH_BLOCK_SIZE := 262144
TARGET_USERIMAGES_USE_EXT4 := true
TARGET_COPY_OUT_VENDOR := vendor
TARGET_COPY_OUT_PRODUCT := product
TARGET_COPY_OUT_SYSTEM_EXT := system_ext

# SELinux
BOARD_VENDOR_SEPOLICY_DIRS += device/{vendor}/{codename}/sepolicy/vendor
""", encoding="utf-8")

    # 4. device.mk
    device_mk = out_dir / "device.mk"
    device_mk.write_text(f"""# Proprietary vendor blobs
$(call inherit-product, vendor/{vendor}/{codename}/{codename}-vendor.mk)

# Overlays
DEVICE_PACKAGE_OVERLAYS += device/{vendor}/{codename}/overlay

# Permissions
PRODUCT_COPY_FILES += \\
    frameworks/native/data/etc/android.hardware.telephony.gsm.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.telephony.gsm.xml \\
    frameworks/native/data/etc/android.hardware.wifi.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.wifi.xml

# Dynamic Partitions
PRODUCT_USE_DYNAMIC_PARTITIONS := true
""", encoding="utf-8")

    # 5. sepolicy directory
    sepolicy_dir = out_dir / "sepolicy" / "vendor"
    sepolicy_dir.mkdir(parents=True, exist_ok=True)
    (sepolicy_dir / "file_contexts").write_text("# Vendor file contexts\n", encoding="utf-8")

    print(f"\n=======================================================")
    print(f" 📱 Android Device Tree Scaffolded Successfully       ")
    print(f"=======================================================")
    print(f"Vendor:          {vendor}")
    print(f"Codename:        {codename}")
    print(f"SoC Target:      {soc}")
    print(f"Device Directory: {out_dir}")
    print(f"Files Created:")
    print(f"  - AndroidProducts.mk")
    print(f"  - lineage_{codename}.mk")
    print(f"  - BoardConfig.mk (Arm64, Dynamic Super Partitions)")
    print(f"  - device.mk")
    print(f"  - sepolicy/vendor/file_contexts")
    print(f"=======================================================\n")

def cmd_parse_avc(args):
    log_file = Path(args.log)
    if not log_file.exists():
        print(f"Error: Log file '{log_file}' not found.", file=sys.stderr)
        sys.exit(1)
        
    content = log_file.read_text(encoding="utf-8", errors="ignore")
    # Pattern: avc:  denied  { perm1 perm2 } for  comm="xyz" ... scontext=u:r:source_t:s0 tcontext=u:object_r:target_t:s0 tclass=class_t
    avc_pattern = re.compile(
        r'avc:\s+denied\s+\{\s*([^}]+)\s*\}\s+for\s+.*?'
        r'scontext=u:r:([^:]+):s0\s+tcontext=u:(?:object_r|r):([^:]+):s0\s+tclass=([^\s]+)'
    )
    
    rules = {}
    matches = avc_pattern.findall(content)
    
    for perms_str, scontext, tcontext, tclass in matches:
        perms = set(perms_str.strip().split())
        key = (scontext, tcontext, tclass)
        if key not in rules:
            rules[key] = set()
        rules[key].update(perms)
        
    out_lines = []
    out_lines.append("# Generated SELinux Allow Rules from AVC Denials")
    out_lines.append(f"# Source: {log_file.name} | Total Unique Violations: {len(rules)}\n")
    
    for (scontext, tcontext, tclass), perms in sorted(rules.items()):
        perms_formatted = " ".join(sorted(perms))
        out_lines.append(f"allow {scontext} {tcontext}:{tclass} {{ {perms_formatted} }};")
        
    result_text = "\n".join(out_lines) + "\n"
    
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result_text, encoding="utf-8")
        print(f"[✓] Extracted {len(rules)} SELinux policy rules written to: {out_path}")
    else:
        print(f"\n=======================================================")
        print(f" 🛡️ Extracted SELinux Allow Rules ({len(rules)} rules) ")
        print(f"=======================================================")
        print(result_text)
        print(f"=======================================================\n")

def cmd_calc_partitions(args):
    super_size_mb = args.super_mb
    system_mb = args.system_mb
    vendor_mb = args.vendor_mb
    product_mb = args.product_mb
    system_ext_mb = args.system_ext_mb
    
    allocated = system_mb + vendor_mb + product_mb + system_ext_mb
    headroom = super_size_mb - allocated
    
    print(f"\n=======================================================")
    print(f" 💾 Android Dynamic Super Partition Budget             ")
    print(f"=======================================================")
    print(f"Total Super Size:        {super_size_mb} MB ({super_size_mb * 1024 * 1024:,} bytes)")
    print(f"  - system:              {system_mb} MB")
    print(f"  - vendor:              {vendor_mb} MB")
    print(f"  - product:             {product_mb} MB")
    print(f"  - system_ext:          {system_ext_mb} MB")
    print(f"Total Allocated:         {allocated} MB")
    print(f"Free Headroom:           {headroom} MB")
    
    if headroom < 0:
        print(f"\n🚨 [CRITICAL ERROR] Partition budget exceeded by {-headroom} MB!")
        print(f"Your images will not fit into the physical super partition.")
        sys.exit(2)
    elif headroom < 100:
        print(f"\n⚠️ [WARNING] Very tight margin ({headroom} MB). Consider reducing image sizing.")
    else:
        print(f"\n🟢 [HEALTHY] Super partition budget is well balanced.")
    print(f"=======================================================\n")

def cmd_vintf_lint(args):
    manifest_file = Path(args.manifest)
    if not manifest_file.exists():
        print(f"Error: Manifest file '{manifest_file}' not found.", file=sys.stderr)
        sys.exit(1)
        
    content = manifest_file.read_text(encoding="utf-8")
    essential_hals = [
        "android.hardware.audio",
        "android.hardware.camera.provider",
        "android.hardware.graphics.allocator",
        "android.hardware.graphics.composer",
        "android.hardware.keymaster",
        "android.hardware.sensors",
        "android.hardware.wifi"
    ]
    
    missing = []
    for hal in essential_hals:
        if hal not in content:
            missing.append(hal)
            
    print(f"\n=======================================================")
    print(f" 🔍 VINTF Compatibility Matrix Lint: {manifest_file.name} ")
    print(f"=======================================================")
    if missing:
        print(f"⚠️ Missing Essential HAL Service Declarations ({len(missing)}):")
        for m in missing:
            print(f"  - {m}")
        print(f"\nResult: Review device HAL configurations before lunch build.")
    else:
        print(f"🟢 All essential hardware HAL declarations found in manifest.")
        print(f"Result: Manifest passes basic VINTF compliance check.")
    print(f"=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="Android Custom ROM & OS Engineering Toolkit")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # scaffold
    p_scaf = subparsers.add_parser("scaffold", help="Scaffold a device tree skeleton")
    p_scaf.add_argument("--vendor", required=True, help="OEM Vendor (e.g. xiaomi, oneplus, google)")
    p_scaf.add_argument("--codename", required=True, help="Device Codename (e.g. alioth, kebab, cheetah)")
    p_scaf.add_argument("--soc", default="qcom", help="SoC Target (qcom, mtk, tensor, exynos)")
    p_scaf.add_argument("--output", help="Output directory path")
    
    # parse-avc
    p_avc = subparsers.add_parser("parse-avc", help="Parse dmesg/logcat avc denials into .te rules")
    p_avc.add_argument("--log", required=True, help="Path to dmesg or logcat text file")
    p_avc.add_argument("--output", help="Output file path for generated .te rules")
    
    # calc-partitions
    p_part = subparsers.add_parser("calc-partitions", help="Calculate dynamic super partition budgets")
    p_part.add_argument("--super-mb", type=int, default=9126, help="Total Super partition size in MB")
    p_part.add_argument("--system-mb", type=int, default=3500, help="System image size in MB")
    p_part.add_argument("--vendor-mb", type=int, default=1500, help="Vendor image size in MB")
    p_part.add_argument("--product-mb", type=int, default=2500, help="Product image size in MB")
    p_part.add_argument("--system-ext-mb", type=int, default=800, help="System_ext image size in MB")
    
    # vintf-lint
    p_vintf = subparsers.add_parser("vintf-lint", help="Lint VINTF device manifest.xml")
    p_vintf.add_argument("--manifest", required=True, help="Path to manifest.xml")
    
    args = parser.parse_args()
    
    if args.command == "scaffold":
        cmd_scaffold(args)
    elif args.command == "parse-avc":
        cmd_parse_avc(args)
    elif args.command == "calc-partitions":
        cmd_calc_partitions(args)
    elif args.command == "vintf-lint":
        cmd_vintf_lint(args)

if __name__ == "__main__":
    main()

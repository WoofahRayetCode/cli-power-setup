#!/usr/bin/env python3
"""
LAA PE Patcher: Large Address Aware (4GB Patch) Inspector & Utility.
Checks and toggles the IMAGE_FILE_LARGE_ADDRESS_AWARE (0x0020) flag in Windows PE32 binaries.
Prevents 32-bit game crashes on modern Windows & Linux/Proton systems.
"""

import sys
import os
import struct
import argparse
from pathlib import Path

IMAGE_FILE_LARGE_ADDRESS_AWARE = 0x0020

def check_pe_laa(filepath: str) -> tuple[bool, int, int]:
    """Inspects a PE file and returns (is_laa_enabled, characteristics_offset, current_flags)."""
    with open(filepath, "rb") as f:
        # Check MZ header
        mz = f.read(2)
        if mz != b"MZ":
            raise ValueError(f"Not a valid PE executable (magic header != MZ): {filepath}")
        
        # Seek to e_lfanew (pointer to PE header at offset 0x3C)
        f.seek(0x3C)
        pe_offset = struct.unpack("<I", f.read(4))[0]
        
        # Seek to PE signature
        f.seek(pe_offset)
        pe_sig = f.read(4)
        if pe_sig != b"PE\x00\x00":
            raise ValueError(f"Invalid PE signature: {pe_sig}")
            
        # COFF File Header is 20 bytes long
        # Offset 0: Machine (2 bytes)
        # Offset 18: Characteristics (2 bytes)
        char_offset = pe_offset + 4 + 18
        f.seek(char_offset)
        characteristics = struct.unpack("<H", f.read(2))[0]
        
        is_laa = bool(characteristics & IMAGE_FILE_LARGE_ADDRESS_AWARE)
        return is_laa, char_offset, characteristics

def set_pe_laa(filepath: str, enable: bool = True):
    """Enables or disables the LAA flag in a PE executable."""
    is_laa, char_offset, characteristics = check_pe_laa(filepath)
    
    if enable and is_laa:
        print(f"[✓] {filepath}: Large Address Aware (4GB) flag is ALREADY enabled.")
        return
    if not enable and not is_laa:
        print(f"[✓] {filepath}: Large Address Aware (4GB) flag is ALREADY disabled.")
        return
        
    new_char = (characteristics | IMAGE_FILE_LARGE_ADDRESS_AWARE) if enable else (characteristics & ~IMAGE_FILE_LARGE_ADDRESS_AWARE)
    
    # Create safety backup if not already present
    backup_path = filepath + ".bak"
    if not os.path.exists(backup_path):
        import shutil
        shutil.copy2(filepath, backup_path)
        print(f"[+] Created safety backup at {backup_path}")
        
    with open(filepath, "r+b") as f:
        f.seek(char_offset)
        f.write(struct.pack("<H", new_char))
        
    status = "ENABLED" if enable else "DISABLED"
    print(f"[★] SUCCESS: Large Address Aware (4GB) flag {status} for {filepath}")
    print(f"    Characteristics modified: 0x{characteristics:04X} -> 0x{new_char:04X}")

def main():
    parser = argparse.ArgumentParser(description="Inspect and patch Large Address Aware (4GB LAA) flag on 32-bit PE binaries.")
    parser.add_argument("binary", help="Path to the .exe target binary")
    parser.add_argument("--enable", action="store_true", help="Enable Large Address Aware flag (allow 4GB virtual address space)")
    parser.add_argument("--disable", action="store_true", help="Disable Large Address Aware flag")
    
    args = parser.parse_args()
    if not os.path.isfile(args.binary):
        print(f"[-] Error: Target file '{args.binary}' not found.", file=sys.stderr)
        sys.exit(1)
        
    try:
        if args.enable:
            set_pe_laa(args.binary, enable=True)
        elif args.disable:
            set_pe_laa(args.binary, enable=False)
        else:
            is_laa, offset, char = check_pe_laa(args.binary)
            status = "ENABLED (4GB address space unlocked)" if is_laa else "DISABLED (capped at 2GB, vulnerable to CTD memory exhaustion)"
            print(f"Target: {args.binary}")
            print(f"Header Characteristics: 0x{char:04X}")
            print(f"LAA Status: {status}")
            if not is_laa:
                print("Tip: Run with --enable to patch binary for 4GB address space.")
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

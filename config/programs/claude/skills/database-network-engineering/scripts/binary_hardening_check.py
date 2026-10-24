#!/usr/bin/env python3
import sys
import struct
import argparse
from pathlib import Path

def inspect_elf(file_path: Path):
    if not file_path.exists():
        print(f"[!] Error: File not found: {file_path}", file=sys.stderr)
        return 1

    data = file_path.read_bytes()
    if len(data) < 64 or data[:4] != b"\x7fELF":
        print(f"[!] Error: Not a valid ELF binary: {file_path}", file=sys.stderr)
        return 1

    ei_class = data[4] # 1 = 32-bit, 2 = 64-bit
    is_64 = (ei_class == 2)
    
    # Read e_type (offset 16, uint16)
    e_type = struct.unpack_from("<H", data, 16)[0]
    is_pie = (e_type == 3) # ET_DYN (Shared object / PIE executable)

    # Search for program headers
    if is_64:
        e_phoff = struct.unpack_from("<Q", data, 32)[0]
        e_phentsize = struct.unpack_from("<H", data, 54)[0]
        e_phnum = struct.unpack_from("<H", data, 56)[0]
    else:
        e_phoff = struct.unpack_from("<I", data, 28)[0]
        e_phentsize = struct.unpack_from("<H", data, 42)[0]
        e_phnum = struct.unpack_from("<H", data, 44)[0]

    has_nx = False
    has_relro = False
    has_bind_now = False

    PT_GNU_STACK = 0x6474e551
    PT_GNU_RELRO = 0x6474e552

    for i in range(e_phnum):
        offset = e_phoff + (i * e_phentsize)
        if offset + 32 > len(data):
            break
        p_type = struct.unpack_from("<I", data, offset)[0]
        
        if p_type == PT_GNU_STACK:
            # Flags offset: 4 in 64-bit, 24 in 32-bit
            flags = struct.unpack_from("<I", data, offset + (4 if is_64 else 24))[0]
            # PF_X = 1. If PF_X is NOT set, stack is non-executable (NX enabled)
            if (flags & 1) == 0:
                has_nx = True
        elif p_type == PT_GNU_RELRO:
            has_relro = True

    # Check for stack canary symbol
    has_canary = b"__stack_chk_fail" in data

    # Check for full relro via BIND_NOW dynamic flag
    has_bind_now = b"BIND_NOW" in data or b"\x18\x00\x00\x00" in data

    print("=" * 60)
    print(f" 🛡️  Binary Hardening Audit (checksec): {file_path.name}")
    print("=" * 60)
    print(f" Architecture:     {'64-bit ELF' if is_64 else '32-bit ELF'}")
    
    # RELRO
    if has_relro and has_bind_now:
        print(" RELRO:            [32mFull RELRO[0m")
    elif has_relro:
        print(" RELRO:            [33mPartial RELRO[0m")
    else:
        print(" RELRO:            [31mNo RELRO[0m")

    # Stack Canary
    if has_canary:
        print(" Stack Canary:     [32mEnabled (__stack_chk_fail)[0m")
    else:
        print(" Stack Canary:     [31mDisabled / None detected[0m")

    # NX
    if has_nx:
        print(" NX (DEP):         [32mEnabled (Non-executable stack)[0m")
    else:
        print(" NX (DEP):         [31mDisabled (Executable stack risk)[0m")

    # PIE
    if is_pie:
        print(" PIE:              [32mPIE Enabled (Full ASLR Support)[0m")
    else:
        print(" PIE:              [31mNo PIE (Fixed Base Address)[0m")

    print("=" * 60)
    return 0

def main():
    parser = argparse.ArgumentParser(description="Standalone Binary Hardening Inspector (checksec)")
    parser.add_argument("binary", type=Path, help="Path to ELF binary or shared object (.so)")
    args = parser.parse_args()

    sys.exit(inspect_elf(args.binary))

if __name__ == "__main__":
    main()

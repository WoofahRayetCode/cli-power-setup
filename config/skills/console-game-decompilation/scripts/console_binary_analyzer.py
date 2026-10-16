#!/usr/bin/env python3
"""
Console Game Binary Analyzer & Decompilation Scaffold Generator.
Inspects PS1 (PS-X EXE), PS2 (ELF32 MIPS), PS3 (ELF64 PPC/Cell),
Original Xbox (XBE), and Xbox 360 (XEX) binaries.
Generates splat-compatible split configurations and decomp skeletons.
Zero external dependencies.
"""
import sys
import os
import struct
import json
import argparse
from pathlib import Path

def identify_console_binary(file_path: Path):
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    data = file_path.read_bytes()
    size = len(data)
    if size < 16:
        return {"type": "unknown", "error": "File too small"}

    # 1. PS-X EXE (PS1)
    if data.startswith(b"PS-X EXE"):
        initial_pc, initial_gp, text_addr, text_size = struct.unpack("<IIII", data[0x10:0x20])
        return {
            "type": "PS1",
            "format": "PS-X EXE",
            "architecture": "MIPS I (R3000A)",
            "file_size": size,
            "entry_point": hex(initial_pc),
            "initial_gp": hex(initial_gp),
            "load_address": hex(text_addr),
            "text_size": text_size,
            "data_offset": 0x800  # Standard PS-X EXE header size
        }

    # 2. ELF (PS2 / PS3)
    if data.startswith(b"\x7fELF"):
        bitness = data[4]
        endian = data[5]
        endian_char = "<" if endian == 1 else ">"

        if bitness == 1:  # 32-bit (PS2)
            e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags = struct.unpack(
                f"{endian_char}HHIIIII", data[16:40]
            )
            arch = "MIPS III / R5900 (PS2 Emotion Engine)" if e_machine == 8 else f"MIPS (machine {e_machine})"
            return {
                "type": "PS2",
                "format": "ELF32",
                "architecture": arch,
                "endianness": "little" if endian == 1 else "big",
                "file_size": size,
                "entry_point": hex(e_entry),
                "ph_offset": e_phoff,
                "sh_offset": e_shoff,
                "flags": hex(e_flags)
            }
        elif bitness == 2:  # 64-bit (PS3 Cell / PowerPC)
            e_type, e_machine, e_version, e_entry, e_phoff, e_shoff, e_flags = struct.unpack(
                f"{endian_char}HHIQQQI", data[16:48]
            )
            arch = "PowerPC 64 (PS3 Cell PPE/SPE)" if e_machine in (20, 21) else f"PPC64 (machine {e_machine})"
            return {
                "type": "PS3",
                "format": "ELF64",
                "architecture": arch,
                "endianness": "big" if endian == 2 else "little",
                "file_size": size,
                "entry_point": hex(e_entry),
                "ph_offset": e_phoff,
                "sh_offset": e_shoff,
                "flags": hex(e_flags)
            }

    # 3. Original Xbox (XBE)
    if data.startswith(b"XBEH"):
        base_addr, headers_size, image_size, image_header_size, timestamp = struct.unpack(
            "<IIIII", data[0x104:0x118]
        )
        cert_addr, sections_count, section_headers_addr = struct.unpack(
            "<III", data[0x118:0x124]
        )
        entry_addr = struct.unpack("<I", data[0x13C:0x140])[0]
        # XBE entry points are XOR-encoded in retail builds (XOR key: 0x5B6D40B6 for retail)
        return {
            "type": "Xbox",
            "format": "XBE (Xbox Executable)",
            "architecture": "x86-32 (Intel Pentium III / Coppermine)",
            "file_size": size,
            "base_address": hex(base_addr),
            "raw_entry_point": hex(entry_addr),
            "sections_count": sections_count,
            "headers_size": headers_size,
            "image_size": image_size
        }

    # 4. Xbox 360 (XEX / XEX2)
    if data.startswith(b"XEX2") or data.startswith(b"XEX1") or data.startswith(b"XEX%"):
        magic = data[:4].decode("latin1", errors="ignore")
        module_flags, pe_offset, sec_info_offset, cert_count = struct.unpack(
            ">IIII", data[4:20]
        )
        return {
            "type": "Xbox 360",
            "format": f"XEX ({magic})",
            "architecture": "PowerPC 64 (Xenon 3-core 6-thread)",
            "endianness": "big",
            "file_size": size,
            "module_flags": hex(module_flags),
            "pe_offset": hex(pe_offset),
            "security_info_offset": hex(sec_info_offset),
            "cert_count": cert_count
        }

    # 5. Nintendo GameCube / Wii (DOL executable)
    # Check for text/data section offset tables (standard DOL starts with 7 text + 11 data offsets)
    if size >= 0x100:
        t0_offset, t1_offset, t2_offset = struct.unpack(">III", data[:12])
        if t0_offset == 0x100 and t1_offset < size and t2_offset < size:
            return {
                "type": "GameCube/Wii",
                "format": "DOL Executable",
                "architecture": "PowerPC 750 (Gekko / Broadway)",
                "endianness": "big",
                "file_size": size,
                "first_text_offset": hex(t0_offset)
            }

    return {
        "type": "Unknown",
        "format": "Raw Binary",
        "file_size": size,
        "magic_hex": data[:8].hex()
    }

def generate_splat_config(info: dict, binary_path: Path):
    name = binary_path.stem
    btype = info.get("type", "Generic")

    config = {
        "name": name,
        "platform": btype.lower(),
        "architecture": info.get("architecture", "mips"),
        "options": {
            "find_file_boundaries": True,
            "compiler": "GCC" if btype in ("PS1", "PS2") else "MSVC",
            "base_path": "src",
            "target_path": str(binary_path)
        },
        "segments": [
            {
                "name": "header",
                "type": "header",
                "start": 0,
                "vram": info.get("load_address", "0x80010000")
            },
            {
                "name": "main_text",
                "type": "c",
                "start": info.get("data_offset", 0x800),
                "vram": info.get("entry_point", "0x80010000"),
                "subsegments": [
                    [info.get("data_offset", 0x800), "asm", "entry"]
                ]
            }
        ]
    }
    return config

def main():
    parser = argparse.ArgumentParser(description="Console Game Binary Decompilation Analyzer")
    parser.add_argument("binary", help="Path to executable (PS-X EXE, ELF, XBE, XEX, DOL)")
    parser.add_argument("--json", action="store_true", help="Output JSON results")
    parser.add_argument("--splat", action="store_true", help="Generate splat split YAML configuration")
    parser.add_argument("--out-dir", default="decomp", help="Target output directory for decomp skeleton")

    args = parser.parse_args()
    bin_path = Path(args.binary)

    try:
        info = identify_console_binary(bin_path)
    except Exception as e:
        print(f"[!] Error reading binary: {e}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(info, indent=2))
        return

    print("=" * 65)
    print(f" 🎮 Console Binary Decompilation Analysis: {bin_path.name}")
    print("=" * 65)
    for k, v in info.items():
        print(f"  • {k.replace('_', ' ').title():<22}: {v}")
    print("-" * 65)

    if args.splat:
        splat_cfg = generate_splat_config(info, bin_path)
        out_yaml = Path(args.out_dir) / f"{bin_path.stem}.yaml"
        out_yaml.parent.mkdir(parents=True, exist_ok=True)
        # Simple YAML serialization
        import yaml
        try:
            out_yaml.write_text(yaml.dump(splat_cfg, sort_keys=False), encoding="utf-8")
            print(f"[✓] Generated splat split config: {out_yaml}")
        except ImportError:
            # Fallback JSON/YAML if pyyaml not installed
            out_yaml.with_suffix(".json").write_text(json.dumps(splat_cfg, indent=2), encoding="utf-8")
            print(f"[✓] Generated split config (JSON fallback): {out_yaml.with_suffix('.json')}")

if __name__ == "__main__":
    main()

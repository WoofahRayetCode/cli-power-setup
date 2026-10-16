#!/usr/bin/env python3
import sys
import os
import struct
import zlib
import argparse
from pathlib import Path

# VPAK Format Specification:
# Header (32 bytes):
#   Magic: b'VPAK' (4 bytes)
#   Version: uint32 (4 bytes) -> 1
#   FileCount: uint32 (4 bytes)
#   TocOffset: uint64 (8 bytes)
#   Reserved: 12 bytes
# TOC Entry:
#   PathLength: uint16
#   Path: UTF-8 string
#   Offset: uint64
#   CompressedSize: uint64
#   UncompressedSize: uint64
#   Flags: uint32 (bit 0 = is_compressed)

MAGIC = b'VPAK'
VERSION = 1

def pack_directory(input_dir, output_file, compress=True):
    input_path = Path(input_dir).resolve()
    if not input_path.exists() or not input_path.is_dir():
        print(f"[!] Error: Input directory '{input_dir}' does not exist.")
        return 1

    files_to_pack = [p for p in input_path.rglob("*") if p.is_file()]
    print(f"[→] Packing {len(files_to_pack)} files from {input_path} -> {output_file}...")

    toc_entries = []
    
    with open(output_file, "wb") as out_f:
        # Placeholder for 32-byte header
        out_f.write(b'\x00' * 32)

        current_offset = 32
        for p in files_to_pack:
            rel_path = str(p.relative_to(input_path)).replace("\\", "/")
            raw_data = p.read_bytes()
            uncompressed_size = len(raw_data)

            if compress:
                comp_data = zlib.compress(raw_data, level=6)
                if len(comp_data) < uncompressed_size:
                    data_to_write = comp_data
                    flags = 1  # compressed
                else:
                    data_to_write = raw_data
                    flags = 0
            else:
                data_to_write = raw_data
                flags = 0

            comp_size = len(data_to_write)
            out_f.write(data_to_write)

            toc_entries.append({
                "path": rel_path,
                "offset": current_offset,
                "comp_size": comp_size,
                "raw_size": uncompressed_size,
                "flags": flags
            })
            current_offset += comp_size

        # Write TOC
        toc_offset = out_f.tell()
        for entry in toc_entries:
            path_bytes = entry["path"].encode("utf-8")
            out_f.write(struct.pack("<H", len(path_bytes)))
            out_f.write(path_bytes)
            out_f.write(struct.pack("<QQQI", entry["offset"], entry["comp_size"], entry["raw_size"], entry["flags"]))

        # Rewrite Header
        out_f.seek(0)
        header = struct.pack("<4sIIQ12s", MAGIC, VERSION, len(toc_entries), toc_offset, b'\x00' * 12)
        out_f.write(header)

    archive_size = os.path.getsize(output_file)
    print(f"[✓] Successfully created VPAK archive: {output_file} ({archive_size} bytes, {len(toc_entries)} files).")
    return 0

def list_archive(archive_file):
    if not os.path.exists(archive_file):
        print(f"[!] Archive not found: {archive_file}")
        return 1

    with open(archive_file, "rb") as f:
        header = f.read(32)
        if len(header) < 32:
            print("[!] Invalid archive: header too short.")
            return 1

        magic, version, file_count, toc_offset, _ = struct.unpack("<4sIIQ12s", header)
        if magic != MAGIC:
            print(f"[!] Invalid magic header: {magic}")
            return 1

        print(f"\n--- VPAK Archive: {archive_file} (v{version}) ---")
        print(f"Total Files: {file_count}, TOC Offset: 0x{toc_offset:X}\n")
        f.seek(toc_offset)

        for _ in range(file_count):
            path_len_data = f.read(2)
            if not path_len_data:
                break
            path_len = struct.unpack("<H", path_len_data)[0]
            path_str = f.read(path_len).decode("utf-8")
            offset, comp_size, raw_size, flags = struct.unpack("<QQQI", f.read(28))
            is_comp = "[COMP]" if (flags & 1) else "[RAW] "
            print(f"  {is_comp} {raw_size:>10}B -> {comp_size:>10}B  | 0x{offset:08X} | {path_str}")
        print("-------------------------------------------------\n")
    return 0

def main():
    parser = argparse.ArgumentParser(description="VFS Game Asset Container Tool (VPAK)")
    parser.add_argument("--input", help="Directory to pack")
    parser.add_argument("--output", help="Output VPAK file path")
    parser.add_argument("--compress", action="store_true", default=True, help="Compress files with zlib")
    parser.add_argument("--list", help="Inspect and list files in a VPAK archive")

    args = parser.parse_args()

    if args.list:
        sys.exit(list_archive(args.list))

    if args.input and args.output:
        sys.exit(pack_directory(args.input, args.output, args.compress))

    parser.print_help()

if __name__ == "__main__":
    main()

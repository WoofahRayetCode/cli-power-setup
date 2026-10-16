#!/usr/bin/env python3
import sys
import struct
import zlib
import argparse
from pathlib import Path

MAGIC = b"GSAV"

def inspect_save_file(file_path: Path):
    if not file_path.exists():
        print(f"[!] Error: File not found: {file_path}", file=sys.stderr)
        return 1

    data = file_path.read_bytes()
    if len(data) < 37:
        print(f"[!] Error: File too small for GSAV container ({len(data)} bytes)", file=sys.stderr)
        return 1

    magic, c_ver, schema_ver, timestamp, uncomp_sz, comp_sz, checksum, comp_type = struct.unpack_from(
        "<4sIIqQQQB", data, 0
    )

    if magic != MAGIC:
        print(f"[!] Error: Invalid magic bytes: {magic} (Expected: {MAGIC})", file=sys.stderr)
        return 1

    comp_names = {0: "None (Raw)", 1: "Zstandard", 2: "Zlib/Deflate"}
    print("=" * 60)
    print(f" 💾 Game Save State Inspector: {file_path.name}")
    print("=" * 60)
    print(f" Magic Identifier:       {magic.decode('ascii', errors='ignore')}")
    print(f" Container Version:      {c_ver}")
    print(f" Schema Version:         {schema_ver}")
    print(f" Timestamp (Epoch):      {timestamp}")
    print(f" Uncompressed Size:      {uncomp_sz} bytes ({uncomp_sz / 1024:.2f} KB)")
    print(f" Compressed Size:        {comp_sz} bytes ({comp_sz / 1024:.2f} KB)")
    print(f" Compression Codec:      {comp_names.get(comp_type, f'Unknown ({comp_type})')}")
    print(f" Header Checksum:        0x{checksum:016X}")

    payload = data[37:]
    if comp_type == 2:
        try:
            decomp = zlib.decompress(payload)
            calc_crc = zlib.crc32(decomp) & 0xFFFFFFFF
            print(f" Payload Validation:     Decompressed successfully ({len(decomp)} bytes)")
            print(f" Calculated CRC32:       0x{calc_crc:08X}")
        except Exception as e:
            print(f"[!] Warning: Zlib decompression failed: {e}")
    elif comp_type == 0:
        calc_crc = zlib.crc32(payload) & 0xFFFFFFFF
        print(f" Calculated CRC32:       0x{calc_crc:08X}")

    print("=" * 60)
    return 0

def pack_save_file(input_payload: Path, output_file: Path, schema_ver: int = 1, compress: bool = True):
    raw_data = input_payload.read_bytes()
    uncomp_sz = len(raw_data)
    crc = zlib.crc32(raw_data) & 0xFFFFFFFF

    if compress:
        comp_data = zlib.compress(raw_data, level=6)
        comp_sz = len(comp_data)
        comp_type = 2
        payload = comp_data
    else:
        comp_sz = 0
        comp_type = 0
        payload = raw_data

    header = struct.pack(
        "<4sIIqQQQB",
        MAGIC,
        1,          # container ver
        schema_ver, # schema ver
        1700000000, # sample timestamp
        uncomp_sz,
        comp_sz,
        crc,
        comp_type
    )

    output_file.write_bytes(header + payload)
    print(f"[✓] Created valid GSAV container: {output_file} ({len(header) + len(payload)} bytes)")

def main():
    parser = argparse.ArgumentParser(description="Game Save State Inspector & Builder (GSAV)")
    parser.add_argument("--inspect", type=Path, help="Inspect a GSAV container file")
    parser.add_argument("--pack", type=Path, help="Pack a raw payload file into GSAV")
    parser.add_argument("--out", type=Path, help="Output GSAV path (used with --pack)")
    parser.add_argument("--schema", type=int, default=1, help="Schema version integer")

    args = parser.parse_args()

    if args.inspect:
        sys.exit(inspect_save_file(args.inspect))
    elif args.pack and args.out:
        pack_save_file(args.pack, args.out, args.schema)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

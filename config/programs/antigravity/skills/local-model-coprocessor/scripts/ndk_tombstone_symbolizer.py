#!/usr/bin/env python3
import sys
import os
import re
import subprocess
import argparse

def symbolize_log(log_path, symbols_dir):
    if not os.path.exists(log_path):
        print(f"[!] Log file not found: {log_path}")
        return 1

    print(f"[→] Parsing native stack trace from {log_path}...")
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # Pattern: #00 pc 0000000000012345  /data/app/.../libnative.so (function+offset)
    pattern = re.compile(r'#(\d+)\s+pc\s+([0-9a-fA-F]+)\s+.*?/([^/\s]+\.so)')

    found_frames = False
    for line in lines:
        match = pattern.search(line)
        if match:
            found_frames = True
            frame_num, pc_addr, lib_name = match.groups()
            lib_path = os.path.join(symbols_dir, lib_name)
            
            symbol_info = "??:0"
            if os.path.isfile(lib_path):
                # Try addr2line if available
                res = subprocess.run(["addr2line", "-C", "-f", "-e", lib_path, f"0x{pc_addr}"],
                                     capture_output=True, text=True)
                if res.returncode == 0 and res.stdout.strip():
                    symbol_info = " -> " + " ".join(res.stdout.strip().splitlines())

            print(f"#{frame_num} [0x{pc_addr}] {lib_name}{symbol_info}")

    if not found_frames:
        print("[!] No native stack frames found in log.")
    else:
        print("[✓] Symbolization complete.")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Android NDK Native Stack Trace Symbolizer")
    parser.add_argument("--logcat", required=True, help="Path to crash logcat or tombstone text file")
    parser.add_argument("--symbols", required=True, help="Directory containing unstripped .so libraries with debug symbols")
    args = parser.parse_args()

    sys.exit(symbolize_log(args.logcat, args.symbols))

if __name__ == "__main__":
    main()

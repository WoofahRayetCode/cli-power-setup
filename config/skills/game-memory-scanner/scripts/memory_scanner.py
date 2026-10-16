#!/usr/bin/env python3
"""
Game Memory Scanner & Dynamic Pointer Engine (memory_scanner.py)
Provides cross-platform memory inspection, value scanning, candidate filtering,
AOB signature pattern matching, and memory freezing for game trainer development.
"""

import argparse
import ctypes
import json
import os
import re
import struct
import sys
import time
from pathlib import Path


def find_pid(process_name_or_pid):
    """Finds process ID by PID or process name."""
    if str(process_name_or_pid).isdigit():
        pid = int(process_name_or_pid)
        if os.path.exists(f"/proc/{pid}"):
            return pid
        return None

    name = str(process_name_or_pid).lower()
    matches = []
    for entry in os.scandir("/proc"):
        if entry.is_dir() and entry.name.isdigit():
            pid = int(entry.name)
            try:
                # Check comm
                comm_path = os.path.join(entry.path, "comm")
                if os.path.exists(comm_path):
                    with open(comm_path, "r", errors="ignore") as f:
                        comm = f.read().strip().lower()
                        if name in comm:
                            matches.append(pid)
                            continue

                # Check cmdline
                cmdline_path = os.path.join(entry.path, "cmdline")
                if os.path.exists(cmdline_path):
                    with open(cmdline_path, "rb") as f:
                        cmdline = f.read().replace(b"\x00", b" ").decode("utf-8", errors="ignore").lower()
                        if name in cmdline:
                            matches.append(pid)
            except (PermissionError, ProcessLookupError, FileNotFoundError):
                continue

    if matches:
        return matches[-1]  # Return most recent matching process
    return None


def parse_maps(pid, perm_filter="rw"):
    """Parses /proc/<pid>/maps for memory regions matching permission filter."""
    regions = []
    maps_file = f"/proc/{pid}/maps"
    if not os.path.exists(maps_file):
        raise ProcessLookupError(f"Process {pid} does not exist or /proc/{pid}/maps is inaccessible.")

    with open(maps_file, "r", errors="ignore") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            addr_range, perms = parts[0], parts[1]
            if not all(p in perms for p in perm_filter):
                continue
            
            # Skip read-only special device files or vsyscall
            pathname = parts[5] if len(parts) >= 6 else ""
            if "[vsyscall]" in pathname or "[vvar]" in pathname:
                continue

            start_str, end_str = addr_range.split("-")
            start = int(start_str, 16)
            end = int(end_str, 16)
            size = end - start

            # Skip huge mapped file sections (> 512MB) unless heap/stack to avoid scanning whole asset files
            if size > 512 * 1024 * 1024 and not (pathname.startswith("[heap]") or pathname == ""):
                continue

            regions.append((start, end, perms, pathname))
    return regions


def pack_value(val_type, value_str):
    """Packs value string into binary bytes."""
    v_type = val_type.lower()
    if v_type in ("i32", "int32", "int"):
        val = int(value_str)
        return struct.pack("<i", val), 4
    elif v_type in ("u32", "uint32"):
        val = int(value_str)
        return struct.pack("<I", val), 4
    elif v_type in ("i64", "int64"):
        val = int(value_str)
        return struct.pack("<q", val), 8
    elif v_type in ("u64", "uint64"):
        val = int(value_str)
        return struct.pack("<Q", val), 8
    elif v_type in ("f32", "float"):
        val = float(value_str)
        return struct.pack("<f", val), 4
    elif v_type in ("f64", "double"):
        val = float(value_str)
        return struct.pack("<d", val), 8
    elif v_type in ("hex", "bytes"):
        cleaned = value_str.replace(" ", "").replace("0x", "")
        b = bytes.fromhex(cleaned)
        return b, len(b)
    else:
        raise ValueError(f"Unsupported data type: {val_type}")


def unpack_value(val_type, raw_bytes):
    """Unpacks binary bytes into typed Python value."""
    v_type = val_type.lower()
    if v_type in ("i32", "int32", "int"):
        return struct.unpack("<i", raw_bytes[:4])[0]
    elif v_type in ("u32", "uint32"):
        return struct.unpack("<I", raw_bytes[:4])[0]
    elif v_type in ("i64", "int64"):
        return struct.unpack("<q", raw_bytes[:8])[0]
    elif v_type in ("u64", "uint64"):
        return struct.unpack("<Q", raw_bytes[:8])[0]
    elif v_type in ("f32", "float"):
        return round(struct.unpack("<f", raw_bytes[:4])[0], 4)
    elif v_type in ("f64", "double"):
        return round(struct.unpack("<d", raw_bytes[:8])[0], 6)
    elif v_type in ("hex", "bytes"):
        return raw_bytes.hex().upper()
    return None


def read_proc_mem(pid, addr, size):
    """Reads raw bytes from /proc/<pid>/mem."""
    mem_path = f"/proc/{pid}/mem"
    try:
        with open(mem_path, "rb", buffering=0) as f:
            f.seek(addr)
            return f.read(size)
    except (OSError, PermissionError):
        return None


def write_proc_mem(pid, addr, data):
    """Writes raw bytes to /proc/<pid>/mem."""
    mem_path = f"/proc/{pid}/mem"
    try:
        with open(mem_path, "wb", buffering=0) as f:
            f.seek(addr)
            f.write(data)
            return True
    except (OSError, PermissionError) as e:
        print(f"[✗] Memory write error at 0x{addr:X}: {e}", file=sys.stderr)
        return False


def cmd_scan(args):
    """Executes initial memory scan."""
    pid = find_pid(args.target)
    if not pid:
        print(f"[✗] Could not find running process matching '{args.target}'", file=sys.stderr)
        sys.exit(1)

    target_bytes, val_len = pack_value(args.type, args.value)
    regions = parse_maps(pid, perm_filter="rw")
    print(f"[→] Scanning PID {pid} across {len(regions)} writable memory regions for {args.type} = {args.value}...")

    candidates = []
    mem_path = f"/proc/{pid}/mem"

    try:
        with open(mem_path, "rb", buffering=0) as f:
            for start, end, perms, path in regions:
                size = end - start
                # Read in chunks of 4MB
                chunk_size = 4 * 1024 * 1024
                offset = 0
                while offset < size:
                    cur_read = min(chunk_size, size - offset)
                    try:
                        f.seek(start + offset)
                        buf = f.read(cur_read)
                    except OSError:
                        offset += cur_read
                        continue

                    if not buf:
                        offset += cur_read
                        continue

                    idx = 0
                    while True:
                        idx = buf.find(target_bytes, idx)
                        if idx == -1:
                            break
                        addr = start + offset + idx
                        # Align on 4-byte boundaries for integers/floats
                        if val_len >= 4 and (addr % 4 != 0):
                            idx += 1
                            continue

                        candidates.append({
                            "address": f"0x{addr:X}",
                            "value": unpack_value(args.type, target_bytes),
                            "region": path or "anonymous"
                        })
                        if len(candidates) >= args.max_results:
                            print(f"[!] Reached max candidate limit ({args.max_results}). Truncating scan.")
                            break
                        idx += val_len

                    if len(candidates) >= args.max_results:
                        break
                    offset += cur_read

                if len(candidates) >= args.max_results:
                    break
    except PermissionError:
        print(f"[✗] Permission denied accessing /proc/{pid}/mem. Ensure ptrace_scope=0 or run with CAP_SYS_PTRACE.", file=sys.stderr)
        sys.exit(1)

    out_file = Path(args.output)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "pid": pid,
        "type": args.type,
        "target_value": args.value,
        "timestamp": time.time(),
        "candidates": candidates
    }
    out_file.write_text(json.dumps(payload, indent=2))
    print(f"[✓] Scan complete. Found {len(candidates)} candidates. Saved to {out_file}.")


def cmd_filter(args):
    """Filters previous scan candidates by new value or delta."""
    in_file = Path(args.candidates)
    if not in_file.exists():
        print(f"[✗] Candidates file not found: {in_file}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(in_file.read_text())
    pid = data.get("pid")
    val_type = data.get("type")
    candidates = data.get("candidates", [])

    if not os.path.exists(f"/proc/{pid}"):
        print(f"[✗] Original process PID {pid} is no longer running.", file=sys.stderr)
        sys.exit(1)

    dummy_bytes, val_len = pack_value(val_type, "0")
    filtered = []

    print(f"[→] Filtering {len(candidates)} candidates for PID {pid} (Rule: {args.condition or args.value})...")
    for cand in candidates:
        addr = int(cand["address"], 16)
        prev_val = cand["value"]
        raw = read_proc_mem(pid, addr, val_len)
        if not raw or len(raw) < val_len:
            continue

        curr_val = unpack_value(val_type, raw)

        match = False
        if args.value is not None:
            expected_val = unpack_value(val_type, pack_value(val_type, args.value)[0])
            if curr_val == expected_val:
                match = True
        elif args.condition == "increased":
            if curr_val > prev_val:
                match = True
        elif args.condition == "decreased":
            if curr_val < prev_val:
                match = True
        elif args.condition == "changed":
            if curr_val != prev_val:
                match = True
        elif args.condition == "unchanged":
            if curr_val == prev_val:
                match = True

        if match:
            filtered.append({
                "address": cand["address"],
                "value": curr_val,
                "previous_value": prev_val,
                "region": cand.get("region", "anonymous")
            })

    out_file = Path(args.output or args.candidates)
    data["candidates"] = filtered
    data["last_filter"] = time.time()
    out_file.write_text(json.dumps(data, indent=2))
    print(f"[✓] Filtering complete. Retained {len(filtered)} / {len(candidates)} candidates. Saved to {out_file}.")


def cmd_aob(args):
    """Scans executable memory regions for Array-of-Bytes (AOB) patterns."""
    pid = find_pid(args.target)
    if not pid:
        print(f"[✗] Could not find running process matching '{args.target}'", file=sys.stderr)
        sys.exit(1)

    # Parse AOB tokens: "48 89 5C 24 ?? 57" -> regex bytes
    tokens = args.pattern.strip().split()
    regex_parts = []
    for t in tokens:
        if t in ("??", "?"):
            regex_parts.append(b".")
        else:
            regex_parts.append(re.escape(bytes.fromhex(t)))
    pattern = re.compile(b"".join(regex_parts), re.DOTALL)

    regions = parse_maps(pid, perm_filter="r-x")
    print(f"[→] Scanning PID {pid} across {len(regions)} executable code regions for AOB signature...")

    matches = []
    mem_path = f"/proc/{pid}/mem"

    with open(mem_path, "rb", buffering=0) as f:
        for start, end, perms, path in regions:
            if args.module and args.module.lower() not in path.lower():
                continue
            size = end - start
            try:
                f.seek(start)
                buf = f.read(size)
            except OSError:
                continue

            if not buf:
                continue

            for m in pattern.finditer(buf):
                addr = start + m.start()
                matches.append({
                    "address": f"0x{addr:X}",
                    "offset": f"0x{m.start():X}",
                    "module": path or "main",
                    "matched_bytes": m.group(0).hex().upper()
                })

    print(f"[✓] Found {len(matches)} signature match(es):")
    for m in matches[:10]:
        print(f"  -> {m['address']} (Module: {m['module']}, Match: {m['matched_bytes'][:16]}...)")
    if len(matches) > 10:
        print(f"  ... and {len(matches) - 10} more matches.")


def cmd_freeze(args):
    """Freezes an address to a static value by writing continuously."""
    pid = find_pid(args.target)
    if not pid:
        print(f"[✗] Process '{args.target}' not found.", file=sys.stderr)
        sys.exit(1)

    addr = int(args.addr, 16)
    data, val_len = pack_value(args.type, args.value)

    print(f"[❄️ FREEZE ACTIVE] Locking 0x{addr:X} ({args.type}) to {args.value} in PID {pid}. Press Ctrl+C to stop.")
    try:
        while True:
            write_proc_mem(pid, addr, data)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[✓] Freeze deactivated.")


def cmd_read_write(args):
    """Handles read or write subcommands."""
    pid = find_pid(args.target)
    if not pid:
        print(f"[✗] Process '{args.target}' not found.", file=sys.stderr)
        sys.exit(1)

    addr = int(args.addr, 16)
    if args.action == "read":
        dummy, val_len = pack_value(args.type, "0")
        raw = read_proc_mem(pid, addr, val_len)
        if raw and len(raw) == val_len:
            val = unpack_value(args.type, raw)
            print(f"[✓] 0x{addr:X} [{args.type}] = {val} (Hex: {raw.hex().upper()})")
        else:
            print(f"[✗] Failed to read from 0x{addr:X}")
    elif args.action == "write":
        data, val_len = pack_value(args.type, args.value)
        if write_proc_mem(pid, addr, data):
            print(f"[✓] Wrote {args.value} [{args.type}] to 0x{addr:X}.")


def cmd_pointer_scan(args):
    """Scans for static/base pointers pointing to dynamic target address."""
    pid = find_pid(args.target)
    if not pid:
        print(f"[✗] Process '{args.target}' not found.", file=sys.stderr)
        sys.exit(1)

    target_addr = int(args.target_addr, 16)
    max_offset = int(args.max_offset, 16) if args.max_offset.startswith("0x") else int(args.max_offset)
    regions = parse_maps(pid, perm_filter="rw")

    print(f"[→] Pointer Scan: Searching for pointers pointing to 0x{target_addr:X} (Max Offset: +0x{max_offset:X})...")
    candidates = []

    mem_path = f"/proc/{pid}/mem"
    with open(mem_path, "rb", buffering=0) as f:
        for start, end, perms, path in regions:
            size = end - start
            try:
                f.seek(start)
                buf = f.read(size)
            except OSError:
                continue

            if not buf or len(buf) < 8:
                continue

            # Read 64-bit pointers aligned to 8 bytes
            for i in range(0, len(buf) - 8, 8):
                ptr_val = struct.unpack("<Q", buf[i:i+8])[0]
                if target_addr - max_offset <= ptr_val <= target_addr:
                    offset = target_addr - ptr_val
                    ptr_addr = start + i
                    candidates.append({
                        "base_pointer": f"0x{ptr_addr:X}",
                        "points_to": f"0x{ptr_val:X}",
                        "offset": f"0x{offset:X}",
                        "module": path or "heap"
                    })
                    if len(candidates) >= 20:
                        break
            if len(candidates) >= 20:
                break

    print(f"[✓] Discovered {len(candidates)} pointer candidate(s):")
    for c in candidates:
        print(f"  -> [{c['base_pointer']}] + {c['offset']} => 0x{target_addr:X} (Region: {c['module']})")


def main():
    parser = argparse.ArgumentParser(description="Game Memory Scanner & Dynamic Pointer Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # scan
    p_scan = subparsers.add_parser("scan", help="Perform initial memory scan for a value")
    p_scan.add_argument("--target", required=True, help="Process name (e.g. xrEngine.exe) or PID")
    p_scan.add_argument("--type", default="i32", choices=["i32", "u32", "i64", "u64", "f32", "f64"], help="Data type")
    p_scan.add_argument("--value", required=True, help="Target value to search for")
    p_scan.add_argument("--output", default="candidates.json", help="Path to save candidate results")
    p_scan.add_argument("--max-results", type=int, default=5000, help="Maximum number of candidates to store")

    # filter
    p_filter = subparsers.add_parser("filter", help="Filter previously saved candidates")
    p_filter.add_argument("--candidates", required=True, help="Path to previous candidates.json")
    p_filter.add_argument("--value", help="Exact new value to filter by")
    p_filter.add_argument("--condition", choices=["increased", "decreased", "changed", "unchanged"], help="Relative filter condition")
    p_filter.add_argument("--output", help="Output file (defaults to overwrite candidates file)")

    # aob
    p_aob = subparsers.add_parser("aob", help="Scan for Array-of-Bytes (AOB) signature pattern")
    p_aob.add_argument("--target", required=True, help="Process name or PID")
    p_aob.add_argument("--pattern", required=True, help="Hex byte pattern with wildcards (e.g. '48 89 5C 24 ?? 57')")
    p_aob.add_argument("--module", help="Filter scan to specific module/library")

    # read
    p_read = subparsers.add_parser("read", help="Read memory value at address")
    p_read.add_argument("--target", required=True, help="Process name or PID")
    p_read.add_argument("--addr", required=True, help="Memory address in hex (e.g. 0x7FFE1234)")
    p_read.add_argument("--type", default="i32", choices=["i32", "u32", "i64", "u64", "f32", "f64", "hex"], help="Data type")
    p_read.set_defaults(action="read")

    # write
    p_write = subparsers.add_parser("write", help="Write memory value at address")
    p_write.add_argument("--target", required=True, help="Process name or PID")
    p_write.add_argument("--addr", required=True, help="Memory address in hex")
    p_write.add_argument("--type", default="i32", choices=["i32", "u32", "i64", "u64", "f32", "f64"], help="Data type")
    p_write.add_argument("--value", required=True, help="Value to write")
    p_write.set_defaults(action="write")

    # freeze
    p_freeze = subparsers.add_parser("freeze", help="Continuously write value to freeze address")
    p_freeze.add_argument("--target", required=True, help="Process name or PID")
    p_freeze.add_argument("--addr", required=True, help="Memory address in hex")
    p_freeze.add_argument("--type", default="i32", choices=["i32", "u32", "i64", "u64", "f32", "f64"], help="Data type")
    p_freeze.add_argument("--value", required=True, help="Value to freeze")
    p_freeze.add_argument("--interval", type=float, default=0.1, help="Write interval in seconds")

    # pointer-scan
    p_ptr = subparsers.add_parser("pointer-scan", help="Search for pointers referencing a target address")
    p_ptr.add_argument("--target", required=True, help="Process name or PID")
    p_ptr.add_argument("--target-addr", required=True, help="Target dynamic address in hex")
    p_ptr.add_argument("--max-offset", default="0x1000", help="Maximum structure offset in hex")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "filter":
        cmd_filter(args)
    elif args.command == "aob":
        cmd_aob(args)
    elif args.command in ("read", "write"):
        cmd_read_write(args)
    elif args.command == "freeze":
        cmd_freeze(args)
    elif args.command == "pointer-scan":
        cmd_pointer_scan(args)


if __name__ == "__main__":
    main()

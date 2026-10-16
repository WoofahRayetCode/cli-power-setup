#!/usr/bin/env python3
"""
PE Dependency Check: Standalone PE Import Table & DLL Dependency Inspector.
Extracts all imported DLLs from a Windows PE (.exe / .dll) binary without external tools.
Helps diagnose 0xC0000135 (Unable to Locate DLL) launch failures on Windows and Wine/Proton.
"""

import sys
import os
import struct
import argparse

def parse_pe_imports(filepath: str) -> list[str]:
    with open(filepath, "rb") as f:
        # Check MZ header
        if f.read(2) != b"MZ":
            raise ValueError(f"Not a valid PE executable: {filepath}")
            
        f.seek(0x3C)
        pe_offset = struct.unpack("<I", f.read(4))[0]
        
        f.seek(pe_offset)
        if f.read(4) != b"PE\x00\x00":
            raise ValueError("Invalid PE signature")
            
        # COFF File Header: 20 bytes
        # Machine (2), NumberOfSections (2), ... SizeOfOptionalHeader (2)
        f.seek(pe_offset + 4 + 2)
        num_sections = struct.unpack("<H", f.read(2))[0]
        
        f.seek(pe_offset + 4 + 16)
        size_opt_header = struct.unpack("<H", f.read(2))[0]
        
        opt_header_offset = pe_offset + 24
        f.seek(opt_header_offset)
        magic = struct.unpack("<H", f.read(2))[0]
        
        is_64bit = (magic == 0x20B)  # PE32+
        is_32bit = (magic == 0x10B)  # PE32
        
        if not (is_32bit or is_64bit):
            raise ValueError(f"Unknown Optional Header magic: 0x{magic:X}")
            
        # Data directories offset:
        # For PE32: offset 96 from start of Optional Header
        # For PE32+: offset 112 from start of Optional Header
        data_dir_offset = opt_header_offset + (112 if is_64bit else 96)
        
        # Import Table is the 2nd entry (index 1) in Data Directories (each entry 8 bytes: RVA (4), Size (4))
        f.seek(data_dir_offset + 8)
        import_rva, import_size = struct.unpack("<II", f.read(8))
        
        if import_rva == 0 or import_size == 0:
            return []  # No imports
            
        # Parse Section Headers to convert RVA to File Offset
        sections_offset = opt_header_offset + size_opt_header
        f.seek(sections_offset)
        
        sections = []
        for _ in range(num_sections):
            sec_data = f.read(40)
            sec_name = sec_data[:8].rstrip(b"\x00").decode("utf-8", errors="ignore")
            v_size, v_addr, raw_size, raw_ptr = struct.unpack("<IIII", sec_data[8:24])
            sections.append({
                "name": sec_name,
                "v_addr": v_addr,
                "v_size": v_size,
                "raw_ptr": raw_ptr,
                "raw_size": raw_size
            })
            
        def rva_to_offset(rva):
            for sec in sections:
                if sec["v_addr"] <= rva < sec["v_addr"] + max(sec["v_size"], sec["raw_size"]):
                    return sec["raw_ptr"] + (rva - sec["v_addr"])
            return None

        import_file_offset = rva_to_offset(import_rva)
        if import_file_offset is None:
            return []
            
        # Read IMAGE_IMPORT_DESCRIPTOR array (each 20 bytes: OriginalFirstThunk(4), TimeDateStamp(4), ForwarderChain(4), Name(4), FirstThunk(4))
        f.seek(import_file_offset)
        dll_names = []
        
        while True:
            desc = f.read(20)
            if len(desc) < 20 or desc == b"\x00" * 20:
                break
            orig_thunk, timestamp, forwarder, name_rva, first_thunk = struct.unpack("<IIIII", desc)
            if name_rva == 0:
                break
            name_offset = rva_to_offset(name_rva)
            if name_offset is not None:
                cur_pos = f.tell()
                f.seek(name_offset)
                name_bytes = b""
                while True:
                    ch = f.read(1)
                    if ch == b"\x00" or not ch:
                        break
                    name_bytes += ch
                dll_name = name_bytes.decode("utf-8", errors="ignore")
                dll_names.append(dll_name)
                f.seek(cur_pos)
                
        return dll_names

def main():
    parser = argparse.ArgumentParser(description="Inspect DLL dependencies from Windows PE binaries.")
    parser.add_argument("binary", help="Target PE binary (.exe or .dll)")
    args = parser.parse_args()
    
    if not os.path.isfile(args.binary):
        print(f"[-] Error: File '{args.binary}' not found.", file=sys.stderr)
        sys.exit(1)
        
    try:
        dlls = parse_pe_imports(args.binary)
        print(f"=== DLL Dependencies for {args.binary} ({len(dlls)} libraries) ===")
        for dll in sorted(dlls, key=lambda s: s.lower()):
            print(f"  • {dll}")
    except Exception as e:
        print(f"[-] Error parsing imports: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

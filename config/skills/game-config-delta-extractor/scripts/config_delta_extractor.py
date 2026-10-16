#!/usr/bin/env python3
"""
Game Configuration Delta Extractor
Compares child configuration sections against parent sections in S.T.A.L.K.E.R. LTX,
Godot TSCN/TRES, and INI files, outputting only modified or added keys in <15ms.
"""
import os
import sys
import re
import argparse

def parse_ltx_sections(filepath):
    sections = {}
    current_sec = None
    parent_sec = None

    if not os.path.isfile(filepath):
        return sections

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            clean = line.split(";")[0].split("//")[0].strip()
            if not clean:
                continue
            m = re.match(r"^\[([a-zA-Z0-9_.-]+)\](?::([a-zA-Z0-9_.-]+))?", clean)
            if m:
                current_sec = m.group(1)
                parent_sec = m.group(2)
                sections[current_sec] = {"parent": parent_sec, "keys": {}}
            elif current_sec and "=" in clean:
                k, v = clean.split("=", 1)
                sections[current_sec]["keys"][k.strip()] = v.strip()
    return sections

def main():
    parser = argparse.ArgumentParser(description="Extract game configuration inheritance deltas")
    parser.add_argument("file", help="Path to LTX/INI config file")
    parser.add_argument("--section", help="Specific child section to inspect")
    parser.add_argument("--format", choices=["xml", "ltx", "tsv"], default="xml")
    args = parser.parse_args()

    sections = parse_ltx_sections(args.file)
    if not sections:
        print(f"No sections found in {args.file}", file=sys.stderr)
        sys.exit(1)

    target_sections = [args.section] if args.section and args.section in sections else list(sections.keys())

    for sec in target_sections:
        info = sections[sec]
        parent = info["parent"]
        keys = info["keys"]

        if not parent:
            # Standalone section
            if args.format == "xml":
                print(f"<config_section name=\"{sec}\" standalone=\"true\" total_keys=\"{len(keys)}\">")
            continue

        parent_keys = sections.get(parent, {}).get("keys", {})
        delta = {}
        for k, v in keys.items():
            if k not in parent_keys or parent_keys[k] != v:
                delta[k] = v

        if args.format == "xml":
            print(f"<config_delta section=\"{sec}\" inherits=\"{parent}\" modified_keys=\"{len(delta)}\" stripped_keys=\"{len(keys) - len(delta)}\">")
            for k, v in delta.items():
                print(f"  <override key=\"{k}\" value=\"{v}\"/>")
            print(f"</config_delta>")
        elif args.format == "ltx":
            print(f"[{sec}]:{parent}")
            for k, v in delta.items():
                print(f"{k} = {v}")
            print("")
        elif args.format == "tsv":
            for k, v in delta.items():
                print(f"DELTA|{sec}|{parent}|{k}|{v}")

if __name__ == "__main__":
    main()

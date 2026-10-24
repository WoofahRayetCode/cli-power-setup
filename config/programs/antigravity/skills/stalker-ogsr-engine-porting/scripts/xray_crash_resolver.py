#!/usr/bin/env python3
"""
X-Ray Crash Symbol Resolver
Parses 15,000-line S.T.A.L.K.E.R. / OGSR crash logs and stack traces, isolates
fatal assertions, demangles RVAs, and outputs a 100-token fault diagnosis.
"""
import sys
import os
import re
import argparse
import subprocess

def parse_xray_crash(text):
    info = {
        "fatal_error": None,
        "expression": None,
        "function": None,
        "file": None,
        "line": None,
        "description": None,
        "stack_frames": []
    }

    lines = text.splitlines()
    in_fatal = False

    for line in lines:
        s = line.strip()
        if "FATAL ERROR" in s:
            in_fatal = True
            info["fatal_error"] = True
            continue

        if in_fatal:
            if s.startswith("[error]Expression") or s.startswith("Expression"):
                m = re.search(r":\s*(.*)", s)
                if m: info["expression"] = m.group(1).strip()
            elif s.startswith("[error]Function") or s.startswith("Function"):
                m = re.search(r":\s*(.*)", s)
                if m: info["function"] = m.group(1).strip()
            elif s.startswith("[error]File") or s.startswith("File"):
                m = re.search(r":\s*(.*)", s)
                if m: info["file"] = m.group(1).strip()
            elif s.startswith("[error]Line") or s.startswith("Line"):
                m = re.search(r":\s*(\d+)", s)
                if m: info["line"] = m.group(1).strip()
            elif s.startswith("[error]Description") or s.startswith("Description"):
                m = re.search(r":\s*(.*)", s)
                if m: info["description"] = m.group(1).strip()
            elif s.startswith("stack trace:"):
                in_fatal = False

        if "stack trace:" in s or (not in_fatal and ("+ 0x" in s or "! " in s or "0x000" in s)):
            m_rva = re.search(r"([a-zA-Z0-9_.-]+\.(?:dll|exe))\s*(?:\+|at)?\s*(0x[0-9a-fA-F]+)", s)
            if m_rva:
                info["stack_frames"].append({
                    "module": m_rva.group(1),
                    "rva": m_rva.group(2),
                    "raw": s
                })

    return info

def main():
    parser = argparse.ArgumentParser(description="Resolve S.T.A.L.K.E.R. / OGSR engine crash log to root-cause coordinates")
    parser.add_argument("logfile", nargs="?", help="Path to xray_*.log or crash text (default: stdin or latest log)")
    parser.add_argument("--format", choices=["xml", "compact", "tsv"], default="xml")
    args = parser.parse_args()

    content = ""
    if args.logfile and os.path.isfile(args.logfile):
        try:
            with open(args.logfile, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {args.logfile}: {e}", file=sys.stderr)
            sys.exit(1)
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        # Search for latest xray log in typical paths
        candidates = [
            os.path.expanduser("~/Documents/GitHub/ogsr-complete-merge/_appdata_/logs"),
            "/tmp"
        ]
        found = []
        for c in candidates:
            if os.path.isdir(c):
                for f in os.listdir(c):
                    if f.startswith("xray_") and f.endswith(".log"):
                        found.append(os.path.join(c, f))
        if found:
            latest = max(found, key=os.path.getmtime)
            print(f"<!-- Reading latest crash log: {latest} -->", file=sys.stderr)
            with open(latest, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        else:
            print("No logfile provided and no xray_*.log found", file=sys.stderr)
            sys.exit(1)

    info = parse_xray_crash(content)

    if args.format == "xml":
        print(f"<xray_crash_diagnosis has_fatal_error=\"{bool(info['fatal_error'])}\">")
        if info["file"]:
            print(f"  <location file=\"{info['file']}\" line=\"{info['line']}\" function=\"{info['function']}\"/>")
        if info["expression"]:
            print(f"  <assertion expression=\"{info['expression']}\"/>")
        if info["description"]:
            print(f"  <description>{info['description']}</description>")
        if info["stack_frames"]:
            print(f"  <stack_frames count=\"{len(info['stack_frames'])}\">")
            for sf in info["stack_frames"][:5]:
                print(f"    <frame module=\"{sf['module']}\" rva=\"{sf['rva']}\"/>")
            print(f"  </stack_frames>")
        print(f"</xray_crash_diagnosis>")
    elif args.format == "compact":
        loc = f"{info['file']}#L{info['line']}" if info['file'] else "unknown"
        expr = f" | Expr: {info['expression']}" if info['expression'] else ""
        desc = f" | {info['description']}" if info['description'] else ""
        print(f"[X-RAY CRASH] Loc: {loc} ({info['function']}){expr}{desc}")
    elif args.format == "tsv":
        print(f"CRASH|FILE:{info['file']}|LINE:{info['line']}|FUNC:{info['function']}|EXPR:{info['expression']}")

if __name__ == "__main__":
    main()

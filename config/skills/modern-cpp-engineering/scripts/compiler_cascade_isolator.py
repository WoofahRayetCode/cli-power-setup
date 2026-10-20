#!/usr/bin/env python3
"""
Compiler Error Cascade Isolator
Intercepts noisy GCC/Clang/MSVC error streams, strips recursive template dumps,
and outputs the exact primary root-cause error and source coordinates in <10ms.
"""
import sys
import re
import argparse

def isolate_errors(log_text):
    lines = log_text.splitlines()
    primary_error = None
    cascades = []
    
    # GCC/Clang format: file:line:col: error: message
    err_pattern = re.compile(r"^([^:\n]+):(\d+):(?:\d+:)?\s+(fatal error|error):\s+(.*)$")
    # MSVC format: file(line): error Cxxxx: message
    msvc_pattern = re.compile(r"^([^(:\n]+)\((\d+)\):\s+error\s+([A-Z0-9]+):\s+(.*)$")

    for i, line in enumerate(lines):
        m_gcc = err_pattern.match(line.strip())
        m_msvc = msvc_pattern.match(line.strip())

        if m_gcc or m_msvc:
            if m_gcc:
                file, line_num, severity, msg = m_gcc.groups()
            else:
                file, line_num, severity, msg = m_msvc.groups()

            # Clean verbose template arguments from message
            clean_msg = re.sub(r"<[A-Za-z0-9_:\s,<>\*&]+>", "<...>", msg)

            err_obj = {
                "file": file.strip(),
                "line": line_num.strip(),
                "severity": severity.strip(),
                "message": clean_msg.strip(),
                "raw_line": line.strip()
            }

            if not primary_error:
                primary_error = err_obj
            else:
                cascades.append(err_obj)

    return primary_error, cascades

def main():
    parser = argparse.ArgumentParser(description="Isolate primary C++ compiler error from noisy cascades")
    parser.add_argument("logfile", nargs="?", help="Path to compiler log (or read stdin)")
    parser.add_argument("--format", choices=["xml", "compact", "tsv"], default="xml")
    args = parser.parse_args()

    if args.logfile:
        try:
            with open(args.logfile, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {args.logfile}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        content = sys.stdin.read()

    primary, cascades = isolate_errors(content)

    if not primary:
        print("<compiler_status status=\"clean_or_warning_only\"/>")
        sys.exit(0)

    if args.format == "xml":
        print(f"<compiler_root_cause file=\"{primary['file']}\" line=\"{primary['line']}\" severity=\"{primary['severity']}\">")
        print(f"  <message>{primary['message']}</message>")
        print(f"  <secondary_cascades_suppressed count=\"{len(cascades)}\"/>")
        if cascades:
            print(f"  <!-- First secondary: {cascades[0]['file']}:{cascades[0]['line']}: {cascades[0]['message']} -->")
        print(f"</compiler_root_cause>")
    elif args.format == "compact":
        print(f"[ROOT ERROR] {primary['file']}#L{primary['line']}: {primary['message']} (+{len(cascades)} cascading errors suppressed)")
    elif args.format == "tsv":
        print(f"ROOT_ERROR|{primary['file']}|{primary['line']}|{primary['message']}|SUPPRESSED:{len(cascades)}")

if __name__ == "__main__":
    main()

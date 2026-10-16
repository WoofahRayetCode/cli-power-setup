#!/usr/bin/env python3
"""
Context Window Governor: Token estimation, partition budgeting, and output containment.
Zero external dependencies.
"""
import sys
import os
import time
import argparse
from pathlib import Path

def estimate_tokens(text: str) -> int:
    """Heuristic token estimator (~3.8 characters per token for code/text)."""
    if not text:
        return 0
    return max(1, int(len(text) / 3.8))

def calculate_budget(total_window: int, current_used: int):
    remaining = max(0, total_window - current_used)
    pct_used = (current_used / total_window) * 100.0 if total_window > 0 else 0.0

    allocations = {
        "total_window": total_window,
        "current_used": current_used,
        "remaining": remaining,
        "utilization_pct": round(pct_used, 1),
        "partitions": {
            "system_and_rules_reserve": int(remaining * 0.20),
            "working_code_ast_buffer": int(remaining * 0.35),
            "tool_output_containment_limit": int(remaining * 0.25),
            "generation_headroom": int(remaining * 0.20)
        }
    }
    return allocations

def clamp_content(content: str, max_lines: int = 60, max_bytes: int = 12000, label: str = "output"):
    lines = content.splitlines()
    byte_len = len(content.encode("utf-8", errors="ignore"))

    if len(lines) <= max_lines and byte_len <= max_bytes:
        return content, False, None

    # Offload full output to /tmp
    tmp_path = Path(f"/tmp/governor_{label}_{int(time.time()*1000)}.log")
    tmp_path.write_text(content, encoding="utf-8", errors="ignore")

    head_count = max_lines // 2
    tail_count = max_lines // 2
    omitted = len(lines) - (head_count + tail_count)

    head = lines[:head_count]
    tail = lines[-tail_count:] if tail_count > 0 else []

    clamped = (
        "\n".join(head) +
        f"\n\n[... {omitted} lines omitted by context-window-governor (Full log: {tmp_path}) ...]\n\n" +
        "\n".join(tail)
    )
    return clamped, True, str(tmp_path)

def main():
    parser = argparse.ArgumentParser(description="Context Window Governor & Token Budget Manager")
    subparsers = parser.add_subparsers(dest="command")

    # Budget
    budget_p = subparsers.add_parser("budget", help="Compute partition budget")
    budget_p.add_argument("--total", type=int, default=200000, help="Total context window (default: 200,000)")
    budget_p.add_argument("--used", type=int, required=True, help="Current tokens used")

    # Estimate
    est_p = subparsers.add_parser("estimate", help="Estimate tokens in a file or string")
    est_p.add_argument("target", help="File path or text string")

    # Clamp
    clamp_p = subparsers.add_parser("clamp", help="Clamp stdin or file to prevent context flooding")
    clamp_p.add_argument("--file", help="Input file path")
    clamp_p.add_argument("--max-lines", type=int, default=60, help="Max lines to retain (default: 60)")
    clamp_p.add_argument("--max-bytes", type=int, default=12000, help="Max bytes to retain (default: 12000)")
    clamp_p.add_argument("--label", default="output", help="Label prefix for offloaded log")

    args = parser.parse_args()

    if args.command == "budget":
        b = calculate_budget(args.total, args.used)
        print(f"📊 Context Budget Telemetry (Total: {b['total_window']:,} | Used: {b['current_used']:,} [{b['utilization_pct']}%])")
        print(f"   Remaining Safe Headroom: {b['remaining']:,} tokens")
        print("   Recommended Allocations for Current Turn:")
        for k, v in b["partitions"].items():
            print(f"    - {k.replace('_', ' ').title()}: {v:,} tokens max")

    elif args.command == "estimate":
        target_path = Path(args.target)
        if target_path.is_file():
            text = target_path.read_text(encoding="utf-8", errors="ignore")
            tok = estimate_tokens(text)
            print(f"📄 {target_path}: ~{tok:,} tokens ({len(text):,} chars, {len(text.splitlines()):,} lines)")
        else:
            tok = estimate_tokens(args.target)
            print(f"🔤 String: ~{tok:,} tokens ({len(args.target):,} chars)")

    elif args.command == "clamp":
        if args.file:
            content = Path(args.file).read_text(encoding="utf-8", errors="ignore")
        else:
            content = sys.stdin.read()

        clamped, was_clamped, path = clamp_content(content, args.max_lines, args.max_bytes, args.label)
        print(clamped)
        if was_clamped:
            sys.stderr.write(f"\n[!] context-window-governor: Clamped excessive output. Full raw output preserved at: {path}\n")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

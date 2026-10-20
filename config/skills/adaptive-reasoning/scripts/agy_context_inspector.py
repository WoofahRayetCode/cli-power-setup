#!/usr/bin/env python3
"""
Antigravity Context & Cost Inspector (agy-context)
Provides parity with 'claude /context' and 'claude /cost' for Antigravity CLI.
Inspects active conversation step trajectory, token consumption, prompt cache hit rates,
model allocation, and monetary savings.
"""

import argparse
import glob
import json
import os
import sqlite3
import sys

def fmt_tok(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}k"
    return str(n)

def find_target_conversation(cid=None):
    base_dir = os.path.expanduser("~/.gemini/antigravity-cli")
    if cid:
        cand = f"{base_dir}/brain/{cid}/.system_generated/logs/transcript.jsonl"
        if os.path.exists(cand):
            return cand, cid

    presence_locks = glob.glob(f"{base_dir}/presence/*.lock")
    if presence_locks:
        latest_lock = max(presence_locks, key=os.path.getmtime)
        active_cid = os.path.basename(latest_lock).replace(".lock", "")
        cand = f"{base_dir}/brain/{active_cid}/.system_generated/logs/transcript.jsonl"
        if os.path.exists(cand):
            return cand, active_cid

    transcripts = glob.glob(f"{base_dir}/brain/*/.system_generated/logs/transcript.jsonl")
    if transcripts:
        latest = max(transcripts, key=os.path.getmtime)
        cid = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(latest))))
        return latest, cid

    return None, None

def main():
    parser = argparse.ArgumentParser(description="Antigravity Context & Token Cost Inspector")
    parser.add_argument("--conversation", help="Specific conversation ID to inspect")
    parser.add_argument("--turns", type=int, default=10, help="Number of recent turns to display in trajectory table")
    parser.add_argument("--json", action="store_true", help="Output telemetry as JSON")
    args = parser.parse_args()

    transcript_path, cid = find_target_conversation(args.conversation)
    if not transcript_path or not os.path.exists(transcript_path):
        print("Error: No active Antigravity CLI conversation transcript found.")
        sys.exit(1)

    steps = []
    tot_cached = 0
    tot_uncached = 0
    tot_output = 0
    last_ctx = 0

    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                row = json.loads(line)
                if row.get("type") == "PLANNER_RESPONSE":
                    s_idx = row.get("step_index", len(steps) + 1)
                    c = row.get("cache_read_tokens", 0)
                    i = row.get("input_tokens", 0)
                    o = row.get("output_tokens", 0)
                    tools = [t.get("tool_name", "tool") for t in row.get("tool_calls", [])]
                    tool_desc = ", ".join(tools) if tools else "response"

                    tot_cached += c
                    tot_uncached += i
                    tot_output += o
                    last_ctx = c + i

                    turn_tot = c + i
                    hit_rate = (c / turn_tot * 100.0) if turn_tot > 0 else 0.0

                    steps.append({
                        "step": s_idx,
                        "action": tool_desc[:30],
                        "input": i,
                        "cached": c,
                        "output": o,
                        "hit_pct": hit_rate
                    })
            except Exception:
                pass

    total_in = tot_cached + tot_uncached
    overall_cache_pct = (tot_cached / total_in * 100.0) if total_in > 0 else 0.0
    ctx_cap = 1_000_000
    ctx_pct = (last_ctx / ctx_cap) * 100.0

    # Pricing estimation (Assuming $3.00/M base input, $0.30/M cached input, $15.00/M output)
    full_cost = (total_in / 1_000_000.0) * 3.00 + (tot_output / 1_000_000.0) * 15.00
    actual_cost = (tot_uncached / 1_000_000.0) * 3.00 + (tot_cached / 1_000_000.0) * 0.30 + (tot_output / 1_000_000.0) * 15.00
    dollars_saved = max(0.0, full_cost - actual_cost)

    if args.json:
        print(json.dumps({
            "conversation_id": cid,
            "total_steps": len(steps),
            "current_context_tokens": last_ctx,
            "context_capacity_pct": ctx_pct,
            "cumulative_cached_tokens": tot_cached,
            "cumulative_uncached_tokens": tot_uncached,
            "cumulative_output_tokens": tot_output,
            "cache_efficiency_pct": overall_cache_pct,
            "estimated_dollars_saved": dollars_saved
        }, indent=2))
        return

    print("\n=======================================================")
    print(" 📊 Antigravity Context & Token Cost Inspector         ")
    print("=======================================================")
    print(f"Conversation ID:    {cid}")
    print(f"Current Context:    {fmt_tok(last_ctx)} / 1.0M tokens ({ctx_pct:.1f}% capacity)")
    print(f"Cache Efficiency:   {overall_cache_pct:.1f}% cache hit rate")
    print(f"Cumulative Savings: {fmt_tok(tot_cached)} tokens cached (Est. ${dollars_saved:.2f} saved)")
    print("-------------------------------------------------------")
    print("Recent Step Trajectory (Last Turns):")
    print(f" {'Step':<6} {'Action / Tool':<28} {'Input':<9} {'Cached':<9} {'Out':<6} {'Hit %'}")
    print(" " + "-" * 66)

    for s in steps[-args.turns:]:
        print(f" #{s['step']:<5} {s['action']:<28} {fmt_tok(s['input']):<9} {fmt_tok(s['cached']):<9} {fmt_tok(s['output']):<6} {s['hit_pct']:>5.1f}%")

    print("-------------------------------------------------------")
    if ctx_pct >= 50.0:
        print("⚠️ [CONTEXT CAPACITY WARNING]: Context utilization exceeds 50%.")
        print("   Run /compact to compress conversation history and preserve rate limits.")
    else:
        print("✓ Context headroom healthy. No compaction currently needed.")
    print("=======================================================\n")

if __name__ == "__main__":
    main()

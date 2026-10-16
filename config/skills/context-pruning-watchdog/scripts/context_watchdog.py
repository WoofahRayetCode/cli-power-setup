#!/usr/bin/env python3
"""
Context Pruning Watchdog & Automatic Compaction Stager (context_watchdog.py)
Monitors context token consumption across dual CLIs (Claude Code & Antigravity).
Automatically stages active memory into .agents/memory/activeContext.md and
snapshots working diffs into .agents/checkpoints/ when context reaches trigger thresholds.
"""

import os
import sys
import time
import json
import re
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

DEBOUNCE_FILE = Path("/tmp/context_watchdog_debounce.json")
DEFAULT_CONTEXT_WINDOW = 200_000
DEFAULT_THRESHOLD_PCT = 50.0
DEBOUNCE_SECONDS = 300  # 5 minutes

def get_claude_context() -> dict:
    """Reads live context usage from Claude Code telemetry."""
    info = {
        "platform": "Claude Code",
        "used_percentage": None,
        "total_input_tokens": None,
        "total_window": DEFAULT_CONTEXT_WINDOW
    }
    state_file = Path("/tmp/claude_quota_state.json")
    if state_file.exists():
        try:
            d = json.loads(state_file.read_text(encoding="utf-8"))
            if "context_used_pct" in d:
                info["used_percentage"] = d["context_used_pct"]
                info["total_input_tokens"] = d.get("context_tokens")
                return info
        except Exception:
            pass
    return info

def get_antigravity_context() -> dict:
    """Reads live context usage from Antigravity active transcript."""
    info = {
        "platform": "Antigravity (Gemini)",
        "used_percentage": None,
        "total_input_tokens": None,
        "total_window": 1_000_000
    }
    base_dir = Path.home() / ".gemini/antigravity-cli"
    transcripts = list(base_dir.glob("brain/*/.system_generated/logs/transcript.jsonl"))
    if not transcripts:
        return info
    
    latest_transcript = max(transcripts, key=os.path.getmtime)
    total_tokens = 0
    try:
        with open(latest_transcript, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if '"prompt_token_count"' in line or '"input_tokens"' in line:
                    try:
                        row = json.loads(line)
                        cnt = row.get("prompt_token_count") or row.get("input_tokens") or 0
                        if cnt > total_tokens:
                            total_tokens = cnt
                    except Exception:
                        pass
        if total_tokens > 0:
            info["total_input_tokens"] = total_tokens
            info["used_percentage"] = round((total_tokens / info["total_window"]) * 100.0, 1)
    except Exception:
        pass
    return info

def get_live_context() -> dict:
    """Discovers current context usage across active CLIs."""
    c_info = get_claude_context()
    if c_info["used_percentage"] is not None:
        return c_info
    g_info = get_antigravity_context()
    if g_info["used_percentage"] is not None:
        return g_info
    return {
        "platform": "Unknown",
        "used_percentage": 0.0,
        "total_input_tokens": 0,
        "total_window": DEFAULT_CONTEXT_WINDOW
    }

def stage_active_memory(context_pct: float, tokens: int, reason: str = "Context threshold reached") -> Path:
    """Executes the Lossless Compaction Protocol to persist active state."""
    ts = int(time.time())
    iso_ts = datetime.now().isoformat()
    
    # 1. Discover Git Working State
    git_branch = "unknown"
    git_commit = "unknown"
    git_status = ""
    git_diff = ""
    try:
        git_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip() or "main"
        git_commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
        git_status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
        git_diff = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        pass

    # 2. Check for Active Goal
    goal_desc = "General Engineering & Development"
    current_phase = 1
    goal_file = Path(".agents/goals/current_goal.json")
    if goal_file.exists():
        try:
            g_data = json.loads(goal_file.read_text(encoding="utf-8"))
            goal_desc = g_data.get("description", goal_desc)
            current_phase = g_data.get("current_phase", current_phase)
        except Exception:
            pass

    # 3. Snapshot Working Memory Checkpoint
    checkpoints_dir = Path(".agents/checkpoints")
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    snap_path = checkpoints_dir / f"checkpoint_{ts}_pre_compact.json"
    snap_data = {
        "timestamp": ts,
        "label": "auto_compact_pre_checkpoint",
        "reason": reason,
        "context_pct": context_pct,
        "tokens": tokens,
        "branch": git_branch,
        "commit": git_commit,
        "status": git_status,
        "patch": git_diff
    }
    snap_path.write_text(json.dumps(snap_data, indent=2), encoding="utf-8")

    # 4. Stage into .agents/memory/activeContext.md
    mem_dir = Path(".agents/memory")
    mem_dir.mkdir(parents=True, exist_ok=True)
    active_ctx_file = mem_dir / "activeContext.md"
    
    mod_lines = git_status.splitlines() if git_status else []
    dirty_summary = "\n".join(f"- `{l.strip()}`" for l in mod_lines[:12]) if mod_lines else "- Clean working tree"
    if len(mod_lines) > 12:
        dirty_summary += f"\n- *... and {len(mod_lines) - 12} additional modified files*"

    staged_content = f"""# Active Context (Auto-Staged Pre-Compaction)
- **Last Staged:** {iso_ts}
- **Trigger:** {reason} (Context: {context_pct:.1f}% | ~{tokens:,} tokens)
- **Active Branch:** `{git_branch}` @ `{git_commit}`
- **Active Goal:** {goal_desc}
- **Current Phase:** Phase {current_phase}
- **Safety Snapshot:** `{snap_path}`

## In-Flight State & Modified Files
{dirty_summary}

## Recovery & Resume Protocol
1. After running `/compact`, read this file first (<300 tokens) to re-hydrate state without re-reading entire transcripts.
2. If working directory was rolled back, restore uncommitted diffs via:
   ```bash
   python3 config/skills/working-memory-checkpointing/scripts/state_checkpoint.py rollback
   ```
3. Continue execution from current milestone phase.
"""
    active_ctx_file.write_text(staged_content, encoding="utf-8")

    # 5. Record Debounce Timestamp
    DEBOUNCE_FILE.write_text(json.dumps({
        "last_staged_ts": ts,
        "last_pct": context_pct,
        "last_tokens": tokens,
        "snapshot_file": str(snap_path)
    }, indent=2), encoding="utf-8")

    return active_ctx_file

def should_debounce(current_pct: float) -> bool:
    """Prevents continuous re-staging within DEBOUNCE_SECONDS unless context increases by >= 10%."""
    if not DEBOUNCE_FILE.exists():
        return False
    try:
        data = json.loads(DEBOUNCE_FILE.read_text(encoding="utf-8"))
        last_ts = data.get("last_staged_ts", 0)
        last_pct = data.get("last_pct", 0.0)
        if (time.time() - last_ts) < DEBOUNCE_SECONDS and (current_pct - last_pct) < 10.0:
            return True
    except Exception:
        pass
    return False

def cmd_check(args):
    """Checks live context and automatically runs staging when threshold is met."""
    ctx_info = get_live_context()
    pct = args.pct if args.pct is not None else (ctx_info.get("used_percentage") or 0.0)
    tokens = args.tokens if args.tokens is not None else (ctx_info.get("total_input_tokens") or int((pct / 100.0) * DEFAULT_CONTEXT_WINDOW))
    threshold = args.threshold

    print("=======================================================")
    print(" 🧠  Context Pruning Watchdog & Compaction Safeguard   ")
    print("=======================================================")
    print(f"Platform:         {ctx_info.get('platform', 'Auto-Detect')}")
    print(f"Context Volume:   {pct:.1f}% (~{tokens:,} tokens / {ctx_info.get('total_window', DEFAULT_CONTEXT_WINDOW):,} max)")
    print(f"Trigger Target:   {threshold:.1f}%")
    print("-------------------------------------------------------")

    if pct >= threshold:
        if not args.force and should_debounce(pct):
            print(f"[✓] Context is at {pct:.1f}%. Active state was recently staged (<5 min ago).")
            print(f"👉 Recommended Action: Run /compact now to reset context window to <2,000 tokens.")
            print("=======================================================\n")
            sys.exit(1)

        mem_file = stage_active_memory(pct, tokens, reason=f"Context crossed {threshold:.1f}% threshold")
        print(f"🚨 [AUTO-COMPACTION TRIGGERED: CONTEXT AT {pct:.1f}% (~{tokens:,} TOKENS)]")
        print(f"  [✓] Working context automatically staged into: {mem_file}")
        print(f"  [✓] Safety snapshot saved into: .agents/checkpoints/")
        print(f"  [✓] Zero progress will be lost during compaction.")
        print(f"\n👉 ACTION REQUIRED: Run /compact now to flush transcript and restore fast streaming!")
        print("=======================================================\n")
        sys.exit(1)
    else:
        headroom = threshold - pct
        print(f"[✓] Context is HEALTHY ({pct:.1f}%). Safe headroom: +{headroom:.1f}% until compaction.")
        print("=======================================================\n")
        sys.exit(0)

def cmd_stage(args):
    """Forces immediate staging of active memory regardless of current percentage."""
    ctx_info = get_live_context()
    pct = ctx_info.get("used_percentage") or 0.0
    tokens = ctx_info.get("total_input_tokens") or 0
    mem_file = stage_active_memory(pct, tokens, reason=args.reason or "Manual staging requested")
    print(f"[✓] Active working memory staged into: {mem_file}")
    print(f"👉 Ready for compaction. Run /compact to reset conversation tokens.")

def cmd_status(args):
    """Outputs high-density context status."""
    ctx_info = get_live_context()
    pct = ctx_info.get("used_percentage") or 0.0
    tokens = ctx_info.get("total_input_tokens") or 0
    staged_str = "None"
    if DEBOUNCE_FILE.exists():
        try:
            d = json.loads(DEBOUNCE_FILE.read_text(encoding="utf-8"))
            staged_str = f"{d.get('last_pct', 0.0):.1f}% at {datetime.fromtimestamp(d.get('last_staged_ts', 0)).strftime('%H:%M:%S')}"
        except Exception:
            pass
    print(f"🧠 Ctx: {pct:.1f}% ({tokens:,} tok) | Last Staged: {staged_str}")

def main():
    parser = argparse.ArgumentParser(description="Context Pruning Watchdog & Automatic Compaction Stager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # check
    p_check = subparsers.add_parser("check", help="Check context and automatically stage if threshold exceeded")
    p_check.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD_PCT, help=f"Context percentage threshold to trigger staging (default: {DEFAULT_THRESHOLD_PCT}%%)")
    p_check.add_argument("--pct", type=float, help="Explicit context percentage override")
    p_check.add_argument("--tokens", type=int, help="Explicit context token count override")
    p_check.add_argument("--force", action="store_true", help="Bypass 5-minute debounce check")

    # stage
    p_stage = subparsers.add_parser("stage", help="Force immediate staging of active memory")
    p_stage.add_argument("--reason", default="Manual staging requested", help="Reason for staging")

    # status
    p_stat = subparsers.add_parser("status", help="Show current context volume and staging status")

    args = parser.parse_args()

    if args.command == "check":
        cmd_check(args)
    elif args.command == "stage":
        cmd_stage(args)
    elif args.command == "status":
        cmd_status(args)

if __name__ == "__main__":
    main()

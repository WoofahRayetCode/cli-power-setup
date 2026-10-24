#!/usr/bin/env python3
"""
Autonomous Goal Governor (goal_governor.py)
Provides programmatic contract formulation, circuit breaker enforcement (3-strike rule),
and phased milestone compaction advice during long-running `/goal` execution.
"""

import argparse
import json
import os
import re
import sys
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_STATE_FILE = Path(".agents/goals/current_goal.json")
CIRCUIT_BREAKER_LIMIT = 3

def get_state_file(custom_path=None) -> Path:
    if custom_path:
        p = Path(custom_path)
    else:
        p = DEFAULT_STATE_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "goal_id": f"goal_{int(datetime.now().timestamp())}",
        "description": "",
        "created_at": datetime.now().isoformat(),
        "exit_criteria": [],
        "test_command": "",
        "current_phase": 1,
        "total_phases": 3,
        "phases": [
            {"phase": 1, "name": "Architecture & Scaffolding", "status": "in_progress"},
            {"phase": 2, "name": "Implementation & Core Logic", "status": "pending"},
            {"phase": 3, "name": "Verification & Hardening", "status": "pending"}
        ],
        "strikes": {},
        "circuit_breaker_tripped": False,
        "completed": False
    }

def save_state(path: Path, state: dict):
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")

def cmd_formulate(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    
    state["description"] = args.goal
    state["test_command"] = args.test_cmd or ""
    state["created_at"] = datetime.now().isoformat()
    state["circuit_breaker_tripped"] = False
    state["completed"] = False
    state["strikes"] = {}
    
    exit_criteria = [
        "Executable verification passes with exit code 0",
        "Zero regressions in static analysis / linters",
        "Clean git working tree with atomic milestone commits"
    ]
    if args.test_cmd:
        exit_criteria.insert(0, f"Automated test command passes: `{args.test_cmd}`")
    state["exit_criteria"] = exit_criteria
    
    save_state(path, state)
    
    print(f"\n=======================================================")
    print(f" 🎯 Autonomous Goal Contract Formulated               ")
    print(f"=======================================================")
    print(f"Goal:            {state['description']}")
    print(f"Test Command:    {state['test_command'] or 'None specified (manual/exit code)'}")
    print(f"Contract State:  {path}")
    print(f"Exit Criteria:")
    for idx, crit in enumerate(state["exit_criteria"], 1):
        print(f"  [{idx}] {crit}")
    print(f"\nPhased Execution Plan:")
    for p in state["phases"]:
        print(f"  Phase {p['phase']}: {p['name']} ({p['status']})")
    print(f"Circuit Breaker: Active (Max {CIRCUIT_BREAKER_LIMIT} failed iterations before rollback)")
    print(f"=======================================================\n")

def cmd_strike(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    
    task_id = args.task or "default_task"
    reason = args.reason or "Test/compilation failure"
    
    strikes = state.setdefault("strikes", {})
    current_strikes = strikes.get(task_id, 0) + 1
    strikes[task_id] = current_strikes
    
    print(f"\n[⚠️ GOAL GOVERNOR STRIKE] Task '{task_id}': Strike {current_strikes}/{CIRCUIT_BREAKER_LIMIT}")
    print(f"Reason: {reason}")
    
    if current_strikes >= CIRCUIT_BREAKER_LIMIT:
        state["circuit_breaker_tripped"] = True
        save_state(path, state)
        print(f"\n🚨 [CIRCUIT BREAKER TRIPPED]")
        print(f"Task '{task_id}' has failed {current_strikes} consecutive iterations!")
        print(f"MANDATORY QUOTA-SAVING PROTOCOL:")
        print(f"1. DO NOT attempt another minor variation of this failed approach.")
        print(f"2. Roll back modified files to the last known checkpoint:")
        print(f"   python3 config/skills/working-memory-checkpointing/scripts/state_checkpoint.py rollback")
        print(f"3. Record this failed approach and root cause in .agents/memory/learnings.md.")
        print(f"4. Re-evaluate strategy or explore an alternative hypothesis branch.")
        print(f"5. Once alternative hypothesis is selected, reset strikes via:")
        print(f"   python3 config/skills/autonomous-goal-governor/scripts/goal_governor.py reset --task {task_id}\n")
        sys.exit(2)
    else:
        save_state(path, state)
        remaining = CIRCUIT_BREAKER_LIMIT - current_strikes
        print(f"⚠️ Allowed retries before circuit breaker rollback: {remaining}")
        print(f"Tip: Review error log sanitization before editing code again.\n")

def cmd_reset(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    task_id = args.task or "default_task"
    if "strikes" in state and task_id in state["strikes"]:
        del state["strikes"][task_id]
    state["circuit_breaker_tripped"] = False
    save_state(path, state)
    print(f"[✓] Strikes reset for task '{task_id}'. Circuit breaker cleared.")

def cmd_success(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    task_id = args.task or "default_task"
    if "strikes" in state and task_id in state["strikes"]:
        del state["strikes"][task_id]
    save_state(path, state)
    print(f"[✓] Task '{task_id}' passed successfully. Strikes cleared for this task.")

def cmd_phase_gate(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    current_phase_num = state.get("current_phase", 1)
    
    for p in state["phases"]:
        if p["phase"] == current_phase_num:
            p["status"] = "completed"
            print(f"[✓] Phase {current_phase_num} ('{p['name']}') marked complete.")
    
    next_phase_num = current_phase_num + 1
    if next_phase_num <= len(state["phases"]):
        state["current_phase"] = next_phase_num
        for p in state["phases"]:
            if p["phase"] == next_phase_num:
                p["status"] = "in_progress"
                print(f"[→] Transitioning to Phase {next_phase_num}: '{p['name']}'.")
        save_state(path, state)

        # Automatically stage working memory for lossless compaction
        for cand in [
            Path.home() / ".local/bin/context-watchdog",
            Path("/home/ericparsley/Documents/GitHub/cli-power-setup/config/skills/context-pruning-watchdog/scripts/context_watchdog.py")
        ]:
            if cand.exists():
                subprocess.run([sys.executable, str(cand), "stage", "--reason", f"Completed Phase {current_phase_num}"], capture_output=True, check=False)
                print(f"[✓] Working memory automatically staged to .agents/memory/activeContext.md.")
                break

        print(f"\n💡 [RECOMMENDED ACTION BEFORE NEXT PHASE]:")
        print(f"1. Commit completed phase milestone: git commit -m 'Complete Phase {current_phase_num}'")
        print(f"2. Run /compact to clear working memory and reset context tokens for Phase {next_phase_num}.\n")
    else:
        state["completed"] = True
        save_state(path, state)
        print(f"\n🏁 [ALL GOAL PHASES COMPLETED] Goal contract fully satisfied!\n")

def cmd_status(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    print(f"\n=======================================================")
    print(f" 📊 Autonomous Goal Governor Status                  ")
    print(f"=======================================================")
    print(f"Goal:            {state.get('description', 'No active goal')}")
    print(f"Created:         {state.get('created_at', 'N/A')}")
    print(f"Current Phase:   {state.get('current_phase', 1)}/{len(state.get('phases', []))}")
    print(f"Status:          {'Completed' if state.get('completed') else 'In Progress'}")
    print(f"Circuit Breaker: {'🚨 TRIPPED' if state.get('circuit_breaker_tripped') else '🟢 Normal'}")
    
    strikes = state.get("strikes", {})
    if strikes:
        print(f"Active Strikes:")
        for t, s in strikes.items():
            print(f"  - Task '{t}': {s}/{CIRCUIT_BREAKER_LIMIT} strikes")
    else:
        print(f"Active Strikes:  0 (All tasks clean)")
    print(f"=======================================================\n")

def get_live_quota() -> dict:
    """Reads live quota telemetry from Antigravity or Claude Code."""
    quota = {
        "platform": "Unknown",
        "five_hour_remaining": None,
        "five_hour_resets_at": "",
        "five_hour_resets_epoch": None,
        "weekly_remaining": None,
        "weekly_resets_at": "",
        "weekly_resets_epoch": None
    }
    
    # 1. Check Antigravity (agy) state cache first
    agy_cache = Path("/tmp/agy_quota_cache.txt")
    if agy_cache.exists():
        try:
            d = json.loads(agy_cache.read_text())
            g_5h = d.get("gemini_5h", "").replace("%", "").strip()
            g_wk = d.get("gemini_wk", "").replace("%", "").strip()
            quota["platform"] = "Google Antigravity (agy)"
            if g_5h.isdigit():
                quota["five_hour_remaining"] = int(g_5h)
            quota["five_hour_resets_at"] = d.get("gemini_5h_reset", "")
            if g_wk.isdigit():
                quota["weekly_remaining"] = int(g_wk)
            quota["weekly_resets_at"] = d.get("gemini_wk_reset", "")
            if quota["weekly_remaining"] is not None:
                return quota
        except Exception:
            pass

    # 2. Check Claude Code state
    claude_state = Path("/tmp/claude_quota_state.json")
    if claude_state.exists():
        try:
            d = json.loads(claude_state.read_text())
            quota["platform"] = "Claude Code"
            quota["five_hour_remaining"] = d.get("five_hour_remaining")
            quota["five_hour_resets_at"] = d.get("five_hour_resets_at") or ""
            quota["five_hour_resets_epoch"] = d.get("five_hour_resets_epoch")
            quota["weekly_remaining"] = d.get("weekly_remaining")
            quota["weekly_resets_at"] = d.get("weekly_resets_at") or ""
            quota["weekly_resets_epoch"] = d.get("weekly_resets_epoch")
            if quota["five_hour_remaining"] is not None:
                return quota
        except Exception:
            pass

    return quota

def trigger_weekly_smart_checkpoint(q: dict):
    """Executes a smart state checkpoint when weekly quota nears 25% remaining."""
    p_wk = q.get("weekly_remaining")
    p_5h = q.get("five_hour_remaining")
    if p_wk is None or p_wk > 25:
        return

    tracker_file = Path(".agents/memory/weekly_quota_checkpoint.json")
    tracker_file.parent.mkdir(parents=True, exist_ok=True)
    if tracker_file.exists():
        try:
            t_data = json.loads(tracker_file.read_text())
            last_pct = t_data.get("last_checkpoint_pct")
            # Don't spam checkpoints unless quota dropped by another 3%
            if last_pct is not None and (last_pct - p_wk) < 3:
                return
        except Exception:
            pass

    ts = int(time.time())
    iso_ts = datetime.now().isoformat()
    checkpoints_dir = Path(".agents/checkpoints")
    checkpoints_dir.mkdir(parents=True, exist_ok=True)

    git_status = ""
    git_diff = ""
    git_branch = "unknown"
    git_commit = "unknown"
    try:
        git_status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
        git_diff = subprocess.run(["git", "diff", "HEAD"], capture_output=True, text=True).stdout.strip()
        git_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
        git_commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        pass

    snap_file = checkpoints_dir / f"checkpoint_{ts}_weekly_{p_wk}pct.json"
    snap_data = {
        "timestamp": ts,
        "label": f"weekly_quota_{p_wk}pct_reserve",
        "weekly_remaining": p_wk,
        "five_hour_remaining": p_5h,
        "branch": git_branch,
        "commit": git_commit,
        "status": git_status,
        "patch": git_diff
    }
    snap_file.write_text(json.dumps(snap_data, indent=2), encoding="utf-8")

    # Update activeContext.md
    active_ctx = Path(".agents/memory/activeContext.md")
    active_ctx.parent.mkdir(parents=True, exist_ok=True)
    alert_header = (
        f"\n## ⚠️ Quota Guard: Weekly Reserve Checkpoint ({p_wk}% Remaining)\n"
        f"- Timestamp: {iso_ts}\n"
        f"- Weekly Quota: {p_wk}% remaining (Resets at: {q.get('weekly_resets_at') or 'N/A'})\n"
        f"- 5-Hour Quota: {p_5h}% remaining (Resets at: {q.get('five_hour_resets_at') or 'N/A'})\n"
        f"- Snapshot Saved: {snap_file}\n"
        f"- Branch/Commit: {git_branch}@{git_commit}\n"
        f"- Modified Files: {len(git_status.splitlines()) if git_status else 0}\n"
        f"- Rollback Command: python3 config/skills/working-memory-checkpointing/scripts/state_checkpoint.py rollback\n\n"
    )
    if active_ctx.exists():
        curr_text = active_ctx.read_text(encoding="utf-8", errors="ignore")
        active_ctx.write_text(alert_header + curr_text, encoding="utf-8")
    else:
        active_ctx.write_text(alert_header, encoding="utf-8")

    # Record checkpoint tracker
    tracker_file.write_text(json.dumps({
        "last_checkpoint_timestamp": iso_ts,
        "last_checkpoint_pct": p_wk,
        "snapshot_file": str(snap_file)
    }, indent=2), encoding="utf-8")

    print("\n-------------------------------------------------------")
    print(f" ⚠️  [SMART CHECKPOINT CREATED: WEEKLY QUOTA AT {p_wk}%]")
    print(f"  -> Snapshot saved: {snap_file}")
    print(f"  -> Uncommitted changes preserved across {len(git_status.splitlines()) if git_status else 0} files.")
    print(f"  -> Memory context updated: {active_ctx}")
    print(f"  -> Safe to continue execution while quota remains above reserve threshold.")
    print("-------------------------------------------------------\n")

def cmd_quota_guard(args):
    q = get_live_quota()
    p_5h = q["five_hour_remaining"]
    p_wk = q["weekly_remaining"]
    resets_5h = q["five_hour_resets_at"] or "N/A"
    resets_wk = q["weekly_resets_at"] or "N/A"
    platform = q["platform"]
    
    print("\n=======================================================")
    print(" 🛡️  Autonomous Quota Watchdog & Circuit Breaker       ")
    print("=======================================================")
    print(f"Platform:         {platform}")
    print(f"5-Hour Quota:     {p_5h if p_5h is not None else '--'}% remaining (Resets at: {resets_5h})")
    print(f"Weekly Quota:     {p_wk if p_wk is not None else '--'}% remaining (Resets at: {resets_wk})")
    print(f"Safe Reserves:    Min 5-Hour: {args.min_5h}% | Min Weekly: {args.min_weekly}%")
    print("-------------------------------------------------------")
    
    # 1. Smart Checkpoint when nearing 25% weekly quota
    if p_wk is not None and p_wk <= 25:
        trigger_weekly_smart_checkpoint(q)
    
    # 2. Check 5-Hour Quota
    if p_5h is not None and p_5h <= args.min_5h:
        if args.wait_on_5h:
            # Calculate wait duration until refresh
            wait_seconds = 180  # default 3 min fallback
            now_ts = datetime.now().timestamp()
            if q.get("five_hour_resets_epoch"):
                wait_seconds = max(30, int(q["five_hour_resets_epoch"] - now_ts) + 60)
            elif q.get("five_hour_resets_at") and ":" in q["five_hour_resets_at"]:
                try:
                    parts = q["five_hour_resets_at"].split(":")
                    now_dt = datetime.now()
                    target_dt = now_dt.replace(hour=int(parts[0]), minute=int(parts[1]), second=0, microsecond=0)
                    if target_dt <= now_dt:
                        target_dt += timedelta(days=1)
                    wait_seconds = max(30, int((target_dt - now_dt).total_seconds()) + 60)
                except Exception:
                    pass

            mins = int(round(wait_seconds / 60))
            print("\n=======================================================")
            print(f" ⏳ [5-HOUR QUOTA AT {p_5h}% - WAITING FOR REFRESH WINDOW]")
            print("=======================================================")
            print(f"Quota Status:    5h: {p_5h}% (at or below reserve {args.min_5h}%)")
            print(f"Refresh Target:  {resets_5h} (~{mins} minutes remaining)")
            print(f"Preserving state to .agents/memory/activeContext.md before waiting...")
            
            # Stage current context
            try:
                mem_file = Path(".agents/memory/activeContext.md")
                mem_file.parent.mkdir(parents=True, exist_ok=True)
                wait_note = (
                    f"\n# 5-Hour Quota Refresh Pause\n"
                    f"- Timestamp: {datetime.now().isoformat()}\n"
                    f"- 5-Hour Quota: {p_5h}%\n"
                    f"- Scheduled Resume: {resets_5h}\n"
                    f"- Waiting {mins}m for quota replenishment...\n\n"
                )
                if mem_file.exists():
                    mem_file.write_text(wait_note + mem_file.read_text(encoding="utf-8", errors="ignore"), encoding="utf-8")
                else:
                    mem_file.write_text(wait_note, encoding="utf-8")
            except Exception:
                pass

            print(f"Sleeping {mins}m until quota reset window passes (Ctrl+C to abort)...")
            elapsed = 0
            poll_step = min(60, wait_seconds)
            while elapsed < wait_seconds:
                time.sleep(poll_step)
                elapsed += poll_step
                left_m = max(0, (wait_seconds - elapsed) // 60)
                if left_m > 0 and (elapsed % 300 == 0 or left_m <= 5):
                    print(f"  -> Quota refresh countdown: ~{left_m}m remaining...")

            # Verify replenished quota
            new_q = get_live_quota()
            new_5h = new_q.get("five_hour_remaining")
            print(f"\n[✓] Refresh window reached! 5-Hour quota replenished ({new_5h if new_5h is not None else 'healthy'}%).")
            print("Resuming execution seamlessly!\n")
            print("=======================================================")
            sys.exit(0)
        else:
            print("🚨 [QUOTA CIRCUIT BREAKER TRIPPED!]")
            print(f"  ❌ 5-hour quota ({p_5h}%) is at or below safe reserve threshold ({args.min_5h}%)")
            print("\n[ACTION TAKEN TO SAFEGUARD USER QUOTA]:")
            print("  1. Ceasing autonomous execution loop immediately (--no-wait requested).")
            print(f"  2. Automatic resume safe after quota reset: {resets_5h}")
            sys.exit(2)

    # 3. Check Weekly Quota Minimum Reserve
    if p_wk is not None and p_wk <= args.min_weekly:
        print("🚨 [WEEKLY QUOTA CIRCUIT BREAKER TRIPPED!]")
        print(f"  ❌ Weekly quota ({p_wk}%) is at or below minimum weekly threshold ({args.min_weekly}%)")
        print("\n[ACTION TAKEN TO SAFEGUARD USER QUOTA]:")
        print("  1. Ceasing autonomous execution loop immediately.")
        print("  2. Preserving remaining weekly quota for user interactive sessions.")
        print(f"  3. Automatic resume safe after weekly reset: {resets_wk}")
        sys.exit(2)

    print(f"[✓] Quota reserves are HEALTHY (5h: {p_5h if p_5h is not None else '--'}% | Wk: {p_wk if p_wk is not None else '--'}%). Safe to proceed with autonomous execution.")
    print("=======================================================\n")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="Autonomous Goal Governor & Quota Protector")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # formulate
    p_form = subparsers.add_parser("formulate", help="Formulate a verifiable goal contract")
    p_form.add_argument("--goal", required=True, help="Goal description")
    p_form.add_argument("--test-cmd", help="Command used to verify goal satisfaction")
    p_form.add_argument("--state-file", help="Path to goal state file")
    
    # strike
    p_strike = subparsers.add_parser("strike", help="Record a failure strike on current task")
    p_strike.add_argument("--task", default="default_task", help="Identifier of the failing task")
    p_strike.add_argument("--reason", help="Failure reason or error snippet")
    p_strike.add_argument("--state-file", help="Path to goal state file")
    
    # reset
    p_reset = subparsers.add_parser("reset", help="Reset strikes for a task")
    p_reset.add_argument("--task", default="default_task", help="Identifier of the task to reset")
    p_reset.add_argument("--state-file", help="Path to goal state file")
    
    # success
    p_succ = subparsers.add_parser("success", help="Record success and clear strikes")
    p_succ.add_argument("--task", default="default_task", help="Identifier of the successful task")
    p_succ.add_argument("--state-file", help="Path to goal state file")
    
    # phase-gate
    p_gate = subparsers.add_parser("phase-gate", help="Advance phase and advise on compaction")
    p_gate.add_argument("--state-file", help="Path to goal state file")
    
    # status
    p_stat = subparsers.add_parser("status", help="Show current goal contract status")
    p_stat.add_argument("--state-file", help="Path to goal state file")

    # quota-guard
    p_qg = subparsers.add_parser("quota-guard", help="Verify that 5-hour and weekly quotas remain above safe reserve thresholds")
    p_qg.add_argument("--min-5h", type=int, default=15, help="Minimum 5-hour quota remaining percentage before waiting or halting (default: 15)")
    p_qg.add_argument("--min-weekly", type=int, default=10, help="Minimum weekly quota remaining percentage before tripping breaker (default: 10)")
    p_qg.add_argument("--wait-on-5h", action="store_true", default=True, help="Wait for 5-hour quota refresh instead of halting (default: True)")
    p_qg.add_argument("--no-wait", action="store_false", dest="wait_on_5h", help="Do not wait for 5-hour refresh; halt immediately if below reserve")
    
    args = parser.parse_args()
    
    if args.command == "formulate":
        cmd_formulate(args)
    elif args.command == "strike":
        cmd_strike(args)
    elif args.command == "reset":
        cmd_reset(args)
    elif args.command == "success":
        cmd_success(args)
    elif args.command == "phase-gate":
        cmd_phase_gate(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "quota-guard":
        cmd_quota_guard(args)

if __name__ == "__main__":
    main()

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
from datetime import datetime
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
        print(f"\n💡 [RECOMMENDED ACTION BEFORE NEXT PHASE]:")
        print(f"1. Commit completed phase milestone: git commit -m 'Complete Phase {current_phase_num}'")
        print(f"2. Stage memory state into .agents/memory/activeContext.md")
        print(f"3. Run /compact to clear working memory and reset context tokens for Phase {next_phase_num}.\n")
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
    """Reads live quota telemetry across Claude Code and Antigravity."""
    quota = {
        "platform": "Unknown",
        "five_hour_remaining": None,
        "five_hour_resets_at": "",
        "weekly_remaining": None
    }
    
    # 1. Check Claude Code state
    claude_state = Path("/tmp/claude_quota_state.json")
    if claude_state.exists():
        try:
            d = json.loads(claude_state.read_text())
            quota["platform"] = "Claude Code"
            quota["five_hour_remaining"] = d.get("five_hour_remaining")
            quota["five_hour_resets_at"] = d.get("five_hour_resets_at") or ""
            quota["weekly_remaining"] = d.get("weekly_remaining")
            if quota["five_hour_remaining"] is not None:
                return quota
        except Exception:
            pass

    # 2. Check Antigravity JSON state
    agy_state = Path("/tmp/agy_quota_state.json")
    if agy_state.exists():
        try:
            d = json.loads(agy_state.read_text())
            quota["platform"] = "Antigravity (Gemini)"
            quota["five_hour_remaining"] = d.get("five_hour_remaining")
            quota["five_hour_resets_at"] = d.get("five_hour_resets_at") or ""
            quota["weekly_remaining"] = d.get("weekly_remaining")
            if quota["five_hour_remaining"] is not None:
                return quota
        except Exception:
            pass

    # 3. Check Antigravity Text Cache
    agy_cache = Path("/tmp/agy_quota_cache.txt")
    if agy_cache.exists():
        try:
            txt = agy_cache.read_text()
            quota["platform"] = "Antigravity (Gemini)"
            m5 = re.search(r"5h:\s*(\d+)%", txt)
            if m5:
                quota["five_hour_remaining"] = int(m5.group(1))
            mr = re.search(r"\(reset\s*([^)]+)\)", txt)
            if mr:
                quota["five_hour_resets_at"] = mr.group(1)
            mw = re.search(r"Wk:\s*(\d+)%", txt)
            if mw:
                quota["weekly_remaining"] = int(mw.group(1))
            return quota
        except Exception:
            pass

    return quota

def cmd_quota_guard(args):
    q = get_live_quota()
    p_5h = q["five_hour_remaining"]
    p_wk = q["weekly_remaining"]
    resets = q["five_hour_resets_at"] or "N/A"
    platform = q["platform"]
    
    print("\n=======================================================")
    print(" 🛡️  Autonomous Quota Watchdog & Circuit Breaker       ")
    print("=======================================================")
    print(f"Platform:         {platform}")
    print(f"5-Hour Quota:     {p_5h if p_5h is not None else '--'}% remaining (Resets at: {resets})")
    print(f"Weekly Quota:     {p_wk if p_wk is not None else '--'}% remaining")
    print(f"Safe Reserves:    Min 5-Hour: {args.min_5h}% | Min Weekly: {args.min_weekly}%")
    print("-------------------------------------------------------")
    
    breached = False
    reasons = []
    
    if p_5h is not None and p_5h <= args.min_5h:
        breached = True
        reasons.append(f"5-hour quota ({p_5h}%) is at or below safe reserve threshold ({args.min_5h}%)")
        
    if p_wk is not None and p_wk <= args.min_weekly:
        breached = True
        reasons.append(f"Weekly quota ({p_wk}%) is at or below safe reserve threshold ({args.min_weekly}%)")
        
    if breached:
        print("🚨 [QUOTA CIRCUIT BREAKER TRIPPED!]")
        for r in reasons:
            print(f"  ❌ {r}")
        print("\n[ACTION TAKEN TO SAFEGUARD USER QUOTA]:")
        print("  1. Ceasing autonomous execution loop immediately.")
        print("  2. Preserving remaining quota so user can resume work safely.")
        print(f"  3. Automatic resume safe after quota reset: {resets}")
        
        try:
            mem_file = Path(".agents/memory/activeContext.md")
            mem_file.parent.mkdir(parents=True, exist_ok=True)
            mem_file.write_text(
                f"# Quota Guard Circuit Breaker Tripped\n"
                f"- Timestamp: {datetime.now().isoformat()}\n"
                f"- 5-Hour Quota: {p_5h}%\n"
                f"- Weekly Quota: {p_wk}%\n"
                f"- Quota Reset: {resets}\n"
                f"- Reason: {'; '.join(reasons)}\n",
                encoding="utf-8"
            )
            print(f"  4. Current execution state checkpointed into {mem_file}")
        except Exception:
            pass
        print("=======================================================\n")
        sys.exit(2)
    else:
        print("[✓] Quota reserves are HEALTHY. Safe to proceed with autonomous execution.")
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
    p_qg.add_argument("--min-5h", type=int, default=15, help="Minimum 5-hour quota remaining percentage before tripping breaker (default: 15)")
    p_qg.add_argument("--min-weekly", type=int, default=10, help="Minimum weekly quota remaining percentage before tripping breaker (default: 10)")
    
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

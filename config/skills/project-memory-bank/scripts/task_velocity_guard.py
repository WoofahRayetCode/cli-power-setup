#!/usr/bin/env python3
"""
Task Velocity & Timeboxing Governor (task_velocity_guard.py)
============================================================
Enforces strict task velocity, step budgeting, anti-thrashing heuristics,
and diminishing-returns boundaries so agent engineering workflows never
take longer than necessary or fall into endless iterative rabbit holes.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

LEDGER_PATH = Path("/tmp/task_velocity_ledger.json")


def load_ledger() -> Dict[str, Any]:
    """Load or initialize active velocity tracking ledger."""
    if LEDGER_PATH.exists():
        try:
            return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "active_task": None,
        "start_time": None,
        "max_minutes": 15,
        "step_budget": 10,
        "steps": [],
        "file_edits": {},
        "churn_warnings": 0
    }


def save_ledger(data: Dict[str, Any]) -> None:
    """Persist ledger to disk."""
    LEDGER_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def start_task(name: str, step_budget: int = 10, max_minutes: int = 15) -> Dict[str, Any]:
    """Initialize a timeboxed task with explicit step and duration budgets."""
    data = {
        "active_task": name,
        "start_time": time.time(),
        "max_minutes": max_minutes,
        "step_budget": step_budget,
        "steps": [],
        "file_edits": {},
        "churn_warnings": 0
    }
    save_ledger(data)
    return data


def record_step(action_desc: str, target_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Record an execution step.
    Evaluates:
    - Step budget saturation
    - Duration timebox
    - File churn frequency (>= 3 edits triggers loop breaker)
    """
    ledger = load_ledger()
    if not ledger.get("active_task"):
        # Auto-start generic task if none active
        ledger = start_task("unnamed_task", step_budget=10, max_minutes=15)

    now = time.time()
    elapsed_sec = now - ledger["start_time"]
    step_num = len(ledger["steps"]) + 1

    alerts = []

    # Check step budget
    if step_num > ledger["step_budget"]:
        alerts.append(f"⚠️ STEP BUDGET EXCEEDED: Step {step_num}/{ledger['step_budget']}. Diminishing returns threshold reached. Wrap up task immediately.")

    # Check timebox
    elapsed_min = elapsed_sec / 60.0
    if elapsed_min > ledger["max_minutes"]:
        alerts.append(f"⏱️ TIMEBOX EXCEEDED: Elapsed {elapsed_min:.1f}m > limit of {ledger['max_minutes']}m. Stop speculative exploration.")

    # Check file churn
    if target_file:
        norm_file = str(Path(target_file).resolve())
        count = ledger["file_edits"].get(norm_file, 0) + 1
        ledger["file_edits"][norm_file] = count
        if count >= 3:
            alerts.append(f"🔄 CHURN LOOP DETECTED: File '{Path(target_file).name}' modified {count} times! Halt trial-and-error editing.")
            ledger["churn_warnings"] += 1

    step_record = {
        "step": step_num,
        "timestamp": now,
        "elapsed_sec": round(elapsed_sec, 1),
        "action": action_desc,
        "file": target_file,
        "alerts": alerts
    }
    ledger["steps"].append(step_record)
    save_ledger(ledger)

    return {
        "step": step_num,
        "elapsed_minutes": round(elapsed_min, 1),
        "alerts": alerts,
        "status": "AT_RISK" if alerts else "HEALTHY"
    }


def get_status() -> Dict[str, Any]:
    """Retrieve current velocity and budget health."""
    ledger = load_ledger()
    if not ledger.get("active_task"):
        return {"status": "IDLE", "message": "No active task currently governed."}

    elapsed_min = (time.time() - ledger["start_time"]) / 60.0
    steps_used = len(ledger["steps"])
    budget = ledger["step_budget"]
    percent_steps = (steps_used / budget) * 100 if budget else 0

    return {
        "status": "RUNNING",
        "task": ledger["active_task"],
        "elapsed_minutes": round(elapsed_min, 1),
        "max_minutes": ledger["max_minutes"],
        "steps_used": steps_used,
        "step_budget": budget,
        "budget_consumption_pct": round(percent_steps, 1),
        "churn_warnings": ledger["churn_warnings"],
        "file_edits": ledger["file_edits"]
    }


def conclude_task() -> Dict[str, Any]:
    """Conclude task and return performance summary."""
    status = get_status()
    if status["status"] == "IDLE":
        return status

    # Clear active task
    save_ledger({"active_task": None})
    return status


def main():
    parser = argparse.ArgumentParser(description="Task Velocity & Timeboxing Governor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # start
    start_p = subparsers.add_parser("start", help="Start governing a new task")
    start_p.add_argument("name", type=str, help="Task name")
    start_p.add_argument("--steps", type=int, default=8, help="Maximum step budget (default: 8)")
    start_p.add_argument("--minutes", type=int, default=15, help="Timebox duration in minutes (default: 15)")

    # step
    step_p = subparsers.add_parser("step", help="Record a step and check velocity health")
    step_p.add_argument("action", type=str, help="Action description")
    step_p.add_argument("--file", type=str, default=None, help="Target file being modified")

    # status
    subparsers.add_parser("status", help="Get current velocity telemetry")

    # finish
    subparsers.add_parser("finish", help="Conclude task and print velocity summary")

    args = parser.parse_args()

    if args.command == "start":
        res = start_task(args.name, step_budget=args.steps, max_minutes=args.minutes)
        print(f"⚡ [Velocity Guard Started] Task: '{args.name}' | Step Budget: {args.steps} | Timebox: {args.minutes}m")

    elif args.command == "step":
        res = record_step(args.action, target_file=args.file)
        print(f"Step {res['step']} ({res['elapsed_minutes']}m) - Health: [{res['status']}]")
        for alert in res["alerts"]:
            print(f"  {alert}", file=sys.stderr)

    elif args.command == "status":
        st = get_status()
        if st["status"] == "IDLE":
            print("[Velocity Guard] Idle. No active task.")
        else:
            print(f"⚡ Task Velocity: {st['task']}")
            print(f"  • Steps:   {st['steps_used']}/{st['step_budget']} ({st['budget_consumption_pct']}%)")
            print(f"  • Time:    {st['elapsed_minutes']}m / {st['max_minutes']}m")
            print(f"  • Churn:   {st['churn_warnings']} warnings")

    elif args.command == "finish":
        st = conclude_task()
        print(f"[✓] Task Concluded. Total Steps: {st.get('steps_used', 0)}, Duration: {st.get('elapsed_minutes', 0)}m.")


if __name__ == "__main__":
    main()

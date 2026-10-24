#!/usr/bin/env python3
"""
Autonomous Anti-Stuck Game Test Watchdog (game_test_watchdog.py)
Monitors game executables and test runners for freezes, infinite loops,
log stagnation, and orphaned background processes. Autonomously captures
screen diagnostics, sweeps modals, and terminates hung process trees.
"""

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def find_pids_by_pattern(pattern: str) -> list[int]:
    """Finds process IDs matching regex pattern."""
    try:
        res = subprocess.run(["pgrep", "-f", pattern], capture_output=True, text=True)
        return [int(p) for p in res.stdout.strip().split() if p.isdigit()]
    except Exception:
        return []


def get_process_cpu_mem(pid: int) -> tuple[float, float]:
    """Returns (cpu_pct, mem_pct) for a given pid."""
    try:
        res = subprocess.run(["ps", "-p", str(pid), "-o", "%cpu,%mem"], capture_output=True, text=True)
        lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
        if len(lines) >= 2:
            parts = lines[1].split()
            return float(parts[0]), float(parts[1])
    except Exception:
        pass
    return 0.0, 0.0


def sweep_game_processes(patterns: list[str] = None) -> list[dict]:
    """Terminates orphaned game and crash dialog processes."""
    if patterns is None:
        patterns = ["xrEngine", "umu-run", "pressure-vessel", "notepad.exe", "BugTrap"]

    killed = []
    for pat in patterns:
        pids = find_pids_by_pattern(pat)
        for pid in pids:
            if pid == os.getpid():
                continue
            try:
                # Read cmdline for reporting
                cmd = Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\x00", b" ").decode(errors="ignore").strip()
                # Kill process group if leader, else process
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.2)
                try:
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                killed.append({"pid": pid, "pattern": pat, "cmd": cmd[:120]})
            except Exception:
                pass
    return killed


def capture_window_screenshot(output_path: Path) -> bool:
    """Attempts to capture game window screenshot via import/scrot."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        # Search for game window
        xprop = subprocess.run(["xprop", "-root", "_NET_CLIENT_LIST"], capture_output=True, text=True)
        wids = re.findall(r"0x[0-9a-f]+", xprop.stdout.lower())
        for wid in wids:
            info = subprocess.run(["xprop", "-id", wid, "WM_CLASS", "WM_NAME"], capture_output=True, text=True)
            if re.search(r"xrengine|stalker|ogsr|wine|game", info.stdout, re.IGNORECASE):
                subprocess.run(["import", "-window", wid, str(output_path)], capture_output=True, timeout=5)
                return output_path.exists()
    except Exception:
        pass
    return False


def monitor_game_test(pattern: str, log_file: Path, timeout_stagnant: float, max_loops: int, max_duration: float, auto_kill: bool) -> dict:
    """Monitors running game test for stalls, thrashing, and freezes."""
    start_ts = time.time()
    last_log_size = -1
    last_log_change_ts = time.time()
    recent_lines = []

    print(f"[Watchdog Active] Pattern: '{pattern}' | Log: {log_file} | Timeout: {timeout_stagnant}s | Loop Limit: {max_loops}")

    while True:
        elapsed = time.time() - start_ts
        if max_duration and elapsed > max_duration:
            reason = f"Max test duration exceeded ({elapsed:.1f}s > {max_duration:.1f}s)"
            return handle_stuck(reason, pattern, log_file, auto_kill)

        pids = find_pids_by_pattern(pattern)
        if not pids:
            return {"status": "completed", "reason": "Process exited cleanly", "elapsed_s": round(elapsed, 1)}

        # 1. Check Log File Activity & Stagnation
        if log_file and log_file.exists():
            try:
                cur_size = log_file.stat().st_size
                if cur_size != last_log_size:
                    last_log_size = cur_size
                    last_log_change_ts = time.time()

                    # Read last 15 lines for loop detection
                    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                        lines = [l.strip() for l in f.readlines()[-30:] if l.strip()]
                    
                    # Detect identical repeating lines
                    if lines:
                        latest = lines[-1]
                        recent_lines.append(latest)
                        if len(recent_lines) > max_loops * 2:
                            recent_lines.pop(0)

                        repeats = sum(1 for l in recent_lines if l == latest)
                        if repeats >= max_loops and "!" in latest:
                            reason = f"Infinite loop detected: line repeated {repeats} times: '{latest[:100]}'"
                            return handle_stuck(reason, pattern, log_file, auto_kill)

                elif (time.time() - last_log_change_ts) > timeout_stagnant:
                    reason = f"Log stagnation: no log writes for {timeout_stagnant}s (size: {cur_size} bytes)"
                    return handle_stuck(reason, pattern, log_file, auto_kill)
            except Exception:
                pass

        # 2. Check for Wine Modal Crash Windows
        try:
            xprop = subprocess.run(["xprop", "-root", "_NET_CLIENT_LIST"], capture_output=True, text=True)
            wids = re.findall(r"0x[0-9a-f]+", xprop.stdout.lower())
            for wid in wids:
                info = subprocess.run(["xprop", "-id", wid, "WM_NAME"], capture_output=True, text=True)
                if re.search(r"Notepad|BugTrap|Fatal Error|Crash", info.stdout, re.IGNORECASE):
                    reason = f"Modal crash window detected: '{info.stdout.strip()}'"
                    return handle_stuck(reason, pattern, log_file, auto_kill)
        except Exception:
            pass

        time.sleep(3)


def handle_stuck(reason: str, pattern: str, log_file: Path, auto_kill: bool) -> dict:
    """Handles detected stuck test condition."""
    print(f"\n🚨 [GAME TEST STUCK DETECTED]")
    print(f"Reason: {reason}")

    shot_path = Path("/tmp/game_stuck_diagnostic.png")
    captured = capture_window_screenshot(shot_path)
    if captured:
        print(f"Visual Diagnostic Screenshot: {shot_path}")

    tail_lines = []
    if log_file and log_file.exists():
        try:
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                tail_lines = [l.strip() for l in f.readlines()[-20:]]
        except Exception:
            pass

    killed_list = []
    if auto_kill:
        print(f"[→] Terminating hung game processes matching '{pattern}'...")
        killed_list = sweep_game_processes([pattern, "xrEngine", "umu-run", "pressure-vessel", "notepad.exe"])
        print(f"[✓] Terminated {len(killed_list)} process(es).")

    return {
        "status": "stuck_terminated" if auto_kill else "stuck_detected",
        "reason": reason,
        "screenshot": str(shot_path) if captured else None,
        "log_tail": tail_lines,
        "terminated_pids": [k["pid"] for k in killed_list]
    }


def cmd_watch(args):
    log_p = Path(args.log_file).resolve() if args.log_file else None
    res = monitor_game_test(
        pattern=args.pattern,
        log_file=log_p,
        timeout_stagnant=args.timeout,
        max_loops=args.max_loops,
        max_duration=args.max_duration,
        auto_kill=not args.no_kill
    )
    if res["status"] in ("stuck_detected", "stuck_terminated"):
        print("\n--- Diagnostic Report ---")
        print(json.dumps(res, indent=2))
        sys.exit(2)
    else:
        print(f"[✓] {res.get('reason')} ({res.get('elapsed_s', 0)}s elapsed)")
        sys.exit(0)


def cmd_sweep(args):
    print("=======================================================")
    print(" 🧹  Game Process & Modal Window Sweep                ")
    print("=======================================================")
    killed = sweep_game_processes(args.patterns)
    if killed:
        for k in killed:
            print(f"[✓] Terminated PID {k['pid']} ({k['pattern']}): {k['cmd']}")
        print(f"Total swept: {len(killed)} process(es).")
    else:
        print("[✓] No orphaned game processes or crash dialogs found.")
    print("=======================================================\n")


def cmd_status(args):
    print("=======================================================")
    print(" 🎮  Active Game Process & Telemetry Status            ")
    print("=======================================================")
    patterns = args.patterns or ["xrEngine", "umu-run", "pressure-vessel", "notepad.exe"]
    found = 0
    for pat in patterns:
        pids = find_pids_by_pattern(pat)
        for pid in pids:
            found += 1
            cpu, mem = get_process_cpu_mem(pid)
            try:
                cmd = Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\x00", b" ").decode(errors="ignore").strip()
            except Exception:
                cmd = "unknown"
            print(f"PID {pid:6d} | CPU: {cpu:5.1f}% | Mem: {mem:4.1f}% | {pat:12s} | {cmd[:80]}")
    if found == 0:
        print("[✓] All game processes idle/clean.")
    print("=======================================================\n")


def main():
    parser = argparse.ArgumentParser(description="Autonomous Anti-Stuck Game Test Watchdog")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # watch
    p_watch = subparsers.add_parser("watch", help="Monitor a running game test and terminate if stuck")
    p_watch.add_argument("--pattern", default="xrEngine", help="Process name pattern to monitor (default: xrEngine)")
    p_watch.add_argument("--log-file", help="Path to engine log to track updates and loops")
    p_watch.add_argument("--timeout", type=float, default=60.0, help="Max seconds without log growth before declaring stagnation (default: 60)")
    p_watch.add_argument("--max-loops", type=int, default=5, help="Max repeated identical error/action lines before declaring loop (default: 5)")
    p_watch.add_argument("--max-duration", type=float, default=900.0, help="Hard maximum test run duration in seconds (default: 900)")
    p_watch.add_argument("--no-kill", action="store_true", help="Do not terminate process on stall (diagnostic only)")

    # sweep
    p_sweep = subparsers.add_parser("sweep", help="Cleanly kill orphaned game processes and Wine modals")
    p_sweep.add_argument("--patterns", nargs="*", help="Process name patterns to sweep")

    # status
    p_stat = subparsers.add_parser("status", help="Show active game processes and CPU/memory telemetry")
    p_stat.add_argument("--patterns", nargs="*", help="Process name patterns to inspect")

    args = parser.parse_args()

    if args.command == "watch":
        cmd_watch(args)
    elif args.command == "sweep":
        cmd_sweep(args)
    elif args.command == "status":
        cmd_status(args)


if __name__ == "__main__":
    main()

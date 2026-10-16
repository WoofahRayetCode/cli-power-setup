#!/usr/bin/env python3
"""
Autonomous X-Ray Engine Crash Log Interceptor & Window Dismissal Handler
========================================================================
Detects Wine/Proton Notepad and BugTrap popup windows generated when the X-Ray / OGSR
engine crashes, extracts the full diagnostic triage (fatal error, stack trace, lua callstack),
archives the crash report, and immediately terminates the lingering Notepad window so
automated playtesting, CI, and test runners do not hang.
"""

import argparse
import glob
import json
import os
import re
import signal
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SEARCH_LOG_DIRS = [
    Path("/home/ericparsley/Documents/GitHub/ogsr-complete-merge/_appdata_/logs"),
    Path("/home/ericparsley/Desktop/STALKER_Complete/_appdata_/logs"),
    Path("_appdata_/logs").resolve(),
    Path.home() / ".local/share/Steam/steamapps/compatdata"
]


def resolve_wine_path(raw_path: str) -> Optional[Path]:
    """Convert Wine Windows path (e.g. Z:\\home\\... or C:\\...) to Linux Path."""
    p_str = raw_path.strip().strip('"').strip("'")
    if not p_str:
        return None

    # Handle Z:\ drive mapping (root filesystem in Wine)
    if re.match(r'^[zZ]:[\\/]', p_str):
        linux_sub = re.sub(r'^[zZ]:[\\/]', '/', p_str).replace('\\', '/')
        cand = Path(linux_sub)
        if cand.exists():
            return cand

    # Handle standard Linux path directly passed
    cand = Path(p_str.replace('\\', '/'))
    if cand.exists():
        return cand

    # If basename only or relative, search in standard log directories
    base = cand.name
    for d in SEARCH_LOG_DIRS:
        if d.exists():
            for found in d.glob(f"**/{base}"):
                if found.is_file():
                    return found

    return None


def find_latest_xray_log(max_age_seconds: float = 300.0) -> Optional[Path]:
    """Find the most recently modified xray_*.log in known directories."""
    candidates = []
    now = time.time()
    for d in SEARCH_LOG_DIRS:
        if not d.exists():
            continue
        try:
            for log_file in d.glob("**/xray_*.log"):
                if log_file.is_file():
                    mtime = log_file.stat().st_mtime
                    if now - mtime <= max_age_seconds:
                        candidates.append((mtime, log_file))
        except Exception:
            continue

    if candidates:
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]
    return None


def parse_xray_log(log_path: Path) -> Dict[str, any]:
    """Extract structured triage data from an X-Ray / OGSR crash log."""
    report = {
        "log_path": str(log_path),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(log_path.stat().st_mtime)),
        "filesize_bytes": log_path.stat().st_size,
        "fatal_error": None,
        "expression": None,
        "function": None,
        "file": None,
        "line": None,
        "description": None,
        "stack_trace": [],
        "lua_errors": [],
        "critical_warnings": [],
        "memory_summary": {},
        "tail_lines": []
    }

    try:
        content = log_path.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()
        report["tail_lines"] = lines[-35:] if len(lines) >= 35 else lines

        in_fatal = False
        in_stack = False

        for l in lines:
            line_clean = l.strip()

            if "FATAL ERROR" in line_clean:
                in_fatal = True
                report["fatal_error"] = True

            if in_fatal:
                if "Expression" in line_clean and not report["expression"]:
                    report["expression"] = line_clean.split("Expression", 1)[-1].lstrip(" :").strip()
                elif "Function" in line_clean and not report["function"]:
                    report["function"] = line_clean.split("Function", 1)[-1].lstrip(" :").strip()
                elif "File" in line_clean and not report["file"]:
                    report["file"] = line_clean.split("File", 1)[-1].lstrip(" :").strip()
                elif "Line" in line_clean and not report["line"]:
                    report["line"] = line_clean.split("Line", 1)[-1].lstrip(" :").strip()
                elif "Description" in line_clean and not report["description"]:
                    report["description"] = line_clean.split("Description", 1)[-1].lstrip(" :").strip()

            if "stack trace:" in line_clean.lower():
                in_stack = True
                continue

            if in_stack:
                if line_clean.startswith("0x") or line_clean.startswith("[") or "xr" in line_clean:
                    report["stack_trace"].append(line_clean)
                elif not line_clean:
                    in_stack = False

            if "! [LUA" in line_clean or "SCRIPT ERROR:" in line_clean or "attempt to index" in line_clean:
                report["lua_errors"].append(line_clean)

            if line_clean.startswith("! ") and len(report["critical_warnings"]) < 10:
                report["critical_warnings"].append(line_clean)

            if "Engine memory usage (Working Set):" in line_clean:
                report["memory_summary"]["working_set"] = line_clean.split(":")[-1].strip()
            if "physical memory installed" in line_clean:
                report["memory_summary"]["physical"] = line_clean

    except Exception as e:
        report["read_error"] = str(e)

    return report


def scan_active_popups() -> List[Dict[str, any]]:
    """Scan running processes for Wine/Proton Notepad or crash dialog instances."""
    popups = []
    pids = [int(p) for p in os.listdir("/proc") if p.isdigit()]

    for pid in pids:
        cmdline_file = Path(f"/proc/{pid}/cmdline")
        if not cmdline_file.exists():
            continue
        try:
            raw_cmd = cmdline_file.read_bytes().split(b"\x00")
            cmd_args = [arg.decode("utf-8", errors="ignore") for arg in raw_cmd if arg]
            cmd_str = " ".join(cmd_args).lower()

            # Identify Wine Notepad opening a crash log or BugTrap
            is_notepad = "notepad" in cmd_str
            is_bugtrap = any(k in cmd_str for k in ["bugtrap", "werfault", "winedbg"])
            is_log_target = any(".log" in arg.lower() for arg in cmd_args) or any("xray" in arg.lower() for arg in cmd_args)

            if is_notepad or (is_bugtrap and is_log_target):
                log_file_path = None
                for arg in cmd_args:
                    if ".log" in arg.lower():
                        resolved = resolve_wine_path(arg)
                        if resolved:
                            log_file_path = resolved
                            break

                if not log_file_path:
                    # Fallback to the newest xray log created recently
                    log_file_path = find_latest_xray_log(max_age_seconds=180.0)

                popups.append({
                    "pid": pid,
                    "cmd": cmd_args,
                    "is_notepad": is_notepad,
                    "is_bugtrap": is_bugtrap,
                    "log_path": log_file_path
                })
        except Exception:
            continue

    return popups


def dismiss_process(pid: int, timeout: float = 1.0) -> bool:
    """Terminate the process gently via SIGTERM, escalating to SIGKILL."""
    try:
        os.kill(pid, signal.SIGTERM)
        start = time.time()
        while time.time() - start < timeout:
            if not Path(f"/proc/{pid}").exists():
                return True
            time.sleep(0.05)
        # Force kill if still holding up
        os.kill(pid, signal.SIGKILL)
        return True
    except ProcessLookupError:
        return True
    except Exception as e:
        print(f"[Warning] Failed to kill PID {pid}: {e}", file=sys.stderr)
        return False


def sweep_and_dismiss(archive_dir: Optional[Path] = None) -> List[Dict[str, any]]:
    """Scan, read all active crash logs, close the notepad windows, and return reports."""
    popups = scan_active_popups()
    triaged = []

    for pop in popups:
        pid = pop["pid"]
        log_path = pop["log_path"]
        print(f"\n[💥 Intercepted Crash Window] PID: {pid} | Command: {' '.join(pop['cmd'])}")

        report = None
        if log_path and log_path.exists():
            print(f"  -> Reading crash log: {log_path}")
            report = parse_xray_log(log_path)
            
            # Print high-density triage summary
            if report.get("expression") or report.get("description"):
                print(f"  -> Fatal Expression: {report.get('expression')}")
                print(f"  -> Description:      {report.get('description')}")
                print(f"  -> Location:         {report.get('file')}:{report.get('line')}")
                print(f"  -> Function:         {report.get('function')}")
            elif report.get("lua_errors"):
                print(f"  -> Lua Error:        {report['lua_errors'][0]}")
            else:
                print(f"  -> Read {len(report['tail_lines'])} trailing log lines.")

            # Save triage report to archive
            out_dir = archive_dir or (log_path.parent if log_path else Path("/tmp/xray_triage"))
            out_dir.mkdir(parents=True, exist_ok=True)
            report_file = out_dir / f"crash_triage_{int(time.time())}_{pid}.json"
            report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
            print(f"  -> Saved structured triage ledger: {report_file}")
        else:
            print("  -> Notice: Specific log file could not be mapped; closing modal window.")

        # Dismiss the window so it doesn't hold up tests
        success = dismiss_process(pid)
        print(f"  -> Dismissed and closed popup window (PID: {pid}): {'Success' if success else 'Failed'}")
        
        triaged.append({
            "pid": pid,
            "log": str(log_path) if log_path else None,
            "dismissed": success,
            "report": report
        })

    return triaged


def monitor_daemon(interval: float = 0.5, max_duration: Optional[float] = None, archive_dir: Optional[Path] = None):
    """Continuous background loop monitoring for crash popups."""
    print(f"🛡️  [X-Ray Crash Watchdog Active] Polling every {interval}s for Wine notepad/crash dialogs...")
    start_time = time.time()
    count = 0

    try:
        while True:
            triaged = sweep_and_dismiss(archive_dir=archive_dir)
            if triaged:
                count += len(triaged)
                print(f"[✓] Intercepted and cleared {len(triaged)} crash popup(s). Total cleared: {count}")

            if max_duration and (time.time() - start_time >= max_duration):
                print(f"[Watchdog] Reached duration limit ({max_duration}s). Stopping.")
                break

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[Watchdog] Interrupted by user. Exiting cleanly.")


def main():
    parser = argparse.ArgumentParser(description="Autonomous X-Ray Engine Crash Log Interceptor & Window Dismissal Handler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # sweep
    sweep_p = subparsers.add_parser("sweep", help="Scan for active crash popups, read logs, archive triage, and close windows")
    sweep_p.add_argument("--archive-dir", type=str, default=None, help="Directory to save structured triage reports")

    # triage
    triage_p = subparsers.add_parser("triage", help="Parse and summarize an existing X-Ray crash log file")
    triage_p.add_argument("log_file", type=str, help="Path to xray_*.log file")

    # monitor
    mon_p = subparsers.add_parser("monitor", help="Run continuous background watchdog daemon")
    mon_p.add_argument("--interval", type=float, default=0.5, help="Polling interval in seconds (default: 0.5)")
    mon_p.add_argument("--duration", type=float, default=None, help="Maximum run duration in seconds")
    mon_p.add_argument("--archive-dir", type=str, default=None, help="Directory to save structured triage reports")

    args = parser.parse_args()

    if args.command == "sweep":
        archive = Path(args.archive_dir) if args.archive_dir else None
        results = sweep_and_dismiss(archive_dir=archive)
        if not results:
            print("[✓] Sweep clean: No active X-Ray crash popups or lingering notepad windows.")

    elif args.command == "triage":
        path = Path(args.log_file)
        if not path.exists():
            print(f"Error: File not found: {path}", file=sys.stderr)
            sys.exit(1)
        rep = parse_xray_log(path)
        print("=======================================================================")
        print(f" ☢️  X-Ray Crash Log Triage: {path.name}")
        print("=======================================================================")
        print(f"Timestamp:   {rep['timestamp']} | Size: {rep['filesize_bytes']} bytes")
        if rep["expression"]:
            print(f"Expression:  {rep['expression']}")
            print(f"Description: {rep.get('description')}")
            print(f"Location:    {rep.get('file')}:{rep.get('line')}")
            print(f"Function:    {rep.get('function')}")
        if rep["lua_errors"]:
            print(f"Lua Errors:  {len(rep['lua_errors'])} detected")
            for err in rep["lua_errors"][:3]:
                print(f"  • {err}")
        if rep["stack_trace"]:
            print("Stack Trace:")
            for s in rep["stack_trace"][:8]:
                print(f"  -> {s}")
        if rep["memory_summary"]:
            print(f"Memory:      {rep['memory_summary']}")
        print("-----------------------------------------------------------------------")

    elif args.command == "monitor":
        archive = Path(args.archive_dir) if args.archive_dir else None
        monitor_daemon(interval=args.interval, max_duration=args.duration, archive_dir=archive)


if __name__ == "__main__":
    main()

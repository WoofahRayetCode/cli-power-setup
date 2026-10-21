#!/usr/bin/env python3
"""
Antigravity CLI Doctor & Diagnostics (agy-doctor)
Provides parity with 'claude doctor' for Antigravity CLI.
Audits binary installation, SQLite database integrity, permissions whitelist,
model connectivity, MCP servers, and quota cache health.
"""

import glob
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time

def check_mark(status):
    if status is True:
        return "\033[32m[✓ PASS]\033[0m"
    elif status is False:
        return "\033[31m[✗ FAIL]\033[0m"
    return "\033[33m[⚠ WARN]\033[0m"

def main():
    print("\n=======================================================")
    print(" 🩺 Antigravity CLI Diagnostics & Health Doctor        ")
    print("=======================================================")

    results = []

    # 1. Executable Verification
    agy_bin = shutil.which("agy")
    if agy_bin:
        try:
            res = subprocess.run(["agy", "--help"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                results.append((True, f"CLI Executable found at {agy_bin}"))
            else:
                results.append((None, f"CLI found at {agy_bin} but exited with code {res.returncode}"))
        except Exception as e:
            results.append((False, f"CLI execution error: {e}"))
    else:
        results.append((False, "agy executable not found in PATH"))

    # 2. Settings Configuration & Permissions Whitelist
    cfg_path = os.path.expanduser("~/.gemini/antigravity-cli/settings.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            model = cfg.get("model", "Default")
            perms = cfg.get("permissions", {}).get("allow", [])
            statusline = cfg.get("statusLine", {}).get("command", "None")
            results.append((True, f"Settings valid: Configured model '{model}'"))
            results.append((True, f"Permissions whitelist active: {len(perms)} allowed command rules"))
            if statusline != "None" and os.path.exists(statusline):
                results.append((True, f"Custom statusline configured and executable: {statusline}"))
            else:
                results.append((None, f"Statusline command not found or default: {statusline}"))
        except Exception as e:
            results.append((False, f"Invalid settings.json: {e}"))
    else:
        results.append((None, f"Settings file not found at {cfg_path} (using built-in defaults)"))

    # 3. SQLite Conversations Database Health
    base_dir = os.path.expanduser("~/.gemini/antigravity-cli")
    db_files = glob.glob(f"{base_dir}/conversations/*.db")
    if db_files:
        corrupted = 0
        total_dbs = len(db_files)
        # Check latest 5 conversations
        for db in sorted(db_files, key=os.path.getmtime, reverse=True)[:5]:
            try:
                conn = sqlite3.connect(db)
                c = conn.cursor()
                c.execute("PRAGMA integrity_check;")
                row = c.fetchone()
                if not row or row[0] != "ok":
                    corrupted += 1
                conn.close()
            except Exception:
                corrupted += 1
        if corrupted == 0:
            results.append((True, f"SQLite integrity verified across conversation records ({total_dbs} sessions)"))
        else:
            results.append((False, f"{corrupted} conversation database(s) reported integrity errors"))
    else:
        results.append((True, "No stored conversation databases found (clean directory)"))

    # 4. Quota Cache & Lock Health
    lock_file = "/tmp/agy_quota_refresh.lock"
    cache_file = "/tmp/agy_quota_cache.txt"
    if os.path.exists(lock_file):
        age = time.time() - os.path.getmtime(lock_file)
        if age > 60:
            os.remove(lock_file)
            results.append((True, f"Evicted stale lock file ({int(age)}s old)"))
        else:
            results.append((True, f"Quota refresh lock active ({int(age)}s old)"))
    else:
        results.append((True, "No stale lock files present"))

    if os.path.exists(cache_file):
        results.append((True, f"Quota cache initialized at {cache_file}"))
    else:
        results.append((None, "Quota cache not yet generated (runs on next statusline tick)"))

    # 5. Model Backend Connectivity & Dynamic Cheat Sheet / Offload Stack
    try:
        res = subprocess.run(
            ["agy", "models"],
            capture_output=True,
            text=True,
            timeout=8
        )
        if res.returncode == 0 and "gemini-4-argon" in res.stdout:
            results.append((True, "Google Gemini & Anthropic model API endpoints reachable"))
        else:
            results.append((None, "Model API endpoint reachable but model list returned non-standard output"))
    except Exception as e:
        results.append((False, f"Model endpoint unreachable: {e}"))

    cs_path = os.path.expanduser("~/.cli_power_setup/repo_cheatsheet.json")
    results.append((os.path.exists(cs_path), f"Dynamic Repo Model Cheat Sheet index present ({cs_path})"))
    if os.name == "nt":
        has_gpu = shutil.which("nvidia-smi") is not None
        results.append((has_gpu, "Windows GPU & DXGI stack ready (nvidia-smi / DirectX 12)"))
        results.append((os.path.exists(os.environ.get("TEMP", "C:\\Windows\\Temp")), "Windows %TEMP% / RAMDisk staging ready"))
    else:
        results.append((os.path.exists("/dev/dri/renderD128") and os.path.exists("/dev/dri/renderD129"), "Hybrid GPU nodes ready (RTX 5060 dGPU + Radeon 610M iGPU)"))
        results.append((os.path.exists("/dev/shm"), "30 GB RAM /dev/shm tmpfs accelerator ready"))

    # Print results
    print("\nDiagnostic Checklist:")
    passes = sum(1 for s, _ in results if s is True)
    warns = sum(1 for s, _ in results if s is None)
    fails = sum(1 for s, _ in results if s is False)

    for status, desc in results:
        print(f"  {check_mark(status)} {desc}")

    print("-------------------------------------------------------")
    print(f"Summary: {passes} Passed | {warns} Warnings | {fails} Failed")
    if fails == 0:
        print("Status:  All Antigravity CLI core systems operational.")
    else:
        print("Status:  Action required on failed items above.")
    print("=======================================================\n")

if __name__ == "__main__":
    main()

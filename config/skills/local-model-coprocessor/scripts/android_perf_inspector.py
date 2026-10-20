#!/usr/bin/env python3
import sys
import subprocess
import argparse
import shutil
import re

def check_adb():
    if not shutil.which("adb"):
        print("[!] Error: 'adb' is not installed or not in PATH.")
        sys.exit(1)

def run_adb(cmd):
    full_cmd = ["adb"] + cmd
    res = subprocess.run(full_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return ""
    return res.stdout

def analyze_jank(package):
    print(f"[→] Querying gfxinfo framestats for '{package}'...")
    output = run_adb(["shell", "dumpsys", "gfxinfo", package])
    if not output:
        print(f"[!] Could not query gfxinfo for {package}. Is the app running?")
        return

    # Extract Total frames rendered and Janky frames
    total_match = re.search(r'Total frames rendered:\s+(\d+)', output)
    jank_match = re.search(r'Janky frames:\s+(\d+)\s+\((.*?)\)', output)
    p50_match = re.search(r'50th percentile:\s+(\d+)ms', output)
    p90_match = re.search(r'90th percentile:\s+(\d+)ms', output)
    p99_match = re.search(r'99th percentile:\s+(\d+)ms', output)

    print(f"\n--- Graphics Rendering Performance ({package}) ---")
    if total_match:
        print(f"Total Frames:    {total_match.group(1)}")
    if jank_match:
        print(f"Janky Frames:    {jank_match.group(1)} ({jank_match.group(2)})")
    if p50_match:
        print(f"Median (p50):    {p50_match.group(1)} ms")
    if p90_match:
        print(f"90th Percentile: {p90_match.group(1)} ms")
    if p99_match:
        print(f"99th Percentile: {p99_match.group(1)} ms")
    print("--------------------------------------------------\n")

def analyze_battery(package):
    print(f"[→] Querying batterystats for '{package}'...")
    output = run_adb(["shell", "dumpsys", "batterystats", package])
    if not output:
        print(f"[!] Could not query batterystats for {package}.")
        return

    lines = [l for l in output.splitlines() if any(k in l for k in ["Wake lock", "Job", "Sync", "Total cpu time", "Foreground"])]
    print(f"\n--- Battery & Resource Stats ({package}) ---")
    for l in lines[:20]:
        print(f"  {l.strip()}")
    print("--------------------------------------------\n")

def main():
    check_adb()
    parser = argparse.ArgumentParser(description="Android Performance & Jank Inspector")
    parser.add_argument("--package", required=True, help="Android package name (e.g. com.example.app)")
    parser.add_argument("--jank", action="store_true", help="Analyze jank and frame rendering latency")
    parser.add_argument("--battery", action="store_true", help="Analyze battery and wake lock usage")

    args = parser.parse_args()

    if args.jank or not (args.battery):
        analyze_jank(args.package)
    if args.battery:
        analyze_battery(args.package)

if __name__ == "__main__":
    main()

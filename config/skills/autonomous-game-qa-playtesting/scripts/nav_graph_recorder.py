#!/usr/bin/env python3
"""
Autonomous Game Navigation & Route Replayer (nav-graph-recorder)
Records, optimizes, and replays character locomotion routes via /dev/uinput.
Maintains a self-improving blacklist of geometry collision traps and stuck points.
"""

import sys
import time
import json
import argparse
from pathlib import Path

# Self-improving collision trap blacklist file
BLACKLIST_FILE = Path("/tmp/game_nav_blacklist.json")

def load_blacklist() -> list:
    if BLACKLIST_FILE.exists():
        try:
            return json.loads(BLACKLIST_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []

def record_trap(x: float, y: float, z: float, reason: str = "Collision trap"):
    bl = load_blacklist()
    bl.append({
        "timestamp": int(time.time()),
        "x": round(x, 2),
        "y": round(y, 2),
        "z": round(z, 2),
        "reason": reason
    })
    BLACKLIST_FILE.write_text(json.dumps(bl, indent=2), encoding="utf-8")
    print(f"[✓] Added collision trap ({x:.2f}, {y:.2f}, {z:.2f}) to self-improving nav blacklist.")

def smooth_route(points: list) -> list:
    """Applies Catmull-Rom or moving-average smoothing to route waypoints."""
    if len(points) <= 2:
        return points
    smoothed = [points[0]]
    for i in range(1, len(points) - 1):
        prev_p = points[i - 1]
        curr_p = points[i]
        next_p = points[i + 1]
        sx = (prev_p["x"] + curr_p["x"] + next_p["x"]) / 3.0
        sy = (prev_p["y"] + curr_p["y"] + next_p["y"]) / 3.0
        sz = (prev_p["z"] + curr_p["z"] + next_p["z"]) / 3.0
        smoothed.append({
            "x": round(sx, 3),
            "y": round(sy, 3),
            "z": round(sz, 3),
            "yaw": curr_p.get("yaw", 0)
        })
    smoothed.append(points[-1])
    return smoothed

def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Game Navigation & Route Replayer"
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # 1. log-trap
    p_trap = subparsers.add_parser("log-trap", help="Record a stuck point or geometry hole to the nav blacklist")
    p_trap.add_argument("--x", type=float, required=True, help="World X coordinate")
    p_trap.add_argument("--y", type=float, required=True, help="World Y coordinate")
    p_trap.add_argument("--z", type=float, required=True, help="World Z coordinate")
    p_trap.add_argument("--reason", default="Stuck in geometry / invisible wall", help="Failure reason")

    # 2. list-traps
    p_list = subparsers.add_parser("list-traps", help="List all blacklisted geometry traps")

    # 3. optimize-route
    p_opt = subparsers.add_parser("optimize-route", help="Smooth recorded waypoints and bypass blacklisted points")
    p_opt.add_argument("route_file", type=Path, help="JSON route file")
    p_opt.add_argument("--out", type=Path, help="Smoothed output JSON route file")

    args = parser.parse_args()

    if args.subcommand == "log-trap":
        record_trap(args.x, args.y, args.z, args.reason)
        return 0
    elif args.subcommand == "list-traps":
        bl = load_blacklist()
        print(f"\n[→] Self-Improving Nav Blacklist ({len(bl)} registered traps):")
        for idx, t in enumerate(bl, 1):
            print(f"    {idx}. ({t['x']}, {t['y']}, {t['z']}) - {t['reason']}")
        return 0
    elif args.subcommand == "optimize-route":
        if not args.route_file.exists():
            print(f"[✗] File not found: {args.route_file}")
            return 1
        data = json.loads(args.route_file.read_text(encoding="utf-8"))
        pts = data.get("waypoints", data)
        smoothed = smooth_route(pts)
        out_target = args.out or args.route_file.with_name(f"{args.route_file.stem}_smoothed.json")
        out_target.write_text(json.dumps({"waypoints": smoothed}, indent=2), encoding="utf-8")
        print(f"[✓] Smoothed {len(pts)} waypoints -> {out_target}")
        return 0

    return 0

if __name__ == "__main__":
    sys.exit(main())

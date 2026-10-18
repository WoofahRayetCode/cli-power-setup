#!/usr/bin/env python3
"""
OpenAI Operator & Anthropic Computer-Use Desktop Driver
Controls GUI mouse, keyboard, and window focus across Wayland and X11 using ydotool and evdev.
"""

import argparse
import os
import subprocess
import sys
import time

def run_ydotool(*args):
    cmd = ["ydotool"] + list(args)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        # Fallback to direct evdev / uinput if needed
        return False, res.stderr.strip()
    return True, res.stdout.strip()

def cmd_click(args):
    x, y = args.x, args.y
    # Move mouse
    run_ydotool("mousemove", "-a", str(x), str(y))
    time.sleep(0.05)
    btn = "0x110" if args.button == "left" else "0x111" if args.button == "right" else "0x112"
    if args.double:
        run_ydotool("click", btn)
        time.sleep(0.05)
        ok, out = run_ydotool("click", btn)
    else:
        ok, out = run_ydotool("click", btn)
    if ok:
        print(f"[✓] Operator: Clicked {args.button} button at ({x}, {y}){' (double)' if args.double else ''}")
    else:
        print(f"[✗] Operator: Click failed: {out}", file=sys.stderr)
        sys.exit(1)

def cmd_move(args):
    x, y = args.x, args.y
    ok, out = run_ydotool("mousemove", "-a", str(x), str(y))
    if ok:
        print(f"[✓] Operator: Moved cursor to ({x}, {y})")
    else:
        print(f"[✗] Operator: Move failed: {out}", file=sys.stderr)
        sys.exit(1)

def cmd_type(args):
    text = args.text
    ok, out = run_ydotool("type", "--", text)
    if ok:
        print(f"[✓] Operator: Typed {len(text)} characters")
    else:
        print(f"[✗] Operator: Type failed: {out}", file=sys.stderr)
        sys.exit(1)

def cmd_key(args):
    combo = args.combo
    ok, out = run_ydotool("key", combo)
    if ok:
        print(f"[✓] Operator: Sent key combo: {combo}")
    else:
        print(f"[✗] Operator: Key failed: {out}", file=sys.stderr)
        sys.exit(1)

def cmd_bounds(args):
    # Query resolution via wl-paste/wlr-randr/xrandr
    res = subprocess.run(["xrandr", "--current"], capture_output=True, text=True)
    if res.returncode == 0:
        for line in res.stdout.splitlines():
            if " connected" in line and "primary" in line or (" connected" in line and "x" in line):
                parts = line.split()
                for p in parts:
                    if "x" in p and "+" in p:
                        print(f"Screen bounds: {p}")
                        return
    print("Screen bounds: 1920x1080 (default)")

def main():
    parser = argparse.ArgumentParser(description="OpenAI Operator & Computer Use Desktop Driver")
    sub = parser.add_subparsers(dest="action", required=True)

    click_p = sub.add_parser("click", help="Click at coordinate")
    click_p.add_argument("x", type=int, help="X pixel")
    click_p.add_argument("y", type=int, help="Y pixel")
    click_p.add_argument("--button", choices=["left", "right", "middle"], default="left")
    click_p.add_argument("--double", action="store_true", help="Double click")
    click_p.set_defaults(func=cmd_click)

    move_p = sub.add_parser("move", help="Move cursor to coordinate")
    move_p.add_argument("x", type=int, help="X pixel")
    move_p.add_argument("y", type=int, help="Y pixel")
    move_p.set_defaults(func=cmd_move)

    type_p = sub.add_parser("type", help="Type string")
    type_p.add_argument("text", help="Text to type")
    type_p.set_defaults(func=cmd_type)

    key_p = sub.add_parser("key", help="Press key combo")
    key_p.add_argument("combo", help="Key combo (e.g. 29:1 42:1 28:1 28:0 42:0 29:0 or key name)")
    key_p.set_defaults(func=cmd_key)

    bounds_p = sub.add_parser("bounds", help="Query screen bounds")
    bounds_p.set_defaults(func=cmd_bounds)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

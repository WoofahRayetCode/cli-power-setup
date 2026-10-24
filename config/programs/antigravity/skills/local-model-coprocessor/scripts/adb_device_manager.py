#!/usr/bin/env python3
"""
Android Device Automation & Maintenance Manager (android-device-automation)
"""
import subprocess, sys, argparse, os

def run_adb(args):
    return subprocess.run(["adb"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def get_devices():
    res = run_adb(["devices"])
    lines = [l.split("\t")[0] for l in res.stdout.strip().split("\n")[1:] if "\tdevice" in l]
    return lines

def capture_screen(output="/tmp/android_screen.png"):
    with open(output, "wb") as f:
        subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f)
    print(f"[✓] Android screenshot captured: {output}")

def tap(x, y):
    run_adb(["shell", "input", "tap", str(x), str(y)])
    print(f"[✓] Tapped coordinate: ({x}, {y})")

def swipe(x1, y1, x2, y2, duration=300):
    run_adb(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)])
    print(f"[✓] Swiped from ({x1},{y1}) to ({x2},{y2})")

def clean_caches():
    print("[→] Trimming package caches...")
    run_adb(["shell", "pm", "trim-caches", "1000M"])
    print("[✓] Caches trimmed successfully.")

def main():
    parser = argparse.ArgumentParser(description="Android ADB Automation Tool")
    parser.add_argument("--devices", action="store_true", help="List connected devices")
    parser.add_argument("--screencap", "-s", metavar="PATH", nargs="?", const="/tmp/android_screen.png", help="Capture screen")
    parser.add_argument("--tap", nargs=2, type=int, metavar=("X", "Y"), help="Tap coordinates")
    parser.add_argument("--swipe", nargs=4, type=int, metavar=("X1", "Y1", "X2", "Y2"), help="Swipe coordinates")
    parser.add_argument("--clean", action="store_true", help="Clean system caches")
    args = parser.parse_args()

    if args.devices:
        devs = get_devices()
        print("Connected Android Devices:", devs if devs else "None")
    elif args.screencap:
        capture_screen(args.screencap)
    elif args.tap:
        tap(args.tap[0], args.tap[1])
    elif args.swipe:
        swipe(args.swipe[0], args.swipe[1], args.swipe[2], args.swipe[3])
    elif args.clean:
        clean_caches()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

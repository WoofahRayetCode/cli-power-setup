#!/usr/bin/env python3
"""Screen dimmer: instead of switching the panel OFF when nothing is happening, turn the backlight down to almost nothing (1.5 %) and bring it back at the first touch of the laptop's keyboard/touchpad.
The panel stays ON, so screenshots (spectacle) work without waking anything, windows are not re-stacked by a DPMS wake, and the picture is still there, just dark.
  dimmer.py run            loop (guardian keeps it alive); dims after DIM_AFTER s without keyboard/touchpad activity, restores on activity
  dimmer.py mode dim|off   dim (default): KDE's own screen-off is disabled on AC and this loop dims | off: back to KDE's screen-off after 60 s, the loop idles
  dimmer.py now|restore    dim / restore immediately
Brightness goes through KDE PowerDevil's D-Bus (units 0..10000). The pre-dim level is saved in /tmp/dimmer.saved and restored on exit."""
import os, signal, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dpms import activity
here = Path(__file__).resolve().parent.parent; MODE = here / ".agents/screen_mode"; SAVED = Path("/tmp/dimmer.saved")
import json
SB, SBP = "org.kde.ScreenBrightness", "/org/kde/ScreenBrightness"
DIM_AFTER, DIM_LEVEL = 60, 4500                     # 45 %: the lowest brightness any screen gets (dimmed or not) until the user says otherwise
AWAKE = here / ".agents/awake_brightness.json"      # per screen: the brightness you like while you are at the computer: coming back from a dim ALWAYS returns to it, and it follows any change you make yourself
def q(*a):
    try: return subprocess.run(["qdbus6", *a], capture_output=True, text=True, timeout=6).stdout.strip()
    except Exception: return ""
def displays():
    out = q(SB, SBP, "org.freedesktop.DBus.Properties.Get", "org.kde.ScreenBrightness", "DisplaysDBusNames")
    return [l.strip() for l in out.splitlines() if l.strip().startswith("display")]
def level(d):
    v = q(SB, f"{SBP}/{d}", "org.freedesktop.DBus.Properties.Get", "org.kde.ScreenBrightness.Display", "Brightness"); return int(v) if v.lstrip("-").isdigit() else None
def setl(d, v): q(SB, f"{SBP}/{d}", "org.kde.ScreenBrightness.Display.SetBrightness", str(int(v)), "0")
def awake():
    try: return json.loads(AWAKE.read_text())
    except Exception: return {}
def save_awake(a): AWAKE.write_text(json.dumps(a))
def dim():
    a = awake(); saved = {}
    for d in displays():
        cur = level(d)
        if cur is None: continue
        a.setdefault(d, max(cur, DIM_LEVEL)); saved[d] = a[d]
        if cur > DIM_LEVEL + 50: setl(d, DIM_LEVEL)
    save_awake(a)
    if saved: SAVED.write_text(json.dumps(saved))
def restore():
    if not SAVED.exists(): return
    a = awake()
    try: saved = json.loads(SAVED.read_text())
    except Exception: saved = {}
    for d in displays(): setl(d, max(a.get(d) or saved.get(d) or 7800, DIM_LEVEL))
    SAVED.unlink(missing_ok=True)
def follow_user():
    """while awake (not dimmed): a brightness you set yourself becomes the new 'awake' level; nothing ever stays below the 25 % minimum"""
    a = awake(); changed = False
    for d in displays():
        cur = level(d)
        if cur is None: continue
        if cur < DIM_LEVEL - 50 and not SAVED.exists(): setl(d, DIM_LEVEL); cur = DIM_LEVEL                # enforce the minimum
        if not SAVED.exists() and cur > DIM_LEVEL + 50 and a.get(d) != cur: a[d] = cur; changed = True
    if changed: save_awake(a)
def kde_off(seconds):
    subprocess.run(["kwriteconfig6", "--file", "powerdevilrc", "--group", "AC", "--group", "Display", "--key", "TurnOffDisplayIdleTimeoutSec", str(seconds)], capture_output=True)
    subprocess.run(["qdbus6", "org.kde.Solid.PowerManagement", "/org/kde/Solid/PowerManagement", "org.kde.Solid.PowerManagement.reparseConfiguration"], capture_output=True)
def mode(): 
    try: return MODE.read_text().strip() or "dim"
    except Exception: return "dim"
def run():
    signal.signal(signal.SIGTERM, lambda *a: (restore(), sys.exit(0)))
    last, idle, applied = activity(), 0, None
    while True:
        m = mode()
        if m != applied:
            applied = m; restore() if m == "off" else None; kde_off(60 if m == "off" else 86400)      # dim mode: KDE must not switch the panel off by itself
        a = activity()
        follow_user()
        if a != last: last, idle = a, 0; restore()
        else: idle += 3
        if m == "dim" and idle >= DIM_AFTER and not SAVED.exists(): dim()
        time.sleep(3)
if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "run"
    if c == "run": run()
    elif c == "mode" and len(sys.argv) > 2 and sys.argv[2] in ("dim", "off"): MODE.write_text(sys.argv[2]); print("screen mode:", sys.argv[2], "(applied within 3 s by the running loop)")
    elif c == "now": dim()
    elif c == "restore": restore()
    else: sys.exit(__doc__)

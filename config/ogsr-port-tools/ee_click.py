#!/usr/bin/env python3
"""Click at absolute screen pixels with a virtual absolute pointer (/dev/uinput through python-evdev), which Wayland/KWin treats as a real mouse:
  ee_click.py X Y [double]     (run with ~/.cache/eevenv/bin/python; needs write access to /dev/uinput, which this user has through an ACL)
Screen size 1920x1200. Used to drive the Steam EE menus (tools/ee_session.sh click)."""
import sys, time
from evdev import UInput, AbsInfo, ecodes as e
W, H = 1920, 1200
# Safety (user rule 2026-10-18: never interact with Steam messages/popups): clicks are only allowed inside the game's drawing area, and never in the bottom-right corner
# where the Steam overlay shows its toast ("Access Steam features from the overlay"). The game window is at 0,0 with a 28 px title bar and a 1280x720 client area.
GAME = (8, 36, 1272, 744); TOAST = (980, 670, 1280, 748)
x, y = int(sys.argv[1]), int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else "click"; n = 2 if mode == "double" else 1
if not (GAME[0] <= x <= GAME[2] and GAME[1] <= y <= GAME[3]) or (TOAST[0] <= x <= TOAST[2] and TOAST[1] <= y <= TOAST[3]):
    sys.exit(f"ee_click: refusing to click at {x},{y} (outside the game area or on the Steam toast corner)")
cap = {e.EV_KEY: [e.BTN_LEFT], e.EV_ABS: [(e.ABS_X, AbsInfo(0, 0, W - 1, 0, 0, 0)), (e.ABS_Y, AbsInfo(0, 0, H - 1, 0, 0, 0))]}
with UInput(cap, name="zone-virtual-pointer") as ui:
    time.sleep(1.0)                                   # let the compositor notice the new device
    for px, py in ((x - 3, y - 3), (x, y)):           # approach in two steps so the game sees a hover first
        ui.write(e.EV_ABS, e.ABS_X, px); ui.write(e.EV_ABS, e.ABS_Y, py); ui.syn(); time.sleep(0.2)
    for _ in range(0 if mode == "move" else n):
        ui.write(e.EV_KEY, e.BTN_LEFT, 1); ui.syn(); time.sleep(0.08); ui.write(e.EV_KEY, e.BTN_LEFT, 0); ui.syn(); time.sleep(0.15)
    time.sleep(0.3 if mode != "move" else 2.5)           # 'move': keep the device alive a moment so the pointer stays where it is for a screenshot

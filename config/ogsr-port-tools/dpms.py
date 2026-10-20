#!/usr/bin/env python3
"""Display power helper for unattended runs (KDE Wayland). The screen is allowed to be OFF whenever nothing needs it (no burn-in); screenshot code wakes it only for the capture.
  from dpms import wake_for_capture   ->  call before a screenshot: wakes the panel if it is off, returns a function `done()` that puts it back to sleep ~3 s later (only if WE woke it)
  dpms.py state|on|off
State is read from /sys/class/drm/*eDP*/dpms. Real user input resets KDE's own idle timer as usual; this module never touches the idle timer or the sleep inhibitor."""
import glob, re, subprocess, sys, threading, time
def state():
    for f in glob.glob("/sys/class/drm/card*-eDP-*/dpms"):
        try: return open(f).read().strip()
        except OSError: pass
    return "On"
def activity():
    """Count of keyboard / touchpad interrupts (Wayland offers no idle time): it changes only when the user touches the laptop's own input devices."""
    n = 0
    try:
        for l in open("/proc/interrupts"):
            if re.search(r"i8042|ELAN|SYNA|atkbd", l): n += sum(int(x) for x in l.split()[1:] if x.isdigit())
    except OSError: pass
    return n
def _set(on): subprocess.run(["kscreen-doctor", "--dpms", "on" if on else "off"], capture_output=True, timeout=10)
def raise_game():
    """After the panel wakes KWin can restack windows (the game ended up behind the terminal): put the game back in front, focus untouched (tools/kwin_raise_game.js)."""
    js = str(__import__("pathlib").Path(__file__).resolve().parent / "kwin_raise_game.js")
    try:
        subprocess.run(["qdbus6", "org.kde.KWin", "/Scripting", "org.kde.kwin.Scripting.unloadScript", "ogsr_raise"], capture_output=True, timeout=5)
        i = subprocess.run(["qdbus6", "org.kde.KWin", "/Scripting", "org.kde.kwin.Scripting.loadScript", js, "ogsr_raise"], capture_output=True, text=True, timeout=5).stdout.strip()
        if i and i != "-1": subprocess.run(["qdbus6", "org.kde.KWin", f"/Scripting/Script{i}", "org.kde.kwin.Script.run"], capture_output=True, timeout=5)
    except Exception: pass
_lock = threading.Lock(); _pending = {"t": None}
def wake_for_capture(settle=1.2):
    was_off = state() == "Off"
    if was_off:
        _set(True); time.sleep(settle); raise_game()
    a0 = activity()
    def done():
        if not was_off: return
        def later():
            time.sleep(3)
            with _lock:
                if _pending["t"] is not None and time.time() - _pending["t"] < 2.5: return     # another capture started meanwhile: that one turns it off
                if activity() != a0: return      # a key was pressed since the wake: the user is here, KDE's idle timer (60 s) will blank the screen later
                _set(False)
        _pending["t"] = time.time(); threading.Thread(target=later, daemon=True).start()
    return done
if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else "state"
    print(state()) if c == "state" else _set(c == "on")

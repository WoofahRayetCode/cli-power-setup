#!/usr/bin/env python3
"""Keeps Joplin Desktop alive and responsive (its local API on port 41184 is what the STALKER bridge and the phone inbox depend on).
  joplin_watchdog.py run        loop forever (sysguard job 'joplin_watchdog'); one instance only
  joplin_watchdog.py status     one line: process / API / last sync age / restarts this hour
Every 30 s: process missing -> start it; API not answering for > 90 s while the process runs -> ask it to quit (SIGTERM), after 60 s force it, then start it; last sync older than
30 min (the interval is 60 s) while the API answers -> log a warning, and after 60 min restart it. Safety: a 60 s grace after every start, at most 3 recoveries per hour (then it only
logs and writes the 'needs you' line), never force-kills during the grace of a polite quit. Joplin starts minimised (its own setting), so a restart does not steal focus."""
import json, os, re, signal, subprocess, sys, time, urllib.request
from pathlib import Path
here = Path(__file__).resolve().parent.parent
LOG = Path.home() / ".config/joplin-desktop/log.txt"; STATE = here / ".agents/joplin_watchdog.json"; OUT = here / ".agents/joplin_watchdog.log"; PID = here / ".agents/joplin_watchdog.pid"
def say(m):
    with open(OUT, "a") as f: f.write(time.strftime("%F %T ") + m + "\n")
def pids(): return [int(p) for p in subprocess.run("pgrep -f '^[^ ]*electron[0-9]* /usr/lib/joplin-desktop/app.asar( |$)'", shell=True, capture_output=True, text=True).stdout.split()]
def api_ok():
    try: return b"JoplinClipperServer" in urllib.request.urlopen("http://127.0.0.1:41184/ping", timeout=3).read()
    except Exception: return False
def sync_age():
    """seconds since the last 'Synchronizer:' line in Joplin's log (None if unknown)"""
    try:
        tail = LOG.read_text(errors="ignore").splitlines()[-400:]
        for l in reversed(tail):
            m = re.match(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d): Synchronizer:", l)
            if m: return time.time() - time.mktime(time.strptime(m.group(1), "%Y-%m-%d %H:%M:%S"))
    except Exception: pass
    return None
def load():
    try: return json.loads(STATE.read_text())
    except Exception: return {"restarts": [], "api_down_since": None, "started": 0}
def save(s): STATE.write_text(json.dumps(s))
def desktop_ready():
    """a Wayland/X display must exist before Electron is started (at login the watchdog can start before the desktop does: Joplin then dies at once)"""
    rt = os.environ.get("XDG_RUNTIME_DIR", "/run/user/%d" % os.getuid())
    return any((Path(rt) / n).exists() for n in ("wayland-0", "wayland-1")) and subprocess.run("pgrep -x kwin_wayland", shell=True, capture_output=True).returncode == 0
def start(s, why):
    env = dict(os.environ); env.setdefault("XDG_RUNTIME_DIR", "/run/user/%d" % os.getuid()); 
    socks = sorted(x.name for x in Path(env["XDG_RUNTIME_DIR"]).glob("wayland-[0-9]") if (Path(env["XDG_RUNTIME_DIR"]) / (x.name + ".lock")).exists())
    if socks: env["WAYLAND_DISPLAY"] = socks[-1]               # the LIVE socket: this process may carry a stale one from a previous login (that was the failure)
    env.setdefault("DISPLAY", ":0")
    say(f"starting Joplin ({why})"); subprocess.Popen(["joplin-desktop"], env=env, stdout=open(here / ".agents/joplin_start.out", "ab"), stderr=subprocess.STDOUT, start_new_session=True)
    s["started"] = time.time(); s["api_down_since"] = None; s["restarts"] = [t for t in s["restarts"] if time.time() - t < 3600] + [time.time()]; save(s)
def stop(s):
    for p in pids():
        try: os.kill(p, signal.SIGTERM)
        except OSError: pass
    for _ in range(30):
        if not pids(): return
        time.sleep(2)
    say("did not quit in 60 s: forcing")
    for p in pids():
        try: os.kill(p, signal.SIGKILL)
        except OSError: pass
    time.sleep(3)
def recover(s, why):
    if not desktop_ready(): return                              # no desktop yet: wait, do not burn attempts
    # back-off instead of giving up: wait 1, 2, 5, 10, then 30 min between attempts while it keeps failing (a long healthy run resets it)
    n = s.get("fails", 0); wait = [0, 60, 120, 300, 600, 1800][min(n, 5)]
    if time.time() - s.get("started", 0) < wait: return
    if n >= 4 and not s.get("said"): s["said"] = True; (here / ".agents/needs_you.txt").open("a").write("Joplin keeps failing to start; the watchdog keeps retrying with back-off (see .agents/joplin_start.out).\n")
    s["fails"] = n + 1
    if pids(): stop(s)
    start(s, why)
def tick():
    s = load(); now = time.time()
    if now - s.get("started", 0) < 60: return
    running = bool(pids())
    if not running: return recover(s, "process missing")
    if api_ok():
        if s.get("fails") and now - s.get("started", 0) > 600: s["fails"] = 0; s["said"] = False       # healthy for 10 min: forgive earlier failures
        s["api_down_since"] = None; save(s); age = sync_age()
        if age is not None and age > 3600: recover(s, f"no sync for {int(age // 60)} min")
        elif age is not None and age > 1800 and int(now) % 600 < 30: say(f"warning: last sync {int(age // 60)} min ago")
    else:
        s["api_down_since"] = s["api_down_since"] or now; save(s)
        if now - s["api_down_since"] > 90: recover(s, "API not answering for > 90 s")
def main():
    c = sys.argv[1] if len(sys.argv) > 1 else "status"
    if c == "status":
        s = load(); a = sync_age(); print(f"process {'up' if pids() else 'MISSING'} | API {'ok' if api_ok() else 'DOWN'} | last sync {'?' if a is None else f'{int(a // 60)} min ago'} | recoveries this hour {len([t for t in s['restarts'] if time.time() - t < 3600])}"); return
    if PID.exists():
        try: os.kill(int(PID.read_text()), 0); sys.exit(0)        # already running
        except Exception: pass
    PID.write_text(str(os.getpid())); say("watchdog started")
    while True:
        try: tick()
        except Exception as e: say(f"error: {e}")
        time.sleep(30)
main()

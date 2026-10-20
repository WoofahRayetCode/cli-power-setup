#!/usr/bin/env python3
"""Controller for a game session driven by complete_autowalk.script: presses a key whenever the game sits at "Press any key to play", watches the
walker's status file, clears crash dialogs, takes window-only screenshots, and writes a report.
usage: autoplay.py [--duration 300] [--shots 30] [--out DIR] [--stop-on-done]
Never touches any window but the game's; keys are XTEST events aimed at the game window."""
import argparse, glob, os, re, subprocess, sys, time
from pathlib import Path
here = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser(); ap.add_argument("--duration", type=int, default=300); ap.add_argument("--shots", type=int, default=30)
ap.add_argument("--out", default=str(here / "docs/walk")); ap.add_argument("--stop-on-done", action="store_true"); a = ap.parse_args()
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
logs = here / "_appdata_/logs"; status_f = logs / "walk_status.txt"
def sh(*c, t=15):
    done = None
    if c and c[0] == "import":              # a screenshot: wake the panel only for the capture (tools/dpms.py), then let it sleep again
        try: sys.path.insert(0, str(Path(__file__).resolve().parent)); import dpms; done = dpms.wake_for_capture()
        except Exception: done = None
    try: return subprocess.run(c, capture_output=True, text=True, timeout=t).stdout
    except Exception: return ""
    finally:
        if done: done()
def find_wid():
    for i in re.findall(r"0x[0-9a-f]+", sh("xprop", "-root", "_NET_CLIENT_LIST")):
        if re.search(r"xrengine|stalker|ogsr", sh("xprop", "-id", i, "WM_CLASS", "WM_NAME"), re.I): return i
def status():
    try:
        if time.time() - status_f.stat().st_mtime > 4: return None
        return dict(kv.split("=", 1) for kv in status_f.read_text().split() if "=" in kv)
    except Exception: return None
def screen_state(wid, tmp=str(Path("/tmp") / "autoplay_screen.png")):
    """Read the loading screen like a person: crop the bottom strip (percentage + caption) and OCR it. Returns (kind, pct, caption):
    kind = 'press_key' | 'loading' | 'playing' | 'unknown'.  The loading screen always shows 'NN%' and a caption such as 'Starting the game'."""
    sh("import", "-window", wid, tmp)
    sh("magick", tmp, "-crop", "560x90+360+610", "-colorspace", "Gray", "-resize", "250%", "-negate", "-threshold", "55%", tmp + ".c.png")
    txt = sh("tesseract", tmp + ".c.png", "-", "--psm", "6", t=20).strip().replace("\n", " ")
    m = re.search(r"(\d{1,3})\s*%", txt)
    if re.search(r"press\s*any", txt, re.I): return "press_key", 100, txt
    if m: return "loading", int(m.group(1)), txt
    return ("playing" if len(txt) < 3 else "unknown"), None, txt
import ctypes, ctypes.util
_x = None; _last_pos = None; _moved_t = 0.0
POINTER_IDLE_S = 4.0   # a pointer that merely RESTS over the game window (alt-tab, keyboard only) is not the user playing: only movement / a button counts
def pointer_in(wid):
    """True while the user is USING the mouse over the game window (XQueryPointer on the root + the window's root-relative rectangle): the pointer is
    inside AND it moved or a button is down within POINTER_IDLE_S. A resting pointer does not pause the walker."""
    global _x, _last_pos, _moved_t
    try:
        if _x is None:
            lib = ctypes.cdll.LoadLibrary(ctypes.util.find_library("X11")); lib.XOpenDisplay.restype = ctypes.c_void_p
            lib.XDefaultRootWindow.restype = ctypes.c_ulong; lib.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
            lib.XQueryPointer.argtypes = [ctypes.c_void_p, ctypes.c_ulong] + [ctypes.c_void_p] * 7
            lib.XTranslateCoordinates.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_int, ctypes.c_int] + [ctypes.c_void_p] * 3
            lib.XGetGeometry.argtypes = [ctypes.c_void_p, ctypes.c_ulong] + [ctypes.c_void_p] * 7
            d = lib.XOpenDisplay(None); _x = (lib, d, lib.XDefaultRootWindow(d)) if d else False
        if not _x: return False
        lib, d, root = _x; w = int(wid, 16)
        ri, ci = ctypes.c_ulong(), ctypes.c_ulong(); rx, ry, wx, wy = (ctypes.c_int() for _ in range(4)); mask = ctypes.c_uint()
        if not lib.XQueryPointer(d, root, ctypes.byref(ri), ctypes.byref(ci), ctypes.byref(rx), ctypes.byref(ry), ctypes.byref(wx), ctypes.byref(wy), ctypes.byref(mask)): return False
        if not ci.value: return False   # XWayland keeps the last X position while the pointer is over Wayland windows: require an X window under it
        gr = ctypes.c_ulong(); gx, gy = ctypes.c_int(), ctypes.c_int(); gw, gh, gb, gd = (ctypes.c_uint() for _ in range(4))
        if not lib.XGetGeometry(d, w, ctypes.byref(gr), ctypes.byref(gx), ctypes.byref(gy), ctypes.byref(gw), ctypes.byref(gh), ctypes.byref(gb), ctypes.byref(gd)): return False
        ox, oy, ch = ctypes.c_int(), ctypes.c_int(), ctypes.c_ulong()
        lib.XTranslateCoordinates(d, w, root, 0, 0, ctypes.byref(ox), ctypes.byref(oy), ctypes.byref(ch))
        pos = (rx.value, ry.value)
        if pos != _last_pos or (mask.value & 0x1F00): _moved_t = time.time()   # Button1-5 mask bits
        _last_pos = pos
        return ox.value <= rx.value < ox.value + gw.value and oy.value <= ry.value < oy.value + gh.value and time.time() - _moved_t < POINTER_IDLE_S
    except Exception:
        return False
pause_f = logs / "walk_pause.txt"
EVENT_SHOT = [("anomaly contact", "anomaly"), ("detour around", "detour"), ("stuck 3 ", "stuck"), ("skip waypoint", "skip"),
              ("objective", "objective"), ("WALK engage ", "engage"), ("WALK done", "done"), ("torch on", "torch"), ("! LISTEN ", "listen"),
              ("coach_start", "coach"), ("coach_end", "coach_done")]
log_pos = {"f": None, "n": 0}
req_f, resp_f = logs / "walk_request.txt", logs / "walk_route_dyn.txt"
served = {"rid": None}
def serve_route_request():
    """co-planner for the in-game task follower: 'rid level fx fy fz tx ty tz' -> A* route (tools/navplan.py) -> walk_route_dyn.txt"""
    try: parts = req_f.read_text().split()
    except Exception: return None
    if len(parts) < 8 or parts[0] == served["rid"]: return None
    rid, lvl = parts[0], parts[1]; served["rid"] = rid
    fr, to = ",".join(parts[2:5]), ",".join(parts[5:8])
    tmp = logs / "walk_route_dyn.tmp"; pts = logs / "walk_route_pts.tmp"
    r = subprocess.run([sys.executable, str(here / "tools/navplan.py"), "route", "dyn", lvl, f"--from={fr}", f"--to={to}", "--out", str(pts)], capture_output=True, text=True, timeout=120)
    ok = r.returncode == 0 and pts.exists()
    body = pts.read_text() if ok else ""
    tmp.write_text(f"rid {rid} {'ok' if ok else 'fail'}\n" + body); tmp.replace(resp_f)           # atomic: the walker never reads half a file
    return f"route request {rid} on {lvl}: " + ((r.stdout.strip().splitlines() or ['?'])[-1] if ok else "FAILED " + (r.stderr or r.stdout).strip()[-120:])
def new_log_lines():
    """lines appended to the engine log since the last call"""
    lg = newest_log()
    if not lg: return []
    if lg != log_pos["f"]: log_pos.update(f=lg, n=0)
    try:
        with open(lg, "rb") as fh:
            fh.seek(log_pos["n"]); data = fh.read(); log_pos["n"] += len(data)
        return data.decode("cp1251", "replace").splitlines()
    except Exception: return []
def newest_log():
    l = sorted(glob.glob(str(logs / "xray_*.log")), key=os.path.getmtime)
    return l[-1] if l else None
t0 = time.time(); wid = None; last_key = 0; last_shot = 0; last_sweep = 0; n_keys = 0; samples = []; shots = 0
last_screen = 0; load_sig = None; load_since = time.time(); stall_noted = False
wp_seen = {}; last_progress = (None, time.time()); state_prev = None; events = []; load_s = None; synced_at = None; user_in = False; user_events = 0; last_ev_shot = 0; ev_shots = []
harness_error = None; idle_since = None; walk_cfg_line = None
def log_has(pat):
    lg = newest_log()
    try: return bool(lg) and pat in open(lg, errors='replace').read()
    except Exception: return False
while time.time() - t0 < a.duration:
    time.sleep(1)
    wid = wid or find_wid()
    if not wid:
        if subprocess.run(["pgrep", "-f", "xrEngine[.]exe -nointro"], capture_output=True).returncode: events.append("game exited"); break
        continue
    inside = pointer_in(wid)
    if inside != user_in:
        user_in = inside
        if inside:
            user_events += 1; pause_f.write_text("pointer in game window\n")
            events.append(f"{time.time()-t0:5.0f}s USER pointer entered the game window -> walker paused (coaching active)")
        else:
            pause_f.unlink(missing_ok=True); events.append(f"{time.time()-t0:5.0f}s USER pointer left the game window -> walker resumes")
    msg = serve_route_request()
    if msg: events.append(f"{time.time()-t0:5.0f}s {msg}")
    st = status()
    state = "playing" if st else "loading"
    if state != state_prev: events.append(f"{time.time()-t0:5.0f}s state -> {state}"); state_prev = state
    if state == "playing" and load_s is None: load_s = round(time.time() - t0, 1)
    if state == "loading" and synced_at is None and log_has("End of synchronization"): synced_at = time.time()
    # the engine log says the level is loaded but the walker is not running yet: the game sits at "Press any key" (OCR can miss it)
    if state == "loading" and synced_at and time.time() - synced_at > 6 and time.time() - last_key > 4 and not user_in:
        subprocess.run([sys.executable, str(here / "tools/press_key.py"), wid, "Shift_L"], capture_output=True); last_key = time.time(); n_keys += 1
        events.append(f"{time.time()-t0:5.0f}s level synced {time.time()-synced_at:.0f} s ago, walker silent -> any key")
    if state == "loading" and time.time() - last_screen > 3:         # not in the level yet: read the load screen (percentage + caption) like a person would
        last_screen = time.time()
        kind, pct, cap = screen_state(wid)
        sig = (kind, pct)
        if sig != load_sig: load_sig, load_since = sig, time.time(); events.append(f"{time.time()-t0:5.0f}s screen: {kind} {pct if pct is not None else ''} {cap[:40]!r}")
        elif kind in ("loading", "unknown") and time.time() - load_since > 150 and not stall_noted:
            stall_noted = True
            lg = newest_log(); tail = open(lg, errors="replace").read().splitlines()[-6:] if lg else []
            events.append(f"{time.time()-t0:5.0f}s STALL: {kind} {pct}% for 150 s; log tail: " + " | ".join(x[-70:] for x in tail))
        if kind == "press_key" and time.time() - last_key > 2.5:     # 100%: any key starts the level
            subprocess.run([sys.executable, str(here / "tools/press_key.py"), wid, "Shift_L"], capture_output=True); last_key = time.time(); n_keys += 1
    # self-checks: a walker that has nothing to do, or that never started, is a HARNESS error: stop early and say exactly why
    if st:
        if st.get("want") in ("idle", "none"):
            idle_since = idle_since or time.time()
            if time.time() - idle_since > 30:
                harness_error = f"walker idle for 30 s (status want={st.get('want')}): " + (walk_cfg_line or "no '! WALK config' line in the log (script not registered or errored)")
                events.append(f"{time.time()-t0:5.0f}s HARNESS ERROR: {harness_error}"); break
        else: idle_since = None
    elif synced_at and time.time() - synced_at > 90 and state == "loading" and not samples:
        lg = newest_log(); errs = [l.strip()[-140:] for l in open(lg, errors="replace") if re.search(r"SCRIPT RUNTIME|LUA error|FATAL", l)][:3] if lg else []
        harness_error = "walker never wrote walk_status.txt 90 s after the level loaded" + (": " + " | ".join(errs) if errs else " (no script error in the log: is [walk] in the hook?)")
        events.append(f"{time.time()-t0:5.0f}s HARNESS ERROR: {harness_error}"); break
    elif samples and state == "loading" and time.time() - samples[-1][0] - t0 > 120 and not log_has("LEVELTOUR teleport") and not log_has("change_level"):
        harness_error = f"walker status stale for 120 s (last want={samples[-1][1].get('want')}): the script stopped updating"
        events.append(f"{time.time()-t0:5.0f}s HARNESS ERROR: {harness_error}"); break
    if st:
        samples.append((time.time() - t0, st))
        key = (st.get("level"), st.get("wp"))
        if key != last_progress[0] or st.get("want") == "user": last_progress = (key, time.time())
        elif time.time() - last_progress[1] > 60:
            events.append(f"{time.time()-t0:5.0f}s no waypoint progress for 60 s at wp {key} -> hop"); last_progress = (key, time.time())
            subprocess.run([sys.executable, str(here / "tools/press_key.py"), wid, "space"], capture_output=True)
        if a.stop_on_done and st.get("done") == "true": events.append("route done"); break
    if time.time() - last_sweep > 6:
        last_sweep = time.time()
        r = sh(str(here / "tools/crash_shot.sh"))
        if "Intercepted" in r: events.append("CRASH: " + " | ".join(l.strip() for l in r.splitlines() if "Description" in l)[:200]); break
    # screenshot what the walker just reacted to (visual QA of detours, anomaly contacts, stuck spots, objectives): max one per 4 s
    for line in new_log_lines():
        if '! WALK config:' in line: walk_cfg_line = line.split('] ', 2)[-1].strip(); events.append(f"{time.time()-t0:5.0f}s {walk_cfg_line[:150]}")
        if '! HEARD ' in line or '! LISTEN ' in line: events.append(f"{time.time()-t0:5.0f}s {line.split('] ', 2)[-1].strip()[:150]}")
        if '! WALK SELFCHECK' in line: events.append(f"{time.time()-t0:5.0f}s {line.split('] ', 2)[-1].strip()[:150]}")
        tag = next((tg for pat, tg in EVENT_SHOT if pat in line), None)
        if tag and time.time() - last_ev_shot > 4:
            last_ev_shot = time.time(); fn = out / f"ev_{len(ev_shots)+1:03d}_{tag}.png"
            sh("import", "-window", wid, str(fn)); ev_shots.append(f"{fn.name}: {line.split('] ', 2)[-1].strip()[:90]}")
    if a.shots and time.time() - last_shot > a.shots and st:
        last_shot = time.time(); shots += 1; sh("import", "-window", wid, str(out / f"walk_{shots:03d}.png"))
pause_f.unlink(missing_ok=True)
log = newest_log(); walk_lines = []; script_errors = []
if log:
    script_errors = [l.split("] ", 2)[-1].strip()[:160] for l in open(log, errors="replace") if re.search(r"SCRIPT RUNTIME|SCRIPT ERROR|LUA error|FATAL ERROR|stack traceback", l)]
    walk_lines = [l.split("] ", 2)[-1].strip() for l in open(log, errors="replace") if "! WALK" in l or "! AUTODEF protecting" in l]
fps = [float(s["fps"]) for _, s in samples if s.get("fps") not in (None, "0")]
rep = [f"autoplay {time.strftime('%F %T')}  duration {time.time()-t0:.0f}s  samples {len(samples)}  any-key presses {n_keys}  screenshots {shots}"]
if harness_error: rep.append("HARNESS ERROR (fix the harness, this run tested nothing): " + harness_error)
if samples:
    last = samples[-1][1]
    rep += [f"last: level={last.get('level')} wp={last.get('wp')} hp={last.get('hp')} pos={last.get('x')},{last.get('y')},{last.get('z')} done={last.get('done')}",
            f"max hostiles within 30 m: {max(int(s.get('hostile30', 0)) for _, s in samples)}  max stuck counter: {max(int(s.get('stuck', 0)) for _, s in samples)}"]
if fps: rep.append(f"fps avg {sum(fps)/len(fps):.0f} min {min(fps):.0f}")
rep += ["event screenshots:"] + [f"  {e}" for e in ev_shots] + ["events:"] + [f"  {e}" for e in events] + ["walker log:"] + [f"  {l}" for l in walk_lines[-60:]]
(out / "report.txt").write_text("\n".join(rep) + "\n"); print("\n".join(rep))
import json
last = samples[-1][1] if samples else {}
def num(v):
    try: return float(v)
    except Exception: return None
track = [[round(tt, 1), num(s.get("x")), num(s.get("z")), num(s.get("hp")), int(num(s.get("hostile30")) or 0), num(s.get("fps"))] for tt, s in samples[::2] if num(s.get("x")) is not None]
(out / "last_run.json").write_text(json.dumps({"time": time.strftime("%F %T"), "duration": round(time.time() - t0), "level": last.get("level"), "route": last.get("route"),
    "load_s": load_s, "any_key": n_keys, "track": track, "user_events": user_events, "script_errors": script_errors[:20], "harness_error": harness_error,
    "done": last.get("done") == "true", "wp": last.get("wp"), "hp": last.get("hp"), "events": events, "walk": walk_lines, "fps_avg": round(sum(fps)/len(fps)) if fps else None}))

#!/usr/bin/env python3
"""Learn from the last autoplay run (docs/walk/last_run.json) and keep a memory (docs/walk/memory.json) that tools/navplan.py and the next run use.
Every run is also appended to docs/walk/history.jsonl (regression database), so trends and regressions show up across sessions.
Rules (each came from a failure seen in a run):
  * blocked (hard, navplan removes nodes): 'stuck N at' with N >= 3, 'skip waypoint', 'fell'; radius 2.0 m, widened by 0.75 m per repeat (max 4.5)
  * danger (soft, navplan adds cost): positions where HP dropped or hostiles were within 30 m; weight grows with repeats
  * slow spots: positions where fps fell below 50 % of the run average (performance hot spots to look at, not avoided)
  * crashes: signature (first Description/FATAL line) counted; a signature never seen before is reported as NEW
  * load time (launch -> in level): flagged when > 2x the median of earlier runs; any-key presses and intro skip are tracked
  * a run that ended without 'done' while the waypoint index stopped moving -> that waypoint is a trouble spot
  * time budget: next run gets 1.6x the best completion time (min 90 s) so failures are found faster
usage: walkcoach.py            -> prints what it learned; last line is OK (route done) or REPLAN"""
import json, math, re, shutil, statistics, sys, time, traceback
from pathlib import Path
here = Path(__file__).resolve().parent.parent
run_f = here / "docs/walk/last_run.json"; mem_f = here / "docs/walk/memory.json"; hist_f = here / "docs/walk/history.jsonl"
bak_f = mem_f.with_suffix(".json.bak")
def fail(why):
    """never let a coach bug derail the loop: restore the last good memory, say so, ask for a re-plan"""
    if bak_f.exists(): shutil.copy(bak_f, mem_f)
    print(f"COACH RECOVERED: {why} (memory restored from last good copy)"); print("REPLAN"); sys.exit(0)
try:
    run = json.loads(run_f.read_text())
except Exception as e: fail(f"last_run.json unreadable: {e}")
try:
    mem = json.loads(mem_f.read_text()) if mem_f.exists() else {}
    if not isinstance(mem, dict): raise ValueError("not an object")
    if mem_f.exists(): shutil.copy(mem_f, bak_f)          # last good memory
except Exception as e:
    mem = json.loads(bak_f.read_text()) if bak_f.exists() else {}; print(f"memory.json corrupt ({e}): using the backup")
run.setdefault("walk", []); run.setdefault("events", []); run.setdefault("done", False); run.setdefault("wp", None); run.setdefault("duration", 0); run.setdefault("time", time.strftime("%F %T"))
# a run the user touched (pointer in the game window / view moved by hand) teaches nothing about the route
tainted = bool(run.get("user_events")) or any("user input detected" in l for l in run["walk"])
def main():
    global run, mem
    lvl = run.get("level") or "unknown"
    m = mem.setdefault(lvl, {}); [m.setdefault(k, v) for k, v in (("blocked", []), ("danger", []), ("slow", []), ("routes", {}))]
    g = mem.setdefault("_global", {"crashes": {}, "runs": 0}); g["runs"] += 1
    said = []

    def merge_spot(lst, x, z, r0, grow, rmax, extra=None):
        hit = next((b for b in lst if math.hypot(b[0] - x, b[1] - z) < max(3.0, b[2])), None)
        if hit:
            hit[2] = min(hit[2] + grow, rmax)
            if extra is not None and len(hit) > 3: hit[3] = min(hit[3] + extra, 6.0)
            return False
        lst.append([round(x, 1), round(z, 1), r0] + ([2.0] if extra is not None else []))
        return True

    # 1) hard blocks from walker messages
    new_block = 0
    for l in ([] if tainted else run.get("walk", [])):
        s = re.search(r"WALK (?:stuck (\d+) at|skip waypoint \d+ \(stuck spot|fell \(y=[-\d.]+\) -> back to)\s*\(?([-\d.]+),([-\d.]+),([-\d.]+)", l)
        if s and (int(s.group(1)) if s.group(1) else 99) >= 3:
            new_block += merge_spot(m["blocked"], float(s.group(2)), float(s.group(4)), 2.0, 0.75, 4.5)
    # 1b) anomaly contacts (god mode hides the damage, but a player would have been hurt): permanent block, the anomaly radius + 1 m
    for l in ([] if tainted else run.get("walk", [])):
        s = re.search(r"WALK anomaly contact (\S+) at ([-\d.]+),([-\d.]+),([-\d.]+) r=([\d.]+)", l)
        if s:
            new_block += merge_spot(m["blocked"], float(s.group(2)), float(s.group(4)), float(s.group(5)) + 1.0, 0.5, 8.0)
            said.append(f"anomaly contact: {s.group(1)} -> blocked")
    # 2) soft danger + slow spots from position samples (autoplay writes "track": [[t, x, z, hp, hostile30, fps], ...])
    track = [] if tainted else run.get("track", [])
    if tainted: said.append("run touched by the user (pointer in window / manual view move): recorded, nothing learned")
    new_danger = new_slow = 0
    for a, b in zip(track, track[1:]):
        if (b[3] is not None and a[3] is not None and b[3] < a[3] - 0.02) or (b[4] or 0) > 0:
            new_danger += merge_spot(m["danger"], b[1], b[2], 6.0, 1.0, 12.0, extra=0.5)
    fps = [s[5] for s in track if s[5]]
    if len(fps) > 10:
        avg = sum(fps) / len(fps)
        for s in track:
            if s[5] and s[5] < 0.5 * avg: new_slow += merge_spot(m["slow"], s[1], s[2], 5.0, 0.0, 5.0)
    # 3) crash memory
    crash = next((e for e in run.get("events", []) if e.strip().split("s ", 1)[-1].startswith("CRASH")), None)
    if crash:
        sig = re.sub(r"\s+", " ", crash.split("CRASH:", 1)[-1]).strip()[:160] or "unknown"
        seen = g["crashes"].get(sig, 0); g["crashes"][sig] = seen + 1
        said.append(("NEW crash: " if not seen else f"repeat crash (x{seen + 1}): ") + sig)
    # 4) load time / any-key / intro regression check
    hist = [json.loads(l) for l in hist_f.read_text().splitlines()] if hist_f.exists() else []
    lt = run.get("load_s")
    prev_lt = [h["load_s"] for h in hist if h.get("load_s")]
    if lt and len(prev_lt) >= 3 and lt > 2 * statistics.median(prev_lt):
        said.append(f"LOAD REGRESSION: {lt:.0f} s vs median {statistics.median(prev_lt):.0f} s")
    if run.get("any_key"): said.append(f"any-key presses needed: {run['any_key']} (harness sets keypress_on_start off: should be 0)")
    if run.get("intro_played"): said.append("new-game intro played although -skipgameintro was passed")
    # harness errors are not game results: say so, keep the run out of the route statistics, and ask for a fix rather than a re-plan
    if run.get("harness_error"):
        print("HARNESS ERROR: " + run["harness_error"])
        with hist_f.open("a") as f: f.write(json.dumps({"time": run["time"], "level": lvl, "harness_error": run["harness_error"]}) + "\n")
        mem_f.write_text(json.dumps(mem, indent=1)); print("HARNESS"); return
    # 5) route stats + adaptive time budget
    r = m["routes"].setdefault(run.get("route") or "?", {"attempts": 0, "successes": 0, "best_s": None})
    r["attempts"] += 1; r["last"] = {"done": run["done"], "wp": run["wp"], "seconds": run["duration"], "time": run["time"], "fps_avg": run.get("fps_avg")}
    if run["done"]:
        r["successes"] += 1; r["best_s"] = min(run["duration"], r["best_s"] or 1e9)
    r["budget_s"] = max(90, round(1.6 * r["best_s"])) if r["best_s"] else None
    mem_f.write_text(json.dumps(mem, indent=1))
    with hist_f.open("a") as f:
        f.write(json.dumps({"time": run["time"], "level": lvl, "route": run.get("route"), "done": run["done"], "wp": run["wp"], "duration": run["duration"],
                            "load_s": lt, "fps_avg": run.get("fps_avg"), "fps_min": min(fps) if fps else None, "any_key": run.get("any_key"),
                            "crash": bool(crash), "new_blocked": new_block, "new_danger": new_danger}) + "\n")
    print(f"level {lvl} route {run.get('route')}: done={run['done']} wp={run['wp']}  load {lt or '?'} s  fps avg {run.get('fps_avg')}")
    print(f"learned: blocked +{new_block} (total {len(m['blocked'])}), danger +{new_danger} (total {len(m['danger'])}), slow spots +{new_slow} (total {len(m['slow'])})")
    print(f"route record: attempts {r['attempts']} ok {r['successes']} best {r['best_s']} s next budget {r['budget_s']} s")
    for s in said: print(s)
    # 6) grade against the test spec the walker announced ("! WALK test NAME: description | pass=a,b,c | ...")
    spec = next((re.search(r"WALK test (\S+): (.*?) \| pass=([^|]*)", l) for l in run["walk"] if "WALK test " in l), None)
    if spec:
        name, crit = spec.group(1), [c.strip() for c in spec.group(3).split(",") if c.strip()]
        fails = []
        for c in crit:
            k, _, v = c.partition("=")
            if k == "objectives":
                bad = [l for l in run["walk"] if "objective" in l and "FAILED" in l]
                if bad or not any("objective" in l and "DONE" in l for l in run["walk"]): fails.append("objectives: " + ("; ".join(b[-90:] for b in bad) or "none completed"))
            elif k == "route" and not run["done"]: fails.append(f"route not finished (wp {run['wp']})")
            elif k == "no_crash" and crash: fails.append("crash")
            elif k == "no_script_error" and run.get("script_errors"): fails.append(f"{len(run['script_errors'])} script errors, first: {run['script_errors'][0][:100]}")
            elif k == "no_anomaly_contact":
                n = sum("anomaly contact" in l for l in run["walk"])
                if n: fails.append(f"{n} anomaly contacts")
            elif k == "max_skips":
                n = sum("skip waypoint" in l for l in run["walk"])
                if n > int(v): fails.append(f"{n} skipped waypoints > {v}")
            elif k == "max_load_s" and lt and lt > float(v): fails.append(f"load {lt:.0f} s > {v}")
            elif k == "min_fps" and fps and min(fps) < float(v): fails.append(f"fps min {min(fps):.0f} < {v}")
        if tainted: fails.append("user touched the game: result not trusted")
        print(f"TEST {name}: {'PASS' if not fails else 'FAIL'}" + ("" if not fails else " - " + " | ".join(fails)))
        with (here / "docs/walk/tests.jsonl").open("a") as f:
            f.write(json.dumps({"time": run["time"], "test": name, "pass": not fails, "fails": fails, "duration": run["duration"]}) + "\n")
    print("OK" if run["done"] else "REPLAN")   # learned spots are used by the next plan either way
try:
    main()
except SystemExit: raise
except Exception:
    fail("coach crashed: " + traceback.format_exc().strip().splitlines()[-1])

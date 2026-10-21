#!/usr/bin/env python3
"""Walker data collector (the training data for the GPU trainer, and the report Antigravity reads to help the walker learn).
Runs while an OGSR game with the auto walker is up (guardian starts it). Read-only: only reads the files the game writes.
  docs/learn/walker_dataset.jsonl   1 row / 2 s: {t, level, x, z, wp, dist, want, speed, stuck, hostile30, fps, n_enemy, n_ally, nearest_enemy, nearest_anomaly, nearest_artifact}
                                    + event rows {ev: kick|learned|hot|skip|stuck, ...} parsed from the newest xray log (with the angle tried and whether it worked)
  .agents/walker_report.md          every 60 s: per level - minutes walked, metres moved, stuck seconds, kicks, learned, hot cells (the worst first), and a one-line verdict
Rotates the dataset at 50 MB."""
import glob, json, math, os, re, time
from collections import Counter, defaultdict
from pathlib import Path
here = Path(__file__).resolve().parent.parent; LOGS = here / "_appdata_/logs"; DS = here / "docs/learn/walker_dataset.jsonl"; REP = here / ".agents/walker_report.md"
DS.parent.mkdir(exist_ok=True)
st = {"log": None, "pos": 0, "last": None, "stats": defaultdict(lambda: Counter()), "t_row": 0, "t_rep": 0, "hot": Counter()}
def status():
    try: line = (LOGS / "walk_status.txt").read_text().strip().splitlines()[-1]
    except Exception: return None
    d = dict(re.findall(r"(\w+)=(\S+)", line)); return d if "x" in d else None
def world():
    near = {"E": 1e9, "Z": 1e9, "A": 1e9}; ne = na = 0
    try:
        rows = [l.split() for l in (LOGS / "walk_world.txt").read_text().splitlines()]
        me = next(r for r in rows if r[0] == "P"); mx, mz = float(me[1]), float(me[2])
        for r in rows:
            if r[0] in "EMFNZAI" and len(r) >= 3:
                d = math.hypot(float(r[1]) - mx, float(r[2]) - mz)
                if r[0] in "EM": ne += 1; near["E"] = min(near["E"], d)
                elif r[0] == "F": na += 1
                elif r[0] in "ZA": near[r[0]] = min(near[r[0]], d)
    except Exception: pass
    return {"n_enemy": ne, "n_ally": na, **{"nearest_" + {"E": "enemy", "Z": "anomaly", "A": "artifact"}[k]: (round(v, 1) if v < 1e8 else None) for k, v in near.items()}}
def emit(row):
    with open(DS, "a") as f: f.write(json.dumps(row) + "\n")
def events(level):
    fs = sorted(glob.glob(str(LOGS / "xray_*.log")), key=os.path.getmtime)
    if not fs: return
    f = fs[-1]
    if f != st["log"]: st["log"], st["pos"] = f, max(0, os.path.getsize(f) - 30000)
    try:
        with open(f, "rb") as fh: fh.seek(st["pos"]); data = fh.read().decode("utf-8", "ignore"); st["pos"] = fh.tell()
    except Exception: return
    for l in data.splitlines():
        t = time.time(); S = st["stats"][level]
        m = re.search(r"WALK UNSTICK Aisha portal \(([^)]*), kick (\d+) here, angle (\S+)\) (-?[\d.]+),[-\d.]+,(-?[\d.]+) -> (-?[\d.]+),[-\d.]+,(-?[\d.]+)", l)
        if m: emit({"t": t, "ev": "kick", "level": level, "mode": m.group(1), "n": int(m.group(2)), "angle": m.group(3), "from": [float(m.group(4)), float(m.group(5))], "to": [float(m.group(6)), float(m.group(7))]}); S["kicks"] += 1
        elif "UNSTICK learned" in l:
            m = re.search(r"approach (-?\d+) deg.*at (-?[\d.]+),(-?[\d.]+)", l); emit({"t": t, "ev": "learned", "level": level, "angle": m and m.group(1), "at": m and [float(m.group(2)), float(m.group(3))]}); S["learned"] += 1
        elif "WALK hot spot" in l: emit({"t": t, "ev": "hot", "level": level, "text": l.split("WALK hot spot")[-1].strip()[:80]}); S["hot"] += 1
        elif "WALK skip waypoint" in l: emit({"t": t, "ev": "skip", "level": level, "text": l.split("WALK skip")[-1].strip()[:80]}); S["skips"] += 1
        elif "WALK stuck" in l:
            m = re.search(r"stuck (\d+) at (-?[\d.]+),[-\d.]+,(-?[\d.]+)", l)
            if m: S["stuck_s"] += 1; st["hot"][(level, int(float(m.group(2)) // 6), int(float(m.group(3)) // 6))] += 1
def report():
    lines = [f"# Walker report {time.strftime('%F %T')}", "", "| level | min | metres | stuck s | kicks | learned | gave up | hot |", "|---|---|---|---|---|---|---|---|"]
    for lv, S in sorted(st["stats"].items()):
        lines.append(f"| {lv} | {S['sec'] / 60:.1f} | {S['m']:.0f} | {S['stuck_s']} | {S['kicks']} | {S['learned']} | {S['skips']} | {S['hot']} |")
    worst = st["hot"].most_common(5)
    lines += ["", "Worst cells (level, cell x/6m, z/6m: stuck seconds): " + "; ".join(f"{k[0]} {k[1]},{k[2]}: {v}" for k, v in worst)]
    tot = Counter();  [tot.update(S) for S in st["stats"].values()]
    verdict = "no data yet" if not tot["sec"] else (f"stuck {100 * tot['stuck_s'] / max(1, tot['sec']):.1f}% of the time, {tot['kicks']} kicks, {tot['learned']} learned, {tot['skips']} waypoints given up"
              + ("  -> the walker is losing time to snags: look at the worst cells" if tot["stuck_s"] > 0.15 * tot["sec"] else "  -> healthy"))
    lines += ["", "Verdict: " + verdict]
    REP.write_text("\n".join(lines) + "\n")
def main():
    gone = None
    while True:
        up = bool(os.popen("pgrep -f '[x]rEngine.exe' | head -1").read().strip())
        if not up:
            gone = gone or time.time()
            if time.time() - gone > 60: return
            time.sleep(5); continue
        gone = None; s = status(); now = time.time()
        if s and now - os.path.getmtime(LOGS / "walk_status.txt") < 10:
            lvl = s.get("level", "?"); x, z = float(s["x"]), float(s["z"]); S = st["stats"][lvl]
            if st["last"] and st["last"][0] == lvl:
                dm = math.hypot(x - st["last"][1], z - st["last"][2]); S["m"] += dm if dm < 30 else 0
                S["sec"] += min(2.0, now - st["last"][3])
            st["last"] = (lvl, x, z, now); events(lvl)
            if now - st["t_row"] >= 2:
                st["t_row"] = now
                emit({"t": round(now, 1), "level": lvl, "x": x, "z": z, "wp": s.get("wp"), "dist": float(s.get("dist", -1)), "want": s.get("want"), "speed": float(s.get("speed", 0)),
                      "stuck": int(s.get("stuck", 0)), "hostile30": int(s.get("hostile30", 0)), "fps": float(s.get("fps", 0)), **world()})
        if now - st["t_rep"] >= 60: st["t_rep"] = now; report()
        try:
            if DS.exists() and DS.stat().st_size > 50e6: DS.rename(DS.with_suffix(f".{int(now)}.jsonl"))
        except Exception: pass
        time.sleep(2)
if __name__ == "__main__":
    if os.popen("pgrep -f '^python3 .*walker_collect.py' | grep -vx %d | head -1" % os.getpid()).read().strip(): raise SystemExit(0)
    main()

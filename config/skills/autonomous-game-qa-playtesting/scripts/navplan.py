#!/usr/bin/env python3
"""Plan walkable routes for complete_autowalk.script from the level's AI navmesh (exported by the walker with [walk] dump = true).
  navplan.py pois LEVEL [pattern]                              list points of interest (smart terrains, level changers, story objects)
  navplan.py route NAME LEVEL --from x,y,z --to x,y,z          A* over the navmesh -> walk_routes.ltx [NAME]
  navplan.py route NAME LEVEL --from x,y,z --to-poi PATTERN    ... to the nearest POI whose name/section contains PATTERN
Input files: _appdata_/logs/nav_<level>.txt ("id x y z" per node) and poi_<level>.txt. Nodes are a regular grid (~0.7 m): neighbours are found from positions."""
import argparse, heapq, math, re, sys
from pathlib import Path
here = Path(__file__).resolve().parent.parent
logs = here / "_appdata_/logs"
def load_nav(level):
    f = logs / f"nav_{level}.txt"
    if not f.exists(): sys.exit(f"{f} missing: run a game with [walk] dump = true on {level} first (tools/autowalk.sh)")
    ids, pos = [], []
    for l in f.open():
        if l.startswith("#"): continue
        i, x, y, z = l.split(); ids.append(int(i)); pos.append((float(x), float(y), float(z)))
    return ids, pos
def build(pos):
    xs = sorted({round(p[0], 2) for p in pos}); step = min((b - a for a, b in zip(xs, xs[1:]) if b - a > 0.05), default=0.7)
    cell = {}
    for n, (x, y, z) in enumerate(pos): cell.setdefault((round(x / step), round(z / step)), []).append(n)
    return step, cell
def neighbours(n, pos, cell, step, maxdy=0.9):
    x, y, z = pos[n]; cx, cz = round(x / step), round(z / step)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        for m in cell.get((cx + dx, cz + dz), ()):
            if abs(pos[m][1] - y) <= maxdy:
                if dx and dz:       # diagonals only when both orthogonal neighbours exist (no corner cutting)
                    if not any(abs(pos[k][1] - y) <= maxdy for k in cell.get((cx + dx, cz), ())) or not any(abs(pos[k][1] - y) <= maxdy for k in cell.get((cx, cz + dz), ())): continue
                yield m, math.dist((x, z), (pos[m][0], pos[m][2]))
def nearest(pos, p):
    return min(range(len(pos)), key=lambda n: (pos[n][0]-p[0])**2 + (pos[n][2]-p[2])**2 + 4*(pos[n][1]-p[1])**2)
def node_penalty(pos, cell, step, danger):
    """extra cost per node: hugging walls/ledges (few walkable neighbours) is where the walker snags; learned danger spots (damage, hostiles) cost more"""
    memo = {}
    def pen(m):
        if m in memo: return memo[m]
        deg = sum(1 for _ in neighbours(m, pos, cell, step))
        p = max(0, 8 - deg) * 0.35 * step
        for dx, dz, r, w in danger:
            if (pos[m][0]-dx)**2 + (pos[m][2]-dz)**2 <= r*r: p += w * step
        memo[m] = p; return p
    return pen
def astar(pos, cell, step, s, g, pen=lambda m: 0.0):
    openh = [(0, s)]; came = {s: None}; cost = {s: 0.0}
    while openh:
        _, n = heapq.heappop(openh)
        if n == g: break
        for m, d in neighbours(n, pos, cell, step):
            c = cost[n] + d + pen(m)
            if c < cost.get(m, 1e18):
                cost[m] = c; came[m] = n
                heapq.heappush(openh, (c + math.dist((pos[m][0], pos[m][2]), (pos[g][0], pos[g][2])), m))
    if g not in came: return None
    path = []; n = g
    while n is not None: path.append(n); n = came[n]
    return path[::-1]
def simplify(pos, path, max_gap=5.0):
    """keep a waypoint at every turn of more than ~25 degrees and at least every max_gap metres"""
    out = [path[0]]; last_dir = None; acc = 0.0
    for a, b in zip(path, path[1:]):
        d = (pos[b][0]-pos[a][0], pos[b][2]-pos[a][2]); L = math.hypot(*d) or 1; d = (d[0]/L, d[1]/L); acc += L
        if last_dir and (d[0]*last_dir[0] + d[1]*last_dir[1] < 0.9 or acc >= max_gap): out.append(a); acc = 0.0
        last_dir = d
    out.append(path[-1]); return out
def clear_line(pos, cell, step, a, b, deg):
    """straight a->b stays on walkable floor (stairs ok) and never gets closer to a wall than its own end points (narrow corridors: as central as they are)"""
    (ax, ay, az), (bx, by, bz) = pos[a], pos[b]
    need = min(8, deg(a), deg(b))
    L = math.hypot(bx - ax, bz - az); n = max(1, int(L / (step * 0.5)))
    for k in range(1, n):
        f = k / n; x, y, z = ax + (bx - ax) * f, ay + (by - ay) * f, az + (bz - az) * f
        cand = [m for m in cell.get((round(x / step), round(z / step)), ()) if abs(pos[m][1] - y) <= 0.9]
        if not cand or deg(cand[0]) < need: return False
    return True
def string_pull(pos, cell, step, path, max_gap=6.0):
    """keep as few waypoints as possible, but never let a straight leg cut a corner or brush a wall (stairwells, door frames)"""
    memo = {}
    def deg(m):
        if m not in memo: memo[m] = sum(1 for _ in neighbours(m, pos, cell, step))
        return memo[m]
    out = [path[0]]; i = 0
    while i < len(path) - 1:
        j = i + 1
        while j + 1 < len(path) and math.dist((pos[path[i]][0], pos[path[i]][2]), (pos[path[j+1]][0], pos[path[j+1]][2])) <= max_gap \
                and clear_line(pos, cell, step, path[i], path[j + 1], deg):
            j += 1
        out.append(path[j]); i = j
    return out
def load_pois(level):
    f = logs / f"poi_{level}.txt"
    if not f.exists(): sys.exit(f"{f} missing (dump the level first)")
    r = []
    for l in f.open(errors="replace"):
        p = l.strip().split("|")
        if len(p) >= 7: r.append(dict(name=p[0], sect=p[1], sid=p[2], pos=(float(p[3]), float(p[4]), float(p[5])), lvid=int(p[6])))
    return r
ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
a1 = sub.add_parser("pois"); a1.add_argument("level"); a1.add_argument("pattern", nargs="?", default="")
a2 = sub.add_parser("route"); a2.add_argument("name"); a2.add_argument("level"); a2.add_argument("--from", dest="src", required=True)
a2.add_argument("--to"); a2.add_argument("--to-poi"); a2.add_argument("--out", help="also write the waypoints as plain 'x y z' lines (runtime routes for the task follower)"); a = ap.parse_args()
if a.cmd == "pois":
    for p in load_pois(a.level):
        if a.pattern in p["name"] or a.pattern in p["sect"]: print(f'{p["name"]:34} {p["sect"]:22} story={p["sid"]:>5}  {p["pos"][0]:8.1f} {p["pos"][1]:7.1f} {p["pos"][2]:8.1f}')
    sys.exit()
ids, pos = load_nav(a.level); step, cell = build(pos); pos_all = pos
import json
mem_f = here / "docs/walk/memory.json"
lmem = json.loads(mem_f.read_text()).get(a.level, {}) if mem_f.exists() else {}
bad = lmem.get("blocked", [])     # learned by tools/walkcoach.py
danger = [(d[0], d[1], d[2], d[3] if len(d) > 3 else 2.0) for d in lmem.get("danger", [])]   # soft: paths may cross, but prefer not to
# anomalies from the level dump (poi_<level>.txt, section zone_*): hard no-go circles; radiation fields: soft cost
ZONE_R = {"gravi": 4.0, "mincer": 4.0, "mosquito": 4.0, "zharka": 3.5, "buzz": 3.5, "witches": 4.0, "galantine": 4.0, "electra": 4.0, "ameba": 4.0, "burning": 3.5, "teleport": 3.0}
if (logs / f"poi_{a.level}.txt").exists():
    nz = 0
    for p in load_pois(a.level):
        s = p["sect"]
        if not s.startswith("zone_") and "anomal" not in s: continue
        if "radioactive" in s or "field" in s: danger.append((p["pos"][0], p["pos"][2], 12.0, 3.0)); continue
        r = next((v for k, v in ZONE_R.items() if k in s), 4.0); bad = bad + [[p["pos"][0], p["pos"][2], r + 1.5]]; nz += 1
    if nz: print(f"anomalies from the level dump: {nz} blocked")
if bad:
    import numpy as np
    P = np.asarray(pos); ok = np.ones(len(P), dtype=bool)
    for bx, bz, br in bad: ok &= (P[:, 0] - bx) ** 2 + (P[:, 2] - bz) ** 2 > br * br       # vectorised: 100+ circles x 600k nodes in well under a second
    keep = np.flatnonzero(ok).tolist()
    print(f"avoiding {len(bad)} remembered trouble spots ({len(pos)-len(keep)} nodes removed)")
    pos = [pos[n] for n in keep]; step, cell = build(pos)
src = tuple(map(float, a.src.split(",")))
if a.to: dst = tuple(map(float, a.to.split(",")))
else:
    c = [p for p in load_pois(a.level) if p["name"] == a.to_poi] or [p for p in load_pois(a.level) if a.to_poi in p["name"] or a.to_poi in p["sect"]]   # exact name wins
    if not c: sys.exit(f"no POI matches {a.to_poi}")
    c.sort(key=lambda p: math.dist(p["pos"], src)); dst = c[0]["pos"]; print("goal:", c[0]["name"], c[0]["pos"])
s, g = nearest(pos, src), nearest(pos, dst)
path = astar(pos, cell, step, s, g, node_penalty(pos, cell, step, danger))
if not path and bad:   # learned blocks may have cut the map in two: forget them for this plan rather than fail the run
    print(f"no path with {len(bad)} learned blocks: planning without them (soft danger costs kept)")
    pos = pos_all; step, cell = build(pos); s, g = nearest(pos, src), nearest(pos, dst)
    path = astar(pos, cell, step, s, g, node_penalty(pos, cell, step, danger))
if not path: sys.exit(f"no path (nodes {len(pos)}, grid step {step:.2f}); start/goal may be on separate islands")
wps = string_pull(pos, cell, step, path); length = sum(math.dist((pos[x][0], pos[x][2]), (pos[y][0], pos[y][2])) for x, y in zip(path, path[1:]))
if a.out:
    Path(a.out).write_text("".join(f"{pos[n][0]:.2f} {pos[n][1]:.2f} {pos[n][2]:.2f}\n" for n in wps)); print(f"route {a.name}: {len(wps)} waypoints, {length:.0f} m -> {a.out}"); sys.exit()
f = here / "gamedata/config/misc/walk_routes.ltx"
text = f.read_text() if f.exists() else ""
text = re.sub(rf"\n?\[{re.escape(a.name)}\].*?(?=\n\[|\Z)", "", text, flags=re.S).rstrip() + "\n"
text += f"\n[{a.name}]\nlevel = {a.level}\n" + "".join(f"p{i+1} = {pos[n][0]:.2f}, {pos[n][1]:.2f}, {pos[n][2]:.2f}\n" for i, n in enumerate(wps))
f.write_text(text); print(f"route {a.name}: {len(wps)} waypoints, {length:.0f} m over {len(path)} nodes -> {f}")

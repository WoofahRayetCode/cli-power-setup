#!/usr/bin/env python3
"""Walker Mind: a live top-down wireframe of what the auto walker is "thinking" (for fun, and to see why it gets stuck). A small always-on-top window under the status window.
Reads only files the game already writes (no input, never touches the game): _appdata_/logs/walk_status.txt (position, waypoint, want, stuck, hostiles, fps), walk_route_pts.tmp (the route),
stuck_spots.txt (hot cells), and the newest xray log (stuck / UNSTICK / learned lines).
Drawing: range rings and a faint 10 m grid (wireframe), the route as a line with waypoint dots (the current target is a bright ring with a line to it), the player's trail and heading,
red squares on hot stuck cells (kicks so far), orange arrows for Aisha's portal kicks, and a thought line: what it is doing (want=fwd/turn/strafe...), speed, stuck counter, danger, FPS.
Run: python3 tools/walker_mind.py   (the layout script docks it bottom-right; it closes itself 30 s after the game is gone)"""
import glob, math, os, re, time, tkinter as tk
from PIL import Image, ImageEnhance, ImageTk
from collections import deque
from pathlib import Path
here = Path(__file__).resolve().parent.parent; LOGS = here / "_appdata_/logs"
W, H, SCALE = 640, 422, 3.2   # 422 = the 450 px tall slot minus the 28 px title bar          # px, px, px per metre (about 100 m across)
BG, GRID, RING, ROUTE, WP, CUR, ME, HOT, KICK, TXT = "#0b0f14", "#16202b", "#22364a", "#2f9e6e", "#5fd3a0", "#ffd166", "#4cc9f0", "#ef476f", "#ff9f1c", "#c8d3df"
trail = deque(maxlen=400); state = {"lvl": None, "route_mt": 0, "route": [], "kicks": deque(maxlen=12), "events": deque(maxlen=4), "log": None, "pos": 0, "hot": {}, "hot_mt": 0, "gone": None}
def status():
    try: line = (LOGS / "walk_status.txt").read_text().strip().splitlines()[-1]
    except Exception: return None
    d = dict(re.findall(r"(\w+)=(\S+)", line)); return d if "x" in d else None
def load_route():
    p = LOGS / "walk_route_pts.tmp"
    try:
        if p.stat().st_mtime != state["route_mt"]:
            state["route_mt"] = p.stat().st_mtime; state["route"] = [(float(a[0]), float(a[2])) for a in (l.split() for l in p.read_text().splitlines()) if len(a) >= 3]
    except Exception: pass
def load_hot(lvl):
    p = LOGS / "stuck_spots.txt"
    try:
        if p.stat().st_mtime != state["hot_mt"]:
            state["hot_mt"] = p.stat().st_mtime; state["hot"] = {}
            for l in p.read_text().splitlines():
                m = re.match(r"([^|]+)\|(-?\d+)\|(-?\d+)\|(\d+)\|(-?\d+)", l)
                if m and m.group(1) == lvl:
                    state["hot"][(int(m.group(2)) * 6 + 3, int(m.group(3)) * 6 + 3)] = int(m.group(4))
                    if int(m.group(5)) != 0: state.setdefault("solved", set()).add((int(m.group(2)) * 6 + 3, int(m.group(3)) * 6 + 3))
    except Exception: pass
ICON = here / "docs/learn/icons/aisha_cat.png"          # a cat emote (Noto Color Emoji) used for Aisha on the map
def cat_icon(px):
    try: return Image.open(ICON).convert("RGBA").resize((px, int(px * 0.89)), Image.LANCZOS)
    except Exception: return None
MAPS = here / "docs/learn/minimaps"
def level_map(lvl):
    """the game's own top-down map of this level (map_<name>.png from textures/map + bound_rect from game_maps_single.ltx), dimmed, cached; None when the level has none"""
    if state.get("map_lvl") == lvl: return state.get("map")
    state["map_lvl"], state["map"] = lvl, None
    try:
        txt = (MAPS / "game_maps_single.ltx").read_text(errors="ignore")
        sec = re.search(r"\[%s\]([^\[]*)" % re.escape(lvl), txt, re.I | re.S).group(1)
        tex = re.search(r"texture\s*=\s*map\\(\w+)", sec).group(1)
        r = [float(v) for v in re.search(r"bound_rect\s*=\s*([-\d.,\s]+)", sec).group(1).replace(",", " ").split()[:4]]
        im = Image.open(MAPS / f"{tex}.png").convert("RGB"); im = ImageEnhance.Brightness(im).enhance(0.55)
        state["map"] = (im, r)            # r = x1, z1, x2, z2 in world metres; the map's top edge is z2 (north)
    except Exception: pass
    return state["map"]
def map_photo(lvl, ox, oz):
    m = level_map(lvl)
    if not m: return None
    im, (x1, z1, x2, z2) = m; ppm_x, ppm_z = im.width / (x2 - x1), im.height / (z2 - z1)          # image pixels per metre
    left, right = ox - W / 2 / SCALE, ox + W / 2 / SCALE; top, bottom = oz + (H / 2 - 18) / SCALE, oz - (H / 2 + 18) / SCALE
    box = ((left - x1) * ppm_x, (z2 - top) * ppm_z, (right - x1) * ppm_x, (z2 - bottom) * ppm_z)
    view = Image.new("RGB", (W, H), (11, 15, 20))
    try: view = im.transform((W, H), Image.AFFINE, ((box[2] - box[0]) / W, 0, box[0], 0, (box[3] - box[1]) / H, box[1]), Image.BILINEAR, fillcolor=(11, 15, 20))
    except Exception: pass
    return ImageTk.PhotoImage(view)
def read_world():
    """walk_world.txt (written once a second by complete_autowalk.script): things near the player"""
    out = []
    try:
        if time.time() - (LOGS / "walk_world.txt").stat().st_mtime > 8: return out
        for l in (LOGS / "walk_world.txt").read_text().splitlines():
            a = l.split(None, 4)
            if len(a) >= 3 and a[0] in "EFNMZAIC": out.append((a[0], float(a[1]), float(a[2]), a[3:]))
    except Exception: pass
    return out
def explored(lvl, x, z):
    """areas walked on this level, remembered across sessions (2 m cells) in docs/learn/explored_<level>.json: the 'game world' layer"""
    p = here / "docs/learn" / f"explored_{lvl}.json"
    if state.get("exp_lvl") != lvl:
        state["exp_lvl"], state["exp"], state["exp_dirty"] = lvl, set(), 0
        try: state["exp"] = {tuple(c) for c in __import__("json").loads(p.read_text())}
        except Exception: pass
    cell = (int(x // 2), int(z // 2))
    if cell not in state["exp"]: state["exp"].add(cell); state["exp_dirty"] += 1
    if state["exp_dirty"] >= 40:
        state["exp_dirty"] = 0
        try: p.parent.mkdir(exist_ok=True); p.write_text(__import__("json").dumps(sorted(state["exp"])))
        except Exception: pass
    return state["exp"]
def read_log():
    fs = sorted(glob.glob(str(LOGS / "xray_*.log")), key=os.path.getmtime)
    if not fs: return
    f = fs[-1]
    if f != state["log"]: state["log"], state["pos"] = f, max(0, os.path.getsize(f) - 20000)
    try:
        with open(f, "rb") as fh:
            fh.seek(state["pos"]); data = fh.read().decode("utf-8", "ignore"); state["pos"] = fh.tell()
    except Exception: return
    for l in data.splitlines():
        m = re.search(r"WALK UNSTICK Aisha portal \(([^)]*)\).* (-?[\d.]+),(-?[\d.]+),(-?[\d.]+) -> (-?[\d.]+),(-?[\d.]+),(-?[\d.]+)", l)
        if m: state["kicks"].append(((float(m.group(2)), float(m.group(4))), (float(m.group(5)), float(m.group(7))), False)); state["events"].append("portal kick: " + m.group(1))
        elif "WALK hot spot" in l: state["events"].append("hot spot: training harder")
        elif "WALK LEARNED" in l:
            state["flash"] = (l.split("WALK LEARNED", 1)[-1].strip()[:70], time.time() + 8)
        elif "UNSTICK learned" in l:
            if state["kicks"]: k = state["kicks"].pop(); state["kicks"].append((k[0], k[1], True))
            state["events"].append("learned: " + l.split("learned:")[-1].strip()[:50])
        elif "WALK skip waypoint" in l: state["events"].append("gave up a waypoint")
        elif "SLING #" in l: state["events"].append("slung by a hit!")
        elif "WALK stuck" in l: state["events"].append("stuck " + (re.search(r"stuck (\d+)", l) or [0, "?"])[1])
class App:
    def __init__(self):
        self.r = tk.Tk(className="walker-mind"); self.r.title("Walker Mind"); self.r.geometry(f"{W}x{H}+1280+720"); self.r.attributes("-topmost", True); self.r.attributes("-type", "utility")
        self.c = tk.Canvas(self.r, width=W, height=H, bg=BG, highlightthickness=0); self.c.pack(fill="both", expand=True)
        self.r.configure(bg=BG); self.c.bind("<Configure>", self.resize); self.tick()
    def resize(self, e):
        """the drawing area follows the window (no white strip when the window is resized by hand)"""
        global W, H, SCALE
        if e.width > 100 and e.height > 100: W, H = e.width, e.height; SCALE = max(3.2, min(W, H - 36) / 125.0)      # a bigger window shows the same ~125 m across, bigger
    def px(self, x, z, ox, oz): return W / 2 + (x - ox) * SCALE, H / 2 - 18 - (z - oz) * SCALE      # north (+z) up
    def tick(self):
        c = self.c; c.delete("all"); s = status()
        game_up = bool(os.popen("pgrep -f '[x]rEngine.exe' | head -1").read().strip())
        if not game_up and "--keep" not in os.sys.argv:                                  # --keep (default setup): stay open as a window of the 3-window layout
            state["gone"] = state["gone"] or time.time()
            if time.time() - state["gone"] > 30: self.r.destroy(); return
        else: state["gone"] = None
        if s and not game_up:                                                              # game closed: keep drawing the LAST known state (dimmed label), not a blank window
            state["last_seen"] = True
        else: state["last_seen"] = False
        if not s:
            c.create_text(W / 2, H / 2 - 10, text="WALKER MIND", fill=RING, font=("monospace", 16, "bold"))
            c.create_text(W / 2, H / 2 + 14, text="waiting for the auto walker (starts with the game)", fill=TXT, font=("monospace", 10)); self.r.after(1000, self.tick); return
        x, z = float(s["x"]), float(s["z"]); lvl = s.get("level"); load_route(); read_log()
        if lvl != state["lvl"]: state["lvl"] = lvl; trail.clear(); state["kicks"].clear(); state["hot_mt"] = 0
        load_hot(lvl)
        if not trail or (x - trail[-1][0]) ** 2 + (z - trail[-1][1]) ** 2 > 0.04: trail.append((x, z))
        ox, oz = x, z
        for g in range(-12, 13):                                                         # wireframe grid, 10 m
            gx = (math.floor(ox / 10) + g) * 10; gz = (math.floor(oz / 10) + g) * 10
            a, b = self.px(gx, oz - 60, ox, oz), self.px(gx, oz + 60, ox, oz); c.create_line(a[0], a[1], b[0], b[1], fill=GRID)
            a, b = self.px(ox - 100, gz, ox, oz), self.px(ox + 100, gz, ox, oz); c.create_line(a[0], a[1], b[0], b[1], fill=GRID)
        ph = map_photo(lvl, ox, oz)
        if ph is not None: self.ph = ph; c.create_image(0, 0, image=ph, anchor="nw")        # the game's own top-down map under everything
        ex = explored(lvl, x, z)                                                          # walked-before ground (dim tiles)
        cx0, cz0 = int(ox // 2), int(oz // 2)
        for ix in range(cx0 - 50, cx0 + 51):
            for iz in range(cz0 - 32, cz0 + 33):
                if (ix, iz) in ex:
                    a = self.px(ix * 2, iz * 2 + 2, ox, oz); c.create_rectangle(a[0], a[1], a[0] + 2 * SCALE, a[1] + 2 * SCALE, fill="#13222e", outline="", stipple="gray50")
        for r in (10, 25, 50):
            cx, cy = self.px(ox, oz, ox, oz); c.create_oval(cx - r * SCALE, cy - r * SCALE, cx + r * SCALE, cy + r * SCALE, outline=RING)
            c.create_text(cx + r * SCALE * 0.71, cy - r * SCALE * 0.71, text=f"{r}m", fill=RING, font=("monospace", 7))
        for (hx, hz), n in state["hot"].items():                                          # hot stuck cells
            a = self.px(hx - 3, hz + 3, ox, oz); b = self.px(hx + 3, hz - 3, ox, oz)
            solved = (hx, hz) in state.get("solved", ())      # LEARNED: green = a way through was found here, red = still beating it
            col = "#43d17a" if solved else HOT
            c.create_rectangle(a[0], a[1], b[0], b[1], outline=col, width=2 if n > 2 else 1); c.create_text(a[0] + 9, a[1] + 8, text=("OK " if solved else "") + str(n), fill=col, font=("monospace", 8, "bold"))
        pts = state["route"]; wp = s.get("wp", "1/1").split("/")[0]; wp = int(wp) if wp.isdigit() else 1
        if len(pts) > 1: c.create_line(*[v for p in pts for v in self.px(p[0], p[1], ox, oz)], fill=ROUTE)
        for i, p in enumerate(pts):
            a = self.px(p[0], p[1], ox, oz); c.create_oval(a[0] - 2, a[1] - 2, a[0] + 2, a[1] + 2, fill=WP, outline="")
        if 1 <= wp <= len(pts):
            t = pts[wp - 1]; a = self.px(t[0], t[1], ox, oz); me = self.px(x, z, ox, oz)
            c.create_line(me[0], me[1], a[0], a[1], fill=CUR, dash=(4, 3)); c.create_oval(a[0] - 7, a[1] - 7, a[0] + 7, a[1] + 7, outline=CUR, width=2)
        for (p, q, won) in state["kicks"]:                                                      # portal kicks
            a, b = self.px(p[0], p[1], ox, oz), self.px(q[0], q[1], ox, oz); c.create_line(a[0], a[1], b[0], b[1], fill="#43d17a" if won else KICK, arrow=tk.LAST, width=2)
        for kind, wx, wz, extra in read_world():                                           # the world around him
            a = self.px(wx, wz, ox, oz)
            if not (0 <= a[0] <= W and 0 <= a[1] <= H - 36): continue
            if kind == "Z":
                rr = float(extra[0]) * SCALE if extra else 8; c.create_oval(a[0] - rr, a[1] - rr, a[0] + rr, a[1] + rr, outline="#b77cff", fill="#2a1840", stipple="gray25"); c.create_text(a[0], a[1], text="Z", fill="#b77cff", font=("monospace", 7))
            elif kind == "A": c.create_polygon(a[0], a[1] - 6, a[0] + 5, a[1], a[0], a[1] + 6, a[0] - 5, a[1], fill="#4cf0e0", outline="")
            elif kind == "I": c.create_rectangle(a[0] - 2, a[1] - 2, a[0] + 2, a[1] + 2, fill="#ffd166", outline="")
            elif kind in "EM": c.create_polygon(a[0], a[1] - 6, a[0] + 6, a[1] + 5, a[0] - 6, a[1] + 5, fill="#ef476f" if kind == "E" else "#a4133c", outline="white")
            elif kind == "F": c.create_oval(a[0] - 5, a[1] - 5, a[0] + 5, a[1] + 5, fill="#43d17a", outline="white")
            elif kind == "C":                                                                  # Aisha: the cat emote (falls back to a drawn cat if the icon file is missing)
                if getattr(self, "cat_ph", None) is None:
                    ci = cat_icon(34); self.cat_ph = ImageTk.PhotoImage(ci) if ci else False
                if self.cat_ph: c.create_image(a[0], a[1] - 4, image=self.cat_ph)
                else: c.create_oval(a[0] - 7, a[1] - 7, a[0] + 7, a[1] + 6, fill="#f4ede4", outline="white")
                c.create_text(a[0], a[1] + 18, text="Aisha", fill="#ffd9a8", font=("monospace", 7, "bold"))
            elif kind == "N": c.create_oval(a[0] - 4, a[1] - 4, a[0] + 4, a[1] + 4, fill="#8a99a8", outline="")
        n = len(trail)                                                                     # PAST: the trail fades from dim (old) to bright (just now)
        for i in range(1, n, 1):
            f = i / n; col = "#%02x%02x%02x" % (int(30 + 46 * f), int(70 + 130 * f), int(110 + 130 * f))
            a, b = self.px(trail[i - 1][0], trail[i - 1][1], ox, oz), self.px(trail[i][0], trail[i][1], ox, oz); c.create_line(a[0], a[1], b[0], b[1], fill=col, width=1 + int(f * 2))
        me = self.px(x, z, ox, oz)
        if len(trail) > 5:
            dx, dz = x - trail[-5][0], z - trail[-5][1]; n = math.hypot(dx, dz) or 1
            c.create_line(me[0], me[1], me[0] + dx / n * 22, me[1] - dz / n * 22, fill=ME, arrow=tk.LAST, width=2)
        c.create_oval(me[0] - 4, me[1] - 4, me[0] + 4, me[1] + 4, fill=ME, outline="white")
        want = {"fwd": "walking forward", "turn": "turning towards the target", "strafe": "side-stepping round a snag"}.get(s.get("want", ""), s.get("want", "?"))
        mood = "STUCK x" + s["stuck"] if s.get("stuck", "0") != "0" else ("DANGER: %s hostiles" % s["hostile30"] if s.get("hostile30", "0") != "0" else "calm")
        c.create_rectangle(0, H - 36, W, H, fill="#070a0e", outline="")
        c.create_text(6, H - 28, anchor="w", text=f"{lvl}  wp {s.get('wp')}  dist {s.get('dist')} m  {want}", fill=TXT, font=("monospace", 8))
        c.create_text(6, H - 15, anchor="w", text=f"speed {s.get('speed')}  fps {s.get('fps')}  {mood}   | {' > '.join(list(state['events'])[-2:])}", fill=HOT if "STUCK" in mood else TXT, font=("monospace", 8))
        fl = state.get("flash")
        if fl and time.time() < fl[1]:                                                       # a flashing green banner for 8 s: it learned something new
            on = int(time.time() * 3) % 2 == 0
            c.create_rectangle(2, 20, W - 2, 46, fill="#0c3b22" if on else "#10532f", outline="#43d17a", width=2)
            c.create_text(W / 2, 33, text="LEARNED  " + fl[0], fill="#b9ffd4", font=("monospace", 10, "bold"))
        c.create_text(W - 6, 8, anchor="e", text="WALKER MIND" + ("  (game closed: last seen)" if state.get("last_seen") else ""), fill=RING, font=("monospace", 8, "bold"))
        c.create_text(6, 8, anchor="w", text="NOW", fill=CUR, font=("monospace", 7, "bold")); c.create_text(34, 8, anchor="w", text="PAST", fill="#4a9fd0", font=("monospace", 7, "bold"))
        c.create_text(68, 8, anchor="w", text="LEARNED", fill="#43d17a", font=("monospace", 7, "bold")); c.create_text(124, 8, anchor="w", text="STUCK", fill=HOT, font=("monospace", 7, "bold"))
        c.create_text(168, 8, anchor="w", text="E enemy  F ally  N neutral  Aisha = cat  Z anomaly  A artifact  I item", fill="#6f7f90", font=("monospace", 7))
        self.r.after(500, self.tick)
if __name__ == "__main__":
    if os.popen("pgrep -f '^python3 .*walker_mind.py' | grep -vx %d | head -1" % os.getpid()).read().strip(): raise SystemExit(0)
    App().r.mainloop()

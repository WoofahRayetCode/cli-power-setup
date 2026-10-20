#!/usr/bin/env python3
"""Server-side picture of the Walker Mind window (for the phone app's "Mind" tab): the same data as tools/walker_mind.py (map of the level, walked ground, hot stuck cells, route, trail,
entities around him, Aisha, kicks) drawn offscreen with PIL, no display needed.   render(w, h) -> PNG bytes"""
import io, math, re, sys, time
from collections import deque
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import walker_mind as wm
from PIL import Image, ImageDraw, ImageFont
trail = deque(maxlen=500); _last = {"lvl": None, "t": 0}
def sample():
    """call about once a second: remember where he has been"""
    s = wm.status()
    if not s: return None
    x, z = float(s["x"]), float(s["z"])
    if s.get("level") != _last["lvl"]: trail.clear(); _last["lvl"] = s.get("level")
    if not trail or (x - trail[-1][0]) ** 2 + (z - trail[-1][1]) ** 2 > 0.04: trail.append((x, z))
    return s
def render(W=720, H=720):
    s = sample()
    im = Image.new("RGB", (W, H), (11, 15, 20)); d = ImageDraw.Draw(im)
    try: f8 = ImageFont.load_default(size=14); f10 = ImageFont.load_default(size=18)
    except TypeError: f8 = f10 = ImageFont.load_default()
    if not s:
        d.text((W // 2 - 140, H // 2), "walker idle: no game running", fill=(200, 211, 223), font=f10); b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()
    x, z = float(s["x"]), float(s["z"]); lvl = s.get("level"); SC = max(3.2, min(W, H - 60) / 125.0)
    ox, oz = x, z; cy0 = H / 2 - 30
    def px(a, b): return W / 2 + (a - ox) * SC, cy0 - (b - oz) * SC
    m = wm.level_map(lvl)
    if m:
        mi, (x1, z1, x2, z2) = m; ppx, ppz = mi.width / (x2 - x1), mi.height / (z2 - z1)
        left, right = ox - W / 2 / SC, ox + W / 2 / SC; top, bottom = oz + cy0 / SC, oz - (H - cy0) / SC
        box = ((left - x1) * ppx, (z2 - top) * ppz, (right - x1) * ppx, (z2 - bottom) * ppz)
        try: im = mi.transform((W, H), Image.AFFINE, ((box[2] - box[0]) / W, 0, box[0], 0, (box[3] - box[1]) / H, box[1]), Image.BILINEAR, fillcolor=(11, 15, 20)); d = ImageDraw.Draw(im)
        except Exception: pass
    for g in range(-14, 15):
        gx = (math.floor(ox / 10) + g) * 10; a, b = px(gx, oz - 90), px(gx, oz + 90); d.line([a, b], fill=(24, 36, 48))
        gz = (math.floor(oz / 10) + g) * 10; a, b = px(ox - 120, gz), px(ox + 120, gz); d.line([a, b], fill=(24, 36, 48))
    for r in (10, 25, 50):
        cx, cy = px(ox, oz); d.ellipse([cx - r * SC, cy - r * SC, cx + r * SC, cy + r * SC], outline=(34, 54, 74)); d.text((cx + r * SC * .71, cy - r * SC * .71), f"{r}m", fill=(60, 90, 120), font=f8)
    wm.load_hot(lvl)
    for (hx, hz), n in wm.state["hot"].items():
        a, b = px(hx - 3, hz + 3), px(hx + 3, hz - 3); solved = (hx, hz) in wm.state.get("solved", ()); col = (67, 209, 122) if solved else (239, 71, 111)
        d.rectangle([a, b], outline=col, width=2); d.text((a[0] + 4, a[1] + 2), ("OK " if solved else "") + str(n), fill=col, font=f8)
    wm.load_route(); pts = wm.state["route"]; wp = s.get("wp", "1/1").split("/")[0]; wp = int(wp) if wp.isdigit() else 1
    if len(pts) > 1: d.line([px(p[0], p[1]) for p in pts], fill=(47, 158, 110), width=1)
    n = len(trail)
    for i in range(1, n):
        f = i / n; d.line([px(*trail[i - 1]), px(*trail[i])], fill=(int(30 + 46 * f), int(70 + 130 * f), int(110 + 130 * f)), width=1 + int(f * 2))
    for kind, wx, wz, extra in wm.read_world():
        a = px(wx, wz)
        if not (0 <= a[0] <= W and 0 <= a[1] <= H): continue
        if kind == "Z": rr = (float(extra[0]) if extra else 3) * SC; d.ellipse([a[0] - rr, a[1] - rr, a[0] + rr, a[1] + rr], outline=(183, 124, 255), width=2)
        elif kind == "A": d.polygon([(a[0], a[1] - 7), (a[0] + 6, a[1]), (a[0], a[1] + 7), (a[0] - 6, a[1])], fill=(76, 240, 224))
        elif kind == "I": d.rectangle([a[0] - 2, a[1] - 2, a[0] + 2, a[1] + 2], fill=(255, 209, 102))
        elif kind in "EM": d.polygon([(a[0], a[1] - 7), (a[0] + 7, a[1] + 6), (a[0] - 7, a[1] + 6)], fill=(239, 71, 111) if kind == "E" else (164, 19, 60), outline=(255, 255, 255))
        elif kind == "F": d.ellipse([a[0] - 6, a[1] - 6, a[0] + 6, a[1] + 6], fill=(67, 209, 122), outline=(255, 255, 255))
        elif kind == "N": d.ellipse([a[0] - 4, a[1] - 4, a[0] + 4, a[1] + 4], fill=(138, 153, 168))
        elif kind == "C":
            ci = wm.cat_icon(40)
            if ci: im.paste(ci, (int(a[0] - ci.width / 2), int(a[1] - ci.height / 2 - 4)), ci)
            else: d.ellipse([a[0] - 8, a[1] - 8, a[0] + 8, a[1] + 7], fill=(244, 237, 228), outline=(255, 255, 255))
            d.text((a[0] - 14, a[1] + 14), "Aisha", fill=(255, 217, 168), font=f8)
    if 1 <= wp <= len(pts):
        t = pts[wp - 1]; a = px(t[0], t[1]); me = px(x, z); d.line([me, a], fill=(255, 209, 102), width=2); d.ellipse([a[0] - 8, a[1] - 8, a[0] + 8, a[1] + 8], outline=(255, 209, 102), width=3)
    me = px(x, z)
    if len(trail) > 5:
        dx, dz = x - trail[-5][0], z - trail[-5][1]; nn = math.hypot(dx, dz) or 1; d.line([me, (me[0] + dx / nn * 26, me[1] - dz / nn * 26)], fill=(76, 201, 240), width=3)
    d.ellipse([me[0] - 5, me[1] - 5, me[0] + 5, me[1] + 5], fill=(76, 201, 240), outline=(255, 255, 255))
    d.rectangle([0, H - 52, W, H], fill=(7, 10, 14))
    want = {"fwd": "walking forward", "turn": "turning towards the target", "strafe": "side-stepping round a snag"}.get(s.get("want", ""), s.get("want", "?"))
    mood = "STUCK x" + s["stuck"] if s.get("stuck", "0") != "0" else ("DANGER: %s hostiles" % s["hostile30"] if s.get("hostile30", "0") != "0" else "calm")
    d.text((8, H - 48), f"{lvl}  wp {s.get('wp')}  dist {s.get('dist')} m  {want}", fill=(200, 211, 223), font=f8)
    d.text((8, H - 26), f"speed {s.get('speed')}  fps {s.get('fps')}  {mood}", fill=(239, 71, 111) if "STUCK" in mood else (200, 211, 223), font=f8)
    age = time.time() - (wm.LOGS / "walk_status.txt").stat().st_mtime if (wm.LOGS / "walk_status.txt").exists() else 999
    if age > 15: d.text((W - 230, 8), f"last seen {int(age // 60)} min ago (game closed)", fill=(255, 209, 102), font=f8)
    b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()
if __name__ == "__main__":
    Path("/tmp/mind_render.png").write_bytes(render(720, 720)); print("wrote /tmp/mind_render.png")

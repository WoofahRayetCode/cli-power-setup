#!/usr/bin/env python3
"""Ops log: one live feed of what the helpers and tests are doing (guardian, work log, walker learned/stuck, needs-you, model-test results, Discord/phone messages). Newest at the bottom.
Run in its own terminal (the dual-screen layout opens it top-right of the main screen)."""
import glob, json, os, re, time
from pathlib import Path
here = Path(__file__).resolve().parent.parent
C = {"g": "\x1b[32m", "y": "\x1b[33m", "r": "\x1b[31m", "c": "\x1b[36m", "m": "\x1b[35m", "d": "\x1b[2m", "0": "\x1b[0m"}
SRC = [("guardian", here / ".agents/guardian.log", "y"), ("work", here / "docs/WORK_LOG.md", "c"), ("tests", here / "docs/learn/model_eval_hard.jsonl", "m"), ("needs", here / ".agents/needs_you.txt", "r"),
       ("agenda", here / ".agents/agenda.txt", "g")]
pos = {}
os.system('stty -echo 2>/dev/null')            # keys pressed while this window has focus must not be echoed into the feed
def fresh(p, first):
    try: size = p.stat().st_size
    except OSError: return []
    if p not in pos: pos[p] = max(0, size - first)
    if size < pos[p]: pos[p] = 0
    with open(p, "rb") as f: f.seek(pos[p]); data = f.read().decode("utf-8", "ignore"); pos[p] = f.tell()
    return [l for l in data.splitlines() if l.strip()]
def fmt(tag, color, l):
    if tag == "tests":
        try: r = json.loads(l); return f"{r['model'].split('/')[-1][:24]} {r['kind']} {'pass' if r['ok'] else 'FAIL'} {r['sec']:.0f}s"
        except Exception: pass
    return re.sub(r"\s+", " ", l)[:200]
def xray_learned():
    fs = sorted(glob.glob(str(here / "_appdata_/logs/xray_*.log")), key=os.path.getmtime)
    return [l for l in fresh(Path(fs[-1]), 0) if "WALK LEARNED" in l or "WALK skip" in l] if fs else []
first = True
while True:
    out = []
    for tag, p, col in SRC:
        for l in fresh(p, 600 if first else 0)[-6 if first else None:]: out.append((tag, col, fmt(tag, col, l)))
    for l in xray_learned(): out.append(("walker", "g", re.sub(r"\s+", " ", l.split("WALK", 1)[-1])[:200]))
    for tag, col, text in out: print(f"{C['d']}{time.strftime('%H:%M')}{C['0']} {C[col]}{tag:8}{C['0']} {text}", flush=True)
    first = False; time.sleep(3)

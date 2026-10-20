#!/usr/bin/env python3
"""One-block summary for the status window: NVIDIA model downloads and the model tests (docs/learn/model_eval_hard.jsonl). Prints plain lines (no colours)."""
import json, re, subprocess
from collections import defaultdict
from pathlib import Path
here = Path(__file__).resolve().parent.parent
def sh(c):
    try: return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=8, cwd=here).stdout
    except Exception: return ""
NV = ("nemotron", "OpenReasoning")
have = [l.split() for l in sh("ollama list").splitlines()[1:] if any(k.lower() in l.lower() for k in NV)]
out = []
pulling = sh("ps -eo args | grep -E '^ollama pull ' | head -3").strip()      # the real pull processes (exact), not any shell that mentions the words
cur_pull = [l.split()[2] for l in pulling.splitlines() if len(l.split()) >= 3][:1]
prog = ""
queue_names = []
for f in sorted((Path.home() / ".cache/bgrun").glob("pull*.log"), key=lambda p: p.stat().st_mtime)[-1:]:
    txt = f.read_text(errors="ignore")[-3000:].replace("\r", "\n")
    m = re.findall(r"pulling \w+:\s+(\d+)%[^\n]*?([\d.]+ [GM]B/\s*[\d.]+ [GM]B)\s+([\d.]+ [MK]B/s)?", txt)
    if m and pulling: prog = " %s%% %s" % (m[-1][0], m[-1][1].replace(" ", "")) + (" at " + m[-1][2] if m[-1][2] else "")
cmdline = sh("ps -eo args | grep -E '^bash -c .*ollama pull' | grep -v grep | head -1")
names = re.findall(r"ollama pull ([\w./:-]+)", cmdline)
if cur_pull and cur_pull[0] in names: queue_names = names[names.index(cur_pull[0]) + 1:]
out.append("models installed: %d NVIDIA" % len(have) + (("   DOWNLOADING: " + cur_pull[0] + prog + (("  (then " + ", ".join(queue_names) + ")") if queue_names else "")) if cur_pull else "   no download running"))
rows = []
try: rows = [json.loads(l) for l in (here / "docs/learn/model_eval_hard.jsonl").read_text().splitlines() if l.strip()]
except Exception: pass
PLAN = {"math": 6 * 11, "code": 5 * 11, "vision": 3 * 4}
by = defaultdict(lambda: [0, 0])
for r in rows: by[r["kind"]][1] += 1; by[r["kind"]][0] += r["ok"]
done = sum(min(v[1], PLAN.get(k, 0)) for k, v in by.items()); total = sum(PLAN.values())
run = sh("pgrep -fa 'model_eval_hard.py' | grep -v pgrep | head -1").strip()
stage = (re.search(r"model_eval_hard.py (\w+)", run) or [0, "idle"])[1] if run else ("finished" if done >= total else "idle")
out.append(f"tests: {done}/{total} checks, stage {stage}  " + "  ".join(f"{k} {v[0]}/{v[1]}" for k, v in sorted(by.items())))
if rows:
    best = defaultdict(lambda: [0, 0])
    for r in rows: best[r["model"]][1] += 1; best[r["model"]][0] += r["ok"]
    top = sorted(best.items(), key=lambda kv: -kv[1][0] / max(1, kv[1][1]))[:3]
    out.append("best so far: " + ", ".join(f"{m.split('/')[-1][:22]} {v[0]}/{v[1]}" for m, v in top))
# what is being worked on right now
loaded = [l.split()[0] for l in sh("ollama ps").splitlines()[1:] if l.strip()]
cur = ""
if run:
    stage = (re.search(r"model_eval_hard.py (\w+)", run) or [0, "?"])[1]
    last = rows[-1] if rows else None
    if last: cur = f"now: {stage} test, last result {last['model'].split('/')[-1][:24]} ({'pass' if last['ok'] else 'fail'}, {last['sec']:.0f}s)"
    else: cur = f"now: {stage} test starting"
    if loaded: cur += f"; on the GPU: {loaded[0].split('/')[-1][:26]}"
elif cur_pull: cur = "now: downloading " + cur_pull[0]
elif done >= total: cur = "now: all tests finished: deciding keep/replace/remove"
else: cur = "now: waiting for the next test stage"
nxt = {"math": "this model's code test, then the next big model", "code": "the next big model, then the keep/remove decisions", "vision": "the big-model round", "finished": "README + skills update"}.get(stage, "")
out.insert(1, cur + (f"  | next: {nxt}" if nxt else ""))
def bar(n, d, w=14): f = 0 if d <= 0 else min(w, int(round(w * n / d))); return "▰" * f + "▱" * (w - f)
# progress bars: the current ROUND (the models listed in the running queue script) and the model being tested right now
round_models = []
for q in sorted((here / ".agents").glob("eval_*.sh"), key=lambda p: p.stat().st_mtime)[-1:]:
    txt = q.read_text(); m = re.search(r"for m in ([^;]+); do", txt)
    round_models = m.group(1).split() if m else re.findall(r"model_eval_hard.py (?:math|code|vision) ((?:[\w./:-]+ ?)+)", txt)[0].split() if re.search(r"model_eval_hard.py", txt) else []
if run and round_models:
    PER = {"math": 6, "code": 5, "vision": 3}
    want = {(k, m) for m in round_models for k in ("math", "code")} if "for m in" in (q.read_text() if round_models else "") else {(stage, m) for m in round_models}
    got = {(r["kind"], r["model"]) for r in rows}; cnt = defaultdict(int)
    for r in rows: cnt[(r["kind"], r["model"])] += 1
    tot = sum(PER[k] for k, m in want); dn = sum(min(PER[k], cnt[(k, m)]) for k, m in want)
    cm = rows[-1]["model"] if rows else ""; ck = stage if stage in PER else "math"
    # ETA: remaining tasks x the model's own average seconds per task (an unstarted model uses the slowest average seen in this round)
    import time as _tm
    avg = {m: (sum(r["sec"] for r in rows if r["model"] == m) / max(1, sum(1 for r in rows if r["model"] == m))) for m in round_models if any(r["model"] == m for r in rows)}
    slow = max(avg.values()) if avg else 30.0
    left = sum(max(0, PER["math"] - cnt[("math", m)]) * avg.get(m, slow) + max(0, PER["code"] - cnt[("code", m)]) * avg.get(m, slow) for m in round_models)
    eta = f"  ETA ~{int(left // 60)} min (done ~{_tm.strftime('%H:%M', _tm.localtime(_tm.time() + left))})" if dn < tot else "  done"
    out.insert(2, f"round {bar(dn, tot)} {dn}/{tot} {100 * dn // max(1, tot)}%{eta}")
    # the task being worked on right now = the first task of this stage that has no result yet for this model
    try:
        import sys as _s, time as _t; _s.path.insert(0, str(here / "tools")); import model_eval_hard as meh
        tasks = [d for d, _ in meh.CODE] if ck == "code" else [q for q, _ in meh.MATH] if ck == "math" else []
        have = {r["task"] for r in rows if r["model"] == cm and r["kind"] == ck}
        nxt_i = next((i for i, d in enumerate(tasks) if d[:60] not in have), None)
        if nxt_i is None and tasks: nxt_i = len(tasks) - 1
        age = int(_t.time() - (here / "docs/learn/model_eval_hard.jsonl").stat().st_mtime)
        if tasks: out.insert(4 if cm else 3, f"task {nxt_i + 1}/{len(tasks)}: {tasks[nxt_i][:70]} (working {age // 60}:{age % 60:02d})")
    except Exception: pass
    # the pipeline: every model of the round with its state, then what follows
    def state_of(m):
        n = sum(cnt[(k, m)] for k in ("math", "code"))
        return "✔" if n >= PER["math"] + PER["code"] else "▶" if m == cm and run else ("◐" if n else "○")
    out.append("pipeline: " + "  ".join(f"{state_of(m)} {m.split('/')[-1][:18]}" for m in round_models) + "  → keep/remove decisions → README + skills")
    if cm: out.insert(3, f"{cm.split('/')[-1][:22]} {ck} {bar(min(PER[ck], cnt[(ck, cm)]), PER[ck], 8)} {min(PER[ck], cnt[(ck, cm)])}/{PER[ck]}")
def _rank(l):
    return 0 if l.startswith("models installed") else 1 if l.startswith("now:") else 2 if l.startswith("round") else 3 if re.search(r" (math|code|vision) ▰", l) else 4 if l.startswith("task ") else 5 if l.startswith("pipeline:") else 5.5 if l.startswith("tests:") else 6
print("\n".join(sorted(out, key=_rank)))

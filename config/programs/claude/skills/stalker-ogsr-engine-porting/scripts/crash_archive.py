#!/usr/bin/env python3
"""Archive a crash as one folder with a name, a description and the save files to reproduce it.
Called by tools/crash_shot.sh after the Wine crash window was read and closed (autoplay, level_smoke, bench and the general
crash watcher in play.sh all go through it). Each crash -> docs/crashes/<date_time>_<level>_<slug>/ with:
  README.md   name (level + short cause), description (what was happening: task, position, last walker events, last log lines),
              the fatal expression / description / location, and the exact command that loads the matching save
  engine.log  the full engine log of the crashed session, triage.json (from xray_crash_handler.py), crash_*.png (the dialog)
  saves/      the newest crash-point and campaign/autosave .sav files written before the crash (+ their .dds thumbnails if any)
  walk/       walk_status.txt / last_run.json when the auto walker was running
docs/crashes/INDEX.md gets one line per crash (newest last). Same crash signature twice -> the README of the first gets a 'seen again' line.
usage: crash_archive.py [--note "free text"]"""
import glob, json, os, re, shutil, sys, time
from pathlib import Path
here = Path(__file__).resolve().parent.parent
logs = here / "_appdata_/logs"; saves = here / "_appdata_/savedgames"; out_root = here / "docs/crashes"; out_root.mkdir(parents=True, exist_ok=True)
note = sys.argv[sys.argv.index("--note") + 1] if "--note" in sys.argv else ""
def newest(pattern, n=1, within=None):
    fs = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    if within: fs = [f for f in fs if time.time() - os.path.getmtime(f) < within]
    return fs[:n]
log = (newest(str(logs / "xray_*.log")) or [None])[0]
if not log: sys.exit("no engine log")
text = open(log, errors="replace").read()
lines = text.splitlines()
# crash facts: triage json written by the sweep (last 2 min), else parse the log tail ourselves
tri = {}
tj = newest(str(logs / "crash_triage_*.json"), within=180) + newest("/tmp/xray_triage/crash_triage_*.json", within=180)
if tj:
    try: tri = json.load(open(tj[0]))
    except Exception: tri = {}
def find(pat):
    for l in reversed(lines[-400:]):
        m = re.search(pat, l)
        if m: return m.group(1).strip()
    return ""
expr = tri.get("expression") or find(r"Expression\s*:\s*(.*)")
desc = tri.get("description") or find(r"Description\s*:\s*(.*)") or find(r"(SCRIPT RUNTIME ERROR.*|LUA error.*)")
where = (f"{tri.get('file')}:{tri.get('line')}" if tri.get("file") else find(r"File\s*:\s*(.*)"))
func = tri.get("function") or find(r"Function\s*:\s*(.*)")
level = find(r"ACTORTRACE (\S+) ") or find(r"\* Loading .*?level\s+(\S+)") or "unknown"
pos = find(r"ACTORTRACE \S+ pos=([-\d.,]+)")
task = find(r"WALK campaign goal: (.*?) \[") or find(r"status.*route=(\S+)")
walk_tail = [l.split("] ", 2)[-1].strip() for l in lines if "! WALK" in l][-8:]
sig_src = (desc or expr or "unknown") + " " + where
slug = re.sub(r"[^a-z0-9]+", "-", sig_src.lower()).strip("-")[:48] or "crash"
stamp = time.strftime("%Y%m%d_%H%M%S", time.localtime(os.path.getmtime(log)))
name = f"{level} - {(desc or expr or 'crash')[:70]}"
# duplicate? (same slug seen before): add a 'seen again' line to the first folder and still keep this one's files
prev = sorted(p for p in out_root.glob(f"*_{slug}") if p.is_dir())
d = out_root / f"{stamp}_{level}_{slug}"; d.mkdir(exist_ok=True); (d / "saves").mkdir(exist_ok=True); (d / "walk").mkdir(exist_ok=True)
shutil.copy(log, d / "engine.log")
if tj: shutil.copy(tj[0], d / "triage.json")
for f in newest(str(here / "docs/crashes/crash_*.png"), 2, within=300): shutil.move(f, d / Path(f).name)
# saves: newest crash point, newest campaign milestone, newest autosave/quick (written before the crash)
picked = []
for pat in ("crashpoint_*.sav", "campaign_*.sav", "*autosave*.sav", "*.sav"):
    for f in newest(str(saves / pat), 2):
        if f not in picked and Path(f).name != "all.sav" and os.path.getmtime(f) <= os.path.getmtime(log) + 5: picked.append(f)   # all.sav is the engine's spawn snapshot, not a save
    if len(picked) >= 3: break
for f in picked[:3]:
    shutil.copy(f, d / "saves" / Path(f).name)
    thumb = Path(f).with_suffix(".dds")
    if thumb.exists(): shutil.copy(thumb, d / "saves" / thumb.name)
for f in ("walk_status.txt",):
    if (logs / f).exists(): shutil.copy(logs / f, d / "walk" / f)
if (here / "docs/walk/last_run.json").exists(): shutil.copy(here / "docs/walk/last_run.json", d / "walk/last_run.json")
best_save = Path(picked[0]).stem if picked else None
repro = (f"AUTOWALK_LOAD={best_save} tools/autowalk.sh - 300        # auto walker from the save\n"
         f"./play.sh -start \"server({best_save}/single/alife/load)\" client(localhost)   # play it yourself") if best_save else "(no save file was available)"
readme = f"""# {name}
- **When:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(log)))}   **Level:** {level}   **Position:** {pos or '?'}
- **Expression:** `{expr or '-'}`
- **Description:** {desc or '-'}
- **Location:** {where or '-'}   **Function:** {func or '-'}
- **What was happening:** {task or 'free play'}{(' - ' + note) if note else ''}
- **Signature folder:** `{d.name}`{(' (seen before: ' + prev[0].name + ')') if prev else ''}

## Reproduce
```
{repro}
```
Saves in `saves/` (newest first): {', '.join(Path(p).name for p in picked[:3]) or 'none'}

## Last walker events
{chr(10).join('- ' + l for l in walk_tail) or '- (walker not running)'}

## Last log lines
```
{chr(10).join(l[:160] for l in lines[-25:])}
```
"""
(d / "README.md").write_text(readme)
if prev:
    with (prev[0] / "README.md").open("a") as f: f.write(f"\n- seen again: {stamp} -> `{d.name}`\n")
idx = out_root / "INDEX.md"
if not idx.exists(): idx.write_text("# Crash index (newest last)\n| when | level | what | where | save | folder |\n|---|---|---|---|---|---|\n")
with idx.open("a") as f:
    f.write(f"| {stamp} | {level} | {(desc or expr or '-')[:60].replace('|', '/')} | {where[:50].replace('|', '/')} | {best_save or '-'} | `{d.name}` |\n")
print(f"crash archived: {d}  ({name})")

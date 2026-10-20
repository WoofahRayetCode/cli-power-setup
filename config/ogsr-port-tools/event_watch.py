#!/usr/bin/env python3
"""Event watcher for live reporting in the Claude chat: runs in the background, exits (printing what happened) as soon as something worth telling the user happens, waits 20 s after the
first event to collect related ones, then exits so Claude is woken up, reports, and starts it again.
Watches: NEEDS YOU changes, guardian recoveries/give-ups, walker "learned" lines, game crash windows, a REAL phone appearing on adb, the Discord token file, new Joplin inbox items,
second screen (un)plugged, a new Walker/test result summary line in the work log, agenda changes. Also exits after 55 min with "heartbeat" so Claude gives a status."""
import glob, json, os, re, subprocess, sys, time
from pathlib import Path
here = Path(__file__).resolve().parent.parent
def rd(p):
    try: return Path(p).read_text(errors="ignore")
    except Exception: return ""
def sh(c):
    try: return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=10, cwd=here).stdout.strip()
    except Exception: return ""
def snapshot():
    s = {}
    s["needs"] = rd(here / ".agents/needs_you.txt").strip()
    s["guardian"] = rd(here / ".agents/guardian.log").strip().splitlines()[-1:] 
    s["agenda"] = rd(here / ".agents/agenda.txt")
    s["worklog_n"] = len(rd(here / "docs/WORK_LOG.md").splitlines())
    s["phone"] = [l.split()[0] for l in sh("~/Android/Sdk/platform-tools/adb devices").splitlines()[1:] if l.strip() and not l.startswith("emulator")]
    s["discord"] = os.path.exists(os.path.expanduser("~/.config/stalker-discord/token"))
    s["screens"] = sh("kscreen-doctor -o | sed 's/\\x1b\\[[0-9;]*m//g' | grep -c '^\t enabled\\|^\tenabled'")
    s["inbox"] = len([l for l in rd(here / ".agents/queue.jsonl").splitlines() if '"status": "new"' in l or '"status": "queued"' in l])
    xs = sorted(glob.glob(str(here / "_appdata_/logs/xray_*.log")), key=os.path.getmtime)
    s["learned"] = sum(1 for l in rd(xs[-1]).splitlines() if "WALK LEARNED" in l or "UNSTICK learned" in l) if xs else 0
    s["crash"] = bool(sh("pgrep -f 'notepad.exe' | head -1")) 
    return s
def describe(a, b):
    out = []
    if a["needs"] != b["needs"]: out.append("NEEDS YOU changed: " + (b["needs"][:200] or "(cleared)"))
    if a["guardian"] != b["guardian"] and b["guardian"] and re.search(r"killing|stale|gave up|crash|failed|error|leaving|missing", b["guardian"][0]): out.append("guardian: " + b["guardian"][0][:200])
    if a["agenda"] != b["agenda"]: out.append("agenda changed")
    if a["phone"] != b["phone"]: out.append("phone on adb: " + (", ".join(b["phone"]) or "disconnected"))
    if a["discord"] != b["discord"]: out.append("Discord token " + ("added: the bot should start" if b["discord"] else "removed"))
    if a["screens"] != b["screens"]: out.append(f"screens enabled: {a['screens']} -> {b['screens']}")
    if b["inbox"] > a["inbox"]: out.append(f"{b['inbox'] - a['inbox']} new inbox request(s) (phone/Joplin)")
    if b["learned"] > a["learned"]: out.append(f"walker learned something new ({b['learned'] - a['learned']})")
    if b["crash"] and not a["crash"]: out.append("game crash window appeared (the guardian closes it)")
    if b["worklog_n"] > a["worklog_n"] + 3: out.append("several new work-log lines")
    return out
def main():
    base = snapshot(); t0 = time.time(); found = []; first = None
    while True:
        time.sleep(10); cur = snapshot(); ev = describe(base, cur)
        if ev:
            found += [e for e in ev if e not in found]; first = first or time.time(); base = cur
        if first and time.time() - first >= 20: print("EVENTS:\n- " + "\n- ".join(found)); return
        if time.time() - t0 > 55 * 60: print("HEARTBEAT: no events in 55 minutes.\n" + sh("python3 tools/nvidia_progress.py | head -3") + "\n" + rd(here / ".agents/task.txt")); return
main()

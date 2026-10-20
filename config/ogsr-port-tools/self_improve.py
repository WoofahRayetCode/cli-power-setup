#!/usr/bin/env python3
"""Self-improvement loop for the helpers (guardian, Joplin watchdog, status web, night walk, EE tests) and the local workers.
  failures.jsonl  (.agents/)  one line per recovery/failure: {t, who, why}   <- written by the guardian (allowed()) and by anything calling `self_improve.py note WHO WHY`
  self_improve.py run         (guardian: hourly) groups the last 24 h by (who, why); for each cause seen 3+ times a small local model proposes a diagnosis + fix idea
                              from that helper's own log tail; the result is appended once to .agents/lessons.md (dedup by key) and, for causes seen 6+ times, put on the
                              needs-you line so a human/Claude patches the code. Also runs `local-worker evolve` (lessons the workers read in every prompt).
  self_improve.py show        print lessons.md
Costs no cloud tokens (qwen2.5:7b on the local Ollama; falls back to a rule-based note)."""
import json, subprocess, sys, time, urllib.request
from collections import Counter
from pathlib import Path
here = Path(__file__).resolve().parent.parent; F = here / ".agents/failures.jsonl"; LES = here / ".agents/lessons.md"
LOGS = {"joplin_watchdog": ".agents/joplin_start.out", "statusweb": ".agents/job_statusweb.log", "sysguard": ".agents/sysguard.out", "nightwalk": ".agents/job_nightwalk.log", "autosend": ".agents/guardian.log", "frozen": ".agents/guardian.log", "ee_session": ".agents/guardian.log"}
def ctx():
    """facts that usually explain a failure: load, free RAM, display env, game running, how long the machine has been up, newest kernel/user-journal error line"""
    import os
    def sh(c):
        try: return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=8).stdout.strip()
        except Exception: return ""
    return {"load": os.getloadavg()[0], "mem_avail_gb": round(int([l for l in open("/proc/meminfo") if l.startswith("MemAvailable")][0].split()[1]) / 1048576, 1), "uptime_s": int(float(open("/proc/uptime").read().split()[0])),
            "wayland": os.environ.get("WAYLAND_DISPLAY"), "live_sockets": sh("ls /run/user/%d | grep -E '^wayland-[0-9]$' | tr '\\n' ' '" % os.getuid()), "game": bool(sh("pgrep -f '[x]rEngine.exe'")),
            "last_err": sh("journalctl --user -p err -n 1 --no-pager -o cat")[:160]}
def note(who, why, log=None):
    with open(F, "a") as f: f.write(json.dumps({"t": time.time(), "who": who, "why": str(why)[:160], "ctx": ctx(), "log_tail": (tail(log or LOGS.get(who, ".agents/guardian.log"), 400))}) + "\n")
def tail(p, n=1800):
    try: return (here / p).read_text(errors="ignore")[-n:]
    except Exception: return ""
def ask(prompt):
    try:
        r = urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:11434/api/generate", json.dumps({"model": "qwen2.5:7b", "prompt": prompt, "stream": False, "options": {"num_ctx": 4096, "temperature": 0.1}}).encode(), {"Content-Type": "application/json"}), timeout=180)
        return json.load(r).get("response", "").strip()
    except Exception: return ""
def audit(rows):
    """Log-quality audit: a helper whose log is empty/stale while it is failing, or whose failures carry no log tail, is a LOGGING gap: write that as a lesson so the helper's logging gets fixed."""
    seen = Counter(r["who"] for r in rows if time.time() - r["t"] < 86400)
    known = LES.read_text() if LES.exists() else ""
    for who, n in seen.items():
        if n < 3: continue
        lp = here / LOGS.get(who, ".agents/guardian.log"); empty = [r for r in rows if r["who"] == who and not r.get("log_tail")]
        gap = (not lp.exists() and "its log file does not exist") or (lp.exists() and time.time() - lp.stat().st_mtime > 7200 and "its log has not been written for 2 h while it keeps failing") or (len(empty) >= n - 1 and "failure records carry no log tail")
        key = f"[logging-gap|{who}]"
        if gap and key not in known:
            with open(LES, "a") as f: f.write(f"\n## {key} {time.strftime('%F %H:%M')}\n{who}: {gap}. Fix: make the helper write what it was doing, the error text and exit code to {LOGS.get(who, 'a log')} before it exits.\n")
NEEDS = here / ".agents/needs_you.txt"; SEEN = here / ".agents/needs_seen.json"
HELPER_OF = (("joplin", "joplin_watchdog"), ("statusweb", "statusweb"), ("sysguard", "sysguard"), ("night walk", "nightwalk"), ("nightwalk", "nightwalk"), ("autosend", "autosend"), ("ee_session", "ee_session"), ("guardian", "guardian"))
def watch_needs():
    """Monitor the NEEDS YOU line: every new line is a helper that could not heal itself. Log it as a failure (so the 3x/6x rules and the diagnosis see it), get an immediate
    diagnosis from the local model into .agents/lessons.md, and keep an open-items list (.agents/needs_open.md) that Claude reads each turn to patch the helper's code."""
    try: seen = set(json.loads(SEEN.read_text()))
    except Exception: seen = set()
    try: lines = [l.strip() for l in NEEDS.read_text().splitlines() if l.strip()]
    except Exception: return
    new = [l for l in lines if l not in seen]
    for l in new:
        who = next((w for k, w in HELPER_OF if k in l.lower()), "needs_you")
        note(who, "NEEDS YOU: " + l)
        out = ask(f"A helper reported this on the needs-you line of a status screen: '{l}'.\nIts log tail:\n{tail(LOGS.get(who, '.agents/guardian.log'))}\nIn at most 3 lines: probable cause and the concrete code/config change that would make the helper fix this itself next time.") or "(no model: read the helper's log)"
        with open(LES, "a") as f: f.write(f"\n## [needs-you|{l[:60]}] {time.strftime('%F %H:%M')}\n{out}\n")
        with open(here / ".agents/needs_open.md", "a") as f: f.write(f"- [ ] {time.strftime('%F %H:%M')} {l}  -> {out.splitlines()[0] if out else ''}\n")
        seen.add(l)
    if new: SEEN.write_text(json.dumps(sorted(seen)[-200:]))
def run():
    rows = []
    try: rows = [json.loads(l) for l in F.read_text().splitlines()[-2000:]]
    except Exception: pass
    c = Counter((r["who"], r["why"]) for r in rows if time.time() - r["t"] < 86400)
    known = LES.read_text() if LES.exists() else ""
    for (who, why), n in c.most_common(6):
        key = f"[{who}|{why[:60]}]"
        if n < 3 or key in known: continue
        log = tail(LOGS.get(who, ".agents/guardian.log"))
        out = ask(f"A background helper '{who}' on a Linux/KDE Wayland desktop keeps failing ({n} times in 24 h), reason: {why}.\nContext at the latest failure: {json.dumps(next((r.get('ctx') for r in reversed(rows) if r['who'] == who), {}))}\nIts log tail:\n{log}\n\nIn at most 4 lines: the most likely root cause, then one concrete fix to the helper's code or environment. No preamble.") \
              or f"(no model) seen {n}x; check {LOGS.get(who, 'guardian.log')}"
        with open(LES, "a") as f: f.write(f"\n## {key} {time.strftime('%F %H:%M')} ({n}x)\n{out}\n")
        if n >= 6: (here / ".agents/needs_you.txt").open("a").write(f"Helper {who} keeps failing ({why[:50]}): diagnosis in .agents/lessons.md\n")
    audit(rows)
    subprocess.run("local-worker evolve", shell=True, capture_output=True, timeout=60)
if __name__ == "__main__":
    a = sys.argv[1:] or ["run"]
    if a[0] == "needs": watch_needs()
    elif a[0] == "note": note(a[1], " ".join(a[2:]))
    elif a[0] == "show": print(LES.read_text() if LES.exists() else "(no lessons yet)")
    else: run()

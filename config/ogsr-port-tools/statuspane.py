#!/usr/bin/env python3
"""Renderer for the dedicated status window: blocks in priority order, fitted to the window (rows x columns). When there is not enough room the LOWEST
priority blocks are shortened or dropped first, so NEEDS YOU / NOW / LOCAL WORKERS always stay visible. Costs no tokens: local files and local commands.
  priority: 1 needs-you  2 now  3 local workers (resources)  4 game / night walk  5 status line  6 ticker"""
import json, os, re, shutil, subprocess, sys, time, textwrap
from pathlib import Path
here = Path(__file__).resolve().parent.parent
C = {"h": "\x1b[1;36m", "y": "\x1b[1;33m", "m": "\x1b[1;35m", "g": "\x1b[1;32m", "d": "\x1b[2m", "0": "\x1b[0m"}
def sh(c, inp=None, t=8):
    try: return subprocess.run(c, shell=True, input=inp, capture_output=True, text=True, timeout=t).stdout
    except Exception: return ""
def rd(p): 
    try: return Path(p).read_text().strip()
    except Exception: return ""
def strip(s): return re.sub(r"\x1b\[[0-9;]*m", "", s)
def wrap(text, w, maxl=None):
    out = []
    for l in text.splitlines():
        out += textwrap.wrap(strip(l), w) or [""] if "\x1b" not in l else [l[:w + 40]]
    return out[:maxl] if maxl else out
def block(title, color, lines): return [f"{C[color]}{title}{C['0']}"] + lines
def statusline_input():
    """the REAL input Claude Code last sent the status command (quota, model, context), saved by claude-statusline; the made-up one below only when none exists / it is over 15 min old"""
    real = Path.home() / ".cache/claude-statusline/real_input.json"
    try:
        if time.time() - real.stat().st_mtime < 900:
            d = json.loads(real.read_text())
            if d.get("rate_limits") or d.get("model"): return json.dumps(d)
    except Exception: pass
    proj = Path.home() / ".claude/projects" / str(here).replace("/", "-")
    fs = sorted(proj.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    t = str(fs[0]) if fs else ""
    return json.dumps({"session_id": Path(t).stem, "transcript_path": t, "cwd": str(here), "model": {"id": "claude-sonnet-5-5", "display_name": "Sonnet 5.5"},
                       "workspace": {"current_dir": str(here), "project_dir": str(here)}, "cost": {"total_cost_usd": 0, "total_lines_added": 0, "total_lines_removed": 0, "total_duration_ms": 0}, "version": "2.1.302"})
def daypart(h=None):
    """name of the part of the day, for the window titles: morning 5-12, afternoon 12-17, evening 17-21, night 21-5"""
    h = time.localtime().tm_hour if h is None else h
    return "MORNING" if 5 <= h < 12 else "AFTERNOON" if 12 <= h < 17 else "EVENING" if 17 <= h < 21 else "NIGHT"
def compose(cols, rows):
    B = {}   # priority -> (full lines, minimal lines)
    B[1] = (block("NEEDS YOU", "y", wrap(rd(here / ".agents/needs_you.txt") or "Nothing right now.", cols)), None)
    now_txt = re.sub(r"^(overnight|tonight|night|morning|midday|afternoon|evening)\b", lambda m: daypart().lower(), rd(here / ".agents/task.txt") or "idle", flags=re.I)   # the leading time-of-day word always matches the clock
    B[2] = (block("NOW", "h", wrap(now_txt, cols, 4)), None)
    ag = [l.strip() for l in rd(here / ".agents/agenda.txt").splitlines() if l.strip() and not l.startswith("#")]
    inbox = []                                                          # newer tasks from the user that are still OPEN: Joplin inbox queue (status not done) + phone/Discord/web messages waiting to be typed in
    for f, key in ((here / ".agents/queue.jsonl", "text"), (Path.home() / ".cache/claude-autosend/remote_queue.jsonl", "text")):
        try:
            for l in rd(f).splitlines()[-30:]:
                r = json.loads(l)
                if r.get("status", "new") in ("new", "queued", "open", "") and r.get(key): inbox.append(re.sub(r"\s+", " ", r[key])[:90])
        except Exception: pass
    ag_lines = [f"{i + 1}. {t}" for i, t in enumerate(ag[:5])] + ([f"+{len(ag) - 5} more"] if len(ag) > 5 else []) + (["new from you:"] + [f"  - {t}" for t in inbox[-3:]] if inbox else [])
    if ag_lines: B[2.2] = (block("AGENDA", "y", sum([wrap(l, cols, 2) for l in ag_lines], [])), block("AGENDA", "y", [l[:cols] for l in ag_lines[:2]]))
    w = [l[:cols] for l in sh("local-worker status 2>/dev/null").splitlines()]
    B[3] = (block("LOCAL WORKERS", "m", w[:5]), block("LOCAL WORKERS", "m", w[:2]))
    wr = rd(here / ".agents/walker_report.md"); vd = re.search(r"Verdict: (.*)", wr); wl = re.search(r"Worst cells[^:]*: (.*)", wr)
    wlines = wrap(vd.group(1), cols, 3) + (wrap("worst: " + wl.group(1)[:90], cols, 2) if wl and wl.group(1).strip() else []) if vd else []
    if wlines: B[3.5] = (block("WALKER LEARNING", "g", wlines), block("WALKER LEARNING", "g", wlines[:2]))
    nv = [l[:cols] for l in sh("python3 tools/nvidia_progress.py 2>/dev/null").splitlines()]
    if nv: B[3.6] = (block("NVIDIA MODELS", "m", sum([wrap(l, cols, 3) for l in nv], [])), block("NVIDIA MODELS", "m", nv[:2]))
    night = sorted((here / "docs/night").glob("2*.md"))
    nl = [l[:cols] for l in rd(night[-1]).splitlines() if re.match(r"l\d\d", l)][-8:] if night else []
    gm = "game running" if sh("pgrep -f '[x]rEngine.exe -nointro'").strip() else "game closed"
    B[4] = (block(f"GAME / {daypart()} WALK", "g", [gm] + nl), block(f"GAME / {daypart()} WALK", "g", [gm] + nl[-2:]))
    sl = [l for l in sh("claude-statusline", statusline_input()).splitlines() if l.strip()]
    sl_w = sum([wrap(l, cols) if "\x1b" not in l else [l] for l in sl], [])
    B[2.5] = (block("STATUS LINE", "d", sl_w[:7]), block("STATUS LINE", "d", sl_w[:3]))     # quota stays visible: right after NOW
    tk = rd(Path.home() / ".claude/ticker.txt")
    B[6] = (block("TICKER", "d", wrap(tk, cols, 8)), block("TICKER", "d", wrap(tk, cols, 2)))
    budget, out, used = rows - 2, {}, 0
    for pri in sorted(B):                       # fill from the most important block down
        full, mini = B[pri]
        for cand in (full, mini):
            if cand and used + len(cand) + 1 <= budget: out[pri] = cand; used += len(cand) + 1; break
    NEED["lines"] = 1 + sum(len(full) + 1 for full, mini in B.values())      # rows needed to show EVERY block in full (+ header/blank), for the auto font size
    return [""] + [l for pri in sorted(out) for l in out[pri] + [""]]
NEED = {"lines": 0}
FONT = {"size": 9, "t": 0.0}; FONT_MIN, FONT_MAX = 6, 11
def set_font(n):
    """kitty font size of THIS window (kitten @ acts on the window it is run from)"""
    sock = os.environ.get("STALKER_SOCK") or os.environ.get("KITTY_LISTEN_ON")
    if not sock: return False
    r = subprocess.run(["kitten", "@", "--to", sock, "set-font-size", str(n)], capture_output=True, timeout=5)
    try: open("/tmp/statuspane_font.log", "a").write(f"{time.strftime('%T')} set {n} rc={r.returncode} {r.stderr.decode()[:120]}\n")
    except OSError: pass
    FONT["t"] = time.time()
    if r.returncode == 0: FONT["size"] = n; return True
    return False
def autosize(rows):
    """the biggest font at which every block fits: smaller when there is more to show, bigger again when there is less (checked every refresh, changes at most every 8 s, with some slack so it does not flap)"""
    if time.time() - FONT["t"] < 8: return
    need, f = NEED["lines"] + 2, FONT["size"]
    try: open("/tmp/statuspane_font.log", "a").write(f"{time.strftime('%T')} need={need} rows={rows} font={f}\n")
    except OSError: pass
    if need > rows and f > FONT_MIN: set_font(max(FONT_MIN, min(f - 1, int(f * rows / need))))              # too much: shrink (jump straight to the size that fits)
    elif f < FONT_MAX:
        best = min(FONT_MAX, int(f * rows / (need * 1.05)))                                                  # rows shrink about in proportion to the size: biggest size that still fits
        if best > f: set_font(best)
def main():
    if os.environ.get("STALKER_AUTOSIZE", "1") == "1": set_font(FONT["size"])
    while True:
        size = shutil.get_terminal_size((80, 60)); cols, rows = size.columns, size.lines
        main_win = os.environ.get("STALKER_MAIN_WIN"); sock = os.environ.get("STALKER_MAIN_SOCK") or os.environ.get("STALKER_SOCK") or os.environ.get("KITTY_LISTEN_ON")
        if main_win and sock and subprocess.run(["kitten", "@", "--to", sock, "ls", "--match", f"id:{main_win}"], capture_output=True).returncode != 0: return
        lines = compose(cols, rows - 1)
        if os.environ.get("STALKER_AUTOSIZE", "1") == "1": autosize(rows)
        sys.stdout.write("\x1b[H\x1b[2J" + f"{C['h']}STALKER PORT{C['0']}  {time.strftime('%a %b %d')}  {time.strftime('%I:%M:%S %p').lstrip('0')}  {C['y']}{daypart().lower()}{C['0']}\n" + "\n".join(lines[:rows - 2]) + "\n"); sys.stdout.flush()
        if len(sys.argv) > 1 and sys.argv[1] == "--once": return
        time.sleep(3)
os.environ.pop("CLAUDE_STATUS_PANE", None)
if __name__ == "__main__":
    main()

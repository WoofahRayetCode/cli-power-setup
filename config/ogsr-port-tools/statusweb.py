#!/usr/bin/env python3
"""Read-only phone dashboard: the same blocks as the status window (needs-you, now, local workers, game, status line, ticker) plus a feed of what Claude is doing
(descriptions of its recent tool calls and replies, never the commands themselves). Open it in the phone's browser, or add it to the home screen / use the Android shell app.
  statusweb.py run [--port 8765]     serve on all interfaces; every request needs the secret token (?t=...), kept in ~/.cache/statusweb/token
  statusweb.py url                   print the links (LAN and Tailscale)
Nothing can be changed through it: GET only, no commands, no files other than the status data below."""
import html, json, os, re, secrets, socket, subprocess, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
here = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here / "tools"))
import statuspane
D = Path.home() / ".cache/statusweb"; D.mkdir(parents=True, exist_ok=True); TOK = D / "token"
if not TOK.exists(): TOK.write_text(secrets.token_urlsafe(18)); TOK.chmod(0o600)
TOKEN = TOK.read_text().strip()
PIN_F, SENDS = D / "pin", D / "sends.log"
QUEUE = Path.home() / ".cache/claude-autosend/remote_queue.jsonl"      # claude-autosend's watcher types these into the Claude prompt when it is empty
def pin():
    try: return PIN_F.read_text().strip()
    except OSError: return ""
def tailnet_or_local(ip):
    return ip == "127.0.0.1" or re.match(r"^100\.(6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.", ip) is not None     # loopback or Tailscale (100.64.0.0/10)
def recent_sends():
    try: return [float(x) for x in SENDS.read_text().split() if time.time() - float(x) < 3600]
    except Exception: return []
CLS = {"1;36": "h", "1;33": "y", "1;35": "m", "1;32": "g", "2": "d", "1": "b"}
def ansi_html(s):
    out, open_ = [], False
    for part in re.split(r"(\x1b\[[0-9;:]*m)", s):
        m = re.match(r"\x1b\[([0-9;:]*)m", part)
        if m:
            if open_: out.append("</span>"); open_ = False
            c = CLS.get(m.group(1))
            if c: out.append(f'<span class="{c}">'); open_ = True
        else: out.append(html.escape(part))
    return "".join(out) + ("</span>" if open_ else "")
def activity(n=14):
    """what Claude did lately: assistant replies (first line) and tool descriptions from the newest session transcript"""
    proj = Path.home() / ".claude/projects" / str(here).replace("/", "-")
    fs = sorted(proj.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not fs: return []
    out = []
    try:
        with open(fs[0], "rb") as f:
            f.seek(0, 2); size = f.tell(); f.seek(max(0, size - 400000)); lines = f.read().decode("utf-8", "ignore").splitlines()[1:]
    except OSError: return []
    for l in lines[-300:]:
        try: e = json.loads(l)
        except Exception: continue
        if e.get("type") != "assistant": continue
        ts = (e.get("timestamp") or "")[11:16]
        for c in (e.get("message", {}).get("content") or []):
            if c.get("type") == "text" and c["text"].strip(): out.append(f"{ts} says: {c['text'].strip().splitlines()[0][:140]}")
            elif c.get("type") == "tool_use":
                i = c.get("input") or {}
                out.append(f"{ts} {c.get('name')}: {str(i.get('description') or i.get('file_path') or i.get('pattern') or i.get('query') or '')[:120]}")
    return out[-n:]
EV = D / "events.jsonl"; _ev = {"id": 0, "needs": None, "pos": {}, "seen": set(), "inited": False}
def _ev_add(kind, text, t=None):
    _ev["id"] += 1
    with open(EV, "a") as f: f.write(json.dumps({"id": _ev["id"], "t": t or time.strftime("%F %T"), "kind": kind, "text": text[:900]}) + "\n")
def _tail(path, key, first=0):
    try: size = path.stat().st_size
    except OSError: return []
    if key not in _ev["pos"]: _ev["pos"][key] = max(0, size - first)
    if size < _ev["pos"][key]: _ev["pos"][key] = 0
    with open(path, "rb") as f: f.seek(_ev["pos"][key]); data = f.read().decode("utf-8", "ignore"); _ev["pos"][key] = f.tell()
    return [l for l in data.splitlines() if l.strip()]
def collect_events():
    """feeds /api/events (the Android app's notifications and chat): NEEDS YOU changes, walker 'learned' lines, guardian problems, Claude's replies, messages sent from the phone"""
    first = not _ev["inited"]
    if first:
        _ev["inited"] = True
        try: _ev["id"] = max([json.loads(l)["id"] for l in EV.read_text().splitlines()] or [0])
        except Exception: _ev["id"] = 0
    n = (here / ".agents/needs_you.txt").read_text().strip() if (here / ".agents/needs_you.txt").exists() else ""
    if _ev["needs"] is None: _ev["needs"] = n
    elif n != _ev["needs"]:
        _ev["needs"] = n
        if n: _ev_add("needs", n)
    for l in _tail(here / ".agents/guardian.log", "g", 0 if not first else 0):
        if re.search(r"killing|stale|gave up|crash|failed|error|leaving it", l): _ev_add("guardian", l)
    xs = sorted((here / "_appdata_/logs").glob("xray_*.log"), key=lambda p: p.stat().st_mtime)
    if xs:
        for l in _tail(xs[-1], "x", 0):
            if "WALK LEARNED" in l: _ev_add("learned", l.split("WALK LEARNED", 1)[-1].strip())
    proj = Path.home() / ".claude/projects" / str(here).replace("/", "-")
    fs = sorted(proj.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if fs:
        for l in _tail(fs[0], "c", 0):
            try: e = json.loads(l)
            except Exception: continue
            if e.get("type") == "user":                                    # what the user typed in the terminal: mirror it to the app (phone messages are already shown by the queue, tool results and system notes are skipped)
                cont = (e.get("message", {}) or {}).get("content")
                txt = cont if isinstance(cont, str) else " ".join(c.get("text", "") for c in (cont or []) if isinstance(c, dict) and c.get("type") == "text")
                txt = (txt or "").strip()
                if txt and not txt.startswith(("<", "[message from the user", "📱 PHONE", "[REMOTE COMMAND", "Caveat:", "[Request interrupted")) and "<system-reminder>" not in txt[:60]:
                    key = "me:" + txt[:200]
                    if key not in _ev["seen"]: _ev["seen"].add(key); _ev_add("me", "(typed here) " + txt[:700])
                continue
            if e.get("type") != "assistant": continue
            for c in (e.get("message", {}).get("content") or []):
                if c.get("type") == "text" and len(c["text"].strip()) > 20:
                    key = c["text"].strip()[:200]                                      # the transcript repeats some messages: dedupe by content
                    if key not in _ev["seen"]: _ev["seen"].add(key); _ev_add("claude", c["text"].strip())
    for l in _tail(QUEUE, "q", 0):
        try: r = json.loads(l)
        except Exception: continue
        if r.get("status") == "new": _ev_add("me", r.get("text", ""))
def events_after(after, limit=60):
    try: rows = [json.loads(l) for l in EV.read_text().splitlines()[-400:]]
    except Exception: rows = []
    return [r for r in rows if r["id"] > after][-limit:]
def state():
    w = (here / ".agents/walker_report.md").read_text() if (here / ".agents/walker_report.md").exists() else ""; v = re.search(r"Verdict: (.*)", w)
    rd = lambda p: (here / p).read_text().strip() if (here / p).exists() else ""
    return {"time": time.strftime("%F %T"), "needs": rd(".agents/needs_you.txt"), "now": rd(".agents/task.txt"), "walker": v.group(1) if v else "", "game": bool(subprocess.run("pgrep -f '[x]rEngine.exe'", shell=True, capture_output=True).stdout.strip()),
            "workers": subprocess.run("local-worker status | head -1", shell=True, capture_output=True, text=True, cwd=here).stdout.strip(), "commands_on": bool(pin()), "last_event": _ev["id"]}
def live_env():
    """environment with the LIVE Wayland socket: processes started before a re-login carry a stale WAYLAND_DISPLAY (wayland-0) and kscreen-doctor / spectacle then fail silently"""
    env = dict(os.environ); rt = env.get("XDG_RUNTIME_DIR", "/run/user/%d" % os.getuid()); env["XDG_RUNTIME_DIR"] = rt
    socks = sorted(x.name for x in Path(rt).glob("wayland-[0-9]") if (Path(rt) / (x.name + ".lock")).exists())
    if socks: env["WAYLAND_DISPLAY"] = socks[-1]
    env.setdefault("DBUS_SESSION_BUS_ADDRESS", "unix:path=%s/bus" % rt); return env
_game = {"t": 0.0, "jpg": b""}
def game_jpg(w=960):
    """live picture of the game window for the app's Game tab: one spectacle capture of the whole desktop (works with the screen dimmed), cropped to the game window slot (top-left of the main screen,
    1280x720 + title bar), cached for 1 s. Nothing else on the desktop is ever sent: when no game is running a plain 'no game' picture is returned instead."""
    import io, threading
    from PIL import Image, ImageDraw
    if time.time() - _game["t"] < 1.0 and _game["jpg"]: return _game["jpg"]
    def placeholder(msg):
        im = Image.new("RGB", (960, 540), (15, 20, 25)); ImageDraw.Draw(im).text((330, 260), msg, fill=(200, 211, 223)); b = io.BytesIO(); im.save(b, "JPEG", quality=70); return b.getvalue()
    if not subprocess.run("pgrep -f '[x]rEngine.exe'", shell=True, capture_output=True).stdout.strip(): _game["jpg"], _game["t"] = placeholder("no game running"), time.time(); return _game["jpg"]
    out = subprocess.run("kscreen-doctor -o", shell=True, capture_output=True, text=True, timeout=10, env=live_env()).stdout
    out = re.sub(r"\x1b\[[0-9;]*m", "", out); geo = [tuple(map(int, m)) for m in re.findall(r"Geometry: (-?\d+),(-?\d+) (\d+)x(\d+)", out)]
    if not geo: return placeholder("screen layout unknown")
    mx, my, mw, mh = max(geo, key=lambda g: g[2] * g[3]); minx, miny = min(g[0] for g in geo), min(g[1] for g in geo)
    f = "/tmp/zm_game_shot.png"
    subprocess.run(["spectacle", "-b", "-n", "-f", "-o", f], capture_output=True, timeout=20, env=live_env())
    im = Image.open(f).convert("RGB"); box = (mx - minx, my - miny, mx - minx + 1280, my - miny + 722)
    im = im.crop(box); h = int(w * im.height / im.width); im = im.resize((w, h)); b = io.BytesIO(); im.save(b, "JPEG", quality=72); _game["jpg"], _game["t"] = b.getvalue(), time.time(); return _game["jpg"]
def _plain(t): return re.sub(r"\x1b\[[0-9;:]*m", "", t)
def _bar(pct, w=10): f = int(round(w * pct / 100)); return "▰" * f + "▱" * (w - f)
def tab_text(name):
    """text of the app's tabs: the same information as the windows on the laptop"""
    rd = lambda p: (here / p).read_text(errors="ignore").strip() if (here / p).exists() else ""
    if name == "status": return "\n".join(_plain(l) for l in statuspane.compose(70, 90))
    if name == "models": return subprocess.run("python3 tools/nvidia_progress.py", shell=True, capture_output=True, text=True, cwd=here, timeout=20).stdout
    if name == "agenda": return rd(".agents/agenda.txt") + "\n\nneeds you: " + (rd(".agents/needs_you.txt") or "nothing")
    if name == "ops":
        out = [f"{r['t'][11:16]} {r['kind']:8} {r['text'][:140]}" for r in events_after(0, 60)]
        out += ["", "-- guardian"] + rd(".agents/guardian.log").splitlines()[-8:] + ["", "-- walker"] + rd(".agents/walker_report.md").splitlines()[-4:]
        return "\n".join(out)
    if name == "monitor":
        def cpu():
            return [list(map(int, l.split()[1:8])) for l in open("/proc/stat") if l.startswith("cpu") and l[3].isdigit()]
        a = cpu(); time.sleep(0.4); b = cpu(); rows = []
        for i, (x, y) in enumerate(zip(a, b)):
            tot = sum(y) - sum(x); idle = (y[3] + y[4]) - (x[3] + x[4]); pct = 0 if tot <= 0 else 100 * (tot - idle) / tot; rows.append((i, pct))
        lines = ["CPU (%d threads)" % len(rows)] + ["  ".join(f"C{i:<2}{_bar(p, 6)}{p:3.0f}%" for i, p in rows[k:k + 3]) for k in range(0, len(rows), 3)]
        g = subprocess.run("nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw --format=csv,noheader,nounits", shell=True, capture_output=True, text=True).stdout.strip().split(",")
        if len(g) >= 6: lines += ["", f"GPU {g[0].strip()}", f"  load {g[1].strip()}%  VRAM {int(g[2]) / 1024:.1f}/{int(g[3]) / 1024:.1f} GB  {g[4].strip()}C  {float(g[5]):.0f} W"]
        mem = {l.split(":")[0]: int(l.split()[1]) for l in open("/proc/meminfo")}
        lines += ["", f"RAM  {(mem['MemTotal'] - mem['MemAvailable']) / 1048576:.1f}/{mem['MemTotal'] / 1048576:.1f} GB   load {os.getloadavg()[0]:.1f}", "", "top processes (CPU %)"]
        lines += [l[:80] for l in subprocess.run("ps -eo pcpu,pmem,comm --sort=-pcpu | head -9", shell=True, capture_output=True, text=True).stdout.splitlines()]
        return "\n".join(lines)
    return "unknown tab"
def snapshot():
    lines = statuspane.compose(64, 80)
    return {"time": time.strftime("%F %T"), "html": "\n".join(ansi_html(l) for l in lines), "activity": activity(), "autopilot": subprocess.run("claude-autosend autopilot status", shell=True, capture_output=True, text=True).stdout.strip()}
PAGE = """<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><meta name=theme-color content="#0f1419"><title>STALKER Port</title>
<style>:root{color-scheme:dark light;--bg:#0f1419;--fg:#e6e6e6;--mut:#8a9199;--h:#4dd0e1;--y:#ffd54f;--m:#ce93d8;--g:#81c784}@media(prefers-color-scheme:light){:root{--bg:#fafafa;--fg:#1d2127;--mut:#5f6770;--h:#00838f;--y:#b26a00;--m:#7b1fa2;--g:#2e7d32}}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.35 ui-monospace,Menlo,monospace}main{padding:12px 16px 40px;max-width:900px;margin:auto}h2{font:600 12px sans-serif;letter-spacing:.08em;color:var(--mut);margin:18px 0 6px}
pre{white-space:pre-wrap;word-break:break-word;margin:0}.h{color:var(--h);font-weight:700}.y{color:var(--y);font-weight:700}.m{color:var(--m);font-weight:700}.g{color:var(--g);font-weight:700}.d{color:var(--mut)}.b{font-weight:700}#t{color:var(--mut);font-size:12px}</style></head>
<body><main><div id=t>connecting…</div><div class=d>Android app: <a href="zonemonitor.apk?t=" id=apk style="color:var(--h)">download Zone Monitor</a></div><h2>STATUS</h2><pre id=s></pre><h2>WHAT CLAUDE IS DOING</h2><pre id=a></pre><h2>AUTOPILOT</h2><pre id=p></pre>
<h2>SEND A COMMAND TO CLAUDE</h2><div id=c><input id=pin type=password placeholder="PIN" autocomplete=off style="width:6em"> <input id=txt placeholder="message to Claude" style="width:60%"> <button id=go onclick="send()">Send</button><div id=r class=d></div></div>
<script>const q=new URLSearchParams(location.search).get("t")||"";async function go(){try{const r=await fetch("api?t="+encodeURIComponent(q),{cache:"no-store"});if(!r.ok)throw 0;const d=await r.json();
document.getElementById("t").textContent="updated "+d.time;document.getElementById("s").innerHTML=d.html;document.getElementById("a").textContent=d.activity.join("\\n");document.getElementById("p").textContent=d.autopilot}catch(e){document.getElementById("t").textContent="offline - retrying"}}document.getElementById("apk").href="zonemonitor.apk?t="+encodeURIComponent(q);try{document.getElementById("pin").value=localStorage.getItem("zpin")||""}catch(e){}
async function send(){const pin=document.getElementById("pin").value,text=document.getElementById("txt").value;if(!text.trim())return;try{localStorage.setItem("zpin",pin)}catch(e){}
const r=await fetch("send?t="+encodeURIComponent(q),{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({pin:pin,text:text})});document.getElementById("r").textContent=(await r.text());if(r.ok)document.getElementById("txt").value=""}
go();setInterval(go,3000)</script></body></html>"""
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        u = urlparse(self.path); t = parse_qs(u.query).get("t", [""])[0]
        def reply(code, msg): self.send_response(code); self.send_header("Content-Type", "text/plain"); self.end_headers(); self.wfile.write(msg.encode())
        if u.path != "/send" or not secrets.compare_digest(t, TOKEN): return reply(403, "forbidden")
        if not (tailnet_or_local(self.client_address[0]) or os.environ.get("STATUSWEB_LAN_COMMANDS")): return reply(403, "commands are only accepted over Tailscale")
        if not pin(): return reply(403, "commands are off: no PIN set (on the laptop: statusweb.py setpin)")
        try: n = int(self.headers.get("Content-Length", "0")); body = json.loads(self.rfile.read(min(n, 4000)))
        except Exception: return reply(400, "bad request")
        if not secrets.compare_digest(str(body.get("pin", "")), pin()): time.sleep(2); return reply(403, "wrong PIN")
        text = re.sub(r"\s+", " ", str(body.get("text", ""))).strip()[:1000]
        if not text: return reply(400, "empty")
        if len(recent_sends()) >= 10: return reply(429, "limit: 10 commands per hour")
        QUEUE.parent.mkdir(parents=True, exist_ok=True)
        with open(QUEUE, "a") as f: f.write(json.dumps({"t": time.strftime("%F %T"), "text": text, "from": self.client_address[0], "status": "new"}) + "\n")
        with open(SENDS, "a") as f: f.write(f"{time.time()}\n")
        with open(here / "docs/INBOX.md", "a") as f: f.write(f"- [{time.strftime('%F %H:%M')}] [remote] {text}\n")
        reply(200, "queued: it is typed into Claude's prompt as soon as the prompt is empty")
    def do_GET(self):
        u = urlparse(self.path); t = parse_qs(u.query).get("t", [""])[0]
        if not secrets.compare_digest(t, TOKEN): self.send_response(403); self.end_headers(); self.wfile.write(b"forbidden"); return
        if u.path in ("/", "/index.html"): body, ct = PAGE.encode(), "text/html; charset=utf-8"
        elif u.path == "/api": body, ct = json.dumps(snapshot()).encode(), "application/json"
        elif u.path == "/api/mind.png":
            q = parse_qs(u.query); import walker_mind_render as wmr
            try: w, h = int(q.get("w", ["720"])[0]), int(q.get("h", ["720"])[0])
            except ValueError: w, h = 720, 720
            body, ct = wmr.render(max(200, min(w, 1600)), max(200, min(h, 1600))), "image/png"
        elif u.path == "/api/game.jpg":
            q = parse_qs(u.query)
            try: w = max(320, min(int(q.get("w", ["960"])[0]), 1600))
            except ValueError: w = 960
            body, ct = game_jpg(w), "image/jpeg"
        elif u.path == "/api/tab": body, ct = tab_text(parse_qs(u.query).get("name", [""])[0]).encode(), "text/plain; charset=utf-8"
        elif u.path == "/api/state": body, ct = json.dumps(state()).encode(), "application/json"
        elif u.path == "/api/events":
            a = parse_qs(u.query).get("after", ["0"])[0]; body, ct = json.dumps(events_after(int(a) if a.isdigit() else 0)).encode(), "application/json"
        elif u.path == "/zonemonitor.apk":                      # the Android shell app (android/ZoneMonitor/build.sh): download and install it on the phone
            apk = here / "android/ZoneMonitor/build/zonemonitor.apk"
            if not apk.is_file(): self.send_response(404); self.end_headers(); return
            body, ct = apk.read_bytes(), "application/vnd.android.package-archive"
        else: self.send_response(404); self.end_headers(); return
        self.send_response(200); self.send_header("Content-Type", ct); self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
def ips():
    out = subprocess.run("ip -4 -o addr show scope global | awk '{print $4}' | cut -d/ -f1", shell=True, capture_output=True, text=True).stdout.split()
    return out
if __name__ == "__main__":
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8765
    if len(sys.argv) > 1 and sys.argv[1] == "setpin":
        p = sys.argv[2] if len(sys.argv) > 2 else str(secrets.randbelow(900000) + 100000); PIN_F.write_text(p); PIN_F.chmod(0o600); print("PIN set:", p, "(commands now accepted over Tailscale)")
    elif len(sys.argv) > 1 and sys.argv[1] == "url":
        for ip in ips(): print(f"http://{ip}:{port}/?t={TOKEN}")
    else:
        import threading
        def _loop():
            n = 0
            while True:
                try:
                    if n % 8 == 0: collect_events()
                    import walker_mind_render as _wmr; _wmr.sample()          # trail of the Walker Mind picture: one sample a second
                except Exception as ex: print("events:", ex, flush=True)
                n += 1; time.sleep(1)
        threading.Thread(target=_loop, daemon=True).start()
        print("serving on port", port, flush=True); ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()

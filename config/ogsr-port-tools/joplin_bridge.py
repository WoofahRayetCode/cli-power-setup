#!/usr/bin/env python3
"""Two-way bridge to Joplin Desktop (syncs to the phone) through its local Data API.
  joplin_bridge.py watch [--interval 60]   keeps running: publishes status, picks up new phone entries
  joplin_bridge.py status                  one-shot publish
  joplin_bridge.py inbox                   one-shot read of the phone inbox
  joplin_bridge.py done "fragment" ...     mark matching inbox lines [done] after they are completed (never deletes)
Notebook "STALKER Port" with three notes:
  "1 STATUS (Antigravity writes)"   what is running now, last results, the ticker text, free space, newest night report, research results   (overwritten every cycle)
  "2 INBOX (you write)"        type ideas / bugs / links here on the phone. Every NEW line is appended to docs/INBOX.md as [phone] and to .agents/queue.jsonl;
                               lines containing a URL are fetched (YouTube: title/description via oEmbed) and summarised by a local model into "3 RESEARCH"
  "3 RESEARCH (Antigravity writes)" summaries of the links / ideas you sent, with what could be built from them
Needs Joplin's clipper service (it is on: port 41184). The token is read from Joplin's settings.json and never printed. Local model: llmrun (game-aware, CPU while the game runs)."""
import json, os, re, sys, time, html, urllib.request, urllib.parse
from pathlib import Path
here = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(here / "tools"))
import joplin_sync as J
QUEUE, SEEN = here / ".agents/queue.jsonl", here / ".agents/joplin_seen.json"
NB = "STALKER Port"; T_STATUS, T_INBOX, T_RES = "1 STATUS (Antigravity writes)", "2 INBOX (you write)", "3 RESEARCH (Antigravity writes)"
def connect():
    port = J.find_port()
    if not port: raise RuntimeError("Joplin API not answering")
    J.BASE = f"http://127.0.0.1:{port}"; J.TOKEN = json.load(open(os.path.expanduser("~/.config/joplin-desktop/settings.json"))).get("api.token")
def note(folder, title, default=""):
    ns = [n for n in J.paged(f"/folders/{folder['id']}/notes", {"fields": "id,title,body"}) if n["title"] == title]
    return ns[0] if ns else J.api("POST", "/notes", body={"title": title, "body": default, "parent_id": folder["id"]}) | {"body": default}
def folder():
    fs = J.paged("/folders"); return next((f for f in fs if f["title"] == NB), None) or J.api("POST", "/folders", body={"title": NB})
def sh(cmd):
    import subprocess; return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=here).stdout.strip()
def status_text():
    tick = (here / ".agents/ticker.txt").read_text().strip() if (here / ".agents/ticker.txt").exists() else "-"
    night = sorted((here / "docs/night").glob("*.md"))[-1:] or []
    need = (here / ".agents/needs_you.txt").read_text().strip() if (here / ".agents/needs_you.txt").exists() else "Nothing. Sleep, eat, take your time."
    parts = [f"# Status {time.strftime('%F %H:%M')}", "## In 10 seconds", f"- **Happening now:** {tick}", f"- **Needs you:** {need}", "- **Safe to ignore everything below** unless that line says otherwise.", "", "## Machine", "```", sh("python3 tools/sysguard.py status | head -12"), "```", "## Disk", "```", sh("python3 tools/diskwatch.py status | head -6"), "```",
             "## Crashes", "```", sh("python3 tools/crashwatch.py verify | tail -8"), "```"]
    if night: parts += ["## Latest night report", night[0].read_text()[-1800:]]
    bl = here / ".agents/backlog.md"
    if bl.exists(): parts += ["## Backlog (open)", "\n".join(l for l in bl.read_text().splitlines() if "[ ]" in l)[:1800]]
    return "\n".join(parts)
def fetch_text(url):
    try:
        if "youtube.com" in url or "youtu.be" in url:
            j = json.load(urllib.request.urlopen(urllib.request.Request("https://noembed.com/embed?url=" + urllib.parse.quote(url), headers={"User-Agent": "Mozilla/5.0"}), timeout=15))
            return f"YouTube video: {j.get('title')} by {j.get('author_name')}"
        raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=20).read(400000).decode("utf-8", "ignore")
        raw = re.sub(r"(?s)<(script|style).*?</\1>", " ", raw); return html.unescape(re.sub(r"<[^>]+>", " ", raw))[:6000]
    except Exception as e: return f"(could not fetch: {e})"
def summarise(line):
    import llmrun
    url = (re.findall(r"https?://\S+", line) or [None])[0]
    body = fetch_text(url) if url else ""
    p = (f"The user of a STALKER Complete -> OGSR port (LuaJIT, LTX, Blender models, Twitch, fun features) sent this from their phone: {line}\n\nPage content:\n{body[:5000]}\n\n"
         "Summarise in <= 8 lines, then list 3 concrete things we could build from it (file/tool/effort).")
    return llmrun.ask("qwen3:30b-a3b", p, 900)
def inbox():
    connect(); f = folder(); n = note(f, T_INBOX, "Write ideas, bugs and links here, one per line. Antigravity picks up new lines.\n\n")
    seen = set(json.loads(SEEN.read_text())) if SEEN.exists() else set()
    new = [l.strip() for l in n["body"].splitlines()[2:] if l.strip() and l.strip() not in seen and not l.startswith("#") and not l.strip().lower().startswith("[done]")]
    if not new: return 0
    res = note(f, T_RES, "")
    add = ""
    for l in new:
        seen.add(l)
        with open(here / "docs/INBOX.md", "a") as fh: fh.write(f"- [{time.strftime('%F %H:%M')}] [phone] {l}\n")
        QUEUE.parent.mkdir(exist_ok=True)
        with open(QUEUE, "a") as fh: fh.write(json.dumps({"when": time.strftime("%F %T"), "text": l, "source": "phone", "status": "new"}) + "\n")
        try: add += f"\n## {l[:80]}\n{summarise(l)}\n"
        except Exception as e: add += f"\n## {l[:80]}\n(summary failed: {e})\n"
    J.api("PUT", f"/notes/{res['id']}", body={"body": (res.get("body") or "") + add})
    SEEN.write_text(json.dumps(sorted(seen))); print(f"{len(new)} phone entries queued"); return len(new)
DOCS = {"4 WORK LOG (everything done)": "docs/WORK_LOG.md", "5 MODELS and AI fleet": "docs/MODELS.md", "6 BACKLOG": ".agents/backlog.md", "7 TOOLS and how to run them": "PROJECT_STATE.md", "9 Q&A (questions you asked, answers I gave)": "docs/QA.md", "10 EE port: plan, engine gaps, tools": "docs/EE_PORT.md", "11 EE bugs and patch mods": "docs/EE_BUGS.md", "12 ZoneForge: features I added": "docs/ZONEFORGE_FEATURES.md", "13 Discord bot setup (step by step)": "docs/DISCORD_SETUP_NOTE.md", "14 NVIDIA models: what they replace": "docs/NVIDIA_MODELS.md", "15 Android app (Zone Monitor)": "docs/ANDROID_APP.md"}
def upload_resource(path, title=None):
    """POST /resources (multipart: props + data) -> resource id. Images embed as ![](:/id), other files as [name](:/id)."""
    import mimetypes, uuid
    path = Path(path); b = uuid.uuid4().hex; mt = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"props\"\r\n\r\n" + json.dumps({"title": title or path.name}) + f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"data\"; filename=\"{path.name}\"\r\nContent-Type: {mt}\r\n\r\n").encode() + path.read_bytes() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(f"{J.BASE}/resources?token={J.TOKEN}", data=body, method="POST", headers={"Content-Type": f"multipart/form-data; boundary={b}"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read().decode())["id"]
GALLERY = "8 GALLERY (screenshots + sounds, newest first)"
def gallery(max_images=6, max_sounds=4):
    """attach the newest unseen game screenshots (downscaled) and sound files to the gallery note"""
    import subprocess, hashlib
    connect(); f = folder(); n = note(f, GALLERY, "# Gallery\nProgress shots of models/levels and the newest sounds, newest section first.\n")
    seen_f = here / ".agents/joplin_gallery_seen.json"; seen = set(json.loads(seen_f.read_text())) if seen_f.exists() else set()
    new = []
    imgs = sorted([p for d in ("docs/shots", "docs/walk", "docs/tape") for p in (here / d).glob("*.png")], key=lambda p: p.stat().st_mtime, reverse=True)
    snds = sorted([p for d in ("gamedata/sounds/fun", "gamedata/sounds/wildlife", "gamedata/sounds/actor") for p in (here / d).glob("*.ogg")], key=lambda p: p.stat().st_mtime, reverse=True)
    sec = ""
    for p in imgs[:30]:
        h = hashlib.sha1((p.name + str(p.stat().st_size)).encode()).hexdigest()
        if h in seen or len(new) >= max_images: continue
        small = Path("/tmp") / (p.stem + ".jpg")
        if subprocess.run(["magick", str(p), "-resize", "1100x", "-quality", "80", str(small)], capture_output=True).returncode: continue
        rid = upload_resource(small, p.name); seen.add(h); new.append(p.name); sec += f"**{p.name}**  \n![{p.name}](:/{rid})\n\n"
    ns = 0
    for p in snds[:30]:
        h = hashlib.sha1((p.name + str(p.stat().st_size)).encode()).hexdigest()
        if h in seen or ns >= max_sounds or p.stat().st_size > 1_500_000: continue
        rid = upload_resource(p, p.name); seen.add(h); ns += 1; sec += f"sound: [{p.name}](:/{rid})\n\n"
    if sec:
        body = n.get("body") or ""; head, _, rest = body.partition("\n\n")
        J.api("PUT", f"/notes/{n['id']}", body={"body": head + f"\n\n## {time.strftime('%F %H:%M')}\n{sec}" + rest})
        seen_f.write_text(json.dumps(sorted(seen))); print(f"gallery: +{len(new)} images, +{ns} sounds")
def publish_docs():
    connect(); f = folder()
    for title, rel in DOCS.items():
        p = here / rel
        if not p.exists(): continue
        n = note(f, title, "")
        if title.startswith("13 ") and (n.get("body") or "").strip(): continue       # the setup note holds YOUR answers: written once, never overwritten
        J.api("PUT", f"/notes/{n['id']}", body={"body": p.read_text()[:180000]})
def discord_note():
    """Note 13 (Discord setup): copy the user id you typed under 'Your answers' to ~/.config/stalker-discord/owner_id (not secret), and if a bot TOKEN was pasted into the note by mistake,
    black it out in the note at once and tell the user to reset it (a token in a synced note is a leak). The token itself only ever goes in through tools/discord_setup.sh."""
    import re
    connect(); f = folder(); n = note(f, "13 Discord bot setup (step by step)", "")
    body = n.get("body") or ""
    if not body: return
    changed = False
    if re.search(r"[A-Za-z0-9_-]{23,28}\.[A-Za-z0-9_-]{6,7}\.[A-Za-z0-9_-]{27,}", body):
        body = re.sub(r"[A-Za-z0-9_-]{23,28}\.[A-Za-z0-9_-]{6,7}\.[A-Za-z0-9_-]{27,}", "[TOKEN REMOVED: reset it in the developer portal]", body); changed = True
        (here / ".agents/needs_you.txt").open("a").write("A Discord bot token was pasted into a Joplin note: I removed it from the note; reset the token in the Discord developer portal (Bot, Reset Token) and use tools/discord_setup.sh.\n")
    m = re.search(r"Discord user id:\s*(\d{15,22})", body)
    cfgdir = Path.home() / ".config/stalker-discord"
    if m:
        cfgdir.mkdir(parents=True, exist_ok=True); (cfgdir / "owner_id").write_text(m.group(1)); (cfgdir / "owner_id").chmod(0o600)
    if changed: J.api("PUT", f"/notes/{n['id']}", body={"body": body})
def publish():
    connect(); f = folder(); n = note(f, T_STATUS, ""); J.api("PUT", f"/notes/{n['id']}", body={"body": status_text()})
def mark_done(*frags):
    """joplin_bridge.py done "text fragment" ...   prefix the matching INBOX lines with [done] (never deletes); the queue entry is set to status done.
    The watcher ignores [done] lines, so they are not queued again."""
    connect(); f = folder(); n = note(f, T_INBOX, ""); out, hit = [], []
    for l in n["body"].splitlines():
        if l.strip() and not l.strip().lower().startswith("[done]") and not l.startswith("#") and any(x.lower() in l.lower() for x in frags):
            hit.append(l.strip()); l = "[done] " + l
        out.append(l)
    if hit:
        J.api("PUT", f"/notes/{n['id']}", body={"body": "\n".join(out)})
        if QUEUE.exists():
            rows = [json.loads(x) for x in QUEUE.read_text().splitlines() if x.strip()]
            for r in rows:
                if r.get("text", "").strip() in hit: r["status"] = "done"
            QUEUE.write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(f"{len(hit)} inbox lines marked [done]"); return len(hit)
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"; iv = int(sys.argv[sys.argv.index("--interval") + 1]) if "--interval" in sys.argv else 60
    if cmd == "watch":
        t_pub = 0
        while True:
            try:
                inbox(); discord_note()
                if time.time() - t_pub > 300: publish(); publish_docs(); gallery(); t_pub = time.time()
            except Exception as e: print("joplin bridge:", e)
            time.sleep(iv)
    elif cmd == "inbox": inbox()
    elif cmd == "done": mark_done(*sys.argv[2:])
    elif cmd == "docs": publish_docs()
    elif cmd == "discordnote": discord_note()
    elif cmd == "gallery": gallery()
    else: publish()

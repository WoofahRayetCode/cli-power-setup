#!/usr/bin/env python3
"""STALKER port Discord bot: talks ONLY to you, in direct messages. Run with ~/.cache/discordbot/bin/python tools/discord_bot.py
Setup (once, needs you): see docs/DISCORD_BOT.md. Config in ~/.config/stalker-discord/ : `token` (bot token), `owner_id` (your numeric Discord user id); both chmod 600.
Safety: every message from anybody but owner_id is ignored (no reply at all); it never joins channels (guild messages are ignored); commands are limited to the list below;
text for Antigravity goes through the same remote queue as the phone dashboard (10 per hour); nothing is ever executed from message text.
Pushes (DM, batched, at most one message per 10 s): NEEDS YOU changes, guardian recoveries, walker "learned" events, new local-model failures, hourly digest.
Commands (send as a DM): help | status | needs | walker | log | models | guardian | ask <text for Antigravity> | nightwalk on|off | digest on|off | mute <min>
Any other text is treated as `ask <text>` (queued for Antigravity, who answers in the terminal; his short replies are sent back here when the work log changes)."""
import asyncio, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
import discord
here = Path(__file__).resolve().parent.parent; CFG = Path.home() / ".config/stalker-discord"
QUEUE = Path.home() / ".cache/agy-autosend/remote_queue.jsonl"; SENDS = Path.home() / ".cache/discord_sends.txt"
def cfg(n):
    try: return (CFG / n).read_text().strip()
    except Exception: return ""
TOKEN, OWNER = cfg("token"), cfg("owner_id")
if not TOKEN or not OWNER.isdigit(): print("discord bot: not configured (see docs/DISCORD_BOT.md)"); sys.exit(0)
OWNER = int(OWNER)
def sh(c, t=15):
    try: return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t, cwd=here).stdout.strip()
    except Exception as e: return f"(error: {e})"
def rd(p, n=1500):
    try: return Path(p).read_text(errors="ignore")[-n:].strip()
    except Exception: return ""
st = {"mute": 0, "digest": True, "pos": {}, "needs": rd(here / ".agents/needs_you.txt", 4000), "last_digest": time.time()}
def new_lines(path, key, first_tail=0):
    p = Path(path)
    try: size = p.stat().st_size
    except Exception: return []
    if key not in st["pos"]: st["pos"][key] = max(0, size - first_tail)
    if size < st["pos"][key]: st["pos"][key] = 0
    with open(p, "rb") as f: f.seek(st["pos"][key]); data = f.read().decode("utf-8", "ignore"); st["pos"][key] = f.tell()
    return [l for l in data.splitlines() if l.strip()]
def status_text():
    w = rd(here / ".agents/walker_report.md", 900); v = re.search(r"Verdict: (.*)", w)
    return "\n".join(["**STALKER port status**", "now: " + (rd(here / ".agents/task.txt", 200) or "idle"), "needs you: " + (rd(here / ".agents/needs_you.txt", 300) or "nothing"),
        "game: " + ("running" if sh("pgrep -f '[x]rEngine.exe' | head -1") else "closed"), "walker: " + (v.group(1) if v else "no data"), "guardian: " + sh("tail -1 .agents/guardian.log")[:120], "workers: " + sh("local-worker status | head -1")])
def ask_claude(text):
    recent = [float(x) for x in rd(SENDS, 4000).split() if x.replace(".", "").isdigit() and time.time() - float(x) < 3600]
    if len(recent) >= 10: return "limit: 10 messages to Antigravity per hour"
    QUEUE.parent.mkdir(parents=True, exist_ok=True)
    with open(QUEUE, "a") as f: f.write(json.dumps({"t": time.strftime("%F %T"), "text": text[:1000], "from": "discord", "status": "new"}) + "\n")
    with open(SENDS, "a") as f: f.write(f"{time.time()}\n")
    with open(here / "docs/INBOX.md", "a") as f: f.write(f"- [{time.strftime('%F %H:%M')}] [discord] {text[:500]}\n")
    return "queued for Antigravity: it is typed into his prompt as soon as the prompt is empty"
def command(text):
    t = text.strip(); low = t.lower(); a = low.split()
    if not a or a[0] in ("help", "?"): return __doc__.split("Commands (send as a DM):")[1].split("\n")[0].strip()
    if a[0] == "status": return status_text()
    if a[0] == "needs": return rd(here / ".agents/needs_you.txt", 1500) or "nothing needs you"
    if a[0] == "walker": return rd(here / ".agents/walker_report.md", 1700) or "no walker data yet"
    if a[0] == "log": return "```\n" + sh("tail -8 docs/WORK_LOG.md")[-1700:] + "\n```"
    if a[0] == "models": return "```\n" + sh("local-worker status | head -12")[-1700:] + "\n```"
    if a[0] == "guardian": return "```\n" + sh("tail -10 .agents/guardian.log")[-1700:] + "\n```"
    if a[0] == "nightwalk" and len(a) > 1 and a[1] in ("on", "off"):
        want, stop = here / ".agents/nightwalk.want", here / ".agents/nightwalk.stop"
        if a[1] == "on": want.touch(); stop.unlink(missing_ok=True)
        else: stop.touch()
        return f"night walk {a[1]} (the guardian applies it within 30 s)"
    if a[0] == "digest" and len(a) > 1 and a[1] in ("on", "off"): st["digest"] = a[1] == "on"; return f"hourly digest {a[1]}"
    if a[0] == "mute" and len(a) > 1 and a[1].isdigit(): st["mute"] = time.time() + 60 * int(a[1]); return f"pushes muted for {a[1]} min (commands still work)"
    if a[0] == "ask": return ask_claude(t[3:].strip()) if len(t) > 4 else "ask what?"
    return ask_claude(t)
class Bot(discord.Client):
    async def setup_hook(self): self.loop.create_task(self.pusher())
    async def on_ready(self):
        print("discord bot ready as", self.user)
        u = await self.fetch_user(OWNER); await u.send("STALKER port bot online. Send `help` for commands.")
    async def on_message(self, m):
        if m.author.id != OWNER or m.guild is not None: return          # ONLY the owner, ONLY in a direct message; everything else is ignored silently
        out = await asyncio.get_event_loop().run_in_executor(None, command, m.content)
        for i in range(0, len(out), 1900): await m.channel.send(out[i:i + 1900])
    async def pusher(self):
        await self.wait_until_ready(); u = await self.fetch_user(OWNER); last_sent = 0
        while not self.is_closed():
            await asyncio.sleep(10); msgs = []
            try:
                n = rd(here / ".agents/needs_you.txt", 4000)
                if n != st["needs"]:
                    if n: msgs.append("**NEEDS YOU:** " + n[:600])
                    st["needs"] = n
                for l in new_lines(here / ".agents/guardian.log", "g", 0):
                    if re.search(r"killing|stale|gave up|crash|failed|error|leaving it", l): msgs.append("guardian: " + l[:200])
                for l in new_lines(here / "docs/WORK_LOG.md", "w", 0): msgs.append("log: " + l[:260])
                xs = sorted((here / "_appdata_/logs").glob("xray_*.log"), key=os.path.getmtime)
                if xs:
                    for l in new_lines(xs[-1], "x", 0):
                        if "WALK LEARNED" in l: msgs.append("**walker learned:** " + l.split("WALK LEARNED", 1)[-1].strip()[:200])
                        elif "WALK skip waypoint" in l: msgs.append("walker gave up a waypoint: " + l.split("WALK skip", 1)[-1].strip()[:120])
                if st["digest"] and time.time() - st["last_digest"] > 3600: st["last_digest"] = time.time(); msgs.append(status_text())
            except Exception as e: msgs.append(f"(bot error: {e})")
            if msgs and time.time() > st["mute"] and time.time() - last_sent > 10:
                text = "\n".join(msgs)[:1900]; last_sent = time.time()
                try: await u.send(text)
                except Exception as e: print("send failed", e)
intents = discord.Intents.default(); intents.message_content = True; intents.dm_messages = True
Bot(intents=intents).run(TOKEN)

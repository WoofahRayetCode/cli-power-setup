#!/usr/bin/env python3
"""guardian: one small supervisor that notices when things this setup depends on have died or got stuck, and recovers them. Runs as the systemd user service
`stalker-guardian` (Restart=always), so it is itself supervised. Log: .agents/guardian.log   status: guardian.py status
Checks every 30 s (each recovery is rate-limited to 4 per hour; past that it only logs and writes the 'needs you' line):
  sysguard            the job supervisor (python3 tools/sysguard.py run)              -> start it
  statusweb           the phone dashboard on :8765 must answer                           -> restart it
  joplin_watchdog     keeps Joplin alive                                                  -> start it
  agy-autosend     the prompt watcher for the kitty window (only while that window exists) -> start it
  nightwalk           the OGSR overnight tour, wanted while .agents/nightwalk.want exists and no EE session / stop file -> start it
  frozen game         the OGSR game whose newest log has not changed for 8 minutes      -> kill it (the night walk moves on)
  wine crash windows  notepad.exe opened by Wine to show an xray crash log               -> close it
  hung screenshots    `import -window` / spectacle older than 90 s                        -> kill
  stale EE session    /tmp/ee_session.env older than 90 min, or no EE game window for 5 min while it exists -> tools/ee_session.sh stop (restores user.ltx, removes the test mod, resumes the night walk)"""
import glob, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
here = Path(__file__).resolve().parent.parent; os.chdir(here)
LOG, STATE = here / ".agents/guardian.log", here / ".agents/guardian.json"
def say(m): open(LOG, "a").write(time.strftime("%F %T ") + m + "\n")
def sh(c, t=20):
    try: return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=t).stdout.strip()
    except Exception: return ""
def alive(pat): return bool(sh(f"pgrep -f '^(/usr/bin/|/bin/)?(python3|bash) ([^ ]+ )*([^ ]*/)?{pat}' | head -1"))   # anchored at the start of the command line: a shell that merely MENTIONS the pattern does not match
def load():
    try: return json.loads(STATE.read_text())
    except Exception: return {}
def allowed(st, name):
    try:
        import importlib.util as _u; sp = _u.spec_from_file_location("self_improve", here / "tools/self_improve.py"); m = _u.module_from_spec(sp); sp.loader.exec_module(m); m.note(name, "recovery needed")   # the self-improve loop learns from these
    except Exception: pass
    now = time.time(); st[name] = [t for t in st.get(name, []) if now - t < 3600]
    if len(st[name]) >= 4:
        if len(st[name]) == 4: say(f"{name}: 4 recoveries this hour, leaving it"); (here / ".agents/needs_you.txt").write_text(f"Guardian gave up on {name} for this hour (see .agents/guardian.log).\n"); st[name].append(now)
        return False
    st[name].append(now); return True
def spawn(cmd): subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
def game_pids(): return [int(p) for p in sh("pgrep -f '[x]rEngine.exe'").split()]
def ee_window():
    return bool(sh("for w in $(xprop -root _NET_CLIENT_LIST 2>/dev/null | grep -o '0x[0-9a-f]*'); do xprop -id $w WM_CLASS 2>/dev/null; done | grep -c steam_app_2427") not in ("", "0"))
def ogsr_pids(): return [int(p) for p in sh("pgrep -f 'ogsr-complete-merge.bin_x64.xrEngine[.]exe'").split()]   # the OGSR game only: the EE engines write their log at exit, so a quiet log means nothing there
def newest_log_age():
    fs = list((here / "_appdata_/logs").glob("xray_*.log"))
    return min((time.time() - f.stat().st_mtime for f in fs), default=9e9)
def tick(st):
    ee = Path("/tmp/ee_session.env")
    if not alive("tools/sysguard.py run") and allowed(st, "sysguard"): say("sysguard missing: starting"); spawn("python3 tools/sysguard.py run >> .agents/sysguard.out 2>&1")
    tok = sh("cat ~/.cache/statusweb/token")
    try: urllib.request.urlopen(f"http://127.0.0.1:8765/api?t={tok}", timeout=8).read(); web = True
    except Exception: web = False
    if not web and allowed(st, "statusweb"): say("statusweb not answering: restarting"); sh("pkill -f '^python3 tools/statusweb.py run'"); time.sleep(1); spawn("python3 tools/statusweb.py run > .agents/job_statusweb.log 2>&1")
    if not alive("tools/joplin_watchdog.py run") and allowed(st, "joplin_watchdog"): say("joplin_watchdog missing: starting"); spawn("python3 tools/joplin_watchdog.py run")
    if Path("/tmp/kitty-yolo").exists() and sh("kitten @ --to unix:/tmp/kitty-yolo ls --match id:1 2>/dev/null | head -c 5") and not alive("agy-autosend daemon") and allowed(st, "autosend"):
        say("agy-autosend watcher missing: starting"); spawn("KITTY_WINDOW_ID=1 KITTY_LISTEN_ON=unix:/tmp/kitty-yolo agy-autosend daemon"); sh("rm -f ~/.cache/agy-autosend/daemon_1.pid")
    want = (here / ".agents/nightwalk.want").exists() and not (here / ".agents/nightwalk.stop").exists()
    if want and not ee.exists() and not alive("tools/nightwalk.sh") and not alive("tools/ee_test.sh") and allowed(st, "nightwalk"):
        say("night walk missing (wanted): starting"); spawn("tools/nightwalk.sh 420 6 > .agents/job_nightwalk.log 2>&1")
    ws = here / "_appdata_/logs/walk_status.txt"      # the "Walker Mind" wireframe window: part of the 3-window setup whenever the status window is open
    if (sh("pgrep -f '^kitty --title STALKER status'") or (ogsr_pids() and ws.exists() and time.time() - ws.stat().st_mtime < 30)) and not alive("tools/walker_mind.py"): spawn("python3 tools/walker_mind.py --keep"); sh("sleep 3; tools/layout.sh")
    if ogsr_pids() and ws.exists() and time.time() - ws.stat().st_mtime < 30 and not alive("tools/walker_collect.py"): spawn("python3 tools/walker_collect.py")      # training data + report
    if ogsr_pids() and not ee.exists() and newest_log_age() > 480 and allowed(st, "frozen"):
        say("game log silent for 8 min: killing the game"); [os.kill(p, 15) for p in ogsr_pids()]; time.sleep(8); [os.kill(p, 9) for p in ogsr_pids()]
    # stalled game: the engine still draws frames (log keeps getting FRAMEWAIT lines) but the scripts stopped (ACTORTRACE every 5 s is gone): a modal box such as "Travel to next area?" is waiting for a click
    if ogsr_pids() and not ee.exists():
        try:
            xs = sorted(glob.glob(str(here / "_appdata_/logs/xray_*.log")), key=os.path.getmtime)
            tail = Path(xs[-1]).read_text(errors="ignore")[-60000:].splitlines() if xs else []
            tr = [l for l in tail if "ACTORTRACE" in l]
            if tail and tr and time.time() - Path(xs[-1]).stat().st_mtime < 60:          # the log is still being written (engine alive) ...
                t = time.mktime(time.strptime(re.search(r"\[(\d\d\.\d\d\.\d\d \d\d:\d\d:\d\d)", tr[-1]).group(1), "%d.%m.%y %H:%M:%S"))      # ... but the newest ACTORTRACE is old
                if time.time() - t > 300 and allowed(st, "stalled_game"): say("game stalled (no script activity for 5 min, engine still drawing; probably a modal box): restarting it"); [os.kill(p, 15) for p in ogsr_pids()]; time.sleep(8); [os.kill(p, 9) for p in ogsr_pids()]
        except Exception as e: say(f"stall check error: {e}")
    for pid in sh("pgrep -f 'notepad.exe' ").split():
        if "xray" in sh(f"tr '\\0' ' ' < /proc/{pid}/cmdline 2>/dev/null"): say(f"closing Wine crash window (notepad {pid})"); sh(f"kill {pid}")
    for pid in sh("pgrep -f '^import -window|spectacle -b'").split():
        if float(sh(f"ps -o etimes= -p {pid}") or 0) > 90: say(f"killing hung screenshot process {pid}"); sh(f"kill -KILL {pid}")
    if ee.exists():
        age = time.time() - ee.stat().st_mtime
        if ee_window(): st["ee_seen"] = time.time()
        stale = age > 5400 or (age > 300 and time.time() - st.get("ee_seen", ee.stat().st_mtime) > 300)
        if stale and allowed(st, "ee_session"): say(f"stale EE session ({int(age / 60)} min old): cleaning up"); sh("tools/ee_session.sh stop", t=90)
def extras(st):
    ds = here / "docs/learn/walker_dataset.jsonl"      # GPU trainer: only with no game running, at most every 30 min, when the dataset grew
    if not ogsr_pids() and not game_pids() and ds.exists() and time.time() - st.get("trained", 0) > 1800 and ds.stat().st_size > st.get("trained_size", 0) + 20000 and not alive("tools/offline_trainer.py"):
        st["trained"], st["trained_size"] = time.time(), ds.stat().st_size; spawn("~/.cache/gputrainer/bin/python tools/offline_trainer.py")
    if (Path.home() / ".config/stalker-discord/token").exists() and not sh("pgrep -f '^[^ ]*/discordbot/bin/python[0-9.]* tools/discord_bot.py'") and allowed(st, "discord_bot"): say("discord bot missing: starting"); spawn("~/.cache/discordbot/bin/python tools/discord_bot.py >> .agents/discord_bot.log 2>&1")
    if time.time() - st.get("adb_t", 0) > 60:        # keep the phone's ADB connection (over Tailscale, adb tcpip 5555) alive without the cable
        st["adb_t"] = time.time()
        if "100.67.106.78:5555\tdevice" not in sh("~/Android/Sdk/platform-tools/adb devices", t=8) and "poco" in sh("tailscale status 2>/dev/null | grep -i poco-x8"): sh("timeout 8 ~/Android/Sdk/platform-tools/adb connect 100.67.106.78:5555", t=10)
    # dimmer moved to min-max-idle-bright GUI app (takes place of tools/dimmer.py)
    # if not alive("tools/dimmer.py run") and allowed(st, "dimmer"): say("dimmer missing: starting"); spawn("python3 tools/dimmer.py run")
    if time.time() - st.get("needs_w", 0) > 60: st["needs_w"] = time.time(); spawn("python3 tools/self_improve.py needs")      # new NEEDS YOU lines -> diagnosis + open item
    if time.time() - st.get("self_imp", 0) > 3600: st["self_imp"] = time.time(); spawn("python3 tools/self_improve.py run")
    if time.time() - st.get("ai_ckpt", 0) > 600 and not alive("tools/ckpt_worker.py"): st["ai_ckpt"] = time.time(); spawn("python3 tools/ckpt_worker.py")    # small local model writes the narrative checkpoint
def checkpoint(st):
    # every 5 min: a small machine-written snapshot so a reboot/crash loses at most 5 minutes of "where I was"
    if time.time() - st.get("ckpt", 0) < 300: return
    st["ckpt"] = time.time()
    d = here / ".agents/checkpoints"; d.mkdir(exist_ok=True)
    snap = "\n".join([time.strftime("%F %T"), "uptime: " + sh("uptime -p"), "game: " + ("running" if ogsr_pids() or game_pids() else "not running"),
        "nightwalk.want: " + str((here / ".agents/nightwalk.want").exists()), "ee_session: " + str(Path("/tmp/ee_session.env").exists()),
        "git dirty files: " + sh("git status --porcelain | wc -l"), "last work log:", sh("tail -5 docs/WORK_LOG.md")])
    (d / "auto_latest.txt").write_text(snap + "\n")
def kde_mismatch(st):
    # the running kwin older than the installed kscreenlocker = the lock screen breaks (seen 2026-10-18); keep auto-lock off and shout
    ver = sh("pacman -Q kwin | cut -d' ' -f2"); started = sh("ps -o lstart= -p $(pgrep -x kwin_wayland | head -1)")
    try: t0 = time.mktime(time.strptime(started, "%a %b %d %H:%M:%S %Y"))
    except Exception: return
    up = float(sh("stat -c %Y /usr/bin/kwin_wayland") or 0)
    if up > t0 + 60 and not st.get("mismatch_said"):
        st["mismatch_said"] = True; say(f"kwin {ver} installed after this session started: lock screen may fail, REBOOT/re-login before locking")
        (here / ".agents/needs_you.txt").open("a").write(f"{time.strftime('%F %T')} KDE was updated under a running session: log out/in (or reboot) soon; auto-lock is disabled meanwhile.\n")
def main():
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(sh("tail -8 .agents/guardian.log") or "(no log yet)"); return
    say("guardian started"); st = load()
    while True:
        try: tick(st); extras(st); checkpoint(st); kde_mismatch(st); STATE.write_text(json.dumps(st))
        except Exception as e: say(f"error: {e}")
        time.sleep(30)
main()

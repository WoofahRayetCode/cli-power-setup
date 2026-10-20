#!/usr/bin/env bash
# Re-applies the system-level tweaks made in the 2026-10-18 STALKER/OGSR port sessions after a reset. Idempotent; safe to run twice.
#   scripts/restore-system-tweaks.sh [--force]     --force also overwrites the port project's tools with the snapshots in config/ogsr-port-tools/
# Details of every tweak: docs/SYSTEM_TWEAKS.md.  Nothing here commits or pushes anything.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; force=0; [[ "${1:-}" == "--force" ]] && force=1
PROJECT="${OGSR_PROJECT:-$HOME/Documents/GitHub/ogsr-complete-merge}"; ok() { echo "[✓] $*"; }; skip() { echo "[-] $*"; }
mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications"

# 1. CLI helpers: bgrun (auto-background after N s), claude-yolo (+ opens the right-hand status widget), local-coprocessor (ledger written once)
for b in bgrun claude-yolo claude-autosend local-worker local-coprocessor; do install -m 755 "$here/bin/$b" "$HOME/.local/bin/$b" && ok "bin/$b -> ~/.local/bin"; done

# 2. YOLO launchers: kitty --hold keeps the window open so a startup error stays visible
for d in Claude-Code-YOLO.desktop Claude-Code-YOLO-new.desktop STALKER-Status-Window.desktop; do
  install -m 755 "$here/config/system-tweaks/desktop/$d" "$HOME/.local/share/applications/$d"; [[ -d "$HOME/Desktop" ]] && install -m 755 "$here/config/system-tweaks/desktop/$d" "$HOME/Desktop/$d"; ok "$d"
done; command -v update-desktop-database >/dev/null && update-desktop-database "$HOME/.local/share/applications" 2>/dev/null

# 3. KWin rule: the game window (wm class xrengine) can never steal keyboard focus (focus stealing prevention = Extreme); user clicks / Alt-Tab still work
python3 - "$here"/config/system-tweaks/kde/kwinrule_*.ini <<'PY'
import configparser, os, sys, subprocess
rc = os.path.expanduser("~/.config/kwinrulesrc")
c = configparser.RawConfigParser(); c.optionxform = str; c.read(rc)
if not c.has_section("General"): c.add_section("General")
changed = False
for path in sys.argv[1:]:
    if not path.endswith(".ini"): continue
    s = configparser.RawConfigParser(); s.optionxform = str; s.read(path); sec = s.sections()[0]; desc = s.get(sec, "Description")
    if any(c.has_option(x, "Description") and c.get(x, "Description") == desc for x in c.sections()): print("[-] kwin rule present:", desc); continue
    n = int(c.get("General", "count", fallback="0")) + 1; ids = [x for x in c.get("General", "rules", fallback="").split(",") if x] + [str(n)]
    c.set("General", "count", str(n)); c.set("General", "rules", ",".join(ids)); c.add_section(str(n))
    for k, v in s.items(sec): c.set(str(n), k, v)
    changed = True; print("[✓] kwin rule added:", desc)
if changed:
    with open(rc, "w") as f: c.write(f, space_around_delimiters=False)
    subprocess.run(["qdbus6", "org.kde.KWin", "/KWin", "org.kde.KWin.reconfigure"], capture_output=True)
PY

# 4. Screen off after 60 s on AC (KDE's lowest setting)
if command -v kwriteconfig6 >/dev/null; then kwriteconfig6 --file powerdevilrc --group AC --group Display --key TurnOffDisplayIdleTimeoutSec 60; systemctl --user restart plasma-powerdevil.service 2>/dev/null; ok "screen off 60 s (AC)"; fi

# 5. Speech corrections dictionary (merge, never overwrite what is there)
python3 - "$here/config/system-tweaks/speech_corrections.seed.json" <<'PY'
import json, os, sys
p = os.path.expanduser("~/.claude/speech_corrections.json"); os.makedirs(os.path.dirname(p), exist_ok=True)
cur = json.load(open(p)) if os.path.exists(p) else {"map": {}}; seed = json.load(open(sys.argv[1]))
for k, v in seed["map"].items(): cur.setdefault("map", {}).setdefault(k, v)
json.dump(cur, open(p, "w"), indent=1); print("[✓] speech_corrections merged:", len(cur["map"]), "entries")
PY

# 6. Port project tools (only if the project exists; existing files are kept unless --force)
if [[ -d "$PROJECT/tools" ]]; then
  for f in "$here"/config/ogsr-port-tools/* "$here"/config/system-tweaks/kwin/*; do
    t="$PROJECT/tools/$(basename "$f")"; if [[ ! -e "$t" || $force == 1 ]]; then install -m 755 "$f" "$t" && ok "project tools/$(basename "$f")"; else skip "project tools/$(basename "$f") exists (use --force)"; fi
  done
else skip "port project not found at $PROJECT (set OGSR_PROJECT)"; fi

echo "Not persistent (set per session): laptop 'performance' profile -> laptop_performance_controller.py set-profile performance / wake-mode to revert."

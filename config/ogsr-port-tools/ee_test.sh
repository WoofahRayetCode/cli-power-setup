#!/usr/bin/env bash
# Try a ZoneForge mod in a Steam Enhanced Edition game, windowed 1280x720 like the OGSR test window (never uploads anything).
#   tools/ee_test.sh <soc|cs|cop> <mod folder> [seconds=150]
# Steps: pause the OGSR night walk and free the GPU -> back up the game's user.ltx -> windowed 1280x720 -> `zoneforge test` (copies the mod into <game>/gamedata)
#        -> launch through Steam -> wait, lay the screen out, screenshot, scan the log for script errors -> close the game -> restore user.ltx -> `zoneforge test --undo`
#        -> resume the night walk. Report in docs/ee_tests/<game>_<time>.md.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$here"
game="${1:?soc|cs|cop}"; mod="$(realpath "${2:?mod folder}")"; secs="${3:-150}"; zf="$HOME/Documents/GitHub/zoneforge/.venv/bin/zoneforge"
case "$game" in soc) app=2427410; dir="STALKER Shadow of Chornobyl - EE";; cs) app=2427420; dir="STALKER Clear Sky - EE";; cop) app=2427430; dir="STALKER Call of Prypiat - EE";; *) echo "game?"; exit 2;; esac
G="/mnt/games/SteamLibrary/steamapps/common/$dir"; [[ -d "$G" ]] || { echo "game folder missing: $G"; exit 2; }
out="docs/ee_tests/${game}_$(date +%m%d_%H%M).md"; mkdir -p docs/ee_tests; shot="${out%.md}.png"
log() { echo "$*" | tee -a "$out"; }
echo "# EE test $game $(date)  mod: $mod" > "$out"
pgrep -f "[x]rEngine.exe" >/dev/null && was_ogsr=1 || was_ogsr=0
resume=0
if pgrep -f "bash tools/[n]ightwalk.sh" >/dev/null; then
  log "pausing the OGSR night walk"; resume=1
  kill -KILL $(pgrep -f "bash tools/[n]ightwalk.sh") 2>/dev/null; kill -TERM $(pgrep -f "bash tools/[a]utowalk.sh") 2>/dev/null
  for _ in $(seq 60); do pgrep -f "[x]rEngine.exe" >/dev/null || break; sleep 2; done
fi
pgrep -f "[x]rEngine.exe" >/dev/null && { log "a game is still running; stopping"; exit 3; }
curl -s localhost:11434/api/ps | python3 -c "import sys,json;[print(m['name']) for m in json.load(sys.stdin)['models']]" 2>/dev/null | while read -r m; do ollama stop "$m" >/dev/null 2>&1; done   # free the GPU for the game
U="$(ls -d "$G"/../../compatdata/"$app"/pfx/drive_c/users/steamuser/Saved\ Games/*/STEAM/user.ltx 2>/dev/null | head -1)"   # the file the game REALLY reads (the one in the game folder is a template)
[[ -f "$U" ]] || { log "no user.ltx under compatdata/$app"; exit 2; }
cp -f "$U" "$U.pre_ee_test"                                   # restored at the end
sed -i -e 's/^rs_display_mode .*/rs_display_mode st_display_mode_windowed/' -e 's/^vid_mode .*/vid_mode 1280x720/' "$U"
grep -q '^rs_display_mode' "$U" || echo "rs_display_mode st_display_mode_windowed" >> "$U"
grep -q '^vid_mode' "$U" || echo "vid_mode 1280x720" >> "$U"
log "display ($U): $(grep -E '^(rs_display_mode|vid_mode)' "$U" | tr '\n' ' ')"
"$zf" test --path "$mod" 2>&1 | tail -4 | tee -a "$out"
cleanup() { pkill -TERM -f "[x]rEngine.exe" 2>/dev/null; sleep 6; pkill -KILL -f "[x]rEngine.exe" 2>/dev/null
  cp -f "$U.pre_ee_test" "$U" && rm -f "$U.pre_ee_test"
  "$zf" test --undo --path "$mod" 2>&1 | tail -2 | tee -a "$out"
  (( resume )) && [[ -z "${EE_NO_RESUME:-}" ]] && { log "resuming the night walk"; setsid nohup tools/nightwalk.sh 420 6 > .agents/job_nightwalk.log 2>&1 & }; }
trap cleanup EXIT INT TERM
log "launching appid $app"; steam -applaunch "$app" ${EE_ARGS:-} >/dev/null 2>&1 &   # EE_ARGS e.g. -nointro -start server(l01_escape/single/alife/new) client(localhost)
t0=$(date +%s); wid=""
while (( $(date +%s) - t0 < secs )); do
  sleep 3
  if [[ -z "$wid" ]]; then for w in $(xprop -root _NET_CLIENT_LIST 2>/dev/null | grep -o '0x[0-9a-f]*'); do xprop -id "$w" WM_CLASS 2>/dev/null | grep -q "steam_app_$app" && wid="$w"; done; [[ -n "$wid" ]] && { log "game window $wid after $(( $(date +%s) - t0 )) s"; tools/layout.sh; sleep 4; log "window now: $(tools/wingeo.sh | tr "\n" ";")"; }; fi
done
[[ -n "$wid" ]] && timeout 20 import -window "$wid" "$shot" 2>/dev/null && log "screenshot $shot"
lf="$(ls -t "$G"/../../compatdata/"$app"/pfx/drive_c/users/steamuser/Saved\ Games/*/STEAM/logs/xray.log 2>/dev/null | head -1)"
log "game log: ${lf:-not found}"
[[ -n "$lf" ]] && { log "mod / error lines:"; grep -a -i -E "zf_|\[SWS\]|script|lua|error|assert|rocket" "$lf" | tail -25 | tee -a "$out"; }
"$zf" log "$game" 2>&1 | tail -6 | tee -a "$out"
[[ -n "$wid" ]] || log "RESULT: the game window never appeared within ${secs}s"

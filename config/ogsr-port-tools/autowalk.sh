#!/usr/bin/env bash
# Walk a recorded route in a fresh game, hands-free: tools/autowalk.sh ROUTE [duration=300] [extra hook lines e.g. "stress = 4"]
#   record mode (a person walks, nothing is replayed):  AUTOWALK_RECORD=1 tools/autowalk.sh - 600
# Starts a new game windowed (like level_smoke.sh), the hook gives the god-mode test loadout + [walk]; tools/autoplay.py presses any key at the load
# screen, watches the walker, takes game-window screenshots to docs/walk/, and prints a report. Refuses if the game is already running.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
route="${1:?route name (section in walk_routes.ltx) or -}"; dur="${2:-300}"; extra="${3:-}"
# a previous run may still be shutting down (umu/wine wrapper lingers ~10-20 s): wait for it rather than refuse
for _ in $(seq 90); do pgrep -f "xrEngine[.]exe -nointro" >/dev/null || break; sleep 1; done
if pgrep -f "xrEngine[.]exe -nointro" >/dev/null; then echo "xrEngine already running (90 s wait); refusing"; exit 3; fi
hook="$here/gamedata/config/misc/zz_test_hook.ltx"
# preflight: everything the run needs must exist, or the walker idles and the run tests nothing
pf=0
[[ "$route" != "-" && "$route" != "auto" ]] && ! grep -q "^\[$route\]" "$here/gamedata/config/misc/walk_routes.ltx" 2>/dev/null && { echo "preflight: route [$route] is not in walk_routes.ltx (plan it: tools/navplan.py route $route LEVEL --from=x,y,z --to-poi NAME)"; pf=1; }
[[ -n "${AUTOWALK_TEST:-}" ]] && ! grep -q "^\[$AUTOWALK_TEST\]" "$here/gamedata/config/misc/walk_tests.ltx" 2>/dev/null && { echo "preflight: test [$AUTOWALK_TEST] is not in walk_tests.ltx"; pf=1; }
objs="${AUTOWALK_OBJECTIVES:-}"; for o in ${objs//,/ }; do grep -q "^\[$o\]" "$here/gamedata/config/misc/walk_objectives.ltx" 2>/dev/null || { echo "preflight: objective [$o] is not in walk_objectives.ltx"; pf=1; }; done
[[ -n "${AUTOWALK_CAMPAIGN:-}" ]] && for f in walk_campaign.ltx walk_dialog_hints.ltx; do [[ -f "$here/gamedata/config/misc/$f" ]] || { echo "preflight: $f missing"; pf=1; }; done
[[ -n "${AUTOWALK_LOAD:-}" ]] && [[ ! -f "$here/_appdata_/savedgames/$AUTOWALK_LOAD.sav" ]] && { echo "preflight: save $AUTOWALK_LOAD.sav not found"; pf=1; }
[[ "$route" == "-" && -z "${AUTOWALK_WALK_EXTRA:-}${AUTOWALK_RECORD:-}${AUTOWALK_DUMP:-}${AUTOWALK_CAMPAIGN:-}${AUTOWALK_TEST:-}${AUTOWALK_OBJECTIVES:-}" && -z "$extra" ]] && { echo "preflight: nothing to do (no route, test, objectives, campaign, record or dump)"; pf=1; }
for s in complete_autowalk complete_auto_defense ogsr_complete_compat; do luajit -bl "$here/gamedata/scripts/$s.script" >/dev/null 2>&1 || { echo "preflight: $s.script does not compile"; pf=1; }; done
(( pf )) && exit 4
source "$here/tools/windowed.sh"; windowed_on "$here"
cleanup() { kill -TERM -- -"${launch:-0}" 2>/dev/null || true; sleep 8; kill -KILL -- -"${launch:-0}" 2>/dev/null || true; sleep 2; [[ -f "$hook" && "$(md5sum < "$hook")" == "${hook_sig:-}" ]] && rm -f "$hook"; windowed_off "$here"; }
trap cleanup EXIT INT TERM
{ printf '[test]\ndelay = 8\n'; [[ -n "$extra" ]] && printf '%s\n' "$extra"
  printf '\n[walk]\n'; if [[ -n "${AUTOWALK_RECORD:-}" ]]; then printf 'record = true\n'; else [[ "$route" != "-" ]] && printf 'route = %s\n' "$route"; printf 'start_delay = 6\nsprint = true\n'; [[ -z "${AUTOWALK_TEST:-}" ]] && printf 'limit = %s\n' "$dur"; fi
  [[ -n "${AUTOWALK_WALK_EXTRA:-}" ]] && printf '%s\n' "$AUTOWALK_WALK_EXTRA"   # extra [walk] lines (nightwalk: engage, loot)
  [[ -n "${AUTOWALK_DUMP:-}" ]] && printf 'dump = true\n'
  [[ -n "${AUTOWALK_OBJECTIVES:-}" ]] && printf 'objectives = %s\n' "$AUTOWALK_OBJECTIVES"   # e.g. esc_sid_start (walk_objectives.ltx)
  [[ -n "${AUTOWALK_TEST:-}" ]] && printf 'test = %s\n' "$AUTOWALK_TEST"                       # walk_tests.ltx: goal + rules + pass criteria
  [[ -n "${AUTOWALK_CAMPAIGN:-}" ]] && printf 'campaign = true\nengage = defend\nloot = true\n'   # play the story (walk_campaign.ltx)
  [[ -n "${AUTOWALK_ENDING:-}" ]] && printf 'ending = %s\n' "$AUTOWALK_ENDING"; }  > "$hook"       # which ending to go for (tools/endings.sh)
hook_sig=$(md5sum < "$hook")
rm -f "$here"/_appdata_/logs/*.log "$here"/_appdata_/logs/walk_status.txt "$here"/_appdata_/logs/walk_pause.txt "$here"/_appdata_/logs/walk_request.txt "$here"/_appdata_/logs/walk_route_dyn.txt "$here"/docs/walk/ev_*.png "$here"/docs/walk/walk_*.png; mkdir -p "$here/docs/walk"   # one run per folder state
export PROTONPATH="${PROTONPATH:-$HOME/.local/share/Steam/compatibilitytools.d/GE-Proton11-7-x86_64}"
( cd "$here" && exec setsid ./play.sh -nointro -skipgameintro -precache_frames 6 -noclipcursor -start "server(${AUTOWALK_LOAD:-all}/single/alife/$([[ -n "${AUTOWALK_LOAD:-}" ]] && echo load || echo new))" client\(localhost\) >"$here/_appdata_/boot_stdout.txt" 2>&1 ) &
launch=$!
python3 "$here/tools/autoplay.py" --duration "$dur" --shots "${AUTOWALK_SHOTS:-30}" --stop-on-done

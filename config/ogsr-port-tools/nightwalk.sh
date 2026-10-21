#!/usr/bin/env bash
# Unattended overnight tour: the auto walker (route = auto) walks every level's offline-planned coverage tour while auto insanity runs, the crash watcher
# fixes / analyses crashes, and a morning report lands in docs/night/.   tools/nightwalk.sh [stay_seconds=420] [max_hours=8] [levels comma list]
#   stop early: touch .agents/nightwalk.stop        fixer for new crashes: FIX=agy|local|none (default local = Ollama analysis when the game is closed)
# After a crash the next session starts at the level after the last one reached, so every level gets its turn. Tours resume where they stopped.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$here"
stay="${1:-420}"; hours="${2:-8}"
levels="${3:-l01_escape,l02_garbage,l03_agroprom,l03u_agr_underground,l04_darkvalley,l04u_labx18,l05_bar,l06_rostok,l07_military,l08_yantar,l08u_brainlab,l10_radar,l10u_bunker,l11_pripyat,l12_stancia,l12_stancia_2,l12u_control_monolith,l12u_sarcofag}"
IFS=, read -ra LV <<< "$levels"; n=${#LV[@]}
hook=gamedata/config/misc/zz_test_hook.ltx; stop=.agents/nightwalk.stop; rm -f "$stop"
python3 tools/ainav.py info >/dev/null 2>&1 || { echo "level.ai not readable"; exit 2; }
[[ -f gamedata/config/misc/walk_tours.ltx ]] || python3 tools/navsim.py all --episodes 4 >/dev/null
if pgrep -f "[c]rashwatch.py watch" >/dev/null; then cw=0; else python3 tools/crashwatch.py watch --fix "${FIX:-local}" > docs/night/crashwatch.log 2>&1 & cw=$!; fi; trap '[[ $cw -gt 0 ]] && kill $cw 2>/dev/null; rm -f "$hook"; cp "$ltxbak" _appdata_/complete_fun_user.ltx 2>/dev/null' EXIT
ltxbak="$(mktemp)"; cp _appdata_/complete_fun_user.ltx "$ltxbak"
python3 - <<'PY'
p='_appdata_/complete_fun_user.ltx'; lines=open(p).read().splitlines()
kv={l.split(' = ')[0]:l for l in lines if ' = ' in l}
kv.update({'insanity_auto':'insanity_auto = true','insanity_ramp':'insanity_ramp = false','auto_target_fps':'auto_target_fps = 45','autowalk_mode':'autowalk_mode = 0','adaptive_physics':'adaptive_physics = true'})
open(p,'w').write("\n".join([l for l in lines if ' = ' not in l]+list(kv.values()))+"\n")
PY
end=$(( $(date +%s) + hours*3600 )); start_idx=0; session=0
report="docs/night/$(date +%Y%m%d_%H%M).md"; echo "# Night walk $(date)" > "$report"; inbox0=$(wc -l < docs/INBOX.md 2>/dev/null || echo 0)
while (( $(date +%s) < end )) && [[ ! -f "$stop" ]]; do
  session=$((session+1))
  order=(); for ((i=0;i<n;i++)); do order+=("${LV[$(( (start_idx+i) % n ))]}"); done
  lv=$(IFS=,; echo "${order[*]}"); total=$(( n*(stay+30) + 120 ))
  { printf '[test]\ndelay = 8\nlevels = %s\nstay = %s\n\n[walk]\nroute = auto\nstart_delay = 6\nsprint = true\nengage = defend\nloot = false\nlimit = 0\n' "$lv" "$stay"; } > "$hook"
  echo "session $session: $lv (stay ${stay}s, ${total}s max)"
  rm -f _appdata_/logs/*.log
  AUTOWALK_WALK_EXTRA=$'engage = defend\nloot = false' tools/autowalk.sh auto "$total" "levels = $lv
stay = $stay" > "docs/night/session_$session.out" 2>&1
  lf=$(ls -t _appdata_/logs/xray_*.log 2>/dev/null | head -1)
  if [[ -n "$lf" ]]; then
    cp "$lf" "docs/night/session_${session}.log"
    last=$(grep -o "LEVELTOUR arrived [a-z0-9_]*" "$lf" | tail -1 | awk '{print $3}')
    for ((i=0;i<n;i++)); do [[ "${LV[$i]}" == "$last" ]] && start_idx=$(( (i+1) % n )); done
    { echo "## session $session (last level: ${last:-?})"; echo '```'; grep -h "WALK tour progress\|WALK UNSTICK\|WALK aisha leg\|FATAL ERROR\|IDPRESSURE" "$lf" | sed 's/^\[[^]]*\] \[[0-9]*\] //' | sort | uniq -c | sort -rn | head -25
      python3 tools/leveltable.py "$lf" 2>/dev/null | tail -22; echo '```'; } >> "$report"
  fi
  sleep 20
done
echo "done: $report"
{ echo; echo "## new inbox entries during the run"; tail -n +$((inbox0+1)) docs/INBOX.md 2>/dev/null; } >> "$report"

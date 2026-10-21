#!/usr/bin/env bash
# Right-hand status widget for the kitty window running Antigravity (needs allow_remote_control, the YOLO launchers set it).
#   tools/widget.sh          open (once) a ~28% pane on the right: task, needs-you line, ticker, newest night report; refreshes every 5 s, no tokens
#   tools/widget.sh --show   print the panel text once (what the pane runs)
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
show() {
  printf '\e[1;36mSTALKER PORT\e[0m  %s\n\n' "$(date +%H:%M:%S)"
  printf '\e[1mNOW\e[0m\n%s\n\n' "$(fold -s -w 34 "$here/.agents/task.txt" 2>/dev/null)"
  printf '\e[1;33mNEEDS YOU\e[0m\n%s\n\n' "$(fold -s -w 34 "$here/.agents/needs_you.txt" 2>/dev/null)"
  printf '\e[1mTICKER\e[0m\n%s\n\n' "$(fold -s -w 34 "$HOME/.gemini/config/ticker.txt" 2>/dev/null | head -14)"
  printf '\e[1;35mLOCAL WORKERS\e[0m\n%s\n\n' "$(local-worker status 2>/dev/null | cut -c1-46)"
  n=$(ls -t "$here"/docs/night/2*.md 2>/dev/null | head -1); [[ -n "$n" ]] && printf '\e[1mNIGHT\e[0m %s\n%s\n' "$(basename "$n")" "$(grep -E '^l[0-9]' "$n" | tail -5 | cut -c1-34)"
}
if [[ "${1:-}" == "--show" ]]; then show; exit 0; fi
sock="${KITTY_LISTEN_ON:-unix:/tmp/kitty-yolo}"
kitten @ --to "$sock" ls 2>/dev/null | grep -q '"title": "STALKER widget"' && exit 0
kitten @ --to "$sock" launch --type=window --location=vsplit --bias=28 --keep-focus --title "STALKER widget" \
  bash -c "while :; do clear; '$here/tools/widget.sh' --show; sleep 5; done" >/dev/null 2>&1 || { echo "widget: kitty remote control not reachable on $sock (start via the Antigravity YOLO shortcut)"; exit 1; }

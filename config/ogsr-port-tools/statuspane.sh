#!/usr/bin/env bash
# Dedicated status window: the same status line Antigravity shows (agy-token-statusline) plus the STALKER widget text, refreshed every 3 s. Costs no tokens.
#   tools/statuspane.sh           run the refresh loop in THIS terminal
#   tools/statuspane.sh --open    open the "STALKER status" kitty window (through the main window's remote control when available) and lay the screen out
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "${1:-}" == "--open" ]]; then
  # three-window setup: Antigravity terminal + STALKER status + "Walker Mind" (kept open, bottom right); the layout script docks them
  pgrep -f '^python3 .*walker_mind.py' >/dev/null || (setsid nohup python3 "$here/tools/walker_mind.py" --keep >/dev/null 2>&1 &)
  # the status window is its OWN kitty process with its own remote-control socket: that is the only way to change ITS font size (kitty's font command cannot target one window of a
  # shared kitty), so the pane can shrink/grow its text to fit the content without touching the Antigravity terminal.
  if [[ "$("$here/tools/layout_kind.sh")" == dual ]]; then      # two screens: also open the ops log and system monitor terminals (right column of the main screen)
    pgrep -f 'class stalker-ops' >/dev/null || (cd "$here" && setsid nohup kitty --title "Ops log" --class stalker-ops -o font_size=9 -o window_padding_width=4 -o confirm_os_window_close=0 python3 "$here/tools/opslog.py" >/dev/null 2>&1 &)
    pgrep -f 'class stalker-mon' >/dev/null || (cd "$here" && setsid nohup kitty --title "System monitor" --class stalker-mon -o font_size=7 -o window_padding_width=3 -o confirm_os_window_close=0 btop --config "$HOME/.config/btop/stalker-mon.conf" >/dev/null 2>&1 &)
    pgrep -f 'class stalker-mon2' >/dev/null || (cd "$here" && setsid nohup kitty --title "GPU / memory / network / processes" --class stalker-mon2 -o font_size=7 -o window_padding_width=3 -o confirm_os_window_close=0 btop --config "$HOME/.config/btop/stalker-mon2.conf" >/dev/null 2>&1 &)
  fi
  SS=/tmp/kitty-status
  if kitten @ --to "unix:$SS" ls >/dev/null 2>&1; then for d in 0 2; do sleep "$d"; "$here/tools/layout.sh"; done; exit 0; fi
  rm -f "$SS"
  (cd "$here" && STALKER_MAIN_WIN="${STALKER_MAIN_WIN:-${KITTY_WINDOW_ID:-1}}" STALKER_MAIN_SOCK="${KITTY_LISTEN_ON:-unix:/tmp/kitty-yolo}" STALKER_SOCK="unix:$SS" \
    setsid nohup kitty --title "STALKER status" --class stalker-status --listen-on "unix:$SS" -o allow_remote_control=socket-only -o font_size=9 -o window_padding_width=4 -o confirm_os_window_close=0 \
    "$here/tools/statuspane.sh" >/dev/null 2>&1 &)
  sleep 2
  # a freshly opened window can appear a little late: lay the screen out again a few times (each run replaces the previous layout script)
  for d in 0 3 4 5; do sleep "$d"; "$here/tools/layout.sh"; done; exit 0
fi
unset CLAUDE_STATUS_PANE
exec python3 "$here/tools/statuspane.py"

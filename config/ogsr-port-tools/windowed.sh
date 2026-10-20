#!/usr/bin/env bash
# Sourced by the test harness: run the game in a 1280x720 window (so the terminal stays reachable), restore the user's settings afterwards.
# windowed_on  -> backs up _appdata_/user_ogsr.ltx and forces windowed 1280x720
# windowed_off -> restores the backup (call after the game process has exited)
WIN_RES="${TEST_RES:-1280x720}"
windowed_on() {
  local f="$1/_appdata_/user_ogsr.ltx"
  [[ -f "$f" ]] || return 0
  [[ -f "$f.pre_test" ]] || cp "$f" "$f.pre_test"
  local fs=off; [[ -n "${TEST_FULLSCREEN:-}" ]] && fs=on     # TEST_FULLSCREEN=1 TEST_RES=1920x1200 -> real fullscreen
  sed -i -e "s/^vid_mode .*/vid_mode $WIN_RES/" -e "s/^rs_fullscreen .*/rs_fullscreen $fs/" "$f"
  grep -q '^rs_fullscreen' "$f" || echo "rs_fullscreen $fs" >> "$f"
  # hands-free runs: do not stop at "Press any key to play" (synthetic key events are unreliable while the window is not focused)
  if grep -q '^keypress_on_start' "$f"; then sed -i "s/^keypress_on_start .*/keypress_on_start off/" "$f"; else echo "keypress_on_start off" >> "$f"; fi
  "$1/tools/layout.sh" >/dev/null 2>&1   # persistent KWin layout script: game top-left, terminals around it, above the taskbar
  focus_guard_on "$1"   # narrow guard since 2026-10-18: acts only ~2.5 s after a harness key press (press_key.py / gamectl.py take X focus and need it handed back)
  local lj="$1/tools/kwin_layering.js"; qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.unloadScript ogsr_layering >/dev/null 2>&1; lid=$(qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.loadScript "$lj" ogsr_layering 2>/dev/null); [[ -n "$lid" && "$lid" != "-1" ]] && qdbus6 org.kde.KWin "/Scripting/Script$lid" org.kde.kwin.Script.run >/dev/null 2>&1
}
# One-shot focus guard (KWin script): the game window must not pull focus away from what the user is typing in.
focus_guard_on() {
  local js="$1/tools/kwin_focus_guard.js" id
  command -v qdbus6 >/dev/null 2>&1 || return 0
  qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.unloadScript ogsr_focus_guard >/dev/null 2>&1
  id=$(qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.loadScript "$js" ogsr_focus_guard 2>/dev/null)
  [[ -n "$id" && "$id" != "-1" ]] && qdbus6 org.kde.KWin "/Scripting/Script$id" org.kde.kwin.Script.run >/dev/null 2>&1
}
focus_guard_off() {
  command -v qdbus6 >/dev/null 2>&1 || return 0
  qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.unloadScript ogsr_focus_guard >/dev/null 2>&1
}
windowed_off() {
  focus_guard_off
  local f="$1/_appdata_/user_ogsr.ltx"
  [[ -f "$f.pre_test" ]] && { sleep 3; mv -f "$f.pre_test" "$f"; }
}

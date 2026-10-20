#!/usr/bin/env bash
# Print where the game / terminal / status windows are (KWin truth, not X11): tools/wingeo.sh
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; n="ogsr_wingeo_$(date +%s%N)"
id=$(qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.loadScript "$here/tools/kwin_wingeo.js" "$n" 2>/dev/null); [[ -n "$id" && "$id" != "-1" ]] && qdbus6 org.kde.KWin "/Scripting/Script$id" org.kde.kwin.Script.run >/dev/null 2>&1
sleep 1; journalctl --user --since "-4 sec" --no-pager | grep WINGEO | sed 's/.*WINGEO /WINGEO /'; qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.unloadScript "$n" >/dev/null 2>&1

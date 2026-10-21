#!/usr/bin/env bash
# Apply the screen layout (tools/kwin_layout.js): game top-left with a 1280x720 drawing area, Antigravity terminal below it, status window on the right, all above the taskbar.
# The script stays loaded (re-fits when the game window appears or resizes). KWin keeps a stale copy when a script is reloaded under the same name,
# so every run uses a NEW plugin name and unloads the previous one.
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; st=/tmp/ogsr_layout.name
# one run at a time: two overlapping runs left an orphan layout script (single + dual instances then fought over the windows)
exec 9>/tmp/ogsr_layout.lock; flock 9
for old in ogsr_layout ogsr_layout2 $(cat "$st" 2>/dev/null); do qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.unloadScript "$old" >/dev/null 2>&1; done
name="ogsr_layout_$(date +%s)"; echo "$name" > "$st"
# KWin caches a script by its FILE PATH too (an edited kwin_layout.js kept running the old text): always load a fresh copy under a new path
src=kwin_layout.js; [[ "$("$here/tools/layout_kind.sh")" == dual ]] && src=kwin_layout_dual.js        # second screen attached: the two-screen layout
cp "$here/tools/$src" "/tmp/$name.js"; rm -f $(ls -t /tmp/ogsr_layout_*.js 2>/dev/null | tail -n +4)
id=$(qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.loadScript "/tmp/$name.js" "$name" 2>/dev/null); [[ -n "$id" && "$id" != "-1" ]] && qdbus6 org.kde.KWin "/Scripting/Script$id" org.kde.kwin.Script.run >/dev/null 2>&1

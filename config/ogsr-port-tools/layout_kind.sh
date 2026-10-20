#!/usr/bin/env bash
# prints "dual" or "single": which screen layout to use. .agents/layout_mode = auto (default: dual when two screens are enabled) | single | dual
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; m="$(cat "$here/.agents/layout_mode" 2>/dev/null || echo auto)"
case "$m" in single|dual) echo "$m"; exit 0;; esac
n=$(kscreen-doctor -o 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g' | grep -c "^	enabled")
[[ "$n" -ge 2 ]] && echo dual || echo single

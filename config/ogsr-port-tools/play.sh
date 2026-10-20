#!/usr/bin/env bash
# Launch STALKER Complete on OGSR (x64, DX11) through umu-run + GE-Proton.
# First run: ./play.sh --setup   (installs vcrun2022 + d3dcompiler_47 into the prefix)
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export WINEPREFIX="${OGSR_PREFIX:-$HOME/.local/share/ogsr-complete-prefix}"
export PROTONPATH="${PROTONPATH:-GE-Proton11-7}"
# the GE folder may carry an -x86_64 suffix (newer installers); umu wants the folder name
[[ -d "$HOME/.local/share/Steam/compatibilitytools.d/$PROTONPATH" || ! -d "$HOME/.local/share/Steam/compatibilitytools.d/$PROTONPATH-x86_64" ]] || PROTONPATH="$PROTONPATH-x86_64"
export GAMEID="${GAMEID:-umu-ogsr-complete}"
export WINEDLLOVERRIDES="${WINEDLLOVERRIDES:-dbghelp=n,b;dxgi=n,b}"
# Always render on the NVIDIA GPU (never the AMD iGPU or llvmpipe): DXVK only enumerates devices whose name matches
export DXVK_FILTER_DEVICE_NAME="${DXVK_FILTER_DEVICE_NAME:-NVIDIA}"
cd "$here"
"$here/tools/audio_fix.sh" 2>/dev/null || true      # follow the default audio output device
# Performance overlay (MangoHud): FPS, frametime, avg FPS, 1% lows, GPU/CPU use, VRAM, RAM, CPU/GPU power. Disable with NO_OVERLAY=1.
if [[ -z "${NO_OVERLAY:-}" ]] && command -v mangohud >/dev/null 2>&1; then
    export MANGOHUD=1
    export MANGOHUD_CONFIGFILE="${MANGOHUD_CONFIGFILE:-$here/mangohud.conf}"   # tools/bench.sh points this at a copy with logging added
fi
if [[ "${1:-}" == "--setup" ]]; then
    umu-run winetricks -q vcrun2022 d3dcompiler_47
    exit 0
fi
# General crash watch: while the game runs, read + close any Wine crash dialog and file it under docs/crashes/ (NO_CRASHWATCH=1 to disable)
if [[ -z "${NO_CRASHWATCH:-}" ]]; then
    ( sleep 20; while pgrep -f "xrEngine[.]exe -nointro" >/dev/null; do "$here/tools/crash_shot.sh" >/dev/null 2>&1; sleep 6; done ) >/dev/null 2>&1 &
fi
exec umu-run bin_x64/xrEngine.exe "$@"

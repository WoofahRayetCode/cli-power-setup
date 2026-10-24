#!/usr/bin/env bash
# ==============================================================================
# Linux Game Window & Input Capture Helper (game-window-helper)
# Configures Gamescope / Wine pointer capture, borderless windowing,
# and prevents focus stealing during CLI paired development.
# ==============================================================================
set -euo pipefail

usage() {
    cat <<EOF
Usage: $(basename "$0") <command> [args...]

Commands:
  run-gamescope <game_binary> [args...]   Launch game wrapped in sandboxed Gamescope
  configure-wine-mouse <wineprefix>       Configure Wine registry for pointer grab & clipping
  toggle-windowed <user_ltx>              Switch S.T.A.L.K.E.R. user.ltx between fullscreen & windowed
  prevent-focus-stealing                  Configure KWin / X11 to prevent Wine focus stealing
EOF
    exit 1
}

CMD="${1:-}"
shift || usage

case "$CMD" in
    run-gamescope)
        if ! command -v gamescope >/dev/null 2>&1; then
            echo "[✗] gamescope is not installed on this system."
            exit 1
        fi
        echo "[→] Launching game in Gamescope (borderless, grabbed cursor, MangoHud)..."
        exec gamescope -W 1920 -H 1080 -b --grab --force-grab-cursor --mangoapp -- "$@"
        ;;

    configure-wine-mouse)
        PREFIX="${1:-${WINEPREFIX:-$HOME/.wine}}"
        echo "[→] Configuring Wine cursor confinement in prefix: $PREFIX..."
        WINEPREFIX="$PREFIX" wine reg add "HKCU\\Software\\Wine\\X11 Driver" /v GrabPointer /t REG_SZ /d "Y" /f
        WINEPREFIX="$PREFIX" wine reg add "HKCU\\Software\\Wine\\DirectInput" /v MouseWarpOverride /t REG_SZ /d "enable" /f
        echo "[✓] Wine pointer grab & clipping enabled."
        ;;

    toggle-windowed)
        LTX_FILE="${1:-user.ltx}"
        if [ ! -f "$LTX_FILE" ]; then
            echo "[✗] File not found: $LTX_FILE"
            exit 1
        fi
        if grep -q "rs_fullscreen on" "$LTX_FILE"; then
            sed -i 's/rs_fullscreen on/rs_fullscreen off/' "$LTX_FILE"
            echo "[✓] Toggled $LTX_FILE to BORDERLESS / WINDOWED mode (rs_fullscreen off)."
        else
            sed -i 's/rs_fullscreen off/rs_fullscreen on/' "$LTX_FILE"
            echo "[✓] Toggled $LTX_FILE to FULLSCREEN mode (rs_fullscreen on)."
        fi
        ;;

    prevent-focus-stealing)
        echo "[→] Applying KWin focus stealing prevention..."
        if command -v kwriteconfig5 >/dev/null 2>&1; then
            kwriteconfig5 --file kwinrc --group Windows --key FocusStealingPrevention 3
            echo "[✓] KWin focus stealing prevention set to High."
        elif command -v kwriteconfig6 >/dev/null 2>&1; then
            kwriteconfig6 --file kwinrc --group Windows --key FocusStealingPrevention 3
            echo "[✓] KWin 6 focus stealing prevention set to High."
        else
            echo "[!] Non-KDE environment detected. Wine focus isolation handled via Gamescope sandbox."
        fi
        ;;

    *)
        usage
        ;;
esac

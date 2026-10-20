# Screen layout and terminal setup (saved 2026-10-18)

Applied by `tools/layout.sh` (picks `tools/layout_kind.sh`: dual when 2 screens are enabled, else single). The KWin script stays loaded and re-fits windows when the game appears; the guardian re-applies it when the screens or the Stalker Mind / status windows change (`screens_watch` in `tools/guardian.py`).

## Screens
- Main: laptop panel eDP-1, 2560x1600 logical (scale 0.75, mode 1920x1200@144), at 0,0.
- Second: HDMI-A-1, 1920x1080, scale 1, at 2560,0 (logical coordinates).
- `.agents/layout_mode`: `auto` (default) | `single` | `dual`.

## Dual-screen layout (kwin_layout_dual.js), as measured live
| Window | Class | Position / size | Screen |
|---|---|---|---|
| Game (OGSR Engine) | steam_app_* | 0,0 1280x720 (+frame) | main |
| Claude Code YOLO terminal (kitty) | kitty | 0,720 1280x851 (rest of the height) | main |
| Ops log | stalker-ops | 1280,0 1280x260 | main |
| System monitor (all CPU threads) | stalker-mon | 1280,260 1280x340 | main |
| GPU / memory / network / processes | stalker-mon2 | 1280,600 1280x971 | main |
| STALKER status | stalker-status | 2560,0 960x1080 | second |
| Stalker Mind (map, radar, "what he sees", Strelok feed) | stalker-mind | 3520,0 960x1080 | second |

## Single-screen layout (kwin_layout.js, 1920x1200)
Game 1280x720 top-left; Claude terminal 0,720 1280x450; STALKER status 1280,0 640x720; Stalker Mind 1280,720 640x450 (bottom right).

## Terminals / fonts
- kitty config `~/.config/kitty/kitty.conf`: MesloLGM Nerd Font Mono, font_size 11, audio bell off, remote control socket-only.
- Claude terminal: font 10 (restored after an autosize shrank it); never stretched.
- STALKER status is its own kitty process (`--class stalker-status`, socket `/tmp/kitty-status`, auto font size); Ops log `stalker-ops` font 9; monitors `stalker-mon`/`stalker-mon2` font 7.
- Stalker Mind is a Tk window (`tools/stalker_mind.py --keep`); KWin gives focus straight back to the user's window if it ever takes it.

## How to restore
`bash tools/layout.sh` (uses a fresh /tmp script path each time; KWin caches scripts by path). Check with a KWin debug print (journal output lags a few seconds) or `tools/wingeo.sh`.

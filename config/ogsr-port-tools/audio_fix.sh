#!/usr/bin/env bash
# Makes the OGSR game follow the system's DEFAULT audio output instead of a device name saved in its settings (the saved name was an old USB headset: "Speakers (JLab USB Audio Analog Stereo)").
# Run before every launch (play.sh calls it); does nothing while the game is running, because the engine rewrites its settings file when it exits.
f="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/_appdata_/user_ogsr.ltx"
pgrep -f '[x]rEngine.exe' >/dev/null && exit 0
[[ -f "$f" ]] && grep -q '^snd_device_default off' "$f" && sed -i 's/^snd_device_default off/snd_device_default on/' "$f" && echo "audio: game now follows the default output device"
exit 0

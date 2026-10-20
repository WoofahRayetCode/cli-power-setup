#!/usr/bin/env bash
# Where does the sound go? Prints the default output device and where every game audio stream is routed (directly or through EasyEffects); warns when they differ.
def=$(pactl get-default-sink 2>/dev/null); echo "default output: $def"
echo "game streams:"; found=0
for n in "OGSR Engine" "xrEngine" "STALKER"; do
  pw-link -l 2>/dev/null | grep -A3 "^$n.*output_FL" | head -4 | sed 's/^/   /' && found=1
done
route=$(pw-link -l 2>/dev/null | grep -A2 "^ee_soe_output_level:output_FL" | grep -o "alsa_output[^:]*" | head -1)
[[ -n "$route" ]] && echo "EasyEffects output goes to: $route" && [[ "$route" != "$def" ]] && echo "WARNING: EasyEffects is NOT using the default device ($def)"
exit 0

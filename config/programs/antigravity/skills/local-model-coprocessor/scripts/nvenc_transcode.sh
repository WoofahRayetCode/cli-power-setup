#!/usr/bin/env bash
# Hardware-accelerated batch video transcoder using NVIDIA NVENC
set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"
CODEC="${3:-av1}" # av1, hevc, or h264

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo "Usage: $0 <input.mp4> <output.mp4> [av1|hevc|h264]"
    exit 1
fi

ENC="av1_nvenc"
if [ "$CODEC" = "hevc" ]; then ENC="hevc_nvenc"; fi
if [ "$CODEC" = "h264" ]; then ENC="h264_nvenc"; fi

echo "[→] Transcoding $INPUT to $OUTPUT using $ENC (-14 LUFS)..."
ffmpeg -y -hwaccel cuda -i "$INPUT" \
    -c:v "$ENC" -preset p7 -cq 23 \
    -af "loudnorm=I=-14:LRA=7:TP=-1" \
    -c:a aac -b:a 192k -movflags +faststart "$OUTPUT"
echo "[✓] Transcode complete: $OUTPUT"

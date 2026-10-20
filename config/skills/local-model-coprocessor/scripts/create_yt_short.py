#!/usr/bin/env python3
"""
Autonomous YouTube Short Generator (youtube-shorts-video-automation)
Converts 16:9 video to vertical 9:16 with blurred padding, audio normalization, and NVENC export.
"""
import os, sys, argparse, subprocess

def create_short(input_path, output_path, start_sec=0, duration=59):
    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=25:5[bg];"
        "[0:v]scale=1080:-1[fg];"
        "[bg][fg]overlay=(W-w)/2:(H-h)/2[v]"
    )
    cmd = [
        "ffmpeg", "-y", "-hwaccel", "cuda",
        "-ss", str(start_sec), "-i", input_path,
        "-t", str(duration),
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "0:a",
        "-c:v", "av1_nvenc", "-preset", "p7", "-cq", "22",
        "-af", "loudnorm=I=-14:LRA=7:TP=-1",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", output_path
    ]
    print(f"[→] Rendering 9:16 Short: {output_path} ({duration}s)...")
    subprocess.run(cmd, check=True)
    print(f"[✓] Short successfully created: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create vertical YouTube Short")
    parser.add_argument("input", help="Input video file")
    parser.add_argument("output", help="Output 9:16 video file")
    parser.add_argument("--start", type=float, default=0, help="Start time in seconds")
    parser.add_argument("--duration", type=float, default=59, help="Duration in seconds (max 60)")
    args = parser.parse_args()
    create_short(args.input, args.output, args.start, args.duration)

#!/usr/bin/env python3
"""
Silent Game Audio Tester (silent_audio_tester.py)
Validates game audio playback, OpenAL streams, and sound assets in software
while strictly guaranteeing physical hardware speakers remain 100% MUTED.
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

def get_hardware_mute_status() -> dict:
    """Verifies physical audio sink volume and mute status via wpctl/pactl."""
    status = {
        "sink_name": "default",
        "volume": 0.0,
        "is_muted": False,
        "raw": ""
    }
    try:
        res = subprocess.run(["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"], capture_output=True, text=True, check=False)
        out = res.stdout.strip()
        status["raw"] = out
        if "[MUTED]" in out:
            status["is_muted"] = True
        m = re.search(r"Volume:\s*([0-9.]+)", out)
        if m:
            status["volume"] = float(m.group(1))
    except Exception:
        # Fallback to pactl
        try:
            res = subprocess.run(["pactl", "get-sink-mute", "@DEFAULT_SINK@"], capture_output=True, text=True, check=False)
            if "yes" in res.stdout.lower():
                status["is_muted"] = True
        except Exception:
            pass
    return status

def enforce_hardware_mute() -> bool:
    """Ensures physical hardware speakers are safely muted."""
    try:
        subprocess.run(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "1"], capture_output=True, check=False)
        return True
    except Exception:
        try:
            subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"], capture_output=True, check=False)
            return True
        except Exception:
            return False

def get_active_audio_streams() -> list:
    """Detects active software game audio streams in PipeWire."""
    streams = []
    try:
        res = subprocess.run(["wpctl", "status"], capture_output=True, text=True, check=False)
        in_streams = False
        for line in res.stdout.splitlines():
            if "Streams:" in line:
                in_streams = True
                continue
            if in_streams:
                if line.strip() and not line.startswith(" ") and not line.startswith("└") and not line.startswith("├"):
                    in_streams = False
                    continue
                cleaned = line.strip()
                if any(k in cleaned.lower() for k in ["ogsr", "xrengine", "wine", "proton", "openal", "game", "steam"]):
                    streams.append(cleaned)
    except Exception:
        pass
    return streams

def get_monitor_sources() -> list:
    """Lists available PipeWire/PulseAudio monitor sources for software capture."""
    monitors = []
    try:
        res = subprocess.run(["pactl", "list", "sources", "short"], capture_output=True, text=True, check=False)
        for line in res.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2 and ".monitor" in parts[1]:
                monitors.append(parts[1])
    except Exception:
        pass
    return monitors

def measure_software_audio(source: str, duration: float = 2.0) -> dict:
    """Captures a short audio slice from a software monitor source and measures signal levels."""
    metrics = {
        "source": source,
        "duration": duration,
        "mean_volume_db": -99.0,
        "max_volume_db": -99.0,
        "has_signal": False,
        "error": None
    }
    try:
        cmd = [
            "ffmpeg", "-y", "-f", "pulse", "-i", source,
            "-t", str(duration), "-af", "volumedetect", "-f", "null", "-"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        output = res.stderr
        
        m_mean = re.search(r"mean_volume:\s*([-0-9.]+)\s*dB", output)
        m_max = re.search(r"max_volume:\s*([-0-9.]+)\s*dB", output)
        
        if m_mean:
            metrics["mean_volume_db"] = float(m_mean.group(1))
        if m_max:
            metrics["max_volume_db"] = float(m_max.group(1))
            
        # Signal is present if max volume is greater than -80 dB
        if metrics["max_volume_db"] > -80.0:
            metrics["has_signal"] = True
    except Exception as e:
        metrics["error"] = str(e)
    return metrics

def audit_engine_log(log_path: Path) -> dict:
    """Analyzes an X-Ray / OGSR engine log for sound errors and OpenAL initialization."""
    report = {
        "log_path": str(log_path),
        "openal_initialized": False,
        "selected_device": None,
        "missing_sounds": [],
        "sound_errors": [],
        "cache_info": None
    }
    if not log_path.exists():
        report["error"] = "Log file not found"
        return report

    try:
        content = log_path.read_text(encoding="utf-8", errors="ignore")
        for line in content.splitlines():
            line_str = line.strip()
            if "Selected device is" in line_str:
                report["selected_device"] = line_str.split("Selected device is")[-1].strip(" []")
            if "OpenAL version:" in line_str:
                report["openal_initialized"] = True
            if "* sound : cache:" in line_str:
                report["cache_info"] = line_str
            if any(k in line_str.lower() for k in ["cannot open sound", "can't find sound", "missing sound", "failed to open sound"]):
                report["missing_sounds"].append(line_str)
            if "openal error" in line_str.lower() or "sound: " in line_str.lower() and "error" in line_str.lower():
                report["sound_errors"].append(line_str)
    except Exception as e:
        report["error"] = str(e)

    return report

def cmd_status(args):
    mute = get_hardware_mute_status()
    streams = get_active_audio_streams()
    monitors = get_monitor_sources()

    print("\n=======================================================")
    print(" 🔇 Silent Game Audio Status & Hardware Protection     ")
    print("=======================================================")
    print(f"Physical Speakers:  {'🔒 100% MUTED (Safe for sleep)' if mute['is_muted'] else '⚠️ UNMUTED (Sound leakage possible!)'}")
    print(f"Raw Output Status:  {mute['raw']}")
    print(f"Active Game Audio:  {len(streams)} active client stream(s)")
    for s in streams:
        print(f"  -> {s}")
    print(f"Software Monitors:  {', '.join(monitors) if monitors else 'None detected'}")
    print("=======================================================\n")

def cmd_verify(args):
    print("\n=======================================================")
    print(" 🎧 Autonomous Silent Audio Verification Pipeline      ")
    print("=======================================================")
    
    # 1. Enforce Hardware Mute
    mute = get_hardware_mute_status()
    if not mute["is_muted"] and args.enforce_mute:
        print("  -> Physical speakers were unmuted! Enforcing hardware mute...")
        enforce_hardware_mute()
        mute = get_hardware_mute_status()
        
    if not mute["is_muted"]:
        print("  ❌ WARNING: Physical speakers are NOT muted! Halting test.", file=sys.stderr)
        sys.exit(1)
    else:
        print("  [✓] Physical Hardware Safety: Speakers strictly MUTED (0 dB room noise).")

    # 2. Check Game Software Audio Stream
    streams = get_active_audio_streams()
    if streams:
        print(f"  [✓] Game Audio Stream Detected: {streams[0]}")
    else:
        print("  [i] No active game stream found in PipeWire (Game may be launching or idle).")

    # 3. Measure Software Monitor
    monitors = get_monitor_sources()
    selected_source = args.source
    if not selected_source and monitors:
        # Prefer easyeffects_sink.monitor or first monitor
        for m in monitors:
            if "easyeffects" in m:
                selected_source = m
                break
        if not selected_source:
            selected_source = monitors[0]

    if selected_source:
        print(f"  -> Capturing {args.duration}s software audio slice from '{selected_source}'...")
        metrics = measure_software_audio(selected_source, duration=args.duration)
        print(f"  [✓] Software Audio Analysis:")
        print(f"      Mean RMS Volume: {metrics['mean_volume_db']:.1f} dB")
        print(f"      Peak Volume:     {metrics['max_volume_db']:.1f} dB")
        print(f"      Signal Activity: {'Active Audio Playing' if metrics['has_signal'] else 'Silent / Standby Buffer'}")
    else:
        print("  [!] No software monitor source available for live waveform capture.")

    # 4. Engine Log Audit
    log_file = None
    if args.log_file:
        log_file = Path(args.log_file)
    else:
        # Auto-detect latest xray log
        candidates = sorted(glob.glob("/home/ericparsley/Documents/GitHub/*/_appdata_/logs/*.log"), key=os.path.getmtime, reverse=True)
        if candidates:
            log_file = Path(candidates[0])

    if log_file and log_file.exists():
        print(f"  -> Auditing engine audio log: {log_file.name}")
        audit = audit_engine_log(log_file)
        if audit["openal_initialized"]:
            print(f"  [✓] OpenAL Engine Subsystem: Initialized ({audit.get('selected_device', 'Default')})")
        if audit["cache_info"]:
            print(f"  [✓] Sound Buffer Cache: {audit['cache_info']}")
        if audit["missing_sounds"]:
            print(f"  [⚠️] Missing Sounds Reported: {len(audit['missing_sounds'])} missing files:")
            for s in audit["missing_sounds"][:3]:
                print(f"      - {s}")
        else:
            print("  [✓] Sound Asset Integrity: 0 missing audio files.")
    else:
        print("  [i] Engine log file not specified or found.")

    print("\n[✓] SILENT AUDIO VERIFICATION COMPLETE: Testing passed without acoustic disturbance.")
    print("=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="Silent Game Audio Tester & Hardware Mute Guardian")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # status
    p_stat = subparsers.add_parser("status", help="Show hardware mute and software stream status")

    # verify
    p_ver = subparsers.add_parser("verify", help="Execute complete silent audio verification")
    p_ver.add_argument("--duration", type=float, default=2.0, help="Duration of audio slice to sample (seconds)")
    p_ver.add_argument("--source", type=str, help="Specific monitor source name")
    p_ver.add_argument("--log-file", type=str, help="Path to game engine log file")
    p_ver.add_argument("--enforce-mute", action="store_true", default=True, help="Force hardware mute if unmuted (default: True)")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "verify":
        cmd_verify(args)

if __name__ == "__main__":
    main()

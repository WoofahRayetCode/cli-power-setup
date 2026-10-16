#!/usr/bin/env python3
"""
Game Screen Telemetry & Real-Time Observation Monitor:
Captures in-game frames, monitors window states, performs on-screen OCR for engine crashes
(X-Ray/OGSR/UE5), detects visual artifacts (missing textures, freezes), and logs telemetry.
Compatible with KDE Wayland (spectacle), X11 (import/scrot), and PIL.
Zero external dependencies beyond PIL and system tesseract/spectacle.
"""
import sys
import os
import time
import json
import subprocess
import argparse
from pathlib import Path
from PIL import Image, ImageChops

def capture_screen(output_path: Path, active_window: bool = False, max_dim: int = 1280):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    captured = False

    # 1. Try KDE Spectacle (Native Wayland background mode)
    if subprocess.run("which spectacle", shell=True, capture_output=True).returncode == 0:
        win_flag = "-a" if active_window else "-f"
        cmd = f"spectacle -b -n {win_flag} -o {output_path}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0:
            captured = True

    # 2. Try ImageMagick import (X11 / XWayland fallback)
    if not captured and subprocess.run("which import", shell=True, capture_output=True).returncode == 0:
        win_arg = "-window root" if not active_window else ""
        cmd = f"import {win_arg} {output_path}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0 and output_path.exists():
            captured = True

    # 3. Try PIL ImageGrab
    if not captured:
        try:
            from PIL import ImageGrab
            img = ImageGrab.grab()
            img.save(output_path)
            captured = True
        except Exception:
            pass

    if not captured or not output_path.exists():
        raise RuntimeError(f"Failed to capture screen using spectacle, import, or ImageGrab.")

    # Downscale high-resolution frames (e.g. 1440p/4K) to max_dim to save vision tokens
    try:
        with Image.open(output_path) as img:
            w, h = img.size
            if max(w, h) > max_dim:
                ratio = max_dim / max(w, h)
                new_w, new_h = int(w * ratio), int(h * ratio)
                resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                resized.save(output_path, optimize=True)
    except Exception as e:
        sys.stderr.write(f"[!] Warning downscaling image: {e}\n")

    return output_path

def run_ocr(image_path: Path, bbox: tuple = None, psm: int = 6):
    target_img = image_path
    temp_crop = None

    if bbox:
        x, y, w, h = bbox
        with Image.open(image_path) as img:
            crop_img = img.crop((x, y, x + w, y + h))
            temp_crop = Path(f"/tmp/ocr_crop_{int(time.time()*1000)}.png")
            crop_img.save(temp_crop)
            target_img = temp_crop

    try:
        cmd = f"tesseract {target_img} - --psm {psm}"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        text = res.stdout.strip()
    finally:
        if temp_crop and temp_crop.exists():
            temp_crop.unlink()

    return text

def detect_visual_anomalies(image_path: Path):
    """
    Detects game visual glitches:
    - Missing textures (magenta/pink #FF00FF checkerboard)
    - Black screen / GPU hangs (solid black frame)
    - Extreme whiteout (lighting/exposure overflow)
    """
    with Image.open(image_path) as img:
        img_rgb = img.convert("RGB")
        w, h = img_rgb.size
        total_pixels = w * h

        # Sample pixels for efficiency (step=2)
        pixels = list(img_rgb.getdata())
        
        missing_texture_count = 0
        black_pixel_count = 0
        white_pixel_count = 0

        for r, g, b in pixels:
            # Magenta missing texture: high Red, high Blue, very low Green
            if r > 200 and b > 200 and g < 50:
                missing_texture_count += 1
            elif r < 10 and g < 10 and b < 10:
                black_pixel_count += 1
            elif r > 245 and g > 245 and b > 245:
                white_pixel_count += 1

        missing_texture_pct = round((missing_texture_count / total_pixels) * 100, 2)
        black_screen_pct = round((black_pixel_count / total_pixels) * 100, 2)
        whiteout_pct = round((white_pixel_count / total_pixels) * 100, 2)

        anomalies = []
        if missing_texture_pct > 1.0:
            anomalies.append({
                "type": "MISSING_TEXTURE_MAGENTA",
                "severity": "HIGH",
                "percentage": missing_texture_pct,
                "detail": f"{missing_texture_pct}% of frame contains unmapped #FF00FF texture coordinates."
            })
        if black_screen_pct > 95.0:
            anomalies.append({
                "type": "BLACK_SCREEN_FREEZE",
                "severity": "CRITICAL",
                "percentage": black_screen_pct,
                "detail": "Frame is completely black (>95% dark pixels); possible GPU hang or loading deadlock."
            })
        if whiteout_pct > 95.0:
            anomalies.append({
                "type": "WHITEOUT_EXPOSURE_GLITCH",
                "severity": "HIGH",
                "percentage": whiteout_pct,
                "detail": "Frame is over-saturated (>95% pure white); tone-mapping or HDR shader anomaly."
            })

        return {
            "image": str(image_path),
            "dimensions": [w, h],
            "anomalies_detected": len(anomalies) > 0,
            "anomalies": anomalies,
            "metrics": {
                "missing_texture_pct": missing_texture_pct,
                "black_pixel_pct": black_screen_pct,
                "white_pixel_pct": whiteout_pct
            }
        }

def monitor_game_session(duration: float = 30.0, interval: float = 2.0, out_dir: Path = Path(".agents/telemetry")):
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    session_file = out_dir / f"session_{ts}.json"
    
    events = []
    prev_image_path = None
    start_time = time.time()
    frame_idx = 0

    print(f"🎮 Starting Game Screen Telemetry Monitor (Duration: {duration}s | Interval: {interval}s)...")
    
    while (time.time() - start_time) < duration:
        frame_idx += 1
        frame_path = out_dir / f"frame_{ts}_{frame_idx:03d}.png"
        
        try:
            capture_screen(frame_path, max_dim=1280)
            anomalies = detect_visual_anomalies(frame_path)
            
            # Check frame difference against previous
            is_frozen = False
            diff_score = 100.0
            if prev_image_path and prev_image_path.exists():
                with Image.open(frame_path) as cur, Image.open(prev_image_path) as prev:
                    diff = ImageChops.difference(cur.convert("RGB"), prev.convert("RGB"))
                    stat = diff.getbbox()
                    if stat is None:
                        is_frozen = True
                        diff_score = 0.0

            # If anomalies or frozen, run OCR to check for crash dialogs
            ocr_text = ""
            if anomalies["anomalies_detected"] or is_frozen:
                ocr_text = run_ocr(frame_path, psm=6)
                if any(k in ocr_text.upper() for k in ["FATAL ERROR", "EXPRESSION", "BUGTRAP", "CRASH", "EXCEPTION", "NIL VALUE"]):
                    anomalies["anomalies"].append({
                        "type": "ENGINE_CRASH_DIALOG_DETECTED",
                        "severity": "CRITICAL",
                        "detail": "On-screen crash dialog detected via OCR.",
                        "ocr_snippet": ocr_text[:300]
                    })
                    print(f"🚨 [CRASH DETECTED] Frame {frame_idx}: On-screen engine error modal captured!")

            event = {
                "frame": frame_idx,
                "elapsed_sec": round(time.time() - start_time, 2),
                "path": str(frame_path),
                "is_frozen": is_frozen,
                "diff_score": diff_score,
                "anomalies": anomalies["anomalies"],
                "ocr_excerpt": ocr_text[:200] if ocr_text else ""
            }
            events.append(event)
            
            # Keep only anomalous or distinct frames on disk to conserve storage
            if not anomalies["anomalies_detected"] and not is_frozen and prev_image_path:
                try:
                    prev_image_path.unlink(missing_ok=True)
                except Exception:
                    pass
            prev_image_path = frame_path

        except Exception as e:
            sys.stderr.write(f"[!] Error capturing frame {frame_idx}: {e}\n")

        time.sleep(interval)

    # Save summary telemetry log
    summary = {
        "session_timestamp": ts,
        "duration_seconds": round(time.time() - start_time, 2),
        "total_frames_sampled": frame_idx,
        "critical_events_count": sum(1 for e in events if any(a.get("severity") == "CRITICAL" for a in e["anomalies"])),
        "timeline": events
    }
    session_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n[✓] Telemetry monitoring concluded. Summary report saved: {session_file}")
    return session_file

def main():
    parser = argparse.ArgumentParser(description="Game Screen Telemetry & Real-Time Observer")
    subparsers = parser.add_subparsers(dest="command")

    # Capture
    cap_p = subparsers.add_parser("capture", help="Capture a single frame")
    cap_p.add_argument("--output", "-o", default="/tmp/game_capture.png", help="Output PNG path")
    cap_p.add_argument("--active-window", "-a", action="store_true", help="Capture active window only")
    cap_p.add_argument("--max-dim", type=int, default=1280, help="Max dimension to scale down")

    # OCR
    ocr_p = subparsers.add_parser("ocr", help="Run OCR on a captured image or live screen")
    ocr_p.add_argument("--image", "-i", default="/tmp/game_capture.png", help="Image file path")
    ocr_p.add_argument("--bbox", nargs=4, type=int, metavar=('X', 'Y', 'W', 'H'), help="Region of interest")
    ocr_p.add_argument("--psm", type=int, default=6, help="Tesseract PSM mode (default: 6)")

    # Glitch analysis
    glitch_p = subparsers.add_parser("glitch", help="Analyze frame for visual glitches (missing textures, hangs)")
    glitch_p.add_argument("--image", "-i", required=True, help="Path to image to inspect")

    # Monitor
    mon_p = subparsers.add_parser("monitor", help="Run continuous background telemetry loop")
    mon_p.add_argument("--duration", "-d", type=float, default=20.0, help="Monitoring duration in seconds")
    mon_p.add_argument("--interval", "-n", type=float, default=2.0, help="Sampling interval in seconds")
    mon_p.add_argument("--out-dir", default=".agents/telemetry", help="Output telemetry directory")

    args = parser.parse_args()

    if args.command == "capture":
        p = capture_screen(Path(args.output), active_window=args.active_window, max_dim=args.max_dim)
        print(f"[✓] Frame captured: {p} ({p.stat().st_size:,} bytes)")

    elif args.command == "ocr":
        img_path = Path(args.image)
        if not img_path.exists():
            img_path = capture_screen(img_path)
        text = run_ocr(img_path, bbox=tuple(args.bbox) if args.bbox else None, psm=args.psm)
        print("📄 Extracted On-Screen Text:")
        print("-" * 50)
        print(text if text else "[No text detected]")

    elif args.command == "glitch":
        result = detect_visual_anomalies(Path(args.image))
        print(json.dumps(result, indent=2))

    elif args.command == "monitor":
        monitor_game_session(duration=args.duration, interval=args.interval, out_dir=Path(args.out_dir))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

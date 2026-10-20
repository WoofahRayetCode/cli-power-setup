#!/usr/bin/env python3
"""
Cross-Platform Screen Capture & Bounding-Box Cropper (screen-vision-inspector)
Supports Linux (X11, XWayland, Wayland), macOS, and Windows.
"""
import os
import sys
import argparse
import subprocess

def capture_screen(output_path, bbox=None, max_dim=1280):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img = None

    # Method 1: PIL.ImageGrab
    try:
        from PIL import ImageGrab, Image
        img = ImageGrab.grab()
    except Exception:
        img = None

    # Method 2: ImageMagick 'import' (Linux X11/XWayland fallback)
    if img is None:
        try:
            tmp_full = "/tmp/_full_raw_grab.png"
            subprocess.run(["import", "-window", "root", tmp_full], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            from PIL import Image
            img = Image.open(tmp_full)
            os.remove(tmp_full)
        except Exception:
            img = None

    # Method 3: grim (Wayland native fallback)
    if img is None:
        try:
            tmp_full = "/tmp/_grim_raw_grab.png"
            subprocess.run(["grim", tmp_full], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            from PIL import Image
            img = Image.open(tmp_full)
            os.remove(tmp_full)
        except Exception:
            img = None

    if img is None:
        print("[!] Error: No available screen capture backend found (PIL.ImageGrab, ImageMagick import, grim).", file=sys.stderr)
        return False

    # Apply crop if bounding box specified: x, y, width, height
    if bbox:
        x, y, w, h = bbox
        img = img.crop((x, y, x + w, y + h))

    # Downscale if exceeding max_dim (token quota preservation)
    if max_dim and (img.width > max_dim or img.height > max_dim):
        ratio = min(max_dim / img.width, max_dim / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

    img.save(output_path, "PNG", optimize=True)
    print(f"[✓] Screen captured: {output_path} ({img.width}x{img.height})")
    return True

def main():
    parser = argparse.ArgumentParser(description="Autonomous Screen Vision Capture Tool")
    parser.add_argument("--output", "-o", default="/tmp/screen_capture.png", help="Output file path (default: /tmp/screen_capture.png)")
    parser.add_argument("--bbox", nargs=4, type=int, metavar=('X', 'Y', 'W', 'H'), help="Crop to bounding box")
    parser.add_argument("--max-dim", type=int, default=1280, help="Downscale image to max dimension for token savings (default: 1280)")
    args = parser.parse_args()

    success = capture_screen(args.output, args.bbox, args.max_dim)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

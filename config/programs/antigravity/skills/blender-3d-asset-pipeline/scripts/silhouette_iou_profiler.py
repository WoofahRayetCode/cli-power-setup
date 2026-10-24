#!/usr/bin/env python3
"""
silhouette_iou_profiler.py: Local CPU/RAM 2D Drawing Contour Slice Extractor & 3D Silhouette IoU Verifier.
Extracts mathematical height-slice width profiles and color swatches from 2D concept art/drawings,
and computes Intersection-over-Union (IoU) overlap against rendered 3D views.
"""

import argparse
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image


def extract_foreground_mask(img: Image.Image) -> np.ndarray:
    rgba = np.array(img.convert("RGBA"))
    alpha = rgba[..., 3]
    if np.min(alpha) < 240 and np.max(alpha) > 15:
        # Image has meaningful alpha channel
        return alpha > 32
    # Otherwise estimate background color from the 4 corner pixels
    rgb = rgba[..., :3].astype(np.float32)
    corners = np.array([rgb[0, 0], rgb[0, -1], rgb[-1, 0], rgb[-1, -1]])
    bg_color = np.median(corners, axis=0)
    dist = np.linalg.norm(rgb - bg_color, axis=-1)
    return dist > 22.0


def cmd_profile(image_path: str, num_slices: int, json_out: str | None) -> None:
    img = Image.open(image_path)
    mask = extract_foreground_mask(img)
    ys, xs = np.where(mask)
    if len(ys) == 0:
        print("[✗] Could not detect foreground subject in image.", file=sys.stderr)
        sys.exit(1)

    y_min, y_max = int(ys.min()), int(ys.max())
    x_min, x_max = int(xs.min()), int(xs.max())
    bbox_h = max(1, y_max - y_min)
    bbox_w = max(1, x_max - x_min)
    aspect_hw = round(bbox_h / float(bbox_w), 4)

    slices = []
    for i in range(num_slices):
        t = i / float(max(1, num_slices - 1))
        # t=0.0 is bottom (feet), t=1.0 is top (head/ears)
        row_y = int(round(y_max - t * bbox_h))
        row_y = max(y_min, min(y_max, row_y))
        row_xs = np.where(mask[row_y])[0]
        if len(row_xs) > 0:
            left = (float(row_xs.min()) - x_min) / bbox_w
            right = (float(row_xs.max()) - x_min) / bbox_w
            center = round((left + right) * 0.5 - 0.5, 4)
            half_width = round((right - left) * 0.5, 4)
        else:
            center, half_width = 0.0, 0.0
        slices.append({"height_t": round(t, 3), "x_center": center, "half_width": half_width})

    # Extract dominant color swatches inside foreground mask via quantized palette
    rgba = np.array(img.convert("RGBA"))
    fg_pixels = rgba[mask][..., :3]
    fg_img = Image.fromarray(fg_pixels.reshape(1, -1, 3).astype(np.uint8)).quantize(colors=8)
    palette = fg_img.getpalette()[:24]
    hex_swatches = [
        f"#{palette[i]:02x}{palette[i+1]:02x}{palette[i+2]:02x}"
        for i in range(0, len(palette), 3)
    ]

    result = {
        "source_image": str(Path(image_path).resolve()),
        "bbox_pixels": {"width": bbox_w, "height": bbox_h, "height_to_width_ratio": aspect_hw},
        "dominant_hex_palette": hex_swatches,
        "vertical_slices": slices,
    }
    if json_out:
        Path(json_out).write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"[✓] Saved {num_slices}-slice mathematical contour profile -> {json_out} (H/W={aspect_hw})")
    else:
        print(json.dumps(result, indent=2))


def crop_to_subject(mask: np.ndarray, size: tuple[int, int] = (512, 512)) -> np.ndarray:
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return np.zeros(size, dtype=bool)
    cropped = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    pil_m = Image.fromarray((cropped * 255).astype(np.uint8)).resize(size, Image.Resampling.NEAREST)
    return np.array(pil_m) > 127


def cmd_compare(ref_path: str, render_path: str, diff_out: str | None) -> None:
    m_ref = crop_to_subject(extract_foreground_mask(Image.open(ref_path)))
    m_ren = crop_to_subject(extract_foreground_mask(Image.open(render_path)))

    inter = np.logical_and(m_ref, m_ren).sum()
    union = np.logical_or(m_ref, m_ren).sum()
    iou = float(inter) / float(max(1, union))

    if diff_out:
        vis = np.zeros((512, 512, 3), dtype=np.uint8)
        vis[np.logical_and(m_ref, m_ren)] = [40, 220, 80]      # Green = Matched silhouette
        vis[np.logical_and(m_ref, ~m_ren)] = [230, 50, 50]     # Red   = Missing 3D volume (needs expansion)
        vis[np.logical_and(~m_ref, m_ren)] = [60, 120, 240]    # Blue  = Excess 3D volume (needs slimming)
        Image.fromarray(vis).save(diff_out)

    status = "PASS (>=0.80)" if iou >= 0.80 else "NEEDS_PROPORTION_TUNING (<0.80)"
    print(f"[IoU Telemetry] Silhouette IoU: {iou:.4f} | Status: {status} | Diff Overlay: {diff_out or 'N/A'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="2D Drawing Contour Profiler & 3D Silhouette IoU Comparator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_prof = sub.add_parser("profile", help="Extract slice width profile and hex palette from 2D drawing")
    p_prof.add_argument("image", help="Path to 2D reference drawing")
    p_prof.add_argument("--slices", type=int, default=32, help="Number of vertical height slices")
    p_prof.add_argument("--json", help="Output JSON path")

    p_cmp = sub.add_parser("compare", help="Compare 2D reference silhouette against 3D rendered view")
    p_cmp.add_argument("reference", help="Path to 2D reference image")
    p_cmp.add_argument("render", help="Path to 3D rendered image")
    p_cmp.add_argument("--diff-out", help="Path to save RGB silhouette mismatch overlay PNG")

    args = parser.parse_args()
    if args.cmd == "profile":
        cmd_profile(args.image, args.slices, args.json)
    elif args.cmd == "compare":
        cmd_compare(args.reference, args.render, args.diff_out)


if __name__ == "__main__":
    main()

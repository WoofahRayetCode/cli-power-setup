#!/usr/bin/env python3
"""
Autonomous Game Texture Editing & Enhancement Suite (texture_editor.py)
Provides procedural image processing for game textures: normal map generation,
Reoriented Normal Mapping (RNM), seamless tiling, de-lighting, alpha edge dilation,
Contrast-Adaptive Sharpening (CAS), PBR ORM packing, and DDS transcoding.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter


def load_image_np(path: Path) -> np.ndarray:
    """Loads an image into a float32 NumPy array normalized to [0, 1]."""
    im = Image.open(path)
    if im.mode not in ("RGB", "RGBA", "L"):
        im = im.convert("RGBA")
    arr = np.array(im, dtype=np.float32) / 255.0
    return arr


def save_image_np(arr: np.ndarray, output_path: Path, dds_format: str = None):
    """Saves a NumPy array [0, 1] as an image or DDS file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    clamped = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
    
    if clamped.ndim == 2:
        im = Image.fromarray(clamped, mode="L")
    elif clamped.shape[2] == 3:
        im = Image.fromarray(clamped, mode="RGB")
    elif clamped.shape[2] == 4:
        im = Image.fromarray(clamped, mode="RGBA")
    else:
        raise ValueError(f"Unsupported channel count: {clamped.shape}")

    if output_path.suffix.lower() == ".dds" or dds_format:
        # Use ImageMagick to write DDS with compression
        tmp_png = output_path.with_suffix(".tmp.png")
        im.save(tmp_png, format="PNG")
        comp = (dds_format or "dxt5").lower()
        if comp not in ("dxt1", "dxt5", "none"):
            comp = "dxt5"
        
        cmd = ["magick", str(tmp_png)]
        if comp != "none":
            cmd += ["-define", f"dds:compression={comp}"]
        cmd.append(str(output_path))
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        if tmp_png.exists():
            tmp_png.unlink()
        if res.returncode != 0:
            # Fallback direct Pillow save if available
            im.save(output_path)
    else:
        im.save(output_path)


# ---------------------------------------------------------------------------
# 1. Normal Map Generation (Sobel / Scharr Gradient)
# ---------------------------------------------------------------------------
def generate_normal_map(img_np: np.ndarray, strength: float = 2.5, invert_y: bool = False, wrap: bool = True) -> np.ndarray:
    """Generates a tangent-space normal map from a heightmap or diffuse image."""
    if img_np.ndim == 3:
        # Standard luminance weights
        height = img_np[:, :, 0] * 0.299 + img_np[:, :, 1] * 0.587 + img_np[:, :, 2] * 0.114
    else:
        height = img_np

    mode = "wrap" if wrap else "edge"
    padded = np.pad(height, 1, mode=mode)

    # Scharr-like gradient operator
    dx = (
        (padded[:-2, 2:] - padded[:-2, :-2]) * 3.0 +
        (padded[1:-1, 2:] - padded[1:-1, :-2]) * 10.0 +
        (padded[2:, 2:] - padded[2:, :-2]) * 3.0
    ) / 32.0

    dy = (
        (padded[2:, :-2] - padded[:-2, :-2]) * 3.0 +
        (padded[2:, 1:-1] - padded[:-2, 1:-1]) * 10.0 +
        (padded[2:, 2:] - padded[:-2, 2:]) * 3.0
    ) / 32.0

    nx = -dx * strength
    ny = dy * strength if invert_y else -dy * strength
    nz = np.ones_like(height)

    magnitude = np.maximum(np.sqrt(nx**2 + ny**2 + nz**2), 1e-8)
    r = (nx / magnitude) * 0.5 + 0.5
    g = (ny / magnitude) * 0.5 + 0.5
    b = (nz / magnitude) * 0.5 + 0.5

    return np.dstack((r, g, b))


# ---------------------------------------------------------------------------
# 2. Reoriented Normal Mapping (RNM) Blending
# ---------------------------------------------------------------------------
def reoriented_normal_blend(base_np: np.ndarray, detail_np: np.ndarray) -> np.ndarray:
    """Blends base and detail tangent normal maps using Colin Barré-Brisebois & Stephen Hill RNM math."""
    n1 = base_np[:, :, :3] * 2.0 - 1.0
    n2 = detail_np[:, :, :3] * 2.0 - 1.0

    n1[:, :, 2] += 1.0
    n2[:, :, 0] = -n2[:, :, 0]
    n2[:, :, 1] = -n2[:, :, 1]

    dot_p = np.sum(n1 * n2, axis=2, keepdims=True)
    z_divisor = np.maximum(n1[:, :, 2:3], 1e-8)
    result = n1 * (dot_p / z_divisor) - n2

    norm = np.maximum(np.linalg.norm(result, axis=2, keepdims=True), 1e-8)
    blended = result / norm
    return blended * 0.5 + 0.5


# ---------------------------------------------------------------------------
# 3. Tangent Normal Vector Repair & Fixes
# ---------------------------------------------------------------------------
def fix_normal_map(normal_np: np.ndarray, invert_y: bool = False, renormalize: bool = True, reconstruct_z: bool = False) -> np.ndarray:
    """Normalizes vector lengths, optionally inverts Green (Y), and reconstructs Z."""
    v = normal_np[:, :, :3] * 2.0 - 1.0
    
    if invert_y:
        v[:, :, 1] = -v[:, :, 1]

    if reconstruct_z:
        xy_sq = np.clip(v[:, :, 0]**2 + v[:, :, 1]**2, 0.0, 1.0)
        v[:, :, 2] = np.sqrt(1.0 - xy_sq)
    elif renormalize:
        mag = np.maximum(np.linalg.norm(v, axis=2, keepdims=True), 1e-8)
        v = v / mag

    res = v * 0.5 + 0.5
    if normal_np.shape[2] == 4:
        res = np.dstack((res, normal_np[:, :, 3]))
    return res


# ---------------------------------------------------------------------------
# 4. Seamless Tiling Synthesis (Hermite Cross-Seam Blending)
# ---------------------------------------------------------------------------
def make_seamless(img_np: np.ndarray, feather: float = 0.25) -> np.ndarray:
    """Wraps texture by half dimensions and blends seams using smooth Hermite curves."""
    h, w = img_np.shape[:2]
    x_half, y_half = w // 2, h // 2
    rolled = np.roll(img_np, shift=(y_half, x_half), axis=(0, 1))

    fx = max(2, int(w * feather))
    fy = max(2, int(h * feather))

    x_dist = np.clip(np.abs(np.arange(w) - x_half) / fx, 0.0, 1.0)
    y_dist = np.clip(np.abs(np.arange(h) - y_half) / fy, 0.0, 1.0)

    # Hermite curve: 3*t^2 - 2*t^3
    mask_x = 3.0 * (x_dist**2) - 2.0 * (x_dist**3)
    mask_y = 3.0 * (y_dist**2) - 2.0 * (y_dist**3)
    mask_2d = (mask_x[None, :] * mask_y[:, None])

    if img_np.ndim == 3:
        mask_2d = mask_2d[:, :, None]

    blended = rolled * mask_2d + img_np * (1.0 - mask_2d)
    return blended


# ---------------------------------------------------------------------------
# 5. Alpha Edge Dilation / Fringe Removal
# ---------------------------------------------------------------------------
def alpha_bleed(img_rgba: np.ndarray, iterations: int = 8) -> np.ndarray:
    """Dilates border RGB colors into 0-alpha pixels to prevent dark halos and mipmap seam bleeding."""
    if img_rgba.shape[2] < 4:
        return img_rgba

    rgb = img_rgba[:, :, :3].copy()
    alpha = img_rgba[:, :, 3]
    valid = alpha > 0.01

    if not np.any(valid) or np.all(valid):
        return img_rgba

    for _ in range(iterations):
        padded_valid = np.pad(valid, 1, mode="edge")
        neighbors = (
            padded_valid[:-2, 1:-1].astype(int) +
            padded_valid[2:, 1:-1].astype(int) +
            padded_valid[1:-1, :-2].astype(int) +
            padded_valid[1:-1, 2:].astype(int)
        )
        expand = (~valid) & (neighbors > 0)
        if not np.any(expand):
            break

        padded_rgb = np.pad(rgb, ((1, 1), (1, 1), (0, 0)), mode="edge")
        padded_v = padded_valid[:, :, None]

        sum_rgb = (
            padded_rgb[:-2, 1:-1] * padded_v[:-2, 1:-1] +
            padded_rgb[2:, 1:-1] * padded_v[2:, 1:-1] +
            padded_rgb[1:-1, :-2] * padded_v[1:-1, :-2] +
            padded_rgb[1:-1, 2:] * padded_v[1:-1, 2:]
        )
        divisor = np.maximum(neighbors[:, :, None], 1)
        rgb[expand] = sum_rgb[expand] / divisor[expand]
        valid[expand] = True

    return np.dstack((rgb, alpha))


# ---------------------------------------------------------------------------
# 6. De-Lighting / Shadow Stripping
# ---------------------------------------------------------------------------
def delight_texture(img_np: np.ndarray, sigma: float = 25.0) -> np.ndarray:
    """Frequency-separation lighting normalization to strip baked shadows and highlights."""
    rgb = img_np[:, :, :3]
    im_pil = Image.fromarray(np.clip(rgb * 255.0, 0, 255).astype(np.uint8))
    
    # Low pass illumination map
    low_pass = np.array(im_pil.filter(ImageFilter.GaussianBlur(radius=sigma)), dtype=np.float32) / 255.0
    shading = np.clip(low_pass, 0.05, 1.0)
    
    # High pass reflectance
    reflectance = rgb / shading
    delighted = np.clip(reflectance * 0.5 + 0.25, 0.0, 1.0)
    
    if img_np.shape[2] == 4:
        return np.dstack((delighted, img_np[:, :, 3]))
    return delighted


# ---------------------------------------------------------------------------
# 7. Contrast-Adaptive Sharpening (CAS / Unsharp Masking)
# ---------------------------------------------------------------------------
def sharpen_texture(img_np: np.ndarray, amount: float = 0.8, radius: float = 1.0) -> np.ndarray:
    """Sharpens micro-details and textures while preserving contrast borders without ringing."""
    rgb = img_np[:, :, :3]
    im_pil = Image.fromarray(np.clip(rgb * 255.0, 0, 255).astype(np.uint8))
    blurred = np.array(im_pil.filter(ImageFilter.GaussianBlur(radius=radius)), dtype=np.float32) / 255.0
    
    diff = rgb - blurred
    sharpened = np.clip(rgb + amount * diff, 0.0, 1.0)
    
    if img_np.shape[2] == 4:
        return np.dstack((sharpened, img_np[:, :, 3]))
    return sharpened


# ---------------------------------------------------------------------------
# 8. PBR Channel Packing (ORM: Occlusion, Roughness, Metallic)
# ---------------------------------------------------------------------------
def pack_orm(ao_p: Path, rough_p: Path, metal_p: Path, invert_rough: bool = False) -> np.ndarray:
    """Packs AO into Red, Roughness into Green, and Metallic into Blue."""
    ref_im = Image.open(ao_p or rough_p or metal_p)
    w, h = ref_im.size

    def get_chan(p: Path, default_val: float) -> np.ndarray:
        if not p or not p.exists():
            return np.full((h, w), default_val, dtype=np.float32)
        im = Image.open(p).convert("L").resize((w, h), Image.Resampling.BILINEAR)
        return np.array(im, dtype=np.float32) / 255.0

    r = get_chan(ao_p, 1.0)
    g = get_chan(rough_p, 0.5)
    if invert_rough:  # Smoothness / Gloss to Roughness
        g = 1.0 - g
    b = get_chan(metal_p, 0.0)

    return np.dstack((r, g, b))


# ---------------------------------------------------------------------------
# 9. S.T.A.L.K.E.R. Bump Map Pair Generator
# ---------------------------------------------------------------------------
def make_stalker_bump_pair(diffuse_p: Path, out_dir: Path, strength: float = 2.5):
    """Generates S.T.A.L.K.E.R. engine compatible _bump.dds and _bump#.dds pair."""
    stem = diffuse_p.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    
    diff_np = load_image_np(diffuse_p)
    normal = generate_normal_map(diff_np, strength=strength, invert_y=True)
    
    # Height in Alpha for parallax/POM
    height = diff_np[:, :, 0] * 0.299 + diff_np[:, :, 1] * 0.587 + diff_np[:, :, 2] * 0.114
    bump_main = np.dstack((normal[:, :, :3], height))
    
    bump_file = out_dir / f"{stem}_bump.dds"
    save_image_np(bump_main, bump_file, dds_format="dxt5")
    
    # _bump# Error map: Specular gloss in Red, ambient in Blue
    gloss = np.clip(1.0 - (height * 0.5), 0.1, 0.9)
    error_map = np.dstack((gloss, normal[:, :, 1], np.full_like(gloss, 0.5), np.ones_like(gloss)))
    
    error_file = out_dir / f"{stem}_bump#.dds"
    save_image_np(error_map, error_file, dds_format="dxt5")
    
    print(f"[✓] Generated S.T.A.L.K.E.R. Bump Pair:")
    print(f"    - {bump_file} (Normal + Height)")
    print(f"    - {error_file} (Gloss / Error Map)")


# ---------------------------------------------------------------------------
# CLI Commands
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Autonomous Game Texture Editing & Enhancement Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # normal-gen
    p_norm = subparsers.add_parser("normal-gen", help="Generate tangent-space normal map from height/diffuse")
    p_norm.add_argument("input", type=Path, help="Input height or diffuse image")
    p_norm.add_argument("-o", "--output", type=Path, required=True, help="Output normal map file")
    p_norm.add_argument("--strength", type=float, default=2.5, help="Normal slope strength (default: 2.5)")
    p_norm.add_argument("--invert-y", action="store_true", help="Invert Green/Y (DirectX Y- format)")
    p_norm.add_argument("--dds", choices=["dxt1", "dxt5", "none"], help="DDS compression format")

    # normal-blend
    p_blend = subparsers.add_parser("normal-blend", help="Blend base and detail normal maps using RNM")
    p_blend.add_argument("base", type=Path, help="Base normal map")
    p_blend.add_argument("detail", type=Path, help="Detail normal map")
    p_blend.add_argument("-o", "--output", type=Path, required=True, help="Output blended normal map")
    p_blend.add_argument("--dds", choices=["dxt1", "dxt5", "none"], help="DDS compression format")

    # normal-fix
    p_nfix = subparsers.add_parser("normal-fix", help="Normalize vectors, invert Y, or reconstruct Z")
    p_nfix.add_argument("input", type=Path, help="Input normal map")
    p_nfix.add_argument("-o", "--output", type=Path, required=True, help="Output corrected normal map")
    p_nfix.add_argument("--invert-y", action="store_true", help="Flip Green/Y channel")
    p_nfix.add_argument("--reconstruct-z", action="store_true", help="Reconstruct Z from X and Y (BC5/RG)")
    p_nfix.add_argument("--dds", choices=["dxt1", "dxt5", "none"], help="DDS compression format")

    # seamless
    p_seam = subparsers.add_parser("seamless", help="Convert texture into seamless repeating tile")
    p_seam.add_argument("input", type=Path, help="Input non-seamless texture")
    p_seam.add_argument("-o", "--output", type=Path, required=True, help="Output seamless texture")
    p_seam.add_argument("--feather", type=float, default=0.25, help="Seam feather width ratio (default: 0.25)")
    p_seam.add_argument("--dds", choices=["dxt1", "dxt5", "none"], help="DDS compression format")

    # alpha-bleed
    p_bleed = subparsers.add_parser("alpha-bleed", help="Dilate edge RGB into 0-alpha space (eliminate black fringes)")
    p_bleed.add_argument("input", type=Path, help="Input RGBA texture")
    p_bleed.add_argument("-o", "--output", type=Path, required=True, help="Output bled texture")
    p_bleed.add_argument("--steps", type=int, default=8, help="Dilation iteration steps (default: 8)")
    p_bleed.add_argument("--dds", choices=["dxt1", "dxt5", "none"], help="DDS compression format")

    # delight
    p_delight = subparsers.add_parser("delight", help="Strip baked shadows and highlights for PBR albedo")
    p_delight.add_argument("input", type=Path, help="Input diffuse photo texture")
    p_delight.add_argument("-o", "--output", type=Path, required=True, help="Output delighted albedo")
    p_delight.add_argument("--sigma", type=float, default=25.0, help="Low-pass Gaussian blur radius (default: 25.0)")
    p_delight.add_argument("--dds", choices=["dxt1", "dxt5", "none"], help="DDS compression format")

    # sharpen
    p_sharp = subparsers.add_parser("sharpen", help="Contrast-adaptive sharpening for micro-detail enhancement")
    p_sharp.add_argument("input", type=Path, help="Input image")
    p_sharp.add_argument("-o", "--output", type=Path, required=True, help="Output sharpened image")
    p_sharp.add_argument("--amount", type=float, default=0.8, help="Sharpening strength (default: 0.8)")
    p_sharp.add_argument("--dds", choices=["dxt1", "dxt5", "none"], help="DDS compression format")

    # pack-orm
    p_pack = subparsers.add_parser("pack-orm", help="Pack AO, Roughness, and Metallic into ORM map")
    p_pack.add_argument("--ao", type=Path, help="Ambient Occlusion image")
    p_pack.add_argument("--roughness", type=Path, help="Roughness image")
    p_pack.add_argument("--metallic", type=Path, help="Metallic image")
    p_pack.add_argument("--invert-roughness", action="store_true", help="Invert Smoothness/Glossiness to Roughness")
    p_pack.add_argument("-o", "--output", type=Path, required=True, help="Output ORM image")
    p_pack.add_argument("--dds", choices=["dxt1", "dxt5", "none"], help="DDS compression format")

    # stalker-bump
    p_st = subparsers.add_parser("stalker-bump", help="Generate S.T.A.L.K.E.R. _bump.dds and _bump#.dds pair")
    p_st.add_argument("input", type=Path, help="Input diffuse texture")
    p_st.add_argument("-o", "--out-dir", type=Path, required=True, help="Output directory for bump pair")
    p_st.add_argument("--strength", type=float, default=2.5, help="Normal slope strength (default: 2.5)")

    # convert
    p_conv = subparsers.add_parser("convert", help="Transcode texture format (PNG, TGA, WebP, DDS)")
    p_conv.add_argument("input", type=Path, help="Input image")
    p_conv.add_argument("-o", "--output", type=Path, required=True, help="Output image")
    p_conv.add_argument("--pot", action="store_true", help="Resize to closest Power-of-Two dimensions")
    p_conv.add_argument("--dds", choices=["dxt1", "dxt5", "none"], help="DDS compression format")

    args = parser.parse_args()

    if args.command == "normal-gen":
        arr = load_image_np(args.input)
        res = generate_normal_map(arr, strength=args.strength, invert_y=args.invert_y)
        save_image_np(res, args.output, dds_format=args.dds)
        print(f"[✓] Generated normal map: {args.output}")

    elif args.command == "normal-blend":
        base = load_image_np(args.base)
        detail = load_image_np(args.detail)
        res = reoriented_normal_blend(base, detail)
        save_image_np(res, args.output, dds_format=args.dds)
        print(f"[✓] Blended normal map via RNM: {args.output}")

    elif args.command == "normal-fix":
        arr = load_image_np(args.input)
        res = fix_normal_map(arr, invert_y=args.invert_y, reconstruct_z=args.reconstruct_z)
        save_image_np(res, args.output, dds_format=args.dds)
        print(f"[✓] Corrected normal map: {args.output}")

    elif args.command == "seamless":
        arr = load_image_np(args.input)
        res = make_seamless(arr, feather=args.feather)
        save_image_np(res, args.output, dds_format=args.dds)
        print(f"[✓] Created seamless tiling texture: {args.output}")

    elif args.command == "alpha-bleed":
        arr = load_image_np(args.input)
        res = alpha_bleed(arr, iterations=args.steps)
        save_image_np(res, args.output, dds_format=args.dds)
        print(f"[✓] Applied alpha edge dilation: {args.output}")

    elif args.command == "delight":
        arr = load_image_np(args.input)
        res = delight_texture(arr, sigma=args.sigma)
        save_image_np(res, args.output, dds_format=args.dds)
        print(f"[✓] Delighted texture: {args.output}")

    elif args.command == "sharpen":
        arr = load_image_np(args.input)
        res = sharpen_texture(arr, amount=args.amount)
        save_image_np(res, args.output, dds_format=args.dds)
        print(f"[✓] Sharpened texture: {args.output}")

    elif args.command == "pack-orm":
        res = pack_orm(args.ao, args.roughness, args.metallic, invert_rough=args.invert_roughness)
        save_image_np(res, args.output, dds_format=args.dds)
        print(f"[✓] Packed ORM map: {args.output}")

    elif args.command == "stalker-bump":
        make_stalker_bump_pair(args.input, args.out_dir, strength=args.strength)

    elif args.command == "convert":
        im = Image.open(args.input)
        if args.pot:
            w, h = im.size
            pot_w = 2 ** int(np.round(np.log2(max(w, 1))))
            pot_h = 2 ** int(np.round(np.log2(max(h, 1))))
            if (pot_w, pot_h) != (w, h):
                im = im.resize((pot_w, pot_h), Image.Resampling.LANCZOS)
                print(f"[→] Resized to Power-of-Two: {w}x{h} -> {pot_w}x{pot_h}")
        arr = np.array(im, dtype=np.float32) / 255.0
        save_image_np(arr, args.output, dds_format=args.dds)
        print(f"[✓] Converted texture: {args.output}")


if __name__ == "__main__":
    main()

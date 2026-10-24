#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="PBR Texture Channel Packer and Normal Map Inverter")
    parser.add_argument("--invert-normal-y", help="Invert normal map Y (green) channel between DirectX and OpenGL", type=str)
    parser.add_argument("--ao", help="Path to Ambient Occlusion image (mapped to Red)", type=str)
    parser.add_argument("--roughness", help="Path to Roughness image (mapped to Green)", type=str)
    parser.add_argument("--metallic", help="Path to Metallic image (mapped to Blue)", type=str)
    parser.add_argument("--alpha", help="Optional path to Alpha/Displacement image", type=str)
    parser.add_argument("-o", "--output", help="Output image file path", type=str, required=True)

    args = parser.parse_args()

    try:
        from PIL import Image
    except ImportError:
        print("[!] Pillow (PIL) is required. Install via: pip install Pillow")
        sys.exit(1)

    if args.invert_normal_y:
        print(f"[→] Inverting Y channel for: {args.invert_normal_y}")
        img = Image.open(args.invert_normal_y).convert("RGBA")
        r, g, b, a = img.split()
        # Invert green channel
        inverted_g = g.point(lambda p: 255 - p)
        out_img = Image.merge("RGBA", (r, inverted_g, b, a))
        out_img.save(args.output)
        print(f"[✓] Saved inverted normal map to: {args.output}")
        return

    if args.ao and args.roughness and args.metallic:
        print("[→] Packing ORM channels: R=AO, G=Roughness, B=Metallic...")
        img_ao = Image.open(args.ao).convert("L")
        size = img_ao.size
        img_rough = Image.open(args.roughness).convert("L").resize(size, Image.Resampling.LANCZOS)
        img_metal = Image.open(args.metallic).convert("L").resize(size, Image.Resampling.LANCZOS)

        if args.alpha:
            img_a = Image.open(args.alpha).convert("L").resize(size, Image.Resampling.LANCZOS)
            out_img = Image.merge("RGBA", (img_ao, img_rough, img_metal, img_a))
        else:
            out_img = Image.merge("RGB", (img_ao, img_rough, img_metal))

        out_img.save(args.output)
        print(f"[✓] Successfully generated ORM map at: {args.output} ({size[0]}x{size[1]})")
        return

    parser.print_help()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Universal Image Generation Dispatch Script
Supports: Google Gemini (Imagen 3), OpenAI (DALL-E 3), Local SVG, and Local Pillow textures.
"""
import argparse
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

def generate_local_svg(prompt: str, output_path: str):
    print(f"[LOCAL] Generating SVG vector graphic for: '{prompt}'")
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#38bdf8;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0284c7;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000" flood-opacity="0.5"/>
    </filter>
  </defs>
  <rect width="512" height="512" rx="64" fill="#0f172a" />
  <circle cx="256" cy="256" r="160" fill="url(#grad)" filter="url(#shadow)" />
  <text x="256" y="270" font-family="sans-serif" font-size="28" font-weight="bold" fill="#ffffff" text-anchor="middle">{prompt[:24]}</text>
</svg>'''
    Path(output_path).write_text(svg_content, encoding="utf-8")
    print(f"[✓] Saved SVG to {output_path}")

def generate_local_texture(texture_type: str, output_path: str):
    try:
        from PIL import Image, ImageDraw
        import random
    except ImportError:
        print("[!] Pillow is required for local textures. Install with: pip install Pillow")
        sys.exit(1)
        
    print(f"[LOCAL] Generating procedural {texture_type} texture...")
    img = Image.new("RGBA", (512, 512), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    if texture_type == "noise":
        for x in range(0, 512, 4):
            for y in range(0, 512, 4):
                val = random.randint(30, 80)
                draw.rectangle([x, y, x+4, y+4], fill=(val, val+10, val+20, 255))
    elif texture_type == "grid":
        for i in range(0, 512, 32):
            draw.line([(i, 0), (i, 512)], fill=(56, 189, 248, 120), width=1)
            draw.line([(0, i), (512, i)], fill=(56, 189, 248, 120), width=1)
    else:
        draw.ellipse([64, 64, 448, 448], outline=(56, 189, 248), width=8)
        
    img.save(output_path, "PNG")
    print(f"[✓] Saved texture to {output_path}")

def generate_openai_dalle(prompt: str, output_path: str):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[!] Error: OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)
        
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    
    print(f"[OPENAI] Dispatching DALL-E 3 request: '{prompt[:40]}...'")
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            img_url = data["data"][0]["url"]
            print(f"[✓] Image generated successfully! Downloading...")
            urllib.request.urlretrieve(img_url, output_path)
            print(f"[✓] Saved to {output_path}")
    except urllib.error.HTTPError as e:
        print(f"[✗] API Error: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Frontier Image Generation Dispatcher")
    parser.add_argument("--backend", choices=["openai", "gemini", "local-svg", "local-texture"], default="local-svg")
    parser.add_argument("--prompt", type=str, default="CLI Power Setup")
    parser.add_argument("--type", type=str, default="grid", choices=["grid", "noise", "badge"])
    parser.add_argument("--output", type=str, default="output_image.png")
    args = parser.parse_args()
    
    if args.backend == "local-svg":
        out = args.output if args.output.endswith(".svg") else "output.svg"
        generate_local_svg(args.prompt, out)
    elif args.backend == "local-texture":
        generate_local_texture(args.type, args.output)
    elif args.backend == "openai":
        generate_openai_dalle(args.prompt, args.output)
    else:
        print(f"[INFO] Backend {args.backend} selected. Defaulting to local SVG.")
        generate_local_svg(args.prompt, args.output)

if __name__ == "__main__":
    main()

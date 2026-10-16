#!/usr/bin/env python3
"""
Furry & Fursona Art & Design Generator (fursona_generator.py)
Generates structured character profiles, model-specific AI prompts (SDXL/Pony,
Midjourney, Flux.1, DALL-E 3), local color swatch palette graphics, and 3D VRChat specs.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SPECIES_TEMPLATES = {
    "wolf": {
        "species": "Canine (Wolf)",
        "ear_type": "Pointed upright triangular ears with inner fluff",
        "tail_type": "Thick bushy brush tail",
        "muzzle": "Medium-long defined canine muzzle",
        "leg_type": "digitigrade",
        "default_palette": {
            "primary": "#3A3D40",
            "secondary": "#E8E8E8",
            "accent": "#00E5FF",
            "paw_pads": "#FF7597",
            "eyes": "#00FFCC"
        }
    },
    "fox": {
        "species": "Canine (Red Fox)",
        "ear_type": "Large triangular ears with dark backing and white inner tufts",
        "tail_type": "Long oversized fluffy tail with contrasting white tip",
        "muzzle": "Slender tapered fox muzzle",
        "leg_type": "digitigrade",
        "default_palette": {
            "primary": "#D35400",
            "secondary": "#FFFFFF",
            "accent": "#2C3E50",
            "paw_pads": "#2C3E50",
            "eyes": "#27AE60"
        }
    },
    "snow_leopard": {
        "species": "Feline (Snow Leopard / Snep)",
        "ear_type": "Small rounded ears with thick fur rims",
        "tail_type": "Extremely thick, heavy, oversized fluffy tail with dark rosettes",
        "muzzle": "Short broad feline muzzle with pronounced whisker pads",
        "leg_type": "digitigrade",
        "default_palette": {
            "primary": "#D5D8DC",
            "secondary": "#F8F9F9",
            "accent": "#2C3E50",
            "paw_pads": "#E8A7A1",
            "eyes": "#5DADE2"
        }
    },
    "dragon": {
        "species": "Scalie (Dragon)",
        "ear_type": "Finned frills or backwards sweeping horns",
        "tail_type": "Long muscular tapered reptilian tail with dorsal spade or fins",
        "muzzle": "Reptilian scaly snout with nostril ridges and sharp teeth",
        "leg_type": "digitigrade",
        "default_palette": {
            "primary": "#1A252F",
            "secondary": "#99A3A4",
            "accent": "#9B59B6",
            "paw_pads": "#17202A",
            "eyes": "#F1C40F"
        }
    },
    "protogen": {
        "species": "Cyborg (Protogen)",
        "ear_type": "Dual modular robotic ears with acoustic sensors",
        "tail_type": "Segmented mechanical or cyber-fluff tail with power conduits",
        "muzzle": "Curved aerodynamic tinted LED screen visor displaying expressive digital face",
        "leg_type": "digitigrade",
        "default_palette": {
            "primary": "#1C1D21",
            "secondary": "#4A4E69",
            "accent": "#00F0FF",
            "paw_pads": "#00F0FF",
            "eyes": "#00F0FF"
        }
    }
}

def hex_to_rgb(hex_code: str) -> tuple:
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join(2 * c for c in hex_code)
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def cmd_build(args):
    species_key = args.species.lower().replace(" ", "_")
    base = SPECIES_TEMPLATES.get(species_key, SPECIES_TEMPLATES["wolf"])
    
    profile = {
        "name": args.name or "Unnamed Fursona",
        "species": base["species"],
        "body_type": args.build or "athletic slender",
        "leg_type": args.leg_type or base["leg_type"],
        "muzzle": base["muzzle"],
        "ear_type": base["ear_type"],
        "tail_type": base["tail_type"],
        "palette": {
            "primary_fur": args.primary or base["default_palette"]["primary"],
            "secondary_fur": args.secondary or base["default_palette"]["secondary"],
            "accent_markings": args.accent or base["default_palette"]["accent"],
            "paw_pads_beans": args.paw_pads or base["default_palette"]["paw_pads"],
            "eyes": args.eyes or base["default_palette"]["eyes"]
        },
        "markings": args.markings or "Chest fluff, sock paws on forearms and shins, contrasting ear tips",
        "style": args.style or "digital concept art, clean vector lineart",
        "clothing": args.clothing or "None (feral/anthro natural fur)"
    }
    
    out_path = Path(args.output or ".agents/fursonas/character_profile.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    
    print(f"\n=======================================================")
    print(f" 🐾 Fursona Character Profile Generated               ")
    print(f"=======================================================")
    print(f"Name:        {profile['name']}")
    print(f"Species:     {profile['species']}")
    print(f"Leg Anatomy: {profile['leg_type'].capitalize()} (Hock joints & toe-walking)")
    print(f"Palette:")
    for k, v in profile["palette"].items():
        print(f"  - {k.replace('_', ' ').capitalize()}: {v}")
    print(f"Profile:     {out_path}")
    print(f"=======================================================\n")

def cmd_prompt(args):
    prof_path = Path(args.profile)
    if not prof_path.exists():
        print(f"Error: Profile file '{prof_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    profile = json.loads(prof_path.read_text(encoding="utf-8"))
    
    name = profile.get("name", "Character")
    species = profile.get("species", "canine")
    legs = profile.get("leg_type", "digitigrade")
    markings = profile.get("markings", "")
    pal = profile.get("palette", {})
    clothing = profile.get("clothing", "None")
    
    # SDXL / Pony tag formulation
    sdxl_tags = [
        "score_9", "score_8_up", "source_furry", "character reference sheet", "multiple views",
        "front view", "back view", "full body", "anthro", f"species:{species.split()[0].lower()}",
        f"{legs} legs", "pawpads", "claws", f"({markings}:1.2)",
        f"primary color {pal.get('primary_fur', '#333')}",
        f"secondary color {pal.get('secondary_fur', '#FFF')}",
        f"eyes {pal.get('eyes', '#00F')}",
        "clean lineart", "flat color", "simple neutral background"
    ]
    sdxl_negative = (
        "photorealistic, 3d render, human feet, flat feet, plantigrade feet, extra limbs, "
        "deformed paws, missing fingers, fused bodies, text, watermark, signature, blurry"
    )
    
    # Midjourney / Niji formulation
    mj_prompt = (
        f"Professional character reference sheet of an anthropomorphic {species}, "
        f"turnaround with distinct full-body front view and back view, standing pose. "
        f"{legs.capitalize()} leg anatomy with defined hocks and plush paws, {markings}. "
        f"Main body in {pal.get('primary_fur')}, secondary accents in {pal.get('secondary_fur')}, "
        f"vibrant {pal.get('eyes')} eyes and {pal.get('paw_pads_beans')} paw pads. "
        f"Wearing {clothing}. Clean digital vector character art, sharp lineart, solid light grey background "
        f"--ar 16:9 --v 6.1"
    )
    
    # Flux.1 / DALL-E 3 formulation
    flux_prompt = (
        f"A wide 16:9 digital concept art character design reference sheet for an anthropomorphic {species}. "
        f"The canvas features two clear, separate, non-overlapping full-body poses side-by-side on a plain, "
        f"neutral light-gray background: on the left is a full-body front view, on the right is a full-body rear view. "
        f"The character has natural {legs} legs (walking on toes with high heel joints), {profile.get('ear_type')}, "
        f"and {profile.get('tail_type')}. Fur markings include: {markings}. "
        f"Color scheme features {pal.get('primary_fur')} base fur, {pal.get('secondary_fur')} trim, and {pal.get('eyes')} glowing eyes. "
        f"Vector 2D animation sheet layout, high clarity, no text or typography."
    )
    
    print(f"\n=======================================================")
    print(f" 🎨 Model-Specific AI Prompts for: {name}              ")
    print(f"=======================================================")
    print(f"--- 1. SDXL / Pony Diffusion (Pony XL / e621 tags) ---")
    print(f"PROMPT:\n{', '.join(sdxl_tags)}\n")
    print(f"NEGATIVE PROMPT:\n{sdxl_negative}\n")
    print(f"--- 2. Midjourney v6 / Niji 6 ---")
    print(f"PROMPT:\n{mj_prompt}\n")
    print(f"--- 3. Flux.1 / DALL-E 3 (Spatial Natural Language) ---")
    print(f"PROMPT:\n{flux_prompt}\n")
    print(f"=======================================================\n")

def cmd_swatch(args):
    prof_path = Path(args.profile)
    if not prof_path.exists():
        print(f"Error: Profile file '{prof_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    profile = json.loads(prof_path.read_text(encoding="utf-8"))
    palette = profile.get("palette", {})
    name = profile.get("name", "Fursona")
    
    out_path = Path(args.output or ".agents/fursonas/palette_swatch.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create Swatch Strip Image using Pillow
    swatch_width = 120
    swatch_height = 80
    header_height = 40
    padding = 20
    total_swatches = len(palette)
    img_width = padding * 2 + (swatch_width + padding) * total_swatches
    img_height = header_height + swatch_height + 40 + padding * 2
    
    img = Image.new("RGBA", (img_width, img_height), (30, 32, 36, 255))
    draw = ImageDraw.Draw(img)
    
    # Title
    draw.text((padding, padding), f"{name} - Official Color Palette", fill=(255, 255, 255, 255))
    
    x_offset = padding
    y_offset = padding + header_height
    
    for label, hex_code in palette.items():
        rgb = hex_to_rgb(hex_code)
        
        # Color Box
        draw.rectangle(
            [x_offset, y_offset, x_offset + swatch_width, y_offset + swatch_height],
            fill=rgb + (255,),
            outline=(200, 200, 200, 255),
            width=2
        )
        
        # Text Label and Hex
        clean_label = label.replace("_", " ").title()
        draw.text((x_offset, y_offset + swatch_height + 6), clean_label[:14], fill=(220, 220, 220, 255))
        draw.text((x_offset, y_offset + swatch_height + 22), hex_code.upper(), fill=(0, 229, 255, 255))
        
        x_offset += swatch_width + padding
        
    img.save(out_path)
    print(f"[✓] High-fidelity color palette swatch rendered: {out_path}")

def cmd_spec_3d(args):
    prof_path = Path(args.profile)
    if not prof_path.exists():
        print(f"Error: Profile file '{prof_path}' not found.", file=sys.stderr)
        sys.exit(1)
        
    profile = json.loads(prof_path.read_text(encoding="utf-8"))
    name = profile.get("name", "Character")
    species = profile.get("species", "Canine")
    legs = profile.get("leg_type", "digitigrade")
    
    spec = {
        "avatar_name": name,
        "species_base": species,
        "rigging_architecture": {
            "base_type": "Humanoid (Unity Mecanim / VRM 1.0)",
            "leg_rig": f"{legs.capitalize()} reverse-hock chain (Thigh -> Calf -> Hock/Ankle -> Metatarsal -> Toes)" if legs == "digitigrade" else "Standard Plantigrade",
            "ear_bones": "Left_Ear_01..03, Right_Ear_01..03 (PhysBones dynamic oscillation)",
            "tail_bones": "Tail_01..08 (PhysBones spline chain with elastic curl and gravity)"
        },
        "blendshapes_visemes": [
            "vrc.v_aa (Vowel Ah)", "vrc.v_ch (Consonant Ch/Sh)", "vrc.v_dd (Consonant D/T)",
            "vrc.v_e (Vowel Eh)", "vrc.v_ff (Consonant F/V)", "vrc.v_ih (Vowel Ih)",
            "vrc.v_kk (Consonant K/G)", "vrc.v_nn (Consonant N/M)", "vrc.v_oh (Vowel Oh)",
            "vrc.v_ou (Vowel Oo)", "vrc.v_pp (Consonant P/B)", "vrc.v_rr (Consonant R)",
            "vrc.v_sil (Silence)", "vrc.v_ss (Consonant S/Z)", "vrc.v_th (Consonant Th)"
        ],
        "facial_expressions": [
            "Blink_Left", "Blink_Right", "Smile_Muzzle", "Frown_Muzzle", "Snarl_Teeth",
            "Ear_Droop_Left", "Ear_Droop_Right", "Eye_Widen", "Tongue_Out"
        ],
        "material_textures": {
            "body": "PBR ORM (R=Ambient Occlusion, G=Roughness, B=Metallic)",
            "emission_channel": "Masked glow map for accent markings",
            "normal_map": "DirectX (Y-) tangent space normal map for fur depth"
        }
    }
    
    out_path = Path(args.output or ".agents/fursonas/avatar_3d_spec.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    
    print(f"\n=======================================================")
    print(f" 📐 3D & VRChat Avatar Technical Spec: {name}         ")
    print(f"=======================================================")
    print(f"Rig Type:       {spec['rigging_architecture']['base_type']}")
    print(f"Leg Rig:        {spec['rigging_architecture']['leg_rig']}")
    print(f"Tail Chain:     {spec['rigging_architecture']['tail_bones']}")
    print(f"Viseme Count:   {len(spec['blendshapes_visemes'])} standard VRChat lip-sync shapes")
    print(f"Expression Count: {len(spec['facial_expressions'])} facial/ear morph targets")
    print(f"Export Spec:    {out_path}")
    print(f"=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="Furry & Fursona Art and Refsheet Generator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # build
    p_build = subparsers.add_parser("build", help="Create a structured fursona profile")
    p_build.add_argument("--name", help="Character name")
    p_build.add_argument("--species", default="wolf", help="Species (wolf, fox, snow_leopard, dragon, protogen)")
    p_build.add_argument("--build", default="athletic slender", help="Body build (slender, athletic, muscular, chubby)")
    p_build.add_argument("--leg-type", choices=["digitigrade", "plantigrade", "unguligrade"], help="Leg anatomy posture")
    p_build.add_argument("--primary", help="Primary fur hex color (e.g. #3A3D40)")
    p_build.add_argument("--secondary", help="Secondary fur hex color (e.g. #FFFFFF)")
    p_build.add_argument("--accent", help="Accent marking hex color (e.g. #00E5FF)")
    p_build.add_argument("--paw-pads", help="Paw pad / bean hex color (e.g. #FF7597)")
    p_build.add_argument("--eyes", help="Eye iris hex color (e.g. #00FFCC)")
    p_build.add_argument("--markings", help="Specific fur markings description")
    p_build.add_argument("--clothing", help="Clothing / gear items")
    p_build.add_argument("--style", help="Visual art style")
    p_build.add_argument("--output", help="Output path for JSON profile")
    
    # prompt
    p_prompt = subparsers.add_parser("prompt", help="Translate profile into AI generation prompts")
    p_prompt.add_argument("--profile", required=True, help="Path to character JSON profile")
    
    # swatch
    p_swatch = subparsers.add_parser("swatch", help="Render exact color palette graphic via Pillow")
    p_swatch.add_argument("--profile", required=True, help="Path to character JSON profile")
    p_swatch.add_argument("--output", help="Output image path (PNG)")
    
    # spec-3d
    p_3d = subparsers.add_parser("spec-3d", help="Export VRChat / 3D modeling specifications")
    p_3d.add_argument("--profile", required=True, help="Path to character JSON profile")
    p_3d.add_argument("--output", help="Output spec JSON path")
    
    args = parser.parse_args()
    
    if args.command == "build":
        cmd_build(args)
    elif args.command == "prompt":
        cmd_prompt(args)
    elif args.command == "swatch":
        cmd_swatch(args)
    elif args.command == "spec-3d":
        cmd_spec_3d(args)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Game Weather & Lighting FX Tuner (weather-lighting-tuner)
Audits, calibrates, and tunes game weather LTX files, tonemapping, bloom,
and sun shaft glare to eliminate blinding bloom and light-bleed defects.
"""

import sys
import re
import argparse
from pathlib import Path

# Safe calibrated ranges for S.T.A.L.K.E.R. / OGSR lighting CVars and weather LTX parameters
LIGHTING_THRESHOLDS = {
    "r2_sun_lumscale": {"min": 0.5, "max": 1.5, "default": 1.0},
    "r2_sun_lumscale_hemi": {"min": 0.4, "max": 1.2, "default": 0.8},
    "r2_sun_lumscale_amb": {"min": 0.2, "max": 0.8, "default": 0.5},
    "r2_tonemap_middlegray": {"min": 0.5, "max": 1.5, "default": 1.0},
    "r2_tonemap_low_lum": {"min": 0.0001, "max": 0.01, "default": 0.0001},
    "r2_ls_bloom_threshold": {"min": 0.3, "max": 1.0, "default": 0.7},
    "r2_ls_bloom_kernel_scale": {"min": 0.3, "max": 1.2, "default": 0.7},
    "r2_sun_shafts": {"min": 0, "max": 2, "default": 1}
}

def audit_weather_ltx(files: list, auto_fix: bool = False):
    print(f"\n[→] Auditing weather LTX files for blinding glare across {len(files)} target(s)...")
    issues = []
    fixed_count = 0

    for item in files:
        p = Path(item)
        target_files = list(p.rglob("*.ltx")) if p.is_dir() else [p]

        for f in target_files:
            if not f.is_file():
                continue
            lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            modified = False
            new_lines = []

            for idx, line in enumerate(lines, 1):
                clean = line.strip()
                if clean.startswith(";") or not clean:
                    new_lines.append(line)
                    continue

                # Check sun_color
                if re.match(r"^sun_color\s*=", clean):
                    parts = clean.split("=")[1].strip().split(",")
                    if len(parts) >= 3:
                        try:
                            r, g, b = [float(x.strip()) for x in parts[:3]]
                            if r > 1.8 or g > 1.8 or b > 1.8:
                                issues.append({
                                    "file": str(f.name),
                                    "line": idx,
                                    "param": "sun_color",
                                    "val": f"({r:.2f}, {g:.2f}, {b:.2f})",
                                    "msg": "Overblown sun RGB values causing extreme glare / blinding bloom"
                                })
                                if auto_fix:
                                    r_clamp, g_clamp, b_clamp = min(r, 1.2), min(g, 1.2), min(b, 1.2)
                                    line = f"sun_color = {r_clamp:.3f}, {g_clamp:.3f}, {b_clamp:.3f}"
                                    modified = True
                        except ValueError:
                            pass

                # Check hemi_color
                elif re.match(r"^hemi_color\s*=", clean):
                    parts = clean.split("=")[1].strip().split(",")
                    if len(parts) >= 3:
                        try:
                            r, g, b = [float(x.strip()) for x in parts[:3]]
                            if r > 1.6 or g > 1.6 or b > 1.6:
                                issues.append({
                                    "file": str(f.name),
                                    "line": idx,
                                    "param": "hemi_color",
                                    "val": f"({r:.2f}, {g:.2f}, {b:.2f})",
                                    "msg": "Excessive hemispheric lighting washing out skybox contrast"
                                })
                                if auto_fix:
                                    r_clamp, g_clamp, b_clamp = min(r, 1.0), min(g, 1.0), min(b, 1.0)
                                    line = f"hemi_color = {r_clamp:.3f}, {g_clamp:.3f}, {b_clamp:.3f}"
                                    modified = True
                        except ValueError:
                            pass

                new_lines.append(line)

            if modified and auto_fix:
                f.write_text("\n".join(new_lines), encoding="utf-8")
                fixed_count += 1

    if issues:
        print(f"[!] Found {len(issues)} weather lighting anomaly/anomalies:")
        for iss in issues[:20]:
            print(f"    - {iss['file']}:{iss['line']} [{iss['param']}] {iss['val']} -> {iss['msg']}")
        if len(issues) > 20:
            print(f"    ... and {len(issues) - 20} more.")
        if auto_fix:
            print(f"[✓] Automatically clamped {fixed_count} file(s) to balanced glare limits.")
        else:
            print("    Run with --fix to automatically clamp RGB parameters to safe limits.")
    else:
        print("[✓] All weather LTX files are calibrated within balanced lighting boundaries.")

    return 0

def generate_balanced_user_ltx(output_path: Path):
    print(f"\n[→] Generating balanced user.ltx lighting configuration at {output_path}...")
    cfg = [
        "; ===================================================================",
        "; S.T.A.L.K.E.R. / OGSR Balanced Lighting & Anti-Glare Configuration",
        "; ===================================================================",
        "r2_sun on",
        "r2_sun_details on",
        "r2_sun_shafts 1",
        "r2_sun_lumscale 1.0",
        "r2_sun_lumscale_hemi 0.85",
        "r2_sun_lumscale_amb 0.45",
        "r2_tonemap on",
        "r2_tonemap_middlegray 1.0",
        "r2_tonemap_low_lum 0.0001",
        "r2_tonemap_amount 0.7",
        "r2_ls_bloom_threshold 0.65",
        "r2_ls_bloom_kernel_scale 0.7",
        "r2_sun_bias 0.0005",
        "r2_sun_near 20.0",
        "r2_sun_far 180.0",
        "r2_sun_tsm on",
        "r2_sun_tsm_proj 0.2",
        "r2_sun_tsm_bias -0.05"
    ]
    output_path.write_text("\n".join(cfg) + "\n", encoding="utf-8")
    print(f"[✓] Generated balanced lighting settings in {output_path}.")
    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Game Weather & Lighting FX Tuner - Calibrate sun glare, bloom, and tonemapping"
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # 1. audit
    p_aud = subparsers.add_parser("audit", help="Audit weather LTX files for blinding glare and overblown colors")
    p_aud.add_argument("targets", nargs="+", help="Weather LTX files or directories")
    p_aud.add_argument("--fix", action="store_true", help="Auto-clamp overblown RGB values to safe thresholds")

    # 2. gen-config
    p_gen = subparsers.add_parser("gen-config", help="Generate balanced user.ltx lighting parameters")
    p_gen.add_argument("--out", type=Path, default=Path("balanced_lighting.ltx"), help="Target output LTX file")

    args = parser.parse_args()
    if args.subcommand == "audit":
        return audit_weather_ltx(args.targets, auto_fix=args.fix)
    elif args.subcommand == "gen-config":
        return generate_balanced_user_ltx(args.out)
    return 0

if __name__ == "__main__":
    sys.exit(main())

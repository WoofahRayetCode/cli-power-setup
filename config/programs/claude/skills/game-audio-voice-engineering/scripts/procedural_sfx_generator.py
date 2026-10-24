#!/usr/bin/env python3
import sys
import math
import wave
import struct
import random
import argparse
from pathlib import Path

SAMPLE_RATE = 48000

def generate_samples(preset: str, duration: float = 0.0, base_freq: float = 0.0) -> list[float]:
    samples = []
    
    if preset == "coin":
        dur = duration or 0.18
        total_samples = int(SAMPLE_RATE * dur)
        f1, f2 = base_freq or 987.77, (base_freq or 987.77) * 1.3348 # B5 -> E6
        mid = total_samples // 2
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            f = f1 if i < mid else f2
            env = 1.0 - (i / total_samples) ** 1.5
            val = math.sin(2 * math.pi * f * t) * env
            samples.append(val)

    elif preset == "laser":
        dur = duration or 0.22
        total_samples = int(SAMPLE_RATE * dur)
        start_f = base_freq or 880.0
        end_f = 110.0
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            progress = i / total_samples
            f = start_f * (end_f / start_f) ** progress
            env = (1.0 - progress) ** 0.8
            # Blend sine and square for retro punch
            val = (0.7 * math.sin(2 * math.pi * f * t) + 0.3 * (1.0 if math.sin(2 * math.pi * f * t) > 0 else -1.0)) * env
            samples.append(val)

    elif preset == "explosion":
        dur = duration or 0.8
        total_samples = int(SAMPLE_RATE * dur)
        thump_f = base_freq or 60.0
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            progress = i / total_samples
            env = math.exp(-4.5 * progress)
            noise = random.uniform(-1.0, 1.0)
            thump = math.sin(2 * math.pi * thump_f * t) * math.exp(-8.0 * progress)
            val = (0.75 * noise + 0.5 * thump) * env
            samples.append(val)

    elif preset == "jump":
        dur = duration or 0.22
        total_samples = int(SAMPLE_RATE * dur)
        start_f = base_freq or 150.0
        end_f = 600.0
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            progress = i / total_samples
            f = start_f + (end_f - start_f) * (progress ** 0.8)
            env = math.sin(math.pi * progress) if progress < 0.2 else (1.0 - progress)
            val = math.sin(2 * math.pi * f * t) * env
            samples.append(val)

    elif preset == "hit":
        dur = duration or 0.15
        total_samples = int(SAMPLE_RATE * dur)
        f = base_freq or 120.0
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            progress = i / total_samples
            env = math.exp(-12.0 * progress)
            click = random.uniform(-1.0, 1.0) if i < 150 else 0.0
            thump = math.sin(2 * math.pi * f * t)
            val = (0.8 * thump + 0.4 * click) * env
            samples.append(val)

    elif preset == "ui-click":
        dur = duration or 0.02
        total_samples = int(SAMPLE_RATE * dur)
        f = base_freq or 1400.0
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            progress = i / total_samples
            env = math.exp(-25.0 * progress)
            val = math.sin(2 * math.pi * f * t) * env
            samples.append(val)

    elif preset == "ui-chime":
        dur = duration or 0.6
        total_samples = int(SAMPLE_RATE * dur)
        f1 = base_freq or 523.25 # C5
        f2 = f1 * 1.5           # G5
        f3 = f1 * 2.0           # C6
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            progress = i / total_samples
            env = math.exp(-3.5 * progress)
            val = (0.5 * math.sin(2 * math.pi * f1 * t) + 
                   0.3 * math.sin(2 * math.pi * f2 * t) + 
                   0.2 * math.sin(2 * math.pi * f3 * t)) * env
            samples.append(val)

    elif preset == "powerup":
        dur = duration or 0.45
        total_samples = int(SAMPLE_RATE * dur)
        notes = [330.0, 392.0, 493.88, 587.33, 659.25] # E4, G4, B4, D5, E5
        step_len = total_samples // len(notes)
        for i in range(total_samples):
            t = i / SAMPLE_RATE
            note_idx = min(i // step_len, len(notes) - 1)
            f = notes[note_idx]
            sub_prog = (i % step_len) / step_len
            env = (1.0 - sub_prog * 0.4) * (1.0 - (i / total_samples) * 0.2)
            val = math.sin(2 * math.pi * f * t) * env
            samples.append(val)
    else:
        print(f"[!] Unknown preset: {preset}", file=sys.stderr)
        return []

    return samples

def write_wav(output_path: Path, samples: list[float]):
    # Normalize peak to 0.90 to avoid clipping
    peak = max(abs(s) for s in samples) if samples else 0.0
    scale = (0.90 / peak) if peak > 0 else 1.0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output_path), "wb") as wav_file:
        wav_file.setnchannels(1)      # Mono
        wav_file.setsampwidth(2)     # 16-bit
        wav_file.setframerate(SAMPLE_RATE)
        
        raw_frames = bytearray()
        for s in samples:
            sample_val = int(max(-1.0, min(1.0, s * scale)) * 32767.0)
            raw_frames.extend(struct.pack("<h", sample_val))
            
        wav_file.writeframes(raw_frames)

def main():
    presets = ["coin", "laser", "explosion", "jump", "hit", "ui-click", "ui-chime", "powerup"]
    parser = argparse.ArgumentParser(description="Procedural Audio & SFX Synthesizer")
    parser.add_argument("--preset", choices=presets, default="coin", help="SFX Preset type")
    parser.add_argument("--out", type=Path, default=Path("sfx_output.wav"), help="Output WAV path")
    parser.add_argument("--duration", type=float, default=0.0, help="Override duration in seconds")
    parser.add_argument("--freq", type=float, default=0.0, help="Override base frequency in Hz")
    parser.add_argument("--all", action="store_true", help="Generate all presets into specified folder")

    args = parser.parse_args()

    if args.all:
        out_dir = args.out if args.out.suffix == "" else args.out.parent
        print(f"[→] Generating all {len(presets)} procedural sound effects into: {out_dir}")
        for p in presets:
            samples = generate_samples(p)
            file_path = out_dir / f"{p}.wav"
            write_wav(file_path, samples)
            print(f" [✓] Created: {file_path.name} ({len(samples)} samples, {len(samples)/SAMPLE_RATE*1000:.1f}ms)")
        print(f"[✓] Successfully generated all sound effects.")
        return

    samples = generate_samples(args.preset, args.duration, args.freq)
    if not samples:
        sys.exit(1)

    write_wav(args.out, samples)
    print(f"[✓] Generated procedural SFX '{args.preset}': {args.out} ({len(samples)/SAMPLE_RATE*1000:.1f}ms, {SAMPLE_RATE}Hz 16-bit PCM)")

if __name__ == "__main__":
    main()

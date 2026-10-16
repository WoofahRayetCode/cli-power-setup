---
name: ai-procedural-audio-generation
description: AI-powered and procedural audio generation for game development, content creation, and applications. Covers procedural DSP synthesis (oscillators, envelopes, noise bursts, chiptune/sfxr), text-to-sound-effect (SFX) models, adaptive game soundtrack layering, UI sound design, and loudness normalization.
---

# AI & Procedural Audio Generation

This skill provides architectural pipelines, algorithms, and prompt engineering protocols for generating game sound effects, procedural DSP audio, content creation background scores, and application UI audio cues.

---

## 1. Procedural DSP Audio Synthesis Pipeline

For instant, zero-latency, zero-cost procedural audio generation without external APIs or heavy models:

```text
┌────────────────┐     ┌──────────────┐     ┌──────────────┐     ┌─────────────┐
│ Waveform Gen   │ ──> │ Frequency    │ ──> │ ADSR         │ ──> │ Output WAV  │
│ (Sine/Square/  │     │ Sweep / Mod  │     │ Envelope     │     │ (48kHz/16b) │
│  Saw/Noise)    │     │ (LFO / Pitch)│     │ Shaping      │     │             │
└────────────────┘     └──────────────┘     └──────────────┘     └─────────────┘
```

### Core Mathematical Waveform Primitives
* **Sine Wave (Pristine Tones & Chimes):**
  $$s(t) = A \cdot \sin(2\pi f t)$$
* **Square Wave (Chiptune & 8-bit Retro):**
  $$s(t) = A \cdot 	ext{sgn}(\sin(2\pi f t))$$
* **Sawtooth Wave (Aggressive Synths & Lasers):**
  $$s(t) = 2 A \left( f t - \lfloor f t + 0.5 floor ight)$$
* **Triangle Wave (Soft Bass & Melodies):**
  $$s(t) = 2 A \left| 2 (f t - \lfloor f t + 0.5 floor) ight| - A$$
* **White / Pink Noise (Explosions, Wind, Impacts):**
  Uniform random sampling $r \in [-1.0, 1.0]$, filtered through low-pass biquad stages for rumble and high-pass for hiss.

### ADSR Envelope Shaping
Every synthesized sound must apply an Attack-Decay-Sustain-Release envelope to eliminate DC offset pops and clicking:
* **Attack ($t_A$):** Linear or exponential rise from 0 to peak amplitude $A_{\max}$.
* **Decay ($t_D$):** Exponential drop from $A_{\max}$ to sustain level $S$.
* **Sustain ($t_S$):** Constant amplitude hold while key/trigger is active.
* **Release ($t_R$):** Smooth exponential decay to zero ($A(t) = S \cdot e^{-5 t / t_R}$).

---

## 2. Game Development Sound Design Categories

| Category | Typical Synthesis Formula | Target Duration | Common Uses |
| :--- | :--- | :--- | :--- |
| **Laser / Blaster** | Downward exponential frequency sweep ($880	ext{Hz} 	o 110	ext{Hz}$) + square/sine mix | 100ms–250ms | Sci-fi weapons, projectile firing |
| **Explosion / Impact** | White noise burst + sub-bass 60Hz thump + exponential decay envelope | 400ms–1.5s | Grenades, vehicle destruction, heavy hits |
| **Pickup / Coin** | Dual-tone ascending arpeggio ($B_5 	o E_6$) with instant attack | 120ms–200ms | Item collection, score increment, rewards |
| **Jump / Whoosh** | Upward linear frequency sweep ($150	ext{Hz} 	o 600	ext{Hz}$) with soft clipping | 150ms–300ms | Character jumping, dodge rolls, melee swings |
| **UI Click / Toggle** | High-frequency sine ping (1,200Hz) with steep 15ms exponential falloff | 15ms–40ms | Button taps, slider notches, menu navigation |
| **UI Success Chime** | Major triad harmonic chord ($C_5 + E_5 + G_5$) with smooth bell decay | 500ms–1.2s | Level complete, achievement unlock, task done |

---

## 3. Frontier AI Audio Generation Models

When rich, organic, or acoustic sound effects and music tracks are required:

### A. Text-to-Sound-Effect (SFX) Models
* **ElevenLabs Sound Effects API:**
  Best for cinematic Foley, ambient creature vocalizations, and environmental audio.
  * *Prompting Rule:* Specify action + material + acoustic space:
    `"heavy steel dungeon door slamming shut with metal latch click, stone corridor reverb"`
* **Meta AudioCraft (AudioGen):**
  Open-source local model for sound effects and acoustic texture generation. Runs on NVIDIA CUDA/Tensor Cores.
* **Stable Audio:**
  High-fidelity 44.1kHz stereo sound effects and musical stems with precise duration conditioning.

### B. Adaptive Game Music & Content Creation Soundtrack
* **Vertical Layering (Stem-Based Adaptive Music):**
  Generate 3–4 synchronized loops at identical tempo (BPM) and key:
  1. Base Ambience (Pads, low drones).
  2. Rhythm & Percussion (Drums, bassline).
  3. Lead Melody & Tension (Strings, brass, aggressive arpeggios).
  Cross-fade stems based on game intensity (e.g. exploration $	o$ combat).
* **Horizontal Re-sequencing:**
  Generate modular intro, transition, loop, and sting segments with musically aligned transition markers (beat/measure boundaries).

---

## 4. Loudness Normalization & Mastering Standards

Always master exported audio to target platform loudness constraints:
* **YouTube & Video Platforms:** **-14 LUFS** ($\pm 1.0$ LUFS, -1.0 dB True Peak).
* **Mobile Apps & Podcasts:** **-16 LUFS** (-1.0 dB True Peak).
* **Video Game Engines (Interactive):** **-24 LUFS** (-2.0 dB True Peak) for gameplay SFX to preserve dynamic headroom for explosions.
* **FFmpeg Loudnorm Command:**
  ```bash
  ffmpeg -i input.wav -af "loudnorm=I=-14:TP=-1.0:LRA=11" -ar 48000 output_master.wav
  ```

---

## 5. Offline Procedural SFX Generator Tool

Use `scripts/procedural_sfx_generator.py` to instantly synthesize crisp game sound effects, UI pings, explosions, coins, and chimes into 48kHz WAV files—**100% offline, zero API keys, zero external Python libraries required**.

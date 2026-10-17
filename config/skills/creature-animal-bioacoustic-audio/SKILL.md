---
name: creature-animal-bioacoustic-audio
description: Realistic animal and creature vocalization engineering (cats, dogs, wolves, mutants, wildlife) combining real CC0 acoustic field recordings, Klatt/Rosenberg mammalian glottal-formant vocal tract DSP synthesis (scipy.signal), and automatic GSC X-Ray / OGSR v3 24-byte binary Ogg comment header injection.
---

# Creature & Animal Bioacoustic Audio Engineering (`creature-animal-bioacoustic-audio`)

Never generate naive sine-wave beeps (`np.sin(2*np.pi*f*t)`) for animal or creature sounds, and never write bare `ffmpeg -c:a libvorbis` `.ogg` files into S.T.A.L.K.E.R. X-Ray / OGSR (`! Invalid ogg-comment version`). Always use `~/.local/bin/creature-sound-forge` to produce authentic mammalian vocalizations with verified 24-byte GSC v3 spatial audio headers.

---

## 1. Fast CLI Execution (`creature-sound-forge`)

```bash
# 1. Real CC0 domestic cat meow (sweet / classic / pleading) + GSC v3 Ogg header
~/.local/bin/creature-sound-forge cat_meow_sweet \
  -o gamedata/sounds/actor/aisha_meow.ogg \
  --min-dist 2.0 --max-dist 28.0 --max-ai-dist 15.0

# 2. Pitch-varied real cat meow variations (+1.2 semitones for younger/affectionate inflection)
~/.local/bin/creature-sound-forge cat_meow_classic --pitch 1.2 \
  -o gamedata/sounds/actor/aisha_meow_2.ogg

# 3. Real CC0 domestic cat laryngeal purr (26 Hz cycle + pharyngeal resonance)
~/.local/bin/creature-sound-forge cat_purr \
  -o gamedata/sounds/actor/aisha_purr.ogg \
  --min-dist 1.5 --max-dist 10.0

# 4. Physical Klatt/Rosenberg glottal-formant feline trill-meow ("prrrt-mew!") or hiss
~/.local/bin/creature-sound-forge synth_chirp -o gamedata/sounds/actor/aisha_chirp.ogg
~/.local/bin/creature-sound-forge synth_hiss  -o gamedata/sounds/actor/aisha_hiss.ogg

# 5. Repair / inject GSC v3 24-byte binary Ogg comment on any existing .ogg file
~/.local/bin/creature-sound-forge fix_ogg_header -o path/to/sound.ogg --min-dist 2.0 --max-dist 30.0
```

---

## 2. Mammalian Bioacoustic Physics (Why Sine Waves Sound Fake)

Real mammalian vocalizations (`Felis catus`, `Canis lupus`, etc.) follow **Source-Filter Vocal Tract Theory**:
1. **Glottal Excitation Source (Rosenberg Asymmetric Pulse):**
   - Vocal folds open gradually (`open quotient Oq ≈ 0.58`) and snap shut rapidly (`speed quotient Sq ≈ 2.2`), producing a rich harmonic spectrum (`-12 dB/oct` roll-off) with natural micro-jitter (`0.5%`) and breath aspiration noise.
2. **Time-Varying Vocal Tract Formant Cascade (`F1–F4`):**
   - A domestic cat's `"meow"` is a diphthong/triphthong articulatory trajectory `/m - i - a - u - w/` as the jaw opens and closes:
     - **Nasal Onset `/m/` (`0–12%`):** `F1 = 390 Hz`, `F2 = 1180 Hz`
     - **Palatal Peak `/i/` (`12–32%`):** `F0` arches to `550–680 Hz`; `F1 = 720–890 Hz`, `F2 = 2520 Hz`, `F3 = 3780 Hz`, `F4 = 4850 Hz`
     - **Open Core `/a/` (`32–62%`):** `F1 = 890→680 Hz`, `F2 = 2150→1480 Hz`
     - **Labial Close `/u–w/` (`62–100%`):** `F0` glides down to `350 Hz`; `F1 = 410 Hz`, `F2 = 960 Hz`
3. **Feline Laryngeal Purr (`25–28 Hz`):**
   - Driven by a neural oscillator gating glottal impulses at `26.2 Hz` across both inhalation and exhalation phases, coupled with `140–420 Hz` pharyngeal resonance.

---

## 3. Exact GSC X-Ray / OGSR v3 Binary Ogg Comment Layout (`SoundRender_Source_loader.cpp`)

In OGSR (`xrSound/SoundRender_Source_loader.cpp:97-131`), `ovm->user_comments[0]` inside the Vorbis `0x03 "vorbis"` packet must be a raw 24-byte little-endian struct (`struct.pack("<IfffIf", ...)`), **not** an ASCII `encoder=Lavc...` tag:

| Offset | Type | Field | Typical Companion Value |
| :--- | :--- | :--- | :--- |
| `0x00` | `uint32` | `version` (`OGG_COMMENT_VERSION`) | `0x00000003` (`3`) |
| `0x04` | `float32` | `m_fMinDist` | `2.0f` (meters) |
| `0x08` | `float32` | `m_fMaxDist` | `28.0f` (meters) |
| `0x0C` | `float32` | `m_fBaseVolume` | `1.0f` (`0.0–2.0`) |
| `0x10` | `uint32` | `m_uGameType` | `128` (World Ambient / non-aggro) |
| `0x14` | `float32` | `m_fMaxAIDist` | `15.0f` (meters) |

When modifying the `0x03 "vorbis"` packet, the Ogg page lacing table (`header[26]`) and direct non-reflected CRC-32 (`poly = 0x04C11DB7` at `header[22:26]`) must be recomputed via `creature-sound-forge`.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`Path(tempfile.gettempdir())`, standard Python `wave`/`struct`/`numpy`/`scipy`, and `ffmpeg` CLI discovery).

## Related & Interoperating Skills
- **`game-audio-ogg-gsc-encoder`**: GSC Ogg Vorbis binary comment encoding and distance presets.
- **`voice-speech-audio-synthesis`**: NPC voice synthesis and Whisper STT.
- **`pbr-radiometry-color-dsp-math`**: Audio/signal processing math, FFT convolution, and biquad filter design.

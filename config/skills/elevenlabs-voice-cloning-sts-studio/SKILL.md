---
name: elevenlabs-voice-cloning-sts-studio
description: ElevenLabs feature parity for expressive neural Text-to-Speech (TTS), Zero-Shot Instant Voice Cloning (F5-TTS, Chatterbox, CosyVoice 2, LTAS spectral timbre cloning), Speech-to-Speech (STS) voice conversion (Seed-VC, RVC v2, independent pitch/formant warping), character acoustic FX (PDA radio, gasmask, psy-chorus), and GSC X-Ray v3 Ogg encoding via ~/.local/bin/eleven-studio.
---

# ElevenLabs Voice Cloning & Speech-to-Speech Studio (`elevenlabs-voice-cloning-sts-studio`)

Provides complete feature parity with **ElevenLabs Multilingual TTS v2, Instant Voice Cloning (IVC), and Speech-to-Speech (STS) Voice Changer** — executing locally for **$0 / 0 cloud quota** via `~/.local/bin/eleven-studio` (or dispatching to the ElevenLabs REST API when `ELEVENLABS_API_KEY` and `--use-api` are provided).

---

## 1. Instant CLI Execution (`~/.local/bin/eleven-studio`)

```bash
# 1. Expressive Character Neural TTS + S.T.A.L.K.E.R. PDA Radio / Gas-Mask FX + GSC v3 Ogg Header
~/.local/bin/eleven-studio tts "Attention stalkers, an emission is approaching. Seek shelter immediately." \
  -c military_commander \
  --fx pda_radio \
  -o gamedata/sounds/characters_voice/scenario/megafon/emission_warn.ogg

# 2. Zero-Shot Spectral Timbre Cloning from an Existing Game NPC .ogg File
#    Extracts the 32-band LTAS vocal-tract envelope from --ref-audio and imprints it onto the new line:
~/.local/bin/eleven-studio tts "Marked One, bring me that artifact and I will make it worth your while." \
  -c sidorovich \
  --ref-audio gamedata/sounds/characters_voice/scenario/trader/trader_script1a_1.ogg \
  -o gamedata/sounds/characters_voice/scenario/trader/trader_custom_1.ogg

# 3. Speech-to-Speech (STS) Voice Changer (Independent Pitch & Vocal-Tract Formant Shifting)
#    Preserves 100% of original cadence/emotion while shifting F0 (-2.5 semitones) and formants (0.88x):
~/.local/bin/eleven-studio sts \
  -i raw_mic_recording.wav \
  -o gamedata/sounds/characters_voice/human_01/monolith/fight/attack_1.ogg \
  --pitch -2.5 --formant 0.88 --fx monolith_psy
```

---

## 2. Character Presets & Zone Acoustic FX Chains

| Preset (`-c`) | Base Neural Voice | Default Acoustic FX (`--fx`) | Best Use Case |
| :--- | :--- | :--- | :--- |
| **`stalker_veteran`** | `en-US-ChristopherNeural` (`-8Hz`, `-5%`) | `none` | Loner / veteran Stalker dialogue |
| **`sidorovich`** | `en-US-RogerNeural` (`-14Hz`, `-8%`) | `none` | Gruff trader / barkeep |
| **`military_commander`** | `en-US-EricNeural` (`-10Hz`, `+4%`) | `pda_radio` (`360–3300 Hz` + overdrive + squelch) | Military / Duty squad radio comms |
| **`ecologist`** | `en-GB-RyanNeural` (`+0Hz`, `+2%`) | `gasmask` (respirator cavity resonance `<3.8 kHz`) | Sakharov / Kruglov / suit dialogue |
| **`monolith_preacher`** | `en-US-ChristopherNeural` (`-18Hz`, `-12%`) | `monolith_psy` (dual psy-chorus + metallic delay) | Monolith fanatics / C-Consciousness |
| **`female_companion`** | `en-US-AriaNeural` (`+4Hz`, `+0%`) | `none` | Female NPC / companion voice |
| **`russian_stalker`** | `ru-RU-DmitryNeural` (`-8Hz`, `-4%`) | `none` | Authentic Russian Zone dialogue |
| **`ukrainian_stalker`** | `uk-UA-OstapNeural` (`-6Hz`, `-4%`) | `none` | Authentic Ukrainian Zone dialogue |

---

## 3. Local RTX 5060 (`8 GB VRAM`) Deep Neural Voice Cloning Stack

When full waveform zero-shot neural cloning or diffusion STS is needed on the RTX 5060 GPU:
1. **F5-TTS (`SWivid/F5-TTS`, Flow-Matching Zero-Shot Cloning):**
   - Clones any speaker's voice, accent, and pacing from a `3–10s` reference clip (`~3.2 GB VRAM` in `fp16`).
2. **Chatterbox TTS (Resemble AI MIT Open-Weight TTS):**
   - Supports continuous **`exaggeration` (`0.0–1.0`)** and **`cfg_weight`** sliders matching ElevenLabs' `style_exaggeration` and `stability` controls.
3. **Seed-VC & RVC v2 (Zero-Shot / Retrieval Speech-to-Speech):**
   - Converts spoken source audio into any target voice model while preserving laughter, whispers, combat shouts, and exact syllable timing.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux (`/dev/shm` RAM-disk staging) and Windows 10/11 (`tempfile.gettempdir()`, standard Python `scipy`/`numpy`/`edge_tts`/`ffmpeg`).

## Related & Interoperating Skills
- **`elevenlabs-voice-isolator-dubbing-sfx`**: Studio Voice Isolator, cross-language AI game dubbing, and Text-to-SFX.
- **`voice-speech-audio-synthesis`**: Whisper STT and `agy-mic-button` floating terminal dictation.
- **`game-audio-ogg-gsc-encoder`**: 24-byte GSC X-Ray v3 binary Ogg Vorbis header specification.

---
name: game-audio-ogg-gsc-encoder
description: Converts and encodes game audio to Ogg Vorbis while injecting and preserving proprietary GSC binary engine comment chunks (min/max distance, volume, AI perception) required by S.T.A.L.K.E.R. engines.
---

# Game Audio Ogg GSC Encoder (`game-audio-ogg-gsc-encoder`)

In the S.T.A.L.K.E.R. X-Ray and OGSR engines, audio files (`.ogg`) are not standard Vorbis streams. They contain an embedded proprietary binary comment chunk (`snd_flags`, `min_dist`, `max_dist`, `base_volume`, `ai_sound_type`).

Converting audio with generic tools (e.g. `ffmpeg -i in.wav out.ogg` or Audacity) strips this binary header. When loaded in-game, missing GSC chunks cause sounds to play at 100% volume everywhere on the map, break AI hearing perception, or trigger engine crashes (`Invalid sound format`).

This skill governs engine-safe audio transcoding with valid GSC binary metadata.

---

## 1. Proprietary GSC Comment Header Structure

```
+-------------------------------------------------------------+
| Ogg Vorbis Stream Header                                    |
+-------------------------------------------------------------+
| Vorbis Comment Field:                                       |
| - Vendor String: "Xiph.Org libVorbis..."                    |
| - User Comments:                                            |
|   - "GSC_SND" (Magic marker + binary parameters):           |
|     - Quality / Flags (4 bytes uint32)                      |
|     - Min Distance (4 bytes float32, e.g. 1.0m)             |
|     - Max Distance (4 bytes float32, e.g. 30.0m)            |
|     - Base Volume  (4 bytes float32, e.g. 1.0)              |
|     - AI Sound Type (4 bytes uint32, e.g. Gunshot / Footstep)|
+-------------------------------------------------------------+
| Encoded Vorbis Audio Packets                                |
+-------------------------------------------------------------+
```

---

## 2. Safe Audio Transcoding Workflow

```bash
# 1. Convert source (Wwise .wem or WAV) to intermediate 44.1kHz / 48kHz mono WAV
ffmpeg -i input_wwise.wem -ac 1 -ar 44100 intermediate.wav

# 2. Encode to Ogg with GSC comment chunk injection via ZoneForge / oggenc-gsc
python3 -m zoneforge.cli audio encode \
  --input intermediate.wav \
  --output gamedata/sounds/weapons/ak74/ak74_shoot.ogg \
  --min-dist 2.0 \
  --max-dist 150.0 \
  --ai-type gunshot
```

---

## 3. Standard Distance Presets

| Sound Category | Min Distance | Max Distance | AI Sound Type |
| :--- | :--- | :--- | :--- |
| **Inventory / UI Click** | 0.1 m | 1.0 m | `0` (Silent to AI) |
| **NPC Footstep** | 1.0 m | 15.0 m | `1` (Footstep / Movement) |
| **Anomaly Hum / Idle** | 2.0 m | 25.0 m | `0` (Environmental) |
| **Pistol / SMG Shot** | 3.0 m | 100.0 m | `2` (Gunshot) |
| **Rifle / Sniper Shot** | 5.0 m | 250.0 m | `2` (Gunshot) |
| **Explosion / RPG** | 10.0 m | 400.0 m | `3` (Explosion) |

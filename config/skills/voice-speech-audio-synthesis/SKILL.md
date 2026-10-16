---
name: voice-speech-audio-synthesis
description: Speech-to-text transcription via Whisper, natural voice generation using Piper/Kokoro/OpenAI TTS, game NPC dialogue synthesis, and subtitle timing.
---

# Voice, Speech & Audio Synthesis

This skill standardizes speech-to-text transcription (via Whisper) and high-quality offline/online text-to-speech (TTS) voice generation. It enables automated creation of game NPC voice lines, podcast/briefing audio, and subtitle synchronization.

---

## 🎙️ 1. Speech-to-Text Transcription (`faster-whisper` / Whisper CLI)

Transcribe any local audio file into text and timed subtitles (SRT/VTT):

```bash
# Using faster-whisper (high-performance local CTranslate2 engine)
python3 - << 'EOF'
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("audio.mp3", beam_size=5)

print(f"[INFO] Detected language: {info.language} (probability: {info.language_probability:.2f})")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
EOF
```

---

## 🗣️ 2. Offline Neural Voice Generation (Piper / Kokoro TTS)

Generate natural human voices locally without external cloud API fees:

```bash
# Using Piper TTS (lightweight offline neural voice engine)
echo "Attention stalkers. An emission is approaching. Seek shelter immediately." |   piper --model en_US-lessac-medium.onnx --output_file emission_alert.wav
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `audio-dsp-tuning`:** To process generated speech through 6-stage broadcast chains (de-esser, compressor, EQ).
* **Handoff to `game-modding`:** To package dialogue files with S.T.A.L.K.E.R. proprietary GSC Vorbis sound comment chunks.

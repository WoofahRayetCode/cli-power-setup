---
name: youtube-shorts-video-automation
description: Automated creation of viral YouTube Shorts, TikToks, and long-form YouTube edits with 9:16 vertical re-framing, hook-first pacing, kinetic word-by-word subtitles, silence trimming jump cuts, split-screen layouts, and audio ducking.
---

# YouTube Shorts & Creator Video Automation

This skill automates the creation of high-retention **YouTube Shorts**, **TikToks**, **Instagram Reels**, and modern YouTube long-form content.

---

## 🎯 When to Activate

* **16:9 to 9:16 Vertical Re-Framing:** Converting widescreen gameplay, tutorials, or podcasts into vertical mobile shorts with blurred top/bottom padding or split-screen framing.
* **Auto-Silence Trimming & Jump Cuts:** Detecting pauses and breathing gaps (>0.4s) and splicing them out automatically to create fast-paced, high-retention YouTube edits.
* **Kinetic Word-Level Subtitles:** Burning dynamic, colorful animated captions (MrBeast / Hormozi style) generated from Whisper timestamps.
* **Audio Ducking:** Automatically lowering background music when speaking and raising it during pauses.
* **Hook-First Video Slicing:** Extracting high-energy highlights and placing a 3-second hook at the start of the video.

---

## 🛠️ Automated Short Creation Engine

### 1. 16:9 Widescreen to 9:16 Vertical with Blurred Background:
```bash
ffmpeg -hwaccel cuda -i input_16x9.mp4 -filter_complex \
  "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:5[bg]; \
   [0:v]scale=1080:-1[fg]; \
   [bg][fg]overlay=(W-w)/2:(H-h)/2[v]" \
  -map "[v]" -map 0:a -c:v av1_nvenc -preset p6 -cq 23 -c:a aac -b:a 192k short_9x16.mp4
```

### 2. Auto-Trim Silences (High-Retention Jump Cuts):
```bash
ffmpeg -i input.mp4 -af "silenceremove=start_periods=1:start_duration=0.2:start_threshold=-35dB:detection=peak" output_snappy.mp4
```

### 3. Kinetic Caption Staging:
Convert Whisper `.srt` into stylized Advanced SubStation Alpha (`.ass`):
* Font: Impact, Montserrat ExtraBold, or Arial Rounded MT
* Highlight color: Yellow (`#FACC15`) or Emerald (`#10B981`)
* Text outline: 3px solid black border (`Outline=3, Shadow=1`)

---

## 📊 Summary Output Format
* `youtube shorts: [✓] Rendered 9:16 vertical short (58s, AV1 NVENC, blurred background padding)`
* `jump-cut trimming: [✓] Removed 14 pauses (12.4s saved, pace increased by 18%)`

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`video-production-automation`**: Hardware-accelerated video engineering and automated post-production using FFmpeg with NVIDIA NVENC (AV1, HEVC...
- **`game-exploratory-fuzzing`**: Evolutionary input fuzzing, novelty-guided action mutation, and crash delta minimization for automated game QA...
- **`android-device-automation`**: Real-time Android device control, scrcpy screen observation, mobile game bot scripting, automated app manageme...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

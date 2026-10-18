---
name: claude-multimodal-vision-auditor
description: Directs Claude Code's multimodal vision capabilities toward screen telemetry, UI layout audits, rendering artifact triage, and local GPU perceptual diffing.
---

# Claude Multimodal Vision Auditor (`claude-multimodal-vision-auditor`)

Claude 3.7 Sonnet has native multimodal vision capabilities, allowing it to inspect and audit visual assets, game screenshots, UI layouts, and 3D renders.

This skill equips Claude Code with an automated visual capture and inspection pipeline, bringing it to full parity with Gemini Argon 4's visual grounding.

---

## 📸 1. Visual Capture Pipeline

When diagnosing visual glitches, missing textures, or UI alignment:
1. **Screen Capture**: Capture the active desktop or window to `/dev/shm`:
   ```bash
   spectacle -b -n -o /dev/shm/active_screen.png
   # Or via ImageMagick import:
   import -window root /dev/shm/active_screen.png
   ```
2. **Local GPU Pre-Processing**: Before loading massive 4K/1080p images into Claude, run local perceptual diffing and OCR:
   ```bash
   python3 ~/.gemini/config/skills/local-gpu-vision-ocr-preprocessor/scripts/local_vision_ocr.py /dev/shm/active_screen.png
   ```
   This extracts text and bounding boxes locally via host GPU/Tesseract, cutting cloud multimodal token consumption by 85–95%.
3. **Targeted Inspection**: Crop specifically to the region of interest (e.g. game dialogue window, HUD, or Blender 3D viewport) and inspect with Claude.

---

## 🔍 2. Game Glitch & Telemetry Triage

- **Missing Textures**: Detect the classic magenta/black checkerboard pattern in S.T.A.L.K.E.R. / OGSR engine rendering.
- **HUD & Telemetry Verification**: Inspect MangoHud and DXVK overlays for frametimes, VRAM allocation, and thermal throttles.
- **Blender 3D Silhouette Matching**: Inspect 2x2 contact sheets rendered from Blender to verify `Silhouette IoU >= 0.80` against reference concept art.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

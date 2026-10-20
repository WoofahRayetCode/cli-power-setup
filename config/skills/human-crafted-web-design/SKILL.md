---
name: human-crafted-web-design
description: Anti-AI web design heuristics, Linear/Stripe aesthetics, typography hierarchy, and production Tailwind.
---

# Human-Crafted Web Design (`human-crafted-web-design`)

Professional frontend aesthetics that avoid generic AI design tropes. Production Tailwind CSS, tactile dark-mode, and micro-interactions.

## Design Heuristics
- **Avoid AI Slop:** No purple/blue neon gradient blobs on generic black; use deep slate `#090d16` or rich zinc `#09090b`.
- **Typography:** Strict modular scale (`text-xs`, `text-sm`, `text-base`, `text-xl`, `text-3xl`). Use high-legibility fonts (Inter, Geist Sans, JetBrains Mono).
- **Tactile Inputs:** Subtle 1px borders with border-opacity (`border-white/10`), active press scales (`active:scale-[0.98]`), and crisp focus rings.
- **Template Generator:**
  `python3 config/skills/human-crafted-web-design/scripts/archetype_template_generator.py`

## Related & Interoperating Skills
- **`interactive-data-visualization-web`**: Browser-based interactive D3.js force graphs, Vis.js timelines, KaTeX, and reactive single-file micro-apps.
- **`game-audio-voice-engineering`**: Game audio Ogg Vorbis GSC comment headers, procedural SFX, spatial HRTF, ElevenLabs, and Piper TTS.
- **`project-memory-bank`**: Persistent project memory curation (.agents/memory/activeContext.md), checkpoints, and task velocity guardrail...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

---
name: stalker-ogsr-engine-porting
description: 64-bit S.T.A.L.K.E.R. OGSR/X-Ray migration, LuaJIT FFI, LTX inheritance, crash triage, and night ops.
---

# S.T.A.L.K.E.R. OGSR Engine Porting (`stalker-ogsr-engine-porting`)

Comprehensive authority for porting mods, scripting, and testing on the 64-bit S.T.A.L.K.E.R. OGSR / X-Ray engine.

## Subsystems & Guidelines
- **64-Bit LuaJIT & FFI:** Prevent Luabind crashes. Never pass 64-bit raw pointers through 32-bit integer callbacks. Use LuaJIT FFI for high-speed C struct manipulation.
- **LTX Inheritance Discipline:** Respect section headers (`[section]:parent`), case sensitivity, and strip identical inherited parameters via `config_delta_extractor.py`.
- **Crash Triage & Modal Sweep:**
  Dismiss lingering crash popups and parse crash stack traces:
  `python3 ~/.gemini/config/skills/stalker-ogsr-engine-porting/scripts/xray_crash_handler.py sweep`
  Archive and resolve RVA addresses to lines:
  `python3 ~/.gemini/config/skills/stalker-ogsr-engine-porting/scripts/crash_archive.py`
  `python3 ~/.gemini/config/skills/stalker-ogsr-engine-porting/scripts/xray_crash_resolver.py`
- **Autonomous Playtesting:**
  `python3 ~/.gemini/config/skills/stalker-ogsr-engine-porting/scripts/stalker_playtest_runner.py`

## Related & Interoperating Skills
- **`game-audio-voice-engineering`**: Game audio Ogg Vorbis GSC comment headers, procedural SFX, spatial HRTF, ElevenLabs, and Piper TTS.
- **`stalker2-ue5-asset-transpiler`**: S.T.A.L.K.E.R. 2 UE5 IoStore asset extraction, audio conversion, and vegetation transpilation to OGSR.
- **`autonomous-game-qa-playtesting`**: Autonomous game testing, nav-graph recording, /dev/uinput simulation, MangoHud, screen OCR, and fuzzing.

---
name: client-memory-anti-tamper-re
description: Game memory scanning, pointer paths, XOR masking, DLL proxy generation, anti-debugging, and rr replay.
---

# Client Memory & Anti-Tamper Engineering (`client-memory-anti-tamper-re`)

Runtime memory scanning, pointer chain resolution, anti-cheat detection, DLL proxy generation, and time-travel replay debugging.

## Workflows
- **Memory Scanning:** Scan process memory for dynamic addresses and pointer paths:
  `python3 ~/.claude/skills/client-memory-anti-tamper-re/scripts/memory_scanner.py`
- **DLL Proxy Generation:** Automatically generate forwarding DLL proxies that intercept exported function calls:
  `python3 ~/.claude/skills/client-memory-anti-tamper-re/scripts/dll_proxy_generator.py`
- **Save State Serialization:** Inspect binary save states and verify checksum integrity:
  `python3 ~/.claude/skills/client-memory-anti-tamper-re/scripts/save_state_inspector.py`
- **Time-Travel Debugging:** Deterministic record and replay of segfaults using Mozilla `rr`.

## Related & Interoperating Skills
- **`reverse-engineer-anything`**: Reverse Engineer Anything (REA) MCP server integration, function diffing, and obligation ledgers.
- **`console-game-decompilation`**: Matching binary decompilation for console ROMs and retro binaries using Splat, m2c, and objdiff.
- **`game-audio-voice-engineering`**: Game audio Ogg Vorbis GSC comment headers, procedural SFX, spatial HRTF, ElevenLabs, and Piper TTS.

---
name: cross-agent-context-deduplicator
description: Eliminates redundant transcript ingestion and context pollution between concurrent Argon and Fable agents by clamping sync payloads to strict 15-line symbol diff abstracts.
---

# Cross-Agent Context Deduplicator (`cross-agent-context-deduplicator`)

When Argon and Fable exchange state updates via `tandem-agent-sync`, injecting full command histories, raw compiler logs, or verbose multi-paragraph explanations pollutes the recipient model's context window.

This skill enforces a **strict 15-line abstract ceiling** on all cross-agent synchronization packets, passing only symbol-coordinate diffs and machine-verifiable milestones.

---

## 1. High-Density Diff Abstraction

### Sub-optimal (Verbose Context Injection):
```text
"Argon completed unpacking pakchunk16 using retoc. We extracted 1,736 curve assets from the IoStore container, including AimingWeaponFOVCurve, AimingWeaponRecoilPitchCurve, and AssaultRifleDispersionDefault. Then we wrote a Python script to parse the curves and map them into weapons.ltx, changing scope_zoom_factor to 1.25..."
```
*(Token overhead: 150+ tokens per update across 50 turns = 7,500 wasted tokens).*

### Hardened (High-Density Symbol Coordinates):
```text
[ARGON_MILESTONE: ASSETS_SYNCED]
- Source: pakchunk16 (1,736 curves)
- Transpiled: config/weapons/weapons.ltx#L45-L80 (scope_zoom, cam_dispersion)
- Build Status: Validated LTX syntax
- Next: Awaiting Fable C++ build pass
```
*(Token count: ~32 tokens — **78% reduction**).*

---

## 2. Ingestion Guardrails

1. **Strip Tool Output:** Never include raw bash stdout, compiler dumps, or stack traces in cross-agent handoffs unless specifically requested for crash triage.
2. **Use Symbol Ranges:** Reference edits via file coordinates:
   `<file_path>#L<start>-L<end>:<function_name>`
3. **Flat Machine Schema:** All cross-agent communication is parsed directly through `.agents/handoff.json` without conversational preambles.

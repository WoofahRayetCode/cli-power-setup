---
name: cohere-provenance-grounding-ledger
description: Emulates Cohere Command R+ grounded provenance citations. Traces every game config parameter and C++ modification to its exact vanilla baseline coordinate to eliminate hallucinated parameters.
---

# Cohere Provenance Grounding Ledger (`cohere-provenance-grounding-ledger`)

Cohere Command R+ pioneered strict **grounded attribution**: every assertion and generated parameter must cite its exact origin coordinates rather than relying on ungrounded model assumptions.

In game engine porting and modding, large language models frequently hallucinate plausible-sounding configuration keys (e.g. inventing non-existent LTX keys like `bullet_drop_factor` or guessing default audio attenuation distances). When loaded into the game, hallucinated keys trigger silent parameter ignores or fatal engine crashes (`Cannot find variable in section`).

This skill enforces strict provenance citations for all game configs and C++ engine hooks.

---

## 1. Grounded Attribution Syntax

When generating or modifying game configurations:

```ini
[wpn_ak74]:identity_immunities
; PROVENANCE: Extracted from vanilla SoC 1.0006 config/weapons/w_ak74.ltx#L15
cost                 = 2000
; PROVENANCE: Transpiled from S.T.A.L.K.E.R. 2 pakchunk16 AimingWeaponFOVCurve (key 0.0)
scope_zoom_factor    = 1.25
; PROVENANCE: Verified against OGSR xrGame/WeaponAK74.cpp#L48
cam_dispersion       = 0.15
```

---

## 2. Invariant Attribution Rules

1. **Verify Before Emitting:** Never emit a configuration key without verifying its presence in either:
   - The vanilla baseline (`unpacked/config/` or stock OGSR).
   - The engine C++ reader method (`pSettings->r_float(section, "key")`).
2. **Flag Non-Standard Keys:** If an engine extension adds a custom parameter, cite the exact commit or pull request introducing it.
3. **Zero Parameter Hallucination:** If a parameter default cannot be cited, look up the parent section inheritance before writing code.

## Related & Interoperating Skills
- **`game-modding`**: Specialized workflows, format rules, and safety checks for game modding, focusing on S.T.A.L.K.E.R. Legends of...
- **`xray-crash-log-diagnostician`**: Triages and diagnoses S.T.A.L.K.E.R. X-Ray and OGSR engine crashes, BugTrap logs, and Wine/Proton stack traces...
- **`game-config-delta-extractor`**: Game configuration delta extractor and inheritance pruner. Strips identical inherited keys in S.T.A.L.K.E.R. L...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

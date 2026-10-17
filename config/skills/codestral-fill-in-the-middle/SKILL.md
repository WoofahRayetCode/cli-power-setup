---
name: codestral-fill-in-the-middle
description: Emulates Mistral Codestral Fill-in-the-Middle (FIM) surgical infilling. Anchors prefix and suffix code boundaries to generate exact bridge logic with zero indentation drift or hallucination.
---

# Codestral Fill-in-the-Middle (`codestral-fill-in-the-middle`)

Mistral Codestral pioneered native **Fill-In-The-Middle (FIM)** generation: rather than rewriting entire functions, it accepts an explicit immutable prefix and suffix, generating strictly the missing bridge code between them.

This skill equips Gemini 4 Argon with Codestral-grade FIM anchoring, guaranteeing zero indentation drift or accidental logic deletion during chunk edits.

---

## 1. The FIM Structure

When targeting modifications inside complex nested loops or functions:

```
[PREFIX_ANCHOR (Immutable)]
void CWeaponAK74::UpdateCL() {
    inherited::UpdateCL();
    if (GetState() == eFire) {

[INFILL_TARGET (Surgical Replacement)]
        // Exactly what needs to change:
        ApplyRecoilKick(cam_dispersion, cam_dispersion_inc);

[SUFFIX_ANCHOR (Immutable)]
    }
    UpdateHUD();
}
```

---

## 2. Invariant Rules for FIM Chunk Editing

1. **Exact Boundary Matching:** Always select 2 lines of identical code above and below the target modification to serve as the immutable prefix and suffix anchors.
2. **Indentation Preservation:** Strictly mirror the exact whitespace (spaces vs tabs) of the surrounding block.
3. **Zero Surrounding Rewrite:** Never re-generate the prefix or suffix code in the replacement chunk.

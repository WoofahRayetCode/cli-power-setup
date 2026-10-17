---
name: windsurf-cascade-flow-tracker
description: Emulates Codeium Windsurf Cascade Flow on Gemini 4 Argon. Tracks multi-file dependency ripple effects, symbol references, and cascading changes across C++, Lua, and LTX configurations.
---

# Windsurf Cascade Flow Tracker (`windsurf-cascade-flow-tracker`)

Codeium Windsurf's signature architecture is its **Cascade Flow Tracker**: when an edit is made in one file, Cascade dynamically traces the ripple effects across all dependent files, function call-sites, and configuration references before running builds.

This skill equips Gemini 4 Argon with proactive ripple-effect tracking across C++ engine headers, Lua scripts, and S.T.A.L.K.E.R. LTX inheritance trees.

---

## 1. The Cascade Ripple Matrix

Whenever modifying a shared interface:

```
[ Primary Modification: CWeapon::Fire() parameter added ]
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
[ Dependent C++ Subclasses ]   [ Lua Script Bindings ]   [ LTX Weapon Configs ]
- CWeaponAK74::Fire()          - script_engine.cpp       - wpn_ak74.ltx
- CWeaponShotgun::Fire()         Luabind registration      (Check fire_modes)
```

---

## 2. Invariant Tracking Rules

1. **Header-to-Implementation Proactive Check:**
   If a C++ header (`.h` / `.hpp`) struct or method signature is modified:
   - Identify all implementation files (`.cpp`) overriding that method via `grep -rn "MethodName" src/`.
   - Apply surgical diffs to all call-sites in a single batch turn rather than waiting for compiler errors.
2. **LTX Hierarchy Trace:**
   If a base LTX section (`[identity_immunities]`) is modified, check all inheriting sections (`[wpn_*]`) to ensure no required parameters were orphaned.
3. **Context Economy:** Track ripple effects as compact symbol coordinates (`<file>#L<line>`) rather than ingesting entire files.

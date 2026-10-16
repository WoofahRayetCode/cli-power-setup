---
name: stalker-ogsr-migration
description: Migration, adaptation, and porting of legacy S.T.A.L.K.E.R. Shadow of Chernobyl mods (Complete, AMK, Autumn Aurora) to the 64-bit OGSR Engine. Covers 64-bit binary layout, DX11 shader reconciliation, LuaJIT callback adaptation, ACDC spawn translation, LTX sanitization, and crash log diagnosis.
---

# S.T.A.L.K.E.R. Mod to OGSR Engine Migration Protocol

This skill governs the systematic porting and adaptation of legacy 32-bit *S.T.A.L.K.E.R.: Shadow of Chernobyl* mods (such as *S.T.A.L.K.E.R. Complete 2009*, *AMK*, or *Autumn Aurora*) onto the modern 64-bit **OGSR Engine** (DirectX 11, multithreaded renderer, 64-bit pointers, and LuaJIT).

---

## 🏗️ 1. Engine & Binary Layout (`bin_x64/`)

1. **Protect Vanilla Baselines:**
   - Keep the original 32-bit `bin/` directory intact as a reference baseline.
   - Install OGSR into `bin_x64/`. The primary game executable is `bin_x64/xrEngine.exe`.
2. **Purge Custom 32-bit DLLs:**
   - Legacy mods frequently ship custom 32-bit native libraries (e.g. `complete_blood_pools.dll`, modded 32-bit `xrGame.dll`).
   - **Rule:** Never copy 32-bit DLLs into `bin_x64/`. They will fail to link or crash with error code `0xC000007B` (invalid image format). Custom features must be migrated to OGSR LuaJIT scripts or engine config parameters.
3. **Verify `fsgame.ltx`:**
   Ensure `$game_bin$` points to the 64-bit directory:
   ```ini
   $game_bin$ = false| false| $fs_root$| bin_x64\
   ```

---

## 🎨 2. Shader & Rendering Pipeline Reconciliation

Complete 2009 shipped custom DirectX 9 `shaders/r2/` (depth of field, motion blur, bloom). OGSR completely replaces this with a modern DirectX 11 deferred renderer (`shaders/r3/`, `shaders/r4/`).

* **Critical Rule:** **Delete or omit `gamedata/shaders/` from the legacy mod.**
* Leaving legacy DX9 shaders in `gamedata/shaders/` causes immediate fatal shader compiler crashes (`FATAL ERROR: Expression: !failed()`) or renders a pitch-black world.
* Allow OGSR's native DX11 shaders (packaged in OGSR database archives) to manage rendering, lighting, ambient occlusion, and sunshafts.

---

## 📜 3. Lua Script & Callback Modernization

Complete mod introduces custom scripts (`sleeping_bag.script`, `repair.script`, `teleport.script`, `sound_theme.script`). OGSR runs 64-bit LuaJIT with updated C++ engine bindings.

### Callback Architecture Migration
In legacy SoC, custom logic was polled continuously in `actor_binder:update` in `bind_stalker.script`, degrading performance. OGSR provides clean event-driven signals:

| Legacy SoC Pattern | OGSR Event Callback | Example Use |
| :--- | :--- | :--- |
| `actor_binder:update()` polling loop | `on_actor_update(delta)` | Weather, radiation checks, stamina |
| Scanning inventory on every frame | `on_item_use(obj)` | Sleeping bag, repair kits, medical items |
| Keypress hacks via input hooks | `on_key_press(key)` | Quick-throw grenades, night vision hotkeys |
| Entity death checks | `on_npc_death(victim, killer)` | Quest milestones, karma counters |

### Adapting Complete's Sleeping Bag
```lua
-- Modern OGSR pattern in bind_stalker.script or custom signal module:
function on_item_use(item)
    if item:section() == "device_sleeping_bag" then
        -- Trigger Complete's sleep dialog UI safely
        sleeping_bag.main()
    end
end
```

---

## 🗺️ 4. Spawn System & `all.spawn` Porting

If the legacy mod modifies `all.spawn` (e.g. Complete's sleeping bag, teleporters, or custom quest stashes):

1. **Unpack with Universal ACDC:**
   ```bash
   perl universal_acdc.pl -d all.spawn -out ./spawn_src -g ../ -m soc
   ```
2. **Verify Item Section Names:**
   Ensure every spawned item has a matching definition in `gamedata/config/misc/devices.ltx`, `quest_items.ltx`, or `items.ltx`.
3. **Repack for OGSR:**
   ```bash
   perl universal_acdc.pl -c ./spawn_src -out all.spawn -g ../ -m soc
   ```
   *(OGSR handles vanilla level graphs automatically, but custom spawn sections must be syntax-clean).*

---

## ⚙️ 5. LTX Configuration Sanitization

OGSR enforces strict LTX parser validation and will abort on errors that vanilla X-Ray silently ignored:

1. **Section Headers:** Ensure section names contain no trailing spaces or malformed brackets: `[wpn_ak74]` (not `[wpn_ak74 ]`).
2. **Weapon HUD & Bones:** Every weapon section must include valid visual and HUD descriptors:
   ```ini
   visual                  = dynamics\weapons\wpn_ak74\wpn_ak74.ogf
   hud                     = wpn_ak74_hud
   attach_bone_name        = bip01_r_hand
   ```
3. **Audio Chunk Integrity:** Verify sound files referenced in configs retain the GSC comment chunk (distance attenuation and volume) using ZoneForge tools.

---

## 🩺 6. OGSR Log Diagnostics (`_appdata_/logs/*.log`)

Always check the tail of `_appdata_/logs/xrEngine.log` when a Crash to Desktop (CTD) occurs:

| Error Log Signature | Root Cause | Exact Resolution |
| :--- | :--- | :--- |
| `Expression: !failed()` in shader compile | Legacy `gamedata/shaders/` is conflicting with OGSR DX11. | Delete `gamedata/shaders/` and let OGSR supply DX11 shaders. |
| `CAN'T OPEN SECTION '...'` | An item, ammo, or NPC section is missing from LTX files. | Grep the missing section name in configs and restore definition. |
| `attempt to call field '...' (a nil value)` | Script called a deprecated or renamed engine function. | Update the script to use modern OGSR Lua exports. |
| `XML node not found in ...` | UI XML is missing a layout node expected by OGSR. | Check the UI XML file and add the missing control/tag. |
| `0xC000007B` on launch | A 32-bit DLL was placed into `bin_x64/`. | Remove 32-bit DLLs from `bin_x64/`. |

---

## 🎮 7. Closed-Loop Autonomous Playtesting & Vision Control (Hands-Free QA)

When porting legacy mods like *S.T.A.L.K.E.R. Complete 2009* to the 64-bit OGSR Engine, **never leave testing idle**. If there is no manual input from the user, the agent must autonomously take control of the game using the integrated locomotion controller and machine vision stack to stress-test rendering, physics, and scripting.

```
+-------------------------------------------------------------------------------+
|             Autonomous Hands-Free Playtest & QA Orchestrator                  |
+-------------------------------------------------------------------------------+
       |                                                    |
       v                                                    v
[Locomotion Controller]                             [Visual Telemetry Engine]
game_playtest_controller.py                         game_screen_monitor.py
  - orbit (circle-strafe NPCs & campfires)            - scans for #FF00FF magenta
  - sweep (360° panoramic horizon yaw/pitch)          - detects graphics freezes & blackouts
  - wander (autonomous level navigation)              - captures BugTrap modal dialogs
  - stress-locomotion (sprint/jump/crouch)                  |
  - action-cycle (weapons/reload/inventory)                 v
                                                    [Agentic Perception & OCR]
                                                    agent_visual_grounding.py (SSIM diff)
                                                    document_ocr_pipeline.py (Crash OCR)
                                                            |
                                                            v
                                            [Automated Crash Log Triage]
                                            local_model_coprocessor.py (0 cloud tokens)
                                            -> Immediate LTX/Lua fix & re-test
```

### Protocol Steps:

#### Step 1: Pre-Flight Static Linting (`local-ast-compiler-engine`)
Before launching `bin_x64/xrEngine.exe`, run parallel static validation across all CPU cores to catch malformed syntax or scripts in $<20\text{ms}$:
```bash
python3 config/skills/local-ast-compiler-engine/scripts/local_ast_compiler.py check-syntax --path gamedata/scripts/
```

#### Step 2: Spawn Background Visual Monitor & Telemetry (`game-screen-telemetry-monitor`)
Launch the real-time screen watcher in the background to monitor game frames every 2 seconds:
```bash
python3 config/skills/game-screen-telemetry-monitor/scripts/game_screen_monitor.py \
  monitor --interval 2 --duration 120 --out-dir /tmp/ogsr_telemetry &
MONITOR_PID=$!
```

#### Step 3: Inject Autonomous Locomotion & Action Sequences (`game-qa-playtest-controller`)
Take active control of the character via kernel `/dev/uinput` to execute non-linear stress maneuvers:
```bash
# 1. 360° Panoramic horizon sweep with vertical pitch oscillation (tests DX11 skybox, sunshafts, lighting LODs)
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py sweep --duration 8.0 --pitch

# 2. Circle-strafe orbit around focal targets (tests DX11 bump maps, specular highlights, and mesh collision)
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py orbit --duration 10.0 --direction right

# 3. Autonomous level wandering (tests terrain navmesh, obstacle bounce-back, and level geometry boundaries)
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py wander --duration 30.0

# 4. Stress physics & character state machines (rapid sprint, bunny-hop jump, and crouch transitions)
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py stress-locomotion --duration 12.0

# 5. Combat & UI action cycle (weapon swap, aim, fire, reload, interact with KEY_F, and toggle inventory KEY_TAB)
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py action-cycle --cycles 3

# 6. Inject testing cheats & immunities (God Mode & Unlimited Ammo)
python3 config/skills/game-qa-playtest-controller/scripts/game_playtest_controller.py enable-cheats --god-mode --infinite-ammo
```

#### Step 3b: Testing Immunities & God Mode Configuration
To prevent player death from halting autonomous QA during level transitions, shader testing, or combat AI loops:
1. **Engine CVars (`_appdata_/user.ltx`):** Ensure `g_god on` and `g_unlimitedammo on` are present before launching.
2. **Actor LTX Immunities:** In `gamedata/config/creatures/actor.ltx`, set all damage multipliers under `[actor_immunities_gd_master]` to `0.0` (zero damage from bullets, claws, radiation, fire, chemical burn, and falling).
3. **All-in-One CLI Execution:** Use `stalker-playtest-runner --god-mode --infinite-ammo --adaptive` to automatically configure immunities, inject console cheats, monitor screen telemetry, and recover from unexpected deaths.

#### Step 4: Verify Visual Mutation & UI State (`agentic-visual-perception`)
Verify that injected actions actually mutated game state rather than hanging on silent freezes:
```bash
# Verify inventory opened or frame changed via Structural Similarity (SSIM)
python3 config/skills/agentic-visual-perception/scripts/agent_visual_grounding.py \
  diff --frame-a /tmp/ogsr_telemetry/frame_01.png --frame-b /tmp/ogsr_telemetry/frame_02.png --threshold 0.05
```

#### Step 5: Automated Crash Extraction & Triage (`visual-document-ocr-intelligence` + `local-model-coprocessor`)
If the game exits or triggers an X-Ray / BugTrap fatal crash:
1. The monitor captures the desktop crash modal. Preprocess and OCR the error:
   ```bash
   python3 config/skills/visual-document-ocr-intelligence/scripts/document_ocr_pipeline.py \
     ocr --image /tmp/ogsr_telemetry/crash_dialog.png --engine tesseract
   ```
2. Summarize `_appdata_/logs/xrEngine.log` locally using the local coprocessor (billing 0 cloud tokens):
   ```bash
   python3 config/skills/local-model-coprocessor/scripts/local_model_coprocessor.py \
     summarize-log --file _appdata_/logs/xrEngine.log
   ```
3. Parse the exact `Expression:`, `File:`, and `Line:` to apply the corresponding LTX, Lua callback, or shader fix from Section 6, then re-trigger the automated playtest loop until 100% clean.



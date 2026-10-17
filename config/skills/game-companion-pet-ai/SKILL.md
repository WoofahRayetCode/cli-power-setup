---
name: game-companion-pet-ai
description: Custom companion & pet NPC architecture: state machine behaviors (follow, guard, objective guide), god mode status, dynamic light emission in dark areas, homing projectile attacks with audio vocalization, and 3D pet asset pipelines.
---

# Game Companion & Pet AI Engineering (`game-companion-pet-ai`)

The `game-companion-pet-ai` skill provides architectural blueprints, Lua state machine templates, combat integrations, and 3D modeling pipelines for authoring immortal, autonomous companion pets (such as feline/canine companions) in game engines (specialized for **S.T.A.L.K.E.R. X-Ray / OGSR** and RPG engines).

---

## 1. Companion State Machine Architecture

A companion pet requires specialized behaviors distinct from standard human squad members:

```
[Follow & Tether] ◄─── Player Moves
       │
       ├── Darkness Detected (Ambient < 0.2) ──► [Activate Torch/Lantern Light]
       │
       ├── Enemies Detected within Radius   ──► [Combat Support: Homing Missile + Vocalization]
       │
       └── Player Stalled / Lost            ──► [Scout Ahead / Guide to Active Objective]
```

### A. Tether Distance & Dynamic Speed Matching
- **Tether Distance:** Desired distance is $2.5\text{m}$ to $4.0\text{m}$ behind/beside the player.
- **Dynamic Speed:** Matches the player's movement mode:
  - If player is walking: Companion walks.
  - If player is sprinting: Companion sprints.
  - If player is $> 50\text{m}$ away (e.g. fast travel or level transition): Safely teleports companion behind the player's camera.

---

## 2. Immortal God Mode & Anomaly Immunity

Companions must not die or trigger permadeath failure states:

```lua
-- gamedata/scripts/companion_godmode.script
function init_companion_godmode(pet_obj)
    if not pet_obj then return end
    
    -- 1. Clamp health to 100%
    pet_obj:set_health_ex(1.0)
    
    -- 2. Strip all damage callbacks
    if pet_obj.bind_object then
        -- Override hit callback to return 0 damage
        pet_obj:set_callback(callback.hit, function(obj, amount, local_dir, who, bone_index)
            return false -- Absorb hit completely
        end, nil)
    end
end
```

---

## 3. Combat Integration: Homing Projectiles & Vocalization

A unique attack pattern where the pet launches a guided missile with contextual sound (e.g. meowing upon attack):

```lua
-- gamedata/scripts/companion_combat.script
local ATTACK_COOLDOWN = 3000 -- 3 second cooldown to avoid sound fatigue
local last_attack_time = 0

function update_companion_combat(pet_obj)
    local tg = time_global()
    if tg - last_attack_time < ATTACK_COOLDOWN then return end
    
    -- Find highest priority enemy
    local target = find_priority_threat(pet_obj:position(), 30.0)
    if target then
        -- 1. Play contextual vocalization (e.g. Meow sound)
        local sound = sound_object("characters_voice\\scenario\\cat_attack_meow")
        if sound then
            sound:play_at_pos(pet_obj, pet_obj:position(), 0, sound_object.s3d)
        end
        
        -- 2. Spawn guided rocket from pet head/mouth bone
        local spawn_pos = pet_obj:bone_position("bip01_head")
        local rocket = alife():create("wpn_fake_missile", spawn_pos, pet_obj:level_vertex_id(), pet_obj:game_vertex_id())
        
        -- 3. Apply homing impulse vector toward target
        last_attack_time = tg
    end
end
```

---

## 4. Darkness Illumination (Eye/Collar Dynamic Light)

In dark tunnels, underground labs, or night cycles, the companion emits soft localized light:

```lua
-- gamedata/scripts/companion_light.script
local companion_torch = nil

function update_companion_light(pet_obj)
    if not pet_obj then return end
    
    -- Check environmental light level
    local is_dark = level.get_time_hours() < 6 or level.get_time_hours() > 21
    if is_dark or level.name() == "l03u_agr_underground" or level.name() == "l08u_brainlab" then
        if not companion_torch then
            companion_torch = render_light():create()
            companion_torch:set_type(render_light.point)
            companion_torch:set_range(8.0) -- 8 meter soft radius
            companion_torch:set_color(1.0, 0.95, 0.8) -- Warm natural glow
        end
        companion_torch:set_position(pet_obj:bone_position("bip01_head"))
    else
        if companion_torch then
            companion_torch:destroy()
            companion_torch = nil
        end
    end
end
```

---

## 5. 3D Asset Modeling & Rigging Pipeline (Blender $\rightarrow$ Game Engine)

1. **Mesh Topology:** Model quad-dominant short-hair cat mesh in Blender (~4,000 to 8,000 polygons for real-time game LOD).
2. **PBR Fur Texture:** Calico pattern (white base, orange and black patched patches) baked into Diffuse/Albedo, with subtle Tangent-Space Normal for fur directionality.
3. **Rigging & Armature:** Quadruped skeletal rig (Spine, 4 legs with Two-Bone IK, tail curve bones, head/jaw bone for vocalization).
4. **Export:** Export as `.ogf` using the X-Ray Blender tools or `.fbx` with unified bone scale ($1.0$).

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`game-weather-lighting-fx`**: Dynamic game weather cycles, HDR tonemapping, sun shafts/god rays, skybox balance, and blinding glare/light-bl...
- **`game-qol-gameplay-scripting`**: Autonomous quality-of-life gameplay scripting: proximity radar scanning, intelligent auto-loot for quest/ammo/...
- **`game-ai-agent-play`**: Autonomous game-playing agent engineering and reinforcement learning (Gymnasium, OpenCV computer vision, rewar...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

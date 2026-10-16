---
name: game-dynamic-stress-orchestrator
description: Dynamic in-game stress testing and entity orchestration: collision-safe multi-entity wave spawning, cross-faction battle simulations (helicopters vs mutants), and real-time performance saturation profiling.
---

# Game Dynamic Stress Orchestrator (`game-dynamic-stress-orchestrator`)

The `game-dynamic-stress-orchestrator` skill governs runtime stress testing, scalable entity wave spawning, multi-faction AI combat simulations, and engine load profiling in 3D game engines (specialized for **S.T.A.L.K.E.R. X-Ray / OGSR** and open-world engines).

---

## 1. Collision-Safe Multi-Entity Wave Spawning

### The "Spawn Explosion" Problem
When stress testing an engine by spawning 15–30 mutants or stalkers, novice scripts spawn all entities at the player's exact coordinate `db.actor:position()`. This causes instant physics collision repulsion, violently launching the player under the map or into the skybox.

### The Circular Ring Distribution Pattern
Entities must be distributed radially around the player, verifying that every spawn point sits on a valid navigation vertex:

```lua
-- gamedata/scripts/stress_spawner.script
function spawn_stress_wave(section_name, count, min_radius, max_radius)
    if not db.actor then return end
    local actor_pos = db.actor:position()
    local angle_step = (2 * math.pi) / count

    for i = 1, count do
        local angle = i * angle_step
        local radius = min_radius + math.random() * (max_radius - min_radius)
        local spawn_x = actor_pos.x + radius * math.cos(angle)
        local spawn_z = actor_pos.z + radius * math.sin(angle)
        local spawn_pos = vector():set(spawn_x, actor_pos.y + 0.5, spawn_z)

        -- Validate level vertex on navigation mesh
        local lvid = level.vertex_id(spawn_pos)
        if lvid and lvid < 4294967295 then
            alife():create(section_name, spawn_pos, lvid, db.actor:game_vertex_id())
        end
    end
    news_manager.send_tip(db.actor, "Spawned " .. count .. "x " .. section_name .. " in safe perimeter", nil, nil, 3000)
end
```

---

## 2. Multi-Faction Battle Simulations (Air Support & Mutants)

To test AI squad logic, pathfinding load, and sound mixing under peak stress:

```lua
-- gamedata/scripts/battle_simulation.script
function trigger_heli_mutant_clash()
    -- 1. Spawn a flight patrol helicopter
    local heli = alife():create("helicopter", db.actor:position():add(vector():set(0, 40, -100)), db.actor:level_vertex_id(), db.actor:game_vertex_id())
    
    -- 2. Spawn opposing mutant packs (Snorks & Pseudodogs)
    spawn_stress_wave("snork_normal", 8, 25.0, 40.0)
    spawn_stress_wave("pseudodog_normal", 6, 20.0, 35.0)
    
    -- 3. Spawn rival Bandit squad
    spawn_stress_wave("bandit_regular", 6, 35.0, 50.0)
end
```

---

## 3. Real-Time Engine Saturation Profiling

When running stress tests, correlate entity counts with MangoHud / DXVK performance telemetry:

1. **Entity Count vs 1% Lows:** If framerate drops below 35 FPS, the engine's single-threaded AI update loop (`xrServer::Update`) is bottlenecked.
2. **Dynamic Cleanup:** Automatically release stress-spawned entities when testing concludes or when the player changes levels:
   ```lua
   function cleanup_stress_entities()
       local sim = alife()
       for id = 1, 65534 do
           local obj = sim:object(id)
           if obj and is_stress_entity(obj) then
               sim:release(obj, true)
           end
       end
   end
   ```

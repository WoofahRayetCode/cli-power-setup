---
name: game-autonomous-navigation-ai
description: Autonomous AI player navigation, level vertex/waypoint graph mapping, route recording & playback, obstacle/invisible wall avoidance, and reactive combat lock-on (aimbot steering).
---

# Autonomous Game Navigation AI (`game-autonomous-navigation-ai`)

The `game-autonomous-navigation-ai` skill governs automated player character locomotion, level waypoint graph pathfinding, route recording and replay, collision trap avoidance, and reactive combat steering across video games (specialized for **S.T.A.L.K.E.R. X-Ray Engine / OGSR** and open-world 3D titles).

---

## 1. Core Navigation Challenges & Solutions

### A. Level Geometry Traps & Invisible Level-Changer Walls
- **Problem:** Automated walking routes frequently collide with invisible level transition boxes (`level_changer`), getting the player trapped or triggering unwanted level loads prematurely.
- **Self-Improving Solution:**
  - When velocity stalls for $> 2.0\text{s}$ while movement keys are held, record the current world position vector `(x, y, z)` into `.agents/qa/nav_blacklist.json`.
  - On subsequent route executions, the pathfinder inflates an avoidance bounding sphere ($\text{radius} = 3.5\text{m}$) around blacklisted points, dynamically computing tangent detour vectors.

### B. Falling Under the Map & Geometry Meshes (`cform`)
- **Problem:** Running along steep train track embankments or debris piles can clip the actor capsule through unclosed collision meshes, causing endless falling under the map.
- **Safeguard:**
  - Continuous vertical rate-of-change monitoring: If $y$-velocity drops faster than $-15\text{m/s}$ without a jump input, immediately invoke an emergency teleport hook back to the nearest validated level vertex:
    ```lua
    -- gamedata/scripts/anti_fall_guard.script
    local last_valid_pos = nil
    function check_actor_fall()
        if not db.actor then return end
        local pos = db.actor:position()
        if pos.y < -30.0 then -- Actor has fallen below terrain floor
            if last_valid_pos then
                db.actor:set_actor_position(last_valid_pos)
            end
        else
            last_valid_pos = vector():set(pos.x, pos.y, pos.z)
        end
    end
    ```

---

## 2. A* Navigation over Level Vertex Graphs

In S.T.A.L.K.E.R. X-Ray, the entire game world is partitioned into a dense network of **Level Vertices** (`level_vertex_id`):

```lua
-- Autonomous Navigation Steerer
function navigate_to_target(target_pos)
    local actor = db.actor
    local actor_pos = actor:position()
    
    -- Calculate yaw towards target
    local dir = target_pos:sub(actor_pos):normalize()
    local target_yaw = -math.atan2(dir.x, dir.z)
    
    -- Inject smooth mouse look towards target_yaw
    actor:set_actor_direction(target_yaw)
    
    -- Inject sprint forward via input controller
    level.send_event_key_press(bind_to_dik(key_bindings.kFWD))
end
```

---

## 3. Reactive Combat Steering (Aimbot & Threat Lock-On)

When enemies attack the automated walker during gameplay runs:

1. **Threat Evaluation:** Scan nearby hostiles within $35\text{m}$. Prioritize targets currently inflicting damage on the player or key story allies (e.g. Rookie loner in Garbage, Mole at Agroprom).
2. **Smooth Lock-On:** Calculate the pitch and yaw angle towards the enemy's head bone (`bip01_head`).
3. **Engage & Circle-Strafe:** Alternate strafe vectors (`kLSTRAFE` / `kRSTRAFE`) while firing to avoid incoming projectiles.

---

## 4. Helper Script Reference: `nav-graph-recorder`

```bash
# Record a stuck point or invisible wall to the self-improving blacklist:
python3 config/skills/game-autonomous-navigation-ai/scripts/nav_graph_recorder.py log-trap --x 45.2 --y -2.1 --z 112.8 --reason "Invisible wall near Garbage level transition"

# List all learned collision traps:
python3 config/skills/game-autonomous-navigation-ai/scripts/nav_graph_recorder.py list-traps

# Smooth recorded waypoints to eliminate jerky camera turns:
python3 config/skills/game-autonomous-navigation-ai/scripts/nav_graph_recorder.py optimize-route gamedata/routes/cordon_patrol.json
```

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`game-self-improving-qa-pipeline`**: Closed-loop self-improving game QA test harness: automated loading screen dismissal, 88% loading stall watchdo...
- **`game-dynamic-stress-orchestrator`**: Dynamic in-game stress testing and entity orchestration: collision-safe multi-entity wave spawning, cross-fact...
- **`game-qa-playtest-controller`**: Autonomous multi-axis game testing locomotion controller using Linux /dev/uinput and evdev. Injects dynamic ch...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

---

## X-Ray/OGSR Engine Pitch Sign Convention & Overhead Obstacle Detour
In X-Ray/OGSR, camera/actor pitch sign is inverted relative to standard math: positive pitch = looking DOWN, while vector:getP() for a downward vector is negative. Always negate vector:getP() when aiming at low/prone targets (e.g. spine bone of wounded NPCs or downhill enemies). In tight stairwells (e.g. Cordon Sid bunker), add overhead clearance checks for hanging lamps.

---

## Promoted Executable Tool (`walkcoach.py`)
- **Location:** `~/.gemini/config/skills/game-autonomous-navigation-ai/scripts/walkcoach.py`
- **Invocation:** `~/.gemini/config/skills/game-autonomous-navigation-ai/scripts/walkcoach.py`

---

## Promoted Executable Tool (`navplan.py`)
- **Location:** `~/.gemini/config/skills/game-autonomous-navigation-ai/scripts/navplan.py`
- **Invocation:** `~/.gemini/config/skills/game-autonomous-navigation-ai/scripts/navplan.py`

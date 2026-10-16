---
name: stalker-level-ai-graph-triage
description: Diagnoses and repairs S.T.A.L.K.E.R. and X-Ray/OGSR level AI navmesh and graph defects. Triages 'Cannot find level vertex' CTDs, audits all.spawn cross-level transits, validates level.ai and game.graph connectivity, and resolves NPC pathfinding deadlocks.
---

# S.T.A.L.K.E.R. Level AI & Graph Triage (`stalker-level-ai-graph-triage`)

In S.T.A.L.K.E.R. engine modding and porting (Shadow of Chernobyl to OGSR Engine), merging levels and updating spawn archives (`all.spawn`) frequently causes game-crashing AI navigation errors. Disconnected AI nodes, invalid level vertex IDs, and orphaned smart terrain waypoints trigger instant CTDs when NPCs attempt to pathfind.

This skill governs the systematic diagnosis and repair of level AI navigation graphs.

---

## 1. Crash Log Pattern Recognition & Root Cause Triage

| Crash Signature in `xray_*.log` | Root Cause | Immediate Remediation |
| :--- | :--- | :--- |
| `! Cannot find level vertex` | NPC or monster spawned outside the walkable AI map (`level.ai`) | Clamp spawn coordinates (`position`) to the nearest valid AI node index (`m_level_vertex_id`) |
| `! Invalid position: node not found` | Teleportation or cross-level transition placed above void or inside geometry | Raycast Z coordinate downward to intersect valid ground polygon; update `all.spawn` entry |
| `! node is not connected to graph` | An isolated cluster of AI nodes has no path to the global `game.graph` | Recompile cross-table via `xrAI -g <level_name>` or add linking AI graph point |
| `xrServer::Process_event_reject: smart_terrain` | NPC assigned to a smart terrain with missing path look/walk waypoints | Audit `way_*.ltx` or `all.spawn` section for matching `[level_prefix_smart_walk]` |

---

## 2. `all.spawn` Cross-Level Transit Verification

When porting levels, cross-level changers (`level_changer`) must have exact bidirectional coordinates and valid level vertex bindings:

### Verification Checklist for `level_changer` Sections:
```ini
[alife_l01_escape_level_changer]
; 1. Local level coordinates & vertex IDs
position                = -135.2, -24.8, -355.6
game_vertex_id          = 2       ; Must be within Escape vertex range in game.graph
level_vertex_id         = 12456   ; Must be a valid node in gamedata/levels/l01_escape/level.ai

; 2. Destination coordinates & vertex IDs
dest_game_vertex_id     = 252     ; Must be within Garbage vertex range in game.graph
dest_level_vertex_id    = 3412    ; Must be valid node in gamedata/levels/l02_garbage/level.ai
dest_position           = 35.4, 0.4, -280.1
dest_direction          = 0.0, 0.0, 0.0
dest_level_name         = l02_garbage
```

---

## 3. Autonomous AI Navmesh Validation Workflow

When diagnosing NPC pathfinding crashes:
1. **Extract Crash Coordinates:** Grep `xray_*.log` for:
   `grep -E "(position|vertex|smart_terrain|Cannot find)" xray_*.log`
2. **Decompile `all.spawn`:**
   Use ACDC tool: `perl acdc.pl -d all.spawn -out ./unpacked_spawn -sort complex`
3. **Audit Waypoint Coordinates:**
   Cross-check NPC coordinates against level bounding box (`level.ltx` `[level_map]` bounds).
4. **Recompile & Test:**
   Compile back to `all.spawn` with `perl acdc.pl -c ./unpacked_spawn -out all.spawn.new` and verify with autonomous playtest runner.

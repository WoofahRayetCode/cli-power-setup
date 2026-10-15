---
name: xray-lua-scripting
description: S.T.A.L.K.E.R. X-Ray Engine Lua scripting guidelines and safeguards. Use when writing, modifying, or debugging game scripts, quest logic, callbacks, inventory hooks, or AI logic in S.T.A.L.K.E.R. EE.
---

# S.T.A.L.K.E.R. X-Ray Lua Scripting Guide

This skill governs Lua scripting for the X-Ray Engine in **S.T.A.L.K.E.R.: Legends of the Zone Trilogy – Enhanced Edition** (Shadow of Chornobyl, Clear Sky, Call of Pripyat).

## Core Architecture & Execution Model

The X-Ray Engine executes a customized Lua 5.1 / LuaJIT runtime. Scripts reside in `gamedata/scripts/` and export global functions or module tables matching their filename (e.g. `bind_stalker.script`).

### 1. Engine Callbacks & Lifecycles
- **`net_Spawn` Lifecycle:**
  - Game objects (`game_object`, `cse_abstract`) are not fully bound when the level initializes.
  - Never call `level.object_by_id()` or manipulate game objects during global script initialization.
  - Always hook into `net_Spawn(data)` or bind callbacks after the object has spawned into the level.
- **Save/Load Serialization (`save` / `load`):**
  - When storing custom mod state in net-packets, write and read data in the **exact same binary order** using `net_packet` methods (`w_u8`, `w_stringZ`, `r_u8`, `r_stringZ`).
  - Packet size limit is strictly 8192 bytes for standard game objects. Avoid stuffing large tables into a single packet.

### 2. Common Engine Pitfalls & Safety Rules
- **Nil Object Access:**
  - Calling methods on a dead, released, or despawned game object causes an immediate CTD (Crash to Desktop) with `nil value` or memory access violation.
  - Always guard with:
    ```lua
    if obj and obj:alive() then
        -- Safe to inspect or call methods
    end
    ```
- **Actor Availability:**
  - The player character `db.actor` is `nil` during level transitions and loading screens.
  - Always check `if not db.actor then return end` in periodic or timed callbacks.
- **ALife & Story IDs:**
  - Use `alife():story_object(story_id)` for unique world objects.
  - To spawn items into actor inventory safely:
    ```lua
    alife():create("section_name", db.actor:position(), db.actor:level_vertex_id(), db.actor:game_vertex_id(), db.actor:id())
    ```

### 3. Debugging Lua Scripts
- Inspect the engine log located in the game's user data directory (or Proton prefix) under `savedgames/` or `logs/` (e.g. `xray_<user>.log`).
- Look for `FATAL ERROR` or script tracebacks ending in `.script:line_number`.
- Use `printf("DEBUG: ...")` or custom logger helpers rather than raw `print()`.

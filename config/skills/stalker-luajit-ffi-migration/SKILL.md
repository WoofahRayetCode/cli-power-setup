---
name: stalker-luajit-ffi-migration
description: Manages Lua script migration to 64-bit LuaJIT and FFI in modern S.T.A.L.K.E.R. engines (OGSR Engine). Audits deprecated Luabind C++ exports, prevents LuaJIT GC64 memory limits and raw pointer corruption, and traps silent callback failures.
---

# S.T.A.L.K.E.R. LuaJIT & FFI Migration (`stalker-luajit-ffi-migration`)

The 64-bit OGSR Engine replaced vanilla S.T.A.L.K.E.R. Shadow of Chernobyl’s standard Lua 5.1 interpreter with **LuaJIT 64-bit** (incorporating FFI and modified Luabind registrations). Legacy mod scripts (from SoC / Complete) frequently fail silently or trigger native segmentation faults when calling altered C++ engine methods or passing unboxed pointers.

This skill establishes defensive practices for modernizing legacy S.T.A.L.K.E.R. Lua scripts.

---

## 1. Luabind vs. LuaJIT 64-bit API Discrepancies

OGSR modernized numerous C++ class exports. Legacy scripts calling non-existent or altered Luabind methods fail:

| Legacy SoC (Lua 5.1) | OGSR Engine (LuaJIT 64-bit) | Migration Rule |
| :--- | :--- | :--- |
| `npc:set_relation(relation, target)` | `npc:set_relation(relation, target)` (strict type check) | Ensure `target` is a valid `game_object`, not `nil` or ID number |
| `alife():create(..., -1)` | `alife():create(..., u16(-1))` | ID parameter must fit `u16` without overflow |
| `level.main_input_receiver()` | `level.main_input_receiver()` (returns `CUIDialogWnd*`) | Check `if receiver then` before accessing dialog methods |
| Direct memory pointer thunks | LuaJIT FFI `ffi.cast("type*", ptr)` | Use type-safe FFI structs; never pass raw integers as pointers |

---

## 2. Defensive Script Traps & Nil Guards

In legacy Lua, calling a method on an offline or dead ALife object often caused hard C++ engine exceptions inside the Luabind wrapper:

### Defensive Pattern:
```lua
-- PROHIBITED: Unchecked member access on potential offline object
function get_stalker_health(npc_id)
    local obj = level.object_by_id(npc_id)
    return obj.health -- CRASH if npc is offline, unloaded, or despawned
end

-- ENFORCED: Safe nil-guard with ALife fallback
function get_stalker_health(npc_id)
    if not npc_id or npc_id == 65535 then return 0 end
    
    local obj = level.object_by_id(npc_id)
    if obj then
        return obj.health or 0
    end
    
    -- Check if entity exists in ALife offline registry
    local se_obj = alife():object(npc_id)
    if se_obj then
        -- Return cached offline state
        return 1.0
    end
    return 0
end
```

---

## 3. LuaJIT FFI Struct Safety & Calling Conventions

When using LuaJIT FFI to interface directly with engine DLLs (`xrGame.dll`, `xrCore.dll`):
- **Calling Convention:** Windows x64 uses Microsoft fastcall convention; never specify `__stdcall` on 64-bit FFI declarations.
- **Pointer Lifetimes:** When acquiring pointers from C++ via FFI, never store raw pointers across game frame boundaries without verifying engine ownership.
- **String Passing:** Always pass `const char*` using `ffi.string()` or standard Lua strings to prevent dangling pointers after garbage collection cycles.

---

## 4. Script Triage Workflow

When debugging script CTDs:
1. Grep `xray_*.log` for Lua error traces:
   `grep -A 10 -B 2 "\[error\]Script" xray_*.log`
2. Check Lua callstack:
   `grep -A 15 "stack traceback:" xray_*.log`
3. If traceback ends inside a C++ engine thunk (`[C]: in function '...'`), isolate the exact arguments passed from the preceding Lua line to identify the invalid pointer or type mismatch.

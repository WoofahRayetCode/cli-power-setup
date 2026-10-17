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

---

## 4. Advanced Scripting Integrations

- **Modular Quality-of-Life Mechanics (`game-qol-gameplay-scripting`):** Author modular event-driven hooks (dynamic carry weight, stamina scaling, field repair kits, zone change autosaves) without rewriting vanilla core binders.
- **Companion & Follower AI Systems (`game-companion-pet-ai`):** Implement companion NPCs, pet mutants, leash thresholds, stealth suppression, and loyalty state machines in X-Ray / OGSR.
- **Dialogue Script Logic & Callbacks (`game-dialogue-ui-localization`):** Author XML precondition functions (`<precondition>script.function</precondition>`) and phrase action handlers (`<action>script.function</action>`), verifying talk UI constraints with `game-dialogue-tool`.

## Windows 10/11 & Cross-Platform Game Modding Parity (`windows-linux-cross-os-runtime-bridge`)
- **Native Windows vs. Linux Wine/Proton:** On Windows 10/11, execute `xrEngine.exe` and mod tools natively via DirectX 11/12 without Wine overhead. On Linux, route through Proton/Wine and DXVK/VKD3D.
- **LLP64 vs. LP64 64-Bit C++ Safety:** On Windows x64 MSVC/Clang-CL (LLP64), `long` and `unsigned long` (`DWORD`) are **32-bit (4 bytes)** whereas on Linux x86_64 (LP64) `long` is 64-bit. Never cast pointers to `long` or `DWORD`—always use `uintptr_t`, `intptr_t`, or `size_t`.
- **Crash Modal Interception & WER Dumps:** On Windows, `xray_crash_handler.py sweep` queries WMI (`Win32_Process`) and terminates lingering `notepad.exe`/`WerFault.exe` popups via `taskkill /F /PID`, reading logs from `%USERPROFILE%\Documents\STALKER-SHOC\logs` and `_appdata_\logs`.
- **Native Win32 Playtest Input & Window Capture:** When `sys.platform == "win32"`, `game_playtest_controller.py` automatically dispatches Win32 `keybd_event` / `mouse_event` (`SendInput`), `ClipCursor`, and `PIL.ImageGrab` instead of Linux `/dev/uinput` and `spectacle`.
- **Steam Library Auto-Discovery:** `steam-mod-scanner` automatically reads `HKCU\Software\Valve\Steam\SteamPath` and `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` on Windows alongside `~/.local/share/Steam` on Linux.

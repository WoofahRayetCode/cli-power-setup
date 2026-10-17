---
name: gamemaker-gml-engineering
description: Modern GameMaker (2024+) game development workflows in GML Code. Covers lightweight constructors/structs, state machines, delta-timing, surface memory management, texture page optimization, sound emitter hierarchies, and YYP project architecture.
---

# GameMaker & GML Code Development Guide

This skill governs 2D and 2.5D game architecture, performant GML (GameMaker Language) scripting, and cross-platform export discipline in modern **GameMaker (2024+)**.

---

## 1. Modern GML Architecture Principles

### A. Constructors & Lightweight Structs (Object Bloat Elimination)
* **The Anti-Pattern:** Creating a heavy GameMaker `object` (with full event overhead) for every particle, bullet, inventory item, or UI element.
* **The Modern Pattern:** Use lightweight constructors and structs for data-driven entities:
  ```gml
  function Item(_id, _name, _count) constructor {
      item_id = _id;
      name = _name;
      count = _count;
      
      static use = function(_user) {
          // Shared behavior via static method (0 duplicated function overhead)
          _user.hp += 10;
          count -= 1;
      };
  }
  ```

### B. Finite State Machines (FSM) via Method Variables
Replace messy nested `if/else` or gigantic `switch (state)` trees with first-class state methods:
```gml
// In Create Event
state_idle = function() {
    sprite_index = spr_player_idle;
    if (abs(input_x) > 0.1) state = state_run;
    if (input_jump) { vspd = -jump_power; state = state_jump; }
};

state_run = function() {
    sprite_index = spr_player_run;
    x += input_x * move_speed;
    if (abs(input_x) <= 0.1) state = state_idle;
};

state = state_idle;

// In Step Event
state();
```

---

## 2. Rendering, Surfaces & Memory Discipline

### A. Volatile Surface Life Cycle
Surfaces in GameMaker are volatile VRAM buffers that can be destroyed at any moment by Windows/OS focus losses, display resolution changes, or alt-tab events:
```gml
// Draw GUI or Draw Event
if (!surface_exists(surf_lighting)) {
    surf_lighting = surface_create(view_wport[0], view_hport[0]);
}

surface_set_target(surf_lighting);
draw_clear_alpha(c_black, 0.8);
// Perform additive light blending here
surface_reset_target();

draw_surface(surf_lighting, 0, 0);

// Cleanup Event (MANDATORY to prevent massive GPU VRAM memory leaks)
if (surface_exists(surf_lighting)) {
    surface_free(surf_lighting);
}
```

### B. Data Structures Cleanup (`ds_*`)
Unlike lightweight arrays and structs (which are automatically garbage-collected), traditional data structures (`ds_grid`, `ds_list`, `ds_map`, `ds_priority`) **must** be explicitly freed in the `Clean Up` event:
```gml
// Clean Up Event
if (ds_exists(grid_inventory, ds_type_grid)) {
    ds_grid_destroy(grid_inventory);
}
```
*(Tip: In modern GameMaker, prefer native Arrays and Structs over `ds_list` / `ds_map` to leverage automatic garbage collection).*

---

## 3. Texture Group & Draw Call Optimization

1. **Texture Page Swapping:**
   - Group related sprites (e.g. `tg_player`, `tg_ui`, `tg_level_forest`) into dedicated **Texture Groups** in the IDE.
   - Drawing a UI sprite, then an enemy sprite, then a UI sprite forces a texture page swap and flushes the vertex batch.
2. **Batch Break Avoidance:**
   - Changing draw color (`draw_set_color`), alpha (`draw_set_alpha`), blend mode (`gpu_set_blendmode`), or shaders within a loop breaks the vertex batch into multiple draw calls.
   - Batch similar draw operations together.

---

## 4. Delta Timing & Smooth Frame Pacing

GameMaker defaults to step-based fixed timesteps (`room_speed` / 60 FPS). For smooth variable refresh rates (144Hz, 240Hz, or Steam Deck 40Hz):
```gml
// In global initialization script
#macro DT (delta_time / 1000000)

// In Step Event movement
x += (hspd * target_fps) * DT;
y += (vspd * target_fps) * DT;
```

## Related & Interoperating Skills
- **`csharp-dotnet-engineering`**: Modern C# and .NET 8/9 engineering standards. Use when writing C# applications, Unity/Godot C# logic, memory o...
- **`godot-game-dev`**: Game development workflows for Godot Engine (GDScript 2.0 & C#). Use when designing game systems, scene trees,...
- **`unreal-engine-dev`**: Game development workflows for Unreal Engine 5 (C++ and Blueprints). Use when implementing Gameplay Framework ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

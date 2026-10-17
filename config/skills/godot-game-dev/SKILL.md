---
name: godot-game-dev
description: Game development workflows for Godot Engine (GDScript 2.0 & C#). Use when designing game systems, scene trees, custom nodes, signals, UI layouts, or running headless Godot CLI builds and GUT tests.
---

# Godot Engine Development Guide

This skill governs game development within the **Godot Engine** (Godot 4.x), focusing on GDScript 2.0 and modular node architecture.

## Core Architecture Principles

### 1. Scene & Node Lifecycle
- **Node Tree Discipline:**
  - Avoid tight coupling with hardcoded node paths (e.g. `get_node("../../Parent/Player")`).
  - Use **Signals up, functions down**: parent nodes call methods on child nodes; child nodes emit signals to communicate upwards.
  - Separate initialization logic:
    - Use `_enter_tree()` only when establishing scene tree hierarchy.
    - Use `_ready()` for initializing references (`@onready`) and connecting signals.
    - Keep physics and collision movements strictly inside `_physics_process(delta)`.
    - Use `_process(delta)` strictly for non-physics visual updates and animations.

### 2. GDScript 2.0 Best Practices
- **Strict Static Typing:**
  - Always use explicit type hints for variables, function parameters, and return types (`var speed: float = 200.0`, `func take_damage(amount: int) -> void:`).
  - Static typing enables compiler optimizations, reduces runtime type checking overhead, and catches errors during static analysis.
- **Exporting Variables:**
  - Use `@export` with explicit types or groupings (`@export_group("Combat")`, `@export_range(0, 100) var health: int = 100`).
- **Resource Management:**
  - Leverage custom `Resource` classes for data-driven design (inventories, stats, weapon configs) rather than monolithic singleton managers.

### 3. Headless CLI & Testing
- Run headless checks and exports via terminal:
  ```bash
  godot --headless --path . --check-only
  godot --headless --path . -s addons/gut/gut_cmdln.gd
  ```
- Use GUT (Godot Unit Test) framework for automated logic testing before manual visual verification.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`unity-game-dev`**: Game development workflows for Unity Engine (C#). Use when developing MonoBehaviours, ScriptableObjects, physi...
- **`godot-shader-vfx`**: Authoring 2D and 3D visual shaders, canvas item shaders, spatial shaders, particle systems, and screen-reading...
- **`modern-cpp-engineering`**: Modern C++ standards (C++20/C++23) and systems engineering. Use when authoring or debugging C++ code, game eng...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

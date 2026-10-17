---
name: modern-cpp-engineering
description: Modern C++ standards (C++20/C++23) and systems engineering. Use when authoring or debugging C++ code, game engine plugins, DLLs, memory management with RAII, smart pointers, Concepts, or managing CMake builds.
---

# Modern C++ Engineering Guide

This skill governs modern C++ development (C++20 / C++23), focusing on memory safety, RAII, zero-cost abstractions, and preventing compilation thrashing.

## Core Architectural Principles

### 1. Modern Memory & Pointer Discipline
- **Zero Naked `new` / `delete`:**
  - Memory allocation must follow strict RAII (Resource Acquisition Is Initialization).
  - Use `std::make_unique<T>()` for exclusive ownership.
  - Use `std::make_shared<T>()` only when shared lifetime is genuinely required.
  - Use `std::span<T>` and `std::string_view` for non-owning, zero-copy buffer and string parameters.

### 2. Modern C++20 / C++23 Idioms
- **Concepts & Constraints:** Use `template <typename T> requires ...` or `template <std::integral T>` to produce clean, readable compiler errors instead of massive SFINAE template spews.
- **Move Semantics:** Implement move constructors and move assignment operators (`noexcept`) for custom resource-managing classes. Follow the Rule of Zero or Rule of Five.
- **Structure Binding & Optional Values:**
  - Use structured bindings (`auto [key, val] : map`).
  - Use `std::optional<T>` and `std::expected<T, E>` for recoverable error handling rather than output pointer arguments or sentinel error values.

### 3. Build & Static Analysis
- Maintain clean CMake targets (`target_include_directories(PRIVATE ...)`, `target_compile_features(cxx_std_20)`).
- Verify code cleanliness with Clang tooling:
  ```bash
  clang-tidy -p build/ path/to/file.cpp
  clang-format -i path/to/file.cpp
  ```

## Cross-OS Windows 10/11 & Linux Runtime Bridge (`windows-linux-cross-os-runtime-bridge`)
- **Unified Windows & Linux Execution:** Pair with `windows-linux-cross-os-runtime-bridge` for portable CPU thread saturation (`os.cpu_count()` / `$env:NUMBER_OF_PROCESSORS` / `$(nproc)`), scratch staging (`Path(tempfile.gettempdir())` / `R:\` RAMDisk / `/dev/shm`), and dual-GPU routing (Windows `UserGpuPreferences` vs Linux `DRI_PRIME`).
- **Dynamic Cheat Sheet, Git Sync & Self-Evolution:** Consult `agy-cheatsheet` (`cs` / `dynamic-repo-model-cheatsheet`) for live per-repo model/effort selection, commit verified milestones via `repo-auto-sync <repo> --checkpoint --push` (`autonomous-git-repo-sync-governor`), and promote reusable cross-OS scripts via `skill-evolve` (`self-evolving-skill-synthesizer`).

## Related & Interoperating Skills
- **`rust-engineering`**: Rust software engineering and compiler-first workflows. Use when authoring or debugging Rust code, managing li...
- **`godot-game-dev`**: Game development workflows for Godot Engine (GDScript 2.0 & C#). Use when designing game systems, scene trees,...
- **`csharp-dotnet-engineering`**: Modern C# and .NET 8/9 engineering standards. Use when writing C# applications, Unity/Godot C# logic, memory o...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

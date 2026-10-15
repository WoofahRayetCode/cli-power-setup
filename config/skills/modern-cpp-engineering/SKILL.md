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

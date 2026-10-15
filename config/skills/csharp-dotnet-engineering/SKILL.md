---
name: csharp-dotnet-engineering
description: Modern C# and .NET 8/9 engineering standards. Use when writing C# applications, Unity/Godot C# logic, memory optimization with Span and Memory, async/await cancellation patterns, or running dotnet test and Roslyn analyzers.
---

# Modern C# and .NET Engineering Guide

This skill governs C# software development across modern .NET 8/9 and game engine C# scripting (Unity / Godot).

## Core Architectural Principles

### 1. High-Performance & Memory Efficiency
- **Zero-Allocation Data Slicing:**
  - Use `ReadOnlySpan<T>` and `ReadOnlyMemory<T>` for parsing binary streams, strings, or file buffers without heap allocations.
  - Use `ArrayPool<T>.Shared` for temporary large buffers.
- **Value Types vs Reference Types:**
  - Use `readonly record struct` for small, immutable data transfer objects (DTOs) and vectors.
  - Use `sealed class` by default on reference types to enable JIT devirtualization optimizations.

### 2. Async/Await & Cancellation Discipline
- Always pass `CancellationToken` through all asynchronous method chains (`async Task MyMethodAsync(CancellationToken cancellationToken = default)`).
- Avoid `Task.Run` for I/O-bound operations; use native asynchronous I/O APIs (`FileStream.ReadAsync`, `HttpClient.GetAsync`).
- Never use `.Result` or `.Wait()` on asynchronous tasks (risks threadpool starvation and deadlocks). Use `await`.

### 3. Modern Language Features (C# 11 - 13)
- Use file-scoped namespaces (`namespace MyProject.Core;`) to reduce indentation clutter.
- Enforce nullable reference types (`<Nullable>enable</Nullable>`) and resolve all nullability warnings at compile time.
- Use pattern matching with property patterns and relational patterns (`if (obj is Player { Health: > 0, IsInvulnerable: false })`).

### 4. Build & Roslyn Verification
- Check code against analyzers with zero warnings:
  ```bash
  dotnet build --no-incremental /p:TreatWarningsAsErrors=true
  dotnet test --logger "console;verbosity=normal"
  ```

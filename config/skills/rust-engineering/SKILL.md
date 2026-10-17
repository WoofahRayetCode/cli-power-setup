---
name: rust-engineering
description: Rust software engineering and compiler-first workflows. Use when authoring or debugging Rust code, managing lifetimes and the borrow checker, designing zero-cost abstractions, or running Cargo check, Clippy, and tests.
---

# Rust Engineering & Compiler-First Workflow

This skill governs Rust programming, leveraging the compiler as an instant verification tool to eliminate hallucination and borrow-checker thrashing loops.

## Core Engineering Principles

### 1. Ownership & Idiomatic Borrowing
- Do NOT sprinkle `.clone()` to bypass borrow checker errors.
- Design data structures with clear ownership boundaries:
  - Prefer passing borrowed references (`&str`, `&[T]`) rather than owned values (`String`, `Vec<T>`) for read-only access.
  - Use `Cow<'a, str>` or `Arc<T>` when shared ownership is genuinely required across threads.
- Robust Error Handling:
  - Avoid `.unwrap()` and `.expect()` in production library code.
  - Use `thiserror` for typed library errors and `anyhow` for application/CLI boundaries with context (`.context("failed to parse header")?`).

### 2. Fast Compiler Feedback Loop
- Before running heavy builds or test suites, run fast compiler checks:
  ```bash
  cargo check --message-format=short
  cargo clippy -- -D warnings
  ```
- Read compiler diagnostic suggestions directly—they give exact line numbers and borrowing corrections.
- Make targeted 1-line edits via `replace_file_content` to fix the specific diagnostic rather than rewriting whole structs.

### 3. Idiomatic Memory & Concurrency
- Use standard iterators (`.filter()`, `.map()`, `.collect()`) for zero-cost abstraction optimizations.
- Use `crossbeam` or `tokio` channels for message passing rather than shared mutable state where possible.

## Cross-OS Windows 10/11 & Linux Runtime Bridge (`windows-linux-cross-os-runtime-bridge`)
- **Unified Windows & Linux Execution:** Pair with `windows-linux-cross-os-runtime-bridge` for portable CPU thread saturation (`os.cpu_count()` / `$env:NUMBER_OF_PROCESSORS` / `$(nproc)`), scratch staging (`Path(tempfile.gettempdir())` / `R:\` RAMDisk / `/dev/shm`), and dual-GPU routing (Windows `UserGpuPreferences` vs Linux `DRI_PRIME`).
- **Dynamic Cheat Sheet, Git Sync & Self-Evolution:** Consult `agy-cheatsheet` (`cs` / `dynamic-repo-model-cheatsheet`) for live per-repo model/effort selection, commit verified milestones via `repo-auto-sync <repo> --checkpoint --push` (`autonomous-git-repo-sync-governor`), and promote reusable cross-OS scripts via `skill-evolve` (`self-evolving-skill-synthesizer`).

---
name: rust-engineering
description: Rust development, Cargo builds, borrow checker, lifetimes, zero-cost abstractions, and clippy.
---

# Rust Software Engineering (`rust-engineering`)

Zero-cost abstractions, memory safety, and production-grade Rust systems development.

## Core Guidelines
- **Toolchains & Cargo:** Manage dependencies with `Cargo.toml`, enforce `cargo clippy --all-targets -- -D warnings`, and format with `cargo fmt`.
- **Ownership & Lifetimes:** Prefer borrowing (`&T`, `&mut T`) over cloning. Use `Cow<'a, T>` for flexible allocation. Avoid `Rc<RefCell<T>>` in multi-threaded contexts; use `Arc<RwLock<T>>` or message channels (`tokio::sync::mpsc`, `crossbeam`).
- **Error Handling:** Use `thiserror` for library domain errors and `anyhow` for top-level application boundaries. Never leave naked `.unwrap()` calls in production code.
- **Unsafe Boundaries:** Encapsulate all `unsafe` blocks with strict invariant proofs in comments (`// SAFETY: ...`).

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`modern-cpp-engineering`**: Modern C++20/23 standards, CMake 3.25+, RAII, smart pointers, 64-bit alignment, and memory sanitizers.
- **`token-economy`**: Output token containment: zero conversational fluff, high-density status, silent tools, and surgical diffs.
- **`python-engineering`**: Python 3.11+ software engineering, typed async, Ruff, Mypy, pytest, and performance profiling.
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

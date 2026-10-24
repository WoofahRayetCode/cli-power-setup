---
name: python-engineering
description: Python 3.11+ software engineering, typed async, Ruff, Mypy, pytest, and performance profiling.
---

# Modern Python Engineering (`python-engineering`)

Production Python software engineering adhering to Python 3.11+ standards, strict typing, high-speed linting, and robust testing.

## Standards
- **Typing & Annotations:** Annotate all public functions with `typing` and built-in generics (`list[str]`, `dict[str, Any]`, `X | None`). Verify with `mypy --strict`.
- **Toolchain:** Format and lint with Ruff (`ruff check .`, `ruff format .`). Manage virtual environments cleanly via `.venv`.
- **Testing:** Comprehensive test suites using `pytest -v`. Write test fixtures cleanly in `conftest.py`.
- **Performance:** Use `__slots__` on high-volume data classes. Profile hot paths with `cProfile` and replace Python loops with NumPy or Cython extensions.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`linux-systems-engineering`**: Linux systems programming, POSIX, io_uring, systemd, CachyOS/Arch packaging, and laptop ACPI controls.
- **`rust-engineering`**: Rust development, Cargo builds, borrow checker, lifetimes, zero-cost abstractions, and clippy.
- **`database-network-engineering`**: SQLite WAL tuning, PostgreSQL schemas, raw TCP/UDP, tshark packet capture, and cryptographic security.

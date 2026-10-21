---
name: linux-systems-engineering
description: Linux systems programming, POSIX, io_uring, systemd, CachyOS/Arch packaging, and laptop ACPI controls.
---

# Linux Systems Engineering (`linux-systems-engineering`)

Low-level Linux systems programming, asynchronous I/O, systemd service architecture, Arch/CachyOS packaging, and laptop performance management.

## Capabilities
- **POSIX & Modern Async I/O:** Systems programming in C/C++/Rust using epoll, eventfd, timerfd, and high-performance `io_uring`.
- **Systemd Daemons & Units:** Design secure systemd service units with sandboxing (`ProtectSystem=strict`, `PrivateTmp=yes`, `NoNewPrivileges=yes`).
- **Arch / CachyOS Packaging:** Author PKGBUILDs, DKMS modules, and kernel patches adhering to Arch packaging standards.
- **Laptop Performance & Thermal Governor:**
  Control acoustics, TDP, and fan curves via:
  `laptop-perf [status|sleep-mode|balanced|performance|boost]`
  Script: `~/.claude/skills/linux-systems-engineering/scripts/laptop_performance_controller.py`

## Related & Interoperating Skills
- **`cross-platform-web-desktop`**: Cross-platform desktop and extension development with Tauri 2.0 (Rust), Electron IPC, and Manifest V3.
- **`python-engineering`**: Python 3.11+ software engineering, typed async, Ruff, Mypy, pytest, and performance profiling.
- **`modern-web-architecture`**: Modern Jamstack and SSG development with Astro, VitePress, Content Collections, and GitHub Pages CI/CD.

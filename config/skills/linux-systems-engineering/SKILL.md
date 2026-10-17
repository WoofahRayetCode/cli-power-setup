---
name: linux-systems-engineering
description: Linux systems programming in C/C++/Rust, POSIX APIs, asynchronous I/O (epoll, io_uring), process/signal management, systemd service units, and diagnostics (strace, gdb, perf, sanitizers).
---

# Linux Systems Engineering & POSIX Development

This skill standardizes low-level Linux systems programming, kernel interface interactions, systemd service design, and deep runtime diagnostics.

---

## 🐧 Core Focus Areas

1. **POSIX APIs & High-Performance I/O:** File descriptors, non-blocking I/O, `epoll`, `io_uring`, and memory-mapped files (`mmap`).
2. **Process & Signal Architecture:** Process lifecycles (`fork`/`execve`), daemonization, real-time signals, `sigaction`, and zombie reaping (`waitpid`).
3. **Systemd Service Design:** Production-grade unit authoring (`Type=notify`), watchdog integration (`WatchdogSec`), cgroups v2 resource quotas, and security sandboxing.
4. **Deep Runtime Diagnostics:** Syscall tracing (`strace`), core dump inspection (`gdb`, `coredumpctl`), memory sanitizers (ASan, UBSan, TSan), and Linux perf/eBPF analysis.

---

## ⚙️ 1. High-Performance I/O & Event Loops

When building high-throughput Linux services or background daemons:

* **Event Multiplexing with `epoll`:**
  * Use edge-triggered mode (`EPOLLET`) with non-blocking sockets (`O_NONBLOCK`):
  ```c
  struct epoll_event ev;
  ev.events = EPOLLIN | EPOLLET | EPOLLRDHUP;
  ev.data.fd = sockfd;
  epoll_ctl(epollfd, EPOLL_CTL_ADD, sockfd, &ev);
  ```
* **Modern Asynchronous I/O with `io_uring`:**
  * Prefer `io_uring` for high-IOPS disk or network operations to avoid syscall context switches:
  * Submit submission queue entries (SQEs) and harvest completion queue entries (CQEs) in batches.
* **Memory-Mapped Files (`mmap`):**
  * Map large binary files directly into address space (`PROT_READ`, `MAP_SHARED` or `MAP_PRIVATE` with `madvise(MADV_SEQUENTIAL)`).

---

## 🛡️ 2. Production-Grade Systemd Units

Author hardened systemd service units for background daemons (e.g. `/etc/systemd/system/myservice.service`):

```ini
[Unit]
Description=My Low-Level Linux Service
After=network.target
Wants=network.target

[Service]
Type=notify
ExecStart=/usr/local/bin/myservice --config /etc/myservice/config.toml
Restart=always
RestartSec=5s
WatchdogSec=15s

# Hardened Security Sandboxing
ProtectSystem=strict
ProtectHome=read-only
PrivateTmp=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
NoNewPrivileges=true
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX

[Install]
WantedBy=multi-user.target
```

---

## 🔍 3. Systematic Diagnostics & Triage

* **Syscall Tracing (`strace`):**
  * Trace syscall performance bottlenecks and file access:
    ```bash
    strace -f -tt -T -e trace=file,network,process -o trace.log ./target_bin
    ```
* **Core Dump Analysis (`gdb` / `coredumpctl`):**
  * Extract stack traces from crashes:
    ```bash
    coredumpctl debug
    (gdb) bt full
    (gdb) info registers
    ```
* **Memory Sanitizers:** Compile with `-fsanitize=address,undefined -fno-omit-frame-pointer` during CI/testing.

---

## 🔄 Interoperability & Handoffs

* **Handoff to `bash-posix-automation`:** For service management shell scripts and automated install pipelines.
* **Handoff to `linux-desktop-packaging`:** When packaging systemd-integrated services into Flatpak/AppImage bundles.
* **Handoff to `cmake-cross-platform`:** When abstracting Linux POSIX calls behind portable cross-platform interfaces.\n

## Windows 10/11 Native Counterparts (`windows-linux-cross-os-runtime-bridge`)
- **Packages & Toolchains:** Use `winget` / `scoop` / `choco` and `vswhere.exe` (MSVC / Clang-CL) on Windows in place of `pacman` / `yay`. For desktop packaging on Windows, target MSIX / WiX / WinGet manifests (`windows-app-engineering`).
- **Profiling & Time-Travel Debugging:** On Windows 10/11, use **Windows Performance Recorder (`wpr -start GeneralProfile` / `wpa.exe`)** in place of Linux `perf`, and **WinDbg Preview Time-Travel Debugging (`ttd.exe -launch <app.exe>`)** in place of Mozilla `rr`.
- **Hardware, Thermal & Power Profiles:** Query sensors via WMI/CIM (`Get-CimInstance -Namespace root/wmi MSAcpi_ThermalZoneTemperature`, `nvidia-smi`) and switch power plans via `powercfg /setactive` on Windows.
- **File System Hot-Reload & ADB:** Use `.NET System.IO.FileSystemWatcher` (`Register-ObjectEvent`) on Windows in place of `inotifywait`, and resolve `adb.exe` from `%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe`.

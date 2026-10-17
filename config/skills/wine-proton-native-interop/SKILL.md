---
name: wine-proton-native-interop
description: Native Linux and Wine/Proton interop engineering. Covers Win32-to-Linux IPC sockets, shared memory shims, Wine DLL call thunking, custom Wine builtin modules, and running hybrid native/Proton tooling.
---

# Wine & Proton Native Linux Interop Engineering

This skill provides advanced systems patterns for bridging native Linux host capabilities (POSIX daemons, Unix Domain Sockets, pipe communication, Wayland/Vulkan extensions) with Windows applications running inside Wine or Proton.

---

## 1. Win32 to Linux Host Communication Channels

When a game or tool running in Proton needs to communicate with a native Linux companion app (e.g. OBS Studio, hardware sensor daemon, Discord RPC):

### A. Named Pipe / Unix Domain Socket Bridge
Proton exposes Unix domain sockets directly to the Windows environment via Wine's named pipe mapping:
- Windows Path: `\\.\pipe\my_custom_service`
- Native Linux Path: `~/.steam/steam/steamapps/compatdata/<appid>/pfx/dosdevices/pipe/my_custom_service`

A native Linux Python or Rust daemon can listen on this socket and exchange JSON messages with the Windows game process in real time with sub-millisecond latency.

### B. Shared Memory (shm) Mapping
For high-bandwidth telemetry (frame buffers, audio streams):
- Use Win32 `CreateFileMappingA(INVALID_HANDLE_VALUE, ...)` in the game.
- Wine maps anonymous shared memory into the host Linux kernel tmpfs (`/dev/shm`), allowing zero-copy inspection by native host tools.

---

## 2. Wine DLL Call Thunking

To call native Linux shared libraries (`.so`) directly from a Windows PE application running under Proton:
1. Author a dual-personality Wine builtin DLL (`my_bridge.dll.so`):
   - Compiles against Wine headers (`wine/debug.h`, `winternl.h`).
   - Translates Windows 64-bit ABI calling conventions into native System V AMD64 ABI.
   - Forwards function parameters directly to host Linux libraries (`libvulkan.so`, `libasound.so`, `libpipewire.so`).
2. Register the thunk library in Wine's builtin list via `WINEDLLOVERRIDES="my_bridge=b"`.

---

## 3. Wine Debugging & Relay Traces

To trace exact API calls passing between the game executable and Wine/Proton:
```bash
# Trace all Win32 API calls made by the game to isolate hanging functions
WINEDEBUG=+relay,+seh python3 "$PROTON_PATH/proton" run Game.exe 2>&1 | grep -v "ntdll"
```
* Identifies exactly which Win32 API call hung or returned `STATUS_NOT_IMPLEMENTED`.

## Cross-OS Windows 10/11 & Linux Runtime Bridge (`windows-linux-cross-os-runtime-bridge`)
- **Unified Windows & Linux Execution:** Pair with `windows-linux-cross-os-runtime-bridge` for portable CPU thread saturation (`os.cpu_count()` / `$env:NUMBER_OF_PROCESSORS` / `$(nproc)`), scratch staging (`Path(tempfile.gettempdir())` / `R:\` RAMDisk / `/dev/shm`), and dual-GPU routing (Windows `UserGpuPreferences` vs Linux `DRI_PRIME`).
- **Dynamic Cheat Sheet, Git Sync & Self-Evolution:** Consult `agy-cheatsheet` (`cs` / `dynamic-repo-model-cheatsheet`) for live per-repo model/effort selection, commit verified milestones via `repo-auto-sync <repo> --checkpoint --push` (`autonomous-git-repo-sync-governor`), and promote reusable cross-OS scripts via `skill-evolve` (`self-evolving-skill-synthesizer`).

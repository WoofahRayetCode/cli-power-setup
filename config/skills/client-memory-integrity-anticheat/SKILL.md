---
name: client-memory-integrity-anticheat
description: In-depth client runtime security, anti-debugging, memory scanner detection, obfuscated value storage (XOR/bitwise masks), and anti-tamper heartbeat synchronization for desktop games and sensitive client apps.
---

# Client Runtime Memory Integrity & Anti-Cheat Architecture

This skill provides native patterns and architectures for protecting client-side applications and games from memory scanners (Cheat Engine), dynamic debuggers (x64dbg, IDA, GDB, Frida), and illegal runtime hooks.

---

## 1. Obfuscated / Masked Value Storage

Never store critical gameplay or application values (player health, ammo, premium currency, auth state) as raw contiguous 32-bit/64-bit integers in memory. Memory search utilities easily scan for `100 -> 90 -> 80`:

### XOR + Monotonic Key Encryption Pattern (C++ / Python)
```cpp
template <typename T>
class ObfuscatedValue {
private:
    T encrypted_val;
    uint32_t key;

public:
    ObfuscatedValue(T initial) {
        set(initial);
    }

    void set(T val) {
        key = rand() ^ 0x5A5A5A5A;
        encrypted_val = val ^ key;
    }

    T get() const {
        return encrypted_val ^ key;
    }
};
```
* **Defense Effect:** Searching memory for integer `100` yields zero matches because the memory location stores a pseudo-random value that re-keys on every mutation.

---

## 2. Dynamic Anti-Debugging & Hook Detection

### A. Windows Native Anti-Debug Probes
```cpp
#include <windows.h>
#include <winternl.h>

bool is_debugger_present() {
    // 1. Direct Win32 API Check
    if (IsDebuggerPresent()) return true;

    // 2. Direct PEB (Process Environment Block) BeingDebugged flag
    PPEB pPeb = (PPEB)__readgsqword(0x60); // x64 PEB
    if (pPeb && pPeb->BeingDebugged) return true;

    // 3. Hardware Breakpoint Trap (DR0 - DR3 registers)
    CONTEXT ctx = { 0 };
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
    HANDLE hThread = GetCurrentThread();
    if (GetThreadContext(hThread, &ctx)) {
        if (ctx.Dr0 || ctx.Dr1 || ctx.Dr2 || ctx.Dr3) return true;
    }

    return false;
}
```

### B. Linux / POSIX Anti-Debug via `ptrace`
```c
#include <sys/ptrace.h>
#include <unistd.h>

bool check_linux_debugger() {
    // Attempt to trace self. If another debugger (GDB/Frida) is already attached, it fails.
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
        return true; // Debugger detected!
    }
    return false;
}
```

---

## 3. Server-Authoritative Simulation & Heartbeat Validation

In networked multiplayer or synced single-player systems:
1. **Never Trust the Client:**
   - The client only sends **inputs** (keys pressed, joystick deltas), never outcomes (e.g. `I took 0 damage` or `I am at position X,Y,Z`).
2. **Periodic State Heartbeats:**
   - The client periodically computes a rolling hash of its memory state and active loaded DLLs, signing it with a session key.
   - If a client fails 3 consecutive heartbeats or sends an inconsistent state hash, quarantine the connection gracefully.

## Related & Interoperating Skills
- **`game-security-anti-tamper`**: Game engine runtime security, anti-tamper architectures, memory modification detection, DLL hijacking preventi...
- **`game-memory-scanner`**: High-performance game memory scanner and pointer discovery engine for Linux & Windows/Proton games. Scans virt...
- **`game-trainer-engineering`**: Cross-platform game trainer development across Windows and Linux. Covers dynamic memory scanning, multi-level ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

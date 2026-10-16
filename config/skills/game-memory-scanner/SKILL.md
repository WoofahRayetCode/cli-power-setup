---
name: game-memory-scanner
description: High-performance game memory scanner and pointer discovery engine for Linux & Windows/Proton games. Scans virtual memory ranges, filters candidates iteratively (exact, increased, decreased, changed), resolves multi-level pointer paths, performs AOB wildcard signature scans, and freezes addresses.
---

# Game Memory Scanner & Dynamic Pointer Engine (`game-memory-scanner`)

The `game-memory-scanner` skill provides low-level virtual memory inspection, dynamic value scanning, candidate filtering, pointer path resolution, and AOB signature pattern matching for PC games running natively on Linux or through Steam Proton / Wine.

---

## 1. Core Architecture

```
                          Target Game Process
                   (Native Linux or Wine / Proton)
                                 │
                                 ▼
                     /proc/<pid>/maps Inspection
                 (Filter: 'rw-p' heap, stack, data)
                                 │
                                 ▼
                    [ game-memory-scanner scan ]
             Initial Pass: Searches 4MB blocks for value
                                 │
                                 ▼
                     Candidate Addresses JSON
                                 │
                      Game State Mutates (Take Hit)
                                 │
                                 ▼
                   [ game-memory-scanner filter ]
       Second Pass: Keeps only 'decreased' or exact match
                                 │
                                 ▼
                 Resolved Entity Health / Ammo Offset
                                 │
           +─────────────────────┴─────────────────────+
           ▼                                           ▼
[ game-memory-scanner freeze ]             [ pointer-scan & AOB ]
 Locks value at 100ms intervals             Finds base module pointer chain
```

---

## 2. CLI Tool Reference (`game-memory-scanner`)

Companion utility: `game-memory-scanner` (installed to `~/.local/bin/game-memory-scanner`).

### A. Initial Memory Scan (`scan`)
Scans all writable heap and data memory regions in the target process for an initial value:
```bash
# Scan for initial player health (e.g. 100 as 32-bit int)
game-memory-scanner scan --target "xrEngine.exe" --type i32 --value 100 --output /tmp/health_candidates.json

# Scan for player stamina / coordinates as 32-bit float
game-memory-scanner scan --target "game_linux" --type f32 --value 1.0 --output /tmp/stamina_candidates.json
```

### B. Iterative Candidate Filtering (`filter`)
After mutating the in-game value (taking damage, firing a round, spending currency), filter candidate addresses:
```bash
# Filter for exact new health value after taking a hit
game-memory-scanner filter --candidates /tmp/health_candidates.json --value 85

# Filter for relative change when exact value is unknown (e.g. health bar)
game-memory-scanner filter --candidates /tmp/health_candidates.json --condition decreased

# Repeat until candidate list narrows to 1–3 surviving addresses
```

### C. AOB (Array of Bytes) Signature Scanning (`aob`)
Locate code functions and instructions across game updates using wildcard byte signatures in executable (`r-xp`) sections:
```bash
# Scan executable code for player damage calculation routine
game-memory-scanner aob --target "xrEngine.exe" --pattern "48 89 5C 24 ?? 57 48 83 EC 20 48 8B D9"
```

### D. Direct Memory Read / Write (`read` / `write`)
Inspect or alter live values directly:
```bash
# Read live value at address
game-memory-scanner read --target "xrEngine.exe" --addr 0x7FFE9402B0 --type i32

# Overwrite live value (e.g. set ammo to 999)
game-memory-scanner write --target "xrEngine.exe" --addr 0x7FFE9402B0 --type i32 --value 999
```

### E. Memory Freeze Cheat Loop (`freeze`)
Locks an address by continuously writing the desired value at a given frequency, preventing engine subtractions:
```bash
# Freeze health to 100 (updates every 50ms)
game-memory-scanner freeze --target "xrEngine.exe" --addr 0x7FFE9402B0 --type i32 --value 100 --interval 0.05
```

### F. Multi-Level Pointer Scanning (`pointer-scan`)
Discovers pointers referencing dynamic heap addresses:
```bash
# Search for base pointers pointing to the dynamic health address within a 0x1000 offset
game-memory-scanner pointer-scan --target "xrEngine.exe" --target-addr 0x7FFE9402B0 --max-offset 0x800
```

---

## 3. Linux & Steam Proton / Wine System Permissions

Reading `/proc/<pid>/mem` across processes on modern Linux kernels requires ptrace permissions:

```bash
# Temporarily enable ptrace for game debugging (resets on reboot)
echo 0 | sudo tee /proc/sys/kernel/yama/ptrace_scope

# Permanent setting in /etc/sysctl.d/10-ptrace.conf:
# kernel.yama.ptrace_scope = 0
```

---
name: game-security-anti-tamper
description: Game engine runtime security, anti-tamper architectures, memory modification detection, DLL hijacking prevention, save file HMAC integrity seals, server-side simulation sanity validation, and anti-teleport physics checks. Use when securing multiplayer games, protecting save files against hex editing, or hardening game binaries against injection.
---

# Game Security & Anti-Tamper Engineering

This skill defines defensive standards, integrity verification pipelines, and runtime protections against cheating, memory modification, DLL injection, and save file tampering in video game engines.

---

## 1. Threat Vectors in Video Games

```text
┌─────────────────────────────────────────────────────────────┐
│                      Attack Surface                         │
├──────────────────────────────┬──────────────────────────────┤
│ Client-Side Memory Injection │ Cheat Engine, DLL Detours    │
│ DLL Hijacking / Proxying     │ Malicious version.dll/dxgi   │
│ Save File / Inventory Tamper │ Hex editing currency/health  │
│ Network Desync Exploits      │ Fake teleportation, godmode  │
└──────────────────────────────┴──────────────────────────────┘
```

---

## 2. Save File & Asset HMAC Integrity Seals

Never trust client-stored save files without cryptographic authentication:
* **HMAC-SHA256 Signature Header:**
  Append an HMAC signature to the save file footer or header using a server-managed or engine-obfuscated key:
  $$	ext{Tag} = 	ext{HMAC-SHA256}(K, 	ext{Payload})$$
* **Constant-Time Signature Verification:**
  Always compare signatures using constant-time algorithms (`CRYPTO_memcmp` or `hmac.compare_digest`) to prevent timing side-channel attacks.
* **Save State Monotonic Counter:**
  Embed a monotonic version counter and UTC timestamp. Reject save files with counter values lower than the player's last recorded server progress (prevents rollback duplication exploits).

---

## 3. DLL Hijacking & Injection Defenses

### A. Safe DLL Loading Order (Windows Win32)
Malicious actors often drop a proxy `version.dll` or `dxgi.dll` into the game directory:
```cpp
// Call immediately at entry point (WinMain / main):
SetDefaultDllDirectories(LOAD_LIBRARY_SEARCH_SYSTEM32);
SetDllDirectoryA(""); // Remove current working directory from search path
```

### B. Module Verification
Before calling third-party plugins or dynamically loaded libraries (`LoadLibraryExW`), verify the Authenticode digital signature via `WinVerifyTrust` with `WINTRUST_ACTION_GENERIC_VERIFY_V2`.

---

## 4. Multiplayer Server-Side Simulation Sanity Gates

Client-side prediction must always be bounded by authoritative server sanity rules:
* **Speed & Teleport Validation:**
  $$\Delta \mathbf{P}_{\max} = (v_{\max} \cdot \Delta t) + \epsilon_{	ext{latency}}$$
  If $\lVert \mathbf{P}_{	ext{client}} - \mathbf{P}_{	ext{prev}} Vert > \Delta \mathbf{P}_{\max}$, snap player back to valid state.
* **Raycast Line-of-Sight Checks:**
  Never accept client-reported bullet hits directly. The server must trace a ray through the world geometry from the shooter's verified position to verify line-of-sight before registering damage.

---
name: argon-deep-memory-allocator-sanitizer
description: Mathematical 64-bit pointer, struct padding, and memory alignment sanitizer for Gemini 4 Argon. Eliminates pointer truncation and alignment faults in legacy C++ game engine ports.
---

# Argon Deep Memory Allocator Sanitizer (`argon-deep-memory-allocator-sanitizer`)

When modernizing or modding 32-bit legacy game engines (e.g. S.T.A.L.K.E.R. X-Ray to 64-bit OGSR Engine), subtle memory bugs cause silent heap corruption and elusive runtime crashes under Wine/Proton.

This skill directs Argon's deep reasoning engine (`--effort high` / `pro`) to formally prove memory safety, struct alignment, and pointer bitness integrity before modifying engine code.

---

## 1. 64-Bit Bitness & Alignment Invariants

1. **Pointer-to-Integer Truncation:**
   - **Fatal:** Casting pointers to `u32`, `DWORD`, `unsigned long`, or `int` (truncates 64-bit addresses to 32 bits on Linux/x86_64).
   - **Mandatory:** Always use `uintptr_t`, `intptr_t`, or `size_t`.
2. **Struct Padding & Serialization Invariance:**
   - Binary game save files and network packets expect exact 32-bit byte offsets.
   - When compiling on 64-bit, 8-byte pointer alignment inserts implicit padding bytes, corrupting saved games.
   - **Mandatory:** Enforce `#pragma pack(push, 1)` or explicit alignas qualifiers on serialized struct headers.
3. **LuaJIT GC64 Memory Boundaries:**
   - 64-bit LuaJIT requires pointers passed through FFI/Luabind to stay within the 47-bit virtual address space or use GC64 mode.
   - Audit all raw userdata pointers returned to Lua scripts to ensure pointer integrity.

---

## 2. Pre-Modification Reasoning Checklist

When modifying any memory allocator, container, or pointer-casting method in C++:
- [ ] Is every integer holding an address typed as `uintptr_t`?
- [ ] Does any struct member change offset across 32-bit vs 64-bit compilation?
- [ ] Are SIMD types (`__m128`, `DirectX::XMVECTOR`) aligned to 16-byte boundaries?
- [ ] Are dynamic memory allocations freed using matching engine allocators (`xr_delete` / `xr_free` vs standard `delete`/`free`)?

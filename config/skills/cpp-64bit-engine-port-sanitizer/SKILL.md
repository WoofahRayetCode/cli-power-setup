---
name: cpp-64bit-engine-port-sanitizer
description: Detects and repairs 64-bit bitness porting defects in C++ game engines (e.g. X-Ray/OGSR). Audits pointer-to-integer truncations, #pragma pack(1) struct padding discrepancies, 64-bit ABI calling convention drift, and virtual method table alignment.
---

# C++ 64-bit Engine Port Sanitizer (`cpp-64bit-engine-port-sanitizer`)

Migrating legacy 32-bit game engines (e.g. X-Ray 1.0006) to 64-bit architectures (e.g. OGSR 64-bit) introduces subtle memory corruption bugs, heap corruption, and hard crashes that evade standard compiler warnings.

This skill governs the systematic detection, diagnosis, and remediation of 64-bit bitness porting defects.

---

## 1. Pointer Truncation & Integer Safety

In 32-bit x86 architectures, pointers and integers (`DWORD`, `long`, `unsigned int`) are both 32-bit. In 64-bit x86_64 architectures (LLP64 on Windows, LP64 on Linux), pointers are **64-bit**, while `int` and `long` (on Win64) remain **32-bit**.

### Anti-Patterns & Safe Replacements:
```cpp
// PROHIBITED: Truncates upper 32 bits of 64-bit address -> CRASH on heap > 4GB
DWORD ptrVal = (DWORD)pObject;
int callbackId = (int)pCallback;

// ENFORCED: Portable pointer-sized integer types
uintptr_t ptrVal = (uintptr_t)pObject;
intptr_t callbackId = (intptr_t)pCallback;
size_t bufferSize = sizeof(DataPacket);
```

### Audit Rule:
- Search for dangerous casts across all engine headers:
  `grep -rnE "\((DWORD|unsigned int|long|int)\)\s*&?[a-zA-Z0-9_]+->?[a-zA-Z0-9_]*" src/`

---

## 2. Struct Packing & Memory Alignment (`#pragma pack`)

Legacy 32-bit engines often packed structs with `#pragma pack(push, 1)` for disk serialization (save states, network packets). In 64-bit, unaligned 64-bit pointers and integers cause severe performance degradation on x86_64 or hard hardware bus faults on ARM64.

### Audit & Safe Pattern:
```cpp
// PROHIBITED: Struct with mixed pointers and packed bytes without explicit padding
#pragma pack(push, 1)
struct LegacySaveHeader {
    char magic[4];     // 4 bytes
    void* pEngineData; // 8 bytes in 64-bit (offset 4 is NOT 8-byte aligned!)
};
#pragma pack(pop)

// ENFORCED: Explicit padding and fixed-width disk types
#pragma pack(push, 1)
struct SafeSaveHeader {
    char     magic[4];       // 4 bytes
    uint32_t reserved;       // 4 bytes explicit padding to align 64-bit int
    uint64_t engineDataUid;  // 8-byte persistent ID instead of in-memory pointer
};
#pragma pack(pop)
static_assert(sizeof(SafeSaveHeader) == 16, "SafeSaveHeader size mismatch");
```

---

## 3. ABI & Calling Convention Harmonization

- **x86 Legacy:** `__cdecl`, `__stdcall`, `__thiscall`, `__fastcall` had distinct stack and register semantics.
- **x64 Unified ABI:** 64-bit Windows uses a single unified calling convention (RCX, RDX, R8, R9 register passing).
- **Audit:** Replace legacy `__thiscall` and `__stdcall` function pointer typedefs with portable standard macros:
  ```cpp
  #if defined(_WIN64) || defined(__x86_64__)
      #define ENGINE_API
  #else
      #define ENGINE_API __stdcall
  #endif
  ```

---

## 4. Virtual Table (vtable) Alignment & Multiple Inheritance

When classes use multiple inheritance with virtual methods:
- In 64-bit, each virtual base pointer (`vptr`) is 8 bytes instead of 4 bytes.
- Never use raw byte offset math (`*(char**)this + offset`) to access member variables or virtual tables. Always use standard `reinterpret_cast` or `dynamic_cast`.

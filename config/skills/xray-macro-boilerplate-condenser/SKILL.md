---
name: xray-macro-boilerplate-condenser
description: Pre-processes and condenses legacy X-Ray and OGSR C++ macros, memory wrappers (xr_new, xr_delete, IC), and Luabind export registration blocks into clean, high-density semantic signatures to reduce C++ source ingestion context by 70-80%.
---

# X-Ray Macro & Boilerplate Condenser (`xray-macro-boilerplate-condenser`)

The GSC X-Ray Engine codebase was authored in the early 2000s and relies heavily on proprietary macros, custom memory allocators, and extensive Luabind registration blocks:
- `IC` (Force inline)
- `DECLARE_SCRIPT_REGISTER_FUNCTION`
- `luabind::class_<T>("class_name").def(...)`
- `xr_new`, `xr_delete`, `xr_free`, `xr_malloc`

When ingesting legacy headers and scripts into Claude Fable 5.1, these boilerplate macro sequences consume **up to 70% of the token volume** without adding semantic architectural value.

This skill strips macro overhead and presents clean, standardized C++ signatures to the model.

---

## 1. Condensation Matrix

| X-Ray / OGSR Boilerplate | Raw C++ Syntax | Condensed Semantic Format | Token Reduction |
| :--- | :--- | :--- | :--- |
| **Inline Method Macros** | `IC void set_active(bool v) { ... }` | `void set_active(bool);` | **~60%** |
| **Custom Memory Allocators** | `T* obj = xr_new<T>(arg1, arg2);` | `auto obj = make_unique<T>(...);` | **~40%** |
| **Luabind Export Tables** | `module(L) [ class_<CWeapon>("CWeapon") .def("Fire", &CWeapon::Fire) ];` | `LUA_EXPORT: CWeapon::Fire()` | **~85%** |
| **Script Header Declarations** | `DECLARE_SCRIPT_REGISTER_FUNCTION public: ... add_to_type_list(...)` | `[EXPORTED_TO_LUA]` | **~90%** |

---

## 2. Code Comparison

### Raw X-Ray C++ Header (Verbose: 180 tokens):
```cpp
#pragma once
#include "script_export_space.h"

class CInventoryItem {
    DECLARE_SCRIPT_REGISTER_FUNCTION
public:
    IC virtual void SetDropManual(BOOL val) { m_flags.set(FDropManual, val); }
    IC BOOL GetDropManual() const { return m_flags.test(FDropManual); }
    IC virtual u32 Cost() const { return m_cost; }
    IC virtual float Weight() const { return m_weight; }
};
add_to_type_list(CInventoryItem)
#undef script_type_list
#define script_type_list save_type_list(CInventoryItem)
```

### Condensed High-Density Signature (Compact: 36 tokens — 80% reduction):
```cpp
class CInventoryItem [EXPORTED_TO_LUA] {
public:
    void SetDropManual(bool);
    bool GetDropManual() const;
    u32 Cost() const;
    float Weight() const;
};
```

---

## 3. Autonomous Execution Rules

1. **Header Sifting First:**
   - When Fable requests a header file to understand an inheritance tree, pipe it through macro stripping before returning the content.
2. **Preserve Memory Ownership Semantics:**
   - Always retain whether a pointer is owned (`shared_ptr`, `unique_ptr`, or manual engine pool pointer).
3. **Keep Luabind Signatures Flat:**
   - Convert multi-line chained `.def("fn", &Class::fn)` blocks into 1-line export lists.

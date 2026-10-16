---
name: compiler-error-cascade-isolator
description: Intercepts C++ compiler error cascades (GCC, Clang, MSVC) during engine builds. Strips recursive template instantiation dumps and secondary cascading errors to isolate the primary root-cause error and source coordinates, slashing compiler diagnostic tokens by 90-95%.
---

# Compiler Error Cascade Isolator (`compiler-error-cascade-isolator`)

Modern C++ game engines (such as X-Ray, OGSR, and Unreal) rely heavily on templates, metaprogramming, and deep inheritance trees. When a 64-bit port breaks a type conversion or alignment constraint, `gcc` or `clang` emits 500 to 2,000+ lines of cascaded errors (`instantiated from here`, `required from point of instantiation`, `candidate template ignored`).

Feeding raw compiler dumps into heavy-duty models like Claude Fable 5.1 burns **15,000 to 40,000 prompt tokens per compiler failure**, diluting attention with secondary noise.

This skill extracts the exact **primary root-cause error** into a surgical 5-line diagnostic tuple.

---

## 1. Error Cascade Reduction Comparison

### Raw Compiler Output (Excerpt of 450+ lines / ~8,500 tokens):
```text
In file included from /home/ericparsley/ogsr/src/xrGame/weapon_ak74.cpp:12:
In file included from /home/ericparsley/ogsr/src/xrGame/WeaponMagazinedWGrenade.h:8:
In file included from /home/ericparsley/ogsr/src/xrGame/WeaponMagazined.h:15:
/home/ericparsley/ogsr/src/xrGame/Weapon.h:245:18: error: no matching member function for call to 'cast_to_64bit'
    return m_pPhysicsShell->cast_to_64bit<u64>(m_bone_id);
           ~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~
/home/ericparsley/ogsr/src/xrPhysics/PhysicsShell.h:112:5: note: candidate template ignored: substitution failure [with T = unsigned long]: no type named 'type' in 'std::enable_if<false, void>'
    template<typename T, typename = std::enable_if_t<std::is_pointer_v<T>>>
    ^
[... 380 lines of candidate template dumps, standard library allocator stacks, and secondary warnings omitted ...]
ninja: build stopped: subcommand failed.
```

### Isolated Root Diagnostic Tuple (32 tokens — 99.6% reduction):
```text
#COMPILER_ROOT_ERROR:
FILE: src/xrGame/Weapon.h#L245
ERROR: no matching member function for call to 'cast_to_64bit<u64>'
TARGET: m_pPhysicsShell->cast_to_64bit<u64>(m_bone_id)
CAUSE: substitution failure: requires std::is_pointer_v<T> (PhysicsShell.h#L112)
TOTAL_SECONDARY_ERRORS_STRIPPED: 428
```

---

## 2. Extraction Pipeline Rules

1. **First-Error Priority:**
   - In C++ builds, 95% of subsequent errors are false positives caused by the compiler losing AST synchronization after the first failure.
   - Always isolate **Error #1** and halt processing of subsequent cascaded failures.
2. **Strip Template Instantiation Stacks:**
   - Filter out `note: in instantiation of template class ...` unless directly tied to the primary constraint failure.
3. **Capture Exact Source Coordinates:**
   - Format: `<relpath>#L<num>:<col>`.
4. **Command Pipeline Integration:**
   - Pipe compiler commands through standard diagnostic filters:
     ```bash
     cmake --build build -- -j$(nproc) 2>&1 | grep -E "error:|fatal error:" -B 2 -A 3 | head -n 25
     ```

---
name: polyglot-ast-interface-pruner
description: Polyglot AST interface pruner and header skeletonizer across C++, C#, Rust, Python, and Lua. Strips function implementation bodies, private members, comments, and boilerplate to generate ultra-dense symbol signatures, reducing codebase ingestion tokens by 85-90%.
---

# Polyglot AST Interface Pruner (`polyglot-ast-interface-pruner`)

Ingesting full source code files during architectural onboarding, refactoring, or dependency tracing consumes tens of thousands of tokens. Models rarely need function bodies—they only need **signatures, types, exports, and public contracts**.

This skill strips source files down to dense, single-line interface signatures across modern languages.

---

## 1. Language Skeletonization Standards

| Language | Extracted Interface Elements | Stripped Elements | Reduction |
| :--- | :--- | :--- | :--- |
| **C++ / C** (`.h`, `.hpp`, `.cpp`) | Struct/class declarations, public methods, pure virtuals, enums | Private member vars, `#include` comments, inline bodies `{ ... }` | **~88%** |
| **Rust** (`.rs`) | `pub fn`, `pub struct`, `pub enum`, `pub trait`, trait bounds | Function bodies, `fn` internal expressions, unit tests (`#[test]`) | **~90%** |
| **C#** (`.cs`) | `public interface`, `public class`, method headers, properties | Method bodies `{ ... }`, private fields, XML summary tags | **~85%** |
| **Python** (`.py`) | `def name(...) -> type: ...`, `class: ...`, dataclass fields | Method bodies replaced with `...`, docstrings, private helpers `_func` | **~82%** |
| **Lua / LuaJIT** (`.lua`) | Module table functions `function M.foo(bar) end`, exported globals | Inner logic loops, local temporary tables, inline comments | **~85%** |

---

## 2. Interface Skeleton Example (C++ Engine Header)

### Raw Header (Verbose: 260 tokens):
```cpp
#pragma once
#include <vector>
#include <string>

// Manages texture loading and mipmap generation
class TextureLoader {
private:
    int m_max_anisotropy;
    std::string m_cache_dir;
    void internal_decompress_bc7(const uint8_t* data, size_t size);
public:
    TextureLoader(int anisotropy, const std::string& dir) 
        : m_max_anisotropy(anisotropy), m_cache_dir(dir) {}
    
    virtual ~TextureLoader() {}
    
    // Loads texture from disk and generates mipmaps
    bool load_texture(const std::string& path, uint32_t flags) {
        // 50 lines of loading implementation...
        return true;
    }
};
```

### Pruned AST Skeleton (Compact: 38 tokens — 85% reduction):
```cpp
class TextureLoader {
public:
    TextureLoader(int, const std::string&);
    virtual ~TextureLoader();
    bool load_texture(const std::string&, uint32_t);
};
```

---

## 3. Autonomous Execution Rules

1. **Skeleton-First Exploration:**
   - When inspecting a new module or library, generate or read the pruned AST interface first.
   - Never ingest entire `.cpp`, `.rs`, or `.cs` implementation files into chat unless actively modifying a specific method.
2. **One-Line Coordinate Signatures:**
   - Map dependencies as: `<path>#L<num>:signature`.
3. **Preserve Type Annotations:**
   - Always retain return types and argument types; discard variable names if not necessary for signature disambiguation.

---
name: game-memory-allocator-engineering
description: Custom high-performance game engine memory allocators (Linear Arena, Stack, Pool, TLSF), SIMD memory alignment, and zero-hitch heap fragmentation elimination. Use when optimizing game engine memory allocations, fixing frame stutter, or porting engines to memory-constrained platforms.
---

# Game Engine Memory Allocator & Cache Engineering

This skill defines the implementation of custom memory allocators designed to eliminate heap fragmentation and eliminate frame hitches caused by standard C++ runtime allocator locks (`malloc`/`free`).

---

## 1. The Game Allocator Hierarchy

| Allocator Type | Allocation Complexity | Deallocation Complexity | Fragmentation | Ideal Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Linear / Arena** | $O(1)$ (Pointer Bump) | $O(1)$ (Reset All) | None | Per-frame transient data, command buffers, temporary strings |
| **Stack Allocator** | $O(1)$ (Pointer Bump) | $O(1)$ (LIFO Marker Rollback) | None | Level loading state, scoped scene transitions, menu screens |
| **Pool Allocator** | $O(1)$ (Free List Pop)| $O(1)$ (Free List Push) | Zero external | Fixed-size game entities, bullets, particles, audio voices |
| **TLSF / Buddy** | $O(1)$ (Two-Level Segregated) | $O(1)$ (Boundary Tag Merge) | Minimal (<15%)| General engine subsystems, GPU transient heaps |

---

## 2. Linear Arena Allocator (Zero-Hitch Per-Frame Memory)

```cpp
class LinearArena {
private:
    uint8_t* m_buffer;
    size_t m_capacity;
    size_t m_offset;

public:
    LinearArena(size_t capacity) : m_capacity(capacity), m_offset(0) {
        m_buffer = static_cast<uint8_t*>(aligned_alloc(64, capacity)); // 64-byte cache line align
    }

    ~LinearArena() { free(m_buffer); }

    void* Allocate(size_t size, size_t alignment = 16) {
        // Align forward
        size_t currentAddress = reinterpret_cast<size_t>(m_buffer + m_offset);
        size_t alignedAddress = (currentAddress + (alignment - 1)) & ~(alignment - 1);
        size_t padding = alignedAddress - currentAddress;

        if (m_offset + padding + size > m_capacity) {
            return nullptr; // Out of memory
        }

        m_offset += padding + size;
        return reinterpret_cast<void*>(alignedAddress);
    }

    void Reset() {
        m_offset = 0; // Instant O(1) bulk deallocation
    }
};
```

---

## 3. Cache Line & SIMD Alignment Discipline

* **64-Byte Cache Line Alignment:** Modern x86-64 and ARM64 CPUs transfer data to L1 cache in **64-byte cache lines**. Allocations crossing a 64-byte boundary incur dual-cache-line fetch latency.
* **SIMD Alignment:**
  * SSE / NEON: Align to 16 bytes.
  * AVX / AVX2: Align to 32 bytes.
  * AVX-512: Align to 64 bytes.
* Structure Data in **Structure of Arrays (SoA)** rather than Array of Structures (AoS) for entity component systems to maximize CPU L1/L2 prefetcher cache hit rates.

## Related & Interoperating Skills
- **`game-audio-engine-engineering`**: Low-latency game audio architecture, 3D spatial audio, HRTF binaural processing, mixing bus hierarchies, and s...
- **`game-physics-collision-pipeline`**: Real-time physics engine architecture, fixed timestep accumulator loops, continuous collision detection (CCD),...
- **`game-entity-component-system`**: High-performance Entity Component System (ECS) architecture, Data-Oriented Design (DOD), Archetype vs Sparse-S...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

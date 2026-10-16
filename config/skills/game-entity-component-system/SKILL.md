---
name: game-entity-component-system
description: High-performance Entity Component System (ECS) architecture, Data-Oriented Design (DOD), Archetype vs Sparse-Set storage, Structure-of-Arrays (SoA) memory layout, and multithreaded system scheduling. Use when designing game engine logic, optimizing cache misses, or porting object-oriented game code to ECS.
---

# Game Entity Component System (ECS) & Data-Oriented Design

This skill provides architectural standards for high-throughput Entity Component Systems, data-oriented memory layouts, cache line optimization, and parallel system iteration in game engines.

---

## 1. Core Architectural Paradigms

### A. Data-Oriented Design (DOD) vs Object-Oriented (OOP)
* **OOP Pitfall (Array of Structures - AoS):**
  `struct Monster { Vector3 pos; Matrix44 animMatrix; float health; SoundEffect hitSound; };`
  Iterating over positions burns memory bandwidth loading 128+ bytes per entity when only 12 bytes (`Vector3`) are needed, incurring constant CPU L1/L2 cache misses.
* **DOD Standard (Structure of Arrays - SoA):**
  Store component fields contiguously in homogeneous, cache-line-aligned arrays. When updating physics or rendering, the CPU stream loads pure contiguous payload without cache pollution.

### B. Archetype Storage vs Sparse-Set Storage
| Pattern | Memory Layout | Iteration Speed | Add/Remove Component Cost | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **Archetype** (Flecs, Unity DOTS, Bevy) | Contiguous tables grouped by exact component signature | Maximum (Pure flat memory stream) | Higher (Entity must move tables) | Stable entity compositions, massive batch queries |
| **Sparse-Set** (EnTT) | Sparse array of entity IDs pointing to packed dense component array | High (Dense component array iteration) | Ultra-fast ($O(1)$ swap-and-pop) | Highly dynamic components, frequent adds/removes, flags |

---

## 2. Component Storage & Memory Alignment

### Contiguous Dense Array Layout (C++20 Reference)
```cpp
template<typename T>
class DenseComponentPool {
    alignas(64) std::vector<T> m_DenseData;
    std::vector<uint32_t> m_DenseToEntity;
    std::vector<uint32_t> m_EntityToDense; // Sparse lookup (indexed by entity ID)

public:
    T* TryGet(uint32_t entityId) {
        if (entityId >= m_EntityToDense.size()) return nullptr;
        uint32_t idx = m_EntityToDense[entityId];
        if (idx == UINT32_MAX) return nullptr;
        return &m_DenseData[idx];
    }

    void Emplace(uint32_t entityId, T&& component) {
        if (entityId >= m_EntityToDense.size()) {
            m_EntityToDense.resize(entityId + 1, UINT32_MAX);
        }
        uint32_t denseIdx = static_cast<uint32_t>(m_DenseData.size());
        m_EntityToDense[entityId] = denseIdx;
        m_DenseToEntity.push_back(entityId);
        m_DenseData.push_back(std::forward<T>(component));
    }

    void Remove(uint32_t entityId) {
        uint32_t denseIdx = m_EntityToDense[entityId];
        uint32_t lastIdx = static_cast<uint32_t>(m_DenseData.size() - 1);
        uint32_t lastEntity = m_DenseToEntity[lastIdx];

        // Swap and pop
        m_DenseData[denseIdx] = std::move(m_DenseData[lastIdx]);
        m_DenseToEntity[denseIdx] = lastEntity;
        m_EntityToDense[lastEntity] = denseIdx;

        m_DenseData.pop_back();
        m_DenseToEntity.pop_back();
        m_EntityToDense[entityId] = UINT32_MAX;
    }

    T* Data() { return m_DenseData.data(); }
    size_t Size() const { return m_DenseData.size(); }
};
```

---

## 3. Multithreaded System Scheduling & Access Masks

* **Read/Write Access Bitmasks:**
  Every system registers its read and write component masks before execution:
  * Two systems can execute concurrently if neither writes to a component that the other reads or writes.
  * System Dependency Graph: Directed Acyclic Graph (DAG) automatically resolved per frame:
    $$	ext{CanParallel}(S_A, S_B) = (W_A \cap (R_B \cup W_B) = \emptyset) \land (W_B \cap (R_A \cup W_A) = \emptyset)$$
* **Command Buffer Staging:**
  Systems executing in worker threads must **never** mutate the entity hierarchy (create entity, destroy entity, add/remove component) directly during query iteration. Structural changes are staged into a thread-local `EntityCommandBuffer` and flushed synchronously at frame phase barriers.

---

## 4. Entity Lifecycle & Generational IDs

```text
Entity ID (64-bit):
[ 32-bit Generation Counter ] [ 32-bit Index ]
```
* **Dangling Reference Defense:** When an entity is destroyed, increment its generation counter. Stale handles from other systems or scripts instantly fail the generation check (`handle.gen == registry.gen[handle.idx]`), eliminating use-after-free pointer corruption.

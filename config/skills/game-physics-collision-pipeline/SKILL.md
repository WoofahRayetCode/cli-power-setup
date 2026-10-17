---
name: game-physics-collision-pipeline
description: Real-time physics engine architecture, fixed timestep accumulator loops, continuous collision detection (CCD), broadphase BVH spatial hashing, narrowphase GJK/EPA solvers, and Jolt/PhysX integration. Use when porting physics runtimes, fixing tunneling, or optimizing simulation performance.
---

# Game Physics Engine & Collision Pipeline Engineering

This skill defines the mathematical mechanics, broadphase/narrowphase algorithms, and deterministic timestep loops for game physics engines (Jolt Physics, PhysX, Havok, Box2D).

---

## 1. The Semi-Implicit Euler Accumulator Loop

> [!IMPORTANT]
> Never advance physics simulation with raw variable delta time (`dt = frameTime`). Variable timesteps break determinism, destabilize spring constraints, and cause erratic collision tunneling.

Always use a **fixed timestep accumulator loop** with state interpolation:

```cpp
const float fixedDelta = 1.0f / 60.0f; // 60Hz fixed simulation step
float accumulator = 0.0f;

void UpdateGame(float frameDelta) {
    // Prevent "spiral of death" during severe frame drops
    frameDelta = std::min(frameDelta, 0.25f);
    accumulator += frameDelta;

    while (accumulator >= fixedDelta) {
        // Save previous transforms for render interpolation
        PhysicsSavePreviousState();
        // Fixed physics step
        PhysicsStepSimulation(fixedDelta);
        accumulator -= fixedDelta;
    }

    // Alpha blend factor for render interpolation: [0.0, 1.0]
    float alpha = accumulator / fixedDelta;
    RenderInterpolate(alpha);
}
```

---

## 2. Collision Pipeline Architecture

```text
[ All Objects in Scene ]
          │
          ▼
   [ 1. Broadphase ] ──► Dynamic AABB Tree / Spatial Hash Grid (O(N log N))
          │            (Rejects clearly separated pairs)
          ▼
   [ 2. Midphase ]   ──► Compound shapes & mesh triangle queries
          │
          ▼
   [ 3. Narrowphase ]──► GJK (Overlap test) + EPA (Penetration depth & normal)
          │
          ▼
   [ 4. Constraint ] ──► Projected Gauss-Seidel / Sequential Impulses (PGS)
```

### A. Broadphase: Dynamic AABB Tree
* Store bounding boxes with a "fattened" margin (skin thickness of 0.02m) so moving objects don't trigger tree re-balances on every frame.
* Fast raycasting and frustum queries traverse the tree with branch bounding box rejection.

### B. Narrowphase: GJK & EPA
* **GJK (Gilbert-Johnson-Keerthi):** Finds if the Minkowski difference $A - B$ contains the origin via a simplex (point, line, triangle, tetrahedron).
* **EPA (Expanding Polytope Algorithm):** When GJK detects an overlap, EPA expands the simplex polytope toward the surface of $A - B$ to compute the **minimal penetration depth** and **contact normal vector**.

### C. Continuous Collision Detection (CCD)
* Fast-moving projectiles (bullets, arrows) will tunnel through thin walls in discrete collision detection.
* **Raycast / Sphere Cast:** Sweep the bounding sphere along the velocity vector:
  $$\text{Ray}(t) = P_0 + t \cdot \vec{v}, \quad t \in [0, \Delta t]$$

## Related & Interoperating Skills
- **`game-audio-engine-engineering`**: Low-latency game audio architecture, 3D spatial audio, HRTF binaural processing, mixing bus hierarchies, and s...
- **`game-debug-ui-tools`**: In-engine debug UI systems, Dear ImGui integration, immediate-mode 3D debug drawing (AABBs, rays, contact mani...
- **`game-networking-state-sync`**: Multiplayer network architecture, client-side prediction, server reconciliation, entity interpolation, snapsho...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

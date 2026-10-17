---
name: game-3d-linear-algebra-quaternions
description: 3D/4D linear algebra, change-of-basis similarity transforms (UE5 <-> X-Ray/OGSR <-> Blender), quaternion SLERP/dual-quaternions, Euler HPB/PYR conversions, and MikkTSpace tangent handedness math.
---

# Game 3D Linear Algebra, Coordinate Bases & Quaternions

## When to Use
Activate this skill whenever:
- Porting 3D meshes, skeletal rigs (`FTransform`), animations, camera trajectories, or spawn coordinates across engines (**Unreal Engine 5 / S.T.A.L.K.E.R. 2**, **S.T.A.L.K.E.R. X-Ray / OGSR**, **Blender 5.2+**, **Godot**, **Unity**).
- Constructing or debugging 4x4 affine transformation matrices (`Fmatrix` / `_matrix<float>`), rotation quaternions (`Fquaternion`), or Euler angles (`setHPB` / `getHPB` vs `FRotator`) without gimbal lock or flipped normals.
- Computing MikkTSpace tangent/bitangent sign ($w \in \{-1, +1\}$) or Normal Map Y-channel inversion (DirectX $-Y$ vs OpenGL $+Y$).

---

## 1. Cross-Engine Coordinate Basis & Unit Matrix Ledger

Every engine defines handedness, up-axis, forward-axis, unit scale, and matrix memory layout differently. **Never swap coordinates ad-hoc**; always apply the formal change-of-basis permutation matrix $B$ and scale factor $s$:

| Engine / Tool | Handedness | Right | Up | Forward | Unit Scale | Matrix Layout |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **X-Ray / OGSR (`Fmatrix`)** | **Left-Handed** | `+X` (`i`) | `+Y` (`j`) | `+Z` (`k`) | `1.0` m | Row-Major (`v * M`) |
| **Unreal Engine 5 (S.T.A.L.K.E.R. 2)** | **Left-Handed** | `+Y` | `+Z` | `+X` | `0.01` m (`cm`) | Row-Major (`v * M`) |
| **Blender 5.2+ (`bpy`)** | **Right-Handed** | `+X` | `+Z` | `-Y` (or `+Y`) | `1.0` m | Column-Major (`M @ v`) |
| **Godot 4 / OpenGL / glTF** | **Right-Handed** | `+X` | `+Y` | `-Z` | `1.0` m | Column-Major |

### Exact UE5 (S.T.A.L.K.E.R. 2) $\rightarrow$ X-Ray / OGSR Transformation
Both UE5 and X-Ray are **Left-Handed**, meaning the basis change is a pure **even cyclic axis permutation** ($\det(B) = +1$, preserving winding order and avoiding inside-out triangle flips!):
- **Position Mapping ($\text{cm} \rightarrow \text{m}$):**
  $$P_{\text{XRay}} = 0.01 \cdot \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{bmatrix} \begin{bmatrix} X_{\text{UE5}} \\ Y_{\text{UE5}} \\ Z_{\text{UE5}} \end{bmatrix} = \begin{bmatrix} 0.01 \, Y_{\text{UE5}} \\ 0.01 \, Z_{\text{UE5}} \\ 0.01 \, X_{\text{UE5}} \end{bmatrix}$$
- **Quaternion Mapping ($\det(B) = +1 \implies$ pure component permutation, no sign flip!):**
  $$Q_{\text{XRay}} = \left(q_x, q_y, q_z, q_w\right)_{\text{XRay}} = \left(q_y^{\text{UE5}},\; q_z^{\text{UE5}},\; q_x^{\text{UE5}},\; q_w^{\text{UE5}}\right)$$
- **Linear 3x3 / 4x4 Matrix Similarity Transform:**
  $$M_{\text{XRay}} = B \, M_{\text{UE5}} \, B^T, \quad B = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{bmatrix}$$

### Exact Blender (Right-Handed Z-Up) $\leftrightarrow$ X-Ray / OGSR (Left-Handed Y-Up)
Converting between Right-Handed Z-Up (Blender) and Left-Handed Y-Up (X-Ray) uses the reflection permutation $B_{\text{B2X}}$ ($\det(B_{\text{B2X}}) = -1$, swapping $Y \leftrightarrow Z$):
- **Position & Normal Mapping:**
  $$P_{\text{XRay}} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & 1 & 0 \end{bmatrix} \begin{bmatrix} X_B \\ Y_B \\ Z_B \end{bmatrix} = \begin{bmatrix} X_B \\ Z_B \\ Y_B \end{bmatrix}$$
- **Quaternion Mapping ($\det = -1$ requires negating the axial vector components or $w$):**
  $$Q_{\text{XRay}} = \left(-q_x^B,\; -q_z^B,\; -q_y^B,\; q_w^B\right) \equiv \left(q_x^B,\; q_z^B,\; q_y^B,\; -q_w^B\right)$$
- **Triangle Winding Order:** Because $\det(B_{\text{B2X}}) = -1$, you **must** swap triangle indices $(i_0, i_1, i_2) \rightarrow (i_0, i_2, i_1)$ during `.ogf` / `.dm` binary export so backface culling in X-Ray/OGSR remains outward-facing.

---

## 2. X-Ray / OGSR `Fmatrix` (`_matrix<T>`) & `HPB` Euler Math

In `ogsr_engine/xrCore/_matrix.h`, X-Ray stores a 4x4 row-major matrix as four 4D row vectors:
- `i` (`_11, _12, _13, _14`): Right axis ($+X$)
- `j` (`_21, _22, _23, _24`): Up axis ($+Y$)
- `k` (`_31, _32, _33, _34`): Direction / Forward axis ($+Z$)
- `c` (`_41, _42, _43, _44`): Translation ($T_x, T_y, T_z, 1$)

### Heading-Pitch-Bank (`setHPB` / `getHPB`) Exact Formula
In X-Ray (`_matrix::setHPB(h, p, b)` where $h = \text{yaw around } Y$, $p = \text{pitch around } X$, $b = \text{bank/roll around } Z$):
$$\begin{aligned}
\mathbf{i} &= \begin{bmatrix} -ch \cdot cb + sh \cdot sp \cdot sb, & cp \cdot sb, & sh \cdot cb + ch \cdot sp \cdot sb \end{bmatrix} \\
\mathbf{j} &= \begin{bmatrix} sh \cdot cb + ch \cdot sp \cdot cb, & cp \cdot cb, & -ch \cdot sb + sh \cdot sp \cdot cb \end{bmatrix} \\
\mathbf{k} &= \begin{bmatrix} -sh \cdot cp, & sp, & ch \cdot cp \end{bmatrix}
\end{aligned}$$
where $sh = \sin(h), ch = \cos(h), sp = \sin(p), cp = \cos(p), sb = \sin(b), cb = \cos(b)$.
- Notice that for zero pitch/bank ($p=0, b=0$), a positive heading $h$ points the forward vector $\mathbf{k}$ along $(-\sin h, 0, \cos h)$.

---

## 3. Quaternion Mathematics, SLERP & Dual Quaternions

### Unit Quaternion Operations
For unit quaternions $q = (\mathbf{v}, w) = (x, y, z, w)$ with $\|q\|^2 = x^2 + y^2 + z^2 + w^2 = 1$:
- **Hamilton Product ($q_1 \otimes q_2$):**
  $$q_1 \otimes q_2 = \left(w_1 \mathbf{v}_2 + w_2 \mathbf{v}_1 + \mathbf{v}_1 \times \mathbf{v}_2,\; w_1 w_2 - \mathbf{v}_1 \cdot \mathbf{v}_2\right)$$
- **Fast Vector Rotation ($\mathbf{p}' = q \otimes (\mathbf{p}, 0) \otimes q^*$):**
  $$\mathbf{t} = 2 (\mathbf{v} \times \mathbf{p}), \quad \mathbf{p}' = \mathbf{p} + w \mathbf{t} + (\mathbf{v} \times \mathbf{t})$$
  *(Requires only 15 multiplications and 15 additions—faster than converting to a 3x3 matrix for single vectors).*
- **Double-Cover Antipodal Guard (Critical before SLERP/NLERP):**
  Because $q$ and $-q$ represent the exact same 3D rotation, **always** check the dot product before interpolating keyframes:
  $$\text{if } (q_0 \cdot q_1 < 0) \implies q_1 \leftarrow -q_1$$
  Omitting this causes 360-degree bone spins on S.T.A.L.K.E.R. weapon reload and NPC animations!
- **Spherical Linear Interpolation (SLERP):**
  $$\text{slerp}(q_0, q_1, t) = \frac{\sin((1-t)\Omega)}{\sin\Omega} q_0 + \frac{\sin(t\Omega)}{\sin\Omega} q_1, \quad \cos\Omega = |q_0 \cdot q_1|$$
  *(Fallback to normalized linear interpolation $\text{nlerp}(q_0, q_1, t)$ when $\cos\Omega > 0.9995$ to prevent $0/0$ division).*

---

## 4. MikkTSpace Tangent Frame & Normal Map Handedness

For a triangle with positions $(\mathbf{p}_0, \mathbf{p}_1, \mathbf{p}_2)$ and UVs $((u_0, v_0), (u_1, v_1), (u_2, v_2))$:
$$\Delta \mathbf{p}_1 = \mathbf{p}_1 - \mathbf{p}_0, \quad \Delta \mathbf{p}_2 = \mathbf{p}_2 - \mathbf{p}_0, \quad \Delta u_1 = u_1 - u_0, \quad \Delta v_1 = v_1 - v_0, \quad \Delta u_2 = u_2 - u_0, \quad \Delta v_2 = v_2 - v_0$$
$$r = \frac{1}{\Delta u_1 \Delta v_2 - \Delta u_2 \Delta v_1}, \quad \mathbf{T}_{\text{raw}} = r (\Delta v_2 \Delta \mathbf{p}_1 - \Delta v_1 \Delta \mathbf{p}_2), \quad \mathbf{B}_{\text{raw}} = r (\Delta u_1 \Delta \mathbf{p}_2 - \Delta u_2 \Delta \mathbf{p}_1)$$
- **Gram-Schmidt Orthogonalization:**
  $$\mathbf{T} = \text{normalize}\!\left(\mathbf{T}_{\text{raw}} - (\mathbf{N} \cdot \mathbf{T}_{\text{raw}})\mathbf{N}\right), \quad w = \text{sign}\!\left((\mathbf{N} \times \mathbf{T}) \cdot \mathbf{B}_{\text{raw}}\right) \in \{-1, +1\}$$
- **DirectX (X-Ray / OGSR / UE5) vs OpenGL Normal Map Green Channel:**
  DirectX uses top-left UV origin ($+V$ points down), whereas OpenGL uses bottom-left ($+V$ points up). To convert an OpenGL normal map to X-Ray/OGSR/DX11 without re-baking:
  $$G_{\text{DX}} = 255 - G_{\text{GL}} \quad \Longleftrightarrow \quad N_y \leftarrow -N_y$$

---

## 5. Local Zero-Quota CLI Verification (`game-math-solver`)

Use `game-math-solver` in `~/.local/bin/` to execute exact coordinate basis transforms, quaternion conversions, and symbolic matrix proofs locally on CPU:
```bash
game-math-solver coord --from ue5 --to xray --pos 250 -400 120 --quat 0.0 0.0 0.70710678 0.70710678
game-math-solver coord --from blender --to xray --pos 1.5 3.2 0.8
```

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`cross-engine-3d-import-export-bridge`**: Unified Blender 5.2+ to Game Engine 3D export matrix covering Unreal Engine 5 (Nanite/UCX), Godot 4.x (.glb/-c...
- **`game-animation-skeletal-pipeline`**: Real-time skeletal animation, quaternion slerp/nlerp interpolation, dual quaternion skinning, inverse kinemati...
- **`game-texture-material-pipeline`**: High-performance asset pipelines for modern PBR and legacy game textures. Use when converting textures across ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

---
name: physics-ballistics-ode-numerical-math
description: Game physics mathematics, Open Dynamics Engine (ODE) ERP/CFM LCP constraint solver equations (X-Ray/OGSR xrPhysics), frame-rate independent exponential damping, external ballistics ODEs, and RK4/Symplectic Euler integration.
---

# Game Physics, Ballistics ODEs, Ragdoll Constraints & Numerical Integration

## When to Use
Activate this skill whenever:
- Tuning or debugging S.T.A.L.K.E.R. X-Ray / OGSR physics (`xrPhysics` / `PHWorld.h` / Open Dynamics Engine `ODE`), ragdoll joints, destructible props, doors, or vehicle suspensions (`ERP`, `CFM`, `fixed_step = 0.01f`).
- Eliminating high-framerate (120Hz–240Hz) physics jitter, camera recoil drift, or UI spring oscillation using exact frame-rate independent exponential decay.
- Calculating external weapon ballistics (`k_air`, bullet drop, sight zeroing angle, time-of-flight, kinetic penetration energy) in LTX configurations and C++ projectile steppers.

---

## 1. Open Dynamics Engine (ODE) Constraint Solver Math (`ERP` & `CFM`)

S.T.A.L.K.E.R. X-Ray and 64-bit OGSR (`ogsr_engine/xrGame/PHWorld.h`) use the **Open Dynamics Engine (ODE)** Linear Complementarity Problem (LCP) solver (`dWorldQuickStep`).
Joints and contacts are governed by two fundamental LCP parameters:
- **$\text{ERP} \in (0, 1)$ (Error Reduction Parameter):** Fraction of joint positional error corrected during the next fixed step $h$ (`fixed_step`, typically $0.01\text{ s}$ or $0.02\text{ s}$).
- **$\text{CFM} > 0$ (Constraint Force Mixing):** Softness/regularization added to the diagonal of the constraint Jacobian matrix $J M^{-1} J^T + \frac{\text{CFM}}{h} I$ (prevents singular matrix crashes!).

### Exact Bijective Conversion Between `(ERP, CFM)` and Spring-Damper `(k_p, k_d)`
For step size $h$ (`fixed_step`), spring constant $k_p$ ($\text{N/m}$), and damping constant $k_d$ ($\text{N}\cdot\text{s/m}$):
$$\text{ERP} = \frac{h \, k_p}{h \, k_p + k_d}, \qquad \text{CFM} = \frac{1}{h \, k_p + k_d}$$
Inverse mapping (recovering physical stiffness & damping from engine `ERP` and `CFM`):
$$k_p = \frac{\text{ERP}}{h \cdot \text{CFM}}, \qquad k_d = \frac{1 - \text{ERP}}{\text{CFM}}$$

> [!IMPORTANT]
> **Changing `fixed_step` Without Rescaling `ERP`/`CFM` Breaks Ragdolls:**
> If an OGSR port halves `fixed_step` from $h_1 = 0.02\text{ s}$ (50Hz) to $h_2 = 0.01\text{ s}$ (100Hz) without updating `ERP` and `CFM`, the effective spring stiffness $k_p = \frac{\text{ERP}}{h \cdot \text{CFM}}$ **doubles**, causing ragdolls and physics doors to violently explode! Always recompute $(\text{ERP}_2, \text{CFM}_2)$ from invariant $(k_p, k_d)$ using `game-math-solver ode`.

---

## 2. Frame-Rate Independent Exponential Decay & Critically Damped Springs

### The Classic Frame-Rate Bug in Legacy 32-bit Engines
Legacy code often writes:
```cpp
// BROKEN: frame-rate dependent Euler step (explodes if k * dt >= 1.0, changes speed at 60 FPS vs 240 FPS)
current += (target - current) * k * dt;
```
### Exact Analytical Solution (First-Order ODE $\frac{dx}{dt} = -\lambda (x - x_{\text{target}})$)
Integrating over an arbitrary frame delta $\Delta t$ yields the **exact, unconditionally stable** update for any framerate ($1\text{ FPS}$ to $1000\text{ FPS}$):
$$x(t + \Delta t) = x_{\text{target}} + \left(x(t) - x_{\text{target}}\right) e^{-\lambda \Delta t} = \text{std::lerp}\!\left(x(t),\; x_{\text{target}},\; 1.0f - \exp(-\lambda \, \Delta t)\right)$$
- **Half-Life Parameterization ($t_{1/2}$):** If a value should reach $50\%$ of its target in $t_{1/2}$ seconds:
  $$\lambda = \frac{\ln 2}{t_{1/2}} \approx \frac{0.693147}{t_{1/2}}, \qquad \alpha(\Delta t) = 1 - 2^{-\Delta t / t_{1/2}}$$

### Exact Critically Damped Second-Order Spring (Weapon Sway, Camera Recoil, UI)
For $\ddot{x} + 2\omega_0 \dot{x} + \omega_0^2 (x - x_{\text{target}}) = 0$ (critical damping $\zeta = 1$, zero overshoot):
Let $y_0 = x(t) - x_{\text{target}}$ and $e = e^{-\omega_0 \Delta t}$:
$$\begin{aligned}
x(t + \Delta t) &= x_{\text{target}} + \left(y_0 + (\dot{x}(t) + \omega_0 y_0)\Delta t\right) e^{-\omega_0 \Delta t} \\
\dot{x}(t + \Delta t) &= \left(\dot{x}(t) - (\dot{x}(t) + \omega_0 y_0)\omega_0 \Delta t\right) e^{-\omega_0 \Delta t}
\end{aligned}$$

---

## 3. External Projectile Ballistics Mathematics (S.T.A.L.K.E.R. LTX & C++)

In X-Ray/OGSR ballistics, a projectile with initial muzzle velocity $v_0$ (`bullet_speed`) experiences quadratic aerodynamic drag $k_{\text{air}}$ (`air_resistance_k`) and gravity $g$:
$$\frac{d\vec{v}}{dt} = -k_{\text{air}} \|\vec{v}\| \vec{v} + \vec{g}$$

### Horizontal Velocity & Time-of-Flight Analytical Integral (Flat Fire Approximation)
Along horizontal range $x \in [0, R]$ where $\|\vec{v}\| \approx v_x$:
$$\frac{dv_x}{dx} = \frac{dv_x / dt}{dx / dt} = -k_{\text{air}} v_x \implies v_x(x) = v_0 \, e^{-k_{\text{air}} x}$$
- **Exact Time-of-Flight $T(R)$ to Range $R$:**
  $$T(R) = \int_0^R \frac{dx}{v_x(x)} = \frac{e^{k_{\text{air}} R} - 1}{k_{\text{air}} v_0}$$
  *(In the limit $k_{\text{air}} \to 0$, $T(R) \to R / v_0$).*
- **Gravity Drop & Sight Zeroing Angle $\theta_0$ for Zero Range $R_0$:**
  $$\Delta y_{\text{drop}}(R) = \frac{1}{2} g \, T(R)^2, \qquad \theta_0 = \arctan\!\left(\frac{g \, T(R_0)^2}{2 R_0}\right)$$

---

## 4. Numerical Integrators: Symplectic Euler vs. RK4

- **Semi-Implicit (Symplectic) Euler (1st-order, preserves Hamiltonian energy bounds in real-time physics):**
  $$\vec{v}_{n+1} = \vec{v}_n + \vec{a}(\vec{x}_n, \vec{v}_n) \Delta t, \qquad \vec{x}_{n+1} = \vec{x}_n + \vec{v}_{n+1} \Delta t$$
  *(Note: Always update $\vec{x}_{n+1}$ using the **new** velocity $\vec{v}_{n+1}$; using $\vec{v}_n$ is Explicit Euler, which artificially injects energy and explodes orbital/spring systems!)*
- **Runge-Kutta 4th Order (RK4, $\mathcal{O}(\Delta t^4)$ global accuracy for ballistics & offline trajectories):**
  $$k_1 = f(t_n, y_n), \quad k_2 = f\!\left(t_n + \tfrac{h}{2}, y_n + \tfrac{h}{2}k_1\right), \quad k_3 = f\!\left(t_n + \tfrac{h}{2}, y_n + \tfrac{h}{2}k_2\right), \quad k_4 = f(t_n + h, y_n + h k_3)$$
  $$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

---

## 5. Local Zero-Quota CLI Verification (`game-math-solver`)
```bash
game-math-solver ode --erp 0.2 --cfm 1e-5 --step 0.02 --new-step 0.01
game-math-solver ballistics --v0 900 --drag 0.0012 --range 300
```

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`compiler-error-cascade-isolator`**: Intercepts C++ compiler error cascades (GCC, Clang, MSVC) during engine builds. Strips recursive template inst...
- **`game-dynamic-stress-orchestrator`**: Dynamic in-game stress testing and entity orchestration: collision-safe multi-entity wave spawning, cross-fact...
- **`game-physics-collision-pipeline`**: Real-time physics engine architecture, fixed timestep accumulator loops, continuous collision detection (CCD),...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

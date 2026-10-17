---
name: game-input-system-abstraction
description: Cross-platform game input abstraction layers, raw sub-pixel mouse polling, radial deadzone math, controller glyph auto-detection, and low-latency input event buffering (SDL3, Win32 RawInput, evdev, Steam Input). Use when porting game controls across PC, Steam Deck, Linux, and Android.
---

# Game Input System & Controller Abstraction Engineering

This skill defines the architecture for cross-platform, sub-millisecond input handling across mouse, keyboard, and gamepads, featuring mathematically correct radial deadzones and auto-sensing UI glyphs.

---

## 1. Radial Deadzone Math (Axial vs. Scaled Radial)

> [!WARNING]
> Standard axial deadzones (`if (abs(x) < deadzone) x = 0; if (abs(y) < deadzone) y = 0;`) create an unnatural "cross-shaped" deadzone that prevents smooth 360-degree diagonal aiming.

Always use **Scaled Radial Deadzones**:

```cpp
struct StickInput { float x; float y; };

StickInput ApplyScaledRadialDeadzone(float rawX, float rawY, float deadzoneMin, float deadzoneMax) {
    float magnitude = std::sqrt(rawX * rawX + rawY * rawY);
    if (magnitude < deadzoneMin) {
        return { 0.0f, 0.0f };
    }

    // Normalize direction
    float normX = rawX / magnitude;
    float normY = rawY / magnitude;

    // Rescale from [deadzoneMin, deadzoneMax] to [0.0, 1.0]
    float scaledMagnitude = std::min(1.0f, (magnitude - deadzoneMin) / (deadzoneMax - deadzoneMin));
    return { normX * scaledMagnitude, normY * scaledMagnitude };
}
```

---

## 2. Raw Sub-Pixel Mouse Accumulation

* Never query OS cursor position `GetCursorPos()` or rely on OS desktop pointer acceleration.
* In Windows: Use **Raw Input** (`WM_INPUT` with `RIDEV_INPUTSINK`).
* In Linux: Use `libinput` / `evdev` raw relative motion events (`EV_REL`).
* Accumulate sub-pixel delta floats:
  $$\Delta X = \text{rawDeltaX} \cdot \text{Sensitivity} \cdot \text{m\_pitch}, \quad \Delta Y = \text{rawDeltaY} \cdot \text{Sensitivity} \cdot \text{m\_yaw}$$

---

## 3. Dynamic Controller Glyph & Device Sensing

Maintain an active input state machine:
* When `WM_KEYDOWN` or mouse delta exceeds threshold: set `ActiveInputDevice = KeyboardMouse`, switch UI prompts to keyboard icons (`[E] Interact`).
* When gamepad button or stick magnitude $> 0.2$: inspect controller GUID/VendorID:
  * Sony (`0x054c`): Switch UI to PlayStation icons (`[✕] Interact`).
  * Microsoft / XInput (`0x045e`): Switch UI to Xbox icons (`[A] Interact`).
  * Nintendo (`0x057e`): Switch UI to Nintendo layout (`[B] Interact`).

## Related & Interoperating Skills
- **`game-physics-collision-pipeline`**: Real-time physics engine architecture, fixed timestep accumulator loops, continuous collision detection (CCD),...
- **`game-ai-agent-play`**: Autonomous game-playing agent engineering and reinforcement learning (Gymnasium, OpenCV computer vision, rewar...
- **`game-asset-pack-archive-engineering`**: Virtual file systems (VFS), game asset pack archive containers (PAK, XDB, AssetBundles), chunked zstd/zlib com...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

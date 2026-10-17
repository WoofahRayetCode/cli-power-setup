---
name: mobile-thermal-frame-pacing
description: Mobile thermal management, Android Swappy frame pacing, dynamic resolution scaling (DRS), and battery efficiency algorithms for Android and PC games.
---

# Mobile Thermal & Frame Pacing (`mobile-thermal-frame-pacing`)

Mobile devices lack active fan cooling. Unregulated game loops cause SoC temperatures to exceed 45°C within minutes, triggering aggressive hardware thermal throttling that drops frame rates from 60 FPS to 15 FPS.

This skill integrates Android Game SDK frame pacing (`Swappy`), hardware thermal monitoring, and Dynamic Resolution Scaling (DRS) to ensure smooth, stutter-free performance across mobile and PC platforms.

---

## 1. Frame Pacing with Android Swappy

Standard swapchain presentation (`vkQueuePresentKHR`) on mobile frequently encounters buffer swaps out of sync with the display refresh rate (e.g. 60Hz, 90Hz, 120Hz), causing judder and micro-stutters.

```cpp
#include <swappy/swappyVk.h>

// 1. Initialize Swappy during engine bring-up
SwappyVk_initAndStartTracer(jniEnv, jActivity);
SwappyVk_setQueueFamilyIndex(device, queue, queueFamilyIndex);
SwappyVk_setAutoSwapInterval(true);

// 2. Wrap swapchain presentation
SwappyVk_queuePresent(queue, &presentInfo);
```

---

## 2. Dynamic Resolution Scaling (DRS)

When frame time exceeds budget (e.g. > 15.0 ms for a 60 FPS target):
1. **Dynamic Viewport Scaling:** Dynamically adjust the rendering viewport without reallocating framebuffers:
   ```cpp
   float target_scale = clamp(target_frametime / actual_frametime, 0.65f, 1.0f);
   VkViewport viewport = {
       0.0f, 0.0f,
       screen_width * target_scale,
       screen_height * target_scale,
       0.0f, 1.0f
   };
   vkCmdSetViewport(commandBuffer, 0, 1, &viewport);
   ```
2. **Upscaling:** Upscale the scaled framebuffer to native resolution using hardware bilinear sampling or FSR 1.0 / mobile spatial upscalers.

---

## 3. Android Thermal Throttling Listener

```kotlin
val powerManager = getSystemService(Context.POWER_SERVICE) as PowerManager
powerManager.addThermalStatusListener { status ->
    when (status) {
        PowerManager.THERMAL_STATUS_MODERATE -> {
            // Lower particle count, disable bloom
            NativeBridge.setVisualQuality(QualityLevel.MEDIUM)
        }
        PowerManager.THERMAL_STATUS_SEVERE, PowerManager.THERMAL_STATUS_CRITICAL -> {
            // Drop target FPS to 30, enable aggressive DRS
            NativeBridge.setTargetFPS(30)
            NativeBridge.setVisualQuality(QualityLevel.LOW)
        }
    }
}
```

---
name: game-ai-agent-play
description: Autonomous game-playing agent engineering and reinforcement learning (Gymnasium, OpenCV computer vision, reward modeling, and low-latency input simulation via uinput/evdev/pyautogui).
---

# Autonomous Game AI & Agent Gameplay

This skill guides the design, training, and execution of autonomous game-playing agents using computer vision, reinforcement learning (RL), and low-latency input simulation.

---

## 🎯 When to Activate

* **Autonomous Gameplay & Botting:** Scripting vision-driven bots that play desktop or web games autonomously.
* **Reinforcement Learning Environments:** Creating custom Gymnasium/Gym environments from game windows.
* **Game State Recognition:** Using OpenCV (template matching, contour detection, color thresholding, OCR) to extract health, score, player coordinates, and enemy positions in real-time.
* **Input Simulation:** Emulating keyboard, mouse, and gamepad inputs via Linux kernel `/dev/uinput`, `evdev`, `ydotool`, or `pyautogui`.

---

## 🛠️ The 3-Stage Autonomous Game Loop

```text
[Capture Frame] -> [Extract Game State (Vision/OCR)] -> [Action Policy (RL / Heuristic)] -> [Inject Input (/dev/uinput)]
```

### 1. High-Speed Frame Capture (Pillow / OpenCV):
```python
from PIL import ImageGrab
import numpy as np
import cv2

# Grab 60fps window region
screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))
gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
```

### 2. State Detection via Template Matching:
```python
result = cv2.matchTemplate(gray, target_icon, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
if max_val > 0.85:
    target_x, target_y = max_loc
```

### 3. Low-Latency Linux Input Injection (`uinput` / `ydotool`):
Use kernel-level `/dev/uinput` or `evdev` to avoid game anti-cheat or window focus drops.

---

## 📊 Summary Output Format
* `game-ai-loop: [✓] Latency: 12ms/frame (83 FPS) | State: IN_COMBAT | Action: DODGE_RIGHT`
* `rl policy: [✓] Model: PPO (PyTorch CUDA) | Episode 142 | Reward: +850`

## Related & Interoperating Skills
- **`game-networking-state-sync`**: Multiplayer network architecture, client-side prediction, server reconciliation, entity interpolation, snapsho...
- **`game-companion-pet-ai`**: Custom companion & pet NPC architecture: state machine behaviors (follow, guard, objective guide), god mode st...
- **`game-qa-playtest-controller`**: Autonomous multi-axis game testing locomotion controller using Linux /dev/uinput and evdev. Injects dynamic ch...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

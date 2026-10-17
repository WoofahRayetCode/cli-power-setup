---
name: game-audio-engine-engineering
description: Low-latency game audio architecture, 3D spatial audio, HRTF binaural processing, mixing bus hierarchies, and sound bank asset pipelines (FMOD, Wwise, OpenAL Soft, MiniAudio, Oboe). Use when building audio engines, porting sound runtimes, or fixing audio clipping/desyncs.
---

# Game Audio Engine Engineering & Spatial Sound Architecture

This skill defines the technical standards for low-latency game audio engines, 3D spatial attenuation, binaural HRTF positioning, dynamic mixing bus topologies, and sound asset compression.

---

## 1. Low-Latency Audio Core & Callback Discipline

Audio hardware operates on rigid buffer deadlines (e.g. 128 to 512 samples per buffer at 48kHz, giving 2.6ms to 10.6ms time budgets).
* **Zero Allocation in Audio Callback:** `malloc`, `free`, and `new` are strictly forbidden inside the real-time audio thread (`onAudioReady` / `MixCallback`). All voice structures, DSP buffers, and sample handles must be pre-allocated.
* **Lock-Free Communication:** Never acquire a mutex or blocking lock in the audio callback. Communicate between game main thread and audio thread using a **lock-free single-producer single-consumer (SPSC) ring buffer** or atomic command queue.

---

## 2. 3D Spatial Audio & Distance Attenuation

### A. Inverse Distance Clamped Model (OpenAL / Physical Standard)
$$A(d) = \frac{d_{\text{min}}}{d_{\text{min}} + \text{Rolloff} \cdot (\max(d, d_{\text{min}}) - d_{\text{min}})}$$
* $d < d_{\text{min}}$: Gain is $1.0$ (no amplification).
* $d > d_{\text{max}}$: Gain is clamped or faded to $0.0$ to trigger virtual voice stealing.

### B. Equal-Power Panning Law (2D Stereo Fallback)
For a listener angle $\theta \in [-\frac{\pi}{2}, \frac{\pi}{2}]$:
$$G_{\text{left}} = \cos\left( \frac{\theta + \pi/2}{2} \right), \quad G_{\text{right}} = \sin\left( \frac{\theta + \pi/2}{2} \right)$$
Preserves total perceived acoustic power ($G_{\text{left}}^2 + G_{\text{right}}^2 = 1$).

### C. Head-Related Transfer Function (HRTF) & Occlusion
* **Binaural HRTF:** Convolve spatial audio with measured impulse responses for left and right ears, providing true up/down and front/back localization on headphones.
* **Low-Pass Filter (LPF) Occlusion:** When geometry raycasts hit an obstacle between sound source and listener, do not mute abruptly. Sweep a biquad low-pass filter down to 500Hz–1000Hz to simulate wall absorption.

---

## 3. Mixing Bus Hierarchies & Voice Stealing

```text
                       [ Master Bus ]
                             ▲
         ┌───────────────────┼───────────────────┐
         │                   │                   │
   [ Music Bus ]       [ SFX Bus ]         [ Voice / Dialogue ]
         │                   │                   │
         └─────────► [ Sidechain Ducking ] ◄─────┘
```

* **Dynamic Ducking:** Duck Music and SFX buses by -4dB to -6dB when dialogue voices are active.
* **Voice Stealing Priority:** Rank active voices by $\text{Priority} = \text{Volume} \times \text{CategoryWeight} / \text{Distance}$. Evict lowest priority voices when hardware voice limits (e.g. 64 or 128 voices) are saturated.

---

## 4. Headless & Silent Audio Verification (`silent_audio_tester.py`)

When running automated game QA or porting builds while physical speakers must remain silent (e.g., overnight or while resting):
```bash
python3 config/skills/game-audio-engine-engineering/scripts/silent_audio_tester.py verify --duration 2.0
```
* **Hardware Mute Guardian:** Verifies and enforces that physical master hardware sinks (`@DEFAULT_AUDIO_SINK@`) remain strictly `[MUTED]` to prevent acoustic noise in the room.
* **Software Monitor Capture:** Samples live audio waveform buffers directly from PipeWire / PulseAudio software sinks (`easyeffects_sink.monitor`), calculating RMS mean volume (dB), peak amplitude, and dynamic range.
* **Engine Log Auditing:** Parses game engine logs for OpenAL context status, sound cache lines, and missing sound asset errors.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`game-memory-allocator-engineering`**: Custom high-performance game engine memory allocators (Linear Arena, Stack, Pool, TLSF), SIMD memory alignment...
- **`game-networking-state-sync`**: Multiplayer network architecture, client-side prediction, server reconciliation, entity interpolation, snapsho...
- **`game-performance-overlay-telemetry`**: In-game HUD performance metrics and telemetry profiling (MangoHud, DXVK HUD, PresentMon). Configures FPS, fram...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

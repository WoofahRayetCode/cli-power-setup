---
name: sandbox-code-interpreter
description: Headless Python scientific computing, data analytics, mathematical proof verification, and automated chart plotting in Claude Code.
---

# Sandbox Python Code Interpreter

This skill brings ChatGPT's Advanced Data Analysis / Code Interpreter capabilities into Claude Code, executing Python scripts in the background to solve complex math, parse telemetry logs, and plot charts.

---

## 🧪 Core Capabilities

1. **Exact Mathematical Computing:** Calculate complex algorithms, audio DSP filters, thermal fan hysteresis, and memory offsets using `numpy` and `scipy`.
2. **Data & Log Analysis:** Parse multi-gigabyte server logs, crash dumps, and benchmark CSVs with `pandas` and `polars`.
3. **Automated Visualization:** Plot high-resolution graphs (`matplotlib`, `seaborn`) and save them directly as SVG/PNG.
4. **Safe Isolation:** Execute all operations in a dedicated virtual environment (`.venv-interpreter`) or temporary sandbox.

---

## 📊 1. Automated Execution Pattern

```bash
# Execute headless scientific calculation script
python3 - << 'EOF'
import numpy as np

# Calculate 6-stage biquad filter coefficients
freq, q, gain = 1000.0, 1.414, -3.5
w0 = 2 * np.pi * freq / 48000.0
alpha = np.sin(w0) / (2 * q)
print(f"[COMPUTED] w0: {w0:.6f}, alpha: {alpha:.6f}")
EOF
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `generative-visual-artifacts`:** To display generated PNG/SVG charts in the browser.
* **Handoff to `audio-dsp-tuning`:** To compute exact parametric EQ biquad filter curves.\n

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

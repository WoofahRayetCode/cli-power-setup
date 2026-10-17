---
name: generative-visual-artifacts
description: Generates self-contained interactive HTML/SVG widgets, KaTeX mathematical formulas, and live browser previews directly from Claude Code CLI.
---

# Generative Visual Artifacts & Live Browser Previews

This skill bridges the visual gap in terminal-based AI assistants by generating self-contained interactive web widgets, diagrams, and dashboards that open instantly in the user's browser.

---

## 🎨 Supported Visual Formats

1. **Interactive HTML5 / JS Dashboards:** Single-file bundles with Tailwind CSS (via CDN) and Chart.js for data visualization.
2. **Vector Graphics & UI Wireframes:** Clean, scalable inline SVG diagrams and responsive layout mockups.
3. **Scientific KaTeX Rendering:** Mathematical models, algorithm complexity formulas, and DSP transfer functions.
4. **Mermaid Architectural Graphs:** Sequence diagrams, state machines, and system dependency flowcharts.

---

## 🚀 1. Ephemeral Browser Preview Pattern

When presenting visual concepts to the user:

```bash
# 1. Write the self-contained HTML artifact
cat << 'EOF' > /tmp/preview_artifact.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <title>System Telemetry</title>
</head>
<body class="bg-slate-900 text-white p-6">
  <div class="max-w-4xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Live Fan Curve Telemetry</h1>
    <canvas id="telemetryChart"></canvas>
  </div>
  <script>
    const ctx = document.getElementById('telemetryChart');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['30C', '45C', '60C', '75C', '90C'],
        datasets: [{ label: 'Fan RPM %', data: [0, 20, 50, 80, 100], borderColor: '#38bdf8' }]
      }
    });
  </script>
</body>
</html>
EOF

# 2. Launch browser viewer
xdg-open /tmp/preview_artifact.html 2>/dev/null || open /tmp/preview_artifact.html 2>/dev/null
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `sandbox-code-interpreter`:** When charts require backend scientific Python computations before rendering.\n

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

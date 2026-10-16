---
name: interactive-data-visualization-web
description: Browser-based interactive data visualization for history, mythology, game lore, and complex architectures. Generates zero-build D3.js force-directed network graphs, Vis.js chronological timelines, and interactive entity stat charts.
---

# Interactive Data Visualization for Web & Research

This skill governs the generation of zero-build, browser-native interactive visualizations to present deep research—including historical chronologies, mythological pantheons, faction diplomacy networks, and technical architecture graphs.

---

## 📊 1. Visualization Formats & Engines

| Visualization Type | Engine | Best Used For | Features |
| :--- | :--- | :--- | :--- |
| **Chronological Timeline** | Vis.js Timeline | Historical epochs, battle timelines, mod release history | Dynamic zoom, pan, event clustering, era ranges |
| **Pantheon & Lineage Network** | D3.js Force Simulation | Divine family trees, faction alliances, character relations | Drag-and-drop physics, auto-centering, zoom/pan |
| **Comparative Radar Charts** | ECharts / Chart.js | Deific domains, character stats, entity attributes | Multi-axis overlay, tooltips, responsive SVG/Canvas |
| **Cartographic Maps** | Leaflet.js | Historical trade routes, territorial empires, game maps | Interactive tile layers, custom SVG markers, popups |

---

## 🚀 2. Zero-Build Standalone Generation CLI

Generate standalone, embeddable interactive HTML files directly from JSON datasets:

```bash
# 1. Generate an interactive chronological timeline
python3 config/skills/interactive-data-visualization-web/scripts/data_vis_generator.py \
  timeline data/crusades_events.json --title "Timeline of the Crusades" --out dist/timeline.html

# 2. Generate a D3.js force-directed pantheon relationship graph
python3 config/skills/interactive-data-visualization-web/scripts/data_vis_generator.py \
  network data/norse_pantheon.json --title "Aesir & Vanir Lineage" --out dist/pantheon.html
```

---

## 🔗 3. Workflow Integration

1. **Research & Extraction:** Gather primary sources and compile structured datasets via `humanities-lore-research`.
2. **Visual Generation:** Render interactive graphs or timelines via `interactive-data-visualization-web`.
3. **Aesthetic Framing:** Wrap inside a thematic archetype (e.g. `mythic-parchment` or `dark-glassmorphism`) via `creative-web-design-archetypes`.
4. **Publishing:** Deploy to GitHub Pages via `static-site-architecture`.

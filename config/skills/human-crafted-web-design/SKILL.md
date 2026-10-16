---
name: human-crafted-web-design
description: Anti-AI web design heuristics, Linear and Stripe-grade UI aesthetics, professional typography hierarchy, tactile dark-mode interfaces, and production Tailwind CSS.
---

# Human-Crafted Web Design & Anti-AI Aesthetics

This skill establishes visual design and front-end engineering standards to build websites that look like they were designed by senior product designers at **Linear, Stripe, Vercel, or Raycast**, actively eliminating generic "AI slop" clichés.

---

## 🚫 1. Banned AI Design Clichés

Never generate websites exhibiting these telltale AI tropes:
1. **Neon Gradients on Everything:** No blurry floating purple/cyan radial gradient spheres behind text.
2. **Buzzword Soup Headlines:** Ban phrases like *"Unleash the Power of Next-Gen AI Solutions to Supercharge Your Workflow"*.
3. **The Identical 3-Card Column:** Avoid 3 floating rounded cards with centered icons (Rocket, Shield, Zap) and 2 lines of generic text.
4. **Vague Illustrations:** No stock 3D clay figures, generic isometric illustrations, or floating disconnected geometric shapes.
5. **Lack of Interaction Polish:** Never deliver pages without active hover states, focus rings, and realistic component data.

---

## 💎 2. Human-Crafted Design Heuristics

### A. The Linear / Stripe Tactile Aesthetic
* **Subtle 1px Borders:** Use hairline borders (`border border-neutral-800` or `border border-white/10`) to separate content sections instead of heavy drop shadows.
* **Surface Layering:** Create depth with stacked neutral backgrounds:
  * Page background: `#09090b` (Zinc 950)
  * Card/Panel background: `#121215` (Zinc 900)
  * Elevated/Hover background: `#18181b` (Zinc 800)
* **Subtle Gradients:** Confine gradients to subtle 1px border highlights or delicate hero ambient fades (e.g. `linear-gradient(to bottom, rgba(255,255,255,0.05), transparent)`).

### B. Typographic Mastery
* **Font Stacks:** Modern, crisp geometric or humanistic sans-serifs (Geist, Inter, Satoshi) with strict typographic scales:
  * Hero Title: `text-4xl md:text-6xl font-semibold tracking-tight leading-tight`
  * Section Title: `text-2xl md:text-3xl font-medium tracking-tight text-white`
  * Body Copy: `text-sm md:text-base text-neutral-400 leading-relaxed font-normal`
  * Micro-labels / Kicker: `text-xs uppercase tracking-widest text-neutral-500 font-mono`

### C. Specific, Metric-Driven Copywriting
* Replace vague claims with concrete technical value:
  * *Bad:* "Fast, reliable data syncing for all your needs."
  * *Good:* "Syncs 50,000 records in 180ms over local SQLite WAL sockets."

---

## 🛠️ 3. Production Component Pattern

A clean, human-designed feature card in Tailwind CSS:

```html
<div class="group relative rounded-xl border border-neutral-800 bg-neutral-900/50 p-6 transition-all duration-200 hover:border-neutral-700 hover:bg-neutral-900">
  <div class="flex items-center justify-between mb-4">
    <span class="font-mono text-xs text-sky-400 bg-sky-950/50 border border-sky-800/50 px-2.5 py-0.5 rounded-full">v2.4 Kernel</span>
    <span class="text-xs text-neutral-500">Updated today</span>
  </div>
  <h3 class="text-base font-semibold text-white tracking-tight group-hover:text-sky-300 transition-colors">Zero-Allocation Pipeline</h3>
  <p class="mt-2 text-sm text-neutral-400 leading-relaxed">Streams incoming raw sensor telemetry using unmanaged memory buffers, reducing garbage collection pauses to 0ms.</p>
</div>
```

---

## 🔄 Interoperability & Handoffs

* **Pairing with `generative-visual-artifacts`:** Launches live browser previews using `xdg-open`.
* **Pairing with `threejs-webgl-engineering`:** Embeds high-performance 3D canvas viewports inside clean landing page layouts.

---
name: documentation-site-generator
description: Static documentation site generation using VitePress and MkDocs Material, automated API reference extraction, and GitHub Pages deployment.
---

# Developer Documentation Site Generator

This skill establishes automated creation of developer documentation sites using modern static generators like **VitePress** and **MkDocs Material**, with automated API extraction and 1-click GitHub Pages deployment.

---

## 📚 1. Zero-Config VitePress Site (`docs/`)

Set up a high-performance documentation portal in under 30 seconds:

```bash
# Initialize documentation folder
mkdir -p docs
cat << 'EOF' > docs/index.md
---
layout: home
hero:
  name: "Project Name"
  text: "High-performance systems engineering"
  tagline: "Automated, verified, and quota-optimized"
  actions:
    - theme: brand
      text: Get Started
      link: /guide/getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/WoofahRayetCode
---
EOF
```

Configure `docs/.vitepress/config.mjs`:
```javascript
export default {
  title: 'Project Docs',
  description: 'Comprehensive Technical Documentation',
  themeConfig: {
    nav: [{ text: 'Home', link: '/' }, { text: 'Guide', link: '/guide/' }],
    sidebar: [
      { text: 'Introduction', items: [{ text: 'Getting Started', link: '/guide/getting-started' }] }
    ]
  }
}
```

---

## 🚀 2. Automated GitHub Pages Deployment (`.github/workflows/docs.yml`)

```yaml
name: Deploy Documentation
on:
  push:
    branches: [main]
    paths: ['docs/**']
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npx vitepress build docs
      - uses: actions/upload-pages-artifact@v3
        with: { path: docs/.vitepress/dist }
      - uses: actions/deploy-pages@v4
```

---

## 🔄 Interoperability & Handoffs

* **Pairing with `project-memory-bank`:** Transcribes `.agents/memory/systemPatterns.md` into customer-facing documentation.
* **Handoff to `github-actions-cicd`:** Integrates docs deployment with continuous delivery.

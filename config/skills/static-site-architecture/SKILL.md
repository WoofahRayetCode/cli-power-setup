---
name: static-site-architecture
description: Modern Jamstack and static site generator (SSG) architecture. Covers Astro, VitePress, Starlight, Content Collections with Zod schemas, zero-JS baseline performance, and automated GitHub Pages CI/CD deployment pipelines.
---

# Static Site Architecture & Jamstack Engineering

This skill governs the architecture, scaffolding, and deployment of modern, high-performance static websites, digital lore encyclopedias, technical documentation portals, and research archives using modern Jamstack methodologies.

---

## 🏗️ 1. Static Site Generator (SSG) Ecosystem

| Engine | Best Use Case | JS Footprint | Markdown / MDX | Schema Validation |
| :--- | :--- | :--- | :--- | :--- |
| **Astro** | Digital lore encyclopedias, rich blogs, portfolios | 0kB JS by default (Islands) | First-class MDX | Zod Content Collections |
| **VitePress / Starlight** | Modding documentation, API guides, structured wikis | Lightweight Vue/Astro | Built-in search & sidebar | Config Frontmatter |
| **Eleventy (11ty) / Pure HTML** | Zero-dependency, ultra-fast archival builds | 0kB | Flexible template engines | Custom JSON Schemas |

---

## 📦 2. Astro Content Collections & Schema Discipline

When authoring historical archives, mythology entries, or mod documentation, enforce strict Zod schema validation (`src/content/config.ts`):

```typescript
import { defineCollection, z } from 'astro:content';

const loreCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    domain: z.enum(['Mythology', 'History', 'Folklore', 'GameLore']),
    culture_or_era: z.string(),
    archetype: z.string().optional(),
    tags: z.array(z.string()).default([]),
    date_recorded: z.date().optional(),
    primary_sources: z.array(z.string()).default([]),
    featured_image: z.string().optional(),
  }),
});

export const collections = {
  lore: loreCollection,
};
```

---

## 🚀 3. Automated CI/CD Deployment (GitHub Pages)

Deploy instantly without manual builds using GitHub Actions (`.github/workflows/deploy.yml`):
* Uses GitHub Pages official actions (`actions/configure-pages@v5`, `actions/upload-pages-artifact@v3`, `actions/deploy-pages@v4`).
* Zero server maintenance, automated HTTPS, and global edge CDN caching.

---

## 🛠️ 4. Scaffolding CLI

```bash
# Scaffold a pure static site with GitHub Pages CI/CD workflow
python3 config/skills/static-site-architecture/scripts/static_site_scaffolder.py \
  pure-static --title "Chronicles of Ancient Lore" --dest ./site_build
```

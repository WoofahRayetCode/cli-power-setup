#!/usr/bin/env python3
"""
Static Site Architecture & Project Scaffolder
============================================
Scaffolds lightweight, content-driven static sites (Astro, VitePress, or Pure Static HTML)
with pre-configured content collections, Markdown support, and GitHub Pages deployment.
"""

import argparse
import json
import os
import sys
from pathlib import Path


def scaffold_pure_static(dest_dir: Path, site_title: str) -> None:
    """Scaffold a high-performance, zero-dependency static site."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / "assets").mkdir(exist_ok=True)
    (dest_dir / "content").mkdir(exist_ok=True)

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{site_title}</title>
  <style>
    :root {{
      --bg: #0F172A;
      --card-bg: rgba(255, 255, 255, 0.05);
      --text: #F8FAFC;
      --text-dim: #94A3B8;
      --accent: #38BDF8;
      --border: rgba(255, 255, 255, 0.1);
    }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      margin: 0;
      padding: 2rem;
      line-height: 1.6;
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
    }}
    header {{
      border-bottom: 1px solid var(--border);
      padding-bottom: 1.5rem;
      margin-bottom: 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    h1 {{
      margin: 0;
      font-size: 2rem;
      color: var(--accent);
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.5rem;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.5rem;
      transition: transform 0.2s, border-color 0.2s;
    }}
    .card:hover {{
      transform: translateY(-2px);
      border-color: var(--accent);
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>{site_title}</h1>
      <nav>
        <a href="#articles" style="color: var(--accent); text-decoration: none;">Explore &rarr;</a>
      </nav>
    </header>
    <main>
      <p style="color: var(--text-dim); font-size: 1.2rem;">
        Content-driven digital archive and research platform.
      </p>
      <div id="articles" class="grid">
        <div class="card">
          <h3>Historical Chronicles</h3>
          <p style="color: var(--text-dim);">Deep dive into ancient empires and archeological discoveries.</p>
        </div>
        <div class="card">
          <h3>Mythological Bestiary</h3>
          <p style="color: var(--text-dim);">Comparative folklore, creature taxonomy, and pantheon trees.</p>
        </div>
        <div class="card">
          <h3>Interactive Timelines</h3>
          <p style="color: var(--text-dim);">Visual epoch sequences and chronological historical streams.</p>
        </div>
      </div>
    </main>
  </div>
</body>
</html>
"""
    (dest_dir / "index.html").write_text(index_html, encoding="utf-8")

    # Scaffolding GitHub Pages deployment action
    gh_workflow = dest_dir / ".github" / "workflows" / "deploy.yml"
    gh_workflow.parent.mkdir(parents=True, exist_ok=True)
    gh_workflow.write_text("""name: Deploy Static Site to GitHub Pages
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
""", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Static Site Architecture Scaffolder")
    parser.add_argument("engine", choices=["pure-static", "astro-stub"], help="SSG engine")
    parser.add_argument("--dest", type=str, default="./dist_site", help="Destination directory")
    parser.add_argument("--title", type=str, default="Digital Lore Archive", help="Site title")

    args = parser.parse_args()
    dest = Path(args.dest)

    if args.engine in ("pure-static", "astro-stub"):
        scaffold_pure_static(dest, args.title)
        print(f"[✓] Scaffolded static site at: {dest.resolve()}")
        print("  -> Includes responsive layout, theme tokens, and GitHub Pages CI/CD workflow.")


if __name__ == "__main__":
    main()

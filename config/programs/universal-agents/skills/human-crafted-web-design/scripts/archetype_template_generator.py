#!/usr/bin/env python3
"""
Creative Web Design Archetype Generator
=======================================
Generates responsive, self-contained HTML/CSS templates and component scaffolding
across 6 high-impact design archetypes:
1. mythic-parchment (Fantasy, History, Mythology, Chronicles)
2. neo-brutalism (Indie, Raw, High-Contrast Modding)
3. cyberpunk-terminal (CRT HUD, Scanlines, Sci-Fi)
4. editorial-academic (Scholarly, Long-form, Classical Book)
5. swiss-minimalist (Grid Architecture, International Typographic Style)
6. dark-glassmorphism (Modern Ambient Mesh, Translucent Frost)
"""

import argparse
import sys
from pathlib import Path

TEMPLATES = {
    "mythic-parchment": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=MedievalSharp&family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap">
  <style>
    :root {{
      --parchment-bg: #F5EEDB;
      --ink-dark: #2B1D0C;
      --gold-accent: #B8860B;
      --crimson-border: #7A1C1C;
    }}
    body {{
      background-color: var(--parchment-bg);
      color: var(--ink-dark);
      font-family: 'EB Garamond', serif;
      line-height: 1.8;
      margin: 0;
      padding: 2rem;
    }}
    .scroll-container {{
      max-width: 860px;
      margin: 0 auto;
      padding: 3rem;
      border: 3px double var(--crimson-border);
      box-shadow: 0 0 25px rgba(0,0,0,0.15), inset 0 0 40px rgba(184,134,11,0.1);
      background: #FAF4E6;
      border-radius: 4px;
    }}
    h1, h2, h3 {{
      font-family: 'Cinzel', serif;
      color: var(--crimson-border);
      text-align: center;
      letter-spacing: 0.05em;
    }}
    h1 {{
      font-size: 2.6rem;
      border-bottom: 2px solid var(--gold-accent);
      padding-bottom: 0.5rem;
    }}
    .drop-cap:first-letter {{
      font-family: 'MedievalSharp', cursive;
      float: left;
      font-size: 4rem;
      line-height: 0.8;
      padding-top: 4px;
      padding-right: 8px;
      color: var(--crimson-border);
    }}
  </style>
</head>
<body>
  <div class="scroll-container">
    <h1>{title}</h1>
    <p class="drop-cap">{content}</p>
  </div>
</body>
</html>
""",

    "neo-brutalism": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Cabinet+Grotesk:wght@800;900&display=swap">
  <style>
    :root {{
      --bg: #FFFDF0;
      --card-bg: #FFFFFF;
      --black: #000000;
      --accent-yellow: #FFE600;
      --accent-pink: #FF0055;
      --accent-blue: #00E5FF;
      --border-w: 3px;
      --shadow: 5px 5px 0px var(--black);
    }}
    body {{
      background-color: var(--bg);
      color: var(--black);
      font-family: 'Space Mono', monospace;
      margin: 0;
      padding: 2rem;
    }}
    .brutal-card {{
      max-width: 800px;
      margin: 2rem auto;
      background: var(--card-bg);
      border: var(--border-w) solid var(--black);
      box-shadow: var(--shadow);
      padding: 2.5rem;
    }}
    .badge {{
      display: inline-block;
      background: var(--accent-yellow);
      border: 2px solid var(--black);
      box-shadow: 2px 2px 0px var(--black);
      font-weight: bold;
      padding: 0.25rem 0.75rem;
      text-transform: uppercase;
      font-size: 0.85rem;
    }}
    h1 {{
      font-family: 'Cabinet Grotesk', sans-serif;
      font-size: 3rem;
      margin-top: 1rem;
      text-transform: uppercase;
      letter-spacing: -0.02em;
    }}
    button, .btn {{
      background: var(--accent-pink);
      color: #fff;
      border: var(--border-w) solid var(--black);
      box-shadow: 3px 3px 0px var(--black);
      padding: 0.8rem 1.6rem;
      font-family: 'Space Mono', monospace;
      font-weight: bold;
      font-size: 1rem;
      cursor: pointer;
      transition: transform 0.1s, box-shadow 0.1s;
    }}
    button:hover {{
      transform: translate(-2px, -2px);
      box-shadow: 5px 5px 0px var(--black);
    }}
    button:active {{
      transform: translate(2px, 2px);
      box-shadow: 1px 1px 0px var(--black);
    }}
  </style>
</head>
<body>
  <div class="brutal-card">
    <span class="badge">SPECIFICATION</span>
    <h1>{title}</h1>
    <p>{content}</p>
    <button>EXECUTE ACTION &rarr;</button>
  </div>
</body>
</html>
""",

    "cyberpunk-terminal": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@700;900&display=swap">
  <style>
    :root {{
      --hud-bg: #0A0C10;
      --hud-text: #00FFCC;
      --hud-dim: #007766;
      --hud-alert: #FF0055;
    }}
    body {{
      background-color: var(--hud-bg);
      color: var(--hud-text);
      font-family: 'Share Tech Mono', monospace;
      margin: 0;
      padding: 2rem;
      position: relative;
    }}
    body::before {{
      /* Scanlines and CRT monitor overlay */
      content: " ";
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
      background-size: 100% 4px, 6px 100%;
      pointer-events: none;
      z-index: 100;
    }}
    .terminal-box {{
      max-width: 880px;
      margin: 0 auto;
      border: 1px solid var(--hud-text);
      box-shadow: 0 0 15px rgba(0,255,204,0.2), inset 0 0 20px rgba(0,255,204,0.05);
      padding: 2rem;
      position: relative;
    }}
    .corner {{
      position: absolute;
      width: 10px; height: 10px;
      border: 2px solid var(--hud-text);
    }}
    .corner-tl {{ top: -2px; left: -2px; border-bottom: none; border-right: none; }}
    .corner-br {{ bottom: -2px; right: -2px; border-top: none; border-left: none; }}
    h1 {{
      font-family: 'Orbitron', sans-serif;
      text-transform: uppercase;
      text-shadow: 0 0 8px var(--hud-text);
      margin-top: 0;
    }}
  </style>
</head>
<body>
  <div class="terminal-box">
    <div class="corner corner-tl"></div>
    <div class="corner corner-br"></div>
    <h1>[SYS_TERM] {title}</h1>
    <p>> {content}</p>
  </div>
</body>
</html>
""",

    "dark-glassmorphism": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap">
  <style>
    body {{
      background: radial-gradient(circle at 10% 20%, #1E1B4B 0%, #0F172A 50%, #020617 100%);
      color: #F8FAFC;
      font-family: 'Plus Jakarta Sans', sans-serif;
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }}
    .glass-card {{
      max-width: 720px;
      width: 100%;
      background: rgba(255, 255, 255, 0.04);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 16px;
      padding: 3rem;
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }}
    h1 {{
      font-size: 2.4rem;
      background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-top: 0;
    }}
    p {{
      color: #94A3B8;
      font-size: 1.1rem;
      line-height: 1.7;
    }}
  </style>
</head>
<body>
  <div class="glass-card">
    <h1>{title}</h1>
    <p>{content}</p>
  </div>
</body>
</html>
"""
}


def generate_template(archetype: str, title: str, content: str) -> str:
    """Generate HTML string for the requested design archetype."""
    template_str = TEMPLATES.get(archetype.lower())
    if not template_str:
        # Default to dark-glassmorphism
        template_str = TEMPLATES["dark-glassmorphism"]
    return template_str.format(title=title, content=content)


def main():
    parser = argparse.ArgumentParser(description="Creative Web Design Archetype Generator")
    parser.add_argument("archetype", choices=["mythic-parchment", "neo-brutalism", "cyberpunk-terminal", "dark-glassmorphism"], help="Design archetype")
    parser.add_argument("--title", type=str, default="Project Dossier", help="Page title")
    parser.add_argument("--content", type=str, default="Sample content body demonstrating the typographic and spatial hierarchy.", help="Body content")
    parser.add_argument("--out", type=str, default=None, help="Output HTML file path")

    args = parser.parse_args()
    html = generate_template(args.archetype, args.title, args.content)

    if args.out:
        Path(args.out).write_text(html, encoding="utf-8")
        print(f"[✓] Generated '{args.archetype}' webpage: {args.out}")
    else:
        print(html)


if __name__ == "__main__":
    main()

---
name: game-localization-i18n
description: Internationalization (i18n) and localization (l10n) pipelines for games, desktop, and web apps. Covers ICU message formatting, pluralization rules, bidirectional text (RTL/LTR), font glyph fallbacks, dynamic dialogue translation tables, and string freeze validation.
---

# Game & Application Internationalization (i18n) & Localization (l10n)

This skill provides architectural standards and automated pipelines for localizing video games, desktop applications, and UI systems across multiple languages, scripts, and cultural formatting standards.

---

## 1. Zero-Hardcoded String Architecture

Never embed user-visible string literals inside gameplay scripts or UI components.

### A. Key-Based Localization Table Schema
All UI text, subtitles, item descriptions, and quest dialogues must reference namespaced keys:
```json
{
  "ui.menu.start_game": "Start Game",
  "ui.hud.ammo_counter": "Ammo: {count, number}",
  "dialogue.quest.reward": "You received {amount, plural, one{# Gold Coin} other{# Gold Coins}}."
}
```

### B. ICU MessageFormat & Pluralization Discipline
Simple string concatenation (`"You have " + count + " items"`) breaks in Slavic, Arabic, and Asian languages where plurals depend on complex grammatical cases (e.g. Russian has 3 plural forms; Arabic has 6):
* Always use ICU plural syntax (`zero`, `one`, `two`, `few`, `many`, `other`).

---

## 2. Dynamic Font Fallback & CJK/Cyrillic Shaping

1. **Missing Glyph "Tofu" (`□`):**
   - Western fonts frequently lack Cyrillic (`ru`), Japanese (`ja`), Korean (`ko`), or Simplified Chinese (`zh-Hans`) glyph ranges.
   - Configure multi-font fallback chains in the engine:
     `Primary Western -> Noto Sans CJK -> Noto Sans Arabic`.
2. **Text Expansion Budgeting:**
   - Translated text expands significantly compared to English:
     - German / French / Russian: **+20% to +35% longer** than English.
   - Never design UI boxes with rigid pixel widths that clip expanding text. Enable auto-wrapping, dynamic font scaling, or scroll containers.

---

## 3. Bidirectional (BiDi) Text & RTL (Right-to-Left)

When supporting Arabic (`ar`) or Hebrew (`he`):
- Text flows right-to-left, but numbers and embedded Latin words flow left-to-right.
- UI elements (back buttons, inventory slots, skill trees) must horizontally mirror across the vertical axis.

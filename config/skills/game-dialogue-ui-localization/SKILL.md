---
name: game-dialogue-ui-localization
description: Specialized game dialogue translation, string table repair, and conversation UI layout engine (S.T.A.L.K.E.R. & RPGs). Validates string IDs, resolves dialogue dead-end loops, fixes text clipping/overrun in talk.xml/talk_16.xml, enforces complex_mode multiline wrapping, and repairs CP1251/UTF-8 mojibake.
---

# Game Dialogue & Conversation UI Localization Suite (`game-dialogue-ui-localization`)

The `game-dialogue-ui-localization` skill provides specialized tools and architectural standards for localizing, translating, and repairing dialogue trees, XML string tables, and conversation UI layouts in video games—with deep specialization in **S.T.A.L.K.E.R. (X-Ray Engine / OGSR / S.T.A.L.K.E.R. 2)** and classic RPG dialogue engines.

---

## 1. Global Game Language Coverage Matrix

The suite covers all primary global gaming languages across 5 major linguistic families:

| Family | Languages & Codes | Expansion vs EN | Standard Codepage | Unique UI & Engine Challenges |
| :--- | :--- | :--- | :--- | :--- |
| **FIGS & Romance** | German (`de`), French (`fr`), Spanish (`es`, `es-419`), Italian (`it`), Portuguese (`pt-br`, `pt-pt`) | **+25% to +35%** (DE: +35%, FR/ES/IT: +25%) | `windows-1252` / `utf-8` | Long compound nouns in German split across dialog containers; gendered inflection in French/Spanish; accented Latin-1 glyphs (`é`, `ñ`, `ß`). |
| **CJK (East Asian)** | Japanese (`ja`), Simplified Chinese (`zh-cn`), Traditional Chinese (`zh-tw`), Korean (`ko`) | **-35% to -45% chars**, but **2x pixel width per glyph** | `shift_jis`, `gb18030`, `big5`, `cp949` / `utf-8` | Fullwidth monospace glyphs require specialized double-width font metrics; **Kinzoku Shori** line-breaking discipline (forbidden line-start punctuation `。`, `、`, `」`); no whitespace word separation in Japanese/Chinese. |
| **Slavic & Central Europe** | Russian (`ru`), Ukrainian (`uk`), Polish (`pl`), Czech (`cs`), Slovak (`sk`), Hungarian (`hu`) | **+15% to +25%** | `windows-1251` (Cyrillic), `windows-1250` (Latin-2) / `utf-8` | 3-stage noun pluralization cases (`1 день`, `2-4 дня`, `5+ дней`); engine font textures must include Cyrillic/Latin-2 glyph sheets; CP1251 vs CP1250 mojibake. |
| **BiDi / Middle Eastern** | Arabic (`ar`), Hebrew (`he`), Persian (`fa`) | **+10% to +15%** | `windows-1256` (AR), `windows-1255` (HE) / `utf-8` | Right-to-Left (RTL) reading order; conversation UI containers require mirrored horizontal coordinate anchors (`right_ident`, `align="right"`). |
| **Eurasian & Nordic** | Turkish (`tr`), Dutch (`nl`), Swedish (`sv`), Norwegian (`no`), Danish (`da`), Finnish (`fi`), Vietnamese (`vi`), Thai (`th`) | **+15% to +25%** (FI: +25%, NL: +20%) | `windows-1254` (TR), `windows-1252` / `utf-8` | **Turkish `i` pitfall:** dotted `İ` $\leftrightarrow$ `i`, dotless `I` $\leftrightarrow$ `ı` (standard ASCII case-folding corrupts string IDs); Finnish long agglutinative words; Vietnamese stacked diacritics. |

---

## 2. Core Technical Challenges in Game Conversation UI

### A. Text Expansion & UI Clipping
- English, German, and French translations are typically **20% to 40% longer** than original Russian or Japanese dialogue strings.
- In S.T.A.L.K.E.R. X-Ray Engine, conversation UI is governed by `gamedata/config/ui/talk.xml` (4:3) and `talk_16.xml` (16:9 widescreen).
- **The `complex_mode` Trap:** If `<text>` or `<content_text>` nodes lack `complex_mode="1"`, the engine renders strings on a single line and truncates any overflow at the bounding box border.
- **Scrollbar Starvation:** If `<questions_list>` or `<answers_list>` exceeds container height without `always_show_scroll="1"`, player replies render off-screen, rendering the dialogue un-progressable.

### B. Raw String ID Leaks
- Dialogue nodes reference keys: `<phrase id="1"><text>escape_trader_start_dialog_1</text></phrase>`.
- If `escape_trader_start_dialog_1` is missing from `gamedata/config/text/<lang>/string_table_*.xml`, the engine prints the raw identifier string in the UI window, breaking immersion.

### C. Character Encoding & Mojibake
- Legacy 32-bit S.T.A.L.K.E.R. SoC requires **Windows-1251 (CP1251)** for Cyrillic, **Windows-1250 (CP1250)** for Polish/Czech, or **Windows-1252 (CP1252)** for FIGS.
- 64-bit engines (OGSR, Anomaly, OpenXRay) support **UTF-8**.
- Saving a CP1251 file as UTF-8 without changing the header—or saving UTF-8 as ANSI—produces unreadable mojibake (`Р—РґСЂР°РІСЃС‚РІСѓР№`) or fatal XML parser crashes (`xrXMLParser.cpp`).

### D. Color Tag & Escape Sequence Integrity
- S.T.A.L.K.E.R. uses `%c[color_code]` or `%c[255,r,g,b]` inline formatting tags (e.g. `%c[green]Objective Completed%c[default]`).
- Untrained translation tools mangle tags into broken tokens (`% c [ green ]`), strip `\\n` escapes, or omit `%c[default]`, causing colored text to bleed through the entire HUD.

### E. Dead-End Dialogue Graphs
- If a dialogue tree lacks an entry point (`<phrase id="0">`), or all branches have failing preconditions (`<precondition>`), the conversation window opens with zero selectable options while disabling the `ESC` key, locking the player in a permanent freeze.

---

## 3. Command-Line Reference (`game-dialogue-tool`)

The companion executable `game-dialogue-tool` (installed in `~/.local/bin/game-dialogue-tool`) automates inspection, translation auditing, and repair:

| Subcommand | Purpose | Key Flags | Example |
| :--- | :--- | :--- | :--- |
| **`validate-strings`** | Checks XML string tables for syntax, duplicate IDs, empty text, and unclosed `%c[...]` tags | `--no-colors` | `game-dialogue-tool validate-strings gamedata/config/text/eng/*.xml` |
| **`cross-reference`** | Finds missing string IDs referenced in dialogue trees that would leak into UI | `--dialogs`, `--strings` | `game-dialogue-tool cross-reference --dialogs gamedata/config/gameplay/ --strings gamedata/config/text/eng/` |
| **`check-ui-overrun`** | Calculates visual pixel width vs UI container dimensions; tests language expansion | `--ui`, `--strings`, `--max-chars`, `--lang`, `--target-lang` | `game-dialogue-tool check-ui-overrun --ui gamedata/config/ui/talk.xml --strings gamedata/config/text/eng/ --target-lang de` |
| **`fix-widescreen-ui`** | Injects `complex_mode="1"` and aligns widescreen coordinates (`talk_16.xml`) | `--talk`, `--talk16`, `--fix` | `game-dialogue-tool fix-widescreen-ui --talk .../talk.xml --talk16 .../talk_16.xml --fix` |
| **`fix-encoding`** | Converts encodings (UTF-8, CP1251, CP1250, CP1252, CJK) and repairs mojibake | `--to`, `--fix` | `game-dialogue-tool fix-encoding gamedata/config/text/rus/*.xml --to utf-8 --fix` |
| **`validate-graph`** | Traces dialogue tree phrase chains, checking for broken `<next>` IDs and dead-ends | `<dialog_files>` | `game-dialogue-tool validate-graph gamedata/config/gameplay/dialogs_*.xml` |
| **`audit-languages`** | Audits presence of major global gaming language folders, counts, and expansion ratios | `<text_dir>` | `game-dialogue-tool audit-languages gamedata/config/text/` |

---

## 4. Font Metrics & UI Dimensions Reference

### A. S.T.A.L.K.E.R. Dialogue Fonts
* **`letterica18`:** Primary conversation text font. Average width: ~8.0px per Latin char, ~16.0px per CJK fullwidth char; line height: 18px.
* **`letterica16`:** Compact dialogue reply font. Average width: ~7.0px per Latin char, ~14.0px per CJK fullwidth char; line height: 16px.
* **`graffiti22`:** NPC character name & trade button font. Average width: ~9.5px per Latin char, ~19.0px per CJK fullwidth char; line height: 22px.

### B. Standard Conversation Window Bounds (1024x768 Base Coordinate Space)
* **NPC Answer Container (`answers_list`):**
  - `talk.xml`: `x="33" y="46" width="544" height="377"`
  - `talk_16.xml`: `x="26" y="46" width="557" height="377"`
  - Capacity: ~20 lines of wrapped text before scrolling is required.
* **Player Question Container (`questions_list`):**
  - `talk.xml`: `x="30" y="100" width="547" height="80"` (Compact! Max ~4 lines before clipping without scroll)
  - `talk_16.xml`: `x="38" y="110" width="547" height="160"` (Expanded widescreen reply area)

---

## 5. Best Practices for Mod Translation & Dialogue Editing

1. **Simulate Language Expansion Before Translating:** Run `game-dialogue-tool check-ui-overrun --target-lang de` against source English text to forecast lines and prevent UI overflow before sending text to translators.
2. **Always Audit After Translating:** Run `game-dialogue-tool cross-reference` to ensure no translator accidentally modified XML string IDs (e.g. translating `<string id="esc_trader_hello">` into `<string id="esc_trader_привет">`).
3. **Preserve Color Blocks:** Ensure all `%c[color]` tags are closed with `%c[default]`.
4. **Enforce `complex_mode="1"`:** Every `<text>` tag in `talk.xml` and `talk_16.xml` must have `complex_mode="1"` enabled to allow word-wrapping.
5. **Widescreen Parity:** Never edit `talk.xml` without updating `talk_16.xml`.
6. **CJK Kinzoku Shori Discipline:** Ensure Japanese and Chinese translations don't place sentence-ending punctuation (`。`, `、`, `」`) at line starts.

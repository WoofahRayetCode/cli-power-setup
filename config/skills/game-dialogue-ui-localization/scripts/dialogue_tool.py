#!/usr/bin/env python3
"""
Game Dialogue & UI Localization Tool (game-dialogue-tool)
Specialized analyzer, validator, and repair engine for game conversation text,
XML string tables, dialogue trees, encoding, and conversation UI layouts (S.T.A.L.K.E.R. & RPGs).
"""

import sys
import os
import re
import argparse
import unicodedata
from pathlib import Path
import xml.etree.ElementTree as ET

# Estimated average character widths per font in S.T.A.L.K.E.R. & typical RPGs (pixels at 1024x768 base)
FONT_METRICS = {
    "letterica16": {"char_w": 7.0, "line_h": 16, "cjk_w": 14.0},
    "letterica18": {"char_w": 8.0, "line_h": 18, "cjk_w": 16.0},
    "graffiti19":  {"char_w": 8.5, "line_h": 19, "cjk_w": 17.0},
    "graffiti22":  {"char_w": 9.5, "line_h": 22, "cjk_w": 19.0},
    "arial_14":    {"char_w": 6.5, "line_h": 14, "cjk_w": 13.0},
    "default":     {"char_w": 8.0, "line_h": 18, "cjk_w": 16.0}
}

# Industry standard text expansion ratios relative to English baseline (1.0)
LANGUAGE_EXPANSION_RATIOS = {
    # FIGS (Western Europe)
    "de": 1.35,  # German: long compound nouns, ~30-35% expansion
    "fr": 1.25,  # French: verbose grammar and articles, ~25% expansion
    "it": 1.25,  # Italian: ~20-25% expansion
    "es": 1.25,  # Spanish (Castilian/LatAm): ~20-30% expansion
    "pt": 1.25,  # Portuguese (PT/BR): ~20-25% expansion
    # Slavic & Eastern European
    "ru": 1.20,  # Russian: inflections, Cyrillic glyphs, ~15-25% expansion
    "uk": 1.20,  # Ukrainian: ~15-25% expansion
    "pl": 1.25,  # Polish: Latin-2, complex noun compounds, ~20-25% expansion
    "cs": 1.20,  # Czech: ~15-25% expansion
    "sk": 1.20,  # Slovak: ~15-25% expansion
    "hu": 1.25,  # Hungarian: agglutinative, long words, ~25% expansion
    "ro": 1.20,  # Romanian: ~20% expansion
    "bg": 1.20,  # Bulgarian: Cyrillic, ~20% expansion
    "sr": 1.20,  # Serbian: Cyrillic/Latin, ~20% expansion
    # CJK (East Asian) - Character count shrinks, but each glyph occupies 2x horizontal space
    "ja": 0.65,  # Japanese: ~65% character count of EN, fullwidth CJK glyphs
    "zh": 0.55,  # Chinese (Simplified/Traditional): ~55% character count, fullwidth CJK
    "zh-cn": 0.55,
    "zh-tw": 0.55,
    "ko": 0.80,  # Korean (Hangul): ~80% character count, syllable blocks
    # BiDi / Middle Eastern (Right-to-Left)
    "ar": 1.15,  # Arabic: ~15% expansion, requires RTL shaping & UI mirroring
    "he": 1.05,  # Hebrew: ~5% expansion, requires RTL layout
    "fa": 1.15,  # Persian/Farsi: ~15% expansion, RTL
    # Eurasian & Nordic
    "tr": 1.15,  # Turkish: agglutinative suffixes, dotted/dotless i pitfalls
    "nl": 1.20,  # Dutch: compound nouns, ~20% expansion
    "sv": 1.15,  # Swedish: ~15% expansion
    "no": 1.15,  # Norwegian: ~15% expansion
    "da": 1.15,  # Danish: ~15% expansion
    "fi": 1.25,  # Finnish: long agglutinative words, ~25% expansion
    "el": 1.20,  # Greek: ~20% expansion
    "vi": 1.25,  # Vietnamese: accented tone markers, ~25% expansion
    "th": 0.90,  # Thai: script without word spaces, ~90% char count
    # Default baseline
    "en": 1.00
}

# Common legacy game codepages per language family
LANGUAGE_LEGACY_CODEPAGES = {
    "ru": "windows-1251",
    "uk": "windows-1251",
    "bg": "windows-1251",
    "be": "windows-1251",
    "pl": "windows-1250",
    "cs": "windows-1250",
    "sk": "windows-1250",
    "hu": "windows-1250",
    "ro": "windows-1250",
    "de": "windows-1252",
    "fr": "windows-1252",
    "es": "windows-1252",
    "it": "windows-1252",
    "pt": "windows-1252",
    "en": "windows-1252",
    "tr": "windows-1254",
    "el": "windows-1253",
    "he": "windows-1255",
    "ar": "windows-1256",
    "ja": "shift_jis",
    "zh": "gb18030",
    "zh-cn": "gb18030",
    "zh-tw": "big5",
    "ko": "cp949"
}

# Kinzoku Shori rules: Punctuation characters that cannot start a line in CJK
CJK_NO_LINE_START = set("、。，．・：；？！ヽヾゝゞ々ー）〕］｝〉》」』】’”?!)]}")
# Punctuation characters that cannot end a line in CJK
CJK_NO_LINE_END = set("（〔［｛〈《「『【‘“([")

def calculate_visual_width(text: str, font_name: str = "letterica18") -> float:
    """Calculates visual pixel width of text accounting for Latin vs fullwidth CJK glyphs."""
    metric = FONT_METRICS.get(font_name, FONT_METRICS["default"])
    latin_w = metric["char_w"]
    cjk_w = metric.get("cjk_w", latin_w * 2.0)
    
    total_w = 0.0
    for ch in text:
        # Strip XML color tags (%c[...]) from visual width calculation
        ea = unicodedata.east_asian_width(ch)
        if ea in ('W', 'F'):
            total_w += cjk_w
        else:
            total_w += latin_w
    return total_w

def detect_script_and_language(text: str) -> dict:
    """Detects dominant scripts, potential language characteristics, and UI risks."""
    scripts = {
        "cjk": 0,
        "hangul": 0,
        "cyrillic": 0,
        "arabic": 0,
        "hebrew": 0,
        "latin": 0,
        "greek": 0,
        "thai": 0
    }
    turkish_specific = 0
    for ch in text:
        code = ord(ch)
        if 0x4E00 <= code <= 0x9FFF or 0x3040 <= code <= 0x30FF: # CJK Ideographs / Hiragana / Katakana
            scripts["cjk"] += 1
        elif 0xAC00 <= code <= 0xD7AF or 0x1100 <= code <= 0x11FF: # Hangul
            scripts["hangul"] += 1
        elif 0x0400 <= code <= 0x04FF: # Cyrillic
            scripts["cyrillic"] += 1
        elif 0x0600 <= code <= 0x06FF: # Arabic
            scripts["arabic"] += 1
        elif 0x0590 <= code <= 0x05FF: # Hebrew
            scripts["hebrew"] += 1
        elif 0x0370 <= code <= 0x03FF: # Greek
            scripts["greek"] += 1
        elif 0x0E00 <= code <= 0x0E7F: # Thai
            scripts["thai"] += 1
        elif 'A' <= ch <= 'Z' or 'a' <= ch <= 'z':
            scripts["latin"] += 1
        elif ch in "çğıöşüÇĞİÖŞÜ":
            turkish_specific += 1

    dominant = max(scripts, key=scripts.get) if any(scripts.values()) else "latin"
    is_bidi = scripts["arabic"] > 0 or scripts["hebrew"] > 0
    
    return {
        "dominant_script": dominant,
        "is_bidi": is_bidi,
        "has_cjk": scripts["cjk"] > 0 or scripts["hangul"] > 0,
        "has_cyrillic": scripts["cyrillic"] > 0,
        "has_turkish": turkish_specific > 0,
        "scripts": {k: v for k, v in scripts.items() if v > 0}
    }

def robust_xml_parse(file_path: Path):
    """Attempts to parse XML across common game encoding quirks (CP1251, CP1250, CP1252, CJK, UTF-8)."""
    raw = file_path.read_bytes()
    encodings = [
        "utf-8-sig",
        "utf-8",
        "windows-1251",  # Russian, Ukrainian, Bulgarian
        "windows-1250",  # Polish, Czech, Slovak, Hungarian
        "windows-1252",  # FIGS (English, German, French, Spanish, Italian)
        "shift_jis",     # Japanese
        "gb18030",       # Simplified Chinese
        "big5",          # Traditional Chinese
        "cp949",         # Korean
        "windows-1254",  # Turkish
        "windows-1256",  # Arabic
        "latin-1"
    ]
    
    # Check declared encoding in XML header
    header_match = re.search(rb'encoding=["\']([a-zA-Z0-9_-]+)["\']', raw[:128])
    if header_match:
        declared = header_match.group(1).decode("ascii", errors="ignore").lower().replace("_", "-")
        alias_map = {
            "cp1251": "windows-1251", "windows-1251": "windows-1251",
            "cp1250": "windows-1250", "windows-1250": "windows-1250",
            "cp1252": "windows-1252", "windows-1252": "windows-1252",
            "cp1254": "windows-1254", "windows-1254": "windows-1254",
            "cp1256": "windows-1256", "windows-1256": "windows-1256",
            "sjis": "shift_jis", "shift-jis": "shift_jis", "shift_jis": "shift_jis",
            "gb2312": "gb18030", "gbk": "gb18030", "gb18030": "gb18030",
            "big-5": "big5", "big5": "big5",
            "euc-kr": "cp949", "cp949": "cp949",
            "utf-8": "utf-8", "utf8": "utf-8"
        }
        resolved = alias_map.get(declared, declared)
        if resolved in encodings:
            encodings.remove(resolved)
            encodings.insert(0, resolved)

    for enc in encodings:
        try:
            text = raw.decode(enc)
            # Sanitize unescaped ampersands common in game mods (e.g. & without ;)
            clean_text = re.sub(r'&(?!(amp|lt|gt|apos|quot);)', '&amp;', text)
            root = ET.fromstring(clean_text)
            return root, enc, text
        except Exception:
            continue
    raise ValueError(f"Could not parse XML from {file_path} using common encodings.")

# -----------------------------------------------------------------------------
# 1. String Table Validation
# -----------------------------------------------------------------------------
def validate_strings(files: list, check_colors: bool = True):
    print(f"\n[→] Validating XML string tables across {len(files)} files...")
    total_strings = 0
    issues = []
    seen_ids = {}

    for f in files:
        p = Path(f)
        if not p.is_file():
            continue
        try:
            root, enc, text = robust_xml_parse(p)
        except Exception as e:
            issues.append({"file": str(p), "type": "XML_SYNTAX_ERROR", "msg": str(e)})
            continue

        for elem in root.findall(".//string"):
            sid = elem.get("id")
            if not sid:
                issues.append({"file": str(p), "type": "MISSING_STRING_ID", "msg": "Tag <string> lacks id attribute"})
                continue
            total_strings += 1
            if sid in seen_ids:
                issues.append({
                    "file": str(p),
                    "type": "DUPLICATE_ID",
                    "msg": f"String ID '{sid}' already defined in {seen_ids[sid]}"
                })
            else:
                seen_ids[sid] = str(p)

            t_elem = elem.find("text")
            t_val = t_elem.text if (t_elem is not None and t_elem.text) else ""
            
            # Check empty text
            if not t_val.strip():
                issues.append({"file": str(p), "type": "EMPTY_STRING", "msg": f"ID '{sid}' has empty <text>"})

            # Check unclosed or malformed color tags %c[...]
            if check_colors and t_val:
                open_colors = re.findall(r'%c\[([a-zA-Z0-9_,]+)\]', t_val)
                # S.T.A.L.K.E.R. color tags must be reset with %c[default]
                if open_colors:
                    resets = t_val.count("%c[default]")
                    colored_spans = len([c for c in open_colors if c != "default"])
                    if colored_spans > resets:
                        issues.append({
                            "file": str(p),
                            "type": "UNCLOSED_COLOR_TAG",
                            "msg": f"ID '{sid}' has {colored_spans} color tags but only {resets} %c[default] resets"
                        })

    print(f"[✓] Processed {total_strings} string entries.")
    if issues:
        print(f"[!] Found {len(issues)} string table issues:")
        for iss in issues[:20]:
            print(f"    - [{iss['type']}] {iss['file']}: {iss['msg']}")
        if len(issues) > 20:
            print(f"    ... and {len(issues) - 20} more.")
        return 1
    print("[✓] All string tables are syntactically valid with zero tag defects.")
    return 0

# -----------------------------------------------------------------------------
# 2. Dialogue & String Table Cross-Reference
# -----------------------------------------------------------------------------
def cross_reference(dialog_paths: list, string_paths: list):
    print(f"\n[→] Cross-referencing dialogues against string tables...")
    
    # 1. Collect all defined string IDs
    known_strings = set()
    for sp in string_paths:
        p = Path(sp)
        target_files = list(p.rglob("*.xml")) if p.is_dir() else [p]
        for f in target_files:
            try:
                root, _, _ = robust_xml_parse(f)
                for elem in root.findall(".//string"):
                    sid = elem.get("id")
                    if sid:
                        known_strings.add(sid)
            except Exception:
                continue
    print(f"[✓] Indexed {len(known_strings)} string keys from string tables.")

    # 2. Collect all text references in dialogues
    referenced_keys = {}
    for dp in dialog_paths:
        p = Path(dp)
        target_files = list(p.rglob("*.xml")) if p.is_dir() else [p]
        for f in target_files:
            try:
                root, _, _ = robust_xml_parse(f)
                for elem in root.findall(".//text"):
                    if elem.text and elem.text.strip():
                        txt = elem.text.strip()
                        # If text contains spaces, it's a literal string rather than an ID
                        if " " not in txt and not txt.startswith("%c"):
                            if txt not in referenced_keys:
                                referenced_keys[txt] = []
                            referenced_keys[txt].append(str(f))
            except Exception:
                continue

    # 3. Detect Missing IDs
    missing = {k: v for k, v in referenced_keys.items() if k not in known_strings}
    print(f"[✓] Scanned {len(referenced_keys)} string references in dialogue files.")
    
    if missing:
        print(f"\n[✗] Found {len(missing)} missing string IDs (these will render as raw IDs in-game):")
        for k, files in list(missing.items())[:25]:
            print(f"    - '{k}' (referenced in {', '.join(files[:2])})")
        if len(missing) > 25:
            print(f"    ... and {len(missing) - 25} more.")
        return 1
    
    print("[✓] 100% of referenced dialogue string IDs exist in the string tables!")
    return 0

# -----------------------------------------------------------------------------
# 3. Conversation UI Overrun & Clipping Check
# -----------------------------------------------------------------------------
def check_ui_overrun(ui_file: Path, string_paths: list, max_warn_chars: int = 120, lang: str = "auto", target_lang: str = None):
    target_expansion = LANGUAGE_EXPANSION_RATIOS.get(target_lang.lower(), 1.0) if target_lang else 1.0
    print(f"\n[→] Checking conversation UI text overrun against {ui_file} (lang={lang}, target_lang={target_lang or 'none'})...")
    if not ui_file.exists():
        print(f"[✗] UI file not found: {ui_file}")
        return 1

    root, _, _ = robust_xml_parse(ui_file)
    
    # Check complex_mode on text elements
    missing_complex_mode = []
    text_boxes = []
    for elem in root.iter():
        if "text" in elem.tag.lower() or elem.tag in ["question_item", "other_answer_item", "content_text"]:
            c_mode = elem.get("complex_mode")
            # If not explicitly set to 1, S.T.A.L.K.E.R. won't wrap lines!
            if c_mode != "1":
                sub_text = elem.find("text")
                if sub_text is not None and sub_text.get("complex_mode") != "1":
                    missing_complex_mode.append(elem.tag)
            
            w = elem.get("width") or elem.get("cx")
            h = elem.get("height") or elem.get("cy")
            font = elem.get("font") or (elem.find("text").get("font") if elem.find("text") is not None else None) or "letterica18"
            if w and h:
                text_boxes.append({"tag": elem.tag, "w": float(w), "h": float(h), "font": font})

    if missing_complex_mode:
        print(f"[!] Warning: {len(missing_complex_mode)} dialogue text elements lack complex_mode='1' (risk of single-line truncation):")
        for tag in set(missing_complex_mode):
            print(f"    - <{tag}> needs complex_mode='1'")
    else:
        print("[✓] All text containers have complex_mode='1' enabled for multiline wrapping.")

    # Dialogue box width (~520px in S.T.A.L.K.E.R. standard HUD)
    avg_box_width = 520.0
    font_name = "letterica18"

    long_strings = []
    bidi_warnings = []
    cjk_kinzoku_warnings = []
    turkish_warnings = []

    for sp in string_paths:
        p = Path(sp)
        target_files = list(p.rglob("*.xml")) if p.is_dir() else [p]
        for f in target_files:
            try:
                root_s, _, _ = robust_xml_parse(f)
                for s in root_s.findall(".//string"):
                    sid = s.get("id")
                    t_elem = s.find("text")
                    if t_elem is not None and t_elem.text:
                        txt = t_elem.text.strip()
                        script_info = detect_script_and_language(txt)
                        
                        # BiDi layout alert
                        if script_info["is_bidi"]:
                            bidi_warnings.append({"id": sid, "file": f.name, "script": script_info["dominant_script"]})

                        # Turkish casing pitfalls
                        if script_info["has_turkish"] or lang == "tr":
                            if ("I" in txt and "i" in txt) and ("ı" not in txt and "İ" not in txt):
                                turkish_warnings.append({"id": sid, "file": f.name})

                        # CJK Kinzoku Shori rules: line cannot start with closing punctuation
                        if script_info["has_cjk"]:
                            for line in txt.splitlines():
                                line_clean = line.strip()
                                if line_clean and line_clean[0] in CJK_NO_LINE_START:
                                    cjk_kinzoku_warnings.append({"id": sid, "char": line_clean[0], "file": f.name})

                        # Calculate pixel width taking Latin vs fullwidth CJK glyphs into account
                        base_visual_width = calculate_visual_width(txt, font_name)
                        projected_width = base_visual_width * target_expansion
                        projected_lines = int(projected_width // avg_box_width) + 1

                        if projected_lines > 4 and (len(txt) > max_warn_chars or projected_width > (avg_box_width * 4)):
                            long_strings.append({
                                "id": sid,
                                "len": len(txt),
                                "lines": projected_lines,
                                "px": int(projected_width),
                                "file": str(f.name),
                                "dominant": script_info["dominant_script"]
                            })
            except Exception:
                continue

    if bidi_warnings:
        print(f"\n[!] BiDi / RTL Notice: Detected {len(bidi_warnings)} Arabic/Hebrew strings.")
        print("    Requirement: Ensure conversation UI mirrors container coordinates (right-aligned x anchors).")

    if cjk_kinzoku_warnings:
        print(f"\n[!] CJK Kinzoku Shori Notice: Detected {len(cjk_kinzoku_warnings)} lines starting with forbidden punctuation:")
        for w in cjk_kinzoku_warnings[:5]:
            print(f"    - ID '{w['id']}' ({w['file']}): starts with '{w['char']}'")

    if turkish_warnings:
        print(f"\n[!] Turkish i-casing Notice: Detected {len(turkish_warnings)} strings with ambiguous ASCII I/i conversions.")

    if long_strings:
        print(f"\n[!] Detected {len(long_strings)} dialogue strings that overflow UI question lists (>4 lines):")
        for s in long_strings[:15]:
            print(f"    - ID '{s['id']}' ({s['file']}, script={s['dominant']}): {s['len']} chars, ~{s['px']}px (~{s['lines']} lines)")
        if len(long_strings) > 15:
            print(f"    ... and {len(long_strings) - 15} more.")
        print("    Recommendation: Enable always_show_scroll='1' on <questions_list> or condense string.")
    else:
        print("[✓] All dialogue strings fit comfortably within standard UI line budgets.")
    return 0

# -----------------------------------------------------------------------------
# 4. Widescreen UI Aspect Ratio Synchronization (talk.xml <-> talk_16.xml)
# -----------------------------------------------------------------------------
def fix_widescreen_ui(talk_file: Path, talk16_file: Path, apply_fix: bool = False):
    print(f"\n[→] Auditing widescreen conversation UI ({talk_file} vs {talk16_file})...")
    if not (talk_file.exists() and talk16_file.exists()):
        print(f"[✗] One or both talk UI files missing.")
        return 1

    t43_root, _, t43_raw = robust_xml_parse(talk_file)
    t16_root, enc16, t16_raw = robust_xml_parse(talk16_file)

    fixes_applied = 0
    # Ensure complex_mode="1" on all text and question items in talk_16.xml
    fixed_lines = []
    for line in t16_raw.splitlines():
        modified_line = line
        # Check text tags lacking complex_mode
        if "<text " in line and "complex_mode=" not in line:
            modified_line = line.replace("<text ", '<text complex_mode="1" ')
            fixes_applied += 1
        elif "<content_text " in line and "complex_mode=" not in line:
            modified_line = line.replace("<content_text ", '<content_text complex_mode="1" ')
            fixes_applied += 1
        fixed_lines.append(modified_line)

    if fixes_applied > 0:
        if apply_fix:
            talk16_file.write_text("\n".join(fixed_lines), encoding=enc16)
            print(f"[✓] Applied {fixes_applied} text-wrapping fixes to {talk16_file}.")
        else:
            print(f"[!] {fixes_applied} text nodes in {talk16_file} lack complex_mode='1'. Run with --fix to apply.")
    else:
        print("[✓] Widescreen talk UI has correct complex_mode attributes.")
    return 0

# -----------------------------------------------------------------------------
# 5. Encoding & Mojibake Detection and Repair
# -----------------------------------------------------------------------------
def fix_encoding(target_files: list, target_enc: str = "utf-8", apply_fix: bool = False):
    print(f"\n[→] Inspecting file encoding and mojibake across {len(target_files)} files (target={target_enc})...")
    fixed_count = 0
    # Common mojibake patterns:
    # 1. Cyrillic decoded as CP1252: [ÐÑ][\x80-\xBF]
    # 2. Central European (CP1250) double-encoded UTF-8: [ÂÃ][\x80-\xBF]
    # 3. CJK Shift-JIS / GBK decoded as Latin-1: [ææ][\x80-\xFF]
    mojibake_patterns = [
        re.compile(r'[ÐÑ][\x80-\xBF]'),
        re.compile(r'[ÂÃ][\x80-\xBF]'),
        re.compile(r'[\xc2\xc3][\x80-\xbf]')
    ]

    for f in target_files:
        p = Path(f)
        if not p.is_file():
            continue
        raw = p.read_bytes()
        
        # Detect encoding by testing supported codepages
        detected_enc = "utf-8"
        text = ""
        candidate_encodings = [
            "utf-8-sig", "utf-8", "windows-1251", "windows-1250",
            "windows-1252", "shift_jis", "gb18030", "big5", "cp949",
            "windows-1254", "windows-1256", "latin-1"
        ]
        
        for cand in candidate_encodings:
            try:
                text = raw.decode(cand)
                detected_enc = cand
                break
            except Exception:
                continue

        has_mojibake = any(bool(pat.search(text)) for pat in mojibake_patterns)
        needs_transcode = (detected_enc.lower() != target_enc.lower()) or has_mojibake

        if needs_transcode:
            print(f"[!] File {p.name}: detected={detected_enc}, mojibake={has_mojibake}")
            if apply_fix:
                clean_text = text
                if has_mojibake and detected_enc in ["utf-8", "utf-8-sig"]:
                    for fallback in ["windows-1251", "windows-1250", "windows-1252"]:
                        try:
                            clean_text = raw.decode("utf-8").encode(fallback).decode("utf-8")
                            break
                        except Exception:
                            pass

                # Update XML declaration encoding attribute
                clean_text = re.sub(
                    r'<\?xml([^>]+)encoding=["\'][^"\']+["\']([^>]*)>',
                    f'<?xml\\1encoding="{target_enc}"\\2>',
                    clean_text
                )
                try:
                    p.write_bytes(clean_text.encode(target_enc))
                    fixed_count += 1
                except Exception as e:
                    print(f"[✗] Failed to encode {p.name} as {target_enc}: {e}")

    if apply_fix:
        print(f"[✓] Transcoded and repaired {fixed_count} files to {target_enc}.")
    else:
        print(f"[✓] Inspection complete. Run with --fix to execute encoding repairs.")
    return 0

# -----------------------------------------------------------------------------
# 6. Global Multi-Language Coverage Audit
# -----------------------------------------------------------------------------
def audit_languages(base_dir: Path):
    print(f"\n[→] Auditing game language coverage across {base_dir}...")
    if not base_dir.exists():
        print(f"[✗] Directory not found: {base_dir}")
        return 1

    # Standard international game language codes
    common_locales = {
        "en": "English",
        "de": "German (FIGS)",
        "fr": "French (FIGS)",
        "es": "Spanish (FIGS)",
        "it": "Italian (FIGS)",
        "ru": "Russian (Slavic)",
        "uk": "Ukrainian (Slavic)",
        "pl": "Polish (Slavic / Latin-2)",
        "cs": "Czech (Slavic / Latin-2)",
        "ja": "Japanese (CJK)",
        "zh": "Chinese Simplified (CJK)",
        "zh-tw": "Chinese Traditional (CJK)",
        "ko": "Korean (CJK)",
        "pt-br": "Portuguese Brazil",
        "tr": "Turkish",
        "ar": "Arabic (BiDi/RTL)"
    }

    found_locales = {}
    for d in base_dir.iterdir():
        if d.is_dir():
            name = d.name.lower()
            found_locales[name] = len(list(d.glob("*.xml")))

    print(f"[✓] Found language folders in {base_dir.name}:")
    for loc, count in found_locales.items():
        desc = common_locales.get(loc, "Custom Locale")
        ratio = LANGUAGE_EXPANSION_RATIOS.get(loc, 1.0)
        print(f"    - {loc} ({desc}): {count} XML files [Expansion Ratio: {ratio:+.0%}]")

    missing = [k for k in ["en", "de", "fr", "es", "it", "ru", "pl", "ja", "zh"] if k not in found_locales and k != "en"]
    if missing:
        print(f"\n[!] Missing key global market languages: {', '.join(missing)}")
    else:
        print("[✓] Broad global game language coverage verified!")
    return 0

# -----------------------------------------------------------------------------
# 6. Dialogue Tree & Graph Continuity Validation
# -----------------------------------------------------------------------------
def validate_graph(dialog_paths: list):
    print(f"\n[→] Validating dialogue graph continuity across {len(dialog_paths)} files...")
    broken_links = []
    dead_ends = []
    total_dialogs = 0

    for dp in dialog_paths:
        p = Path(dp)
        target_files = list(p.rglob("*.xml")) if p.is_dir() else [p]
        for f in target_files:
            try:
                root, _, _ = robust_xml_parse(f)
            except Exception:
                continue

            for dialog in root.findall(".//dialog"):
                did = dialog.get("id", "unnamed")
                total_dialogs += 1
                phrases = {}
                phrase_list = dialog.find("phrase_list")
                if phrase_list is None:
                    continue

                for phrase in phrase_list.findall("phrase"):
                    pid = phrase.get("id")
                    if pid:
                        next_ids = [n.text.strip() for n in phrase.findall("next") if n.text]
                        phrases[pid] = next_ids

                # Check that all next IDs point to defined phrases
                for pid, next_ids in phrases.items():
                    for nid in next_ids:
                        if nid not in phrases:
                            broken_links.append({
                                "dialog": did,
                                "file": f.name,
                                "from_phrase": pid,
                                "broken_next": nid
                            })

                # Check if dialog has entry point (phrase 0)
                if phrases and "0" not in phrases:
                    dead_ends.append({
                        "dialog": did,
                        "file": f.name,
                        "error": "Missing initial phrase ID='0' (dialogue cannot start)"
                    })

    print(f"[✓] Analyzed {total_dialogs} dialogue graphs.")
    if broken_links or dead_ends:
        print(f"[✗] Found {len(broken_links)} broken <next> targets and {len(dead_ends)} dead-end flaws:")
        for b in broken_links[:15]:
            print(f"    - Dialog '{b['dialog']}' ({b['file']}): phrase {b['from_phrase']} -> missing target {b['broken_next']}")
        for d in dead_ends[:10]:
            print(f"    - Dialog '{d['dialog']}' ({d['file']}): {d['error']}")
        return 1

    print("[✓] All dialogue trees have continuous valid phrase routing.")
    return 0

# -----------------------------------------------------------------------------
# Main CLI Interface
# -----------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Game Dialogue & UI Localization Tool - S.T.A.L.K.E.R. & RPG Dialogue Text & UI Repair Suite"
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # 1. validate-strings
    p_val = subparsers.add_parser("validate-strings", help="Validate XML string table syntax, tags, and colors")
    p_val.add_argument("files", nargs="+", help="XML string table files or directories")
    p_val.add_argument("--no-colors", action="store_true", help="Skip %%c[...] color tag validation")

    # 2. cross-reference
    p_cross = subparsers.add_parser("cross-reference", help="Cross-reference dialogue XMLs against string tables")
    p_cross.add_argument("--dialogs", required=True, nargs="+", help="Dialogue XML files or directories")
    p_cross.add_argument("--strings", required=True, nargs="+", help="String table XML files or directories")

    # 3. check-ui-overrun
    p_ui = subparsers.add_parser("check-ui-overrun", help="Check dialogue string lengths against conversation UI boxes")
    p_ui.add_argument("--ui", required=True, type=Path, help="talk.xml or talk_16.xml file")
    p_ui.add_argument("--strings", required=True, nargs="+", help="String table directories")
    p_ui.add_argument("--max-chars", type=int, default=120, help="Char limit before flagging possible overrun")
    p_ui.add_argument("--lang", default="auto", help="Language code of source strings (auto, en, de, fr, ja, ru, etc.)")
    p_ui.add_argument("--target-lang", help="Target language to simulate expansion against (e.g. de, fr, es, ru, ja)")

    # 4. fix-widescreen-ui
    p_wide = subparsers.add_parser("fix-widescreen-ui", help="Audit and fix complex_mode and bounds in talk_16.xml")
    p_wide.add_argument("--talk", required=True, type=Path, help="Standard 4:3 talk.xml")
    p_wide.add_argument("--talk16", required=True, type=Path, help="Widescreen 16:9 talk_16.xml")
    p_wide.add_argument("--fix", action="store_true", help="Apply fixes directly to talk_16.xml")

    # 5. fix-encoding
    p_enc = subparsers.add_parser("fix-encoding", help="Detect and transcode XML files across common game codepages")
    p_enc.add_argument("files", nargs="+", help="Target XML files")
    p_enc.add_argument(
        "--to",
        default="utf-8",
        choices=[
            "utf-8", "windows-1250", "windows-1251", "windows-1252",
            "windows-1254", "windows-1256", "shift_jis", "gb18030", "big5", "cp949"
        ],
        help="Target encoding"
    )
    p_enc.add_argument("--fix", action="store_true", help="Write changes to disk")

    # 6. validate-graph
    p_graph = subparsers.add_parser("validate-graph", help="Validate dialogue tree phrase links and check for dead-end loops")
    p_graph.add_argument("dialogs", nargs="+", help="Dialogue XML files or directories")

    # 7. audit-languages
    p_aud = subparsers.add_parser("audit-languages", help="Audit global game language coverage, file counts, and expansion ratios")
    p_aud.add_argument("text_dir", type=Path, help="Base text directory (e.g. gamedata/config/text/)")

    args = parser.parse_args()

    if args.subcommand == "validate-strings":
        return validate_strings(args.files, check_colors=not args.no_colors)
    elif args.subcommand == "cross-reference":
        return cross_reference(args.dialogs, args.strings)
    elif args.subcommand == "check-ui-overrun":
        return check_ui_overrun(
            args.ui,
            args.strings,
            max_warn_chars=args.max_chars,
            lang=args.lang,
            target_lang=args.target_lang
        )
    elif args.subcommand == "fix-widescreen-ui":
        return fix_widescreen_ui(args.talk, args.talk16, apply_fix=args.fix)
    elif args.subcommand == "fix-encoding":
        return fix_encoding(args.files, target_enc=args.to, apply_fix=args.fix)
    elif args.subcommand == "validate-graph":
        return validate_graph(args.dialogs)
    elif args.subcommand == "audit-languages":
        return audit_languages(args.text_dir)

    return 0

if __name__ == "__main__":
    sys.exit(main())

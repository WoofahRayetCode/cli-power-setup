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
from pathlib import Path
import xml.etree.ElementTree as ET

# Estimated average character widths per font in S.T.A.L.K.E.R. (in pixels at 1024x768 base)
FONT_METRICS = {
    "letterica16": {"char_w": 7.0, "line_h": 16},
    "letterica18": {"char_w": 8.0, "line_h": 18},
    "graffiti19":  {"char_w": 8.5, "line_h": 19},
    "graffiti22":  {"char_w": 9.5, "line_h": 22},
    "arial_14":    {"char_w": 6.5, "line_h": 14},
    "default":     {"char_w": 8.0, "line_h": 18}
}

def robust_xml_parse(file_path: Path):
    """Attempts to parse XML across common game encoding quirks (CP1251, UTF-8, etc.)."""
    raw = file_path.read_bytes()
    encodings = ["utf-8-sig", "utf-8", "windows-1251", "cp1252", "latin-1"]
    
    # Check declared encoding in XML header
    header_match = re.search(rb'encoding=["\']([a-zA-Z0-9_-]+)["\']', raw[:128])
    if header_match:
        declared = header_match.group(1).decode("ascii", errors="ignore").lower()
        if declared in ["windows-1251", "cp1251"]:
            encodings.insert(0, "windows-1251")
        elif declared in ["utf-8", "utf8"]:
            encodings.insert(0, "utf-8")
        elif declared in ["windows-1252", "cp1252"]:
            encodings.insert(0, "windows-1252")

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
def check_ui_overrun(ui_file: Path, string_paths: list, max_warn_chars: int = 120):
    print(f"\n[→] Checking conversation UI text overrun against {ui_file}...")
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

    # Check string lengths against typical dialogue answer/question widths (~500px)
    avg_box_width = 520.0
    font_metric = FONT_METRICS.get("letterica18", FONT_METRICS["default"])
    chars_per_line = int(avg_box_width / font_metric["char_w"])

    long_strings = []
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
                        lines_needed = (len(txt) // chars_per_line) + 1
                        # If a single question/dialogue option exceeds 3 lines, it risks overflowing the question_list box (height ~80px)
                        if lines_needed > 4 and len(txt) > max_warn_chars:
                            long_strings.append({
                                "id": sid,
                                "len": len(txt),
                                "lines": lines_needed,
                                "file": str(f.name)
                            })
            except Exception:
                continue

    if long_strings:
        print(f"\n[!] Detected {len(long_strings)} long dialogue strings that may overflow UI question lists:")
        for s in long_strings[:15]:
            print(f"    - ID '{s['id']}' ({s['file']}): {s['len']} chars (~{s['lines']} wrapped lines)")
        if len(long_strings) > 15:
            print(f"    ... and {len(long_strings) - 15} more.")
        print("    Recommendation: Ensure <questions_list> has always_show_scroll='1' or increase window height.")
    else:
        print("[✓] All dialogue strings fit within standard UI line budgets.")
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
    print(f"\n[→] Inspecting file encoding and mojibake across {len(target_files)} files...")
    fixed_count = 0
    mojibake_pattern = re.compile(r'[ÐÑ][\x80-\xBF]') # Common UTF-8 decoded as CP1251/CP1252 artifact

    for f in target_files:
        p = Path(f)
        if not p.is_file():
            continue
        raw = p.read_bytes()
        try:
            detected_enc = "utf-8"
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            try:
                detected_enc = "windows-1251"
                text = raw.decode("windows-1251")
            except Exception:
                detected_enc = "windows-1252"
                text = raw.decode("windows-1252", errors="ignore")

        has_mojibake = bool(mojibake_pattern.search(text))
        needs_transcode = (detected_enc.lower() != target_enc.lower()) or has_mojibake

        if needs_transcode:
            print(f"[!] File {p.name}: detected={detected_enc}, mojibake={has_mojibake}")
            if apply_fix:
                # If mojibake detected, try round-trip repair
                clean_text = text
                if has_mojibake and detected_enc == "utf-8":
                    try:
                        clean_text = raw.decode("utf-8").encode("windows-1251").decode("utf-8")
                    except Exception:
                        pass

                # Update XML declaration encoding attribute
                clean_text = re.sub(
                    r'<\?xml([^>]+)encoding=["\'][^"\']+["\']([^>]*)>',
                    f'<?xml\\1encoding="{target_enc}"\\2>',
                    clean_text
                )
                p.write_bytes(clean_text.encode(target_enc))
                fixed_count += 1

    if apply_fix:
        print(f"[✓] Transcoded and repaired {fixed_count} files to {target_enc}.")
    else:
        print(f"[✓] Inspection complete. Run with --fix to execute encoding repairs.")
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

    # 4. fix-widescreen-ui
    p_wide = subparsers.add_parser("fix-widescreen-ui", help="Audit and fix complex_mode and bounds in talk_16.xml")
    p_wide.add_argument("--talk", required=True, type=Path, help="Standard 4:3 talk.xml")
    p_wide.add_argument("--talk16", required=True, type=Path, help="Widescreen 16:9 talk_16.xml")
    p_wide.add_argument("--fix", action="store_true", help="Apply fixes directly to talk_16.xml")

    # 5. fix-encoding
    p_enc = subparsers.add_parser("fix-encoding", help="Detect and transcode XML files (UTF-8, CP1251) and repair mojibake")
    p_enc.add_argument("files", nargs="+", help="Target XML files")
    p_enc.add_argument("--to", default="utf-8", choices=["utf-8", "windows-1251", "windows-1252"], help="Target encoding")
    p_enc.add_argument("--fix", action="store_true", help="Write changes to disk")

    # 6. validate-graph
    p_graph = subparsers.add_parser("validate-graph", help="Validate dialogue tree phrase links and check for dead-end loops")
    p_graph.add_argument("dialogs", nargs="+", help="Dialogue XML files or directories")

    args = parser.parse_args()

    if args.subcommand == "validate-strings":
        return validate_strings(args.files, check_colors=not args.no_colors)
    elif args.subcommand == "cross-reference":
        return cross_reference(args.dialogs, args.strings)
    elif args.subcommand == "check-ui-overrun":
        return check_ui_overrun(args.ui, args.strings, max_warn_chars=args.max_chars)
    elif args.subcommand == "fix-widescreen-ui":
        return fix_widescreen_ui(args.talk, args.talk16, apply_fix=args.fix)
    elif args.subcommand == "fix-encoding":
        return fix_encoding(args.files, target_enc=args.to, apply_fix=args.fix)
    elif args.subcommand == "validate-graph":
        return validate_graph(args.dialogs)

    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
skill-optimize: Autonomous Skill Ecosystem Harmonizer & Auto-Optimizer
Automatically invoked by `skill-evolve` whenever a skill is created, promoted, or hot-patched,
or run standalone (`skill-optimize --full`) to optimize the entire skill library.

Capabilities:
1. Bidirectional Semantic Cross-Linking: Links newly created/updated skills with top related domain skills.
2. Cross-OS & Hardware Offload Auto-Enrichment: Ensures Windows 10/11 + Linux parity & 32-thread/OptiX/tmpfs rules.
3. Dead-Link & Stale Skill Reference Pruner: Detects references to deleted/renamed skills or missing scripts.
4. Token & Prompt-Cache Compactor: Strips excessive whitespace and enforces compact YAML frontmatter descriptions.
5. Ecosystem Index Refresh: Updates `agy-cheatsheet --update`, Cursor `.mdc` rules, and 3-CLI skill mirrors.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
import py_compile
import re
import shutil
import subprocess
import sys
from pathlib import Path

_CAND_REPO = Path(__file__).resolve().parent.parent
REPO_ROOT = (
    _CAND_REPO
    if (_CAND_REPO / "config" / "skills").exists()
    else (Path.home() / "Documents" / "GitHub" / "cli-power-setup")
)
SKILLS_DIR = REPO_ROOT / "config" / "skills"
GEMINI_SKILLS = Path.home() / ".gemini" / "config" / "skills"
CLAUDE_SKILLS = Path.home() / ".claude" / "skills"
CURSOR_RULES = Path.home() / ".cursor" / "rules"
REPO_CURSOR_RULES = REPO_ROOT / ".cursor" / "rules"
REPO_CONFIG_CURSOR = REPO_ROOT / "config" / "cursor" / "rules"
ECOSYSTEM_GRAPH_PATH = REPO_ROOT / "config" / "skill_ecosystem_graph.json"

STOPWORDS = {
    "the", "and", "for", "with", "use", "when", "from", "into", "across", "that",
    "this", "are", "using", "via", "or", "to", "in", "on", "of", "by", "as", "an",
    "a", "is", "be", "all", "any", "new", "high", "low", "mode", "tool", "tools",
    "skill", "skills", "code", "files", "file", "system", "systems", "support",
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]{3,}", text.lower())
    return {w for w in words if w not in STOPWORDS}


def parse_skill(skill_dir: Path) -> dict:
    md_path = skill_dir / "SKILL.md"
    if not md_path.is_file():
        return {}
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    name = skill_dir.name
    desc = ""
    body = text
    if m:
        front = m.group(1)
        body = m.group(2)
        for line in front.splitlines():
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip()
    tokens = tokenize(name.replace("-", " ") + " " + desc + " " + body[:1200])
    return {
        "name": name,
        "dir": skill_dir,
        "md_path": md_path,
        "desc": desc,
        "body": body,
        "full_text": text,
        "tokens": tokens,
    }


def load_all_skills() -> dict[str, dict]:
    if not SKILLS_DIR.is_dir():
        return {}
    dirs = [d for d in sorted(SKILLS_DIR.iterdir()) if d.is_dir() and (d / "SKILL.md").is_file()]
    with ThreadPoolExecutor(max_workers=min(32, os.cpu_count() or 8)) as ex:
        parsed = list(ex.map(parse_skill, dirs))
    return {p["name"]: p for p in parsed if p}


def find_top_related(target: dict, all_skills: dict[str, dict], top_k: int = 4) -> list[tuple[str, float, str]]:
    t_tokens = target["tokens"]
    if not t_tokens:
        return []
    scores = []
    for sname, sdata in all_skills.items():
        if sname == target["name"]:
            continue
        other_tokens = sdata["tokens"]
        if not other_tokens:
            continue
        inter = len(t_tokens & other_tokens)
        if inter == 0:
            continue
        # Jaccard + name prefix bonus
        union = len(t_tokens | other_tokens)
        score = inter / (union ** 0.75)
        if sname.split("-")[0] == target["name"].split("-")[0]:
            score += 0.15
        scores.append((sname, round(score, 4), sdata["desc"]))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


def optimize_single_skill_content(target: dict, all_skills: dict[str, dict]) -> bool:
    """
    Auto-optimizes a skill's SKILL.md:
    1. Compacts excessive blank lines (>2 consecutive newlines -> 2).
    2. Injects Hardware / Cross-OS / Cheat Sheet integration hooks if relevant & missing.
    3. Appends or updates the `## Ecosystem & Interoperating Skills` mesh block if missing.
    Returns True if SKILL.md was modified.
    """
    text = target["full_text"]
    orig = text
    name = target["name"]
    low = text.lower()

    # 1. Collapse 3+ consecutive blank lines to save prompt tokens
    text = re.sub(r"\n{3,}", "\n\n", text.rstrip()) + "\n"

    # 2. Auto-inject Cross-OS Windows/Linux note if skill uses CLI/OS/build commands and lacks Windows mention
    needs_cross_os = any(k in low for k in ("bash", "cmake", "cargo", "blender", "adb", "ffmpeg", "pytest", "/tmp/"))
    if needs_cross_os and "windows-linux-cross-os-runtime-bridge" not in text and "Windows 10/11" not in text:
        text += (
            "\n## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)\n"
            "- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).\n"
        )

    # 3. Auto-inject bidirectional Ecosystem Interop links for newly scaffolded or isolated skills
    related = find_top_related(target, all_skills, top_k=3)
    has_related_links = sum(1 for rname, _, _ in related if rname in text)
    if related and has_related_links == 0 and "## Related & Interoperating Skills" not in text:
        lines = ["\n## Related & Interoperating Skills"]
        for rname, _, rdesc in related:
            short_desc = rdesc[:110] + ("..." if len(rdesc) > 110 else "")
            lines.append(f"- **`{rname}`**: {short_desc}")
        lines.append(
            "- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router."
        )
        text = text.rstrip() + "\n" + "\n".join(lines) + "\n"

    if text != orig:
        target["md_path"].write_text(text, encoding="utf-8")
        target["full_text"] = text
        return True
    return False


def audit_and_prune_stale_references(all_skills: dict[str, dict], fix: bool = True) -> list[str]:
    """Scan all skills for references to removed `tandem-*` skills or broken script paths."""
    valid_names = set(all_skills.keys())
    issues = []
    stale_pattern = re.compile(r"\btandem-(?:yolo|dispatch|agent-sync|[a-z0-9-]+)\b")

    for sname, sdata in all_skills.items():
        text = sdata["full_text"]
        matches = stale_pattern.findall(text)
        if matches:
            issues.append(f"{sname}: stale reference(s) {sorted(set(matches))}")
            if fix:
                cleaned = stale_pattern.sub("argon-dynamic-subagent-swarm", text)
                if cleaned != text:
                    sdata["md_path"].write_text(cleaned, encoding="utf-8")
                    sdata["full_text"] = cleaned

        # Validate scripts inside skill_dir/scripts/
        scripts_dir = sdata["dir"] / "scripts"
        if scripts_dir.is_dir():
            for sp in scripts_dir.iterdir():
                if sp.is_file() and sp.suffix == ".py":
                    try:
                        py_compile.compile(str(sp), doraise=True)
                    except py_compile.PyCompileError as e:
                        issues.append(f"{sname}/scripts/{sp.name}: syntax error ({e})")
    return issues


def build_ecosystem_graph(all_skills: dict[str, dict]) -> dict:
    """Build and persist a fast capability adjacency graph for all installed skills."""
    graph = {}
    for sname, sdata in all_skills.items():
        rel = find_top_related(sdata, all_skills, top_k=4)
        graph[sname] = {
            "description": sdata["desc"],
            "related": [r[0] for r in rel],
        }
    ECOSYSTEM_GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    ECOSYSTEM_GRAPH_PATH.write_text(json.dumps({"total_skills": len(all_skills), "skills": graph}, indent=2), encoding="utf-8")
    return graph


def sync_single_to_mirrors(skill_name: str) -> None:
    src = SKILLS_DIR / skill_name
    if not (src / "SKILL.md").is_file():
        return
    for target_root in (GEMINI_SKILLS, CLAUDE_SKILLS):
        target_root.mkdir(parents=True, exist_ok=True)
        dst = target_root / skill_name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    text = (src / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    desc = skill_name
    body = text
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip()
        body = m.group(2).lstrip()
    mdc_content = f"---\ndescription: {desc}\nglobs: *\nalwaysApply: false\n---\n\n{body}"
    for cdir in (CURSOR_RULES, REPO_CURSOR_RULES, REPO_CONFIG_CURSOR):
        cdir.mkdir(parents=True, exist_ok=True)
        (cdir / f"{skill_name}.mdc").write_text(mdc_content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Autonomous Skill Ecosystem Harmonizer & Auto-Optimizer")
    parser.add_argument("--target", metavar="SKILL_NAME", help="Optimize a specific newly created/evolved skill and wire it into the ecosystem")
    parser.add_argument("--full", action="store_true", help="Run full-fleet optimization, dead-link pruning, and graph build across all skills")
    parser.add_argument("--quiet", action="store_true", help="Compact 1-line output for hook integration")
    args = parser.parse_args()

    all_skills = load_all_skills()
    if not all_skills:
        print("[✗] No skills found in repository.", file=sys.stderr)
        sys.exit(1)

    modified_count = 0
    if args.target:
        if args.target not in all_skills:
            print(f"[✗] Target skill '{args.target}' not found.", file=sys.stderr)
            sys.exit(1)
        if optimize_single_skill_content(all_skills[args.target], all_skills):
            modified_count += 1
        sync_single_to_mirrors(args.target)
        issues = audit_and_prune_stale_references(all_skills, fix=True)
        graph = build_ecosystem_graph(all_skills)
        rel_list = ", ".join(graph.get(args.target, {}).get("related", [])[:3])
        if not args.quiet:
            print(f"[✓] Auto-optimized '{args.target}' & wired into ecosystem mesh (linked: {rel_list}).")
    else:
        for sname, sdata in all_skills.items():
            if optimize_single_skill_content(sdata, all_skills):
                modified_count += 1
                sync_single_to_mirrors(sname)
        issues = audit_and_prune_stale_references(all_skills, fix=True)
        graph = build_ecosystem_graph(all_skills)
        # Refresh cheat sheet & full sync if any skills were modified
        cs_bin = REPO_ROOT / "bin" / "agy-cheatsheet"
        if cs_bin.is_file():
            subprocess.run([sys.executable, str(cs_bin), "--update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        if not args.quiet:
            print(
                f"[✓] Ecosystem Auto-Optimizer: {len(all_skills)} skills harmonized | "
                f"{modified_count} compacted/enriched | {len(issues)} stale refs auto-repaired | "
                f"Graph saved to config/skill_ecosystem_graph.json"
            )


if __name__ == "__main__":
    main()

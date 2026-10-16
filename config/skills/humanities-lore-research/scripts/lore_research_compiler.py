#!/usr/bin/env python3
"""
Humanities, History & Mythology Lore Research Compiler
======================================================
Compiles historical data, mythological pantheons, folklore, and worldbuilding
into structured encyclopedic schemas, chronological timeline streams, and
node-link relationship graphs for web site rendering and digital encyclopedias.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def create_entity_dossier(
    name: str,
    domain: str,
    culture_or_era: str,
    archetype: Optional[str] = None,
    summary: str = "",
    attributes: Optional[List[str]] = None,
    relationships: Optional[List[Dict[str, str]]] = None,
    primary_sources: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Build a validated entity dossier for a historical figure, deity, or creature."""
    return {
        "id": name.lower().replace(" ", "_"),
        "name": name,
        "domain": domain,
        "culture_or_era": culture_or_era,
        "archetype": archetype or "Unclassified",
        "summary": summary,
        "attributes": attributes or [],
        "relationships": relationships or [],
        "primary_sources": primary_sources or []
    }


def compile_timeline(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort and validate chronological events for web timeline visualization."""
    def parse_year(ev: Dict[str, Any]) -> float:
        # Support BCE (negative) and CE (positive)
        year_val = ev.get("year", 0)
        if isinstance(year_val, (int, float)):
            return float(year_val)
        y_str = str(year_val).strip().upper()
        if "BCE" in y_str or "BC" in y_str:
            num = float("".join(c for c in y_str if c.isdigit() or c == "."))
            return -num
        num_str = "".join(c for c in y_str if c.isdigit() or c in ".-")
        return float(num_str) if num_str else 0.0

    sorted_events = sorted(events, key=parse_year)
    return sorted_events


def build_relationship_graph(entities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Transform entity dossiers into node-link graph for D3 / Vis.js network visualization."""
    nodes = []
    links = []
    seen_nodes = set()

    for ent in entities:
        ent_id = ent.get("id") or ent["name"].lower().replace(" ", "_")
        if ent_id not in seen_nodes:
            nodes.append({
                "id": ent_id,
                "label": ent["name"],
                "group": ent.get("culture_or_era", "General"),
                "domain": ent.get("domain", "Mythology")
            })
            seen_nodes.add(ent_id)

        for rel in ent.get("relationships", []):
            target = rel.get("target", "").lower().replace(" ", "_")
            if target:
                if target not in seen_nodes:
                    nodes.append({
                        "id": target,
                        "label": rel.get("target"),
                        "group": ent.get("culture_or_era", "General"),
                        "domain": ent.get("domain", "Mythology")
                    })
                    seen_nodes.add(target)
                links.append({
                    "source": ent_id,
                    "target": target,
                    "relation": rel.get("type", "associated_with")
                })

    return {"nodes": nodes, "links": links}


def render_markdown_wiki_page(entity: Dict[str, Any]) -> str:
    """Generate an encyclopedic wiki markdown document for static site generators."""
    lines = [
        f"# {entity['name']}",
        f"**Domain:** {entity.get('domain', 'N/A')} | **Culture/Era:** {entity.get('culture_or_era', 'N/A')} | **Archetype:** {entity.get('archetype', 'N/A')}\n",
        "## Overview",
        f"{entity.get('summary', 'No summary provided.')}\n",
        "## Attributes & Domains of Influence",
    ]
    for attr in entity.get("attributes", []):
        lines.append(f"- **{attr}**")

    lines.append("\n## Mythological & Historical Relationships")
    for rel in entity.get("relationships", []):
        lines.append(f"- **{rel.get('type', 'Associated with').replace('_', ' ').title()}:** {rel.get('target', 'Unknown')}")

    if entity.get("primary_sources"):
        lines.append("\n## Primary Sources & Historical Records")
        for src in entity["primary_sources"]:
            lines.append(f"- *{src}*")

    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Humanities, History & Mythology Lore Research Compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # export-wiki
    wiki_p = subparsers.add_parser("export-wiki", help="Convert entity JSON dossier to markdown wiki page")
    wiki_p.add_argument("json_file", type=str, help="Path to entity JSON file")
    wiki_p.add_argument("--out", type=str, default=None, help="Output markdown path")

    # compile-network
    net_p = subparsers.add_parser("compile-network", help="Compile multiple entity dossiers into a relationship graph")
    net_p.add_argument("files", nargs="+", help="Input entity JSON files")
    net_p.add_argument("--out", type=str, default="relationship_graph.json", help="Output network JSON path")

    # sort-timeline
    time_p = subparsers.add_parser("sort-timeline", help="Sort event list chronologically")
    time_p.add_argument("timeline_file", type=str, help="Input raw timeline events JSON")
    time_p.add_argument("--out", type=str, default="sorted_timeline.json", help="Output sorted timeline JSON")

    args = parser.parse_args()

    if args.command == "export-wiki":
        data = json.loads(Path(args.json_file).read_text(encoding="utf-8"))
        md = render_markdown_wiki_page(data)
        if args.out:
            Path(args.out).write_text(md, encoding="utf-8")
            print(f"[✓] Wiki page generated: {args.out}")
        else:
            print(md)

    elif args.command == "compile-network":
        entities = []
        for f in args.files:
            entities.append(json.loads(Path(f).read_text(encoding="utf-8")))
        graph = build_relationship_graph(entities)
        Path(args.out).write_text(json.dumps(graph, indent=2), encoding="utf-8")
        print(f"[✓] Network graph compiled ({len(graph['nodes'])} nodes, {len(graph['links'])} links): {args.out}")

    elif args.command == "sort-timeline":
        events = json.loads(Path(args.timeline_file).read_text(encoding="utf-8"))
        sorted_evs = compile_timeline(events)
        Path(args.out).write_text(json.dumps(sorted_evs, indent=2), encoding="utf-8")
        print(f"[✓] Sorted {len(sorted_evs)} timeline events: {args.out}")


if __name__ == "__main__":
    main()

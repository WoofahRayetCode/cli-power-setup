#!/usr/bin/env python3
"""
Interactive Data Visualization Web Generator
============================================
Generates standalone, zero-build interactive web visualizations for history,
mythology, and complex systems:
- Vis.js interactive chronological timeline
- D3.js force-directed pantheon / faction network graph
- Interactive entity radar/attribute chart
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def generate_interactive_timeline(events: List[Dict[str, Any]], title: str = "Historical Timeline") -> str:
    """Generate self-contained Vis.js interactive timeline widget."""
    vis_items = []
    for i, ev in enumerate(events):
        vis_items.append({
            "id": i + 1,
            "content": f"<strong>{ev.get('title', 'Event')}</strong>",
            "start": str(ev.get("year", "2000")),
            "title": ev.get("description", "")
        })

    events_json = json.dumps(vis_items, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <script type="text/javascript" src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
  <link href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet" type="text/css" />
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #0B0F19;
      color: #F3F4F6;
      padding: 2rem;
      margin: 0;
    }}
    h1 {{
      color: #38BDF8;
      text-align: center;
      margin-bottom: 1.5rem;
    }}
    #timeline {{
      background: #111827;
      border: 1px solid #374151;
      border-radius: 8px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }}
    .vis-item {{
      background-color: #0284C7;
      border-color: #38BDF8;
      color: #FFFFFF;
      border-radius: 4px;
    }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <div id="timeline"></div>
  <script type="text/javascript">
    const container = document.getElementById('timeline');
    const items = new vis.DataSet({events_json});
    const options = {{
      zoomable: true,
      moveable: true,
      stack: true,
      margin: {{ item: 10, axis: 5 }}
    }};
    new vis.Timeline(container, items, options);
  </script>
</body>
</html>
"""


def generate_network_graph(graph_data: Dict[str, Any], title: str = "Pantheon & Faction Graph") -> str:
    """Generate self-contained D3.js force-directed relationship graph."""
    graph_json = json.dumps(graph_data, indent=2)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body {{
      margin: 0;
      background: #090D16;
      color: #F9FAFB;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      overflow: hidden;
    }}
    h1 {{
      position: absolute;
      top: 15px; left: 20px;
      margin: 0;
      font-size: 1.4rem;
      color: #38BDF8;
      pointer-events: none;
    }}
    svg {{
      width: 100vw;
      height: 100vh;
    }}
    .links line {{
      stroke: #4B5563;
      stroke-opacity: 0.6;
      stroke-width: 1.5px;
    }}
    .nodes circle {{
      stroke: #FFFFFF;
      stroke-width: 1.5px;
      cursor: pointer;
    }}
    .node-label {{
      font-size: 12px;
      fill: #E5E7EB;
      pointer-events: none;
    }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <svg></svg>
  <script>
    const data = {graph_json};
    const width = window.innerWidth;
    const height = window.innerHeight;

    const svg = d3.select("svg")
      .attr("viewBox", [0, 0, width, height]);

    const simulation = d3.forceSimulation(data.nodes)
      .force("link", d3.forceLink(data.links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.append("g")
      .attr("class", "links")
      .selectAll("line")
      .data(data.links)
      .join("line");

    const node = svg.append("g")
      .attr("class", "nodes")
      .selectAll("g")
      .data(data.nodes)
      .join("g")
      .call(d3.drag()
        .on("start", (event, d) => {{
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x; d.fy = d.y;
        }})
        .on("drag", (event, d) => {{
          d.fx = event.x; d.fy = event.y;
        }})
        .on("end", (event, d) => {{
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null; d.fy = null;
        }}));

    node.append("circle")
      .attr("r", 10)
      .attr("fill", "#0284C7");

    node.append("text")
      .attr("class", "node-label")
      .attr("x", 14)
      .attr("y", 4)
      .text(d => d.label || d.id);

    simulation.on("tick", () => {{
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("transform", d => `translate(${{d.x}},${{d.y}})`);
    }});
  </script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Interactive Data Visualization Web Generator")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # timeline
    t_p = subparsers.add_parser("timeline", help="Generate Vis.js interactive timeline HTML")
    t_p.add_argument("events_json", type=str, help="JSON file containing array of events")
    t_p.add_argument("--title", type=str, default="Chronological Timeline", help="Timeline title")
    t_p.add_argument("--out", type=str, default="timeline.html", help="Output HTML file")

    # network
    n_p = subparsers.add_parser("network", help="Generate D3.js force-directed network graph HTML")
    n_p.add_argument("graph_json", type=str, help="JSON file with 'nodes' and 'links'")
    n_p.add_argument("--title", type=str, default="Pantheon Relationship Graph", help="Graph title")
    n_p.add_argument("--out", type=str, default="network.html", help="Output HTML file")

    args = parser.parse_args()

    if args.command == "timeline":
        events = json.loads(Path(args.events_json).read_text(encoding="utf-8"))
        html = generate_interactive_timeline(events, title=args.title)
        Path(args.out).write_text(html, encoding="utf-8")
        print(f"[✓] Generated interactive timeline: {args.out}")

    elif args.command == "network":
        graph_data = json.loads(Path(args.graph_json).read_text(encoding="utf-8"))
        html = generate_network_graph(graph_data, title=args.title)
        Path(args.out).write_text(html, encoding="utf-8")
        print(f"[✓] Generated force-directed network graph: {args.out}")


if __name__ == "__main__":
    main()

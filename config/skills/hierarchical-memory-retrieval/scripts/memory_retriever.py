#!/usr/bin/env python3
"""
High-speed BM25 / keyword memory retriever across .agents/memory, .agents/episodes,
and project docs. Zero external dependencies.
"""
import sys
import os
import re
import json
import math
import argparse
from pathlib import Path
from collections import Counter

STOP_WORDS = {
    "a", "about", "above", "after", "again", "all", "am", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from",
    "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him",
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she",
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "why", "with", "would", "you", "your", "yours", "yourself", "yourselves"
}

def tokenize(text: str):
    return [t for t in re.findall(r'[a-zA-Z0-9_\-\.]{2,}', text.lower()) if t not in STOP_WORDS]

def extract_sections(content: str, file_path: Path):
    """Splits markdown content into logical heading sections."""
    lines = content.splitlines()
    sections = []
    current_title = file_path.name
    current_lines = []

    for line in lines:
        if line.startswith("#"):
            if current_lines:
                text = "\n".join(current_lines).strip()
                if text:
                    sections.append((current_title, text))
                current_lines = []
            current_title = line.strip("# \t*")
        else:
            current_lines.append(line)

    if current_lines:
        text = "\n".join(current_lines).strip()
        if text:
            sections.append((current_title, text))

    if not sections and content.strip():
        sections.append((file_path.name, content.strip()))

    return sections

def search_memory(query: str, target_dirs, top_k: int = 3):
    q_tokens = tokenize(query)
    if not q_tokens:
        return []

    documents = []  # list of (file_path, section_title, snippet, token_counter)
    
    for base_dir in target_dirs:
        p = Path(base_dir)
        if not p.exists():
            continue
        for root, _, files in os.walk(p):
            for file in files:
                if file.endswith((".md", ".txt", ".json", ".log")):
                    file_path = Path(root) / file
                    try:
                        content = file_path.read_text(encoding="utf-8", errors="ignore")
                        sections = extract_sections(content, file_path)
                        for title, text in sections:
                            tokens = tokenize(f"{title} {text}")
                            if tokens:
                                documents.append((str(file_path), title, text, Counter(tokens)))
                    except Exception:
                        continue

    if not documents:
        return []

    # Simple BM25 scoring
    doc_count = len(documents)
    avg_dl = sum(sum(c.values()) for _, _, _, c in documents) / max(1, doc_count)
    k1 = 1.5
    b = 0.75

    # Document frequency
    df = Counter()
    for _, _, _, c in documents:
        for token in set(c.keys()):
            df[token] += 1

    scored = []
    for fpath, title, text, tf in documents:
        dl = sum(tf.values())
        score = 0.0
        for token in q_tokens:
            if token in tf:
                doc_freq = df[token]
                idf = math.log((doc_count - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
                freq = tf[token]
                numerator = freq * (k1 + 1.0)
                denominator = freq + k1 * (1.0 - b + b * (dl / avg_dl))
                score += idf * (numerator / denominator)
                
                # Bonus if token in title
                if token in title.lower():
                    score += 1.5

        if score > 0:
            # Extract first 3-5 non-empty lines for preview snippet
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            snippet = " ".join(lines[:4])
            if len(snippet) > 280:
                snippet = snippet[:280] + "..."
            scored.append({
                "score": round(score, 3),
                "file": fpath,
                "section": title,
                "snippet": snippet
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]

def main():
    parser = argparse.ArgumentParser(description="Hierarchical Memory & Context Retriever")
    parser.add_argument("query", help="Keywords or question to search across memory")
    parser.add_argument("--dirs", nargs="+", default=[".agents/memory", ".agents/episodes", ".agents/checkpoints", "docs"],
                        help="Directories to search (default: .agents/memory, .agents/episodes)")
    parser.add_argument("--top", type=int, default=3, help="Number of results to return (default: 3)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    results = search_memory(args.query, args.dirs, top_k=args.top)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    if not results:
        print(f"[!] No relevant memory snippets found for query: '{args.query}'")
        return

    print(f"🔍 Top {len(results)} Memory Matches for: '{args.query}'")
    print("-" * 60)
    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['file']} > {r['section']} (Relevance: {r['score']})")
        print(f"    Excerpt: {r['snippet']}\n")

if __name__ == "__main__":
    main()

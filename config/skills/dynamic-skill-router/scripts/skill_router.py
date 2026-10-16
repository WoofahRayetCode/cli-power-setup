#!/usr/bin/env python3
import sys
import os
import re
import json
import argparse
from pathlib import Path
from collections import Counter
import math

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent

def load_skills():
    skills = {}
    if not SKILLS_DIR.exists():
        return skills

    for skill_path in SKILLS_DIR.iterdir():
        if not skill_path.is_dir():
            continue
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8", errors="ignore")
        # Extract name and description
        desc_match = re.search(r'description:\s*(.*?)(?:\n---|\n[a-zA-Z0-9_-]+:)', content, re.DOTALL)
        desc = desc_match.group(1).strip() if desc_match else ""
        skills[skill_path.name] = {
            "name": skill_path.name,
            "description": desc,
            "full_text": content[:1500]  # First 1500 chars for keyword indexing
        }
    return skills

def tokenize(text):
    return re.findall(r'[a-zA-Z0-9_-]{2,}', text.lower())

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
    "why", "with", "would", "you", "your", "yours", "yourself", "yourselves", "help"
}

def score_skills(query, skills):
    raw_tokens = tokenize(query)
    q_tokens = [t for t in raw_tokens if t not in STOP_WORDS]
    if not q_tokens:
        q_tokens = raw_tokens
    if not q_tokens:
        return []

    # Calculate document frequencies
    total_docs = len(skills)
    doc_freqs = Counter()
    doc_tokens_map = {}

    for name, data in skills.items():
        tokens = tokenize(f"{name} {name} {name} {data['description']} {data['full_text']}")
        unique_tokens = set(tokens)
        for t in unique_tokens:
            doc_freqs[t] += 1
        doc_tokens_map[name] = tokens

    scores = []
    for name, data in skills.items():
        doc_tokens = doc_tokens_map[name]
        doc_len = len(doc_tokens)
        if doc_len == 0:
            continue

        counts = Counter(doc_tokens)
        score = 0.0
        matched_terms = []

        for token in q_tokens:
            if token in counts:
                # BM25-style IDF
                df = doc_freqs.get(token, 1)
                idf = math.log((total_docs - df + 0.5) / (df + 0.5) + 1.0)
                tf = counts[token] / (counts[token] + 1.5)

                # Massive boost for skill name matches
                name_boost = 6.0 if token in name.lower() else 1.0
                score += (tf * idf * name_boost)
                matched_terms.append(token)

        if score > 0:
            scores.append({
                "skill": name,
                "score": score,
                "matched_terms": list(set(matched_terms)),
                "description": data["description"]
            })

    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores

def main():
    parser = argparse.ArgumentParser(description="Dynamic Semantic Skill Router")
    parser.add_argument("query", help="User task or prompt query")
    parser.add_argument("-k", "--top-k", type=int, default=3, help="Number of top skills to return (default: 3)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show matched terms and detailed scores")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()
    skills = load_skills()

    results = score_skills(args.query, skills)[:args.top_k]

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print(f"\n--- 🧭 Dynamic Skill Router Matches for: '{args.query}' ---")
    if not results:
        print("[!] No confident skill matches found.")
        return

    for idx, r in enumerate(results, 1):
        print(f"\n{idx}. \033[1;36m{r['skill']}\033[0m (Score: {r['score']:.4f})")
        print(f"   {r['description']}")
        if args.verbose:
            print(f"   Matched keywords: {', '.join(r['matched_terms'])}")
    print("\n-------------------------------------------------------------\n")

if __name__ == "__main__":
    main()

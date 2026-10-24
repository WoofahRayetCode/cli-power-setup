#!/usr/bin/env python3
"""
Perplexity Pro & Sonar Multi-Vector Query Decomposer
Decomposes complex technical questions into orthogonal search vectors
for parallel execution and grounded synthesis.
"""

import argparse
import sys

def decompose(query):
    print("════════════════════════════════════════════════════════════════════")
    print(" 🔍 PERPLEXITY PRO / SONAR MULTI-VECTOR QUERY DECOMPOSITION")
    print("════════════════════════════════════════════════════════════════════")
    print(f"Target Prompt: \"{query}\"\n")
    
    vectors = [
        ("Vector 1 [Ground-Truth Docs]", f"\"{query}\" official documentation api reference site:docs.* OR site:github.com"),
        ("Vector 2 [GitHub Issues & PRs]", f"\"{query}\" issue OR pr site:github.com closed fix patch"),
        ("Vector 3 [Real-Time Commit Log]", f"\"{query}\" commit diff refactor site:github.com"),
        ("Vector 4 [Stack Traces & Errors]", f"\"{query}\" error crash stack trace exception solution")
    ]
    
    for name, vquery in vectors:
        print(f"▶ {name}:")
        print(f"  Query: {vquery}\n")
    print("════════════════════════════════════════════════════════════════════")

def main():
    parser = argparse.ArgumentParser(description="Perplexity Multi-Vector Query Decomposer")
    parser.add_argument("query", help="Technical inquiry to decompose")
    args = parser.parse_args()
    decompose(args.query)

if __name__ == "__main__":
    main()

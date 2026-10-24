#!/usr/bin/env python3
"""
Chain-of-Verification & First-Principles Reasoner (verification_reasoner.py)
===========================================================================
Formulates structured Chain-of-Verification (CoVe) questions, performs
pre-mortem adversarial red-teaming, and applies Ockham's Razor hypothesis
ranking to eliminate logical fallacies and confirmation bias in complex reasoning.
"""

import argparse
import json
import sys
from typing import Any, Dict, List


def generate_cove_framework(claim_or_hypothesis: str, domain: str = "software") -> Dict[str, Any]:
    """Generate structured Chain-of-Verification queries for a technical hypothesis."""
    base_questions = [
        f"1. Invariant Check: What fundamental system constraints must hold true for '{claim_or_hypothesis}'?",
        "2. Pre-Mortem Red Team: If this implementation crashes or causes silent data corruption, what was the most probable root cause?",
        "3. Boundary & Edge Conditions: What happens under zero/null input, memory exhaustion, or concurrency race conditions?",
        "4. Ockham's Razor Test: Is there a simpler, lower-complexity mechanism that achieves the exact same functional outcome?",
        "5. Reversibility & Blast Radius: If this hypothesis is proven incorrect, how quickly can the system be rolled back?"
    ]

    return {
        "hypothesis": claim_or_hypothesis,
        "domain": domain,
        "verification_queries": base_questions,
        "evaluation_protocol": [
            "Answer each query independently without confirmation bias.",
            "Verify with executable tests before modifying core architectures.",
            "If any invariant is violated, discard or pivot immediately."
        ]
    }


def rank_hypotheses_ockham(hypotheses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rank debugging hypotheses by Ockham's Razor score:
    Score = (Likelihood 1-10) / (Verification Effort 1-10 * Complexity 1-10)
    High score = test first (cheap to test, high probability).
    """
    for h in hypotheses:
        prob = float(h.get("probability", 5))
        effort = max(1.0, float(h.get("verification_effort", 3)))
        comp = max(1.0, float(h.get("complexity", 3)))
        h["ockham_score"] = round(prob / (effort * comp), 3)

    return sorted(hypotheses, key=lambda x: x["ockham_score"], reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Chain-of-Verification & First-Principles Reasoner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # cove
    cove_p = subparsers.add_parser("cove", help="Generate Chain-of-Verification queries for a proposal")
    cove_p.add_argument("hypothesis", type=str, help="Proposed solution, hypothesis, or design claim")
    cove_p.add_argument("--domain", type=str, default="software", help="Engineering domain")

    # rank
    rank_p = subparsers.add_parser("rank", help="Rank debugging hypotheses via Ockham's Razor")
    rank_p.add_argument("json_file", type=str, help="Path to JSON file containing list of hypotheses")

    args = parser.parse_args()

    if args.command == "cove":
        res = generate_cove_framework(args.hypothesis, domain=args.domain)
        print("🧠 [Chain-of-Verification (CoVe) Protocol]")
        print(f"Hypothesis: \"{res['hypothesis']}\"\n")
        print("Cross-Examination Invariant Queries:")
        for q in res["verification_queries"]:
            print(f"  • {q}")
        print("\nEvaluation Protocol:")
        for p in res["evaluation_protocol"]:
            print(f"  [✓] {p}")

    elif args.command == "rank":
        data = json.loads(open(args.json_file, encoding="utf-8").read())
        ranked = rank_hypotheses_ockham(data)
        print("⚡ [Ockham's Razor Hypothesis Ranking (Test Top First)]")
        for i, h in enumerate(ranked, 1):
            print(f"{i}. [{h['ockham_score']}] {h.get('name', 'Hypothesis')}: Prob={h.get('probability')}, Effort={h.get('verification_effort')}")


if __name__ == "__main__":
    main()

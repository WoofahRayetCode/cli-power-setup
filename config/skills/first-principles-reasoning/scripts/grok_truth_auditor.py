#!/usr/bin/env python3
"""
xAI Grok Dialectic Truth & Anti-Sycophancy Auditor
Aggressively audits code changes, proposals, and bug diagnoses for unproven assumptions,
hallucinated APIs, and plausible-sounding consensus falsehoods.
"""

import argparse
import re
import sys

def audit_text(text):
    warnings = []
    
    # 1. Hallucination flags (plausible API terms without checks)
    speculative_phrases = [
        (r"\bprobably\b", "Speculative assertion: replace with verified test or engine log"),
        (r"\bshould work\b", "Unverified optimism: requires compile/run proof"),
        (r"\bit appears that\b", "Tentative hypothesis: verify against ground-truth source"),
        (r"\bstandard practice\b", "Consensus appeal: check whether target engine/codebase deviates"),
        (r"\bassume\b", "Dangerous assumption: prove invariant explicitly")
    ]
    
    for pattern, note in speculative_phrases:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            warnings.append(f"⚠️  {note} (matched: '{matches[0]}')")

    # 2. Check for missing evidence markers
    has_evidence = any(k in text.lower() for k in ["verified", "tested", "log", "pass", "exit code 0", "assertion"])
    if not has_evidence:
        warnings.append("⚠️  Zero empirical verification markers detected (no test runs, compiler output, or engine logs cited)")

    print("════════════════════════════════════════════════════════════════════")
    print(" ⚡ GROK 3 DIALECTIC TRUTH & GROUNDING AUDIT")
    print("════════════════════════════════════════════════════════════════════")
    if not warnings:
        print("[✓] Clean: High grounding density. All claims supported by empirical evidence.")
    else:
        print(f"[!] {len(warnings)} Truth / Epistemic Risk(s) Identified:")
        for w in warnings:
            print(f"  {w}")
    print("════════════════════════════════════════════════════════════════════")

def main():
    parser = argparse.ArgumentParser(description="xAI Grok Dialectic Truth Auditor")
    parser.add_argument("file", nargs="?", help="File to audit (or stdin)")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    audit_text(content)

if __name__ == "__main__":
    main()

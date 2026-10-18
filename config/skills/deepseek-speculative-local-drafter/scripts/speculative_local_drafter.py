#!/usr/bin/env python3
"""
DeepSeek-V3 Speculative Local Drafter
Offloads candidate diff drafting and boilerplate generation to local Ollama SLMs
(qwen2.5:1.5b / deepseek-r1:1.5b) on host hardware before cloud token expenditure.
"""

import argparse
import json
import subprocess
import sys

def draft_with_ollama(model, prompt):
    print(f"[→] DeepSeek Speculative Drafter: Dispatching prompt to local '{model}'...")
    try:
        res = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        if res.returncode == 0:
            return res.stdout.strip()
        else:
            return f"Error from Ollama: {res.stderr.strip()}"
    except Exception as e:
        return f"Local drafter exception: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="DeepSeek-V3 Speculative Local Drafter")
    parser.add_argument("prompt", help="Code generation or refactoring prompt to draft locally")
    parser.add_argument("--model", default="qwen2.5:1.5b", help="Local Ollama model (default: qwen2.5:1.5b)")
    args = parser.parse_args()

    draft = draft_with_ollama(args.model, args.prompt)
    print("════════════════════════════════════════════════════════════════════")
    print(f" 🤖 SPECULATIVE CANDIDATE DRAFT ({args.model})")
    print("════════════════════════════════════════════════════════════════════")
    print(draft)
    print("════════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    main()

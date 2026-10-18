#!/usr/bin/env python3
"""
DeepSeek-V3 Speculative Local Drafter
Offloads candidate diff drafting and boilerplate generation to local Ollama SLMs
(qwen2.5:1.5b / deepseek-r1:1.5b) on host hardware before cloud token expenditure.
Uses high-performance zero-dependency HTTP REST API directly to localhost:11434.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

OLLAMA_API = "http://127.0.0.1:11434/api/generate"

def draft_with_ollama(model, prompt, temperature=0.2):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 1024
        }
    }
    
    req = urllib.request.Request(
        OLLAMA_API,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                return True, data.get("response", "").strip()
            else:
                return False, f"HTTP {response.status}: {response.read().decode('utf-8')}"
    except urllib.error.URLError as e:
        return False, f"Ollama daemon unreachable at {OLLAMA_API}: {e}"
    except Exception as e:
        return False, f"Local drafter exception: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="DeepSeek-V3 Speculative Local Drafter")
    parser.add_argument("prompt", help="Code generation or refactoring prompt to draft locally")
    parser.add_argument("--model", default="qwen2.5:1.5b", help="Local Ollama model (default: qwen2.5:1.5b)")
    parser.add_argument("--raw", action="store_true", help="Print raw generated text without banner")
    args = parser.parse_args()

    ok, draft = draft_with_ollama(args.model, args.prompt)
    if not ok:
        print(f"[✗] Drafter Error: {draft}", file=sys.stderr)
        sys.exit(1)

    if args.raw:
        print(draft)
    else:
        print("════════════════════════════════════════════════════════════════════")
        print(f" 🤖 SPECULATIVE CANDIDATE DRAFT ({args.model})")
        print("════════════════════════════════════════════════════════════════════")
        print(draft)
        print("════════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    main()

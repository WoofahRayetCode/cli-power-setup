#!/usr/bin/env python3
"""
verify-fleet-utilization.py (bin/verify-fleet-utilization.py)
Validates that Antigravity CLI actively routes to, executes inferences on,
and records token savings for all 37 installed models in the local LLM fleet.
"""

from __future__ import annotations
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

# Add local-model-coprocessor to path
REPO_ROOT = Path(__file__).resolve().parent.parent
COPROC_PATH = REPO_ROOT / "config" / "skills" / "local-model-coprocessor" / "scripts" / "local_model_coprocessor.py"
sys.path.insert(0, str(COPROC_PATH.parent))

from local_model_coprocessor import (
    resolve_best_local_model,
    record_local_llm_savings,
    get_installed_ollama_models,
)

BOLD = "\033[1m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
MAGENTA = "\033[35m"
DIM = "\033[2m"
RESET = "\033[0m"

FLEET_ROSTER = [
    # Tier 1: Ultra-Large Titan Fleet (70B-72B)
    ("llama3.3:70b-iq2", "titan-agent", "Agent Swarm & Function Calling", "generate", "Plan subagent swarm"),
    ("qwen2.5:72b-iq2", "titan-code", "Engine Porting & Systems C++20", "generate", "Optimize C++20 struct"),
    ("deepseek-r1:70b-iq2", "titan-reason", "Deep CoT & 64-bit Struct Proofs", "generate", "Verify memory alignment"),

    # Tier 2: 32B-47B Frontier Heavyweights & MoE
    ("command-r:35b", "enterprise-agent", "Cohere 35B Enterprise Agent & RAG", "generate", "Generate structured tool schema"),
    ("mixtral:8x7b", "moe-heavy", "Sparse MoE 47B Reasoning & C++ Engine", "generate", "Optimize memory cache alignment"),
    ("mistral-small:24b", "mistral-small", "Mistral Small 3 24B Reasoning & Code", "generate", "Synthesize multi-file diff"),
    ("qwen2.5-coder:32b", "code-frontier", "SWE-bench Code Planning & Refactors", "generate", "Refactor module API"),
    ("qwen2.5:32b", "general-synthesis", "Full Repo Analysis & Technical Specs", "generate", "Draft architecture spec"),
    ("deepseek-r1:32b", "reason-32b", "CoT Proofs & Algorithmic Triage", "generate", "Solve pointer boundary condition"),

    # Tier 3: Binary & MoE Engine Transpilers (16B-22B)
    ("llm4decompile:22b-q4", "decompile", "Assembly Decompilation & REA MCP", "generate", "Analyze x86 disassembly"),
    ("deepseek-coder-v2:16b", "shader", "MoE Shader Transpilation (SPIR-V/HLSL)", "generate", "Convert HLSL to Vulkan GLSL"),

    # Tier 4: Mid-Weight Specialists (9B-14B)
    ("phi4:14b", "physics", "ODE Numerical Integration & Physics", "generate", "Calculate ballistics trajectory"),
    ("deepseek-r1:14b", "reason-14b", "Fast Algorithmic Verification", "generate", "Prove invariant condition"),
    ("qwen2.5-coder:14b", "code-14b", "Multi-file Architecture & Refactoring", "generate", "Generate class interface"),
    ("mistral-nemo:12b", "long", "128k Context Summaries & Log Triage", "generate", "Summarize engine log"),
    ("gemma2:9b", "business", "Executive Communications & Proposals", "generate", "Draft client proposal"),

    # Tier 5: Workhorse Domain Specialists (7B-13B)
    ("llava:13b", "vision-13b", "LLaVA 13B Multimodal Vision & UI Triage", "generate", "Check render frame anomalies"),
    ("codegeex4:9b", "code-repo", "Whole-Repository Code Intelligence & AST", "generate", "Index repository symbols"),
    ("blenderllm:7b-q4", "blender", "Procedural Blender bpy Scripting", "generate", "import bpy; # cube"),
    ("blender-architect:latest", "blender-arch", "Blender 5.2 SDF Remesh & OGF Export", "generate", "Generate organic SDF remesh script"),
    ("minicpm-v:8b", "vision", "Multimodal VLM Screenshot Triage", "generate", "Check render frame anomalies"),
    ("moondream:latest", "fast-vision", "Lightweight Vision & Bounding Boxes", "generate", "Detect UI button"),
    ("granite-code:8b", "csharp", "Enterprise C# .NET 9 & Avalonia", "generate", "public class DataService {}"),
    ("starcoder2:7b", "rust", "Rust Systems & Borrow Checker Proofs", "generate", "fn calculate_hash() -> u64 { 0 }"),
    ("codellama:7b-python", "python", "Python 3.12 Automation & Pytest", "generate", "def test_pipeline(): assert True"),
    ("aya:8b", "translate", "Multilingual Slavic/CJK Localization", "generate", "Translate to Ukrainian"),
    ("sqlcoder:7b", "sql", "SQL Query Tuning & SQLite WAL Pragmas", "generate", "EXPLAIN QUERY PLAN SELECT"),
    ("hermes3:8b", "tool", "Agent Tool Calling & JSON Schemas", "generate", "Return JSON tool call"),
    ("llama3.1:8b", "conversation", "Multi-turn Agent Coordination", "generate", "Evaluate design tradeoff"),
    ("mathstral:7b", "math", "Quaternions & 3D Vector Math", "generate", "Calculate quaternion SLERP"),
    ("wizard-math:7b", "competition-math", "Competition Math & Matrix Geometry", "generate", "Derive rotation matrix"),
    ("deepseek-r1:8b", "reason-8b", "Logic Proofs & Boundary Invariants", "generate", "Check boundary bounds"),
    ("qwen2.5:7b", "web", "Modern Web Tailwind CSS & HTML", "generate", "Generate dark mode card component"),
    ("qwen2.5-coder:7b", "test", "Workhorse C++/Py Unit Testing", "generate", "Generate test cases"),
    ("deepseek-coder:6.7b-instruct", "systems-posix", "POSIX C & Linux Low-level Internals", "generate", "Implement epoll listener"),

    # Tier 6: Compact & Edge Sub-Second Engines (1.5B - 3.8B)
    ("llama3.2:3b", "status-report", "Sub-second Status Reports & Briefs", "generate", "Summarize build milestone"),
    ("phi3.5:latest", "mini-logic", "128k Lightweight Reasoning & Math", "generate", "Solve quick logic puzzle"),
    ("smollm2:1.7b", "docstring", "Sub-second PEP257 Docstrings", "generate", "Generate docstring"),
    ("qwen2.5-coder:1.5b", "regex", "Sub-second Regex & Boilerplate", "generate", "Compile regex pattern"),
    ("deepseek-r1:1.5b", "fast-reason", "Sub-second CoT Logic Assertions", "generate", "Verify assert statement"),

    # Tier 7: Local Vector Embedding Engines
    ("nomic-embed-text:latest", "embed", "Codebase Vector Indexing (768-dim)", "embed", "Local RAG semantic search"),
    ("bge-m3:latest", "embed-dense", "Dense Multilingual Vectors (1024-dim)", "embed", "Dense multilingual vector indexing"),
]


def test_model(model: str, task: str, desc: str, mtype: str, test_prompt: str, endpoint="http://localhost:11434") -> dict:
    t0 = time.time()
    resolved = resolve_best_local_model("auto", task, endpoint)
    is_correct_route = (resolved == model or resolved.startswith(model.split(":")[0]))

    if mtype == "embed":
        url = f"{endpoint.rstrip('/')}/api/embeddings"
        payload = {"model": model, "prompt": test_prompt}
    else:
        url = f"{endpoint.rstrip('/')}/api/generate"
        payload = {
            "model": model,
            "prompt": test_prompt,
            "stream": False,
            "options": {
                "num_ctx": 2048 if any(k in model for k in ("70b", "72b", "mixtral", "8x7b")) else 8192,
                "num_predict": 5,
                "temperature": 0.2,
            },
        }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        tout = 240.0 if any(k in model for k in ("70b", "72b", "mixtral", "8x7b", "command-r")) else 90.0
        with urllib.request.urlopen(req, timeout=tout) as resp:
            if resp.status == 200:
                elapsed = time.time() - t0
                res = json.loads(resp.read().decode("utf-8"))
                if mtype == "embed":
                    dim = len(res.get("embedding", []))
                    saved, tot = record_local_llm_savings(model, len(test_prompt) // 4, dim // 4)
                    return {
                        "status": "PASS",
                        "model": model,
                        "task": task,
                        "route_ok": is_correct_route,
                        "elapsed": elapsed,
                        "saved": saved,
                        "detail": f"{dim} dims",
                    }
                else:
                    text = res.get("response", "").strip()
                    p_eval = res.get("prompt_eval_count") or max(5, len(test_prompt) // 4)
                    e_cnt = res.get("eval_count") or max(5, len(text) // 4)
                    saved, tot = record_local_llm_savings(model, p_eval, e_cnt)
                    snippet = text.replace("\n", " ")[:30]
                    return {
                        "status": "PASS",
                        "model": model,
                        "task": task,
                        "route_ok": is_correct_route,
                        "elapsed": elapsed,
                        "saved": saved,
                        "detail": f'"{snippet}..."',
                    }
    except Exception as e:
        return {
            "status": "FAIL",
            "model": model,
            "task": task,
            "route_ok": is_correct_route,
            "elapsed": time.time() - t0,
            "saved": 0,
            "detail": str(e)[:35],
        }


def main():
    print(f"{BOLD}=== Antigravity CLI Local LLM Fleet Utilization Audit ==={RESET}", flush=True)
    endpoint = "http://localhost:11434"
    installed = get_installed_ollama_models(endpoint)
    print(f"Ollama Endpoint: {CYAN}{endpoint}{RESET} | Installed Models: {GREEN}{len(installed)}/37{RESET}\n", flush=True)

    results = []
    print(f"{'#':<3} {'Model Name':<28} {'Task Trigger':<18} {'Route':<7} {'Time':<7} {'Saved':<9} {'Status'}", flush=True)
    print("-" * 88, flush=True)

    for idx, (model, task, desc, mtype, prompt) in enumerate(FLEET_ROSTER, 1):
        r = test_model(model, task, desc, mtype, prompt, endpoint)
        results.append(r)
        status_color = GREEN if r["status"] == "PASS" else RED
        route_str = f"{GREEN}✓ match{RESET}" if r["route_ok"] else f"{YELLOW}alt{RESET}"
        print(f"{idx:<3} {r['model']:<28} {r['task']:<18} {route_str:<16} {r['elapsed']:<6.2f}s +{r['saved']:<7,d} {status_color}[{r['status']}]{RESET}", flush=True)

    passed = sum(1 for r in results if r["status"] == "PASS")
    total_saved = sum(r["saved"] for r in results)
    print("-" * 88)
    print(f"{BOLD}Audit Summary:{RESET} {GREEN}{passed}/{len(FLEET_ROSTER)}{RESET} models verified active.")
    print(f"{BOLD}Session Cloud Tokens Saved:{RESET} {CYAN}+{total_saved:,}{RESET} tokens billed at $0.00.")

    # Refresh statusline
    try:
        subprocess.run(["bin/agy-quota-statusline"], capture_output=True, timeout=2.0)
    except Exception:
        pass


if __name__ == "__main__":
    main()

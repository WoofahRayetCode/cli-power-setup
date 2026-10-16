#!/usr/bin/env python3
"""
Adaptive Model & Reasoning Router (adaptive_model_router.py)
Dynamically escalates cognitive effort and model tiers based on task difficulty,
consecutive failure signatures, and crash diagnostics to prevent trial-and-error thrashing.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_STATE_FILE = Path(".agents/memory/adaptive_reasoning_state.json")

def get_state_file(custom_path=None) -> Path:
    p = Path(custom_path) if custom_path else DEFAULT_STATE_FILE
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def load_state(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "updated_at": datetime.now().isoformat(),
        "tasks": {},
        "current_tier": 1,
        "active_model": "flash",
        "reasoning_effort": "low"
    }

def save_state(path: Path, state: dict):
    state["updated_at"] = datetime.now().isoformat()
    path.write_text(json.dumps(state, indent=2), encoding="utf-8")

def calculate_difficulty_score(error_text: str, attempts: int = 0) -> dict:
    """
    Computes a difficulty score (0-100) based on error signatures and attempt count.
    """
    score = 10
    factors = []
    
    if not error_text:
        return {
            "score": score,
            "tier": 1,
            "model": "flash",
            "reasoning": "low",
            "strategy": "Direct surgical diffs",
            "factors": ["Standard execution"]
        }

    err_lower = error_text.lower()
    
    # 1. Fatal errors, crashes, and memory safety (High Impact)
    if any(k in err_lower for k in ["fatal error", "segfault", "segmentation fault", "core dumped", "access violation", "nullpointer", "panic", "bugtrap"]):
        score += 45
        factors.append("Fatal crash / memory violation detected (+45)")
        
    # 2. Concurrency, race conditions, deadlocks
    if any(k in err_lower for k in ["deadlock", "race condition", "timeout", "blocking call", "thread starvation"]):
        score += 35
        factors.append("Concurrency / synchronization hazard (+35)")

    # 3. Shader / Graphics API compilation errors
    if any(k in err_lower for k in ["spirv", "glslang", "e_fail", "d3d11", "d3d12", "shader compile", "vk_error"]):
        score += 30
        factors.append("Graphics API / Shader compilation failure (+30)")

    # 4. Linker, undefined reference, missing symbol
    if any(k in err_lower for k in ["undefined reference", "unresolved external", "symbol not found", "cannot find module"]):
        score += 25
        factors.append("Linker / symbol resolution failure (+25)")

    # 5. Simple syntax errors (Low Impact, easily solvable locally)
    if any(k in err_lower for k in ["syntaxerror", "unexpected token", "indentationerror", "semicolon expected"]):
        score += 10
        factors.append("Syntax error (+10)")

    # 6. Consecutive retry penalty
    if attempts > 0:
        penalty = min(attempts * 25, 50)
        score += penalty
        factors.append(f"Retry penalty ({attempts} prior failed attempt(s): +{penalty})")

    score = min(score, 100)

    # Determine Tier & Escalation Threshold
    if score >= 70 or attempts >= 2:
        tier = 3
        model = "pro"
        reasoning = "high"
        strategy = "Tree-of-Thought (deliberative-reasoning-tree) + Pro/Argon Subagent"
    elif score >= 35 or attempts == 1:
        tier = 2
        model = "flash"
        reasoning = "medium"
        strategy = "Systematic root-cause diagnosis (systematic-debugging) + AST analysis"
    else:
        tier = 1
        model = "flash"
        reasoning = "low"
        strategy = "Fast pinpoint edit (replace_file_content) with low latency"

    return {
        "score": score,
        "tier": tier,
        "model": model,
        "reasoning": reasoning,
        "strategy": strategy,
        "factors": factors
    }

def cmd_route(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    
    task_id = args.task or "active_task"
    task_info = state["tasks"].get(task_id, {"attempts": 0, "last_error": ""})
    
    attempts = args.attempts if args.attempts is not None else task_info.get("attempts", 0)
    error_text = args.error or task_info.get("last_error", "")
    
    assessment = calculate_difficulty_score(error_text, attempts=attempts)
    
    if args.json:
        result = {
            "task": task_id,
            "attempts": attempts,
            "difficulty_assessment": assessment,
            "recommended_subagent": {
                "TypeName": "research" if assessment["tier"] == 3 else "self",
                "Model": assessment["model"],
                "Role": "Deep Architectural Debugger" if assessment["tier"] == 3 else "Standard Engineer"
            }
        }
        print(json.dumps(result, indent=2))
        return

    print("\n=======================================================")
    print(" 🧠 Adaptive Model & Reasoning Complexity Router       ")
    print("=======================================================")
    print(f"Task Identifier:    {task_id}")
    print(f"Prior Failed Tries: {attempts}")
    print(f"Difficulty Score:   {assessment['score']}/100")
    print(f"Cognitive Tier:     Tier {assessment['tier']} ({'Deep Architectural' if assessment['tier'] == 3 else 'Standard' if assessment['tier'] == 2 else 'Trivial'})")
    print("-------------------------------------------------------")
    print(f"Recommended Model:  {assessment['model'].upper()} ({'Gemini 4 Argon / Pro Tier' if assessment['model'] == 'pro' else 'Gemini 3.8 Flash / Turbo'})")
    print(f"Reasoning Depth:    {assessment['reasoning'].upper()}")
    print(f"Execution Strategy: {assessment['strategy']}")
    print("-------------------------------------------------------")
    print("Diagnostic Factors:")
    for f in assessment["factors"]:
        print(f"  • {f}")
    
    if assessment["tier"] == 3:
        print("\n⚡ [ESCALATION ACTION MANDATE]:")
        print("  1. Do NOT make further random guesses or blind code modifications.")
        print("  2. Activate 'deliberative-reasoning-tree' to red-team 3 hypothesis branches.")
        print(f"  3. Dispatch subagent with Model=\"pro\" for deep architectural triage:")
        print(f"     invoke_subagent(Subagents=[{{'TypeName': 'self', 'Model': 'pro', 'Role': 'Deep Debugger', 'Prompt': '...'}}])")
    print("=======================================================\n")

def cmd_fail(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    
    task_id = args.task or "active_task"
    task_record = state["tasks"].setdefault(task_id, {"attempts": 0, "failures": []})
    task_record["attempts"] += 1
    
    fail_entry = {
        "timestamp": datetime.now().isoformat(),
        "reason": args.reason or "Unknown failure"
    }
    task_record["failures"].append(fail_entry)
    task_record["last_error"] = args.reason or ""
    
    assessment = calculate_difficulty_score(task_record["last_error"], attempts=task_record["attempts"])
    state["current_tier"] = assessment["tier"]
    state["active_model"] = assessment["model"]
    state["reasoning_effort"] = assessment["reasoning"]
    
    save_state(path, state)
    
    print(f"\n[⚠️ TASK DIFFICULTY REGISTERED]: '{task_id}' failed (Attempt #{task_record['attempts']}).")
    print(f"  -> Cognitive Tier Escalated to: Tier {assessment['tier']} (Model: {assessment['model'].upper()} | Reasoning: {assessment['reasoning'].upper()})")
    print(f"  -> Strategy: {assessment['strategy']}\n")

def cmd_pass(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    
    task_id = args.task or "active_task"
    if task_id in state["tasks"]:
        del state["tasks"][task_id]
        
    state["current_tier"] = 1
    state["active_model"] = "flash"
    state["reasoning_effort"] = "low"
    
    save_state(path, state)
    
    print(f"\n[✓ TASK RESOLVED]: '{task_id}' verified passing.")
    print("  -> De-escalating Cognitive Tier to: Tier 1 (Model: FLASH | Reasoning: LOW).")
    print("  -> Maximum quota preservation active.\n")

def cmd_status(args):
    path = get_state_file(args.state_file)
    state = load_state(path)
    
    print("\n=======================================================")
    print(" 📊 Adaptive Reasoning & Model Router Status          ")
    print("=======================================================")
    print(f"Active Model:       {state.get('active_model', 'flash').upper()}")
    print(f"Reasoning Effort:   {state.get('reasoning_effort', 'low').upper()}")
    print(f"Cognitive Tier:     Tier {state.get('current_tier', 1)}")
    print(f"Tracked Tasks:      {len(state.get('tasks', {}))}")
    for tid, rec in state.get("tasks", {}).items():
        print(f"  - {tid}: {rec.get('attempts', 0)} failed attempt(s) | Last: {rec.get('last_error', 'N/A')[:60]}")
    print("=======================================================\n")

def evaluate_plan_complexity(plan_text: str) -> dict:
    score = 15
    factors = []
    text_lower = plan_text.lower()

    # Step count analysis
    task_matches = re.findall(r"(?:^|\n)\s*(?:-\s*\[\s*\]|\d+\.\s+|###?\s*(?:Step|Task|Phase))", plan_text)
    task_count = max(len(task_matches), 1)
    if task_count >= 8:
        score += 25
        factors.append(f"Large multi-step plan ({task_count} tasks, +25)")
    elif task_count >= 4:
        score += 15
        factors.append(f"Multi-phase plan ({task_count} tasks, +15)")

    # Deep architectural triggers
    tier3_keywords = [
        ("reverse engineer", 30), ("decompil", 30), ("kernel", 35), ("acpi", 35),
        ("vulkan", 25), ("directx", 25), ("dx11", 20), ("dx12", 25), ("shader", 20),
        ("memory allocator", 30), ("concurrency", 25), ("multithread", 20),
        ("anti-cheat", 25), ("detour hook", 30), ("dll proxy", 25), ("cryptograph", 25),
        ("x-ray", 20), ("ogsr", 20), ("assembly", 30), ("mips", 30), ("powerpc", 30)
    ]
    for kw, pts in tier3_keywords:
        if kw in text_lower:
            score += pts
            factors.append(f"High-complexity domain '{kw}' (+{pts})")
            break

    # Standard engineering triggers
    tier2_keywords = [
        ("refactor", 15), ("unit test", 10), ("migration", 15), ("database", 15),
        ("sqlite", 10), ("room", 10), ("compose", 10), ("api", 10), ("parser", 15)
    ]
    for kw, pts in tier2_keywords:
        if kw in text_lower:
            score += pts
            factors.append(f"Core engineering pattern '{kw}' (+{pts})")
            break

    score = min(100, score)

    if score >= 50:
        tier = 3
        model_gemini = "gemini-4-argon-high"
        model_claude = "claude-sonnet-5-5-high"
        effort = "high"
        strategy = "Architect on Argon High / Sonnet High; execute granular code diffs surgically"
    elif score >= 25:
        tier = 2
        model_gemini = "gemini-4-argon-medium"
        model_claude = "claude-sonnet-5-5-medium"
        effort = "medium"
        strategy = "Standard engineering execution on Argon Medium / Sonnet Medium with compiler verification"
    else:
        tier = 1
        model_gemini = "gemini-3.8-flash-low"
        model_claude = "claude-sonnet-5-5-low"
        effort = "low"
        strategy = "Instant-speed execution on Flash Low / Sonnet Low with low reasoning overhead"

    return {
        "score": score,
        "tier": tier,
        "task_count": task_count,
        "recommended_model_gemini": model_gemini,
        "recommended_model_claude": model_claude,
        "reasoning_effort": effort,
        "strategy": strategy,
        "factors": factors
    }

def cmd_plan(args):
    plan_text = ""
    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            plan_text = f.read()
    elif args.text:
        plan_text = args.text
    else:
        if not sys.stdin.isatty():
            plan_text = sys.stdin.read()

    if not plan_text.strip():
        print("Error: No plan text provided. Specify --file <path>, --text '<plan>', or pipe via stdin.")
        sys.exit(1)

    eval_res = evaluate_plan_complexity(plan_text)

    if args.json:
        print(json.dumps(eval_res, indent=2))
        return

    tier_label = "Deep Architectural (Tier 3)" if eval_res["tier"] == 3 else "Standard Engineering (Tier 2)" if eval_res["tier"] == 2 else "Trivial / Direct (Tier 1)"

    print("\n=======================================================")
    print(" 📋 Pre-Execution Plan Model & Reasoning Recommender   ")
    print("=======================================================")
    print(f"Plan Tasks Detected:  {eval_res['task_count']}")
    print(f"Complexity Score:     {eval_res['score']}/100 -> {tier_label}")
    print("-------------------------------------------------------")
    print(f"Recommended (Gemini): {eval_res['recommended_model_gemini']}")
    print(f"Recommended (Claude): {eval_res['recommended_model_claude']}")
    print(f"Recommended Effort:   --effort {eval_res['reasoning_effort']}")
    print(f"Execution Strategy:   {eval_res['strategy']}")
    print("-------------------------------------------------------")
    print("Identified Complexity Factors:")
    for f in eval_res["factors"]:
        print(f"  • {f}")
    print("-------------------------------------------------------")
    print("Suggested CLI Launch Command:")
    print(f"  agy --model {eval_res['recommended_model_gemini']} --effort {eval_res['reasoning_effort']}")
    print("=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="Adaptive Model & Reasoning Router")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # plan
    p_plan = subparsers.add_parser("plan", help="Analyze plan complexity and recommend optimal model and reasoning depth")
    p_plan.add_argument("--file", help="Path to markdown plan file")
    p_plan.add_argument("--text", help="Plan text string")
    p_plan.add_argument("--json", action="store_true", help="Output assessment as JSON")

    # route
    p_route = subparsers.add_parser("route", help="Evaluate task difficulty and recommend model/reasoning tier")
    p_route.add_argument("--task", help="Task identifier")
    p_route.add_argument("--error", help="Error log text or failure reason")
    p_route.add_argument("--attempts", type=int, help="Number of consecutive failed attempts")
    p_route.add_argument("--json", action="store_true", help="Output assessment as JSON")
    p_route.add_argument("--state-file", help="Path to state file")

    # fail
    p_fail = subparsers.add_parser("fail", help="Record task failure and trigger cognitive escalation")
    p_fail.add_argument("--task", required=True, help="Task identifier")
    p_fail.add_argument("--reason", required=True, help="Error message or failure reason")
    p_fail.add_argument("--state-file", help="Path to state file")

    # pass
    p_pass = subparsers.add_parser("pass", help="Record task success and de-escalate back to Flash")
    p_pass.add_argument("--task", required=True, help="Task identifier")
    p_pass.add_argument("--state-file", help="Path to state file")

    # status
    p_stat = subparsers.add_parser("status", help="Show current router status and cognitive tier")
    p_stat.add_argument("--state-file", help="Path to state file")

    args = parser.parse_args()

    if args.command == "plan":
        cmd_plan(args)
    elif args.command == "route":
        cmd_route(args)
    elif args.command == "fail":
        cmd_fail(args)
    elif args.command == "pass":
        cmd_pass(args)
    elif args.command == "status":
        cmd_status(args)

if __name__ == "__main__":
    main()

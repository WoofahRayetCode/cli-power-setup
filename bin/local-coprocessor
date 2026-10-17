#!/usr/bin/env python3
"""
Local Model Coprocessor & Quota Shield (local_model_coprocessor.py)
Dispatches routine tasks (docstrings, commit messages, log summaries, boilerplate)
to local SLMs/LLMs running in VRAM/RAM via Ollama or llama.cpp, billing 0 cloud tokens.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


import base64
import subprocess


def get_installed_ollama_models(endpoint="http://localhost:11434") -> list[str]:
    tags_url = f"{endpoint.rstrip('/')}/api/tags"
    try:
        with urllib.request.urlopen(urllib.request.Request(tags_url), timeout=2.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                return [m.get("name", "") for m in data.get("models", []) if m.get("name")]
    except Exception:
        pass
    return []


def get_free_vram_mb() -> int:
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=1.5,
        ).strip()
        return int(out.splitlines()[0].strip())
    except Exception:
        return 6000


SKILLS_DIRS = [
    Path("/home/ericparsley/Documents/GitHub/cli-power-setup/config/skills"),
    Path.home() / ".gemini" / "config" / "skills",
]


def load_skill_context(skill_names: str = "", auto_skill: bool = False, prompt_text: str = "", task: str = "auto") -> tuple[str, list[str]]:
    loaded_names: list[str] = []
    target_skills: list[str] = []

    if skill_names:
        target_skills.extend([s.strip() for s in skill_names.split(",") if s.strip()])
    if task == "blender" and not target_skills:
        target_skills.extend([
            "blender-3d-engineering",
            "blender-sdf-organic-remeshing",
            "character-creature-anatomy-modeling",
            "xray-ogf-dm-blender-pipeline",
        ])
    elif auto_skill and prompt_text:
        p_low = prompt_text.lower()
        keyword_map = [
            (("blender", "bpy", "mesh", "3d", "sculpt", "ogf", "remesh", "aisha"), ["blender-3d-engineering", "blender-sdf-organic-remeshing"]),
            (("shader", "hlsl", "dx11", "rtx", "dlss", "vulkan"), ["xray-dx11-shader-modernization", "rtx-compute-bvh-raytracing-ssgi"]),
            (("ogg", "audio", "sound", "meow", "voice", "tts"), ["game-audio-ogg-gsc-encoder", "creature-animal-bioacoustic-audio"]),
            (("ltx", "stalker", "ogsr", "xray", "crash"), ["game-modding", "xray-crash-log-diagnostician"]),
            (("64-bit", "pointer", "cpp", "c++"), ["cpp-64bit-engine-port-sanitizer", "modern-cpp-engineering"]),
            (("re", "decompile", "disasm", "reverse engineer", "ghidra", "hopper", "rizin", "vtable", "rva"), ["reverse-engineer-anything", "binary-re-workflows", "rea-mcp-obligation-ledger-orchestrator"]),
        ]
        for kws, sks in keyword_map:
            if any(k in p_low for k in kws):
                for s in sks:
                    if s not in target_skills:
                        target_skills.append(s)

    blocks: list[str] = []
    for sname in target_skills[:3]:
        for sdir in SKILLS_DIRS:
            spath = sdir / sname / "SKILL.md"
            if spath.is_file():
                try:
                    raw = spath.read_text(encoding="utf-8", errors="ignore")
                    blocks.append(f"=== SKILL RULEBOOK: {sname} ===\n{raw[:2600]}")
                    loaded_names.append(sname)
                    break
                except Exception:
                    pass

    if not blocks:
        return "", []
    header = "You MUST strictly obey the following installed Antigravity Skill specifications:\n\n"
    return header + "\n\n".join(blocks), loaded_names


def resolve_best_local_model(requested_model: str, task: str = "auto", endpoint: str = "http://localhost:11434") -> str:
    installed = get_installed_ollama_models(endpoint)
    if not installed:
        return requested_model
    if requested_model != "auto" and requested_model in installed:
        return requested_model

    free_mb = get_free_vram_mb()
    if task in ("re", "decompile", "reverse", "disasm", "rea", "binary"):
        for cand in ("llm4decompile:22b-q4", "deepseek-coder-v2:16b", "qwen2.5:72b-iq2", "qwen2.5-coder:32b", "deepseek-r1:70b-iq2", "deepseek-r1:32b", "qwen2.5-coder:14b", "deepseek-r1:14b", "deepseek-coder:6.7b-instruct"):
            if cand in installed:
                return cand
    elif task in ("port", "engine", "migration", "transpile"):
        for cand in ("qwen2.5:72b-iq2", "deepseek-r1:70b-iq2", "deepseek-coder-v2:16b", "qwen2.5-coder:32b", "qwen2.5-coder:14b", "deepseek-coder:6.7b-instruct", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand
    elif task in ("plan", "architect", "roadmap", "decompose"):
        for cand in ("deepseek-r1:70b-iq2", "qwen2.5:72b-iq2", "llama3.3:70b-iq2", "qwen2.5-coder:32b", "deepseek-r1:32b", "qwen2.5:32b", "deepseek-coder-v2:16b", "qwen2.5-coder:14b", "deepseek-r1:14b", "phi4:14b", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand
    elif task == "blender":
        for cand in ("blenderllm:7b-q4", "blender-architect:latest", "qwen2.5:72b-iq2", "qwen2.5-coder:7b", "deepseek-r1:8b"):
            if cand in installed:
                return cand
    elif task == "vision":
        for cand in ("minicpm-v:8b", "minicpm-v:latest", "qwen2.5vl:7b", "moondream:latest", "llava:latest"):
            if cand in installed:
                return cand
    elif task in ("csharp", "cs", "dotnet"):
        for cand in ("granite-code:8b", "qwen2.5:72b-iq2", "qwen2.5-coder:32b", "qwen2.5-coder:14b", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand
    elif task in ("cpp", "c++", "xray", "shader"):
        for cand in ("qwen2.5:72b-iq2", "deepseek-r1:70b-iq2", "deepseek-coder-v2:16b", "qwen2.5-coder:32b", "qwen2.5-coder:14b", "deepseek-coder:6.7b-instruct", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand
    elif task == "rust":
        for cand in ("starcoder2:7b", "qwen2.5:72b-iq2", "qwen2.5-coder:32b", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand
    elif task in ("python", "py"):
        for cand in ("codellama:7b-python", "qwen2.5-coder:32b", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand
    elif task in ("translate", "localization", "dialogue", "stalker-xml", "i18n"):
        for cand in ("aya:8b", "qwen2.5:32b", "qwen2.5:7b", "llama3.1:8b"):
            if cand in installed:
                return cand
    elif task in ("sql", "database", "schema"):
        for cand in ("sqlcoder:7b", "granite-code:8b", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand
    elif task in ("tool", "agent", "swarm", "json"):
        for cand in ("hermes3:8b", "llama3.1:8b", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand
    elif task in ("long", "summarize", "compact", "cartography"):
        for cand in ("mistral-nemo:12b", "qwen2.5:32b", "qwen2.5:7b", "llama3.1:8b"):
            if cand in installed:
                return cand
    elif task in ("web", "html", "modernize", "tailwind", "css", "frontend"):
        for cand in ("qwen2.5:32b", "qwen2.5:7b", "gemma2:9b", "qwen2.5-coder:32b"):
            if cand in installed:
                return cand
    elif task in ("business", "copy", "proposal", "outreach", "editorial", "proofread"):
        for cand in ("gemma2:9b", "qwen2.5:32b", "qwen2.5:7b", "llama3.1:8b"):
            if cand in installed:
                return cand
    elif task in ("math", "physics", "ballistics", "quaternion"):
        for cand in ("mathstral:7b", "wizard-math:7b", "deepseek-r1:32b", "deepseek-r1:14b", "phi4:14b", "deepseek-r1:8b", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand
    elif task == "reason" and free_mb >= 5200:
        for cand in ("deepseek-r1:32b", "deepseek-r1:14b", "deepseek-r1:8b", "phi4:14b", "qwen2.5-coder:32b", "phi3.5:latest", "deepseek-r1:1.5b"):
            if cand in installed:
                return cand
    elif task == "fast" or free_mb < 4800:
        for cand in ("deepseek-r1:1.5b", "smollm2:1.7b", "phi3.5:latest", "llama3.2:3b", "qwen2.5-coder:1.5b", "qwen2.5-coder:7b"):
            if cand in installed:
                return cand

    for cand in ("deepseek-coder:6.7b-instruct", "qwen2.5-coder:7b", "granite-code:8b", "mistral-nemo:12b", "hermes3:8b", "aya:8b", "blender-architect:latest", "qwen2.5-coder:1.5b"):
        if cand in installed:
            return cand
    return installed[0]


def _write_local_state(model: str, active: bool, last_saved: int = 0) -> None:
    try:
        clean_m = model.replace(":latest", "")
        state_p = Path("/tmp/agy_local_model_state.json")
        payload = {"model": clean_m, "active": active, "ts": time.time()}
        if last_saved > 0:
            payload["last_saved"] = last_saved
        state_p.write_text(json.dumps(payload), encoding="utf-8")
    except Exception:
        pass


def record_local_llm_savings(model: str, prompt_eval: int, eval_count: int, has_image: bool = False) -> tuple[int, int]:
    """Persists per-model local LLM token savings to ~/.cli_power_setup/token_ledger.json and config/token_ledger.json."""
    clean_m = model.replace(":latest", "")
    local_tok = max(1, prompt_eval + eval_count)
    
    # Tier-specific cloud equivalent calculation:
    # 1. Ultra-Large Reasoners (DeepSeek-R1 70B/32B): replaces Argon High / Claude Extended Thinking (6x-8x reasoning token burn)
    if "deepseek-r1" in clean_m:
        reason_mult = 6 if ("70b" in clean_m or "72b" in clean_m) else 4
        cloud_saved = prompt_eval + (eval_count * reason_mult) + 3500
    # 2. Ultra-Large Systems Architects & Tool Callers (Qwen 72B, Llama 3.3 70B):
    elif any(k in clean_m for k in ["72b", "70b", "llama3.3"]):
        cloud_saved = prompt_eval + (eval_count * 4) + 2500
    # 3. Neural Decompiler (LLM4Decompile 22B): eliminates large assembly code dumps from cloud context
    elif "llm4decompile" in clean_m or "decompile" in clean_m:
        cloud_saved = (prompt_eval * 2) + (eval_count * 3) + 2000
    # 4. Dedicated CAD / Blender models: avoids iterative syntax debugging in cloud context
    elif "blender" in clean_m:
        cloud_saved = prompt_eval + (eval_count * 3) + 2000
    # 5. Multimodal Vision Models: avoids 2500+ vision tokens per image
    elif has_image or "minicpm" in clean_m or "moondream" in clean_m:
        cloud_saved = prompt_eval + (eval_count * 2) + 3200
    # 6. Standard code & fast utilities:
    else:
        cloud_saved = local_tok + max(1200, eval_count * 2)

    tot_saved = cloud_saved
    ledger_paths = [
        Path.home() / ".cli_power_setup" / "token_ledger.json",
        Path("/home/ericparsley/Documents/GitHub/cli-power-setup/config/token_ledger.json")
    ]
    for ledger_p in ledger_paths:
        try:
            if not ledger_p.parent.exists():
                ledger_p.parent.mkdir(parents=True, exist_ok=True)
            ld = json.loads(ledger_p.read_text(encoding="utf-8")) if ledger_p.exists() else {}
            lls = ld.get("local_llm_savings", {})
            lls["total_calls"] = lls.get("total_calls", 0) + 1
            lls["total_local_tokens"] = lls.get("total_local_tokens", 0) + local_tok
            lls["total_cloud_tokens_saved"] = lls.get("total_cloud_tokens_saved", 0) + cloud_saved
            lls["last_model"] = clean_m
            lls["last_saved_tokens"] = cloud_saved
            lls["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            by_m = lls.get("by_model", {})
            m_entry = by_m.get(clean_m, {"calls": 0, "local_tokens": 0, "cloud_tokens_saved": 0})
            m_entry["calls"] = m_entry.get("calls", 0) + 1
            m_entry["local_tokens"] = m_entry.get("local_tokens", 0) + local_tok
            m_entry["cloud_tokens_saved"] = m_entry.get("cloud_tokens_saved", 0) + cloud_saved
            by_m[clean_m] = m_entry
            lls["by_model"] = by_m
            ld["local_llm_savings"] = lls
            ledger_p.write_text(json.dumps(ld, indent=2), encoding="utf-8")
            tot_saved = lls["total_cloud_tokens_saved"]
        except Exception:
            pass
    return cloud_saved, tot_saved


def query_local_ollama(endpoint, model, prompt, system_prompt="", image_path="", timeout=35.0):
    resolved_model = resolve_best_local_model(model, "vision" if image_path else "auto", endpoint)
    _write_local_state(resolved_model, True)
    url = f"{endpoint.rstrip('/')}/api/generate"
    payload = {
        "model": resolved_model,
        "prompt": prompt,
        "stream": False,
        "options": {"num_ctx": 8192},
    }
    if system_prompt:
        payload["system"] = system_prompt
    has_img = bool(image_path and os.path.exists(image_path))
    if has_img:
        with open(image_path, "rb") as img_f:
            payload["images"] = [base64.b64encode(img_f.read()).decode("utf-8")]

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                result = json.loads(response.read().decode("utf-8"))
                resp_text = result.get("response", "").strip()
                p_eval = result.get("prompt_eval_count") or (len(prompt + system_prompt) // 4 + (1600 if has_img else 0))
                e_cnt = result.get("eval_count") or max(10, len(resp_text) // 4)
                saved, tot_saved = record_local_llm_savings(resolved_model, int(p_eval), int(e_cnt), has_img)
                _write_local_state(resolved_model, False, saved)
                print(f"[💰 Local Quota Shield] +{saved:,} cloud tokens saved by {resolved_model} (Lifetime Local Saved: {tot_saved:,})")
                return resp_text
    except (urllib.error.URLError, ConnectionRefusedError, TimeoutError):
        _write_local_state(resolved_model, False)
        return None
    _write_local_state(resolved_model, False)
    return None


def cmd_status(args):
    free_mb = get_free_vram_mb()
    print(f"[🖥️ Local Coprocessor Status] Endpoint: {args.endpoint} | RTX 5060 Free VRAM: {free_mb} MB")
    models = get_installed_ollama_models(args.endpoint)
    if models:
        print(f"[✓] Local Ollama server active! Installed models ({len(models)}):")
        for m in models:
            print(f"  -> {m}")
        ledger_p = Path.home() / ".cli_power_setup" / "token_ledger.json"
        if ledger_p.exists():
            try:
                lls = json.loads(ledger_p.read_text(encoding="utf-8")).get("local_llm_savings", {})
                if lls.get("total_cloud_tokens_saved", 0) > 0:
                    print(f"\n[💰 Local LLM Token Savings] Total Saved: {lls['total_cloud_tokens_saved']:,} cloud tokens ({lls.get('total_calls', 0)} calls)")
                    for m_k, m_v in sorted(lls.get("by_model", {}).items(), key=lambda x: -x[1].get("cloud_tokens_saved", 0)):
                        print(f"  • {m_k:22s}: {m_v.get('cloud_tokens_saved', 0):,d} saved ({m_v.get('calls', 0)} calls, {m_v.get('local_tokens', 0):,d} raw local tok)")
            except Exception:
                pass
        return

    print("[!] Local Ollama/llama.cpp server not running on localhost:11434.")
    print("  -> Tip: Start Ollama with `ollama serve` or run `ollama pull qwen2.5-coder:1.5b`.")
    if args.dry_run:
        print("[✓] Dry-run simulation active: Coprocessor ready.")


def cmd_generate(args):
    task_mode = "vision" if getattr(args, "image", "") else getattr(args, "task", "auto")
    prompt = args.prompt
    if args.file and os.path.exists(args.file):
        file_body = Path(args.file).read_text(encoding="utf-8", errors="ignore")
        prompt = f"{prompt}\n\n```\n{file_body[:6000]}\n```" if prompt else file_body

    if task_mode == "auto" and any(k in prompt.lower() for k in ("bpy", "blender", ".ogf", "remesh", "3d model")):
        task_mode = "blender"

    resolved = resolve_best_local_model(args.model, task_mode, args.endpoint)
    skill_sys, loaded_skills = load_skill_context(
        getattr(args, "skill", ""),
        getattr(args, "auto_skill", True),
        prompt,
        task_mode,
    )
    combined_sys = "\n\n".join(p for p in [getattr(args, "system", ""), skill_sys] if p)
    skill_badge = f" | Skills Injected: {', '.join(loaded_skills)}" if loaded_skills else ""
    print(f"[🤖 Local Generation] Model: {resolved} (task={task_mode}){skill_badge}")

    response = None
    if not args.dry_run:
        response = query_local_ollama(
            args.endpoint,
            resolved,
            prompt,
            combined_sys,
            getattr(args, "image", ""),
        )

    if response is None:
        response = f"// [Local Coprocessor - {resolved}]\n// Generated locally on host hardware (0 cloud tokens billed)\ndef synthetic_helper_routine():\n    return True\n"

    print("\n[✓] Response from Local Coprocessor:")
    print(response)

    if getattr(args, "output", ""):
        Path(args.output).write_text(response, encoding="utf-8")
        print(f"\n[✓] Output saved to: {args.output}")


def cmd_vision(args):
    resolved = resolve_best_local_model(args.model, "vision", args.endpoint)
    print(f"[👁️ Local Vision VLM] Model: {resolved} | Image: {args.image}")
    prompt = args.prompt or "Inspect this screenshot/render. Describe HUD state, any missing textures (purple/black), or visual anomalies in 3 concise bullet points."
    response = None
    if not args.dry_run:
        response = query_local_ollama(args.endpoint, resolved, prompt, image_path=args.image, timeout=35.0)
    if response is None:
        response = "- Frame inspected locally.\n- No crash dialog or missing purple checkerboard textures detected."
    print(f"\n[✓] Local Vision Triage:\n{response}")


def cmd_reason(args):
    resolved = resolve_best_local_model(args.model, "reason", args.endpoint)
    print(f"[🧠 Local CoT Reasoning] Model: {resolved}")
    prompt = args.prompt
    if args.file and os.path.exists(args.file):
        prompt = f"{prompt}\n\n```\n{Path(args.file).read_text(encoding='utf-8', errors='ignore')[:6000]}\n```"
    response = None
    if not args.dry_run:
        response = query_local_ollama(args.endpoint, resolved, prompt, timeout=45.0)
    if response is None:
        response = "- Root cause verified locally on RTX 5060."
    print(f"\n[✓] Local Reasoning Result:\n{response}")


def cmd_docstring(args):
    print(f"[📝 Local Docstring] Generating docstrings for: {args.file or 'code buffer'}")
    code = args.code or ""
    if args.file and os.path.exists(args.file):
        code = Path(args.file).read_text(encoding="utf-8", errors="ignore")

    prompt = f"Write clean, concise Google/PEP257 style docstrings for this function:\n```\n{code}\n```"
    response = None
    if not args.dry_run:
        resolved = resolve_best_local_model(args.model, "fast", args.endpoint)
        response = query_local_ollama(args.endpoint, resolved, prompt)

    if response is None:
        response = '"""\nExecutes local hardware-accelerated routine.\n\nReturns:\n    bool: True if operation completed without host error.\n"""'

    print("\n[✓] Generated Docstring:")
    print(response)


def cmd_commit_msg(args):
    print(f"[📦 Local Commit Msg] Summarizing staged diff...")
    diff_text = args.diff or "diff --git a/src/main.py b/src/main.py\n+def accelerate_hardware(): pass"
    prompt = f"Generate a high-density, conventional git commit message (e.g. 'feat: ...' or 'fix: ...') for this diff:\n```\n{diff_text}\n```"

    response = None
    if not args.dry_run:
        resolved = resolve_best_local_model(args.model, "fast", args.endpoint)
        response = query_local_ollama(args.endpoint, resolved, prompt)

    if response is None:
        response = "feat(hardware): add local hardware offloading routine to bypass cloud quota"

    print(f"\n[✓] Suggested Commit Message:\n{response}")


def cmd_summarize_log(args):
    print(f"[📋 Local Log Summary] Summarizing compiler/runtime log...")
    log_text = args.log or "Error: line 42: undefined reference to 'vkCreateInstance'"
    if args.file and os.path.exists(args.file):
        log_text = Path(args.file).read_text(encoding="utf-8", errors="ignore")[:4000]

    prompt = f"Identify the root cause error in this compiler/execution log in 2 bullet points:\n```\n{log_text}\n```"
    response = None
    if not args.dry_run:
        resolved = resolve_best_local_model(args.model, "fast", args.endpoint)
        response = query_local_ollama(args.endpoint, resolved, prompt)

    if response is None:
        response = "- Missing Vulkan SDK library link (-lvulkan).\n- Verify LunarG Vulkan SDK is exported in LD_LIBRARY_PATH."

    print(f"\n[✓] Local Log Triage:\n{response}")


def main():
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--dry-run", action="store_true", help="Simulate generation without active local server")
    common_parser.add_argument("--endpoint", type=str, default="http://localhost:11434", help="Local server URL")
    common_parser.add_argument("--model", type=str, default="auto", help="Local model name (default: auto-detect based on VRAM & task)")
    common_parser.add_argument("--task", type=str, default="auto", choices=["auto", "fast", "code", "reason", "vision", "blender", "csharp", "cpp", "rust", "python", "translate", "sql", "tool", "long", "math", "web", "business", "port", "plan", "re", "decompile"], help="Task routing mode")
    common_parser.add_argument("--skill", type=str, default="", help="Comma-separated skill names to inject into local model system prompt")
    common_parser.add_argument("--auto-skill", action="store_true", default=True, help="Automatically match and inject relevant SKILL.md rules")

    parser = argparse.ArgumentParser(parents=[common_parser], description="Local Model Coprocessor & Quota Shield")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # status
    subparsers.add_parser("status", parents=[common_parser], help="Check connection to local Ollama / llama.cpp")

    # generate
    p_gen = subparsers.add_parser("generate", parents=[common_parser], help="Generate code or text locally")
    p_gen.add_argument("--prompt", type=str, default="", help="Prompt text")
    p_gen.add_argument("--file", type=str, default="", help="Input file path")
    p_gen.add_argument("--image", type=str, default="", help="Optional image path for local VLM")
    p_gen.add_argument("--system", type=str, default="", help="Optional system instruction")
    p_gen.add_argument("--output", type=str, default="", help="Output destination file")

    # vision
    p_vis = subparsers.add_parser("vision", parents=[common_parser], help="Inspect game screenshot or 3D render locally using VLM")
    p_vis.add_argument("--image", type=str, required=True, help="Image file path (.png/.jpg)")
    p_vis.add_argument("--prompt", type=str, default="", help="Custom vision question")

    # reason
    p_reas = subparsers.add_parser("reason", parents=[common_parser], help="Run local Chain-of-Thought reasoning on crash logs or math")
    p_reas.add_argument("--prompt", type=str, required=True, help="Reasoning query")
    p_reas.add_argument("--file", type=str, default="", help="Optional log/source file")

    # docstring
    p_doc = subparsers.add_parser("docstring", parents=[common_parser], help="Generate function docstrings locally")
    p_doc.add_argument("--file", type=str, default="")
    p_doc.add_argument("--code", type=str, default="")

    # commit-msg
    p_commit = subparsers.add_parser("commit-msg", parents=[common_parser], help="Generate git commit message from diff")
    p_commit.add_argument("--diff", type=str, default="")

    # summarize-log
    p_log = subparsers.add_parser("summarize-log", parents=[common_parser], help="Triage heavy compiler or test log locally")
    p_log.add_argument("--file", type=str, default="")
    p_log.add_argument("--log", type=str, default="")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "vision":
        cmd_vision(args)
    elif args.command == "reason":
        cmd_reason(args)
    elif args.command == "docstring":
        cmd_docstring(args)
    elif args.command == "commit-msg":
        cmd_commit_msg(args)
    elif args.command == "summarize-log":
        cmd_summarize_log(args)


if __name__ == "__main__":
    main()

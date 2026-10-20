#!/usr/bin/env python3
"""Game-aware local LLM runner: every tool asks models through here so the game and the models can share this laptop (RTX 5060 8 GB, 32 threads, 30 GB RAM).
  game running  -> the game keeps the VRAM it needs (measured, at least 4.5 GB; 6.5 GB while .agents/benchmark.on exists = a performance benchmark is running; override
                   LLM_GAME_VRAM_GB) and the model gets the REST of the 8 GB: it is put fully on the GPU if it fits, else only as many layers as fit (rest on CPU, 8 threads),
                   else CPU only (then at most 8 threads, 2 when the machine is busy, and the model processes are put on the IDLE scheduler class so the game always gets the CPU first); big models are swapped for a small one (<= 8 B) so frame times stay clean; keep_alive 2 min
  game closed   -> GPU offload as far as VRAM allows (Ollama splits layers between GPU and RAM), all threads, keep_alive 10 min
usage: llmrun.py MODEL "prompt"      (python: from llmrun import ask)
Models live on two Ollama instances (11434 system, 11435 games drive); the one that has the model is used."""
import json, os, subprocess, sys, urllib.request
SMALL_FOR_GAME = "qwen2.5-coder:7b"
BIG = ("30b", "32b", "33b", "35b", "70b", "72b", "8x7b", "22b", "24b")
def game_running(): return subprocess.run("pgrep -f '[x]rEngine.exe -nointro' >/dev/null", shell=True).returncode == 0
def _post(host, path, body, timeout):
    req = urllib.request.Request(f"http://{host}{path}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))
def _has(host, model):
    try: return any(m["name"] == model or m["name"].split(":")[0] == model.split(":")[0] and ":" not in model for m in json.load(urllib.request.urlopen(f"http://{host}/api/tags", timeout=3))["models"])
    except Exception: return False
HERE = os.path.dirname(os.path.abspath(__file__))
def _smi(q):
    try: return subprocess.run(["nvidia-smi", f"--query-{q}", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=6).stdout.strip().splitlines()
    except Exception: return []
def game_vram_gb():
    """VRAM the running game uses now (xrEngine / Wine process), GB; 0 if unknown"""
    try:
        pids = set(subprocess.run("pgrep -f '[x]rEngine.exe'", shell=True, capture_output=True, text=True).stdout.split())
        return sum(int(l.split(",")[1]) for l in _smi("compute-apps=pid,used_memory") if l.split(",")[0].strip() in pids) / 1024
    except Exception: return 0.0
def vram_budget_gb():
    """GB of VRAM a local model may use while the game runs = total - reserve for the game (measured+1 GB, never less than the floor) - what other apps already hold"""
    try:
        tot, used = (int(x) / 1024 for x in _smi("gpu=memory.total,memory.used")[0].split(","))
        floor = float(os.environ.get("LLM_GAME_VRAM_GB") or (6.5 if os.path.exists(os.path.join(HERE, "..", ".agents/benchmark.on")) else 4.5))
        game = game_vram_gb(); reserve = max(floor, game + 1.0)
        models_now = 0.0                                                    # VRAM our own models already hold (they are ours to use, not "other apps")
        for host in ("127.0.0.1:11434", "127.0.0.1:11435"):
            try: models_now += sum(m.get("size_vram", 0) for m in json.load(urllib.request.urlopen(f"http://{host}/api/ps", timeout=2))["models"]) / 2**30
            except Exception: pass
        others = max(0.0, used - game - models_now)
        return max(0.0, tot - reserve - others)
    except Exception: return 0.0
def _size_gb(host, model):
    try: return next(m["size"] for m in json.load(urllib.request.urlopen(f"http://{host}/api/tags", timeout=3))["models"] if m["name"] == model) / 2**30
    except Exception: return 5.0
def cpu_threads_for_model(gaming):
    """threads a model may use: alone = all; with the game = what is left after the game's share (it needs ~8 of the 32 threads to run smoothly: render, sound, physics, engine
    workers) and never more than 8; when the machine is already busy (load > 60 % of the threads) just 2"""
    n = os.cpu_count() or 16
    if not gaming: return n
    t = max(2, min(8, n - 12))
    return 2 if os.getloadavg()[0] > 0.6 * n else t
def _set_sched(gaming):
    """while a game runs the model processes are put on the IDLE scheduler class (they only get CPU the game leaves free); otherwise back to normal. Best effort."""
    pol = "-i" if gaming else "-o"
    try:
        pids = subprocess.run(["pgrep", "-u", str(os.getuid()), "-f", "^[^ ]*(llama-server|ollama (serve|runner))"], capture_output=True, text=True).stdout.split()   # only processes of this user (the system service belongs to the ollama user: capped by num_thread instead)
        for pid in pids: subprocess.run(["chrt", pol, "-p", "0", pid], capture_output=True, timeout=3)
    except Exception: pass
def ask(model, prompt, timeout=1200):
    gaming = game_running()
    _set_sched(gaming)
    if gaming and any(b in model for b in BIG): model = SMALL_FOR_GAME
    host = next((h for h in ("127.0.0.1:11435", "127.0.0.1:11434") if _has(h, model)), "127.0.0.1:11434")
    opts = {"num_thread": cpu_threads_for_model(gaming)}
    if gaming:
        budget, size = vram_budget_gb() * 0.85, _size_gb(host, model)       # 15 % slack for the context cache
        frac = 1.0 if size <= budget else (budget / size if budget > 0.8 else 0.0)
        if frac < 1.0: opts["num_gpu"] = int(frac * 40)                     # layers on the GPU (a 7 B model has ~30-40); 0 = CPU only
    r = _post(host, "/api/generate", {"model": model, "prompt": prompt, "stream": False, "keep_alive": "2m" if gaming else "10m", "options": opts}, timeout)
    _record(model, r)
    return r.get("response", "")
_rec = None
def _record(model, r):
    """Count the tokens this local call kept out of the cloud in the shared ledger the status line reads (~/.cli_power_setup/token_ledger.json, local_llm_savings).
    The 'cloud tokens saved' figure is the same ESTIMATE local-coprocessor uses (per-model-tier multipliers), not a measured number. Never lets a ledger error break a call."""
    global _rec
    try:
        if _rec is None:
            import importlib.machinery, importlib.util
            l = importlib.machinery.SourceFileLoader("local_coprocessor", os.path.expanduser("~/.local/bin/local-coprocessor")); sp = importlib.util.spec_from_loader("local_coprocessor", l)
            _rec = importlib.util.module_from_spec(sp); l.exec_module(_rec)
        _rec.record_local_llm_savings(model, r.get("prompt_eval_count") or 0, r.get("eval_count") or 0)
    except Exception: pass
if __name__ == "__main__":
    print(ask(sys.argv[1], " ".join(sys.argv[2:])))

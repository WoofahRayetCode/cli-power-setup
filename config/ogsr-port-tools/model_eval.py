#!/usr/bin/env python3
"""Evidence for model decisions: run the same validated tasks through several local models and compare pass rate and speed.
  model_eval.py MODEL [MODEL ...]      appends one row per (model, task) to docs/learn/model_eval.jsonl and prints a table
Tasks are the kinds the workers do (lua / python / xml / json / ltx / small reasoning with a checkable answer); validation is local-worker's own validator (luajit -b, ast, XML parse, ...).
While a game runs the numbers are CPU/partial-GPU numbers; quality (pass rate) is comparable, speed only between models in the same run."""
import ast, importlib.machinery, importlib.util, json, os, re, sys, time, urllib.request
from pathlib import Path
here = Path(__file__).resolve().parent.parent; OUT = here / "docs/learn/model_eval.jsonl"
src = open(os.path.expanduser("~/.local/bin/local-worker")).read().rstrip()
src = src[:src.rindex("\nmain()")] if src.endswith("\nmain()") else src        # the worker script runs main() at import: load its functions without that
class _NS: pass
lw = _NS(); ns = {"__name__": "lw"}; exec(compile(src, "local-worker", "exec"), ns); lw.__dict__.update(ns)
HINT = lw.HINTS
TASKS = [
 ("lua", "Write a Lua 5.1 function clamp(v, lo, hi) and lerp(a, b, t)."),
 ("lua", "Write a Lua 5.1 function that returns the distance between two tables {x=,z=} on the XZ plane."),
 ("lua", "Write Lua 5.1 code with a function pick_random(list) returning a random element or nil for an empty table."),
 ("python", "Write a Python function parse_ltx(text) returning a dict section->dict key->value; comments start with ;"),
 ("python", "Write a Python function moving_avg(values, n) returning a list of moving averages."),
 ("xml", "Write a well-formed XML string_table with two <string id=\"a\"><text>Hi</text></string> entries."),
 ("xml", "Write a well-formed XML <dialog> with an id attribute and two <phrase> children with ids 0 and 1."),
 ("json", "Write a JSON object with three factions, each with name and hostile_to array."),
 ("json", "Write a JSON list of three items, each with section, cost (number) and weight (number)."),
 ("ltx", "Write an LTX section [zf_test]:parent with cost = 100, weight = 0.5 and a ; comment."),
 ("ltx", "Write two LTX sections [a] and [b]:a, each with two key = value lines."),
]
REASON = [("What is 17 * 23? Answer with the number only.", "391"), ("A rocket flies 12 m/s for 7 s, how many metres? Number only.", "84"), ("How many days in a leap year? Number only.", "366")]
def ask(model, prompt):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.1, "num_ctx": 4096}}).encode()
    t = time.time(); r = json.load(urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:11434/api/generate", body, {"Content-Type": "application/json"}), timeout=600))
    return r["response"], time.time() - t
def main():
    models = sys.argv[1:] or []
    for m in models:
        ok = n = 0; secs = 0.0
        for kind, task in TASKS:
            prompt = f"You are a precise {kind} code generator. Output ONLY the {kind} content, no explanations.\n{HINT.get(kind, '')}\nTask: {task}\n"
            try: out, dt = ask(m, prompt); err = lw.validate(kind, lw.strip(out))
            except Exception as e: out, dt, err = "", 0, f"call failed: {e}"
            n += 1; ok += err is None; secs += dt
            OUT.parent.mkdir(exist_ok=True); open(OUT, "a").write(json.dumps({"t": time.strftime("%F %T"), "model": m, "kind": kind, "ok": err is None, "sec": round(dt, 1), "err": err, "task": task[:60]}) + "\n")
        for q, a in REASON:
            try: out, dt = ask(m, q); good = a in re.sub(r"<think>.*?</think>", "", out, flags=re.S)
            except Exception: good, dt = False, 0
            n += 1; ok += good; secs += dt
            open(OUT, "a").write(json.dumps({"t": time.strftime("%F %T"), "model": m, "kind": "reason", "ok": good, "sec": round(dt, 1), "err": None, "task": q[:60]}) + "\n")
        print(f"{m:34} pass {ok}/{n}  {secs / n:5.1f} s/task")
main()

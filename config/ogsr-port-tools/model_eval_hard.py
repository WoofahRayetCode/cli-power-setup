#!/usr/bin/env python3
"""Harder, discriminating checks for model-replacement decisions (docs/learn/model_eval_hard.jsonl):
  code   python functions that must PASS unit tests (run in a subprocess, 10 s limit)
  math   word problems with exact numeric answers (the model may think first: the LAST number it writes is compared)
  vision a generated picture (3 red circles, 2 blue squares, the word ZONE): count / read it  (only models that accept images)
usage: model_eval_hard.py code|math|vision MODEL [MODEL ...]"""
import base64, io, json, re, subprocess, sys, tempfile, time, urllib.request
from pathlib import Path
here = Path(__file__).resolve().parent.parent; OUT = here / "docs/learn/model_eval_hard.jsonl"
CODE = [("def is_prime(n): return True if n is prime else False; handle n<2", "assert is_prime(2) and is_prime(97) and not is_prime(1) and not is_prime(91) and not is_prime(-5)"),
        ("def merge_intervals(iv): merge overlapping [a,b] intervals, return sorted list of lists", "assert merge_intervals([[1,3],[2,6],[8,10],[9,12]])==[[1,6],[8,12]] and merge_intervals([])==[]"),
        ("def parse_ltx(text): dict section->dict key->value; '[a]:b' header keeps section 'a'; lines starting with ';' are comments; 'k = v' pairs", "r=parse_ltx('[a]:p\\n; c\\nx = 1\\ny=2\\n[b]\\nz = 3'); assert r=={'a':{'x':'1','y':'2'},'b':{'z':'3'}}"),
        ("def lcs(a, b): length of the longest common subsequence of two strings", "assert lcs('ABCBDAB','BDCABA')==4 and lcs('','a')==0"),
        ("def dist_point_segment(px,pz,ax,az,bx,bz): shortest distance from a point to a line segment", "assert abs(dist_point_segment(0,1,-1,0,1,0)-1)<1e-9 and abs(dist_point_segment(3,0,-1,0,1,0)-2)<1e-9")]
MATH = [("A rocket travels 12.5 m/s for 8 seconds, then 20 m/s for 4.5 seconds. Total distance in metres?", 190),
        ("How many ways can 5 different books be arranged on a shelf if 2 particular books must be next to each other?", 48),
        ("A stalker carries 38 kg; each artifact weighs 0.6 kg and each medkit 0.4 kg. He has 9 artifacts and 12 medkits besides a 30 kg load. Total weight in kg?", 40.2),
        ("What is the sum of the integers from 1 to 100 that are divisible by 3 or 5?", 2418),
        ("If 15 percent of a number is 63, what is 40 percent of the number?", 168),
        ("A train leaves at 60 km/h; 2 hours later a second leaves the same station at 90 km/h on the same track. After how many hours (from the second's start) does it catch up?", 4)]
def post(model, prompt, images=None, timeout=300):
    b = {"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.1, "num_ctx": 4096, "num_predict": 2500}}
    if images: b["images"] = images
    t = time.time(); r = json.load(urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:11434/api/generate", json.dumps(b).encode(), {"Content-Type": "application/json"}), timeout=timeout))
    return r["response"], time.time() - t
def done_before(model, kind, task):
    try: return any(json.loads(l).get("model") == model and json.loads(l).get("kind") == kind and json.loads(l).get("task") == task[:60] for l in OUT.read_text().splitlines())
    except Exception: return False
def rec(model, kind, ok, sec, task):
    OUT.parent.mkdir(exist_ok=True); open(OUT, "a").write(json.dumps({"t": time.strftime("%F %T"), "model": model, "kind": kind, "ok": bool(ok), "sec": round(sec, 1), "task": task[:60]}) + "\n")
def run_code(model):
    ok = 0
    for desc, test in CODE:
        if done_before(model, 'code', desc): ok += 0; continue
        try:
            out, dt = post(model, f"Write ONLY Python code (no explanations, no tests, no markdown): {desc}")
            code = re.sub(r"<think>.*?</think>", "", out, flags=re.S); m = re.search(r"```(?:python)?\n(.*?)```", code, re.S); code = m.group(1) if m else code
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f: f.write(code + "\n" + test + "\n")
            good = subprocess.run([sys.executable, "-I", f.name], capture_output=True, timeout=10).returncode == 0
        except Exception: good, dt = False, 0
        ok += good; rec(model, "code", good, dt, desc)
    return ok, len(CODE)
def run_math(model):
    ok = 0
    for q, a in MATH:
        if done_before(model, 'math', q): continue
        try:
            out, dt = post(model, q + "\nThink briefly, then finish with 'ANSWER: <number>'."); out = re.sub(r"<think>.*?</think>", "", out, flags=re.S)
            nums = re.findall(r"-?\d+(?:\.\d+)?", out.split("ANSWER:")[-1].replace(",", "")); good = bool(nums) and abs(float(nums[0] if "ANSWER:" in out else nums[-1]) - a) < 0.01
        except Exception: good, dt = False, 0
        ok += good; rec(model, "math", good, dt, q)
    return ok, len(MATH)
def run_vision(model):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (480, 320), "white"); d = ImageDraw.Draw(im)
    for i in range(3): d.ellipse((30 + i * 90, 40, 100 + i * 90, 110), fill="red")
    for i in range(2): d.rectangle((40 + i * 120, 170, 110 + i * 120, 240), fill="blue")
    d.text((330, 200), "ZONE", fill="black"); d.text((330, 215), "ZONE", fill="black")
    buf = io.BytesIO(); im.save(buf, "PNG"); img = [base64.b64encode(buf.getvalue()).decode()]
    ok = 0; qs = [("How many red circles are in the picture? Answer with a digit only.", "3"), ("How many blue squares are in the picture? Answer with a digit only.", "2"), ("What word is written in the picture? One word.", "zone")]
    for q, a in qs:
        try: out, dt = post(model, q, img); good = a in out.lower()
        except Exception: good, dt = False, 0
        ok += good; rec(model, "vision", good, dt, q)
    return ok, len(qs)
if __name__ == "__main__":
    kind, models = sys.argv[1], sys.argv[2:]
    for m in models:
        ok, n = {"code": run_code, "math": run_math, "vision": run_vision}[kind](m); print(f"{kind:6} {m:40} {ok}/{n}", flush=True)

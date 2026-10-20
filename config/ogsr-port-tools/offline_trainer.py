#!/usr/bin/env python3
"""Offline GPU trainer for the auto walker (run with ~/.cache/gputrainer/bin/python; only while no game is running: the guardian checks).
Reads docs/learn/walker_dataset.jsonl (kick / learned / hot events + position rows, written by tools/walker_collect.py) and fits, on the CUDA GPU,
a small logistic model P(a portal kick at angle a gets him past the snag) over angle buckets (cos/sin features + kick count + hostiles near).
Writes the ranking of angles to docs/learn/kick_prior.txt (and copies it to _appdata_/logs/kick_prior.txt, where the game reads it): the walker tries the most promising
approach angle FIRST at a new snag instead of the fixed list. Needs >= 12 kick events to say anything; below that it writes nothing (the fixed list stays).
Also prints a short training report to docs/learn/trainer_report.md. Small VRAM use (< 300 MB), so it can also run next to a game if forced with --force."""
import json, math, os, subprocess, sys, time
from pathlib import Path
here = Path(__file__).resolve().parent.parent; DS = here / "docs/learn/walker_dataset.jsonl"
def main():
    if "--force" not in sys.argv and subprocess.run("pgrep -f '[x]rEngine.exe'", shell=True, capture_output=True).returncode == 0:
        print("a game is running: not training (use --force)"); return
    import torch
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    rows = [json.loads(l) for l in DS.read_text().splitlines() if l.strip()] if DS.exists() else []
    kicks = [r for r in rows if r.get("ev") == "kick" and str(r.get("angle", "")).lstrip("-").isdigit()]
    wins = [r for r in rows if r.get("ev") == "learned" and r.get("angle") is not None]
    rep = [f"# Trainer report {time.strftime('%F %T')}", f"device {dev}; {len(rows)} rows, {len(kicks)} kick events, {len(wins)} learned events"]
    if len(kicks) < 12:
        rep.append("not enough kick events yet (need 12): nothing written, the walker keeps its fixed angle list"); (here / "docs/learn/trainer_report.md").write_text("\n".join(rep) + "\n"); print("\n".join(rep)); return
    won = {(w["level"], int(w["angle"])) for w in wins}
    X, y = [], []
    for k in kicks:
        a = math.radians(int(k["angle"])); X.append([math.cos(a), math.sin(a), math.cos(2 * a), math.sin(2 * a), min(k.get("n", 1), 6) / 6.0]); y.append(1.0 if (k["level"], int(k["angle"])) in won else 0.0)
    Xt = torch.tensor(X, device=dev); yt = torch.tensor(y, device=dev)
    w = torch.zeros(Xt.shape[1], device=dev, requires_grad=True); b = torch.zeros(1, device=dev, requires_grad=True)
    opt = torch.optim.Adam([w, b], lr=0.05)
    for _ in range(600):
        opt.zero_grad(); loss = torch.nn.functional.binary_cross_entropy_with_logits(Xt @ w + b, yt) + 1e-3 * (w ** 2).sum(); loss.backward(); opt.step()
    scores = []
    for ang in range(-180, 181, 30):
        a = math.radians(ang); f = torch.tensor([[math.cos(a), math.sin(a), math.cos(2 * a), math.sin(2 * a), 0.0]], device=dev)
        scores.append((float(torch.sigmoid(f @ w + b).detach()), ang))
    scores.sort(reverse=True)
    out = "\n".join(f"{a} {s:.3f}" for s, a in scores) + "\n"
    (here / "docs/learn/kick_prior.txt").write_text(out)
    try: (here / "_appdata_/logs/kick_prior.txt").write_text(out)
    except Exception: pass
    rep += [f"final loss {float(loss.detach()):.4f}; win rate in data {sum(y) / len(y):.2f}", "best angles: " + ", ".join(f"{a} ({s:.2f})" for s, a in scores[:5])]
    (here / "docs/learn/trainer_report.md").write_text("\n".join(rep) + "\n"); print("\n".join(rep))
main()

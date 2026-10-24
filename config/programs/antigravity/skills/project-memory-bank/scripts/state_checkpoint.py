#!/usr/bin/env python3
"""
Working Memory & State Checkpointing CLI:
Snapshots and restores uncommitted code diffs, hypothesis notes, and working state.
Zero external dependencies.
"""
import sys
import os
import re
import json
import time
import subprocess
import argparse
from pathlib import Path

CHECKPOINTS_DIR = Path(".agents/checkpoints")

def run_cmd(cmd, check=True):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {cmd}\n{res.stderr}")
    return res.stdout.strip()

def save_checkpoint(label: str = "auto", hypothesis: str = ""):
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = int(time.time())
    slug = re.sub(r'[^a-zA-Z0-9_-]', '_', label.lower())[:30]
    filename = f"checkpoint_{ts}_{slug}.json"
    target_path = CHECKPOINTS_DIR / filename

    try:
        status = run_cmd("git status --porcelain", check=False)
        diff = run_cmd("git diff HEAD", check=False)
        branch = run_cmd("git branch --show-current", check=False)
        commit = run_cmd("git rev-parse --short HEAD", check=False)
    except Exception as e:
        status, diff, branch, commit = "", "", "unknown", "unknown"

    data = {
        "timestamp": ts,
        "label": label,
        "hypothesis": hypothesis,
        "branch": branch,
        "commit": commit,
        "status": status,
        "patch": diff
    }

    target_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[✓] Checkpoint saved: {target_path} (Branch: {branch}@{commit})")
    if status:
        mod_count = len(status.splitlines())
        print(f"    Preserved uncommitted diff across {mod_count} files.")
    else:
        print("    Working directory clean at snapshot time.")
    return target_path

def list_checkpoints():
    if not CHECKPOINTS_DIR.exists():
        print("[!] No checkpoints directory found (.agents/checkpoints).")
        return []

    files = sorted(CHECKPOINTS_DIR.glob("checkpoint_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        print("[!] No state checkpoints saved yet.")
        return []

    print(f"📋 Saved Working State Checkpoints ({len(files)} total):")
    print("-" * 65)
    for p in files:
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            ts_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(d.get("timestamp", 0)))
            label = d.get("label", "unnamed")
            branch = d.get("branch", "main")
            commit = d.get("commit", "HEAD")
            hyp = f" | Note: {d['hypothesis']}" if d.get("hypothesis") else ""
            print(f"• [{p.stem}] {ts_str} ({branch}@{commit}) - '{label}'{hyp}")
        except Exception:
            print(f"• [{p.stem}] (Corrupt or unreadable)")
    return files

def restore_checkpoint(target_id: str):
    if not CHECKPOINTS_DIR.exists():
        print("[!] No checkpoints directory found.")
        return False

    matches = list(CHECKPOINTS_DIR.glob(f"*{target_id}*.json"))
    if not matches:
        print(f"[!] Checkpoint '{target_id}' not found.")
        return False

    target_path = matches[0]
    data = json.loads(target_path.read_text(encoding="utf-8"))
    patch = data.get("patch", "")

    print(f"[→] Restoring checkpoint: {target_path.name} ('{data.get('label')}')")

    # Reset current dirty state
    try:
        run_cmd("git reset --hard HEAD", check=False)
        run_cmd("git clean -fd", check=False)
    except Exception as e:
        print(f"[!] Warning resetting git state: {e}")

    # Re-apply patch if present
    if patch.strip():
        tmp_patch = Path("/tmp/state_restore.patch")
        tmp_patch.write_text(patch, encoding="utf-8")
        res = subprocess.run(f"git apply {tmp_patch}", shell=True, text=True, capture_output=True)
        if res.returncode == 0:
            print("[✓] Uncommitted diff successfully re-applied.")
        else:
            print(f"[!] Git apply warning: {res.stderr}")
    else:
        print("[✓] Clean working tree state restored.")

    return True

def prune_checkpoints(keep: int = 5):
    if not CHECKPOINTS_DIR.exists():
        return
    files = sorted(CHECKPOINTS_DIR.glob("checkpoint_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if len(files) <= keep:
        print(f"[✓] {len(files)} checkpoints found; within retention limit of {keep}.")
        return

    to_delete = files[keep:]
    for f in to_delete:
        f.unlink()
    print(f"[✓] Pruned {len(to_delete)} older checkpoints; retained {keep} latest.")

def main():
    parser = argparse.ArgumentParser(description="Working Memory State Checkpointer")
    subparsers = parser.add_subparsers(dest="command")

    # Save
    save_p = subparsers.add_parser("save", help="Save atomic working state checkpoint")
    save_p.add_argument("label", nargs="?", default="milestone", help="Brief label for checkpoint")
    save_p.add_argument("--hypothesis", "-m", default="", help="Active hypothesis or experiment notes")

    # List
    subparsers.add_parser("list", help="List saved checkpoints")

    # Restore
    rest_p = subparsers.add_parser("restore", help="Restore working tree state to a checkpoint")
    rest_p.add_argument("target_id", help="Checkpoint timestamp or name substring")

    # Prune
    prune_p = subparsers.add_parser("prune", help="Prune older checkpoints")
    prune_p.add_argument("--keep", type=int, default=5, help="Number of recent checkpoints to retain")

    args = parser.parse_args()

    if args.command == "save":
        save_checkpoint(args.label, args.hypothesis)
    elif args.command == "list":
        list_checkpoints()
    elif args.command == "restore":
        restore_checkpoint(args.target_id)
    elif args.command == "prune":
        prune_checkpoints(args.keep)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

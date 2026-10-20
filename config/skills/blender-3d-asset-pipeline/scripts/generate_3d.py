#!/usr/bin/env python3
"""
Universal AI 3D Mesh Generation Dispatcher
Supports: Tripo3D API (Text-to-3D & Image-to-3D) and Offline Procedural Fallback.
"""
import argparse
import os
import sys
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

def generate_tripo_text_to_3d(prompt: str, output_path: str):
    api_key = os.environ.get("TRIPO_API_KEY")
    if not api_key:
        print("[!] Error: TRIPO_API_KEY environment variable is not set.")
        print("[!] Tip: You can test offline generation with: --backend offline-box")
        sys.exit(1)

    url = "https://api.tripo3d.ai/v2/openapi/task"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "type": "text_to_model",
        "prompt": prompt
    }

    print(f"[TRIPO] Dispatching Text-to-3D task: '{prompt}'...")
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            task_id = data.get("data", {}).get("task_id")
            print(f"[✓] Task dispatched! ID: {task_id}")
            
            # Poll for completion
            poll_url = f"https://api.tripo3d.ai/v2/openapi/task/{task_id}"
            while True:
                time.sleep(4)
                poll_req = urllib.request.Request(poll_url, headers={"Authorization": f"Bearer {api_key}"})
                with urllib.request.urlopen(poll_req) as p_resp:
                    p_data = json.loads(p_resp.read().decode('utf-8'))
                    status = p_data.get("data", {}).get("status")
                    progress = p_data.get("data", {}).get("progress", 0)
                    print(f"[TRIPO] Status: {status} ({progress}%)...")
                    
                    if status == "success":
                        model_url = p_data["data"]["output"]["model"]
                        print(f"[✓] 3D Model created! Downloading from {model_url}...")
                        urllib.request.urlretrieve(model_url, output_path)
                        print(f"[✓] Successfully saved 3D model to: {output_path}")
                        break
                    elif status in ["failed", "cancelled"]:
                        print(f"[✗] Generation failed: {p_data}")
                        sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"[✗] HTTP Error: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)

def generate_offline_box(output_path: str):
    print(f"[OFFLINE] Generating procedural 3D box model (Wavefront OBJ)...")
    obj_content = """# Procedural 3D Box
v -0.5 -0.5  0.5
v  0.5 -0.5  0.5
v  0.5  0.5  0.5
v -0.5  0.5  0.5
v -0.5 -0.5 -0.5
v  0.5 -0.5 -0.5
v  0.5  0.5 -0.5
v -0.5  0.5 -0.5
f 1 2 3 4
f 8 7 6 5
f 4 3 7 8
f 5 6 2 1
f 2 6 7 3
f 5 1 4 8
"""
    obj_out = output_path if output_path.endswith(".obj") else output_path.replace(".glb", ".obj")
    Path(obj_out).write_text(obj_content, encoding="utf-8")
    print(f"[✓] Successfully generated offline 3D model: {obj_out}")

def main():
    parser = argparse.ArgumentParser(description="Tripo AI 3D Mesh Generator")
    parser.add_argument("--backend", choices=["tripo", "offline-box"], default="offline-box")
    parser.add_argument("--prompt", type=str, default="A stylized wooden treasure chest")
    parser.add_argument("--output", type=str, default="output_model.glb")
    args = parser.parse_args()

    if args.backend == "tripo":
        generate_tripo_text_to_3d(args.prompt, args.output)
    else:
        generate_offline_box(args.output)

if __name__ == "__main__":
    main()

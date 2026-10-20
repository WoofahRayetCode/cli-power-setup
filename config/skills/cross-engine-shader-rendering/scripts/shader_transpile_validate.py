#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil

def main():
    if len(sys.argv) < 2:
        print("Usage: shader_transpile_validate.py <shader_file> [-S vert|frag|comp|geom|tesc|tese] [--opt]")
        sys.exit(1)

    shader_path = sys.argv[1]
    if not os.path.isfile(shader_path):
        print(f"[!] Error: File '{shader_path}' not found.")
        sys.exit(1)

    glslang = shutil.which("glslangValidator")
    spirv_val = shutil.which("spirv-val")
    spirv_opt = shutil.which("spirv-opt")

    if not glslang:
        print("[!] Error: 'glslangValidator' is not installed or not in PATH.")
        sys.exit(1)

    output_spv = f"/tmp/{os.path.basename(shader_path)}.spv"
    cmd = [glslang, "-V", shader_path, "-o", output_spv]

    # Forward extra args
    extra_args = sys.argv[2:]
    run_opt = "--opt" in extra_args
    if run_opt:
        extra_args.remove("--opt")

    cmd.extend(extra_args)

    print(f"[→] Compiling {shader_path} -> {output_spv}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"[✗] Compilation failed:\n{res.stdout}\n{res.stderr}")
        sys.exit(res.returncode)
    print(f"[✓] Compiled to SPIR-V successfully ({os.path.getsize(output_spv)} bytes).")

    if spirv_val:
        print(f"[→] Validating SPIR-V bytecode with spirv-val...")
        val_res = subprocess.run([spirv_val, output_spv], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if val_res.returncode != 0:
            print(f"[✗] Validation failed:\n{val_res.stderr}")
            sys.exit(val_res.returncode)
        print("[✓] SPIR-V bytecode is 100% valid.")

    if run_opt and spirv_opt:
        opt_spv = f"/tmp/{os.path.basename(shader_path)}.opt.spv"
        print(f"[→] Optimizing SPIR-V bytecode with spirv-opt -O...")
        opt_res = subprocess.run([spirv_opt, "-O", output_spv, "-o", opt_spv], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if opt_res.returncode == 0:
            orig_sz = os.path.getsize(output_spv)
            new_sz = os.path.getsize(opt_spv)
            print(f"[✓] Optimization complete: {orig_sz}B -> {new_sz}B (saved {orig_sz - new_sz} bytes).")

if __name__ == "__main__":
    main()

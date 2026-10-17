---
name: local-ast-compiler-engine
description: High-performance multithreaded AST analysis, symbol table scanning, and structural linting running across all host CPU cores (nproc). Detects syntax errors and extracts symbol trees in milliseconds locally, eliminating trial-and-error reasoning turns.
---

# Local Multithreaded AST & Compiler Engine (`local-ast-compiler-engine`)

The `local-ast-compiler-engine` skill leverages all available host CPU cores (`-j$(nproc)`) to parse Abstract Syntax Trees (ASTs), extract symbol trees, and perform structural code linting locally before or instead of calling cloud AI models.

By diagnosing syntax errors, missing arguments, and broken references locally in $<50\text{ms}$, this skill prevents the AI from burning multiple turns of trial-and-error reasoning to debug basic structural flaws.

---

## 1. Hardware Parallelism & Multithreading

```
+------------------------------------------------------------------------+
|                          Codebase Target Path                          |
+------------------------------------------------------------------------+
                                    |
            +-----------------------+-----------------------+
            |                       |                       |
            v                       v                       v
      CPU Thread 1            CPU Thread 2           CPU Thread N
  (ast.parse batch 1)     (ast.parse batch 2)     (ast.parse batch N)
            |                       |                       |
            +-----------------------+-----------------------+
                                    |
                                    v
+------------------------------------------------------------------------+
|                         Aggregated Diagnostics                         |
|  - Pinpoint Syntax Errors (file, line number, column offset)           |
|  - Full Class & Function Symbol Index                                  |
|  - Instant (<10ms) Verification Proof for Agent Checklist              |
+------------------------------------------------------------------------+
```

---

## 2. Core Capabilities

* **CPU Core Saturation**: Automatically detects `os.cpu_count()` and spawns worker pools to process hundreds of files concurrently.
* **Hermetic Syntax Verification**: Catches unterminated strings, invalid indentation, unclosed brackets, and malformed grammar locally before executing tests.
* **Symbol Table Mapping**: Extracts all `FunctionDef`, `AsyncFunctionDef`, and `ClassDef` identifiers with their argument signatures and line numbers.
* **Structural AST Search**: Searches for specific AST call patterns (e.g. bare exceptions, unclosed file handles) without regex false positives.

---

## 3. CLI Helper Tool Reference (`local_ast_compiler.py`)

Located at `config/skills/local-ast-compiler-engine/scripts/local_ast_compiler.py`.

### Commands
```bash
# 1. Parallel syntax check across all CPU cores
python3 config/skills/local-ast-compiler-engine/scripts/local_ast_compiler.py \
  check-syntax --path ./config/skills/

# 2. Extract symbol hierarchy (classes, functions, signatures)
python3 config/skills/local-ast-compiler-engine/scripts/local_ast_compiler.py \
  scan-symbols --path ./src/main.py

# 3. Structural AST pattern search
python3 config/skills/local-ast-compiler-engine/scripts/local_ast_compiler.py \
  search-pattern --path ./src --pattern "read_text"
```

## Windows 10/11 & Cross-OS Hardware Offload Parity (`windows-linux-cross-os-runtime-bridge`)
- **CPU Thread Saturation:** Use `os.cpu_count()` in Python, `$env:NUMBER_OF_PROCESSORS` in PowerShell 7 (`CMAKE_BUILD_PARALLEL_LEVEL=$env:NUMBER_OF_PROCESSORS`, `CARGO_BUILD_JOBS=$env:NUMBER_OF_PROCESSORS`, `msbuild /m`), and `$(nproc)` on Linux.
- **RAM-Disk & Scratch I/O:** Resolve scratch paths via `Path("/dev/shm")` on Linux, an ImDisk/OSFMount RAMDrive (`R:\`) if mounted on Windows, or `Path(tempfile.gettempdir())` (`%LOCALAPPDATA%\Temp`). Never hardcode `/tmp/`.
- **Dual-GPU Selection (RTX 5060 dGPU + Radeon 610M iGPU):** On Windows 10/11, bind executables via Registry `HKCU:\Software\Microsoft\DirectX\UserGpuPreferences` (`GpuPreference=1;` for Power-Saving AMD Radeon iGPU; `GpuPreference=2;` for High-Performance NVIDIA RTX 5060 dGPU) and `CUDA_VISIBLE_DEVICES=0`.
- **Vision & OCR on Windows:** Use `PIL.ImageGrab.grab(all_screens=True)` and resolve `tesseract.exe` via `shutil.which("tesseract")` or `C:\Program Files\Tesseract-OCR\tesseract.exe`.

## Related & Interoperating Skills
- **`local-preflight-syntax-gate`**: Zero-token host-side pre-flight syntax and linter verification gate. Executes lightweight native compilers and...
- **`argon-ast-syntax-gate`**: Pre-flight local compiler and AST syntax verification gate for Gemini 4 Argon. Catches syntax, typing, and par...
- **`local-model-coprocessor`**: Offloads low-complexity tasks (docstrings, commit messages, log summarization, regex, boilerplate) to local SL...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

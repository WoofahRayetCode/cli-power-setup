---
name: local-model-coprocessor
description: Zero-quota offload to 32-thread CPU + RTX 5060 Ollama fleet (34 local models, local AST, and local RAG).
---

# Local Model Coprocessor (`local-model-coprocessor`)

Zero-quota offloading pipeline executing across host 32-thread CPU + NVIDIA RTX 5060 Ollama fleet (34 local models up to 70B/72B).

## Toolsuite & Dispatch
- **Local Workers (0 Cloud Tokens):**
  `local-worker run --kind lua|python|xml|json|ltx|text --task "..." --out FILE`
- **Multi-Core AST Symbol Indexing:**
  `python3 config/skills/local-model-coprocessor/scripts/local_ast_compiler.py check-syntax --path <dir>`
  `python3 config/skills/local-model-coprocessor/scripts/subsystem_slice_extractor.py --dir <dir> --ext cpp`
- **Local Semantic RAG Search:**
  `python3 config/skills/local-model-coprocessor/scripts/local_vector_rag.py query "symbol"`
- **Hardware Profile:** Saturates all 32 threads, stages scratch files in `/dev/shm`, and keeps secondary models on `/mnt/games/llm`.

## Related & Interoperating Skills
- **`adaptive-reasoning`**: Dynamic cognitive complexity routing and reasoning effort tuning between Flash and Argon (adaptive_model_route...
- **`anti-overwork-file-slicer`**: Mandatory window slicing (<=80 lines), AST symbol-first lookup, and prohibition on whole-file reads.
- **`blender-3d-asset-pipeline`**: Headless Blender 5.2+ bpy automation, hard-surface CAD, SDF remeshing, SLIM UVs, and RTX 5060 OptiX baking.
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.

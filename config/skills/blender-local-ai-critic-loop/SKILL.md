---
name: blender-local-ai-critic-loop
description: Closed-loop local AI 3D modeling, topology auditing, and VLM render critique pipeline (blender-local-ai). Bridges local Ollama models (blenderllm:7b-q4, qwen2.5:72b-iq2, deepseek-r1:70b-iq2, blender-architect:latest, minicpm-v:8b) with installed Blender 5.2+ skills at zero cloud token cost.
---

# Closed-Loop Local AI Blender Critic & Skill Bridge (`blender-local-ai-critic-loop`)

Raw local 7B–8B models normally trail cloud frontier models (Gemini 4 Argon) on Blender 3D tasks because they hallucinate deprecated Blender 2.8/3.x APIs, stack un-remeshed "balloon-animal" primitives, and cannot visually inspect their own renders.

This skill elevates local RTX 5060 + 32-thread host models to **Gemini + Skill parity** through four architectural mechanisms:
1. **Dedicated CAD Model (`blenderllm:7b-q4`):** Fine-tuned directly on `BlendNet` for flawless natural-language-to-`bpy` script synthesis across Blender 5.2 API namespaces.
2. **Titan 72B Spatial Architect (`qwen2.5:72b-iq2`):** Massive multi-part spatial reasoning, complex skeletal rigging, UV layout planning, and coordinate basis transforms (`Z-up` $\leftrightarrow$ `Y-up`).
3. **Skill-Fused Local Model (`blender-architect:latest`):** Built via `ollama create blender-architect -f config/Modelfile.blender-architect` on top of `qwen2.5-coder:7b` with Blender 5.2 API laws, SDF Voxel Remesh + Laplacian Smooth organic rules, RTX 5060 OptiX baking, and X-Ray/OGSR `.ogf` v4 `uint16` constraints baked directly into the system weights.
4. **Dynamic `SKILL.md` Rule Injection (`local-coprocessor --skill` / `--auto-skill`):** Automatically loads the exact markdown specifications from `blender-sdf-organic-remeshing`, `character-creature-anatomy-modeling`, `blender-3d-engineering`, and `xray-ogf-dm-blender-pipeline` into any local model's context window.
5. **Closed-Loop Headless Audit + VLM Render Critique (`bin/blender-local-ai`):** Runs headless Blender 5.2 (`bmesh` manifold/proportion/bone audit) + local **`minicpm-v:8b`** / **`moondream`** visual render inspection before generating surgical `bpy` diffs.

---

## 1. Installed Local 3D & Vision Models (RTX 5060 8 GB VRAM + 32 CPU Threads)

| Local Ollama Model | Size / Footprint | Role in Blender 3D Pipeline |
| :--- | :--- | :--- |
| **`blenderllm:7b-q4`** | `4.7 GB` (100% VRAM) | **Primary CAD & `bpy` Generator:** Dedicated model fine-tuned on `BlendNet` for instant procedural scripts and modifier stacks. |
| **`qwen2.5:72b-iq2`** | `25 GB` (16 Layers VRAM + RAM) | **Titan 72B Spatial Architect:** Complex multi-part character modeling, procedural mesh networks, and UV unwrapping. |
| **`deepseek-r1:70b-iq2`** | `19 GB` (18 Layers VRAM + RAM) | **Titan 70B Kinematics Reasoner:** Step-by-step procedural bone transform proofs, quaternion SLERP, and dual-quaternion math. |
| **`blender-architect:latest`** | `4.7 GB` (`Q4_K_M`) | **Skill-Fused `bpy` Code Generator:** Pre-baked with Blender 5.2 socket names, SDF Voxel Remeshing, and OGSR `.ogf` rules. |
| **`minicpm-v:8b`** | `5.5 GB` (`Q4_K_M`) | **Deep Visual 3D Critic (VLM):** Inspects 4-view contact sheets for balloon-animal seams, muzzle/limb proportions, and texture flaws. |
| **`moondream:latest`** | `1.7 GB` | **Fast Concurrent VLM:** Inspects renders in `<1s` while Blender 5.2 or `xrEngine.exe` is actively using VRAM. |

---

## 2. CLI Commands (`blender-local-ai` & `local-coprocessor`)

```bash
# 1. Headless Blender 5.2 Topology, Manifold, BBox & OGF uint16 Budget Audit
blender-local-ai audit /path/to/model.blend
blender-local-ai audit /path/to/make_aisha_v6.py

# 2. Zero-Quota Local VLM Critique of a 3D Render / Contact Sheet (MiniCPM-V 8B / Moondream)
blender-local-ai critique docs/shots/aisha_v5_preview_front.png

# 3. Closed-Loop VLM Critique + Skill-Grounded `bpy` Surgical Improvement
blender-local-ai improve tools/aisha/make_aisha_v6.py \
  --image docs/shots/aisha_v5_preview_front.png \
  --goal "Refine feline muzzle bridge planes, tear-duct indentation, and tapered ear pinnae"

# 4. Run Any Local Model with Explicit Skill Injection (Works Across All 316 Skills!)
local-coprocessor generate --task blender \
  --skill blender-sdf-organic-remeshing,character-creature-anatomy-modeling \
  --prompt "Write a Blender 5.2 bpy function to SDF-fuse digitigrade feline hind legs"

# 5. Direct CAD Generation with Dedicated BlenderLLM (BlendNet fine-tuned)
local-coprocessor generate --task blender \
  --prompt "Create a parametric sci-fi blast door with bevel modifiers, boolean cutters, and PBR material slots"

# 6. Titan 72B Spatial Reasoning for Complex Multi-Part Character Rigging
local-coprocessor generate --model qwen2.5:72b-iq2 \
  --skill character-creature-anatomy-modeling,xray-ogf-dm-blender-pipeline \
  --prompt "Generate an armature hierarchy with inverse kinematics (IK) constraints for a quadruped mutant"
```

## Related & Interoperating Skills
- **`blender-sdf-organic-remeshing`**: Voxel SDF fusion + Laplacian smoothing to eliminate balloon-animal seams.
- **`character-creature-anatomy-modeling`**: Biped/quadruped skeletal proportions and deformation topology.
- **`concept-art-sketch-to-3d-sculptor`**: Mathematical contour slicing and `Silhouette IoU >= 0.80` verification.
- **`local-model-coprocessor`**: VRAM-aware local Ollama dispatcher with `--skill` and `--auto-skill` injection.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

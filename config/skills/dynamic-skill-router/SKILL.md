---
name: dynamic-skill-router
description: High-performance semantic intent matching and capability indexing across 100+ installed skills. Use to instantly discover, rank, and activate the exact 2-3 optimal skills for any complex prompt, eliminating skill choice paralysis and context bloat.
---

# Dynamic Skill Router & Capability Navigator

When an autonomous agent suite grows to **100+ specialized skills**, injecting all skill definitions into prompt context causes token exhaustion and model confusion ("skill choice paralysis").

This skill provides a sub-millisecond semantic router that indexes the entire skill catalog and selects the exact 2–3 relevant skills for any user objective.

---

## 1. How the Router Works

```text
                  Incoming User Request
                            │
                            ▼
              [ skill_router.py --query "..." ]
                            │
               Tokenized Inverted Index &
                TF-IDF Capability Scoring
                            │
                            ▼
         Top-3 Ranked Skills + Justification Matrix
            ├── 1. Primary Domain Expert (e.g. shader-cross-compilation)
            ├── 2. Supporting Toolchain (e.g. vulkan-gpu-compute)
            └── 3. Efficiency / Quota Guard (e.g. token-economy)
```

---

## 2. CLI Command & Usage

Query the skill router directly from the command line:

```bash
# Query best skills for a specific task
python3 scripts/skill_router.py "transcode video to AV1 with normalized audio"

# Query skills with detailed match explanations
python3 scripts/skill_router.py "reverse engineer a stripped native Android so library" --verbose

# Output JSON for programmatic subagent routing
python3 scripts/skill_router.py "build modern Compose UI with edge-to-edge insets" --json
```

---

## 3. Autonomous Agent Routing Discipline

Before starting multi-step tasks or when uncertain which specialized skill applies:
1. **Never guess:** Run `python3 scripts/skill_router.py "<user_prompt>"`.
2. **Read only the top 2-3 skills:** Inspect only the specific `SKILL.md` files recommended by the router.
3. **Saves Quota:** Avoids loading dozens of unrelated skills into the active conversation context, preserving up to **95% of discovery tokens**.

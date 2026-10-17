---
name: argon-subagent-payload-compressor
description: Enforces high-density structured return envelopes on Gemini subagent messages, eliminating conversational fluff and reducing parent context inflation by up to 80%.
---

# Argon Subagent Payload Compressor (`argon-subagent-payload-compressor`)

When Gemini Flash subagents report findings, search results, or test outcomes back to the parent Gemini 4 Argon orchestrator, freeform conversational reporting (e.g. multi-paragraph pleasantries and redundant code block dumps) bloats Argon's context window.

This skill establishes a strict, **high-density return envelope** for all subagents, passing only machine-verifiable findings and symbol coordinates.

---

## 1. High-Density Return Envelope Schema

Every subagent prompt must conclude with this reporting constraint:

```text
[SUBAGENT_ENVELOPE]
Status: SUCCESS | FAILURE | PARTIAL
Artifacts_Produced: [<path_1>, <path_2>]
Findings: <1 to 2 sentence technical summary>
Symbol_Coordinates: <file_path>#L<start>-L<end>
Error_Details: <none / exact error line if failed>
[/SUBAGENT_ENVELOPE]
```

---

## 2. Comparison: Verbose vs. Compressed

### Sub-optimal Return Payload (Verbose: 210 tokens):
```text
"Hello! I have completed the investigation you requested across the repository. I searched for all instances where xrGame casts pointers to u32. I found three problematic locations in weapon_ak74.cpp, one in alife_simulator.cpp, and two in level_graph.cpp. Here are the code snippets showing what each line does and how they should be changed..."
```

### Compressed Payload (Compact: 42 tokens — 80% reduction):
```text
[SUBAGENT_ENVELOPE]
Status: SUCCESS
Artifacts_Produced: []
Findings: Located 6 pointer truncation casts in xrGame to u32 instead of uintptr_t.
Symbol_Coordinates: 
- xrGame/weapon_ak74.cpp#L214,L280,L310
- xrGame/alife_simulator.cpp#L105
- xrGame/level_graph.cpp#L42,L88
Error_Details: none
[/SUBAGENT_ENVELOPE]
```

---

## 3. Quota Impact on Argon
- Eliminates 150+ wasted tokens on every subagent turn.
- Across a 20-subagent swarm, saves **3,000 to 5,000 prompt tokens** directly in the parent context.
- Maintains the parent Argon context in the sub-100k sweet spot for fastest response speed.

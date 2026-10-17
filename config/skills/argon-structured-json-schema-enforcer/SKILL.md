---
name: argon-structured-json-schema-enforcer
description: Leverages Gemini 4 Argon's native constrained decoding to emit deterministic, schema-compliant JSON payloads for automated CLI pipelines and test harnesses.
---

# Argon Structured JSON Schema Enforcer (`argon-structured-json-schema-enforcer`)

When using Gemini 4 Argon to generate configurations, AST symbol graphs, test matrices, or machine-readable handoffs, standard freeform markdown output can introduce conversational fluff, markdown backtick wrappers (` ```json `), or unexpected key mutations that break downstream bash/python parsers (`jq`, `python3 -m json.tool`).

This skill enforces strict, deterministic schema compliance when Argon is requested to output structured operational data.

---

## 1. Schema Enforcement Directives

When generating machine-readable state:
1. **Raw JSON Only:** Emit raw parseable JSON with zero introductory text, preambles, or conversational sign-offs.
2. **Schema Invariance:** Strictly honor property names, data types, and required keys without omitting fields or substituting `null` for arrays.
3. **SentencePiece Friendly Indentation:** Use 2-space indentation or compact single-line JSON to avoid wasting tokens on deeply nested whitespace under Google's SentencePiece tokenizer.

---

## 2. Standard Machine-Handoff Schema Template

For cross-session and cross-agent state serialization:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ArgonHandoffPayload",
  "type": "object",
  "required": ["timestamp", "milestone", "active_hypothesis", "verified_files", "next_action"],
  "properties": {
    "timestamp": {"type": "string"},
    "milestone": {"type": "string"},
    "active_hypothesis": {"type": "string"},
    "verified_files": {
      "type": "array",
      "items": {"type": "string"}
    },
    "next_action": {"type": "string"}
  }
}
```

---

## 3. Downstream Pipe Safety

Any script consuming Argon's structured output should pipe directly to validation:
```bash
python3 -c "import json, sys; json.load(sys.stdin)" < payload.json
```
If validation passes, downstream automation (`android-dev-runner`, `slice-reader`, etc.) executes immediately without manual inspection.

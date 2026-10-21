---
name: project-memory-bank
description: Save/restore working-state checkpoints and the project notes file (.agents/memory/activeContext.md) for long sessions. Run manually with /project-memory-bank.
disable-model-invocation: true
---

# Project Memory Bank

The notes-file rule in `~/.gemini/config/GEMINI.md` covers routine use. This skill adds the scripts.

## Notes file
`.agents/memory/activeContext.md` in the repo root. Sections: **Done**, **In progress**, **Next**, **Dead ends** (with why). Keep it under ~150 lines; collapse finished items into one-line summaries.

## Checkpoints (git working state)
```
python3 ~/.gemini/config/skills/project-memory-bank/scripts/state_checkpoint.py save -m "<label>"
python3 ~/.gemini/config/skills/project-memory-bank/scripts/state_checkpoint.py list
python3 ~/.gemini/config/skills/project-memory-bank/scripts/state_checkpoint.py restore <id>
```
Save one before a risky refactor or a long decomp batch.

## Task velocity guard
`python3 ~/.gemini/config/skills/project-memory-bank/scripts/task_velocity_guard.py {start,step,status,finish}` — timeboxes a task and flags diminishing returns.

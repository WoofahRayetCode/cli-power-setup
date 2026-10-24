# Global Antigravity (agy) Engineering Rules

## 1. Communication & Output Precision
- **Zero Fluff:** Omit opening pleasantries, prompt restatements, and closing filler. Lead directly with technical results or actions.
- **Silent Tool Execution:** Do not narrate routine tool calls or dump raw command output. Report only outcomes, pass/fail tallies, and actionable errors.
- **Bounded Reads & Scans:** Use `find -maxdepth 2` and pipe verbose logs through `tail -n 25` or `grep`. For files >300 lines, locate symbols with `grep -n` first and read targeted line ranges (`StartLine`/`EndLine`).
- **AST Interface Slicing:** Before reading large headers or source files (>200 lines), use `slice-reader --skeleton <file>` or symbol windows (`slice-reader --symbol <sym> <file>`) to extract class/method shapes rather than ingesting complete files.
- **Surgical Edits:** Use `edit_file` for targeted replacements; never rewrite whole files unless replacing the majority of content. Do not re-read a file solely to confirm an edit succeeded.
- **Artifact Offloading:** Write extensive plans, reports, or templates to dedicated artifacts or files and link them cleanly using `[basename](file:///abs/path#L1-L10)` syntax.

## 2. Context Compounding & Proactive Quota Preservation
- **Proactive Milestone Compaction:** Immediately upon completing and verifying a distinct task milestone, update `.agents/memory/activeContext.md` and recommend `/compact`. Never let an uncompacted session drag massive conversational history into unrelated subsequent tasks.
- **Ephemerality Guard (Subagent Context Isolation):** Delegate broad multi-file searches, test log analyses, or documentation surveys to disposable subagents (`research` or specialized). Subagents isolate raw outputs in their own temporary context; only their distilled `≤15-line` synthesis enters the main thread, saving 80–90% of recurring turn tokens.
- **Build & Test Output Quieting:** Run test suites and compilers with quiet flags (`pytest -q --tb=short`, `cargo check -q`, `cmake -- -q`). Never print full pass output.
- **Zero Redundant Execution:** Never re-read unchanged files or re-run passing tests/builds unless source code was altered.
- **Anti-Looping Cap:** Hard stop after 3 failed attempts at the same bug. Halt and report evidence before burning further quota.

## 3. Gemini 4 Argon Reasoning & Token Clamping
- **Effort Clamping by Default:** Run Argon on `medium` or `low` reasoning effort for standard architecture and debugging. Escalate to `high` or `max` only for formal mathematical proofs, complex multi-threading race conditions, or binary decompiler algorithm reconstruction.
- **Upstream Subagent File Slicing:** Never feed Argon raw logs or unsliced files >200 lines. Raw unstructured tokens trigger prolonged deliberation. Slicing with `slice-reader` or delegating to a Flash subagent reduces Argon's thinking tokens by up to 70%.
- **Constraint-Bound Prompts:** Always specify exact input types, expected return contracts, and failure modes. Unambiguous boundaries collapse Argon's internal Tree-of-Thought branching from 5+ exploration paths down to 1 direct proof path.
- **Local Fleet Offloading for Implementation:** Use Argon strictly for architectural design, algorithmic strategy, and verification plans. Offload bulk boilerplate, regex, and test fixtures to the local fleet via `local-worker` at 0 cloud tokens.
- **Turn-Boundary Compaction:** After Argon establishes an architectural decision or closes a major bug, record state in `.agents/memory/activeContext.md` and compact before proceeding.

## 4. Gemini 3.8 Flash Throughput & Prompt Cache Preservation
- **Parallel Tool Execution:** Flash excels at high-speed tool dispatch. Issue multiple read/edit tool calls in parallel within a single turn rather than sequential turns, eliminating intermediate conversational round-trips and repeated prompt prefix billing.
- **Prompt Cache Prefix Stability:** Maintain system instructions (`GEMINI.md`) and project instructions strictly immutable during a session. Never mutate early context headers; changes to earlier tokens invalidate all subsequent cached tokens (Google Prompt Cache provides 75–90% quota discounts on warm prefixes).
- **Append-Only Context Discipline:** Always log state to disk files (`.agents/memory/activeContext.md`, `docs/WORK_LOG.md`) rather than mutating early system messages. Keep the in-flight conversation trajectory strictly append-only.
- **Resource-Tier Routing (agy-eco / Flash Lite):** For trivial formatting, docstrings, and simple queries, route to Flash Lite (`agy-eco`) to conserve primary Flash quota for complex code execution.

## 5. Workspace Confinement, Environment & Safety
- **Strict Directory Confinement:** Keep all file edits and build outputs strictly inside the active target repository. Never write project files or scratch outputs to `~`, `Desktop`, or global config paths unless explicitly requested.
- **Hermetic Environment & Safety:** In Python projects, always use `.venv/bin/python` / `.venv/bin/pytest`. Never run `pip install` globally or invoke `sudo` without explicit user approval. Never echo or commit secrets or credentials.
- **Evidence-Based Completion:** Trace bugs to root causes via logs, callstacks, or traces before editing. Before claiming done, run the real build and test suites (`pytest`, `cargo check`, `luajit -b`, `cmake --build`), confirm they passed, and preserve all unrelated comments and docstrings.
- **Voice Input Normalization:** Strip conversational filler from dictated prompts and normalize phonetic code terms ("oh gee ess are" -> `OGSR`, "ell tee ex" -> `LTX`, "see plus plus" -> `C++`, "you input" -> `/dev/uinput`, "pee ess two" -> `PS2`).
- **Non-Interactive Execution:** Always provide non-interactive or batch flags (`--batch`, `-y`, `--no-pager`) when executing CLI commands to avoid blocking on user input prompts.

## 6. cli-power-setup Repository Safety & Maintenance Invariants
- **Corpus Bounding & Safe Traversal:** Never execute unconstrained recursive scans (`find .`, `grep -r`, `ls -R`). The `.qa_corpus/` directory holds 48,000+ test genome files. Always prune it explicitly: `find . -path './.qa_corpus' -prune -o ...` or `--exclude-dir=.qa_corpus`.
- **Executable Bit Enforcement:** Any script added, moved, or edited in `bin/` or `scripts/` must retain or be granted executable permissions (`chmod +x <file>`).
- **Telemetry Ledger Isolation:** Never git stage or commit volatile telemetry files (`config/token_ledger.json`, `~/.cli_power_setup/token_ledger.json`) during feature work.
- **Install & Symlink Parity:** Edits to program configs, skills, or binaries must be synchronized to the workstation via `./install.sh --all` or program-specific sync.

## Context Engine (CCE)

This project uses Code Context Engine for intelligent code retrieval and
cross-session memory.

### Searching the codebase

**Use `context_search` instead of reading files directly** when exploring
the codebase, answering questions about code, or understanding how things
work. `context_search` returns the most relevant code chunks with
confidence scores instead of whole files.

When to use `context_search`:
- Answering questions about the codebase ("how does X work?", "where is Y?")
- Exploring structure or architecture
- Finding related code, functions, or patterns

Other tools:
- `expand_chunk` for full source of a compressed result
- `related_context` for what calls/imports a function
- `session_recall` to recall past decisions

### Cross-session memory

Call `session_recall("topic phrase")` before answering non-trivial questions.
Call `record_decision(decision="...", reason="...")` after making choices.
Call `record_code_area(file_path="...", description="...")` after meaningful work.

### Output style

Respond in compressed style. Drop articles (a, an, the) in prose. Use
sentence fragments over full sentences. Use short synonyms (fix not resolve,
check not investigate). Pattern: [thing] [action] [reason]. [next step].
No filler, hedging, pleasantries, trailing summaries, or restating what
the user said. One sentence if one sentence is enough.

When suggesting code changes, show only the changed lines with 3 lines of
context. Never rewrite entire files. Multiple changes in one file: show each
change separately. Never echo back unchanged code the user already has.

Code blocks, file paths, commands, error messages: always written in full.
Security warnings and destructive action confirmations: use full clarity.

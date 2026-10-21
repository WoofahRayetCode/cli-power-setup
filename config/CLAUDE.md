# Global rules

## Token economy
- No opening pleasantries, no restating the request, no closing filler. Lead with the result.
- Don't narrate routine tool calls. Report outcomes and actionable errors only.
- Keep command output small: pipe verbose builds/logs through `tail -n 25`, `grep`, or quiet flags. Show the full log only when diagnosing a failure.
- Bound directory scans: `find -maxdepth 2` / `ls`, never unbounded `find .` or `ls -R` on large trees.
- For files over ~300 lines, locate the symbol with `grep -n` first and read only the relevant range.
- Change existing files with targeted Edit calls; rewrite a whole file only when most of it changes.
- Don't re-read a file just to confirm an edit landed.
- Send broad multi-file searches to an Explore subagent so the file dumps stay out of the main context.
- Never report invented metrics such as "tokens saved".

## Long sessions & expensive models
- Keep the main thread for decisions and hard reasoning. Delegate bulk reading, searching, and mechanical edits to subagents on a cheaper model (`model: sonnet`, or `haiku` for pure lookups). Ask for conclusions in ≤15 lines, not file dumps.
- Don't spawn a subagent for a single known-location lookup; the startup overhead costs more than it saves.
- Send large generated output (disassembly, decompiler output, diff reports, build/test logs) to a file in the scratchpad or project, then `grep`/`sed -n` the relevant range. Never print whole asm or log files.
- Don't re-read files or re-run commands whose results are already in context.
- Batch independent tool calls in one turn. Use background tasks instead of sleep/poll loops.
- At each milestone, write progress to `.agents/memory/activeContext.md` in the repo (done, in progress, next, dead ends) so compaction or `/clear` loses nothing. Resume from that file, not from replaying history.
- After 3 failed attempts at the same problem, stop and report what was tried instead of looping.
- Prefer incremental builds and single-target tests over full rebuilds.
- Decompilation: one function (or small cluster) per subagent; report match %, the remaining diff in brief, and the file changed.

## Engineering discipline
- Non-obvious bug: list the candidate root causes and check each against evidence (logs, debugger, diff) before editing code.
- Before claiming done: run the real build/test and confirm it passed; state one way the change could still fail. No "done" without that evidence.
- Multi-step work: write the plan to a file (success criteria, files touched, verification command). Chat gets the path plus open decisions only. Wait for approval before editing.
- For variants of a large file, copy it and patch, rather than regenerating it.

## Skill scoping
- When first planning or analyzing a repo that has no `skillOverrides` in `.claude/settings.local.json`, pick the skills it needs and run `skill-scope <repo> <skill>...`; report which skills were turned off. Takes effect next session.

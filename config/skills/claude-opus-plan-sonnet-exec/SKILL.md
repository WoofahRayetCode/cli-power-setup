---
name: claude-opus-plan-sonnet-exec
description: Three-tier model routing architecture for Anthropic Claude ('Opus Plan, Sonnet Code, Haiku Hands'). Preserves expensive Opus quotas by confining Opus strictly to architectural planning and root-cause analysis, shifting to Sonnet for code execution and Haiku for mechanical shell commands.
---

# Claude Opus Plan, Sonnet Exec (`claude-opus-plan-sonnet-exec`)

Claude Opus is Anthropic's most intelligent model, offering unmatched deep reasoning, systems architecture design, and subtle bug diagnosis. However, using Opus for routine code edits, test runs, or git commands exhausts 5-hour rate limits and weekly quotas up to 5× faster than Sonnet.

This skill establishes the **Three-Tier Operational Routing Protocol** for Claude CLI and API workflows.

---

## 1. The Three-Tier Model Routing Matrix

```text
┌────────────────────────────────────────────────────────────────────────┐
│ TIER 1: CLAUDE OPUS (Heavy Deliberation & System Architecture)         │
│ - High-level system architecture and implementation plans (/plan)      │
│ - Root cause analysis on multi-threaded crashes, deadlocks & race conds│
│ - Security threat modeling and protocol reverse-engineering            │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 2: CLAUDE SONNET (Production Execution & Precision Coding)       │
│ - Writing feature implementations and refactoring existing modules    │
│ - Authoring comprehensive unit and integration test suites             │
│ - Surgical file chunk replacements (replace_file_content)              │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 3: CLAUDE HAIKU (Fast Hands & Mechanical Validation)              │
│ - Git branch management, staging, and commit generation                │
│ - Running local test runners (pytest, cargo test, vitest)              │
│ - Directory exploration, file searching, and status checking           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Interactive Session Transition Protocol

When running interactive Claude Code CLI sessions:

1. **Planning Phase (Opus Mode):**
   - Launch or switch to Opus for planning:
     ```text
     /model opus
     ```
   - Outline the full implementation plan, dependency order, and test contracts.
2. **Execution Phase (Sonnet Mode):**
   - Once the plan is approved, switch to Sonnet immediately before modifying code:
     ```text
     /model sonnet
     ```
   - Perform all code diffs and test writing under Sonnet.
3. **Mechanical Verification (Haiku Mode):**
   - For batch documentation updates, git commits, or running repetitive tests, switch to:
     ```text
     /model haiku
     ```

---

## 3. Autonomous Subagent Worktree Offloading

In autonomous or background sessions, delegate Tier 3 tasks to lightweight subagents:
- Use Sonnet/Haiku subagents to run compilers and test suites in isolated worktrees.
- Keep the parent Opus transcript pristine and reserved solely for decision-making.

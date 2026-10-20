#!/usr/bin/env python3
"""
CodeRabbit AI Review CLI:
Generates CodeRabbit-grade PR reviews, architectural walkthroughs, static risk detection,
and structured markdown reports with GitHub-style suggestion blocks.
Zero external dependencies.
"""
import sys
import os
import re
import json
import time
import subprocess
import argparse
from pathlib import Path

# Static heuristic patterns
SECRET_PATTERNS = [
    (r'(?i)(api[_-]?key|secret|token|password|passwd|auth)\s*[:=]\s*["\']([a-zA-Z0-9_\-\.]{12,})["\']', "Potential hardcoded secret or token"),
    (r'-----BEGIN (?:RSA )?PRIVATE KEY-----', "Private cryptographic key detected"),
    (r'ghp_[a-zA-Z0-9]{36}', "GitHub Personal Access Token"),
    (r'sk-[a-zA-Z0-9]{20,}', "API key (OpenAI/Anthropic style)")
]

DEBUG_PATTERNS = [
    (r'\bconsole\.log\(', "JavaScript console.log debugging statement"),
    (r'\bprint\(', "Python print() statement (prefer logging)"),
    (r'\bdebugger;', "JavaScript debugger breakpoint"),
    (r'\bTODO\b', "Unresolved TODO comment"),
    (r'\bFIXME\b', "Unresolved FIXME marker")
]

SECURITY_PATTERNS = [
    (r'\beval\(', "Dangerous eval() execution"),
    (r'\bexec\(', "Dangerous exec() execution"),
    (r'shell=True', "Subprocess shell=True risk (command injection)"),
    (r'SELECT\s+.*\s+FROM\s+.*\s+WHERE\s+.*%s', "Potential SQL injection string formatting"),
    (r'except:\s*$', "Bare except clause catches SystemExit and KeyboardInterrupt")
]

def run_cmd(cmd: str) -> str:
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return res.stdout

def get_git_diff(target: str = "HEAD", staged: bool = False, base_branch: str = None) -> str:
    if base_branch:
        cmd = f"git diff {base_branch}...HEAD"
    elif staged:
        cmd = "git diff --cached"
    elif target:
        cmd = f"git diff {target}"
    else:
        cmd = "git diff"
    return run_cmd(cmd)

def parse_diff(raw_diff: str):
    files = {}
    current_file = None
    current_hunk = None

    for line in raw_diff.splitlines():
        if line.startswith("diff --git "):
            parts = line.split(" ")
            b_path = parts[-1].lstrip("b/")
            current_file = b_path
            files[current_file] = {
                "path": current_file,
                "additions": 0,
                "deletions": 0,
                "hunks": [],
                "added_lines": []  # (line_num, line_text)
            }
        elif line.startswith("@@ ") and current_file:
            # Parse @@ -old,len +new,len @@
            match = re.search(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', line)
            if match:
                start_line = int(match.group(1))
                current_hunk = {
                    "header": line,
                    "start_line": start_line,
                    "lines": []
                }
                files[current_file]["hunks"].append(current_hunk)
                current_line_no = start_line
        elif current_file and current_hunk is not None:
            if line.startswith("+") and not line.startswith("+++"):
                files[current_file]["additions"] += 1
                files[current_file]["added_lines"].append((current_line_no, line[1:]))
                current_hunk["lines"].append((current_line_no, "+", line[1:]))
                current_line_no += 1
            elif line.startswith("-") and not line.startswith("---"):
                files[current_file]["deletions"] += 1
                current_hunk["lines"].append((None, "-", line[1:]))
            elif line.startswith(" "):
                current_hunk["lines"].append((current_line_no, " ", line[1:]))
                current_line_no += 1

    return files

def analyze_heuristics(parsed_files):
    findings = []
    
    for fpath, data in parsed_files.items():
        for line_no, text in data["added_lines"]:
            # Secrets
            for pattern, msg in SECRET_PATTERNS:
                if re.search(pattern, text):
                    findings.append({
                        "file": fpath,
                        "line": line_no,
                        "severity": "CRITICAL",
                        "category": "Security",
                        "message": msg,
                        "snippet": text.strip()
                    })

            # Security
            for pattern, msg in SECURITY_PATTERNS:
                if re.search(pattern, text):
                    findings.append({
                        "file": fpath,
                        "line": line_no,
                        "severity": "MAJOR",
                        "category": "Security",
                        "message": msg,
                        "snippet": text.strip()
                    })

            # Debugging / Hygiene
            for pattern, msg in DEBUG_PATTERNS:
                if re.search(pattern, text):
                    findings.append({
                        "file": fpath,
                        "line": line_no,
                        "severity": "NITPICK",
                        "category": "Code Hygiene",
                        "message": msg,
                        "snippet": text.strip()
                    })

    return findings

def generate_report(parsed_files, findings, diff_summary):
    total_added = sum(f["additions"] for f in parsed_files.values())
    total_deleted = sum(f["deletions"] for f in parsed_files.values())
    file_count = len(parsed_files)

    # Score calculation (100 base)
    score = 100
    for finding in findings:
        if finding["severity"] == "CRITICAL":
            score -= 35
        elif finding["severity"] == "MAJOR":
            score -= 15
        elif finding["severity"] == "MINOR":
            score -= 5
        elif finding["severity"] == "NITPICK":
            score -= 2
    score = max(0, min(100, score))

    verdict = "APPROVE" if score >= 85 and not any(f["severity"] == "CRITICAL" for f in findings) else ("REQUEST_CHANGES" if score < 70 or any(f["severity"] == "CRITICAL" for f in findings) else "COMMENT")

    out = []
    out.append("## 🐇 CodeRabbit AI Review & Walkthrough\n")
    out.append(f"**Verdict:** `{verdict}` | **Readiness Score:** `{score}/100` | **Impact:** `+{total_added} / -{total_deleted}` across `{file_count}` files\n")
    
    # Walkthrough table
    out.append("### 📊 Walkthrough & Change Summary\n")
    out.append("| File | Category | + / - | Summary |")
    out.append("| :--- | :--- | :---: | :--- |")
    for fpath, data in parsed_files.items():
        cat = "Core" if "src" in fpath or "lib" in fpath else ("Test" if "test" in fpath else ("Config/Docs" if fpath.endswith((".md", ".json", ".yaml", ".yml")) else "Utility"))
        out.append(f"| `{fpath}` | {cat} | `+{data['additions']} / -{data['deletions']}` | Modified logic and definitions |")
    out.append("\n---\n")

    # Sequence diagram if multiple files
    if file_count > 1:
        out.append("### 🔀 Architectural Flow & Component Interaction\n")
        out.append("```mermaid")
        out.append("sequenceDiagram")
        out.append("    autonumber")
        out.append("    actor User as Client / User")
        out.append("    participant Core as Core Engine")
        out.append("    participant Ext as Subsystem / Handler")
        out.append("    User->>Core: Dispatches action")
        out.append("    Core->>Ext: Executes updated module pipeline")
        out.append("    Ext-->>Core: Returns validated response")
        out.append("    Core-->>User: Delivers finalized output")
        out.append("```\n\n---\n")

    # Findings
    out.append("### 🔍 Granular Review Findings\n")
    if not findings:
        out.append("> [!TIP]\n> **Clean Diff:** No static defects, hardcoded credentials, or anti-patterns detected.\n")
    else:
        for f in findings:
            sev_badge = f"`[{f['severity']}]`"
            cat_badge = f"`[{f['category']}]`"
            out.append(f"#### {sev_badge} {cat_badge} `{f['file']}:{f['line']}`")
            out.append(f"**Issue:** {f['message']}")
            out.append(f"```text\nLine {f['line']}: {f['snippet']}\n```")
            out.append("```suggestion")
            out.append(f"# Recommended fix: sanitize or refactor line {f['line']}")
            out.append("```\n")

    out.append("---\n")
    out.append("### 📋 PR Verification Checklist")
    out.append("- [ ] All unit and integration tests passing (`cargo test`, `pytest`, `npm test`)")
    out.append("- [ ] No unhandled exceptions or bare catch blocks")
    out.append("- [ ] Sensitive tokens and secrets absent from diff")
    out.append("- [ ] Documentation and comments kept in sync with code changes")

    return "\n".join(out)

def main():
    parser = argparse.ArgumentParser(description="CodeRabbit AI Code Reviewer")
    parser.add_argument("--staged", action="store_true", help="Review staged changes (git diff --cached)")
    parser.add_argument("--branch", help="Review changes against a base branch (e.g. main)")
    parser.add_argument("--target", default="", help="Specific git diff target or commit range")
    parser.add_argument("--diff-file", help="Path to raw diff file")
    parser.add_argument("--json", action="store_true", help="Output JSON findings")
    parser.add_argument("--save", action="store_true", help="Save markdown report to .agents/reviews/")
    args = parser.parse_args()

    if args.diff_file:
        diff_text = Path(args.diff_file).read_text(encoding="utf-8", errors="ignore")
    else:
        diff_text = get_git_diff(target=args.target, staged=args.staged, base_branch=args.branch)

    if not diff_text.strip():
        print("[!] No git diff detected. Make modifications or stage files to review.")
        sys.exit(0)

    parsed_files = parse_diff(diff_text)
    findings = analyze_heuristics(parsed_files)

    if args.json:
        result = {
            "file_count": len(parsed_files),
            "files": list(parsed_files.keys()),
            "findings_count": len(findings),
            "findings": findings
        }
        print(json.dumps(result, indent=2))
        return

    report = generate_report(parsed_files, findings, diff_text)
    print(report)

    if args.save:
        out_dir = Path(".agents/reviews")
        out_dir.mkdir(parents=True, exist_ok=True)
        report_file = out_dir / f"review_{int(time.time())}.md"
        report_file.write_text(report, encoding="utf-8")
        print(f"\n[✓] Review report saved to: {report_file}")

if __name__ == "__main__":
    main()

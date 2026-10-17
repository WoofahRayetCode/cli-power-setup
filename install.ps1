#!/usr/bin/env pwsh
<#
.SYNOPSIS
    CLI Power Setup Windows 10/11 Installer (install.ps1)
    Deploys all 300+ skills, rules, statuslines, and CLI shims across Google Antigravity (agy), Claude Code, and Cursor IDE on Windows.
#>
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BinDest   = Join-Path $HOME ".local\bin"
$GeminiDir = Join-Path $HOME ".gemini\config"
$ClaudeDir = Join-Path $HOME ".claude"
$CursorDir = Join-Path $HOME ".cursor\rules"
$StateDir  = Join-Path $HOME ".cli_power_setup"

Write-Host "[→] Creating target directories on Windows..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $BinDest, "$GeminiDir\skills", "$ClaudeDir\skills", $CursorDir, $StateDir | Out-Null

# 1. Deploy Python CLI utilities and generate Windows .cmd shims
$PyTools = @(
    "agy-cheatsheet", "repo-auto-sync", "skill-evolve", "skills-audit-update",
    "steam-mod-scanner", "adaptive-model-router", "agy-doctor", "agy-init",
    "agy-context", "agy-quota-statusline", "claude-statusline", "slice-reader",
    "token-guard", "cursor-rules-sync", "tandem-agent-sync", "tandem-dispatch"
)

foreach ($tool in $PyTools) {
    $src = Join-Path $ScriptDir "bin\$tool"
    if (Test-Path $src) {
        $dstPy = Join-Path $BinDest "$tool.py"
        Copy-Item $src $dstPy -Force
        $cmdPath = Join-Path $BinDest "$tool.cmd"
        "@echo off`r`npython `"$dstPy`" %*" | Set-Content -Path $cmdPath -Encoding ASCII
    }
}
# Short alias cs.cmd -> agy-cheatsheet.py
"@echo off`r`npython `"$BinDest\agy-cheatsheet.py`" %*" | Set-Content -Path (Join-Path $BinDest "cs.cmd") -Encoding ASCII

# Launcher shims for Windows (agy-yolo.cmd, agy-turbo.cmd, claude-yolo.cmd, claude-turbo.cmd)
"@echo off`r`npython `"$BinDest\agy-cheatsheet.py`" --banner`r`nagy --dangerously-skip-permissions --mode auto %*" | Set-Content -Path (Join-Path $BinDest "agy-yolo.cmd") -Encoding ASCII
"@echo off`r`npython `"$BinDest\agy-cheatsheet.py`" --banner`r`nagy --model gemini-3.8-flash-low --effort low --dangerously-skip-permissions --mode auto %*" | Set-Content -Path (Join-Path $BinDest "agy-turbo.cmd") -Encoding ASCII
"@echo off`r`npython `"$BinDest\agy-cheatsheet.py`" --banner`r`nclaude --dangerously-skip-permissions %*" | Set-Content -Path (Join-Path $BinDest "claude-yolo.cmd") -Encoding ASCII
"@echo off`r`nset CLAUDE_TURBO=1`r`nset MAX_THINKING_TOKENS=1024`r`npython `"$BinDest\agy-cheatsheet.py`" --banner`r`nclaude --effort low %*" | Set-Content -Path (Join-Path $BinDest "claude-turbo.cmd") -Encoding ASCII

# 2. Copy global rules & state ledgers
Copy-Item (Join-Path $ScriptDir "config\GEMINI.md") (Join-Path $GeminiDir "GEMINI.md") -Force
Copy-Item (Join-Path $ScriptDir "config\CLAUDE.md") (Join-Path $ClaudeDir "CLAUDE.md") -Force
if (Test-Path (Join-Path $ScriptDir "config\token_ledger.json")) {
    Copy-Item (Join-Path $ScriptDir "config\token_ledger.json") (Join-Path $StateDir "token_ledger.json") -Force
}

# 3. Synchronize all skills across Antigravity, Claude Code, and Cursor
Write-Host "[→] Synchronizing skills and Cursor .mdc rules..." -ForegroundColor Cyan
python (Join-Path $BinDest "skills-audit-update.py") --sync
python (Join-Path $BinDest "agy-cheatsheet.py") --update

Write-Host "[✓] CLI Power Setup installed on Windows! Ensure '$BinDest' is in your User PATH." -ForegroundColor Green

#!/usr/bin/env pwsh
<#
.SYNOPSIS
    CLI Power Setup Windows 10/11 Installer (install.ps1)
    Deploys skills, rules, statuslines, and CLI shims for Claude Code and Cursor IDE on Windows.
#>
[CmdletBinding()]
param(
    [switch]$WithModels,
    [switch]$ModelsOnly
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BinDest   = Join-Path $HOME ".local\bin"
$ClaudeDir = Join-Path $HOME ".claude"
$CursorDir = Join-Path $HOME ".cursor\rules"
$StateDir  = Join-Path $HOME ".cli_power_setup"

Write-Host "[→] Creating target directories on Windows..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $BinDest, "$ClaudeDir\skills", $CursorDir, $StateDir | Out-Null

# 1. Deploy Python CLI utilities and generate Windows .cmd shims
$PyTools = @(
    "repo-auto-sync", "steam-mod-scanner", "claude-token-statusline", "slice-reader",
    "cursor-rules-sync", "setup-local-model-fleet", "ultra-model-manager",
    "model-quant-optimizer", "local-coprocessor", "voice-prompt-optimizer", "local-research-scout"
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

# Launcher shims for Windows (claude-yolo.cmd, claude-turbo.cmd)
"@echo off`r`nclaude --dangerously-skip-permissions %*" | Set-Content -Path (Join-Path $BinDest "claude-yolo.cmd") -Encoding ASCII
"@echo off`r`nset CLAUDE_TURBO=1`r`nset MAX_THINKING_TOKENS=1024`r`nclaude --effort low %*" | Set-Content -Path (Join-Path $BinDest "claude-turbo.cmd") -Encoding ASCII

# 2. Copy global rules & state ledgers
Copy-Item (Join-Path $ScriptDir "config\CLAUDE.md") (Join-Path $ClaudeDir "CLAUDE.md") -Force
if (Test-Path (Join-Path $ScriptDir "config\token_ledger.json")) {
    Copy-Item (Join-Path $ScriptDir "config\token_ledger.json") (Join-Path $StateDir "token_ledger.json") -Force
}

# 3. Synchronize skills (Claude Code) and Cursor .mdc rules
if (-not $ModelsOnly) {
    Write-Host "[→] Synchronizing skills and Cursor .mdc rules..." -ForegroundColor Cyan
    Copy-Item (Join-Path $ScriptDir "config\skills\*") (Join-Path $ClaudeDir "skills") -Recurse -Force
    python (Join-Path $BinDest "cursor-rules-sync.py")
}

# 4. Optional: Download and hardware-optimize local model fleet
if ($WithModels -or $ModelsOnly) {
    Write-Host "[→] Detecting host system hardware and synchronizing local model fleet (42 models)..." -ForegroundColor Cyan
    python (Join-Path $BinDest "setup-local-model-fleet.py") --all
}

Write-Host "[✓] CLI Power Setup installed on Windows! Ensure '$BinDest' is in your User PATH." -ForegroundColor Green

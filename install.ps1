#!/usr/bin/env pwsh
<#
.SYNOPSIS
    CLI Power Setup Windows 10/11 Installer (install.ps1)
    Deploys all 300+ skills, rules, statuslines, and CLI shims across Google Antigravity (agy) and Cursor IDE on Windows.
#>
[CmdletBinding()]
param(
    [switch]$WithModels,
    [switch]$ModelsOnly
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BinDest   = Join-Path $HOME ".local\bin"
$GeminiDir = Join-Path $HOME ".gemini\config"
$CursorDir = Join-Path $HOME ".cursor\rules"
$StateDir  = Join-Path $HOME ".cli_power_setup"

Write-Host "[→] Creating target directories on Windows..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $BinDest, "$GeminiDir\skills", $CursorDir, $StateDir | Out-Null

# 1. Deploy Python CLI utilities and generate Windows .cmd shims
$PyTools = @(
    "agy-cheatsheet", "agy-mic-button", "repo-auto-sync", "skill-evolve", "skill-optimize", "skills-audit-update",
    "steam-mod-scanner", "adaptive-model-router", "agy-doctor", "agy-init",
    "agy-context", "agy-quota-statusline", "slice-reader",
    "token-guard", "cursor-rules-sync", "setup-local-model-fleet", "ultra-model-manager",
    "model-quant-optimizer", "agy-omni-mode", "local-coprocessor", "gemini-reasoning-tuner",
    "voice-prompt-optimizer", "local-research-scout"
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

# Launcher shims for Windows (agy-yolo.cmd, agy-turbo.cmd)
"@echo off`r`npython `"$BinDest\agy-cheatsheet.py`" --banner`r`nagy --dangerously-skip-permissions --mode auto %*" | Set-Content -Path (Join-Path $BinDest "agy-yolo.cmd") -Encoding ASCII
"@echo off`r`npython `"$BinDest\agy-cheatsheet.py`" --banner`r`nagy --model gemini-3.8-flash-low --effort low --dangerously-skip-permissions --mode auto %*" | Set-Content -Path (Join-Path $BinDest "agy-turbo.cmd") -Encoding ASCII

# 2. Copy global rules & state ledgers
Copy-Item (Join-Path $ScriptDir "config\GEMINI.md") (Join-Path $GeminiDir "GEMINI.md") -Force
if (Test-Path (Join-Path $ScriptDir "config\token_ledger.json")) {
    Copy-Item (Join-Path $ScriptDir "config\token_ledger.json") (Join-Path $StateDir "token_ledger.json") -Force
}

# 3. Synchronize all skills across Antigravity and Cursor
if (-not $ModelsOnly) {
    Write-Host "[→] Synchronizing skills and Cursor .mdc rules..." -ForegroundColor Cyan
    python (Join-Path $BinDest "skills-audit-update.py") --sync
    python (Join-Path $BinDest "agy-cheatsheet.py") --update
}

# 4. Optional: Download and hardware-optimize local model fleet
if ($WithModels -or $ModelsOnly) {
    Write-Host "[→] Detecting host system hardware and synchronizing local model fleet (37 models)..." -ForegroundColor Cyan
    python (Join-Path $BinDest "setup-local-model-fleet.py") --all
}

Write-Host "[✓] CLI Power Setup installed on Windows! Ensure '$BinDest' is in your User PATH." -ForegroundColor Green

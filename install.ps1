#!/usr/bin/env pwsh
<#
.SYNOPSIS
    CLI Power Setup Windows 10/11 Installer (install.ps1)
    Deploys skills, rules, statuslines, and CLI shims for Antigravity (agy) on Windows.
#>
[CmdletBinding()]
param(
    [switch]$WithModels,
    [switch]$ModelsOnly
)

$ErrorActionPreference = "Stop"

$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Path
$BinDest    = Join-Path $HOME ".local\bin"
$GeminiDir  = Join-Path $HOME ".gemini\config"
$StateDir   = Join-Path $HOME ".cli_power_setup"

Write-Host "[→] Creating target directories on Windows..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $BinDest, "$GeminiDir\skills", $StateDir | Out-Null

# 1. Deploy Python CLI utilities and generate Windows .cmd shims
$PyTools = @(
    "repo-auto-sync", "steam-mod-scanner", "slice-reader",
    "export-skills", "setup-local-model-fleet", "ultra-model-manager",
    "model-quant-optimizer", "local-coprocessor", "voice-prompt-optimizer", "local-research-scout",
    "agy-doctor", "agy-context", "agy-init", "agy-quota-statusline", "agy-cheatsheet"
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

# Launcher shims for Windows (yolo.cmd, agy-yolo.cmd, agy-turbo.cmd, agy-eco.cmd, cs.cmd)
"@echo off`r`nagy --dangerously-skip-permissions --mode auto %*" | Set-Content -Path (Join-Path $BinDest "agy-yolo.cmd") -Encoding ASCII
"@echo off`r`nagy --dangerously-skip-permissions --mode auto %*" | Set-Content -Path (Join-Path $BinDest "yolo.cmd") -Encoding ASCII
"@echo off`r`nagy --model gemini-3.8-flash-low --effort low --dangerously-skip-permissions --mode auto %*" | Set-Content -Path (Join-Path $BinDest "agy-turbo.cmd") -Encoding ASCII
"@echo off`r`nagy --model gemini-3.8-flash-low --effort low --mode auto %*" | Set-Content -Path (Join-Path $BinDest "agy-eco.cmd") -Encoding ASCII
"@echo off`r`npython `"$BinDest\agy-cheatsheet.py`" %*" | Set-Content -Path (Join-Path $BinDest "cs.cmd") -Encoding ASCII

# 2. Copy global rules & state ledgers
Copy-Item (Join-Path $ScriptDir "config\GEMINI.md") (Join-Path $GeminiDir "GEMINI.md") -Force
if (Test-Path (Join-Path $ScriptDir "config\token_ledger.json")) {
    Copy-Item (Join-Path $ScriptDir "config\token_ledger.json") (Join-Path $StateDir "token_ledger.json") -Force
}

# 3. Synchronize skills to Antigravity config
if (-not $ModelsOnly) {
    Write-Host "[→] Synchronizing Antigravity skills..." -ForegroundColor Cyan
    Copy-Item (Join-Path $ScriptDir "config\skills\*") (Join-Path $GeminiDir "skills") -Recurse -Force
}

# 4. Optional: Download and hardware-optimize local model fleet
if ($WithModels -or $ModelsOnly) {
    Write-Host "[→] Detecting host system hardware and synchronizing local model fleet..." -ForegroundColor Cyan
    python (Join-Path $BinDest "setup-local-model-fleet.py") --all
}

Write-Host "[✓] CLI Power Setup installed for Antigravity (agy) on Windows! Ensure '$BinDest' is in your User PATH." -ForegroundColor Green
Write-Host "    To export skills to other tools, run: python `"$BinDest\export-skills.py`" --target cursor|agents|windsurf" -ForegroundColor Cyan

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [switch]$ConfirmGeneralArkKey,

    [string]$RepoPath = "D:\Users\aa133\Desktop\BO_Multi_12_20\New_LLMBO",

    [string]$ApiBase = "https://ark.cn-beijing.volces.com/api/v3",

    [string[]]$Models = @(
        "deepseek-v4-flash",
        "deepseek-v4-pro"
    ),

    [int[]]$Seeds = @(8409, 8410, 8411, 8412, 8413),

    [int[]]$PilotSeeds = @(8409, 8410),

    [int]$Iterations = 50,

    [int]$PilotIterations = 12,

    [string]$OutputRoot = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $ConfirmGeneralArkKey.IsPresent) {
    throw "Safety stop: pass -ConfirmGeneralArkKey only after confirming ARK_API_KEY is a general pay-as-you-go Ark API key, not a Coding Plan key."
}

if ($ApiBase -match "/api/coding(?:/|$)") {
    throw "Safety stop: the Coding Plan endpoint cannot be used for this non-coding optimization experiment. Use the general Ark /api/v3 endpoint and a general Ark API key."
}

if ([string]::IsNullOrWhiteSpace($env:ARK_API_KEY)) {
    throw "ARK_API_KEY is not set in this PowerShell process. Set it at runtime; do not place it in this script or commit it to the repository."
}

$resolvedRepo = (Resolve-Path -LiteralPath $RepoPath).Path
$pythonPath = Join-Path $resolvedRepo ".venv\Scripts\python.exe"
$runnerPath = Join-Path $resolvedRepo "tools\run_region_lift_v2_50iter.py"

if (-not (Test-Path -LiteralPath $pythonPath -PathType Leaf)) {
    throw "Python environment not found: $pythonPath"
}
if (-not (Test-Path -LiteralPath $runnerPath -PathType Leaf)) {
    throw "Experiment runner not found: $runnerPath"
}

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $OutputRoot = Join-Path (Split-Path -Parent $PSScriptRoot) "results\region_lift_ark_$timestamp"
}
$OutputRoot = [System.IO.Path]::GetFullPath($OutputRoot)
New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null

$variants = @(
    "warmstart_plain_ei",
    "warmstart_region_lgbo_proposition1",
    "sham_region_lgbo_proposition1",
    "random_region_lgbo_proposition1"
)

$hadLlmApiKey = Test-Path Env:LLM_API_KEY
$previousLlmApiKey = $env:LLM_API_KEY
$hadPythonUnbuffered = Test-Path Env:PYTHONUNBUFFERED
$previousPythonUnbuffered = $env:PYTHONUNBUFFERED

try {
    # The runner reads LLM_API_KEY. This assignment exists only in the current
    # process and is restored below; the credential is never written to disk.
    $env:LLM_API_KEY = $env:ARK_API_KEY
    $env:PYTHONUNBUFFERED = "1"

    Push-Location -LiteralPath $resolvedRepo
    try {
        foreach ($model in $Models) {
            $safeModelName = $model -replace "[^A-Za-z0-9._-]", "_"
            $modelOutput = Join-Path $OutputRoot $safeModelName

            Write-Host "Starting matched Region-Lift experiment for model: $model"
            Write-Host "Output: $modelOutput"

            $runnerArgs = @(
                $runnerPath,
                "--output-root", $modelOutput,
                "--iterations", $Iterations.ToString(),
                "--model", $model,
                "--api-base", $ApiBase,
                "--two-stage-gate",
                "--pilot-iterations", $PilotIterations.ToString(),
                "--variants"
            ) + $variants + @("--seeds") + ($Seeds | ForEach-Object { $_.ToString() }) + @("--pilot-seeds") + ($PilotSeeds | ForEach-Object { $_.ToString() })

            & $pythonPath @runnerArgs
            if ($LASTEXITCODE -ne 0) {
                throw "Experiment runner failed for $model with exit code $LASTEXITCODE."
            }
        }
    }
    finally {
        Pop-Location
    }
}
finally {
    if ($hadLlmApiKey) {
        $env:LLM_API_KEY = $previousLlmApiKey
    }
    else {
        Remove-Item Env:LLM_API_KEY -ErrorAction SilentlyContinue
    }

    if ($hadPythonUnbuffered) {
        $env:PYTHONUNBUFFERED = $previousPythonUnbuffered
    }
    else {
        Remove-Item Env:PYTHONUNBUFFERED -ErrorAction SilentlyContinue
    }
}

Write-Host "All requested model runs completed. Results: $OutputRoot"

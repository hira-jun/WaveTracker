param(
    [int]$Port = 3000,
    [switch]$SkipInstall
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw 'npm が見つかりません。Node.js 20+ をインストールしてから再実行してください。'
}

if (-not $SkipInstall) {
    Write-Host '[WaveTracker] Installing frontend dependencies...'
    npm install
}

Write-Host "[WaveTracker] Starting frontend dev server on port $Port..."
npm run dev -- --host 0.0.0.0 --port $Port

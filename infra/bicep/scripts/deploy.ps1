param(
  [Parameter(Mandatory = $true)]
  [string]$ResourceGroupName,

  [Parameter(Mandatory = $false)]
  [string]$ParameterFile = '../params/dev.bicepparam'
)

$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
$templateFile = Join-Path $scriptDir '../main.bicep'
$resolvedParams = Join-Path $scriptDir $ParameterFile

Write-Host "Deploying WaveTracker infra with Bicep..." -ForegroundColor Cyan
Write-Host "Resource Group: $ResourceGroupName" -ForegroundColor Cyan
Write-Host "Template: $templateFile" -ForegroundColor Cyan
Write-Host "Parameters: $resolvedParams" -ForegroundColor Cyan

az deployment group create `
  --resource-group $ResourceGroupName `
  --template-file $templateFile `
  --parameters $resolvedParams

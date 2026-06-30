param(
  [string]$OutputDir = ".\\out"
)

$ErrorActionPreference = "Stop"

$timestamp = Get-Date
$sessionId = $timestamp.ToString("yyyyMMdd-HHmmss")
$sessionDir = Join-Path $OutputDir "wifi-survey-$sessionId"
$logsDir = Join-Path $sessionDir "logs"

New-Item -ItemType Directory -Path $sessionDir -Force | Out-Null
New-Item -ItemType Directory -Path $logsDir -Force | Out-Null

$networksTxt = Join-Path $sessionDir "networks.txt"
$interfaceTxt = Join-Path $sessionDir "interface.txt"
$scanJson = Join-Path $sessionDir "scan.json"
$metadataJson = Join-Path $sessionDir "metadata.json"

function Convert-SignalToDbm {
  param([string]$Signal)

  if ($Signal -match '(\d+)%') {
    return [math]::Round(([int]$matches[1] / 2) - 100)
  }

  return -90
}

function Get-InterfaceReadings {
  param([string]$Text, [string]$CapturedAt)

  $readings = @()
  $current = [ordered]@{}

  function New-ReadingFromCurrent {
    param([hashtable]$Current, [string]$CapturedAt)

    if ($Current.Count -eq 0) {
      return $null
    }

    $ssid = if ($Current.Contains('ssid') -and $Current.ssid) { $Current.ssid } else { 'unknown-ssid' }
    $bssid = if ($Current.Contains('bssid') -and $Current.bssid) { $Current.bssid } else { '00:00:00:00:00:00' }
    $channel = if ($Current.Contains('channel') -and $Current.channel) { [int]$Current.channel } else { 0 }
    $signalDbm = if ($Current.Contains('signal')) { Convert-SignalToDbm $Current.signal } else { -90 }

    return [ordered]@{
      ssid = $ssid
      bssid = $bssid
      channel = $channel
      signal_dbm = $signalDbm
      captured_at = $CapturedAt
    }
  }

  foreach ($line in $Text -split "`r?`n") {
    if ($line -match '^\s*Name\s*:\s*(.+)$') {
      if ($current.Count -gt 0) {
        $reading = New-ReadingFromCurrent -Current $current -CapturedAt $CapturedAt
        if ($null -ne $reading) {
          $readings += $reading
        }
        $current = [ordered]@{}
      }

      $current.name = $matches[1].Trim()
      continue
    }

    if ($line -match '^\s*SSID\s*\d*\s*:\s*(.+)$') {
      $current.ssid = $matches[1].Trim()
      continue
    }

    if ($line -match '^\s*BSSID\s*\d*\s*:\s*(.+)$') {
      $current.bssid = $matches[1].Trim()
      continue
    }

    if ($line -match '^\s*Channel\s*:\s*(\d+)') {
      $current.channel = $matches[1]
      continue
    }

    if ($line -match '^\s*Signal\s*:\s*(.+)$') {
      $current.signal = $matches[1].Trim()
      continue
    }
  }

  if ($current.Count -gt 0) {
    $reading = New-ReadingFromCurrent -Current $current -CapturedAt $CapturedAt
    if ($null -ne $reading) {
      $readings += $reading
    }
  }

  if ($readings.Count -eq 0) {
    $readings += [ordered]@{
      ssid = 'unknown-ssid'
      bssid = '00:00:00:00:00:00'
      channel = 0
      signal_dbm = -90
      captured_at = $CapturedAt
    }
  }

  return ,$readings
}

$interfacesText = netsh wlan show interfaces | Out-String
$networksText = netsh wlan show networks mode=bssid | Out-String
$interfacesText | Out-File -FilePath $interfaceTxt -Encoding utf8
$networksText | Out-File -FilePath $networksTxt -Encoding utf8
netsh wlan show wlanreport | Out-File -FilePath (Join-Path $logsDir "wlanreport.txt") -Encoding utf8

$hostnameHash = [Convert]::ToHexString(
  [System.Security.Cryptography.SHA256]::HashData(
    [System.Text.Encoding]::UTF8.GetBytes($env:COMPUTERNAME)
  )
)

$metadata = [ordered]@{
  schemaVersion = "1.0"
  platform = "windows"
  collectedAt = $timestamp.ToString("o")
  sessionId = $sessionId
  hostnameHash = $hostnameHash
}
$metadata | ConvertTo-Json -Depth 4 | Out-File -FilePath $metadataJson -Encoding utf8

$scan = [ordered]@{
  readings = Get-InterfaceReadings -Text $interfacesText -CapturedAt $timestamp.ToString("o")
}
$scan | ConvertTo-Json -Depth 6 | Out-File -FilePath $scanJson -Encoding utf8

$zipPath = Join-Path $OutputDir "wifi-survey-$sessionId.zip"
if (Test-Path $zipPath) {
  Remove-Item $zipPath -Force
}
Compress-Archive -Path (Join-Path $sessionDir "*") -DestinationPath $zipPath -Force

Write-Host "WaveTracker Windows collector completed: $zipPath"
param(
  [string]$OutputDir = ".\\out",
  [int]$SessionDurationSeconds = 60,
  [int]$SampleIntervalSeconds = 10
)

$ErrorActionPreference = "Stop"

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::InputEncoding = $utf8NoBom
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom

if ($SessionDurationSeconds -le 0) {
  throw "SessionDurationSeconds must be greater than zero."
}

if ($SampleIntervalSeconds -le 0) {
  throw "SampleIntervalSeconds must be greater than zero."
}

$sessionStart = Get-Date
$sessionId = $sessionStart.ToString("yyyyMMdd-HHmmss")
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

function Get-NetworkReadings {
  param([string]$Text, [string]$CapturedAt)

  $readings = @()
  $currentSsid = 'unknown-ssid'
  $currentReading = $null

  foreach ($line in $Text -split "`r?`n") {
    if ($line -match '^\s*SSID\s*\d*\s*:\s*(.*)$') {
      if ($null -ne $currentReading) {
        $readings += [ordered]@{
          ssid = if ($currentReading.Contains('ssid') -and $currentReading.ssid) { $currentReading.ssid } else { 'unknown-ssid' }
          bssid = if ($currentReading.Contains('bssid') -and $currentReading.bssid) { $currentReading.bssid } else { '00:00:00:00:00:00' }
          channel = if ($currentReading.Contains('channel') -and $currentReading.channel) { [int]$currentReading.channel } else { 0 }
          signal_dbm = if ($currentReading.Contains('signal')) { Convert-SignalToDbm $currentReading.signal } else { -90 }
          captured_at = $CapturedAt
        }
      }

      $currentReading = $null
      $currentSsid = $matches[1].Trim()
      continue
    }

    if ($line -match '^\s*BSSID\s*\d*\s*:\s*(.+)$') {
      if ($null -ne $currentReading) {
        $readings += [ordered]@{
          ssid = if ($currentReading.Contains('ssid') -and $currentReading.ssid) { $currentReading.ssid } else { 'unknown-ssid' }
          bssid = if ($currentReading.Contains('bssid') -and $currentReading.bssid) { $currentReading.bssid } else { '00:00:00:00:00:00' }
          channel = if ($currentReading.Contains('channel') -and $currentReading.channel) { [int]$currentReading.channel } else { 0 }
          signal_dbm = if ($currentReading.Contains('signal')) { Convert-SignalToDbm $currentReading.signal } else { -90 }
          captured_at = $CapturedAt
        }
      }

      $currentReading = [ordered]@{
        ssid = $currentSsid
        bssid = $matches[1].Trim()
        channel = 0
        signal = $null
      }

      continue
    }

    if ($line -match '^\s*Channel\s*:\s*(\d+)') {
      if ($null -ne $currentReading) {
        $currentReading.channel = $matches[1]
      }
      continue
    }

    if ($line -match '^\s*Signal\s*:\s*(.+)$') {
      if ($null -ne $currentReading) {
        $currentReading.signal = $matches[1].Trim()
      }
      continue
    }
  }

  if ($null -ne $currentReading) {
    $readings += [ordered]@{
      ssid = if ($currentReading.Contains('ssid') -and $currentReading.ssid) { $currentReading.ssid } else { 'unknown-ssid' }
      bssid = if ($currentReading.Contains('bssid') -and $currentReading.bssid) { $currentReading.bssid } else { '00:00:00:00:00:00' }
      channel = if ($currentReading.Contains('channel') -and $currentReading.channel) { [int]$currentReading.channel } else { 0 }
      signal_dbm = if ($currentReading.Contains('signal')) { Convert-SignalToDbm $currentReading.signal } else { -90 }
      captured_at = $CapturedAt
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

$sessionEnd = $sessionStart.AddSeconds($SessionDurationSeconds)
$allReadings = @()
$latestInterfacesText = $null
$latestNetworksText = $null
$sampleIndex = 0

Write-Host "WaveTracker Windows collector started: sampling every $SampleIntervalSeconds seconds for about $SessionDurationSeconds seconds"

while ((Get-Date) -lt $sessionEnd) {
  $sampleIndex += 1
  $capturedAt = Get-Date
  $remainingSeconds = [math]::Max(0, [int][math]::Ceiling(($sessionEnd - $capturedAt).TotalSeconds))
  Write-Host "Collecting sample $sampleIndex (about $remainingSeconds seconds remaining)"
  $interfacesText = netsh wlan show interfaces | Out-String
  $networksText = netsh wlan show networks mode=bssid | Out-String

  $allReadings += Get-NetworkReadings -Text $networksText -CapturedAt $capturedAt.ToString("o")
  $latestInterfacesText = $interfacesText
  $latestNetworksText = $networksText

  $nextSampleAt = $capturedAt.AddSeconds($SampleIntervalSeconds)
  if ($nextSampleAt -ge $sessionEnd) {
    break
  }

  $sleepDuration = $nextSampleAt - (Get-Date)
  if ($sleepDuration.TotalMilliseconds -gt 0) {
    Write-Host "Waiting $([int][math]::Ceiling($sleepDuration.TotalSeconds)) seconds before the next sample"
    Start-Sleep -Milliseconds ([int]$sleepDuration.TotalMilliseconds)
  }
}

if ($null -eq $latestInterfacesText) {
  $latestInterfacesText = ""
}

if ($null -eq $latestNetworksText) {
  $latestNetworksText = ""
}

$latestInterfacesText | Out-File -FilePath $interfaceTxt -Encoding utf8
$latestNetworksText | Out-File -FilePath $networksTxt -Encoding utf8
netsh wlan show wlanreport | Out-File -FilePath (Join-Path $logsDir "wlanreport.txt") -Encoding utf8

$hostnameHash = [Convert]::ToHexString(
  [System.Security.Cryptography.SHA256]::HashData(
    [System.Text.Encoding]::UTF8.GetBytes($env:COMPUTERNAME)
  )
)

$metadata = [ordered]@{
  schemaVersion = "1.0"
  platform = "windows"
  collectedAt = $sessionStart.ToString("o")
  sessionId = $sessionId
  hostnameHash = $hostnameHash
}
$metadata | ConvertTo-Json -Depth 4 | Out-File -FilePath $metadataJson -Encoding utf8

$scan = [ordered]@{
  readings = $allReadings
}
$scan | ConvertTo-Json -Depth 6 | Out-File -FilePath $scanJson -Encoding utf8

$zipPath = Join-Path $OutputDir "wifi-survey-$sessionId.zip"
if (Test-Path $zipPath) {
  Remove-Item $zipPath -Force
}
Compress-Archive -Path (Join-Path $sessionDir "*") -DestinationPath $zipPath -Force

Write-Host "WaveTracker Windows collector completed: $zipPath"
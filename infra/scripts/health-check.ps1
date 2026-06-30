Write-Host "Checking backend..."
$backend = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:8000/health" -Method Get
if ($backend.StatusCode -ne 200) { throw "Backend health check failed" }

Write-Host "Checking frontend..."
$frontend = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:3000" -Method Get
if ($frontend.StatusCode -lt 200 -or $frontend.StatusCode -ge 400) { throw "Frontend check failed" }

Write-Host "Checking postgres port..."
$tcp = Test-NetConnection -ComputerName "localhost" -Port 5432 -WarningAction SilentlyContinue
if (-not $tcp.TcpTestSucceeded) { throw "Postgres port is not reachable" }

Write-Host "All services are reachable."

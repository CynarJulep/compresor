# Autoarranque silencioso Compresor Docker al login.
$ErrorActionPreference = 'Stop'
$ProjectDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path (Join-Path $ProjectDir 'docker-compose.yml'))) {
  $ProjectDir = 'C:\Renzo\compresor\compresor'
}

$bootDir = Join-Path $env:LOCALAPPDATA 'CompresorDocker'
New-Item -ItemType Directory -Force -Path $bootDir | Out-Null
$runner = Join-Path $bootDir 'boot.ps1'
$log = Join-Path $bootDir 'boot.log'
$vbs = Join-Path $bootDir 'boot-silent.vbs'

@"
`$ErrorActionPreference = 'Continue'
Set-Location '$ProjectDir'
`$log = '$log'
function Log(`$m) { "[`$(Get-Date -Format o)] `$m" | Out-File `$log -Append -Encoding utf8 }
Log 'compresor docker boot start'
Start-Sleep -Seconds 30
for (`$i = 0; `$i -lt 60; `$i++) {
  docker info 1>`$null 2>`$null
  if (`$LASTEXITCODE -eq 0) { break }
  Start-Sleep -Seconds 5
}
# Liberar 8501 por si la tarea Windows revive
& '$ProjectDir\scripts\stop-windows-server.ps1' *>> `$log
Start-Sleep -Seconds 2
docker compose up -d *>> `$log
Log "compose exit=`$LASTEXITCODE"
Log 'done'
"@ | Set-Content -Path $runner -Encoding utf8

@"
Set sh = CreateObject("WScript.Shell")
sh.Run "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""$runner""", 0, False
"@ | Set-Content -Path $vbs -Encoding ascii

$startup = [Environment]::GetFolderPath('Startup')
Copy-Item $vbs (Join-Path $startup 'Compresor-Docker.vbs') -Force
Write-Host "Autostart OK: Compresor-Docker.vbs"
Write-Host "Deshabilitá la tarea CompresorArchivos si aún corre (Admin): schtasks /Change /TN CompresorArchivos /DISABLE"

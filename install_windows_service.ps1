#Requires -Version 5.1
# Instala el compresor como tarea de Windows (SYSTEM).
# Corre al encender, se reinicia si se cae, vive con la sesion bloqueada.

$ErrorActionPreference = "Stop"
$TaskName = "CompresorArchivos"
$Port = 8501
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Bat = Join-Path $Root "run_server.bat"
$Python = Join-Path $Root ".venv\Scripts\python.exe"

function Test-IsAdmin {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    $p = New-Object Security.Principal.WindowsPrincipal($id)
    return $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-IsAdmin)) {
    $p = Start-Process -FilePath "powershell.exe" -Verb RunAs -Wait -PassThru -ArgumentList @(
        "-NoProfile",
        "-ExecutionPolicy", "Bypass",
        "-File", $PSCommandPath
    )
    exit $p.ExitCode
}

Write-Host "=== Compresor - instalar servidor permanente ==="
Write-Host ("Carpeta: " + $Root)

if (-not (Test-Path $Python)) {
    Write-Host ("ERROR: no esta el venv en " + $Python)
    exit 1
}
if (-not (Test-Path $Bat)) {
    Write-Host ("ERROR: falta " + $Bat)
    exit 1
}

New-Item -ItemType Directory -Force -Path (Join-Path $Root "logs") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Root "data") | Out-Null

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue

$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument ("/c `"" + $Bat + "`"") -WorkingDirectory $Root
$trigger = New-ScheduledTaskTrigger -AtStartup
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -DontStopOnIdleEnd `
    -StartWhenAvailable `
    -RestartCount 999 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Compresor de archivos a menos de 1 MB. Puerto 8501." `
    -Force | Out-Null

Write-Host ("Tarea OK: " + $TaskName + " SYSTEM al arrancar")

netsh advfirewall firewall delete rule name="Compresor" | Out-Null
netsh advfirewall firewall add rule name="Compresor" dir=in action=allow protocol=TCP localport=$Port | Out-Null
Write-Host ("Firewall OK: TCP " + $Port)

Start-ScheduledTask -TaskName $TaskName
Write-Host "Arrancando..."

$ok = $false
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep -Seconds 1
    try {
        $r = Invoke-WebRequest -Uri ("http://127.0.0.1:" + $Port + "/") -UseBasicParsing -TimeoutSec 2
        if ($r.StatusCode -ge 200 -and $r.StatusCode -lt 400) {
            $ok = $true
            Write-Host ("HEALTH: HTTP " + $r.StatusCode)
            break
        }
    } catch {}
}

if (-not $ok) {
    Write-Host "AVISO: la tarea arranco pero el puerto no respondio aun."
    Write-Host ("Mira: " + (Join-Path $Root "logs\server.log"))
    exit 1
}

Write-Host ""
Write-Host ("Listo. En esta PC:  http://127.0.0.1:" + $Port)
Write-Host ("En la red:          http://10.3.2.117:" + $Port)
Write-Host "Sigue corriendo con la sesion bloqueada y al reiniciar Windows."
exit 0

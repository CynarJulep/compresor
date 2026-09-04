# Detiene el Streamlit nativo / libera el puerto 8501 para Docker.
$ErrorActionPreference = 'Continue'
$ports = @(8501)
foreach ($port in $ports) {
  Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue |
    ForEach-Object {
      $procId = $_.OwningProcess
      Write-Host "Matando PID $procId (puerto $port)..."
      Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
    }
}
# Procesos streamlit del venv del compresor
Get-CimInstance Win32_Process -Filter "Name='python.exe'" -ErrorAction SilentlyContinue |
  Where-Object { $_.CommandLine -match 'compresor.*streamlit|streamlit run app\.py' } |
  ForEach-Object {
    Write-Host "Matando streamlit PID $($_.ProcessId)..."
    Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
  }

# Intentar deshabilitar tarea Windows (puede pedir admin)
schtasks /Change /TN "CompresorArchivos" /DISABLE 2>$null
Write-Host "Listo. Puerto 8501 debería estar libre."

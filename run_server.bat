@echo off
REM Arranque del compresor (lo llama la tarea programada CompresorArchivos).
cd /d "%~dp0"

if not exist "logs" mkdir logs
if not exist "data" mkdir data

if exist "logs\server.log" (
  for %%A in ("logs\server.log") do (
    if %%~zA GTR 20000000 move /Y "logs\server.log" "logs\server.log.old" >nul
  )
)

echo ===== %DATE% %TIME% start =====>> "logs\server.log"
set PYTHONUNBUFFERED=1
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
".venv\Scripts\python.exe" -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true --server.fileWatcherType none >> "logs\server.log" 2>&1
echo ===== %DATE% %TIME% exit %ERRORLEVEL% =====>> "logs\server.log"
exit /b %ERRORLEVEL%

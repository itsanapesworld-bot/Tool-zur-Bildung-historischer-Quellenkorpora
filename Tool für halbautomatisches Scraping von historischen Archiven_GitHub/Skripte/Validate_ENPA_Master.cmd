@echo off
setlocal
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
cd /d "%PROJECT_DIR%"
call "%PROJECT_DIR%\enpa_automation\find_python.cmd"
if errorlevel 1 goto :failed

echo Pruefe das aktive Arbeitsmappenprofil aus config.json.
"%ENPA_PYTHON%" "%PROJECT_DIR%\enpa_automation\validate_master.py" --config "%PROJECT_DIR%\enpa_automation\config.json"
if errorlevel 1 goto :failed
echo.
echo Fertig. Dieses Fenster kann geschlossen werden.
pause
exit /b 0

:failed
echo.
echo Der Vorgang wurde mit einem Fehler beendet.
pause
exit /b 1

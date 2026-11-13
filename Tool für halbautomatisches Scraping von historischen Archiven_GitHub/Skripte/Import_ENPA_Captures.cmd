@echo off
setlocal
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
cd /d "%PROJECT_DIR%"
call "%PROJECT_DIR%\enpa_automation\find_python.cmd"
if errorlevel 1 goto :failed

echo Importziel: aktives Arbeitsmappenprofil aus enpa_automation\config.json
echo In readOnlyWorkbookProfiles aufgefuehrte Profile bleiben fuer Schreibzugriffe gesperrt.

"%ENPA_PYTHON%" "%PROJECT_DIR%\enpa_automation\import_captures.py" --config "%PROJECT_DIR%\enpa_automation\config.json"
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

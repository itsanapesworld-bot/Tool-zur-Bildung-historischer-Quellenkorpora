@echo off
setlocal
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
cd /d "%PROJECT_DIR%"
call "%PROJECT_DIR%\enpa_automation\find_python.cmd"
if errorlevel 1 goto :failed

"%ENPA_PYTHON%" "%PROJECT_DIR%\enpa_automation\portable_selftest.py" --config "%PROJECT_DIR%\enpa_automation\config.json"
if errorlevel 1 goto :failed

echo.
echo Portabilitaetspruefung erfolgreich.
if /i not "%~1"=="--no-pause" pause
exit /b 0

:failed
echo.
echo Die Portabilitaetspruefung ist fehlgeschlagen.
if /i not "%~1"=="--no-pause" pause
exit /b 1

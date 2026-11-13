@echo off
setlocal
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
cd /d "%PROJECT_DIR%"
call "%PROJECT_DIR%\enpa_automation\find_python.cmd"
if errorlevel 1 goto :failed
"%ENPA_PYTHON%" "%PROJECT_DIR%\enpa_automation\offline_demo.py"
if errorlevel 1 goto :failed
echo Offline-Demonstration erfolgreich.
if /i not "%~1"=="--no-pause" pause
exit /b 0
:failed
echo Offline-Demonstration fehlgeschlagen.
if /i not "%~1"=="--no-pause" pause
exit /b 1

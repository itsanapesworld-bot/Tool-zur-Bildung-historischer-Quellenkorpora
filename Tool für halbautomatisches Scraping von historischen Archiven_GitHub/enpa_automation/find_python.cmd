@echo off
set "ENPA_PYTHON="
set "ENPA_PROJECT_ROOT=%~dp0.."
if defined ENPA_PYTHON_OVERRIDE call :try_python "%ENPA_PYTHON_OVERRIDE%"
if defined ENPA_PYTHON exit /b 0
call :try_python "%ENPA_PROJECT_ROOT%\.venv\Scripts\python.exe"
if defined ENPA_PYTHON exit /b 0
for /f "usebackq delims=" %%I in (`py -3 -c "import sys; print(sys.executable)" 2^>nul`) do call :try_python "%%I"
if defined ENPA_PYTHON exit /b 0
for /f "usebackq delims=" %%I in (`python -c "import sys; print(sys.executable)" 2^>nul`) do call :try_python "%%I"
if defined ENPA_PYTHON exit /b 0
echo FEHLER: Python 3.11 oder neuer mit openpyxl fehlt.
echo Fuehre zuerst Skripte\Setup_ENPA.cmd aus.
exit /b 1

:try_python
if not exist "%~1" exit /b 1
"%~1" -c "import sys, openpyxl; sys.exit(0 if sys.version_info >= (3,11) else 1)" >nul 2>&1
if errorlevel 1 exit /b 1
set "ENPA_PYTHON=%~1"
exit /b 0

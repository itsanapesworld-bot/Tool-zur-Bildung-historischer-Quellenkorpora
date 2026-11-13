@echo off
setlocal
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
cd /d "%PROJECT_DIR%"

set "BASE_PYTHON="
if defined ENPA_PYTHON_OVERRIDE if exist "%ENPA_PYTHON_OVERRIDE%" set "BASE_PYTHON=%ENPA_PYTHON_OVERRIDE%"
if not defined BASE_PYTHON if exist "%PROJECT_DIR%\.venv\Scripts\python.exe" set "BASE_PYTHON=%PROJECT_DIR%\.venv\Scripts\python.exe"
if not defined BASE_PYTHON (
for /f "usebackq delims=" %%I in (`py -3 -c "import sys; print(sys.executable)" 2^>nul`) do set "BASE_PYTHON=%%I"
)
if not defined BASE_PYTHON (
  for /f "usebackq delims=" %%I in (`python -c "import sys; print(sys.executable)" 2^>nul`) do set "BASE_PYTHON=%%I"
)

if not defined BASE_PYTHON (
  echo.
  echo FEHLER: Python 3 wurde nicht gefunden.
  echo Installiere Python 3.11 oder neuer von https://www.python.org/downloads/
  echo Aktiviere bei der Installation "Add Python to PATH".
  if /i not "%~1"=="--no-pause" pause
  exit /b 1
)

"%BASE_PYTHON%" -c "import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)"
if errorlevel 1 goto :failed

if not exist "%PROJECT_DIR%\.venv\Scripts\python.exe" (
  echo Erstelle lokale Python-Umgebung in .venv ...
  "%BASE_PYTHON%" -m venv "%PROJECT_DIR%\.venv"
  if errorlevel 1 goto :failed
)

echo Installiere beziehungsweise aktualisiere Projektabhaengigkeiten ...
"%PROJECT_DIR%\.venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :failed
"%PROJECT_DIR%\.venv\Scripts\python.exe" -m pip install -r "%PROJECT_DIR%\enpa_automation\requirements.txt"
if errorlevel 1 goto :failed

echo.
echo Einrichtung erfolgreich.
"%PROJECT_DIR%\.venv\Scripts\python.exe" "%PROJECT_DIR%\enpa_automation\initialize_project.py" --config "%PROJECT_DIR%\enpa_automation\config.json"
if errorlevel 1 goto :failed
call "%~dp0Check_ENPA_Setup.cmd" --no-pause
if errorlevel 1 goto :failed
if /i not "%~1"=="--no-pause" pause
exit /b 0

:failed
echo.
echo FEHLER: Die Einrichtung konnte nicht abgeschlossen werden.
echo Pruefe die Internetverbindung und die Python-Installation.
if /i not "%~1"=="--no-pause" pause
exit /b 1

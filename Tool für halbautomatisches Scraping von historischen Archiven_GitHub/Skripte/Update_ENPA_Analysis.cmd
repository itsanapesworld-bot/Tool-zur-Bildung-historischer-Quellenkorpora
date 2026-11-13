@echo off
setlocal
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
cd /d "%PROJECT_DIR%"

call "%PROJECT_DIR%\enpa_automation\find_python.cmd"
if errorlevel 1 (
  pause
  exit /b 1
)

echo Aktualisiere Datengrundlage...
"%ENPA_PYTHON%" "%PROJECT_DIR%\enpa_automation\export_search_term_relevance_data.py" --config "%PROJECT_DIR%\enpa_automation\config.json"
if errorlevel 1 goto :error

echo Erstelle Auswertungsdatei...
"%ENPA_PYTHON%" "%PROJECT_DIR%\enpa_automation\build_search_term_relevance_workbook.py" --config "%PROJECT_DIR%\enpa_automation\config.json"
if errorlevel 1 goto :error

echo.
echo Fertig: Arbeitsmappen\Auswertung Suchbegriffe_Relevanz.xlsx
pause
exit /b 0

:error
echo.
echo Die Auswertung konnte nicht aktualisiert werden.
pause
exit /b 1

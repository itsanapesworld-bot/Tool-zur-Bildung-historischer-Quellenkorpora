@echo off
setlocal
for %%I in ("%~dp0..") do set "PROJECT_DIR=%%~fI"
cd /d "%PROJECT_DIR%"
call "%PROJECT_DIR%\enpa_automation\find_python.cmd"
if errorlevel 1 goto :failed
echo Erzeuge Arbeitsmappen\Master_Codiermatrix_Leer.xlsx vollstaendig aus Code und Konfiguration.
echo Keine befuellte Exceldatei wird als Vorlage benoetigt oder eingelesen.
echo Eine vorhandene Datei mit genau diesem Namen wird ersetzt.
echo Kalibrierungs- und Vergleichsmatrix werden nicht veraendert.
"%ENPA_PYTHON%" "%PROJECT_DIR%\enpa_automation\build_master.py" --config "%PROJECT_DIR%\enpa_automation\config.json" --overwrite
if errorlevel 1 goto :failed
echo.
echo Die neue Vorlage vor der Nutzung unter einem eigenen Namen speichern.
echo Fertig. Dieses Fenster kann geschlossen werden.
pause
exit /b 0

:failed
echo.
echo Der Vorgang wurde mit einem Fehler beendet.
pause
exit /b 1

# ENPA Werkzeug zur halbautomatischen Korpusbildung

Version 2.7.0. Dieses Werkzeug erzeugt Suchabfragen für **e-newspaperarchives.ch**, sichert sichtbare Treffer über ein Browser-Lesezeichen und importiert Capture-Dateien in eine Excel-Codiermatrix. Regelbasierte Vorcodierungen unterstützen die anschließende manuelle Vollartikelsichtung. Sie sind keine abschließenden historischen Befunde.

Das Werkzeug unterstützt ausschließlich die ENPA-Suchoberfläche. Andere historische Archive benötigen eine eigene Anpassung von Suche, Capture und Metadaten. Trotz des Ordnernamens handelt es sich nicht um einen universellen Scraper.

## Voraussetzungen

- Windows 10 oder 11, Python 3.11 oder neuer einschließlich pip und venv.
- Ein aktueller Browser mit Lesezeichenfunktion. Der Capture-Ablauf ist für Chrome vorgesehen.
- Microsoft Excel für verifizierte Formelberechnung, Filter und Dropdowns. Andere Tabellenprogramme wurden für diese Veröffentlichungskopie nicht geprüft.
- Internetzugang für die Erstinstallation und die tatsächlichen ENPA-Abfragen. Die Offline-Demonstration benötigt nach der Installation keinen Archivzugriff.

Der Python-Kern benötigt ausschließlich `openpyxl`. Node.js, Codex, python-docx, PDFs und eine vorhandene Forschungsdatei sind nicht erforderlich. Programme werden nicht mitgeliefert.

## Installation

1. Den gesamten Veröffentlichungsordner herunterladen oder klonen. Seine Unterordner müssen zusammenbleiben.
2. Python 3.11 oder neuer von [python.org](https://www.python.org/downloads/windows/) installieren; den Python-Launcher beziehungsweise Python im Suchpfad aktivieren.
3. `Skripte/Setup_ENPA.cmd` ausführen. Es erstellt `.venv`, installiert die festgelegten Abhängigkeiten und legt die fehlende eigene Forschungsdatei an.
4. `Skripte/Check_ENPA_Setup.cmd` ausführen. Die vorhandenen Beispielmatrizen und die leere Mastervorlage gehören zum Paket.
5. `Skripte/Test_ENPA_Offline_Demo.cmd` ausführen. Der Test importiert ausschließlich synthetische Captures in ein vorübergehendes Testprojekt.

`ENPA_PYTHON_OVERRIDE` kann optional auf eine installierte Python-Datei zeigen. Der normale Ablauf braucht diese Variable nicht. Das Programm erkennt den Projektstamm über `enpa_project.json`; verschobene und umbenannte Projektordner benötigen keine Pfadänderung.

## Dateien und Beispieldaten

`Arbeitsmappen` enthält drei veröffentlichte Dateien:

- `Master_Codiermatrix_Leer.xlsx`: leere Vorlage mit 35 Codierungsspalten und der vollständigen aktuellen Auswertungsstruktur.
- `Codiermatrix_e-newspaperarchives_Naturgefahrenforschung_Kalibrierungsdaten_1851_1944_1987.xlsx`: **genau 100 vollständig frei erfundene Beispielzeilen**.
- `Codiermatrix_e-newspaperarchives_Naturgefahrenforschung_Vergleichsdaten_ohne_Verzerrungskontext.xlsx`: **genau 100 vollständig frei erfundene Beispielzeilen**.

Die beiden Beispielmatrizen enthalten keine übernommenen Archivtexte, realen Artikelkennungen, privaten Notizen oder manuellen Forschungsnachcodierungen. Texte, URLs, Schadensangaben, Codierungen und Prüfstatus sind künstlich. `example.invalid` kennzeichnet nicht aufrufbare Demonstrationslinks. Historische Jahreszahlen, Zeitungskürzel und Suchbegriffe dienen nur als Parameter. Auch der Status *geprüft* ist in diesen Dateien erfunden. Die Zahlen in den Auswertungen sind ausschließlich Demoergebnisse.

Die Beispiele zeigen verschiedene Codes, zehn doppelte Artikelzuordnungen und vier Ausschlusszeilen je Matrix. Kategorien und Suchbegriffe können denselben Artikel mehrfach enthalten. Das Kompaktranking zählt Suchtreffer; die bereinigte Auswertung zählt stabile Artikelkennungen.

Die Kalibrierungsdemonstration enthält außerdem `08_Kontrollieren_Ausschliessen` mit ausschließlich aus den erfundenen Zeilen berechneten Prüfbeispielen. Die private manuelle Entscheidungsübersicht wurde nicht übernommen. Die gemeinsame Master- und Vergleichsstruktur umfasst zwölf Blätter; die Kalibrierungsdemonstration hat dieses zusätzliche dreizehnte Blatt.

`examples/build_demo_workbooks.py` erzeugt dieselben 100 Beispiele je Matrix ohne Zufallswerte und ohne Forschungsdateien einzulesen. Standardziel ist `examples/regenerated`; vorhandene Ausgaben werden nur mit `--overwrite` ersetzt. `examples/sample_capture_synthetic.json` zeigt das Capture-Format mit drei frei erfundenen Treffern.

`Setup_ENPA.cmd` erzeugt außerdem `Arbeitsmappen/Codiermatrix_Forschung.xlsx` als eigene leere Arbeitsdatei, sofern sie fehlt. Diese Datei bleibt ebenso wie echte Captures, Berichte und Sicherungen durch `.gitignore` aus Git ausgeschlossen. Die veröffentlichten Beispiele sind als Profile `calibration` und `comparison` für automatische Importe gesperrt. Standardmäßig schreibt der Import nur ins Profil `research`.

## Konfiguration und neue Forschungsvorhaben

`enpa_automation/config.json` ist die aktive Konfiguration; `config.example.json` dokumentiert den neutralen Ausgangsstand. Suchfenster, Suchbegriffe, Zeitungsauswahl, aktive Kategorien, Phasenschema und Pfade sind konfigurierbar. Die ausgelieferten Fenster bilden ein Beispiel für 1910 und seine Jubiläen. Das Programm untersucht diese Zeiträume erst nach bewusst ausgelösten Browserabfragen.

Für ein neues Forschungsvorhaben:

1. `Skripte/Build_ENPA_Master.cmd` ausführen und `Master_Codiermatrix_Leer.xlsx` unter einem eigenen Namen speichern.
2. Unter `workbookProfiles.research.path` und `workbook` denselben eigenen Dateipfad eintragen. `activeWorkbookProfile` bleibt `research`. Für weitere Profile können dieselben Regeln verwendet werden.
3. `queries`, `searchCategories`, `categoriesToRun` und `defaultPublications` auf das Untersuchungsdesign abstimmen. Vollständige Wortformen statt Sternchensuchen verwenden; Singular, Plural und historische Varianten getrennt erfassen.

`masterWorkbook` bleibt immer `${PROJECT_DIR}/Arbeitsmappen/Master_Codiermatrix_Leer.xlsx`. Der Builder ersetzt ausschließlich diese Datei und verweigert konfigurierte Forschungsdateien als Ausgabeziel. Umbenannte Kopien berührt er nicht. Wer Daten im festen Vorlagennamen belässt, verliert sie beim nächsten Builder-Lauf.

Die Pfadplatzhalter `${PROJECT_DIR}`, `${CONFIG_DIR}`, `${HOME}` und `${DOWNLOADS}` werden auf dem jeweiligen Rechner aufgelöst. Die ausgelieferte Konfiguration enthält keine fest eingetragenen Benutzerpfade.

Die vorhandenen Zeitungseinheiten der Auswertung sind *Der Bund*, *Seeländer Bote und Bieler Tagblatt* sowie *Neue Zürcher Zeitung*. Eine andere Gruppierung erfordert eine Anpassung von `PAPER_GROUPS` in `analysis_views.py`, den Zeitungskürzeln und den entsprechenden Vorcodierungsankern. Die vorhandenen Anker und Codes beziehen sich auf Naturgefahrenkommunikation; andere Themen benötigen eine eigene Kalibrierung.

## Erfassung und Import

1. `Skripte/Generate_ENPA_Links.cmd` starten, Falltyp wählen und die erzeugte `outputs/enpa_v2/manual_capture_links.html` im Browser öffnen.
2. Das Lesezeichen *ENPA erfassen* aus dieser HTML-Datei in die Browser-Lesezeichenleiste übernehmen.
3. Für jede Abfrage die erste Trefferseite öffnen und mit dem Lesezeichen als JSON speichern. Eventuelle Zugriffsschutzprüfungen erfolgen im normalen Browser.
4. Den Linkgenerator erneut ausführen. Er berechnet anhand der gespeicherten Gesamttrefferzahlen alle erforderlichen Folgeseiten mit jeweils 100 Treffern.
5. Jede Folgeseite einzeln öffnen und ebenfalls speichern. Eine Abfrage mit 347 Treffern benötigt vier gespeicherte Seiten.
6. `Skripte/Import_ENPA_Captures.cmd` ausführen. Es importiert nur Captures, die zu den aktuellen Suchfenstern, Kategorien, Suchbegriffen und erlaubten Falltypen passen.
7. Vorcodierungen in `01_Codierung` anhand der vollständigen Artikel und Digitalisate manuell prüfen. Nicht belegbare Werte bleiben leer oder *unklar*.
8. `Skripte/Validate_ENPA_Master.cmd` ausführen und die CSV-Berichte prüfen. `Skripte/Update_ENPA_Analysis.cmd` erzeugt zusätzlich eine Suchwortauswertung des aktiven Profils.

Die Matrix bewahrt Suchbegriff, Suchstring, Datum, URL und Ausschnitt jeder Suchfundzeile. Stabile Artikelkennungen verbinden Dubletten. Beim Import entstehen aktualisierte Hilfsblätter, Kurzübersicht, Auswertung und Kompaktranking. Exakte Wiederimporte erzeugen keine weiteren Zeilen. Der Import sichert die bisherige Datei und ersetzt sie erst nach einer Kandidatenprüfung.

*nachcodieren* bedeutet offene Prüfung; *geprüft* bezeichnet eine manuelle Entscheidung; *unklar* hält Unsicherheit fest. *ausschliessen* beziehungsweise der Altwert *auszuschliessen* entfernt eine Trefferzeile aus den Kennzahlen. Diese Statuswerte sind in `docs/datenwoerterbuch.md` erläutert.

## Bekannte Grenzen

Sehr lange Windows-Dateipfade können Excel am Öffnen einer Arbeitsmappe hindern. Bei einem tief verschachtelten Download- oder Projektverzeichnis den ganzen Projektordner in einen kurzen Pfad verschieben, beispielsweise `C:/ENPA`. Die Konfiguration bleibt durch die relativen Pfadplatzhalter gültig.

Cloudflare und sitzungsabhängige Zugriffe können die Browsererhebung unterbrechen. Das Werkzeug umgeht keinen Zugriffsschutz und führt keine unbeaufsichtigte Massenerhebung aus. Der Offline-Test belegt nur die lokale Verarbeitungskette.

OCR-Fehler und historische Schreibweisen beeinflussen Suche und Vorcodierung. Ein Suchsnippet kann mehrere Texte verbinden oder nur eine Überschrift enthalten. Die Trefferliste liefert nicht zuverlässig Druckseiten oder vollständige Artikeltexte; solche Felder bleiben ohne geprüfte Grundlage leer. OCR-Qualität erfordert manuelle Sichtung. Metadaten und Artikelgrenzen müssen ebenfalls geprüft werden.

Folgefragen zu historischen Aussagen, Archivvollständigkeit, Recall und Relevanz müssen am tatsächlichen Quellenbestand untersucht werden. Die Demoquoten messen keine Suchgüte. Prozentvergleiche setzen harmonisierte Suchfenster, Zeitungsauswahl, Begriffe, Einheiten, Relevanzregeln und Dublettenbehandlung voraus.

## Prüfung der Veröffentlichungskopie

Die Prüfverfahren und ihre Ergebnisse stehen in `docs/pruefung.md`. Die Kopie wurde in einem anders benannten Verzeichnis mit eigener Python-Umgebung auf demselben Windows-Rechner geprüft. Eine frische virtuelle Maschine und ein erneuter Live-Browserlauf sind damit nicht belegt.

Die Tests starten mit `python -m unittest discover -s enpa_automation -p "test_*.py"`. Der Offline-Test prüft zusätzlich Linkerzeugung, Import, Dubletten, Wiederimport, Schutz einer manuellen Testkorrektur, Validierung und Suchwortauswertung.

## Datenschutz, Veröffentlichung und Rechte

Das Paket enthält ausschließlich den benötigten Python-Kern, Windows-Starter, Begriffskataloge, Dokumentation und synthetische Beispiele. Forschungs-PDFs, Entwürfe, Chats, Rohcaptures, persönliche Metadaten, Browserprofile, Archive und frühere Fassungen gehören nicht zum Paket. Interne Node-Werkzeuge und Dokumentgeneratoren gehören nicht zum veröffentlichten Kern.

`.gitignore` schützt künftige lokale Forschungsdateien. Änderungen an bereits versionierten Beispielmatrizen werden dadurch nicht ausgeblendet; diese Dateien müssen synthetisch bleiben. Vor späteren Uploads `python enpa_automation/check_publication.py` ausführen. Dabei werden Dateien und XLSX-Inhalte kontrolliert; der Scan ersetzt keine inhaltliche Prüfung neuer eigener Daten.

GitHub blockiert reguläre Dateien über 100 MiB; beim Browserupload gelten 25 MiB pro Datei. Die hier gewünschte zusätzliche Obergrenze beträgt 100 MB für den gesamten Veröffentlichungsordner. [GitHub-Dateigrenzen](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

Die Lizenzwahl wurde nicht vorweggenommen. `LICENSE_STATUS.md` dokumentiert den aktuellen Stand ohne eine erfundene Erlaubnis zur Weiterverwendung. GitHub erlaubt Veröffentlichungen ohne gewählte Softwarelizenz; diese sind damit nicht automatisch Open Source. [GitHub-Lizenzhinweise](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

`CITATION.cff` enthält eine anonyme projektbezogene Zitierempfehlung ohne private Kontaktdaten. Für öffentliche Rückmeldungen kann nach dem Upload der Issues-Bereich des Repositories dienen. Angaben zu eingebundenen Namenskatalogen stehen in `THIRD_PARTY_NOTICES.md`. Zeitungsbilder, fremde Forschungspublikationen und umfangreiche Quellentexte werden nicht mitgeliefert.

Die lokale Kopie enthält keine alte Git-Historie und wurde noch nicht auf GitHub hochgeladen. Veröffentlichungsschritte stehen in `docs/veroeffentlichung.md`.

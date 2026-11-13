# Prüfung der Veröffentlichungskopie

Stand: 6. Oktober 2026; Version 2.7.0. Die Prüfungen betrafen ausschließlich neue Veröffentlichungskopien und synthetische Testdaten. Die ursprünglichen Forschungsdateien dienten nicht als Importziel.

## Nachgewiesene Ergebnisse

| Prüfung | Ergebnis |
| --- | --- |
| Python-Tests | 33 Tests aus den vier mitgelieferten Testmodulen bestanden. Sie prüften unter anderem Builder-Sicherheit, Dropdowns, Kategorien, Ausschlussstatus, Dubletten und Paginierung. |
| Verschobenes Projekt | Eine Kopie in einem anders benannten Verzeichnis mit Leerzeichen lief mit eigener virtueller Umgebung unter Python 3.12.14 und openpyxl 3.1.5. Projektinitialisierung, Selbsttest, Windows-Prüfstarter, Tests und Offline-Verarbeitung bestanden. |
| Einrichtungsstarter | `Setup_ENPA.cmd` lief mit der lokalen virtuellen Umgebung ohne ENPA-Python-Override durch. Die Prüfsumme einer bereits vorhandenen eigenen Arbeitsmappe blieb dabei unverändert. |
| Offline-Verarbeitung | Linkerzeugung, synthetischer Capture-Import, Wiederimport, Validierung und zusätzliche Suchwortauswertung liefen durch. Drei Suchfundzeilen ergaben zwei Artikelkennungen. Der Wiederimport ergänzte keine Zeilen und erhielt eine manuell gesetzte Testkorrektur. |
| Capture-Lesezeichen | Ein separater Test in einem frischen Chrome-Kontext lieferte zwei künstliche Treffer aus einer ausschließlich lokal bereitgestellten HTML-Seite. Gesamttrefferzahl, Titel, Zeitungszuordnung, Datum und Suchwort stimmten; die nicht belegbare Druckseite blieb leer. Dieser Test benötigte externe Testwerkzeuge, die nicht zum Laufzeitpaket gehören. |
| Excel | Microsoft Excel 16.0 öffnete und berechnete alle drei veröffentlichten Arbeitsmappen. Der Scan fand keine Formelfehler. Tabellen, Filter und Datenvalidierungen waren vorhanden. |
| Master | Keine Codierdatensätze; Auswertungszahlen null. Zwölf Blätter einschließlich Auswertung, Kompaktranking und Dublettenhilfe. |
| Vergleichsdemonstration | Genau 100 frei erfundene Zeilen; zwölf Blätter. |
| Kalibrierungsdemonstration | Genau 100 frei erfundene Zeilen; dreizehn Blätter einschließlich der synthetischen Kontrollübersicht. |
| Datenschutz | Dateitypen, Textdateien und die XML-Inhalte der XLSX-Dateien wurden auf E-Mail-Muster, absolute Benutzerpfade und mögliche Zugangsdaten geprüft. Ein zusätzlicher Namensscan sowie die Kontrolle der Arbeitsmappen-Metadaten fanden keine übernommenen persönlichen Angaben. |
| Git-Dateiauswahl | Ein getrennter Git-Testverlauf nahm genau die 53 vorgesehenen Paketdateien auf. Eigene Forschungsdateien, Ausgaben, virtuelle Umgebung, Archive und Wordentwürfe blieben durch die Ausschlussregeln unberücksichtigt. Der Testverlauf wurde nicht mitgeliefert. |
| Originalschutz | Die Prüfsummen von 35 ursprünglich erfassten Kern-, Starter-, Konfigurations- und Arbeitsmappendateien blieben unverändert. Im ursprünglichen Projekt wurde nichts gelöscht oder bearbeitet. |

Die beiden Demonstrationsmatrizen lieferten in Excel jeweils 96 nicht ausgeschlossene Suchfundzeilen, 88 unterschiedliche Artikelkennungen und 31 relevante Artikel der Codes N1–N3. Vier Zeilen trugen den Ausschlussstatus. Diese Werte dienen ausschließlich zur Funktionskontrolle; sie sind keine historischen Ergebnisse oder gemessenen Suchqualitäten.

Nach der Excel-Berechnung wurden persönliche Bearbeitungsmetadaten und absolute Speicherpfade aus den neuen XLSX-Dateien entfernt. Die Zellen, Formelresultate und Validierungen blieben erhalten. Eine anschließende Öffnungsprüfung entdeckte zunächst einen Namespacefehler in der Metadatenbereinigung. Nach dessen Korrektur öffnete Excel alle drei finalen Dateien am Veröffentlichungsspeicherort erneut erfolgreich. Die ausschließlich lesende Kontrolle veränderte ihre Prüfsummen nicht.

## Grenzen der Prüfung

Der Verzeichnistest erfolgte auf demselben Windows-Rechner, nicht auf einer frischen virtuellen Maschine. Er prüfte die Unabhängigkeit vom ursprünglichen Projektpfad und von dessen Python-Abhängigkeiten; er ersetzt keinen Test aller Windows- und Python-Konfigurationen.

Es fand keine erneute Live-Erhebung auf e-newspaperarchives.ch statt. Die Offline-Prüfung belegt weder den aktuellen Aufbau der Archivoberfläche noch die Überwindung von Zugriffsschutz. Andere Tabellenprogramme wurden nicht geprüft. OCR-Güte und historische Aussagekraft lassen sich nicht anhand erfundener Zeilen validieren.

## Wiederholbare Prüfungen

Nach der Einrichtung im Projektverzeichnis:

```text
python -m unittest discover -s enpa_automation -p "test_*.py"
python enpa_automation/portable_selftest.py
python enpa_automation/offline_demo.py
python enpa_automation/check_publication.py
```

Wenn die Projektumgebung nicht aktiviert ist, statt `python` die Datei `.venv/Scripts/python.exe` verwenden. Die Offline-Demonstration arbeitet in einem temporären Projekt und verändert keine Forschungsdatei. Der Veröffentlichungsscan arbeitet nur lesend. Den synthetischen Inhalt neu hinzugefügter Veröffentlichungsdateien muss die veröffentlichende Person zusätzlich selbst kontrollieren.

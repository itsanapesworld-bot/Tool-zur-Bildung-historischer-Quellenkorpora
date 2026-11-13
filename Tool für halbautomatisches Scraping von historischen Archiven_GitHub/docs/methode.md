# Verarbeitung und manuelle Prüfung

Die Konfiguration legt Suchfenster, Zeitungen und vollständige Suchwortformen fest. Der Linkgenerator bildet daraus nachvollziehbare ENPA-Abfragen. Ein Browser-Lesezeichen sichert die auf der Trefferseite sichtbaren Metadaten und Ausschnitte. Alle Folgeseiten müssen gesondert erfasst werden.

Der Import prüft die Capture-Provenienz gegen die aktuelle Konfiguration, überspringt bereits importierte Kombinationen von Artikelkennung, Kategorie und Abfrage und vergibt fortlaufende Treffer-IDs. Verschiedene Suchfunde desselben Artikels bleiben als Suchprovenienz erhalten. Das Feld *Dublette zu ID* verbindet sie.

Die Vorcodierung sucht im vorhandenen Text nach Naturgefahren-, Schadens-, Orts- und weiteren Kontextankern. Sie gewichtet die Regeln in der Reihenfolge des aktuellen Codes und hält unsichere Fälle als *UN*, *O1* oder *nachcodieren* offen. Sie ersetzt weder Digitalisatprüfung noch historische Interpretation. Die Anker befinden sich in `enpa_common.py` und in den drei Namenskatalogen; die Feldentscheidungen in `import_captures.py`.

`01_Codierung` bleibt die Stelle für manuelle Korrekturen. `07_Kurzübersicht` bündelt Artikel und Suchprovenienz. `98_Dubletten_Hilfe` dokumentiert die Artikelgruppen. `97_Auswertung_Hilfe` enthält die Formeln für Rohzeilen, bereinigte Artikel, Kategorien und Ausschlüsse. `05_Auswertung` liefert die Kennzahlen und Filter nach Zeitung, Untersuchungsjahr, Ereignisjahr und Fensterart. `09_Kompakt_Ranking` vereinigt konfigurierte Schreibvarianten zu Sammelbegriffen; seine Zähleinheit bleibt die Suchfundzeile.

Bei bereinigten Kennzahlen liefert der Eintrag mit der kleinsten Treffer-ID den maßgeblichen Hauptcode. Suchkategorien dürfen denselben Artikel enthalten und sind deshalb nicht zur Artikelgesamtsumme addierbar. Codekonflikte bleiben sichtbar. Ausschlussstatus entfernt die betreffende Suchfundzeile aus den Kennzahlen. Auch nach regelbasierter Deduplizierung müssen unsichere Artikelgrenzen geprüft werden.

Der Import baut abhängige Ansichten und Formelgrenzen neu auf. Änderungen vorhandener Codierwerte lösen Excel-Neuberechnung aus. Neue manuelle Zeilen, geänderte Artikelkennungen, Datumsangaben oder Suchkategorien können einen erneuten Aufbau der Hilfsansichten erfordern. Der Offline-Test demonstriert die Wiederholung des Imports, ohne Forschungsdateien anzufassen.

Die Suchfenster des mitgelieferten Beispiels umfassen 21 Tage einschließlich des ersten Tages und jeweils sieben Tage für Jubiläen. Diese Parameter sind kein universelles Untersuchungsdesign. Suchwörter, Anker und Regeln müssen am jeweiligen Forschungsgegenstand geprüft werden. Keine Demoauswertung liefert empirische Präzision, Recall oder historische Häufigkeiten.

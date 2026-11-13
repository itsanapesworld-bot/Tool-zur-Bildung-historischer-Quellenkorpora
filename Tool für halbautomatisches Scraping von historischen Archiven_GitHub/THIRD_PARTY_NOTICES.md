# Abhängigkeiten und Namenskataloge

## Python

Der Betrieb benötigt Python und openpyxl einschließlich dessen Abhängigkeit et-xmlfile. Diese Software wird nicht in das Paket kopiert; Setup installiert sie separat. Die jeweilige Lizenz und Herkunft sind den installierten Paketen zu entnehmen. Python: https://www.python.org/ ; openpyxl: https://openpyxl.readthedocs.io/ ; et-xmlfile: https://et-xmlfile.readthedocs.io/ .

## Namenskataloge

`swiss_municipality_catalog.py` enthält Ortsnamen und Varianten, die laut vorhandenem Katalogkopf aus einer Gemeindestands-Arbeitsmappe sowie historischen Gemeindebezeichnungen zusammengestellt wurden. Die ursprüngliche Arbeitsmappe ist nicht Bestandteil dieser Veröffentlichungskopie. Eine genaue, im Ursprungskatalog nicht enthaltene Download-URL oder Lizenz wird hier nicht erfunden.

`swiss_water_catalog.py` enthält Gewässernamen aus der projekterstellten Liste `enpa_automation/data/schweizer_gewaesser_uebersicht_20260820.md`. Die Liste ist ein Arbeitskatalog und kein nachgewiesener vollständiger amtlicher Bestand.

`non_swiss_place_catalog.py` enthält Ortsnamen und Schreibvarianten aus `enpa_automation/data/non_swiss_places_20260811.txt`. Es handelt sich um einen Begriffskatalog für regelbasierte Textanker, nicht um Personen- oder Zeitungstextdaten. Die Datumsangaben bezeichnen den übernommenen Katalogstand.

Die ursprünglichen Wartungswerkzeuge und Quellarbeitsmappen wurden nicht mitgeliefert. Die Kataloge sind direkt lesbare Python- beziehungsweise Textdateien. Die Vorcodierung benötigt keine Laufzeitdownloads dieser Kataloge. Ihre inhaltliche Genauigkeit und Eignung müssen für neue Untersuchungsräume geprüft werden.

## Archiv

Dieses Werkzeug ist keine offizielle Software von e-newspaperarchives.ch. ENPA-Namen und reale Zeitungskürzel dienen der Beschreibung der Schnittstelle. Es werden keine Zeitungsscans, Originalartikel oder Archiveigenen Softwarebibliotheken mitgeliefert.

# Codiermatrix und Statuswerte

Eine Zeile in `01_Codierung` bezeichnet einen Suchfund zu einer bestimmten Abfrage. Mehrere Zeilen können denselben Artikel betreffen. Die Spalten bleiben zwischen leerer Vorlage, Beispielen und Import identisch.

| Spalte | Bedeutung |
| --- | --- |
| ID | Fortlaufende, dauerhafte Kennung einer Suchfundzeile. |
| Falljahr | Jahr des zugehörigen Untersuchungsfensters. |
| Falltyp | Konfigurierter Untersuchungszweck. |
| Zeitung | Internes Zeitungskürzel, beispielsweise DBU, SEB, BT oder NZZ. |
| Ausgabe-Datum | Datum der Zeitungsausgabe. |
| Zeitung-Nr. | Ausgabenummer, sofern verfügbar. |
| Seite | Gedruckte Seite; ohne überprüfbare Grundlage leer. |
| Artikel-/Segment-ID | Segmentkennung beziehungsweise erfasste Segmentüberschrift. |
| URL e-newspaperarchives | Quellenadresse; in Beispielen ausschließlich example.invalid. |
| Suchkategorie A-H | Konfigurierte Suchwortgruppe. |
| Suchbegriff | Zugeordneter Trefferbegriff, nicht automatisch der gesamte Suchstring. |
| Suchstring / Abfrage | Tatsächliche Suchabfrage für die Provenienz. |
| OCR-Ausschnitt / Textstelle | Verfügbarer Textausschnitt des Suchfunds. |
| Vollartikel geprüft? | Manuelle Prüfung: Ja oder Nein; ohne Entscheidung leer. |
| Hauptcode | Maßgebliche thematische Vor- beziehungsweise Nachcodierung. |
| Nebencode 1 | Zusätzlicher thematischer Code. |
| Nebencode 2 | Zweiter zusätzlicher thematischer Code. |
| Ereignisbezug | direkt, indirekt, kein Bezug oder unklar. |
| Raumbezug | Regelbasierter beziehungsweise manuell geprüfter räumlicher Bezug. |
| Relevanzgrad 0-5 | Grad des thematischen Bezugs; keine Trefferwahrscheinlichkeit. |
| OCR-Qualität 1-5 | Manuell zu prüfende Lesbarkeit; ohne Sichtprüfung leer. |
| Segmentierungsproblem | Festgestellte beziehungsweise vermutete Probleme der Artikelgrenze. |
| Dublette zu ID | Verknüpfte Suchfund-IDs desselben Artikels. |
| Nachrichtenwert Nähe 0-5 | Text- und Raumanker als regelbasierte Vorbereitung. |
| Nachrichtenwert Schaden 0-5 | Textlich dargestellter Schadensbezug; kein gemessenes objektives Schadensausmaß. |
| Nachrichtenwert Konflikt 0-5 | Im Text erkannter Konfliktbezug. |
| Nachrichtenwert Aktualität 0-5 | Regelbasierte zeitliche Zuordnung, sofern hinreichend belegbar. |
| Risikokommunikation / Phase | Kommunikationskategorie des aktiven Phasenschemas. |
| Deutungsmuster | Vorbereitete Deutungszuordnung anhand von Textankern. |
| Kurzbegründung Codierung | Begründung der Feldentscheidungen. |
| Kontrollstatus | Offene, geprüfte, unklare oder ausgeschlossene Zeile. |
| Codierer:in | Manuell eintragbare Kennung; in Beispielen Demo. |
| Codiert am | Datum der Codierung. |
| Prüfbemerkung | Offene Punkte und Hinweise für die Nachprüfung. |
| Volltext | Optionaler manuell beziehungsweise gesondert gesicherter Artikeltext; Trefferlisten liefern ihn nicht zuverlässig. |

Die Codebedeutungen stehen in `02_Codebuch`: N1 Naturgefahr Schweiz direkt, N2 Ausland direkt, N3 indirekte Naturgefahrenkommunikation, M1/M2 menschengemachte Gefahr national/international, K1 Krieg/Konflikt, U1 Umwelt/Klima allgemein, W1 Werbung/Inserat, S1 themenfern, O1 OCR/Segment unklar, UN unklar. Der historische Dublettencode D1 ersetzt die aktuellen Artikelverknüpfungen nicht.

*nachcodieren* ist eine offene Prüfung. *geprüft* kennzeichnet eine manuelle Entscheidung. *unklar* hält verbleibende Unsicherheit fest. *ausschliessen* und der Altwert *auszuschliessen* unterdrücken die betreffende Zeile in der Auswertung. Keine dieser Bezeichnungen belegt bei den synthetischen Beispielen einen realen Prüfungsvorgang.

Das standardmäßig aktive Phasenschema bleibt `legacy_v1`. Das optional verfügbare `functional_v2` darf nur nach eigener methodischer Entscheidung aktiviert werden. Bei einem Schemawechsel dürfen alte und neue Zuordnungen nicht unbemerkt vermischt werden.

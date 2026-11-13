# Lokale Veröffentlichungskopie auf GitHub übernehmen

Dieser Ordner ist die bereinigte Veröffentlichungskopie. Das ursprüngliche Forschungsprojekt gehört nicht in das Repository. Die beigefügten XLSX-Dateien enthalten nur die leere Vorlage und synthetische Demonstrationen.

1. `python enpa_automation/check_publication.py` ausführen und die Dateiliste prüfen.
2. Bei einem Git-Upload hier einen neuen Verlauf anlegen: `git init -b main`. Die `.git`-Historie des Forschungsprojekts wurde nicht kopiert.
3. `git add -n .` zeigt die geplanten Dateien. Nach Kontrolle `git add .` und `git status --short` ausführen. Keine eigenen echten Forschungsdateien ergänzen.
4. Einen Commit erstellen und den Ordner gemäß der offiziellen GitHub-Anleitung mit einem neu angelegten Repository verbinden. Bei einer zunächst privaten Veröffentlichung die GitHub-Dateiliste und herunterladbare Fassung kontrollieren, bevor die Sichtbarkeit geändert wird.

Es wurden keine GitHub-Zugangsdaten oder Remote-Adresse eingetragen, keine persönlichen Git-Autorendaten gesetzt und keine Dateien hochgeladen. `CITATION.cff` enthält keine erfundene Repository-URL; die echte URL kann nach der Veröffentlichung ergänzt werden.

Die Lizenzentscheidung bleibt in `LICENSE_STATUS.md` ausdrücklich offen. GitHub erfordert für das Hochladen keine Open-Source-Lizenz. Eine bewusst gewählte Nutzungsfreigabe muss die Rechteinhaberschaft separat festlegen.

GitHub begrenzt reguläre Einzeldateien auf 100 MiB und Browseruploads auf 25 MiB pro Datei. Die Veröffentlichungskopie hält zusätzlich die verlangte Grenze von 100 MB für den gesamten Ordner ein. Ein ZIP ist eine Transportdatei; um die Software als Repository nutzbar zu machen, werden seine entpackten Inhalte versioniert.

Offizielle Quellen:

- https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github
- https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository

"""Build the complete, data-free ENPA workbook from code and configuration only."""
from __future__ import annotations

import argparse
import os
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.views import Selection

from analysis_views import refresh_analysis_views
from compact_ranking import update_compact_ranking
from enpa_common import (
    CODEBOOK_ROWS, CODING_HEADERS, DEFAULT_CONFIG, LISTS, WRAPPED_TEXT_HEADERS,
    clean, expand_categories, load_config, resolve_config_path, risk_phase_values,
)

OUTPUT_BASENAME = "Master_Codiermatrix_Leer.xlsx"
MAX_CODING_ROWS = 60000
MASTER_CODING_HEADERS = CODING_HEADERS + ["Volltext"]
RECALL_HEADERS = ["Falljahr", "Ereignis", "Bekannter Treffer", "Gefunden?", "Suchkategorie", "Suchbegriff", "Bemerkung"]
SHEET_NAMES = [
    "00_Readme", "01_Codierung", "06_Recall_Kontrolle", "02_Codebuch",
    "03_Suchbegriffe", "04_Falljahre_Korpus", "05_Auswertung", "07_Kurzübersicht",
    "99_Listen", "09_Kompakt_Ranking", "98_Dubletten_Hilfe", "97_Auswertung_Hilfe",
]
VALIDATION_MAP = {
    "Falltyp": "Falltyp", "Zeitung": "Zeitung", "Suchkategorie A-H": "Suchkategorie",
    "Vollartikel geprüft?": "Vollartikel geprüft", "Hauptcode": "Code",
    "Nebencode 1": "Code", "Nebencode 2": "Code", "Ereignisbezug": "Ereignisbezug",
    "Raumbezug": "Raumbezug", "Relevanzgrad 0-5": "Relevanz", "OCR-Qualität 1-5": "OCR",
    "Segmentierungsproblem": "Segmentierungsproblem", "Nachrichtenwert Nähe 0-5": "Nachrichtenwert Nähe",
    "Nachrichtenwert Schaden 0-5": "Nachrichtenwert Schaden", "Nachrichtenwert Konflikt 0-5": "Nachrichtenwert Konflikt",
    "Nachrichtenwert Aktualität 0-5": "Nachrichtenwert Aktualität",
    "Risikokommunikation / Phase": "Risikophase", "Deutungsmuster": "Deutungsmuster", "Kontrollstatus": "Kontrollstatus",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Erstellt eine vollständige leere ENPA-Codiermatrix ohne Excelvorlage.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--output", default="")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def configured_path(config, key):
    value = clean(config.get(key))
    return resolve_config_path(config, value) if value else None


def protected_workbooks(config):
    paths = set()
    active = configured_path(config, "workbook")
    if active:
        paths.add(active.resolve())
    for spec in (config.get("workbookProfiles") or {}).values():
        path = resolve_config_path(config, spec.get("path"))
        if path:
            paths.add(path.resolve())
    return paths


def resolve_output(config, argument):
    output = Path(argument).resolve() if argument else configured_path(config, "masterWorkbook")
    if output is None:
        raise ValueError("config.json benötigt masterWorkbook.")
    output = output.resolve()
    if output.name.casefold() != OUTPUT_BASENAME.casefold():
        raise ValueError(f"Der Builder darf nur {OUTPUT_BASENAME} erzeugen: {output}")
    if output in protected_workbooks(config):
        raise ValueError(f"Geschützte Forschungsarbeitsmappe darf nicht überschrieben werden: {output}")
    return output


def style_header(ws, row=1, end=None):
    for cell in ws[row][:end or ws.max_column]:
        cell.fill = PatternFill("solid", fgColor="4472C4")
        cell.font = Font(name="Arial", size=11, bold=True, color="FFFFFF")
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 34


def write_row(ws, row, values):
    for col, value in enumerate(values, 1):
        ws.cell(row, col, value)
        ws.cell(row, col).alignment = Alignment(vertical="top", wrap_text=True)


def add_table(ws, name, ref):
    table = Table(displayName=name, ref=ref)
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True, showColumnStripes=False)
    ws.add_table(table)


def list_formula(column, length):
    letter = get_column_letter(column)
    return f"='99_Listen'!${letter}$2:${letter}${length + 1}"


def add_validation(ws, col, formula, max_row=MAX_CODING_ROWS):
    # Public API also used by apply_master_dropdowns.py.
    dv = DataValidation(type="list", formula1=formula, allow_blank=True, showDropDown=False,
                        errorTitle="Ungültiger Wert", error="Bitte einen Wert aus der Dropdown-Liste auswählen.", showErrorMessage=True)
    ws.add_data_validation(dv)
    letter = get_column_letter(col)
    dv.add(f"{letter}2:{letter}{max_row}")


def build_lists_sheet(wb, config):
    ws = wb["99_Listen"]
    lists = dict(LISTS)
    lists["Risikophase"] = risk_phase_values(config)
    if config.get("phaseCodingScheme", "functional_v2") == "legacy_v1":
        lists["Risikophase"] = list(dict.fromkeys(["Vorlauf"] + lists["Risikophase"]))
    mapping = {}
    for col, (name, items) in enumerate(lists.items(), 1):
        ws.cell(1, col, name)
        for row, item in enumerate(items, 2):
            ws.cell(row, col, item)
        ws.column_dimensions[get_column_letter(col)].width = max(14, min(35, len(name) + 4))
        mapping[name] = (col, len(items))
    style_header(ws)
    return mapping


def build_coding_sheet(wb, lists):
    ws = wb["01_Codierung"]
    write_row(ws, 1, MASTER_CODING_HEADERS)
    style_header(ws)
    widths = [10, 10, 24, 10, 14, 12, 10, 34, 48, 16, 26, 42, 70, 18,
              16, 16, 16, 16, 18, 18, 18, 24, 16, 18, 18, 18, 18, 26,
              24, 44, 18, 18, 14, 48, 70]
    for col, (header, width) in enumerate(zip(MASTER_CODING_HEADERS, widths), 1):
        dim = ws.column_dimensions[get_column_letter(col)]
        dim.width = width
        dim.alignment = Alignment(vertical="top", wrap_text=header in WRAPPED_TEXT_HEADERS or header == "Volltext")
        ws.cell(2, col).alignment = copy(dim.alignment)
        if header in ("Ausgabe-Datum", "Codiert am"):
            dim.number_format = "dd.mm.yyyy" if header == "Ausgabe-Datum" else "yyyy-mm-dd"
            ws.cell(2, col).number_format = dim.number_format
    ws.row_dimensions[2].height = 28
    add_table(ws, "CodierungDaten", "A1:AI2")
    columns = {header: col for col, header in enumerate(MASTER_CODING_HEADERS, 1)}
    for header, list_name in VALIDATION_MAP.items():
        list_col, length = lists[list_name]
        add_validation(ws, columns[header], list_formula(list_col, length))


def build_recall_sheet(wb):
    ws = wb["06_Recall_Kontrolle"]
    write_row(ws, 1, RECALL_HEADERS)
    style_header(ws)
    for col, width in enumerate([12, 32, 44, 14, 16, 24, 50], 1):
        ws.column_dimensions[get_column_letter(col)].width = width
        for row in range(2, 51):
            ws.cell(row, col).alignment = Alignment(wrap_text=True, vertical="top")
    for row in range(2, 51):
        ws.row_dimensions[row].height = 28.5
    add_table(ws, "RecallKontrolleDaten", "A1:G50")


def build_reference_sheets(wb, config):
    ws = wb["02_Codebuch"]
    write_row(ws, 1, ["Code", "Kategorie", "Definition"])
    for row, values in enumerate(CODEBOOK_ROWS, 2):
        write_row(ws, row, values)
        ws.row_dimensions[row].height = 32
    write_row(ws, len(CODEBOOK_ROWS) + 2, ["D1", "Dublette (historischer Code)", "Bereits erfasster Artikel. Die aktuelle Dublettenbereinigung verwendet stabile Artikel-IDs und das Feld Dublette zu ID; D1 ist kein automatischer Relevanzcode."])
    ws.row_dimensions[len(CODEBOOK_ROWS) + 2].height = 44
    style_header(ws)
    for col, width in zip("ABC", [10, 34, 90]):
        ws.column_dimensions[col].width = width
    ws = wb["03_Suchbegriffe"]
    write_row(ws, 1, ["Kategorie", "Label", "Begriff", "historisch", "Suchstring-Hinweis"])
    row = 2
    for category in expand_categories(config):
        data = config["searchCategories"][category]
        for historical, key in (("nein", "terms"), ("ja", "historicalTerms")):
            for term in data.get(key, []):
                hint = "Historische Form gemäss includeHistoricalTermsForYearsUpTo." if historical == "ja" else "Mehrwort- und Bindestrichbegriffe werden in Anführungszeichen gesucht."
                write_row(ws, row, [category, data.get("label", ""), term, historical, hint])
                row += 1
    style_header(ws)
    add_table(ws, "SuchbegriffeDaten", f"A1:E{max(2, row - 1)}")
    for col, width in zip("ABCDE", [12, 38, 34, 12, 70]):
        ws.column_dimensions[col].width = width
    ws = wb["04_Falljahre_Korpus"]
    write_row(ws, 1, ["Name", "Ereignis", "Ereignisbeginn", "Ereignisende", "Fenster", "Von", "Bis"])
    keys = ["name", "eventName", "eventStart", "eventEnd", "windowType", "dateFrom", "dateTo"]
    for row, query in enumerate(config.get("queries", []), 2):
        write_row(ws, row, [query.get(key, "") for key in keys])
        ws.row_dimensions[row].height = 32
    style_header(ws)
    for col in range(1, 8):
        ws.column_dimensions[get_column_letter(col)].width = 48 if col == 1 else 32 if col == 2 else 24


def style_analysis(wb):
    ws = wb["05_Auswertung"]
    ws.merge_cells("A1:R1")
    ws["A1"].font = Font(name="Arial", size=14, bold=True, color="FFFFFF")
    ws.row_dimensions[1].height = 30
    for row in range(3, 7):
        ws.merge_cells(start_row=row, start_column=5, end_row=row, end_column=8)
        ws.cell(row, 5).fill = PatternFill("solid", fgColor="E2EFDA")
        ws.cell(row, 5).alignment = Alignment(wrap_text=True, vertical="center")
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.column_dimensions["A"].width = 47
    ws.row_dimensions[10].height = 40
    for row in range(21, 25):
        ws.row_dimensions[row].height = 42
    for row in range(1, ws.max_row + 1):
        if ws.cell(row, 1).value in ("Kategorie", "Zeitungseinheit"):
            ws.row_dimensions[row].height = 58
        elif ws.cell(row, 1).value and str(ws.cell(row, 1).value).startswith(("Gesamtbestand", "Auswertung nach")):
            ws.row_dimensions[row].height = 30
        elif row >= 28:
            ws.row_dimensions[row].height = 30
    for name in ("07_Kurzübersicht", "98_Dubletten_Hilfe", "97_Auswertung_Hilfe"):
        sheet = wb[name]
        style_header(sheet)
        for col in range(1, sheet.max_column + 1):
            sheet.column_dimensions[get_column_letter(col)].width = 24
            sheet.cell(2, col).alignment = Alignment(wrap_text=True, vertical="top")
        sheet.row_dimensions[2].height = 28
    wb["07_Kurzübersicht"].column_dimensions["G"].width = 70
    wb["07_Kurzübersicht"].column_dimensions["D"].number_format = "dd.mm.yyyy"
    wb["98_Dubletten_Hilfe"].sheet_state = "visible"
    wb["97_Auswertung_Hilfe"].sheet_state = "hidden"


def build_readme(wb):
    ws = wb["00_Readme"]
    rows = [
        ["ENPA Master-Codiermatrix – leere Vorlage"],
        ["Aufbau", "Vollständig aus Python-Code und Konfiguration erzeugt. Keine befüllte Exceldatei wird als Vorlage gelesen."],
        ["Workflow", "1. Vorlage unter eigenem Namen speichern. 2. Suchlinks erzeugen. 3. Treffer als Capture-JSON erfassen. 4. Captures importieren. 5. Vorcodierungen manuell prüfen. 6. Arbeitsmappe validieren."],
        ["Codierung", "01_Codierung enthält die Originaldaten und Nachcodierungen. Die Dropdowns gelten bis Zeile 60000; OCR-Qualität bleibt ohne manuelle Prüfung leer."],
        ["Ausschluss", "Kontrollstatus ausschliessen (auch Altwert auszuschliessen) entfernt Beiträge aus allen Auswertungen. 05_Auswertung weist die ausgeschlossenen Zeilen separat aus."],
        ["Ansichten", "05_Auswertung und Hilfsblätter sowie 07_Kurzübersicht werden nach Importen aus 01_Codierung aufgebaut. Bestehende Zeilen reagieren über Formeln auf Nachcodierungen."],
        ["Ranking", "09_Kompakt_Ranking zählt Suchtreffer, nicht eindeutige Artikel. Gesamtsumme addiert alle Begriffe unabhängig vom Tabellenfilter; die Gesamtquote ist Summe relevant geteilt durch Summe Treffer."],
        ["Recall-Kontrolle", "06_Recall_Kontrolle ist eine formatierte Tabelle mit sieben Überschriften, 49 leeren Eingabezeilen und Filtern. Bekannte Kontrollbeiträge müssen selbst eingetragen werden."],
        ["Schutzregel", "Der Builder darf ausschliesslich Master_Codiermatrix_Leer.xlsx ersetzen, niemals eine konfigurierte Forschungsarbeitsmappe."],
    ]
    for row, values in enumerate(rows, 1):
        write_row(ws, row, values)
        ws.row_dimensions[row].height = 45 if row > 1 else 30
    ws["A1"].font = Font(name="Arial", size=14, bold=True)
    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 110


def build_workbook(config):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name in SHEET_NAMES:
        wb.create_sheet(name)
    build_coding_sheet(wb, build_lists_sheet(wb, config))
    build_recall_sheet(wb)
    build_reference_sheets(wb, config)
    refresh_analysis_views(wb, config)
    style_analysis(wb)
    columns = {header: col for col, header in enumerate(MASTER_CODING_HEADERS, 1)}
    update_compact_ranking(wb, wb["01_Codierung"], columns, 2, config, include_catalog=True)
    ranking = wb["09_Kompakt_Ranking"]
    last = int(ranking.tables["KompaktRankingLive"].ref.split("G")[1]) - 1
    ranking.conditional_formatting.add(f"G2:G{last}", ColorScaleRule(start_type="min", start_color="F8696B", mid_type="percentile", mid_value=50, mid_color="FFEB84", end_type="max", end_color="63BE7B"))
    build_readme(wb)
    for ws in wb:
        ws.freeze_panes = None
        ws.sheet_view.topLeftCell = "A1"
        ws.sheet_view.selection = [Selection(activeCell="A1", sqref="A1")]
        ws.sheet_view.tabSelected = ws.title == "01_Codierung"
        ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.active = SHEET_NAMES.index("01_Codierung")
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    return wb


build_master = build_workbook


def validate_candidate(path):
    wb = openpyxl.load_workbook(path, data_only=False)
    try:
        if set(wb.sheetnames) != set(SHEET_NAMES):
            raise ValueError("Kandidatenprüfung: Arbeitsblätter fehlen.")
        ws = wb["01_Codierung"]
        if [cell.value for cell in ws[1]] != MASTER_CODING_HEADERS:
            raise ValueError("Kandidatenprüfung: Codierungsspalten fehlen.")
        if any(clean(value) for row in ws.iter_rows(min_row=2, values_only=True) for value in row):
            raise ValueError("Kandidatenprüfung: Vorlage enthält Forschungsdaten.")
        if ws.tables["CodierungDaten"].ref != "A1:AI2" or len(ws.data_validations.dataValidation) != len(VALIDATION_MAP):
            raise ValueError("Kandidatenprüfung: Eingabetabelle oder Dropdowns fehlen.")
        recall = wb["06_Recall_Kontrolle"]
        if [cell.value for cell in recall[1]] != RECALL_HEADERS or recall.tables["RecallKontrolleDaten"].autoFilter is None:
            raise ValueError("Kandidatenprüfung: Recall-Überschriften oder Filter fehlen.")
        analysis = wb["05_Auswertung"]
        if analysis.freeze_panes or analysis["A10"].value != "Ausgeschlossene Beiträge ohne Einfluss auf die Auswertung":
            raise ValueError("Kandidatenprüfung: Auswertung ist nicht aktuell.")
        if len(analysis.data_validations.dataValidation) != 4 or wb["97_Auswertung_Hilfe"].max_column != 31:
            raise ValueError("Kandidatenprüfung: Auswertungsfilter oder Ausschlusshilfe fehlen.")
        if wb["09_Kompakt_Ranking"].tables["KompaktRankingLive"].totalsRowCount != 1:
            raise ValueError("Kandidatenprüfung: Ranking-Summenzeile fehlt.")
        if any(dim.hidden for dim in ws.row_dimensions.values()):
            raise ValueError("Kandidatenprüfung: Eingabezeilen sind ausgeblendet.")
        count = sum(cell.data_type == "f" for row in analysis for cell in row)
        if count < 100:
            raise ValueError("Kandidatenprüfung: Auswertungsformeln fehlen.")
        return {"sheets": len(wb.sheetnames), "analysis_formulas": count, "coding_dropdowns": len(VALIDATION_MAP)}
    finally:
        wb.close()


def main():
    args = parse_args()
    config = load_config(args.config)
    output = resolve_output(config, args.output)
    if output.exists() and not args.overwrite:
        raise FileExistsError(f"Datei existiert bereits: {output}. Nutze --overwrite.")
    output.parent.mkdir(parents=True, exist_ok=True)
    candidate = output.with_name(f".{output.stem}.tmp{output.suffix}")
    wb = build_workbook(config)
    try:
        wb.save(candidate)
        wb.close()
        validation = validate_candidate(candidate)
        os.replace(candidate, output)
    finally:
        wb.close()
        candidate.unlink(missing_ok=True)
    print(f"MASTER={output}")
    print("VORLAGE=Keine; vollständig aus Code und Konfiguration erzeugt.")
    print(f"VALIDIERUNG={validation}")
    print("SCHUTZ=Forschungsarbeitsmappen wurden weder gelesen noch verändert.")


if __name__ == "__main__":
    main()

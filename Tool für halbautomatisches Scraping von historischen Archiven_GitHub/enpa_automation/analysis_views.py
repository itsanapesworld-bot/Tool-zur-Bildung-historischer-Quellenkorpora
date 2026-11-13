from __future__ import annotations

import re
from collections import defaultdict
from copy import copy
from datetime import date, datetime
from typing import Any
from urllib.parse import parse_qs, urlparse

from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.filters import AutoFilter
from openpyxl.worksheet.table import Table, TableColumn, TableFormula, TableStyleInfo

from enpa_common import CODING_HEADERS, SHORT_OVERVIEW_HEADERS, clean, find_col, header_map


PAPER_GROUPS = [
    ("Der Bund", {"DBU", "DBB"}),
    ("Seeländer Bote und Bieler Tagblatt", {"SEB", "SLB", "BT", "BTB"}),
    ("Neue Zürcher Zeitung", {"NZZ"}),
]
PHASE_LABELS = {
    "primary": "Hauptuntersuchungszeitraum",
    "anniversary_1": "1-Jahresjubiläum",
    "anniversary_5": "5-Jahresjubiläum",
    "anniversary_10": "10-Jahresjubiläum",
}
EXCLUDED_STATUSES = {"ausschliessen", "auszuschliessen"}
HELPER_HEADERS = [
    "Treffer-ID", "ENPA-Artikel-ID", "Zeitungseinheit", "Untersuchungsjahr",
    "Ereignisjahr", "Fensterart", "Hauptcode Rohzeile", "N1 Roh", "N2 Roh",
    "N3 Roh", "Relevant Roh", "M1 Roh", "M2 Roh", "S1 Roh", "UN/O1 Roh",
    "Hauptcode Original", "Einzelartikel", "Relevant bereinigt", "M1 bereinigt",
    "M2 bereinigt", "Sonstige bereinigt", "Unklar bereinigt",
    "Andere/fehlende Codes", "Suchkategorie", "Artikel je Kategorie",
    "N1 bereinigt", "N2 bereinigt", "N3 bereinigt", "Codekonflikt", "Rohzeile",
    "Ausgeschlossen",
]
DUPLICATE_HEADERS = [
    "Stabile ENPA-Artikel-ID", "Kanonische Treffer-ID", "Hauptcode des Originals",
    "Suchkategorien des Artikels", "Suchbegriffe des Artikels",
    *[f"Kategorie {category}" for category in "ABCDEFGH"],
]


def _parse_date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = clean(value)
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def _stable_article_id(url: Any, fallback: Any) -> str:
    text = clean(url)
    if text:
        value = parse_qs(urlparse(text).query).get("d", [""])[0]
        if value:
            return value
        return text
    return clean(fallback)


def _record_sort_key(record_id: Any) -> tuple[int, str]:
    text = clean(record_id)
    match = re.search(r"(\d+)", text)
    return (int(match.group(1)) if match else 10**12, text.casefold())


def _paper_label(code: Any) -> str:
    value = clean(code)
    for label, codes in PAPER_GROUPS:
        if value in codes:
            return label
    return "Nicht zugeordnet"


def _windows(config: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for query in config.get("queries", []):
        start = _parse_date(query.get("dateFrom"))
        end = _parse_date(query.get("dateTo"))
        event_start = _parse_date(query.get("eventStart"))
        if not start or not end:
            continue
        result.append({
            "start": start,
            "end": end,
            "year": start.year,
            "event": event_start.year if event_start else start.year,
            "phase": PHASE_LABELS.get(clean(query.get("windowType")), clean(query.get("windowType"))) or "nicht zugeordnet",
        })
    return result


def _sheet_reset(ws, headers: list[str]) -> None:
    same_headers = [ws.cell(1, col).value for col in range(1, len(headers) + 1)] == headers
    sample_styles = [copy(ws.cell(2, col)._style) for col in range(1, len(headers) + 1)]
    sample_height = ws.row_dimensions[2].height
    for merged in list(ws.merged_cells.ranges):
        ws.unmerge_cells(str(merged))
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)
    for row in list(ws.row_dimensions):
        if row > 1:
            del ws.row_dimensions[row]
    for column, style in enumerate(sample_styles, 1):
        ws.cell(2, column)._style = style
    ws.row_dimensions[2].height = sample_height
    for column, header in enumerate(headers, 1):
        ws.cell(1, column).value = header
    if not same_headers:
        for cell in ws[1]:
            cell.fill = PatternFill("solid", fgColor="4472C4")
            cell.font = Font(bold=True, color="FFFFFF")
            cell.alignment = Alignment(vertical="center", wrap_text=True)


def _replace_table(ws, name: str, ref: str, style: str = "TableStyleMedium2") -> None:
    old = ws.tables.get(name)
    if old is not None:
        old.ref = ref
        old.autoFilter = AutoFilter(ref=ref)
        old.sortState = None
        for column in old.tableColumns:
            column.calculatedColumnFormula = None
        ws.auto_filter.ref = None
        return
    for table_name in list(ws.tables):
        del ws.tables[table_name]
    table = Table(displayName=name, ref=ref)
    table.tableStyleInfo = TableStyleInfo(
        name=style,
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    ws.add_table(table)
    ws.auto_filter.ref = None


def set_compact_ranking_totals(ws, last_data_row: int | None = None) -> int:
    """Keep an unfiltered SUM row outside the sortable search-term records."""
    table = ws.tables.get("KompaktRankingLive")
    if table is None:
        raise ValueError("KompaktRankingLive fehlt in 09_Kompakt_Ranking.")
    if last_data_row is None:
        last_data_row = int(re.search(r"\d+$", table.ref).group())
        if table.totalsRowCount:
            last_data_row -= table.totalsRowCount
    last_data_row = max(2, last_data_row)
    total_row = last_data_row + 1
    table.ref = f"A1:G{total_row}"
    table.totalsRowCount = 1
    table.totalsRowShown = True
    table.autoFilter = AutoFilter(ref=f"A1:G{last_data_row}")
    table.sortState = None
    if len(table.tableColumns) != 7:
        table.tableColumns = [
            TableColumn(id=col, name=str(ws.cell(1, col).value))
            for col in range(1, 8)
        ]
    for column in table.tableColumns:
        column.totalsRowFunction = None
        column.totalsRowFormula = None
        column.totalsRowLabel = None
    table.tableColumns[0].totalsRowLabel = "Gesamtsumme"
    ws.cell(total_row, 1).value = "Gesamtsumme"
    ws.cell(total_row, 2).value = None
    for col in range(3, 7):
        label = str(ws.cell(1, col).value)
        formula = f"SUM(KompaktRankingLive[{label}])"
        ws.cell(total_row, col).value = "=" + formula
        table.tableColumns[col - 1].totalsRowFunction = "custom"
        table.tableColumns[col - 1].totalsRowFormula = TableFormula(attr_text=formula)
    ws.cell(total_row, 7).value = f'=IF(C{total_row}=0,"",D{total_row}/C{total_row})'
    table.tableColumns[6].totalsRowFunction = "custom"
    table.tableColumns[6].totalsRowFormula = TableFormula(
        attr_text=f'IF(C{total_row}=0,"",D{total_row}/C{total_row})'
    )
    for col in range(1, 8):
        cell = ws.cell(total_row, col)
        cell._style = copy(ws.cell(1, col)._style)
        cell.alignment = Alignment(vertical="center", horizontal="left" if col < 3 else "right")
        cell.number_format = "0.0%" if col == 7 else "#,##0" if col > 2 else "General"
    ws.row_dimensions[total_row].height = 28
    for conditional, rules in list(ws.conditional_formatting._cf_rules.items()):
        if str(conditional.sqref).startswith("G2:G") and all(rule.type == "colorScale" for rule in rules):
            del ws.conditional_formatting._cf_rules[conditional]
            for rule in rules:
                ws.conditional_formatting.add(f"G2:G{last_data_row}", rule)
    ws.auto_filter.ref = None
    return total_row


def _source(column: str, row: int) -> str:
    return f"'01_Codierung'!${column}${row}"


def _included_expression(row: int) -> str:
    status = _source("AE", row)
    return f'AND({status}<>"ausschliessen",{status}<>"auszuschliessen")'


def _first_active_formula(row: int, earlier_rows: list[int]) -> str:
    conditions = [_included_expression(row)]
    if earlier_rows:
        conditions.append(
            "NOT(OR(" + ",".join(_included_expression(earlier) for earlier in earlier_rows) + "))"
        )
    return "=IF(AND(" + ",".join(conditions) + "),1,0)"


def _canonical_code_formula(rows: list[int]) -> str:
    result = '""'
    for row in reversed(rows):
        result = f'IF({_included_expression(row)},{_source("O", row)},{result})'
    return f"={result}"


def _conditional_concat(items: list[tuple[str, str]]) -> str:
    pieces = []
    for index, (condition, value) in enumerate(items):
        previous = [prior[0] for prior in items[:index]]
        separator = f'IF(OR({",".join(previous)}),", ","")&' if previous else ""
        pieces.append(f'IF({condition},{separator}{value},"")')
    return "=" + "&".join(pieces)


def _distinct_values_formula(column: str, rows: list[int]) -> str:
    cells = [_source(column, row) for row in rows]
    items = []
    for index, cell in enumerate(cells):
        conditions = [f'{cell}<>""'] + [f"{cell}<>{prior}" for prior in cells[:index]]
        items.append((f'AND({",".join(conditions)})', cell))
    return _conditional_concat(items)


def _category_formula(rows: list[int]) -> str:
    items = []
    for category in "ABCDEFGH":
        condition = "OR(" + ",".join(f'{_source("J", row)}="{category}"' for row in rows) + ")"
        items.append((condition, f'"{category}"'))
    return _conditional_concat(items)


def _category_flag_formula(category: str, rows: list[int]) -> str:
    condition = "OR(" + ",".join(f'{_source("J", row)}="{category}"' for row in rows) + ")"
    return f"=IF({condition},1,0)"


def _collect_records(wb, config: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    ws = wb["01_Codierung"]
    headers = header_map(ws)
    cols = {header: find_col(headers, header) for header in CODING_HEADERS}
    windows = _windows(config)
    records = []
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in range(2, ws.max_row + 1):
        record_id = clean(ws.cell(row, cols["ID"]).value)
        url = clean(ws.cell(row, cols["URL e-newspaperarchives"]).value)
        if not record_id and not url:
            continue
        issue_date = _parse_date(ws.cell(row, cols["Ausgabe-Datum"]).value)
        matches = [window for window in windows if issue_date and window["start"] <= issue_date <= window["end"]]
        window = matches[0] if len(matches) == 1 else None
        article_id = _stable_article_id(url, record_id or f"Zeile-{row}")
        record = {
            "row": row,
            "id": record_id or f"Zeile-{row}",
            "article": article_id,
            "paper": _paper_label(ws.cell(row, cols["Zeitung"]).value),
            "year": str(issue_date.year) if issue_date else "Nicht zugeordnet",
            "event": str(window["event"]) if window else "Nicht zugeordnet",
            "phase": window["phase"] if window else "nicht zugeordnet",
            "category": clean(ws.cell(row, cols["Suchkategorie A-H"]).value),
            "status": clean(ws.cell(row, cols["Kontrollstatus"]).value).casefold(),
        }
        records.append(record)
        groups[article_id].append(record)
    return records, groups


def _rebuild_duplicate_helper(wb, groups: dict[str, list[dict[str, Any]]]) -> None:
    ws = wb["98_Dubletten_Hilfe"] if "98_Dubletten_Hilfe" in wb.sheetnames else wb.create_sheet("98_Dubletten_Hilfe")
    _sheet_reset(ws, DUPLICATE_HEADERS)
    ordered = sorted(groups.items(), key=lambda item: _record_sort_key(min(item[1], key=lambda r: _record_sort_key(r["id"]))["id"]))
    for out_row, (article, members) in enumerate(ordered, 2):
        canonical = min(members, key=lambda record: _record_sort_key(record["id"]))
        rows = [member["row"] for member in sorted(members, key=lambda record: record["row"])]
        ws.cell(out_row, 1).value = article
        ws.cell(out_row, 2).value = canonical["id"]
        ws.cell(out_row, 3).value = f"={_source('O', canonical['row'])}"
        ws.cell(out_row, 4).value = _category_formula(rows)
        ws.cell(out_row, 5).value = _distinct_values_formula("K", rows)
        for offset, category in enumerate("ABCDEFGH", 6):
            ws.cell(out_row, offset).value = _category_flag_formula(category, rows)
    last = max(2, len(ordered) + 1)
    ws.auto_filter.ref = f"A1:M{last}"
    ws.freeze_panes = "A2"
    ws.sheet_state = "hidden"
    widths = [30, 22, 20, 27, 44] + [12] * 8
    for index, width in enumerate(widths, 1):
        ws.column_dimensions[ws.cell(1, index).column_letter].width = width


def _rebuild_overview(wb, groups: dict[str, list[dict[str, Any]]]) -> None:
    ws = wb["07_Kurzübersicht"] if "07_Kurzübersicht" in wb.sheetnames else wb.create_sheet("07_Kurzübersicht")
    _sheet_reset(ws, SHORT_OVERVIEW_HEADERS)
    ordered = sorted(groups.items(), key=lambda item: _record_sort_key(min(item[1], key=lambda r: _record_sort_key(r["id"]))["id"]))
    for index, (_article, members) in enumerate(ordered, 2):
        canonical = min(members, key=lambda record: _record_sort_key(record["id"]))
        row = canonical["row"]
        helper_row = index
        formulas = [
            f"={_source('A', row)}", f"={_source('B', row)}", f"={_source('D', row)}",
            f"={_source('E', row)}", f"='98_Dubletten_Hilfe'!$D${helper_row}",
            f"='98_Dubletten_Hilfe'!$E${helper_row}", f"={_source('M', row)}",
            f"='98_Dubletten_Hilfe'!$C${helper_row}", f"={_source('P', row)}",
            f"={_source('Q', row)}", f"={_source('S', row)}", f"={_source('T', row)}",
            f"={_source('W', row)}", f"={_source('AB', row)}",
        ]
        for column, formula in enumerate(formulas, 1):
            ws.cell(index, column).value = formula
    last = max(2, len(ordered) + 1)
    _replace_table(ws, "KurzuebersichtDaten", f"A1:N{last}")
    ws.freeze_panes = "A2"
    widths = [18, 12, 28, 15, 20, 30, 52, 14, 14, 14, 20, 17, 25, 28]
    for index, width in enumerate(widths, 1):
        ws.column_dimensions[ws.cell(1, index).column_letter].width = width


def _rebuild_evaluation_helper(wb, records: list[dict[str, Any]], groups: dict[str, list[dict[str, Any]]]) -> int:
    ws = wb["97_Auswertung_Hilfe"] if "97_Auswertung_Hilfe" in wb.sheetnames else wb.create_sheet("97_Auswertung_Hilfe")
    _sheet_reset(ws, HELPER_HEADERS)
    ordered_groups = {
        key: sorted(members, key=lambda record: _record_sort_key(record["id"]))
        for key, members in groups.items()
    }
    for out_row, record in enumerate(records, 2):
        row = record["row"]
        members = ordered_groups[record["article"]]
        member_rows = [member["row"] for member in members]
        member_index = next(index for index, member in enumerate(members) if member["row"] == row)
        earlier_rows = member_rows[:member_index]
        earlier_category_rows = [
            member["row"]
            for member in members[:member_index]
            if member["category"] == record["category"]
        ]
        included = _included_expression(row)
        code_flag = lambda code: (
            f'=IF(AND({included},OR('
            + ",".join(f'{_source(col, row)}="{code}"' for col in "OPQ")
            + ")),1,0)"
        )
        conflicts = ",".join(
            f'AND({_included_expression(member["row"])},{_source("O", member["row"])}<>"",'
            f'{_source("O", member["row"])}<>P{out_row})'
            for member in members
        )
        values = [
            f"={_source('A', row)}", record["article"], record["paper"], record["year"],
            record["event"], record["phase"], f"={_source('O', row)}", code_flag("N1"),
            code_flag("N2"), code_flag("N3"), f"=IF(SUM(H{out_row}:J{out_row})>0,1,0)",
            f'=IF(AND({included},G{out_row}="M1"),1,0)', f'=IF(AND({included},G{out_row}="M2"),1,0)',
            f'=IF(AND({included},G{out_row}="S1"),1,0)', f'=IF(AND({included},OR(G{out_row}="UN",G{out_row}="O1")),1,0)',
            _canonical_code_formula(member_rows), _first_active_formula(row, earlier_rows),
            f'=Q{out_row}*IF(OR(P{out_row}="N1",P{out_row}="N2",P{out_row}="N3"),1,0)',
            f'=Q{out_row}*IF(P{out_row}="M1",1,0)', f'=Q{out_row}*IF(P{out_row}="M2",1,0)',
            f'=Q{out_row}*IF(OR(P{out_row}="S1",P{out_row}="W1",P{out_row}="K1",P{out_row}="U1"),1,0)',
            f'=Q{out_row}*IF(OR(P{out_row}="UN",P{out_row}="O1"),1,0)',
            f'=Q{out_row}-SUM(R{out_row}:V{out_row})', f"={_source('J', row)}",
            _first_active_formula(row, earlier_category_rows),
            f'=Q{out_row}*IF(P{out_row}="N1",1,0)', f'=Q{out_row}*IF(P{out_row}="N2",1,0)',
            f'=Q{out_row}*IF(P{out_row}="N3",1,0)', f'=Q{out_row}*IF(OR({conflicts}),1,0)',
            f'=IF({included},1,0)', f'=IF({included},0,1)',
        ]
        for column, value in enumerate(values, 1):
            ws.cell(out_row, column).value = value
    last = max(2, len(records) + 1)
    ws.auto_filter.ref = f"A1:AE{last}"
    ws.freeze_panes = "A2"
    ws.sheet_state = "hidden"
    return last


def _add_list_validation(ws, cell: str, values: list[str]) -> None:
    escaped = [value.replace('"', '""') for value in values]
    formula = '"' + ",".join(escaped) + '"'
    validation = DataValidation(type="list", formula1=formula, allow_blank=False, showDropDown=False)
    ws.add_data_validation(validation)
    validation.add(cell)


def _refresh_evaluation_template(ws, config: dict[str, Any], helper_last: int) -> bool:
    """Refresh existing formulas without discarding the reference presentation."""
    if ws["A11"].value != "Kategorie" or ws["A27"].value != "Zeitungseinheit":
        return False
    period_titles = [
        row for row in range(28, ws.max_row + 1)
        if str(ws.cell(row, 1).value or "").startswith("Auswertung nach Untersuchungszeitraum")
    ]
    if len(period_titles) != 1:
        return False
    period_title = period_titles[0]
    year_meta = {str(window["year"]): (str(window["event"]), window["phase"]) for window in _windows(config)}
    actual_year_rows = [
        tuple(str(ws.cell(row, col).value or "") for col in range(1, 5))
        for row in range(28, period_title)
        if ws.cell(row, 1).value in {label for label, _ in PAPER_GROUPS}
    ]
    expected_year_rows = [
        (paper, "Alle" if year is None else year, "Alle" if year is None else year_meta[year][0],
         "Alle" if year is None else year_meta[year][1])
        for paper, _ in PAPER_GROUPS for year in [None] + sorted(year_meta)
    ]
    if actual_year_rows != expected_year_rows:
        return False
    source_range = re.compile(r"('97_Auswertung_Hilfe'!)\$?([A-Z]+)\$?2:\$?\2\$?\d+")
    for row in ws.iter_rows():
        for cell in row:
            if cell.data_type == "f":
                cell.value = source_range.sub(
                    lambda match: f"{match.group(1)}${match.group(2)}$2:${match.group(2)}${helper_last}",
                    cell.value,
                )
    ws["A10"] = "Ausgeschlossene Beiträge ohne Einfluss auf die Auswertung"
    ws["B10"] = ws["B3"].value.replace("$AD$", "$AE$")
    if not ws["A10"].has_style:
        ws["A10"]._style = copy(ws["A9"]._style)
        ws["B10"]._style = copy(ws["B9"]._style)
    ws.row_dimensions[10].height = max(ws.row_dimensions[10].height or 0, 38)
    ws.data_validations.dataValidation = []
    years = sorted(year_meta)
    events = sorted({event for event, _ in year_meta.values()})
    phases = [phase for phase in PHASE_LABELS.values() if phase in {phase for _, phase in year_meta.values()}]
    for cell, values in (
        ("E3", ["Alle"] + [label for label, _ in PAPER_GROUPS] + ["Nicht zugeordnet"]),
        ("E4", ["Alle"] + years + ["Nicht zugeordnet"]),
        ("E5", ["Alle"] + events + ["Nicht zugeordnet"]),
        ("E6", ["Alle"] + phases + ["nicht zugeordnet"]),
    ):
        _add_list_validation(ws, cell, values)
        if str(ws[cell].value) not in values:
            ws[cell].value = "Alle"
    ws.freeze_panes = None
    return True


def _rebuild_evaluation(wb, config: dict[str, Any], helper_last: int) -> None:
    ws = wb["05_Auswertung"] if "05_Auswertung" in wb.sheetnames else wb.create_sheet("05_Auswertung")
    if _refresh_evaluation_template(ws, config, helper_last):
        return
    for merged in list(ws.merged_cells.ranges):
        ws.unmerge_cells(str(merged))
    if ws.max_row:
        ws.delete_rows(1, ws.max_row)
    ws.data_validations.dataValidation = []
    ws.sheet_view.showGridLines = False
    rng = lambda column: f"'97_Auswertung_Hilfe'!${column}$2:${column}${helper_last}"
    filters = []
    for column, cell in (("C", "$E$3"), ("D", "$E$4"), ("E", "$E$5"), ("F", "$E$6")):
        default = "*" if column in {"C", "F"} else "<>"
        filters.extend([rng(column), f'IF({cell}="Alle","{default}",{cell})'])
    summ = lambda column, extra=None, custom=None: "=SUMIFS(" + ",".join([rng(column)] + (filters if custom is None else custom) + (extra or [])) + ")"
    ws.merge_cells("A1:R1")
    ws["A1"] = "Auswertung nach Zeitung, Untersuchungsjahr und Untersuchungszeitraum"
    ws["A1"].font = Font(bold=True, size=15, color="FFFFFF")
    ws["A1"].fill = PatternFill("solid", fgColor="1F4E78")
    ws["A1"].alignment = Alignment(vertical="center")
    labels = [
        "Rohzeilen", "Bereinigte Treffer ohne Dubletten", "Relevante Treffer N1–N3 ohne Dubletten",
        "Menschengemachte Gefahren M1/M2 ohne Dubletten", "Sonstige Codes S1/W1/K1/U1 ohne Dubletten",
        "Unklar UN/O1 ohne Dubletten", "Andere/fehlende Codes ohne Dubletten",
    ]
    for row, label in enumerate(labels, 3):
        ws.cell(row, 1).value = label
    for row, column in ((3, "AD"), (4, "Q"), (5, "R"), (7, "U"), (8, "V"), (9, "W")):
        ws.cell(row, 2).value = summ(column)
    ws["B6"] = summ("S") + "+" + summ("T")[1:]
    ws["A10"] = "Ausgeschlossene Beiträge ohne Einfluss auf die Auswertung"
    ws["B10"] = summ("AE")
    for row, label in ((3, "Zeitungseinheit"), (4, "Untersuchungsjahr"), (5, "Ereignisjahr"), (6, "Fensterart")):
        ws.cell(row, 4).value = label
        ws.cell(row, 5).value = "Alle"
    ws["D8"] = "Relevanzquote bereinigt"
    ws["E8"] = '=IF(B4=0,"",B5/B4)'
    ws["E8"].number_format = "0.0%"
    ws["D9"] = "Artikel mit Codekonflikten"
    ws["E9"] = summ("AC")
    years = sorted({str(window["year"]) for window in _windows(config)})
    events = sorted({str(window["event"]) for window in _windows(config)})
    phases = [phase for phase in PHASE_LABELS.values() if phase in {window["phase"] for window in _windows(config)}]
    _add_list_validation(ws, "E3", ["Alle"] + [label for label, _codes in PAPER_GROUPS] + ["Nicht zugeordnet"])
    _add_list_validation(ws, "E4", ["Alle"] + years + ["Nicht zugeordnet"])
    _add_list_validation(ws, "E5", ["Alle"] + events + ["Nicht zugeordnet"])
    _add_list_validation(ws, "E6", ["Alle"] + phases + ["nicht zugeordnet"])
    headers = [
        "Kategorie", "Rohzeilen", "N1 roh", "N2 roh", "N3 roh", "M1 roh", "M2 roh", "S1 roh",
        "UN/O1 roh", "Relevanzquote roh", "Artikel ohne Dubletten", "N1 bereinigt", "N2 bereinigt",
        "N3 bereinigt", "Quote N1 bereinigt", "Quote N2 bereinigt", "Quote N3 bereinigt",
        "Quote N1–N3 bereinigt",
    ]
    for column, header in enumerate(headers, 1):
        ws.cell(11, column).value = header
    for row, category in enumerate("ABCDEFGH", 12):
        ws.cell(row, 1).value = category
        extra = [rng("X"), f"$A{row}"]
        for column, helper_column in ((2, "AD"), (3, "H"), (4, "I"), (5, "J"), (6, "L"), (7, "M"), (8, "N"), (9, "O"), (11, "Y")):
            ws.cell(row, column).value = summ(helper_column, extra)
        ws.cell(row, 10).value = f'=IF(B{row}=0,"",{summ("K", extra)[1:]}/B{row})'
        for column, code in ((12, "N1"), (13, "N2"), (14, "N3")):
            ws.cell(row, column).value = summ("Y", extra + [rng("P"), f'"{code}"'])
        for column, numerator in ((15, "L"), (16, "M"), (17, "N")):
            ws.cell(row, column).value = f'=IF(K{row}=0,"",{numerator}{row}/K{row})'
        ws.cell(row, 18).value = f'=IF(K{row}=0,"",SUM(L{row}:N{row})/K{row})'
        for column in (10, 15, 16, 17, 18):
            ws.cell(row, column).number_format = "0.0%"
        for column in (11, 12, 13, 14):
            ws.cell(row, column).number_format = "#,##0"
    notes = [
        "Bereinigt: jede nicht ausgeschlossene stabile ENPA-Artikel-ID einmal; massgeblich ist der Hauptcode des nicht ausgeschlossenen Eintrags mit der kleinsten Treffer-ID. Nebencodes zählen nur in den Rohkennzahlen.",
        "Suchkategorien können denselben Artikel enthalten. Bereinigte Kategorien dürfen nicht zur Gesamtartikelzahl addiert werden.",
        "Jahr aus Ausgabe-Datum; Ereignisjahr und Fensterart aus 04_Falljahre_Korpus. Null bedeutet keine Treffer im Bestand, nicht vollständige Archivabdeckung.",
        "Kontrollstatus ausschliessen und der historische Altwert auszuschliessen bleiben ohne Einfluss auf sämtliche Kennzahlen. Nach Importen baut das Importskript diese Auswertung neu auf.",
    ]
    for row, note in enumerate(notes, 21):
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=18)
        ws.cell(row, 1).value = note
        ws.cell(row, 1).alignment = Alignment(wrap_text=True, vertical="center")
    ws.merge_cells("A26:R26")
    ws["A26"] = "Gesamtbestand nach Zeitung und Untersuchungsjahr (unabhängig von den Filtern oben)"
    group_headers = ["Zeitungseinheit", "Untersuchungsjahr", "Ereignisjahr", "Fensterart", "Rohzeilen", "Einzelartikel", "Relevant N1–N3", "Relevanzquote", "N1", "N2", "N3", "M1", "M2", "S1/W1/K1/U1", "UN/O1", "Andere/fehlend", "Codekonflikte"]
    for column, header in enumerate(group_headers, 1):
        ws.cell(27, column).value = header
    year_meta = {str(window["year"]): (str(window["event"]), window["phase"]) for window in _windows(config)}
    row = 28
    for paper, _codes in PAPER_GROUPS:
        for year in [None] + sorted(year_meta):
            ws.cell(row, 1).value = paper
            ws.cell(row, 2).value = "Alle" if year is None else year
            ws.cell(row, 3).value = "Alle" if year is None else year_meta[year][0]
            ws.cell(row, 4).value = "Alle" if year is None else year_meta[year][1]
            criteria = [rng("C"), f"$A{row}"]
            if year is not None:
                criteria += [rng("D"), f'$B{row}&""']
            for column, helper_column in ((5, "AD"), (6, "Q"), (7, "R"), (9, "Z"), (10, "AA"), (11, "AB"), (12, "S"), (13, "T"), (14, "U"), (15, "V"), (16, "W"), (17, "AC")):
                ws.cell(row, column).value = summ(helper_column, custom=criteria)
            ws.cell(row, 8).value = f'=IF(F{row}=0,"",G{row}/F{row})'
            ws.cell(row, 8).number_format = "0.0%"
            row += 1
    period_title_row = row + 2
    ws.merge_cells(start_row=period_title_row, start_column=1, end_row=period_title_row, end_column=18)
    ws.cell(period_title_row, 1).value = "Auswertung nach Untersuchungszeitraum (alle Ereignisjahre)"
    period_header_row = period_title_row + 1
    period_headers = list(group_headers)
    period_headers[1] = "Untersuchungszeitraum"
    for column, header in enumerate(period_headers, 1):
        ws.cell(period_header_row, column).value = header
    row = period_header_row + 1
    for paper in ["Alle Zeitungen"] + [label for label, _codes in PAPER_GROUPS]:
        for phase in phases:
            ws.cell(row, 1).value = paper
            ws.cell(row, 2).value = PHASE_LABELS.get(phase, phase)
            ws.cell(row, 3).value = "Alle"
            ws.cell(row, 4).value = phase
            criteria = [rng("F"), f"$D{row}"]
            if paper != "Alle Zeitungen":
                criteria += [rng("C"), f"$A{row}"]
            for column, helper_column in ((5, "AD"), (6, "Q"), (7, "R"), (9, "Z"), (10, "AA"), (11, "AB"), (12, "S"), (13, "T"), (14, "U"), (15, "V"), (16, "W"), (17, "AC")):
                ws.cell(row, column).value = summ(helper_column, custom=criteria)
            ws.cell(row, 8).value = f'=IF(F{row}=0,"",G{row}/F{row})'
            ws.cell(row, 8).number_format = "0.0%"
            row += 1
    for header_row in (11, 27, period_header_row):
        for cell in ws[header_row][:18]:
            cell.fill = PatternFill("solid", fgColor="4472C4")
            cell.font = Font(bold=True, color="FFFFFF")
            cell.alignment = Alignment(wrap_text=True, vertical="center")
    for title_row in (26, period_title_row):
        ws.cell(title_row, 1).fill = PatternFill("solid", fgColor="D9EAF7")
        ws.cell(title_row, 1).font = Font(bold=True, color="1F2933")
    ws.freeze_panes = None
    widths = [38, 26, 17, 20, 17, 17, 17, 17, 17, 19, 22, 18, 18, 18, 20, 20, 20, 23]
    for index, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(index)].width = width


def refresh_analysis_views(wb, config: dict[str, Any]) -> dict[str, int]:
    records, groups = _collect_records(wb, config)
    active_groups = {
        key: [record for record in members if record["status"] not in EXCLUDED_STATUSES]
        for key, members in groups.items()
    }
    active_groups = {key: members for key, members in active_groups.items() if members}
    _rebuild_duplicate_helper(wb, active_groups)
    _rebuild_overview(wb, active_groups)
    helper_last = _rebuild_evaluation_helper(wb, records, groups)
    _rebuild_evaluation(wb, config, helper_last)
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    return {
        "raw_rows": sum(record["status"] not in EXCLUDED_STATUSES for record in records),
        "excluded_rows": sum(record["status"] in EXCLUDED_STATUSES for record in records),
        "unique_articles": len(active_groups),
        "helper_last_row": helper_last,
    }

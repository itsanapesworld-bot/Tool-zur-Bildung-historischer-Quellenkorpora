from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo

from enpa_common import DEFAULT_CONFIG, load_config, resolve_project_path


CODE_COLUMNS = [
    "N1",
    "N2",
    "N3",
    "M1",
    "M2",
    "K1",
    "U1",
    "W1",
    "S1",
    "O1",
    "D1_Hauptcode",
    "UN",
]


def recommendation(row: dict[str, object]) -> str:
    hits = int(row.get("Treffer") or 0)
    relevance = float(row.get("Relevanzquote") or 0)
    unclear = float(row.get("Pruefquote_UN_O1_D1") or 0)
    if hits >= 50 and relevance < 0.10:
        return "starker Ausschlusskandidat"
    if hits >= 20 and relevance < 0.20:
        return "Ausschluss prüfen"
    if hits >= 20 and unclear >= 0.50:
        return "manuell prüfen: viele unklare/Dubletten"
    if relevance >= 0.50:
        return "tendenziell behalten"
    return "prüfen"


def with_recommendation(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for source in rows:
        row = dict(source)
        row["Empfehlung"] = (
            "Datenqualität prüfen"
            if row.get("Suchkategorie A-H") == "(leer)"
            else recommendation(row)
        )
        result.append(row)
    return result


def interference_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return sorted(
        (row for row in with_recommendation(rows) if int(row.get("Treffer") or 0) > 0),
        key=lambda row: (
            -int(row.get("Treffer") or 0)
            * (1 - float(row.get("Relevanzquote") or 0)),
            -int(row.get("Treffer") or 0),
            str(row.get("Suchbegriff") or "").casefold(),
        ),
    )


def compact_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for row in rows:
        relevant = sum(int(row.get(code) or 0) for code in ("N1", "N2", "N3"))
        human_made = sum(int(row.get(code) or 0) for code in ("M1", "M2"))
        hits = int(row.get("Treffer") or 0)
        result.append(
            {
                "Kategorie": row.get("Suchkategorie A-H") or "",
                "Begriff": row.get("Suchbegriff") or "",
                "Treffergesamtanzahl": hits,
                "Treffer gesamt N1-N3": relevant,
                "Treffer gesamt M1+M2": human_made,
                "Sonstige Treffer": hits - relevant - human_made,
                "Relevanzquote": float(row.get("Relevanzquote") or 0),
            }
        )
    return sorted(
        result,
        key=lambda row: (
            -int(row["Treffergesamtanzahl"]),
            str(row["Kategorie"]).casefold(),
            str(row["Begriff"]).casefold(),
        ),
    )


def set_widths(ws, headers: list[str]) -> None:
    for index, header in enumerate(headers, start=1):
        width = 13
        if header in {"Suchbegriff", "Begriff"}:
            width = 28
        elif header == "Empfehlung":
            width = 38
        elif len(header) > 24:
            width = 22
        ws.column_dimensions[ws.cell(1, index).column_letter].width = width


def add_data_sheet(
    workbook: Workbook,
    name: str,
    headers: list[str],
    rows: list[dict[str, object]],
    table_name: str,
) -> None:
    ws = workbook.create_sheet(name)
    ws.append(headers)
    for row in rows:
        ws.append([row.get(header, "") for header in headers])

    header_fill = PatternFill("solid", fgColor="1F4E78")
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="center")

    ws.freeze_panes = "A2"
    ws.sheet_view.showGridLines = False
    ws.row_dimensions[1].height = 36
    set_widths(ws, headers)

    percent_columns = {
        index
        for index, header in enumerate(headers, start=1)
        if "quote" in header.casefold()
    }
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top")
            if cell.column in percent_columns:
                cell.number_format = "0.0%"

    if ws.max_row >= 2:
        reference = f"A1:{ws.cell(ws.max_row, ws.max_column).coordinate}"
        table = Table(displayName=table_name, ref=reference)
        table.tableStyleInfo = TableStyleInfo(
            name="TableStyleMedium2",
            showFirstColumn=False,
            showLastColumn=False,
            showRowStripes=True,
            showColumnStripes=False,
        )
        ws.add_table(table)

    for column in percent_columns:
        letter = ws.cell(1, column).column_letter
        ws.conditional_formatting.add(
            f"{letter}2:{letter}{max(ws.max_row, 2)}",
            ColorScaleRule(
                start_type="num",
                start_value=0,
                start_color="F8696B",
                mid_type="num",
                mid_value=0.5,
                mid_color="FFEB84",
                end_type="num",
                end_value=1,
                end_color="63BE7B",
            ),
        )


def add_readme(workbook: Workbook, data: dict[str, object]) -> None:
    ws = workbook.active
    ws.title = "00_Readme"
    rows = [
        ["Auswertung Suchbegriffe_Relevanz"],
        [],
        ["Zweck", "Treffer- und Relevanzanalyse nach Suchkategorie und Suchbegriff."],
        ["Datenbasis", str(data.get("source_workbook") or "")],
        ["Erstellt", str(data.get("created_at") or datetime.now().isoformat())],
        ["Ausgewertete Zeilen", int(data.get("rows_seen") or 0)],
        [],
        [
            "Relevanzquote",
            "Anteil der Artikel mit N1, N2 oder N3 in Hauptcode, Nebencode 1 oder Nebencode 2; jeder Artikel zählt höchstens einmal.",
        ],
        [
            "Prüfquote",
            "Anteil der Treffer mit UN, O1 oder D1-Markierung; diese benötigen "
            "gegebenenfalls eine manuelle Prüfung.",
        ],
        [
            "03_Stoerpotenzial",
            "Sortiert Begriffe nach der absoluten Zahl nicht relevanter Treffer.",
        ],
        [
            "04_Kompakt_Ranking",
            "Kompakte Sortierung nach absoluter Treffergesamtanzahl.",
        ],
        [],
        [
            "Hinweis",
            "Empfehlungen sind heuristische Hinweise und ersetzen keine "
            "inhaltliche Entscheidung.",
        ],
    ]
    for row in rows:
        ws.append(row)
    ws["A1"].font = Font(size=18, bold=True, color="1F4E78")
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 105
    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A3"


def build(input_path: Path, output_path: Path) -> None:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    categories = with_recommendation(list(data.get("category_rows") or []))
    terms = with_recommendation(list(data.get("term_rows") or []))

    category_headers = [
        "Suchkategorie A-H",
        "Treffer",
        *CODE_COLUMNS,
        "D1_Markierung",
        "Relevant_N1_N3",
        "Nicht_relevant_M1_M2_K1_U1_W1_S1",
        "Unklar_UN_O1",
        "Relevanzquote",
        "Pruefquote_UN_O1_D1",
        "Empfehlung",
    ]
    term_headers = [
        "Suchkategorie A-H",
        "Suchbegriff",
        "Treffer",
        *CODE_COLUMNS,
        "D1_Markierung",
        "Relevant_N1_N3",
        "Nicht_relevant_M1_M2_K1_U1_W1_S1",
        "Unklar_UN_O1",
        "Relevanzquote",
        "Pruefquote_UN_O1_D1",
        "Empfehlung",
    ]
    compact_headers = [
        "Kategorie",
        "Begriff",
        "Treffergesamtanzahl",
        "Treffer gesamt N1-N3",
        "Treffer gesamt M1+M2",
        "Sonstige Treffer",
        "Relevanzquote",
    ]

    workbook = Workbook()
    add_readme(workbook, data)
    add_data_sheet(
        workbook,
        "01_Kategorien_A-H",
        category_headers,
        categories,
        "KategorieSummary",
    )
    add_data_sheet(
        workbook,
        "02_Suchbegriffe_Detail",
        term_headers,
        terms,
        "SuchbegriffeDetail",
    )
    add_data_sheet(
        workbook,
        "03_Stoerpotenzial",
        term_headers,
        interference_rows(list(data.get("term_rows") or [])),
        "Stoerpotenzial",
    )
    add_data_sheet(
        workbook,
        "04_Kompakt_Ranking",
        compact_headers,
        compact_rows(list(data.get("term_rows") or [])),
        "KompaktRanking",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(f".{output_path.stem}.tmp.xlsx")
    workbook.save(temporary)
    temporary.replace(output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument(
        "--input",
        default="outputs/enpa_v2/auswertung_suchbegriffe_relevanz_data.json",
    )
    parser.add_argument(
        "--output",
        default="Arbeitsmappen/Auswertung Suchbegriffe_Relevanz.xlsx",
    )
    args = parser.parse_args()

    config = load_config(Path(args.config).resolve())
    input_path = resolve_project_path(config, args.input)
    output_path = resolve_project_path(config, args.output)
    build(input_path, output_path)
    print(f"OUTPUT={output_path}")


if __name__ == "__main__":
    main()

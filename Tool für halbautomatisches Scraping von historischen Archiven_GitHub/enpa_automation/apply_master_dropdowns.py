from __future__ import annotations

import argparse
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.filters import AutoFilter

from build_master import add_validation, list_formula
from enpa_common import (
    CODING_HEADERS,
    DEFAULT_CONFIG,
    LISTS,
    load_config,
    risk_phase_values,
)


VALIDATION_MAP = {
    "Falltyp": "Falltyp",
    "Zeitung": "Zeitung",
    "Suchkategorie A-H": "Suchkategorie",
    "Vollartikel geprüft?": "Vollartikel geprüft",
    "Hauptcode": "Code",
    "Nebencode 1": "Code",
    "Nebencode 2": "Code",
    "Ereignisbezug": "Ereignisbezug",
    "Raumbezug": "Raumbezug",
    "Relevanzgrad 0-5": "Relevanz",
    "OCR-Qualität 1-5": "OCR",
    "Segmentierungsproblem": "Segmentierungsproblem",
    "Nachrichtenwert Nähe 0-5": "Nachrichtenwert Nähe",
    "Nachrichtenwert Schaden 0-5": "Nachrichtenwert Schaden",
    "Nachrichtenwert Konflikt 0-5": "Nachrichtenwert Konflikt",
    "Nachrichtenwert Aktualität 0-5": "Nachrichtenwert Aktualität",
    "Risikokommunikation / Phase": "Risikophase",
    "Deutungsmuster": "Deutungsmuster",
    "Kontrollstatus": "Kontrollstatus",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stellt die Dropdownlisten der ENPA-V2-Masterdatei wieder her.")
    parser.add_argument("workbook", type=Path)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    return parser.parse_args()


def update_lists_sheet(
    wb,
    config: dict | None = None,
) -> dict[str, tuple[int, int]]:
    ws = wb["99_Listen"]
    header_style = copy(ws["A1"]._style)
    mapping: dict[str, tuple[int, int]] = {}
    configured_lists = dict(LISTS)
    configured_lists["Risikophase"] = risk_phase_values(config)
    for col, (name, values) in enumerate(configured_lists.items(), start=1):
        for row in range(1, max(ws.max_row, len(values) + 1) + 1):
            ws.cell(row, col).value = None
        header = ws.cell(1, col)
        header.value = name
        header._style = copy(header_style)
        for row, value in enumerate(values, start=2):
            ws.cell(row, col).value = value
        ws.column_dimensions[get_column_letter(col)].width = max(14, min(35, len(name) + 4))
        mapping[name] = (col, len(values))
    ws.freeze_panes = "A2"
    return mapping


def current_list_map(wb) -> dict[str, tuple[int, int]]:
    """Read the current 99_Listen content without overwriting user additions."""
    ws = wb["99_Listen"]
    mapping: dict[str, tuple[int, int]] = {}
    for cell in ws[1]:
        name = str(cell.value).strip() if cell.value is not None else ""
        if not name:
            continue
        length = 0
        for row in range(2, ws.max_row + 1):
            if ws.cell(row, cell.column).value in (None, ""):
                break
            length += 1
        mapping[name] = (cell.column, length)
    return mapping


def remove_list_value(wb, list_name: str, value: str) -> bool:
    """Remove one obsolete option while preserving all other user-maintained values."""
    ws = wb["99_Listen"]
    target_col = None
    for cell in ws[1]:
        if str(cell.value or "").strip() == list_name:
            target_col = cell.column
            break
    if target_col is None:
        return False
    values: list[object] = []
    row = 2
    while row <= ws.max_row and ws.cell(row, target_col).value not in (None, ""):
        values.append(ws.cell(row, target_col).value)
        row += 1
    filtered = [item for item in values if str(item).strip() != value]
    if len(filtered) == len(values):
        return False
    for current_row in range(2, row):
        ws.cell(current_row, target_col).value = None
    for current_row, item in enumerate(filtered, start=2):
        ws.cell(current_row, target_col).value = item
    return True


def update_coding_validations(wb, list_map: dict[str, tuple[int, int]]) -> None:
    ws = wb["01_Codierung"]
    headers = {cell.value: cell.column for cell in ws[1] if cell.value}
    missing = [header for header in CODING_HEADERS if header not in headers]
    if missing:
        raise KeyError(f"Fehlende Spalten in 01_Codierung: {', '.join(missing)}")
    ws.data_validations.dataValidation.clear()
    for header, list_name in VALIDATION_MAP.items():
        list_col, length = list_map[list_name]
        add_validation(ws, headers[header], list_formula(list_col, length))
    last_data_row = ws.max_row
    while last_data_row > 1 and not any(
        ws.cell(last_data_row, col).value not in (None, "") for col in range(2, 14)
    ):
        last_data_row -= 1
    last_header_col = max(
        (cell.column for cell in ws[1] if cell.value not in (None, "")),
        default=len(CODING_HEADERS),
    )
    filter_ref = f"A1:{get_column_letter(last_header_col)}{max(2, last_data_row)}"
    if "CodierungDaten" in ws.tables:
        # A worksheet AutoFilter may not overlap an Excel table AutoFilter.
        # Keeping both caused Excel to remove table1.xml during recovery.
        ws.auto_filter.ref = None
        table = ws.tables["CodierungDaten"]
        table.ref = filter_ref
        if table.autoFilter is None:
            table.autoFilter = AutoFilter(ref=filter_ref)
        else:
            table.autoFilter.ref = filter_ref
    else:
        ws.auto_filter.ref = filter_ref


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    workbook_path = args.workbook.resolve()
    if not workbook_path.exists():
        raise FileNotFoundError(workbook_path)
    wb = openpyxl.load_workbook(workbook_path)
    list_map = update_lists_sheet(wb, config)
    update_coding_validations(wb, list_map)
    wb.save(workbook_path)
    wb.close()
    print(workbook_path)
    print(f"Listen: {len(list_map)}")
    print(f"Dropdown-Spalten: {len(VALIDATION_MAP)}")


if __name__ == "__main__":
    main()

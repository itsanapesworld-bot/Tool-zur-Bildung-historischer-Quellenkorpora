from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import openpyxl

from enpa_common import (
    CODEBOOK_ROWS,
    DEFAULT_CONFIG,
    clean,
    load_config,
    portable_project_path,
    resolve_config_path,
    resolve_workbook_profile,
)


OUTPUT_JSON = Path("../outputs/enpa_v2/auswertung_suchbegriffe_relevanz_data.json")
EXCLUDED_CONTROL_STATUSES = {"ausschliessen", "auszuschliessen"}


def value(row: tuple[Any, ...], columns: dict[str, int], header: str) -> str:
    return clean(row[columns[header] - 1])


def pct(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def sort_category_key(category: str) -> tuple[int, str]:
    order = {letter: index for index, letter in enumerate("ABCDEFGH", start=1)}
    return order.get(category, 99), category


def row_has_d1(main: str, secondary1: str, secondary2: str, duplicate_id: str) -> bool:
    return "D1" in {main, secondary1, secondary2} or bool(clean(duplicate_id))


def make_empty_code_counter() -> Counter[str]:
    return Counter({code: 0 for code, _, _ in CODEBOOK_ROWS})


def record_metrics(
    counter: Counter[str],
    total: int,
    duplicate_marks: int,
    relevant_rows: int,
) -> dict[str, Any]:
    relevant = relevant_rows
    not_related = counter["S1"] + counter["W1"] + counter["K1"] + counter["U1"] + counter["M1"] + counter["M2"]
    unclear = counter["UN"] + counter["O1"]
    return {
        "Treffer": total,
        "N1": counter["N1"],
        "N2": counter["N2"],
        "N3": counter["N3"],
        "M1": counter["M1"],
        "M2": counter["M2"],
        "K1": counter["K1"],
        "U1": counter["U1"],
        "W1": counter["W1"],
        "S1": counter["S1"],
        "O1": counter["O1"],
        "D1_Hauptcode": counter["D1"],
        "UN": counter["UN"],
        "D1_Markierung": duplicate_marks,
        "Relevant_N1_N3": relevant,
        "Nicht_relevant_M1_M2_K1_U1_W1_S1": not_related,
        "Unklar_UN_O1": unclear,
        "Relevanzquote": pct(relevant, total),
        "Pruefquote_UN_O1_D1": pct(unclear + duplicate_marks, total),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Exportiert die Suchwortauswertung des aktiven Profils.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--workbook-profile", default="")
    args = parser.parse_args()
    config = load_config(args.config)
    _profile, workbook_path, _spec = resolve_workbook_profile(config, args.workbook_profile)
    output_dir = resolve_config_path(config, config.get("outputDir"))
    assert output_dir is not None
    output_path = output_dir / "auswertung_suchbegriffe_relevanz_data.json"
    assert workbook_path is not None
    if not workbook_path.exists():
        raise FileNotFoundError(workbook_path)

    wb = openpyxl.load_workbook(workbook_path, read_only=True, data_only=True)
    ws = wb["01_Codierung"]
    header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=True))
    columns = {clean(header): index for index, header in enumerate(header_row, start=1) if clean(header)}

    category_counters: dict[str, Counter[str]] = defaultdict(make_empty_code_counter)
    category_totals: Counter[str] = Counter()
    category_duplicate_marks: Counter[str] = Counter()
    category_relevant_rows: Counter[str] = Counter()
    term_counters: dict[tuple[str, str], Counter[str]] = defaultdict(make_empty_code_counter)
    term_totals: Counter[tuple[str, str]] = Counter()
    term_duplicate_marks: Counter[tuple[str, str]] = Counter()
    term_relevant_rows: Counter[tuple[str, str]] = Counter()

    rows_seen = 0
    rows_excluded = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        category = value(row, columns, "Suchkategorie A-H").upper()
        term = value(row, columns, "Suchbegriff")
        main = value(row, columns, "Hauptcode").upper()
        if not category and not term and not main:
            continue
        status = value(row, columns, "Kontrollstatus").casefold()
        if status in EXCLUDED_CONTROL_STATUSES:
            rows_excluded += 1
            continue
        if not category:
            category = "(leer)"
        if not term:
            term = "(kein Suchbegriff erkannt)"
        if not main:
            main = "(leer)"
        secondary1 = value(row, columns, "Nebencode 1").upper()
        secondary2 = value(row, columns, "Nebencode 2").upper()
        duplicate_id = value(row, columns, "Dublette zu ID")

        rows_seen += 1
        category_totals[category] += 1
        category_counters[category][main] += 1
        term_key = (category, term)
        term_totals[term_key] += 1
        term_counters[term_key][main] += 1
        if {"N1", "N2", "N3"} & {main, secondary1, secondary2}:
            category_relevant_rows[category] += 1
            term_relevant_rows[term_key] += 1
        if row_has_d1(main, secondary1, secondary2, duplicate_id):
            category_duplicate_marks[category] += 1
            term_duplicate_marks[term_key] += 1

    wb.close()

    category_rows = []
    for category in sorted(category_totals, key=sort_category_key):
        metrics = record_metrics(
            category_counters[category],
            category_totals[category],
            category_duplicate_marks[category],
            category_relevant_rows[category],
        )
        category_rows.append({"Suchkategorie A-H": category, **metrics})

    term_rows = []
    for category, term in sorted(term_totals, key=lambda item: (sort_category_key(item[0]), -term_totals[item], item[1].casefold())):
        metrics = record_metrics(
            term_counters[(category, term)],
            term_totals[(category, term)],
            term_duplicate_marks[(category, term)],
            term_relevant_rows[(category, term)],
        )
        term_rows.append({"Suchkategorie A-H": category, "Suchbegriff": term, **metrics})

    data = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_workbook": portable_project_path(config, workbook_path),
        "rows_seen": rows_seen,
        "rows_excluded_without_influence": rows_excluded,
        "code_order": [code for code, _, _ in CODEBOOK_ROWS],
        "category_rows": category_rows,
        "term_rows": term_rows,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output_path)
    print(f"rows_seen={rows_seen}")
    print(f"rows_excluded_without_influence={rows_excluded}")
    print(f"categories={len(category_rows)}")
    print(f"terms={len(term_rows)}")


if __name__ == "__main__":
    main()

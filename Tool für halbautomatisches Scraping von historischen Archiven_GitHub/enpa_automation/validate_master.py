from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

import openpyxl

from enpa_common import (
    DEFAULT_CONFIG,
    ENV_TERMS,
    HAZARD_TERMS,
    FOREIGN_TERMS,
    PREVENTION_TERMS,
    clean,
    contains_any,
    find_col,
    has_human_made_hazard,
    header_map,
    load_config,
    resolve_config_path,
    resolve_workbook_profile,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validiert die ENPA-V2-Masterdatei.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--workbook-profile", default="")
    return parser.parse_args()


def has_anchor(text: str) -> bool:
    return contains_any(text, HAZARD_TERMS + PREVENTION_TERMS + ENV_TERMS)


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    profile, workbook, _profile_spec = resolve_workbook_profile(
        config,
        args.workbook_profile,
    )
    output_dir = resolve_config_path(config, config.get("outputDir"))
    assert workbook and output_dir
    if not workbook.exists():
        raise FileNotFoundError(workbook)
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = output_dir / f"validation_summary_{stamp}.csv"
    flags_path = output_dir / f"validation_flags_{stamp}.csv"
    wb = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    ws = wb["01_Codierung"]
    header_row = next(ws.iter_rows(min_row=1, max_row=1, values_only=False))
    headers = {clean(cell.value).lower(): idx for idx, cell in enumerate(header_row, start=1) if cell.value}
    cols = {
        "id": find_col(headers, "ID"),
        "category": find_col(headers, "Suchkategorie A-H"),
        "term": find_col(headers, "Suchbegriff"),
        "segment": find_col(headers, "Artikel-/Segment-ID"),
        "snippet": find_col(headers, "OCR-Ausschnitt / Textstelle"),
        "main": find_col(headers, "Hauptcode"),
        "status": find_col(headers, "Kontrollstatus"),
    }
    summary = Counter()
    by_term = Counter()
    flags: list[dict[str, str]] = []
    for row_no, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        category = clean(row[cols["category"] - 1])
        main = clean(row[cols["main"] - 1])
        term = clean(row[cols["term"] - 1])
        if not category and not main and not term:
            continue
        status = clean(row[cols["status"] - 1]).casefold()
        if status in {"ausschliessen", "auszuschliessen"}:
            summary[("Kontrollstatus", "ausgeschlossen")] += 1
            continue
        summary[(category, main)] += 1
        by_term[(category, term, main)] += 1
        text = " ".join(clean(row[cols[name] - 1]) for name in ("term", "segment", "snippet"))
        rid = clean(row[cols["id"] - 1]) or f"T{row_no - 1:04d}"
        if category == "G" and main in {"N1", "N2", "N3"} and not has_anchor(text):
            flags.append({
                "id": rid,
                "row": str(row_no),
                "problem": "Kategorie G als relevant ohne Naturgefahrenanker",
                "category": category,
                "term": term,
                "main": main,
                "segment": clean(row[cols["segment"] - 1]),
                "snippet": clean(row[cols["snippet"] - 1])[:400],
            })
        if main == "N3" and not has_anchor(text):
            flags.append({
                "id": rid,
                "row": str(row_no),
                "problem": "N3 ohne Naturgefahren-/Praeventions-/Umweltanker",
                "category": category,
                "term": term,
                "main": main,
                "segment": clean(row[cols["segment"] - 1]),
                "snippet": clean(row[cols["snippet"] - 1])[:400],
            })
        if main in {"M1", "M2"} and not has_human_made_hazard(text):
            flags.append({
                "id": rid,
                "row": str(row_no),
                "problem": "M1/M2 ohne erkennbaren Anker fuer menschengemachte Gefahr",
                "category": category,
                "term": term,
                "main": main,
                "segment": clean(row[cols["segment"] - 1]),
                "snippet": clean(row[cols["snippet"] - 1])[:400],
            })
        if main == "M1" and contains_any(text, FOREIGN_TERMS):
            flags.append({
                "id": rid,
                "row": str(row_no),
                "problem": "M1 mit internationalem Bezug; M2 pruefen",
                "category": category,
                "term": term,
                "main": main,
                "segment": clean(row[cols["segment"] - 1]),
                "snippet": clean(row[cols["snippet"] - 1])[:400],
            })
        if main == "M2" and not contains_any(text, FOREIGN_TERMS):
            flags.append({
                "id": rid,
                "row": str(row_no),
                "problem": "M2 ohne erkennbaren internationalen Bezug; M1 pruefen",
                "category": category,
                "term": term,
                "main": main,
                "segment": clean(row[cols["segment"] - 1]),
                "snippet": clean(row[cols["snippet"] - 1])[:400],
            })
    with summary_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle, delimiter=";")
        writer.writerow(["type", "category", "term", "main", "count"])
        for (category, main), count in sorted(summary.items()):
            writer.writerow(["category_main", category, "", main, count])
        for (category, term, main), count in sorted(by_term.items()):
            writer.writerow(["category_term_main", category, term, main, count])
    with flags_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "row", "problem", "category", "term", "main", "segment", "snippet"], delimiter=";")
        writer.writeheader()
        writer.writerows(flags)
    wb.close()
    print(f"Summary: {summary_path}")
    print(f"Flags: {flags_path}")
    print(f"Arbeitsmappenprofil: {profile}")
    print(f"Auffaellige Zeilen: {len(flags)}")


if __name__ == "__main__":
    main()

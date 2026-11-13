"""Ranking construction shared by the standalone builder and capture importer."""
from collections import Counter

from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo

from analysis_views import set_compact_ranking_totals
from enpa_common import clean, expand_categories, search_terms

RANKING_HEADERS = [
    "Kategorie", "Begriff", "Treffergesamtanzahl", "Treffer gesamt N1-N3",
    "Treffer gesamt M1+M2", "Sonstige Treffer", "Relevanzquote",
]


def compact_ranking_group_map(config):
    groups = {}
    for group in (config or {}).get("compactRankingGroups") or []:
        label = clean(group.get("label"))
        terms = tuple(clean(term) for term in group.get("terms", []) if clean(term))
        if not label or len(terms) < 2:
            continue
        for term in terms:
            if term in groups:
                raise ValueError(f"Suchbegriff ist mehreren Rankinggruppen zugeordnet: {term}")
            groups[term] = (label, terms)
    return groups


def update_compact_ranking(wb, coding_ws, cols, last_data_row, config=None, *, include_catalog=False):
    name = next((name for name in ("09_Kompakt_Ranking", "04_Kompakt_Ranking") if name in wb.sheetnames), None)
    if name is None:
        return
    group_map = compact_ranking_group_map(config)
    counts = Counter()
    terms_by_key = {}
    for values in coding_ws.iter_rows(min_row=2, max_row=max(2, last_data_row), values_only=True):
        category = clean(values[cols["Suchkategorie A-H"] - 1])
        term = clean(values[cols["Suchbegriff"] - 1])
        if clean(values[cols["Kontrollstatus"] - 1]).casefold() in {"ausschliessen", "auszuschliessen"}:
            continue
        if category and term:
            label, terms = group_map.get(term, (term, (term,)))
            key = (category, label)
            counts[key] += 1
            terms_by_key[key] = terms
    if include_catalog:
        # Only configured queries contribute historical forms; no research file is read.
        for category in expand_categories(config):
            for query in config.get("queries", []) or [{"dateFrom": "9999-01-01"}]:
                for term in search_terms(config, category, query):
                    label, terms = group_map.get(term, (term, (term,)))
                    key = (category, label)
                    counts.setdefault(key, 0)
                    terms_by_key[key] = terms
    rows = sorted(counts, key=lambda key: (-counts[key], key[0].casefold(), key[1].casefold()))
    ws = wb[name]
    old_end = ws.max_row
    for row in ws.iter_rows(min_row=2, max_row=max(old_end, len(rows) + 2), min_col=1, max_col=7):
        for cell in row:
            cell.value = None
    for col, header in enumerate(RANKING_HEADERS, 1):
        ws.cell(1, col, header)
        ws.cell(1, col).fill = PatternFill("solid", fgColor="4472C4")
        ws.cell(1, col).font = Font(bold=True, color="FFFFFF")
        ws.cell(1, col).alignment = Alignment(wrap_text=True, vertical="center")
    source_end = max(2, last_data_row)
    ranges = {col: f"'01_Codierung'!${col}$2:${col}${source_end}" for col in ("J", "K", "AE", "O", "P", "Q")}
    if include_catalog and "CodierungDaten" in coding_ws.tables:
        # Native table references automatically expand for manual Excel entry.
        ranges = {col: f"CodierungDaten[{coding_ws[f'{col}1'].value}]" for col in ranges}
    natural = "+".join(f'({ranges[col]}="{code}")' for col in ("O", "P", "Q") for code in ("N1", "N2", "N3"))
    human = "+".join(f'({ranges[col]}="{code}")' for col in ("O", "P", "Q") for code in ("M1", "M2"))
    for row, (category, label) in enumerate(rows, 2):
        ws.cell(row, 1, category)
        ws.cell(row, 2, label)
        totals, naturals, humans = [], [], []
        for term in terms_by_key[(category, label)]:
            escaped = term.replace('"', '""')
            count_term = escaped.replace("~", "~~").replace("*", "~*").replace("?", "~?")
            totals.append(f'COUNTIFS({ranges["J"]},$A{row},{ranges["K"]},"{count_term}",{ranges["AE"]},"<>ausschliessen",{ranges["AE"]},"<>auszuschliessen")')
            common = f'--({ranges["J"]}=$A{row}),--({ranges["K"]}="{escaped}"),--({ranges["AE"]}<>"ausschliessen"),--({ranges["AE"]}<>"auszuschliessen")'
            naturals.append(f'SUMPRODUCT({common},--(({natural})>0))')
            humans.append(f'SUMPRODUCT({common},--(({human})>0),--(({natural})=0))')
        for col, parts in ((3, totals), (4, naturals), (5, humans)):
            ws.cell(row, col, "=" + (parts[0] if len(parts) == 1 else f'SUM({",".join(parts)})'))
        ws.cell(row, 6, f'=MAX(0,$C{row}-$D{row}-$E{row})')
        ws.cell(row, 7, f'=IF($C{row}=0,"",$D{row}/$C{row})')
        for col in range(1, 8):
            ws.cell(row, col).alignment = Alignment(vertical="top", wrap_text=col < 3)
            ws.cell(row, col).number_format = "0.0%" if col == 7 else "#,##0" if col > 2 else "General"
    last = max(2, len(rows) + 1)
    for row in list(ws.row_dimensions):
        if row > max(last + 1, 5):
            del ws.row_dimensions[row]
    if "KompaktRankingLive" not in ws.tables:
        table = Table(displayName="KompaktRankingLive", ref=f"A1:G{last}")
        table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True)
        ws.add_table(table)
    ws.tables["KompaktRankingLive"].ref = f"A1:G{last}"
    ws.tables["KompaktRankingLive"].totalsRowCount = 0
    ws.freeze_panes = None
    notes = [
        ("Berechnungsgrundlage", "01_Codierung"),
        ("Relevant", "Kontrollstatus ausschliessen/auszuschliessen bleibt unberücksichtigt; Haupt- oder Nebencode N1, N2 oder N3"),
        ("Menschengemacht", "Kontrollstatus ausschliessen/auszuschliessen bleibt unberücksichtigt; Haupt- oder Nebencode M1 oder M2, sofern kein N1-N3-Code vorliegt"),
        ("Sonstige Treffer", "Gesamt der nicht ausgeschlossenen Treffer minus N1-N3 minus exklusive M1-M2-Treffer"),
        ("Aktualisierung", "Formeln reagieren auf Nachcodierungen vorhandener Zeilen. Nach neuen Importen wird das Ranking neu aufgebaut."),
    ]
    for row, (label, text) in enumerate(notes, 1):
        ws.cell(row, 9, label)
        ws.cell(row, 10, text)
        ws.cell(row, 10).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[row].height = 42 if row > 1 else 34
    for col, width in zip("ABCDEFGHIJ", [14, 34, 22, 22, 23, 18, 20, 3, 22, 70]):
        ws.column_dimensions[col].width = width
    set_compact_ranking_totals(ws, last)

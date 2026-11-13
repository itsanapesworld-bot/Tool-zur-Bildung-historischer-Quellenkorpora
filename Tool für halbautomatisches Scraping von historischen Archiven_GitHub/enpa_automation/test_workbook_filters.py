from __future__ import annotations

import unittest

from openpyxl import Workbook
from openpyxl.worksheet.table import Table

from apply_master_dropdowns import VALIDATION_MAP, update_coding_validations
from enpa_common import CODING_HEADERS
from import_captures import update_coding_autofilter, update_compact_ranking


def coding_workbook() -> tuple[Workbook, object]:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "01_Codierung"
    headers = CODING_HEADERS + ["Volltext"]
    sheet.append(headers)
    sheet.append([None, 1910] + [None] * (len(headers) - 2))
    sheet.add_table(Table(displayName="CodierungDaten", ref="A1:AI2"))
    sheet.auto_filter.ref = "A1:AH2"
    return workbook, sheet


class WorkbookFilterTests(unittest.TestCase):
    def test_compact_ranking_uses_full_source_range_and_only_real_terms(self) -> None:
        workbook, coding = coding_workbook()
        headers = {cell.value: cell.column for cell in coding[1]}
        coding.delete_rows(2, coding.max_row - 1)

        for category, term, main, secondary, status in [
            ("A", "Hochwasser", "N1", "", "nachcodieren"),
            ("A", "Hochwasser", "S1", "", "geprüft"),
            ("B", "Gewitter", "M1", "N2", "nachcodieren"),
            ("C", "Rauschen", "N1", "", "ausschliessen"),
            ("C", "Altwert", "N1", "", "auszuschliessen"),
        ]:
            row = [None] * len(coding[1])
            row[headers["Falljahr"] - 1] = 1910
            row[headers["Suchkategorie A-H"] - 1] = category
            row[headers["Suchbegriff"] - 1] = term
            row[headers["Hauptcode"] - 1] = main
            row[headers["Nebencode 1"] - 1] = secondary
            row[headers["Kontrollstatus"] - 1] = status
            coding.append(row)

        ranking = workbook.create_sheet("09_Kompakt_Ranking")
        ranking.append(["Kategorie", "Begriff", "Treffergesamtanzahl", "Treffer gesamt N1-N3", "Treffer gesamt M1+M2", "Sonstige Treffer", "Relevanzquote"])
        for _ in range(8):
            ranking.append([None] * 7)
        ranking.add_table(Table(displayName="KompaktRankingLive", ref="A1:G9"))

        update_compact_ranking(workbook, coding, headers, 6)

        self.assertEqual(ranking["A2"].value, "A")
        self.assertEqual(ranking["B2"].value, "Hochwasser")
        self.assertIn("$J$2:$J$6", ranking["C2"].value)
        self.assertIn("$K$2:$K$6", ranking["C2"].value)
        self.assertIn("$P$2:$P$6", ranking["D2"].value)
        self.assertIn("$AE$2:$AE$6", ranking["C2"].value)
        self.assertIn('"<>ausschliessen"', ranking["C2"].value)
        self.assertIn('<>"auszuschliessen"', ranking["D2"].value)
        self.assertTrue(ranking["F2"].value.startswith("=MAX(0,"))
        self.assertEqual(ranking["G2"].number_format, "0.0%")
        self.assertEqual(ranking.tables["KompaktRankingLive"].ref, "A1:G4")
        self.assertEqual(ranking["A4"].value, "Gesamtsumme")
        self.assertEqual(ranking["C4"].value, "=SUM(KompaktRankingLive[Treffergesamtanzahl])")
        self.assertEqual(ranking.tables["KompaktRankingLive"].autoFilter.ref, "A1:G3")
        self.assertNotIn("Rauschen", [ranking[f"B{row}"].value for row in range(2, 6)])
        self.assertNotIn("Altwert", [ranking[f"B{row}"].value for row in range(2, 6)])
        workbook.close()

    def test_compact_ranking_combines_configured_term_variants(self) -> None:
        workbook, coding = coding_workbook()
        headers = {cell.value: cell.column for cell in coding[1]}
        coding.delete_rows(2, coding.max_row - 1)

        for term, main in [
            ("ertrinken", "N1"),
            ("ertrank", "S1"),
            ("ertrunken", "N2"),
        ]:
            row = [None] * len(coding[1])
            row[headers["Falljahr"] - 1] = 1910
            row[headers["Suchkategorie A-H"] - 1] = "A"
            row[headers["Suchbegriff"] - 1] = term
            row[headers["Hauptcode"] - 1] = main
            coding.append(row)

        ranking = workbook.create_sheet("09_Kompakt_Ranking")
        ranking.append(["Kategorie", "Begriff", "Treffergesamtanzahl", "Treffer gesamt N1-N3", "Treffer gesamt M1+M2", "Sonstige Treffer", "Relevanzquote"])
        ranking.append([None] * 7)
        ranking.add_table(Table(displayName="KompaktRankingLive", ref="A1:G2"))

        config = {
            "compactRankingGroups": [{
                "label": "ertr*inken/-ank/-unken",
                "terms": ["ertrinken", "ertrank", "ertrunken"],
            }]
        }
        update_compact_ranking(workbook, coding, headers, 4, config=config)

        self.assertEqual(ranking["A2"].value, "A")
        self.assertEqual(ranking["B2"].value, "ertr*inken/-ank/-unken")
        self.assertTrue(ranking["C2"].value.startswith("=SUM(COUNTIFS("))
        self.assertIn(',"ertrinken",', ranking["C2"].value)
        self.assertIn(',"ertrank",', ranking["C2"].value)
        self.assertIn(',"ertrunken",', ranking["C2"].value)
        self.assertEqual(ranking["C2"].value.count("COUNTIFS("), 3)
        self.assertEqual(ranking.tables["KompaktRankingLive"].ref, "A1:G3")
        self.assertEqual(ranking["A3"].value, "Gesamtsumme")
        self.assertEqual(ranking.tables["KompaktRankingLive"].totalsRowCount, 1)
        workbook.close()

    def test_capture_import_keeps_only_table_filter_and_includes_volltext(self) -> None:
        workbook, sheet = coding_workbook()

        update_coding_autofilter(sheet, 2)

        table = sheet.tables["CodierungDaten"]
        self.assertIsNone(sheet.auto_filter.ref)
        self.assertEqual(table.ref, "A1:AI2")
        self.assertEqual(table.autoFilter.ref, "A1:AI2")
        workbook.close()

    def test_dropdown_update_keeps_only_table_filter_and_includes_volltext(self) -> None:
        workbook, sheet = coding_workbook()
        workbook.create_sheet("99_Listen")
        list_map = {list_name: (1, 1) for list_name in set(VALIDATION_MAP.values())}

        update_coding_validations(workbook, list_map)

        table = sheet.tables["CodierungDaten"]
        self.assertIsNone(sheet.auto_filter.ref)
        self.assertEqual(table.ref, "A1:AI2")
        self.assertEqual(table.autoFilter.ref, "A1:AI2")
        workbook.close()

if __name__ == "__main__":
    unittest.main()

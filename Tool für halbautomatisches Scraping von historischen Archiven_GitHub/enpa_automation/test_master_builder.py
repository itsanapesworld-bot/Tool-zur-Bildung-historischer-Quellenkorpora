from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch

from analysis_views import refresh_analysis_views
from build_master import (
    MASTER_CODING_HEADERS, RECALL_HEADERS, SHEET_NAMES, VALIDATION_MAP,
    build_workbook, resolve_output, validate_candidate,
)
from compact_ranking import update_compact_ranking


def configuration():
    return {
        "__config_path": str(Path(__file__).with_name("config.json")),
        "phaseCodingScheme": "legacy_v1", "categoriesToRun": ["A", "B"],
        "searchCategories": {
            "A": {"label": "Wasser", "terms": ["Hochwasser", "ertrinken", "ertrank"], "historicalTerms": ["Wasserschwellung"]},
            "B": {"label": "Wetter", "terms": ["Gewitter"]},
        },
        "includeHistoricalTermsForYearsUpTo": 1999,
        "compactRankingGroups": [{"label": "ertrinken/ertrank", "terms": ["ertrinken", "ertrank"]}],
        "queries": [
            {"name": "Test", "eventName": "Hochwasser 1910", "eventStart": "1910-06-14", "windowType": phase,
             "dateFrom": f"{year}-06-14", "dateTo": f"{year}-06-{day}"}
            for year, phase, day in ((1910, "primary", "34"), (1911, "anniversary_1", "20"),
                                     (1915, "anniversary_5", "20"), (1920, "anniversary_10", "20"))
        ],
    }


class MasterBuilderTests(TestCase):
    def setUp(self):
        self.config = configuration()
        self.config["queries"][0]["dateTo"] = "1910-07-04"

    def test_build_reads_no_workbook_and_has_all_sheets(self):
        with patch("openpyxl.load_workbook", side_effect=AssertionError("Workbook input forbidden")):
            wb = build_workbook(self.config)
        self.assertEqual(wb.sheetnames, SHEET_NAMES)
        self.assertEqual([cell.value for cell in wb["01_Codierung"][1]], MASTER_CODING_HEADERS)
        self.assertEqual(wb["01_Codierung"].max_row, 2)
        self.assertTrue(all(cell.value is None for cell in wb["01_Codierung"][2]))
        self.assertEqual(len(wb["01_Codierung"].data_validations.dataValidation), len(VALIDATION_MAP))
        for ws in wb:
            self.assertIsNone(ws.freeze_panes)
            self.assertEqual(ws.sheet_view.topLeftCell, "A1")
        wb.close()

    def test_recall_table_and_analysis_sections(self):
        wb = build_workbook(self.config)
        recall = wb["06_Recall_Kontrolle"]
        self.assertEqual([cell.value for cell in recall[1]], RECALL_HEADERS)
        recall_table = recall.tables["RecallKontrolleDaten"]
        self.assertEqual(recall_table.ref, "A1:G50")
        self.assertTrue(recall["G50"].alignment.wrap_text)
        self.assertIsNotNone(recall["A1"].fill.fgColor.rgb)
        self.assertEqual(wb["05_Auswertung"]["A10"].value, "Ausgeschlossene Beiträge ohne Einfluss auf die Auswertung")
        self.assertEqual(wb["97_Auswertung_Hilfe"]["AE1"].value, "Ausgeschlossen")
        self.assertEqual(len(wb["05_Auswertung"].data_validations.dataValidation), 4)
        labels = [cell.value for cell in wb["05_Auswertung"]["B"]]
        for label in ("Hauptuntersuchungszeitraum", "1-Jahresjubiläum", "5-Jahresjubiläum", "10-Jahresjubiläum", "1910", "1911", "1915", "1920"):
            self.assertIn(label, labels)
        wb.close()

    def test_empty_ranking_contains_configured_groups_and_totals(self):
        wb = build_workbook(self.config)
        ws = wb["09_Kompakt_Ranking"]
        terms = [cell.value for cell in ws["B"]]
        self.assertIn("ertrinken/ertrank", terms)
        self.assertIn("Wasserschwellung", terms)
        table = ws.tables["KompaktRankingLive"]
        total = int(table.ref.split("G")[1])
        self.assertEqual(ws.cell(total, 1).value, "Gesamtsumme")
        self.assertEqual(table.totalsRowCount, 1)
        self.assertEqual(ws.cell(total, 3).value, "=SUM(KompaktRankingLive[Treffergesamtanzahl])")
        self.assertEqual(ws.cell(total, 7).value, f'=IF(C{total}=0,"",D{total}/C{total})')
        self.assertIn("<>ausschliessen", ws["C2"].value)
        wb.close()

    def test_roundtrip_validation_without_research_files(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "Master_Codiermatrix_Leer.xlsx"
            wb = build_workbook(self.config)
            wb.save(path)
            wb.close()
            result = validate_candidate(path)
            self.assertEqual(result["sheets"], 12)
            self.assertGreater(result["analysis_formulas"], 500)

    def test_import_refresh_preserves_layout_and_recall(self):
        wb = build_workbook(self.config)
        wb["06_Recall_Kontrolle"]["C2"] = "Manueller Kontrollbeitrag"
        source = wb["01_Codierung"]
        cols = {header: col for col, header in enumerate(MASTER_CODING_HEADERS, 1)}
        for row, article, status in ((2, "same", "ausschliessen"), (3, "same", "geprüft"), (4, "other", "geprüft")):
            values = {"ID": f"T{row}", "Falljahr": 1910, "Zeitung": "DBU", "Ausgabe-Datum": "1910-06-14",
                      "Artikel-/Segment-ID": article, "Suchkategorie A-H": "A", "Suchbegriff": "Hochwasser",
                      "Hauptcode": "N1", "Kontrollstatus": status}
            for header, value in values.items():
                source.cell(row, cols[header], value)
        before = (list(map(str, wb["05_Auswertung"].merged_cells.ranges)), wb["05_Auswertung"].column_dimensions["A"].width)
        stats = refresh_analysis_views(wb, self.config)
        update_compact_ranking(wb, source, cols, 4, self.config)
        self.assertEqual(stats["raw_rows"], 2)
        self.assertEqual(stats["unique_articles"], 2)
        self.assertEqual(stats["excluded_rows"], 1)
        after = (list(map(str, wb["05_Auswertung"].merged_cells.ranges)), wb["05_Auswertung"].column_dimensions["A"].width)
        self.assertEqual(before, after)
        self.assertEqual(wb["06_Recall_Kontrolle"]["C2"].value, "Manueller Kontrollbeitrag")
        self.assertIn("$AE$", wb["05_Auswertung"]["B10"].value)
        self.assertEqual(wb["09_Kompakt_Ranking"].tables["KompaktRankingLive"].ref, "A1:G3")
        wb.close()

    def test_builder_cannot_overwrite_a_research_profile(self):
        with TemporaryDirectory() as directory:
            path = str(Path(directory) / "Master_Codiermatrix_Leer.xlsx")
            config = deepcopy(self.config)
            config["workbook"] = path
            with self.assertRaisesRegex(ValueError, "Geschützte"):
                resolve_output(config, path)
            with self.assertRaises(ValueError):
                resolve_output({}, str(Path(directory) / "comparison.xlsx"))


if __name__ == "__main__":
    main()

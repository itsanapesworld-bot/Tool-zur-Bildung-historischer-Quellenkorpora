from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from enpa_common import expand_categories, search_string, search_terms
from import_captures import capture_search_filter_reason, read_capture_files, sync_cases_sheet


def test_config() -> dict:
    return {
        "categoriesToRun": ["A-H"],
        "includeHistoricalTermsForYearsUpTo": 1999,
        "searchCategories": {
            "A": {
                "terms": ["Überschwemmung", "Hochwasser"],
                "historicalTerms": ["Fluth"],
            },
            "B": {"terms": ["Wolkenbruch"], "historicalTerms": []},
            "C": {"terms": ["unter Wasser"], "historicalTerms": []},
            "D": {"enabled": False, "terms": [], "historicalTerms": []},
            "E": {"terms": ["Hilfskomitee", "Evakuation", "Evakuierung", "evakuieren", "evakuiert"], "historicalTerms": []},
            "F": {"terms": ["Hochwasserschutz"], "historicalTerms": []},
            "G": {"terms": ["Katastrophe", "Naturkatastrophe"], "historicalTerms": []},
            "H": {"terms": ["Klimawandel"], "historicalTerms": []},
        },
    }


def current_record(config: dict, category: str, date_from: str = "1987-08-24") -> dict:
    terms = search_terms(config, category, {"dateFrom": date_from})
    return {
        "category": category,
        "dateFrom": date_from,
        "dateTo": "1987-09-16",
        "searchTerms": terms,
        "searchString": search_string(terms),
        "matchedTerm": terms[0],
        "articleId": "DEMO-IMPORT-FILTER-0001",
    }


class CaptureSearchFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = test_config()
        self.active = set(expand_categories(self.config))

    def reason(self, record: dict) -> str:
        return capture_search_filter_reason(record, self.config, self.active)

    def test_current_capture_is_accepted(self) -> None:
        self.assertEqual(self.reason(current_record(self.config, "A")), "")

    def test_disabled_category_is_rejected(self) -> None:
        record = {"category": "D", "dateFrom": "1987-08-24", "dateTo": "1987-09-16", "searchTerms": ["Rhein"]}
        self.assertIn("deaktiviert", self.reason(record))

    def test_capture_from_old_link_window_is_rejected(self) -> None:
        self.config["queries"] = [{"dateFrom": "1999-05-01", "dateTo": "1999-05-22"}]
        record = current_record(self.config, "A")
        self.assertIn("aktuell in config.json definierten Linkliste", self.reason(record))

    def test_obsolete_term_is_reported(self) -> None:
        record = current_record(self.config, "C")
        record["searchTerms"] = ["Schäden", "unter Wasser"]
        record["searchString"] = search_string(record["searchTerms"])
        reason = self.reason(record)
        self.assertIn("Schäden", reason)

    def test_old_stem_capture_is_rejected(self) -> None:
        record = current_record(self.config, "E")
        record["searchTerms"] = ["Hilfskomitee", "Evaku*"]
        record["searchString"] = "Hilfskomitee OR Evaku"
        reason = self.reason(record)
        self.assertIn("Evaku*", reason)
        self.assertIn("Evakuation", reason)

    def test_search_string_without_search_terms_is_supported(self) -> None:
        record = current_record(self.config, "E")
        record.pop("searchTerms")
        self.assertEqual(self.reason(record), "")

    def test_partial_phrase_hit_is_rejected(self) -> None:
        record = current_record(self.config, "C")
        record["matchedTerm"] = "unter"
        record["title"] = "Unter schwierigen Bedingungen"
        record["snippet"] = "Der Betrieb steht unter grossem Druck."
        self.assertIn("Trefferbegriff 'unter'", self.reason(record))

    def test_question_mark_ocr_variant_is_accepted(self) -> None:
        record = current_record(self.config, "A")
        record["matchedTerm"] = "?berschwemmung"
        record["snippet"] = "Eine ?berschwemmung richtete Schäden an."
        self.assertEqual(self.reason(record), "")

    def test_capture_source_is_attached_to_each_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "enpa_v2_A_1987-08-24_1.json"
            path.write_text(json.dumps({"records": [current_record(self.config, "A")]}), encoding="utf-8")
            records, files = read_capture_files(Path(directory), "enpa_v2_*.json")
            self.assertEqual(files, [path])
            self.assertEqual(records[0]["_captureSource"], str(path.resolve()))


class CasesSheetSyncTests(unittest.TestCase):
    def test_queries_replace_existing_cases_sheet_rows(self) -> None:
        wb = Workbook()
        ws = wb.active
        ws.title = "04_Falljahre_Korpus"
        ws.append(["Name", "Ereignis", "Ereignisbeginn", "Ereignisende", "Fenster", "Von", "Bis"])
        ws.append(["Veraltet", "Alt", "", "", "primary", "1900-01-01", "1900-01-02"])
        config = {
            "queries": [
                {
                    "name": "1910 Hauptzeitraum",
                    "eventName": "Hochwasser 1910",
                    "eventStart": "1910-06-14",
                    "eventEnd": "1910-06-17",
                    "windowType": "primary",
                    "dateFrom": "1910-06-14",
                    "dateTo": "1910-07-08",
                },
                {
                    "name": "1910 1 Jahresjubiläum",
                    "eventName": "Hochwasser 1910",
                    "eventStart": "1910-06-14",
                    "eventEnd": "1910-06-17",
                    "windowType": "anniversary_1",
                    "dateFrom": "1911-06-14",
                    "dateTo": "1911-06-24",
                },
            ]
        }

        sync_cases_sheet(wb, config)

        self.assertEqual(ws["A2"].value, "1910 Hauptzeitraum")
        self.assertEqual(ws["G3"].value, "1911-06-24")
        self.assertTrue(ws["A2"].alignment.wrap_text)
        self.assertEqual(ws.row_dimensions[2].height, 32)
        sync_cases_sheet(wb, {"queries": config["queries"][:1]})
        self.assertIsNone(ws["A3"].value)


if __name__ == "__main__":
    unittest.main()

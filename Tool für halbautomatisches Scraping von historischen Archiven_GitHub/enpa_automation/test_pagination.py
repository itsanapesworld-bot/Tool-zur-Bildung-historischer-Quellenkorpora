from __future__ import annotations

import unittest
from urllib.parse import parse_qs, urlparse

from enpa_common import build_search_url, expand_categories, query_key, search_string, search_terms
from generate_links import BOOKMARKLET_JS, build_rows, capture_block_complete


def pagination_config() -> dict:
    return {
        "falltyp": "Kalibrierung",
        "resultsPerPage": 100,
        "maxResultsPerQuery": "auto",
        "autoInitialResultsPerQuery": 100,
        "categoriesToRun": ["A"],
        "includeHistoricalTermsForYearsUpTo": 1999,
        "captureFilePrefix": "enpa_v2",
        "defaultPublications": [
            {"archiveCode": "BTB", "excelCode": "BT", "label": "Bieler Tagblatt"},
            {"archiveCode": "DBB", "excelCode": "DBU", "label": "Der Bund"},
            {"archiveCode": "NZZ", "excelCode": "NZZ", "label": "Neue Zürcher Zeitung"},
            {"archiveCode": "SLB", "excelCode": "SEB", "label": "Seeländer Bote"},
        ],
        "queries": [
            {
                "name": "Testabfrage",
                "eventName": "Testereignis",
                "eventStart": "1851-08-01",
                "eventEnd": "1851-08-01",
                "windowType": "primary",
                "dateFrom": "1851-08-01",
                "dateTo": "1851-08-21",
            }
        ],
        "searchCategories": {
            "A": {
                "label": "Spezifische Naturgefahrenbegriffe",
                "terms": ["Hochwasser"],
                "historicalTerms": [],
            }
        },
    }


class PaginationTest(unittest.TestCase):
    def test_search_urls_use_100_results_and_101_start(self):
        config = pagination_config()
        query = config["queries"][0]

        first_url, first_meta = build_search_url(config, query, "A", 1)
        second_url, second_meta = build_search_url(config, query, "A", 101)
        first_params = parse_qs(urlparse(first_url).query)
        second_params = parse_qs(urlparse(second_url).query)

        self.assertEqual(first_params["r"], ["1"])
        self.assertEqual(second_params["r"], ["101"])
        self.assertEqual(first_params["results"], ["1"])
        self.assertEqual(second_params["results"], ["1"])
        self.assertIn("--de-100-", first_params["e"][0])
        self.assertIn("--de-100-", second_params["e"][0])
        self.assertIn("-101-byDA-", second_params["e"][0])
        self.assertEqual(first_meta["pageSize"], 100)
        self.assertEqual(second_meta["pageSize"], 100)

    def test_hyphenated_phrases_do_not_break_100_result_state(self):
        config = pagination_config()
        config["searchCategories"]["A"]["terms"] = [
            "Pegel-Regulierung",
            "Elementarschadens-Fonds",
        ]

        url, metadata = build_search_url(config, config["queries"][0], "A", 1)
        params = parse_qs(urlparse(url).query)

        canonical = '"Pegel-Regulierung" OR "Elementarschadens-Fonds"'
        self.assertEqual(params["txq"], [canonical])
        self.assertEqual(metadata["searchString"], canonical)
        self.assertIn("--de-100-", params["e"][0])
        self.assertIn('"Pegel Regulierung" OR "Elementarschadens Fonds"', params["e"][0])
        self.assertNotIn('"Pegel-Regulierung"', params["e"][0])
        self.assertNotIn('"Elementarschadens-Fonds"', params["e"][0])

    def test_known_total_creates_101_and_201_followup_pages(self):
        config = pagination_config()
        _, meta = build_search_url(config, config["queries"][0], "A", 1)
        counts = {
            query_key(meta): {
                "total": 213,
                "positions": set(range(1, 101)),
                "pages": {1},
                "pageSizes": {100},
            }
        }

        rows = build_rows(config, counts)

        self.assertEqual([row["startRank"] for row in rows], [101, 201])
        self.assertTrue(all(row["pageSize"] == 100 for row in rows))

    def test_complete_legacy_20_pages_cover_a_100_block(self):
        entry = {"positions": set(range(1, 101))}
        self.assertTrue(capture_block_complete(entry, 1, 100, 100))

    def test_incomplete_legacy_capture_is_offered_again(self):
        config = pagination_config()
        _, meta = build_search_url(config, config["queries"][0], "A", 1)
        counts = {
            query_key(meta): {
                "total": 34,
                "positions": set(range(1, 21)),
                "pages": {1},
                "pageSizes": {20},
            }
        }

        rows = build_rows(config, counts)

        self.assertEqual([row["startRank"] for row in rows], [1])
        self.assertEqual([row["pageSize"] for row in rows], [100])
        self.assertIn("--de-100-", parse_qs(urlparse(rows[0]["url"]).query)["e"][0])

    def test_77_total_with_only_20_captured_reopens_one_100_result_page(self):
        config = pagination_config()
        _, meta = build_search_url(config, config["queries"][0], "A", 1)
        counts = {
            query_key(meta): {
                "total": 77,
                "positions": set(range(1, 21)),
                "pages": {1},
                "pageSizes": {100},
            }
        }

        rows = build_rows(config, counts)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["startRank"], 1)
        self.assertEqual(rows[0]["pageSize"], 100)
        params = parse_qs(urlparse(rows[0]["url"]).query)
        self.assertEqual(params["r"], ["1"])
        self.assertIn("--de-100-", params["e"][0])

    def test_unknown_total_probes_next_page_after_full_first_page(self):
        config = pagination_config()
        _, meta = build_search_url(config, config["queries"][0], "A", 1)
        counts = {
            query_key(meta): {
                "total": None,
                "positions": set(range(1, 101)),
                "pages": {1},
                "pageSizes": {100},
            }
        }

        rows = build_rows(config, counts)

        self.assertEqual([row["startRank"] for row in rows], [101])

    def test_bookmarklet_uses_page_size_and_absolute_total_fallback(self):
        self.assertIn("records.length<ps", BOOKMARKLET_JS)
        self.assertIn("Number(meta.startRank||1)+records.length-1", BOOKMARKLET_JS)
        self.assertIn("pageSize:ps", BOOKMARKLET_JS)
        self.assertIn("totalResultCountParserVersion:4", BOOKMARKLET_JS)

    def test_explicit_terms_survive_search_url_metadata(self):
        config = pagination_config()
        config["searchCategories"]["A"]["terms"] = [
            "unter Wasser",
            "Elementarschaden-Fond",
            "Katastrophe",
        ]

        url, metadata = build_search_url(config, config["queries"][0], "A", 1)
        params = parse_qs(urlparse(url).query)

        expected = '"unter Wasser" OR "Elementarschaden-Fond" OR Katastrophe'
        self.assertEqual(search_string(config["searchCategories"]["A"]["terms"]), expected)
        self.assertEqual(metadata["searchString"], expected)
        self.assertEqual(params["txq"], [expected])
        self.assertEqual(metadata["searchTerms"], config["searchCategories"]["A"]["terms"])

    def test_bookmarklet_does_not_expand_suffix_wildcards(self):
        self.assertNotIn('if(ch==="*")return"[A-Za-z', BOOKMARKLET_JS)

    def test_disabled_category_is_omitted_even_for_a_to_h_range(self):
        config = pagination_config()
        config["categoriesToRun"] = ["A-H"]
        for category in "BCDEFGH":
            config["searchCategories"][category] = {
                "label": category,
                "terms": [category],
                "historicalTerms": [],
            }
        config["searchCategories"]["D"]["enabled"] = False

        self.assertEqual(expand_categories(config), ["A", "B", "C", "E", "F", "G", "H"])

    def test_prequoted_phrase_is_not_double_quoted(self):
        config = pagination_config()
        config["searchCategories"]["A"]["terms"] = ['"unter Wasser"', '"Elementarschaden-Fond"']
        query = config["queries"][0]

        terms = search_terms(config, "A", query)
        self.assertEqual(terms, ['"unter Wasser"', '"Elementarschaden-Fond"'])
        self.assertEqual(search_string(terms), '"unter Wasser" OR "Elementarschaden-Fond"')

    def test_stem_terms_and_asterisks_are_rejected(self):
        config = pagination_config()
        config["searchCategories"]["A"]["stemTerms"] = ["Katastroph"]
        with self.assertRaisesRegex(ValueError, "veraltete Stammbegriffe"):
            search_terms(config, "A", config["queries"][0])

        del config["searchCategories"]["A"]["stemTerms"]
        config["searchCategories"]["A"]["terms"] = ["Katastroph*"]
        with self.assertRaisesRegex(ValueError, "Sternchen"):
            search_terms(config, "A", config["queries"][0])


if __name__ == "__main__":
    unittest.main()

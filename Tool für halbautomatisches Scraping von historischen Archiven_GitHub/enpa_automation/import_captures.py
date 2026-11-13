from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shutil
import warnings
import zipfile
from collections import Counter
from copy import copy
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import openpyxl
from openpyxl.worksheet.filters import AutoFilter

from analysis_views import refresh_analysis_views
from compact_ranking import compact_ranking_group_map, update_compact_ranking

from enpa_common import (
    AMBIGUOUS_DROWNING_TERMS,
    AMBIGUOUS_NATURAL_HAZARD_TERMS,
    CODING_HEADERS,
    CONTEXTUAL_FOREIGN_PLACE_TERMS,
    CONTEXTUAL_SWISS_PLACE_TERMS,
    DEFAULT_CONFIG,
    WRAPPED_TEXT_HEADERS,
    DAMAGE_TERMS,
    DAM_BREACH_PROCESS_TERMS,
    DAM_BREACH_STRUCTURE_TERMS,
    DAMAGED_COMPOUND_NATURAL_TERMS,
    DAMAGED_NATURAL_CONTEXT_TERMS,
    DAMAGED_TERMS_CONDITIONAL,
    DIRECT_NATURAL_HAZARD_TERMS,
    ENV_TERMS,
    EUROPE_FOREIGN,
    EVACUATION_TERMS,
    EVENT_LOCAL_TERMS,
    FOREIGN_PLACE_ALIASES,
    FOREIGN_PLACE_ALIAS_TERMS,
    FOREIGN_TERMS,
    HAZARD_TERMS,
    HAUNTED_TERMS,
    HUMAN_MADE_HAZARD_TERMS,
    INTERNATIONAL_REFERENCE_TERMS,
    LOCAL_TERMS,
    LOCAL_SWISS_WATER_TERMS,
    NEAR_FOREIGN,
    NEWSPAPER_CANTON_CODES,
    NON_SWISS_COUNTRY_TERMS,
    PHASE_PREVENTION_TERMS,
    PHASE_RECOVERY_TERMS,
    PHASE_RESPONSE_TERMS,
    PHASE_WARNING_TERMS,
    POLITICAL_RESPONSIBILITY_TERMS,
    PREVENTION_TERMS,
    RETROSPECTIVE_TERMS,
    RISK_COMMUNICATION_TERMS,
    REGIONAL_TERMS,
    SHORT_OVERVIEW_HEADERS,
    SOLIDARITY_TERMS,
    SUPPORT_ONLY_SWISS_PLACE_TERMS,
    STRONG_NON_SWISS_PLACE_TERMS,
    SWISS_CITY_TERMS,
    SWISS_PLACE_OCR_ALIASES,
    SWISS_PLACE_OCR_TERMS,
    SWISS_NATIONAL_ADDRESS_QUALIFIERS,
    SWISS_NATIONAL_DESIGNATION_TERMS,
    SWISS_TERMS,
    SWISS_WATER_CANTONS_BY_TERM,
    SWISS_WATER_FOREIGN_COLLISION_TERMS,
    SWISS_WATER_STRONG_TERMS,
    CONTEXTUAL_SWISS_WATER_TERMS,
    TRANSBOUNDARY_PLACE_TERMS,
    INTENSITY_TERMS,
    NOTLAGE_TERMS,
    RAGING_TERMS,
    WATER_BODY_TERMS,
    WATER_LEVEL_QUALIFIERS,
    WATER_LEVEL_TERMS,
    WATER_RISE_PROCESS_TERMS,
    WATER_PROCESS_CONTEXT_TERMS,
    WEATHER_FORCE_TERMS,
    WEATHER_PROCESS_TERMS,
    WEATHER_SHIFT_TERMS,
    CONFLICT_TERMS,
    clean,
    candidate_terms,
    contains_any,
    contains_term,
    conflict_reference_kind,
    ddmmyyyy,
    expand_categories,
    find_col,
    has_human_made_hazard,
    header_map,
    load_config,
    matching_place_aliases,
    matching_terms,
    norm,
    parse_iso,
    quote_term,
    resolve_config_path,
    resolve_project_path,
    resolve_workbook_profile,
    risk_phase_values,
    search_terms,
)


AUTOCODING_RULE_VERSION = "V2.10"
from apply_master_dropdowns import current_list_map, remove_list_value, update_coding_validations


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Importiert ENPA-V2-Capture-JSONs in die Masterdatei.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--capture-dir", default="")
    parser.add_argument("--pattern", default="")
    parser.add_argument(
        "--workbook-profile",
        default="",
        help="Zielprofil aus config.json, z.B. calibration oder comparison.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite-existing", action="store_true", help="Reserviert; V2 ueberspringt vorhandene exakte Treffer standardmaessig.")
    return parser.parse_args()


def ensure_profile_writable(config: dict[str, Any], profile: str) -> None:
    read_only = {
        clean(value)
        for value in config.get("readOnlyWorkbookProfiles", [])
        if clean(value)
    }
    if profile in read_only:
        raise PermissionError(
            f"Das Arbeitsmappenprofil '{profile}' ist schreibgeschuetzt. "
            "Wähle ein beschreibbares eigenes Forschungsprofil."
        )


def duplicate_formula_cells(workbook_path: Path) -> dict[str, list[str]]:
    namespace = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    formula_tag = f"{{{namespace}}}f"
    cell_tag = f"{{{namespace}}}c"
    duplicates: dict[str, list[str]] = {}
    with zipfile.ZipFile(workbook_path, "r") as package:
        for part in package.namelist():
            if not part.startswith("xl/worksheets/") or not part.endswith(".xml"):
                continue
            root = ElementTree.fromstring(package.read(part))
            cells = []
            for cell in root.iter(cell_tag):
                if sum(1 for child in cell if child.tag == formula_tag) > 1:
                    cells.append(cell.get("r", "?"))
            if cells:
                duplicates[part] = cells
    return duplicates


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def frontend_page_value(_record: dict[str, Any]) -> str:
    """Keep page blank because ENPA list captures do not expose print pages."""
    return ""


def read_capture_files(capture_dir: Path, pattern: str) -> tuple[list[dict[str, Any]], list[Path]]:
    records: list[dict[str, Any]] = []
    files = sorted(capture_dir.glob(pattern))
    seen: dict[str, dict[str, Any]] = {}
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        for raw_record in payload.get("records", []):
            if not isinstance(raw_record, dict):
                continue
            record = dict(raw_record)
            source = str(path.resolve())
            record["_captureSource"] = source
            record["_captureSources"] = [source]
            key = exact_key(record)
            if key in seen:
                sources = seen[key].setdefault("_captureSources", [])
                if source not in sources:
                    sources.append(source)
                continue
            seen[key] = record
            records.append(record)
    return records, files


def split_capture_search_string(value: Any) -> list[str]:
    """Return the terms encoded in an ENPA OR query string."""
    raw = clean(value)
    if not raw:
        return []
    terms: list[str] = []
    for part in re.split(r"\s+OR\s+", raw, flags=re.IGNORECASE):
        term = clean(part).strip('"').replace(r'\"', '"')
        if term:
            terms.append(term)
    return terms


def rendered_term_signature(value: Any) -> str:
    """Normalize a project term exactly as it is sent to ENPA."""
    rendered = quote_term(clean(value)).strip('"').replace(r'\"', '"')
    rendered = rendered.casefold()
    rendered = re.sub(r"[‐‑‒–—]", "-", rendered)
    return re.sub(r"\s+", " ", rendered).strip()


def term_signature_map(terms: list[Any]) -> dict[str, str]:
    signatures: dict[str, str] = {}
    for value in terms:
        label = clean(value)
        signature = rendered_term_signature(label)
        if signature and signature not in signatures:
            signatures[signature] = label
    return signatures


def capture_query_terms(record: dict[str, Any]) -> list[str]:
    stored = record.get("searchTerms")
    if isinstance(stored, list):
        terms = [clean(term) for term in stored if clean(term)]
        if terms:
            return terms
    return split_capture_search_string(record.get("searchString"))


def matched_term_is_active(value: Any, expected_terms: list[str]) -> bool:
    candidate = clean(value)
    if not candidate:
        return True
    candidate_signature = rendered_term_signature(candidate)
    for term in expected_terms:
        if candidate_signature == rendered_term_signature(term) or contains_term(candidate, term):
            return True
        # Allow a single OCR replacement at a word edge, e.g. ?berschwemmung.
        candidate_ocr = norm(candidate)
        expected_signature = norm(quote_term(term).strip('"'))
        if (
            len(candidate_ocr) >= 6
            and abs(len(candidate_ocr) - len(expected_signature)) <= 2
            and (candidate_ocr in expected_signature or expected_signature in candidate_ocr)
        ):
            return True
    return False


def capture_search_filter_reason(
    record: dict[str, Any],
    config: dict[str, Any],
    active_categories: set[str],
) -> str:
    """Explain why a capture does not match the currently configured search."""
    category = clean(record.get("category")).upper()
    configured_categories = config.get("searchCategories") or {}
    if not category:
        return "Suchkategorie fehlt im Capture."
    if category not in configured_categories:
        return f"Suchkategorie {category} ist in der aktuellen config.json nicht definiert."
    if category not in active_categories:
        return f"Suchkategorie {category} ist aktuell deaktiviert oder nicht zur Ausführung ausgewählt."

    date_from = clean(record.get("dateFrom"))
    if not parse_iso(date_from):
        return "Startdatum dateFrom fehlt oder ist ungültig; die aktuelle Begriffsmenge ist nicht prüfbar."
    date_to = clean(record.get("dateTo"))
    if not parse_iso(date_to):
        return "Enddatum dateTo fehlt oder ist ungültig; das aktuelle Suchfenster ist nicht prüfbar."
    configured_windows = {
        (clean(query.get("dateFrom")), clean(query.get("dateTo")))
        for query in config.get("queries", [])
        if clean(query.get("dateFrom")) and clean(query.get("dateTo"))
    }
    if configured_windows and (date_from, date_to) not in configured_windows:
        return (
            f"Suchfenster {date_from} bis {date_to} gehört nicht zur aktuell in "
            "config.json definierten Linkliste."
        )
    expected_terms = search_terms(config, category, {"dateFrom": date_from})
    if not expected_terms:
        return f"Für Suchkategorie {category} sind aktuell keine Suchbegriffe aktiviert."

    actual_terms = capture_query_terms(record)
    if not actual_terms:
        return "Suchbegriffe fehlen im Capture; die Übereinstimmung mit config.json ist nicht prüfbar."
    expected = term_signature_map(expected_terms)
    actual = term_signature_map(actual_terms)
    obsolete = [actual[key] for key in sorted(actual.keys() - expected.keys())]
    missing = [expected[key] for key in sorted(expected.keys() - actual.keys())]
    if obsolete or missing:
        details: list[str] = []
        if obsolete:
            details.append("ausgeschlossene oder veraltete Begriffe: " + ", ".join(obsolete))
        if missing:
            details.append("aktuell erwartete Begriffe fehlen: " + ", ".join(missing))
        return "Veraltete Suchabfrage; " + "; ".join(details) + "."

    matched_term = infer_matched_term(record)
    if matched_term and not matched_term_is_active(matched_term, expected_terms):
        return (
            f"Rekonstruierter Trefferbegriff '{matched_term}' gehört nicht zur aktuell "
            f"aktivierten Suchabfrage der Kategorie {category}."
        )
    return ""


IMPORT_REPORT_FIELDS = [
    "status",
    "reason",
    "source_file",
    "row",
    "id",
    "category",
    "term",
    "main",
    "url",
]


def import_report_row(
    record: dict[str, Any],
    status: str,
    reason: str = "",
    **values: Any,
) -> dict[str, Any]:
    sources = record.get("_captureSources")
    source_file = " | ".join(clean(source) for source in sources if clean(source)) if isinstance(sources, list) else ""
    row = {
        "status": status,
        "reason": reason,
        "source_file": source_file or clean(record.get("_captureSource")),
        "row": "",
        "id": "",
        "category": clean(record.get("category")),
        "term": infer_matched_term(record),
        "main": "",
        "url": record_url(record),
    }
    row.update(values)
    return row


def write_import_report(report_path: Path, rows: list[dict[str, Any]]) -> None:
    with report_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=IMPORT_REPORT_FIELDS, delimiter=";")
        writer.writeheader()
        writer.writerows(rows)


def exact_key(record: dict[str, Any]) -> str:
    return "|".join([
        clean(record.get("articleId") or record.get("detailUrl")),
        clean(record.get("category")),
        clean(record.get("searchString")),
        clean(record.get("hitPosition")),
        clean(record.get("falltyp")),
        clean(record.get("dateFrom")),
        clean(record.get("dateTo")),
    ])


def infer_matched_term(record: dict[str, Any]) -> str:
    current = clean(record.get("matchedTerm"))
    terms = [clean(term) for term in record.get("searchTerms", []) if clean(term)]
    sample = " ".join([
        clean(record.get("matchedTermRaw")),
        clean(record.get("title")),
        clean(record.get("snippet")),
        clean(record.get("articleText")),
    ])
    if current and any(norm(current) == norm(term) for term in terms):
        return current
    best = ""
    best_score = -1
    for term in terms:
        score = len(norm(term))
        if contains_any(sample, [term]) and score > best_score:
            best = term
            best_score = score
    return best or current


@lru_cache(maxsize=8192)
def _contextual_place_patterns(term: str) -> tuple[re.Pattern[str], re.Pattern[str]] | None:
    needle = norm(term)
    if not needle:
        return None
    escaped = re.escape(needle)
    return (
        re.compile(
            rf"(?<![a-z0-9])(?:in|bei|aus|von|nach)\s+"
            rf"(?:(?:der|dem|den)\s+)?{escaped}(?![a-z0-9])"
        ),
        re.compile(rf"^{escaped}\s+(?:den\s+)?(?:[0-3]?\d)(?:\s|$)"),
    )


def contextual_place_matches(text: str, title: str, terms: set[str]) -> list[str]:
    """Match ambiguous place names only in explicit syntactic place context."""
    hay = norm(text)
    title_hay = norm(title)
    matches: list[str] = []
    for term in candidate_terms(f"{text} {title}", sorted(terms)):
        patterns = _contextual_place_patterns(term)
        if patterns is None:
            continue
        preposition, dated_heading = patterns
        if preposition.search(hay) or dated_heading.search(title_hay):
            matches.append(term)
    return matches


@lru_cache(maxsize=256)
def _contextual_water_patterns(term: str) -> tuple[re.Pattern[str], ...] | None:
    needle = norm(term)
    if not needle:
        return None
    escaped = re.escape(needle)
    if needle in SWISS_WATER_FOREIGN_COLLISION_TERMS:
        return (
            re.compile(
                rf"^{escaped}\s*[:\-].*(?:hochwasser|ufer|pegel|wasserstand)"
            ),
            re.compile(
                rf"(?<![a-z0-9])(?:an|am|entlang|unterhalb)\s+"
                rf"(?:(?:der|dem|den|die|das)\s+)?{escaped}(?![a-z0-9])"
            ),
            re.compile(
                rf"(?<![a-z0-9])(?:ufer|pegel|wasserstand)\s+"
                rf"(?:(?:der|des|am|im)\s+)?{escaped}(?![a-z0-9])"
            ),
        )
    return (
        re.compile(rf"^{escaped}(?:\s|$)"),
        re.compile(
            rf"(?<![a-z0-9])(?:an|am|entlang|im|in|aus|uber|unterhalb)\s+"
            rf"(?:(?:der|dem|den|die|das)\s+)?{escaped}(?![a-z0-9])"
        ),
        re.compile(
            rf"(?<![a-z0-9])(?:hochwasser|ufer|pegel|wasserstand)\s+"
            rf"(?:(?:der|des|am|im)\s+)?{escaped}(?![a-z0-9])"
        ),
    )


def contextual_water_matches(text: str, title: str) -> list[str]:
    """Match ordinary-language water names only in explicit hydrological context."""
    hay = norm(text)
    title_hay = norm(title)
    matches: list[str] = []
    terms = sorted(CONTEXTUAL_SWISS_WATER_TERMS)
    for term in candidate_terms(f"{text} {title}", terms):
        patterns = _contextual_water_patterns(term)
        if patterns and (patterns[0].search(title_hay) or any(
            pattern.search(hay) for pattern in patterns[1:]
        )):
            matches.append(term)
    return matches


def swiss_water_matches(text: str, title: str = "") -> list[str]:
    combined_text = f"{title} {text}".strip()
    return list(dict.fromkeys(
        matching_terms(combined_text, SWISS_WATER_STRONG_TERMS)
        + contextual_water_matches(text, title)
    ))


STRUCTURAL_PLACE_PREPOSITIONS = {"in", "bei", "aus", "von", "nach"}
STRUCTURAL_PLACE_ARTICLES = {"der", "dem", "den"}
STRUCTURAL_PLACE_STOPS = {
    "aber", "als", "am", "an", "auf", "durch", "ein", "eine", "einem", "einen",
    "einer", "eines", "fur", "für", "gestern", "hat", "heute", "im", "ist", "mit",
    "morgen", "oder", "sowie", "und", "vom", "war", "waren", "wurde", "wurden", "zu",
    "zum", "zur",
}
FUZZY_PLACE_STOPWORDS = {
    "ausland", "bericht", "drahtbericht", "hochwasser", "inland", "kultur", "lokales",
    "politik", "regionales", "sport", "sturm", "uberschwemmung", "ueberschwemmung",
    "unwetter", "wirtschaft", "wolkenbruch",
}


def _compact_place(value: str) -> str:
    return "".join(norm(value).split())


def _catalog_place_term(term: str) -> tuple[str, str] | None:
    raw = clean(term)
    if not raw or "*" in raw:
        return None
    normalized = norm(raw)
    compact = _compact_place(normalized)
    if len(compact) < 4 or not compact.isalpha():
        return None
    return normalized, compact


@lru_cache(maxsize=2)
def _place_match_indexes(
    side: str,
) -> tuple[dict[str, tuple[str, ...]], dict[tuple[int, str], tuple[tuple[str, str], ...]]]:
    if side == "swiss":
        exact_source = list(dict.fromkeys(
            SWISS_TERMS
            + EVENT_LOCAL_TERMS
            + [term for terms in LOCAL_TERMS.values() for term in terms]
            + [term for terms in REGIONAL_TERMS.values() for term in terms]
        ))
        fuzzy_source = list(dict.fromkeys(SWISS_CITY_TERMS + SWISS_PLACE_OCR_TERMS))
    else:
        exact_source = FOREIGN_TERMS
        fuzzy_source = list(dict.fromkeys(STRONG_NON_SWISS_PLACE_TERMS + FOREIGN_PLACE_ALIAS_TERMS))

    exact: dict[str, list[str]] = {}
    for term in exact_source:
        parsed = _catalog_place_term(term)
        if parsed is None:
            continue
        normalized, compact = parsed
        exact.setdefault(compact, [])
        if normalized not in exact[compact]:
            exact[compact].append(normalized)

    buckets: dict[tuple[int, str], list[tuple[str, str]]] = {}
    seen: set[tuple[str, str]] = set()
    for term in fuzzy_source:
        parsed = _catalog_place_term(term)
        if parsed is None:
            continue
        normalized, compact = parsed
        record = (compact, normalized)
        if record in seen:
            continue
        seen.add(record)
        buckets.setdefault((len(compact), compact[0]), []).append(record)
    return (
        {compact: tuple(terms) for compact, terms in exact.items()},
        {key: tuple(records) for key, records in buckets.items()},
    )


def _bounded_edit_distance(left: str, right: str, limit: int) -> int:
    if abs(len(left) - len(right)) > limit:
        return limit + 1
    previous = list(range(len(right) + 1))
    for row_index, left_char in enumerate(left, start=1):
        current = [row_index]
        row_minimum = row_index
        for column_index, right_char in enumerate(right, start=1):
            current.append(min(
                current[-1] + 1,
                previous[column_index] + 1,
                previous[column_index - 1] + (left_char != right_char),
            ))
            row_minimum = min(row_minimum, current[-1])
        if row_minimum > limit:
            return limit + 1
        previous = current
    return previous[-1]


def _structural_place_candidates(text: str, title: str) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(label: str, phrase: str) -> None:
        normalized = norm(phrase)
        if not normalized:
            return
        key = (label, normalized)
        if key not in seen:
            seen.add(key)
            candidates.append(key)

    title_tokens = norm(title).split()
    while title_tokens and title_tokens[0].isdigit():
        title_tokens.pop(0)
    if title_tokens and len(title_tokens) <= 8:
        for start in range(len(title_tokens)):
            for length in range(1, min(4, len(title_tokens) - start) + 1):
                add("Überschrift", " ".join(title_tokens[start:start + length]))

    combined = clean(f"{title} {text}")
    tokens = norm(combined).split()
    for index, token in enumerate(tokens):
        if token not in STRUCTURAL_PLACE_PREPOSITIONS:
            continue
        position = index + 1
        if position < len(tokens) and tokens[position] in STRUCTURAL_PLACE_ARTICLES:
            position += 1
        parts: list[str] = []
        for candidate_token in tokens[position:position + 4]:
            if candidate_token.isdigit() or candidate_token in STRUCTURAL_PLACE_STOPS:
                break
            parts.append(candidate_token)
            add("Präposition", " ".join(parts))

    dateline_pattern = re.compile(
        r"(?:^|[.!?;]\s+)([^,.;!?]{2,60}),\s*(?:den\s+)?\d{1,2}\.\s*(?:d\.)?",
        flags=re.IGNORECASE,
    )
    for match in dateline_pattern.finditer(combined):
        dateline_tokens = norm(match.group(1)).split()
        for length in range(1, min(4, len(dateline_tokens)) + 1):
            add("Datumszeile", " ".join(dateline_tokens[-length:]))

    locality_heading_pattern = re.compile(
        r"(?:^|(?:[.!?;]|[–—-])\s+)"
        r"([A-ZÄÖÜ][A-Za-zÄÖÜäöüß-]*(?:\s+[A-Za-zÄÖÜäöüß-]{1,}){0,3})\."
        r"\s*(?:\([A-Za-zÄÖÜäöüß. -]{1,16}\))?",
    )
    for match in locality_heading_pattern.finditer(combined):
        add("Ortszeile", match.group(1))
    return candidates


def _best_fuzzy_place_matches(candidate: str, side: str) -> tuple[int, list[str]] | None:
    compact = _compact_place(candidate)
    if len(compact) < 6 or compact in FUZZY_PLACE_STOPWORDS or not compact.isalpha():
        return None
    limit = 1 if len(compact) <= 9 else 2
    _, buckets = _place_match_indexes(side)
    hits: list[tuple[int, str]] = []
    for length in range(len(compact) - limit, len(compact) + limit + 1):
        for term_compact, term in buckets.get((length, compact[0]), ()):
            distance = _bounded_edit_distance(compact, term_compact, limit)
            if distance <= limit:
                hits.append((distance, term))
    if not hits:
        return None
    best_distance = min(distance for distance, _ in hits)
    best_terms = list(dict.fromkeys(term for distance, term in hits if distance == best_distance))
    if len(best_terms) != 1:
        return None
    return best_distance, best_terms


@lru_cache(maxsize=512)
def structural_place_matches(text: str, title: str) -> dict[str, list[str]]:
    result = {
        "swiss_formula": [],
        "foreign_formula": [],
        "swiss_fuzzy": [],
        "foreign_fuzzy": [],
        "swiss_formula_detail": [],
        "foreign_formula_detail": [],
        "swiss_fuzzy_detail": [],
        "foreign_fuzzy_detail": [],
        "fuzzy_ambiguous": [],
    }
    swiss_exact, _ = _place_match_indexes("swiss")
    foreign_exact, _ = _place_match_indexes("foreign")
    for label, candidate in _structural_place_candidates(text, title):
        compact = _compact_place(candidate)
        swiss_terms = list(swiss_exact.get(compact, ()))
        foreign_terms = list(foreign_exact.get(compact, ()))
        if swiss_terms and foreign_terms:
            result["fuzzy_ambiguous"].append(candidate)
            continue
        if swiss_terms or foreign_terms:
            side = "swiss" if swiss_terms else "foreign"
            terms = swiss_terms or foreign_terms
            result[f"{side}_formula"].extend(terms)
            for term in terms:
                correction = "; OCR-Trennung korrigiert" if norm(term) != norm(candidate) else ""
                result[f"{side}_formula_detail"].append(
                    f"{term} ({label}{correction}: {candidate})"
                )
            continue

        if label == "Überschrift" and len(norm(candidate).split()) > 1:
            continue

        swiss_fuzzy = _best_fuzzy_place_matches(candidate, "swiss")
        foreign_fuzzy = _best_fuzzy_place_matches(candidate, "foreign")
        if swiss_fuzzy and foreign_fuzzy and swiss_fuzzy[0] == foreign_fuzzy[0]:
            result["fuzzy_ambiguous"].append(candidate)
            continue
        if not swiss_fuzzy and not foreign_fuzzy:
            continue
        side = "swiss" if swiss_fuzzy and (not foreign_fuzzy or swiss_fuzzy[0] < foreign_fuzzy[0]) else "foreign"
        distance, terms = swiss_fuzzy if side == "swiss" else foreign_fuzzy  # type: ignore[misc]
        result[f"{side}_fuzzy"].extend(terms)
        result[f"{side}_fuzzy_detail"].extend(
            f"{term} (OCR/Fuzzy aus {label}: {candidate}; Distanz {distance})"
            for term in terms
        )
    return {key: list(dict.fromkeys(values)) for key, values in result.items()}


SWISS_STRUCTURAL_RUBRIC_TERMS = [
    "lokal*", "regional*", "region", "regionen", "kanton", "kantone", "kantonal*",
    "inland", "eidgenossenschaft", "eidgenössisch*", "eidgenoessisch*",
    "bundesversammlung", "bundespolitik", "bundesrat", "nationalrat",
    "ständerat", "staenderat", "schweiz*",
]
FOREIGN_STRUCTURAL_RUBRIC_TERMS = ["ausland", *NON_SWISS_COUNTRY_TERMS]
EVENT_FLOOD_TERMS = [
    "hochwasser*", "hochwasserkatastroph*", "überschwemm*", "ueberschwemm*",
    "überflutet*", "ueberflutet*", "fluth*", "sturzflut*", "dammbruch*",
    "wasserverheer*", "trat über die ufer", "trat ueber die ufer",
]
AD_ANCHOR_TERMS = [
    "stellenanzeige*", "stellenmarkt*", "privatmarkt*", "wohnungsanzeige*",
    "anzeige*", "voranzeige*", "inserat*", "reklame*",
]
SERVICE_DIRECTORY_TERMS = ["pikettdienste", "pikettdienst"]


def structural_rubric_from_title(title: str) -> str:
    """Recover a clear rubric heading when no dedicated metadata field exists."""
    heading = norm(title)
    if not heading or len(heading.split()) > 7:
        return ""
    swiss_patterns = [
        r"^(?:lokales|regional(?:es)?|region(?:en)?|kantonal(?:es)?|kantone?|inland)$",
        r"^(?:die )?(?:eidgenossenschaft|bundesversammlung|bundespolitik|bundesrat|nationalrat|standerat)$",
        r"^aus den kantonen$",
        r"^aus den verhandlungen der bundesversammlung$",
        r"^schweiz$",
    ]
    if any(re.fullmatch(pattern, heading) for pattern in swiss_patterns):
        return clean(title)

    for term in FOREIGN_STRUCTURAL_RUBRIC_TERMS:
        country = norm(clean(term).rstrip("*"))
        if not country:
            continue
        if heading in {
            country,
            f"aus {country}",
            f"aus dem {country}",
            f"aus der {country}",
            f"berichte aus {country}",
        }:
            return clean(title)
    return ""


def swiss_jura_context_matches(text: str) -> list[str]:
    """Recognize the Swiss usage ``im Jura`` without globalizing plain Jura."""
    hay = norm(text)
    for match in re.finditer(r"\bim\s+jura\b", hay):
        window = hay[max(0, match.start() - 50):match.end() + 50]
        if not matching_terms(window, FOREIGN_TERMS):
            return ["im Jura"]
    return []


def swiss_national_address_matches(text: str) -> list[str]:
    """Log explicit Swiss forms of address without globalizing their adjectives."""
    hay = norm(text)
    qualifiers = "|".join(
        re.escape(norm(term.rstrip("*"))) + r"[a-z0-9]*"
        for term in SWISS_NATIONAL_ADDRESS_QUALIFIERS
    )
    designations = "|".join(
        re.escape(norm(term.rstrip("*"))) + (r"[a-z0-9]*" if term.endswith("*") else "")
        for term in SWISS_NATIONAL_DESIGNATION_TERMS
        if norm(term.rstrip("*")) in {
            "schweizer", "schweizerin", "eidgenosse", "eidgenossin",
            "miteidgenosse", "miteidgenossin", "schweizervolk",
            "schweizerburger", "schweizerburgerin",
        }
    )
    pattern = re.compile(
        rf"\b(?:{qualifiers})(?:\s+[a-z0-9]+){{0,2}}\s+(?:{designations})\b"
    )
    return list(dict.fromkeys(match.group(0) for match in pattern.finditer(hay)))


def space_anchor_matches(
    text: str,
    newspaper: str,
    title: str = "",
    rubric: str = "",
) -> dict[str, list[str]]:
    structural = structural_place_matches(text, title)
    water = swiss_water_matches(text, title)
    local_water = [
        term for term in water if term in LOCAL_SWISS_WATER_TERMS.get(newspaper, set())
    ]
    newspaper_canton = NEWSPAPER_CANTON_CODES.get(newspaper)
    regional_water = [
        term for term in water
        if newspaper_canton
        and term not in local_water
        and newspaper_canton in SWISS_WATER_CANTONS_BY_TERM.get(term, frozenset())
    ]
    water_collision_hits = set(water) & SWISS_WATER_FOREIGN_COLLISION_TERMS
    foreign_strong = [
        term for term in matching_terms(text, FOREIGN_TERMS)
        if term not in water_collision_hits
    ]
    foreign_context = [
        term
        for term in contextual_place_matches(
            text, title, CONTEXTUAL_FOREIGN_PLACE_TERMS
        )
        if term not in water_collision_hits
    ]
    return {
        "local": matching_terms(text, EVENT_LOCAL_TERMS + LOCAL_TERMS.get(newspaper, [])),
        "regional": matching_terms(text, REGIONAL_TERMS.get(newspaper, [])),
        "water_local": local_water,
        "water_regional": regional_water,
        "swiss_water": water,
        "swiss_strong": matching_terms(text, SWISS_TERMS),
        "swiss_national_address": swiss_national_address_matches(text),
        "swiss_jura_context": swiss_jura_context_matches(text),
        "foreign_strong": foreign_strong,
        "swiss_context": contextual_place_matches(text, title, CONTEXTUAL_SWISS_PLACE_TERMS),
        "foreign_context": foreign_context,
        "ambiguous_raw": matching_terms(
            text, sorted(CONTEXTUAL_SWISS_PLACE_TERMS | CONTEXTUAL_FOREIGN_PLACE_TERMS)
        ),
        "support_only": matching_terms(text, sorted(SUPPORT_ONLY_SWISS_PLACE_TERMS)),
        "transboundary": matching_terms(text, sorted(TRANSBOUNDARY_PLACE_TERMS)),
        "rubric_swiss": matching_terms(rubric, SWISS_STRUCTURAL_RUBRIC_TERMS),
        "rubric_foreign": matching_terms(rubric, FOREIGN_STRUCTURAL_RUBRIC_TERMS),
        **structural,
    }


def infer_space(text: str, newspaper: str, title: str = "", rubric: str = "") -> str:
    matches = space_anchor_matches(text, newspaper, title, rubric)
    local_hit = bool(matches["local"] or matches["water_local"])
    regional_hit = bool(matches["regional"] or matches["water_regional"])
    explicit_swiss = bool(
        local_hit
        or regional_hit
        or matches["swiss_strong"]
        or matches["swiss_water"]
        or matches["swiss_national_address"]
        or matches["swiss_context"]
        or matches["swiss_jura_context"]
    )
    explicit_foreign = bool(matches["foreign_strong"] or matches["foreign_context"])
    structural_swiss = matches["swiss_formula"] + matches["swiss_fuzzy"]
    local_compacts = {
        _compact_place(term)
        for term in EVENT_LOCAL_TERMS + LOCAL_TERMS.get(newspaper, [])
        if "*" not in term
    }
    regional_compacts = {
        _compact_place(term)
        for term in REGIONAL_TERMS.get(newspaper, [])
        if "*" not in term
    }
    structural_compacts = {_compact_place(term) for term in structural_swiss}
    if explicit_swiss and explicit_foreign:
        return "Schweiz sowie Ausland"
    if local_hit:
        return "lokal"
    if regional_hit:
        return "regional"
    if explicit_swiss:
        return "Schweiz"
    if explicit_foreign:
        return "Ausland"
    if structural_compacts & local_compacts:
        return "lokal"
    if structural_compacts & regional_compacts:
        return "regional"
    swiss = bool(matches["swiss_formula"] or matches["swiss_fuzzy"])
    foreign = bool(matches["foreign_formula"] or matches["foreign_fuzzy"])
    if swiss and foreign:
        return "Schweiz sowie Ausland"
    if swiss:
        return "Schweiz"
    if foreign:
        return "Ausland"
    # Rubrics are fallback evidence only; explicit article geography above has priority.
    rubric_swiss = bool(matches["rubric_swiss"])
    rubric_foreign = bool(matches["rubric_foreign"])
    if rubric_swiss and rubric_foreign:
        return "Schweiz sowie Ausland"
    if rubric_swiss:
        return "Schweiz"
    if rubric_foreign:
        return "Ausland"
    return "unklar"


PUBLICATION_LABELS = {
    "SEB": ["Seeländer Bote", "Seelaender Bote"],
    "BT": ["Bieler Tagblatt"],
    "DBU": ["Der Bund"],
    "NZZ": ["Neue Zürcher Zeitung", "Neue Zuercher Zeitung"],
}


def strip_capture_boilerplate(snippet: str, newspaper: str) -> str:
    text = clean(snippet)
    for label in PUBLICATION_LABELS.get(newspaper, []):
        text = re.sub(re.escape(label), " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\[(?:ARTIKEL|ABSCHNITT)(?:\+ILLUSTRATION)?\]", " ", text, flags=re.IGNORECASE)
    return clean(text)


MONTH_NAMES = {
    "januar": 1, "jan": 1, "februar": 2, "feb": 2, "märz": 3, "maerz": 3,
    "marz": 3, "april": 4, "mai": 5, "juni": 6, "juli": 7, "august": 8,
    "september": 9, "oktober": 10, "november": 11, "dezember": 12,
}

SOCIAL_HARDSHIP_TERMS = [
    "soziale not", "notleidend*", "notlage*", "elend", "armut*", "verarm*",
    "mittellos*", "hilfsbedürftig*", "hilfsbeduerftig*", "obdachlos*",
    "heimatlos*", "notunterkunft*", "hungersnot*", "hungernd*", "nothilfe*",
    "hilferuf*", "hülferuf*", "huelferuf*", "existenz* vernichtet",
    "existenzgrundlage* zerstört", "existenzgrundlage* zerstoert",
    "hab und gut verloren", "alles verloren", "todesopfer*", "verletzte*",
    "ums leben gekommen", "verloren ihr leben",
]


def evidence_is_incomplete(
    title: str,
    snippet: str,
    article_text: str,
    article_evidence: str,
    evidence_source_count: int,
) -> bool:
    """Identify captures too short to distinguish ambiguity from irrelevance."""
    if len(norm(article_text)) >= 120:
        return False
    shared = norm(article_evidence)
    if evidence_source_count > 1 and len(shared) >= 120:
        return False
    body = norm(snippet)
    return len(body) < 100 or body == norm(title)


def _safe_date(year: int, month: int, day: int) -> date | None:
    try:
        return date(year, month, day)
    except ValueError:
        return None


def infer_occurrence_date(
    text: str,
    issue_date: date | None,
    date_from: date | None,
    date_to: date | None,
) -> date | None:
    """Extract the most plausible event date from title/snippet/article text.

    Bare day numbers are only accepted with German date markers such as
    ``den 7.`` or ``7. d.``. The candidate closest to a natural-hazard term is
    preferred so that a source date (``vom 6.``) does not displace the actual
    event date (``Wolkenbruch, der sich den 1. ...``).
    """
    if not issue_date:
        return None
    source = clean(text)
    normalized = norm(source)
    date_text = source.lower().translate(str.maketrans({"ä": "a", "ö": "o", "ü": "u", "ß": "ss"}))
    hazard_positions: list[int] = []
    for term in HAZARD_TERMS + PREVENTION_TERMS + EVACUATION_TERMS:
        needle = norm(term.rstrip("*"))
        if not needle:
            continue
        start = 0
        while True:
            pos = normalized.find(needle, start)
            if pos < 0:
                break
            hazard_positions.append(pos)
            start = pos + max(1, len(needle))

    candidates: list[tuple[int, int, date]] = []

    def add_candidate(candidate: date | None, position: int, priority: int) -> None:
        if not candidate or candidate > issue_date:
            return
        if date_from and candidate < date_from.replace(year=candidate.year):
            return
        if date_to and candidate > date_to.replace(year=candidate.year):
            return
        distance = min((abs(position - pos) for pos in hazard_positions), default=10_000)
        candidates.append((priority, distance, candidate))

    for match in re.finditer(r"(?<!\d)(\d{1,2})\.(\d{1,2})\.(\d{2,4})(?!\d)", source):
        day, month, year = map(int, match.groups())
        year = year + 1800 if year < 100 and issue_date.year < 1900 else year
        year = year + 1900 if year < 100 else year
        add_candidate(_safe_date(year, month, day), match.start(), 1)

    month_pattern = "|".join(sorted(MONTH_NAMES, key=len, reverse=True))
    for match in re.finditer(rf"(?<!\d)(\d{{1,2}})\.\s*({month_pattern})(?:\s+(\d{{4}}))?", date_text):
        day = int(match.group(1))
        month = MONTH_NAMES[match.group(2)]
        year = int(match.group(3) or issue_date.year)
        candidate = _safe_date(year, month, day)
        if candidate == issue_date and match.start() < 140:
            continue
        add_candidate(candidate, match.start(), 1)

    contextual_patterns = [
        (r"\b(?:am|den|unterm|auf den)\s+(\d{1,2})\.", 0),
        (r"\b(?:vom|des)\s+(\d{1,2})\.", 2),
        (r"\b(\d{1,2})\.\s*d\.", 0),
    ]
    for pattern, priority in contextual_patterns:
        for match in re.finditer(pattern, date_text):
            add_candidate(_safe_date(issue_date.year, issue_date.month, int(match.group(1))), match.start(), priority)

    if not candidates:
        return None
    candidates.sort(key=lambda item: (item[0], item[1], abs((issue_date - item[2]).days)))
    return candidates[0][2]


def natural_hazard_evidence(
    text: str,
    title: str,
    occurrence_date: date | None,
    event_start: date | None,
    event_end: date | None,
    pub_date: date | None = None,
    window_type: str = "",
) -> dict[str, Any]:
    direct_terms = matching_terms(text, DIRECT_NATURAL_HAZARD_TERMS)
    ambiguous_terms = matching_terms(text, AMBIGUOUS_NATURAL_HAZARD_TERMS)
    weather_terms = matching_terms(text, WEATHER_PROCESS_TERMS)
    damage_terms = matching_terms(text, DAMAGE_TERMS)
    water_terms = matching_terms(text, WATER_PROCESS_CONTEXT_TERMS)
    prevention_terms = matching_terms(text, PREVENTION_TERMS)
    evacuation_terms = matching_terms(text, EVACUATION_TERMS)
    risk_terms = matching_terms(text, RISK_COMMUNICATION_TERMS)
    retrospective_terms = matching_terms(text, RETROSPECTIVE_TERMS)
    conditional_terms: list[str] = []
    rule_notes: list[str] = []

    haunted_terms = matching_terms(text, HAUNTED_TERMS)
    haunted_context = bool(haunted_terms) and (
        contains_any(text, HAZARD_TERMS) or contains_term(text, "vom wasser")
    )
    if haunted_context:
        conditional_terms.extend(haunted_terms)
        conditional_terms.extend(matching_terms(text, HAZARD_TERMS + ["vom wasser"]))
        rule_notes.append(
            "Bedingter Naturgefahrenanker: 'heimgesucht' wurde zusammen mit einem Naturgefahren- oder Wasserbezug erkannt."
        )

    raging_terms = matching_terms(text, RAGING_TERMS)
    raging_context_terms = matching_terms(text, WEATHER_FORCE_TERMS)
    if raging_terms and raging_context_terms:
        conditional_terms.extend(raging_terms + raging_context_terms)
        rule_notes.append(
            "Bedingter Naturgefahrenanker: 'wütend/wütet' wurde zusammen mit einem Wetterbegriff erkannt."
        )

    damaged_terms = matching_terms(text, DAMAGED_TERMS_CONDITIONAL)
    damaged_context_terms = matching_terms(text, DAMAGED_NATURAL_CONTEXT_TERMS)
    damaged_compounds = matching_terms(text, DAMAGED_COMPOUND_NATURAL_TERMS)
    if (damaged_terms and damaged_context_terms) or damaged_compounds:
        conditional_terms.extend(damaged_terms + damaged_context_terms + damaged_compounds)
        rule_notes.append(
            "Bedingter Naturgefahrenanker: 'geschädigt' wurde mit einem Naturgefahren-/Wetterbezug oder als eindeutiges Kompositum erkannt."
        )

    weather_shift_terms = matching_terms(text, WEATHER_SHIFT_TERMS)
    weather_shift_context = matching_terms(text, HAZARD_TERMS + INTENSITY_TERMS + ["schneefall*"])
    if weather_shift_terms and weather_shift_context:
        conditional_terms.extend(weather_shift_terms + weather_shift_context)
        rule_notes.append(
            "Bedingter Naturgefahrenanker: Wetterumschlag wurde zusammen mit einem Gefahren- oder Intensitätsbegriff erkannt."
        )

    water_level_terms = matching_terms(text, WATER_LEVEL_TERMS)
    water_level_qualifiers = matching_terms(text, WATER_LEVEL_QUALIFIERS)
    if water_level_terms and water_level_qualifiers:
        conditional_terms.extend(water_level_terms + water_level_qualifiers)
        rule_notes.append(
            "Bedingter Naturgefahrenanker: Wasserstand wurde zusammen mit einer hohen/extremen Pegelqualifikation erkannt."
        )

    water_body_terms = matching_terms(text, WATER_BODY_TERMS)
    water_rise_terms = matching_terms(text, WATER_RISE_PROCESS_TERMS)
    if water_body_terms and water_rise_terms:
        conditional_terms.extend(water_body_terms + water_rise_terms)
        rule_notes.append(
            "Bedingter Naturgefahrenanker: Ein Gewässerbegriff wurde zusammen mit Anschwellen/Übertreten erkannt."
        )

    dam_breach_structures = matching_terms(text, DAM_BREACH_STRUCTURE_TERMS)
    dam_breach_processes = matching_terms(text, DAM_BREACH_PROCESS_TERMS)
    dam_breach_support = list(dict.fromkeys(
        water_body_terms + ambiguous_terms + weather_terms + damage_terms + direct_terms
    ))
    if dam_breach_structures and dam_breach_processes and dam_breach_support:
        conditional_terms.extend(
            dam_breach_structures + dam_breach_processes + dam_breach_support
        )
        rule_notes.append(
            "Bedingter Hochwasseranker: Damm/Dämme und Durchbrechen/Durchbruch wurden "
            "zusammen mit zusätzlichem Wasser-, Flut-, Wetter-, Schadens- oder "
            "Naturgefahrenkontext erkannt."
        )

    confirmed_ambiguous_terms: list[str] = []
    unconfirmed_ambiguous_terms: list[str] = []
    general_ambiguous_support = list(dict.fromkeys(
        direct_terms + weather_terms + damage_terms + water_terms
        + water_rise_terms + conditional_terms
    ))
    strict_drowning_support = list(dict.fromkeys(
        direct_terms + weather_terms + water_rise_terms + conditional_terms
    ))
    for term in ambiguous_terms:
        support = (
            strict_drowning_support
            if term in AMBIGUOUS_DROWNING_TERMS
            else general_ambiguous_support
        )
        if support:
            confirmed_ambiguous_terms.append(term)
        else:
            unconfirmed_ambiguous_terms.append(term)
    if confirmed_ambiguous_terms:
        conditional_terms.extend(confirmed_ambiguous_terms)
        rule_notes.append(
            "Mehrdeutiger Naturgefahrenbegriff wurde nur wegen zusätzlicher Wasser-, Wetter-, "
            "Schadens- oder eindeutiger Naturgefahrenevidenz berücksichtigt: "
            + ", ".join(dict.fromkeys(confirmed_ambiguous_terms + general_ambiguous_support))
            + "."
        )

    solidarity_terms = matching_terms(text, SOLIDARITY_TERMS)
    primary_media_cycle = bool(
        window_type == "primary" and pub_date and event_start and event_end
        and event_start.toordinal() <= pub_date.toordinal() <= event_end.toordinal() + 21
    )
    solidarity_temporal = bool(solidarity_terms and primary_media_cycle)
    if solidarity_temporal:
        rule_notes.append(
            "Aufgrund von zeitlicher Nähe zum untersuchten Ereignis als Naturgefahrenbezogen / relevant (N1,N2,N3) eingeordnet."
        )

    title_hazard = contains_any(title, HAZARD_TERMS)
    temporal_link = False
    if occurrence_date and event_start and event_end:
        temporal_link = event_start.toordinal() - 7 <= occurrence_date.toordinal() <= event_end.toordinal() + 21
    direct_event = bool(direct_terms or conditional_terms) or bool(
        weather_terms and (damage_terms or water_terms or title_hazard or temporal_link)
    )
    natural_context = bool(direct_terms or weather_terms or water_terms or conditional_terms)
    indirect = bool(prevention_terms)
    indirect = indirect or bool(evacuation_terms and natural_context)
    indirect = indirect or bool((risk_terms or retrospective_terms) and natural_context)
    indirect = indirect or bool(solidarity_temporal and not direct_event)
    return {
        "direct": direct_event,
        "indirect": indirect,
        "direct_terms": direct_terms,
        "weather_terms": weather_terms,
        "damage_terms": damage_terms,
        "water_terms": water_terms,
        "prevention_terms": prevention_terms,
        "evacuation_terms": evacuation_terms,
        "risk_terms": risk_terms,
        "retrospective_terms": retrospective_terms,
        "conditional_terms": list(dict.fromkeys(conditional_terms)),
        "confirmed_ambiguous_terms": list(dict.fromkeys(confirmed_ambiguous_terms)),
        "unconfirmed_ambiguous_terms": list(dict.fromkeys(unconfirmed_ambiguous_terms)),
        "solidarity_terms": solidarity_terms,
        "solidarity_temporal": solidarity_temporal,
        "notlage_terms": matching_terms(text, NOTLAGE_TERMS),
        "rule_notes": rule_notes,
        "temporal_link": temporal_link,
    }


def event_related_swiss_rubric_n1(
    text: str,
    rubric: str,
    evidence: dict[str, Any],
    occurrence_date: date | None,
    pub_date: date | None,
    event_start: date | None,
    event_end: date | None,
    window_type: str,
) -> bool:
    """Confirm the narrow primary-period N1 rule based on structural evidence."""
    effective_date = occurrence_date or pub_date
    date_matches = bool(
        effective_date and event_start and event_end
        and event_start.toordinal() - 7 <= effective_date.toordinal() <= event_end.toordinal() + 7
    )
    return bool(
        window_type == "primary"
        and evidence["direct"]
        and matching_terms(text, EVENT_FLOOD_TERMS)
        and matching_terms(rubric, SWISS_STRUCTURAL_RUBRIC_TERMS)
        and date_matches
        and not matching_terms(text, FOREIGN_TERMS)
    )


def uncertainty_cause(
    main: str,
    space: str,
    evidence: dict[str, Any],
    evidence_incomplete: bool,
) -> str:
    if main != "UN":
        return ""
    if evidence["direct"] and space == "unklar":
        return "Naturgefahr sicher, Raumbezug fehlt"
    if space != "unklar":
        return "Raumbezug vorhanden, Naturgefahrenbezug unsicher"
    if evidence_incomplete:
        return "Text für beide Entscheidungen zu kurz"
    return "Naturgefahr wahrscheinlich, Raumbezug fehlt"


def infer_codes(
    text: str,
    category: str,
    space: str,
    rubric: str,
    title: str = "",
    occurrence_date: date | None = None,
    event_start: date | None = None,
    event_end: date | None = None,
    pub_date: date | None = None,
    window_type: str = "",
    evidence_incomplete: bool = False,
    hazard_evidence: dict[str, Any] | None = None,
) -> tuple[str, str, str, list[str]]:
    notes: list[str] = []
    ad_source = f"{rubric} {title}"
    ad_terms = matching_terms(ad_source, AD_ANCHOR_TERMS)
    service_directory = contains_any(title, SERVICE_DIRECTORY_TERMS)
    evidence = hazard_evidence or natural_hazard_evidence(
        text, title, occurrence_date, event_start, event_end, pub_date, window_type
    )
    natural_direct = bool(evidence["direct"])
    natural_indirect = bool(evidence["indirect"])
    human_made = has_human_made_hazard(text)
    human_made_international = human_made and (contains_any(text, INTERNATIONAL_REFERENCE_TERMS) or space in {"Ausland", "Schweiz sowie Ausland"})
    env = contains_any(text, ENV_TERMS)
    conflict_kind = conflict_reference_kind(text)
    swiss = space in {"lokal", "regional", "Schweiz", "Schweiz sowie Ausland"}
    foreign = space in {"Ausland", "Schweiz sowie Ausland"}
    codes: list[str] = []
    if natural_direct:
        if swiss:
            codes.append("N1")
        if foreign:
            codes.append("N2")
        if not codes:
            codes.append("UN")
            notes.append(
                "Hauptcode UN: konkretes Naturgefahrenereignis erkannt, aber Raumbezug unklar; "
                "bitte überprüfen, ob N1 (Schweiz) oder N2 (Ausland) zutrifft."
            )
        trigger_terms = (
            evidence["direct_terms"] + evidence["weather_terms"]
            + evidence["damage_terms"] + evidence["conditional_terms"]
        )
        if trigger_terms:
            notes.append(f"Naturgefahrenregel ausgelöst durch: {', '.join(dict.fromkeys(trigger_terms))}.")
        notes.extend(evidence["rule_notes"])
        if "N1" in codes and event_related_swiss_rubric_n1(
            text,
            rubric,
            evidence,
            occurrence_date,
            pub_date,
            event_start,
            event_end,
            window_type,
        ):
            notes.append(
                "Ereignisbezogene N1-Regel: direkter Hochwasseranker, klar schweizerische "
                "Rubrik, passendes Datum im Hauptuntersuchungszeitraum und kein Auslandsanker."
            )
    elif natural_indirect:
        codes.append("N3")
        trigger_terms = (
            evidence["prevention_terms"] + evidence["evacuation_terms"]
            + evidence["risk_terms"] + evidence["retrospective_terms"]
            + evidence["solidarity_terms"]
        )
        if trigger_terms:
            notes.append(f"Hauptcode N3 nach indirekter Naturgefahren-/Präventionsregel; Auslöser: {', '.join(dict.fromkeys(trigger_terms))}.")
        notes.extend(evidence["rule_notes"])

    if service_directory and not codes:
        return "S1", "", "", [
            "Hauptcode S1: Titelanker 'Pikettdienst' kennzeichnet ein Dienstverzeichnis; "
            "kein beschriebenes Naturgefahrenereignis erkannt."
        ]

    # W1 is checked after natural hazards. A natural-hazard article in an
    # advertisement context therefore keeps its N code and receives W1 as a
    # secondary code; without an N code, W1 remains the primary code.
    if ad_terms:
        codes.append("W1")
        notes.append(f"Code W1: Anzeige-/Inseratanker erkannt ({', '.join(ad_terms)}).")

    # Strong K1 evidence follows any natural-hazard code, but precedes M1/M2.
    # Ambiguous conflict vocabulary is appended later and can only be secondary.
    if conflict_kind == "strong":
        codes.append("K1")
        conflict_terms = matching_terms(text, CONFLICT_TERMS)
        notes.append(f"Code K1: starker Krieg-/Konfliktanker erkannt ({', '.join(conflict_terms)}).")

    # M1/M2 are evaluated only after N1-N3 and K1. With a natural-hazard code
    # they remain secondary instead of displacing the relevant N code.
    if human_made_international:
        codes.append("M2")
        human_terms = matching_terms(text, HUMAN_MADE_HAZARD_TERMS)
        foreign_terms = matching_terms(text, INTERNATIONAL_REFERENCE_TERMS)
        notes.append(
            f"Code M2: menschengemachter Gefahrenanker ({', '.join(human_terms)}) "
            f"plus internationaler Raumanker ({', '.join(foreign_terms) or space})."
        )
    elif human_made:
        codes.append("M1")
        human_terms = matching_terms(text, HUMAN_MADE_HAZARD_TERMS)
        notes.append(f"Code M1: menschengemachter Gefahrenanker erkannt ({', '.join(human_terms)}); kein internationaler Raumanker gefunden.")

    if env:
        codes.append("U1")
        notes.append(f"Code U1: Umwelt-/Klimaanker erkannt ({', '.join(matching_terms(text, ENV_TERMS))}).")
    if not codes and evidence["notlage_terms"]:
        codes.append("UN")
        notes.append(
            "Hauptcode UN: 'Notlage' wurde erkannt, aber ohne belastbaren Naturgefahren-, Konflikt- "
            "oder menschengemachten Gefahrenanker. Die Regel verbietet in diesem Fall eine automatische S1-Zuordnung."
        )
    if not codes and evidence["unconfirmed_ambiguous_terms"] and evidence_incomplete:
        codes.append("UN")
        notes.append(
            "Hauptcode UN: Mehrdeutiger Begriff erkannt ("
            + ", ".join(evidence["unconfirmed_ambiguous_terms"])
            + "), aber die kurze bzw. titelgleiche Trefferfassung enthält keine ausreichende "
            "Evidenz für N1-N3 oder einen sicheren Ausschluss als S1."
        )
    elif not codes and evidence["unconfirmed_ambiguous_terms"]:
        notes.append(
            "Mehrdeutiger Begriff ohne bestätigenden Wasser-, Wetter-, Schadens- oder "
            "Naturgefahrenanker erkannt ("
            + ", ".join(evidence["unconfirmed_ambiguous_terms"])
            + "); deshalb kein N-Code."
        )
    fallback_to_s1 = not codes
    if fallback_to_s1:
        codes.append("S1")
    if conflict_kind == "context" and "K1" not in codes:
        codes.append("K1")
        notes.append(f"Nebencode K1: ambivalenter Krieg-/Konfliktanker erkannt ({', '.join(matching_terms(text, CONFLICT_TERMS))}); deshalb nicht als Hauptcode verwendet.")
    if fallback_to_s1:
        notes.append(
            f"Hauptcode S1 nach Ausschlussregel: Der Treffer aus Suchkategorie {category} enthält keinen "
            "belastbaren Naturgefahren-, Präventions-, Umwelt-, Konflikt- oder menschengemachten Gefahrenanker."
        )
    unique: list[str] = []
    for code in codes:
        if code not in unique:
            unique.append(code)
    omitted = unique[3:]
    if omitted:
        notes.append(
            "Zusätzliche belastbar erkannte Codes ohne freies Codefeld: "
            + ", ".join(omitted)
            + ". Hauptcode und zwei Nebencodes sind bereits belegt."
        )
    unique.extend(["", ""])
    return unique[0], unique[1], unique[2], notes


def infer_event_relation(
    main: str,
    window_type: str,
    space: str,
    text: str,
    occurrence_date: date | None,
    pub_date: date | None,
    event_start: date | None,
    event_end: date | None,
    secondary1: str = "",
    secondary2: str = "",
    date_from: date | None = None,
    date_to: date | None = None,
) -> str:
    codes = {main, secondary1, secondary2}
    natural_codes = codes & {"N1", "N2", "N3"}
    if not natural_codes:
        if main in {"S1", "W1"}:
            return "kein Bezug"
        if main in {"K1", "U1", "M1", "M2", "O1", "UN"}:
            return "unklar"
    if main == "UN":
        return "unklar"
    effective_n = main if main in {"N1", "N2", "N3"} else (
        "N1" if "N1" in natural_codes else "N2" if "N2" in natural_codes else "N3"
    )
    effective_date = occurrence_date or pub_date
    if window_type in {"anniversary_1", "anniversary_5", "anniversary_10"}:
        retrospective = contains_any(text, [
            "jahrestag*", "jährt sich", "jaehrt sich", "vor einem jahr", "vor fünf jahren",
            "vor fuenf jahren", "vor zehn jahren", "damals", "erinnerung*", "rückblick*",
            "rueckblick*",
        ])
        original_year = str(event_start.year) if event_start else ""
        if retrospective or (original_year and contains_term(text, original_year)):
            return "direkt" if effective_n == "N1" and space in {"lokal", "regional", "Schweiz"} else "indirekt"
        return "unklar"
    if not event_start or not event_end or not effective_date:
        return "unklar"
    delta = (effective_date - event_end).days
    in_primary_window = (
        window_type == "primary"
        and (not date_from or effective_date >= date_from)
        and (not date_to or effective_date <= date_to)
    )
    if effective_n == "N1":
        if -7 <= delta <= 7:
            return "direkt"
        if in_primary_window or -21 <= delta <= 21:
            return "indirekt"
        return "unklar"
    if effective_n == "N2":
        # An N2 article is normally spatially related only indirectly. A
        # secondary N1 permits a direct relation when it is also temporally close.
        if "N1" in natural_codes and -7 <= delta <= 7:
            return "direkt"
        if in_primary_window or -21 <= delta <= 21:
            return "indirekt"
        return "unklar"
    if effective_n == "N3":
        if in_primary_window or -21 <= delta <= 21:
            return "indirekt"
        return "unklar"
    return "unklar"


def infer_relevance(main: str, event_relation: str, space: str, actuality: int) -> int:
    if main in {"S1", "W1", "K1", "U1", "M1", "M2", "O1"}:
        return 0
    if main == "UN":
        return 1
    if main == "N1" and event_relation == "direkt" and space in {"lokal", "regional"}:
        return 5
    if main == "N1":
        return 4 if event_relation in {"direkt", "indirekt"} else 2
    if main == "N3":
        return 4 if event_relation == "indirekt" and actuality >= 4 else 3
    if main == "N2":
        return 2 if event_relation in {"direkt", "indirekt"} else 1
    return 0


def infer_phase(
    text: str,
    main: str,
    window_type: str,
    event_relation: str,
    pub_date: date | None,
    occurrence_date: date | None,
    event_start: date | None,
    event_end: date | None,
    phase_scheme: str = "legacy_v1",
) -> str:
    if phase_scheme == "functional_v2":
        if main not in {"N1", "N2", "N3"}:
            return "keine"

        evidence = {
            "Vorsorge/Prävention": set(matching_terms(text, PHASE_PREVENTION_TERMS)),
            "Warnung/akute Kommunikation": set(matching_terms(text, PHASE_WARNING_TERMS)),
            "Bewältigung": set(matching_terms(text, PHASE_RESPONSE_TERMS)),
            "Regeneration/Wiederaufbau": set(matching_terms(text, PHASE_RECOVERY_TERMS)),
            "Erinnerung/Rückblick": set(matching_terms(text, RETROSPECTIVE_TERMS)),
        }
        scores = {label: len(terms) for label, terms in evidence.items() if terms}
        if scores:
            highest = max(scores.values())
            strongest = [label for label, score in scores.items() if score == highest]
            if len(strongest) == 1:
                return strongest[0]
            return "unklar/nachcodieren"
        if (
            window_type in {"anniversary_1", "anniversary_5", "anniversary_10"}
            and event_relation in {"direkt", "indirekt"}
        ):
            return "Erinnerung/Rückblick"
        return "unklar/nachcodieren"

    if phase_scheme != "legacy_v1":
        raise ValueError(
            f"Unbekanntes Phasenschema '{phase_scheme}'. "
            "Verfügbar: functional_v2, legacy_v1"
        )
    if contains_any(text, ["risikomanagement", "gefahrenkarte", "schutzbau", "renaturierung"]):
        return "Risikomanagement"
    if contains_any(text, PREVENTION_TERMS):
        return "Prävention"
    if window_type in {"anniversary_1", "anniversary_5", "anniversary_10"} and event_relation in {"direkt", "indirekt"}:
        return "Erinnerung/Rückblick"
    if main not in {"N1", "N2", "N3"} or event_relation in {"kein Bezug", "unklar"}:
        return "keine"
    effective_date = occurrence_date or pub_date
    if effective_date and event_start and effective_date < event_start:
        return "unklar"
    if effective_date and event_start and event_end and event_start <= effective_date <= event_end:
        return "Ereignis/Akut"
    if effective_date and event_end and effective_date > event_end:
        return "Nachlauf"
    return "unklar"


def infer_news_proximity(text: str, space: str) -> int:
    if space == "lokal":
        return 5
    if space == "regional":
        return 4
    if space in {"Schweiz", "Schweiz sowie Ausland"}:
        return 3
    if contains_any(text, NEAR_FOREIGN):
        return 2
    if contains_any(text, EUROPE_FOREIGN):
        return 1
    return 0


def infer_news_damage(text: str, main: str, space: str) -> int:
    if not contains_any(text, DAMAGE_TERMS):
        return 0
    if main == "N1" and space in {"lokal", "regional"}:
        return 5
    if main == "N1":
        return 4
    if main == "N2":
        return 3
    if space in {"Schweiz", "Schweiz sowie Ausland"}:
        return 2
    return 1


def infer_news_conflict(
    text: str,
    main: str,
    secondary1: str,
    secondary2: str,
    space: str,
) -> int:
    conflict_kind = conflict_reference_kind(text)
    has_k1 = "K1" in {main, secondary1, secondary2}
    if not conflict_kind:
        return 1 if has_k1 else 0
    if conflict_kind == "context":
        return 1
    if main in {"N1", "N3"} and space in {"lokal", "regional"}:
        return 5
    if main in {"N1", "N3"}:
        return 4
    if main == "N2":
        return 3
    return 1


def infer_actuality(
    pub_date: date | None,
    occurrence_date: date | None,
    event_start: date | None,
    event_end: date | None,
    window_type: str,
    main: str,
    event_relation: str,
) -> int:
    # Aktualität beschreibt die zeitliche Nähe zum untersuchten Ereignis und
    # wird deshalb unabhängig vom fachlichen Hauptcode und Ereignisbezug
    # berechnet. Die Parameter bleiben aus Kompatibilitätsgründen Teil der API.
    _ = (main, event_relation)
    if window_type == "anniversary_1":
        return 1
    if window_type in {"anniversary_5", "anniversary_10"}:
        return 0
    effective_date = occurrence_date or pub_date
    if not effective_date or not event_start or not event_end:
        return 0
    days = (effective_date - event_end).days
    if event_start <= effective_date <= event_end or days == 1:
        return 5
    if 2 <= days <= 7:
        return 4
    if 8 <= days <= 14:
        return 3
    if 15 <= days <= 21:
        return 2
    if -7 <= (effective_date - event_start).days < 0:
        return 4
    return 0


def infer_frame_details(text: str, main: str) -> tuple[str, list[str], str]:
    if main == "K1":
        terms = matching_terms(text, CONFLICT_TERMS)
        return "Krieg/Militär", terms, "Hauptcode K1 bestimmt das Deutungsmuster"
    solidarity_terms = ["spenden", "liebesgaben", "hilfskomitee", "sammlung", "solidarität", "solidaritat"]
    if contains_any(text, solidarity_terms):
        return "Spenden/Solidarität", matching_terms(text, solidarity_terms), "Solidaritätsanker in Titel/Snippet/Volltext"
    divine_terms = ["gott", "gottes", "strafe", "heimsuchung"]
    if contains_any(text, divine_terms):
        return "göttliche Prüfung", matching_terms(text, divine_terms), "religiöser Deutungsanker in Titel/Snippet/Volltext"
    hazard_context = main in {"N1", "N2", "N3", "M1", "M2"} or (
        main == "UN" and contains_any(text, HAZARD_TERMS + PREVENTION_TERMS)
    )
    if hazard_context and contains_any(text, SOCIAL_HARDSHIP_TERMS):
        return (
            "soziale Not",
            matching_terms(text, SOCIAL_HARDSHIP_TERMS),
            "expliziter sozialer Folgenanker bei erkannter Naturgefahr oder menschengemachter Gefahr",
        )
    if contains_any(text, POLITICAL_RESPONSIBILITY_TERMS):
        return "politische Verantwortung", matching_terms(text, POLITICAL_RESPONSIBILITY_TERMS), "Anker für politische Verantwortung"
    technical_terms = [
        "hochwasserschutz*", "schutzbau*", "wasserbau*", "wehr", "wehre", "schleuse*",
        "damm", "dämme", "daemme", "pegel regulierung", "pegelregulierung",
        "melioration*", "juragewässerkorrektion*", "juragewaesserkorrektion*",
        "frühwarnung*", "fruehwarnung*", "evakuation*", "evakuierung*",
    ]
    if contains_any(text, technical_terms):
        return "technische Sicherheit", matching_terms(text, technical_terms), "technischer Schutz-/Regulierungsanker"
    if contains_any(text, ENV_TERMS):
        return "Umwelt/Klima", matching_terms(text, ENV_TERMS), "Umwelt-/Klimaanker"
    residual_terms = ["restrisiko*", "gefahr bleibt", "nicht auszuschliessen", "nicht ausgeschlossen"]
    if contains_any(text, residual_terms):
        return "Restrisiko", matching_terms(text, residual_terms), "Restrisikoanker"
    war_terms = ["krieg", "militär", "militar"]
    if contains_any(text, war_terms):
        return "Krieg/Militär", matching_terms(text, war_terms), "Krieg-/Militäranker"
    return "thematisch neutral", [], "kein Anker für ein spezifisches Deutungsmuster"


def infer_frame(text: str, main: str) -> str:
    return infer_frame_details(text, main)[0]


def infer_segmentation(record: dict[str, Any], matched_term: str, title: str, snippet: str, article_text: str) -> str:
    if safe_int(record.get("matchedTermCount")) > 1:
        return "Mehrfachtreffer"
    if clean(record.get("columnError")).lower() in {"1", "true", "yes", "ja"}:
        return "Spaltenfehler"
    combined_body = f"{snippet} {article_text}"
    if matched_term and contains_term(title, matched_term) and not contains_term(combined_body, matched_term):
        return "Überschrift erkannt"
    if contains_any(combined_body, [
        "fortsetzung auf seite", "fortsetzung folgt", "schluss folgt", "fortsetzung von seite",
        "wird fortgesetzt", "schluß folgt", "schluss auf seite",
    ]):
        return "Artikel geteilt"

    explicit_problem = clean(
        record.get("segmentationProblem") or record.get("segmentationIssue")
    )
    if explicit_problem:
        known_values = {
            "keines": "keines",
            "artikel geteilt": "Artikel geteilt",
            "mehrfachtreffer": "Mehrfachtreffer",
            "überschrift erkannt": "Überschrift erkannt",
            "spaltenfehler": "Spaltenfehler",
            "unklar": "unklar",
        }
        return known_values.get(explicit_problem.lower(), "unklar")

    issue_detected = clean(
        record.get("segmentationIssueDetected") or record.get("segmentationError")
    ).lower()
    if issue_detected in {"1", "true", "yes", "ja"}:
        return "unklar"

    detail_error = clean(record.get("detailError"))
    segmentation_checked = clean(record.get("segmentationChecked")).lower() in {
        "1", "true", "yes", "ja",
    }
    detail_available = bool(article_text) and not detail_error
    if segmentation_checked or (
        detail_available
        and (not matched_term or contains_term(combined_body, matched_term))
    ):
        return "keines"
    return ""


def evidence_location(terms: list[str], title: str, snippet: str, article_text: str) -> str:
    locations: list[str] = []
    for label, value in [("Titel", title), ("Snippet", snippet), ("AI-Volltext", article_text)]:
        found = matching_terms(value, terms)
        if found:
            locations.append(f"{label}: {', '.join(dict.fromkeys(found))}")
    return "; ".join(locations)


def space_explanation(
    text: str,
    newspaper: str,
    space: str,
    title: str = "",
    rubric: str = "",
) -> str:
    matches = space_anchor_matches(text, newspaper, title, rubric)
    evidence: list[str] = []
    if matches["local"]:
        evidence.append("lokaler Raumanker: " + ", ".join(dict.fromkeys(matches["local"])))
    if matches["regional"]:
        evidence.append("regionaler Raumanker: " + ", ".join(dict.fromkeys(matches["regional"])))
    if matches["water_local"]:
        evidence.append(
            "lokaler Schweizer Gewässeranker: "
            + ", ".join(dict.fromkeys(matches["water_local"]))
        )
    if matches["water_regional"]:
        evidence.append(
            "regionaler Schweizer Gewässeranker: "
            + ", ".join(dict.fromkeys(matches["water_regional"]))
        )

    swiss_aliases = matching_place_aliases(text, SWISS_PLACE_OCR_ALIASES)
    foreign_aliases = matching_place_aliases(text, FOREIGN_PLACE_ALIASES)
    if swiss_aliases:
        evidence.append("Schweizer Ortsanker: " + ", ".join(swiss_aliases))
    if foreign_aliases:
        evidence.append("ausländischer Ortsanker: " + ", ".join(foreign_aliases))

    swiss_alias_norms = {norm(term) for term in SWISS_PLACE_OCR_TERMS}
    foreign_alias_norms = {norm(term) for term in FOREIGN_PLACE_ALIAS_TERMS}
    water_norms = {norm(term) for term in matches["swiss_water"]}
    swiss_strong = [
        term for term in matches["swiss_strong"]
        if norm(term) not in swiss_alias_norms and norm(term) not in water_norms
    ]
    foreign_strong = [term for term in matches["foreign_strong"] if norm(term) not in foreign_alias_norms]
    if swiss_strong:
        evidence.append("Schweiz-Anker: " + ", ".join(dict.fromkeys(swiss_strong)))
    if matches["swiss_water"]:
        evidence.append(
            "Schweizer Gewässeranker: "
            + ", ".join(dict.fromkeys(matches["swiss_water"]))
        )
    if matches["swiss_national_address"]:
        evidence.append(
            "eindeutige Schweizer Anredeform: "
            + ", ".join(dict.fromkeys(matches["swiss_national_address"]))
        )
    if matches["swiss_jura_context"]:
        evidence.append(
            "Schweizer Jura-Kontext: "
            + ", ".join(dict.fromkeys(matches["swiss_jura_context"]))
        )
    if foreign_strong:
        evidence.append("Ausland-Anker: " + ", ".join(dict.fromkeys(foreign_strong)))
    if matches["swiss_context"]:
        evidence.append(
            "mehrdeutiger Schweizer Ort mit Ortskontext: "
            + ", ".join(dict.fromkeys(matches["swiss_context"]))
        )
    if matches["foreign_context"]:
        evidence.append(
            "mehrdeutiger ausländischer Ort mit Ortskontext: "
            + ", ".join(dict.fromkeys(matches["foreign_context"]))
        )
    if matches["swiss_formula_detail"]:
        evidence.append(
            "besonders gewichtete Schweizer Ortsformel: "
            + ", ".join(matches["swiss_formula_detail"])
        )
    if matches["foreign_formula_detail"]:
        evidence.append(
            "besonders gewichtete ausländische Ortsformel: "
            + ", ".join(matches["foreign_formula_detail"])
        )
    if matches["swiss_fuzzy_detail"]:
        evidence.append(
            "kontextgebundene Schweizer OCR-Ortskorrektur: "
            + ", ".join(matches["swiss_fuzzy_detail"])
        )
    if matches["foreign_fuzzy_detail"]:
        evidence.append(
            "kontextgebundene ausländische OCR-Ortskorrektur: "
            + ", ".join(matches["foreign_fuzzy_detail"])
        )
    if matches["support_only"]:
        evidence.append(
            "nur zusammen mit weiterem Raumanker auswertbarer Ortsbegriff: "
            + ", ".join(dict.fromkeys(matches["support_only"]))
        )
    unresolved_transboundary = [
        term
        for term in matches["transboundary"]
        if not (norm(term) == "jura" and matches["swiss_jura_context"])
    ]
    if unresolved_transboundary:
        evidence.append(
            "grenzüberschreitender Raumbegriff: "
            + ", ".join(dict.fromkeys(unresolved_transboundary))
        )
    if space in {"Schweiz", "Schweiz sowie Ausland"} and matches["rubric_swiss"]:
        evidence.append(
            "struktureller Schweiz-Anker (Rubrik): "
            + ", ".join(dict.fromkeys(matches["rubric_swiss"]))
        )
    if space in {"Ausland", "Schweiz sowie Ausland"} and matches["rubric_foreign"]:
        evidence.append(
            "struktureller Ausland-Anker (Rubrik): "
            + ", ".join(dict.fromkeys(matches["rubric_foreign"]))
        )
    if space == "unklar" and (
        matches["ambiguous_raw"] or matches["support_only"] or matches["transboundary"]
        or matches["fuzzy_ambiguous"]
    ):
        unresolved = list(dict.fromkeys(
            matches["ambiguous_raw"] + matches["support_only"] + matches["transboundary"]
            + matches["fuzzy_ambiguous"]
        ))
        return (
            "Raumbezug unklar: mehrdeutiger oder grenzüberschreitender Ortsbegriff erkannt "
            f"({', '.join(unresolved)}), aber kein ausreichender Orts-, Kantons- oder Länderkontext."
        )
    if evidence:
        return f"Raumbezug {space}: " + "; ".join(evidence) + "."
    return "Raumbezug unklar: In Titel/Snippet/Volltext oder Rubrik wurde kein belastbarer lokaler, regionaler, schweizerischer oder ausländischer Raumanker gefunden."


def temporal_explanation(
    main: str,
    event_relation: str,
    occurrence_date: date | None,
    pub_date: date | None,
    event_start: date | None,
    event_end: date | None,
    date_from: date | None,
    date_to: date | None,
    window_type: str,
) -> str:
    """Explain temporal evidence without inventing missing date boundaries."""
    effective_date = occurrence_date or pub_date
    if not effective_date:
        return (
            f"Ereignisbezug {event_relation}: Weder Ereignis- noch Ausgabedatum ist "
            "für einen belastbaren Zeitvergleich vorhanden."
        )

    date_basis = (
        f"Das aus dem Text erkannte Ereignisdatum {effective_date.strftime('%d.%m.%Y')}"
        if occurrence_date
        else f"Das Ausgabedatum {effective_date.strftime('%d.%m.%Y')} als zeitlicher Näherungswert"
    )
    window_labels = {
        "primary": "primären Suchfensters (Hauptuntersuchungszeitraum / Primärmedienzyklus)",
        "anniversary_1": "1-Jahres-Vergleichsfensters",
        "anniversary_5": "5-Jahres-Vergleichsfensters",
        "anniversary_10": "10-Jahres-Vergleichsfensters",
    }
    window_label = window_labels.get(window_type, "hinterlegten Suchfensters")

    statements: list[str] = []
    if date_from and date_to:
        position = "innerhalb" if date_from <= effective_date <= date_to else "außerhalb"
        statements.append(
            f"{date_basis} liegt {position} des {window_label} vom "
            f"{date_from.strftime('%d.%m.%Y')} bis {date_to.strftime('%d.%m.%Y')}."
        )
    else:
        statements.append(
            f"Für {date_basis[4:].lower()} ist kein vollständiges Suchfenster hinterlegt; "
            "deshalb wird kein zeitlicher Fenstertreffer behauptet."
        )

    if event_start and event_end:
        core = (
            f"Ereigniskern vom {event_start.strftime('%d.%m.%Y')} bis "
            f"{event_end.strftime('%d.%m.%Y')}"
        )
        if event_start <= effective_date <= event_end:
            statements.append(f"Das Datum liegt zugleich innerhalb des {core}." )
        elif effective_date > event_end:
            days = (effective_date - event_end).days
            statements.append(
                f"Das Datum liegt {days} Tag{'e' if days != 1 else ''} nach dem {core}."
            )
        else:
            days = (event_start - effective_date).days
            statements.append(
                f"Das Datum liegt {days} Tag{'e' if days != 1 else ''} vor dem {core}."
            )

    in_window = bool(date_from and date_to and date_from <= effective_date <= date_to)
    if window_type == "primary" and in_window:
        if main in {"N1", "N2", "N3"}:
            statements.append(
                "Konsequenz für die Vorcodierung: Die zeitliche Voraussetzung der Regeln "
                "für den Primärmedienzyklus ist erfüllt; Naturgefahren- und Raumevidenz "
                f"bestimmen zusätzlich den Hauptcode und den Ereignisbezug {event_relation}."
            )
        elif main == "UN":
            statements.append(
                "Konsequenz für die Vorcodierung: Die zeitliche Voraussetzung der Regeln "
                "für den Primärmedienzyklus ist erfüllt. Ohne eindeutige Naturgefahren- und "
                "Raumevidenz reicht die zeitliche Lage allein jedoch nicht für N1 oder N2; "
                "der Ereignisbezug bleibt unklar."
            )
        else:
            statements.append(
                "Konsequenz für die Vorcodierung: Die zeitliche Voraussetzung des "
                "Primärmedienzyklus ist erfüllt, erzeugt allein aber keinen Naturgefahren- "
                "oder Raumcode."
            )
    elif date_from and date_to:
        statements.append(
            f"Konsequenz für die Vorcodierung: Der zeitliche Befund wird beim "
            f"Ereignisbezug {event_relation} berücksichtigt, entscheidet den Hauptcode "
            "aber nicht ohne inhaltliche Naturgefahren- und Raumevidenz."
        )
    else:
        statements.append(
            f"Konsequenz für die Vorcodierung: Der Ereignisbezug {event_relation} kann "
            "aus den fehlenden Fenstergrenzen zeitlich nicht weiter gestützt werden."
        )
    return " ".join(statements)


def auto_code(
    record: dict[str, Any],
    duplicate_id: str,
    phase_scheme: str = "legacy_v1",
) -> dict[str, Any]:
    title = clean(record.get("title"))
    snippet = clean(record.get("snippet"))
    article_text = clean(record.get("articleText"))
    article_evidence = clean(record.get("articleEvidenceText"))
    evidence_source_count = safe_int(record.get("articleEvidenceSourceCount"), 1)
    newspaper = clean(record.get("newspaperExcelCode"))
    text = clean(
        f"{title} {strip_capture_boilerplate(snippet, newspaper)} "
        f"{article_text} {article_evidence}"
    )
    category = clean(record.get("category"))
    supplied_rubric = clean(record.get("rubric"))
    inferred_title_rubric = structural_rubric_from_title(title)
    rubric = clean(f"{supplied_rubric} {inferred_title_rubric}")
    window_type = clean(record.get("windowType"))
    pub_date = parse_iso(record.get("issueDate"))
    event_start = parse_iso(record.get("eventStart"))
    event_end = parse_iso(record.get("eventEnd"))
    date_from = parse_iso(record.get("dateFrom"))
    date_to = parse_iso(record.get("dateTo"))
    occurrence_date = infer_occurrence_date(text, pub_date, date_from, date_to)
    space = infer_space(text, newspaper, title, rubric)
    incomplete_evidence = evidence_is_incomplete(
        title,
        snippet,
        article_text,
        article_evidence,
        evidence_source_count,
    )
    hazard_evidence = natural_hazard_evidence(
        text,
        title,
        occurrence_date,
        event_start,
        event_end,
        pub_date,
        window_type,
    )
    main, secondary1, secondary2, notes = infer_codes(
        text,
        category,
        space,
        rubric,
        title=title,
        occurrence_date=occurrence_date,
        event_start=event_start,
        event_end=event_end,
        pub_date=pub_date,
        window_type=window_type,
        evidence_incomplete=incomplete_evidence,
        hazard_evidence=hazard_evidence,
    )
    event_relation = infer_event_relation(
        main,
        window_type,
        space,
        text,
        occurrence_date,
        pub_date,
        event_start,
        event_end,
        secondary1,
        secondary2,
        date_from,
        date_to,
    )
    actuality = infer_actuality(
        pub_date,
        occurrence_date,
        event_start,
        event_end,
        window_type,
        main,
        event_relation,
    )
    relevance = infer_relevance(main, event_relation, space, actuality)
    phase = infer_phase(
        text,
        main,
        window_type,
        event_relation,
        pub_date,
        occurrence_date,
        event_start,
        event_end,
        phase_scheme=phase_scheme,
    )
    frame, frame_terms, frame_rule = infer_frame_details(text, main)
    matched_term = clean(record.get("matchedTerm"))
    segmentation = infer_segmentation(record, matched_term, title, snippet, article_text)
    reason_codes = ", ".join(code for code in [main, secondary1, secondary2] if code)
    remarks: list[str] = []
    if matched_term:
        location = evidence_location([matched_term], title, snippet, article_text)
        remarks.append(
            f"Suchtreffer: Begriff '{matched_term}' aus Kategorie {category}"
            + (f" erkannt ({location})." if location else "; genaue Fundstelle im Capture nicht rekonstruierbar.")
        )
    remarks.extend(notes)
    un_cause = uncertainty_cause(main, space, hazard_evidence, incomplete_evidence)
    if un_cause:
        remarks.append(f"UN-Ursache: {un_cause}.")
    if evidence_source_count > 1:
        remarks.append(
            f"Artikelweise Evidenzzusammenführung: {evidence_source_count} unterschiedliche "
            "Trefferfassungen derselben stabilen ENPA-Artikel-ID wurden gemeinsam ausgewertet. "
            "Dies ist Artikel-Evidenz; das Feld 'Dublette zu ID' wird separat zeilenweise geführt."
        )
    if frame_terms:
        remarks.append(
            f"Deutungsmuster {frame}: Regel '{frame_rule}' ausgelöst durch "
            f"{evidence_location(frame_terms, title, snippet, article_text) or ', '.join(frame_terms)}."
        )
    else:
        remarks.append(f"Deutungsmuster {frame}: {frame_rule}.")
    if inferred_title_rubric and not supplied_rubric:
        remarks.append(
            "Strukturelle Rubrik aus kurzer Überschrift erschlossen: "
            f"'{inferred_title_rubric}'."
        )
    remarks.append(space_explanation(text, newspaper, space, title, rubric))
    remarks.append(
        temporal_explanation(
            main,
            event_relation,
            occurrence_date,
            pub_date,
            event_start,
            event_end,
            date_from,
            date_to,
            window_type,
        )
    )
    remarks.append(
        f"Risikokommunikation/Phase {phase}: mit Phasenschema {phase_scheme} aus Hauptcode {main}, "
        f"Ereignisbezug {event_relation}, Suchfenster {window_type or 'nicht angegeben'} und "
        "erkannten Funktionsankern abgeleitet."
    )
    if segmentation:
        remarks.append(f"Segmentierungsproblem {segmentation}: anhand der im Capture vorhandenen Trefferstruktur erkannt.")
    if duplicate_id:
        remarks.append(f"Mögliche Dublette zu {duplicate_id}.")
    if main == "UN" or (main in {"N1", "N2", "N3"} and event_relation == "unklar"):
        remarks.append("Vorcodierung unklar, bitte manuell nachcodieren.")
    return {
        "Hauptcode": main,
        "Nebencode 1": secondary1,
        "Nebencode 2": secondary2,
        "Ereignisbezug": event_relation,
        "Raumbezug": space,
        "Relevanzgrad 0-5": relevance,
        "OCR-Qualität 1-5": "",
        "Segmentierungsproblem": segmentation,
        "Nachrichtenwert Nähe 0-5": infer_news_proximity(text, space),
        "Nachrichtenwert Schaden 0-5": infer_news_damage(text, main, space),
        "Nachrichtenwert Konflikt 0-5": infer_news_conflict(
            text, main, secondary1, secondary2, space
        ),
        "Nachrichtenwert Aktualität 0-5": actuality,
        "Risikokommunikation / Phase": phase,
        "Deutungsmuster": frame,
        "Kurzbegründung Codierung": (
            f"Automatische {AUTOCODING_RULE_VERSION}-Vorcodierung anhand Titel/Snippet: "
            f"{reason_codes}. {' '.join(notes)}"
        ),
        "Kontrollstatus": "nachcodieren",
        "Prüfbemerkung": " ".join(remarks),
    }


DUPLICATE_CODE_FIELDS = ("Hauptcode", "Nebencode 1", "Nebencode 2")
DUPLICATE_CONTEXT_FIELDS = (
    "Ereignisbezug",
    "Raumbezug",
    "Relevanzgrad 0-5",
    "Nachrichtenwert Nähe 0-5",
    "Nachrichtenwert Schaden 0-5",
    "Nachrichtenwert Konflikt 0-5",
    "Nachrichtenwert Aktualität 0-5",
    "Risikokommunikation / Phase",
    "Deutungsmuster",
)
DUPLICATE_REFERENCE_FIELDS = DUPLICATE_CODE_FIELDS + DUPLICATE_CONTEXT_FIELDS + (
    "Vollartikel geprüft?",
    "Kontrollstatus",
    "Kurzbegründung Codierung",
    "Prüfbemerkung",
)
RELIABLE_DUPLICATE_CODES = {"N1", "N2", "N3", "M1", "M2", "K1", "U1", "W1", "S1", "O1"}
RELIABLE_DUPLICATE_SPACES = {"lokal", "regional", "Schweiz", "Schweiz sowie Ausland", "Ausland"}


def duplicate_reference_is_reviewed(reference: dict[str, Any]) -> bool:
    full_article = norm(reference.get("Vollartikel geprüft?"))
    control_status = norm(reference.get("Kontrollstatus"))
    return full_article in {"ja", "yes"} or control_status in {
        "gepruft",
        "kontrolliert",
        "abgeschlossen",
    }


def duplicate_reference_is_reliable(reference: dict[str, Any]) -> bool:
    # An exact ENPA article ID identifies the same article. A non-UN main code
    # is therefore sufficient for code inheritance; spatial certainty is a
    # separate analytical field and must not block duplicate alignment.
    return clean(reference.get("Hauptcode")) in RELIABLE_DUPLICATE_CODES


def duplicate_reference_score(reference: dict[str, Any]) -> tuple[int, int, int, int]:
    code = clean(reference.get("Hauptcode"))
    space = clean(reference.get("Raumbezug"))
    return (
        int(duplicate_reference_is_reviewed(reference)),
        int(duplicate_reference_is_reliable(reference)),
        int(space in RELIABLE_DUPLICATE_SPACES),
        int(code in RELIABLE_DUPLICATE_CODES),
    )


def record_id_sort_key(record_id: str) -> tuple[int, str]:
    match = RECORD_ID_RE.fullmatch(clean(record_id))
    return (int(match.group(1)), "") if match else (10**12, clean(record_id))


def duplicate_reference_from_values(values: dict[str, Any], reference_id: str) -> dict[str, Any]:
    reference = {field: values.get(field, "") for field in DUPLICATE_REFERENCE_FIELDS}
    reference["_id"] = reference_id
    return reference


def update_duplicate_reference(
    by_article: dict[str, dict[str, Any]],
    article_id: str,
    candidate: dict[str, Any],
) -> None:
    if not article_id:
        return
    current = by_article.get(article_id)
    candidate_id = clean(candidate.get("_id"))
    if current is None:
        candidate["_canonical_id"] = candidate_id
        by_article[article_id] = candidate
        return

    canonical_candidates = [
        clean(current.get("_canonical_id") or current.get("_id")),
        candidate_id,
    ]
    canonical_id = min(
        (value for value in canonical_candidates if value),
        key=record_id_sort_key,
        default="",
    )
    if duplicate_reference_score(candidate) > duplicate_reference_score(current):
        candidate["_canonical_id"] = canonical_id
        by_article[article_id] = candidate
    else:
        current["_canonical_id"] = canonical_id


def inherit_duplicate_coding(
    coded: dict[str, Any],
    reference: dict[str, Any] | None,
) -> dict[str, Any]:
    if not reference or not duplicate_reference_is_reliable(reference):
        return coded

    inherited = dict(coded)
    reviewed_reference = duplicate_reference_is_reviewed(reference)
    reference_codes = [clean(reference.get(field)) for field in DUPLICATE_CODE_FIELDS]

    for index, field in enumerate(DUPLICATE_CODE_FIELDS):
        inherited[field] = reference_codes[index] if index < len(reference_codes) else ""
    for field in DUPLICATE_CONTEXT_FIELDS:
        value = reference.get(field)
        if clean(value) or value == 0:
            inherited[field] = value

    reference_id = clean(reference.get("_id"))
    canonical_id = clean(reference.get("_canonical_id") or reference_id)
    authority = "manuell geprüften" if reviewed_reference else "automatisch vorcodierten"
    inherited["Kurzbegründung Codierung"] = (
        f"Exakte Dublette zu {canonical_id}: Artikelbezogene Codes und Analysefelder wurden an der "
        f"{authority} Referenz ausgerichtet (Hauptcode {inherited['Hauptcode']}, "
        f"Raumbezug {inherited['Raumbezug']})."
    )
    search_evidence = clean(coded.get("Prüfbemerkung")).partition(". ")[0]
    inherited["Prüfbemerkung"] = (
        (search_evidence + ". " if search_evidence else "")
        + f"Exakte Dublette anhand derselben ENPA-Artikel-ID zu {canonical_id}. "
        + (f"Die Codierungswerte stammen aus der belastbareren Referenz {reference_id}. " if reference_id != canonical_id else "")
        + f"Haupt-/Nebencodes, Ereignis- und Raumbezug, Relevanz, Nachrichtenwerte, Phase und "
        + f"Deutungsmuster wurden von der {authority} Referenz übernommen. "
        + "Suchbegriff, Suchstring, URL und OCR-Ausschnitt bleiben abfragespezifisch. "
        + "Der Prüfstatus wurde nicht übernommen; diese Trefferzeile bleibt nachzukodieren."
    )
    inherited["Kontrollstatus"] = coded.get("Kontrollstatus", "nachcodieren")
    return inherited


def article_id_from_url(url: str) -> str:
    import urllib.parse
    try:
        return urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("d", [""])[0]
    except Exception:
        return ""


def record_url(record: dict[str, Any]) -> str:
    return clean(record.get("permalink") or record.get("detailUrl") or record.get("listUrl"))


def article_id_for_record(record: dict[str, Any]) -> str:
    url = record_url(record)
    return clean(record.get("articleId")) or article_id_from_url(url) or url


def populated_coding_rows(ws, cols: dict[str, int], empty_limit: int = 200):
    """Yield the contiguous populated coding area without scanning reserved rows."""
    empty_run = 0
    max_row = min(ws.max_row or 60000, 60000)
    for row_no, row in enumerate(
        ws.iter_rows(min_row=2, max_row=max_row, values_only=True), start=2
    ):
        url = clean(row[cols["URL e-newspaperarchives"] - 1])
        term = clean(row[cols["Suchbegriff"] - 1])
        if not url and not term:
            empty_run += 1
            if empty_run >= empty_limit:
                break
            continue
        empty_run = 0
        yield row_no, row


def build_article_evidence_map(
    ws,
    cols: dict[str, int],
    incoming_records: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Collect all available title/snippet variants per stable ENPA article ID."""
    buckets: dict[str, list[str]] = {}

    def add(
        article_id: str,
        title: Any,
        snippet: Any,
        article_text: Any = "",
        newspaper: str = "",
    ) -> None:
        if not article_id:
            return
        value = clean(
            f"{clean(title)} {strip_capture_boilerplate(clean(snippet), newspaper)} "
            f"{clean(article_text)}"
        )
        if not value:
            return
        entries = buckets.setdefault(article_id, [])
        normalized = norm(value)
        if normalized and all(norm(existing) != normalized for existing in entries):
            entries.append(value)

    for _, row in populated_coding_rows(ws, cols):
        url = clean(row[cols["URL e-newspaperarchives"] - 1])
        article_id = article_id_from_url(url) or url
        add(
            article_id,
            row[cols["Artikel-/Segment-ID"] - 1],
            row[cols["OCR-Ausschnitt / Textstelle"] - 1],
            newspaper=clean(row[cols["Zeitung"] - 1]),
        )
    for record in incoming_records:
        add(
            article_id_for_record(record),
            record.get("segmentId") or record.get("title"),
            record.get("snippet"),
            record.get("articleText"),
            clean(record.get("newspaperExcelCode")),
        )
    return {
        article_id: {
            "text": " | ".join(entries),
            "sourceCount": len(entries),
        }
        for article_id, entries in buckets.items()
    }


def attach_article_evidence(
    record: dict[str, Any],
    evidence_map: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    enriched = dict(record)
    evidence = evidence_map.get(article_id_for_record(record), {})
    enriched["articleEvidenceText"] = clean(evidence.get("text"))
    enriched["articleEvidenceSourceCount"] = safe_int(evidence.get("sourceCount"), 1)
    return enriched


def first_empty_row(ws, cols: dict[str, int]) -> int:
    max_row = ws.max_row
    check_cols = [cols[name] for name in ["Falljahr", "Falltyp", "Zeitung", "URL e-newspaperarchives", "Suchkategorie A-H", "Suchbegriff"]]
    for idx, row in enumerate(ws.iter_rows(min_row=2, max_row=max_row, values_only=True), start=2):
        if not any(clean(row[col - 1]) for col in check_cols):
            return idx
    return max_row + 1


def sync_cases_sheet(wb, config: dict[str, Any]) -> None:
    sheet_name = "04_Falljahre_Korpus"
    headers = ["Name", "Ereignis", "Ereignisbeginn", "Ereignisende", "Fenster", "Von", "Bis"]
    ws = wb[sheet_name] if sheet_name in wb.sheetnames else wb.create_sheet(sheet_name)
    for col, header in enumerate(headers, start=1):
        ws.cell(1, col).value = header

    last_row = max(ws.max_row, len(config.get("queries", [])) + 1, 2)
    for row in ws.iter_rows(min_row=2, max_row=last_row, min_col=1, max_col=7):
        for cell in row:
            cell.value = None

    for row_no, query in enumerate(config.get("queries", []), start=2):
        values = [
            query.get("name", ""),
            query.get("eventName", ""),
            query.get("eventStart", ""),
            query.get("eventEnd", ""),
            query.get("windowType", ""),
            query.get("dateFrom", ""),
            query.get("dateTo", ""),
        ]
        for col, value in enumerate(values, start=1):
            cell = ws.cell(row_no, col)
            cell.value = value
            alignment = copy(cell.alignment)
            alignment.wrap_text = True
            alignment.vertical = "top"
            cell.alignment = alignment
        ws.row_dimensions[row_no].height = 32
    ws.freeze_panes = "A2"


def existing_keys(ws, cols: dict[str, int]) -> tuple[set[str], dict[str, dict[str, Any]]]:
    keys: set[str] = set()
    by_article: dict[str, dict[str, Any]] = {}
    for row_no, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        url = clean(row[cols["URL e-newspaperarchives"] - 1])
        category = clean(row[cols["Suchkategorie A-H"] - 1])
        search = clean(row[cols["Suchstring / Abfrage"] - 1])
        term = clean(row[cols["Suchbegriff"] - 1])
        if not url and not category and not term:
            continue
        article_id = article_id_from_url(url) or url
        keys.add("|".join([article_id, category, search, ""]))
        if article_id:
            values = {field: row[cols[field] - 1] for field in DUPLICATE_REFERENCE_FIELDS}
            update_duplicate_reference(
                by_article,
                article_id,
                duplicate_reference_from_values(
                    values,
                    stable_record_id(ws.cell(row_no, cols["ID"]).value, row_no),
                ),
            )
    return keys, by_article


def worksheet_row_is_human_locked(values: dict[str, Any]) -> bool:
    checked = norm(values.get("Vollartikel geprüft?")) in {
        "ja", "yes", "x", "gepruft", "1", "true",
    }
    reviewed = norm(values.get("Kontrollstatus")) in {
        "gepruft", "kontrolliert", "abgeschlossen",
    }
    return checked or reviewed or bool(clean(values.get("Codierer:in")))


def align_unreviewed_duplicate_rows(ws, cols: dict[str, int]) -> dict[str, int]:
    """Rebuild duplicate links and back-propagate reliable coding in both directions."""
    groups: dict[str, list[tuple[int, str, dict[str, Any]]]] = {}
    fields = list(dict.fromkeys(
        ["Vollartikel geprüft?", "Kontrollstatus", "Codierer:in"]
        + list(DUPLICATE_REFERENCE_FIELDS)
    ))
    for row_no, row in populated_coding_rows(ws, cols):
        url = clean(row[cols["URL e-newspaperarchives"] - 1])
        if not url:
            continue
        article_id = article_id_from_url(url) or url
        record_id = stable_record_id(ws.cell(row_no, cols["ID"]).value, row_no)
        values = {field: row[cols[field] - 1] for field in fields}
        groups.setdefault(article_id, []).append((row_no, record_id, values))

    stats = Counter()
    inherited_fields = list(dict.fromkeys(
        list(DUPLICATE_CODE_FIELDS) + list(DUPLICATE_CONTEXT_FIELDS)
        + ["Kurzbegründung Codierung", "Prüfbemerkung", "Kontrollstatus"]
    ))
    for entries in groups.values():
        duplicate_links = duplicate_links_by_id(
            record_id for _, record_id, _ in entries
        )
        canonical_id = min(
            (record_id for _, record_id, _ in entries if record_id),
            key=record_id_sort_key,
            default="",
        )
        reference_map: dict[str, dict[str, Any]] = {}
        for _, record_id, values in entries:
            update_duplicate_reference(
                reference_map,
                "article",
                duplicate_reference_from_values(values, record_id),
            )
        reference = reference_map.get("article")
        if reference:
            reference["_canonical_id"] = canonical_id

        for row_no, record_id, values in entries:
            expected_duplicate = duplicate_links.get(record_id, "")
            duplicate_cell = ws.cell(row_no, cols["Dublette zu ID"])
            if clean(duplicate_cell.value) != expected_duplicate:
                duplicate_cell.value = expected_duplicate
                stats["references_rebuilt"] += 1
            if worksheet_row_is_human_locked(values):
                stats["protected"] += 1
                continue
            if not reference or not duplicate_reference_is_reliable(reference):
                continue
            if clean(reference.get("_id")) == record_id:
                continue
            current = {field: values.get(field, "") for field in DUPLICATE_REFERENCE_FIELDS}
            inherited = inherit_duplicate_coding(current, reference)
            changed = False
            for field in inherited_fields:
                old_value = ws.cell(row_no, cols[field]).value
                new_value = inherited.get(field, old_value)
                if clean(old_value) != clean(new_value):
                    ws.cell(row_no, cols[field]).value = new_value
                    changed = True
            if changed:
                stats["rows_aligned"] += 1
    return dict(stats)


RECORD_ID_RE = re.compile(r"^T(\d+)$", re.IGNORECASE)


def format_record_id(number: int) -> str:
    return f"T{number:04d}"


def stable_record_id(value: Any, row_number: int | None = None) -> str:
    """Return a stored ID; understand legacy ROW()-based formulas during migration."""
    stored = clean(value)
    match = RECORD_ID_RE.fullmatch(stored)
    if match:
        return format_record_id(int(match.group(1)))
    if stored.startswith("=") and "ROW()" in stored.upper() and row_number is not None:
        return format_record_id(row_number - 1)
    return ""


DUPLICATE_ID_SEPARATOR = "; "


def duplicate_links_by_id(record_ids: Any) -> dict[str, str]:
    """Map every record ID to all other IDs in its exact-article group."""
    ordered_ids = sorted(
        {clean(record_id) for record_id in record_ids if clean(record_id)},
        key=record_id_sort_key,
    )
    return {
        record_id: DUPLICATE_ID_SEPARATOR.join(
            other_id for other_id in ordered_ids if other_id != record_id
        )
        for record_id in ordered_ids
    }


def next_record_id_number(ws, cols: dict[str, int]) -> int:
    highest = 0
    id_col = cols["ID"]
    for row_number in range(2, ws.max_row + 1):
        record_id = stable_record_id(ws.cell(row_number, id_col).value, row_number)
        match = RECORD_ID_RE.fullmatch(record_id)
        if match:
            highest = max(highest, int(match.group(1)))
    return highest + 1


def write_static_record_id(ws, row: int, col: int, record_id: str) -> None:
    ws.cell(row, col).value = record_id


def update_short_overview(wb, coding_ws, cols: dict[str, int]) -> None:
    ws = wb["07_Kurzübersicht"]
    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row - 1)
    for col, header in enumerate(SHORT_OVERVIEW_HEADERS, start=1):
        ws.cell(1, col).value = header
    out_row = 2
    for row_no, row in enumerate(coding_ws.iter_rows(min_row=2, values_only=True), start=2):
        if not clean(row[cols["Falljahr"] - 1]):
            continue
        for col, header in enumerate(SHORT_OVERVIEW_HEADERS, start=1):
            source_col = cols[header]
            if header == "ID":
                ws.cell(out_row, col).value = f"='01_Codierung'!A{row_no}"
            else:
                ws.cell(out_row, col).value = row[source_col - 1]
        out_row += 1
    filter_ref = f"A1:N{max(2, out_row - 1)}"
    if "KurzuebersichtDaten" in ws.tables:
        ws.auto_filter.ref = None
        table = ws.tables["KurzuebersichtDaten"]
        table.ref = filter_ref
        if table.autoFilter is None:
            table.autoFilter = AutoFilter(ref=filter_ref)
        else:
            table.autoFilter.ref = filter_ref
    else:
        ws.auto_filter.ref = filter_ref


def update_analysis_formula_bounds(
    wb,
    last_data_row: int,
    max_row: int = 60000,
    config: dict[str, Any] | None = None,
) -> None:
    """Keep analysis formulas bounded to populated rows, with a hard project cap."""
    if last_data_row > max_row:
        raise ValueError(
            f"Die Codiermatrix ist bis Excel-Zeile {max_row} begrenzt. "
            f"Der Import würde Zeile {last_data_row} benötigen."
        )
    ws = wb["05_Auswertung"]
    formula_end = max(2, last_data_row)
    source_range = re.compile(
        r"('01_Codierung'!)\$?([A-Z]+)(?:\$?\d+)?:\$?\2(?:\$?\d+)?"
    )

    def replace_range(match: re.Match[str]) -> str:
        sheet, column = match.group(1), match.group(2)
        return f"{sheet}${column}$2:${column}${formula_end}"

    for row in list(range(3, 9)) + list(range(12, 20)):
        for col in range(2, 11):
            value = ws.cell(row, col).value
            if isinstance(value, str) and value.startswith("="):
                ws.cell(row, col).value = source_range.sub(replace_range, value)

    # The bounded range starts at row 2 and therefore excludes the header.
    # Do not subtract another row as the former whole-column formulas did.
    ws["B3"] = f"=COUNTA('01_Codierung'!$B$2:$B${formula_end})"
    ws["B4"] = (
        f"=MAX(0,COUNTA('01_Codierung'!$B$2:$B${formula_end})"
        f"-COUNTIF('01_Codierung'!$W$2:$W${formula_end},\"<>\"))"
    )

    code_ranges = [
        "'01_Codierung'!$O$2:$O$" + str(formula_end),
        "'01_Codierung'!$P$2:$P$" + str(formula_end),
        "'01_Codierung'!$Q$2:$Q$" + str(formula_end),
    ]

    def code_any_expression(code: str) -> str:
        return "+".join(f'({cell_range}="{code}")' for cell_range in code_ranges)

    natural_any = "+".join(
        f'({cell_range}="{code}")'
        for cell_range in code_ranges
        for code in ("N1", "N2", "N3")
    )
    main_range = "'01_Codierung'!$O$2:$O$" + str(formula_end)
    main_nonrelevant = "+".join(
        f'({main_range}="{code}")'
        for code in ("S1", "W1", "K1", "U1", "M1", "M2")
    )
    main_unclear = "+".join(
        f'({main_range}="{code}")'
        for code in ("UN", "O1")
    )
    ws["B5"] = f"=SUMPRODUCT(--(({natural_any})>0))"
    ws["B7"] = f"=SUMPRODUCT(--(({main_nonrelevant})>0),--(({natural_any})=0))"
    ws["B8"] = f"=SUMPRODUCT(--(({main_unclear})>0),--(({natural_any})=0))"
    for row in range(12, 20):
        category_range = "'01_Codierung'!$J$2:$J$" + str(formula_end)
        category_match = f"({category_range}=A{row})"
        ws.cell(row, 3).value = f'=SUMPRODUCT(--{category_match},--(({code_any_expression("N1")})>0))'
        ws.cell(row, 4).value = f'=SUMPRODUCT(--{category_match},--(({code_any_expression("N2")})>0))'
        ws.cell(row, 5).value = f'=SUMPRODUCT(--{category_match},--(({code_any_expression("N3")})>0))'
        ws.cell(row, 10).value = (
            f'=IF(B{row}=0,0,SUMPRODUCT(--{category_match},'
            f'--(({natural_any})>0))/B{row})'
        )

    coding_ws = wb["01_Codierung"]
    coding_headers = header_map(coding_ws)
    coding_cols = {header: find_col(coding_headers, header) for header in CODING_HEADERS}
    update_compact_ranking(wb, coding_ws, coding_cols, last_data_row, config=config)
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True


def update_coding_autofilter(ws, last_data_row: int) -> None:
    """Keep Excel's header filters available after every capture import."""
    filter_end = max(2, last_data_row)
    last_header_col = max(
        (cell.column for cell in ws[1] if cell.value not in (None, "")),
        default=len(CODING_HEADERS),
    )
    filter_ref = f"A1:{openpyxl.utils.get_column_letter(last_header_col)}{filter_end}"
    if "CodierungDaten" in ws.tables:
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
    phase_scheme = clean(config.get("phaseCodingScheme") or "functional_v2")
    risk_phase_values(config)
    capture_dir = resolve_project_path(config, args.capture_dir) if args.capture_dir else resolve_config_path(config, config.get("captureDir"))
    profile, workbook, profile_spec = resolve_workbook_profile(
        config,
        args.workbook_profile,
    )
    ensure_profile_writable(config, profile)
    output_dir = resolve_config_path(config, config.get("outputDir"))
    assert capture_dir and workbook and output_dir
    prefix = clean(config.get("captureFilePrefix")) or "enpa_v2"
    pattern = args.pattern or f"{prefix}_*.json"
    records, files = read_capture_files(capture_dir, pattern)
    if not records:
        raise FileNotFoundError(f"Keine Capture-Dateien gefunden: {capture_dir / pattern}")
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"import_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    report_rows: list[dict[str, Any]] = []
    allowed_falltypen = {
        clean(value)
        for value in profile_spec.get("allowedFalltypen", [])
        if clean(value)
    }
    excluded_by_profile = 0
    if allowed_falltypen:
        selected_records = []
        for record in records:
            falltyp = clean(record.get("falltyp") or config.get("falltyp"))
            if falltyp in allowed_falltypen:
                selected_records.append(record)
            else:
                excluded_by_profile += 1
                report_rows.append(import_report_row(
                    record,
                    "ausgeschlossen",
                    f"Falltyp '{falltyp or '(leer)'}' ist für Arbeitsmappenprofil '{profile}' nicht zugelassen.",
                ))
        records = selected_records
    if not records:
        allowed = ", ".join(sorted(allowed_falltypen)) or "(keine Einschränkung)"
        write_import_report(report_path, report_rows)
        raise ValueError(
            f"Keine Captures passen zum Profil '{profile}'. "
            f"Erlaubte Falltypen: {allowed}. Report: {report_path}"
        )

    active_categories = set(expand_categories(config))
    selected_records = []
    excluded_by_search_config = 0
    for record in records:
        reason = capture_search_filter_reason(record, config, active_categories)
        if reason:
            excluded_by_search_config += 1
            report_rows.append(import_report_row(record, "ausgeschlossen", reason))
        else:
            selected_records.append(record)
    records = selected_records
    if not records:
        write_import_report(report_path, report_rows)
        raise ValueError(
            "Keine Captures entsprechen den aktuell aktivierten Kategorien und "
            f"Suchbegriffen aus config.json. Report: {report_path}"
        )
    if not workbook.exists():
        raise FileNotFoundError(
            f"Masterdatei fehlt: {workbook}. Fuehre zuerst Skripte/Build_ENPA_Master.cmd aus."
        )

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Data Validation extension is not supported.*")
        wb = openpyxl.load_workbook(workbook)
    sync_cases_sheet(wb, config)
    ws = wb["01_Codierung"]
    headers = header_map(ws)
    cols = {header: find_col(headers, header) for header in CODING_HEADERS}
    keys, by_article = existing_keys(ws, cols)
    article_evidence = build_article_evidence_map(ws, cols, records)
    next_row = first_empty_row(ws, cols)
    next_id_number = next_record_id_number(ws, cols)
    added = 0
    skipped = 0
    for record in records:
        url = record_url(record)
        article_id = clean(record.get("articleId")) or article_id_from_url(url) or url
        key = "|".join([article_id, clean(record.get("category")), clean(record.get("searchString")), ""])
        if key in keys:
            skipped += 1
            report_rows.append(import_report_row(
                record,
                "übersprungen",
                "Treffer mit identischer Artikel-, Kategorie- und Suchabfrage ist bereits importiert.",
            ))
            continue
        duplicate_reference = by_article.get(article_id)
        duplicate_id = clean(
            duplicate_reference.get("_canonical_id") or duplicate_reference.get("_id")
        ) if duplicate_reference else ""
        matched_term = infer_matched_term(record)
        record = dict(record)
        record["matchedTerm"] = matched_term
        record = attach_article_evidence(record, article_evidence)
        coded = auto_code(record, duplicate_id, phase_scheme=phase_scheme)
        coded = inherit_duplicate_coding(coded, duplicate_reference)
        row = next_row + added
        record_id = format_record_id(next_id_number + added)
        ws.row_dimensions[row].height = 28
        ws.row_dimensions[row].hidden = False
        write_static_record_id(ws, row, cols["ID"], record_id)
        values = {
            "Falljahr": parse_iso(record.get("dateFrom")).year if parse_iso(record.get("dateFrom")) else "",
            "Falltyp": clean(record.get("falltyp") or config.get("falltyp")),
            "Zeitung": clean(record.get("newspaperExcelCode")),
            "Ausgabe-Datum": ddmmyyyy(record.get("issueDate")),
            "Zeitung-Nr.": clean(record.get("issueNumber")),
            "Seite": frontend_page_value(record),
            "Artikel-/Segment-ID": clean(record.get("segmentId") or record.get("title")),
            "URL e-newspaperarchives": url,
            "Suchkategorie A-H": clean(record.get("category")),
            "Suchbegriff": matched_term,
            "Suchstring / Abfrage": clean(record.get("searchString")),
            "OCR-Ausschnitt / Textstelle": clean(record.get("snippet"))[:32000],
            "Vollartikel geprüft?": "",
            "Dublette zu ID": duplicate_id,
            "Codierer:in": "",
            "Codiert am": date.today(),
        }
        values.update(coded)
        for header, value in values.items():
            ws.cell(row, cols[header]).value = value
        for header in WRAPPED_TEXT_HEADERS:
            cell = ws.cell(row, cols[header])
            alignment = copy(cell.alignment)
            alignment.wrap_text = True
            alignment.vertical = "top"
            cell.alignment = alignment
        keys.add(key)
        update_duplicate_reference(
            by_article,
            article_id,
            duplicate_reference_from_values(values, record_id),
        )
        report_rows.append(import_report_row(
            record,
            "importiert",
            row=row,
            id=record_id,
            category=values["Suchkategorie A-H"],
            term=values["Suchbegriff"],
            main=values["Hauptcode"],
            url=url,
        ))
        added += 1

    duplicate_alignment = align_unreviewed_duplicate_rows(ws, cols)
    last_data_row = next_row + added - 1
    analysis_summary = refresh_analysis_views(wb, config)
    update_compact_ranking(wb, ws, cols, last_data_row, config=config)
    update_coding_autofilter(ws, last_data_row)
    remove_list_value(wb, "Code", "D1")
    update_coding_validations(wb, current_list_map(wb))
    write_import_report(report_path, report_rows)
    if args.dry_run:
        print(
            f"Dry-run: {added} neue Zeilen, {skipped} Duplikate uebersprungen, "
            f"{excluded_by_profile} durch Profil und {excluded_by_search_config} "
            f"durch aktuelle Suchkonfiguration ausgeschlossen, {len(files)} Dateien."
        )
        print(f"Dublettenabgleich: {duplicate_alignment}")
        print(f"Auswertungsaufbau: {analysis_summary}")
        print(f"Report: {report_path}")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = resolve_project_path(config, "Archiv/Excel_Sicherungen/Automatisch")
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f"{workbook.stem}.backup_import_{timestamp}{workbook.suffix}"
    candidate = workbook.with_name(f".{workbook.stem}.import_{timestamp}.tmp{workbook.suffix}")
    try:
        wb.save(candidate)
        duplicate_formulas = duplicate_formula_cells(candidate)
        if duplicate_formulas:
            details = ", ".join(
                f"{part}: {len(cells)}" for part, cells in duplicate_formulas.items()
            )
            raise ValueError(
                "Der Import wurde vor dem Ersetzen der Arbeitsmappe abgebrochen: "
                f"doppelte Formelknoten erkannt ({details})."
            )
        shutil.copy2(workbook, backup)
        os.replace(candidate, workbook)
        print(f"Dublettenabgleich: {duplicate_alignment}")
        print(f"Auswertungsaufbau: {analysis_summary}")
    finally:
        wb.close()
        candidate.unlink(missing_ok=True)
    print(f"Importiert: {added} neue Zeilen")
    print(f"Uebersprungen: {skipped}")
    print(f"Arbeitsmappenprofil: {profile}")
    print(f"Durch Profilfilter ausgeschlossen: {excluded_by_profile}")
    print(f"Durch Suchkonfiguration ausgeschlossen: {excluded_by_search_config}")
    print(f"Capture-Dateien: {len(files)}")
    print(f"Backup: {backup}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()

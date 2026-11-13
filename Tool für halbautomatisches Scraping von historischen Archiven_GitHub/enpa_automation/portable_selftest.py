from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import openpyxl

warnings.filterwarnings("ignore", message="Data Validation extension is not supported.*")

from enpa_common import (
    DEFAULT_CONFIG,
    downloads_dir,
    load_config,
    resolve_config_path,
    resolve_workbook_profile,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prueft die portable ENPA-Installation.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    project_root = Path(config["__project_root"])
    workbook_profiles: dict[str, str] = {}
    configured_profiles = config.get("workbookProfiles") or {}
    if configured_profiles:
        for profile_name in configured_profiles:
            _selected, profile_workbook, _spec = resolve_workbook_profile(
                config,
                profile_name,
            )
            workbook_profiles[profile_name] = str(profile_workbook)
    else:
        _selected, profile_workbook, _spec = resolve_workbook_profile(config)
        workbook_profiles["default"] = str(profile_workbook)
    output_dir = resolve_config_path(config, config.get("outputDir"))
    capture_dir = resolve_config_path(config, config.get("captureDir"))
    master_workbook = resolve_config_path(config, config.get("masterWorkbook"))
    problems: list[str] = []

    if not (project_root / "enpa_project.json").exists():
        problems.append("Projektmarker enpa_project.json fehlt.")
    for profile_name, workbook_path in workbook_profiles.items():
        if not Path(workbook_path).exists():
            problems.append(
                f"Masterdatei für Profil '{profile_name}' fehlt: {workbook_path}"
            )
            continue
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Data Validation extension is not supported.*")
            workbook = openpyxl.load_workbook(
                workbook_path,
                read_only=True,
                data_only=False,
            )
        try:
            if "09_Kompakt_Ranking" not in workbook.sheetnames:
                problems.append(
                    f"Blatt 09_Kompakt_Ranking fehlt im Profil '{profile_name}'."
                )
        finally:
            workbook.close()
    if not output_dir:
        problems.append("Ausgabeordner konnte nicht aufgeloest werden.")
    if not capture_dir:
        problems.append("Capture-Ordner konnte nicht aufgeloest werden.")
    required_master_sheets = {
        "00_Readme", "01_Codierung", "02_Codebuch", "03_Suchbegriffe",
        "04_Falljahre_Korpus", "05_Auswertung", "06_Recall_Kontrolle",
        "07_Kurzübersicht", "09_Kompakt_Ranking", "97_Auswertung_Hilfe",
        "98_Dubletten_Hilfe", "99_Listen",
    }
    if not master_workbook or not master_workbook.exists():
        problems.append(f"Leere Mastervorlage fehlt: {master_workbook}")
    else:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Data Validation extension is not supported.*")
            workbook = openpyxl.load_workbook(master_workbook, read_only=True, data_only=False)
        try:
            missing = sorted(required_master_sheets.difference(workbook.sheetnames))
            if missing:
                problems.append(
                    "Leere Mastervorlage ist unvollständig; fehlende Blätter: "
                    + ", ".join(missing)
                )
            coding = workbook["01_Codierung"]
            populated = sum(
                1 for row in coding.iter_rows(min_row=2, values_only=True)
                if any(value not in (None, "") for value in row)
            )
            if populated:
                problems.append(
                    f"Leere Mastervorlage enthält {populated} belegte Codierzeilen."
                )
        finally:
            workbook.close()

    result = {
        "python": sys.executable,
        "openpyxl": openpyxl.__version__,
        "projectRoot": str(project_root),
        "config": str(Path(args.config).resolve()),
        "workbookProfiles": workbook_profiles,
        "outputDir": str(output_dir),
        "captureDir": str(capture_dir),
        "masterWorkbook": str(master_workbook),
        "detectedDownloads": str(downloads_dir()),
        "status": "OK" if not problems else "FEHLER",
        "problems": problems,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

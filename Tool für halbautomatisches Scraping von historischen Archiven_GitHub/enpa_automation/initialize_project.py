"""Create a missing own research workbook; existing files are never overwritten."""
from pathlib import Path
import argparse

from build_master import build_workbook
from enpa_common import DEFAULT_CONFIG, load_config, resolve_workbook_profile
from import_captures import ensure_profile_writable

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default=str(DEFAULT_CONFIG))
    args=parser.parse_args()
    config=load_config(args.config)
    profile,path,_spec=resolve_workbook_profile(config)
    ensure_profile_writable(config,profile)
    if path.name.casefold()=='master_codiermatrix_leer.xlsx':
        raise ValueError('Vorlage vor der Forschung unter einem eigenen Dateinamen speichern.')
    if path.exists():
        print(f'Bestehende Forschungsdatei unverändert: {path.name}')
        return
    path.parent.mkdir(parents=True,exist_ok=True)
    wb=build_workbook(config)
    try:
        # Exclusive creation protects existing files even if another process creates one concurrently.
        with path.open('xb') as handle: wb.save(handle)
    finally: wb.close()
    print(f'Leere Forschungsdatei erstellt: {path.name}')

if __name__=='__main__': main()

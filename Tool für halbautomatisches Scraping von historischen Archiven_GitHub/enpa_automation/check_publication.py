"""Inspect publication candidates without changing any files."""
from pathlib import Path
import json
import re
import sys
import warnings
import zipfile

import openpyxl

warnings.filterwarnings('ignore',message='Data Validation extension is not supported.*')

ROOT=Path(__file__).resolve().parent.parent
GENERATED={'outputs','Archiv','Export','Sicherungen','tmp','.codex_work','Downloads','.venv','.git','__pycache__','.pytest_cache'}
FORBIDDEN_SUFFIXES={'.pdf','.doc','.docx','.pptx','.zip','.pem','.key','.pfx','.pyc'}
EMAIL=re.compile(r'[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}')
USER_PATH=re.compile(r'(?i)(?:[A-Z]:[/\\]'+'Users'+r'[/\\]|/'+'Users'+r'/|/'+'home'+r'/)[^\s"<>]+')
SECRET=re.compile(r'''(?im)(?:api[_-]?key|password|passwd|client_secret|access_token|authorization)\s*[:=]\s*["']([A-Za-z0-9_+/=-]{12,})["']''')
DEMO_NAMES=[
 'Codiermatrix_e-newspaperarchives_Naturgefahrenforschung_Kalibrierungsdaten_1851_1944_1987.xlsx',
 'Codiermatrix_e-newspaperarchives_Naturgefahrenforschung_Vergleichsdaten_ohne_Verzerrungskontext.xlsx',
]

def check():
    problems=[];count=0;size=0;max_file=0;skipped=0
    for path in ROOT.rglob('*'):
        if not path.is_file(): continue
        relative=path.relative_to(ROOT)
        if any(part in GENERATED for part in relative.parts):
            skipped+=1;continue
        if relative.parts[0]=='Arbeitsmappen' and path.name not in DEMO_NAMES+['Master_Codiermatrix_Leer.xlsx']:
            skipped+=1;continue
        count+=1;size+=path.stat().st_size;max_file=max(max_file,path.stat().st_size)
        if path.suffix.casefold() in FORBIDDEN_SUFFIXES or path.name.startswith('~$') or path.name.startswith('.env'):
            problems.append(f'Nicht vorgesehene Datei: {relative.as_posix()}')
        if path.stat().st_size>25*1024**2: problems.append(f'Datei über Browserupload-Grenze: {relative.as_posix()}')
        contents=[]
        if path.suffix.casefold()=='.xlsx':
            with zipfile.ZipFile(path) as package:
                for name in package.namelist():
                    if name.endswith(('.xml','.rels')): contents.append(package.read(name).decode('utf-8','replace'))
        elif path.suffix.casefold() in ('.py','.cmd','.json','.md','.txt','.cff') or path.name=='.gitignore':
            contents.append(path.read_text(encoding='utf-8',errors='replace'))
        for content in contents:
            if EMAIL.search(content): problems.append(f'E-Mail-Muster: {relative.as_posix()}')
            if USER_PATH.search(content): problems.append(f'Absoluter Benutzerpfad: {relative.as_posix()}')
            if SECRET.search(content): problems.append(f'Mögliche Zugangsdaten: {relative.as_posix()}')
    if size>100_000_000: problems.append('Veröffentlichungsbestand über 100 MB.')
    for name in DEMO_NAMES:
        path=ROOT/'Arbeitsmappen'/name
        if not path.exists(): problems.append(f'Beispielmatrix fehlt: {name}'); continue
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',UserWarning)
            wb=openpyxl.load_workbook(path,read_only=True,data_only=True)
        try:
            ws=wb['01_Codierung'];rows=[row for row in ws.iter_rows(min_row=2,values_only=True) if row[0]]
            if len(rows)!=100: problems.append(f'{name}: statt 100 Beispielzeilen sind {len(rows)} belegt.')
            for row in rows:
                if not str(row[8] or '').startswith('https://example.invalid/') or 'FREI ERFUNDEN' not in str(row[12]):
                    problems.append(f'{name}: Zeile nicht eindeutig synthetisch.');break
            if wb.properties.creator not in ('ENPA example generator','ENPA') or wb.properties.lastModifiedBy not in ('',None):
                problems.append(f'{name}: Personenmetadaten nicht neutral.')
        finally: wb.close()
    master=ROOT/'Arbeitsmappen/Master_Codiermatrix_Leer.xlsx'
    if master.exists():
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',UserWarning)
            wb=openpyxl.load_workbook(master,read_only=True,data_only=False)
        try:
            if any(any(value not in ('',None) for value in row) for row in wb['01_Codierung'].iter_rows(min_row=2,values_only=True)):
                problems.append('Mastervorlage enthält Codierdaten.')
        finally: wb.close()
    result={'status':'OK' if not problems else 'FEHLER','publication_files':count,'bytes':size,
            'largest_file_bytes':max_file,'generated_or_local_files_not_candidates':skipped,
            'problems':sorted(set(problems))}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__=='__main__': sys.exit(0 if check()['status']=='OK' else 1)

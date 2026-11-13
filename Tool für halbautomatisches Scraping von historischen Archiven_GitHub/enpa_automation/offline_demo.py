"""Run a reproducible offline capture/import test in a disposable project."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import openpyxl
from build_master import build_workbook
from enpa_common import load_config, search_string

ROOT=Path(__file__).resolve().parent.parent

def run(script,config,*arguments):
    env=dict(os.environ); env['PYTHONIOENCODING']='utf-8'
    env.pop('ENPA_PROJECT_DIR',None); env.pop('ENPA_CAPTURE_DIR',None)
    subprocess.run([sys.executable,str(ROOT/'enpa_automation'/script),'--config',str(config),*arguments],check=True,cwd=config.parent,env=env)

def main():
    base=load_config(ROOT/'enpa_automation/config.json')
    for key in list(base):
        if key.startswith('__'): del base[key]
    with tempfile.TemporaryDirectory(prefix='enpa-offline-demo-') as directory:
        root=Path(directory)
        (root/'enpa_project.json').write_text('{}',encoding='utf-8')
        base['workbook']='${PROJECT_DIR}/work.xlsx'
        base['masterWorkbook']='${PROJECT_DIR}/Master_Codiermatrix_Leer.xlsx'
        base['activeWorkbookProfile']='demo'
        base['readOnlyWorkbookProfiles']=[]
        base['workbookProfiles']={'demo':{'path':base['workbook'],'allowedFalltypen':['Pilotabfrage']}}
        base['captureDir']='${PROJECT_DIR}/captures'
        base['outputDir']='${PROJECT_DIR}/reports'
        base['falltyp']='Pilotabfrage'
        base['categoriesToRun']=['A','C']
        base['queries']=[{'name':'Offline synthetic example','eventName':'Fiktives Beispiel 1910',
                         'eventStart':'1910-06-14','eventEnd':'1910-06-15','windowType':'primary',
                         'dateFrom':'1910-06-14','dateTo':'1910-07-04'}]
        path=root/'config.json'; path.write_text(json.dumps(base,ensure_ascii=False),encoding='utf-8')
        wb=build_workbook(base); wb.save(root/'work.xlsx'); wb.close()
        captures=root/'captures'; captures.mkdir()
        records=[]
        for category,article,term,text in [
            ('A','DEMO-OFFLINE-0001','Hochwasser','FREI ERFUNDEN: Hochwasser in Bern beschädigte eine fiktive Brücke.'),
            ('C','DEMO-OFFLINE-0001','Dammbruch','FREI ERFUNDEN: Dammbruch in Bern beschädigte dieselbe fiktive Brücke.'),
            ('A','DEMO-OFFLINE-0002','Flut','FREI ERFUNDEN: Eine fiktive Flut in Frankreich beschädigte Häuser.'),
        ]:
            terms=base['searchCategories'][category]['terms']
            records.append({'articleId':article,'permalink':f'https://example.invalid/demo?d={article}',
                'category':category,'searchTerms':terms,'searchString':search_string(terms),'matchedTerm':term,
                'dateFrom':'1910-06-14','dateTo':'1910-07-04','issueDate':'1910-06-15',
                'falltyp':'Pilotabfrage','newspaperExcelCode':'DBU','snippet':text,'title':'FREI ERFUNDEN'})
        capture={'synthetic':True,'description':'Ausschließlich frei erfundene Testdaten','records':records}
        (captures/'enpa_v2_offline_demo.json').write_text(json.dumps(capture,ensure_ascii=False),encoding='utf-8')
        run('generate_links.py',path,'--falltyp','Pilotabfrage')
        run('import_captures.py',path)
        wb=openpyxl.load_workbook(root/'work.xlsx'); ws=wb['01_Codierung']
        assert sum(bool(row[0]) for row in ws.iter_rows(min_row=2,values_only=True))==3
        assert wb['98_Dubletten_Hilfe'].max_row==3
        ws['O2']='N3';ws['AE2']='geprüft';wb.save(root/'work.xlsx');wb.close()
        run('import_captures.py',path)
        wb=openpyxl.load_workbook(root/'work.xlsx');ws=wb['01_Codierung']
        assert sum(bool(row[0]) for row in ws.iter_rows(min_row=2,values_only=True))==3
        assert ws['O2'].value=='N3' and ws['AE2'].value=='geprüft'
        assert 'CodierungDaten' in ws.tables
        for name in ('05_Auswertung','07_Kurzübersicht','09_Kompakt_Ranking','97_Auswertung_Hilfe','98_Dubletten_Hilfe'): assert name in wb.sheetnames
        wb.close()
        run('validate_master.py',path)
        run('export_search_term_relevance_data.py',path)
        run('build_search_term_relevance_workbook.py',path,
            '--input','reports/auswertung_suchbegriffe_relevanz_data.json',
            '--output','analysis.xlsx')
        assert (root/'analysis.xlsx').exists()
        print('OFFLINE_DEMO_OK: drei synthetische Suchtreffer, zwei Artikel, Wiederimport ohne zusätzliche Zeilen, manuelle Testkorrektur erhalten.')

if __name__=='__main__': main()

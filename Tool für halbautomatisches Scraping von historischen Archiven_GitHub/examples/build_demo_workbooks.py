"""Reproduce synthetic demonstration workbooks without reading any research data."""
import argparse
from copy import copy, deepcopy
from datetime import date, timedelta
import json
from pathlib import Path
import sys
from openpyxl.worksheet.filters import AutoFilter
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'enpa_automation'))
from analysis_views import refresh_analysis_views
from build_master import build_workbook, MASTER_CODING_HEADERS
from compact_ranking import update_compact_ranking
from enpa_common import load_config, search_string

LABEL = 'FREI ERFUNDENE BEISPIELDATEN – kein Archivfund, keine Forschungsdaten'
NAMES = {
    'calibration': 'Codiermatrix_e-newspaperarchives_Naturgefahrenforschung_Kalibrierungsdaten_1851_1944_1987.xlsx',
    'comparison': 'Codiermatrix_e-newspaperarchives_Naturgefahrenforschung_Vergleichsdaten_ohne_Verzerrungskontext.xlsx',
}
SCENARIOS = [
    ('A','Hochwasser','N1','Fiktives Hochwasser in Bern beschädigte eine erfundene Brücke.'),
    ('A','Überschwemmung','N2','Fiktive Überschwemmung in Frankreich beschädigte erfundene Häuser.'),
    ('F','Hochwasserschutz','N3','Ein fiktiver Hochwasserschutzplan sah Schutzbauten in Bern vor.'),
    ('C','Dammbruch','N1','Fiktiver Dammbruch in Bern verursachte erfundene Sachschäden.'),
    ('G','Katastrophe','M1','Ein fiktiver technischer Unfall in Bern beschädigte eine erfundene Anlage.'),
    ('G','Katastrophe','M2','Ein fiktiver technischer Unfall in Frankreich zerstörte eine erfundene Anlage.'),
    ('G','Katastrophe','K1','Ein fiktiver Konfliktbericht verwendete Katastrophe ohne Naturgefahrenbezug.'),
    ('H','Klimawandel','U1','Ein fiktiver Umweltbericht erörterte Klimawandel ohne konkretes Naturereignis.'),
    ('B','Gewitter','W1','Ein fiktives Inserat warb mit Gewitter als Produktbezeichnung.'),
    ('E','Hilfskomitee','S1','Ein fiktives Hilfskomitee veranstaltete ein Fest ohne Naturgefahrenbezug.'),
    ('A','Hochwasser','O1','Fiktive OCR-Störung: Hochw?ss?r, Artikelkontext unleserlich.'),
    ('G','Katastrophe','UN','Fiktiver Ausschnitt: Katastrophe. Der Zusammenhang fehlte.'),
]

def demo_config(base, profile):
    config = deepcopy(base)
    years = [1851,1944,1987] if profile == 'calibration' else [1910]
    config['queries'] = []
    for year in years:
        for offset, phase, length in [(0,'primary',21),(1,'anniversary_1',7),(5,'anniversary_5',7),(10,'anniversary_10',7)]:
            start = date(year+offset,6,14)
            config['queries'].append({
                'name': f'Fiktives Beispiel {year} {phase}', 'eventName':f'Fiktives Beispiel {year}',
                'eventStart':f'{year}-06-14','eventEnd':f'{year}-06-15','windowType':phase,
                'dateFrom':start.isoformat(),'dateTo':(start+timedelta(days=length-1)).isoformat(),
            })
    return config

def save_metadata(wb, title):
    wb.properties.creator = 'ENPA example generator'
    wb.properties.lastModifiedBy = ''
    wb.properties.title = title
    wb.properties.subject = LABEL if 'Beispiel' in title else 'Leere Forschungsdatei'
    wb.properties.description = 'Keine übernommenen Zeitungstexte oder personenbezogenen Forschungsdaten.'
    wb.properties.keywords = 'ENPA, synthetic' if 'Beispiel' in title else 'ENPA, empty'
    wb.properties.company = None

def fill_demo(wb, config, profile):
    ws=wb['01_Codierung']
    cols={h:i+1 for i,h in enumerate(MASTER_CODING_HEADERS)}
    papers=['DBU','SEB','BT','NZZ']
    previous=None
    for index in range(100):
        scenario=SCENARIOS[index%len(SCENARIOS)]
        category,term,code,description=scenario
        window=config['queries'][index%len(config['queries'])]
        issue=date.fromisoformat(window['dateFrom'])+timedelta(days=index%3)
        article=f'DEMO-{profile.upper()}-{index+1:04d}'
        duplicate=index%10==9
        if duplicate:
            article=previous['article']
            issue=previous['issue']
            code=previous['code']
            paper=previous['paper']
            description=previous['description']
            window=previous['window']
        else:
            paper=papers[index%len(papers)]
        natural=code in ('N1','N2','N3')
        phase='Ereignis/Akut' if window['windowType']=='primary' else 'Erinnerung/Rückblick'
        status='ausschliessen' if index in (24,49,74,99) else 'geprüft' if index%4==0 else 'nachcodieren'
        values={
            'ID':f'T{index+1:04d}', 'Falljahr':issue.year,
            'Falltyp':'Kalibrierung' if profile=='calibration' else 'regulärer Vergleichsfall',
            'Zeitung':paper,'Ausgabe-Datum':issue, 'Zeitung-Nr.':f'DEMO-{index+1:03d}',
            'Seite':'','Artikel-/Segment-ID':article,
            'URL e-newspaperarchives':f'https://example.invalid/enpa-demo?d={article}',
            'Suchkategorie A-H':category,'Suchbegriff':term,
            'Suchstring / Abfrage':search_string(config['searchCategories'][category]['terms']),
            'OCR-Ausschnitt / Textstelle':f'{LABEL}. {description}',
            'Vollartikel geprüft?':'Nein','Hauptcode':code,'Nebencode 1':'','Nebencode 2':'',
            'Ereignisbezug':'direkt' if code in ('N1','N2') else 'indirekt' if code=='N3' else 'kein Bezug' if code not in ('UN','O1') else 'unklar',
            'Raumbezug':'Schweiz' if code in ('N1','N3','M1') else 'Ausland' if code in ('N2','M2') else 'unklar',
            'Relevanzgrad 0-5':4 if natural else 0,
            'OCR-Qualität 1-5':'', 'Segmentierungsproblem':'unklar' if code=='O1' else 'keines',
            'Dublette zu ID':f'T{index:04d}' if duplicate else '',
            'Nachrichtenwert Nähe 0-5':4 if code in ('N1','N3') else 1 if code=='N2' else 0,
            'Nachrichtenwert Schaden 0-5':3 if code in ('N1','N2','M1','M2') else 0,
            'Nachrichtenwert Konflikt 0-5':4 if code=='K1' else 0,
            'Nachrichtenwert Aktualität 0-5':3 if natural else 0,
            'Risikokommunikation / Phase':phase if natural else 'keine',
            'Deutungsmuster':'technische Sicherheit' if code=='N3' else 'thematisch neutral',
            'Kurzbegründung Codierung':'Alle Codierwerte sind zu Demonstrationszwecken frei gesetzt.',
            'Kontrollstatus':status,'Codierer:in':'Demo','Codiert am':date(2026,10,6),
            'Prüfbemerkung':'FREI ERFUNDEN. Auch geprüft ist hier nur ein Beispielstatus, kein Nachweis einer echten Vollartikelsichtung.',
            'Volltext':f'{LABEL}. {description} Dieser Text wurde ausschließlich für die Softwaredemonstration erstellt.',
        }
        for header,value in values.items():
            cell=ws.cell(index+2,cols[header]); cell.value=value
            cell.alignment=copy(ws.cell(2,cols[header]).alignment)
            cell.number_format=ws.cell(2,cols[header]).number_format
        ws.row_dimensions[index+2].height=28
        previous={'article':article,'issue':issue,'code':code,'paper':paper,'description':description,'window':window}
    ws.tables['CodierungDaten'].ref='A1:AI101'
    ws.tables['CodierungDaten'].autoFilter=AutoFilter(ref='A1:AI101')
    refresh_analysis_views(wb,config)
    update_compact_ranking(wb,ws,cols,101,config)
    if profile=='calibration':
        review=wb.create_sheet('08_Kontrollieren_Ausschliessen')
        review.append(['Kategorie','Begriff','Treffer (synthetischer Prüfstand)',
            'Relevanzquote im Beispiel (%)','Manuell überprüfen?','Ausschluss?','Begründung'])
        for category,term,_code,_description in SCENARIOS:
            if any(row[0]==category and row[1]==term for row in list(review.values)[1:]): continue
            matched=[row for row in wb['01_Codierung'].iter_rows(min_row=2,values_only=True) if row[9]==category and row[10]==term]
            relevant=sum(row[14] in ('N1','N2','N3') for row in matched)
            review.append([category,term,len(matched),100*relevant/len(matched) if matched else 0,
                'Ja','Nur Demo','FREI ERFUNDEN. Berechnung aus den 100 synthetischen Zeilen, keine historische Kalibrierungsentscheidung.'])
        review.add_table(Table(displayName='KontrollDemoDaten',ref=f'A1:G{review.max_row}',
            tableStyleInfo=TableStyleInfo(name='TableStyleMedium2',showRowStripes=True)))
        for cell in review[1]:
            cell.fill=PatternFill('solid',fgColor='4472C4');cell.font=Font(name='Arial',bold=True,color='FFFFFF')
            cell.alignment=Alignment(wrap_text=True,vertical='center')
        review.row_dimensions[1].height=52
        for column,width in zip('ABCDEFG',[14,30,24,25,22,18,72]): review.column_dimensions[column].width=width
        for row in review.iter_rows(min_row=2):
            for cell in row: cell.alignment=Alignment(wrap_text=True,vertical='top')
            review.row_dimensions[row[0].row].height=44
            row[3].number_format='0.0"%"'
    ws=wb['00_Readme']
    ws['A1']=f'ENPA Beispielmatrix {profile}'
    ws['A2']='Beispieldaten'
    ws['B2']=f'{LABEL}. Genau 100 Zeilen. Auch Daten, IDs, Texte, Codierungen und Prüfstatus sind erfunden. Historische Jahreszahlen und Zeitungskürzel dienen ausschließlich als Demonstrationsparameter.'
    ws.row_dimensions[2].height=68
    wb.active=0
    save_metadata(wb,f'ENPA Beispielmatrix {profile}')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',default=str(ROOT/'examples'/'regenerated'))
    parser.add_argument('--overwrite',action='store_true')
    args=parser.parse_args()
    output=Path(args.output_dir).resolve(); output.mkdir(parents=True,exist_ok=True)
    base=load_config(ROOT/'enpa_automation/config.json')
    for profile,name in NAMES.items():
        destination=output/name
        if destination.exists() and not args.overwrite: raise FileExistsError(destination)
        config=demo_config(base,profile)
        wb=build_workbook(config); fill_demo(wb,config,profile); wb.save(destination); wb.close()
        print(f'{profile}: 100 frei erfundene Zeilen -> {destination.name}')
    for name in ('Master_Codiermatrix_Leer.xlsx',):
        destination=output/name
        if destination.exists() and not args.overwrite: raise FileExistsError(destination)
        wb=build_workbook(base); save_metadata(wb,'ENPA leere Vorlage')
        wb.save(destination); wb.close()
        print(f'Leere Matrix -> {destination.name}')

if __name__=='__main__': main()

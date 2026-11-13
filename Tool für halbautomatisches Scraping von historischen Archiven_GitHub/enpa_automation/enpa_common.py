from __future__ import annotations

import base64
import json
import os
import re
import sys
import unicodedata
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

try:
    from .swiss_municipality_catalog import (
        CONTEXTUAL_HISTORICAL_SWISS_MUNICIPALITY_TERMS,
        CONTEXTUAL_OFFICIAL_SWISS_MUNICIPALITY_TERMS,
        HISTORICAL_SWISS_MUNICIPALITY_TERMS_BY_CANTON,
        OFFICIAL_SWISS_MUNICIPALITY_TERMS_BY_CANTON,
    )
except ImportError:
    from swiss_municipality_catalog import (
        CONTEXTUAL_HISTORICAL_SWISS_MUNICIPALITY_TERMS,
        CONTEXTUAL_OFFICIAL_SWISS_MUNICIPALITY_TERMS,
        HISTORICAL_SWISS_MUNICIPALITY_TERMS_BY_CANTON,
        OFFICIAL_SWISS_MUNICIPALITY_TERMS_BY_CANTON,
    )

try:
    from .swiss_water_catalog import (
        SWISS_WATER_CANTON_COUNT,
        SWISS_WATER_SOURCE_FILE,
        SWISS_WATER_TERMS_BY_CANTON,
        SWISS_WATER_UNIQUE_TERM_COUNT,
    )
except ImportError:
    from swiss_water_catalog import (
        SWISS_WATER_CANTON_COUNT,
        SWISS_WATER_SOURCE_FILE,
        SWISS_WATER_TERMS_BY_CANTON,
        SWISS_WATER_UNIQUE_TERM_COUNT,
    )

try:
    from .non_swiss_place_catalog import (
        CONTEXTUAL_NON_SWISS_PLACE_TERMS,
        NON_SWISS_PLACE_TERMS,
    )
except ImportError:
    from non_swiss_place_catalog import (
        CONTEXTUAL_NON_SWISS_PLACE_TERMS,
        NON_SWISS_PLACE_TERMS,
    )

BASE_URL = "https://www.e-newspaperarchives.ch/"
RESULT_PAGE_SIZE = 100
DEFAULT_CONFIG = Path(__file__).with_name("config.json")
PROJECT_MARKER = "enpa_project.json"
FALLBACK_PROJECT_ROOT = Path(__file__).resolve().parent.parent

VALID_FALLTYPEN = [
    "Kalibrierung",
    "Stresstest",
    "Kontrollfall",
    "regulärer Vergleichsfall",
    "Pilotabfrage",
]

CODING_HEADERS = [
    "ID",
    "Falljahr",
    "Falltyp",
    "Zeitung",
    "Ausgabe-Datum",
    "Zeitung-Nr.",
    "Seite",
    "Artikel-/Segment-ID",
    "URL e-newspaperarchives",
    "Suchkategorie A-H",
    "Suchbegriff",
    "Suchstring / Abfrage",
    "OCR-Ausschnitt / Textstelle",
    "Vollartikel geprüft?",
    "Hauptcode",
    "Nebencode 1",
    "Nebencode 2",
    "Ereignisbezug",
    "Raumbezug",
    "Relevanzgrad 0-5",
    "OCR-Qualität 1-5",
    "Segmentierungsproblem",
    "Dublette zu ID",
    "Nachrichtenwert Nähe 0-5",
    "Nachrichtenwert Schaden 0-5",
    "Nachrichtenwert Konflikt 0-5",
    "Nachrichtenwert Aktualität 0-5",
    "Risikokommunikation / Phase",
    "Deutungsmuster",
    "Kurzbegründung Codierung",
    "Kontrollstatus",
    "Codierer:in",
    "Codiert am",
    "Prüfbemerkung",
]

WRAPPED_TEXT_HEADERS = [
    "URL e-newspaperarchives",
    "Suchstring / Abfrage",
    "OCR-Ausschnitt / Textstelle",
    "Kurzbegründung Codierung",
    "Prüfbemerkung",
]

SHORT_OVERVIEW_HEADERS = [
    "ID",
    "Falljahr",
    "Zeitung",
    "Ausgabe-Datum",
    "Suchkategorie A-H",
    "Suchbegriff",
    "OCR-Ausschnitt / Textstelle",
    "Hauptcode",
    "Nebencode 1",
    "Nebencode 2",
    "Raumbezug",
    "Relevanzgrad 0-5",
    "Dublette zu ID",
    "Risikokommunikation / Phase",
]

CODEBOOK_ROWS = [
    ("N1", "Naturgefahr Schweiz direkt", "Artikel beschreibt ein Naturgefahrenereignis oder naturbedingtes Schadensereignis in der Schweiz."),
    ("N2", "Naturgefahr Ausland direkt", "Artikel beschreibt ein Naturgefahrenereignis oder naturbedingtes Schadensereignis im Ausland."),
    ("N3", "Indirekte Naturgefahrenkommunikation", "Artikel behandelt Prävention, Schutz, Risiko- oder Erinnerungskommunikation mit erkennbarem Naturgefahrenbezug."),
    ("M1", "Gefahr menschengemacht national", "Artikel behandelt eine menschengemachte Gefahr, einen technischen Unfall oder anthropogene Schadensursache mit nationalem bzw. schweizerischem Bezug."),
    ("M2", "Gefahr menschengemacht international", "Artikel behandelt eine menschengemachte Gefahr, einen technischen Unfall oder anthropogene Schadensursache mit internationalem bzw. ausländischem Bezug."),
    ("K1", "Krieg/Konflikt", "Treffer ist primär durch Krieg, Militär oder politischen Konflikt geprägt."),
    ("U1", "Umwelt/Klima allgemein", "Umwelt- oder Klimakommunikation ohne konkreten Naturgefahrenbezug."),
    ("W1", "Werbung/Inserat", "Anzeige, Stellenmarkt, Privatmarkt oder ähnlicher nicht-redaktioneller Kontext."),
    ("S1", "Themenfern", "Suchwort kommt vor, aber der Artikel ist thematisch nicht naturgefahrenbezogen."),
    ("O1", "OCR/Segment unklar", "Zuordnung ist wegen OCR- oder Segmentierungsproblem nicht belastbar."),
    ("UN", "Unklar", "Automatisch nicht zuverlässig entscheidbar; manuelle Prüfung nötig."),
]

LEGACY_RISK_PHASES = [
    "Risikomanagement",
    "Prävention",
    "Erinnerung/Rückblick",
    "keine",
    "Ereignis/Akut",
    "Nachlauf",
    "unklar",
]

FUNCTIONAL_RISK_PHASES = [
    "Vorsorge/Prävention",
    "Warnung/akute Kommunikation",
    "Bewältigung",
    "Regeneration/Wiederaufbau",
    "Erinnerung/Rückblick",
    "keine",
    "unklar/nachcodieren",
]

VALID_PHASE_CODING_SCHEMES = {
    "legacy_v1": LEGACY_RISK_PHASES,
    "functional_v2": FUNCTIONAL_RISK_PHASES,
}


def risk_phase_values(config: dict[str, Any] | None = None) -> list[str]:
    """Return the dropdown values for the configured phase coding scheme."""
    scheme = str((config or {}).get("phaseCodingScheme") or "functional_v2").strip()
    if scheme not in VALID_PHASE_CODING_SCHEMES:
        available = ", ".join(sorted(VALID_PHASE_CODING_SCHEMES))
        raise ValueError(
            f"Unbekanntes Phasenschema '{scheme}'. Verfügbar: {available}"
        )
    return list(VALID_PHASE_CODING_SCHEMES[scheme])


LISTS = {
    "Falltyp": VALID_FALLTYPEN,
    "Zeitung": ["SEB", "BT", "DBU", "NZZ"],
    "Suchkategorie": list("ABCDEFGH"),
    "Code": [row[0] for row in CODEBOOK_ROWS],
    "Ereignisbezug": ["direkt", "indirekt", "kein Bezug", "unklar"],
    "Raumbezug": ["lokal", "regional", "Schweiz", "Schweiz sowie Ausland", "Ausland", "unklar"],
    "Relevanz": [0, 1, 2, 3, 4, 5],
    "OCR": [1, 2, 3, 4, 5],
    "Segmentierungsproblem": ["keines", "Artikel geteilt", "Mehrfachtreffer", "Überschrift erkannt", "Spaltenfehler", "unklar"],
    "Risikophase": LEGACY_RISK_PHASES,
    "Deutungsmuster": ["thematisch neutral", "Spenden/Solidarität", "göttliche Prüfung", "Umwelt/Klima", "technische Sicherheit", "Systemvertrauen", "Restrisiko", "soziale Not", "politische Verantwortung", "Krieg/Militär"],
    "Kontrollstatus": ["nachcodieren", "geprüft", "unklar", "ausschliessen"],
    "Vollartikel geprüft": ["Ja", "Nein"],
    "Nachrichtenwert Nähe": [0, 1, 2, 3, 4, 5],
    "Nachrichtenwert Schaden": [0, 1, 2, 3, 4, 5],
    "Nachrichtenwert Konflikt": [0, 1, 2, 3, 4, 5],
    "Nachrichtenwert Aktualität": [0, 1, 2, 3, 4, 5],
}

DIRECT_NATURAL_HAZARD_TERMS = [
    "hochwasser*", "überschwemm*", "ueberschwemm*", "fluth*", "wassernot",
    "wassernoth", "hochwasserkatastroph*", "erdrutsch*", "erdschlipf*",
    "wasserverheer*", "dammbruch*", "naturkatastroph*",
    "weggeschwemmt", "verschlammt", "unter wasser",
    "sintflut*", "sinthfluth*", "sintfluth*", "blitzschlag*",
    "vom blitz erschlagen", "taifun*",
    "hurrikan*", "zyklon*", "murgang*", "bergsturz*", "lawine*",
    "wild* wasser", "wild* wogen", "reissend* strom", "vertranken", "vertrinken",
    "sturzflut*", "überflutet*", "ueberflutet*", "seit menschengedenken",
    "schwemmt*", "hülfeleistung*", "hilfeleistung*", "ununterbrochen* regenperiod*",
    "anhaltend* regenwetter*", "trat über die ufer",
    "trat ueber die ufer", "notbrücke*", "notbruecke*", "notsteg*", "sturmglocke*",
    "tobend* element*", "hülfe in der noth", "hilfe in der not", "wirbelsturm*",
    "spur der verwüstung", "spur der verwuestung", "schneise der verwüstung",
    "schneise der verwuestung", "katastrophengebiet*", "lawinenniedergang*",
    "sturmwetter*", "schneemassen*", "sturmwind*", "hundewetter*", "hundswetter*",
    "naturgewalt*", "von der aussenwelt abgeschnitten",
    "von der außenwelt abgeschnitten", "unwetterkatastroph*",
]
AMBIGUOUS_NATURAL_HAZARD_TERMS = [
    "ertrinken", "ertrank", "ertrunken", "flut", "fluten", "katastrophe", "katastrophen",
    "elementarschaden*", "umweltkatastrophe", "umweltkatastrophen",
]
AMBIGUOUS_DROWNING_TERMS = ["ertrinken", "ertrank", "ertrunken"]
WEATHER_PROCESS_TERMS = [
    "wolkenbruch*", "unwetter*", "dauerregen*", "starkregen*", "schneeschmelz*",
    "gewitter*", "niederschlag*", "sturm*", "orkan*", "hagel*", "regenflut*",
]
HAZARD_TERMS = DIRECT_NATURAL_HAZARD_TERMS + WEATHER_PROCESS_TERMS
HAUNTED_TERMS = ["heimgesucht*"]
NOTLAGE_TERMS = ["notlage*"]
RAGING_TERMS = ["wütend*", "wuetend*", "wütet*", "wuetet*"]
WEATHER_FORCE_TERMS = [
    "regen*", "sturm*", "wind*", "unwetter*", "gewitter*", "hagel*",
    "schnee*", "schneefall*", "wetter*",
]
DAMAGED_TERMS_CONDITIONAL = ["geschädigt*", "geschaedigt*"]
DAMAGED_COMPOUND_NATURAL_TERMS = [
    "brandgeschädigt*", "brandgeschaedigt*", "hochwassergeschädigt*",
    "hochwassergeschaedigt*", "wettergeschädigt*", "wettergeschaedigt*",
    "sturmgeschädigt*", "sturmgeschaedigt*", "lawinengeschädigt*",
    "lawinengeschaedigt*",
]
DAMAGED_NATURAL_CONTEXT_TERMS = HAZARD_TERMS + ["brand*", "wetter*", "schneefall*"]
WEATHER_SHIFT_TERMS = ["wetterumschlag*"]
INTENSITY_TERMS = ["heftig*", "schlimm*"]
WATER_LEVEL_TERMS = ["wasserstand*"]
WATER_LEVEL_QUALIFIERS = [
    "hoch", "hohe", "hoher", "hohen", "hohes", "höchst*", "hoechst*",
    "nie dagewesen*",
]
WATER_BODY_TERMS = [
    "bergbach*", "bach*", "fluss*", "see*", "meer*", "strom*", "gewässer*",
    "gewaesser*", "fliessgewässer*", "fliessgewaesser*", "fließgewässer*",
]
WATER_RISE_PROCESS_TERMS = [
    "anschwellen*", "anschwoll*", "angeschwollen*", "übertreten*", "uebertreten*",
    "übergetreten*", "uebergetreten*",
]
DAM_BREACH_STRUCTURE_TERMS = ["damm", "dämme", "daemme"]
DAM_BREACH_PROCESS_TERMS = [
    "durchbrochen*", "durchbrechen*", "durchbrach*", "dammbruch*",
]
SOLIDARITY_TERMS = [
    "spenden*", "liebesgaben*", "hilfskomitee*", "sammlung*", "mildthätigkeit*",
    "mildtaetigkeit*", "hülfeleistung*", "hilfeleistung*", "hülfe in der noth",
    "hilfe in der not",
]
PREVENTION_TERMS = [
    "hochwasserschutz*", "wasserbau*", "melioration*", "gefahrenkarte*",
    "renaturierung*", "schutzbau*", "risikomanagement*", "juragewässerkorrektion*",
    "juragewaesserkorrektion*", "pegel regulierung", "pegelregulierung",
    "flusskorrektion*", "uferverbauung*", "rückhaltebecken*", "rueckhaltebecken*",
]
EVACUATION_TERMS = ["evakuation*", "evakuierung*", "evakuiert*"]
RISK_COMMUNICATION_TERMS = [
    "risikokommunikation*", "risikomanagement*", "risikoanalyse*", "risikobeurteilung*",
    "gefahrenbeurteilung*", "gefahrenkarte*", "warnung*", "warnsystem*", "frühwarn*",
    "fruehwarn*", "vorsorge*", "prävention*", "praevention*", "schutzmassnahm*",
    "schutzmaßnahm*", "schutzvorkehr*", "evakuationsplan*", "notfallplan*", "alarmplan*",
]
PHASE_PREVENTION_TERMS = PREVENTION_TERMS + [
    "vorsorge*", "prävention*", "praevention*", "risikovorsorge*",
    "schutzmassnahm*", "schutzmaßnahm*", "schutzvorkehr*",
]
PHASE_WARNING_TERMS = [
    "warnung*", "warnsystem*", "frühwarn*", "fruehwarn*", "alarm*",
    "entwarnung*", "verhaltensanweisung*", "verhaltensempfehlung*",
    "pegelstand*", "hochwasserwarnung*", "evakuationswarnung*",
]
PHASE_RESPONSE_TERMS = [
    "rettung*", "gerettet*", "bergung*", "geborgen*", "nothilfe*",
    "soforthilfe*", "hilfsaktion*", "hilfeleistung*", "hülfeleistung*",
    "einsatzkräft*", "einsatzkraeft*", "feuerwehr*", "zivilschutz*",
    "evakuation*", "evakuierung*", "evakuiert*", "räumung*", "raeumung*",
    "notunterkunft*", "spendenaufruf*", "hilfskomitee*",
]
PHASE_RECOVERY_TERMS = [
    "wiederaufbau*", "wiederherstellung*", "instandstellung*", "instandsetzung*",
    "reparatur*", "aufbauarbeit*", "wiederinbetriebnahme*", "entschädigung*",
    "entschaedigung*", "schadenersatz*", "schadensersatz*",
    "versicherungsleistung*", "wiederansiedlung*",
]
RETROSPECTIVE_TERMS = [
    "jahrestag*", "jährt sich", "jaehrt sich", "vor einem jahr", "vor fünf jahren",
    "vor fuenf jahren", "vor zehn jahren", "damals", "erinnerung*", "rückblick*",
    "rueckblick*", "gedenken*", "gedenkfeier*",
]
HUMAN_MADE_HAZARD_TERMS_STRONG = [
    "chemie-katastrophe*", "chemiekatastrophe*", "brandkatastrophe*", "chemiewehr*",
    "kontaminiertes löschwasser",
    "kontaminiertes loeschwasser", "menschengemacht", "menschliches versagen",
    "falsche handhabung", "missachtete sicherheitsbestimmungen", "glimmbrände",
    "glimmbraende", "brandgefährlich", "brandgefaehrlich", "brandgefährlichkeit",
    "brandgefaehrlichkeit", "atomar", "nuklear", "zündquellen", "zuendquellen",
    "brandrisiko", "angeschuldigt", "juristische beurteilung", "reaktorkatastrophe",
    "tschernobyl", "belastetes löschwasser", "belastetes loeschwasser",
    "bodenverschmutzung*", "grundwasserverschmutzung*", "gewässerkontamination*",
    "gewaesserkontamination*", "altlastenrecht", "belasteter standort",
    "hochgiftig", "verheerender unfall", "gifte",
    "unkontrollierter austritt von giftigen und gesundheitsschädlichen substanzen",
    "unkontrollierter austritt von giftigen und gesundheitsschaedlichen substanzen",
    "gefahrengut", "explosion", "chemiebrand*", "ölunfall*", "oelunfall*", "ölverschmutzung*",
    "oelverschmutzung*", "ölaustritt*", "oelaustritt*", "gasleck",
]
HUMAN_MADE_HAZARD_TERMS_CONTEXT = [
    "unternehmen", "menschen", "transport", "pestizid*", "herbizid*",
]
HUMAN_MADE_HAZARD_TERMS = HUMAN_MADE_HAZARD_TERMS_STRONG + HUMAN_MADE_HAZARD_TERMS_CONTEXT
ENV_TERMS = [
    "umwelt*", "klima", "klimawandel*", "treibhauseffekt*", "gletscher*",
    "gewässerschutz*", "gewaesserschutz*", "klimaerwärmung*", "klimaerwaermung*",
    "ozonschicht*", "ozonloch*",
]
DAMAGE_TERMS = [
    "schaden", "schäden", "schadens*", "wasserschaden*", "zerstörung*", "zerstört*",
    "zerstort*", "verwüstung*", "verheerung*", "vernichtet*", "verwüstet*",
    "verwuestet*", "obdachlos*", "tote", "toten", "ums leben*", "verlust*",
    "todesopfer*", "todesopker*", "opfer*", "starben*", "gestorben*", "verletzt*",
    "nothleidend*", "notleidend*", "getroffen", "betroffen",
    "getreffen", "betroffen*",
    "weggerissen*", "eingestürzt*", "eingesturzt*", "überflutet*", "ueberflutet*",
]
WATER_PROCESS_CONTEXT_TERMS = [
    "pegel*", "fluss*", "bach", "bäche", "baeche", "see", "ufer*",
    "strömung*", "stroemung*", "regen*", "geregnet*", "nässe", "naesse",
    "schmelzwasser*",
]
CONFLICT_TERMS_STRONG = [
    "krieg*", "militär*", "militar*", "bewaffnet*", "kampf*", "schlacht*",
    "bombardierung*", "front", "konflikt*", "bürgerkrieg*", "buergerkrieg*",
    "bombe*", "munitionslager*", "munition*", "alliierte*", "luftoperation*",
    "offensive*", "royal air force", "r a f", "die deutschen", "nazi*",
    "granate*", "zerschoss*", "erschoss*", "erschiess*", "geschütz*",
    "geschuetz*", "granattrichter*", "orgie der zerstörung",
    "orgie der zerstoerung", "brände gelegt", "braende gelegt",
    "brandschatzung*", "ss sondergruppe*", "ss sondertrupp*", "gefangen*",
    "eisenhower", "general", "artillerie", "artilleriefeuer", "panzer",
    "zurückgeschlagen*", "zurueckgeschlagen*", "panzergrenadier*", "division*",
    "infanterie", "kampf*", "vorhut*", "nationalsozial*", "kompanie",
    "wehrmann*", "wehrmänner", "wehrmaenner",
]
CONFLICT_TERMS_CONTEXT = [
    "flüchtling*", "fluechtling*", "flüchtlingskind*", "fluechtlingskind*",
    "verlust*", "kommunis*", "faschis*", "offizier*", "interniert*",
]
CONFLICT_TERMS = list(dict.fromkeys(CONFLICT_TERMS_STRONG + CONFLICT_TERMS_CONTEXT))
POLITICAL_RESPONSIBILITY_TERMS = [
    "politische verantwortung", "verantwortlich*", "verantwortung", "vorwurf*",
    "schuldfrage*", "angeschuldigt*", "behördenversagen", "behoerdenversagen",
]

CURATED_SWISS_CITY_TERMS_BY_CANTON = {
    "ZH": [
        "zürich", "zuerich", "winterthur", "uster", "dübendorf", "duebendorf",
        "dietikon", "wetzikon", "wädenswil", "waedenswil", "horgen", "bülach",
        "buelach", "opfikon", "kloten", "schlieren", "adliswil", "volketswil",
        "regensdorf", "thalwil", "illnau effretikon", "wallisellen", "stäfa",
        "staefa", "küsnacht", "kuesnacht", "meilen", "richterswil", "zollikon",
        "rüti", "rueti", "bauma", "affoltern am albis", "pfäffikon", "pfaeffikon",
        "bassersdorf", "männedorf", "maennedorf", "hinwil", "maur", "rümlang",
        "ruemlang", "eglisau", "leimbach", "höcklergebiet", "hoecklergebiet",
    ],
    "BE": [
        "bern", "biel", "bienne", "thun", "köniz", "koeniz", "ostermundigen",
        "burgdorf", "steffisburg", "langenthal", "lyss", "muri bei bern", "spiez",
        "worb", "münchenbuchsee", "muenchenbuchsee", "belp", "moutier",
        "interlaken", "herzogenbuchsee", "utzenstorf", "ußenstorf", "ussenstorf",
        "ußenstors", "ussenstors", "ußenftorf", "ussenftorf", "atzenstorf",
        "signau", "signan", "wabern", "unterseen", "melchnau", "ringgenberg",
        "tüscherz", "tuescherz", "schifflaube", "altenberg",
    ],
    "LU": ["luzern", "lucerne", "emmen", "kriens", "ebikon", "horw", "sursee", "hochdorf"],
    "UR": ["altdorf", "amsteg", "gurtnellen", "flüelen", "flueelen"],
    "SZ": [
        "schwyz", "freienbach", "einsiedeln", "küssnacht", "kuessnacht", "arth",
        "ingenbohl", "muotatal", "muota", "brunnen",
    ],
    "OW": ["sarnen"],
    "NW": ["stans", "dallenwil", "wolfenschiessen", "wolfenschieben", "engelberger aa"],
    "GL": ["glarus", "glarus nord", "näfels", "naefels"],
    "ZG": ["stadt zug", "baar", "cham", "risch"],
    "FR": [
        "freiburg", "fribourg", "bulle", "villars sur glâne", "villars sur glane",
        "estavayer", "düdingen", "duedingen", "murten", "morat", "broc",
    ],
    "SO": ["solothurn", "olten", "grenchen", "zuchwil", "biberist"],
    "BS": ["basel", "riehen"],
    "BL": [
        "liestal", "allschwil", "reinach", "muttenz", "pratteln", "binningen",
        "münchenstein", "muenchenstein", "oberwil", "birsfelden", "aesch", "laufen",
    ],
    "SH": ["schaffhausen", "neuhausen am rheinfall"],
    "AR": ["herisau", "wolfhalden"],
    "AI": ["appenzell"],
    "SG": [
        "st gallen", "sankt gallen", "saint gall", "rapperswil jona", "wil",
        "gossau", "uzwil", "buchs", "altstätten", "altstaetten", "flawil", "rorschach",
        "straubenzell", "nesslau", "neßlau", "haag",
    ],
    "GR": ["chur", "davos", "landquart", "domat ems", "st moritz", "sankt moritz"],
    "AG": [
        "aarau", "wettingen", "baden", "wohlen", "oftringen", "rheinfelden",
        "spreitenbach", "zofingen", "brugg", "möhlin", "moehlin", "lenzburg",
        "suhr", "rothrist", "aarburg", "neuenhof", "turgi", "oberrüti",
        "oberrueti", "merenschwand", "jonen", "lunkhofen",
    ],
    "TG": [
        "frauenfeld", "kreuzlingen", "arbon", "amriswil", "weinfelden",
        "romanshorn", "kradolf", "kradols",
    ],
    "TI": ["bellinzona", "lugano", "locarno", "mendrisio", "chiasso"],
    "VD": [
        "lausanne", "yverdon les bains", "montreux", "nyon", "renens", "vevey",
        "morges", "gland", "prilly", "pully", "ecublens", "la tour de peilz",
        "bussigny", "le mont sur lausanne", "aigle", "payerne", "bex",
    ],
    "VS": [
        "sitten", "sion", "martigny", "monthey", "siders", "sierre", "brig glis",
        "naters",
    ],
    "NE": [
        "neuenburg", "neuchâtel", "neuchatel", "la chaux de fonds", "val de ruz",
        "val de travers", "le locle", "saint blaise", "st blaise", "stblaise",
    ],
    "GE": [
        "genf", "genève", "geneve", "vernier", "lancy", "meyrin", "carouge",
        "onex", "thônex", "thonex", "versoix", "chêne bougeries",
        "chene bougeries", "plan les ouates",
    ],
    "JU": ["delsberg", "delémont", "delemont", "pruntrut", "porrentruy"],
}
_CURATED_SWISS_CITY_TERMS = {
    term
    for terms in CURATED_SWISS_CITY_TERMS_BY_CANTON.values()
    for term in terms
}
SWISS_CITY_TERMS_BY_CANTON = {
    code: list(dict.fromkeys(
        CURATED_SWISS_CITY_TERMS_BY_CANTON.get(code, [])
        + OFFICIAL_SWISS_MUNICIPALITY_TERMS_BY_CANTON.get(code, [])
        + HISTORICAL_SWISS_MUNICIPALITY_TERMS_BY_CANTON.get(code, [])
    ))
    for code in dict.fromkeys(
        list(CURATED_SWISS_CITY_TERMS_BY_CANTON)
        + list(OFFICIAL_SWISS_MUNICIPALITY_TERMS_BY_CANTON)
        + list(HISTORICAL_SWISS_MUNICIPALITY_TERMS_BY_CANTON)
    )
}
# Diese Ortsnamen sind ohne weiteren Kontext nicht eindeutig schweizerisch
# (z.B. Baden in der Schweiz oder Deutschland). Sie bleiben in der
# kantonsbezogenen Referenzliste, werden aber nicht allein als Schweiz-Anker
# verwendet. Ein ausdruecklicher Kantons-/Regionsanker kann sie weiterhin
# aufloesen.
AMBIGUOUS_SWISS_PLACE_TERMS = {
    "baden", "baar", "buchs", "cham", "gland", "march", "maur", "risch",
    "riviera", "wil", "höfe", "hoefe", "brunnen", "laufen", "haag", "neuhaus",
} | (
    (
        set(CONTEXTUAL_OFFICIAL_SWISS_MUNICIPALITY_TERMS)
        | set(CONTEXTUAL_HISTORICAL_SWISS_MUNICIPALITY_TERMS)
    )
    - _CURATED_SWISS_CITY_TERMS
)
SWISS_CITY_ANCHOR_TERMS_BY_CANTON = {
    code: [term for term in terms if term not in AMBIGUOUS_SWISS_PLACE_TERMS]
    for code, terms in SWISS_CITY_TERMS_BY_CANTON.items()
}
SWISS_CITY_TERMS = list(dict.fromkeys(
    term
    for terms in SWISS_CITY_ANCHOR_TERMS_BY_CANTON.values()
    for term in terms
))

# The supplied water catalog is canton-grouped so a hit can be classified
# relative to the newspaper. A few ordinary-language homonyms need an explicit
# hydrological context; obvious transboundary names never decide Switzerland
# on their own.
CONTEXTUAL_SWISS_WATER_TERMS = {
    "alp", "asse", "biber", "giessen", "glatt", "grüene", "hall", "julia",
    "massa", "murg", "orb", "reuse", "ron", "talent", "trueb", "wiese",
}
TRANSBOUNDARY_SWISS_WATER_TERMS = {
    "lac des brenets", "rhone", "rhône", "rodano",
}
SWISS_WATER_FOREIGN_COLLISION_TERMS = {
    term
    for terms in SWISS_WATER_TERMS_BY_CANTON.values()
    for term in terms
    if term in NON_SWISS_PLACE_TERMS
}
SWISS_WATER_STRONG_TERMS_BY_CANTON = {
    code: [
        term for term in terms
        if term not in CONTEXTUAL_SWISS_WATER_TERMS
        and term not in TRANSBOUNDARY_SWISS_WATER_TERMS
    ]
    for code, terms in SWISS_WATER_TERMS_BY_CANTON.items()
}
SWISS_WATER_STRONG_TERMS = list(dict.fromkeys(
    term
    for terms in SWISS_WATER_STRONG_TERMS_BY_CANTON.values()
    for term in terms
))
SWISS_WATER_CANTONS_BY_TERM = {
    term: frozenset(
        code for code, terms in SWISS_WATER_TERMS_BY_CANTON.items() if term in terms
    )
    for term in {
        term for terms in SWISS_WATER_TERMS_BY_CANTON.values() for term in terms
    }
}
NEWSPAPER_CANTON_CODES = {"NZZ": "ZH", "DBU": "BE", "SEB": "BE", "BT": "BE"}
LOCAL_SWISS_WATER_TERMS = {
    "NZZ": {"limmat", "sihl", "zürichsee", "lac de zurich", "lago di zurigo", "schanzengraben"},
    "DBU": {"aare"},
    "SEB": {"bielersee", "lac de bienne"},
    "BT": {"bielersee", "lac de bienne"},
}

SWISS_ALTERNATIVE_TERMS = [
    "züri", "zueri", "zürichbiet*", "zuerichbiet*", "berne", "bernbiet*",
    "lucerne", "urnerland*", "schwyzerland*", "obwalderland*", "nidwalderland*",
    "glarnerland*", "zugerland*", "fribourg", "freiburgerland*", "soleure",
    "bâle ville", "bale ville", "baselstadt*", "bâle campagne", "bale campagne",
    "baselland*", "baselbiet*", "schafuuse", "appenzell rhodes extérieures",
    "appenzell rhodes exterieures", "appenzell rhodes intérieures",
    "appenzell rhodes interieures", "ausserrhoden*", "innerrhoden*", "saint gall",
    "sanktgallerland*", "grisons", "grigioni", "grischun", "bündnerland*",
    "buendnerland*", "argovie", "aargauerland*", "thurgovie", "mostindien",
    "ticino", "sottoceneri", "sopraceneri", "vaud", "waadtland*", "valais",
    "walliserland*", "neuchâtel", "neuchatel", "genève", "geneve",
]

SWISS_REGION_TERMS = [
    "romandie", "welschland", "westschweiz", "suisse romande", "svizzera italiana",
    "italienische schweiz", "deutschschweiz", "alpensüdseite", "alpensuedseite",
    "mittelland", "schweizer mittelland", "nordwestschweiz", "ostschweiz",
    "zentralschweiz", "innerschweiz", "berner oberland", "seeland",
    "berner mittelland", "emmental", "oberaargau", "jura südfuss", "jura suedfuss",
    "engadin", "prättigau", "praettigau", "surselva", "rheintal", "toggenburg",
    "linthgebiet", "march", "höfe", "hoefe", "freiamt", "fricktal", "zurzibiet",
    "knonaueramt", "zürcher unterland", "zuercher unterland", "zürcher oberland",
    "zuercher oberland", "weinland", "pfannenstiel", "glattal", "furttal",
    "limmattal", "laufental", "leimental", "seetal", "unterwalden", "riviera",
    "malcantone", "bleniotal", "maggiatal", "verzascatal", "leventina", "misox",
    "puschlav", "bergell", "chablais", "lavaux", "gros de vaud",
    "riviera vaudoise", "unterwallis", "oberwallis", "val de travers", "val de ruz",
    "franches montagnes",
]
AMBIGUOUS_SWISS_REGION_TERMS = {"march", "höfe", "hoefe", "riviera"}
SWISS_REGION_ANCHOR_TERMS = [
    term for term in SWISS_REGION_TERMS if term not in AMBIGUOUS_SWISS_REGION_TERMS
]

# Ortsnamen, die erst mit syntaktischem Ortskontext (z.B. "in Brunnen")
# belastbar werden. Baden und Riviera brauchen wegen konkreter ausländischer
# Gegenstücke zusätzlich einen eindeutigen Schweizer Anker.
SUPPORT_ONLY_SWISS_PLACE_TERMS = {"baden", "riviera"}
CONTEXTUAL_SWISS_PLACE_TERMS = ({
    "baar", "buchs", "cham", "gland", "maur", "risch", "wil", "brunnen",
    "laufen", "haag", "neuhaus", "march", "höfe", "hoefe",
} | AMBIGUOUS_SWISS_PLACE_TERMS) - SUPPORT_ONLY_SWISS_PLACE_TERMS
CONTEXTUAL_FOREIGN_PLACE_TERMS = {"pest"}
TRANSBOUNDARY_PLACE_TERMS = {
    "rhein", "bodensee", "jura", "alpen",
} | TRANSBOUNDARY_SWISS_WATER_TERMS

# Kanonische Ortsnamen und die im Kalibrierungs- bzw. Vergleichsmaterial
# beobachteten OCR-/Schreibvarianten. Die Varianten sind Codierungsanker,
# keine Suchbegriffe für e-newspaperarchives.ch.
SWISS_PLACE_OCR_ALIASES = {
    "Utzenstorf": [
        "utzenstorf", "ußenstorf", "ussenstorf", "ußenstors", "ussenstors",
        "ußenftorf", "ussenftorf", "atzenstorf",
    ],
    "Signau": ["signau", "signan"],
    "Wolfenschiessen": ["wolfenschiessen", "wolfenschieben"],
    "Näfels": ["näfels", "naefels"],
    "Nesslau": ["nesslau", "neßlau"],
    "Kradolf": ["kradolf", "kradols"],
    "Saint-Blaise": ["saint blaise", "st blaise", "stblaise"],
}
SWISS_PLACE_OCR_TERMS = list(dict.fromkeys(
    term for variants in SWISS_PLACE_OCR_ALIASES.values() for term in variants
))

LOCAL_TERMS = {
    "SEB": ["biel", "bienne", "nidau", "port", "lyss", "seeland", "grosses moos", "großes moos"],
    "BT": ["biel", "bienne", "nidau", "port", "lyss", "seeland", "grosses moos", "großes moos"],
    "DBU": ["bern", "berne", "matte", "aare", "schifflaube", "altenberg"],
    "NZZ": [
        "zürich", "zuerich", "züri", "zueri", "limmat", "zürichsee",
        "zuerichsee", "leimbach", "höcklergebiet", "hoecklergebiet",
    ],
}
EVENT_LOCAL_TERMS = [
    "biel", "nidau", "port", "seeland", "grosses moos", "großes moos", "ligerz",
    "twann", "erlach", "petersinsel", "bielersee", "aarberg", "büren an der aare",
]
REGIONAL_TERMS = {
    "SEB": list(dict.fromkeys(
        ["kanton bern", "bernbiet*", "bernerland*", "murten", "morat", "neuenburg",
         "neuchâtel", "neuchatel", "solothurn", "aarberg", "büren"]
        + SWISS_CITY_ANCHOR_TERMS_BY_CANTON["BE"]
    )),
    "BT": list(dict.fromkeys(
        ["kanton bern", "bernbiet*", "bernerland*", "murten", "morat", "neuenburg",
         "neuchâtel", "neuchatel", "solothurn", "aarberg", "büren"]
        + SWISS_CITY_ANCHOR_TERMS_BY_CANTON["BE"]
    )),
    "DBU": list(dict.fromkeys(
        ["kanton bern", "bernbiet*", "bernerland*", "emmental", "oberland",
         "berner oberland", "berner mittelland", "oberaargau"]
        + SWISS_CITY_ANCHOR_TERMS_BY_CANTON["BE"]
    )),
    "NZZ": list(dict.fromkeys(
        ["kanton zürich", "kanton zuerich", "zürcher", "zuercher", "zürichbiet",
         "zuerichbiet", "zürcher unterland", "zuercher unterland", "zürcher oberland",
         "zuercher oberland", "knonaueramt", "weinland", "pfannenstiel", "glattal",
         "furttal", "limmattal"] + SWISS_CITY_ANCHOR_TERMS_BY_CANTON["ZH"]
    )),
}
SWISS_CANTON_TERMS = [
    # Alle 26 Kantone einschliesslich der historisch als Halbkantone
    # bezeichneten Stände. Adjektivische Formen mit * erfassen auch
    # Pressebezeichnungen wie Bernerland, Glarnerland oder Urnerland.
    "aargau*", "aargauer*", "argovie", "argovia", "appenzell*", "appenzeller*",
    "appenzell a rh", "appenzell ar", "appenzell i rh", "appenzell ir",
    "ausserrhoden*", "ausserroden*", "innerrhoden*", "basel", "basel stadt",
    "basel landschaft", "basel land", "bale ville", "bale campagne",
    "basilea citta", "basilea campagna",
    "baselland*", "baselbiet*", "basler*", "bern", "berner*", "bernisch*",
    "freiburg", "freiburger*", "freiburgisch*", "fribourg*", "fribourgeo*",
    "friburgo", "genf", "genfer*", "geneve*", "genevois*", "ginevra",
    "glarus", "glarner*", "glaris", "glarona",
    "graubünden*", "graubuenden*", "graubündner*", "graubuendner*", "bündner*",
    "buendner*", "grisons", "grigioni", "kanton jura", "jurassier*",
    "jurassisch*", "giura", "luzern*", "lucerne*", "lucerna*", "neuenburg*", "neuchatel*",
    "neuchâtel*", "neuchatelois*", "nidwalden*", "nidwaldner*", "obwalden*",
    "obwaldner*", "unterwalden*", "schaffhausen*", "schaffhauser*", "schaffhouse*",
    "sciaffusa*", "schwyz", "schwyzer*", "schwytz", "svitto", "solothurn*",
    "soleure", "soletta", "st gallen", "sankt gallen", "saint gall", "san gallo",
    "st galler*", "sankt galler*", "st gallisch*", "thurgau*", "thurgauer*",
    "thurgovie", "turgovia", "tessin*",
    "tessiner*", "ticino", "ticinese*", "uri", "urner*", "waadt*",
    "waadtländer*", "waadtlaender*", "vaud", "vaudois*", "wallis*",
    "walliser*", "valais", "vallese", "kanton zug", "stadt zug", "in zug",
    "bei zug", "aus zug", "nach zug", "zuger*", "zoug", "zugo", "zürich*",
    "zuerich*", "zürcher*", "zuercher*", "zurigo",
]
SWISS_NATIONAL_DESIGNATION_TERMS = [
    "schweizerisch*", "schweizer", "schweizerin*",
    "eidgenosse*", "eidgenossin*", "miteidgenosse*", "miteidgenossin*",
    "eidgenössisch*", "eidgenoessisch*", "eidgenossenschaft",
    "schweizervolk*", "schweizerbürger*", "schweizerbuerger*",
    "schweizerbürgerin*", "schweizerbuergerin*",
]
# Diese Anredewoerter sind nie eigenstaendige Raumanker. Sie werden nur in
# unmittelbarer Verbindung mit einer nationalen Personenbezeichnung gewertet.
SWISS_NATIONAL_ADDRESS_QUALIFIERS = ["getreu*", "wert*", "lieb*"]
SWISS_TERMS = list(dict.fromkeys([
    "schweiz", "kanton", "aare", "limmat", "emme",
    "bielersee", "zürichsee", "zuerichsee", "wallis", "graubünden",
    "graubuenden", "bern", "zürich", "zuerich", "solothurn", "neuenburg", "murten",
    "ligerz", "konolfingen", "küttigen", "kuettigen", "biberstein", "fricktal",
    "merligen", "brienz", "thun", "interlaken", "emmental", "waldemme", "entlebuch",
    "oberland", "gotthard", "gotthardpass", "gotthard-pass",
] + SWISS_NATIONAL_DESIGNATION_TERMS + SWISS_CANTON_TERMS + SWISS_CITY_TERMS
  + SWISS_WATER_STRONG_TERMS
  + SWISS_ALTERNATIVE_TERMS + SWISS_REGION_ANCHOR_TERMS))
_PROTECTED_SWISS_PLACE_TERMS = {
    term
    for terms in SWISS_CITY_TERMS_BY_CANTON.values()
    for term in terms
} | set(SWISS_ALTERNATIVE_TERMS) | set(SWISS_REGION_TERMS) | set(SWISS_CANTON_TERMS) | {
    term
    for terms in SWISS_WATER_TERMS_BY_CANTON.values()
    for term in terms
    if term not in SWISS_WATER_FOREIGN_COLLISION_TERMS
}
ADDITIONAL_NON_SWISS_PLACE_TERMS = [
    term
    for term in NON_SWISS_PLACE_TERMS
    if term not in _PROTECTED_SWISS_PLACE_TERMS
]
CONTEXTUAL_FOREIGN_PLACE_TERMS |= {
    term
    for term in CONTEXTUAL_NON_SWISS_PLACE_TERMS
    if term in ADDITIONAL_NON_SWISS_PLACE_TERMS
}
STRONG_NON_SWISS_PLACE_TERMS = [
    term
    for term in ADDITIONAL_NON_SWISS_PLACE_TERMS
    if term not in CONTEXTUAL_FOREIGN_PLACE_TERMS
]
NON_SWISS_COUNTRY_TERMS = [
    "afghanistan", "ägypten", "aegypten", "albanien", "algerien", "andorra", "angola",
    "antigua und barbuda", "äquatorialguinea", "aequatorialguinea", "argentinien",
    "armenien", "aserbaidschan", "äthiopien", "aethiopien", "australien", "bahamas",
    "bahrain", "bangladesch", "bangladesh", "barbados", "belarus", "belgien", "belize", "benin",
    "bhutan", "bolivien", "bosnien und herzegowina", "botswana", "brasilien",
    "brunei", "bulgarien", "burkina faso", "burundi", "chile", "china", "costa rica",
    "côte d'ivoire", "cote d ivoire", "elfenbeinküste", "elfenbeinkueste",
    "dänemark", "daenemark", "deutschland", "dominica", "dominikanische republik",
    "dschibuti", "ecuador", "el salvador", "eritrea", "estland", "eswatini", "fidschi",
    "finnland", "frankreich", "gabun", "gambia", "georgien", "ghana", "grenada",
    "griechenland", "guatemala", "guinea", "guinea-bissau", "guyana", "haiti",
    "honduras", "indien", "indonesien", "irak", "iran", "irland", "island", "israel",
    "italien", "jamaika", "japan", "jemen", "jordanien", "kambodscha", "kamerun",
    "kanada", "kap verde", "kasachstan", "katar", "kenia", "kirgisistan", "kiribati",
    "kolumbien", "komoren", "kongo", "demokratische republik kongo", "republik kongo",
    "kroatien", "kuba", "kuwait", "laos", "lesotho", "lettland", "libanon", "liberia",
    "libyen", "liechtenstein", "litauen", "luxemburg", "madagaskar", "malawi",
    "malaysia", "malediven", "mali", "malta", "marokko", "marshallinseln",
    "mauretanien", "mauritius", "mexiko", "mikronesien", "moldau", "monaco",
    "mongolei", "montenegro", "mosambik", "myanmar", "namibia", "nauru", "nepal",
    "neuseeland", "nicaragua", "niederlande", "niger", "nigeria", "nordkorea",
    "nordmazedonien", "norwegen", "oman", "österreich", "osterreich", "pakistan",
    "palau", "palästina", "palaestina", "panama", "papua-neuguinea", "paraguay",
    "peru", "philippinen", "polen", "portugal", "ruanda", "rumänien", "rumaenien",
    "russland", "salomonen", "sambia", "samoa", "san marino", "são tomé und príncipe",
    "sao tome und principe", "saudi-arabien", "schweden", "senegal", "serbien",
    "seychellen", "sierra leone", "simbabwe", "singapur", "slowakei", "slowenien",
    "somalia", "spanien", "sri lanka", "st. kitts und nevis", "st. lucia",
    "st. vincent und die grenadinen", "südafrika", "suedafrika", "sudan", "südkorea",
    "suedkorea", "südsudan", "suedsudan", "suriname", "syrien", "tadschikistan",
    "tansania", "thailand", "timor-leste", "togo", "tonga", "trinidad und tobago",
    "tschad", "tschechien", "tunesien", "türkei", "tuerkei", "turkmenistan", "tuvalu",
    "uganda", "ukraine", "ungarn", "uruguay", "usbekistan", "vanuatu", "vatikanstadt",
    "venezuela", "vereinigte arabische emirate", "vereinigtes königreich",
    "vereinigtes koenigreich", "usa", "vereinigte staaten", "amerika", "vietnam",
    "zentralafrikanische republik", "zimbabwe", "zypern", "england", "schottland",
    "wales", "nordirland", "grossbritannien", "großbritannien", "uk", "u k",
    "u s a", "sowjetunion", "udssr", "jugoslawien", "tschechoslowakei", "ddr",
    "brd", "kosovo", "taiwan", "hongkong", "holland",
]
INTERNATIONAL_REFERENCE_TERMS = [
    "ausland", "europa", "amerika", "afrika", "asien", "australien", "international",
    "weltweit", "global", "ausländisch", "auslaendisch", "tschernobyl",
] + NON_SWISS_COUNTRY_TERMS
FOREIGN_PLACE_ALIASES = {
    "Budapest": ["budapest"],
    "Neapel": ["neapel", "neapels", "napoli"],
    "Posillipo": ["posillipo", "posilippo"],
    "Köln": ["köln", "koeln", "cologne"],
    "Konstanz": ["konstanz"],
    "Bayern": ["bayern", "südbayern", "suedbayern", "südbayem", "suedbayem"],
    "Westdeutschland": ["westdeutschland"],
    "Uderns": ["uderns"],
    "Tirol": ["tirol", "tyrol"],
    "Erzurum": ["erzurum", "erzerum"],
    "Hüningen": ["hüningen", "hueningen", "huningue"],
    "Monfalcone": ["monfalcone"],
    "Lissabon": ["lissabon", "lisboa"],
    "Brüssel": ["brüssel", "bruessel", "bruxelles", "brüffel", "brueffel"],
    "Versailles": ["versailles"],
    "Villepreux": ["villepreux"],
    "Lemberg": ["lemberg", "lviv", "lwow", "lwów"],
    "Kleinasien": ["kleinasien"],
    "Fréjus": ["fréjus", "frejus"],
    "Florenz": ["florenz", "firenze"],
    "Livorno": ["livorno"],
    "Venedig": ["venedig", "venezia"],
    "Caracas": ["caracas"],
    "Louisiana": ["louisiana"],
    "Nordindien": ["nordindien"],
    "Feldkirch": ["feldkirch", "feldtirch"],
    "Habsheim": ["habsheim"],
    "Calais": ["calais"],
    "Ahrtal": ["ahrtal"],
    "Bad Neuenahr": ["bad neuenahr", "neuenahr"],
    "Bonn": ["bonn", "bonner"],
    "Graz": ["graz", "grazer"],
    "Steiermark": ["steiermark", "steirisch*"],
    "Savoyen": ["savoyen", "savoie"],
}
FOREIGN_PLACE_ALIAS_TERMS = list(dict.fromkeys(
    term for variants in FOREIGN_PLACE_ALIASES.values() for term in variants
))
FOREIGN_PLACE_TERMS = list(dict.fromkeys([
    "paris", "pariser", "london", "londoner", "rom", "römisch*", "roemisch*",
    "mailand", "wien", "wiener", "berlin", "berliner", "münchen", "munchen",
    "hamburg", "karlsruhe", "mannheim", "baden baden", "guam", "moskau",
    "new york", "washington", "peking", "beijing", "tokio", "kyoto",
] + FOREIGN_PLACE_ALIAS_TERMS + STRONG_NON_SWISS_PLACE_TERMS))
FOREIGN_TERMS = INTERNATIONAL_REFERENCE_TERMS + FOREIGN_PLACE_TERMS
NEAR_FOREIGN = [
    "frankreich", "deutschland", "italien", "österreich", "osterreich",
    "neapel", "napoli", "posillipo", "posilippo", "köln", "koeln", "cologne",
    "konstanz", "bayern", "südbayern", "suedbayern", "südbayem", "suedbayem",
    "westdeutschland", "uderns", "tirol", "tyrol", "hüningen", "hueningen",
    "huningue", "monfalcone", "versailles", "villepreux", "fréjus", "frejus",
    "florenz", "firenze", "livorno", "venedig", "venezia", "feldkirch",
    "feldtirch", "habsheim", "calais",
]
EUROPE_FOREIGN = [
    "england", "spanien", "portugal", "norwegen", "schweden", "budapest",
    "lissabon", "lisboa", "brüssel", "bruessel", "bruxelles", "brüffel",
    "brueffel", "lemberg", "lviv", "lwow", "lwów", "holland",
]


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def norm(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or "").casefold())
    text = "".join(character for character in text if not unicodedata.combining(character))
    table = str.maketrans({"œ": "oe", "æ": "ae", "ø": "o", "ð": "d", "þ": "th"})
    return re.sub(r"[^a-z0-9]+", " ", text.translate(table)).strip()


@lru_cache(maxsize=2048)
def _term_pattern(term: str) -> re.Pattern[str] | None:
    raw = clean(term)
    if not raw:
        return None
    token_patterns: list[str] = []
    for token in raw.split():
        wildcard = token.endswith("*")
        needle = norm(token[:-1] if wildcard else token)
        if not needle:
            continue
        token_pattern = re.escape(needle)
        if wildcard:
            token_pattern += "[a-z0-9]*"
        token_patterns.append(token_pattern)
    if not token_patterns:
        return None
    pattern = r"\s+".join(token_patterns)
    return re.compile(rf"(?<![a-z0-9]){pattern}(?![a-z0-9])")


def _normalized_contains(hay: str, term: str) -> bool:
    pattern = _term_pattern(term)
    return bool(hay and pattern and pattern.search(hay))


@lru_cache(maxsize=128)
def _term_candidate_index(
    terms: tuple[str, ...],
) -> tuple[dict[str, tuple[int, ...]], tuple[tuple[str, int], ...], tuple[int, ...]]:
    """Index terms by their first normalized token for bounded matching."""
    exact: dict[str, list[int]] = {}
    prefixes: list[tuple[str, int]] = []
    fallback: list[int] = []
    for index, term in enumerate(terms):
        raw = clean(term)
        first_raw = raw.split()[0] if raw else ""
        wildcard = first_raw.endswith("*")
        normalized_first = norm(first_raw[:-1] if wildcard else first_raw)
        first = normalized_first.split()[0] if normalized_first else ""
        if not first:
            fallback.append(index)
        elif wildcard:
            prefixes.append((first, index))
        else:
            exact.setdefault(first, []).append(index)
    return (
        {token: tuple(indices) for token, indices in exact.items()},
        tuple(prefixes),
        tuple(fallback),
    )


def _candidate_term_indices(hay: str, terms: tuple[str, ...]) -> list[int]:
    if not hay or not terms:
        return []
    exact, prefixes, fallback = _term_candidate_index(terms)
    tokens = set(hay.split())
    candidates = set(fallback)
    for token in tokens:
        candidates.update(exact.get(token, ()))
        for prefix, index in prefixes:
            if token.startswith(prefix):
                candidates.add(index)
    return sorted(candidates)


def candidate_terms(text: Any, terms: list[str] | tuple[str, ...]) -> list[str]:
    """Return only terms whose first normalized token occurs in the text."""
    hay = norm(text)
    term_tuple = tuple(terms)
    return [
        term_tuple[index]
        for index in _candidate_term_indices(hay, term_tuple)
    ]


def contains_term(text: Any, term: str) -> bool:
    return _normalized_contains(norm(text), term)


def contains_any(text: Any, terms: list[str]) -> bool:
    hay = norm(text)
    term_tuple = tuple(terms)
    return any(
        _normalized_contains(hay, term_tuple[index])
        for index in _candidate_term_indices(hay, term_tuple)
    )


def conflict_reference_kind(text: Any) -> str:
    """Return strong or context so ambiguous terms never become primary K1."""
    if contains_any(text, CONFLICT_TERMS_STRONG):
        return "strong"
    if contains_any(text, CONFLICT_TERMS_CONTEXT):
        return "context"
    return ""


def has_conflict_reference(text: Any) -> bool:
    return bool(conflict_reference_kind(text))


def matching_terms(text: Any, terms: list[str]) -> list[str]:
    hay = norm(text)
    term_tuple = tuple(terms)
    return [
        term_tuple[index]
        for index in _candidate_term_indices(hay, term_tuple)
        if _normalized_contains(hay, term_tuple[index])
    ]


def matching_place_aliases(text: Any, aliases: dict[str, list[str]]) -> list[str]:
    """Return canonical place names with the concrete matched OCR variant."""
    matches: list[str] = []
    for canonical, variants in aliases.items():
        found = matching_terms(text, variants)
        if not found:
            continue
        distinct: list[str] = []
        seen_norms: set[str] = set()
        for term in found:
            normalized = norm(term)
            if normalized in seen_norms:
                continue
            seen_norms.add(normalized)
            distinct.append(term)
        canonical_norm = norm(canonical)
        variant_labels = [term for term in distinct if norm(term) != canonical_norm]
        if variant_labels:
            matches.append(f"{canonical} (OCR/Variante: {', '.join(variant_labels)})")
        else:
            matches.append(canonical)
    return matches


def has_human_made_hazard(text: Any) -> bool:
    if contains_any(text, HUMAN_MADE_HAZARD_TERMS_STRONG):
        return True
    # "Öl" ist als normalisierte Form nicht von der Sportabkürzung "OL"
    # unterscheidbar. Der Einzelbegriff zählt deshalb nur mit einem klaren
    # Austritts-, Brand- oder Verschmutzungskontext.
    oil_context = contains_any(text, [
        "öl", "oel", "heizöl*", "heizoel*", "erdöl*", "erdoel*", "benzin*",
        "hydrauliköl*", "hydraulikoel*", "mineralöl*", "mineraloel*", "rohöl*", "rohoel*",
        "treibstoff*", "diesel*", "kraftstoff*", "erdgas-produkt*",
    ]) and contains_any(text, [
        "ausgetreten*", "ausgeflossen*", "ausgelaufen*", "verschmutz*",
        "kontamin*", "leck*", "brand*", "explosion*", "verseucht*",
        "unfall*", "katastroph*", "gefährlich*", "gefahrlich*",
    ])
    if oil_context:
        return True
    # "Unfall" allein ist häufig beiläufig, metaphorisch oder Teil eines
    # Versicherungsbegriffs. M1/M2 verlangt zusätzlich einen konkreten
    # Unfallhergang, technische Ursache oder erkennbare Folgen.
    accident_context = contains_any(text, [
        "unfall*", "bahnunfall*", "verkehrsunfall*", "autounfall*",
        "arbeitsunfall*", "flugunfall*", "schiffsunfall*", "verunglück*",
        "verungluck*",
    ]) and contains_any(text, [
        "tödlich*", "toedlich*", "getötet*", "getoetet*", "verletzt*",
        "kollision*", "zusammenstoss*", "zusammenstoß*", "abgestürzt*",
        "abgesturzt*", "fahrzeug*", "lastwagen*", "auto", "zug", "bahn*",
        "flugzeug*", "helikopter*", "pilot*", "fahrleitung*", "explosion*",
        "brand*", "chemikalie*", "löschwasser*", "loeschwasser*", "gasleck*",
        "öl*", "oel*", "beinbruch*", "knochenbruch*",
    ])
    if accident_context:
        return True
    # Stoffnamen beschreiben auch Handel, Energie oder Landwirtschaft. Erst
    # ihr Austritt, ihre Kontamination oder ein ausdrücklicher Gefahrenkontext
    # macht daraus einen belastbaren M1/M2-Anker.
    substance_context = contains_any(text, [
        "chemikalie*", "schwermetall*", "pestizid*", "herbizid*",
        "pflanzenschutzmittel*",
    ]) and contains_any(text, [
        "ausgetreten*", "ausgeflossen*", "ausgelaufen*", "fliess*", "fließ*",
        "fluss*", "verschmutz*", "kontamin*", "verseucht*", "belastet*",
        "giftig*", "gefährlich*", "gefahrlich*", "unfall*", "brand*",
        "katastroph*", "grundwasser*", "gewässer*", "gewaesser*", "trinkwasser*",
        "gefahr*",
    ])
    if substance_context:
        return True
    # "Altlast" kann metaphorisch verwendet werden. Ohne Boden-, Standort-,
    # Umwelt- oder Schadstoffkontext bleibt es deshalb kein M1/M2-Anker.
    if contains_any(text, ["altlast*"]) and contains_any(text, [
        "boden*", "standort*", "deponie*", "schadstoff*", "kontamin*",
        "verschmutz*", "grundwasser*", "gewässer*", "gewaesser*", "sanierung*",
    ]):
        return True
    # Broad words such as "Menschen", "Unternehmen" or "Transport" support
    # M1/M2 only together with a concrete technical/anthropogenic danger.
    context_terms = [
        "brand*", "explosion*", "kontamination*", "giftig*",
        "schädlich*", "schaedlich*", "chemikalie*", "gasleck*", "austritt*",
        "nuklear*", "atomar*", "reaktor*", "löschwasser*", "loeschwasser*",
        "sicherheitsbestimmung*", "menschliches versagen",
    ]
    return contains_any(text, HUMAN_MADE_HAZARD_TERMS_CONTEXT) and contains_any(text, context_terms)


def find_project_root(start: Path | str | None = None) -> Path:
    override = clean(os.environ.get("ENPA_PROJECT_DIR"))
    if override:
        candidate = Path(os.path.expanduser(_expand_percent_vars(override))).resolve()
        if candidate.exists():
            return candidate
    current = Path(start or DEFAULT_CONFIG).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / PROJECT_MARKER).exists():
            return candidate
        if (
            (candidate / "enpa_automation" / "config.json").exists()
            and (candidate / "Skripte" / "Generate_ENPA_Links.cmd").exists()
        ):
            return candidate
    return FALLBACK_PROJECT_ROOT


def _expand_percent_vars(value: str) -> str:
    return re.sub(
        r"%([^%]+)%",
        lambda match: os.environ.get(match.group(1), match.group(0)),
        value,
    )


def downloads_dir() -> Path:
    override = clean(os.environ.get("ENPA_CAPTURE_DIR"))
    if override:
        return Path(os.path.expanduser(_expand_percent_vars(override))).resolve()
    if sys.platform == "win32":
        try:
            import winreg

            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            downloads_guid = "{374DE290-123F-4565-9164-39C4925E467B}"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                value, _ = winreg.QueryValueEx(key, downloads_guid)
            return Path(os.path.expandvars(value)).expanduser().resolve()
        except (OSError, ImportError):
            pass
    xdg_config = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    user_dirs = xdg_config / "user-dirs.dirs"
    if user_dirs.exists():
        try:
            match = re.search(
                r'^XDG_DOWNLOAD_DIR="([^"]+)"',
                user_dirs.read_text(encoding="utf-8"),
                flags=re.MULTILINE,
            )
            if match:
                value = match.group(1).replace("$HOME", str(Path.home()))
                return Path(value).expanduser().resolve()
        except OSError:
            pass
    return (Path.home() / "Downloads").resolve()


def load_config(path: Path | str | None = None) -> dict[str, Any]:
    config_path = Path(path or DEFAULT_CONFIG).expanduser().resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["__config_path"] = str(config_path)
    config["__project_root"] = str(find_project_root(config_path))
    return config


def resolve_config_path(config: dict[str, Any], value: str | None) -> Path | None:
    if not value:
        return None
    project_root = Path(config.get("__project_root") or find_project_root())
    config_dir = Path(config["__config_path"]).parent
    replacements = {
        "${PROJECT_DIR}": str(project_root),
        "${CONFIG_DIR}": str(config_dir),
        "${HOME}": str(Path.home()),
        "${DOWNLOADS}": str(downloads_dir()),
    }
    expanded = str(value)
    for token, replacement in replacements.items():
        expanded = expanded.replace(token, replacement)
    expanded = os.path.expandvars(_expand_percent_vars(expanded))
    expanded = os.path.expanduser(expanded.replace("/", os.sep))
    path = Path(expanded)
    if path.is_absolute():
        return path.resolve()
    return (config_dir / path).resolve()


def resolve_workbook_profile(
    config: dict[str, Any],
    profile: str | None = None,
) -> tuple[str, Path, dict[str, Any]]:
    """Resolve a named workbook profile while retaining legacy config support."""
    profiles = config.get("workbookProfiles") or {}
    selected = clean(profile) or clean(config.get("activeWorkbookProfile"))
    if profiles:
        selected = selected or next(iter(profiles))
        if selected not in profiles:
            available = ", ".join(sorted(profiles))
            raise ValueError(
                f"Unbekanntes Arbeitsmappenprofil '{selected}'. Verfügbar: {available}"
            )
        raw_spec = profiles[selected]
        spec = {"path": raw_spec} if isinstance(raw_spec, str) else dict(raw_spec)
        workbook = resolve_config_path(config, spec.get("path"))
        if not workbook:
            raise ValueError(f"Im Arbeitsmappenprofil '{selected}' fehlt der Pfad.")
        return selected, workbook, spec

    workbook = resolve_config_path(config, config.get("workbook"))
    if not workbook:
        raise ValueError("In config.json ist keine Arbeitsmappe konfiguriert.")
    return selected or "default", workbook, {}


def resolve_project_path(config: dict[str, Any], value: str | Path) -> Path:
    raw = Path(value).expanduser()
    if raw.is_absolute():
        return raw.resolve()
    project_root = Path(config.get("__project_root") or find_project_root())
    return (project_root / raw).resolve()


def portable_project_path(config: dict[str, Any], value: Path | str) -> str:
    path = Path(value).resolve()
    project_root = Path(config.get("__project_root") or find_project_root())
    try:
        return path.relative_to(project_root).as_posix()
    except ValueError:
        return str(path)


def parse_iso(value: Any) -> date | None:
    text = clean(value)
    if not text:
        return None
    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def ddmmyyyy(value: Any) -> str:
    d = parse_iso(value)
    return d.strftime("%d.%m.%Y") if d else clean(value)


def parse_date_parts(iso_date: str) -> dict[str, str]:
    d = parse_iso(iso_date)
    if not d:
        raise ValueError(f"Datum muss YYYY-MM-DD sein: {iso_date}")
    return {"day": f"{d.day:02d}", "month": f"{d.month:02d}", "year": f"{d.year:04d}"}


def edate(iso_date: str) -> str:
    d = parse_date_parts(iso_date)
    return f"{d['day']}-{d['month']}-{d['year']}"


def normalize_header(value: Any) -> str:
    return clean(value).lower()


def header_map(ws) -> dict[str, int]:
    return {normalize_header(cell.value): cell.column for cell in ws[1] if cell.value}


def find_col(headers: dict[str, int], name: str) -> int:
    key = normalize_header(name)
    if key in headers:
        return headers[key]
    for header, col in headers.items():
        if header.startswith(key):
            return col
    raise KeyError(f"Spalte nicht gefunden: {name}")


def expand_categories(config: dict[str, Any]) -> list[str]:
    all_categories = sorted(config["searchCategories"])
    available = [
        key
        for key in all_categories
        if config["searchCategories"][key].get("enabled", True)
    ]
    requested = config.get("categoriesToRun") or available
    expanded: list[str] = []
    for item in requested:
        raw = clean(item).upper()
        if raw in {"*", "ALL", "ALLE"}:
            expanded.extend(available)
            continue
        match = re.fullmatch(r"([A-Z])-([A-Z])", raw)
        if match:
            start, end = ord(match.group(1)), ord(match.group(2))
            step = 1 if start <= end else -1
            for code in range(start, end + step, step):
                key = chr(code)
                if key in available:
                    expanded.append(key)
            continue
        expanded.append(raw)
    seen: set[str] = set()
    result: list[str] = []
    for key in expanded:
        if key not in all_categories:
            raise KeyError(f"Unbekannte Suchkategorie: {key}")
        if key not in available:
            continue
        if key not in seen:
            seen.add(key)
            result.append(key)
    return result


def include_historical_terms(config: dict[str, Any], query: dict[str, Any]) -> bool:
    cutoff = config.get("includeHistoricalTermsForYearsUpTo")
    if cutoff in (None, False):
        return False
    d = parse_iso(query["dateFrom"])
    return bool(d and d.year <= int(cutoff))


def search_terms(config: dict[str, Any], category: str, query: dict[str, Any]) -> list[str]:
    data = config["searchCategories"][category]
    terms = list(data.get("terms") or [])
    if data.get("stemTerms") or data.get("historicalStemTerms"):
        raise ValueError(
            f"Suchkategorie {category} verwendet veraltete Stammbegriffe. "
            "Bitte alle ENPA-Suchformen ausdrücklich unter 'terms' aufführen."
        )
    if include_historical_terms(config, query):
        terms.extend(data.get("historicalTerms") or [])
    seen: set[str] = set()
    result: list[str] = []
    for term in terms:
        if "*" in clean(term):
            raise ValueError(
                f"ENPA-Suchbegriff '{clean(term)}' enthält ein Sternchen. "
                "Wortstämme werden nicht unterstützt; bitte vollständige Wortformen angeben."
            )
        key = norm(term)
        if key and key not in seen:
            seen.add(key)
            result.append(clean(term))
    return result


def quote_term(term: str) -> str:
    raw = clean(term)
    if not raw or (raw.startswith('"') and raw.endswith('"')):
        return raw
    return f'"{raw.replace(chr(34), chr(92) + chr(34))}"' if re.search(r"[\s-]", raw) else raw


def search_string(terms: list[str]) -> str:
    return " OR ".join(quote_term(term) for term in terms)


def compact_state_search_string(terms: list[str]) -> str:
    """Render terms safely inside ENPA's hyphen-delimited ``e`` state.

    The canonical advanced-search value remains unchanged in ``txq``. Only the
    duplicated compact UI state replaces hyphens inside quoted phrases with
    spaces, otherwise ENPA can reject the requested 100-result page size and
    silently fall back to 20 results.
    """
    rendered: list[str] = []
    for term in terms:
        value = quote_term(term)
        if value.startswith('"') and value.endswith('"'):
            value = value.replace("-", " ")
        rendered.append(value)
    return " OR ".join(rendered)


def publication_codes(config: dict[str, Any]) -> list[str]:
    return [pub["archiveCode"] for pub in config.get("defaultPublications", [])]


def result_page_size(config: dict[str, Any]) -> int:
    value = config.get("resultsPerPage", RESULT_PAGE_SIZE)
    try:
        page_size = int(value)
    except (TypeError, ValueError):
        page_size = RESULT_PAGE_SIZE
    return page_size if page_size > 0 else RESULT_PAGE_SIZE


def query_key(meta: dict[str, Any]) -> str:
    pubs = ",".join(pub.get("archiveCode", str(pub)) if isinstance(pub, dict) else str(pub) for pub in meta.get("defaultPublications", []))
    return "||".join([clean(meta.get("dateFrom")), clean(meta.get("dateTo")), clean(meta.get("category")).upper(), clean(meta.get("searchString")), pubs])


def encode_meta(meta: dict[str, Any]) -> str:
    payload = json.dumps(meta, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return base64.b64encode(payload).decode("ascii")


def build_search_url(config: dict[str, Any], query: dict[str, Any], category: str, start_rank: int) -> tuple[str, dict[str, Any]]:
    terms = search_terms(config, category, query)
    s = search_string(terms)
    state_s = compact_state_search_string(terms)
    frm = parse_date_parts(query["dateFrom"])
    to = parse_date_parts(query["dateTo"])
    pubs = publication_codes(config)
    page_size = result_page_size(config)
    params: list[tuple[str, str]] = [
        ("a", "q"), ("hs", "1"), ("r", str(start_rank)), ("results", "1"), ("txq", s),
        ("dafdq", frm["day"]), ("dafmq", frm["month"]), ("dafyq", frm["year"]),
        ("datdq", to["day"]), ("datmq", to["month"]), ("datyq", to["year"]),
        ("laq", ""),
    ]
    params.extend(("puq", code) for code in pubs)
    params.extend([("txf", "txIN"), ("ssnip", "txt"), ("ccq", "")])
    e_value = f"{edate(query['dateFrom'])}-{edate(query['dateTo'])}--de-{page_size}-{','.join(pubs)}-{start_rank}-byDA-txt-txIN-{state_s}-------0-----"
    params.append(("e", e_value))
    meta = {
        "queryName": query.get("name", ""),
        "eventName": query.get("eventName", ""),
        "eventStart": query.get("eventStart", ""),
        "eventEnd": query.get("eventEnd", ""),
        "windowType": query.get("windowType", ""),
        "dateFrom": query["dateFrom"],
        "dateTo": query["dateTo"],
        "falltyp": config.get("falltyp", ""),
        "category": category,
        "categoryLabel": config["searchCategories"][category].get("label", ""),
        "searchString": s,
        "searchTerms": terms,
        "defaultPublications": config.get("defaultPublications", []),
        "captureFilePrefix": config.get("captureFilePrefix", "enpa_v2"),
        "startRank": start_rank,
        "pageSize": page_size,
    }
    return f"{BASE_URL}?{urlencode(params)}#enpa={encode_meta(meta)}", meta


def is_pilot(falltyp: str) -> bool:
    return norm(falltyp).replace(" ", "") == "pilotabfrage"


def display_id_for_row(row_number: int) -> str:
    return f"T{row_number - 1:04d}"

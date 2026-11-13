# Automatisch erzeugter Datenkatalog; nicht von Hand bearbeiten.
# Aktualisierung: workbook_tools/update_non_swiss_place_catalog.py

SOURCE_FILE = "non_swiss_places_20260811.txt"
CATALOG_VERSION = "2026-08-11"
COUNTRY_COUNT = 42
PLACE_RECORD_COUNT = 4202
PRIMARY_NAME_COUNT = 4196
ALTERNATIVE_NAME_COUNT = 985

NON_SWISS_PLACE_ALIASES_BY_COUNTRY = {
    "Albanien": {
        "ballsh": [
            "ballshi"
        ],
        "berat": [
            "berati"
        ],
        "bilisht": [
            "bilishti"
        ],
        "bulqizë": [
            "bulqiza"
        ],
        "burrel": [
            "burreli"
        ],
        "cërrik": [
            "cërriku"
        ],
        "durrës": [
            "durrësi"
        ],
        "elbasan": [
            "elbasani"
        ],
        "farkë": [
            "farka"
        ],
        "fier": [
            "fieri"
        ],
        "fushë-krujë": [
            "fushë-kruja"
        ],
        "gjirokastër": [
            "gjirokastra"
        ],
        "gramsh": [
            "gramshi"
        ],
        "kamëz": [
            "kamza"
        ],
        "kashar": [
            "kashari"
        ],
        "kavajë": [
            "kavaja"
        ],
        "korçë": [
            "korça"
        ],
        "krujë": [
            "kruja"
        ],
        "kuçovë": [
            "kuçova",
            "qyteti stalin"
        ],
        "kukës": [
            "kukësi"
        ],
        "laç": [
            "laçi"
        ],
        "lezhë": [
            "lezha"
        ],
        "librazhd": [
            "librazhdi"
        ],
        "lushnjë": [
            "lushnja"
        ],
        "paskuqan": [
            "paskuqani"
        ],
        "patos": [
            "patosi"
        ],
        "peqin": [
            "peqini"
        ],
        "përmet": [
            "përmeti"
        ],
        "peshkopi": [
            "peshkopia"
        ],
        "pogradec": [
            "pogradeci"
        ],
        "rrogozhinë": [
            "rrogozhina"
        ],
        "sarandë": [
            "saranda"
        ],
        "shijak": [
            "shijaku"
        ],
        "shkodër": [
            "shkodra"
        ],
        "sukth": [
            "sukthi"
        ],
        "tiranë": [
            "tirana"
        ],
        "vlorë": [
            "vlora"
        ]
    },
    "Belgien": {
        "aalst": [
            "alost"
        ],
        "aalter": [],
        "aarschot": [],
        "andenne": [],
        "anderlecht": [],
        "ans": [],
        "antwerpen": [
            "anvers"
        ],
        "arlon": [
            "aarlen"
        ],
        "asse": [],
        "ath": [
            "aat"
        ],
        "auderghem": [
            "oudergem"
        ],
        "balen": [],
        "bastogne": [
            "bastenaken"
        ],
        "beersel": [],
        "berchem-sainte-agathe": [
            "sint-agatha-berchem"
        ],
        "beringen": [],
        "beveren-kruibeke-zwijndrecht": [],
        "bilzen-hoeselt": [],
        "binche": [],
        "blankenberge": [],
        "boom": [],
        "bornem": [],
        "boussu": [],
        "braine-l'alleud": [
            "eigenbrakel"
        ],
        "braine-le-comte": [
            "'s gravenbrakel"
        ],
        "brasschaat": [],
        "brecht": [],
        "brugge": [
            "bruges",
            "brügge"
        ],
        "bruxelles": [
            "brussel",
            "brüssel"
        ],
        "charleroi": [],
        "châtelet": [],
        "chaudfontaine": [],
        "colfontaine": [],
        "courcelles": [],
        "deinze": [],
        "denderleeuw": [],
        "dendermonde": [
            "termonde"
        ],
        "diepenbeek": [],
        "diest": [],
        "dilbeek": [],
        "dilsen-stokkem": [],
        "edegem": [],
        "eeklo": [],
        "erpe-mere": [],
        "etterbeek": [],
        "eupen": [],
        "evere": [],
        "evergem": [],
        "flémalle": [],
        "fleurus": [],
        "forest": [
            "vorst"
        ],
        "frameries": [],
        "ganshoren": [],
        "geel": [],
        "gembloux": [],
        "genk": [],
        "gent": [
            "gand"
        ],
        "geraardsbergen": [
            "grammont"
        ],
        "grâce-hollogne": [],
        "grimbergen": [],
        "halle": [
            "hal"
        ],
        "hamme": [],
        "harelbeke": [],
        "hasselt": [],
        "heist-op-den-berg": [],
        "herent": [],
        "herentals": [],
        "herstal": [],
        "heusden-zolder": [],
        "hoogstraten": [],
        "houthalen-helchteren": [],
        "huy": [
            "hoei"
        ],
        "ieper": [
            "ypres",
            "ypern"
        ],
        "ixelles": [
            "elsene"
        ],
        "izegem": [],
        "jette": [],
        "kalmthout": [],
        "kapellen": [],
        "kasterlee": [],
        "knokke-heist": [],
        "koekelberg": [],
        "koksijde": [],
        "kontich": [],
        "kortenberg": [],
        "kortrijk": [
            "courtrai"
        ],
        "la louvière": [],
        "lanaken": [],
        "lebbeke": [],
        "leuven": [
            "louvain",
            "löwen"
        ],
        "liège": [
            "luik",
            "lüttich"
        ],
        "lier": [
            "lierre"
        ],
        "lievegem": [],
        "lochristi": [],
        "lokeren": [],
        "lommel": [],
        "maaseik": [],
        "maasmechelen": [],
        "maldegem": [],
        "manage": [],
        "mechelen": [
            "malines"
        ],
        "meise": [],
        "menen": [
            "menin"
        ],
        "merelbeke-melle": [],
        "middelkerke": [],
        "mol": [],
        "molenbeek-saint-jean": [
            "sint-jans-molenbeek"
        ],
        "mons": [
            "bergen"
        ],
        "mortsel": [],
        "mouscron": [
            "moeskroen"
        ],
        "namur": [
            "namen"
        ],
        "nazareth-de pinte": [],
        "nijlen": [],
        "ninove": [],
        "nivelles": [
            "nijvel"
        ],
        "oostende": [
            "ostende"
        ],
        "oostkamp": [],
        "ottignies-louvain-la-neuve": [],
        "oudenaarde": [
            "audenarde"
        ],
        "oudsbergen": [],
        "oupeye": [],
        "overijse": [],
        "pajottegem": [],
        "pelt": [],
        "poperinge": [],
        "puurs-sint-amands": [],
        "ranst": [],
        "rixensart": [],
        "roeselare": [
            "roulers"
        ],
        "ronse": [
            "renaix"
        ],
        "saint-ghislain": [],
        "saint-gilles": [
            "sint-gillis"
        ],
        "saint-josse-ten-noode": [
            "sint-joost-ten-node"
        ],
        "saint-nicolas": [],
        "sambreville": [],
        "schaerbeek": [
            "schaarbeek"
        ],
        "scherpenheuvel-zichem": [
            "montaigu-zichem"
        ],
        "schilde": [],
        "schoten": [],
        "seraing": [],
        "sint-gillis-waas": [],
        "sint-katelijne-waver": [],
        "sint-niklaas": [
            "saint-nicolas"
        ],
        "sint-pieters-leeuw": [],
        "sint-truiden": [
            "saint-trond"
        ],
        "soignies": [
            "zinnik"
        ],
        "stekene": [],
        "temse": [
            "tamise"
        ],
        "tervuren": [],
        "tessenderlo-ham": [],
        "tielt": [],
        "tienen": [
            "tirlemont"
        ],
        "tongeren-borgloon": [
            "tongres-looz"
        ],
        "torhout": [],
        "tournai": [
            "doornik"
        ],
        "tubize": [
            "tubeke"
        ],
        "turnhout": [],
        "uccle": [
            "ukkel"
        ],
        "verviers": [],
        "vilvoorde": [
            "vilvorde"
        ],
        "waregem": [],
        "waterloo": [],
        "watermael-boitsfort": [
            "watermaal-bosvoorde"
        ],
        "wavre": [
            "waver"
        ],
        "westerlo": [],
        "wetteren": [],
        "wevelgem": [],
        "willebroek": [],
        "wingene": [],
        "woluwe-saint-lambert": [
            "sint-lambrechts-woluwe"
        ],
        "woluwe-saint-pierre": [
            "sint-pieters-woluwe"
        ],
        "wuustwezel": [],
        "zaventem": [],
        "zedelgem": [],
        "zele": [],
        "zemst": [],
        "zoersel": [],
        "zonhoven": [],
        "zottegem": [],
        "zwevegem": []
    },
    "Bosnien Herzogowina": {
        "banja luka": [],
        "bihać": [],
        "bijeljina": [],
        "bosanska krupa": [],
        "brčko": [],
        "bugojno": [],
        "cazin": [],
        "derventa": [],
        "doboj": [],
        "foča": [
            "srbinje"
        ],
        "goražde": [],
        "gračanica": [],
        "gradačac": [],
        "gradiška": [
            "bosanska gradiška"
        ],
        "janja": [],
        "kakanj": [],
        "konjic": [],
        "kozarska dubica": [
            "bosanska dubica"
        ],
        "livno": [],
        "ljubuški": [],
        "lukavac": [],
        "modriča": [],
        "mostar": [],
        "novi grad": [
            "bosanski novi"
        ],
        "orašje": [],
        "pale": [],
        "prijedor": [],
        "sanski most": [],
        "sarajevo": [
            "sarajewo"
        ],
        "travnik": [],
        "trebinje": [],
        "tuzla": [],
        "visoko": [],
        "vogošća": [],
        "zenica": [],
        "živinice grad": [],
        "zvornik": []
    },
    "Bulgarien": {
        "ajtos": [],
        "asenovgrad": [
            "assenowgrad"
        ],
        "bankja": [],
        "bansko": [],
        "berkovica": [
            "berkowiza"
        ],
        "blagoevgrad": [
            "blagoewgrad"
        ],
        "botevgrad": [
            "botewgrad"
        ],
        "burgas": [],
        "červen brjag": [
            "tscherwen brjag"
        ],
        "čirpan": [
            "tschirpan"
        ],
        "dimitrovgrad": [
            "dimitrowgrad"
        ],
        "dobrič": [
            "tolbuhin",
            "dobritsch"
        ],
        "dupnica": [
            "stanke dimitrov",
            "dupniza"
        ],
        "gabrovo": [
            "gabrowo"
        ],
        "goce delčev": [
            "goze deltschew"
        ],
        "gorna orjahovica": [
            "gorna orjachowiza"
        ],
        "harmanli": [
            "charmanli"
        ],
        "haskovo": [
            "chaskowo"
        ],
        "ihtiman": [
            "ichtiman"
        ],
        "jambol": [],
        "kǎrdžali": [
            "kardschali"
        ],
        "karlovo": [
            "karlowo"
        ],
        "karnobat": [],
        "kavarna": [
            "kawarna"
        ],
        "kazanlǎk": [
            "kasanlak"
        ],
        "kjustendil": [],
        "kostinbrod": [],
        "kozloduj": [
            "kosloduj"
        ],
        "lom": [],
        "loveč": [
            "lowetsch"
        ],
        "montana": [
            "mihajlovgrad"
        ],
        "nesebǎr": [
            "nessebar"
        ],
        "nova zagora": [
            "nowa sagora"
        ],
        "novi iskǎr": [],
        "novi pazar": [
            "nowi pasar"
        ],
        "panagjurište": [
            "panagjurischte"
        ],
        "pǎrvomaj": [
            "parwomaj"
        ],
        "pazardžik": [
            "pasardschik"
        ],
        "pernik": [],
        "peštera": [
            "peschtera"
        ],
        "petrič": [
            "petritsch"
        ],
        "pleven": [
            "plewen"
        ],
        "plovdiv": [
            "plowdiw"
        ],
        "pomorie": [],
        "popovo": [
            "popowo"
        ],
        "provadija": [
            "prowadija"
        ],
        "radnevo": [
            "radnewo"
        ],
        "radomir": [],
        "rakovski": [
            "rakowski"
        ],
        "razgrad": [
            "rasgrad"
        ],
        "razlog": [
            "raslog"
        ],
        "ruse": [
            "russe"
        ],
        "samokov": [
            "samokow"
        ],
        "sandanski": [],
        "sevlievo": [
            "sewliewo"
        ],
        "silistra": [],
        "sliven": [
            "sliwen"
        ],
        "smoljan": [],
        "sofija": [
            "sofia"
        ],
        "stambolijski": [],
        "stara zagora": [
            "stara sagora"
        ],
        "šumen": [
            "schumen"
        ],
        "svilengrad": [
            "swilengrad"
        ],
        "svištov": [
            "swischtow"
        ],
        "tǎrgovište": [
            "targowischte"
        ],
        "trojan": [],
        "varna": [
            "warna"
        ],
        "veliko tǎrnovo": [
            "weliko tarnowo"
        ],
        "velingrad": [
            "welingrad"
        ],
        "vidin": [
            "widin"
        ],
        "vraca": [
            "wraza"
        ]
    },
    "Dänemark": {
        "aabenraa": [
            "apenrade"
        ],
        "aabybro": [],
        "aalborg": [],
        "aarhus": [],
        "aars": [],
        "assens": [],
        "beder-malling": [],
        "bellinge": [],
        "billund": [],
        "birkerød": [],
        "bjerringbro": [],
        "børkop": [],
        "borup": [],
        "bramming": [],
        "brande": [],
        "brønderslev": [],
        "dragør": [],
        "ebeltoft": [],
        "esbjerg": [],
        "faaborg": [],
        "farum": [],
        "fensmark": [],
        "fredensborg": [
            "fredensborg stationsby"
        ],
        "fredericia": [],
        "frederikshavn": [],
        "frederikssund": [],
        "frederiksværk": [],
        "galten": [],
        "gilleleje": [],
        "give": [],
        "grenaa": [],
        "grindsted": [],
        "haderslev": [
            "hadersleben"
        ],
        "hadsten": [],
        "hadsund": [],
        "hammel": [],
        "haslev": [],
        "hedehusene": [
            "fløng"
        ],
        "hedensted": [],
        "hellebæk": [],
        "helsinge": [],
        "helsingør": [],
        "herning": [],
        "hillerød": [],
        "hinnerup": [],
        "hirtshals": [],
        "hjørring": [],
        "hobro": [],
        "holbæk": [],
        "holstebro": [],
        "hornbæk-dronningmølle": [],
        "hørning": [],
        "hornslet": [],
        "horsens": [],
        "hørsholm": [],
        "humlebæk": [],
        "hundested": [],
        "ikast": [],
        "jyllinge": [],
        "kalundborg": [],
        "kerteminde": [],
        "kirke hvalsø": [],
        "kjellerup": [],
        "klarup": [],
        "københavn": [
            "kopenhagen"
        ],
        "køge": [],
        "kolding": [],
        "korsør": [],
        "lemvig": [],
        "lillerød": [],
        "løgten": [],
        "lystrup": [],
        "maribo": [],
        "mårslet": [],
        "middelfart": [],
        "munkebo": [],
        "næstved": [],
        "nakskov": [],
        "nibe": [],
        "nivå": [],
        "nordborg": [
            "norburg"
        ],
        "nørresundby": [],
        "nyborg": [],
        "nykøbing": [
            "nykøbing falster",
            "nykøbing mors",
            "nykøbing sjælland"
        ],
        "odder": [],
        "odense": [],
        "ølstykke-stenløse": [],
        "otterup": [],
        "randers": [],
        "ribe": [],
        "ringe": [],
        "ringkøbing": [],
        "ringsted": [],
        "rødekro": [
            "rothenkrug"
        ],
        "rønne": [],
        "roskilde": [],
        "ry": [],
        "sæby": [],
        "silkeborg": [],
        "skælskør": [],
        "skagen": [],
        "skanderborg": [],
        "skive": [],
        "skjern": [],
        "slagelse": [],
        "slangerup": [],
        "smørumnedre": [],
        "solrød strand": [],
        "sønderborg": [
            "sonderburg"
        ],
        "sorø": [],
        "støvring": [],
        "strib": [],
        "strøby egede": [],
        "struer": [],
        "svendborg": [],
        "svenstrup": [],
        "taastrup": [],
        "thisted": [],
        "tønder": [
            "tondern"
        ],
        "tune": [],
        "værløse": [],
        "vamdrup": [],
        "varde": [],
        "vejen": [],
        "vejle": [],
        "viborg": [],
        "viby": [],
        "vojens": [],
        "vordingborg": []
    },
    "Deutschland": {
        "aachen": [],
        "aalen": [],
        "ahlen": [],
        "arnsberg": [],
        "aschaffenburg": [],
        "augsburg": [],
        "bad homburg vor der höhe": [],
        "bad kreuznach": [],
        "bad oeynhausen": [],
        "bad salzuflen": [],
        "baden-baden": [],
        "bamberg": [],
        "bayreuth": [],
        "bergheim": [],
        "bergisch gladbach": [],
        "berlin": [],
        "bielefeld": [],
        "böblingen": [],
        "bocholt": [],
        "bochum": [],
        "bonn": [],
        "bottrop": [],
        "brandenburg an der havel": [],
        "braunschweig": [],
        "bremen": [],
        "bremerhaven": [],
        "castrop-rauxel": [],
        "celle": [],
        "chemnitz": [],
        "cottbus": [
            "chóśebuz"
        ],
        "darmstadt": [],
        "delmenhorst": [],
        "dessau-rosslau": [],
        "detmold": [],
        "dinslaken": [],
        "dormagen": [],
        "dorsten": [],
        "dortmund": [],
        "dresden": [],
        "duisburg": [],
        "düren": [],
        "düsseldorf": [],
        "elmshorn": [],
        "erfurt": [],
        "erlangen": [],
        "eschweiler": [],
        "essen": [],
        "esslingen am neckar": [],
        "euskirchen": [],
        "flensburg": [],
        "frankfurt": [
            "frankfurt oder"
        ],
        "frankfurt am main": [],
        "frechen": [],
        "freiburg im breisgau": [],
        "friedrichshafen": [],
        "fulda": [],
        "fürth": [],
        "garbsen": [],
        "gelsenkirchen": [],
        "gera": [],
        "giessen": [],
        "gladbeck": [],
        "göppingen": [],
        "görlitz": [],
        "göttingen": [],
        "greifswald": [],
        "grevenbroich": [],
        "gronau": [
            "gronau westf"
        ],
        "gummersbach": [],
        "gütersloh": [],
        "hagen": [],
        "halle": [
            "halle saale"
        ],
        "hamburg": [],
        "hameln": [],
        "hamm": [],
        "hanau": [],
        "hannover": [],
        "hattingen": [],
        "heidelberg": [],
        "heidenheim an der brenz": [],
        "heilbronn": [],
        "herford": [],
        "herne": [],
        "herten": [],
        "hilden": [],
        "hildesheim": [],
        "hürth": [],
        "ibbenbüren": [],
        "ingolstadt": [],
        "iserlohn": [],
        "jena": [],
        "kaiserslautern": [],
        "karlsruhe": [],
        "kassel": [],
        "kempten": [
            "allgäu"
        ],
        "kerpen": [],
        "kiel": [],
        "kleve": [],
        "koblenz": [],
        "köln": [],
        "konstanz": [],
        "krefeld": [],
        "lahr/schwarzwald": [],
        "landshut": [],
        "langenfeld": [
            "langenfeld rheinland"
        ],
        "langenhagen": [],
        "leipzig": [],
        "leverkusen": [],
        "lingen": [
            "lingen ems"
        ],
        "lippstadt": [],
        "lörrach": [],
        "lübeck": [],
        "lüdenscheid": [],
        "ludwigsburg": [],
        "ludwigshafen am rhein": [],
        "lüneburg": [],
        "lünen": [],
        "magdeburg": [],
        "mainz": [],
        "mannheim": [],
        "marburg": [],
        "marl": [],
        "meerbusch": [],
        "menden": [
            "menden sauerland"
        ],
        "minden": [],
        "moers": [],
        "mönchengladbach": [],
        "mülheim an der ruhr": [],
        "münchen": [],
        "münster": [],
        "neu-ulm": [],
        "neubrandenburg": [],
        "neumünster": [],
        "neuss": [],
        "neustadt an der weinstrasse": [],
        "neuwied": [],
        "norderstedt": [],
        "nordhorn": [],
        "nürnberg": [],
        "oberhausen": [],
        "offenbach am main": [],
        "offenburg": [],
        "oldenburg": [
            "oldenburg oldb"
        ],
        "osnabrück": [],
        "paderborn": [],
        "passau": [],
        "peine": [],
        "pforzheim": [],
        "plauen": [],
        "potsdam": [],
        "pulheim": [],
        "rastatt": [],
        "ratingen": [],
        "ravensburg": [],
        "recklinghausen": [],
        "regensburg": [],
        "remscheid": [],
        "reutlingen": [],
        "rheine": [],
        "rosenheim": [],
        "rostock": [],
        "rüsselsheim am main": [],
        "saarbrücken": [],
        "salzgitter": [],
        "sankt augustin": [],
        "schwäbisch gmünd": [],
        "schweinfurt": [],
        "schwerin": [],
        "siegen": [],
        "sindelfingen": [],
        "solingen": [],
        "stolberg": [
            "stolberg rhld"
        ],
        "stralsund": [],
        "stuttgart": [],
        "trier": [],
        "troisdorf": [],
        "tübingen": [],
        "ulm": [],
        "unna": [],
        "velbert": [],
        "viersen": [],
        "villingen-schwenningen": [],
        "waiblingen": [],
        "weimar": [],
        "wesel": [],
        "wetzlar": [],
        "wiesbaden": [],
        "wilhelmshaven": [],
        "witten": [],
        "wolfenbüttel": [],
        "wolfsburg": [],
        "worms": [],
        "wuppertal": [],
        "würzburg": [],
        "zwickau": []
    },
    "Estland": {
        "abja-paluoja": [],
        "aegviidu": [],
        "antsla": [],
        "elva": [],
        "haapsalu": [],
        "järva-jaani": [],
        "järvakandi": [],
        "jõgeva": [],
        "jõhvi": [],
        "kallaste": [],
        "kärdla": [],
        "karksi-nuia": [],
        "kehra": [],
        "keila": [],
        "kiili": [],
        "kilingi-nõmme": [],
        "kiviõli": [],
        "kohila": [],
        "kohtla-järve": [],
        "kohtla-nõmme": [],
        "kunda": [],
        "kuressaare": [],
        "lavassaare": [],
        "lihula": [],
        "loksa": [],
        "maardu": [],
        "märjamaa": [],
        "mõisaküla": [],
        "mustvee": [],
        "narva": [],
        "narva-jõesuu": [],
        "otepää": [],
        "paide": [],
        "paikuse": [],
        "paldiski": [],
        "pärnu": [],
        "pärnu-jaagupi": [],
        "põltsamaa": [],
        "põlva": [],
        "püssi": [],
        "rakvere": [],
        "räpina": [],
        "rapla": [],
        "saue": [],
        "sillamäe": [],
        "sindi": [],
        "suure-jaani": [],
        "tallinn": [],
        "tamsalu": [],
        "tapa": [],
        "tartu": [],
        "tootsi": [],
        "tõrva": [],
        "türi": [],
        "valga": [],
        "vändra": [],
        "viljandi": [],
        "võhma": [],
        "võru": []
    },
    "Finnland": {
        "äänekoski": [],
        "espoo": [
            "esbo"
        ],
        "hämeenlinna": [],
        "hamina": [],
        "heinola": [],
        "helsinki": [
            "helsingfors"
        ],
        "hollola": [],
        "hyvinkää": [],
        "iisalmi": [],
        "imatra": [],
        "jakobstad": [
            "pietarsaari"
        ],
        "jämsä": [],
        "järvenpää": [],
        "joensuu": [],
        "jyväskylä": [],
        "kaarina": [],
        "kajaani": [],
        "kangasala": [],
        "kemi": [],
        "kerava": [],
        "kirkkonummi": [
            "kyrkslätt"
        ],
        "kokkola": [
            "karleby"
        ],
        "kotka": [],
        "kouvola": [],
        "kuopio": [],
        "kurikka": [],
        "lahti": [],
        "lappeenranta": [],
        "lempäälä": [],
        "lieto": [],
        "lohja": [
            "lojo"
        ],
        "mäntsälä": [],
        "mariehamn": [],
        "mikkeli": [],
        "naantali": [],
        "nokia": [],
        "nurmijärvi": [],
        "oulu": [],
        "pieksämäki": [],
        "pirkkala": [],
        "pori": [],
        "porvoo": [
            "borgå"
        ],
        "raahe": [],
        "raisio": [],
        "raseborg": [
            "raasepori"
        ],
        "rauma": [],
        "riihimäki": [],
        "rovaniemi": [],
        "salo": [],
        "sastamala": [
            "vammala"
        ],
        "savonlinna": [],
        "seinäjoki": [],
        "siilinjärvi": [],
        "sipoo": [
            "sibbo"
        ],
        "tampere": [],
        "tornio": [],
        "turku": [
            "åbo"
        ],
        "tuusula": [],
        "vaasa": [
            "vasa"
        ],
        "valkeakoski": [],
        "vantaa": [
            "vanda"
        ],
        "varkaus": [],
        "vihti": [],
        "ylöjärvi": []
    },
    "Frankreich": {
        "aix-en-provence": [],
        "amiens": [],
        "angers": [],
        "annecy": [],
        "argenteuil": [],
        "besançon": [],
        "bordeaux": [],
        "boulogne-billancourt": [],
        "brest": [],
        "caen": [],
        "clermont-ferrand": [],
        "dijon": [],
        "grenoble": [],
        "le havre": [],
        "le mans": [],
        "lille": [],
        "limoges": [],
        "lyon": [],
        "marseille": [],
        "metz": [],
        "montpellier": [],
        "montreuil": [],
        "mulhouse": [
            "mülhausen"
        ],
        "nancy": [],
        "nantes": [],
        "nice": [
            "nizza"
        ],
        "nîmes": [],
        "orléans": [],
        "paris": [],
        "perpignan": [],
        "reims": [],
        "rennes": [],
        "rouen": [],
        "saint-denis": [],
        "saint-étienne": [],
        "strasbourg": [
            "strassburg"
        ],
        "toulon": [],
        "toulouse": [],
        "tours": [],
        "villeurbanne": []
    },
    "Griechenland": {
        "acharnaí": [
            "acharnes"
        ],
        "ágios nikólaos": [],
        "ágios stéfanos": [],
        "agrínion": [
            "agrinio"
        ],
        "aígion": [
            "egio"
        ],
        "alexándreia": [
            "alexandria"
        ],
        "alexandroúpolis": [
            "alexandroupoli"
        ],
        "amaliás": [
            "amaliada"
        ],
        "áno liósia": [],
        "árgos": [],
        "argostólion": [
            "argostoli"
        ],
        "árta": [],
        "ártemi": [
            "artemida"
        ],
        "asprópyrgos": [],
        "athínai": [
            "athen"
        ],
        "chalkís": [
            "chalkida"
        ],
        "chanía": [],
        "chíos": [
            "chios-stadt"
        ],
        "diavatá": [],
        "dráma": [],
        "édessa": [],
        "elefsís": [
            "eleusis"
        ],
        "ermoúpolis": [
            "ermoupoli"
        ],
        "flórina": [],
        "gázion": [
            "gazi"
        ],
        "giannitsá": [],
        "grevená": [],
        "ierápetra": [],
        "ioánnina": [],
        "irákleion": [
            "iraklio",
            "heraklion"
        ],
        "kalamáta": [],
        "kálymnos": [],
        "kalývia thorikoú": [],
        "kardítsa": [],
        "kastoriá": [],
        "kateríni": [],
        "kavála": [],
        "kérkyra": [
            "korfu-stadt"
        ],
        "kilkís": [],
        "komotiní": [],
        "kórinthos": [
            "korinth"
        ],
        "koropíon": [
            "koropi"
        ],
        "kos": [
            "kos-stadt"
        ],
        "kozáni": [],
        "lamía": [],
        "lárisa": [
            "larissa"
        ],
        "levádeia": [
            "livadia"
        ],
        "limín markopoúlou": [
            "porto rafti"
        ],
        "loutrákion": [
            "loutraki"
        ],
        "mándra": [],
        "markópoulon": [
            "markopoulo"
        ],
        "mégara": [],
        "mesolóngion": [
            "mesolongi"
        ],
        "mytilíni": [],
        "náfpaktos": [],
        "náfplion": [
            "nafplio"
        ],
        "náousa": [
            "naoussa"
        ],
        "néa mákri": [],
        "oraiókastron": [
            "oreokastro"
        ],
        "orestiás": [
            "orestiada"
        ],
        "paianía": [
            "peania"
        ],
        "pallíni": [],
        "pátrai": [
            "patras"
        ],
        "peraía": [],
        "préveza": [],
        "ptolemaḯs": [
            "ptolemaida"
        ],
        "pýrgos": [],
        "rafína": [],
        "réthymnon": [
            "rethymno"
        ],
        "ródos": [
            "rhodos-stadt"
        ],
        "salamís": [],
        "sérrai": [
            "serres"
        ],
        "siteía": [
            "sitia"
        ],
        "spárti": [
            "sparta"
        ],
        "thérmi": [],
        "thessaloníki": [
            "saloniki"
        ],
        "thívai": [
            "thiva",
            "theben"
        ],
        "tríkala": [],
        "trípolis": [
            "tripoli"
        ],
        "týrnavos": [],
        "véroia": [
            "veria"
        ],
        "vólos": [],
        "xánthi": []
    },
    "Grossbritanien": {
        "aberdeen": [],
        "altrincham": [],
        "andover": [],
        "ashford": [],
        "ashton-under-lyne": [],
        "aylesbury": [],
        "banbury": [],
        "bangor": [],
        "barnsley": [],
        "barrow-in-furness": [],
        "barry": [
            "barri"
        ],
        "basildon": [],
        "basingstoke": [],
        "bath": [],
        "bebington": [],
        "bedford": [],
        "beeston": [],
        "belfast": [],
        "birkenhead": [],
        "birmingham": [],
        "blackburn": [],
        "blackpool": [],
        "bloxwich": [],
        "bognor regis": [],
        "bolton": [],
        "bootle": [],
        "bournemouth": [],
        "bracknell": [],
        "bradford": [],
        "brentwood": [],
        "bridgend": [],
        "bridgwater": [],
        "brighton and hove": [],
        "bristol": [],
        "burnley": [],
        "burton upon trent": [],
        "bury": [],
        "cambridge": [],
        "cannock": [],
        "canterbury": [],
        "cardiff": [],
        "carlisle": [],
        "carlton": [],
        "chatham": [],
        "chelmsford": [],
        "cheltenham": [],
        "chester": [],
        "chesterfield": [],
        "clacton-on-sea": [],
        "colchester": [],
        "corby": [],
        "coventry": [],
        "craigavon": [],
        "crawley": [],
        "crewe": [],
        "crosby": [],
        "cumbernauld": [],
        "darlington": [],
        "dartford": [],
        "derby": [],
        "derry": [
            "londonderry"
        ],
        "dewsbury": [],
        "doncaster": [],
        "dudley": [],
        "dundee": [],
        "dunfermline": [],
        "durham": [],
        "east kilbride": [],
        "eastbourne": [],
        "eastleigh": [],
        "edinburgh": [],
        "ellesmere port": [],
        "exeter": [],
        "farnborough": [],
        "folkestone": [],
        "gateshead": [],
        "gillingham": [],
        "glasgow": [],
        "gloucester": [],
        "gosport": [],
        "gravesend": [],
        "grimsby": [],
        "guildford": [],
        "halesowen": [],
        "halifax": [],
        "hamilton": [],
        "harlow": [],
        "harrogate": [],
        "hartlepool": [],
        "hastings": [],
        "hemel hempstead": [],
        "hereford": [],
        "high wycombe": [],
        "hinckley": [],
        "horsham": [],
        "huddersfield": [],
        "huyton with roby": [],
        "ipswich": [],
        "keighley": [],
        "kettering": [],
        "kidderminster": [],
        "kingston upon hull": [
            "hull"
        ],
        "kingswinford": [],
        "kingswood": [
            "fishponds"
        ],
        "kirkcaldy": [],
        "lancaster": [],
        "leeds": [],
        "leicester": [],
        "lincoln": [],
        "lisburn": [],
        "liverpool": [],
        "livingston": [],
        "london": [],
        "loughborough": [],
        "lowestoft": [],
        "luton": [],
        "macclesfield": [],
        "maidenhead": [],
        "maidstone": [],
        "manchester": [],
        "mansfield": [],
        "margate": [],
        "middlesbrough": [],
        "middleton": [],
        "milton keynes": [],
        "newcastle-under-lyme": [],
        "newcastle upon tyne": [],
        "newport": [],
        "northampton": [],
        "norwich": [],
        "nottingham": [],
        "nuneaton": [],
        "oldham": [],
        "oxford": [],
        "paignton": [],
        "paisley": [],
        "peterborough": [],
        "plymouth": [],
        "poole": [],
        "portsmouth": [],
        "preston": [],
        "reading": [],
        "redditch": [],
        "rochdale": [],
        "rochester": [],
        "rotherham": [],
        "royal leamington spa": [],
        "royal sutton coldfield": [
            "sutton coldfield"
        ],
        "royal tunbridge wells": [],
        "rugby": [],
        "runcorn": [],
        "sale": [],
        "salford": [],
        "scarborough": [],
        "scunthorpe": [],
        "sheffield": [],
        "shrewsbury": [],
        "sittingbourne": [],
        "slough": [],
        "smethwick": [],
        "solihull": [],
        "south shields": [],
        "southampton": [],
        "southend-on-sea": [],
        "southport": [],
        "st albans": [],
        "st helens": [],
        "stafford": [],
        "stevenage": [],
        "stockport": [],
        "stockton-on-tees": [],
        "stoke-on-trent": [],
        "stourbridge": [],
        "sunderland": [],
        "swansea": [],
        "swindon": [],
        "tamworth": [],
        "taunton": [],
        "telford": [],
        "thundersley": [
            "south benfleet"
        ],
        "torquay": [],
        "tynemouth": [],
        "wakefield": [],
        "wallasey": [],
        "walsall": [],
        "warrington": [],
        "washington": [],
        "watford": [],
        "wellingborough": [],
        "welwyn garden city": [],
        "west bromwich": [],
        "weston-super-mare": [],
        "weymouth": [],
        "widnes": [],
        "wigan": [],
        "willenhall": [],
        "winchester": [],
        "woking": [],
        "wokingham": [],
        "wolverhampton": [],
        "worcester": [],
        "worthing": [],
        "wythenshawe": [],
        "yeovil": [],
        "york": []
    },
    "Irland": {
        "ardee": [],
        "arklow": [
            "antinbhear mor"
        ],
        "ashbourne": [],
        "athlone": [
            "áth luain"
        ],
        "athy": [],
        "balbriggan": [],
        "ballina": [],
        "ballinasloe": [],
        "ballybofey - stranorlar": [],
        "bandon": [],
        "birr": [],
        "blessington": [
            "ballycomeen"
        ],
        "bray": [
            "brí chualann"
        ],
        "buncrana": [],
        "carlow": [
            "ceatharlach"
        ],
        "carrick-on-suir": [],
        "carrickmacross": [],
        "carrigaline": [],
        "carrigtwohill": [],
        "cashel": [],
        "castlebar": [],
        "cavan": [],
        "celbridge": [],
        "clane": [],
        "clonakilty": [],
        "clonmel": [
            "cluain meala"
        ],
        "cobh": [],
        "cork": [
            "corcaigh"
        ],
        "donabate": [],
        "drogheda": [
            "droichead átha"
        ],
        "dublin": [
            "baile átha cliath"
        ],
        "duleek": [],
        "dunboyne": [],
        "dundalk": [
            "dún dealgan"
        ],
        "dungarvan": [],
        "dunshaughlin": [],
        "edenderry": [],
        "ennis": [
            "inis"
        ],
        "enniscorthy": [],
        "fermoy": [],
        "galway": [
            "an ghaillimh"
        ],
        "gorey": [],
        "greystones": [],
        "kells": [
            "ceannanus mór"
        ],
        "kilcock": [],
        "kildare": [],
        "kilkenny": [
            "cill choinnigh"
        ],
        "killarney": [],
        "kinsale": [],
        "kinsealy - drinan": [],
        "laytown": [],
        "leixlip": [],
        "letterkenny": [],
        "limerick": [
            "luimneach"
        ],
        "listowel": [],
        "longford": [],
        "loughrea": [],
        "lusk": [],
        "malahide": [],
        "mallow": [],
        "maynooth": [],
        "midleton": [],
        "monaghan": [],
        "monasterevin": [],
        "mountmellick": [],
        "mullingar": [],
        "naas": [],
        "navan": [
            "an uaimh"
        ],
        "nenagh": [],
        "new ross": [],
        "newbridge": [
            "droichead nua"
        ],
        "newcastle west": [],
        "oranmore": [],
        "passage west": [],
        "portarlington": [],
        "portlaoise": [
            "maryborough"
        ],
        "portmarnock": [],
        "rathcoole": [],
        "ratoath": [],
        "roscommon": [],
        "roscrea": [],
        "rush": [],
        "sallins": [],
        "shannon": [],
        "skerries": [],
        "sligo": [
            "sligeach"
        ],
        "swords": [],
        "thurles": [],
        "tipperary": [],
        "tralee": [
            "tráighlí"
        ],
        "tramore": [],
        "trim": [],
        "tuam": [],
        "tullamore": [
            "an tulach mhór"
        ],
        "tullow": [],
        "waterford": [
            "port láirge"
        ],
        "westport": [],
        "wexford": [
            "loch garman"
        ],
        "wicklow": [],
        "youghal": []
    },
    "Island": {
        "akranes": [],
        "akureyri": [],
        "álftanes": [],
        "egilsstaðir": [],
        "hveragerði": [],
        "ísafjörður": [],
        "keflavík og njarðvík": [],
        "reykjavík": [],
        "selfoss": [],
        "vestmannaeyjar": []
    },
    "Italien": {
        "acerra": [],
        "acireale": [],
        "afragola": [],
        "agrigento": [],
        "alessandria": [],
        "altamura": [],
        "ancona": [],
        "andria": [],
        "anzio": [],
        "aprilia": [],
        "ardea": [],
        "arezzo": [],
        "asti": [],
        "avellino": [],
        "bagheria": [],
        "bari": [],
        "barletta": [],
        "benevento": [],
        "bergamo": [],
        "bisceglie": [],
        "bitonto": [],
        "bologna": [],
        "bolzano": [
            "bozen"
        ],
        "brescia": [],
        "brindisi": [],
        "busto arsizio": [],
        "cagliari": [],
        "caltanissetta": [],
        "carpi": [],
        "carrara": [],
        "caserta": [],
        "casoria": [],
        "castellammare di stabia": [],
        "catania": [],
        "catanzaro": [],
        "cerignola": [],
        "cesena": [],
        "cinisello balsamo": [],
        "civitavecchia": [],
        "como": [],
        "corigliano-rossano": [],
        "cosenza": [],
        "cremona": [],
        "crotone": [],
        "cuneo": [],
        "faenza": [],
        "fano": [],
        "ferrara": [],
        "firenze": [
            "florenz"
        ],
        "fiumicino": [],
        "foggia": [],
        "foligno": [],
        "forlì": [],
        "gallarate": [],
        "gela": [],
        "genova": [
            "genua"
        ],
        "giugliano in campania": [],
        "grosseto": [],
        "guidonia montecelio": [],
        "imola": [],
        "l'aquila": [],
        "la spezia": [],
        "lamezia terme": [
            "nicastro"
        ],
        "latina": [],
        "lecce": [],
        "legnano": [],
        "livorno": [],
        "lucca": [],
        "manfredonia": [],
        "mantova": [
            "mantua"
        ],
        "marano di napoli": [],
        "marsala": [],
        "massa": [],
        "matera": [],
        "mazara del vallo": [],
        "messina": [],
        "milano": [
            "mailand"
        ],
        "modena": [],
        "modica": [],
        "molfetta": [],
        "moncalieri": [],
        "montesilvano": [],
        "monza": [],
        "napoli": [
            "neapel"
        ],
        "novara": [],
        "olbia": [],
        "padova": [
            "padua"
        ],
        "palermo": [],
        "parma": [],
        "pavia": [],
        "perugia": [],
        "pesaro": [],
        "pescara": [],
        "piacenza": [],
        "pisa": [],
        "pistoia": [],
        "pomezia": [],
        "pordenone": [],
        "portici": [],
        "potenza": [],
        "pozzuoli": [],
        "prato": [],
        "quartu sant'elena": [],
        "ragusa": [],
        "ravenna": [],
        "reggio di calabria": [],
        "reggio nell'emilia": [],
        "rho": [],
        "rimini": [],
        "roma": [
            "rom"
        ],
        "salerno": [],
        "sanremo": [
            "san remo"
        ],
        "sassari": [],
        "savona": [],
        "sesto san giovanni": [],
        "siena": [],
        "siracusa": [
            "syrakus"
        ],
        "taranto": [
            "tarent"
        ],
        "teramo": [],
        "terni": [],
        "tivoli": [],
        "torino": [
            "turin"
        ],
        "torre del greco": [],
        "trani": [],
        "trapani": [],
        "trento": [
            "trient"
        ],
        "treviso": [],
        "trieste": [
            "triest"
        ],
        "udine": [],
        "varese": [],
        "velletri": [],
        "venezia": [
            "venedig"
        ],
        "verona": [],
        "viareggio": [],
        "vicenza": [],
        "vigevano": [],
        "viterbo": [],
        "vittoria": []
    },
    "Kosovo": {
        "ferizaj": [],
        "fushë kosovë": [],
        "gjakovë": [],
        "gjilan": [],
        "matiçan": [],
        "mitrovicë": [],
        "pejë": [],
        "prishtinë": [],
        "prizren": [],
        "vushtrri": []
    },
    "Kroatien": {
        "đakovo": [],
        "bjelovar": [],
        "čakovec": [],
        "dubrovnik": [],
        "dugo selo": [],
        "gospić": [],
        "karlovac": [],
        "kastav": [],
        "koprivnica": [],
        "krapina": [],
        "križevci": [],
        "kutina": [],
        "makarska": [],
        "metković": [],
        "nova gradiška": [],
        "osijek": [],
        "pazin": [],
        "petrinja": [],
        "podstrana": [],
        "požega": [
            "slavonska požega"
        ],
        "pula": [
            "pola"
        ],
        "rijeka": [],
        "rovinj": [],
        "samobor": [],
        "sesvete": [],
        "šibenik": [],
        "sinj": [],
        "sisak": [],
        "slavonski brod": [],
        "solin": [],
        "split": [],
        "trogir": [],
        "varaždin": [],
        "velika gorica": [],
        "vinkovci": [],
        "virovitica": [],
        "vukovar": [],
        "zadar": [],
        "zagreb": [],
        "zaprešić": []
    },
    "Lettland": {
        "daugavpils": [],
        "jēkabpils": [],
        "jelgava": [],
        "jūrmala": [],
        "liepāja": [],
        "ogre": [],
        "rēzekne": [],
        "rīga": [],
        "valmiera": [],
        "ventspils": []
    },
    "Liechtenstein": {
        "balzers": [],
        "eschen": [],
        "mauren": [],
        "ruggell": [],
        "schaan": [],
        "triesen": [],
        "triesenberg": [],
        "vaduz": []
    },
    "Litauen": {
        "akmenė": [],
        "alytus": [],
        "anykščiai": [],
        "ariogala": [],
        "baltoji vokė": [],
        "birštonas": [],
        "biržai": [],
        "daugai": [],
        "druskininkai": [],
        "dūkštas": [],
        "dusetos": [],
        "eišiškės": [],
        "elektrėnai": [],
        "ežerėlis": [],
        "gargždai": [],
        "garliava": [],
        "gelgaudiškis": [],
        "grigiškės": [],
        "ignalina": [],
        "jieznas": [],
        "jonava": [],
        "joniškėlis": [],
        "joniškis": [],
        "jurbarkas": [],
        "kaišiadorys": [],
        "kalvarija": [],
        "kaunas": [],
        "kavarskas": [],
        "kazlų rūda": [],
        "kėdainiai": [],
        "kelmė": [],
        "klaipėda": [
            "memel"
        ],
        "kretinga": [],
        "kudirkos naumiestis": [],
        "kupiškis": [],
        "kuršėnai": [],
        "kybartai": [],
        "lazdijai": [],
        "lentvaris": [],
        "linkuva": [],
        "marijampolė": [
            "kapsukas"
        ],
        "mažeikiai": [],
        "molėtai": [],
        "naujoji akmenė": [],
        "nemenčinė": [],
        "neringa": [],
        "obeliai": [],
        "pabradė": [],
        "pagėgiai": [],
        "pakruojis": [],
        "palanga": [],
        "pandėlys": [],
        "panemunė": [],
        "panevėžys": [],
        "pasvalys": [],
        "plungė": [],
        "priekulė": [],
        "prienai": [],
        "radviliškis": [],
        "ramygala": [],
        "raseiniai": [],
        "rietavas": [],
        "rokiškis": [],
        "rūdiškės": [],
        "šakiai": [],
        "salantai": [],
        "šalčininkai": [],
        "seda": [],
        "šeduva": [],
        "šiauliai": [],
        "šilalė": [],
        "šilutė": [],
        "simnas": [],
        "širvintos": [],
        "skaudvilė": [],
        "skuodas": [],
        "smalininkai": [],
        "subačius": [],
        "švenčionėliai": [],
        "švenčionys": [],
        "tauragė": [],
        "telšiai": [],
        "trakai": [],
        "troškūnai": [],
        "tytuvėnai": [],
        "ukmergė": [],
        "utena": [],
        "užventis": [],
        "vabalninkas": [],
        "varėna": [],
        "varniai": [],
        "veisiejai": [],
        "venta": [],
        "viekšniai": [],
        "vievis": [],
        "vilkaviškis": [],
        "vilkija": [],
        "vilnius": [
            "wilna"
        ],
        "virbalis": [],
        "visaginas": [
            "sniečkus"
        ],
        "žagarė": [],
        "zarasai": [],
        "žiežmariai": []
    },
    "Luxemburg": {
        "beaufort": [
            "beefort",
            "befort"
        ],
        "bertrange": [
            "bartreng",
            "bartringen"
        ],
        "bettembourg": [
            "beetebuerg",
            "bettemburg"
        ],
        "bettendorf": [
            "bettenduerf"
        ],
        "betzdorf": [
            "betzder"
        ],
        "bissen": [
            "biissen"
        ],
        "bous-waldbredimus": [
            "bus-waldbriedemes"
        ],
        "clervaux": [
            "klierf",
            "cliärref",
            "clerf"
        ],
        "contern": [
            "konter"
        ],
        "diekirch": [
            "dikrech"
        ],
        "differdange": [
            "déifferdeng",
            "differdingen"
        ],
        "dippach": [
            "dippech"
        ],
        "dudelange": [
            "diddeleng",
            "düdelingen"
        ],
        "echternach": [
            "iechternach"
        ],
        "esch-sur-alzette": [
            "esch-uelzecht",
            "esch an der alzette"
        ],
        "esch-sur-sûre": [
            "esch-sauer"
        ],
        "ettelbruck": [
            "ettelbréck",
            "ettelbrück"
        ],
        "frisange": [
            "fréiseng",
            "frisingen"
        ],
        "grevenmacher": [
            "gréiwemaacher"
        ],
        "habscht": [],
        "helperknapp": [],
        "hesperange": [
            "hesper",
            "hesperingen"
        ],
        "junglinster": [
            "jonglënster"
        ],
        "käerjeng": [],
        "kayl": [
            "keel",
            "käl"
        ],
        "kehlen": [
            "kielen"
        ],
        "kopstal": [
            "koplescht"
        ],
        "lintgen": [],
        "lorentzweiler": [
            "luerenzweiler"
        ],
        "luxembourg": [
            "lëtzebuerg",
            "luxemburg"
        ],
        "mamer": [],
        "mersch": [
            "miersch"
        ],
        "mertert": [
            "mäertert"
        ],
        "mondercange": [
            "monnerech",
            "monnerich"
        ],
        "mondorf-les-bains": [
            "munneref",
            "bad mondorf"
        ],
        "niederanven": [
            "nidderaanwen",
            "niederanwen"
        ],
        "parc hosingen": [
            "parc housen"
        ],
        "pétange": [
            "péiteng",
            "petingen"
        ],
        "rambrouch": [
            "rammerech",
            "rambruch"
        ],
        "reckange-sur-mess": [
            "recken",
            "reckeng op der mess"
        ],
        "redange-sur-attert": [
            "réiden",
            "redingen"
        ],
        "remich": [
            "réimech"
        ],
        "roeser": [
            "réiser"
        ],
        "rosport-mompach": [
            "rouspert-mompech"
        ],
        "rumelange": [
            "rëmeleng",
            "rümelingen"
        ],
        "sandweiler": [],
        "sanem": [
            "suessem",
            "sassenheim"
        ],
        "schengen": [],
        "schifflange": [
            "schëffleng",
            "schifflingen"
        ],
        "schuttrange": [
            "schëtter",
            "schüttringen"
        ],
        "steinfort": [
            "stengefort"
        ],
        "steinsel": [
            "steesel"
        ],
        "strassen": [
            "stroossen"
        ],
        "troisvierges": [
            "ëlwen",
            "ulflingen"
        ],
        "vallée de l'ernz": [
            "ärenzdallgemeng"
        ],
        "vianden": [
            "veianen",
            "veinen"
        ],
        "walferdange": [
            "walfer",
            "walferdingen"
        ],
        "wiltz": [
            "wolz"
        ],
        "wincrange": [
            "wëntger",
            "wintger"
        ],
        "wormeldange": [
            "wuermeldeng",
            "wormer",
            "wormeldingen"
        ]
    },
    "Malta": {
        "birkirkara": [],
        "marsaskala": [],
        "mosta": [],
        "naxxar": [],
        "qormi": [],
        "san pawl il-baħar": [],
        "sliema": [],
        "żabbar": []
    },
    "Moldawien": {
        "anenii noi": [],
        "bălți": [
            "bel'cy"
        ],
        "basarabeasca": [],
        "biruința": [],
        "briceni": [],
        "bucovăț": [],
        "cahul": [],
        "căinari": [],
        "călărași": [],
        "camenca": [
            "kamenka"
        ],
        "cantemir": [],
        "căușeni": [],
        "ceadîr-lunga": [],
        "chișinău": [
            "kišin'ov",
            "kischinau"
        ],
        "cimișlia": [],
        "codru": [],
        "comrat": [],
        "cornești": [],
        "costești": [],
        "crasnoe": [
            "krasnoe"
        ],
        "cricova": [],
        "criuleni": [],
        "cupcini": [],
        "dnestrovsk": [
            "dnestrovsc"
        ],
        "dondușeni": [],
        "drochia": [],
        "dubăsari": [
            "dubossary"
        ],
        "durlești": [],
        "edineț": [],
        "fălești": [],
        "florești": [],
        "frunză": [],
        "ghindești": [],
        "glodeni": [],
        "grigoriopol": [
            "grigoriopol'"
        ],
        "hîncești": [],
        "ialoveni": [],
        "iargara": [],
        "leova": [],
        "lipcani": [],
        "maiac": [
            "majak"
        ],
        "mărculești": [],
        "nisporeni": [],
        "ocnița": [],
        "orhei": [],
        "otaci": [],
        "pervomaisc": [
            "pervomajsk"
        ],
        "rezina": [],
        "rîbnița": [
            "rybnica"
        ],
        "rîșcani": [],
        "sîngera": [],
        "sîngerei": [],
        "slobozia": [
            "slobodzeja"
        ],
        "șoldănești": [],
        "soroca": [],
        "ștefan vodă": [],
        "strășeni": [],
        "taraclia": [],
        "telenești": [],
        "tighina": [
            "bendery"
        ],
        "tiraspol": [
            "tiraspol'"
        ],
        "tvardița": [],
        "ungheni": [],
        "vadul lui vodă": [],
        "vatra": [],
        "vulcănești": []
    },
    "Montenegro": {
        "andrijevica": [],
        "bar": [],
        "berane": [],
        "bijelo polje": [],
        "budva": [],
        "cetinje": [],
        "danilovgrad": [],
        "gusinje": [],
        "herceg novi": [],
        "kolašin": [],
        "kotor": [],
        "mojkovac": [],
        "nikšić": [],
        "petnjica": [],
        "plav": [],
        "pljevlja": [],
        "plužine": [],
        "podgorica": [],
        "rožaje": [],
        "šavnik": [],
        "tivat": [],
        "tuzi": [],
        "ulcinj": [],
        "žabljak": [],
        "zeta": []
    },
    "Niederlande": {
        "aa en hunze": [],
        "aalsmeer": [],
        "aalten": [],
        "achtkarspelen": [],
        "alblasserdam": [],
        "albrandswaard": [],
        "alkmaar": [],
        "almelo": [],
        "almere": [],
        "alphen aan den rijn": [],
        "alphen-chaam": [],
        "altena": [],
        "ameland": [],
        "amersfoort": [],
        "amstelveen": [],
        "amsterdam": [],
        "apeldoorn": [],
        "arnhem": [],
        "assen": [],
        "asten": [],
        "baarle-nassau": [],
        "baarn": [],
        "barendrecht": [],
        "barneveld": [],
        "beek": [
            "l."
        ],
        "beekdaelen": [],
        "beesel": [],
        "berg en dal": [
            "groesbeek"
        ],
        "bergeijk": [],
        "bergen": [
            "l.",
            "nh."
        ],
        "bergen op zoom": [],
        "berkelland": [],
        "bernheze": [],
        "best": [],
        "beuningen": [],
        "beverwijk": [],
        "bladel": [],
        "blaricum": [],
        "bloemendaal": [],
        "bodegraven-reeuwijk": [],
        "boekel": [],
        "borger-odoorn": [],
        "borne": [],
        "borsele": [],
        "boxtel": [],
        "breda": [],
        "bronckhorst": [],
        "brummen": [],
        "brunssum": [],
        "bunnik": [],
        "bunschoten": [],
        "buren": [],
        "capelle aan den ijssel": [],
        "castricum": [],
        "coevorden": [],
        "cranendonck": [],
        "culemborg": [],
        "dalfsen": [],
        "dantumadiel": [
            "dantumadeel"
        ],
        "de bilt": [],
        "de fryske marren": [],
        "de ronde venen": [],
        "de wolden": [],
        "delft": [],
        "den helder": [],
        "deurne": [],
        "deventer": [],
        "diemen": [],
        "dijk en waard": [],
        "dinkelland": [],
        "doesburg": [],
        "doetinchem": [],
        "dongen": [],
        "dordrecht": [],
        "drechterland": [],
        "drimmelen": [],
        "dronten": [],
        "druten": [],
        "duiven": [],
        "echt-susteren": [],
        "edam-volendam": [],
        "ede": [],
        "eemnes": [],
        "eemsdelta": [],
        "eersel": [],
        "eijsden-margraten": [],
        "eindhoven": [],
        "elburg": [],
        "emmen": [],
        "enkhuizen": [],
        "enschede": [],
        "epe": [],
        "ermelo": [],
        "etten-leur": [],
        "geertruidenberg": [],
        "geldrop-mierlo": [],
        "gemert-bakel": [],
        "gennep": [],
        "gilze en rijen": [],
        "goeree-overflakkee": [],
        "goes": [],
        "goirle": [],
        "gooise meren": [],
        "gorinchem": [],
        "gouda": [],
        "groningen": [],
        "gulpen-wittem": [],
        "haaksbergen": [],
        "haarlem": [],
        "haarlemmermeer": [],
        "halderberge": [],
        "hardenberg": [],
        "harderwijk": [],
        "hardinxveld-giessendam": [],
        "harlingen": [],
        "hattem": [],
        "heemskerk": [],
        "heemstede": [],
        "heerde": [],
        "heerenveen": [],
        "heerlen": [],
        "heeze-leende": [],
        "heiloo": [],
        "hellendoorn": [],
        "helmond": [],
        "hendrik-ido-ambacht": [],
        "hengelo": [
            "o."
        ],
        "het hogeland": [],
        "heumen": [],
        "heusden": [],
        "hillegom": [],
        "hilvarenbeek": [],
        "hilversum": [],
        "hoeksche waard": [],
        "hof van twente": [],
        "hollands kroon": [],
        "hoogeveen": [],
        "hoorn": [],
        "horst aan de maas": [],
        "houten": [],
        "huizen": [],
        "hulst": [],
        "ijsselstein": [],
        "kaag en braassem": [],
        "kampen": [],
        "kapelle": [],
        "katwijk": [],
        "kerkrade": [],
        "koggenland": [],
        "krimpen aan den ijssel": [],
        "krimpenerwaard": [],
        "laarbeek": [],
        "land van cuijk": [],
        "landgraaf": [],
        "landsmeer": [],
        "lansingerland": [],
        "laren": [
            "nh."
        ],
        "leeuwarden": [],
        "leiden": [],
        "leiderdorp": [],
        "leidschendam-voorburg": [],
        "lelystad": [],
        "leudal": [],
        "leusden": [],
        "lingewaard": [],
        "lisse": [],
        "lochem": [],
        "loon op zand": [],
        "lopik": [],
        "losser": [],
        "maasdriel": [],
        "maasgouw": [],
        "maashorst": [],
        "maassluis": [],
        "maastricht": [],
        "medemblik": [],
        "meerssen": [],
        "meierijstad": [],
        "meppel": [],
        "middelburg": [
            "middelburg z"
        ],
        "midden-delfland": [],
        "midden-drenthe": [],
        "midden-groningen": [],
        "moerdijk": [],
        "molenlanden": [],
        "montferland": [],
        "montfoort": [],
        "mook en middelaar": [],
        "neder-betuwe": [],
        "nederweert": [],
        "nieuwegein": [],
        "nieuwkoop": [],
        "nijkerk": [],
        "nijmegen": [],
        "nissewaard": [],
        "noardeast-fryslân": [],
        "noord-beveland": [],
        "noordenveld": [],
        "noordoostpolder": [],
        "noordwijk": [],
        "nuenen, gerwen en nederwetten": [],
        "nunspeet": [],
        "oegstgeest": [],
        "oirschot": [],
        "oisterwijk": [
            "wijk"
        ],
        "oldambt": [],
        "oldebroek": [],
        "oldenzaal": [],
        "olst-wijhe": [],
        "ommen": [],
        "oost gelre": [
            "groenlo"
        ],
        "oosterhout": [],
        "ooststellingwerf": [],
        "oostzaan": [],
        "opmeer": [],
        "opsterland": [],
        "oss": [],
        "oude ijsselstreek": [],
        "ouder-amstel": [],
        "oudewater": [],
        "overbetuwe": [],
        "papendrecht": [],
        "peel en maas": [],
        "pekela": [],
        "pijnacker-nootdorp": [],
        "purmerend": [],
        "putten": [],
        "raalte": [],
        "reimerswaal": [],
        "renkum": [],
        "renswoude": [],
        "reusel-de mierden": [],
        "rheden": [],
        "rhenen": [],
        "ridderkerk": [],
        "rijssen-holten": [],
        "rijswijk": [
            "zh."
        ],
        "roerdalen": [],
        "roermond": [],
        "roosendaal": [],
        "rotterdam": [],
        "rozendaal": [],
        "rucphen": [],
        "'s-gravenhage": [
            "den haag"
        ],
        "'s-hertogenbosch": [
            "herzogenbosch"
        ],
        "schagen": [],
        "scherpenzeel": [],
        "schiedam": [],
        "schiermonnikoog": [],
        "schouwen-duiveland": [],
        "simpelveld": [],
        "sint-michielsgestel": [],
        "sittard-geleen": [],
        "sliedrecht": [],
        "sluis": [],
        "smallingerland": [],
        "soest": [],
        "someren": [],
        "son en breugel": [],
        "stadskanaal": [],
        "staphorst": [],
        "stede broec": [],
        "steenbergen": [],
        "steenwijkerland": [],
        "stein": [
            "l."
        ],
        "stichtse vecht": [],
        "súdwest-fryslân": [],
        "terneuzen": [],
        "terschelling": [],
        "texel": [],
        "teylingen": [],
        "tholen": [],
        "tiel": [],
        "tilburg": [],
        "tubbergen": [],
        "twenterand": [],
        "tynaarlo": [],
        "tytsjerksteradiel": [
            "tietjerksteradeel"
        ],
        "uitgeest": [],
        "uithoorn": [],
        "urk": [],
        "utrecht": [],
        "utrechtse heuvelrug": [],
        "vaals": [],
        "valkenburg aan de geul": [],
        "valkenswaard": [],
        "veendam": [],
        "veenendaal": [],
        "veere": [],
        "veldhoven": [],
        "velsen": [],
        "venlo": [],
        "venray": [],
        "vijfheerenlanden": [],
        "vlaardingen": [],
        "vlieland": [],
        "vlissingen": [],
        "voerendaal": [],
        "voorne aan zee": [],
        "voorschoten": [],
        "voorst": [],
        "vught": [],
        "waadhoeke": [],
        "waalre": [],
        "waalwijk": [],
        "waddinxveen": [],
        "wageningen": [],
        "wassenaar": [],
        "waterland": [],
        "weert": [],
        "west betuwe": [],
        "west maas en waal": [],
        "westerkwartier": [],
        "westerveld": [],
        "westervoort": [],
        "westerwolde": [],
        "westland": [],
        "weststellingwerf": [],
        "wierden": [],
        "wijchen": [],
        "wijdemeren": [],
        "wijk bij duurstede": [],
        "winterswijk": [],
        "woensdrecht": [],
        "woerden": [],
        "wormerland": [],
        "woudenberg": [],
        "zaanstad": [],
        "zaltbommel": [],
        "zandvoort": [],
        "zeewolde": [],
        "zeist": [],
        "zevenaar": [],
        "zoetermeer": [],
        "zoeterwoude": [],
        "zuidplas": [],
        "zundert": [],
        "zutphen": [],
        "zwartewaterland": [],
        "zwijndrecht": [],
        "zwolle": []
    },
    "Nordmazedonien": {
        "aračinovo": [],
        "batinci": [],
        "berovo": [],
        "bitola": [],
        "bogdanci": [],
        "bogovinje": [],
        "čegrane": [],
        "čelopek": [],
        "debar": [],
        "delčevo": [],
        "dobri dol": [],
        "dračevo": [],
        "gevgelija": [],
        "gostivar": [],
        "ilinden": [],
        "kamenjane": [],
        "kavadarci": [],
        "kičevo": [],
        "kočani": [],
        "kratovo": [],
        "kriva palanka": [],
        "kruševo": [],
        "kumanovo": [],
        "labuništa": [],
        "makedonska kamenica": [],
        "marino": [],
        "negotino": [],
        "ohrid": [],
        "pirok": [],
        "prilep": [],
        "probištip": [],
        "radišani": [],
        "radoviš": [],
        "resen": [
            "resno"
        ],
        "singeliḱ": [],
        "skopje": [],
        "štip": [],
        "struga": [],
        "strumica": [],
        "studeničani": [],
        "sveti nikole": [],
        "tetovo": [],
        "veles": [
            "titov veles"
        ],
        "velešta": [],
        "vinica": [],
        "volkovo": [],
        "vrapčište": []
    },
    "Norwegen": {
        "ålesund": [],
        "alta": [],
        "alver": [],
        "arendal": [],
        "ås": [],
        "asker": [],
        "askøy": [],
        "bærum": [],
        "bergen": [],
        "bjørnafjorden": [],
        "bodø": [],
        "drammen": [],
        "eidsvoll": [],
        "elverum": [],
        "færder": [],
        "fredrikstad": [],
        "gjøvik": [],
        "grimstad": [],
        "hå": [],
        "halden": [],
        "hamar": [],
        "harstad": [],
        "haugesund": [],
        "holmestrand": [],
        "horten": [],
        "indre østfold": [],
        "karmøy": [],
        "klepp": [],
        "kongsberg": [],
        "kristiansand": [],
        "kristiansund": [],
        "larvik": [],
        "levanger": [],
        "lier": [],
        "lillehammer": [],
        "lillestrøm": [],
        "lindesnes": [],
        "lørenskog": [],
        "molde": [],
        "moss": [],
        "narvik": [],
        "nes": [],
        "nesodden": [],
        "nittedal": [],
        "nordre follo": [],
        "oslo": [],
        "øvre eiker": [],
        "øygarden": [],
        "porsgrunn": [],
        "rælingen": [],
        "rana": [],
        "ringerike": [],
        "ringsaker": [],
        "sandefjord": [],
        "sandnes": [],
        "sarpsborg": [],
        "skien": [],
        "sola": [],
        "stange": [],
        "stavanger": [],
        "steinkjer": [],
        "stjørdal": [],
        "sunnfjord": [],
        "time": [],
        "tønsberg": [],
        "tromsø": [],
        "trondheim": [],
        "ullensaker": [],
        "vadsø": [],
        "vestby": []
    },
    "Österreich": {
        "altmünster": [],
        "amstetten": [],
        "ansfelden": [],
        "bad ischl": [],
        "bad vöslau": [],
        "baden": [],
        "bischofshofen": [],
        "bludenz": [],
        "braunau am inn": [],
        "bregenz": [],
        "bruck an der mur": [],
        "brunn am gebirge": [],
        "deutschlandsberg": [],
        "dornbirn": [],
        "ebreichsdorf": [],
        "eisenstadt": [],
        "enns": [],
        "feldbach": [],
        "feldkirch": [],
        "feldkirchen in kärnten": [],
        "fürstenfeld": [],
        "gänserndorf": [],
        "gerasdorf bei wien": [],
        "gleisdorf": [],
        "gmunden": [],
        "götzis": [],
        "gratwein-strassengel": [],
        "graz": [],
        "gross-enzersdorf": [],
        "hall in tirol": [],
        "hallein": [],
        "hard": [],
        "hohenems": [],
        "hollabrunn": [],
        "imst": [],
        "innsbruck": [],
        "judenburg": [],
        "kapfenberg": [],
        "klagenfurt am wörthersee": [],
        "klosterneuburg": [],
        "knittelfeld": [],
        "köflach": [],
        "korneuburg": [],
        "krems an der donau": [],
        "kufstein": [],
        "laakirchen": [],
        "lauterach": [],
        "leibnitz": [],
        "leoben": [],
        "leonding": [],
        "lienz": [],
        "linz": [],
        "lustenau": [],
        "marchtrenk": [],
        "mistelbach": [],
        "mödling": [],
        "neunkirchen": [],
        "perchtoldsdorf": [],
        "purkersdorf": [],
        "rankweil": [],
        "ried im innkreis": [],
        "saalfelden am steinernen meer": [],
        "salzburg": [],
        "sankt andrä": [],
        "sankt johann im pongau": [],
        "sankt johann in tirol": [],
        "sankt pölten": [],
        "sankt veit an der glan": [],
        "schwaz": [],
        "schwechat": [],
        "seekirchen am wallersee": [],
        "seiersberg-pirka": [],
        "sierning": [],
        "spittal an der drau": [],
        "steyr": [],
        "stockerau": [],
        "strasshof an der nordbahn": [],
        "telfs": [],
        "ternitz": [],
        "traiskirchen": [],
        "traun": [],
        "trofaiach": [],
        "tulln an der donau": [],
        "villach": [],
        "vöcklabruck": [],
        "voitsberg": [],
        "völkermarkt": [],
        "waidhofen an der ybbs": [],
        "wals-siezenheim": [],
        "weiz": [],
        "wels": [],
        "wien": [],
        "wiener neustadt": [],
        "wolfsberg": [],
        "wörgl": [],
        "zell am see": [],
        "zwettl-niederösterreich": []
    },
    "Polen": {
        "aleksandrów łódzki": [],
        "andrychów": [],
        "augustów": [],
        "łaziska górne": [],
        "bartoszyce": [
            "bartenstein"
        ],
        "bełchatów": [],
        "będzin": [
            "bendzin"
        ],
        "biłgoraj": [],
        "biała podlaska": [],
        "białogard": [
            "belgard"
        ],
        "białystok": [],
        "bielawa": [
            "langenbielau"
        ],
        "bielsk podlaski": [],
        "bielsko-biała": [
            "bielitz-biala"
        ],
        "bieruń": [],
        "bochnia": [
            "salzberg"
        ],
        "bolesławiec": [
            "bunzlau"
        ],
        "brodnica": [
            "strasburg"
        ],
        "brzeg": [
            "brieg"
        ],
        "bydgoszcz": [
            "bromberg"
        ],
        "bytom": [
            "beuthen"
        ],
        "chełm": [],
        "chełmno": [
            "culm"
        ],
        "chodzież": [],
        "chojnice": [
            "konitz"
        ],
        "chorzów": [
            "könighütte"
        ],
        "chrzanów": [
            "krenau"
        ],
        "ciechanów": [],
        "cieszyn": [],
        "czechowice-dziedzice": [],
        "czeladź": [],
        "czerwionka-leszczyny": [],
        "częstochowa": [
            "tschenstochau"
        ],
        "dąbrowa górnicza": [
            "dombrowa"
        ],
        "dębica": [],
        "działdowo": [
            "soldau"
        ],
        "dzierżoniów": [
            "reichenbach"
        ],
        "ełk": [
            "lyck"
        ],
        "łęczna": [],
        "elbląg": [
            "elbing"
        ],
        "głogów": [
            "glogau"
        ],
        "gdańsk": [
            "danzig"
        ],
        "gdynia": [
            "gdingen"
        ],
        "giżycko": [
            "lötzen"
        ],
        "gliwice": [
            "gleiwitz"
        ],
        "gniezno": [
            "gnesen"
        ],
        "goleniów": [
            "gollnow"
        ],
        "gorlice": [
            "görlitz"
        ],
        "gorzów wielkopolski": [
            "landsberg"
        ],
        "gostyń": [],
        "gostynin": [],
        "grajewo": [],
        "grodzisk mazowiecki": [],
        "grudziądz": [
            "graudenz"
        ],
        "gryfino": [
            "greifenhagen"
        ],
        "hajnówka": [],
        "iława": [
            "eylau"
        ],
        "inowrocław": [
            "hohensalza"
        ],
        "jarocin": [],
        "jarosław": [],
        "jasło": [],
        "jastrzębie-zdrój": [],
        "jawor": [
            "jauer"
        ],
        "jaworzno": [
            "arnshalde"
        ],
        "jelenia góra": [
            "hirschberg"
        ],
        "józefów": [],
        "kłodzko": [
            "glatz"
        ],
        "kalisz": [
            "kalisch"
        ],
        "kamienna góra": [
            "landeshut"
        ],
        "katowice": [
            "kattowitz"
        ],
        "kędzierzyn-koźle": [
            "kandrzin-cosel"
        ],
        "kętrzyn": [
            "rastenburg"
        ],
        "kielce": [],
        "kluczbork": [
            "kreuzburg"
        ],
        "knurów": [],
        "koło": [
            "wartbrücken"
        ],
        "kołobrzeg": [
            "kolberg"
        ],
        "kobyłka": [],
        "konin": [],
        "końskie": [],
        "kościan": [
            "kosten"
        ],
        "kościerzyna": [
            "berent"
        ],
        "koszalin": [
            "köslin"
        ],
        "kozienice": [],
        "kraków": [
            "krakau"
        ],
        "kraśnik": [],
        "krasnystaw": [],
        "krosno": [],
        "krotoszyn": [
            "krotoschin"
        ],
        "kutno": [],
        "kwidzyn": [
            "marienwerder"
        ],
        "lębork": [
            "lauenburg"
        ],
        "legionowo": [],
        "legnica": [
            "liegnitz"
        ],
        "leszno": [
            "lissa"
        ],
        "lubań": [
            "lauban"
        ],
        "lubartów": [],
        "lubin": [
            "lüben"
        ],
        "lublin": [],
        "lubliniec": [],
        "luboń": [
            "luban"
        ],
        "mława": [],
        "malbork": [
            "marienburg"
        ],
        "marki": [],
        "mielec": [],
        "mikołów": [],
        "mińsk mazowiecki": [],
        "mrągowo": [
            "sensburg"
        ],
        "mysłowice": [
            "myslowitz"
        ],
        "myszków": [],
        "nakło nad notecią": [],
        "nowa ruda": [
            "neurode"
        ],
        "nowa sól": [
            "neusalz"
        ],
        "nowy dwór mazowiecki": [],
        "nowy sącz": [
            "neusandez"
        ],
        "nowy targ": [
            "neumarkt"
        ],
        "nysa": [
            "neisse"
        ],
        "oława": [
            "ohlau"
        ],
        "łódź": [
            "lodsch"
        ],
        "oleśnica": [
            "oels"
        ],
        "olkusz": [
            "ilkenau"
        ],
        "olsztyn": [
            "allenstein"
        ],
        "łomża": [],
        "opoczno": [],
        "opole": [
            "oppeln"
        ],
        "orzesze": [],
        "ostrołęka": [],
        "ostróda": [
            "osterode"
        ],
        "ostrów mazowiecka": [],
        "ostrów wielkopolski": [
            "ostrowo"
        ],
        "ostrowiec świętokrzyski": [],
        "oświęcim": [
            "auschwitz"
        ],
        "otwock": [],
        "łowicz": [],
        "ozorków": [],
        "płock": [],
        "płońsk": [],
        "pabianice": [],
        "piła": [
            "schneidemühl"
        ],
        "piaseczno": [],
        "piastów": [],
        "piekary śląskie": [],
        "pionki": [],
        "piotrków trybunalski": [
            "petrikau"
        ],
        "police": [
            "pölitz"
        ],
        "polkowice": [
            "polkwitz"
        ],
        "poznań": [
            "posen"
        ],
        "prudnik": [
            "neustadt"
        ],
        "pruszcz gdański": [
            "praust"
        ],
        "pruszków": [],
        "przemyśl": [],
        "pszczyna": [],
        "puławy": [],
        "pyskowice": [],
        "racibórz": [
            "ratibor"
        ],
        "radom": [],
        "radomsko": [],
        "rawicz": [
            "rawitsch"
        ],
        "reda": [],
        "ruda śląska": [],
        "rumia": [
            "rahmel"
        ],
        "rybnik": [],
        "rydułtowy": [],
        "rzeszów": [],
        "słupsk": [
            "stolp"
        ],
        "sandomierz": [],
        "sanok": [],
        "siedlce": [],
        "siemianowice śląskie": [
            "siemianowitz"
        ],
        "sieradz": [],
        "skarżysko-kamienna": [],
        "skawina": [
            "konradshof"
        ],
        "skierniewice": [],
        "sochaczew": [],
        "sopot": [
            "zoppot"
        ],
        "sosnowiec": [
            "sosnowitz"
        ],
        "śrem": [
            "schrimm"
        ],
        "środa wielkopolska": [
            "schroda"
        ],
        "stalowa wola": [],
        "starachowice": [],
        "stargard szczeciński": [
            "stargard"
        ],
        "starogard gdański": [
            "stargard"
        ],
        "strzelce opolskie": [
            "gross-strehlitz"
        ],
        "sulejówek": [],
        "suwałki": [],
        "swarzędz": [
            "schwersenz"
        ],
        "świdnica": [
            "schweidnitz"
        ],
        "świdnik": [],
        "świebodzice": [
            "freiburg"
        ],
        "świebodzin": [
            "schwiebus"
        ],
        "świecie": [
            "schwetz"
        ],
        "świętochłowice": [
            "schwientochlowitz"
        ],
        "świnoujście": [
            "swinemünde"
        ],
        "szczecin": [
            "stettin"
        ],
        "szczecinek": [
            "neustettin"
        ],
        "szczytno": [
            "ortelsburg"
        ],
        "tarnobrzeg": [],
        "tarnów": [
            "tarnau"
        ],
        "tarnowskie góry": [
            "tarnowitz"
        ],
        "tczew": [
            "dirschau"
        ],
        "tomaszów lubelski": [],
        "tomaszów mazowiecki": [],
        "toruń": [
            "thorn"
        ],
        "trzebinia": [],
        "turek": [],
        "tychy": [
            "tichau"
        ],
        "łuków": [],
        "włocławek": [
            "leslau"
        ],
        "wałbrzych": [
            "waldenburg"
        ],
        "wałcz": [
            "deutsch krone"
        ],
        "wągrowiec": [
            "wongrowitz"
        ],
        "warszawa": [
            "warschau"
        ],
        "wejherowo": [
            "neustadt"
        ],
        "wieliczka": [],
        "wieluń": [],
        "wołomin": [],
        "wodzisław śląski": [],
        "wrocław": [
            "breslau"
        ],
        "września": [
            "wreschen"
        ],
        "wyszków": [],
        "ząbki": [],
        "zabrze": [
            "hindenburg"
        ],
        "żagań": [
            "sagan"
        ],
        "zakopane": [],
        "zambrów": [],
        "zamość": [],
        "żary": [
            "sorau"
        ],
        "zawiercie": [
            "warthenau"
        ],
        "zduńska wola": [],
        "zgierz": [],
        "zgorzelec": [
            "görlitz"
        ],
        "zielona góra": [
            "grünberg"
        ],
        "żory": [
            "sohrau"
        ],
        "żyrardów": [],
        "żywiec": []
    },
    "Portugal": {
        "abrantes": [],
        "agualva-cacém": [],
        "águeda": [],
        "albergaria-a-velha": [],
        "albufeira": [],
        "alfena": [],
        "almada": [],
        "almeirim": [],
        "alverca do ribatejo": [],
        "amadora": [],
        "amarante": [],
        "amora": [],
        "angra do heroísmo": [],
        "aveiro": [],
        "barcelos": [],
        "barreiro": [],
        "beja": [],
        "braga": [],
        "bragança": [],
        "caldas da rainha": [],
        "câmara de lobos": [],
        "caniço": [],
        "cartaxo": [],
        "castelo branco": [],
        "chaves": [],
        "coimbra": [],
        "costa da caparica": [],
        "covilhã": [],
        "elvas": [],
        "entroncamento": [],
        "ermesinde": [],
        "esmoriz": [],
        "espinho": [],
        "esposende": [],
        "estarreja": [],
        "estremoz": [],
        "évora": [],
        "fafe": [],
        "faro": [],
        "fátima": [],
        "felgueiras": [],
        "fiães": [],
        "figueira da foz": [],
        "freamunde": [],
        "funchal": [],
        "fundão": [],
        "gafanha da nazaré": [],
        "gondomar": [],
        "guarda": [],
        "guimarães": [],
        "horta": [],
        "ílhavo": [],
        "lagoa": [],
        "lagos": [],
        "lamego": [],
        "leiria": [],
        "lisboa": [
            "lissabon"
        ],
        "lordelo": [
            "são salvador de lordelo"
        ],
        "loulé": [],
        "loures": [],
        "lourosa": [],
        "machico": [],
        "maia": [],
        "marco de canaveses": [],
        "marinha grande": [],
        "matosinhos": [],
        "mirandela": [],
        "montemor-o-novo": [],
        "montijo": [],
        "moura": [],
        "odivelas": [],
        "olhão da restauração": [],
        "oliveira de azeméis": [],
        "ovar": [],
        "paços de ferreira": [],
        "paredes": [],
        "penafiel": [],
        "peniche": [],
        "peso da régua": [],
        "pombal": [],
        "ponta delgada": [],
        "ponte de sor": [],
        "portalegre": [],
        "portimão": [],
        "porto": [],
        "póvoa de santa iria": [],
        "póvoa de varzim": [],
        "quarteira": [],
        "queluz": [],
        "rebordosa": [],
        "ribeira grande": [],
        "rio maior": [],
        "rio tinto": [],
        "sacavém": [],
        "samora correia": [],
        "santa comba dão": [],
        "santa cruz": [],
        "santa maria da feira": [],
        "santarém": [],
        "santo tirso": [],
        "são joão da madeira": [],
        "são mamede de infesta": [],
        "seixal": [],
        "senhora da hora": [],
        "setúbal": [],
        "sines": [],
        "tavira": [],
        "tomar": [],
        "tondela": [],
        "torres novas": [],
        "torres vedras": [],
        "trofa": [
            "bougado"
        ],
        "valbom": [],
        "vale de cambra": [],
        "valongo": [],
        "vendas novas": [],
        "viana do castelo": [],
        "vila do conde": [],
        "vila franca de xira": [],
        "vila nova de famalicão": [],
        "vila nova de gaia": [],
        "vila nova de santo andré": [],
        "vila real": [],
        "vila real de santo antónio": [],
        "viseu": [],
        "vizela": []
    },
    "Rumänien": {
        "adjud": [],
        "aiud": [],
        "alba iulia": [],
        "alexandria": [],
        "apahida": [],
        "arad": [],
        "bacău": [],
        "baia mare": [],
        "baia sprie": [],
        "băicoi": [],
        "băilești": [],
        "balș": [],
        "bârlad": [],
        "bistrița": [],
        "blaj": [],
        "bocșa": [],
        "borșa": [],
        "botoșani": [],
        "brad": [],
        "bragadiru": [],
        "brăila": [],
        "brașov": [
            "kronstadt"
        ],
        "breaza": [],
        "bucurești": [
            "bukarest"
        ],
        "buftea": [],
        "buhuși": [],
        "buzău": [],
        "calafat": [],
        "călărași": [],
        "câmpia turzii": [],
        "câmpina": [],
        "câmpulung": [],
        "câmpulung moldovenesc": [],
        "caracal": [],
        "caransebeș": [],
        "carei": [],
        "cernavodă": [],
        "chiajna": [],
        "chitila": [],
        "cisnădie": [],
        "ciurea": [],
        "cluj-napoca": [
            "klausenburg"
        ],
        "codlea": [],
        "comănești": [],
        "constanța": [
            "konstanza"
        ],
        "corabia": [],
        "craiova": [],
        "cugir": [],
        "cumpăna": [],
        "curtea de argeș": [],
        "dej": [],
        "deva": [],
        "dobroești": [],
        "dorohoi": [],
        "drăgășani": [],
        "drobeta-turnu severin": [],
        "dumbrăvița": [],
        "făgăraș": [],
        "fălticeni": [],
        "fetești": [],
        "filiași": [],
        "florești": [],
        "focșani": [],
        "găești": [],
        "galați": [],
        "gheorgheni": [],
        "gherla": [],
        "giroc": [],
        "giurgiu": [],
        "gura humorului": [],
        "hunedoara": [],
        "huși": [],
        "iași": [],
        "luduș": [],
        "lugoj": [],
        "lupeni": [],
        "măgurele": [],
        "mangalia": [],
        "marghita": [],
        "medgidia": [],
        "mediaș": [],
        "miercurea ciuc": [],
        "mioveni": [
            "colibaşi"
        ],
        "miroslava": [],
        "mizil": [],
        "moinești": [],
        "moreni": [],
        "moșnița nouă": [],
        "motru": [],
        "năvodari": [],
        "negrești-oaș": [],
        "ocna mureș": [],
        "odorheiu secuiesc": [],
        "oltenița": [],
        "onești": [
            "gheorghe gheorghiu-dej"
        ],
        "oradea": [],
        "orăștie": [],
        "otopeni": [],
        "pantelimon": [],
        "pașcani": [],
        "petrila": [],
        "petroșani": [],
        "piatra neamț": [],
        "pitești": [],
        "ploiești": [],
        "popești-leordeni": [],
        "pucioasa": [],
        "rădăuți": [],
        "râmnicu sărat": [],
        "râmnicu vâlcea": [],
        "râșnov": [],
        "reghin": [],
        "reșița": [],
        "roman": [],
        "roșiori de vede": [],
        "săcele": [],
        "salonta": [],
        "satu mare": [],
        "sebeș": [],
        "șelimbăr": [],
        "sfântu gheorghe": [],
        "sibiu": [
            "hermannstadt"
        ],
        "sighetu marmației": [],
        "sighișoara": [],
        "șimleu silvaniei": [],
        "slatina": [],
        "slobozia": [],
        "ștefănești": [
            "florica"
        ],
        "suceava": [],
        "târgoviște": [],
        "târgu jiu": [],
        "târgu mureș": [],
        "târgu neamț": [],
        "târgu secuiesc": [],
        "târnăveni": [],
        "tecuci": [],
        "timișoara": [
            "temeschburg"
        ],
        "toplița": [],
        "tulcea": [],
        "turda": [],
        "turnu măgurele": [],
        "urziceni": [],
        "valea lupului": [],
        "valu lui traian": [],
        "vaslui": [],
        "vatra dornei": [],
        "vicovu de sus": [],
        "vișeu de sus": [],
        "voluntari": [],
        "vulcan": [],
        "zalău": [],
        "zărnești": [],
        "zimnicea": []
    },
    "Russland": {
        "abakan": [],
        "al'metjevsk": [
            "almetjewsk"
        ],
        "angarsk": [],
        "archangel'sk": [
            "archangelsk"
        ],
        "armavir": [
            "armawir"
        ],
        "artëm": [
            "artjom"
        ],
        "arzamas": [
            "arsamas"
        ],
        "astrachan'": [
            "astrachan"
        ],
        "balakovo": [
            "balakowo"
        ],
        "balašicha": [
            "balaschicha"
        ],
        "barnaul": [],
        "batajsk": [
            "bataisk"
        ],
        "belgorod": [],
        "berdsk": [],
        "berezniki": [
            "beresniki"
        ],
        "bijsk": [],
        "blagoveščensk": [
            "blagoweschtschensk"
        ],
        "bratsk": [],
        "brjansk": [],
        "čeboksary": [
            "tscheboksary"
        ],
        "čeljabinsk": [
            "tscheljabinsk"
        ],
        "čerepovec": [
            "tscherepowez"
        ],
        "čerkessk": [
            "tscherkessk"
        ],
        "chabarovsk": [
            "chabarowsk"
        ],
        "chanty-mansijsk": [],
        "chasavjurt": [
            "chassawjurt"
        ],
        "chimki": [],
        "čita": [
            "tschita"
        ],
        "derbent": [],
        "dimitrovgrad": [
            "dimitrowgrad"
        ],
        "dolgoprudnyj": [
            "dolgoprudny"
        ],
        "domodedovo": [
            "domodedowo"
        ],
        "dzeržinsk": [
            "dserschinsk"
        ],
        "èlektrostal'": [
            "elektrostal"
        ],
        "èlista": [],
        "èngel's": [
            "engels"
        ],
        "groznyj": [
            "grosny"
        ],
        "irkutsk": [],
        "ivanovo": [
            "iwanowo"
        ],
        "iževsk": [
            "ustinov",
            "ischewsk"
        ],
        "jakutsk": [],
        "jaroslavl'": [
            "jaroslawl"
        ],
        "jekaterinburg": [
            "sverdlovsk"
        ],
        "jessentuki": [],
        "joškar-ola": [
            "joschkar-ola"
        ],
        "južno-sachalinsk": [
            "juschno-sachalinsk"
        ],
        "kaliningrad": [
            "königsberg"
        ],
        "kaluga": [],
        "kamensk-ural'skij": [
            "kamensk-uralski"
        ],
        "kamyšin": [
            "kamyschin"
        ],
        "kaspijsk": [],
        "kazan'": [
            "kasan"
        ],
        "kemerovo": [
            "kemerowo"
        ],
        "kirov": [
            "vi'atka",
            "kirow"
        ],
        "kislovodsk": [
            "kislowodsk"
        ],
        "kolomna": [],
        "komsomol'sk-na-amure": [
            "komsomolsk am amur"
        ],
        "kopejsk": [
            "kopeisk"
        ],
        "korolëv": [
            "kaliningrad",
            "koroljow"
        ],
        "kostroma": [],
        "kovrov": [
            "kowrow"
        ],
        "krasnodar": [],
        "krasnogorsk": [],
        "krasnojarsk": [],
        "kurgan": [],
        "kursk": [],
        "kyzyl": [
            "kysyl"
        ],
        "lipeck": [
            "lipezk"
        ],
        "ljubercy": [
            "ljuberzy"
        ],
        "machačkala": [
            "machatschkala"
        ],
        "magnitogorsk": [],
        "majkop": [
            "maikop"
        ],
        "miass": [],
        "michajlovsk": [
            "michailowsk"
        ],
        "moskva": [
            "moskau"
        ],
        "murino": [],
        "murmansk": [],
        "murom": [],
        "mytišči": [
            "mytischtschi"
        ],
        "naberežnyje čelny": [
            "brešnev",
            "nabereschnyje tschelny"
        ],
        "nachodka": [],
        "nal'čik": [
            "naltschik"
        ],
        "nazran'": [
            "nasran"
        ],
        "neftejugansk": [],
        "neftekamsk": [
            "nikolo-berëzovka"
        ],
        "nevinnomyssk": [
            "newinnomyssk"
        ],
        "nižnekamsk": [
            "nischnekamsk"
        ],
        "nižnevartovsk": [
            "nischnewartowsk"
        ],
        "nižnij novgorod": [
            "gor'kij",
            "nischni nowgorod"
        ],
        "nižnij tagil": [
            "nischni tagil"
        ],
        "noginsk": [],
        "nojabr'sk": [
            "nojabrsk"
        ],
        "noril'sk": [
            "norilsk"
        ],
        "novočeboksarsk": [
            "nowotscheboksarsk"
        ],
        "novočerkassk": [
            "nowotscherkassk"
        ],
        "novokuzneck": [
            "nowokusnezk"
        ],
        "novomoskovsk": [
            "nowomoskowsk"
        ],
        "novorossijsk": [
            "noworossijsk"
        ],
        "novošachtinsk": [
            "nowoschachtinsk"
        ],
        "novosibirsk": [
            "nowosibirsk"
        ],
        "novyj urengoj": [
            "nowy urengoi"
        ],
        "obninsk": [],
        "odincovo": [
            "odinzowo"
        ],
        "oktjabr'skij": [
            "oktjabrski"
        ],
        "omsk": [],
        "orechovo-zujevo": [
            "orechowo-sujewo"
        ],
        "orël": [
            "orjol"
        ],
        "orenburg": [],
        "orsk": [],
        "penza": [
            "pensa"
        ],
        "perm'": [
            "perm"
        ],
        "pervoural'sk": [
            "perwouralsk"
        ],
        "petropavlovsk-kamčatskij": [
            "petropawlowsk-kamtschatski"
        ],
        "petrozavodsk": [
            "petrosawodsk"
        ],
        "pjatigorsk": [],
        "podol'sk": [
            "podolsk"
        ],
        "prokopjevsk": [
            "prokopjewsk"
        ],
        "pskov": [
            "pskow"
        ],
        "puškino": [
            "puschkino"
        ],
        "ramenskoje": [],
        "reutov": [
            "reutow"
        ],
        "rjazan'": [
            "rjasan"
        ],
        "rostov-na-donu": [
            "rostow am don"
        ],
        "rubcovsk": [
            "rubzowsk"
        ],
        "rybinsk": [
            "andropov"
        ],
        "šachty": [
            "schachty"
        ],
        "salavat": [
            "salawat"
        ],
        "samara": [
            "kujbyšev"
        ],
        "sankt-peterburg": [
            "leningrad",
            "sankt petersburg"
        ],
        "saransk": [],
        "saratov": [
            "saratow"
        ],
        "ščëlkovo": [
            "schtscholkowo"
        ],
        "serpuchov": [
            "serpuchow"
        ],
        "severodvinsk": [
            "sewerodwinsk"
        ],
        "seversk": [
            "tomsk-7",
            "sewersk"
        ],
        "smolensk": [],
        "soči": [
            "sotschi"
        ],
        "staryj oskol": [
            "stary oskol"
        ],
        "stavropol'": [
            "stawropol"
        ],
        "sterlitamak": [],
        "surgut": [],
        "syktyvkar": [
            "syktywkar"
        ],
        "syzran'": [
            "sysran"
        ],
        "taganrog": [],
        "tambov": [
            "tambow"
        ],
        "tjumen'": [],
        "tol'jatti": [
            "togliatti"
        ],
        "tomsk": [],
        "tula": [],
        "tver'": [
            "kalinin",
            "twer"
        ],
        "ufa": [],
        "ul'janovsk": [
            "simbirsk",
            "uljanowsk"
        ],
        "ulan-udè": [],
        "ussurijsk": [],
        "velikij novgorod": [
            "weliki nowgorod"
        ],
        "vidnoje": [
            "widnoje"
        ],
        "vladikavkaz": [
            "ordzonikidse",
            "wladikawkas"
        ],
        "vladimir": [
            "wladimir"
        ],
        "vladivostok": [
            "wladiwostok"
        ],
        "volgodonsk": [
            "wolgodonsk"
        ],
        "volgograd": [
            "wolgograd"
        ],
        "vologda": [
            "wologda"
        ],
        "volžskij": [
            "wolschski"
        ],
        "voronež": [
            "woronesch"
        ],
        "zlatoust": [
            "slatoust"
        ],
        "žukovskij": [
            "schukowski"
        ]
    },
    "Schweden": {
        "ale": [],
        "alingsås": [],
        "alvesta": [],
        "ängelholm": [],
        "arvika": [],
        "avesta": [],
        "boden": [],
        "bollnäs": [],
        "borås": [],
        "borlänge": [],
        "botkyrka": [],
        "burlöv": [],
        "danderyd": [],
        "ekerö": [],
        "enköping": [],
        "eskilstuna": [],
        "eslöv": [],
        "falkenberg": [],
        "falköping": [],
        "falun": [],
        "finspång": [],
        "gällivare": [],
        "gävle": [],
        "gislaved": [],
        "göteborg": [],
        "gotland": [],
        "håbo": [],
        "halmstad": [],
        "haninge": [],
        "härnösand": [],
        "härryda": [],
        "hässleholm": [],
        "helsingborg": [],
        "höganäs": [],
        "huddinge": [],
        "hudiksvall": [],
        "järfälla": [],
        "jönköping": [],
        "kalmar": [],
        "karlshamn": [],
        "karlskoga": [],
        "karlskrona": [],
        "karlstad": [],
        "katrineholm": [],
        "kävlinge": [],
        "kiruna": [],
        "knivsta": [],
        "köping": [],
        "kramfors": [],
        "kristianstad": [],
        "kristinehamn": [],
        "kumla": [],
        "kungälv": [],
        "kungsbacka": [],
        "laholm": [],
        "landskrona": [],
        "lerum": [],
        "lidingö": [],
        "lidköping": [],
        "lindesberg": [],
        "linköping": [],
        "ljungby": [],
        "ljusdal": [],
        "lomma": [],
        "ludvika": [],
        "luleå": [],
        "lund": [],
        "malmö": [],
        "mariestad": [],
        "mark": [],
        "mjölby": [],
        "mölndal": [],
        "mora": [],
        "motala": [],
        "nacka": [],
        "nässjö": [],
        "norrköping": [],
        "norrtälje": [],
        "nybro": [],
        "nyköping": [],
        "nynäshamn": [],
        "örebro": [],
        "örnsköldsvik": [],
        "oskarshamn": [],
        "österåker": [],
        "östersund": [],
        "östhammar": [],
        "partille": [],
        "piteå": [],
        "ronneby": [],
        "sala": [],
        "sandviken": [],
        "sigtuna": [],
        "simrishamn": [],
        "skellefteå": [],
        "skövde": [],
        "söderhamn": [],
        "södertälje": [],
        "sollefteå": [],
        "sollentuna": [],
        "solna": [],
        "staffanstorp": [],
        "stenungsund": [],
        "stockholm": [],
        "strängnäs": [],
        "sundbyberg": [],
        "sundsvall": [],
        "svedala": [],
        "täby": [],
        "tierp": [],
        "trelleborg": [],
        "trollhättan": [],
        "tyresö": [],
        "uddevalla": [],
        "ulricehamn": [],
        "umeå": [],
        "upplands-bro": [],
        "upplands väsby": [],
        "uppsala": [],
        "vallentuna": [],
        "vänersborg": [],
        "varberg": [],
        "värmdö": [],
        "värnamo": [],
        "västerås": [],
        "västervik": [],
        "växjö": [],
        "vellinge": [],
        "vetlanda": [],
        "ystad": []
    },
    "Serbien": {
        "aleksinac": [],
        "apatin": [],
        "aranđelovac": [],
        "bačka palanka": [],
        "bačka topola": [],
        "bečej": [],
        "beograd": [
            "belgrad"
        ],
        "bor": [],
        "borča": [],
        "bujanovac": [],
        "čačak": [],
        "ćuprija": [],
        "futog": [],
        "gornji milanovac": [],
        "inđija": [],
        "jagodina": [
            "svetozarevo"
        ],
        "kaluđerica": [],
        "kikinda": [],
        "knjaževac": [],
        "kragujevac": [],
        "kraljevo": [],
        "kruševac": [],
        "kula": [],
        "lazarevac": [],
        "leskovac": [],
        "loznica": [],
        "mladenovac": [],
        "negotin": [],
        "niš": [
            "nisch"
        ],
        "nova pazova": [],
        "novi pazar": [],
        "novi sad": [],
        "obrenovac": [],
        "pančevo": [],
        "paraćin": [],
        "petrovaradin": [],
        "pirot": [],
        "požarevac": [],
        "preševo": [],
        "priboj": [],
        "prijepolje": [],
        "prokuplje": [],
        "ruma": [],
        "šabac": [],
        "senta": [],
        "šid": [],
        "smederevo": [],
        "smederevska palanka": [],
        "sombor": [],
        "sremčica": [],
        "sremska mitrovica": [],
        "stara pazova": [],
        "subotica": [],
        "surčin": [],
        "temerin": [],
        "trstenik": [],
        "užice": [
            "titovo užice"
        ],
        "valjevo": [],
        "velika plana": [],
        "veternik": [],
        "vlasotince": [],
        "vranje": [],
        "vrbas": [
            "titov vrbas"
        ],
        "vršac": [],
        "zaječar": [],
        "zrenjanin": []
    },
    "Slowakei": {
        "bánovce nad bebravou": [],
        "banská bystrica": [
            "neusohl"
        ],
        "bardejov": [],
        "bratislava": [
            "pressburg"
        ],
        "brezno": [],
        "čadca": [],
        "detva": [],
        "dolný kubín": [],
        "dubnica nad váhom": [],
        "dunajská streda": [],
        "galanta": [],
        "handlová": [],
        "hlohovec": [],
        "humenné": [],
        "kežmarok": [],
        "komárno": [],
        "košice": [
            "kaschau"
        ],
        "kysucké nové mesto": [],
        "levice": [],
        "levoča": [],
        "liptovský mikuláš": [],
        "lučenec": [],
        "malacky": [],
        "martin": [],
        "michalovce": [],
        "nitra": [
            "neutra"
        ],
        "nové mesto nad váhom": [],
        "nové zámky": [
            "neuhäusel"
        ],
        "partizánske": [],
        "pezinok": [],
        "piešťany": [],
        "poprad": [],
        "považská bystrica": [],
        "prešov": [
            "preschau"
        ],
        "prievidza": [
            "priwitz"
        ],
        "púchov": [],
        "rimavská sobota": [],
        "rožňava": [],
        "ružomberok": [],
        "šaľa": [],
        "senec": [],
        "senica": [],
        "sereď": [],
        "skalica": [],
        "snina": [],
        "spišská nová ves": [],
        "stará ľubovňa": [],
        "topoľčany": [],
        "trebišov": [],
        "trenčín": [
            "trentschin"
        ],
        "trnava": [
            "tyrnau"
        ],
        "vranov nad topľou": [],
        "žiar nad hronom": [],
        "žilina": [
            "sillein"
        ],
        "zvolen": [
            "altsohl"
        ]
    },
    "Slowenien": {
        "ajdovščina": [],
        "bled": [],
        "brežice": [],
        "celje": [],
        "črnomelj": [],
        "domžale": [],
        "grosuplje": [],
        "hrastnik": [],
        "idrija": [],
        "izola": [
            "isola"
        ],
        "jesenice": [],
        "kamnik": [],
        "kočevje": [],
        "koper": [
            "capodistria"
        ],
        "kranj": [],
        "krško": [],
        "litija": [],
        "ljubljana": [
            "laibach"
        ],
        "logatec": [],
        "lucija": [
            "lucia"
        ],
        "maribor": [
            "marburg an der drau"
        ],
        "medvode": [],
        "mengeš": [],
        "murska sobota": [],
        "nova gorica": [],
        "novo mesto": [],
        "postojna": [],
        "ptuj": [],
        "radovljica": [],
        "ravne na koroškem": [],
        "rogaška slatina": [],
        "šentjur": [],
        "sežana": [],
        "škofja loka": [],
        "slovenj gradec": [],
        "slovenska bistrica": [],
        "slovenske konjice": [],
        "trbovlje": [],
        "velenje": [
            "titovo velenje"
        ],
        "vrhnika": [],
        "zagorje ob savi": [],
        "žalec": []
    },
    "Spanien": {
        "a coruña": [
            "la coruña"
        ],
        "adeje": [],
        "albacete": [],
        "alcalá de guadaíra": [],
        "alcalá de henares": [],
        "alcobendas": [],
        "alcoi": [
            "alcoy"
        ],
        "alcorcón": [],
        "algeciras": [],
        "alicant": [
            "alicante"
        ],
        "almería": [],
        "aranjuez": [],
        "arganda del rey": [],
        "arona": [],
        "arrecife": [],
        "ávila": [],
        "avilés": [],
        "badajoz": [],
        "badalona": [],
        "barakaldo": [
            "san vicente de baracaldo"
        ],
        "barcelona": [],
        "benalmádena": [],
        "benidorm": [],
        "bilbao": [],
        "boadilla del monte": [],
        "burgos": [],
        "cáceres": [],
        "cádiz": [],
        "calvià": [],
        "cartagena": [],
        "castelldefels": [],
        "castelló de la plana": [
            "castellón de la plana"
        ],
        "cerdanyola del vallès": [],
        "ceuta": [],
        "chiclana de la frontera": [],
        "ciudad real": [],
        "collado villalba": [],
        "colmenar viejo": [],
        "córdoba": [],
        "cornellà de llobregat": [],
        "coslada": [],
        "cuenca": [],
        "donostia": [
            "san sebastián"
        ],
        "dos hermanas": [],
        "eivissa": [
            "ibiza"
        ],
        "el ejido": [],
        "el prat de llobregat": [],
        "el puerto de santa maría": [],
        "elda": [],
        "elx": [
            "elche"
        ],
        "estepona": [],
        "ferrol": [
            "el ferrol"
        ],
        "fuengirola": [],
        "fuenlabrada": [],
        "gandia": [
            "gandía"
        ],
        "getafe": [],
        "getxo": [
            "guecho"
        ],
        "gijón": [],
        "girona": [
            "gerona"
        ],
        "granada": [],
        "granadilla de abona": [],
        "granollers": [],
        "guadalajara": [],
        "huelva": [],
        "huesca": [],
        "irun": [
            "irún"
        ],
        "jaén": [],
        "jerez de la frontera": [],
        "l'hospitalet de llobregat": [],
        "la línea de la concepción": [],
        "las palmas de gran canaria": [],
        "las rozas de madrid": [],
        "leganés": [],
        "león": [],
        "linares": [],
        "lleida": [
            "lérida"
        ],
        "logroño": [],
        "lorca": [],
        "lugo": [],
        "madrid": [],
        "majadahonda": [],
        "málaga": [],
        "manresa": [],
        "marbella": [],
        "mataró": [],
        "melilla": [],
        "mérida": [],
        "mijas": [],
        "molina de segura": [],
        "mollet del vallès": [],
        "móstoles": [],
        "motril": [],
        "murcia": [],
        "orihuela": [],
        "ourense": [
            "orense"
        ],
        "oviedo": [],
        "palencia": [],
        "palma": [
            "palma de mallorca"
        ],
        "pamplona": [
            "iruña"
        ],
        "parla": [],
        "paterna": [],
        "pinto": [],
        "ponferrada": [],
        "pontevedra": [],
        "pozuelo de alarcón": [],
        "reus": [],
        "rincón de la victoria": [],
        "rivas-vaciamadrid": [],
        "roquetas de mar": [],
        "rubí": [],
        "sabadell": [],
        "sagunt": [
            "sagunto"
        ],
        "salamanca": [],
        "san bartolomé de tirajana": [],
        "san cristóbal de la laguna": [
            "la laguna"
        ],
        "san fernando": [],
        "san sebastián de los reyes": [],
        "sanlúcar de barrameda": [],
        "sant boi de llobregat": [],
        "sant cugat del vallès": [],
        "sant vicent del raspeig": [
            "san vicente del raspeig"
        ],
        "santa coloma de gramenet": [
            "santa coloma de gramanet"
        ],
        "santa cruz de tenerife": [],
        "santa lucía de tirajana": [],
        "santander": [],
        "santiago de compostela": [],
        "segovia": [],
        "sevilla": [],
        "siero": [],
        "talavera de la reina": [],
        "tarragona": [],
        "telde": [],
        "terrassa": [
            "tarrasa"
        ],
        "toledo": [],
        "torrejón de ardoz": [],
        "torrelavega": [],
        "torremolinos": [],
        "torrent": [
            "torrente"
        ],
        "torrevieja": [],
        "tres cantos": [],
        "utrera": [],
        "valdemoro": [],
        "valència": [
            "valencia"
        ],
        "valladolid": [],
        "vélez-málaga": [],
        "vic": [],
        "vigo": [],
        "vila-real": [
            "villarreal"
        ],
        "viladecans": [],
        "vilanova i la geltrú": [],
        "vitoria-gasteiz": [],
        "zamora": [],
        "zaragoza": [
            "saragossa"
        ]
    },
    "Tschechische Republik": {
        "beroun": [],
        "blansko": [],
        "bohumín": [],
        "brandýs nad labem-stará boleslav": [],
        "břeclav": [],
        "brno": [
            "brünn"
        ],
        "česká lípa": [],
        "české budějovice": [
            "budweis"
        ],
        "český těšín": [],
        "cheb": [
            "eger"
        ],
        "chomutov": [
            "komotau"
        ],
        "chrudim": [],
        "děčín": [],
        "frýdek-místek": [],
        "havířov": [],
        "havlíčkův brod": [],
        "hodonín": [],
        "hradec králové": [
            "königgrätz"
        ],
        "hranice": [],
        "jablonec nad nisou": [],
        "jihlava": [],
        "jindřichův hradec": [],
        "jirkov": [],
        "karlovy vary": [
            "karlsbad"
        ],
        "karviná": [],
        "kladno": [],
        "klatovy": [],
        "kolín": [],
        "kopřivnice": [],
        "krnov": [],
        "kroměříž": [],
        "kutná hora": [],
        "liberec": [
            "reichenberg"
        ],
        "litoměřice": [],
        "litvínov": [],
        "louny": [],
        "mělník": [],
        "mladá boleslav": [],
        "most": [
            "brüx"
        ],
        "náchod": [],
        "nový jičín": [],
        "olomouc": [],
        "opava": [],
        "orlová": [],
        "ostrava": [
            "ostrau"
        ],
        "otrokovice": [],
        "pardubice": [],
        "písek": [],
        "plzeň": [
            "pilsen"
        ],
        "praha": [
            "prag"
        ],
        "přerov": [],
        "příbram": [],
        "prostějov": [],
        "sokolov": [],
        "strakonice": [],
        "šumperk": [],
        "tábor": [],
        "teplice": [
            "teplitz"
        ],
        "třebíč": [],
        "třinec": [],
        "trutnov": [],
        "uherské hradiště": [],
        "ústí nad labem": [
            "aussig an der elbe"
        ],
        "valašské meziříčí": [],
        "vsetín": [],
        "vyškov": [],
        "žatec": [],
        "žďár nad sázavou": [],
        "zlín": [
            "gottwaldov"
        ],
        "znojmo": []
    },
    "Türkei": {
        "adıyaman": [],
        "adana": [],
        "adapazarı": [
            "sakarya"
        ],
        "afşin": [],
        "afyonkarahisar": [
            "afyon"
        ],
        "ağrı": [
            "karaköse"
        ],
        "ahlat": [],
        "akçaabat": [],
        "akçakale": [],
        "akçakoca": [],
        "akdağmadeni": [],
        "akhisar": [],
        "aksaray": [],
        "akşehir": [],
        "aksu": [],
        "akyazı": [],
        "akyurt": [],
        "alaca": [],
        "alanya": [],
        "alaplı": [],
        "alaşehir": [],
        "aliağa": [],
        "amasya": [],
        "anamur": [],
        "ankara": [],
        "antakya": [
            "hatay"
        ],
        "antalya": [],
        "araklı": [],
        "ardahan": [],
        "ardeşen": [],
        "arnavutköy": [],
        "artvin": [],
        "aydın": [],
        "ayvalık": [],
        "babaeski": [],
        "bafra": [],
        "balıkesir": [],
        "bandırma": [],
        "bartın": [],
        "başiskele": [],
        "batman": [],
        "bayındır": [],
        "bayburt": [],
        "belen": [],
        "bergama": [],
        "besni": [],
        "beypazarı": [],
        "beyşehir": [],
        "biga": [],
        "bilecik": [],
        "bingöl": [],
        "birecik": [],
        "bismil": [],
        "bitlis": [],
        "bodrum": [],
        "boğazlıyan": [],
        "bolu": [],
        "bolvadin": [],
        "bor": [],
        "boyabat": [],
        "bozüyük": [],
        "bucak": [],
        "bulanık": [],
        "bulancak": [],
        "burdur": [],
        "burhaniye": [],
        "bursa": [],
        "çınarcık": [],
        "çan": [],
        "çanakkale": [],
        "çankırı": [],
        "çarşamba": [],
        "çatalca": [],
        "çaycuma": [],
        "çayeli": [],
        "çerkezköy": [],
        "çermik": [],
        "çeşme": [],
        "ceyhan": [],
        "ceylanpınar": [],
        "çiftlikköy": [],
        "çine": [],
        "çivril": [],
        "cizre": [],
        "çorlu": [],
        "çorum": [],
        "çubuk": [],
        "çumra": [],
        "dalaman": [],
        "denizciler": [],
        "denizli": [],
        "derik": [],
        "derince": [],
        "develi": [],
        "devrek": [],
        "didim": [],
        "dikili": [],
        "dilovası": [],
        "dinar": [],
        "diyadin": [],
        "diyarbakır": [],
        "doğubayazıt": [],
        "dörtyol": [],
        "döşemealtı": [],
        "düzce": [],
        "düziçi": [],
        "edirne": [],
        "edremit": [],
        "elâzığ": [],
        "elbistan": [],
        "elmadağ": [],
        "emirdağ": [],
        "erbaa": [],
        "erciş": [],
        "erdek": [],
        "erdemli": [],
        "ereğli": [
            "karadeniz ereğli"
        ],
        "ergani": [],
        "erzin": [
            "yeşilkent"
        ],
        "erzincan": [],
        "erzurum": [],
        "eskil": [],
        "eskişehir": [],
        "espiye": [],
        "fatsa": [],
        "ferizli": [],
        "fethiye": [],
        "finike": [],
        "foça": [],
        "gaziantep": [],
        "gazipaşa": [],
        "gebze": [],
        "gediz": [],
        "gelibolu": [],
        "gemlik": [],
        "genç": [],
        "gerede": [],
        "geyve": [],
        "giresun": [],
        "göksun": [],
        "gölbaşı": [],
        "gölcük": [],
        "gönen": [],
        "görele": [],
        "gümüşhane": [],
        "güroymak": [],
        "gürsu": [],
        "hakkâri": [],
        "harbiye": [],
        "havza": [],
        "hendek": [],
        "hilvan": [],
        "hopa": [],
        "i̇dil": [],
        "iğdır": [],
        "ilgın": [],
        "i̇mamoğlu": [],
        "i̇ncesu": [],
        "i̇ncirliova": [],
        "i̇negöl": [],
        "i̇skenderun": [],
        "i̇slahiye": [],
        "isparta": [],
        "i̇stanbul": [
            "istanbul"
        ],
        "i̇zmir": [
            "izmir"
        ],
        "i̇zmit": [
            "kocaeli"
        ],
        "i̇znik": [],
        "kırıkhan": [],
        "kırıkkale": [],
        "kırkağaç": [],
        "kırklareli": [],
        "kırşehir": [],
        "kızılpınar": [],
        "kızıltepe": [],
        "kadirli": [],
        "kağızman": [],
        "kahramanmaraş": [
            "maraş"
        ],
        "kâhta": [],
        "kaman": [],
        "kapaklı": [],
        "karaağaç": [],
        "karabük": [],
        "karacabey": [],
        "karaköprü": [],
        "karaman": [],
        "karamürsel": [],
        "karapınar": [],
        "karasu": [],
        "kars": [],
        "kartepe": [],
        "kastamonu": [],
        "kayseri": [],
        "kazan": [
            "kahramankazan"
        ],
        "kelkit": [],
        "kemalpaşa": [],
        "kemer": [],
        "kepez": [],
        "keşan": [],
        "kestel": [],
        "kilimli": [],
        "kilis": [],
        "konya": [],
        "körfez": [],
        "korkuteli": [],
        "kovancılar": [],
        "kozan": [],
        "kozlu": [],
        "kozluk": [],
        "kula": [],
        "kulu": [],
        "kumluca": [],
        "kurtalan": [],
        "kuşadası": [],
        "kütahya": [],
        "lüleburgaz": [],
        "mahmutlar": [],
        "malatya": [],
        "malazgirt": [],
        "malkara": [],
        "manavgat": [],
        "manisa": [],
        "mardin": [],
        "marmaris": [],
        "menderes": [],
        "menemen": [],
        "mersin": [
            "i̇çel"
        ],
        "merzifon": [],
        "midyat": [],
        "milas": [],
        "mudanya": [],
        "muğla": [],
        "muratlı": [],
        "muş": [],
        "mustafakemalpaşa": [],
        "mut": [],
        "nazilli": [],
        "nevşehir": [],
        "niğde": [],
        "niksar": [],
        "nizip": [],
        "nurdağı": [],
        "nusaybin": [],
        "ödemiş": [],
        "of": [],
        "oltu": [],
        "ordu": [],
        "orhangazi": [],
        "ortaca": [],
        "ortaköy": [],
        "osmancık": [],
        "osmaniye": [],
        "pamukova": [],
        "patnos": [],
        "payas": [],
        "pazarcık": [],
        "polatlı": [],
        "reyhanlı": [],
        "rize": [],
        "şırnak": [],
        "safranbolu": [],
        "salihli": [],
        "samandağ": [],
        "samsun": [],
        "sandıklı": [],
        "şanlıurfa": [
            "urfa"
        ],
        "sapanca": [],
        "sarıkaya": [],
        "saray": [],
        "sarayköy": [],
        "şarkışla": [],
        "şarköy": [],
        "saruhanlı": [],
        "seferihisar": [],
        "selçuk": [],
        "şereflikoçhisar": [],
        "serik": [],
        "seydişehir": [],
        "siirt": [],
        "silifke": [],
        "silivri": [],
        "silopi": [],
        "silvan": [],
        "simav": [],
        "sinop": [],
        "sivas": [],
        "siverek": [],
        "söke": [],
        "solhan": [],
        "soma": [],
        "sorgun": [],
        "suluova": [],
        "sungurlu": [],
        "suruç": [],
        "susurluk": [],
        "talas": [],
        "tarsus": [],
        "tatvan": [],
        "tavşanlı": [],
        "tekirdağ": [],
        "tekkeköy": [],
        "terme": [],
        "tire": [],
        "tirebolu": [],
        "tokat": [],
        "torbalı": [],
        "tosya": [],
        "trabzon": [],
        "tunceli": [],
        "turgutlu": [],
        "turhal": [],
        "türkoğlu": [],
        "ünye": [],
        "ürgüp": [],
        "urla": [],
        "uşak": [],
        "uzunköprü": [],
        "van": [],
        "vezirköprü": [],
        "viranşehir": [],
        "yahşihan": [],
        "yahyalı": [],
        "yalova": [],
        "yalvaç": [],
        "yatağan": [],
        "yenişehir": [],
        "yerköy": [],
        "yeşilyurt": [],
        "yozgat": [],
        "yüksekova": [],
        "zile": [],
        "zonguldak": []
    },
    "Ukraine": {
        "alčevs'k": [
            "kommunarsk",
            "altschewsk"
        ],
        "alušta": [
            "aluschta"
        ],
        "amvrosiïvka": [
            "amwrossijiwka"
        ],
        "antracyt": [
            "antrazyt"
        ],
        "armjans'k": [
            "armensk"
        ],
        "avdiïvka": [
            "awdijiwka"
        ],
        "bachčysaraj": [
            "bachtschyssaraj"
        ],
        "bachmač": [
            "bachmatsch"
        ],
        "bachmut": [
            "artėmivs'k",
            "artemiwsk"
        ],
        "balaklija": [],
        "balta": [],
        "berdjans'k": [
            "berdjansk"
        ],
        "berdyčiv": [
            "berdytschiw"
        ],
        "berehove": [
            "berehowe"
        ],
        "bila cerkva": [
            "bila zerkwa"
        ],
        "bilhorod-dnistrovs'kyj": [
            "bilhorod-dnistrowskyj"
        ],
        "bojarka": [],
        "boryslav": [
            "boryslaw"
        ],
        "boryspil'": [
            "boryspil"
        ],
        "brjanka": [],
        "brody": [],
        "brovary": [
            "browary"
        ],
        "buča": [
            "butscha"
        ],
        "čerkasy": [
            "tscherkassy"
        ],
        "černihiv": [
            "tschernihiw"
        ],
        "černivci": [
            "czernowitz"
        ],
        "červonohrad": [
            "tscherwonohrad"
        ],
        "charcyz'k": [
            "charsysk"
        ],
        "charkiv": [
            "charkiw"
        ],
        "cherson": [],
        "chmel'nyc'kyj": [
            "chmelnyzkyj"
        ],
        "chmil'nyk": [
            "chmilnyk"
        ],
        "chrestivka": [
            "kirovs'kė",
            "chrestiwka"
        ],
        "chrustal'nyj": [
            "krasnyj luč"
        ],
        "chust": [],
        "čornomors'k": [
            "illičivs'k",
            "tschornomorsk"
        ],
        "čortkiv": [
            "tschortkiw"
        ],
        "čuhuïv": [
            "tschuhujiw"
        ],
        "čystjakove": [
            "torėz",
            "tschystjakowe"
        ],
        "debal'ceve": [
            "debalzewe"
        ],
        "derhači": [
            "derhatschi"
        ],
        "dnipro": [
            "dnipropėtrovs'k",
            "dnipropetrowsk"
        ],
        "dniprorudne": [],
        "dobropillja": [],
        "dokučajevs'k": [
            "dokutschajewsk"
        ],
        "dolyna": [],
        "donec'k": [
            "donezk"
        ],
        "dovžans'k": [
            "svėrdlovs'k",
            "dowschansk"
        ],
        "drohobyč": [
            "drohobytsch"
        ],
        "družkivka": [
            "druschkiwka"
        ],
        "dubno": [],
        "džankoj": [
            "dschankoj"
        ],
        "enerhodar": [],
        "fastiv": [
            "fastiw"
        ],
        "feodosija": [
            "feodossija"
        ],
        "hadjač": [
            "hadjatsch"
        ],
        "hajsyn": [
            "hajssyn"
        ],
        "heničes'k": [
            "henitschesk"
        ],
        "hluchiv": [
            "hluchiw"
        ],
        "holubivka": [
            "kirovs'k",
            "holubiwka"
        ],
        "horišni plavni": [
            "komsomol'sk",
            "horischni plawni"
        ],
        "horlivka": [
            "horliwka"
        ],
        "irpin'": [
            "irpin"
        ],
        "ivano-frankivs'k": [
            "iwano-frankiwsk"
        ],
        "izjum": [
            "isjum"
        ],
        "izmaïl": [
            "ismajil"
        ],
        "jahotyn": [],
        "jalta": [],
        "jasynuvata": [
            "jassynuwata"
        ],
        "jenakijeve": [
            "jenakijewe"
        ],
        "jevpatorija": [
            "gözleve",
            "jewpatorija"
        ],
        "južne": [
            "juschne"
        ],
        "južnoukraïns'k": [
            "juschnoukrajinsk"
        ],
        "kachovka": [
            "kachowka"
        ],
        "kadiïvka": [
            "stachanov",
            "kadijiwka"
        ],
        "kaluš": [
            "kalusch"
        ],
        "kalynivka": [
            "kalyniwka"
        ],
        "kam'janec'-podil's'kyj": [
            "kamjanez-podilskyj"
        ],
        "kam'jans'ke": [
            "dniprodzėržyns'k",
            "kamjanske"
        ],
        "kaniv": [
            "kaniw"
        ],
        "kerč": [
            "kertsch"
        ],
        "kilija": [],
        "kolomyja": [],
        "konotop": [],
        "korosten'": [
            "korosten"
        ],
        "korostyšiv": [
            "korostyschiw"
        ],
        "kostjantynivka": [
            "kostjantyniwka"
        ],
        "kostopil'": [
            "kostopil"
        ],
        "kovel'": [
            "kowel"
        ],
        "kozjatyn": [
            "kosjatyn"
        ],
        "kramators'k": [
            "kramatorsk"
        ],
        "krasnohrad": [],
        "krasnoperekops'k": [],
        "krasyliv": [
            "krassyliw"
        ],
        "kremenčuk": [
            "krementschuk"
        ],
        "kremenec'": [
            "kremenez"
        ],
        "kreminna": [],
        "krolevec'": [
            "krolewez"
        ],
        "kropyvnyc'kyj": [
            "kirovhrad",
            "kropywnyzkyj"
        ],
        "kryvyj rih": [
            "krywyj rih"
        ],
        "kup'jans'k": [
            "kupjansk"
        ],
        "kurachove": [
            "kurachowe"
        ],
        "kyïv": [
            "kiew"
        ],
        "l'viv": [
            "lemberg",
            "lwiw"
        ],
        "ladyžyn": [
            "ladyschyn"
        ],
        "lebedyn": [],
        "ljubotyn": [],
        "lozova": [
            "losowa"
        ],
        "lubny": [],
        "luc'k": [
            "luzk"
        ],
        "luhans'k": [
            "vorošilovgrad",
            "luhansk"
        ],
        "lyman": [
            "krasnyj liman"
        ],
        "lysyčans'k": [
            "lyssytschansk"
        ],
        "makiïvka": [
            "makijiwka"
        ],
        "malyn": [],
        "marhanec'": [
            "marhanez"
        ],
        "mariupol'": [
            "zdanov",
            "mariupol"
        ],
        "melitopol'": [
            "melitopol"
        ],
        "merefa": [],
        "mohyliv-podil's'kyj": [
            "mohyliw-podilskyj"
        ],
        "molodohvardijs'k": [
            "molodohwardijsk"
        ],
        "mukačeve": [
            "mukatschewe"
        ],
        "mykolaïv": [
            "mykolajiw"
        ],
        "myrhorod": [],
        "myrnohrad": [
            "dymytrov"
        ],
        "nadvirna": [
            "nadwirna"
        ],
        "netišyn": [
            "netischyn"
        ],
        "nikopol'": [
            "nikopol"
        ],
        "nižyn": [
            "nischyn"
        ],
        "nova kachovka": [
            "nowa kachowka"
        ],
        "novohrad-volyns'kyj": [
            "nowohrad-wolynskyj"
        ],
        "novojavorivs'k": [
            "nowojaworiwsk"
        ],
        "novomoskovs'k": [
            "nowomoskowsk"
        ],
        "novovolyns'k": [
            "nowowolynsk"
        ],
        "novyj rozdil": [
            "nowyj rosdil"
        ],
        "obuchiv": [
            "obuchiw"
        ],
        "ochtyrka": [],
        "odesa": [
            "odessa"
        ],
        "oleksandrija": [
            "olexandrija"
        ],
        "olešky": [
            "cjurupyns'k",
            "oleschky"
        ],
        "p'jatychatky": [
            "pjatychatky"
        ],
        "pavlohrad": [
            "pawlohrad"
        ],
        "perejaslav-chmel'nyc'kyj": [
            "perejaslaw-chmelnyzkyj"
        ],
        "pereval's'k": [
            "perewalsk"
        ],
        "peršotravens'k": [
            "perschotrawensk"
        ],
        "pervomajs'k": [
            "perwomajsk"
        ],
        "pervomajs'kyj": [
            "perwomajskyj"
        ],
        "podil's'k": [
            "kotovs'k",
            "podilsk"
        ],
        "pokrov": [
            "ordžonikidzė",
            "pokrow"
        ],
        "pokrovs'k": [
            "krasnoarmijs'k",
            "pokrowsk"
        ],
        "polohy": [],
        "polonne": [],
        "poltava": [
            "poltawa"
        ],
        "popasna": [],
        "pryluky": [],
        "reni": [],
        "rivne": [
            "riwne"
        ],
        "romny": [],
        "roven'ky": [
            "rowenky"
        ],
        "rubižne": [
            "rubischne"
        ],
        "šachtars'k": [
            "schachtarsk"
        ],
        "saky": [],
        "sambir": [],
        "sarny": [],
        "selydove": [
            "selydowe"
        ],
        "šepetivka": [
            "schepetiwka"
        ],
        "sevastopol'": [
            "akyar",
            "sewastopol"
        ],
        "simferopol'": [
            "akmescid"
        ],
        "sjevjerodonec'k": [
            "sjewjerodonezk"
        ],
        "slavuta": [
            "slawuta"
        ],
        "slavutyč": [
            "slawutytsch"
        ],
        "slov'jans'k": [
            "slowjansk"
        ],
        "smila": [],
        "snižne": [
            "snischne"
        ],
        "sokal'": [
            "sokal"
        ],
        "sorokyne": [
            "krasnodon"
        ],
        "šostka": [
            "schostka"
        ],
        "starobil's'k": [
            "starobilsk"
        ],
        "starokostjantyniv": [
            "starokostjantyniw"
        ],
        "stebnyk": [],
        "stryj": [],
        "suchodil's'k": [
            "suchodilsk"
        ],
        "sumy": [],
        "svitlovods'k": [
            "switlowodsk"
        ],
        "synel'nykove": [
            "synelnykowe"
        ],
        "ternivka": [
            "terniwka"
        ],
        "ternopil'": [
            "ternopil"
        ],
        "tokmak": [],
        "torec'k": [
            "dzėržyns'k",
            "torezk"
        ],
        "trostjanec'": [
            "trostjanez"
        ],
        "truskavec'": [
            "truskawez"
        ],
        "uman'": [
            "uman"
        ],
        "užhorod": [
            "uschhorod"
        ],
        "varaš": [
            "kuznėcovs'k",
            "warasch"
        ],
        "vasyl'kiv": [
            "wassylkiw"
        ],
        "vatutine": [
            "watutine"
        ],
        "vil'nohirs'k": [
            "wilnohirsk"
        ],
        "vinnycja": [
            "winnyzja"
        ],
        "volnovacha": [
            "wolnowacha"
        ],
        "voločys'k": [
            "wolotschysk"
        ],
        "volodymyr-volyns'kyj": [
            "wolodymyr-wolynskyj"
        ],
        "vovčans'k": [
            "wowtschansk"
        ],
        "voznesens'k": [
            "wosnessensk"
        ],
        "vynohradiv": [
            "wynohradiw"
        ],
        "vyšhorod": [
            "wyschhorod"
        ],
        "vyšneve": [
            "wyschnewe"
        ],
        "zaporižžja": [
            "saporischschja"
        ],
        "zdolbuniv": [
            "sdolbuniw"
        ],
        "žmerynka": [
            "schmerynka"
        ],
        "znam'janka": [
            "snamjanka"
        ],
        "zoločiv": [
            "solotschiw"
        ],
        "zolotonoša": [
            "solotonoscha"
        ],
        "žovti vody": [
            "schowti wody"
        ],
        "žytomyr": [
            "schytomyr"
        ]
    },
    "Ungarn": {
        "abony": [],
        "ajka": [],
        "baja": [],
        "balassagyarmat": [],
        "balmazújváros": [],
        "békés": [],
        "békéscsaba": [],
        "berettyóújfalu": [],
        "biatorbágy": [],
        "budakeszi": [],
        "budaörs": [],
        "budapest": [],
        "cegléd": [],
        "csongrád": [],
        "dabas": [],
        "debrecen": [
            "debrezin"
        ],
        "dombóvár": [],
        "dunaharaszti": [],
        "dunakeszi": [],
        "dunaújváros": [],
        "eger": [],
        "érd": [],
        "esztergom": [],
        "fót": [],
        "göd": [],
        "gödöllő": [],
        "gyál": [],
        "gyömrő": [],
        "gyöngyös": [],
        "győr": [
            "raab"
        ],
        "gyula": [],
        "hajdúböszörmény": [],
        "hajdúnánás": [],
        "hajdúszoboszló": [],
        "hatvan": [],
        "hódmezővásárhely": [],
        "jászberény": [],
        "kalocsa": [],
        "kaposvár": [],
        "karcag": [],
        "kazincbarcika": [],
        "kecskemét": [],
        "keszthely": [],
        "kiskunfélegyháza": [],
        "kiskunhalas": [],
        "kisvárda": [],
        "komárom": [],
        "komló": [],
        "makó": [],
        "mátészalka": [],
        "mezőkövesd": [],
        "mezőtúr": [],
        "miskolc": [],
        "mohács": [],
        "monor": [],
        "mosonmagyaróvár": [],
        "nagykanizsa": [],
        "nagykőrös": [],
        "nyíregyháza": [],
        "orosháza": [],
        "oroszlány": [],
        "ózd": [],
        "paks": [],
        "pápa": [],
        "pécel": [],
        "pécs": [
            "fünfkirchen"
        ],
        "pomáz": [],
        "salgótarján": [],
        "sárvár": [],
        "sátoraljaújhely": [],
        "siófok": [],
        "sopron": [
            "ödenburg"
        ],
        "szarvas": [],
        "százhalombatta": [],
        "szeged": [
            "segedin"
        ],
        "székesfehérvár": [
            "stuhlweissenburg"
        ],
        "szekszárd": [],
        "szentendre": [],
        "szentes": [],
        "szigethalom": [],
        "szigetszentmiklós": [],
        "szolnok": [],
        "szombathely": [
            "steinamanger"
        ],
        "tapolca": [],
        "tata": [],
        "tatabánya": [],
        "tiszaújváros": [],
        "törökbálint": [],
        "törökszentmiklós": [],
        "vác": [],
        "várpalota": [],
        "vecsés": [],
        "veresegyház": [],
        "veszprém": [],
        "zalaegerszeg": [
            "egersee"
        ]
    },
    "Weissrussland": {
        "asipovičy": [
            "osipoviči"
        ],
        "ašmiany": [],
        "astraviec": [],
        "babrujsk": [],
        "barań": [],
        "baranavičy": [
            "baranoviči",
            "baranowitschi"
        ],
        "barysaǔ": [
            "borisov",
            "borisow"
        ],
        "bialyničy": [],
        "biaroza": [
            "berëza"
        ],
        "biarozaǔka": [],
        "bielaaziorsk": [],
        "bierazino": [],
        "braslaǔ": [],
        "brest": [],
        "bychaǔ": [
            "bychov"
        ],
        "čašniki": [],
        "čavusy": [],
        "červień": [],
        "chojniki": [],
        "dobruš": [],
        "drahičyn": [],
        "dziaržynsk": [
            "dzeržinsk"
        ],
        "fanipaĺ": [],
        "hancavičy": [],
        "haradok": [
            "gorodok"
        ],
        "hlybokaje": [
            "glybokaje"
        ],
        "homieĺ": [
            "gomel"
        ],
        "horki": [],
        "hrodna": [
            "grodno"
        ],
        "ivacevičy": [
            "ivaceviči"
        ],
        "ivanava": [],
        "jeĺsk": [
            "jelsk"
        ],
        "kalinkavičy": [],
        "kapyĺ": [],
        "kasciukovičy": [],
        "kleck": [],
        "klimavičy": [],
        "kobryn": [
            "kobrin"
        ],
        "kryčaǔ": [
            "krčiëv"
        ],
        "lahojsk": [
            "logojsk"
        ],
        "leĺčycy": [],
        "lepieĺ": [],
        "liachavičy": [],
        "lida": [],
        "liubań": [],
        "luniniec": [],
        "mačuliščy": [],
        "mahiloǔ": [
            "mogilew"
        ],
        "maladziečna": [
            "molodečno"
        ],
        "malaryta": [],
        "marjina horka": [
            "mar'ina gorka"
        ],
        "masty": [],
        "mazyr": [
            "mozyr'",
            "mosyr"
        ],
        "mikaševičy": [],
        "minsk": [],
        "mscislaǔ": [],
        "navahrudak": [],
        "navapolack": [
            "novopolock",
            "nawapolazk"
        ],
        "niasviž": [],
        "novalukomĺ": [],
        "orša": [
            "orscha"
        ],
        "pastavy": [
            "postavy"
        ],
        "pietrykaǔ": [],
        "pinsk": [],
        "polack": [
            "polock"
        ],
        "pružany": [],
        "rahačoǔ": [
            "rogačëv"
        ],
        "rečyca": [
            "rečica"
        ],
        "salihorsk": [
            "soligorsk"
        ],
        "ščučyn": [],
        "skidzieĺ": [],
        "škloǔ": [],
        "slonim": [],
        "sluck": [],
        "smaliavičy": [],
        "smarhoń": [
            "smorgon'"
        ],
        "staryja darohi": [],
        "stolin": [],
        "stoǔbcy": [],
        "svietlahorsk": [
            "sveltlogorsk"
        ],
        "talačyn": [],
        "uzda": [],
        "valožyn": [],
        "vaǔkavysk": [
            "volkovyjsk"
        ],
        "viciebsk": [
            "witebsk"
        ],
        "vilejka": [],
        "žabinka": [],
        "zaslaǔje": [],
        "žlobin": [],
        "žodzina": [
            "žodino"
        ],
        "žytkavičy": []
    },
    "Zypern": {
        "agía nápa": [],
        "ágios athanásios": [],
        "ágios dométios": [],
        "aglantziá": [],
        "aradíppou": [],
        "athiénou": [],
        "avgórou": [],
        "chlórakas": [],
        "dáli": [],
        "derýneia": [],
        "dromolaxiá-meneoú": [],
        "émpa": [],
        "énkomi": [
            "engomi"
        ],
        "géri": [],
        "germasógeia": [],
        "geroskípou": [],
        "káto polemídia": [],
        "kíti": [],
        "kokkinotrimithiá": [],
        "kolóssi": [],
        "lakatámeia": [],
        "lárnaka": [],
        "latsiá": [],
        "lefkosía": [
            "nikosia"
        ],
        "lemesós": [
            "limassol"
        ],
        "liopétri": [],
        "livádia": [],
        "mésa geitoniá": [],
        "páfos": [
            "néa páfos",
            "paphos"
        ],
        "paralímni": [],
        "pégeia": [],
        "sotíra": [],
        "stróvolos": [],
        "tséri": [],
        "voróklini": [
            "oróklini"
        ],
        "xylofágou": [],
        "ýpsonas": []
    }
}

NON_SWISS_PLACE_TERMS = list(dict.fromkeys(
    term
    for country_places in NON_SWISS_PLACE_ALIASES_BY_COUNTRY.values()
    for canonical, aliases in country_places.items()
    for term in (canonical, *aliases)
))

# Kurze einteilige Namen werden nur in explizitem Ortskontext ausgewertet,
# damit Woerter wie Bath, Sale oder Mors keine falschen Raumanker bilden.
CONTEXTUAL_NON_SWISS_PLACE_TERMS = [
    "aalen",
    "aalst",
    "aars",
    "aat",
    "åbo",
    "abony",
    "adana",
    "adeje",
    "adjud",
    "afyon",
    "ahlat",
    "ahlen",
    "aiud",
    "ajka",
    "ajtos",
    "akmenė",
    "đakovo",
    "aksu",
    "akyar",
    "akyazı",
    "alaca",
    "alaplı",
    "alcoi",
    "alcoy",
    "ale",
    "alost",
    "alta",
    "alver",
    "amora",
    "ans",
    "anzio",
    "arad",
    "araklı",
    "ardea",
    "ardee",
    "árgos",
    "arlon",
    "arona",
    "árta",
    "artëm",
    "ås",
    "asker",
    "askøy",
    "asse",
    "assen",
    "asten",
    "asti",
    "ath",
    "athen",
    "athy",
    "ávila",
    "baarn",
    "baden",
    "bafra",
    "baja",
    "balen",
    "balș",
    "balta",
    "bar",
    "barań",
    "bari",
    "barri",
    "barry",
    "bath",
    "beek",
    "beja",
    "békés",
    "belen",
    "berat",
    "besni",
    "best",
    "bieruń",
    "biga",
    "bihać",
    "bijsk",
    "birr",
    "blaj",
    "bled",
    "boden",
    "bodø",
    "bolu",
    "bonn",
    "boom",
    "bor",
    "borås",
    "borgå",
    "borne",
    "borup",
    "bozen",
    "brad",
    "braga",
    "bray",
    "breda",
    "brest",
    "brieg",
    "brno",
    "brody",
    "brünn",
    "brüx",
    "brzeg",
    "bucak",
    "bucovăț",
    "budva",
    "buren",
    "bursa",
    "bury",
    "bychaǔ",
    "bytom",
    "čadca",
    "cádiz",
    "caen",
    "cahul",
    "çan",
    "carei",
    "carpi",
    "cavan",
    "čavusy",
    "cazin",
    "celje",
    "celle",
    "červień",
    "ceuta",
    "cheb",
    "chíos",
    "chust",
    "çine",
    "čirpan",
    "čita",
    "cizre",
    "clane",
    "clerf",
    "cobh",
    "codru",
    "como",
    "corby",
    "cork",
    "çorlu",
    "çorum",
    "crewe",
    "çubuk",
    "cugir",
    "čuhuïv",
    "culm",
    "çumra",
    "cuneo",
    "dabas",
    "dáli",
    "debar",
    "dej",
    "delft",
    "derby",
    "derik",
    "derry",
    "detva",
    "deva",
    "didim",
    "diest",
    "dijon",
    "dinar",
    "doboj",
    "dobrič",
    "dobruš",
    "dráma",
    "dubno",
    "düren",
    "düzce",
    "łęczna",
    "ede",
    "edineț",
    "eeklo",
    "eger",
    "egio",
    "ekerö",
    "elâzığ",
    "elche",
    "elda",
    "elva",
    "elvas",
    "ëlwen",
    "elx",
    "emmen",
    "émpa",
    "ennis",
    "enns",
    "epe",
    "erbaa",
    "erciş",
    "érd",
    "erdek",
    "erzin",
    "esbo",
    "eskil",
    "eslöv",
    "espoo",
    "essen",
    "eupen",
    "evere",
    "évora",
    "eylau",
    "fafe",
    "falun",
    "fano",
    "farka",
    "farkë",
    "faro",
    "farum",
    "fatsa",
    "fiães",
    "fier",
    "fieri",
    "fløng",
    "foça",
    "forlì",
    "fót",
    "frunză",
    "fulda",
    "fürth",
    "futog",
    "gand",
    "gävle",
    "gazi",
    "gebze",
    "gediz",
    "geel",
    "gela",
    "genç",
    "genk",
    "gent",
    "genua",
    "gera",
    "géri",
    "getxo",
    "geyve",
    "gijón",
    "giroc",
    "give",
    "glatz",
    "göd",
    "goes",
    "gölbaşı",
    "gomel",
    "gönen",
    "gorey",
    "gospić",
    "gostyń",
    "gouda",
    "graz",
    "gürsu",
    "gyál",
    "gyömrő",
    "gyula",
    "hå",
    "håbo",
    "hadjač",
    "hagen",
    "hal",
    "halle",
    "hamar",
    "hamm",
    "hamme",
    "hanau",
    "hard",
    "hatay",
    "havza",
    "herne",
    "hobro",
    "hoei",
    "homieĺ",
    "hoorn",
    "hopa",
    "horki",
    "horta",
    "hull",
    "hulst",
    "hürth",
    "huy",
    "ibiza",
    "ieper",
    "ikast",
    "imola",
    "imst",
    "inis",
    "irpin",
    "irpin'",
    "irun",
    "irún",
    "iruña",
    "isjum",
    "isola",
    "izjum",
    "izmir",
    "izola",
    "jaén",
    "jalta",
    "jämsä",
    "janja",
    "jauer",
    "jawor",
    "jelsk",
    "jena",
    "jette",
    "jõhvi",
    "kâhta",
    "käl",
    "kaluš",
    "kaman",
    "kamëz",
    "kamza",
    "kaniv",
    "kaniw",
    "kapyĺ",
    "kars",
    "kasan",
    "kayl",
    "kazan",
    "kazan'",
    "keel",
    "kehra",
    "keila",
    "kells",
    "kelmė",
    "kemer",
    "kemi",
    "kepez",
    "kerč",
    "kiel",
    "kiew",
    "kiili",
    "kilis",
    "kirov",
    "kirow",
    "kíti",
    "kleck",
    "klepp",
    "kleve",
    "køge",
    "kolín",
    "köln",
    "komló",
    "konin",
    "konya",
    "koper",
    "korça",
    "korçë",
    "kos",
    "kotka",
    "kotor",
    "kovel'",
    "kowel",
    "kozan",
    "kozlu",
    "kranj",
    "krnov",
    "kruja",
    "krujë",
    "kukës",
    "kula",
    "kulu",
    "kumla",
    "kunda",
    "kursk",
    "kutno",
    "kyïv",
    "kysyl",
    "kyzyl",
    "l.",
    "laç",
    "laçi",
    "lagoa",
    "lagos",
    "lahti",
    "lamía",
    "laren",
    "lecce",
    "leeds",
    "león",
    "leova",
    "lepieĺ",
    "lerum",
    "lezha",
    "lezhë",
    "lida",
    "liège",
    "lienz",
    "lier",
    "lieto",
    "lille",
    "linz",
    "lissa",
    "lisse",
    "liubań",
    "livno",
    "lohja",
    "lojo",
    "loksa",
    "lom",
    "lomma",
    "lopik",
    "lorca",
    "loulé",
    "louny",
    "loveč",
    "löwen",
    "luban",
    "lubań",
    "lüben",
    "lubin",
    "lubny",
    "luboń",
    "lucca",
    "lucia",
    "luduș",
    "lugo",
    "lugoj",
    "luik",
    "luleå",
    "lund",
    "lünen",
    "lusk",
    "luton",
    "luzk",
    "lwiw",
    "lyck",
    "lyman",
    "lyon",
    "maia",
    "maiac",
    "mainz",
    "majak",
    "makó",
    "malmö",
    "malyn",
    "mamer",
    "maraş",
    "mark",
    "marki",
    "marl",
    "massa",
    "masty",
    "mazyr",
    "mediaș",
    "meise",
    "memel",
    "menen",
    "mengeš",
    "menin",
    "metz",
    "miass",
    "mijas",
    "milas",
    "minsk",
    "mizil",
    "moers",
    "mol",
    "molde",
    "monor",
    "mons",
    "monza",
    "mora",
    "moss",
    "most",
    "mosta",
    "mosyr",
    "motru",
    "moura",
    "mozyr'",
    "murom",
    "muş",
    "mut",
    "naas",
    "nacka",
    "namen",
    "namur",
    "nancy",
    "narva",
    "navan",
    "nes",
    "neuss",
    "nh.",
    "nibe",
    "nice",
    "nîmes",
    "niš",
    "nisch",
    "nitra",
    "nivå",
    "nizip",
    "nizza",
    "nokia",
    "nurdağı",
    "nybro",
    "nysa",
    "o.",
    "odder",
    "ödemiş",
    "odesa",
    "łódź",
    "oels",
    "of",
    "ogre",
    "ohlau",
    "ohrid",
    "olbia",
    "oltu",
    "ommen",
    "omsk",
    "opava",
    "opole",
    "ordu",
    "orël",
    "orhei",
    "orjol",
    "orsk",
    "oslo",
    "oss",
    "otaci",
    "oulu",
    "ovar",
    "łowicz",
    "ózd",
    "padua",
    "páfos",
    "paide",
    "paks",
    "pale",
    "palma",
    "pápa",
    "paris",
    "parla",
    "parma",
    "pärnu",
    "patos",
    "pavia",
    "payas",
    "pazin",
    "pécel",
    "pécs",
    "peine",
    "pejë",
    "pelt",
    "pensa",
    "penza",
    "peqin",
    "perm",
    "perm'",
    "petrič",
    "pinsk",
    "pinto",
    "pirok",
    "pirot",
    "pisa",
    "písek",
    "piteå",
    "plav",
    "plungė",
    "plzeň",
    "pola",
    "põlva",
    "pomáz",
    "poole",
    "pori",
    "porto",
    "posen",
    "poznań",
    "prag",
    "praha",
    "prato",
    "pskov",
    "pskow",
    "ptuj",
    "pula",
    "püssi",
    "qormi",
    "raab",
    "raahe",
    "radom",
    "rana",
    "ranst",
    "rapla",
    "rauma",
    "reda",
    "reims",
    "reni",
    "resen",
    "resno",
    "reus",
    "rho",
    "ribe",
    "ringe",
    "rivne",
    "riwne",
    "rize",
    "ródos",
    "rom",
    "roma",
    "roman",
    "romny",
    "rønne",
    "ronse",
    "rouen",
    "rubí",
    "rugby",
    "ruma",
    "rumia",
    "ruse",
    "rush",
    "russe",
    "ry",
    "şırnak",
    "šabac",
    "šachty",
    "sæby",
    "sagan",
    "šakiai",
    "saky",
    "sala",
    "sale",
    "salo",
    "sanem",
    "sanok",
    "saray",
    "şarköy",
    "sarny",
    "saue",
    "šavnik",
    "sebeș",
    "seda",
    "šeduva",
    "senec",
    "senta",
    "sereď",
    "serik",
    "sibbo",
    "sibiu",
    "šid",
    "siena",
    "siero",
    "siirt",
    "šilalė",
    "šilutė",
    "simav",
    "sindi",
    "sines",
    "sinj",
    "sinop",
    "sipoo",
    "sisak",
    "sitia",
    "sivas",
    "skien",
    "skive",
    "škloǔ",
    "sligo",
    "sluck",
    "sluis",
    "smila",
    "snina",
    "soest",
    "sofia",
    "sokal",
    "sokal'",
    "söke",
    "sola",
    "solin",
    "solna",
    "soma",
    "sopot",
    "sorau",
    "sorø",
    "šostka",
    "split",
    "śrem",
    "stein",
    "steyr",
    "štip",
    "stolp",
    "strib",
    "stryj",
    "sukth",
    "šumen",
    "sumy",
    "suruç",
    "tábor",
    "täby",
    "talas",
    "tapa",
    "tartu",
    "tata",
    "tczew",
    "telde",
    "telfs",
    "temse",
    "terme",
    "terni",
    "texel",
    "thiva",
    "thorn",
    "tiel",
    "tielt",
    "tierp",
    "time",
    "tire",
    "tivat",
    "tokat",
    "tomar",
    "tomsk",
    "toruń",
    "tõrva",
    "tosya",
    "tours",
    "trani",
    "traun",
    "trier",
    "trim",
    "trofa",
    "tséri",
    "tuam",
    "tula",
    "tune",
    "turda",
    "turek",
    "türi",
    "turin",
    "turku",
    "tuzi",
    "tuzla",
    "tver'",
    "twer",
    "tychy",
    "uccle",
    "udine",
    "ufa",
    "ukkel",
    "łuków",
    "ulm",
    "uman",
    "uman'",
    "umeå",
    "unna",
    "ünye",
    "urfa",
    "ürgüp",
    "urk",
    "urla",
    "utena",
    "uzda",
    "vaals",
    "vaasa",
    "vác",
    "vadsø",
    "vaduz",
    "valga",
    "van",
    "vanda",
    "varaš",
    "varde",
    "varna",
    "vasa",
    "vatra",
    "växjö",
    "veere",
    "vejen",
    "vejle",
    "veles",
    "venlo",
    "venta",
    "veria",
    "viby",
    "vic",
    "vidin",
    "vigo",
    "vihti",
    "viseu",
    "vlora",
    "vlorë",
    "võhma",
    "vólos",
    "vorst",
    "võru",
    "vraca",
    "vrbas",
    "vught",
    "warna",
    "waver",
    "wavre",
    "weert",
    "weiz",
    "wels",
    "wesel",
    "widin",
    "wieluń",
    "wien",
    "wigan",
    "wijk",
    "wilna",
    "wiltz",
    "wolz",
    "wörgl",
    "worms",
    "wraza",
    "york",
    "ypern",
    "ypres",
    "ystad",
    "żabbar",
    "zadar",
    "żagań",
    "žagarė",
    "žalec",
    "zamość",
    "żary",
    "žatec",
    "zeist",
    "zele",
    "zemst",
    "zeta",
    "zh.",
    "zile",
    "žilina",
    "zlín",
    "žlobin",
    "žodino",
    "żory",
    "żywiec"
]

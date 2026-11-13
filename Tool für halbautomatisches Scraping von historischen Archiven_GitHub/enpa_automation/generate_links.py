from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote

from enpa_common import (
    DEFAULT_CONFIG,
    RESULT_PAGE_SIZE,
    VALID_FALLTYPEN,
    build_search_url,
    clean,
    expand_categories,
    is_pilot,
    load_config,
    query_key,
    result_page_size,
    resolve_config_path,
    resolve_project_path,
)


BOOKMARKLET_JS = r"""(()=>{const C=t=>String(t||"").replace(/\s+/g," ").trim();const N=t=>String(t||"").normalize("NFD").replace(/[\u0300-\u036f]/g,"").toLowerCase().replace(/ß/g,"ss").replace(/[^a-z0-9]+/g," ").trim();const M=()=>{const m=location.hash.match(/enpa=([^&]+)/);if(!m)return{};try{return JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(decodeURIComponent(m[1])),c=>c.charCodeAt(0))))}catch(e){alert("ENPA-Metadaten konnten nicht gelesen werden: "+e.message);return{}}};const A=h=>{try{return new URL(h,location.href).href}catch{return h||""}};const esc=s=>String(s||"").replace(/[.*+?^${}()|[\]\\]/g,"\\$&");const rxTerm=t=>C(t).split("").map(ch=>{const l=ch.toLowerCase();if(/\s/.test(ch))return"\\s+";if("-‐‑‒–—".includes(ch))return"[-\\s‐‑‒–—]?";if(l==="ä")return"[äa?]";if(l==="ö")return"[öo?]";if(l==="ü")return"[üu?]";return esc(ch)}).join("");const rawHas=(txt,t)=>{const pat=rxTerm(t);if(!pat)return false;try{return new RegExp("(^|[^A-Za-zÀ-ÖØ-öø-ÿ0-9])"+pat+"(?=$|[^A-Za-zÀ-ÖØ-öø-ÿ0-9])","i").test(String(txt||""))}catch{return false}};const score=(sample,t,bonus)=>{if(!C(sample)||!C(t))return null;const raw=rawHas(sample,t);const pos=(" "+N(sample)+" ").indexOf(" "+N(t)+" ");if(!raw&&pos<0)return null;return{term:t,score:bonus+N(t).length+(raw?10:0),pos:pos<0?999999:pos}};const pick=(txt,terms,hits)=>{let best=null;const test=(sample,bonus)=>{(terms||[]).forEach(t=>{const s=score(sample,t,bonus);if(s&&(!best||s.score>best.score||(s.score===best.score&&s.pos<best.pos)))best=s})};(hits||[]).forEach(h=>test(h,10000));test(txt,1000);return best?best.term:""};const countTerms=(txt,terms,hits)=>{let n=0;(terms||[]).forEach(t=>{if(score(txt,t,1)||(hits||[]).some(h=>score(h,t,1)))n++});return n};const hi=el=>{const sel='mark,em,strong,b,span[class*="hit" i],span[class*="highlight" i],span[class*="search" i],span[class*="match" i],span[style*="background" i],span[style*="yellow" i],font[color]';return[...el.querySelectorAll(sel)].map(x=>C(x.textContent)).filter(x=>x&&x.length<120&&!/^\[.*\]$/.test(x))};const articleId=u=>{try{return new URL(u,location.href).searchParams.get("d")||""}catch{return""}};const pref=id=>(String(id||"").match(/^([A-Z]+)/)||[])[1]||"";const dat=id=>{const m=String(id||"").match(/^[A-Z]+(\d{4})(\d{2})(\d{2})/);return m?m[1]+"-"+m[2]+"-"+m[3]:""};const page=id=>{const m=String(id||"").match(/-\d+\.(\d+)(?:\.|$)/);return m?Number(m[1])+1:""};const box=a=>{let n=a;const l=C(a.textContent).length;for(let i=0;i<7&&n&&n.parentElement;i++){n=n.parentElement;const t=C(n.innerText||n.textContent||"");if(t.length>Math.max(90,l+40))return n}return a.parentElement||a};const totalHits=()=>{const parse=n=>{const s=String(n||"").replace(/[.'’]/g,"");return /^\d{1,7}$/.test(s)?Number(s):0};const num="(\\d{1,3}(?:[.'’]\\d{3})*|\\d{1,7})";const strong=[new RegExp("\\b\\d{1,7}\\s*[-–]\\s*\\d{1,7}\\s*(?:von|of)\\s*"+num+"\\s*(?:Treffer|Treffern|Ergebnisse|Ergebnissen|Resultate|Resultaten|results|matches)?\\b","i"),new RegExp("\\b(?:von|of)\\s*"+num+"\\s*(?:Treffer|Treffern|Ergebnisse|Ergebnissen|Resultate|Resultaten|results|matches)\\b","i")];const weak=new RegExp("\\b"+num+"\\s*(?:Treffer|Treffern|Ergebnisse|Ergebnissen|Resultate|Resultaten|results|matches)\\b","i");const texts=[];document.querySelectorAll("h1,h2,h3,p,div,span,li,td,th").forEach(el=>{const own=C(Array.from(el.childNodes).filter(n=>n.nodeType===3).map(n=>n.textContent).join(" "));const full=C(el.innerText||el.textContent||"");if(own.length>=4&&own.length<=240)texts.push(own);if(full.length>=4&&full.length<=240)texts.push(full)});for(const t of texts){for(const r of strong){const m=t.match(r);const n=m?parse(m[1]):0;if(n)return n}}for(const t of texts.slice(0,80)){const m=t.match(weak);const n=m?parse(m[1]):0;if(n)return n}return 0};const meta=M();const pub={};(meta.defaultPublications||[]).forEach(p=>pub[p.archiveCode]=p.excelCode);const map=new Map();document.querySelectorAll('a[href*="a=d"][href*="d="]').forEach(a=>{const href=A(a.getAttribute("href"));const raw=C(a.innerText||a.textContent||"");if(!href||!raw||/^\[.*\]$/.test(raw))return;const container=box(a);const text=C(container.innerText||container.textContent||"");const title=raw.replace(/\s*\[(ARTIKEL(?:\+ILLUSTRATION)?|ABSCHNITT|ILLUSTRATION)\]\s*$/i,"").trim();const hits=hi(container);const old=map.get(href);if(!old||title.length>old.title.length)map.set(href,{href,title,text,hits})});const records=[...map.values()].map((it,i)=>{const id=articleId(it.href);const p=pref(id);let sr=0;try{sr=Number(new URL(it.href,location.href).searchParams.get("srpos")||0)}catch{}if(!sr){const m=it.text.match(/^\s*(\d{1,5})[.)]/);sr=m?Number(m[1]):Number(meta.startRank||1)+i}const sample=it.title+" "+it.text;return{queryName:meta.queryName||"",eventName:meta.eventName||"",eventStart:meta.eventStart||"",eventEnd:meta.eventEnd||"",windowType:meta.windowType||"",dateFrom:meta.dateFrom||"",dateTo:meta.dateTo||"",falltyp:meta.falltyp||"",category:meta.category||"",categoryLabel:meta.categoryLabel||"",searchString:meta.searchString||"",searchTerms:meta.searchTerms||[],listUrl:location.href.replace(/#.*$/,""),detailUrl:it.href,articleId:id,newspaperArchiveCode:p,newspaperExcelCode:pub[p]||p||"",issueDate:dat(id),issueNumber:"",page:page(id),hitPosition:sr,title:C(it.title),segmentId:C(it.title),rubric:"",snippet:C(it.text),articleText:"",matchedTerm:pick(sample,meta.searchTerms||[],it.hits),matchedTermRaw:C((it.hits||[]).join("; ")),matchedTermCount:countTerms(sample,meta.searchTerms||[],it.hits),scrapedAt:new Date().toISOString()}});const ps=Number(meta.pageSize)||100;let total=totalHits();if(!total&&records.length<ps)total=Number(meta.startRank||1)+records.length-1;const qkey=[meta.dateFrom||"",meta.dateTo||"",meta.category||"",meta.searchString||"",(meta.defaultPublications||[]).map(p=>p.archiveCode||p).join(",")].join("||");records.forEach(r=>{r.totalResultCount=total;r.totalResultCountParserVersion=4;r.queryKey=qkey;r.pageStartRank=meta.startRank||1;r.pageSize=ps});const payload={metadata:{source:"e-newspaperarchives.ch",manualCapture:true,captureUrl:location.href.replace(/#.*$/,""),capturedAt:new Date().toISOString(),recordCount:records.length,totalResultCount:total,queryKey:qkey,pageStartRank:meta.startRank||1,pageSize:ps,totalResultCountParserVersion:4,captureFilePrefix:meta.captureFilePrefix||"enpa_v2"},records};const blob=new Blob([JSON.stringify(payload,null,2)],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);const prefix=String(meta.captureFilePrefix||"enpa_v2").replace(/[^A-Za-z0-9_.-]+/g,"_");a.download=prefix+"_"+(meta.category||"X")+"_"+(meta.dateFrom||"date")+"_"+(meta.startRank||"1")+".json";document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},1000);alert(records.length+" Treffer erfasst. JSON wurde heruntergeladen.")})();"""
_UNRELIABLE_FRONTEND_PAGE_PARSER = (
    r'''const page=id=>{const m=String(id||"").match(/-\d+\.(\d+)(?:\.|$)/);return m?Number(m[1])+1:""};'''
)
if _UNRELIABLE_FRONTEND_PAGE_PARSER not in BOOKMARKLET_JS:
    raise RuntimeError("Der erwartete alte ENPA-Seitenparser wurde nicht gefunden.")
BOOKMARKLET_JS = BOOKMARKLET_JS.replace(
    _UNRELIABLE_FRONTEND_PAGE_PARSER,
    r'''const page=id=>"";''',
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Erzeugt ENPA-V2-Linkliste mit Bookmarklet.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--out", default="")
    parser.add_argument("--capture-dir", default="")
    parser.add_argument("--falltyp", default="")
    return parser.parse_args()


def choose_falltyp(default: str) -> str:
    print("Falltyp fuer die Linkliste auswaehlen:")
    for idx, value in enumerate(VALID_FALLTYPEN, start=1):
        print(f"  {idx}. {value}")
    try:
        default_idx = VALID_FALLTYPEN.index(default) + 1
    except ValueError:
        default_idx = 1
    raw = input(f"Nummer eingeben (Standard {default_idx}): ").strip() or str(default_idx)
    try:
        number = max(1, min(len(VALID_FALLTYPEN), int(raw)))
    except ValueError:
        number = default_idx
    return VALID_FALLTYPEN[number - 1]


def safe_prefix(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", clean(value) or "enpa_v2")


def capture_page_size(meta: dict[str, Any], first: dict[str, Any]) -> int:
    for value in (meta.get("pageSize"), first.get("pageSize")):
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            continue
        if parsed > 0:
            return parsed
    source_url = clean(meta.get("captureUrl") or first.get("listUrl"))
    match = re.search(r"-de-(\d+)-", unquote(source_url))
    return int(match.group(1)) if match else 20


def capture_block_complete(
    entry: dict[str, Any],
    start_rank: int,
    total: int | None,
    page_size: int,
) -> bool:
    if total == 0:
        return True
    end_rank = start_rank + page_size - 1
    if total is not None:
        end_rank = min(end_rank, total)
    if end_rank < start_rank:
        return True
    positions = entry.get("positions", set())
    return all(rank in positions for rank in range(start_rank, end_rank + 1))


def load_capture_counts(capture_dir: Path, prefix: str) -> dict[str, dict[str, Any]]:
    counts: dict[str, dict[str, Any]] = {}
    if not capture_dir.exists():
        return counts
    for path in sorted(capture_dir.glob(f"{prefix}_*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        meta = payload.get("metadata") or {}
        records = payload.get("records") or []
        first = records[0] if records else {}
        key = clean(meta.get("queryKey") or first.get("queryKey"))
        if not key:
            continue
        total = meta.get("totalResultCount", first.get("totalResultCount", None))
        start_rank = int(meta.get("pageStartRank") or first.get("pageStartRank") or first.get("hitPosition") or 1)
        captured_page_size = capture_page_size(meta, first)
        if not isinstance(total, int):
            try:
                total = int(total)
            except Exception:
                total = None
        if isinstance(total, int) and total < max(0, start_rank - 1):
            total = None
        if total is None and len(records) < captured_page_size:
            total = start_rank + len(records) - 1
        entry = counts.setdefault(
            key,
            {
                "total": None,
                "pages": set(),
                "positions": set(),
                "pageSizes": set(),
                "source": str(path),
            },
        )
        if records or total == 0:
            entry["pages"].add(start_rank)
        entry["pageSizes"].add(captured_page_size)
        for index, record in enumerate(records):
            try:
                position = int(record.get("hitPosition") or 0)
            except (TypeError, ValueError):
                position = 0
            entry["positions"].add(position if position > 0 else start_rank + index)
        if isinstance(total, int) and total >= 0:
            old = entry["total"]
            entry["total"] = total if old is None else max(old, total)
            entry["source"] = str(path)
    return counts


def fixed_max(config: dict[str, Any]) -> int:
    page_size = result_page_size(config)
    if is_pilot(config.get("falltyp", "")):
        return int(config.get("pilotMaxResultsPerQuery") or page_size)
    value = config.get("maxResultsPerQuery")
    if isinstance(value, int) and value > 0:
        return value
    return page_size


def build_rows(config: dict[str, Any], counts: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    auto = not is_pilot(config.get("falltyp", "")) and str(config.get("maxResultsPerQuery", "")).lower() == "auto"
    page_size = result_page_size(config)
    initial = max(page_size, int(config.get("autoInitialResultsPerQuery") or page_size))
    for query in config.get("queries", []):
        for category in expand_categories(config):
            url, meta = build_search_url(config, query, category, 1)
            key = query_key(meta)
            known = counts.get(key)
            known_total = known.get("total") if known else None
            if auto and known_total is not None:
                max_results = known_total
            elif auto and known:
                next_probe = 1
                while capture_block_complete(known, next_probe, None, page_size):
                    next_probe += page_size
                max_results = max(initial, next_probe)
            else:
                max_results = initial if auto else fixed_max(config)
            for start_rank in range(1, max_results + 1, page_size):
                if auto and known and capture_block_complete(
                    known, start_rank, known_total, page_size
                ):
                    continue
                page_url, page_meta = build_search_url(config, query, category, start_rank)
                page_meta["totalResultCount"] = known_total if known_total is not None else ""
                page_url = page_url.rsplit("#enpa=", 1)[0] + "#enpa=" + quote(__import__("base64").b64encode(json.dumps(page_meta, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).decode("ascii"))
                rows.append({
                    "task": "Folgeseite erfassen" if known_total is not None and start_rank > 1 else ("Startseite erfassen" if known_total is not None else "Trefferzahl erfassen"),
                    "query": query.get("name", ""),
                    "category": category,
                    "startRank": start_rank,
                    "pageSize": page_size,
                    "total": known_total,
                    "url": page_url,
                    "searchString": page_meta["searchString"],
                })
    return rows


def build_html(config: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    bookmarklet = "javascript:" + quote(BOOKMARKLET_JS, safe="")
    prefix = safe_prefix(config.get("captureFilePrefix", "enpa_v2"))
    generated = __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if rows:
        body = "\n".join(
            "<tr>"
            f"<td>{idx}</td><td>{html.escape(row['task'])}</td><td>{html.escape(row['query'])}</td>"
            f"<td>{html.escape(row['category'])}</td><td>{row['startRank']}</td>"
            f"<td>{html.escape(str(row['total']) if row['total'] is not None else 'noch unbekannt')}</td>"
            f"<td><a href=\"{html.escape(row['url'])}\" target=\"_blank\" rel=\"noreferrer\">Suchseite oeffnen</a></td>"
            f"<td>{html.escape(row['searchString'])}</td></tr>"
            for idx, row in enumerate(rows, start=1)
        )
    else:
        body = '<tr><td colspan="8">Keine offenen Trefferseiten. Jetzt kann importiert oder validiert werden.</td></tr>'
    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>ENPA V2 Linkliste</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; line-height: 1.45; color: #1f2933; }}
    code {{ font-family: Consolas, monospace; }}
    .bookmarklet {{ display: inline-block; padding: 10px 14px; border: 1px solid #334155; border-radius: 6px; background: #f8fafc; color: #111827; text-decoration: none; font-weight: 700; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 20px; font-size: 14px; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 6px 8px; vertical-align: top; }}
    th {{ background: #e2e8f0; text-align: left; }}
  </style>
</head>
<body>
  <h1>ENPA V2 Linkliste</h1>
  <p>Generiert am {html.escape(generated)}. Capture-Dateien werden als <code>{html.escape(prefix)}_*.json</code> heruntergeladen.</p>
  <p>Bookmarklet neu in die Lesezeichenleiste ziehen: <a class="bookmarklet" href="{bookmarklet}">ENPA erfassen</a></p>
  <p>Jede Suchseite zeigt bis zu {result_page_size(config)} Treffer. Folgeseiten beginnen bei 101, 201, 301 usw.</p>
  <p>Arbeite zuerst alle Zeilen mit <code>Trefferzahl erfassen</code> ab. Danach diesen Generator erneut starten; die Liste zeigt dann nur noch offene Folgeseiten.</p>
  <table>
    <thead><tr><th>#</th><th>Aufgabe</th><th>Suchfenster</th><th>Kat.</th><th>Start</th><th>Trefferzahl</th><th>Link</th><th>Suchstring</th></tr></thead>
    <tbody>{body}</tbody>
  </table>
</body>
</html>
"""


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    if args.falltyp:
        config["falltyp"] = args.falltyp
    else:
        config["falltyp"] = choose_falltyp(config.get("falltyp", "Kalibrierung"))
    config["captureFilePrefix"] = safe_prefix(config.get("captureFilePrefix", "enpa_v2"))
    capture_dir = resolve_project_path(config, args.capture_dir) if args.capture_dir else resolve_config_path(config, config.get("captureDir"))
    assert capture_dir is not None
    out_path = resolve_project_path(config, args.out) if args.out else resolve_config_path(config, config.get("outputDir")) / "manual_capture_links.html"
    assert out_path is not None
    out_path.parent.mkdir(parents=True, exist_ok=True)
    counts = load_capture_counts(capture_dir, config["captureFilePrefix"])
    rows = build_rows(config, counts)
    out_path.write_text(build_html(config, rows), encoding="utf-8")
    total_queries = len(config.get("queries", [])) * len(expand_categories(config))
    active_keys = {
        query_key(build_search_url(config, query, category, 1)[1])
        for query in config.get("queries", [])
        for category in expand_categories(config)
    }
    known_active = sum(
        1
        for key in active_keys
        if key in counts and counts[key].get("total") is not None
    )
    print(f"MANUAL_LINKS_HTML={out_path}")
    print(f"Offene Links: {len(rows)}")
    print(f"Bekannte Trefferzaehlen: {known_active} von {total_queries}")


if __name__ == "__main__":
    main()

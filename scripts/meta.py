#!/usr/bin/env python3
"""Look up paper metadata from real sources only. Never from model memory.

Every result is JSON and carries a "source" field saying where it came from.
If nothing is found the script prints {"found": false, ...} and exits 1, so the
caller must mark the reference as unresolved instead of guessing.

Usage:
  python3 scripts/meta.py bib <citekey>            # zotero/library.bib (Better BibTeX export)
  python3 scripts/meta.py arxiv <arxiv-id>         # arXiv API
  python3 scripts/meta.py doi <doi>                # Semantic Scholar
  python3 scripts/meta.py title "<paper title>"    # Semantic Scholar best match
  python3 scripts/meta.py refs <arxiv-id|doi>      # references of a paper (Semantic Scholar),
                                                   # influential ones first: use for Foundations
  python3 scripts/meta.py search "<query>" [n]     # Semantic Scholar keyword search

Set S2_API_KEY in your environment for higher Semantic Scholar rate limits (optional).
Standard library only.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
BIB = VAULT / "zotero" / "library.bib"
S2 = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "title,authors,year,venue,externalIds,abstract,citationCount,url,publicationDate"
UA = "phd-vault-meta/1.0"


def out(obj, ok=True):
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    sys.exit(0 if ok else 1)


def not_found(kind, query, why):
    out({"found": False, "kind": kind, "query": query, "reason": why,
         "instruction": "Mark this reference [!unverified] with metadata_source: unresolved. Do not fill in from memory."}, ok=False)


def http_get(url, headers=None, retries=3):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2 * (attempt + 1) + 1)
                continue
            raise
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(2)
                continue
            raise
    return None


def s2_get(path, params=None):
    url = f"{S2}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {}
    if os.environ.get("S2_API_KEY"):
        headers["x-api-key"] = os.environ["S2_API_KEY"]
    raw = http_get(url, headers)
    return json.loads(raw) if raw else None


def s2_norm(p):
    ext = p.get("externalIds") or {}
    return {
        "found": True,
        "source": "semantic-scholar",
        "title": p.get("title"),
        "authors": [a.get("name") for a in (p.get("authors") or [])],
        "year": p.get("year"),
        "venue": p.get("venue") or None,
        "arxiv": ext.get("ArXiv"),
        "doi": ext.get("DOI"),
        "s2_id": p.get("paperId"),
        "url": p.get("url"),
        "citation_count": p.get("citationCount"),
        "abstract": p.get("abstract"),
        "abstract_note": "This is the API abstract, not the paper body. Label it as abstract if used.",
    }


# ---------- BibTeX (Better BibTeX export) ----------

def parse_bib(text):
    """Minimal BibTeX parser: returns {citekey: {field: value}}."""
    entries = {}
    i = 0
    while True:
        m = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", re.S).search(text, i)
        if not m:
            break
        etype, key = m.group(1).lower(), m.group(2)
        depth, j = 1, m.end()
        while j < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            j += 1
        body = text[m.end(): j - 1]
        fields = {"ENTRYTYPE": etype}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            name, k = fm.group(1).lower(), fm.end()
            if k < len(body) and body[k] == "{":
                d, s = 1, k + 1
                k += 1
                while k < len(body) and d:
                    d += {"{": 1, "}": -1}.get(body[k], 0)
                    k += 1
                val = body[s: k - 1]
            elif k < len(body) and body[k] == '"':
                e = body.find('"', k + 1)
                val = body[k + 1: e]
            else:
                val = re.match(r"[^,\n]*", body[k:]).group(0)
            fields.setdefault(name, re.sub(r"\s+", " ", val.replace("{", "").replace("}", "")).strip())
        entries[key] = fields
        i = j
    return entries


def cmd_bib(key):
    if not BIB.exists():
        not_found("bib", key, f"{BIB.relative_to(VAULT)} does not exist. Set up the Better BibTeX auto-export (see README).")
    entries = parse_bib(BIB.read_text(encoding="utf-8", errors="replace"))
    e = entries.get(key)
    if not e:
        close = [k for k in entries if key.lower()[:6] in k.lower()][:5]
        not_found("bib", key, f"citekey not in library.bib. Similar keys: {close}")
    pdfs = [p for p in re.split(r";", e.get("file", "")) if p.lower().endswith(".pdf")]
    out({
        "found": True, "source": "zotero", "citekey": key,
        "title": e.get("title"),
        "authors": [a.strip() for a in e.get("author", "").split(" and ") if a.strip()],
        "year": e.get("year") or (e.get("date", "")[:4] or None),
        "venue": e.get("booktitle") or e.get("journal") or e.get("journaltitle") or e.get("publisher"),
        "arxiv": e.get("eprint") if "arxiv" in (e.get("archiveprefix", "") + e.get("eprinttype", "")).lower() else None,
        "doi": e.get("doi"), "url": e.get("url"),
        "pdf": pdfs[0] if pdfs else None, "all_files": pdfs,
    })


# ---------- arXiv ----------

def clean_arxiv(aid):
    aid = aid.strip()
    aid = re.sub(r"^(https?://)?(www\.)?arxiv\.org/(abs|pdf)/", "", aid, flags=re.I)
    aid = re.sub(r"^arxiv:", "", aid, flags=re.I)
    return re.sub(r"\.pdf$", "", aid)


def cmd_arxiv(aid):
    aid = clean_arxiv(aid)
    raw = http_get("https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": aid}))
    if not raw:
        not_found("arxiv", aid, "arXiv API returned nothing")
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    entry = ET.fromstring(raw).find("a:entry", ns)
    if entry is None or entry.find("a:title", ns) is None or "Error" in (entry.findtext("a:title", "", ns)):
        not_found("arxiv", aid, "no such arXiv id")
    published = entry.findtext("a:published", "", ns)
    out({
        "found": True, "source": "arxiv", "arxiv": aid,
        "title": re.sub(r"\s+", " ", entry.findtext("a:title", "", ns)).strip(),
        "authors": [a.findtext("a:name", "", ns) for a in entry.findall("a:author", ns)],
        "year": int(published[:4]) if published else None,
        "published": published[:10],
        "venue": entry.findtext("arxiv:journal_ref", None, ns),
        "doi": entry.findtext("arxiv:doi", None, ns),
        "categories": [c.get("term") for c in entry.findall("a:category", ns)],
        "url": f"https://arxiv.org/abs/{aid}",
        "pdf_url": f"https://arxiv.org/pdf/{aid}",
        "abstract": re.sub(r"\s+", " ", entry.findtext("a:summary", "", ns)).strip(),
        "abstract_note": "This is the API abstract, not the paper body. Label it as abstract if used.",
    })


# ---------- Semantic Scholar ----------

def s2_id(ref):
    ref = ref.strip()
    if re.match(r"^10\.\d{4,}/", ref) or ref.lower().startswith("doi:"):
        return "DOI:" + re.sub(r"^doi:", "", ref, flags=re.I)
    if re.match(r"^(arxiv:)?\d{4}\.\d{4,5}(v\d+)?$", ref, re.I) or "arxiv.org" in ref:
        return "ARXIV:" + re.sub(r"v\d+$", "", clean_arxiv(ref))
    return ref  # assume S2 paper id


def cmd_doi(doi):
    p = s2_get(f"/paper/{urllib.parse.quote(s2_id(doi), safe=':/')}", {"fields": S2_FIELDS})
    if not p:
        not_found("doi", doi, "Semantic Scholar has no record")
    out(s2_norm(p))


def cmd_title(title):
    r = s2_get("/paper/search/match", {"query": title, "fields": S2_FIELDS})
    data = (r or {}).get("data") or []
    if not data:
        not_found("title", title, "no Semantic Scholar match")
    p = s2_norm(data[0])
    p["match_score"] = data[0].get("matchScore")
    p["check"] = "Title match is fuzzy: confirm the returned title and year match what the paper cites."
    out(p)


def cmd_search(query, n=10):
    r = s2_get("/paper/search", {"query": query, "fields": "title,authors,year,venue,externalIds,citationCount", "limit": n})
    data = (r or {}).get("data") or []
    out({"found": bool(data), "source": "semantic-scholar", "query": query,
         "results": [{k: v for k, v in s2_norm(p).items() if k not in ("abstract", "abstract_note", "found", "source")} for p in data]},
        ok=bool(data))


def cmd_refs(ref):
    pid = urllib.parse.quote(s2_id(ref), safe=":/")
    r = s2_get(f"/paper/{pid}/references",
               {"fields": "title,authors,year,venue,externalIds,citationCount,isInfluential,intents", "limit": 1000})
    data = (r or {}).get("data") or []
    if not data:
        not_found("refs", ref, "Semantic Scholar has no reference list for this paper (publisher may hide it)")
    rows = []
    for d in data:
        p = d.get("citedPaper") or {}
        if not p.get("title"):
            continue
        row = {k: v for k, v in s2_norm(p).items() if k not in ("abstract", "abstract_note", "found", "source", "url")}
        row["influential"] = bool(d.get("isInfluential"))
        row["intents"] = d.get("intents") or []
        rows.append(row)
    rows.sort(key=lambda x: (not x["influential"], -(x.get("citation_count") or 0)))
    out({"found": True, "source": "semantic-scholar", "paper": ref, "n": len(rows),
         "note": "Influential = Semantic Scholar's signal, not proof. Confirm in the paper's own text (where it says it builds on the work) before listing as a foundation.",
         "references": rows})


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        sys.exit(2)
    cmd, arg = argv[1], argv[2]
    try:
        if cmd == "bib":
            cmd_bib(arg)
        elif cmd == "arxiv":
            cmd_arxiv(arg)
        elif cmd == "doi":
            cmd_doi(arg)
        elif cmd == "title":
            cmd_title(arg)
        elif cmd == "refs":
            cmd_refs(arg)
        elif cmd == "search":
            cmd_search(arg, int(argv[3]) if len(argv) > 3 else 10)
        else:
            print(__doc__)
            sys.exit(2)
    except (urllib.error.URLError, TimeoutError, ET.ParseError) as e:
        not_found(cmd, arg, f"network or parse error: {e}. Try again later; do not guess.")


if __name__ == "__main__":
    main(sys.argv)

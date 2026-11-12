#!/usr/bin/env python3
"""Verificación en línea y cacheada de DOI, arXiv y URL.

No modifica el .bib ni el manuscrito. Las respuestas se guardan en cache/ para
que la auditoría pueda reproducirse sin depender de la red.

Uso:
    python3 verificar_fuentes.py --repo /ruta/al/repositorio
    python3 verificar_fuentes.py --solo-doi
    python3 verificar_fuentes.py --solo-url
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

TARGET_DIR = Path(__file__).resolve().parent
CACHE_DIR = TARGET_DIR / "cache"
DEFAULT_INVENTORY = TARGET_DIR / "inventario_bibliografia.csv"
USER_AGENT = "tesis-bibliography-audit/1.0 (https://github.com/LUS24/tesis-maestria-data-mining)"
TIMEOUT = 20


def normalize(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = value.lower()
    value = re.sub(r"[^a-z0-9áéíóúüñç]+", " ", value, flags=re.I)
    return re.sub(r"\s+", " ", value).strip()


def title_similarity(a: str, b: str) -> float:
    from difflib import SequenceMatcher

    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0
    return round(SequenceMatcher(None, na, nb).ratio(), 4)


def surname(value: str) -> str:
    raw = (value or "").strip()
    if not raw:
        return ""
    if "," in raw:
        return normalize(raw.split(",", 1)[0].strip())
    return normalize(raw.split()[-1])


def cache_path(kind: str, identifier: str) -> Path:
    digest = hashlib.sha256(f"{kind}:{identifier}".encode("utf-8")).hexdigest()[:24]
    return CACHE_DIR / kind / f"{digest}.json"


def load_cache(kind: str, identifier: str):
    path = cache_path(kind, identifier)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
    return None


def save_cache(kind: str, identifier: str, payload: dict) -> None:
    path = cache_path(kind, identifier)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(payload)
    payload["_cache"] = {
        "kind": kind,
        "identifier": identifier,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def get_json(url: str, kind: str, identifier: str, retries: int = 2) -> dict:
    cached = load_cache(kind, identifier)
    if cached is not None:
        return cached
    last_error = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                payload = {
                    "http_status": response.status,
                    "url": response.geturl(),
                    "body": json.loads(response.read().decode("utf-8", errors="replace")),
                }
            save_cache(kind, identifier, payload)
            return payload
        except urllib.error.HTTPError as exc:
            last_error = exc
            payload = {
                "http_status": exc.code,
                "url": url,
                "error": str(exc),
                "body": None,
            }
            if exc.code in (400, 404):
                save_cache(kind, identifier, payload)
                return payload
            time.sleep(1.5 * (attempt + 1))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    payload = {
        "http_status": None,
        "url": url,
        "error": str(last_error),
        "body": None,
    }
    save_cache(kind, identifier, payload)
    return payload


def check_url(url: str, retries: int = 1) -> dict:
    cached = load_cache("url", url)
    if cached is not None:
        return cached
    last_error = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8",
                "Range": "bytes=0-4096",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                data = response.read(4096)
                content_type = response.headers.get("Content-Type", "")
                title = ""
                if "html" in content_type.lower():
                    text = data.decode("utf-8", errors="replace")
                    m = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.I | re.S)
                    if m:
                        title = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
                payload = {
                    "http_status": response.status,
                    "final_url": response.geturl(),
                    "content_type": content_type,
                    "title": title,
                    "error": None,
                }
            save_cache("url", url, payload)
            return payload
        except urllib.error.HTTPError as exc:
            # 403/405/429 no significan necesariamente que el recurso no exista.
            payload = {
                "http_status": exc.code,
                "final_url": url,
                "content_type": exc.headers.get("Content-Type", "") if exc.headers else "",
                "title": "",
                "error": str(exc),
            }
            if exc.code in (400, 401, 403, 404, 405, 410, 429):
                save_cache("url", url, payload)
                return payload
            last_error = exc
            time.sleep(1.0 * (attempt + 1))
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1.0 * (attempt + 1))
    payload = {
        "http_status": None,
        "final_url": url,
        "content_type": "",
        "title": "",
        "error": str(last_error),
    }
    save_cache("url", url, payload)
    return payload


def crossref_metadata(doi: str) -> dict:
    encoded = urllib.parse.quote(doi, safe="")
    payload = get_json(f"https://api.crossref.org/works/{encoded}", "crossref", doi)
    if payload.get("http_status") == 200 and payload.get("body"):
        item = payload["body"].get("message", {})
        title = " ".join(item.get("title") or [])
        authors = []
        for author in item.get("author") or []:
            if author.get("family"):
                authors.append(f"{author.get('family')}, {author.get('given', '')}".strip(", "))
            elif author.get("name"):
                authors.append(author["name"])
        issued = item.get("issued", {}).get("date-parts") or [[None]]
        year = issued[0][0] if issued and issued[0] else None
        return {
            "found": True,
            "source": "Crossref",
            "title": title,
            "authors": authors,
            "year": str(year) if year else "",
            "container": " ".join(item.get("container-title") or []),
            "type": item.get("type", ""),
            "publisher": item.get("publisher", ""),
            "url": item.get("URL", ""),
            "raw_status": payload.get("http_status"),
        }
    return {"found": False, "source": "Crossref", "raw_status": payload.get("http_status"), "error": payload.get("error")}


def datacite_metadata(doi: str) -> dict:
    encoded = urllib.parse.quote(doi, safe="")
    payload = get_json(f"https://api.datacite.org/dois/{encoded}", "datacite", doi)
    if payload.get("http_status") == 200 and payload.get("body"):
        item = payload["body"].get("data", {}).get("attributes", {})
        title = " ".join(t.get("title", "") for t in item.get("titles") or [])
        authors = []
        for creator in item.get("creators") or []:
            if creator.get("name"):
                authors.append(creator["name"])
            elif creator.get("familyName"):
                authors.append(f"{creator.get('familyName')}, {creator.get('givenName', '')}".strip(", "))
        return {
            "found": True,
            "source": "DataCite",
            "title": title,
            "authors": authors,
            "year": str(item.get("publicationYear") or ""),
            "container": item.get("publisher", ""),
            "type": (item.get("types") or {}).get("resourceTypeGeneral", ""),
            "publisher": item.get("publisher", ""),
            "url": item.get("url", ""),
            "raw_status": payload.get("http_status"),
        }
    return {"found": False, "source": "DataCite", "raw_status": payload.get("http_status"), "error": payload.get("error")}


def arxiv_ids_from_url(url: str) -> str:
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?", url or "")
    return m.group(1) if m else ""


def arxiv_metadata(arxiv_id: str) -> dict:
    cached = load_cache("arxiv", arxiv_id)
    if cached is not None:
        return cached
    url = f"https://export.arxiv.org/api/query?id_list={urllib.parse.quote(arxiv_id)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            xml = response.read().decode("utf-8", errors="replace")
        entry = re.search(r"<entry>(.*?)</entry>", xml, flags=re.S)
        if not entry:
            payload = {"found": False, "http_status": response.status, "error": "sin entry"}
        else:
            block = entry.group(1)

            def tag(name: str) -> str:
                m = re.search(rf"<{name}[^>]*>(.*?)</{name}>", block, flags=re.S)
                return html.unescape(re.sub(r"\s+", " ", m.group(1))).strip() if m else ""

            authors = [
                html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
                for m in re.finditer(r"<name>(.*?)</name>", block, flags=re.S)
            ]
            payload = {
                "found": True,
                "http_status": response.status,
                "title": tag("title"),
                "authors": authors,
                "year": tag("published")[:4],
                "container": "arXiv",
                "url": tag("id"),
            }
        save_cache("arxiv", arxiv_id, payload)
        return payload
    except Exception as exc:  # noqa: BLE001
        payload = {"found": False, "http_status": None, "error": str(exc)}
        save_cache("arxiv", arxiv_id, payload)
        return payload


def compare(record: dict, meta: dict) -> tuple[str, str, str, str]:
    if not meta.get("found"):
        return "no_encontrado", "", "", meta.get("error", "")
    title = record.get("titulo", "")
    sim = title_similarity(title, meta.get("title", "")) if title and meta.get("title") else 0.0
    year_ok = (str(record.get("anio", "")) == str(meta.get("year", ""))) if record.get("anio") and meta.get("year") else False
    entry_surnames = {surname(a) for a in record.get("autores", "").split(" | ") if a and a != "others"}
    meta_surnames = {surname(a) for a in meta.get("authors", []) if a}
    author_ok = bool(entry_surnames & meta_surnames)
    flags = []
    if sim < 0.90:
        flags.append("titulo")
    if not year_ok:
        flags.append("anio")
    if not author_ok:
        flags.append("autor")
    status = "coincide" if not flags else "discrepancia_" + "_".join(flags)
    return status, f"{sim:.4f}", "si" if year_ok else "no", "si" if author_ok else "no"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--solo-doi", action="store_true")
    parser.add_argument("--con-arxiv", action="store_true", help="Verificar arXiv dentro de este script; por defecto se usa verificar_arxiv_lotes.py")
    parser.add_argument("--solo-url", action="store_true")
    args = parser.parse_args()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    with args.inventory.open(encoding="utf-8-sig", newline="") as f:
        records = list(csv.DictReader(f))

    doi_rows = []
    arxiv_rows = []
    url_rows = []

    if not args.solo_url:
        for row in records:
            doi = (row.get("doi") or "").strip()
            if doi:
                meta = crossref_metadata(doi)
                if not meta.get("found"):
                    meta = datacite_metadata(doi)
                status, sim, year_ok, author_ok = compare(row, meta)
                doi_rows.append(
                    {
                        "clave": row["clave"],
                        "doi": doi,
                        "fuente_metadatos": meta.get("source", ""),
                        "estado": status,
                        "similitud_titulo": sim,
                        "anio_coincide": year_ok,
                        "autor_coincide": author_ok,
                        "titulo_registrado": row.get("titulo", ""),
                        "titulo_fuente": meta.get("title", ""),
                        "anio_registrado": row.get("anio", ""),
                        "anio_fuente": meta.get("year", ""),
                        "autores_registrados": row.get("autores", ""),
                        "autores_fuente": " | ".join(meta.get("authors", [])),
                        "venue_fuente": meta.get("container", ""),
                        "url_fuente": meta.get("url", ""),
                        "http_status": meta.get("raw_status", ""),
                        "error": meta.get("error", ""),
                    }
                )
                time.sleep(0.12)

            aid = arxiv_ids_from_url(row.get("url", ""))
            if aid and args.con_arxiv:
                meta = arxiv_metadata(aid)
                status, sim, year_ok, author_ok = compare(row, meta)
                arxiv_rows.append(
                    {
                        "clave": row["clave"],
                        "arxiv_id": aid,
                        "estado": status,
                        "similitud_titulo": sim,
                        "anio_coincide": year_ok,
                        "autor_coincide": author_ok,
                        "titulo_registrado": row.get("titulo", ""),
                        "titulo_arxiv": meta.get("title", ""),
                        "anio_registrado": row.get("anio", ""),
                        "anio_arxiv": meta.get("year", ""),
                        "autores_arxiv": " | ".join(meta.get("authors", [])),
                        "http_status": meta.get("http_status", ""),
                        "error": meta.get("error", ""),
                    }
                )
                time.sleep(0.12)

    if not args.solo_doi:
        for i, row in enumerate(records, 1):
            url = (row.get("url") or "").strip()
            if not url:
                continue
            result = check_url(url)
            url_rows.append(
                {
                    "clave": row["clave"],
                    "url": url,
                    "http_status": result.get("http_status"),
                    "url_final": result.get("final_url", ""),
                    "content_type": result.get("content_type", ""),
                    "titulo_pagina": result.get("title", ""),
                    "error": result.get("error", ""),
                }
            )
            if i % 20 == 0:
                print(f"URL verificadas: {i}/{len(records)}", file=sys.stderr)
            time.sleep(0.08)

    def write_csv(name: str, rows: list[dict], fields: list[str]) -> None:
        with (TARGET_DIR / name).open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    if doi_rows:
        write_csv(
            "verificacion_doi.csv",
            doi_rows,
            list(doi_rows[0].keys()),
        )
    if arxiv_rows:
        write_csv(
            "verificacion_arxiv.csv",
            arxiv_rows,
            list(arxiv_rows[0].keys()),
        )
    if url_rows:
        write_csv(
            "verificacion_url.csv",
            url_rows,
            list(url_rows[0].keys()),
        )

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "n_records": len(records),
        "n_doi": len(doi_rows),
        "doi_estados": {},
        "n_arxiv": len(arxiv_rows),
        "arxiv_estados": {},
        "n_url": len(url_rows),
        "url_estados": {},
        "nota": "Un HTTP 401/403/405/429 no prueba que el recurso no exista; requiere revisión manual.",
    }
    for row in doi_rows:
        summary["doi_estados"][row["estado"]] = summary["doi_estados"].get(row["estado"], 0) + 1
    for row in arxiv_rows:
        summary["arxiv_estados"][row["estado"]] = summary["arxiv_estados"].get(row["estado"], 0) + 1
    for row in url_rows:
        status = str(row["http_status"])
        summary["url_estados"][status] = summary["url_estados"].get(status, 0) + 1
    (TARGET_DIR / "resumen_verificacion_online.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

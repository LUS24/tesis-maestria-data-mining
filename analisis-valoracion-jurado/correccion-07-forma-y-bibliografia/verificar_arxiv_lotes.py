#!/usr/bin/env python3
"""Verifica los arXiv IDs en lotes para evitar el límite 429 del API.

Lee inventario_bibliografia.csv y escribe verificacion_arxiv.csv.
No modifica el .bib ni el manuscrito.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

TARGET_DIR = Path(__file__).resolve().parent
DEFAULT_INVENTORY = TARGET_DIR / "inventario_bibliografia.csv"
USER_AGENT = "tesis-bibliography-audit/1.0 (https://github.com/LUS24/tesis-maestria-data-mining)"


def arxiv_id(url: str) -> str:
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?", url or "")
    return m.group(1) if m else ""


def normalize(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value).lower()
    value = re.sub(r"[^a-z0-9áéíóúüñç]+", " ", value, flags=re.I)
    return re.sub(r"\s+", " ", value).strip()


def sim(a: str, b: str) -> float:
    from difflib import SequenceMatcher

    a, b = normalize(a), normalize(b)
    return round(SequenceMatcher(None, a, b).ratio(), 4) if a and b else 0.0


def surname(value: str) -> str:
    raw = (value or "").strip()
    if "," in raw:
        return normalize(raw.split(",", 1)[0].strip())
    return normalize(raw.split()[-1]) if raw else ""


def query(ids: list[str]) -> dict[str, dict]:
    url = "https://export.arxiv.org/api/query?max_results=50&id_list=" + urllib.parse.quote(",".join(ids))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as response:
        xml = response.read().decode("utf-8", errors="replace")
    result: dict[str, dict] = {}
    for block in re.findall(r"<entry>(.*?)</entry>", xml, flags=re.S):
        def tag(name: str) -> str:
            m = re.search(rf"<{name}[^>]*>(.*?)</{name}>", block, flags=re.S)
            return html.unescape(re.sub(r"\s+", " ", m.group(1))).strip() if m else ""

        identifier = tag("id")
        aid_match = re.search(r"([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?", identifier)
        aid = aid_match.group(1) if aid_match else ""
        authors = [
            html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
            for m in re.finditer(r"<name>(.*?)</name>", block, flags=re.S)
        ]
        result[aid] = {
            "found": True,
            "title": tag("title"),
            "authors": authors,
            "year": tag("published")[:4],
            "url": identifier,
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--batch", type=int, default=15)
    args = parser.parse_args()
    with args.inventory.open(encoding="utf-8-sig", newline="") as f:
        records = list(csv.DictReader(f))
    with_ids = [(r, arxiv_id(r.get("url", ""))) for r in records]
    with_ids = [(r, aid) for r, aid in with_ids if aid]
    ids = sorted({aid for _, aid in with_ids})
    meta: dict[str, dict] = {}
    for i in range(0, len(ids), args.batch):
        batch = ids[i : i + args.batch]
        print(f"arXiv lote {i // args.batch + 1}: {len(batch)} IDs")
        for attempt in range(4):
            try:
                meta.update(query(batch))
                break
            except Exception as exc:  # noqa: BLE001
                wait = 5 * (attempt + 1)
                print(f"  error: {exc}; esperando {wait}s")
                time.sleep(wait)
        time.sleep(3)
    rows = []
    for row, aid in with_ids:
        m = meta.get(aid)
        if not m:
            rows.append(
                {
                    "clave": row["clave"],
                    "arxiv_id": aid,
                    "estado": "no_encontrado_en_api",
                    "similitud_titulo": "",
                    "anio_coincide": "",
                    "autor_coincide": "",
                    "titulo_registrado": row["titulo"],
                    "titulo_arxiv": "",
                    "anio_registrado": row["anio"],
                    "anio_arxiv": "",
                    "autores_arxiv": "",
                    "http_status": "",
                    "error": "sin entrada en la respuesta del API",
                }
            )
            continue
        similarity = sim(row["titulo"], m["title"])
        year_ok = str(row["anio"]) == str(m["year"])
        entry_authors = {surname(a) for a in row["autores"].split(" | ") if a and a != "others"}
        source_authors = {surname(a) for a in m["authors"] if a}
        author_ok = bool(entry_authors & source_authors)
        flags = []
        if similarity < 0.9:
            flags.append("titulo")
        if not year_ok:
            flags.append("anio")
        if not author_ok:
            flags.append("autor")
        rows.append(
            {
                "clave": row["clave"],
                "arxiv_id": aid,
                "estado": "coincide" if not flags else "discrepancia_" + "_".join(flags),
                "similitud_titulo": f"{similarity:.4f}",
                "anio_coincide": "si" if year_ok else "no",
                "autor_coincide": "si" if author_ok else "no",
                "titulo_registrado": row["titulo"],
                "titulo_arxiv": m["title"],
                "anio_registrado": row["anio"],
                "anio_arxiv": m["year"],
                "autores_arxiv": " | ".join(m["authors"]),
                "http_status": "200",
                "error": "",
            }
        )
    with (TARGET_DIR / "verificacion_arxiv.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    from collections import Counter

    print(json.dumps(Counter(r["estado"] for r in rows), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

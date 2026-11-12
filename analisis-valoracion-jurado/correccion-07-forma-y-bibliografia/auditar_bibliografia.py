#!/usr/bin/env python3
"""Auditoría local de referencias.bib y de las citas Typst.

No modifica ningún archivo del repositorio. Genera únicamente artefactos
derivados dentro de esta carpeta.

Uso:
    python3 auditar_bibliografia.py --repo /ruta/al/repositorio
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path

TARGET_DIR = Path(__file__).resolve().parent
DEFAULT_REPO = TARGET_DIR.parents[1]
BIB_REL = Path("manuscrito/referencias.bib")
TYP_DIR_REL = Path("manuscrito")


@dataclass
class BibEntry:
    entry_type: str
    key: str
    start_line: int
    end_line: int
    fields: dict[str, str] = field(default_factory=dict)
    field_lines: dict[str, int] = field(default_factory=dict)

    def get(self, name: str, default: str = "") -> str:
        return self.fields.get(name.lower(), default)


def find_matching(text: str, start: int, opening: str, closing: str) -> int:
    """Devuelve el índice del delimitador de cierre, ignorando escapes y comillas."""
    depth = 0
    quote = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == '"' and opening != '"':
            quote = not quote
            continue
        if quote:
            continue
        if ch == opening:
            depth += 1
        elif ch == closing:
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(f"Delimitador sin cierre desde {start}")


def parse_fields(body: str, body_start_line: int) -> tuple[dict[str, str], dict[str, int]]:
    fields: dict[str, str] = {}
    lines: dict[str, int] = {}
    i = 0
    n = len(body)
    while i < n:
        while i < n and body[i] in " \t\r\n,":
            i += 1
        if i >= n:
            break
        name_start = i
        while i < n and re.match(r"[A-Za-z0-9_\-]", body[i]):
            i += 1
        name = body[name_start:i].strip().lower()
        while i < n and body[i] in " \t\r\n":
            i += 1
        if not name or i >= n or body[i] != "=":
            # Avanzar hasta la próxima coma de campo para tolerar comentarios.
            next_comma = body.find(",", i)
            if next_comma == -1:
                break
            i = next_comma + 1
            continue
        i += 1
        while i < n and body[i] in " \t\r\n":
            i += 1
        if i >= n:
            break
        field_line = body_start_line + body.count("\n", 0, name_start)
        if body[i] == "{":
            close = find_matching(body, i, "{", "}")
            value = body[i + 1 : close]
            i = close + 1
        elif body[i] == '"':
            close = find_matching(body, i, '"', '"')
            value = body[i + 1 : close]
            i = close + 1
        else:
            value_start = i
            while i < n and body[i] != ",":
                i += 1
            value = body[value_start:i].strip()
        if name not in fields:
            fields[name] = value.strip()
            lines[name] = field_line
        while i < n and body[i] != ",":
            i += 1
        if i < n:
            i += 1
    return fields, lines


def parse_bibtex(path: Path) -> list[BibEntry]:
    text = path.read_text(encoding="utf-8")
    entries: list[BibEntry] = []
    pos = 0
    while True:
        m = re.search(r"(?m)^@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,", text[pos:])
        if not m:
            break
        absolute = pos + m.start()
        open_brace = text.find("{", absolute)
        close_brace = find_matching(text, open_brace, "{", "}")
        body_start = open_brace + 1
        header_end = pos + m.end()
        body = text[header_end:close_brace]
        start_line = text.count("\n", 0, absolute) + 1
        end_line = text.count("\n", 0, close_brace) + 1
        fields, field_lines = parse_fields(body, text.count("\n", 0, header_end) + 1)
        entries.append(
            BibEntry(
                entry_type=m.group(1).lower(),
                key=m.group(2).strip(),
                start_line=start_line,
                end_line=end_line,
                fields=fields,
                field_lines=field_lines,
            )
        )
        pos = close_brace + 1
    return entries


def strip_tex(value: str) -> str:
    value = value.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_")
    value = re.sub(r"\\[A-Za-z]+\s*", "", value)
    value = value.replace("{", "").replace("}", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_text(value: str) -> str:
    value = strip_tex(value).lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def parse_authors(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    # Autor institucional entre llaves dobles: {{OpenAI}} llega aquí como {OpenAI}.
    if raw.startswith("{") and raw.endswith("}") and raw.count("{") == 1:
        return [strip_tex(raw)]
    # "and" como separador solo fuera de llaves y con cualquier espacio, incluido salto de línea.
    parts: list[str] = []
    depth = 0
    i = 0
    start = 0
    while i < len(raw):
        ch = raw[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        if depth == 0:
            m = re.match(r"\s+and\s+", raw[i:], flags=re.I)
            if m:
                parts.append(raw[start:i].strip())
                i += m.end()
                start = i
                continue
        i += 1
    parts.append(raw[start:].strip())
    return [strip_tex(p) for p in parts if p.strip()]


def surname(author: str) -> str:
    # Los autores institucionales se conservan completos.
    if " " in author and "," not in author and not re.match(r"^[a-z0-9_.-]+$", author):
        return author.strip()
    if "," in author:
        return author.split(",", 1)[0].strip()
    tokens = author.split()
    return tokens[-1] if tokens else author


def initials(author: str) -> str:
    if "," in author:
        given = author.split(",", 1)[1]
    else:
        tokens = author.split()
        given = " ".join(tokens[:-1])
    return "".join(part[0] for part in re.findall(r"[A-Za-zÀ-ÿ]+", given) if part).upper()


def clean_doi(value: str) -> str:
    value = strip_tex(value).strip()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value, flags=re.I)
    return value.rstrip(".,; ")


def clean_url(value: str) -> str:
    return strip_tex(value).strip().rstrip(".,; ")


def entry_year(entry: BibEntry) -> str:
    return strip_tex(entry.get("year")).strip()


def entry_title(entry: BibEntry) -> str:
    return strip_tex(entry.get("title"))


def entry_authors(entry: BibEntry) -> list[str]:
    return parse_authors(entry.get("author"))


def canonical_author_year(entry: BibEntry) -> tuple[str, str]:
    authors = entry_authors(entry)
    if not authors:
        return "", entry_year(entry)
    return normalize_text(surname(authors[0])), entry_year(entry)


def extract_citations(typ_dir: Path, keys: set[str]) -> list[dict[str, object]]:
    citations: list[dict[str, object]] = []
    cite_re = re.compile(r"#cite\(\s*<([^>]+)>")
    bare_re = re.compile(r"(?<![A-Za-z0-9_])@([A-Za-z0-9_\-]+)")
    for path in sorted(typ_dir.rglob("*.typ")):
        if any(part in {".venv", "temp", "salidas"} for part in path.parts):
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            seen: set[str] = set()
            for m in cite_re.finditer(line):
                key = m.group(1).strip()
                if key not in seen:
                    citations.append(
                        {
                            "clave": key,
                            "archivo": str(path.relative_to(typ_dir.parent)),
                            "linea": line_no,
                            "estilo": "#cite",
                            "en_bib": key in keys,
                            "contexto": line.strip()[:500],
                        }
                    )
                    seen.add(key)
            for m in bare_re.finditer(line):
                key = m.group(1).strip()
                if key in keys and key not in seen:
                    citations.append(
                        {
                            "clave": key,
                            "archivo": str(path.relative_to(typ_dir.parent)),
                            "linea": line_no,
                            "estilo": "@",
                            "en_bib": True,
                            "contexto": line.strip()[:500],
                        }
                    )
                    seen.add(key)
    return citations


def domain_category(url: str) -> str:
    if not url:
        return "sin URL"
    low = url.lower()
    if "arxiv.org" in low:
        return "arXiv"
    if "doi.org" in low:
        return "DOI"
    if "openreview.net" in low:
        return "OpenReview"
    if "aclanthology.org" in low:
        return "ACL Anthology"
    if "proceedings." in low or "papers.nips.cc" in low or "jmlr.org" in low:
        return "Actas académicas"
    if any(d in low for d in ["openai.com", "anthropic.com", "google.", "microsoft.com", "meta.com", "huggingface.co", "deepseek.com", "x.ai", "moonshot", "alibaba", "qwen"]):
        return "Proveedor/industria"
    if any(d in low for d in ["wikipedia.org", "blog", "medium.com"]):
        return "Blog/Wikipedia"
    if "github.com" in low:
        return "Repositorio de software"
    if "infoleg" in low or "boletinoficial" in low or "argentina.gob.ar" in low or "saij" in low:
        return "Fuente oficial argentina"
    return "Otro"


def duplicate_title_pairs(entries: list[BibEntry]) -> list[dict[str, object]]:
    pairs = []
    normalized = [(e, normalize_text(entry_title(e))) for e in entries]
    for i in range(len(normalized)):
        e1, t1 = normalized[i]
        if len(t1) < 20:
            continue
        for j in range(i + 1, len(normalized)):
            e2, t2 = normalized[j]
            if len(t2) < 20:
                continue
            ratio = SequenceMatcher(None, t1, t2).ratio()
            if ratio >= 0.90:
                pairs.append(
                    {
                        "clave_1": e1.key,
                        "clave_2": e2.key,
                        "similitud_titulo": round(ratio, 4),
                        "titulo_1": entry_title(e1),
                        "titulo_2": entry_title(e2),
                    }
                )
    return pairs


def suggested_disambiguation(entries: list[BibEntry]) -> tuple[str, str]:
    authors0 = entry_authors(entries[0]) if entries else []
    if not authors0:
        return "sin autor", "Revisar autoría."
    surnames = {normalize_text(surname(entry_authors(e)[0])) for e in entries if entry_authors(e)}
    initials_set = {initials(entry_authors(e)[0]) for e in entries if entry_authors(e)}
    if len(initials_set) > 1:
        return (
            "iniciales del nombre",
            "APA 7: si el primer autor comparte apellido pero difiere el nombre, incluir las iniciales en la cita; no requiere letras de año.",
        )
    lists = {tuple(normalize_text(a) for a in entry_authors(e)) for e in entries}
    if len(lists) > 1:
        return (
            "nombres adicionales",
            "APA 7: mantener el año y agregar los coautores necesarios para distinguir las citas; las letras a/b solo corresponden a trabajos del mismo autor(es) y año.",
        )
    return (
        "letras de año",
        "Mismo autor(es) y año: asignar sufijos a/b en la lista de referencias y en las citas.",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=DEFAULT_REPO)
    args = parser.parse_args()
    repo = args.repo.resolve()
    bib_path = repo / BIB_REL
    typ_dir = repo / TYP_DIR_REL
    entries = parse_bibtex(bib_path)
    keys = [e.key for e in entries]
    key_set = set(keys)
    citations = extract_citations(typ_dir, key_set)

    # 1. Inventario
    inventory_fields = [
        "clave",
        "tipo",
        "linea_inicio",
        "linea_fin",
        "anio",
        "primer_autor",
        "autores",
        "titulo",
        "doi",
        "url",
        "categoria_url",
        "venue",
        "veces_citada",
        "archivos_citada",
        "estado_uso",
    ]
    by_key: dict[str, list[dict[str, object]]] = defaultdict(list)
    for c in citations:
        by_key[str(c["clave"])].append(c)

    with (TARGET_DIR / "inventario_bibliografia.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=inventory_fields)
        w.writeheader()
        for e in entries:
            authors = entry_authors(e)
            venue = e.get("journal") or e.get("booktitle") or e.get("howpublished") or e.get("publisher") or ""
            cites = by_key.get(e.key, [])
            w.writerow(
                {
                    "clave": e.key,
                    "tipo": e.entry_type,
                    "linea_inicio": e.start_line,
                    "linea_fin": e.end_line,
                    "anio": entry_year(e),
                    "primer_autor": surname(authors[0]) if authors else "",
                    "autores": " | ".join(authors),
                    "titulo": entry_title(e),
                    "doi": clean_doi(e.get("doi")),
                    "url": clean_url(e.get("url")),
                    "categoria_url": domain_category(clean_url(e.get("url"))),
                    "venue": strip_tex(venue),
                    "veces_citada": len(cites),
                    "archivos_citada": " | ".join(sorted({str(c["archivo"]) for c in cites})),
                    "estado_uso": "citada" if cites else "no citada",
                }
            )

    # 2. Citas
    with (TARGET_DIR / "citas_por_archivo.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["clave", "archivo", "linea", "estilo", "en_bib", "contexto"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(citations)

    missing_keys = sorted({str(c["clave"]) for c in citations if not c["en_bib"]})
    with (TARGET_DIR / "citas_sin_entrada.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["clave", "archivo", "linea", "contexto"])
        w.writeheader()
        for c in citations:
            if not c["en_bib"]:
                w.writerow({k: c[k] for k in ["clave", "archivo", "linea", "contexto"]})

    # 3. Entradas sin uso
    uncited = [e for e in entries if e.key not in by_key]
    with (TARGET_DIR / "entradas_sin_uso.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["clave", "tipo", "anio", "primer_autor", "titulo", "doi", "url", "linea_inicio", "linea_fin"])
        w.writeheader()
        for e in uncited:
            authors = entry_authors(e)
            w.writerow(
                {
                    "clave": e.key,
                    "tipo": e.entry_type,
                    "anio": entry_year(e),
                    "primer_autor": surname(authors[0]) if authors else "",
                    "titulo": entry_title(e),
                    "doi": clean_doi(e.get("doi")),
                    "url": clean_url(e.get("url")),
                    "linea_inicio": e.start_line,
                    "linea_fin": e.end_line,
                }
            )

    # 4. Duplicados de DOI, clave y títulos
    doi_groups: dict[str, list[BibEntry]] = defaultdict(list)
    for e in entries:
        doi = clean_doi(e.get("doi")).lower()
        if doi:
            doi_groups[doi].append(e)
    duplicate_doi = [
        {"doi": doi, "claves": " | ".join(e.key for e in group), "n": len(group)}
        for doi, group in doi_groups.items()
        if len(group) > 1
    ]
    with (TARGET_DIR / "doi_duplicados.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["doi", "claves", "n"])
        w.writeheader()
        w.writerows(duplicate_doi)
    title_pairs = duplicate_title_pairs(entries)
    with (TARGET_DIR / "titulos_similares.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["clave_1", "clave_2", "similitud_titulo", "titulo_1", "titulo_2"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(title_pairs)

    # 5. Ambigüedades autor-año
    groups: dict[tuple[str, str], list[BibEntry]] = defaultdict(list)
    for e in entries:
        if e.key in by_key:
            groups[canonical_author_year(e)].append(e)
    ambiguous = []
    for (author, year), group in sorted(groups.items()):
        if not author or not year or len(group) < 2:
            continue
        kind, rule = suggested_disambiguation(group)
        ambiguous.append(
            {
                "primer_autor": author,
                "anio": year,
                "n": len(group),
                "claves": " | ".join(e.key for e in group),
                "autores_completos": " || ".join("; ".join(entry_authors(e)) for e in group),
                "titulos": " || ".join(entry_title(e) for e in group),
                "tipo_disambiguacion": kind,
                "regla_apa": rule,
            }
        )
    with (TARGET_DIR / "autor_anio_ambiguos.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["primer_autor", "anio", "n", "claves", "autores_completos", "titulos", "tipo_disambiguacion", "regla_apa"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(ambiguous)

    # 6. Cobertura de identificadores y formato
    no_identifier = []
    preprint = []
    access_date = []
    no_year = []
    for e in entries:
        doi = clean_doi(e.get("doi"))
        url = clean_url(e.get("url"))
        if not doi and not url:
            no_identifier.append(e)
        text = " ".join(e.fields.values())
        if "arxiv preprint" in text.lower() or e.get("eprint") or e.get("archiveprefix") or e.get("archivePrefix"):
            preprint.append(e)
        if e.get("urldate") or re.search(r"accedido|consultado|recuperado", text, re.I):
            access_date.append(e)
        if not entry_year(e):
            no_year.append(e)
    with (TARGET_DIR / "sin_identificador.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["clave", "tipo", "anio", "titulo", "autores", "linea_inicio", "linea_fin"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for e in no_identifier:
            w.writerow(
                {
                    "clave": e.key,
                    "tipo": e.entry_type,
                    "anio": entry_year(e),
                    "titulo": entry_title(e),
                    "autores": " | ".join(entry_authors(e)),
                    "linea_inicio": e.start_line,
                    "linea_fin": e.end_line,
                }
            )
    with (TARGET_DIR / "preprints.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["clave", "tipo", "anio", "venue", "doi", "url", "eprint", "linea_inicio"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for e in preprint:
            w.writerow(
                {
                    "clave": e.key,
                    "tipo": e.entry_type,
                    "anio": entry_year(e),
                    "venue": strip_tex(e.get("journal") or e.get("booktitle") or ""),
                    "doi": clean_doi(e.get("doi")),
                    "url": clean_url(e.get("url")),
                    "eprint": e.get("eprint"),
                    "linea_inicio": e.start_line,
                }
            )
    with (TARGET_DIR / "fechas_de_consulta.csv").open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["clave", "anio", "mes", "urldate", "note", "url", "linea_inicio"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for e in access_date:
            w.writerow(
                {
                    "clave": e.key,
                    "anio": entry_year(e),
                    "mes": strip_tex(e.get("month")),
                    "urldate": strip_tex(e.get("urldate")),
                    "note": strip_tex(e.get("note")),
                    "url": clean_url(e.get("url")),
                    "linea_inicio": e.start_line,
                }
            )

    # 7. Resumen JSON para que otros scripts no reparseen
    summary = {
        "bib_path": str(bib_path),
        "n_entries": len(entries),
        "n_keys_unique": len(key_set),
        "n_citations": len(citations),
        "n_cited_keys": len({str(c["clave"]) for c in citations}),
        "n_uncited": len(uncited),
        "n_missing_keys": len(missing_keys),
        "missing_keys": missing_keys,
        "n_doi": sum(1 for e in entries if clean_doi(e.get("doi"))),
        "n_url": sum(1 for e in entries if clean_url(e.get("url"))),
        "n_no_identifier": len(no_identifier),
        "n_preprint": len(preprint),
        "n_access_date": len(access_date),
        "n_ambiguous_author_year": len(ambiguous),
        "n_duplicate_doi_groups": len(duplicate_doi),
        "n_similar_title_pairs": len(title_pairs),
        "by_type": dict(sorted(Counter(e.entry_type for e in entries).items())),
        "by_domain": dict(sorted(Counter(domain_category(clean_url(e.get("url"))) for e in entries).items())),
        "citation_occurrences_in_capitulos": sum(1 for c in citations if str(c["archivo"]).startswith("manuscrito/capitulos/")),
    }
    (TARGET_DIR / "resumen_auditoria_local.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Consolida inventario, verificaciones y decisiones manuales.

Salida:
  estado_por_entrada.csv
  propuestas_nuevas.csv
  resumen_consolidado.json
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent


def read_csv(name: str) -> list[dict]:
    path = BASE / name
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    inventory = read_csv("inventario_bibliografia.csv")
    manual = {r["clave"]: r for r in read_csv("decisiones_manuales.csv")}
    doi = {r["clave"]: r for r in read_csv("verificacion_doi.csv")}
    arxiv = {r["clave"]: r for r in read_csv("verificacion_arxiv.csv")}

    # Puede haber varias URL por clave (p. ej. DeepSeek). Se conserva la de
    # mejor estado y se listan todas en la columna de detalle.
    url_by_key: dict[str, list[dict]] = {}
    for row in read_csv("verificacion_url.csv"):
        url_by_key.setdefault(row["clave"], []).append(row)

    def best_url(rows: list[dict]) -> tuple[str, str]:
        if not rows:
            return "", ""
        priority = {"206": 0, "200": 1, "202": 2, "403": 3, "401": 4, "405": 5, "429": 6}
        rows = sorted(rows, key=lambda r: priority.get(str(r.get("http_status")), 99))
        best = rows[0]
        all_urls = " | ".join(
            f"{r.get('http_status')}:{r.get('url')}" for r in rows
        )
        return str(best.get("http_status", "")), all_urls

    out_rows = []
    for row in inventory:
        key = row["clave"]
        d = doi.get(key, {})
        a = arxiv.get(key, {})
        url_status, url_detail = best_url(url_by_key.get(key, []))
        doi_status = d.get("estado", "")
        arxiv_status = a.get("estado", "")

        if doi_status == "coincide":
            identifier = "DOI verificado"
        elif d.get("http_status") == "200" and doi_status:
            identifier = "DOI responde; metadatos a revisar"
        elif doi_status == "no_encontrado" and arxiv_status == "coincide":
            identifier = "DOI no indexado; arXiv verificado"
        elif arxiv_status == "coincide":
            identifier = "arXiv verificado"
        elif url_status in {"200", "206", "202"}:
            identifier = "URL responde"
        elif url_status in {"403", "401", "405", "429"}:
            identifier = "URL bloquea automatización; revisar"
        elif row.get("url") and not url_status:
            identifier = "URL no resuelve"
        elif not row.get("doi") and not row.get("url"):
            identifier = "sin identificador"
        else:
            identifier = "revisar"

        m = manual.get(key, {})
        out_rows.append(
            {
                "clave": key,
                "tipo": row["tipo"],
                "anio": row["anio"],
                "primer_autor": row["primer_autor"],
                "titulo": row["titulo"],
                "doi": row["doi"],
                "url": row["url"],
                "veces_citada": row["veces_citada"],
                "estado_doi": doi_status,
                "http_doi": d.get("http_status", ""),
                "estado_arxiv": arxiv_status,
                "http_url": url_status,
                "urls_verificadas": url_detail,
                "estado_identificador": identifier,
                "accion_manual": m.get("accion", ""),
                "prioridad": m.get("prioridad", ""),
                "motivo_manual": m.get("motivo", ""),
                "propuesta_manual": m.get("propuesta", ""),
            }
        )

    fields = list(out_rows[0].keys())
    with (BASE / "estado_por_entrada.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    # Propuestas que no existen en el .bib actual
    current_keys = {r["clave"] for r in inventory}
    proposals = [
        r for r in read_csv("decisiones_manuales.csv")
        if r["clave"] not in current_keys
    ]
    with (BASE / "propuestas_nuevas.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["clave", "accion", "prioridad", "motivo", "evidencia", "propuesta"])
        w.writeheader()
        w.writerows(proposals)

    summary = {
        "n_entradas_actuales": len(inventory),
        "n_citadas": sum(1 for r in inventory if r["estado_uso"] == "citada"),
        "n_no_citadas": sum(1 for r in inventory if r["estado_uso"] == "no citada"),
        "n_doi": sum(1 for r in inventory if r["doi"]),
        "n_arxiv": sum(1 for r in inventory if "arxiv.org" in r["url"]),
        "n_url": sum(1 for r in inventory if r["url"]),
        "n_sin_identificador": sum(1 for r in inventory if not r["doi"] and not r["url"]),
        "estado_identificador": dict(Counter(r["estado_identificador"] for r in out_rows)),
        "acciones_manuales": dict(Counter(r["accion_manual"] for r in out_rows if r["accion_manual"])),
        "prioridades": dict(Counter(r["prioridad"] for r in out_rows if r["prioridad"])),
        "n_propuestas_nuevas": len(proposals),
        "propuestas_nuevas": [r["clave"] for r in proposals],
        "nota": "La auditoría verifica identificadores y metadatos; no sustituye la lectura completa de cada obra.",
    }
    (BASE / "resumen_consolidado.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

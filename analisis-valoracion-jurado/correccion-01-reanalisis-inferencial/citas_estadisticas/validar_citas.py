#!/usr/bin/env python3
"""Valida las citas estadísticas con el mismo criterio de la corrección 07.

Usa las funciones de `correccion-07-forma-y-bibliografia/verificar_fuentes.py`
para consultar Crossref y URL, comparar título, año y primer autor. Escribe la
caché y los resultados dentro de esta carpeta; no modifica la corrección 07.

Uso:
    python3 analisis-valoracion-jurado/correccion-01-reanalisis-inferencial/citas_estadisticas/validar_citas.py
"""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
from typing import Any

BASE = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
INVENTORY = HERE / "inventario_citas_estadisticas.csv"
OUT = HERE / "verificacion_citas_estadisticas.csv"
SUMMARY = HERE / "resumen_validacion_citas.json"
CACHE = HERE / "cache"
CACHE.mkdir(parents=True, exist_ok=True)

VF_PATH = (
    BASE
    / "analisis-valoracion-jurado"
    / "correccion-07-forma-y-bibliografia"
    / "verificar_fuentes.py"
)
spec = importlib.util.spec_from_file_location("vf07", VF_PATH)
if spec is None or spec.loader is None:
    raise SystemExit(f"No se pudo cargar {VF_PATH}")
vf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vf)
vf.CACHE_DIR = CACHE


def read_inventory() -> list[dict[str, str]]:
    with INVENTORY.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def first_author(raw: str) -> str:
    return (raw or "").split(";")[0].strip()


def validate(row: dict[str, str]) -> dict[str, Any]:
    key = row["clave"]
    title = row["titulo"]
    year = str(row["anio"])
    expected_author = first_author(row["autores"])
    doi = (row.get("doi") or "").strip()
    url = (row.get("url") or "").strip()

    result: dict[str, Any] = {
        "clave": key,
        "identificador": doi or url,
        "tipo_identificador": "DOI" if doi else "URL",
        "http_status": "",
        "fuente": "",
        "estado": "",
        "similitud_titulo": "",
        "anio_coincide": "",
        "autor_coincide": "",
        "titulo_fuente": "",
        "anio_fuente": "",
        "autores_fuente": "",
        "venue_fuente": "",
        "url_fuente": "",
        "observacion": "",
    }

    if doi:
        meta = vf.crossref_metadata(doi)
        result["http_status"] = meta.get("raw_status")
        result["fuente"] = meta.get("source", "Crossref")
        if not meta.get("found"):
            result["estado"] = "no_encontrado"
            result["observacion"] = meta.get("error", "Crossref no devolvió metadatos")
            return result
        sim = vf.title_similarity(title, meta.get("title", ""))
        year_match = str(meta.get("year", "")) == year
        authors = meta.get("authors") or []
        author_match = bool(authors) and vf.surname(authors[0]) == vf.surname(expected_author)
        result.update(
            {
                "similitud_titulo": f"{sim:.4f}",
                "anio_coincide": "si" if year_match else "no",
                "autor_coincide": "si" if author_match else "no",
                "titulo_fuente": meta.get("title", ""),
                "anio_fuente": meta.get("year", ""),
                "autores_fuente": " | ".join(authors),
                "venue_fuente": meta.get("container", ""),
                "url_fuente": meta.get("url", ""),
            }
        )
        if sim >= 0.90 and year_match and author_match:
            result["estado"] = "verificado"
        elif sim >= 0.75:
            result["estado"] = "verificado_con_observacion"
            result["observacion"] = "Metadatos localizados; revisar año/autor/título."
        else:
            result["estado"] = "revisar"
            result["observacion"] = "El título no coincide suficientemente con el registro."
        return result

    if url:
        meta = vf.check_url(url)
        status = meta.get("http_status")
        result.update(
            {
                "http_status": status,
                "fuente": "URL",
                "titulo_fuente": meta.get("title", ""),
                "url_fuente": meta.get("final_url", url),
            }
        )
        if status in (200, 202, 206):
            result["estado"] = "url_responde"
            if "jstor" in url.lower() and (
                not meta.get("title") or "Client Challenge" in str(meta.get("title", ""))
            ):
                result["observacion"] = "JSTOR devuelve Client Challenge; URL válida, título no automatizable."
        elif status in (401, 403, 405, 429):
            result["estado"] = "url_bloquea_automatizacion"
            result["observacion"] = "El servidor bloquea la consulta automatizada; revisar manualmente."
        else:
            result["estado"] = "revisar"
            result["observacion"] = meta.get("error", "URL sin respuesta válida")
        return result

    result["estado"] = "sin_identificador"
    result["observacion"] = "La entrada no tiene DOI ni URL."
    return result


def main() -> None:
    rows = read_inventory()
    results = [validate(row) for row in rows]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)

    summary = {
        "n_entradas": len(results),
        "n_doi": sum(1 for r in results if r["tipo_identificador"] == "DOI"),
        "n_url": sum(1 for r in results if r["tipo_identificador"] == "URL"),
        "estados": {},
        "no_verificadas": [
            {"clave": r["clave"], "estado": r["estado"], "observacion": r["observacion"]}
            for r in results
            if r["estado"] not in {"verificado", "url_responde"}
        ],
        "nota": (
            "Validación de metadatos y localizadores con el método de la corrección 07. "
            "No sustituye la lectura completa de cada obra."
        ),
    }
    counts: dict[str, int] = {}
    for r in results:
        counts[r["estado"]] = counts.get(r["estado"], 0) + 1
    summary["estados"] = counts
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nResultados: {OUT}")


if __name__ == "__main__":
    main()

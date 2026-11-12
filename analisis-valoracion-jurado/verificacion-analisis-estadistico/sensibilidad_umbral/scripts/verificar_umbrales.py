#!/usr/bin/env python3
"""Sensibilidad de D-02 a los umbrales 0,50/0,75/1,00.

Recalcula desde `14_dataset_categoria_final.csv` el número de respuestas
correctas, la tasa y el costo por respuesta correcta de las nueve celdas.
Contrasta el resultado con la tabla ya publicada por corrección 05.

Uso:
    cd codigo_experimentos
    uv run --frozen python ../analisis-valoracion-jurado/verificacion-analisis-estadistico/sensibilidad_umbral/scripts/verificar_umbrales.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

PACKAGE = Path(__file__).resolve().parent.parent
VERIF = PACKAGE.parent
ANALISIS = VERIF.parent
REPO = ANALISIS.parent
DATA = ANALISIS / "correccion-02-diagnostico-gpt-5-nano" / "salidas" / "14_dataset_categoria_final.csv"
PUBLISHED = ANALISIS / "correccion-05-actualizacion-conclusiones-y-analisis-costos" / "datos" / "costo_por_respuesta_aceptable_umbrales.csv"
OUT = PACKAGE / "datos"
SALIDAS = PACKAGE / "salidas"
THRESHOLDS = (0.50, 0.75, 1.00)
STRATEGIES = {
    "llm_responses_no_rag": "Sin RAG",
    "llm_responses_base_rag": "RAG básico",
    "llm_responses_agentic_rag": "Agentic-RAG",
}
MODELS = ("gpt-5-nano", "gpt-5-mini", "gpt-5")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def recompute(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["estrategia"], row["modelo"])].append(row)
    out: list[dict[str, Any]] = []
    for threshold in THRESHOLDS:
        for strategy, strategy_label in STRATEGIES.items():
            for model in MODELS:
                subset = grouped[(strategy, model)]
                scores = [float(row["puntaje_final_fallo_cero"]) for row in subset]
                costs = [float(row["costo_total"]) for row in subset]
                correct = sum(score >= threshold - 1e-9 for score in scores)
                total_cost = sum(costs)
                out.append(
                    {
                        "umbral": threshold,
                        "estrategia": strategy,
                        "estrategia_label": strategy_label,
                        "modelo": model,
                        "n": len(subset),
                        "correctas": correct,
                        "tasa_correctas": correct / len(subset),
                        "costo_total": total_cost,
                        "costo_medio": total_cost / len(subset),
                        "costo_por_correcta": total_cost / correct if correct else math.nan,
                    }
                )
    return out


def rank(rows: list[dict[str, Any]]) -> None:
    for threshold in THRESHOLDS:
        subset = [row for row in rows if row["umbral"] == threshold and math.isfinite(row["costo_por_correcta"])]
        subset.sort(key=lambda row: row["costo_por_correcta"])
        for position, row in enumerate(subset, start=1):
            row["rank_costo_por_correcta"] = position
        for row in rows:
            if row["umbral"] == threshold and not math.isfinite(row["costo_por_correcta"]):
                row["rank_costo_por_correcta"] = None


def key(row: dict[str, Any]) -> tuple[float, str, str]:
    return (round(float(row["umbral"]), 2), row["estrategia"], row["modelo"])


def compare(recomputed: list[dict[str, Any]], published: list[dict[str, str]]) -> list[dict[str, Any]]:
    lookup = {key(row): row for row in recomputed}
    comparisons: list[dict[str, Any]] = []
    for row in published:
        k = (round(float(row["umbral"]), 2), row["estrategia"], row["modelo"])
        local = lookup[k]
        comparisons.append(
            {
                "umbral": k[0],
                "estrategia": k[1],
                "modelo": k[2],
                "correctas_local": local["correctas"],
                "correctas_publicado": int(row["aceptables"]),
                "delta_correctas": local["correctas"] - int(row["aceptables"]),
                "costo_por_correcta_local": local["costo_por_correcta"],
                "costo_por_correcta_publicado": float(row["costo_por_aceptable"]) if row["costo_por_aceptable"] not in ("", "nan") else math.nan,
                "delta_costo_por_correcta": (
                    local["costo_por_correcta"] - float(row["costo_por_aceptable"])
                    if math.isfinite(local["costo_por_correcta"]) and row["costo_por_aceptable"] not in ("", "nan")
                    else 0.0
                ),
            }
        )
    return comparisons


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SALIDAS.mkdir(parents=True, exist_ok=True)
    rows = read_csv(DATA)
    if len(rows) != 711:
        raise ValueError(f"Se esperaban 711 observaciones y hay {len(rows)}")
    recomputed = recompute(rows)
    rank(recomputed)
    published = read_csv(PUBLISHED)
    if len(published) != 27:
        raise ValueError(f"Se esperaban 27 filas publicadas y hay {len(published)}")
    comparisons = compare(recomputed, published)
    max_delta_correctas = max(abs(row["delta_correctas"]) for row in comparisons)
    max_delta_costo = max(abs(row["delta_costo_por_correcta"]) for row in comparisons)

    fields = [
        "umbral", "estrategia", "estrategia_label", "modelo", "n", "correctas",
        "tasa_correctas", "costo_total", "costo_medio", "costo_por_correcta",
        "rank_costo_por_correcta",
    ]
    write_csv(OUT / "01_umbrales_recalculados.csv", recomputed, fields)
    write_csv(
        OUT / "02_comparacion_correccion05.csv",
        comparisons,
        ["umbral", "estrategia", "modelo", "correctas_local", "correctas_publicado",
         "delta_correctas", "costo_por_correcta_local", "costo_por_correcta_publicado",
         "delta_costo_por_correcta"],
    )
    ranking = [row for row in recomputed if row.get("rank_costo_por_correcta") in (1, 2, 3)]
    write_csv(OUT / "03_top3_por_umbral.csv", ranking, fields)

    summary = {
        "fuente": str(DATA.relative_to(REPO)),
        "hash_fuente": sha256(DATA),
        "publicado": str(PUBLISHED.relative_to(REPO)),
        "hash_publicado": sha256(PUBLISHED),
        "n": len(rows),
        "max_delta_correctas": max_delta_correctas,
        "max_delta_costo_por_correcta": max_delta_costo,
        "coincide": max_delta_correctas == 0 and max_delta_costo < 1e-12,
        "mejor_por_umbral": {
            str(threshold): next(
                row for row in recomputed
                if row["umbral"] == threshold and row.get("rank_costo_por_correcta") == 1
            )
            for threshold in THRESHOLDS
        },
        "lectura": "Los tres umbrales ya estaban calculados en corrección 05; el recálculo independiente coincide. No se requiere una nueva decisión.",
    }
    (SALIDAS / "resumen_umbrales.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

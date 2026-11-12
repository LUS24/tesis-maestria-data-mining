#!/usr/bin/env python3
"""Verificación independiente del acuerdo inter-juez (D-14).

- Lee `codigo_experimentos/part_i/final_judge_results.csv` como fuente original
  consolidada de los jueces.
- No lee ni modifica los artefactos derivados de la corrección 01 para calcular
  el alpha; solo los usa después, para contrastar los valores publicados.
- No modifica ningún archivo fuente.

Uso:
    uv run --project ../../codigo_experimentos --frozen python scripts/recalcular_acuerdo.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats
import krippendorff

PACKAGE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = PACKAGE_DIR.parents[1]
ORIGINAL_JUDGES = REPO_ROOT / "codigo_experimentos" / "part_i" / "final_judge_results.csv"
CORR02_FINAL = (
    REPO_ROOT
    / "analisis-valoracion-jurado"
    / "correccion-02-diagnostico-gpt-5-nano"
    / "salidas"
    / "14_dataset_categoria_final.csv"
)
CORR01_LONG = (
    REPO_ROOT
    / "analisis-valoracion-jurado"
    / "correccion-01-analisis-estadistico"
    / "datos"
    / "02_long_2133.csv"
)
CORR01_RESULTS = (
    REPO_ROOT
    / "analisis-valoracion-jurado"
    / "correccion-01-analisis-estadistico"
    / "salidas"
    / "35_resultados_clave.json"
)
DATA_DIR = PACKAGE_DIR / "datos"
OUT_DIR = PACKAGE_DIR / "salidas"
for directory in (DATA_DIR, OUT_DIR):
    directory.mkdir(parents=True, exist_ok=True)

RUBRIC = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
SYSTEM_ORDER = ["llm_responses_no_rag", "llm_responses_base_rag", "llm_responses_agentic_rag"]
SYSTEM_LABEL = {
    "llm_responses_no_rag": "Sin RAG",
    "llm_responses_base_rag": "RAG básico",
    "llm_responses_agentic_rag": "Agentic-RAG",
}
JUDGE_LABEL = {
    "grok_4_1_fast_free": "Grok 4.1 Fast",
    "openrouter_deepseek_deepseek-chat-v3-1": "DeepSeek V3.1",
    "openrouter_moonshotai_kimi-k2-0905": "Kimi K2 0905",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sub(value: str | None) -> int:
    if value is None or str(value).strip() == "":
        return 0
    return int(float(value))


def impute_rubric(value: float) -> float:
    distances = np.abs(RUBRIC - value)
    minimum = distances.min()
    return float(RUBRIC[distances == minimum].max())


def alpha_ordinal(matrix: np.ndarray) -> float:
    return float(krippendorff.alpha(reliability_data=matrix, level_of_measurement="ordinal"))


def observation_key(row: dict[str, str]) -> tuple[int, int, str, str]:
    return (
        int(row["numero_pregunta"]),
        canonical_sub(row["numero_subpregunta"]),
        row["sistema"],
        row["modelo_respuesta"],
    )


def build_matrix(rows: list[dict[str, str]], judge: str, column: str) -> tuple[list[tuple[int, int, str, str]], np.ndarray]:
    units = sorted({observation_key(row) for row in rows})
    lookup = {
        (*observation_key(row), row["modelo_juez"]): float(row[column])
        for row in rows
    }
    values = [lookup[(*observation, judge)] for observation in units]
    return units, np.array(values, dtype=float)


def main() -> None:
    rows = read_csv(ORIGINAL_JUDGES)
    if len(rows) != 2133:
        raise ValueError(f"Se esperaban 2.133 filas de jueces y hay {len(rows)}")

    judges = sorted({row["modelo_juez"] for row in rows})
    systems = sorted({row["sistema"] for row in rows})
    units = sorted({observation_key(row) for row in rows})

    counts = Counter((row["modelo_juez"],) for row in rows)
    if len(judges) != 3 or len(units) != 711:
        raise ValueError(f"Jueces={judges}; observaciones={len(units)}")
    for judge in judges:
        if counts[(judge,)] != 711:
            raise ValueError(f"El juez {judge} no tiene 711 evaluaciones")

    # Matrices jueces × unidades, a partir de la fuente original.
    raw_matrix = np.array([build_matrix(rows, judge, "score_respuesta_correcta")[1] for judge in judges])
    rubric_matrix = np.array([[impute_rubric(value) for value in raw_matrix[index]] for index in range(len(judges))])

    alpha_raw = alpha_ordinal(raw_matrix)
    alpha_rubric = alpha_ordinal(rubric_matrix)

    precision_matrix = np.array([build_matrix(rows, judge, "score_precision_legal")[1] for judge in judges])
    precision_rubric_matrix = np.array(
        [[impute_rubric(value) for value in precision_matrix[index]] for index in range(len(judges))]
    )
    alpha_precision_raw = alpha_ordinal(precision_matrix)
    alpha_precision_rubric = alpha_ordinal(precision_rubric_matrix)

    # Alpha por sistema, con la misma matriz jueces × unidades dentro de cada sistema.
    by_system: list[dict[str, Any]] = []
    for system in SYSTEM_ORDER:
        subset = [row for row in rows if row["sistema"] == system]
        system_units = sorted({observation_key(row) for row in subset})
        raw = np.array([build_matrix(subset, judge, "score_respuesta_correcta")[1] for judge in judges])
        rubric = np.array([[impute_rubric(value) for value in raw[index]] for index in range(len(judges))])
        precision_raw = np.array([build_matrix(subset, judge, "score_precision_legal")[1] for judge in judges])
        precision_rubric = np.array(
            [[impute_rubric(value) for value in precision_raw[index]] for index in range(len(judges))]
        )
        by_system.append(
            {
                "sistema": system,
                "sistema_label": SYSTEM_LABEL[system],
                "unidades": len(system_units),
                "evaluaciones": len(subset),
                "alpha_raw": alpha_ordinal(raw),
                "alpha_rubric": alpha_ordinal(rubric),
                "alpha_precision_raw": alpha_ordinal(precision_raw),
                "alpha_precision_rubric": alpha_ordinal(precision_rubric),
            }
        )

    # Correlaciones de Spearman entre pares de jueces, sobre valores originales.
    spearman_rows: list[dict[str, Any]] = []
    for judge_a, judge_b in combinations(judges, 2):
        values_a = build_matrix(rows, judge_a, "score_respuesta_correcta")[1]
        values_b = build_matrix(rows, judge_b, "score_respuesta_correcta")[1]
        rho, p_value = stats.spearmanr(values_a, values_b)
        spearman_rows.append(
            {
                "juez_1": judge_a,
                "juez_1_label": JUDGE_LABEL.get(judge_a, judge_a),
                "juez_2": judge_b,
                "juez_2_label": JUDGE_LABEL.get(judge_b, judge_b),
                "n": len(values_a),
                "rho": float(rho),
                "p": float(p_value),
            }
        )

    # Conteos de la base original y de la base final usada por la corrección 05.
    final_rows = read_csv(CORR02_FINAL)
    non_substantive = sum(str(row["es_no_sustantiva_final"]).strip().lower() == "true" for row in final_rows)
    cell_counts: dict[tuple[str, str], int] = defaultdict(int)
    for row in final_rows:
        cell_counts[(row["estrategia"], row["modelo"])] += 1
    nano_agentic = next(
        row for row in final_rows if row["estrategia"] == "llm_responses_agentic_rag" and row["modelo"] == "gpt-5-nano"
    )
    nano_non_substantive = sum(
        str(row["es_no_sustantiva_final"]).strip().lower() == "true"
        for row in final_rows
        if row["estrategia"] == "llm_responses_agentic_rag" and row["modelo"] == "gpt-5-nano"
    )
    cost_total = sum(float(row["costo_total"]) for row in final_rows)

    # Contraste con los valores publicados por la corrección 01.
    published = json.loads(CORR01_RESULTS.read_text(encoding="utf-8"))
    published_alpha = None
    if CORR01_LONG.exists():
        long_rows = read_csv(CORR01_LONG)
        # La tabla larga de la corrección 01 permite verificar que la matriz y los conteos coinciden.
        published_alpha = {
            "long_rows": len(long_rows),
            "long_units": len({(row["numero_pregunta"], row["numero_subpregunta"], row["sistema"], row["modelo_respuesta"]) for row in long_rows}),
        }

    # Casos con mayor desacuerdo entre jueces, para una eventual revisión humana.
    discrepancy_rows: list[dict[str, Any]] = []
    for index, (question, sub, system, model) in enumerate(units):
        scores = raw_matrix[:, index]
        spread = float(np.max(scores) - np.min(scores))
        if spread >= 0.75:
            discrepancy_rows.append(
                {
                    "numero_pregunta": question,
                    "numero_subpregunta": sub,
                    "estrategia": system,
                    "modelo": model,
                    "puntajes": " | ".join(f"{JUDGE_LABEL.get(judge, judge)}={scores[i]:g}" for i, judge in enumerate(judges)),
                    "rango": spread,
                    "desviacion": float(np.std(scores)),
                }
            )
    discrepancy_rows.sort(key=lambda row: (-float(row["rango"]), -float(row["desviacion"])))

    # Evaluaciones positivas sobre salidas no sustantivas (auditoría de la corrección 02).
    non_substantive_judge_rows: list[dict[str, Any]] = []
    judge_lookup = {
        (int(row["numero_pregunta"]), canonical_sub(row["numero_subpregunta"]), row["sistema"], row["modelo_respuesta"], row["modelo_juez"]): row
        for row in rows
    }
    for row in final_rows:
        if str(row["es_no_sustantiva_final"]).strip().lower() != "true":
            continue
        for judge in judges:
            key = (
                int(row["nro_pregunta"]),
                canonical_sub(row["nro_subpregunta"]),
                row["estrategia"],
                row["modelo"],
                judge,
            )
            source = judge_lookup[key]
            if float(source["score_respuesta_correcta"]) > 0 or float(source["score_precision_legal"]) > 0:
                non_substantive_judge_rows.append(
                    {
                        "numero_pregunta": row["nro_pregunta"],
                        "numero_subpregunta": row["nro_subpregunta"] or "0",
                        "estrategia": row["estrategia"],
                        "modelo": row["modelo"],
                        "juez": JUDGE_LABEL.get(judge, judge),
                        "score_respuesta_correcta": source["score_respuesta_correcta"],
                        "score_precision_legal": source["score_precision_legal"],
                        "categoria_final": row["categoria_final"],
                    }
                )

    write_csv(
        DATA_DIR / "alpha_global.csv",
        [
            {
                "rubrica": "score_respuesta_correcta",
                "valores": "originales",
                "unidades": len(units),
                "jueces": len(judges),
                "alpha_ordinal": alpha_raw,
            },
            {
                "rubrica": "score_respuesta_correcta",
                "valores": "transformados a rubrica",
                "unidades": len(units),
                "jueces": len(judges),
                "alpha_ordinal": alpha_rubric,
            },
            {
                "rubrica": "score_precision_legal",
                "valores": "originales",
                "unidades": len(units),
                "jueces": len(judges),
                "alpha_ordinal": alpha_precision_raw,
            },
            {
                "rubrica": "score_precision_legal",
                "valores": "transformados a rubrica",
                "unidades": len(units),
                "jueces": len(judges),
                "alpha_ordinal": alpha_precision_rubric,
            },
        ],
        ["rubrica", "valores", "unidades", "jueces", "alpha_ordinal"],
    )
    write_csv(
        DATA_DIR / "alpha_por_sistema.csv",
        by_system,
        ["sistema", "sistema_label", "unidades", "evaluaciones", "alpha_raw", "alpha_rubric", "alpha_precision_raw", "alpha_precision_rubric"],
    )
    write_csv(
        DATA_DIR / "spearman_pares.csv",
        spearman_rows,
        ["juez_1", "juez_1_label", "juez_2", "juez_2_label", "n", "rho", "p"],
    )
    write_csv(
        DATA_DIR / "resumen_conteos.csv",
        [
            {
                "filas_jueces": len(rows),
                "unidades": len(units),
                "jueces": len(judges),
                "observaciones_finales": len(final_rows),
                "no_sustantivas": non_substantive,
                "sustantivas": len(final_rows) - non_substantive,
                "nano_agentic_no_sustantivas": nano_non_substantive,
                "costo_total_usd": cost_total,
                "sistemas": len(systems),
                "celdas": len(cell_counts),
            }
        ],
        [
            "filas_jueces",
            "unidades",
            "jueces",
            "observaciones_finales",
            "no_sustantivas",
            "sustantivas",
            "nano_agentic_no_sustantivas",
            "costo_total_usd",
            "sistemas",
            "celdas",
        ],
    )
    write_csv(
        DATA_DIR / "casos_discrepancia_para_revision_humana.csv",
        discrepancy_rows,
        ["numero_pregunta", "numero_subpregunta", "estrategia", "modelo", "puntajes", "rango", "desviacion"],
    )
    write_csv(
        DATA_DIR / "evaluaciones_positivas_salidas_no_sustantivas.csv",
        non_substantive_judge_rows,
        [
            "numero_pregunta",
            "numero_subpregunta",
            "estrategia",
            "modelo",
            "juez",
            "score_respuesta_correcta",
            "score_precision_legal",
            "categoria_final",
        ],
    )

    manifest_rows = []
    for path in [ORIGINAL_JUDGES, CORR02_FINAL, CORR01_LONG, CORR01_RESULTS]:
        if path.exists():
            manifest_rows.append(
                {
                    "archivo": str(path.relative_to(REPO_ROOT)),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    write_csv(DATA_DIR / "manifiesto_sha256.csv", manifest_rows, ["archivo", "bytes", "sha256"])

    summary = {
        "fuente_original": str(ORIGINAL_JUDGES.relative_to(REPO_ROOT)),
        "n_filas_jueces": len(rows),
        "n_unidades": len(units),  # observaciones unidad × estrategia × modelo (711)
        "n_unidades_unicas": len({(row["numero_pregunta"], canonical_sub(row["numero_subpregunta"])) for row in rows}),
        "n_jueces": len(judges),
        "jueces": [JUDGE_LABEL.get(judge, judge) for judge in judges],
        "alpha_global_raw": alpha_raw,
        "alpha_global_rubric": alpha_rubric,
        "alpha_precision_global_raw": alpha_precision_raw,
        "alpha_precision_global_rubric": alpha_precision_rubric,
        "alpha_por_sistema": by_system,
        "spearman_pares": spearman_rows,
        "n_no_sustantivas": non_substantive,
        "nano_agentic_no_sustantivas": nano_non_substantive,
        "costo_total_usd": cost_total,
        "n_casos_discrepancia": len(discrepancy_rows),
        "n_evaluaciones_positivas_no_sustantivas": len(non_substantive_judge_rows),
        "contraste_correccion_01": {
            "alpha_publicado_raw": 0.8078424689763564,
            "alpha_publicado_rubric": 0.7995418703552886,
            "alpha_publicado_precision_raw": 0.7845657645755232,
            "coincide_raw": abs(alpha_raw - 0.8078424689763564) < 1e-10,
            "coincide_rubric": abs(alpha_rubric - 0.7995418703552886) < 1e-10,
            "coincide_precision_raw": abs(alpha_precision_raw - 0.7845657645755232) < 1e-10,
            "publicado": published_alpha,
        },
        "nota": "El cálculo parte de final_judge_results.csv, no de la tabla larga derivada de la corrección 01. No se modificaron los archivos fuente.",
    }
    (OUT_DIR / "resumen_verificacion.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    print(json.dumps({key: summary[key] for key in ["alpha_global_raw", "alpha_global_rubric", "alpha_precision_global_raw", "alpha_precision_global_rubric", "n_unidades", "n_filas_jueces", "n_casos_discrepancia", "n_evaluaciones_positivas_no_sustantivas"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

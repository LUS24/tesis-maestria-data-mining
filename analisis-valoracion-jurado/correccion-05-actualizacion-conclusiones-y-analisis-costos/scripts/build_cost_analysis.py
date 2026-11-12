#!/usr/bin/env python3
"""Corrección IX.1.5 — análisis de costos y artefactos de soporte.

Lee únicamente artefactos derivados de las correcciones 01 y 02. No modifica
fuentes, logs, respuestas ni evaluaciones históricas.

Uso:
    uv run --project ../../codigo_experimentos --frozen python scripts/build_cost_analysis.py
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

PACKAGE_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = PACKAGE_DIR.parents[1]
CORR01 = REPO_ROOT / "analisis-valoracion-jurado" / "correccion-01-analisis-estadistico"
CORR02 = REPO_ROOT / "analisis-valoracion-jurado" / "correccion-02-diagnostico-gpt-5-nano"
CORR03 = REPO_ROOT / "analisis-valoracion-jurado" / "correccion-03-documentar-api-eliminar-determinismo"
CORR04 = REPO_ROOT / "analisis-valoracion-jurado" / "correccion-04-declarar-factores-pub-prompts-etc"
CORR06 = REPO_ROOT / "analisis-valoracion-jurado" / "correccion-06-precisar-corpus-revisar-respuestas"
CORR07 = REPO_ROOT / "analisis-valoracion-jurado" / "correccion-07-forma-y-bibliografia"

DATA_DIR = PACKAGE_DIR / "datos"
FIG_DIR = PACKAGE_DIR / "figuras"
OUT_DIR = PACKAGE_DIR / "salidas"
for directory in (DATA_DIR, FIG_DIR, OUT_DIR):
    directory.mkdir(parents=True, exist_ok=True)

DATA_FINAL = CORR02 / "salidas" / "14_dataset_categoria_final.csv"
RESULTS_01 = CORR01 / "salidas" / "35_resultados_clave.json"
CELLS_01 = CORR01 / "salidas" / "30_tabla_celdas_principal.csv"
PREDICTIONS_01 = CORR01 / "salidas" / "22_modelo_predicciones_celdas.csv"

SEED = 20261112
N_BOOTSTRAP = 5000

STRATEGY_ORDER = [
    "llm_responses_no_rag",
    "llm_responses_base_rag",
    "llm_responses_agentic_rag",
]
STRATEGY_LABEL = {
    "llm_responses_no_rag": "Sin RAG",
    "llm_responses_base_rag": "RAG básico",
    "llm_responses_agentic_rag": "Agentic-RAG",
}
MODEL_ORDER = ["gpt-5-nano", "gpt-5-mini", "gpt-5"]
MODEL_LABEL = {"gpt-5-nano": "gpt-5-nano", "gpt-5-mini": "gpt-5-mini", "gpt-5": "gpt-5"}
THRESHOLDS = [0.5, 0.75, 1.0]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wilson_interval(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = successes / n
    denominator = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return (max(0.0, centre - half), min(1.0, centre + half))


def percentile_interval(values: list[float]) -> tuple[float, float]:
    clean = [value for value in values if value is not None and math.isfinite(value)]
    if not clean:
        return (math.nan, math.nan)
    return (float(np.percentile(clean, 2.5)), float(np.percentile(clean, 97.5)))


def dominates(a: dict[str, Any], b: dict[str, Any], tol: float = 1e-12) -> bool:
    """True si a domina a b: menor o igual costo y mayor o igual desempeño."""
    cost_a, cost_b = float(a["costo_medio"]), float(b["costo_medio"])
    score_a, score_b = float(a["score_medio"]), float(b["score_medio"])
    no_worse = cost_a <= cost_b + tol and score_a >= score_b - tol
    strictly_better = cost_a < cost_b - tol or score_a > score_b + tol
    return no_worse and strictly_better


def frontier(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in rows if not any(dominates(other, row) for other in rows if other is not row)]


def cell_key(row: dict[str, str]) -> tuple[str, str]:
    return (row["estrategia"], row["modelo"])


def load_data() -> tuple[list[dict[str, str]], dict[str, Any]]:
    rows = read_csv(DATA_FINAL)
    results = json.loads(RESULTS_01.read_text(encoding="utf-8"))
    if len(rows) != 711:
        raise ValueError(f"Se esperaban 711 observaciones y hay {len(rows)}")
    keys = {(row["estrategia"], row["modelo"], row["nro_pregunta"], row["nro_subpregunta"]) for row in rows}
    if len(keys) != 711:
        raise ValueError(f"Se esperaban 711 claves únicas y hay {len(keys)}")
    return rows, results


def aggregate_cells(rows: list[dict[str, str]], results: dict[str, Any]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[cell_key(row)].append(row)

    # Predicciones poblacionales del modelo ordinal (solo para referencia).
    predictions: dict[str, dict[str, str]] = {}
    for row in read_csv(PREDICTIONS_01):
        if row["escenario"] == "principal_cero_no_sustantivas":
            predictions[row["cell"].replace("RAG basico", "RAG básico")] = row

    rng = np.random.default_rng(SEED)
    cases = sorted({row["q"] for row in rows}, key=lambda value: int(value))
    by_case_cell: dict[tuple[str, str], dict[str, list[dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        by_case_cell[cell_key(row)][row["q"]].append(row)

    # Una única matriz de remuestreo de casos para todas las celdas y escenarios.
    bootstrap_draws = [rng.choice(cases, size=len(cases), replace=True) for _ in range(N_BOOTSTRAP)]

    cells: list[dict[str, Any]] = []
    for strategy in STRATEGY_ORDER:
        for model in MODEL_ORDER:
            key = (strategy, model)
            subset = grouped[key]
            if len(subset) != 79:
                raise ValueError(f"La celda {key} tiene {len(subset)} filas, no 79")

            costs = np.array([float(row["costo_total"]) for row in subset], dtype=float)
            scores = np.array([float(row["puntaje_final_fallo_cero"]) for row in subset], dtype=float)
            failures = sum(str(row["es_no_sustantiva_final"]).strip().lower() == "true" for row in subset)
            acceptable = scores >= 0.75 - 1e-9
            n_acceptable = int(acceptable.sum())
            total_cost = float(costs.sum())
            mean_cost = float(costs.mean())
            mean_score = float(scores.mean())
            rate = n_acceptable / len(subset)
            rate_lo, rate_hi = wilson_interval(n_acceptable, len(subset))
            cost_per_acceptable = total_cost / n_acceptable if n_acceptable else math.nan

            boot_mean_cost: list[float] = []
            boot_mean_score: list[float] = []
            boot_rate: list[float] = []
            boot_cost_per_acceptable: list[float] = []
            for draw in bootstrap_draws:
                sampled: list[dict[str, str]] = []
                for case in draw:
                    sampled.extend(by_case_cell[key][case])
                sampled_costs = np.array([float(row["costo_total"]) for row in sampled], dtype=float)
                sampled_scores = np.array([float(row["puntaje_final_fallo_cero"]) for row in sampled], dtype=float)
                sampled_acceptable = int((sampled_scores >= 0.75 - 1e-9).sum())
                boot_mean_cost.append(float(sampled_costs.mean()))
                boot_mean_score.append(float(sampled_scores.mean()))
                boot_rate.append(sampled_acceptable / len(sampled_scores))
                if sampled_acceptable:
                    boot_cost_per_acceptable.append(float(sampled_costs.sum() / sampled_acceptable))

            cost_lo, cost_hi = percentile_interval(boot_mean_cost)
            score_lo, score_hi = percentile_interval(boot_mean_score)
            rate_lo_boot, rate_hi_boot = percentile_interval(boot_rate)
            cpa_lo, cpa_hi = percentile_interval(boot_cost_per_acceptable)

            pred = predictions.get(f"{STRATEGY_LABEL[strategy]}|{model}")
            cells.append(
                {
                    "estrategia": strategy,
                    "estrategia_label": STRATEGY_LABEL[strategy],
                    "modelo": model,
                    "n": len(subset),
                    "n_no_sustantiva": failures,
                    "costo_total": total_cost,
                    "costo_medio": mean_cost,
                    "costo_mediana": float(np.median(costs)),
                    "costo_medio_ic95_inf": cost_lo,
                    "costo_medio_ic95_sup": cost_hi,
                    "score_medio": mean_score,
                    "score_mediana": float(np.median(scores)),
                    "score_medio_ic95_inf": score_lo,
                    "score_medio_ic95_sup": score_hi,
                    "aceptables_075": n_acceptable,
                    "tasa_aceptable_075": rate,
                    "tasa_aceptable_075_wilson_inf": rate_lo,
                    "tasa_aceptable_075_wilson_sup": rate_hi,
                    "tasa_aceptable_075_boot_inf": rate_lo_boot,
                    "tasa_aceptable_075_boot_sup": rate_hi_boot,
                    "costo_por_aceptable_075": cost_per_acceptable,
                    "costo_por_aceptable_075_ic95_inf": cpa_lo,
                    "costo_por_aceptable_075_ic95_sup": cpa_hi,
                    "p_ge_075_modelo": float(pred["p_ge_075"]) if pred else math.nan,
                    "p_ge_075_modelo_ic95_inf": float(pred["p_ge_075_ic95_inf"]) if pred else math.nan,
                    "p_ge_075_modelo_ic95_sup": float(pred["p_ge_075_ic95_sup"]) if pred else math.nan,
                }
            )

    # Frontera de Pareto puntual.
    for row in cells:
        row["pareto"] = False
    for row in frontier(cells):
        row["pareto"] = True

    # Frecuencia de pertenencia a la frontera bajo bootstrap por casos.
    frontier_frequency: dict[tuple[str, str], int] = defaultdict(int)
    for draw_index, draw in enumerate(bootstrap_draws):
        replicate_cells: list[dict[str, Any]] = []
        for strategy in STRATEGY_ORDER:
            for model in MODEL_ORDER:
                key = (strategy, model)
                sampled = []
                for case in draw:
                    sampled.extend(by_case_cell[key][case])
                replicate_cells.append(
                    {
                        "estrategia": strategy,
                        "modelo": model,
                        "costo_medio": float(np.mean([float(row["costo_total"]) for row in sampled])),
                        "score_medio": float(np.mean([float(row["puntaje_final_fallo_cero"]) for row in sampled])),
                    }
                )
        for row in frontier(replicate_cells):
            frontier_frequency[(row["estrategia"], row["modelo"])] += 1

    for row in cells:
        row["pareto_bootstrap_freq"] = frontier_frequency[(row["estrategia"], row["modelo"])] / N_BOOTSTRAP

    ranked = sorted(
        [row for row in cells if math.isfinite(row["costo_por_aceptable_075"])],
        key=lambda row: row["costo_por_aceptable_075"],
    )
    for position, row in enumerate(ranked, start=1):
        row["rank_costo_por_aceptable_075"] = position
    for row in cells:
        row.setdefault("rank_costo_por_aceptable_075", "")

    # Etiquetas y redondeo solo al escribir; se conserva precisión internamente.
    for row in cells:
        row["cell"] = f"{row['estrategia_label']} | {row['modelo']}"
    return cells


def aggregate_by_strategy(cells: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for strategy in STRATEGY_ORDER:
        subset = [row for row in cells if row["estrategia"] == strategy]
        total_cost = sum(float(row["costo_total"]) for row in subset)
        n = sum(int(row["n"]) for row in subset)
        acceptable = sum(int(row["aceptables_075"]) for row in subset)
        rows.append(
            {
                "estrategia": strategy,
                "estrategia_label": STRATEGY_LABEL[strategy],
                "n": n,
                "costo_total": total_cost,
                "costo_medio_por_consulta": total_cost / n,
                "aceptables_075": acceptable,
                "tasa_aceptable_075": acceptable / n,
                "costo_por_aceptable_075": total_cost / acceptable if acceptable else math.nan,
            }
        )
    return rows


def threshold_table(cells: list[dict[str, Any]], rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[cell_key(row)].append(row)
    output: list[dict[str, Any]] = []
    for threshold in THRESHOLDS:
        for strategy in STRATEGY_ORDER:
            for model in MODEL_ORDER:
                subset = grouped[(strategy, model)]
                total_cost = sum(float(row["costo_total"]) for row in subset)
                acceptable = sum(float(row["puntaje_final_fallo_cero"]) >= threshold - 1e-9 for row in subset)
                output.append(
                    {
                        "umbral": threshold,
                        "estrategia": strategy,
                        "estrategia_label": STRATEGY_LABEL[strategy],
                        "modelo": model,
                        "n": len(subset),
                        "aceptables": acceptable,
                        "tasa_aceptable": acceptable / len(subset),
                        "costo_total": total_cost,
                        "costo_medio": total_cost / len(subset),
                        "costo_por_aceptable": total_cost / acceptable if acceptable else math.nan,
                    }
                )
    return output


def write_cost_tables(cells: list[dict[str, Any]], by_strategy: list[dict[str, Any]], thresholds: list[dict[str, Any]]) -> None:
    cell_fields = [
        "estrategia",
        "estrategia_label",
        "modelo",
        "n",
        "n_no_sustantiva",
        "costo_total",
        "costo_medio",
        "costo_mediana",
        "costo_medio_ic95_inf",
        "costo_medio_ic95_sup",
        "score_medio",
        "score_mediana",
        "score_medio_ic95_inf",
        "score_medio_ic95_sup",
        "aceptables_075",
        "tasa_aceptable_075",
        "tasa_aceptable_075_wilson_inf",
        "tasa_aceptable_075_wilson_sup",
        "tasa_aceptable_075_boot_inf",
        "tasa_aceptable_075_boot_sup",
        "costo_por_aceptable_075",
        "costo_por_aceptable_075_ic95_inf",
        "costo_por_aceptable_075_ic95_sup",
        "p_ge_075_modelo",
        "p_ge_075_modelo_ic95_inf",
        "p_ge_075_modelo_ic95_sup",
        "pareto",
        "pareto_bootstrap_freq",
        "rank_costo_por_aceptable_075",
    ]
    write_csv(DATA_DIR / "costos_por_celda.csv", cells, cell_fields)

    strategy_fields = [
        "estrategia",
        "estrategia_label",
        "n",
        "costo_total",
        "costo_medio_por_consulta",
        "aceptables_075",
        "tasa_aceptable_075",
        "costo_por_aceptable_075",
    ]
    write_csv(DATA_DIR / "costos_por_estrategia.csv", by_strategy, strategy_fields)

    threshold_fields = [
        "umbral",
        "estrategia",
        "estrategia_label",
        "modelo",
        "n",
        "aceptables",
        "tasa_aceptable",
        "costo_total",
        "costo_medio",
        "costo_por_aceptable",
    ]
    write_csv(DATA_DIR / "costo_por_respuesta_aceptable_umbrales.csv", thresholds, threshold_fields)

    frontier_rows = [row for row in cells if row["pareto"]]
    frontier_fields = [
        "estrategia",
        "estrategia_label",
        "modelo",
        "costo_medio",
        "score_medio",
        "aceptables_075",
        "tasa_aceptable_075",
        "costo_por_aceptable_075",
        "pareto_bootstrap_freq",
    ]
    write_csv(DATA_DIR / "frontera_pareto.csv", frontier_rows, frontier_fields)


def write_previous_recommendation_comparison(cells: list[dict[str, Any]]) -> None:
    lookup = {(row["estrategia_label"], row["modelo"]): row for row in cells}
    names = [
        ("Agentic-RAG", "gpt-5-mini"),
        ("Agentic-RAG", "gpt-5"),
        ("Agentic-RAG", "gpt-5-nano"),
        ("RAG básico", "gpt-5"),
        ("RAG básico", "gpt-5-nano"),
        ("Sin RAG", "gpt-5"),
    ]
    rows: list[dict[str, Any]] = []
    for label, model in names:
        row = lookup[(label, model)]
        rows.append(
            {
                "cell": f"{label} | {model}",
                "costo_medio": row["costo_medio"],
                "costo_por_aceptable_075": row["costo_por_aceptable_075"],
                "score_medio": row["score_medio"],
                "aceptables_075": row["aceptables_075"],
                "tasa_aceptable_075": row["tasa_aceptable_075"],
                "rank_costo_por_aceptable_075": row["rank_costo_por_aceptable_075"],
                "pareto": row["pareto"],
                "pareto_bootstrap_freq": row["pareto_bootstrap_freq"],
            }
        )
    fields = [
        "cell",
        "costo_medio",
        "costo_por_aceptable_075",
        "score_medio",
        "aceptables_075",
        "tasa_aceptable_075",
        "rank_costo_por_aceptable_075",
        "pareto",
        "pareto_bootstrap_freq",
    ]
    write_csv(DATA_DIR / "comparacion_recomendacion_anterior.csv", rows, fields)


def make_figures(cells: list[dict[str, Any]]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 7.5,
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
        }
    )
    strategy_color = {
        "Sin RAG": "#E69F00",
        "RAG básico": "#0072B2",
        "Agentic-RAG": "#009E73",
    }
    model_marker = {"gpt-5-nano": "o", "gpt-5-mini": "s", "gpt-5": "^"}
    short = {
        ("Sin RAG", "gpt-5-nano"): "Sin RAG\nnano",
        ("Sin RAG", "gpt-5-mini"): "Sin RAG\nmini",
        ("Sin RAG", "gpt-5"): "Sin RAG\ngpt-5",
        ("RAG básico", "gpt-5-nano"): "RAG\nnano",
        ("RAG básico", "gpt-5-mini"): "RAG\nmini",
        ("RAG básico", "gpt-5"): "RAG\ngpt-5",
        ("Agentic-RAG", "gpt-5-nano"): "Agentic\nnano",
        ("Agentic-RAG", "gpt-5-mini"): "Agentic\nmini",
        ("Agentic-RAG", "gpt-5"): "Agentic\ngpt-5",
    }

    # Figura 1: costo vs desempeño y frontera de Pareto.
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    frontier_rows = sorted([row for row in cells if row["pareto"]], key=lambda row: row["costo_medio"])
    ax.plot(
        [row["costo_medio"] for row in frontier_rows],
        [row["score_medio"] for row in frontier_rows],
        color="#333333",
        linewidth=1.2,
        linestyle="--",
        zorder=1,
        label="Frontera de Pareto",
    )
    for row in cells:
        color = strategy_color[row["estrategia_label"]]
        marker = model_marker[row["modelo"]]
        size = 95 if row["pareto"] else 65
        ax.scatter(
            row["costo_medio"],
            row["score_medio"],
            s=size,
            color=color,
            marker=marker,
            edgecolor="black" if row["pareto"] else "white",
            linewidth=1.0 if row["pareto"] else 0.5,
            zorder=3,
        )
        ax.annotate(
            short[(row["estrategia_label"], row["modelo"])],
            (row["costo_medio"], row["score_medio"]),
            textcoords="offset points",
            xytext=(5, 4),
            fontsize=7,
        )
    ax.set_xscale("log")
    ax.set_xlabel("Costo medio por consulta (USD, escala logarítmica)")
    ax.set_ylabel("Media de corrección (fallo = 0)")
    ax.set_title("Costo y desempeño por configuración")
    ax.grid(True, which="both", alpha=0.25, linewidth=0.5)
    ax.set_ylim(0.25, 0.90)
    strategy_handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=7, label=label)
        for label, color in strategy_color.items()
    ]
    model_handles = [
        Line2D([0], [0], marker=marker, color="w", markerfacecolor="#777777", markersize=7, label=model)
        for model, marker in model_marker.items()
    ]
    ax.legend(handles=strategy_handles + model_handles, ncol=2, loc="lower right", frameon=True)
    fig.savefig(FIG_DIR / "01_costo_vs_desempenio_pareto.pdf")
    fig.savefig(FIG_DIR / "01_costo_vs_desempenio_pareto.png")
    plt.close(fig)

    # Figura 2: costo por respuesta aceptable (umbral 0,75).
    ordered = sorted(
        [row for row in cells if math.isfinite(row["costo_por_aceptable_075"])],
        key=lambda row: row["costo_por_aceptable_075"],
    )
    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    labels = [f"{short[(row['estrategia_label'], row['modelo'])]}" for row in ordered]
    values = [row["costo_por_aceptable_075"] for row in ordered]
    colors = [strategy_color[row["estrategia_label"]] for row in ordered]
    bars = ax.bar(range(len(ordered)), values, color=colors, edgecolor="black", linewidth=0.5)
    for bar, row in zip(bars, ordered):
        ax.annotate(
            f"${row['costo_por_aceptable_075']:.4f}\n{row['aceptables_075']}/79",
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            textcoords="offset points",
            xytext=(0, 3),
            ha="center",
            va="bottom",
            fontsize=6.5,
        )
    ax.set_yscale("log")
    ax.set_xticks(range(len(ordered)))
    ax.set_xticklabels(labels, rotation=0, fontsize=7)
    ax.set_ylabel("USD por respuesta correcta (log)")
    ax.set_title("Costo por respuesta correcta (umbral ≥ 0,75)")
    ax.grid(axis="y", which="both", alpha=0.25, linewidth=0.5)
    ax.legend(
        handles=[
            Line2D([0], [0], color=color, lw=6, label=label)
            for label, color in strategy_color.items()
        ],
        ncol=3,
        loc="upper left",
        fontsize=6.5,
    )
    fig.savefig(FIG_DIR / "02_costo_por_aceptable.pdf")
    fig.savefig(FIG_DIR / "02_costo_por_aceptable.png")
    plt.close(fig)


def write_summary(cells: list[dict[str, Any]], by_strategy: list[dict[str, Any]], thresholds: list[dict[str, Any]], results: dict[str, Any]) -> None:
    total_cost = sum(float(row["costo_total"]) for row in cells)
    lookup = {(row["estrategia_label"], row["modelo"]): row for row in cells}
    cheapest = min(
        [row for row in cells if math.isfinite(row["costo_por_aceptable_075"])],
        key=lambda row: row["costo_por_aceptable_075"],
    )
    best_score = max(cells, key=lambda row: row["score_medio"])
    old_agentic_mini = lookup[("Agentic-RAG", "gpt-5-mini")]
    rag_gpt5 = lookup[("RAG básico", "gpt-5")]
    no_rag_gpt5 = lookup[("Sin RAG", "gpt-5")]
    agentic_gpt5 = lookup[("Agentic-RAG", "gpt-5")]
    agentic_nano = lookup[("Agentic-RAG", "gpt-5-nano")]
    summary = {
        "n_observaciones": sum(int(row["n"]) for row in cells),
        "n_celdas": len(cells),
        "costo_total_experimento_usd": total_cost,
        "costo_por_estrategia": {
            row["estrategia_label"]: {
                "costo_total_usd": row["costo_total"],
                "costo_medio_por_consulta_usd": row["costo_medio_por_consulta"],
                "aceptables_075": row["aceptables_075"],
                "costo_por_aceptable_075_usd": row["costo_por_aceptable_075"],
            }
            for row in by_strategy
        },
        "celda_mas_barata_por_aceptable_075": {
            "cell": cheapest["cell"],
            "costo_medio_usd": cheapest["costo_medio"],
            "costo_por_aceptable_075_usd": cheapest["costo_por_aceptable_075"],
            "aceptables_075": cheapest["aceptables_075"],
            "score_medio": cheapest["score_medio"],
        },
        "celda_mejor_score_medio": {
            "cell": best_score["cell"],
            "costo_medio_usd": best_score["costo_medio"],
            "score_medio": best_score["score_medio"],
            "aceptables_075": best_score["aceptables_075"],
        },
        "frontera_pareto": [
            {
                "cell": row["cell"],
                "costo_medio_usd": row["costo_medio"],
                "score_medio": row["score_medio"],
                "costo_por_aceptable_075_usd": row["costo_por_aceptable_075"],
                "pareto_bootstrap_freq": row["pareto_bootstrap_freq"],
            }
            for row in cells
            if row["pareto"]
        ],
        "verificacion_recomendacion_anterior": {
            "agentic_mini_costo_medio_usd": old_agentic_mini["costo_medio"],
            "rag_gpt5_costo_medio_usd": rag_gpt5["costo_medio"],
            "no_rag_gpt5_costo_medio_usd": no_rag_gpt5["costo_medio"],
            "agentic_gpt5_costo_medio_usd": agentic_gpt5["costo_medio"],
            "agentic_nano_costo_por_aceptable_075_usd": agentic_nano["costo_por_aceptable_075"],
            "agentic_mini_es_mas_barato_que_rag_gpt5": bool(old_agentic_mini["costo_medio"] < rag_gpt5["costo_medio"]),
            "agentic_mini_es_mas_barato_que_no_rag_gpt5": bool(old_agentic_mini["costo_medio"] < no_rag_gpt5["costo_medio"]),
            "agentic_mini_es_mas_barato_que_agentic_gpt5": bool(old_agentic_mini["costo_medio"] < agentic_gpt5["costo_medio"]),
        },
        "umbrales": {
            str(threshold): [
                {
                    "cell": f"{row['estrategia_label']} | {row['modelo']}",
                    "aceptables": row["aceptables"],
                    "costo_por_aceptable": row["costo_por_aceptable"],
                }
                for row in thresholds
                if row["umbral"] == threshold
            ]
            for threshold in THRESHOLDS
        },
        "resultados_estadisticos_usados": {
            "LR_interaccion": results["modelo_principal"]["LR_interaccion"],
            "p_interaccion": results["modelo_principal"]["p_interaccion"],
            "n_no_sustantivas": results["n_no_sustantivas"],
            "nano_agentic_no_sustantivas": int(agentic_nano["n_no_sustantiva"]),
        },
        "definicion_respuesta_correcta": "Puntaje promedio de los tres jueces >= 0,75; operacionalizacion adoptada en D-02.",
        "nota": "Los costos son los registrados en el experimento (precios de API del período). No se actualizaron a precios corrientes.",
    }
    (OUT_DIR / "resumen_costos.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


def write_manifest() -> None:
    inputs = [
        DATA_FINAL,
        RESULTS_01,
        CELLS_01,
        PREDICTIONS_01,
        CORR03 / "salidas" / "resumen_evidencia.json",
        CORR04 / "salidas" / "resumen_auditoria.json",
        CORR06 / "salidas" / "auditoria_corpus_benchmark.md",
        CORR07 / "resumen_ejecutivo.md",
        REPO_ROOT / "manuscrito" / "capitulos" / "01_texto_preliminar.typ",
        REPO_ROOT / "manuscrito" / "capitulos" / "02_capitulo_01_introduccion.typ",
        REPO_ROOT / "manuscrito" / "capitulos" / "07_capitulo_06_evaluacion.typ",
        REPO_ROOT / "manuscrito" / "capitulos" / "09_capitulo_08_conclusion_y_trabajos_futuros.typ",
        REPO_ROOT / "manuscrito" / "capitulos" / "anexo_01.typ",
        REPO_ROOT / "README.md",
    ]
    rows = []
    for path in inputs:
        if not path.exists():
            raise FileNotFoundError(path)
        rows.append(
            {
                "archivo": str(path.relative_to(REPO_ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    write_csv(DATA_DIR / "manifiesto_entradas.csv", rows, ["archivo", "bytes", "sha256"])


def main() -> None:
    rows, results = load_data()
    cells = aggregate_cells(rows, results)
    by_strategy = aggregate_by_strategy(cells)
    thresholds = threshold_table(cells, rows)
    write_cost_tables(cells, by_strategy, thresholds)
    write_previous_recommendation_comparison(cells)
    make_figures(cells)
    write_summary(cells, by_strategy, thresholds, results)
    write_manifest()
    print("Artefactos de costos generados en", PACKAGE_DIR)


if __name__ == "__main__":
    main()

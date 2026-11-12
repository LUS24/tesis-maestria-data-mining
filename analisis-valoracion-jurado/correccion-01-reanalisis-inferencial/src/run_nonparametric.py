"""Pruebas pareadas y bootstrap por casos para la corrección IX.1.1.

Lee la base derivada de `build_dataset.py`. No modifica fuentes ni registros.
Produce tablas de Friedman, Wilcoxon con corrección de Holm y bootstrap por
casos para los escenarios de tratamiento de respuestas no sustantivas.

Uso:
    uv run --project codigo_experimentos --no-sync --frozen \
      python analisis-valoracion-jurado/correccion-01-reanalisis-inferencial/src/run_nonparametric.py
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "analisis-valoracion-jurado" / "correccion-01-reanalisis-inferencial"
DATOS = OUT / "datos"
SALIDAS = OUT / "salidas"

ESTRATEGIAS = [
    "llm_responses_no_rag",
    "llm_responses_base_rag",
    "llm_responses_agentic_rag",
]
ESTRATEGIA_LABEL = {
    "llm_responses_no_rag": "Sin RAG",
    "llm_responses_base_rag": "RAG basico",
    "llm_responses_agentic_rag": "Agentic-RAG",
}
MODELOS = ["gpt-5-nano", "gpt-5-mini", "gpt-5"]
RUBRICA = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
SEED = 20261112
N_BOOT = 5000

SCENARIOS = {
    "principal_cero_no_sustantivas": {
        "columna": "score_principal_prom",
        "etiqueta": "Principal: no sustantivas = 0",
    },
    "observado_jueces_rubric": {
        "columna": "score_observado_rubric_prom",
        "etiqueta": "Sensibilidad: puntajes observados (rúbrica)",
    },
    "exclusion_no_sustantivas": {
        "columna": "score_exclusion_prom",
        "etiqueta": "Sensibilidad: exclusión de no sustantivas",
    },
    "solo_fallos_tecnicos_cero": {
        "columna": "score_tecnicos_cero_prom",
        "etiqueta": "Sensibilidad: solo fallos técnicos = 0",
    },
}


def ordered_cells() -> list[tuple[str, str]]:
    return [(e, m) for e in ESTRATEGIAS for m in MODELOS]


def bootstrap_ci(
    values_by_case: dict[str, np.ndarray],
    rng: np.random.Generator,
    n_boot: int = N_BOOT,
) -> tuple[float, float, float, float, float, float]:
    """Bootstrap por casos: remuestrea casos completos, no filas.

    Devuelve media, IC95 de la media, mediana e IC95 de la mediana.
    """
    cases = list(values_by_case)
    if not cases:
        return (np.nan,) * 6
    arrays = [values_by_case[c] for c in cases]
    means = np.empty(n_boot)
    medians = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.integers(0, len(cases), size=len(cases))
        sample = np.concatenate([arrays[i] for i in idx])
        means[b] = float(np.mean(sample))
        medians[b] = float(np.median(sample))
    return (
        float(np.mean(np.concatenate(arrays))),
        float(np.quantile(means, 0.025)),
        float(np.quantile(means, 0.975)),
        float(np.median(np.concatenate(arrays))),
        float(np.quantile(medians, 0.025)),
        float(np.quantile(medians, 0.975)),
    )


def paired_rank_biserial(x: np.ndarray, y: np.ndarray) -> tuple[float, int]:
    d = np.asarray(x, dtype=float) - np.asarray(y, dtype=float)
    d = d[np.isfinite(d)]
    d = d[np.abs(d) > 1e-12]
    if len(d) == 0:
        return 0.0, 0
    ranks = stats.rankdata(np.abs(d))
    w_pos = float(ranks[d > 0].sum())
    w_neg = float(ranks[d < 0].sum())
    denom = w_pos + w_neg
    return ((w_pos - w_neg) / denom if denom else 0.0), len(d)


def wilcoxon_pair(x: np.ndarray, y: np.ndarray) -> dict[str, Any]:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    d = x - y
    n_pairs = len(d)
    n_nonzero = int(np.sum(np.abs(d) > 1e-12))
    if n_pairs == 0:
        return {
            "n_pares": 0,
            "n_no_cero": 0,
            "media_diferencia": np.nan,
            "mediana_diferencia": np.nan,
            "wilcoxon_w": np.nan,
            "p_wilcoxon": np.nan,
            "r_rango_biserial": np.nan,
        }
    if n_nonzero == 0:
        return {
            "n_pares": n_pairs,
            "n_no_cero": 0,
            "media_diferencia": 0.0,
            "mediana_diferencia": 0.0,
            "wilcoxon_w": 0.0,
            "p_wilcoxon": 1.0,
            "r_rango_biserial": 0.0,
        }
    try:
        res = stats.wilcoxon(x, y, zero_method="wilcox", alternative="two-sided", method="auto")
        w = float(res.statistic)
        p = float(res.pvalue)
    except ValueError:
        w, p = np.nan, np.nan
    r, _ = paired_rank_biserial(x, y)
    return {
        "n_pares": n_pairs,
        "n_no_cero": n_nonzero,
        "media_diferencia": float(np.mean(d)),
        "mediana_diferencia": float(np.median(d)),
        "wilcoxon_w": w,
        "p_wilcoxon": p,
        "r_rango_biserial": r,
    }


def paired_data(
    df: pd.DataFrame,
    value_col: str,
    estrategia_1: str,
    estrategia_2: str,
    modelo: str,
) -> pd.DataFrame:
    a = df[(df["estrategia"] == estrategia_1) & (df["modelo"] == modelo)][
        ["obs_id", "caso_id", value_col]
    ].rename(columns={value_col: "x"})
    b = df[(df["estrategia"] == estrategia_2) & (df["modelo"] == modelo)][
        ["obs_id", "caso_id", value_col]
    ].rename(columns={value_col: "y"})
    out = a.merge(b, on=["obs_id", "caso_id"], how="inner", validate="one_to_one")
    out = out.dropna(subset=["x", "y"])
    return out


def paired_models_data(
    df: pd.DataFrame,
    value_col: str,
    modelo_1: str,
    modelo_2: str,
    estrategia: str,
) -> pd.DataFrame:
    a = df[(df["estrategia"] == estrategia) & (df["modelo"] == modelo_1)][
        ["obs_id", "caso_id", value_col]
    ].rename(columns={value_col: "x"})
    b = df[(df["estrategia"] == estrategia) & (df["modelo"] == modelo_2)][
        ["obs_id", "caso_id", value_col]
    ].rename(columns={value_col: "y"})
    out = a.merge(b, on=["obs_id", "caso_id"], how="inner", validate="one_to_one")
    out = out.dropna(subset=["x", "y"])
    return out


def bootstrap_pair(
    pair: pd.DataFrame,
    rng: np.random.Generator,
    n_boot: int = N_BOOT,
) -> tuple[float, float, float, float, float, float]:
    by_case = {
        str(case): (group["x"].to_numpy() - group["y"].to_numpy())
        for case, group in pair.groupby("caso_id", sort=False)
    }
    return bootstrap_ci(by_case, rng, n_boot=n_boot)


def cell_bootstrap(
    df: pd.DataFrame,
    value_col: str,
    rng: np.random.Generator,
    n_boot: int = N_BOOT,
) -> dict[tuple[str, str], tuple[float, float, float, float, float, float]]:
    out = {}
    for estrategia, modelo in ordered_cells():
        group = df[(df["estrategia"] == estrategia) & (df["modelo"] == modelo)]
        by_case = {
            str(case): g[value_col].dropna().to_numpy()
            for case, g in group.groupby("caso_id", sort=False)
        }
        by_case = {k: v for k, v in by_case.items() if len(v) > 0}
        out[(estrategia, modelo)] = bootstrap_ci(by_case, rng, n_boot=n_boot)
    return out


def main() -> None:
    SALIDAS.mkdir(parents=True, exist_ok=True)
    rng_global = np.random.default_rng(SEED)

    raw = pd.read_csv(DATOS / "01_wide_711.csv", dtype={"obs_id": str, "caso_id": str})
    for col in [v["columna"] for v in SCENARIOS.values()]:
        raw[col] = pd.to_numeric(raw[col], errors="coerce")

    cell_rows = []
    friedman_rows = []
    wilcoxon_rows = []
    cell_ci_rows = []

    for scenario_name, scenario in SCENARIOS.items():
        value_col = scenario["columna"]
        label = scenario["etiqueta"]
        df = raw[["obs_id", "caso_id", "q", "estrategia", "modelo", "categoria_final", "es_no_sustantiva", value_col]].copy()
        df = df.rename(columns={value_col: "valor"})

        # Resumen por celda y bootstrap por casos.
        rng_cell = np.random.default_rng(SEED + 100 + len(cell_rows))
        cell_ci = cell_bootstrap(df, "valor", rng_cell)
        for (estrategia, modelo), ci in cell_ci.items():
            group = df[(df["estrategia"] == estrategia) & (df["modelo"] == modelo)]
            values = group["valor"].dropna().to_numpy()
            cell_rows.append(
                {
                    "escenario": scenario_name,
                    "escenario_label": label,
                    "estrategia": estrategia,
                    "estrategia_label": ESTRATEGIA_LABEL[estrategia],
                    "modelo": modelo,
                    "n": len(group),
                    "n_no_nulos": int(len(values)),
                    "n_no_sustantiva": int(group["es_no_sustantiva"].sum()),
                    "media": float(np.mean(values)) if len(values) else np.nan,
                    "mediana": float(np.median(values)) if len(values) else np.nan,
                    "sd": float(np.std(values, ddof=1)) if len(values) > 1 else np.nan,
                    "q1": float(np.quantile(values, 0.25)) if len(values) else np.nan,
                    "q3": float(np.quantile(values, 0.75)) if len(values) else np.nan,
                    "prop_ge_075": float(np.mean(values >= 0.75)) if len(values) else np.nan,
                    "n_ge_075": int(np.sum(values >= 0.75)),
                    "media_ic95_inf": ci[1],
                    "media_ic95_sup": ci[2],
                    "mediana_ic95_inf": ci[4],
                    "mediana_ic95_sup": ci[5],
                }
            )

        # Friedman: estrategias dentro de cada modelo.
        for modelo in MODELOS:
            sub = df[df["modelo"] == modelo]
            pivot = sub.pivot_table(index="obs_id", columns="estrategia", values="valor", aggfunc="first")
            pivot = pivot.dropna(subset=ESTRATEGIAS)
            if len(pivot) >= 2:
                arrays = [pivot[e].to_numpy() for e in ESTRATEGIAS]
                chi2, p = stats.friedmanchisquare(*arrays)
                k = len(ESTRATEGIAS)
                n = len(pivot)
                friedman_rows.append(
                    {
                        "escenario": scenario_name,
                        "familia": "estrategia_dentro_de_modelo",
                        "bloque": modelo,
                        "n_bloques": n,
                        "k": k,
                        "chi2": float(chi2),
                        "gl": k - 1,
                        "p": float(p),
                        "kendall_w": float(chi2 / (n * (k - 1))) if n > 0 else np.nan,
                    }
                )

        # Friedman: modelos dentro de cada estrategia.
        for estrategia in ESTRATEGIAS:
            sub = df[df["estrategia"] == estrategia]
            pivot = sub.pivot_table(index="obs_id", columns="modelo", values="valor", aggfunc="first")
            pivot = pivot.dropna(subset=MODELOS)
            if len(pivot) >= 2:
                arrays = [pivot[m].to_numpy() for m in MODELOS]
                chi2, p = stats.friedmanchisquare(*arrays)
                k = len(MODELOS)
                n = len(pivot)
                friedman_rows.append(
                    {
                        "escenario": scenario_name,
                        "familia": "modelo_dentro_de_estrategia",
                        "bloque": ESTRATEGIA_LABEL[estrategia],
                        "n_bloques": n,
                        "k": k,
                        "chi2": float(chi2),
                        "gl": k - 1,
                        "p": float(p),
                        "kendall_w": float(chi2 / (n * (k - 1))) if n > 0 else np.nan,
                    }
                )

        # Comparaciones pareadas: estrategias dentro de modelo.
        family = "estrategia_dentro_de_modelo"
        rows_family = []
        for modelo in MODELOS:
            for e1, e2 in combinations(ESTRATEGIAS, 2):
                pair = paired_data(df, "valor", e1, e2, modelo)
                res = wilcoxon_pair(pair["x"].to_numpy(), pair["y"].to_numpy())
                boot = bootstrap_pair(pair, np.random.default_rng(SEED + len(rows_family) + 1))
                rows_family.append(
                    {
                        "escenario": scenario_name,
                        "familia": family,
                        "bloque": modelo,
                        "comparacion": f"{ESTRATEGIA_LABEL[e1]} - {ESTRATEGIA_LABEL[e2]}",
                        "estrategia_1": e1,
                        "estrategia_2": e2,
                        "modelo_1": modelo,
                        "modelo_2": modelo,
                        **res,
                        "bootstrap_media_ic95_inf": boot[1],
                        "bootstrap_media_ic95_sup": boot[2],
                        "bootstrap_mediana_ic95_inf": boot[4],
                        "bootstrap_mediana_ic95_sup": boot[5],
                    }
                )
        pvals = np.array([r["p_wilcoxon"] for r in rows_family], dtype=float)
        valid = np.isfinite(pvals)
        adjusted = np.full_like(pvals, np.nan)
        if valid.any():
            adjusted[valid] = multipletests(pvals[valid], method="holm")[1]
        for row, p_holm in zip(rows_family, adjusted):
            row["p_holm"] = float(p_holm) if np.isfinite(p_holm) else np.nan
            row["sig_holm_005"] = bool(np.isfinite(p_holm) and p_holm < 0.05)
        wilcoxon_rows.extend(rows_family)

        # Comparaciones pareadas: modelos dentro de estrategia.
        family = "modelo_dentro_de_estrategia"
        rows_family = []
        for estrategia in ESTRATEGIAS:
            for m1, m2 in combinations(MODELOS, 2):
                pair = paired_models_data(df, "valor", m1, m2, estrategia)
                res = wilcoxon_pair(pair["x"].to_numpy(), pair["y"].to_numpy())
                boot = bootstrap_pair(pair, np.random.default_rng(SEED + 1000 + len(rows_family) + 1))
                rows_family.append(
                    {
                        "escenario": scenario_name,
                        "familia": family,
                        "bloque": ESTRATEGIA_LABEL[estrategia],
                        "comparacion": f"{m1} - {m2}",
                        "estrategia_1": estrategia,
                        "estrategia_2": estrategia,
                        "modelo_1": m1,
                        "modelo_2": m2,
                        **res,
                        "bootstrap_media_ic95_inf": boot[1],
                        "bootstrap_media_ic95_sup": boot[2],
                        "bootstrap_mediana_ic95_inf": boot[4],
                        "bootstrap_mediana_ic95_sup": boot[5],
                    }
                )
        pvals = np.array([r["p_wilcoxon"] for r in rows_family], dtype=float)
        valid = np.isfinite(pvals)
        adjusted = np.full_like(pvals, np.nan)
        if valid.any():
            adjusted[valid] = multipletests(pvals[valid], method="holm")[1]
        for row, p_holm in zip(rows_family, adjusted):
            row["p_holm"] = float(p_holm) if np.isfinite(p_holm) else np.nan
            row["sig_holm_005"] = bool(np.isfinite(p_holm) and p_holm < 0.05)
        wilcoxon_rows.extend(rows_family)

        # Guardar CIs de celdas en formato largo.
        for (estrategia, modelo), ci in cell_ci.items():
            cell_ci_rows.append(
                {
                    "escenario": scenario_name,
                    "estrategia": estrategia,
                    "modelo": modelo,
                    "media": ci[0],
                    "media_ic95_inf": ci[1],
                    "media_ic95_sup": ci[2],
                    "mediana": ci[3],
                    "mediana_ic95_inf": ci[4],
                    "mediana_ic95_sup": ci[5],
                }
            )

    cells = pd.DataFrame(cell_rows)
    cells["_e"] = cells["estrategia"].map({e: i for i, e in enumerate(ESTRATEGIAS)})
    cells["_m"] = cells["modelo"].map({m: i for i, m in enumerate(MODELOS)})
    cells = cells.sort_values(["escenario", "_e", "_m"]).drop(columns=["_e", "_m"])
    cells.to_csv(SALIDAS / "10_resumen_celdas_escenarios.csv", index=False, encoding="utf-8")

    friedman = pd.DataFrame(friedman_rows)
    friedman.to_csv(SALIDAS / "11_friedman.csv", index=False, encoding="utf-8")

    wilcoxon = pd.DataFrame(wilcoxon_rows)
    wilcoxon.to_csv(SALIDAS / "12_wilcoxon_posthoc.csv", index=False, encoding="utf-8")

    cell_ci = pd.DataFrame(cell_ci_rows)
    cell_ci.to_csv(SALIDAS / "13_bootstrap_celdas.csv", index=False, encoding="utf-8")

    comparison = pd.read_csv(DATOS / "04_comparacion_medianas_manuscrito.csv")
    comparison.to_csv(SALIDAS / "14_comparacion_medianas_manuscrito.csv", index=False, encoding="utf-8")

    # Resumen legible por máquina.
    primary = cells[cells["escenario"] == "principal_cero_no_sustantivas"]
    summary = {
        "semilla_bootstrap": SEED,
        "n_bootstrap": N_BOOT,
        "n_observaciones": int(len(raw)),
        "n_unidades": int(raw["obs_id"].nunique()),
        "n_casos": int(raw["caso_id"].nunique()),
        "n_no_sustantivas": int(raw["es_no_sustantiva"].sum()),
        "escenario_principal": "principal_cero_no_sustantivas",
        "friedman_principal": friedman[
            friedman["escenario"] == "principal_cero_no_sustantivas"
        ].to_dict(orient="records"),
        "celdas_principal": primary[
            ["estrategia", "modelo", "n", "n_no_sustantiva", "media", "mediana", "prop_ge_075"]
        ].to_dict(orient="records"),
        "nota": (
            "La imputación principal asigna 0 a las tres evaluaciones de toda respuesta no sustantiva. "
            "La exclusión es sensibilidad y no debe interpretarse como efecto causal."
        ),
    }
    (SALIDAS / "15_resumen_no_parametrico.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Filas de celdas: {len(cells)}")
    print(f"Pruebas Friedman: {len(friedman)}")
    print(f"Comparaciones Wilcoxon: {len(wilcoxon)}")
    print(f"Salidas: {SALIDAS}")


if __name__ == "__main__":
    main()

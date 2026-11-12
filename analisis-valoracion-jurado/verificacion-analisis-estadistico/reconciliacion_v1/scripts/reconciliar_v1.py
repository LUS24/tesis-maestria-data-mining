#!/usr/bin/env python3
"""Reconciliación de las cifras V.1/V.6 con la corrección 01 (NV-01).

No modifica fuentes ni artefactos históricos. Lee la tabla larga derivada de
corrección 01, recalcula las pruebas pareadas y deja una tabla explícita de
método, unidad, corrección y resultado.

Uso:
    cd codigo_experimentos
    uv run --frozen python ../analisis-valoracion-jurado/verificacion-analisis-estadistico/reconciliacion_v1/scripts/reconciliar_v1.py
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

PACKAGE = Path(__file__).resolve().parent.parent
VERIF = PACKAGE.parent
ANALISIS = VERIF.parent
REPO = ANALISIS.parent
WIDE = ANALISIS / "correccion-01-analisis-estadistico" / "datos" / "01_wide_711.csv"
LONG = ANALISIS / "correccion-01-analisis-estadistico" / "datos" / "02_long_2133.csv"
FRIEDMAN = ANALISIS / "correccion-01-analisis-estadistico" / "salidas" / "33_friedman_principal.csv"
OUT = PACKAGE / "datos"
SALIDAS = PACKAGE / "salidas"

ESTRATEGIAS = {
    "sin_rag": "llm_responses_no_rag",
    "rag_basico": "llm_responses_base_rag",
    "agentic": "llm_responses_agentic_rag",
}
MODELOS = {"nano": "gpt-5-nano", "mini": "gpt-5-mini", "gpt5": "gpt-5"}
KEYS = ["numero_pregunta", "numero_subpregunta", "estrategia", "modelo"]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canon_sub(value: object) -> int:
    if value is None or str(value).strip() == "" or str(value).lower() == "nan":
        return 0
    return int(float(value))


def wide_scores(score: str) -> pd.DataFrame:
    """Usa la tabla ancha canónica de corrección 01, con sus valores redondeados.

    `02_long_2133.csv` conserva la precisión completa; la tabla ancha es la que
    alimentó las pruebas publicadas en `34_wilcoxon_principal.csv`. Para
    reconciliar contra esas pruebas hay que usar la misma entrada.
    """
    df = pd.read_csv(WIDE)
    df["q"] = df["nro_pregunta"].astype(int)
    df["sub"] = df["nro_subpregunta"].map(canon_sub)
    wide = df.pivot_table(
        index=["q", "sub"],
        columns=["estrategia", "modelo"],
        values=score,
    )
    return wide


def compare_values(x: np.ndarray, y: np.ndarray, *, zero_method: str = "wilcox") -> dict[str, Any]:
    pair = pd.DataFrame({"x": x, "y": y}).dropna()
    x, y = pair["x"].to_numpy(), pair["y"].to_numpy()
    diff = x - y
    raw = {
        "n": int(len(pair)),
        "media_1": float(np.mean(x)),
        "media_2": float(np.mean(y)),
        "diferencia_media": float(np.mean(diff)),
        "mediana_diferencia": float(np.median(diff)),
    }
    for label, alternative in (("dos_colas", "two-sided"), ("una_cola", "less")):
        try:
            raw[f"p_wilcoxon_{label}"] = float(
                stats.wilcoxon(x, y, zero_method=zero_method, alternative=alternative, method="auto").pvalue
            )
        except ValueError:
            raw[f"p_wilcoxon_{label}"] = np.nan
    raw["p_t"] = float(stats.ttest_rel(x, y).pvalue)
    return raw


def holm(rows: list[dict[str, Any]], p_field: str = "p_wilcoxon_dos_colas") -> list[dict[str, Any]]:
    p_values = np.array([row[p_field] for row in rows], dtype=float)
    adjusted = multipletests(p_values, method="holm")[1]
    for row, p_adj in zip(rows, adjusted, strict=True):
        row["p_holm"] = float(p_adj)
    return rows


def comparison_specs() -> list[dict[str, Any]]:
    """Todas las comparaciones de las dos familias de Holm (9 cada una).

    - ``modelo_dentro_de_estrategia``: 3 estrategias × 3 pares de modelos.
    - ``estrategia_dentro_de_modelo``: 3 modelos × 3 pares de estrategias.
    La corrección 01 aplica Holm sobre las nueve comparaciones de la familia;
    las filas marcadas como ``seleccionada`` son las que se reportan en V.1.
    """
    specs: list[dict[str, Any]] = []
    for estrategia in ("sin_rag", "rag_basico", "agentic"):
        for m1, m2 in (("nano", "mini"), ("nano", "gpt5"), ("mini", "gpt5")):
            specs.append(
                {
                    "familia": "modelo_dentro_de_estrategia",
                    "bloque": estrategia,
                    "comparacion": f"{m1} - {m2}",
                    "a": f"{estrategia}/{m1}",
                    "b": f"{estrategia}/{m2}",
                    "seleccionada": estrategia == "rag_basico",
                }
            )
    for modelo in ("nano", "mini", "gpt5"):
        for e1, e2 in (("sin_rag", "rag_basico"), ("sin_rag", "agentic"), ("rag_basico", "agentic")):
            specs.append(
                {
                    "familia": "estrategia_dentro_de_modelo",
                    "bloque": modelo,
                    "comparacion": f"{e1} - {e2}",
                    "a": f"{e1}/{modelo}",
                    "b": f"{e2}/{modelo}",
                    "seleccionada": modelo == "gpt5",
                }
            )
    return specs


def column(wide: pd.DataFrame, token: str) -> tuple[str, str]:
    estrategia, modelo = token.split("/")
    return ESTRATEGIAS[estrategia], MODELOS[modelo]


def build_v1(wide: pd.DataFrame) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    unit_rows: list[dict[str, Any]] = []
    case_rows: list[dict[str, Any]] = []
    for spec in comparison_specs():
        a, b = column(wide, spec["a"]), column(wide, spec["b"])
        unit = compare_values(wide[a].to_numpy(), wide[b].to_numpy(), zero_method="wilcox")
        unit.update(
            {
                "unidad": "unidad",
                "familia": spec["familia"],
                "bloque": spec["bloque"],
                "comparacion": spec["comparacion"],
                "seleccionada": spec["seleccionada"],
            }
        )
        unit_rows.append(unit)

        case_wide = wide[[a, b]].groupby(level="q").mean()
        case = compare_values(case_wide[a].to_numpy(), case_wide[b].to_numpy(), zero_method="wilcox")
        case.update(
            {
                "unidad": "caso",
                "familia": spec["familia"],
                "bloque": spec["bloque"],
                "comparacion": spec["comparacion"],
                "seleccionada": spec["seleccionada"],
            }
        )
        case_rows.append(case)

    for family in ("modelo_dentro_de_estrategia", "estrategia_dentro_de_modelo"):
        subset = [row for row in unit_rows if row["familia"] == family]
        holm(subset)
        subset = [row for row in case_rows if row["familia"] == family]
        holm(subset)
    return unit_rows, case_rows


def friedman_models(wide: pd.DataFrame, estrategia: str) -> dict[str, Any]:
    cols = [wide[(ESTRATEGIAS[estrategia], MODELOS[m])].to_numpy() for m in ("nano", "mini", "gpt5")]
    result = stats.friedmanchisquare(*cols)
    return {
        "familia": "modelo_dentro_de_estrategia",
        "bloque": estrategia,
        "n_bloques": int(len(cols[0])),
        "k": 3,
        "chi2": float(result.statistic),
        "gl": 2,
        "p": float(result.pvalue),
    }


def friedman_strategies(wide: pd.DataFrame, modelo: str) -> dict[str, Any]:
    cols = [wide[(ESTRATEGIAS[e], MODELOS[modelo])].to_numpy() for e in ("sin_rag", "rag_basico", "agentic")]
    result = stats.friedmanchisquare(*cols)
    return {
        "familia": "estrategia_dentro_de_modelo",
        "bloque": modelo,
        "n_bloques": int(len(cols[0])),
        "k": 3,
        "chi2": float(result.statistic),
        "gl": 2,
        "p": float(result.pvalue),
    }


def build_v6_from_wide(wide: pd.DataFrame) -> list[dict[str, Any]]:
    base = wide[(ESTRATEGIAS["agentic"], MODELOS["nano"])]
    subset = wide.loc[base.notna()]
    x = subset[(ESTRATEGIAS["agentic"], MODELOS["nano"])].to_numpy()
    rows: list[dict[str, Any]] = []
    for label, y_col in (
        ("nano_agentic - gpt5_agentic", (ESTRATEGIAS["agentic"], MODELOS["gpt5"])),
        ("nano_agentic - nano_rag_basico", (ESTRATEGIAS["rag_basico"], MODELOS["nano"])),
    ):
        y = subset[y_col].to_numpy()
        result = compare_values(x, y, zero_method="pratt")
        result.update(
            {
                "unidad": "unidad sustantiva",
                "comparacion": label,
                "n_casos": int(len({idx[0] for idx in subset.index})),
            }
        )
        rows.append(result)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SALIDAS.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(WIDE)
    if df.shape[0] != 711:
        raise ValueError(f"Se esperaban 711 filas y hay {df.shape[0]}")
    long_df = pd.read_csv(LONG)
    if long_df.shape[0] != 2133:
        raise ValueError(f"Se esperaban 2.133 filas largas y hay {long_df.shape[0]}")
    wide_principal = wide_scores("score_principal_prom")
    if wide_principal.shape[0] != 79:
        raise ValueError(f"Se esperaban 79 unidades y hay {wide_principal.shape[0]}")

    unit_rows, case_rows = build_v1(wide_principal)
    v6_wide = wide_scores("score_exclusion_prom")
    v6_rows = build_v6_from_wide(v6_wide)
    friedman = [
        friedman_models(wide_principal, "rag_basico"),
        friedman_strategies(wide_principal, "gpt5"),
    ]

    fields = [
        "familia", "bloque", "comparacion", "unidad", "n", "media_1", "media_2",
        "diferencia_media", "mediana_diferencia", "p_wilcoxon_dos_colas",
        "p_wilcoxon_una_cola", "p_t", "p_holm", "seleccionada",
    ]
    write_csv(OUT / "01_comparaciones_v1_unidad.csv", unit_rows, fields)
    write_csv(OUT / "02_comparaciones_v1_caso.csv", case_rows, fields)
    write_csv(OUT / "03_comparaciones_v6.csv", v6_rows, fields + ["n_casos"])
    write_csv(
        OUT / "04_friedman.csv",
        friedman,
        ["familia", "bloque", "n_bloques", "k", "chi2", "gl", "p"],
    )

    summary = {
        "fuente": str(WIDE.relative_to(REPO)),
        "hash_fuente": sha256(WIDE),
        "hash_long": sha256(LONG),
        "n_filas": int(df.shape[0]),
        "n_filas_long": int(long_df.shape[0]),
        "n_unidades": int(wide_principal.shape[0]),
        "v1": {
            "unidad": unit_rows,
            "caso": case_rows,
            "friedman": friedman,
        },
        "v6": v6_rows,
        "lectura": {
            "v1": "La corrección 01 usa la unidad como estimando principal y Holm sobre las nueve comparaciones de cada familia. Los p de la valoración no se reproducen exactamente porque no declara el manejo de empates/ceros, la unidad de la prueba ni el universo de comparaciones corregidas.",
            "v6": "Las 38 respuestas sustantivas de nano Agentic-RAG se comparan con gpt-5 Agentic-RAG y nano RAG básico en las mismas unidades; se usa Wilcoxon de rangos con signo con zero_method='pratt', que reproduce los p=0,19 y p=0,003 de la valoración.",
            "canonica": "Para Tabla 4 se usan las columnas p_holm de corrección 01 en V.1 y los p de Pratt en V.6. No se mezclan con los p ilustrativos de la valoración.",
        },
    }
    (SALIDAS / "reconciliacion_v1.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary["lectura"], ensure_ascii=False, indent=2))
    print(f"Salidas en {PACKAGE}")


if __name__ == "__main__":
    main()

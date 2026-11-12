"""Resume y orienta los resultados de IX.1.1 para su revisión.

Genera tablas legibles y un JSON con los números principales. No modifica
fuentes ni resultados intermedios.

Uso:
    uv run --project codigo_experimentos --no-sync --frozen \
      python analisis-valoracion-jurado/correccion-01-analisis-estadistico/src/summarize_results.py
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "analisis-valoracion-jurado" / "correccion-01-analisis-estadistico"
SALIDAS = OUT / "salidas"

PRIMARY = "principal_cero_no_sustantivas"
SCENARIOS = [
    "principal_cero_no_sustantivas",
    "observado_jueces_rubric",
    "exclusion_no_sustantivas",
    "solo_fallos_tecnicos_cero",
]


def fmt(x: Any, digits: int = 3) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "NA"
    return f"{float(x):.{digits}f}"


def orient_effect(
    df: pd.DataFrame,
    family: str,
    block: str,
    desired: tuple[str, str],
) -> dict[str, Any]:
    """Devuelve el contraste en el orden deseado, invirtiendo si hace falta."""
    sub = df[(df["familia"] == family) & (df["bloque"] == block)]
    a, b = desired
    for _, row in sub.iterrows():
        c = str(row["comparacion"])
        # Los contrastes guardados usan el orden de combn(): Sin RAG-RAG,
        # Sin RAG-Agentic, RAG-Agentic, o nano-mini, nano-gpt-5, mini-gpt-5.
        if c == f"{a} - {b}":
            return {
                "familia": family,
                "bloque": block,
                "comparacion": f"{a} - {b}",
                "dif_esperada": float(row["diferencia_esperada_plugin"]),
                "dif_esperada_ic95_inf": float(row["diferencia_esperada_ic95_inf"]),
                "dif_esperada_ic95_sup": float(row["diferencia_esperada_ic95_sup"]),
                "dif_p_ge_075": float(row["diferencia_p_ge_075_plugin"]),
                "dif_p_ge_075_ic95_inf": float(row["diferencia_p_ge_075_ic95_inf"]),
                "dif_p_ge_075_ic95_sup": float(row["diferencia_p_ge_075_ic95_sup"]),
            }
        if c == f"{b} - {a}":
            return {
                "familia": family,
                "bloque": block,
                "comparacion": f"{a} - {b}",
                "dif_esperada": -float(row["diferencia_esperada_plugin"]),
                "dif_esperada_ic95_inf": -float(row["diferencia_esperada_ic95_sup"]),
                "dif_esperada_ic95_sup": -float(row["diferencia_esperada_ic95_inf"]),
                "dif_p_ge_075": -float(row["diferencia_p_ge_075_plugin"]),
                "dif_p_ge_075_ic95_inf": -float(row["diferencia_p_ge_075_ic95_sup"]),
                "dif_p_ge_075_ic95_sup": -float(row["diferencia_p_ge_075_ic95_inf"]),
            }
    raise KeyError(f"No se encontró {family}/{block}/{desired} en {sub['comparacion'].tolist()}")


def main() -> None:
    cells = pd.read_csv(SALIDAS / "10_resumen_celdas_escenarios.csv")
    effects = pd.read_csv(SALIDAS / "24_efectos_simples_probabilidad.csv")
    model = pd.read_csv(SALIDAS / "20_modelo_interaccion.csv")
    friedman = pd.read_csv(SALIDAS / "11_friedman.csv")
    wilcoxon = pd.read_csv(SALIDAS / "12_wilcoxon_posthoc.csv")
    comparison = pd.read_csv(SALIDAS / "14_comparacion_medianas_manuscrito.csv")
    judges = pd.read_csv(SALIDAS / "25_modelo_por_juez.csv")

    # Tabla de celdas.
    primary_cells = cells[cells["escenario"] == PRIMARY].copy()
    observed_cells = cells[cells["escenario"] == "observado_jueces_rubric"].copy()
    exclusion_cells = cells[cells["escenario"] == "exclusion_no_sustantivas"].copy()
    table_cells = primary_cells[
        [
            "estrategia",
            "estrategia_label",
            "modelo",
            "n",
            "n_no_sustantiva",
            "media",
            "mediana",
            "prop_ge_075",
            "media_ic95_inf",
            "media_ic95_sup",
        ]
    ].rename(
        columns={
            "media": "media_principal",
            "mediana": "mediana_principal",
            "prop_ge_075": "p_ge_075_principal",
            "media_ic95_inf": "media_principal_ic95_inf",
            "media_ic95_sup": "media_principal_ic95_sup",
        }
    )
    table_cells = table_cells.merge(
        observed_cells[
            ["estrategia", "modelo", "media", "mediana", "prop_ge_075"]
        ].rename(
            columns={
                "media": "media_observada",
                "mediana": "mediana_observada",
                "prop_ge_075": "p_ge_075_observada",
            }
        ),
        on=["estrategia", "modelo"],
        how="left",
        validate="one_to_one",
    )
    table_cells = table_cells.merge(
        exclusion_cells[
            ["estrategia", "modelo", "media", "mediana", "n_no_nulos"]
        ].rename(
            columns={
                "media": "media_exclusion",
                "mediana": "mediana_exclusion",
                "n_no_nulos": "n_exclusion",
            }
        ),
        on=["estrategia", "modelo"],
        how="left",
        validate="one_to_one",
    )
    table_cells = table_cells[
        [
            "estrategia",
            "estrategia_label",
            "modelo",
            "n",
            "n_no_sustantiva",
            "media_principal",
            "mediana_principal",
            "p_ge_075_principal",
            "media_principal_ic95_inf",
            "media_principal_ic95_sup",
            "media_observada",
            "mediana_observada",
            "p_ge_075_observada",
            "media_exclusion",
            "mediana_exclusion",
            "n_exclusion",
        ]
    ]
    table_cells.to_csv(SALIDAS / "30_tabla_celdas_principal.csv", index=False, encoding="utf-8")

    # Efectos simples orientados de forma intuitiva.
    eff_primary = effects[effects["escenario"] == PRIMARY]
    rows: list[dict[str, Any]] = []
    for modelo_nivel in ["gpt-5-nano", "gpt-5-mini", "gpt-5"]:
        for desired in [
            ("Agentic-RAG", "RAG basico"),
            ("Agentic-RAG", "Sin RAG"),
            ("RAG basico", "Sin RAG"),
        ]:
            rows.append(orient_effect(eff_primary, "estrategia_dentro_de_modelo", modelo_nivel, desired))
    for strategy in ["Sin RAG", "RAG basico", "Agentic-RAG"]:
        for desired in [
            ("gpt-5-mini", "gpt-5-nano"),
            ("gpt-5", "gpt-5-nano"),
            ("gpt-5", "gpt-5-mini"),
        ]:
            rows.append(orient_effect(eff_primary, "modelo_dentro_de_estrategia", strategy, desired))
    oriented = pd.DataFrame(rows)
    oriented.to_csv(SALIDAS / "31_efectos_simples_orientados.csv", index=False, encoding="utf-8")

    # Comparación específica de la celda nano Agentic-RAG.
    nano_rows = []
    for scenario in SCENARIOS:
        sub = cells[(cells["escenario"] == scenario) & (cells["modelo"] == "gpt-5-nano")]
        for _, row in sub.iterrows():
            nano_rows.append(
                {
                    "escenario": scenario,
                    "estrategia": row["estrategia"],
                    "estrategia_label": row["estrategia_label"],
                    "n_no_nulos": row["n_no_nulos"],
                    "media": row["media"],
                    "mediana": row["mediana"],
                    "p_ge_075": row["prop_ge_075"],
                    "media_ic95_inf": row["media_ic95_inf"],
                    "media_ic95_sup": row["media_ic95_sup"],
                }
            )
    nano = pd.DataFrame(nano_rows)
    nano.to_csv(SALIDAS / "32_tabla_sensibilidad_nano.csv", index=False, encoding="utf-8")

    # Friedman principal en formato legible.
    friedman_primary = friedman[friedman["escenario"] == PRIMARY].copy()
    friedman_primary.to_csv(SALIDAS / "33_friedman_principal.csv", index=False, encoding="utf-8")

    # Wilcoxon principal, con etiquetas.
    wilcoxon_primary = wilcoxon[wilcoxon["escenario"] == PRIMARY].copy()
    wilcoxon_primary.to_csv(SALIDAS / "34_wilcoxon_principal.csv", index=False, encoding="utf-8")

    # JSON de números principales.
    primary_model = model[model["escenario"] == PRIMARY].iloc[0].to_dict()
    key_nano = {}
    for scenario in SCENARIOS:
        sub = nano[(nano["escenario"] == scenario) & (nano["estrategia"] == "llm_responses_agentic_rag")]
        if len(sub):
            r = sub.iloc[0]
            key_nano[scenario] = {
                "media": float(r["media"]),
                "mediana": float(r["mediana"]),
                "p_ge_075": float(r["p_ge_075"]),
                "n_no_nulos": int(r["n_no_nulos"]),
            }

    def find_effect(family: str, block: str, a: str, b: str) -> dict[str, Any]:
        return orient_effect(eff_primary, family, block, (a, b))

    key = {
        "n_observaciones": int(primary_model["n_observaciones"]),
        "n_casos": int(primary_model["n_casos"]),
        "n_unidades": int(primary_model["n_unidades"]),
        "n_jueces": int(primary_model["n_jueces"]),
        "n_no_sustantivas": int(cells[(cells["escenario"] == PRIMARY)]["n_no_sustantiva"].sum()),
        "modelo_principal": {
            "LR_interaccion": float(primary_model["LR_interaccion"]),
            "gl_interaccion": int(primary_model["gl_interaccion"]),
            "p_interaccion": float(primary_model["p_interaccion"]),
            "var_caso": float(primary_model["var_caso"]),
            "var_unidad": float(primary_model["var_unidad"]),
            "AIC_full": float(primary_model["AIC_full"]),
            "AIC_reduced": float(primary_model["AIC_reduced"]),
        },
        "nano_agentic": key_nano,
        "efectos_clave": {
            "nano_agentic_menos_rag": find_effect(
                "estrategia_dentro_de_modelo", "gpt-5-nano", "Agentic-RAG", "RAG basico"
            ),
            "mini_agentic_menos_rag": find_effect(
                "estrategia_dentro_de_modelo", "gpt-5-mini", "Agentic-RAG", "RAG basico"
            ),
            "gpt5_agentic_menos_rag": find_effect(
                "estrategia_dentro_de_modelo", "gpt-5", "Agentic-RAG", "RAG basico"
            ),
        },
        "friedman_principal": friedman_primary.to_dict(orient="records"),
        "jueces": judges.groupby("juez", as_index=False).agg(
            LR_interaccion=("LR_interaccion", "first"),
            p_interaccion=("p_interaccion", "first"),
            convergencia=("convergencia", "first"),
        ).to_dict(orient="records"),
        "comparacion_manuscrito": comparison.to_dict(orient="records"),
        "nota": (
            "El escenario principal imputa 0 a todas las evaluaciones de respuestas no sustantivas. "
            "La exclusión es un análisis de sensibilidad con selección no aleatoria."
        ),
    }
    (SALIDAS / "35_resultados_clave.json").write_text(
        json.dumps(key, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(key["modelo_principal"], indent=2, ensure_ascii=False))
    print("\nCeldas:")
    print(table_cells.to_string(index=False))
    print("\nEfectos orientados:")
    print(oriented.to_string(index=False))
    print(f"\nEscrito en {SALIDAS}")


if __name__ == "__main__":
    main()

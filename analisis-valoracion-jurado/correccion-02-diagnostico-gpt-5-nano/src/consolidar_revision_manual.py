"""Consolida la revisión manual aceptada y prepara la base de IX.1.1.

Entrada:
- salidas/01_dataset_derivado_711.csv (clasificación automática, intacta)
- revision_manual/plantilla_resultados.csv (versión aceptada)
- salidas/mapa_revision_ciega.csv
- part_i/final_judge_results.csv y part_i/combined_metrics_for_analysis.csv

Salida:
- salidas/14_dataset_categoria_final.csv
- salidas/15_resumen_por_celda_final.csv
- salidas/16_conteo_categorias_final.csv
- salidas/16b_tabla_categorias_ancha_final.csv
- salidas/17_auditoria_jueces_salidas_no_sustantivas_final.csv
- salidas/18_resumen_jueces_no_sustantivas_final.csv
- salidas/19_sensibilidad_pares_estrategias_final.csv
- salidas/20_comparacion_medianas_final.csv
- salidas/21_sin_rag_nano_vs_mini_final.csv
- salidas/resumen_ejecutivo_final.json
- figuras_final/01..07 (PDF y PNG)

No modifica la base automática ni los archivos fuente.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import diagnostico as dg

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "analisis-valoracion-jurado" / "correccion-02-diagnostico-gpt-5-nano"
SALIDAS = OUT / "salidas"
REVISION = OUT / "revision_manual"
FIGURAS_FINAL = OUT / "figuras_final"

AUTO_DATASET = SALIDAS / "01_dataset_derivado_711.csv"
TEMPLATE = REVISION / "plantilla_resultados.csv"
MAPPING = SALIDAS / "mapa_revision_ciega.csv"
JUDGES = BASE / "codigo_experimentos" / "part_i" / "final_judge_results.csv"
METRICS = BASE / "codigo_experimentos" / "part_i" / "combined_metrics_for_analysis.csv"

REVIEWED = 87
EXPECTED_OBS = 711
EXPECTED_UNITS = 79


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")


def main() -> None:
    SALIDAS.mkdir(parents=True, exist_ok=True)
    FIGURAS_FINAL.mkdir(parents=True, exist_ok=True)

    auto = read_csv(AUTO_DATASET)
    auto["q"] = auto["q"].astype(int)
    auto["sub"] = auto["sub"].astype(int)
    template = read_csv(TEMPLATE)
    mapping = read_csv(MAPPING)
    judges = read_csv(JUDGES)
    metrics = read_csv(METRICS)

    if len(auto) != EXPECTED_OBS or auto["obs_id"].nunique() != EXPECTED_UNITS:
        raise SystemExit("La base automática no tiene 711 observaciones / 79 unidades.")
    if len(template) != REVIEWED:
        raise SystemExit(f"La plantilla debe tener {REVIEWED} filas; tiene {len(template)}.")
    if len(mapping) != REVIEWED:
        raise SystemExit(f"El mapa debe tener {REVIEWED} filas; tiene {len(mapping)}.")
    if not template["categoria_revisada"].isin(dg.CATEGORIAS).all():
        invalid = template.loc[~template["categoria_revisada"].isin(dg.CATEGORIAS), "review_id"]
        raise SystemExit(f"Categorías inválidas en la plantilla: {invalid.tolist()}")
    if (template["justificacion"].str.strip() == "").any():
        raise SystemExit("La plantilla aceptada tiene justificaciones vacías.")
    if (template["review_id"] != mapping["review_id"]).any():
        raise SystemExit("Los review_id de plantilla y mapa no coinciden en orden.")

    # Traer la clave de observación desde el mapa.
    review = template.merge(
        mapping[["review_id", "obs_id", "estrategia", "modelo"]],
        on="review_id",
        how="left",
        validate="one_to_one",
    )
    if review["obs_id"].isna().any():
        raise SystemExit("Hay review_id sin observación en el mapa.")

    final = auto.merge(
        review[["obs_id", "estrategia", "modelo", "review_id", "categoria_revisada", "justificacion"]],
        on=["obs_id", "estrategia", "modelo"],
        how="left",
        validate="one_to_one",
    )
    if len(final) != EXPECTED_OBS:
        raise SystemExit("La consolidación perdió observaciones.")

    final["categoria_auto"] = final["categoria"]
    final["subcategoria_auto"] = final["subcategoria"]
    final["categoria_manual"] = final["categoria_revisada"]
    final["justificacion_manual"] = final["justificacion"]
    final["revision_manual_id"] = final["review_id"]
    final["categoria_final"] = final["categoria_manual"].fillna(final["categoria_auto"])
    final["subcategoria_final"] = np.where(
        final["categoria_final"] == final["categoria_auto"],
        final["subcategoria_auto"],
        "revision_manual",
    )
    final["fuente_categoria"] = np.where(
        final["categoria_manual"].notna(),
        "revision_manual",
        "clasificacion_automatica",
    )
    final["categoria_label_final"] = final["categoria_final"].map(dg.CATEGORIA_LABEL)
    final["es_no_sustantiva_final"] = final["categoria_final"] != "sustantiva"
    final["es_fallo_tecnico_final"] = final["categoria_final"].isin(dg.CATEGORIAS_TECNICAS)

    original = pd.to_numeric(final["puntaje_original_rubric"], errors="coerce")
    final["puntaje_final_original"] = original
    final["puntaje_final_fallo_cero"] = np.where(
        final["es_no_sustantiva_final"], 0.0, original
    )
    final["puntaje_final_solo_fallos_tecnicos_cero"] = np.where(
        final["es_fallo_tecnico_final"], 0.0, original
    )
    final["puntaje_final_exclusion"] = np.where(
        final["es_no_sustantiva_final"], np.nan, original
    )

    # Alias para reutilizar las funciones de diagnóstico sin tocar la base automática.
    fs = final.copy()
    fs["categoria"] = fs["categoria_final"]
    fs["subcategoria"] = fs["subcategoria_final"]
    fs["es_no_sustantiva"] = fs["es_no_sustantiva_final"]
    fs["es_fallo_tecnico"] = fs["es_fallo_tecnico_final"]
    fs["puntaje_original_rubric"] = fs["puntaje_final_original"]
    fs["puntaje_fallo_cero"] = fs["puntaje_final_fallo_cero"]
    fs["puntaje_solo_fallos_tecnicos_cero"] = fs["puntaje_final_solo_fallos_tecnicos_cero"]
    fs["puntaje_exclusion"] = fs["puntaje_final_exclusion"]
    for bool_col in ["cita_articulo", "menciona_limitacion"]:
        if bool_col in fs.columns:
            fs[bool_col] = fs[bool_col].map(lambda x: str(x).strip().lower() == "true")
    for numeric_col in [
        "costo_total",
        "output_tokens",
        "reasoning_tokens",
        "longitud_caracteres",
        "law_final_result_count",
        "law_output_tokens",
        "law_reasoning_tokens",
    ]:
        if numeric_col in fs.columns:
            fs[numeric_col] = pd.to_numeric(fs[numeric_col], errors="coerce")

    judges["q"] = judges["numero_pregunta"].astype(int)
    judges["sub"] = judges["numero_subpregunta"].map(dg.canon_sub)
    judges["obs_id"] = [dg.obs_id(q, s) for q, s in zip(judges["q"], judges["sub"])]

    judge_audit = dg.build_judge_audit(fs, judges)

    # Actualizar la bandera de jueces para la base final, incluyendo R052.
    fs["juez_no_cero_en_no_sustantiva"] = False
    fs["juez_max_en_no_sustantiva"] = np.nan
    for idx, row in fs[fs["es_no_sustantiva"]].iterrows():
        scores = (
            json.loads(row["respuesta_correcta_scores_json"])
            if isinstance(row["respuesta_correcta_scores_json"], str)
            else []
        )
        fs.at[idx, "juez_no_cero_en_no_sustantiva"] = any(float(s) > 0 for s in scores)
        fs.at[idx, "juez_max_en_no_sustantiva"] = max(scores) if scores else np.nan

    summary = dg.summarize_cells(fs)
    categories = dg.summarize_categories(fs)
    manuscript = dg.build_manuscript_comparison(fs, metrics)
    sensitivity = dg.build_sensitivity(fs)
    no_rag = dg.build_no_rag_descriptive(fs)

    categories_wide = (
        categories.pivot(index=["estrategia", "estrategia_corta", "modelo"], columns="categoria", values="n")
        .fillna(0)
        .astype(int)
        .reset_index()
    )

    judge_summary = (
        judge_audit.groupby(["categoria", "modelo_juez"], dropna=False)
        .agg(
            n_filas=("obs_id", "size"),
            no_cero_correcta=("puntaje_correcta_no_cero", "sum"),
            no_cero_legal=("puntaje_legal_no_cero", "sum"),
        )
        .reset_index()
    )

    # Guardar dataset final y tablas.
    final_out = final.drop(columns=["categoria_revisada", "justificacion", "review_id"])
    final_out.to_csv(SALIDAS / "14_dataset_categoria_final.csv", index=False, encoding="utf-8")
    summary.to_csv(SALIDAS / "15_resumen_por_celda_final.csv", index=False, encoding="utf-8")
    categories.to_csv(SALIDAS / "16_conteo_categorias_final.csv", index=False, encoding="utf-8")
    categories_wide.to_csv(
        SALIDAS / "16b_tabla_categorias_ancha_final.csv", index=False, encoding="utf-8"
    )
    judge_audit.to_csv(
        SALIDAS / "17_auditoria_jueces_salidas_no_sustantivas_final.csv",
        index=False,
        encoding="utf-8",
    )
    judge_summary.to_csv(
        SALIDAS / "18_resumen_jueces_no_sustantivas_final.csv",
        index=False,
        encoding="utf-8",
    )
    sensitivity.to_csv(
        SALIDAS / "19_sensibilidad_pares_estrategias_final.csv", index=False, encoding="utf-8"
    )
    manuscript.to_csv(SALIDAS / "20_comparacion_medianas_final.csv", index=False, encoding="utf-8")
    no_rag.to_csv(SALIDAS / "21_sin_rag_nano_vs_mini_final.csv", index=False, encoding="utf-8")

    # Resumen final legible por máquina.
    nano = final[final["estrategia"] == "llm_responses_agentic_rag"]
    nano = nano[nano["modelo"] == "gpt-5-nano"]
    nano_counts = nano["categoria_final"].value_counts().to_dict()
    no_rag_mini = final[(final["estrategia"] == "llm_responses_no_rag") & (final["modelo"] == "gpt-5-mini")]
    no_rag_nano = final[(final["estrategia"] == "llm_responses_no_rag") & (final["modelo"] == "gpt-5-nano")]
    nonzero_correct = judge_audit[judge_audit["puntaje_correcta_no_cero"]]
    nonzero_legal = judge_audit[judge_audit["puntaje_legal_no_cero"]]

    final_summary = {
        "n_observaciones": int(len(final)),
        "n_unidades": int(final["obs_id"].nunique()),
        "n_casos": int(final["q"].nunique()),
        "n_celdas": int(final.groupby(["estrategia", "modelo"]).ngroups),
        "n_revisadas_manual": int(final["categoria_manual"].notna().sum()),
        "n_cambios_categoria_por_revision": int(
            (final["categoria_manual"].notna() & (final["categoria_manual"] != final["categoria_auto"])).sum()
        ),
        "n_no_sustantivas_total": int(final["es_no_sustantiva_final"].sum()),
        "n_sustantivas_total": int((~final["es_no_sustantiva_final"]).sum()),
        "categorias_finales": final["categoria_final"].value_counts().to_dict(),
        "agentic_nano": {
            "n": int(len(nano)),
            "categorias": {k: int(v) for k, v in nano_counts.items()},
            "n_sustantiva": int((nano["categoria_final"] == "sustantiva").sum()),
            "n_no_sustantiva": int((nano["categoria_final"] != "sustantiva").sum()),
        },
        "sin_rag_nano": {
            "n_sustantiva": int((no_rag_nano["categoria_final"] == "sustantiva").sum()),
            "n_no_sustantiva": int((no_rag_nano["categoria_final"] != "sustantiva").sum()),
            "mediana_original": float(pd.to_numeric(no_rag_nano["puntaje_final_original"], errors="coerce").median()),
        },
        "sin_rag_mini": {
            "n_sustantiva": int((no_rag_mini["categoria_final"] == "sustantiva").sum()),
            "n_no_sustantiva": int((no_rag_mini["categoria_final"] != "sustantiva").sum()),
            "categorias": no_rag_mini["categoria_final"].value_counts().to_dict(),
            "mediana_original": float(pd.to_numeric(no_rag_mini["puntaje_final_original"], errors="coerce").median()),
            "mediana_fallo_cero": float(pd.to_numeric(no_rag_mini["puntaje_final_fallo_cero"], errors="coerce").median()),
            "mediana_exclusion": float(pd.to_numeric(no_rag_mini["puntaje_final_exclusion"], errors="coerce").median()),
        },
        "jueces_no_sustantivas": {
            "n_filas": int(len(judge_audit)),
            "n_puntajes_correcta_no_cero": int(len(nonzero_correct)),
            "n_observaciones_celda_con_al_menos_un_no_cero": int(
                nonzero_correct[["obs_id", "estrategia", "modelo"]].drop_duplicates().shape[0]
            ),
            "n_obs_id_distintos_con_al_menos_un_no_cero": int(nonzero_correct["obs_id"].nunique()),
            "n_puntajes_legal_no_cero": int(len(nonzero_legal)),
        },
        "medianas_finales": manuscript.to_dict(orient="records"),
        "sensibilidad_final": sensitivity.to_dict(orient="records"),
    }
    (SALIDAS / "resumen_ejecutivo_final.json").write_text(
        json.dumps(final_summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Figuras finales separadas de las automáticas.
    old_figures = dg.FIGURAS
    dg.FIGURAS = FIGURAS_FINAL
    try:
        dg.figure_composicion(fs)
        dg.figure_failure_rates(summary)
        dg.figure_nano_states(fs)
        dg.figure_scores_by_state(fs)
        dg.figure_nano_logs(fs)
        dg.figure_nano_scenarios(fs)
        dg.figure_no_rag_nano_mini(fs)
    finally:
        dg.FIGURAS = old_figures

    print("=" * 78)
    print("CONSOLIDACIÓN DE LA REVISIÓN MANUAL ACEPTADA")
    print("=" * 78)
    print(f"Observaciones: {len(final)} | Unidades: {final['obs_id'].nunique()} | Celdas: {final.groupby(['estrategia', 'modelo']).ngroups}")
    print(f"Revisadas manualmente: {int(final['categoria_manual'].notna().sum())}")
    print(f"Cambios de categoría por revisión: {final_summary['n_cambios_categoria_por_revision']}")
    print(f"No sustantivas finales: {final_summary['n_no_sustantivas_total']}")
    print("\nCategorías finales:")
    print(final["categoria_final"].value_counts().to_string())
    print("\nAgentic-RAG + gpt-5-nano:")
    print(nano["categoria_final"].value_counts().to_string())
    print("\nSin RAG + gpt-5-mini:")
    print(no_rag_mini["categoria_final"].value_counts().to_string())
    print("\nJueces sobre no sustantivas finales:")
    print(judge_summary.to_string(index=False))
    print("\nResumen final:", SALIDAS / "resumen_ejecutivo_final.json")
    print("Figuras finales:", FIGURAS_FINAL)


if __name__ == "__main__":
    main()

"""Construye la base analítica de la corrección IX.1.1.

Lee, sin modificarlos, los artefactos derivados de la corrección 02 y los
registros individuales de los jueces. Genera dos tablas nuevas:

- datos/01_wide_711.csv: una fila por unidad × configuración.
- datos/02_long_2133.csv: una fila por unidad × configuración × juez.

La clasificación de respuestas no sustantivas es automática mientras la
plantilla de revisión ciega de la corrección 02 no esté completa. Si está
completa, se usa la categoría revisada por la persona y se registra la fuente.

Uso:
    uv run --project codigo_experimentos --no-sync --frozen \
      python analisis-valoracion-jurado/correccion-01-reanalisis-inferencial/src/build_dataset.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "analisis-valoracion-jurado" / "correccion-01-reanalisis-inferencial"
DATOS = OUT / "datos"
SALIDAS = OUT / "salidas"

CORR02 = BASE / "analisis-valoracion-jurado" / "correccion-02-diagnostico-gpt-5-nano"
SOURCE_WIDE = CORR02 / "salidas" / "01_dataset_derivado_711.csv"
SOURCE_JUDGES = BASE / "codigo_experimentos" / "part_i" / "final_judge_results.csv"
SOURCE_METRICS = BASE / "codigo_experimentos" / "part_i" / "combined_metrics_for_analysis.csv"
TEMPLATE = CORR02 / "revision_manual" / "plantilla_resultados.csv"
MAPPING = CORR02 / "salidas" / "mapa_revision_ciega.csv"

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
RUBRICA = [0.0, 0.25, 0.5, 0.75, 1.0]
CATEGORIAS_VALIDAS = {
    "sustantiva",
    "vacia",
    "solo_espacios",
    "abstencion_explicita",
    "error_explicito",
    "truncada",
    "indeterminada",
}
CATEGORIAS_TECNICAS = {"vacia", "solo_espacios", "error_explicito", "truncada", "indeterminada"}

MEDIANAS_MANUSCRITO = {
    ("llm_responses_no_rag", "gpt-5-nano"): 0.583,
    ("llm_responses_no_rag", "gpt-5-mini"): 0.333,
    ("llm_responses_no_rag", "gpt-5"): 0.833,
    ("llm_responses_base_rag", "gpt-5-nano"): 0.583,
    ("llm_responses_base_rag", "gpt-5-mini"): 0.625,
    ("llm_responses_base_rag", "gpt-5"): 0.833,
    ("llm_responses_agentic_rag", "gpt-5-nano"): 0.083,
    ("llm_responses_agentic_rag", "gpt-5-mini"): 0.917,
    ("llm_responses_agentic_rag", "gpt-5"): 0.958,
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canon_sub(value: Any) -> int:
    if value is None:
        return 0
    s = str(value).strip()
    if s in {"", "None", "nan", "NaN", "NA", "N/A"}:
        return 0
    return int(float(s))


def obs_id(q: Any, sub: Any) -> str:
    return f"Q{int(q):02d}_{canon_sub(sub):02d}"


def rubric_map(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    distances = [abs(x - r) for r in RUBRICA]
    minimum = min(distances)
    return max(r for r, d in zip(RUBRICA, distances) if d == minimum)


def read_csv_strings(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")


def manual_status() -> tuple[dict[str, Any], pd.DataFrame | None]:
    status: dict[str, Any] = {
        "plantilla": str(TEMPLATE.relative_to(BASE)),
        "mapa": str(MAPPING.relative_to(BASE)),
        "existe": TEMPLATE.exists() and MAPPING.exists(),
        "completa": False,
        "usa_manual": False,
        "n_filas": 0,
        "n_categorias_validas": 0,
        "n_categorias_vacias": 0,
        "n_categorias_invalidas": 0,
        "n_justificaciones_vacias": 0,
    }
    if not TEMPLATE.exists() or not MAPPING.exists():
        return status, None

    template = read_csv_strings(TEMPLATE)
    status["n_filas"] = len(template)
    if "categoria_revisada" not in template.columns:
        status["error"] = "Falta categoria_revisada"
        return status, None

    cat = template["categoria_revisada"].str.strip()
    just = template["justificacion"].str.strip() if "justificacion" in template.columns else pd.Series([""] * len(template))
    status["n_categorias_validas"] = int(cat.isin(CATEGORIAS_VALIDAS).sum())
    status["n_categorias_vacias"] = int((cat == "").sum())
    status["n_categorias_invalidas"] = int(((cat != "") & ~cat.isin(CATEGORIAS_VALIDAS)).sum())
    status["n_justificaciones_vacias"] = int((just == "").sum())
    status["completa"] = bool(
        len(template) > 0
        and (cat.isin(CATEGORIAS_VALIDAS)).all()
        and (just != "").all()
    )
    status["usa_manual"] = status["completa"]
    if not status["completa"]:
        return status, None

    mapping = read_csv_strings(MAPPING)
    required = {"review_id", "obs_id", "estrategia", "modelo"}
    if not required.issubset(mapping.columns):
        status["completa"] = False
        status["usa_manual"] = False
        status["error"] = f"Faltan columnas en el mapa: {sorted(required - set(mapping.columns))}"
        return status, None

    lookup = template[["review_id", "categoria_revisada", "justificacion", "revisor", "fecha"]].copy()
    lookup = lookup.rename(
        columns={
            "categoria_revisada": "categoria_manual",
            "justificacion": "justificacion_manual",
            "revisor": "revisor_manual",
            "fecha": "fecha_manual",
        }
    )
    merged = mapping.merge(lookup, on="review_id", how="left", validate="one_to_one")
    if merged["categoria_manual"].isna().any():
        status["completa"] = False
        status["usa_manual"] = False
        status["error"] = "Hay review_id del mapa sin fila en la plantilla"
        return status, None
    return status, merged


def main() -> None:
    DATOS.mkdir(parents=True, exist_ok=True)
    SALIDAS.mkdir(parents=True, exist_ok=True)

    wide_raw = read_csv_strings(SOURCE_WIDE)
    judges = read_csv_strings(SOURCE_JUDGES)
    metrics = read_csv_strings(SOURCE_METRICS)

    for df in (wide_raw, metrics):
        df["q"] = df["nro_pregunta"].astype(int)
        df["sub"] = df["nro_subpregunta"].map(canon_sub)
        df["obs_id"] = [obs_id(q, s) for q, s in zip(df["q"], df["sub"])]

    judges["q"] = judges["numero_pregunta"].astype(int)
    judges["sub"] = judges["numero_subpregunta"].map(canon_sub)
    judges["obs_id"] = [obs_id(q, s) for q, s in zip(judges["q"], judges["sub"])]
    judges["estrategia"] = judges["sistema"]
    judges["modelo"] = judges["modelo_respuesta"]
    judges["juez"] = judges["modelo_juez"]
    judges["score_raw"] = pd.to_numeric(judges["score_respuesta_correcta"], errors="coerce")
    judges["score_rubric"] = judges["score_raw"].map(rubric_map)

    # Clasificación: automática o manual completa.
    status, manual = manual_status()
    wide = wide_raw.copy()
    wide = wide.rename(
        columns={
            "categoria": "categoria_auto",
            "subcategoria": "subcategoria_auto",
            "evidencia": "evidencia_auto",
            "es_no_sustantiva": "es_no_sustantiva_auto",
            "es_fallo_tecnico": "es_fallo_tecnico_auto",
        }
    )
    wide["categoria_final"] = wide["categoria_auto"]
    wide["fuente_clasificacion"] = "automatica"
    wide["categoria_manual"] = ""
    wide["justificacion_manual"] = ""
    wide["revisor_manual"] = ""
    wide["fecha_manual"] = ""

    if status["usa_manual"] and manual is not None:
        lookup = manual[
            [
                "obs_id",
                "estrategia",
                "modelo",
                "categoria_manual",
                "justificacion_manual",
                "revisor_manual",
                "fecha_manual",
            ]
        ].drop_duplicates(["obs_id", "estrategia", "modelo"])
        wide = wide.merge(
            lookup,
            on=["obs_id", "estrategia", "modelo"],
            how="left",
            suffixes=("", "_manual_join"),
            validate="one_to_one",
        )
        has_manual = wide["categoria_manual"].notna() & (wide["categoria_manual"].astype(str).str.strip() != "")
        wide.loc[has_manual, "categoria_final"] = wide.loc[has_manual, "categoria_manual"]
        wide.loc[has_manual, "fuente_clasificacion"] = "manual_ciega"
        for col in ["justificacion_manual", "revisor_manual", "fecha_manual"]:
            manual_col = f"{col}_manual_join"
            if manual_col in wide.columns:
                wide[col] = wide[manual_col].fillna("")
                wide = wide.drop(columns=[manual_col])

    wide["categoria_final"] = wide["categoria_final"].fillna("").astype(str).str.strip()
    if not wide["categoria_final"].isin(CATEGORIAS_VALIDAS).all():
        invalid = wide.loc[~wide["categoria_final"].isin(CATEGORIAS_VALIDAS), ["obs_id", "estrategia", "modelo", "categoria_final"]]
        raise SystemExit(f"Categorías finales inválidas:\n{invalid.to_string(index=False)}")

    wide["es_no_sustantiva"] = wide["categoria_final"] != "sustantiva"
    wide["es_sustantiva"] = ~wide["es_no_sustantiva"]
    wide["es_fallo_tecnico"] = wide["categoria_final"].isin(CATEGORIAS_TECNICAS)
    wide["es_abstencion"] = wide["categoria_final"] == "abstencion_explicita"
    wide["caso_id"] = wide["q"].map(lambda q: f"C{int(q):02d}")
    wide["unidad_id"] = wide["obs_id"]

    # La tabla larga usa los registros individuales de los jueces.
    keep_categories = wide[
        [
            "obs_id",
            "estrategia",
            "modelo",
            "categoria_final",
            "es_no_sustantiva",
            "es_sustantiva",
            "es_fallo_tecnico",
            "es_abstencion",
        ]
    ]
    long = judges.merge(
        keep_categories,
        on=["obs_id", "estrategia", "modelo"],
        how="left",
        validate="many_to_one",
    )
    if long["categoria_final"].isna().any():
        missing = long.loc[long["categoria_final"].isna(), ["obs_id", "estrategia", "modelo"]].drop_duplicates()
        raise SystemExit(f"Observaciones de jueces sin categoría:\n{missing.to_string(index=False)}")

    long["score_principal"] = long.apply(
        lambda r: 0.0 if bool(r["es_no_sustantiva"]) else float(r["score_rubric"]),
        axis=1,
    )
    long["score_observado"] = long["score_rubric"]
    long["score_exclusion"] = long.apply(
        lambda r: pd.NA if bool(r["es_no_sustantiva"]) else float(r["score_rubric"]),
        axis=1,
    )
    long["score_tecnicos_cero"] = long.apply(
        lambda r: 0.0 if bool(r["es_fallo_tecnico"]) else float(r["score_rubric"]),
        axis=1,
    )
    long["score_exclusion"] = pd.to_numeric(long["score_exclusion"], errors="coerce")

    # Agregados por observación.
    agg = (
        long.groupby(["obs_id", "estrategia", "modelo"], as_index=False)
        .agg(
            n_jueces_long=("juez", "nunique"),
            score_principal_prom=("score_principal", "mean"),
            score_principal_median=("score_principal", "median"),
            score_observado_rubric_prom=("score_observado", "mean"),
            score_observado_rubric_median=("score_observado", "median"),
            score_observado_raw_prom=("score_raw", "mean"),
            score_observado_raw_median=("score_raw", "median"),
            score_exclusion_prom=("score_exclusion", "mean"),
            score_exclusion_median=("score_exclusion", "median"),
            score_tecnicos_cero_prom=("score_tecnicos_cero", "mean"),
            score_tecnicos_cero_median=("score_tecnicos_cero", "median"),
            score_principal_sd=("score_principal", "std"),
        )
    )
    if not (agg["n_jueces_long"] == 3).all():
        raise SystemExit("No todas las observaciones tienen tres jueces.")

    wide = wide.merge(
        agg,
        on=["obs_id", "estrategia", "modelo"],
        how="left",
        validate="one_to_one",
    )
    wide["delta_cero_menos_observado"] = wide["score_principal_prom"] - wide["score_observado_rubric_prom"]
    wide["score_observado_raw_prom"] = pd.to_numeric(wide["score_observado_raw_prom"], errors="coerce")

    # Verificaciones de integridad.
    checks = {
        "n_wide": len(wide),
        "n_long": len(long),
        "n_obs_unicas": wide["obs_id"].nunique(),
        "n_casos": wide["caso_id"].nunique(),
        "n_celdas": wide.groupby(["estrategia", "modelo"]).ngroups,
        "n_jueces_unicos": long["juez"].nunique(),
        "n_filas_juez_unicas": len(long.drop_duplicates(["obs_id", "estrategia", "modelo", "juez"])),
        "n_no_sustantivas": int(wide["es_no_sustantiva"].sum()),
        "n_sustantivas": int(wide["es_sustantiva"].sum()),
        "n_medianas_csv_original": int(pd.to_numeric(metrics["respuesta_correcta_avg"], errors="coerce").notna().sum()),
    }
    expected = {
        "n_wide": 711,
        "n_long": 2133,
        "n_obs_unicas": 79,
        "n_casos": 25,
        "n_celdas": 9,
        "n_jueces_unicos": 3,
        "n_filas_juez_unicas": 2133,
    }
    for key, value in expected.items():
        if checks[key] != value:
            raise SystemExit(f"Control fallido {key}: {checks[key]} != {value}")

    # Resumen por celda.
    cell_rows = []
    for (estrategia, modelo), group in wide.groupby(["estrategia", "modelo"], sort=False):
        cell_rows.append(
            {
                "estrategia": estrategia,
                "estrategia_label": ESTRATEGIA_LABEL[estrategia],
                "modelo": modelo,
                "n": len(group),
                "n_sustantiva": int(group["es_sustantiva"].sum()),
                "n_no_sustantiva": int(group["es_no_sustantiva"].sum()),
                "n_vacia": int((group["categoria_final"] == "vacia").sum()),
                "n_solo_espacios": int((group["categoria_final"] == "solo_espacios").sum()),
                "n_abstencion": int((group["categoria_final"] == "abstencion_explicita").sum()),
                "n_error": int((group["categoria_final"] == "error_explicito").sum()),
                "n_truncada": int((group["categoria_final"] == "truncada").sum()),
                "n_indeterminada": int((group["categoria_final"] == "indeterminada").sum()),
                "media_principal": group["score_principal_prom"].mean(),
                "mediana_principal": group["score_principal_prom"].median(),
                "media_observada_rubric": group["score_observado_rubric_prom"].mean(),
                "mediana_observada_rubric": group["score_observado_rubric_prom"].median(),
                "media_observada_raw": group["score_observado_raw_prom"].mean(),
                "mediana_observada_raw": group["score_observado_raw_prom"].median(),
                "media_exclusion": group["score_exclusion_prom"].mean(),
                "mediana_exclusion": group["score_exclusion_prom"].median(),
                "n_exclusion": int(group["score_exclusion_prom"].notna().sum()),
                "prop_ge_075_principal": float((group["score_principal_prom"] >= 0.75).mean()),
                "prop_ge_075_observada": float((group["score_observado_rubric_prom"] >= 0.75).mean()),
            }
        )
    cell_summary = pd.DataFrame(cell_rows)
    cell_summary["_e"] = cell_summary["estrategia"].map({e: i for i, e in enumerate(ESTRATEGIAS)})
    cell_summary["_m"] = cell_summary["modelo"].map({m: i for i, m in enumerate(MODELOS)})
    cell_summary = cell_summary.sort_values(["_e", "_m"]).drop(columns=["_e", "_m"])

    # Comparación con la Tabla 11 del manuscrito.
    compare_rows = []
    for estrategia in ESTRATEGIAS:
        for modelo in MODELOS:
            group = wide[(wide["estrategia"] == estrategia) & (wide["modelo"] == modelo)]
            metrics_cell = metrics[
                (metrics["estrategia"] == estrategia)
                & (metrics["id_modelo_especialista"] == modelo)
            ]
            values_original = pd.to_numeric(metrics_cell["respuesta_correcta_avg"], errors="coerce").dropna()
            compare_rows.append(
                {
                    "estrategia": estrategia,
                    "estrategia_label": ESTRATEGIA_LABEL[estrategia],
                    "modelo": modelo,
                    "mediana_manuscrito_tabla11": MEDIANAS_MANUSCRITO[(estrategia, modelo)],
                    "n_csv_original": int(values_original.notna().sum()),
                    "mediana_csv_original": float(values_original.median()) if len(values_original) else None,
                    "mediana_observada_raw_79": float(group["score_observado_raw_prom"].median()),
                    "mediana_observada_rubric_79": float(group["score_observado_rubric_prom"].median()),
                    "mediana_principal_cero_79": float(group["score_principal_prom"].median()),
                    "mediana_exclusion": float(group["score_exclusion_prom"].median()),
                    "n_exclusion": int(group["score_exclusion_prom"].notna().sum()),
                    "n_no_sustantiva": int(group["es_no_sustantiva"].sum()),
                }
            )
    comparison = pd.DataFrame(compare_rows)

    # Auditoría de las unidades 23-25 y sus 27 medias recuperadas.
    join_audit = wide[wide["q"].isin([23, 24, 25])][
        [
            "q",
            "obs_id",
            "estrategia",
            "modelo",
            "n_jueces_long",
            "score_observado_rubric_prom",
            "score_principal_prom",
            "score_exclusion_prom",
            "categoria_final",
            "respuesta_obtenida",
        ]
    ].copy()
    join_audit["sub_en_fuente"] = ""
    join_audit["sub_en_jueces"] = 0
    join_audit["nota"] = "Unidad única: la fuente usa subpregunta vacía y los jueces usan 0; se normaliza a 00."

    # Manifiesto de entradas.
    inputs = [SOURCE_WIDE, SOURCE_JUDGES, SOURCE_METRICS, TEMPLATE, MAPPING]
    manifest_rows = []
    for path in inputs:
        if path.exists():
            manifest_rows.append(
                {
                    "archivo": str(path.relative_to(BASE)),
                    "sha256": sha256(path),
                    "bytes": path.stat().st_size,
                }
            )
    manifest = pd.DataFrame(manifest_rows)

    # Escritura.
    wide.to_csv(DATOS / "01_wide_711.csv", index=False, encoding="utf-8")
    long.to_csv(DATOS / "02_long_2133.csv", index=False, encoding="utf-8")
    cell_summary.to_csv(DATOS / "03_resumen_celdas.csv", index=False, encoding="utf-8")
    comparison.to_csv(DATOS / "04_comparacion_medianas_manuscrito.csv", index=False, encoding="utf-8")
    join_audit.to_csv(DATOS / "05_auditoria_join_23_25.csv", index=False, encoding="utf-8")
    manifest.to_csv(DATOS / "00_manifiesto_entradas.csv", index=False, encoding="utf-8")
    (DATOS / "00_estado_revision_manual.json").write_text(
        json.dumps(status, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (DATOS / "00_controles_integridad.json").write_text(
        json.dumps(checks, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(json.dumps(checks, indent=2, ensure_ascii=False))
    print(f"\nRevisión manual completa: {status['completa']}")
    print(f"Categorías no sustantivas: {checks['n_no_sustantivas']} de {checks['n_wide']}")
    print(f"Escrito en: {DATOS}")


if __name__ == "__main__":
    main()

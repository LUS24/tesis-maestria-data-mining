"""Diagnóstico reproducible de IX.1.2.

Genera artefactos derivados para diagnosticar la celda Agentic-RAG + gpt-5-nano,
los faltantes y los jueces que puntuaron salidas no sustantivas.

No modifica archivos fuente ni registros históricos. Todas las salidas se
escriben en el directorio de esta corrección.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import re
import statistics
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE = Path(__file__).resolve().parents[3]
EXP = BASE / "codigo_experimentos"
OUT = BASE / "analisis-valoracion-jurado" / "correccion-02-diagnostico-gpt-5-nano"
SALIDAS = OUT / "salidas"
FIGURAS = OUT / "figuras"
REVISION = OUT / "revision_manual"

RESPONSES_PATH = EXP / "part_i" / "responses_text_cleaned.csv"
METRICS_PATH = EXP / "part_i" / "combined_metrics_for_analysis.csv"
JUDGES_PATH = EXP / "part_i" / "final_judge_results.csv"
METADATA_PATH = EXP / "part_i" / "metadata_tokens_cost_cleaned.csv"
BENCHMARK_PATH = BASE / "data" / "evaluation_questions_v20250804_101435.json"
AGENTIC_JSON_PATH = (
    EXP / "part_g" / "llm_responses_agentic_rag_results_with_metrics_and_metadata_FINAL.json"
)
LOGS_PATH = EXP / "part_g" / "chat_data"

ESTRATEGIAS = [
    "llm_responses_no_rag",
    "llm_responses_base_rag",
    "llm_responses_agentic_rag",
]
ESTRATEGIA_CORTA = {
    "llm_responses_no_rag": "sin_rag",
    "llm_responses_base_rag": "rag_basico",
    "llm_responses_agentic_rag": "agentic_rag",
}
ESTRATEGIA_LABEL = {
    "llm_responses_no_rag": "Sin RAG",
    "llm_responses_base_rag": "RAG básico",
    "llm_responses_agentic_rag": "Agentic-RAG",
}
MODELOS = ["gpt-5-nano", "gpt-5-mini", "gpt-5"]
MODELO_LABEL = {
    "gpt-5-nano": "gpt-5-nano",
    "gpt-5-mini": "gpt-5-mini",
    "gpt-5": "gpt-5",
}
RUBRICA = [0.0, 0.25, 0.5, 0.75, 1.0]

CATEGORIAS = [
    "sustantiva",
    "vacia",
    "solo_espacios",
    "abstencion_explicita",
    "error_explicito",
    "truncada",
    "indeterminada",
]
CATEGORIAS_NO_SUSTANTIVAS = [c for c in CATEGORIAS if c != "sustantiva"]
CATEGORIAS_TECNICAS = ["vacia", "solo_espacios", "error_explicito", "truncada", "indeterminada"]

CATEGORIA_LABEL = {
    "sustantiva": "Sustantiva",
    "vacia": "Vacía",
    "solo_espacios": "Solo espacios",
    "abstencion_explicita": "Abstención explícita",
    "error_explicito": "Error explícito",
    "truncada": "Truncada",
    "indeterminada": "Indeterminada",
}

COLORES = {
    "sustantiva": "#0072B2",
    "vacia": "#D55E00",
    "solo_espacios": "#E69F00",
    "abstencion_explicita": "#CC79A7",
    "error_explicito": "#000000",
    "truncada": "#F0E442",
    "indeterminada": "#999999",
}

# Valores publicados en la Tabla 11 del manuscrito (medianas de
# respuesta_correcta_avg). Se usan solo para comparar el efecto del join.
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

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------


def sha256(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canon_sub(value: Any) -> int:
    """Normaliza None/vacío/'0' a 0 para unir las unidades 23, 24 y 25."""
    if value is None:
        return 0
    s = str(value).strip()
    if s in {"", "None", "nan", "NaN", "NA", "N/A"}:
        return 0
    return int(float(s))


def obs_id(q: Any, sub: Any) -> str:
    return f"Q{int(q):02d}_{canon_sub(sub):02d}"


def norm_text(value: Any) -> str:
    if value is None:
        return ""
    text = unicodedata.normalize("NFKC", str(value))
    text = text.replace("\u00a0", " ")
    return re.sub(r"\s+", " ", text).strip()


def rubric_map(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    try:
        x = float(value)
    except (TypeError, ValueError):
        return None
    distances = [abs(x - r) for r in RUBRICA]
    minimum = min(distances)
    return max(r for r, d in zip(RUBRICA, distances) if d == minimum)


def wilson_ci(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float, float]:
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt((p * (1 - p) / n) + (z * z / (4 * n * n))) / denom
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "—"
    try:
        if isinstance(value, float) and math.isnan(value):
            return "—"
    except TypeError:
        pass
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    return f"{float(value):.{digits}f}"


def safe_mean(values: list[float]) -> float | None:
    clean = [float(v) for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
    return statistics.fmean(clean) if clean else None


def safe_median(values: list[float]) -> float | None:
    clean = [float(v) for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
    return statistics.median(clean) if clean else None


def safe_iqr(values: list[float]) -> tuple[float | None, float | None]:
    clean = [float(v) for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
    if len(clean) < 4:
        return (None, None)
    q1, q3 = np.percentile(clean, [25, 75])
    return (float(q1), float(q3))


def first_nonempty(values: list[Any]) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


# ---------------------------------------------------------------------------
# Clasificación de respuestas
# ---------------------------------------------------------------------------


def classify_response(raw: Any) -> dict[str, Any]:
    """Clasifica una respuesta en una categoría principal y una subcategoría.

    La categoría principal sigue la lista acordada en IX.1.2. La subcategoría
    conserva la evidencia fina (marcador de prueba, mensaje de proceso, etc.).
    """
    raw_str = "" if raw is None else str(raw)
    s = norm_text(raw_str)
    low = s.lower()

    result: dict[str, Any] = {
        "categoria": "sustantiva",
        "subcategoria": "respuesta_valida",
        "evidencia": s[:240],
        "menciona_limitacion": bool(
            re.search(
                r"(no dispongo|no cuento con|no tengo (la |el )?(información|texto|normativa|artículos)|"
                r"no puedo (responder|contestar|proporcionar|brindar|determinar|afirmar)|"
                r"no lo s[eé]|sin (la )?información|no es posible (responder|determinar)|"
                r"no hay suficiente información|necesito que (me )?(adjunte|proporcione|indique)|lamento)",
                low,
            )
        ),
        "cita_articulo": bool(re.search(r"art[ií]culo|art\.?\s*\d|\barts?\.?\b", low)),
    }

    if raw_str == "":
        result.update(categoria="vacia", subcategoria="texto_original_vacio", evidencia="<cadena vacía>")
        return result
    if s == "":
        result.update(categoria="solo_espacios", subcategoria="texto_solo_espacios", evidencia="<solo espacios>")
        return result

    if low in {"test", "placeholder", "pending", "todo", "tbd", "n/a", "na"}:
        result.update(categoria="indeterminada", subcategoria="marcador_de_prueba")
        return result
    if low == "{":
        result.update(categoria="truncada", subcategoria="json_incompleto")
        return result

    if re.match(r"^\[(se solicita|se procede|se realiza|se ejecut|se inicia|se consulta|se busca)", low):
        result.update(categoria="indeterminada", subcategoria="mensaje_de_proceso")
        return result
    if re.match(r"^\((se ejecut|se realiz|se consult|se busc)", low):
        result.update(categoria="indeterminada", subcategoria="mensaje_de_proceso")
        return result
    if re.match(
        r"^(por favor[ ,]+)?(espera|espere|aguarde|aguard[ae]|voy a|vamos a|procedo a|procedemos a|"
        r"se procede a|se solicita al usuario|i will|i’ll|i am going to|consulting|retrieving|"
        r"buscando|consultando|analizando|un momento)",
        low,
    ) and len(s) < 260:
        result.update(categoria="indeterminada", subcategoria="mensaje_de_proceso")
        return result
    if re.search(r"(preliminar|no debe aparecer|borrador|draft)", low) and len(s) < 220:
        result.update(categoria="indeterminada", subcategoria="mensaje_interno")
        return result

    if re.search(
        r"(traceback|exception|rate limit|timeout|timed out|internal server error|bad gateway|"
        r"service unavailable|invalid request|api error|connection reset|failed to|"
        r"unexpected error|http\s*[45]\d\d)",
        low,
    ):
        result.update(categoria="error_explicito", subcategoria="error_tecnico")
        return result

    first = low[:300]
    refusal = bool(
        re.search(
            r"(no puedo (responder|contestar|proporcionar|brindar|determinar|afirmar)|no dispongo|"
            r"no cuento con|no tengo (la |el )?(información|texto|normativa|artículos)|no lo s[eé]|"
            r"sin (la )?información|no es posible (responder|determinar)|no hay suficiente información|"
            r"necesito que (me )?(adjunte|proporcione|indique)|lamento)",
            first,
        )
    )
    has_cite = result["cita_articulo"]
    if refusal and (len(s) < 700 or not has_cite):
        result.update(categoria="abstencion_explicita", subcategoria="rechazo_por_falta_de_contexto")
        return result

    if s in {"{", "["} or (s.endswith("...") and len(s) < 300):
        result.update(categoria="truncada", subcategoria="truncamiento_detectado")
        return result

    if len(s) < 25 and not re.search(r"\b(s[ií]|no|correcto|incorrecto|procede|improcedente)\b", low):
        result.update(categoria="indeterminada", subcategoria="texto_muy_corto")
        return result

    return result


# ---------------------------------------------------------------------------
# Carga y parseo de logs
# ---------------------------------------------------------------------------


def read_csv_keep_strings(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8")


def parse_json_maybe(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str):
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def extract_final_result_texts(messages: list[dict[str, Any]]) -> list[str]:
    texts: list[str] = []
    for message in messages:
        for part in message.get("parts") or []:
            if part.get("part_kind") == "tool-call" and part.get("tool_name") == "final_result":
                args = parse_json_maybe(part.get("args"))
                if isinstance(args, dict) and "response_text" in args:
                    value = args.get("response_text")
                    texts.append("" if value is None else str(value))
                else:
                    texts.append("")
    return texts


def extract_selected_documents_counts(messages: list[dict[str, Any]]) -> list[int]:
    counts: list[int] = []
    for message in messages:
        for part in message.get("parts") or []:
            if part.get("part_kind") == "tool-return" and part.get("tool_name") == "retrieve_relevant_documents":
                content = parse_json_maybe(part.get("content"))
                if isinstance(content, dict) and isinstance(content.get("selected_documents"), list):
                    counts.append(len(content["selected_documents"]))
    return counts


def parse_agent_logs() -> pd.DataFrame:
    records: list[dict[str, Any]] = []
    if not LOGS_PATH.exists():
        return pd.DataFrame(records)

    for model_dir in sorted(p for p in LOGS_PATH.iterdir() if p.is_dir()):
        model_name = model_dir.name.replace("openai_", "").replace("_", "-")
        if model_name not in MODELOS:
            continue
        for case_dir in sorted(p for p in model_dir.iterdir() if p.is_dir()):
            match = re.match(r"^(\d{2})_(\d{2})$", case_dir.name)
            if not match:
                continue
            q, sub = int(match.group(1)), int(match.group(2))
            law_path = case_dir / "law_specialist_agent.json"
            retrieval_path = case_dir / "retrieval_agent.json"
            if not law_path.exists():
                continue

            law = json.loads(law_path.read_text(encoding="utf-8"))
            retrieval = json.loads(retrieval_path.read_text(encoding="utf-8")) if retrieval_path.exists() else {}
            law_messages = law.get("messages") or []
            retrieval_messages = retrieval.get("messages") or []

            final_texts = extract_final_result_texts(law_messages)
            selected_counts = extract_selected_documents_counts(law_messages)
            law_tool_calls = [
                part.get("tool_name")
                for message in law_messages
                for part in (message.get("parts") or [])
                if part.get("part_kind") == "tool-call"
            ]
            retrieval_tool_calls = [
                part.get("tool_name")
                for message in retrieval_messages
                for part in (message.get("parts") or [])
                if part.get("part_kind") == "tool-call"
            ]
            law_finish = [m.get("finish_reason") for m in law_messages if m.get("finish_reason")]
            retrieval_finish = [m.get("finish_reason") for m in retrieval_messages if m.get("finish_reason")]

            history_dir = case_dir / "retrieval_history"
            history_files = sorted(history_dir.glob("*.json")) if history_dir.exists() else []
            history_queries: list[str] = []
            history_docs: list[int] = []
            for history_file in history_files:
                try:
                    item = json.loads(history_file.read_text(encoding="utf-8"))
                    history_queries.append(str(item.get("query", "")))
                    history_docs.append(len(item.get("retrieved_documents") or []))
                except (json.JSONDecodeError, OSError):
                    continue

            law_meta = law.get("metadata") or {}
            retrieval_meta = retrieval.get("metadata") or {}
            law_tokens = (law_meta.get("usage") or {}).get("tokens") or {}
            retrieval_tokens = (retrieval_meta.get("usage") or {}).get("tokens") or {}
            law_cost = (law_meta.get("usage") or {}).get("cost") or {}
            retrieval_cost = (retrieval_meta.get("usage") or {}).get("cost") or {}

            records.append(
                {
                    "obs_id": obs_id(q, sub),
                    "q": q,
                    "sub": sub,
                    "modelo": model_name,
                    "law_log_path": str(law_path.relative_to(BASE)),
                    "retrieval_log_path": str(retrieval_path.relative_to(BASE)) if retrieval_path.exists() else None,
                    "law_message_count": len(law_messages),
                    "retrieval_message_count": len(retrieval_messages),
                    "law_final_result_count": len(final_texts),
                    "law_final_text_first": final_texts[0] if final_texts else None,
                    "law_final_text_last": final_texts[-1] if final_texts else None,
                    "law_final_texts_json": json.dumps(final_texts, ensure_ascii=False),
                    "law_selected_docs_counts_json": json.dumps(selected_counts, ensure_ascii=False),
                    "law_selected_docs_first": selected_counts[0] if selected_counts else None,
                    "law_selected_docs_max": max(selected_counts) if selected_counts else None,
                    "law_tool_calls_json": json.dumps(law_tool_calls, ensure_ascii=False),
                    "retrieval_tool_calls_json": json.dumps(retrieval_tool_calls, ensure_ascii=False),
                    "law_finish_reasons_json": json.dumps(law_finish, ensure_ascii=False),
                    "retrieval_finish_reasons_json": json.dumps(retrieval_finish, ensure_ascii=False),
                    "retrieval_history_count": len(history_files),
                    "retrieval_history_queries_json": json.dumps(history_queries, ensure_ascii=False),
                    "retrieval_history_docs_json": json.dumps(history_docs, ensure_ascii=False),
                    "law_model_version": law_meta.get("model_version"),
                    "retrieval_model_version": retrieval_meta.get("model_version"),
                    "law_input_tokens": law_tokens.get("input_tokens"),
                    "law_output_tokens": law_tokens.get("output_tokens"),
                    "law_reasoning_tokens": (law_tokens.get("tokens_details") or {}).get("reasoning_tokens"),
                    "retrieval_input_tokens": retrieval_tokens.get("input_tokens"),
                    "retrieval_output_tokens": retrieval_tokens.get("output_tokens"),
                    "retrieval_reasoning_tokens": (retrieval_tokens.get("tokens_details") or {}).get("reasoning_tokens"),
                    "law_total_price": law_cost.get("total_price"),
                    "retrieval_total_price": retrieval_cost.get("total_price"),
                }
            )

    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Construcción del dataset analítico
# ---------------------------------------------------------------------------


def build_dataset() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    responses = read_csv_keep_strings(RESPONSES_PATH)
    metrics = read_csv_keep_strings(METRICS_PATH)
    judges = read_csv_keep_strings(JUDGES_PATH)
    metadata = read_csv_keep_strings(METADATA_PATH)
    logs = parse_agent_logs()

    for df in (responses, metrics, metadata):
        df["q"] = df["nro_pregunta"].astype(int)
        df["sub"] = df["nro_subpregunta"].map(canon_sub)
        df["obs_id"] = [obs_id(q, s) for q, s in zip(df["q"], df["sub"])]
    judges["q"] = judges["numero_pregunta"].astype(int)
    judges["sub"] = judges["numero_subpregunta"].map(canon_sub)
    judges["obs_id"] = [obs_id(q, s) for q, s in zip(judges["q"], judges["sub"])]

    # Agregación de jueces: promedio crudo y promedio mapeado a la rúbrica.
    judge_rows: list[dict[str, Any]] = []
    for key, group in judges.groupby(["q", "sub", "sistema", "modelo_respuesta"], sort=False):
        q, sub, sistema, modelo = key
        correctness_raw = [float(x) for x in group["score_respuesta_correcta"] if x != ""]
        legal_raw = [float(x) for x in group["score_precision_legal"] if x != ""]
        correctness_rubric = [rubric_map(x) for x in correctness_raw]
        legal_rubric = [rubric_map(x) for x in legal_raw]
        judge_rows.append(
            {
                "q": int(q),
                "sub": int(sub),
                "obs_id": obs_id(q, sub),
                "estrategia": sistema,
                "modelo": modelo,
                "n_jueces": len(group),
                "jueces": "|".join(sorted(group["modelo_juez"].unique())),
                "respuesta_correcta_raw": safe_mean(correctness_raw),
                "respuesta_correcta_rubric": safe_mean(correctness_rubric),
                "respuesta_correcta_std_rubric": (
                    float(np.std(correctness_rubric, ddof=1)) if len(correctness_rubric) > 1 else None
                ),
                "respuesta_correcta_scores_json": json.dumps(correctness_raw, ensure_ascii=False),
                "precision_legal_raw": safe_mean(legal_raw),
                "precision_legal_rubric": safe_mean(legal_rubric),
                "precision_legal_scores_json": json.dumps(legal_raw, ensure_ascii=False),
            }
        )
    judge_agg = pd.DataFrame(judge_rows)

    # Evitar columnas duplicadas al unir.
    metrics_cols = [
        "obs_id",
        "estrategia",
        "id_modelo_especialista",
        "token_f1",
        "rouge_l",
        "sbert_similarity_spanish",
        "bertscore",
        "length_ratio",
        "word_count_ratio",
        "exact_match",
        "jaccard_similarity",
        "levenshtein_similarity",
        "character_error_rate",
        "bleu",
        "rouge_1",
        "rouge_2",
        "sbert_similarity_multilingual",
        "respuesta_correcta_avg",
        "precision_legal_avg",
        "respuesta_correcta_std",
        "precision_legal_std",
    ]
    metrics_small = metrics[metrics_cols].rename(columns={"id_modelo_especialista": "modelo"})
    metadata_cols = [
        "obs_id",
        "estrategia",
        "id_modelo_especialista",
        "model_version",
        "input_tokens",
        "output_tokens",
        "reasoning_tokens",
        "total_price",
        "retrieval_total_price",
    ]
    metadata_small = metadata[metadata_cols].rename(columns={"id_modelo_especialista": "modelo"})

    data = responses.rename(columns={"id_modelo_especialista": "modelo"}).copy()
    data = data.merge(metrics_small, on=["obs_id", "estrategia", "modelo"], how="left", validate="one_to_one")
    data = data.merge(metadata_small, on=["obs_id", "estrategia", "modelo"], how="left", validate="one_to_one")
    data = data.merge(
        judge_agg,
        on=["obs_id", "estrategia", "modelo"],
        how="left",
        validate="one_to_one",
        suffixes=("", "_juez"),
    )

    # Clasificación y banderas.
    classified = data["respuesta_obtenida"].map(classify_response).apply(pd.Series)
    data = pd.concat([data, classified], axis=1)
    data["es_no_sustantiva"] = data["categoria"] != "sustantiva"
    data["es_fallo_tecnico"] = data["categoria"].isin(CATEGORIAS_TECNICAS)
    data["longitud_caracteres"] = data["respuesta_obtenida"].map(lambda x: len(norm_text(x)))
    data["longitud_palabras"] = data["respuesta_obtenida"].map(lambda x: len(norm_text(x).split()))

    # Logs: solo hay logs para Agentic-RAG.
    log_cols = [
        "obs_id",
        "modelo",
        "law_message_count",
        "retrieval_message_count",
        "law_final_result_count",
        "law_final_text_first",
        "law_final_text_last",
        "law_final_texts_json",
        "law_selected_docs_counts_json",
        "law_selected_docs_first",
        "law_selected_docs_max",
        "law_tool_calls_json",
        "retrieval_tool_calls_json",
        "law_finish_reasons_json",
        "retrieval_finish_reasons_json",
        "retrieval_history_count",
        "retrieval_history_queries_json",
        "retrieval_history_docs_json",
        "law_model_version",
        "retrieval_model_version",
        "law_input_tokens",
        "law_output_tokens",
        "law_reasoning_tokens",
        "retrieval_input_tokens",
        "retrieval_output_tokens",
        "retrieval_reasoning_tokens",
        "law_total_price",
        "retrieval_total_price",
    ]
    logs_small = logs[log_cols].copy().rename(
        columns={
            "law_total_price": "log_law_total_price",
            "retrieval_total_price": "log_retrieval_total_price",
        }
    )
    logs_small["estrategia"] = "llm_responses_agentic_rag"
    data = data.merge(
        logs_small,
        on=["obs_id", "estrategia", "modelo"],
        how="left",
        validate="one_to_one",
    )

    # Comparación entre el texto registrado y el final_result del log.
    def log_matches(row: pd.Series) -> Any:
        if row["estrategia"] != "llm_responses_agentic_rag" or not isinstance(row.get("law_final_text_first"), str):
            return None
        return norm_text(row["law_final_text_first"]) == norm_text(row["respuesta_obtenida"])

    data["log_texto_coincide"] = data.apply(log_matches, axis=1)

    # Escenarios de puntuación.
    original = pd.to_numeric(data["respuesta_correcta_rubric"], errors="coerce")
    original_raw = pd.to_numeric(data["respuesta_correcta_raw"], errors="coerce")
    data["puntaje_original_rubric"] = original
    data["puntaje_original_raw"] = original_raw
    data["puntaje_fallo_cero"] = np.where(data["es_no_sustantiva"], 0.0, original)
    data["puntaje_solo_fallos_tecnicos_cero"] = np.where(data["es_fallo_tecnico"], 0.0, original)
    data["puntaje_exclusion"] = np.where(data["es_no_sustantiva"], np.nan, original)

    # Auditoría de jueces sobre salidas no sustantivas.
    data["juez_no_cero_en_no_sustantiva"] = False
    data["juez_max_en_no_sustantiva"] = np.nan
    for idx, row in data[data["es_no_sustantiva"]].iterrows():
        scores = json.loads(row["respuesta_correcta_scores_json"]) if isinstance(row["respuesta_correcta_scores_json"], str) else []
        data.at[idx, "juez_no_cero_en_no_sustantiva"] = any(float(s) > 0 for s in scores)
        data.at[idx, "juez_max_en_no_sustantiva"] = max(scores) if scores else np.nan

    data["costo_total"] = (
        pd.to_numeric(data["total_price"], errors="coerce").fillna(0)
        + pd.to_numeric(data["retrieval_total_price"], errors="coerce").fillna(0)
    )

    sorted_data = data.sort_values(["q", "sub", "estrategia", "modelo"]).reset_index(drop=True)
    sorted_data["estrategia_corta"] = sorted_data["estrategia"].map(ESTRATEGIA_CORTA)
    sorted_data["categoria_label"] = sorted_data["categoria"].map(CATEGORIA_LABEL)
    return sorted_data, responses, metrics, judges, logs


# ---------------------------------------------------------------------------
# Tablas
# ---------------------------------------------------------------------------


def sort_cells(df: pd.DataFrame) -> pd.DataFrame:
    """Ordena celdas según el orden editorial de estrategias y modelos."""
    result = df.copy()
    result["_orden_estrategia"] = result["estrategia"].map({e: i for i, e in enumerate(ESTRATEGIAS)})
    result["_orden_modelo"] = result["modelo"].map({m: i for i, m in enumerate(MODELOS)})
    return result.sort_values(["_orden_estrategia", "_orden_modelo"]).drop(
        columns=["_orden_estrategia", "_orden_modelo"]
    ).reset_index(drop=True)


def summarize_cells(data: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (estrategia, modelo), group in data.groupby(["estrategia", "modelo"], sort=False):
        n = len(group)
        counts = Counter(group["categoria"])
        n_no = n - counts.get("sustantiva", 0)
        tasa, ic_inf, ic_sup = wilson_ci(n_no, n)
        blank = counts.get("vacia", 0) + counts.get("solo_espacios", 0)
        blank_rate, blank_inf, blank_sup = wilson_ci(blank, n)
        original = group["puntaje_original_rubric"].dropna().tolist()
        fallo = group["puntaje_fallo_cero"].dropna().tolist()
        tecnico = group["puntaje_solo_fallos_tecnicos_cero"].dropna().tolist()
        exclusion = group["puntaje_exclusion"].dropna().tolist()
        q1, q3 = safe_iqr(original)
        row = {
            "estrategia": estrategia,
            "estrategia_corta": ESTRATEGIA_CORTA[estrategia],
            "modelo": modelo,
            "n_total": n,
            "n_sustantiva": counts.get("sustantiva", 0),
            "n_no_sustantiva": n_no,
            "n_vacia": counts.get("vacia", 0),
            "n_solo_espacios": counts.get("solo_espacios", 0),
            "n_abstencion_explicita": counts.get("abstencion_explicita", 0),
            "n_error_explicito": counts.get("error_explicito", 0),
            "n_truncada": counts.get("truncada", 0),
            "n_indeterminada": counts.get("indeterminada", 0),
            "tasa_no_sustantiva": tasa,
            "tasa_no_sustantiva_ic95_inf": ic_inf,
            "tasa_no_sustantiva_ic95_sup": ic_sup,
            "tasa_blanco": blank_rate,
            "tasa_blanco_ic95_inf": blank_inf,
            "tasa_blanco_ic95_sup": blank_sup,
            "n_exclusion": len(exclusion),
            "media_original": safe_mean(original),
            "mediana_original": safe_median(original),
            "q1_original": q1,
            "q3_original": q3,
            "media_fallo_cero": safe_mean(fallo),
            "mediana_fallo_cero": safe_median(fallo),
            "media_solo_fallos_tecnicos_cero": safe_mean(tecnico),
            "mediana_solo_fallos_tecnicos_cero": safe_median(tecnico),
            "media_exclusion": safe_mean(exclusion),
            "mediana_exclusion": safe_median(exclusion),
            "n_juez_no_cero_en_no_sustantiva": int(group["juez_no_cero_en_no_sustantiva"].sum()),
            "media_longitud": safe_mean(group["longitud_caracteres"].tolist()),
            "mediana_longitud": safe_median(group["longitud_caracteres"].tolist()),
            "media_output_tokens": safe_mean(pd.to_numeric(group["output_tokens"], errors="coerce").dropna().tolist()),
            "mediana_output_tokens": safe_median(pd.to_numeric(group["output_tokens"], errors="coerce").dropna().tolist()),
            "media_reasoning_tokens": safe_mean(pd.to_numeric(group["reasoning_tokens"], errors="coerce").dropna().tolist()),
            "media_costo_total": safe_mean(group["costo_total"].tolist()),
            "costo_total_celda": float(group["costo_total"].sum()),
            "n_logs": int(group["law_final_result_count"].notna().sum()),
        }
        rows.append(row)
    return sort_cells(pd.DataFrame(rows))


def summarize_categories(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (estrategia, modelo), group in data.groupby(["estrategia", "modelo"], sort=False):
        n = len(group)
        counts = Counter(group["categoria"])
        for categoria in CATEGORIAS:
            rows.append(
                {
                    "estrategia": estrategia,
                    "estrategia_corta": ESTRATEGIA_CORTA[estrategia],
                    "modelo": modelo,
                    "categoria": categoria,
                    "n": counts.get(categoria, 0),
                    "proporcion": counts.get(categoria, 0) / n if n else None,
                }
            )
    return sort_cells(pd.DataFrame(rows))


def build_join_audit(data: pd.DataFrame, judges: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for q in [23, 24, 25]:
        for estrategia in ESTRATEGIAS:
            for modelo in MODELOS:
                metric_row = data[
                    (data["q"] == q)
                    & (data["estrategia"] == estrategia)
                    & (data["modelo"] == modelo)
                ]
                judge_group = judges[
                    (judges["q"] == q)
                    & (judges["sistema"] == estrategia)
                    & (judges["modelo_respuesta"] == modelo)
                ]
                if metric_row.empty:
                    continue
                row = metric_row.iloc[0]
                rows.append(
                    {
                        "q": q,
                        "obs_id": obs_id(q, 0),
                        "sub_en_metrics": "<vacío>" if str(row["nro_subpregunta"]).strip() == "" else row["nro_subpregunta"],
                        "sub_en_judges": int(judge_group["numero_subpregunta"].iloc[0]) if not judge_group.empty else None,
                        "estrategia": estrategia,
                        "modelo": modelo,
                        "n_filas_juez": len(judge_group),
                        "jueces": "|".join(sorted(judge_group["modelo_juez"].unique())) if not judge_group.empty else "",
                        "puntaje_juez_rubric_recalculado": safe_mean(
                            [rubric_map(x) for x in pd.to_numeric(judge_group["score_respuesta_correcta"], errors="coerce").dropna().tolist()]
                        ),
                        "respuesta_correcta_avg_csv_original": pd.to_numeric(
                            row["respuesta_correcta_avg"], errors="coerce"
                        ),
                        "respuesta_correcta_rubric_fix": row["puntaje_original_rubric"],
                        "texto_respuesta": row["respuesta_obtenida"],
                        "diagnostico": "El join falla porque el CSV de métricas usa subpregunta vacía y el de jueces usa 0.",
                    }
                )
    return pd.DataFrame(rows)


def build_judge_audit(data: pd.DataFrame, judges: pd.DataFrame) -> pd.DataFrame:
    extra_cols = [c for c in ["fuente_categoria", "revision_manual_id"] if c in data.columns]
    non_sub = data[data["es_no_sustantiva"]][
        ["obs_id", "q", "sub", "estrategia", "modelo", "categoria", "subcategoria", "respuesta_obtenida"]
        + extra_cols
    ].copy()
    merged = judges.merge(
        non_sub,
        left_on=["obs_id", "q", "sub", "sistema", "modelo_respuesta"],
        right_on=["obs_id", "q", "sub", "estrategia", "modelo"],
        how="inner",
        suffixes=("", "_obs"),
        validate="many_to_one",
    )
    merged = merged.rename(columns={"sistema": "estrategia_juez", "modelo_respuesta": "modelo_juez_respuesta"})
    merged = merged[merged["estrategia_juez"] == merged["estrategia"]]
    merged = merged[merged["modelo_juez_respuesta"] == merged["modelo"]]
    merged["score_correcta_num"] = pd.to_numeric(merged["score_respuesta_correcta"], errors="coerce")
    merged["score_legal_num"] = pd.to_numeric(merged["score_precision_legal"], errors="coerce")
    merged["puntaje_correcta_no_cero"] = merged["score_correcta_num"] > 0
    merged["puntaje_legal_no_cero"] = merged["score_legal_num"] > 0
    merged["justificacion_menciona_articulo"] = merged["reason_respuesta_correcta"].map(
        lambda x: bool(re.search(r"art[ií]culo|art\.?\s*\d", str(x), re.I))
    )
    merged["observacion_celda"] = (
        merged["obs_id"] + "|" + merged["estrategia"] + "|" + merged["modelo"]
    )
    return merged.sort_values(["q", "sub", "modelo_juez"]).reset_index(drop=True)


def format_finish_pattern(pattern: str) -> str:
    try:
        parsed = json.loads(pattern)
        if isinstance(parsed, list):
            return " → ".join(str(x) for x in parsed)
    except (json.JSONDecodeError, TypeError):
        pass
    return str(pattern)


def summarize_finish_patterns(values: pd.Series) -> str:
    counts = Counter(values)
    return "; ".join(
        f"{format_finish_pattern(pattern)} ({n})" for pattern, n in counts.most_common()
    )


def build_logs_summary(logs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for modelo, group in logs.groupby("modelo", sort=False):
        final_texts = group["law_final_text_first"].fillna("").map(norm_text)
        rows.append(
            {
                "modelo": modelo,
                "n": len(group),
                "n_final_texto_vacio": int((final_texts == "").sum()),
                "n_final_texto_no_vacio": int((final_texts != "").sum()),
                "n_final_result_count_1": int((group["law_final_result_count"] == 1).sum()),
                "n_final_result_count_mayor_1": int((group["law_final_result_count"] > 1).sum()),
                "law_finish_reasons": summarize_finish_patterns(group["law_finish_reasons_json"]),
                "retrieval_finish_reasons": summarize_finish_patterns(group["retrieval_finish_reasons_json"]),
                "hist_count_min": int(group["retrieval_history_count"].min()),
                "hist_count_mediana": float(group["retrieval_history_count"].median()),
                "hist_count_max": int(group["retrieval_history_count"].max()),
                "selected_docs_min": float(pd.to_numeric(group["law_selected_docs_first"], errors="coerce").min()),
                "selected_docs_mediana": float(pd.to_numeric(group["law_selected_docs_first"], errors="coerce").median()),
                "selected_docs_max": float(pd.to_numeric(group["law_selected_docs_first"], errors="coerce").max()),
                "law_output_tokens_mediana": float(pd.to_numeric(group["law_output_tokens"], errors="coerce").median()),
                "law_output_tokens_min": float(pd.to_numeric(group["law_output_tokens"], errors="coerce").min()),
                "law_output_tokens_max": float(pd.to_numeric(group["law_output_tokens"], errors="coerce").max()),
                "law_reasoning_tokens_mediana": float(pd.to_numeric(group["law_reasoning_tokens"], errors="coerce").median()),
            }
        )
    result = pd.DataFrame(rows)
    result["_orden"] = result["modelo"].map({m: i for i, m in enumerate(MODELOS)})
    return result.sort_values("_orden").drop(columns="_orden").reset_index(drop=True)


def build_manuscript_comparison(data: pd.DataFrame, original_metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for estrategia in ESTRATEGIAS:
        for modelo in MODELOS:
            group = data[(data["estrategia"] == estrategia) & (data["modelo"] == modelo)]
            orig_csv = original_metrics[
                (original_metrics["estrategia"] == estrategia)
                & (original_metrics["id_modelo_especialista"] == modelo)
            ]
            values_76 = pd.to_numeric(orig_csv["respuesta_correcta_avg"], errors="coerce").dropna().tolist()
            rows.append(
                {
                    "estrategia": estrategia,
                    "estrategia_corta": ESTRATEGIA_CORTA[estrategia],
                    "modelo": modelo,
                    "mediana_manuscrito_tabla11": MEDIANAS_MANUSCRITO.get((estrategia, modelo)),
                    "n_csv_original": len(values_76),
                    "mediana_csv_original": safe_median(values_76),
                    "mediana_corregida_79_jueces_original": safe_median(group["puntaje_original_rubric"].dropna().tolist()),
                    "mediana_fallo_cero": safe_median(group["puntaje_fallo_cero"].dropna().tolist()),
                    "mediana_solo_fallos_tecnicos_cero": safe_median(
                        group["puntaje_solo_fallos_tecnicos_cero"].dropna().tolist()
                    ),
                    "mediana_exclusion": safe_median(group["puntaje_exclusion"].dropna().tolist()),
                    "n_exclusion": int(group["puntaje_exclusion"].notna().sum()),
                    "n_no_sustantiva": int(group["es_no_sustantiva"].sum()),
                }
            )
    return pd.DataFrame(rows)


def paired_wilcoxon(a: list[float], b: list[float]) -> tuple[int, float | None, float | None, float | None]:
    pairs = [(x, y) for x, y in zip(a, b) if not (pd.isna(x) or pd.isna(y))]
    if len(pairs) < 2:
        return (len(pairs), None, None, None)
    diffs = [x - y for x, y in pairs]
    if all(abs(d) < 1e-12 for d in diffs):
        return (len(pairs), 0.0, 0.0, 1.0)
    try:
        result = stats.wilcoxon(
            [x for x, _ in pairs],
            [y for _, y in pairs],
            zero_method="wilcox",
            alternative="two-sided",
            method="auto",
        )
        return (len(pairs), safe_mean(diffs), safe_median(diffs), float(result.pvalue))
    except ValueError:
        return (len(pairs), safe_mean(diffs), safe_median(diffs), None)


def build_sensitivity(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    pairs = [
        ("llm_responses_agentic_rag", "llm_responses_base_rag"),
        ("llm_responses_agentic_rag", "llm_responses_no_rag"),
        ("llm_responses_base_rag", "llm_responses_no_rag"),
    ]
    scenarios = [
        ("original", "puntaje_original_rubric"),
        ("fallo_cero", "puntaje_fallo_cero"),
        ("solo_fallos_tecnicos_cero", "puntaje_solo_fallos_tecnicos_cero"),
        ("exclusion", "puntaje_exclusion"),
    ]
    for modelo in MODELOS:
        for e1, e2 in pairs:
            for scenario, column in scenarios:
                a = data[(data["estrategia"] == e1) & (data["modelo"] == modelo)].set_index("obs_id")[column]
                b = data[(data["estrategia"] == e2) & (data["modelo"] == modelo)].set_index("obs_id")[column]
                common = a.index.intersection(b.index)
                a2 = a.loc[common].tolist()
                b2 = b.loc[common].tolist()
                n, mean_diff, median_diff, p_value = paired_wilcoxon(a2, b2)
                rows.append(
                    {
                        "modelo": modelo,
                        "estrategia_1": e1,
                        "estrategia_2": e2,
                        "escenario": scenario,
                        "n_pares": n,
                        "media_diferencia": mean_diff,
                        "mediana_diferencia": median_diff,
                        "p_wilcoxon_exploratorio": p_value,
                        "nota": (
                            "exclusion usa solo unidades con respuesta sustantiva en ambas estrategias; "
                            "esta selección no es aleatoria y no reemplaza el modelo ordinal de IX.1.1"
                            if scenario == "exclusion"
                            else "diferencia = estrategia_1 - estrategia_2; p sin corrección, solo exploratorio"
                        ),
                    }
                )
    return pd.DataFrame(rows)


def build_no_rag_descriptive(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for modelo in ["gpt-5-nano", "gpt-5-mini"]:
        group = data[(data["estrategia"] == "llm_responses_no_rag") & (data["modelo"] == modelo)]
        original = group["puntaje_original_rubric"].dropna().tolist()
        substantive = group[group["categoria"] == "sustantiva"]["puntaje_original_rubric"].dropna().tolist()
        counts = Counter(group["categoria"])
        q1, q3 = safe_iqr(original)
        rows.append(
            {
                "modelo": modelo,
                "n": len(group),
                "n_sustantiva": counts.get("sustantiva", 0),
                "n_abstencion_explicita": counts.get("abstencion_explicita", 0),
                "n_otras_no_sustantivas": len(group) - counts.get("sustantiva", 0) - counts.get("abstencion_explicita", 0),
                "media_original": safe_mean(original),
                "mediana_original": safe_median(original),
                "q1_original": q1,
                "q3_original": q3,
                "media_solo_sustantivas": safe_mean(substantive),
                "mediana_solo_sustantivas": safe_median(substantive),
                "proporcion_score_ge_075": (
                    sum(1 for x in original if x >= 0.75) / len(original) if original else None
                ),
                "mediana_longitud": safe_median(group["longitud_caracteres"].tolist()),
                "proporcion_menciona_articulo": (
                    float(group["cita_articulo"].sum() / len(group)) if len(group) else None
                ),
                "proporcion_menciona_limitacion": (
                    float(group["menciona_limitacion"].sum() / len(group)) if len(group) else None
                ),
                "mediana_reasoning_tokens": safe_median(
                    pd.to_numeric(group["reasoning_tokens"], errors="coerce").dropna().tolist()
                ),
            }
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------


def save_figure(fig: plt.Figure, stem: str) -> None:
    fig.savefig(FIGURAS / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(FIGURAS / f"{stem}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)


def cell_label(estrategia: str, modelo: str) -> str:
    return f"{ESTRATEGIA_LABEL[estrategia]}\n{modelo}"


def figure_composicion(data: pd.DataFrame) -> None:
    cells = [(e, m) for e in ESTRATEGIAS for m in MODELOS]
    labels = [cell_label(e, m) for e, m in cells]
    counts = {
        categoria: [
            int(((data["estrategia"] == e) & (data["modelo"] == m) & (data["categoria"] == categoria)).sum())
            for e, m in cells
        ]
        for categoria in CATEGORIAS
    }
    fig, ax = plt.subplots(figsize=(14, 5.5))
    bottoms = np.zeros(len(cells))
    for categoria in CATEGORIAS:
        vals = np.array(counts[categoria])
        ax.bar(range(len(cells)), vals, bottom=bottoms, color=COLORES[categoria], label=CATEGORIA_LABEL[categoria])
        bottoms += vals
    ax.set_xticks(range(len(cells)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Unidades de evaluación (n)")
    ax.set_ylim(0, 84)
    ax.axhline(79, color="black", linestyle="--", linewidth=1)
    ax.text(len(cells) - 0.5, 80, "79 unidades por celda", ha="right", va="bottom", fontsize=8)
    ax.legend(ncol=4, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.28))
    ax.set_title("Composición de respuestas por estrategia y modelo")
    fig.tight_layout()
    save_figure(fig, "01_composicion_respuestas_por_celda")


def figure_failure_rates(summary: pd.DataFrame) -> None:
    labels = [cell_label(e, m) for e, m in zip(summary["estrategia"], summary["modelo"])]
    y = summary["tasa_no_sustantiva"].to_numpy() * 100
    lower = summary["tasa_no_sustantiva_ic95_inf"].to_numpy() * 100
    upper = summary["tasa_no_sustantiva_ic95_sup"].to_numpy() * 100
    fig, ax = plt.subplots(figsize=(12, 5.5))
    x = np.arange(len(summary))
    colors = ["#D55E00" if e == "llm_responses_agentic_rag" else "#0072B2" for e in summary["estrategia"]]
    ax.bar(x, y, color=colors, alpha=0.85)
    ax.errorbar(x, y, yerr=[y - lower, upper - y], fmt="none", ecolor="black", capsize=3, linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Tasa de salidas no sustantivas (%)")
    ax.set_ylim(0, 75)
    for xi, yi in zip(x, y):
        if yi > 0:
            ax.text(xi, yi + 1.5, f"{yi:.0f}%", ha="center", fontsize=8)
    ax.set_title("Tasa de salidas no sustantivas por celda (IC 95% Wilson)")
    fig.tight_layout()
    save_figure(fig, "02_tasas_fallo_por_celda")


def figure_nano_states(data: pd.DataFrame) -> None:
    group = data[(data["estrategia"] == "llm_responses_agentic_rag") & (data["modelo"] == "gpt-5-nano")]
    counts = Counter(group["categoria"])
    ordered = [c for c in CATEGORIAS if counts.get(c, 0) > 0]
    values = [counts[c] for c in ordered]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    y = np.arange(len(ordered))
    ax.barh(y, values, color=[COLORES[c] for c in ordered])
    ax.set_yticks(y)
    ax.set_yticklabels([CATEGORIA_LABEL[c] for c in ordered])
    ax.invert_yaxis()
    ax.set_xlabel("Cantidad de unidades (de 79)")
    for yi, vi in zip(y, values):
        ax.text(vi + 0.8, yi, str(vi), va="center", fontsize=10)
    ax.set_xlim(0, max(values) + 6)
    ax.set_title("Agentic-RAG + gpt-5-nano: estados de las 79 salidas")
    fig.tight_layout()
    save_figure(fig, "03_estados_nano_agentic")


def figure_scores_by_state(data: pd.DataFrame) -> None:
    group = data[data["es_no_sustantiva"]].copy()
    categories = [c for c in CATEGORIAS_NO_SUSTANTIVAS if (group["categoria"] == c).any()]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    rng = np.random.default_rng(20261111)
    for i, categoria in enumerate(categories):
        vals = group[group["categoria"] == categoria]["puntaje_original_rubric"].dropna().tolist()
        x = i + rng.uniform(-0.16, 0.16, len(vals))
        ax.scatter(x, vals, s=28, color=COLORES[categoria], alpha=0.8, edgecolor="black", linewidth=0.3)
        if vals:
            ax.plot([i - 0.25, i + 0.25], [statistics.median(vals)] * 2, color="black", linewidth=2)
    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels([CATEGORIA_LABEL[c] for c in categories], rotation=20, ha="right")
    ax.set_ylabel("Puntaje medio de los jueces (rúbrica)")
    ax.set_ylim(-0.05, 1.05)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title("Puntajes de jueces asignados a salidas no sustantivas")
    fig.tight_layout()
    save_figure(fig, "04_puntajes_jueces_salidas_no_sustantivas")


def figure_nano_logs(data: pd.DataFrame) -> None:
    group = data[(data["estrategia"] == "llm_responses_agentic_rag") & (data["modelo"] == "gpt-5-nano")].copy()
    group["estado"] = np.where(group["es_no_sustantiva"], "No sustantiva", "Sustantiva")
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))
    panels = [
        ("law_output_tokens", "Tokens de salida del especialista"),
        ("law_reasoning_tokens", "Tokens de razonamiento del especialista"),
        ("law_selected_docs_first", "Documentos seleccionados por el recuperador"),
    ]
    for ax, (column, title) in zip(axes, panels):
        vals = [
            pd.to_numeric(group[group["estado"] == estado][column], errors="coerce").dropna().tolist()
            for estado in ["Sustantiva", "No sustantiva"]
        ]
        bp = ax.boxplot(vals, tick_labels=["Sustantiva", "No sustantiva"], patch_artist=True, widths=0.55)
        for patch, color in zip(bp["boxes"], ["#0072B2", "#D55E00"]):
            patch.set_facecolor(color)
            patch.set_alpha(0.65)
        ax.set_title(title, fontsize=9)
        ax.tick_params(axis="x", labelsize=8)
    fig.suptitle("Agentic-RAG + gpt-5-nano: tokens y recuperación por estado de salida", fontsize=12)
    fig.tight_layout()
    save_figure(fig, "05_logs_tokens_y_recuperacion_nano")


def figure_nano_scenarios(data: pd.DataFrame) -> None:
    group = data[(data["modelo"] == "gpt-5-nano")]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    scenarios = [
        ("puntaje_original_rubric", "Original (jueces)"),
        ("puntaje_fallo_cero", "Fallo = 0"),
        ("puntaje_exclusion", "Exclusión"),
    ]
    width = 0.25
    x = np.arange(len(ESTRATEGIAS))
    for j, (column, label) in enumerate(scenarios):
        vals = []
        for estrategia in ESTRATEGIAS:
            series = group[group["estrategia"] == estrategia][column].dropna().tolist()
            vals.append(safe_mean(series) if series else np.nan)
        ax.bar(x + (j - 1) * width, vals, width, label=label)
    ax.set_xticks(x)
    ax.set_xticklabels([ESTRATEGIA_LABEL[e] for e in ESTRATEGIAS])
    ax.set_ylabel("Media de respuesta correcta")
    ax.set_ylim(0, 1)
    ax.legend(fontsize=8)
    ax.set_title("gpt-5-nano: sensibilidad al tratamiento de salidas no sustantivas")
    fig.tight_layout()
    save_figure(fig, "06_escenarios_nano")


def figure_no_rag_nano_mini(data: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8, 4.8))
    groups = []
    labels = []
    colors = []
    for modelo, color in [("gpt-5-nano", "#56B4E9"), ("gpt-5-mini", "#CC79A7")]:
        group = data[(data["estrategia"] == "llm_responses_no_rag") & (data["modelo"] == modelo)]
        groups.append(group["puntaje_original_rubric"].dropna().tolist())
        labels.append(f"Sin RAG\n{modelo}")
        colors.append(color)
    bp = ax.boxplot(groups, tick_labels=labels, patch_artist=True, widths=0.55)
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)
    rng = np.random.default_rng(20261111)
    for i, vals in enumerate(groups, start=1):
        x = i + rng.uniform(-0.12, 0.12, len(vals))
        ax.scatter(x, vals, s=18, color="black", alpha=0.55)
    ax.set_ylabel("Respuesta correcta (promedio de jueces)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("Sin RAG: distribución de gpt-5-nano y gpt-5-mini")
    fig.tight_layout()
    save_figure(fig, "07_sim_rag_nano_vs_mini")


# ---------------------------------------------------------------------------
# Revisión manual
# ---------------------------------------------------------------------------


def build_review_packet(data: pd.DataFrame) -> None:
    rng = random.Random(20261111)
    non_sub = data[data["es_no_sustantiva"]].copy()
    substantive = data[data["categoria"] == "sustantiva"].copy()

    # Muestra de control: 30 respuestas sustantivas, estratificada por celda.
    sample_rows = []
    per_cell = 30 // 9
    remainder = 30 - per_cell * 9
    cells = [(e, m) for e in ESTRATEGIAS for m in MODELOS]
    for i, (estrategia, modelo) in enumerate(cells):
        n_take = per_cell + (1 if i < remainder else 0)
        pool = substantive[(substantive["estrategia"] == estrategia) & (substantive["modelo"] == modelo)]
        if len(pool) > n_take:
            sample_rows.extend(pool.sample(n=n_take, random_state=20261111 + i).to_dict("records"))
        else:
            sample_rows.extend(pool.to_dict("records"))
    controls = pd.DataFrame(sample_rows)

    packet = pd.concat([non_sub, controls], ignore_index=True)
    packet = packet.sample(frac=1, random_state=20261111).reset_index(drop=True)
    packet["review_id"] = [f"R{i:03d}" for i in range(1, len(packet) + 1)]
    packet["pregunta"] = packet["texto_pregunta"]
    packet["respuesta_para_revision"] = packet["respuesta_obtenida"]
    packet["longitud_caracteres"] = packet["respuesta_para_revision"].map(lambda x: len(norm_text(x)))

    packet_out = packet[
        ["review_id", "pregunta", "respuesta_para_revision", "longitud_caracteres"]
    ].copy()
    packet_out.to_csv(REVISION / "paquete_revision_ciega.csv", index=False, encoding="utf-8")

    mapping = packet[
        [
            "review_id",
            "obs_id",
            "q",
            "sub",
            "estrategia",
            "estrategia_corta",
            "modelo",
            "categoria",
            "subcategoria",
            "es_no_sustantiva",
            "respuesta_obtenida",
        ]
    ].copy()
    mapping.to_csv(SALIDAS / "mapa_revision_ciega.csv", index=False, encoding="utf-8")

    template = pd.DataFrame(
        {
            "review_id": packet_out["review_id"],
            "categoria_revisada": "",
            "justificacion": "",
            "revisor": "",
            "fecha": "",
        }
    )
    # No sobrescribir una plantilla ya completada o aceptada.
    canonical_template = REVISION / "plantilla_resultados.csv"
    if not canonical_template.exists():
        template.to_csv(canonical_template, index=False, encoding="utf-8")

    # Lista de verificación asistida, separada del paquete ciego.
    non_sub[
        [
            "obs_id",
            "q",
            "sub",
            "estrategia",
            "modelo",
            "categoria",
            "subcategoria",
            "evidencia",
            "longitud_caracteres",
        ]
    ].to_csv(SALIDAS / "lista_verificacion_no_sustantivas.csv", index=False, encoding="utf-8")


# ---------------------------------------------------------------------------
# Manifiesto y resumen
# ---------------------------------------------------------------------------


def write_manifest() -> None:
    paths = [
        RESPONSES_PATH,
        METRICS_PATH,
        JUDGES_PATH,
        METADATA_PATH,
        BENCHMARK_PATH,
        AGENTIC_JSON_PATH,
        EXP / "part_h_1" / "llm_responses_all_results_with_metrics_judged_FINAL.json",
        EXP / "part_g" / "llm_responses_agentic_rag_results_FINAL.json",
        EXP / "part_h" / "llm_responses_all_results_with_metrics_FINAL.json",
        EXP / "part_i" / "metadata_tokens_cost_cleaned.csv",
    ]
    rows = []
    for path in paths:
        rows.append(
            {
                "ruta": str(path.relative_to(BASE)) if path.exists() else str(path),
                "existe": path.exists(),
                "bytes": path.stat().st_size if path.exists() else None,
                "sha256": sha256(path),
            }
        )
    pd.DataFrame(rows).to_csv(SALIDAS / "00_manifiesto_entradas.csv", index=False, encoding="utf-8")

    # Inventario de logs de agentes.
    log_rows = []
    for path in sorted(LOGS_PATH.rglob("*.json")):
        log_rows.append(
            {
                "ruta": str(path.relative_to(BASE)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    pd.DataFrame(log_rows).to_csv(SALIDAS / "00_manifiesto_logs_agentes.csv", index=False, encoding="utf-8")


def write_summary_json(
    data: pd.DataFrame,
    summary: pd.DataFrame,
    join_audit: pd.DataFrame,
    judge_audit: pd.DataFrame,
    logs_summary: pd.DataFrame,
    manuscript: pd.DataFrame,
    sensitivity: pd.DataFrame,
    no_rag: pd.DataFrame,
) -> None:
    nano = data[(data["estrategia"] == "llm_responses_agentic_rag") & (data["modelo"] == "gpt-5-nano")]
    nano_counts = Counter(nano["categoria"])
    nano_summary = summary[
        (summary["estrategia"] == "llm_responses_agentic_rag") & (summary["modelo"] == "gpt-5-nano")
    ].iloc[0]
    judge_nonzero = judge_audit[judge_audit["puntaje_correcta_no_cero"]]
    summary_dict = {
        "n_observaciones": int(len(data)),
        "n_unidades": int(data["obs_id"].nunique()),
        "n_casos": int(data["q"].nunique()),
        "n_celdas": int(data.groupby(["estrategia", "modelo"]).ngroups),
        "n_filas_juez": int(len(judge_audit)),
        "n_evaluaciones_juez_esperadas": int(len(data) * 3),
        "n_medias_ausentes_join": int(len(join_audit)),
        "n_no_sustantivas_total": int(data["es_no_sustantiva"].sum()),
        "nano_agentic": {
            "n": int(len(nano)),
            "categorias": dict(nano_counts),
            "n_sustantiva": int(nano_counts.get("sustantiva", 0)),
            "n_no_sustantiva": int(len(nano) - nano_counts.get("sustantiva", 0)),
            "tasa_no_sustantiva": float(nano_summary["tasa_no_sustantiva"]),
            "ic95_inf": float(nano_summary["tasa_no_sustantiva_ic95_inf"]),
            "ic95_sup": float(nano_summary["tasa_no_sustantiva_ic95_sup"]),
            "media_original": float(nano_summary["media_original"]),
            "mediana_original": float(nano_summary["mediana_original"]),
            "media_fallo_cero": float(nano_summary["media_fallo_cero"]),
            "mediana_fallo_cero": float(nano_summary["mediana_fallo_cero"]),
            "media_exclusion": float(nano_summary["media_exclusion"]),
            "mediana_exclusion": float(nano_summary["mediana_exclusion"]),
            "n_exclusion": int(nano_summary["n_exclusion"]),
            "n_juez_no_cero_en_no_sustantiva": int(nano_summary["n_juez_no_cero_en_no_sustantiva"]),
        },
        "jueces_no_sustantivas": {
            "n_filas": int(len(judge_audit)),
            "n_puntajes_correcta_no_cero": int(judge_nonzero.shape[0]),
            "n_observaciones_celda_con_al_menos_un_no_cero": int(
                judge_audit.groupby(["obs_id", "estrategia", "modelo"])["puntaje_correcta_no_cero"].any().sum()
            ),
            "n_obs_id_distintos_con_al_menos_un_no_cero": int(
                judge_nonzero["obs_id"].nunique()
            ),
            "n_puntajes_legal_no_cero": int(judge_audit["puntaje_legal_no_cero"].sum()),
        },
        "logs": logs_summary.to_dict(orient="records"),
        "comparacion_manuscrito": manuscript.to_dict(orient="records"),
        "sensibilidad": sensitivity.to_dict(orient="records"),
        "sin_rag_nano_mini": no_rag.to_dict(orient="records"),
    }
    (SALIDAS / "resumen_ejecutivo.json").write_text(
        json.dumps(summary_dict, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    for directory in (SALIDAS, FIGURAS, REVISION):
        directory.mkdir(parents=True, exist_ok=True)

    write_manifest()
    data, responses, metrics, judges, logs = build_dataset()

    # Guardas de integridad.
    assert len(data) == 711, f"Se esperaban 711 observaciones, se obtuvieron {len(data)}"
    assert data["obs_id"].nunique() == 79, "Se esperaban 79 unidades"
    assert data.groupby(["estrategia", "modelo"]).size().eq(79).all(), "Cada celda debe tener 79 filas"
    assert len(judges) == 2133, f"Se esperaban 2133 filas de jueces, se obtuvieron {len(judges)}"

    summary = summarize_cells(data)
    categories = summarize_categories(data)
    join_audit = build_join_audit(data, judges)
    judge_audit = build_judge_audit(data, judges)
    logs_summary = build_logs_summary(logs)
    manuscript = build_manuscript_comparison(data, metrics)
    sensitivity = build_sensitivity(data)
    no_rag = build_no_rag_descriptive(data)

    # Tablas principales.
    data.to_csv(SALIDAS / "01_dataset_derivado_711.csv", index=False, encoding="utf-8")
    summary.to_csv(SALIDAS / "02_resumen_por_celda.csv", index=False, encoding="utf-8")
    categories.to_csv(SALIDAS / "03_conteo_categorias_por_celda.csv", index=False, encoding="utf-8")
    categories_wide = (
        categories.pivot(index=["estrategia", "estrategia_corta", "modelo"], columns="categoria", values="n")
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    categories_wide.to_csv(SALIDAS / "03b_tabla_categorias_ancha.csv", index=False, encoding="utf-8")
    join_audit.to_csv(SALIDAS / "04_auditoria_faltantes_join.csv", index=False, encoding="utf-8")
    judge_audit.to_csv(SALIDAS / "05_auditoria_jueces_salidas_no_sustantivas.csv", index=False, encoding="utf-8")
    logs.to_csv(SALIDAS / "06_logs_agentes_237.csv", index=False, encoding="utf-8")
    logs_summary.to_csv(SALIDAS / "07_resumen_logs_por_modelo.csv", index=False, encoding="utf-8")
    manuscript.to_csv(SALIDAS / "08_comparacion_medianas_manuscrito.csv", index=False, encoding="utf-8")
    sensitivity.to_csv(SALIDAS / "09_sensibilidad_pares_estrategias.csv", index=False, encoding="utf-8")
    no_rag.to_csv(SALIDAS / "10_sin_rag_nano_vs_mini.csv", index=False, encoding="utf-8")

    nano = data[(data["estrategia"] == "llm_responses_agentic_rag") & (data["modelo"] == "gpt-5-nano")].copy()
    nano.to_csv(SALIDAS / "11_celda_nano_agentic_79.csv", index=False, encoding="utf-8")

    # Auditoría específica de las 27 medias ausentes.
    join_audit.to_csv(SALIDAS / "12_auditoria_27_medias_ausentes.csv", index=False, encoding="utf-8")

    # Casos no sustantivos con evidencia textual y de log.
    non_sub = data[data["es_no_sustantiva"]].copy()
    non_sub.to_csv(SALIDAS / "13_salidas_no_sustantivas_con_evidencia.csv", index=False, encoding="utf-8")

    build_review_packet(data)
    write_summary_json(data, summary, join_audit, judge_audit, logs_summary, manuscript, sensitivity, no_rag)

    # Figuras.
    figure_composicion(data)
    figure_failure_rates(summary)
    figure_nano_states(data)
    figure_scores_by_state(data)
    figure_nano_logs(data)
    figure_nano_scenarios(data)
    figure_no_rag_nano_mini(data)

    # Imprimir resumen de control.
    print("=" * 78)
    print("DIAGNÓSTICO IX.1.2 — RESUMEN DE CONTROL")
    print("=" * 78)
    print(f"Observaciones: {len(data)} | Unidades: {data['obs_id'].nunique()} | Celdas: {data.groupby(['estrategia', 'modelo']).ngroups}")
    print(f"Filas de jueces: {len(judges)} | Medias ausentes por join: {len(join_audit)}")
    print(f"No sustantivas: {int(data['es_no_sustantiva'].sum())}")
    print("\nAgentic-RAG + gpt-5-nano:")
    print(nano["categoria"].value_counts().to_string())
    print("\nResumen de la celda:")
    print(
        summary[
            (summary["estrategia"] == "llm_responses_agentic_rag") & (summary["modelo"] == "gpt-5-nano")
        ][
            [
                "n_sustantiva",
                "n_no_sustantiva",
                "tasa_no_sustantiva",
                "tasa_no_sustantiva_ic95_inf",
                "tasa_no_sustantiva_ic95_sup",
                "media_original",
                "mediana_original",
                "media_fallo_cero",
                "mediana_fallo_cero",
                "media_exclusion",
                "mediana_exclusion",
                "n_exclusion",
            ]
        ].to_string(index=False)
    )
    print("\nComparación de medianas:")
    print(manuscript.to_string(index=False))
    print("\nSensibilidad de comparaciones clave (gpt-5-nano):")
    print(
        sensitivity[
            (sensitivity["modelo"] == "gpt-5-nano")
        ][
            ["estrategia_1", "estrategia_2", "escenario", "n_pares", "media_diferencia", "mediana_diferencia"]
        ].to_string(index=False)
    )
    print("\nJueces sobre salidas no sustantivas:")
    print(judge_audit.groupby(["categoria"]).agg(n_filas=("obs_id", "size"), no_cero=("puntaje_correcta_no_cero", "sum")).to_string())
    print("\nArtefactos escritos en:", OUT)


if __name__ == "__main__":
    main()

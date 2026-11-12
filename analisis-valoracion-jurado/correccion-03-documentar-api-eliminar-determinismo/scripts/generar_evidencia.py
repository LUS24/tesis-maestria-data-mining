# -*- coding: utf-8 -*-
"""Genera la evidencia reproducible para IX.1.3.

Este script es de solo lectura sobre el repositorio. Todos los artefactos que
produce se escriben dentro de esta carpeta de corrección, en ``salidas/``.

Uso recomendado, desde la raíz del repositorio:

    cd codigo_experimentos
    uv run --no-sync --frozen python \
      ../analisis-valoracion-jurado/correccion-03-documentar-api-eliminar-determinismo/scripts/generar_evidencia.py

No realiza llamadas a APIs externas: la captura del payload se hace con un
transporte HTTP simulado de httpx y una respuesta Chat Completions local.
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import inspect
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import httpx
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.profiles.openai import openai_model_profile
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings


# ---------------------------------------------------------------------------
# Rutas y constantes
# ---------------------------------------------------------------------------

ARTIFACT_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = ARTIFACT_DIR.parents[1]
OUT_DIR = ARTIFACT_DIR / "salidas"
OUT_DIR.mkdir(parents=True, exist_ok=True)

EXPERIMENTS = REPO_ROOT / "codigo_experimentos"
MANUSCRIPT = REPO_ROOT / "manuscrito"

PART_E = EXPERIMENTS / "part_e" / "02_query_llms_for_responses.ipynb"
PART_F = EXPERIMENTS / "part_f" / "01_rag_llm_responses.ipynb"
PART_G_PY = EXPERIMENTS / "part_g" / "01_generate_responses_using_agents.py"
PART_G_IPYNB = EXPERIMENTS / "part_g" / "01_generate_responses_using_agents.ipynb"
PART_H_JSON = EXPERIMENTS / "part_h" / "llm_responses_all_results_with_metrics_FINAL.json"
PART_G_JSON = (
    EXPERIMENTS
    / "part_g"
    / "llm_responses_agentic_rag_results_with_metrics_and_metadata_FINAL.json"
)
PART_I_METADATA = EXPERIMENTS / "part_i" / "metadata_tokens_cost_cleaned.csv"
PART_I_COMBINED = EXPERIMENTS / "part_i" / "combined_metrics_for_analysis.csv"
PART_H1_REPORTS = EXPERIMENTS / "part_h_1" / "reports"
PART_G_LOGS = EXPERIMENTS / "part_g" / "chat_data"

MODELOS = ["gpt-5-nano", "gpt-5-mini", "gpt-5"]
ESTRATEGIAS = {
    "sin_rag": "llm_responses_no_rag",
    "rag_basico": "llm_responses_base_rag",
    "agentic_rag": "llm_responses_agentic_rag",
}
MODELOS_ETIQUETA = {
    "gpt-5-nano": "gpt-5-nano",
    "gpt-5-mini": "gpt-5-mini",
    "gpt-5": "gpt-5",
}
MODELOS_ESPERADOS_VERSION = {
    "gpt-5-nano": "gpt-5-nano-2025-08-07",
    "gpt-5-mini": "gpt-5-mini-2025-08-07",
    "gpt-5": "gpt-5-2025-08-07",
}


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if not rows:
        raise ValueError(f"No hay filas para escribir en {path}")
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_sub(value: Any) -> str:
    """Normaliza el identificador de subpregunta solo para análisis.

    En el corpus hay tres preguntas de unidad única con subpregunta vacía/None
    en unos artefactos y ``0`` en otros. No se modifica la fuente: se conserva
    el valor original en las tablas y se usa esta función para el análisis.
    """
    if value is None:
        return "00"
    text = str(value).strip()
    if text in {"", "0", "00", "None", "null"}:
        return "00"
    return f"{int(text):02d}"


def case_id(value: Any) -> str:
    return f"{int(value):02d}"


def unit_id(case: Any, sub: Any) -> str:
    return f"{case_id(case)}-{canonical_sub(sub)}"


def text_is_blank(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def stats(values: Iterable[Any]) -> dict[str, Any]:
    vals = [float(v) for v in values if v is not None and not (isinstance(v, float) and math.isnan(v))]
    if not vals:
        return {
            "n": 0,
            "min": None,
            "p25": None,
            "mediana": None,
            "p75": None,
            "max": None,
            "media": None,
            "total": None,
        }
    arr = np.asarray(vals, dtype=float)
    return {
        "n": len(vals),
        "min": round(float(arr.min()), 4),
        "p25": round(float(np.percentile(arr, 25)), 4),
        "mediana": round(float(np.median(arr)), 4),
        "p75": round(float(np.percentile(arr, 75)), 4),
        "max": round(float(arr.max()), 4),
        "media": round(float(arr.mean()), 4),
        "total": round(float(arr.sum()), 4),
    }


def value_stats_text(values: Iterable[Any]) -> str:
    s = stats(values)
    if not s["n"]:
        return "sin datos"
    return (
        f"n={s['n']}; min={s['min']:.0f}; p25={s['p25']:.0f}; "
        f"mediana={s['mediana']:.0f}; p75={s['p75']:.0f}; max={s['max']:.0f}; "
        f"media={s['media']:.0f}"
    )


# ---------------------------------------------------------------------------
# Carga de datos primarios
# ---------------------------------------------------------------------------


def load_primary_data() -> list[dict[str, Any]]:
    with PART_H_JSON.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise TypeError("El archivo de respuestas primario no es una lista")
    return data


def primary_records(data: list[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    for item in data:
        for strategy, key in ESTRATEGIAS.items():
            for record in item.get(key, []):
                if strategy == "agentic_rag":
                    model_full = record.get("law_specialist_model", "")
                    model = model_full.split(":")[-1]
                    metadata = record.get("metadata", {}).get("law_specialist_agent", {})
                else:
                    metadata = record.get("metadata", {})
                    model = metadata.get("usage", {}).get("cost", {}).get("model_id", "")
                yield {
                    "item": item,
                    "strategy": strategy,
                    "strategy_key": key,
                    "model": model,
                    "record": record,
                    "metadata": metadata,
                    "unit_id": unit_id(item.get("numero_pregunta"), item.get("numero_subpregunta")),
                    "case_id": case_id(item.get("numero_pregunta")),
                }


def rows_for(data: list[dict[str, Any]], strategy: str, model: str) -> list[dict[str, Any]]:
    return [
        row
        for row in primary_records(data)
        if row["strategy"] == strategy and row["model"] == model
    ]


# ---------------------------------------------------------------------------
# Manifiesto de entradas
# ---------------------------------------------------------------------------


def build_manifest() -> dict[str, Any]:
    files: list[Path] = [
        EXPERIMENTS / "uv.lock",
        EXPERIMENTS / "pyproject.toml",
        PART_E,
        PART_F,
        PART_G_PY,
        PART_G_IPYNB,
        PART_H_JSON,
        PART_G_JSON,
        PART_I_METADATA,
        PART_I_COMBINED,
        MANUSCRIPT / "main.typ",
        MANUSCRIPT / "capitulos" / "06_capitulo_05_metodologia.typ",
        MANUSCRIPT / "capitulos" / "07_capitulo_06_evaluacion.typ",
        REPO_ROOT / "README.md",
        EXPERIMENTS / "performed_tasks_summary.md",
    ]
    for directory, pattern in [
        (PART_G_LOGS, "*.json"),
        (PART_H1_REPORTS, "*.json"),
    ]:
        files.extend(sorted(directory.rglob(pattern)))

    rows = []
    for path in sorted(set(files)):
        if not path.exists():
            raise FileNotFoundError(path)
        rows.append(
            {
                "ruta_relativa": str(path.relative_to(REPO_ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
                "categoria": (
                    "log_agente"
                    if PART_G_LOGS in path.parents
                    else "reporte_juez"
                    if PART_H1_REPORTS in path.parents
                    else "fuente_o_manuscrito"
                ),
            }
        )

    write_csv(OUT_DIR / "manifiesto_entradas.csv", rows)

    counts = Counter(row["categoria"] for row in rows)
    digest = hashlib.sha256(
        "".join(f"{row['ruta_relativa']}:{row['sha256']}\n" for row in rows).encode("utf-8")
    ).hexdigest()
    summary = {
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "archivos": len(rows),
        "bytes": sum(int(row["bytes"]) for row in rows),
        "por_categoria": dict(counts),
        "sha256_conjunto": digest,
        "nota": "Los hashes se calculan antes de generar las tablas derivadas; no se modifica ninguna fuente.",
    }
    write_json(OUT_DIR / "manifiesto_resumen.json", summary)
    return summary


# ---------------------------------------------------------------------------
# Evidencia de Pydantic AI y captura local de payload
# ---------------------------------------------------------------------------


def _mock_chat_response(model: str) -> dict[str, Any]:
    return {
        "id": f"chatcmpl-local-{re.sub(r'[^a-z0-9]+', '-', model)}",
        "object": "chat.completion",
        "created": 1700000000,
        "model": f"{model}-2025-08-07",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": "respuesta local de prueba"},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
            "completion_tokens_details": {"reasoning_tokens": 12},
        },
    }


async def _capture_one(
    *,
    strategy: str,
    role: str,
    model: str,
    settings: ModelSettings,
) -> dict[str, Any]:
    captured: list[dict[str, Any]] = []
    request_info: dict[str, Any] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        request_info["method"] = request.method
        request_info["url"] = str(request.url)
        request_info["headers"] = {
            key: ("[REDACTED]" if key.lower() == "authorization" else value)
            for key, value in request.headers.items()
        }
        captured.append(json.loads(request.content))
        return httpx.Response(200, json=_mock_chat_response(model))

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        base_url="https://api.openai.com/v1",
    ) as client:
        provider = OpenAIProvider(api_key="local-test-key", http_client=client)
        model_obj = OpenAIChatModel(model, provider=provider)

        if role == "especialista" and strategy == "sin_rag":
            agent = Agent(
                model=model_obj,
                system_prompt="Asistente legal de prueba.",
                model_settings=settings,
            )
            prompt = "Pregunta de prueba sin recuperación."
        elif role == "especialista" and strategy == "rag_basico":
            agent = Agent(
                model=model_obj,
                system_prompt=(
                    "Asistente legal de prueba. Contexto recuperado: "
                    "[Artículo 1 de prueba]."
                ),
                model_settings=settings,
            )
            prompt = "Pregunta de prueba con RAG básico."
        elif role == "especialista" and strategy == "agentic_rag":

            def retrieve_relevant_documents(question: str) -> dict[str, Any]:
                """Recupera documentos de prueba para responder la pregunta."""
                return {"selected_documents": [], "question": question}

            agent = Agent(
                model=model_obj,
                instructions=(
                    "Asistente legal de prueba. Usa la herramienta de recuperación "
                    "una vez y responde citando las fuentes."
                ),
                tools=[retrieve_relevant_documents],
                model_settings=settings,
            )
            prompt = "Pregunta de prueba con Agentic-RAG (especialista)."
        elif role == "recuperador":

            def cosine_distance_vector_search(query: str) -> list[dict[str, Any]]:
                """Busca documentos por similitud coseno en la base vectorial."""
                return []

            agent = Agent(
                model=model_obj,
                instructions=(
                    "Especialista en búsqueda legislativa. Descompón la consulta "
                    "en hasta tres subconsultas y usa la herramienta de búsqueda."
                ),
                tools=[cosine_distance_vector_search],
                model_settings=settings,
            )
            prompt = "Consulta de prueba para el agente de recuperación."
        else:
            raise ValueError((strategy, role))

        before = dict(agent.model_settings or {})
        result = await agent.run(prompt, model_settings=settings)
        after = dict(agent.model_settings or {})
        if len(captured) != 1:
            raise RuntimeError(f"Se esperaba una petición y se capturaron {len(captured)}")
        body = captured[0]
        message_roles = [message.get("role") for message in body.get("messages", [])]
        tools = body.get("tools") or []
        tool_names = [
            tool.get("function", {}).get("name")
            for tool in tools
            if isinstance(tool, dict)
        ]
        return {
            "clave": f"{strategy}|{role}|{model}",
            "estrategia": strategy,
            "componente": role,
            "modelo": model,
            "pydantic_ai_version": __import__("pydantic_ai").__version__,
            "endpoint": request_info.get("url"),
            "method": request_info.get("method"),
            "request_headers_redacted": request_info.get("headers"),
            "model_settings_solicitados": before,
            "model_settings_agente_despues_de_run": after,
            "agent_output": result.output,
            "request_body_keys": sorted(body.keys()),
            "modelo_en_body": body.get("model"),
            "message_roles": message_roles,
            "tools_present": bool(tools),
            "tool_names": tool_names,
            "temperature_presente": "temperature" in body,
            "temperature_valor": body.get("temperature"),
            "reasoning_effort_presente": "reasoning_effort" in body,
            "reasoning_effort_valor": body.get("reasoning_effort"),
            "max_completion_tokens_presente": "max_completion_tokens" in body,
            "max_completion_tokens_valor": body.get("max_completion_tokens"),
            "max_tokens_presente": "max_tokens" in body,
            "seed_presente": "seed" in body,
            "top_p_presente": "top_p" in body,
            "request_body_sin_mensajes": {
                key: value
                for key, value in body.items()
                if key != "messages"
            },
            "request_body": body,
        }


async def _capture_all_payloads() -> dict[str, Any]:
    calls: list[dict[str, Any]] = []
    for model in MODELOS:
        settings = ModelSettings(temperature=0.0)
        calls.append(
            await _capture_one(
                strategy="sin_rag", role="especialista", model=model, settings=settings
            )
        )
        calls.append(
            await _capture_one(
                strategy="rag_basico", role="especialista", model=model, settings=settings
            )
        )
        calls.append(
            await _capture_one(
                strategy="agentic_rag", role="especialista", model=model, settings=settings
            )
        )
        calls.append(
            await _capture_one(
                strategy="agentic_rag", role="recuperador", model="gpt-5", settings=settings
            )
        )
    return {
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "nota": (
            "Captura local con httpx.MockTransport. No se llamó a OpenAI ni a otro "
            "proveedor. El proveedor simulado usa el mismo perfil openai_model_profile "
            "y la misma clase OpenAIChatModel que resuelve pydantic_ai.infer_model('openai:...')."
        ),
        "calls": calls,
    }


def _run_coroutine(coro: Any) -> Any:
    """Ejecuta una corrutina también dentro de un notebook con event loop activo."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    # En Jupyter hay un loop activo y asyncio.run no puede usarse. Se ejecuta
    # la corrutina en un hilo nuevo, con su propio loop, sin nest_asyncio.
    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(asyncio.run, coro).result()


def build_pydantic_evidence(payloads: dict[str, Any]) -> dict[str, Any]:
    import pydantic_ai
    from pydantic_ai.models.openai import OpenAIChatModel

    source_file = Path(inspect.getsourcefile(OpenAIChatModel))
    source_lines, start_line = inspect.getsourcelines(OpenAIChatModel._completions_create)
    source_text = "".join(source_lines)
    source_text_lines = source_text.splitlines()
    marker_index = next(
        (
            index
            for index, line in enumerate(source_text_lines)
            if "unsupported_model_settings = OpenAIModelProfile.from_profile" in line
        ),
        -1,
    )
    if marker_index < 0:
        raise RuntimeError("No se encontró el bloque de settings no soportados")
    excerpt_lines = source_text_lines[
        max(0, marker_index - 3) : marker_index + 14
    ]
    excerpt = (
        f"Archivo: {source_file}\n"
        f"Función: OpenAIChatModel._completions_create, desde línea {start_line}\n"
        f"SHA-256 del archivo: {sha256_file(source_file)}\n"
        f"Líneas del archivo: {start_line + marker_index - 3} a "
        f"{start_line + marker_index + 13}\n\n"
        + "\n".join(excerpt_lines)
        + "\n"
    )
    (OUT_DIR / "evidencia_pydantic_ai_excerpt.txt").write_text(excerpt, encoding="utf-8")

    profiles = {}
    for model in MODELOS:
        profile = openai_model_profile(model)
        profiles[model] = {
            "tipo_perfil": type(profile).__name__,
            "openai_unsupported_model_settings": list(
                profile.openai_unsupported_model_settings
            ),
            "temperatura_entre_no_admitidos": "temperature"
            in profile.openai_unsupported_model_settings,
        }

    evidence = {
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "pydantic_ai_version": getattr(pydantic_ai, "__version__", None),
        "modulo_pydantic_ai": str(Path(inspect.getsourcefile(pydantic_ai)).parent),
        "openai_chat_model_source": str(source_file),
        "openai_chat_model_source_sha256": sha256_file(source_file),
        "linea_inicio_completions_create": start_line,
        "perfiles": profiles,
        "captura_payload": {
            call["clave"]: {
                "strategy": call["estrategia"],
                "role": call["componente"],
                "model": call["modelo"],
                "request_body_keys": call["request_body_keys"],
                "temperature_presente": call["temperature_presente"],
                "reasoning_effort_presente": call["reasoning_effort_presente"],
                "max_completion_tokens_presente": call[
                    "max_completion_tokens_presente"
                ],
                "temperature_solicitada": call["model_settings_solicitados"].get(
                    "temperature"
                ),
            }
            for call in payloads["calls"]
        },
        "conclusion": (
            "En Pydantic AI 1.1.0, el perfil de los tres modelos GPT-5 declara "
            "temperature como setting no admitido. OpenAIChatModel elimina los "
            "settings no admitidos antes de construir la petición al endpoint de "
            "Chat Completions. La captura local confirma que temperature no se "
            "incluye en el cuerpo enviado."
        ),
    }
    write_json(OUT_DIR / "evidencia_perfil_pydantic.json", evidence)
    return evidence


def build_reasoning_effort_evidence(data: list[dict[str, Any]]) -> dict[str, Any]:
    generation_files = [PART_E, PART_F, PART_G_PY, PART_G_IPYNB]
    log_files = sorted(PART_G_LOGS.rglob("*.json"))
    primary_artifacts = [PART_H_JSON, PART_G_JSON, PART_I_METADATA, PART_I_COMBINED]
    judge_reports = sorted(PART_H1_REPORTS.rglob("*.json"))
    checked = generation_files + log_files + primary_artifacts + judge_reports
    occurrences: list[dict[str, Any]] = []
    patterns = re.compile(
        r"reasoning_effort|openai_reasoning_effort|\breasoning\s*=",
        re.IGNORECASE,
    )
    for path in checked:
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in patterns.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            snippet = text[max(0, match.start() - 100) : match.start() + 160]
            occurrences.append(
                {
                    "ruta_relativa": str(path.relative_to(REPO_ROOT)),
                    "linea": line,
                    "coincidencia": match.group(0),
                    "contexto": snippet.replace("\n", " "),
                }
            )

    reasoning_records = 0
    reasoning_non_null = 0
    for row in primary_records(data):
        reasoning_records += 1
        token_details = (
            row["metadata"]
            .get("usage", {})
            .get("tokens", {})
            .get("tokens_details", {})
            or {}
        )
        if token_details.get("reasoning_tokens") is not None:
            reasoning_non_null += 1

    evidence = {
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "alcance": [str(path.relative_to(REPO_ROOT)) for path in checked],
        "ocurrencias_de_reasoning_effort_o_reasoning_igual": occurrences,
        "n_archivos_revisados": len(checked),
        "n_respuestas_primarias": reasoning_records,
        "n_respuestas_con_reasoning_tokens": reasoning_non_null,
        "conclusion": (
            "No se encontró un parámetro explícito de esfuerzo de razonamiento "
            "en el código de generación ni en los logs revisados. La presencia "
            "de reasoning_tokens demuestra consumo de tokens de razonamiento, "
            "pero no identifica el nivel de esfuerzo solicitado ni el aplicado "
            "por el proveedor. El esfuerzo histórico debe declararse desconocido."
        ),
    }
    write_json(OUT_DIR / "evidencia_reasoning_effort.json", evidence)
    return evidence


# ---------------------------------------------------------------------------
# Tablas
# ---------------------------------------------------------------------------


def _record_reasoning(row: dict[str, Any]) -> float | None:
    return (
        row["metadata"]
        .get("usage", {})
        .get("tokens", {})
        .get("tokens_details", {})
        .get("reasoning_tokens")
    )


def _record_output_tokens(row: dict[str, Any]) -> float | None:
    return row["metadata"].get("usage", {}).get("tokens", {}).get("output_tokens")


def _record_settings(row: dict[str, Any]) -> dict[str, Any]:
    return row["metadata"].get("model_settings") or {}


def _payload_for(
    payloads: dict[str, Any], strategy: str, role: str, model: str
) -> dict[str, Any]:
    key = f"{strategy}|{role}|{model}"
    for call in payloads["calls"]:
        if call["clave"] == key:
            return call
    raise KeyError(key)


def build_config_table(
    data: list[dict[str, Any]], payloads: dict[str, Any], profiles: dict[str, Any]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for strategy in ["sin_rag", "rag_basico", "agentic_rag"]:
        for model in MODELOS:
            selected = rows_for(data, strategy, model)
            if len(selected) != 79:
                raise AssertionError(f"{strategy}/{model}: se esperaban 79 registros, hay {len(selected)}")
            role = "especialista" if strategy != "agentic_rag" else "especialista"
            payload = _payload_for(payloads, strategy, role, model)
            reasoning = [_record_reasoning(r) for r in selected]
            output = [_record_output_tokens(r) for r in selected]
            settings_logged = Counter(
                _json_dumps(_record_settings(r)) for r in selected
            )
            versions = sorted({r["metadata"].get("model_version") for r in selected})
            rows.append(
                {
                    "estrategia": strategy,
                    "componente": role,
                    "modelo_rol": model,
                    "modelo_especialista": model,
                    "n_observaciones": len(selected),
                    "modelo_efectivo_version": " | ".join(versions),
                    "settings_solicitados_codigo": _json_dumps(
                        {"temperature": 0.0}
                    ),
                    "settings_registrados_log": " | ".join(
                        f"{key} ({count})" for key, count in settings_logged.items()
                    ),
                    "perfil_pydantic_unsupported": "; ".join(
                        profiles[model]["openai_unsupported_model_settings"]
                    ),
                    "temperatura_en_payload": payload["temperature_presente"],
                    "reasoning_effort_solicitado": payload[
                        "reasoning_effort_presente"
                    ],
                    "reasoning_effort_registrado": any(
                        "reasoning_effort" in _record_settings(r)
                        for r in selected
                    ),
                    "max_tokens_solicitado": "no especificado",
                    "reasoning_tokens_n": stats(reasoning)["n"],
                    "reasoning_tokens_min": stats(reasoning)["min"],
                    "reasoning_tokens_p25": stats(reasoning)["p25"],
                    "reasoning_tokens_mediana": stats(reasoning)["mediana"],
                    "reasoning_tokens_p75": stats(reasoning)["p75"],
                    "reasoning_tokens_max": stats(reasoning)["max"],
                    "reasoning_tokens_media": stats(reasoning)["media"],
                    "reasoning_tokens_total": stats(reasoning)["total"],
                    "output_tokens_mediana": stats(output)["mediana"],
                    "proporcion_razonamiento_mediana": round(
                        float(
                            np.median(
                                [
                                    float(r) / float(o)
                                    for r, o in zip(reasoning, output)
                                    if r is not None and o
                                ]
                            )
                        ),
                        4,
                    ),
                    "respuestas_blancas": sum(
                        text_is_blank(r["record"].get("texto")) for r in selected
                    ),
                    "unidades_unicas": len({r["unit_id"] for r in selected}),
                    "ejecuciones_por_unidad": len(selected)
                    / len({r["unit_id"] for r in selected}),
                    "fuente_codigo": (
                        "codigo_experimentos/part_e/02_query_llms_for_responses.ipynb"
                        if strategy == "sin_rag"
                        else "codigo_experimentos/part_f/01_rag_llm_responses.ipynb"
                        if strategy == "rag_basico"
                        else "codigo_experimentos/part_g/01_generate_responses_using_agents.py"
                    ),
                    "fuente_log": str(PART_H_JSON.relative_to(REPO_ROOT)),
                    "notas": (
                        "El log del agente guarda la configuración solicitada, no el cuerpo HTTP."
                        if strategy != "agentic_rag"
                        else "El log del agente registra {}; no es un volcado de la petición."
                    ),
                }
            )

            if strategy == "agentic_rag":
                retrieval_records = [
                    r
                    for r in primary_records(data)
                    if r["strategy"] == "agentic_rag" and r["model"] == model
                ]
                retrieval_meta = [
                    r["record"].get("metadata", {}).get("retrieval_agent", {})
                    for r in retrieval_records
                ]
                retrieval_reasoning = [
                    m.get("usage", {})
                    .get("tokens", {})
                    .get("tokens_details", {})
                    .get("reasoning_tokens")
                    for m in retrieval_meta
                ]
                retrieval_output = [
                    m.get("usage", {}).get("tokens", {}).get("output_tokens")
                    for m in retrieval_meta
                ]
                retrieval_payload = _payload_for(
                    payloads, "agentic_rag", "recuperador", "gpt-5"
                )
                rows.append(
                    {
                        "estrategia": "agentic_rag",
                        "componente": "recuperador",
                        "modelo_rol": "gpt-5",
                        "modelo_especialista": model,
                        "n_observaciones": len(retrieval_records),
                        "modelo_efectivo_version": " | ".join(
                            sorted({m.get("model_version") for m in retrieval_meta})
                        ),
                        "settings_solicitados_codigo": _json_dumps(
                            {"temperature": 0.0}
                        ),
                        "settings_registrados_log": " | ".join(
                            f"{key} ({count})"
                            for key, count in Counter(
                                _json_dumps(m.get("model_settings") or {})
                                for m in retrieval_meta
                            ).items()
                        ),
                        "perfil_pydantic_unsupported": "; ".join(
                            profiles["gpt-5"]["openai_unsupported_model_settings"]
                        ),
                        "temperatura_en_payload": retrieval_payload[
                            "temperature_presente"
                        ],
                        "reasoning_effort_solicitado": retrieval_payload[
                            "reasoning_effort_presente"
                        ],
                        "reasoning_effort_registrado": any(
                            "reasoning_effort" in (m.get("model_settings") or {})
                            for m in retrieval_meta
                        ),
                        "max_tokens_solicitado": "no especificado",
                        "reasoning_tokens_n": stats(retrieval_reasoning)["n"],
                        "reasoning_tokens_min": stats(retrieval_reasoning)["min"],
                        "reasoning_tokens_p25": stats(retrieval_reasoning)["p25"],
                        "reasoning_tokens_mediana": stats(retrieval_reasoning)[
                            "mediana"
                        ],
                        "reasoning_tokens_p75": stats(retrieval_reasoning)["p75"],
                        "reasoning_tokens_max": stats(retrieval_reasoning)["max"],
                        "reasoning_tokens_media": stats(retrieval_reasoning)[
                            "media"
                        ],
                        "reasoning_tokens_total": stats(retrieval_reasoning)[
                            "total"
                        ],
                        "output_tokens_mediana": stats(retrieval_output)["mediana"],
                        "proporcion_razonamiento_mediana": round(
                            float(
                                np.median(
                                    [
                                        float(r) / float(o)
                                        for r, o in zip(
                                            retrieval_reasoning, retrieval_output
                                        )
                                        if r is not None and o
                                    ]
                                )
                            ),
                            4,
                        ),
                        "respuestas_blancas": "N/A (agente de recuperación)",
                        "unidades_unicas": len(
                            {r["unit_id"] for r in retrieval_records}
                        ),
                        "ejecuciones_por_unidad": len(retrieval_records)
                        / len({r["unit_id"] for r in retrieval_records}),
                        "fuente_codigo": "codigo_experimentos/part_g/01_generate_responses_using_agents.py",
                        "fuente_log": str(PART_H_JSON.relative_to(REPO_ROOT)),
                        "notas": (
                            "El recuperador usa siempre gpt-5; su configuración también "
                            "se registra como {} y no como cuerpo HTTP."
                        ),
                    }
                )
    return rows


def build_reasoning_table(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for strategy in ["sin_rag", "rag_basico", "agentic_rag"]:
        for model in MODELOS:
            selected = rows_for(data, strategy, model)
            reasoning = [_record_reasoning(r) for r in selected]
            output = [_record_output_tokens(r) for r in selected]
            s = stats(reasoning)
            rows.append(
                {
                    "estrategia": strategy,
                    "componente": "especialista",
                    "modelo_rol": model,
                    "n": s["n"],
                    "min": s["min"],
                    "p25": s["p25"],
                    "mediana": s["mediana"],
                    "p75": s["p75"],
                    "max": s["max"],
                    "media": s["media"],
                    "total": s["total"],
                    "output_tokens_mediana": stats(output)["mediana"],
                    "proporcion_razonamiento_mediana": round(
                        float(
                            np.median(
                                [
                                    float(r) / float(o)
                                    for r, o in zip(reasoning, output)
                                    if r is not None and o
                                ]
                            )
                        ),
                        4,
                    ),
                    "respuestas_blancas": sum(
                        text_is_blank(r["record"].get("texto")) for r in selected
                    ),
                    "fuente": str(PART_H_JSON.relative_to(REPO_ROOT)),
                }
            )
            if strategy == "agentic_rag":
                meta = [
                    r["record"].get("metadata", {}).get("retrieval_agent", {})
                    for r in selected
                ]
                rvals = [
                    m.get("usage", {})
                    .get("tokens", {})
                    .get("tokens_details", {})
                    .get("reasoning_tokens")
                    for m in meta
                ]
                ovals = [
                    m.get("usage", {}).get("tokens", {}).get("output_tokens")
                    for m in meta
                ]
                s = stats(rvals)
                rows.append(
                    {
                        "estrategia": strategy,
                        "componente": "recuperador",
                        "modelo_rol": "gpt-5",
                        "n": s["n"],
                        "min": s["min"],
                        "p25": s["p25"],
                        "mediana": s["mediana"],
                        "p75": s["p75"],
                        "max": s["max"],
                        "media": s["media"],
                        "total": s["total"],
                        "output_tokens_mediana": stats(ovals)["mediana"],
                        "proporcion_razonamiento_mediana": round(
                            float(
                                np.median(
                                    [
                                        float(r) / float(o)
                                        for r, o in zip(rvals, ovals)
                                        if r is not None and o
                                    ]
                                )
                            ),
                            4,
                        ),
                        "respuestas_blancas": "N/A",
                        "fuente": str(PART_H_JSON.relative_to(REPO_ROOT)),
                    }
                )
    return rows


def build_execution_table(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for strategy in ["sin_rag", "rag_basico", "agentic_rag"]:
        for model in MODELOS:
            selected = rows_for(data, strategy, model)
            timestamps = [
                r["metadata"].get("timestamp")
                for r in selected
                if r["metadata"].get("timestamp")
            ]
            if strategy == "agentic_rag":
                retrieval_timestamps = [
                    r["record"]
                    .get("metadata", {})
                    .get("retrieval_agent", {})
                    .get("timestamp")
                    for r in selected
                ]
                retrieval_timestamps = [t for t in retrieval_timestamps if t]
            else:
                retrieval_timestamps = []
            rows.append(
                {
                    "estrategia": strategy,
                    "modelo": model,
                    "registros": len(selected),
                    "unidades_unicas": len({r["unit_id"] for r in selected}),
                    "casos_unicos": len({r["case_id"] for r in selected}),
                    "duplicados_unidad": len(selected)
                    - len({r["unit_id"] for r in selected}),
                    "timestamps_unicos_especialista": len(set(timestamps)),
                    "timestamps_unicos_recuperador": len(
                        set(retrieval_timestamps)
                    ),
                    "replicas_identificadas": 0
                    if len(selected) == len({r["unit_id"] for r in selected})
                    else len(selected) - len({r["unit_id"] for r in selected}),
                    "campo_run_id_replica": "no existe en el artefacto",
                    "respuestas_blancas": sum(
                        text_is_blank(r["record"].get("texto")) for r in selected
                    ),
                    "fecha_inicio_especialista": min(timestamps) if timestamps else None,
                    "fecha_fin_especialista": max(timestamps) if timestamps else None,
                    "fecha_inicio_recuperador": min(retrieval_timestamps)
                    if retrieval_timestamps
                    else None,
                    "fecha_fin_recuperador": max(retrieval_timestamps)
                    if retrieval_timestamps
                    else None,
                    "modelo_version": " | ".join(
                        sorted({r["metadata"].get("model_version") for r in selected})
                    ),
                    "fuente": str(PART_H_JSON.relative_to(REPO_ROOT)),
                    "nota": (
                        "Una fila por unidad y modelo; no hay evidencia de réplicas. "
                        "Los timestamps prueban ejecuciones distintas por unidad, no repeticiones de la misma unidad."
                    ),
                }
            )
    return rows


def build_judge_table() -> list[dict[str, Any]]:
    reports = sorted(PART_H1_REPORTS.rglob("*.json"))
    by_model: dict[str, dict[Path, dict[str, Any]]] = defaultdict(dict)
    for path in reports:
        with path.open("r", encoding="utf-8") as handle:
            report = json.load(handle)
        # Cada reporte contiene dos evaluadores (una por rúbrica), pero ambos
        # pertenecen al mismo juez y evaluaron los mismos casos. Se deduplica
        # por reporte para no contar dos veces las 79 evaluaciones.
        for evaluator in report.get("evaluators", []):
            args = evaluator.get("arguments", {})
            model = args.get("model")
            if model:
                by_model[model][path] = {
                    "settings": args.get("model_settings", {}),
                    "cases": len(report.get("report", {}).get("cases", [])),
                }

    rows = []
    for model, items_by_path in sorted(by_model.items()):
        items = list(items_by_path.values())
        rows.append(
            {
                "modelo_juez": model,
                "n_reportes": len(items),
                "n_evaluaciones": sum(int(item["cases"]) for item in items),
                "settings_registrados": " | ".join(
                    sorted({_json_dumps(item["settings"]) for item in items})
                ),
                "temperature_en_payload_verificada": "no verificada en este artefacto",
                "reasoning_effort_registrado": "no",
                "nota": (
                    "Configuración de jueces en OpenRouter; no es la configuración "
                    "de los modelos generadores GPT-5 y no se usa para afirmar "
                    "determinismo de las respuestas evaluadas."
                ),
                "fuente": "codigo_experimentos/part_h_1/reports/",
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Ubicaciones y propuestas de edición
# ---------------------------------------------------------------------------

CLAIMS: list[dict[str, Any]] = [
    {
        "archivo": "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
        "buscar": "Se emplea la misma configuración de agente (Pydantic AI con temperatura 0) que en el baseline sin RAG, para mantener la comparabilidad.",
        "problema": "Presenta temperature=0 como configuración efectiva y como garantía de comparabilidad.",
        "propuesto": "Se emplea la misma configuración de agente (Pydantic AI) que en el baseline sin RAG para mantener la comparabilidad. En el código se solicitó `temperature=0.0`, pero la versión 1.1.0 de Pydantic AI elimina ese parámetro para los modelos GPT-5 antes de construir la solicitud; por tanto, no se la presenta como un control efectivo de reproducibilidad.",
        "alcance": "oración completa",
        "prioridad": "obligatoria",
    },
    {
        "archivo": "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
        "buscar": "La temperatura controla la aleatoriedad de las respuestas del modelo (0,0 = determinista).",
        "problema": "Afirma que 0,0 es determinista y sugiere que el valor fue aplicado.",
        "propuesto": "La temperatura es un parámetro de muestreo. En los modelos GPT-5 evaluados, el perfil de Pydantic AI 1.1.0 declara `temperature` como parámetro no admitido y la biblioteca lo elimina antes de construir la solicitud; el valor `0.0` figura en el código y en algunos registros, pero no fue aplicado. El esfuerzo de razonamiento no se registró y debe considerarse desconocido.",
        "alcance": "oración completa",
        "prioridad": "obligatoria",
    },
    {
        "archivo": "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
        "buscar": "| Temperatura                       |                       0,0                        |                        0,0                         |",
        "problema": "La tabla de hiperparámetros atribuye a los agentes una temperatura que el perfil GPT-5 elimina.",
        "propuesto": "| Temperatura solicitada en el código | 0,0#super[†] | 0,0#super[†] |",
        "alcance": "fila completa de tabla",
        "prioridad": "obligatoria",
    },
    {
        "archivo": "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
        "buscar": "+ Soporte para generación con temperatura cero (respuestas determinísticas).",
        "problema": "Incluye como criterio de selección una capacidad que los modelos GPT-5 no ofrecen.",
        "propuesto": "[Eliminar el ítem. Si se desea conservar una nota: «No se utilizó la temperatura como criterio de selección porque el perfil de Pydantic AI para los modelos GPT-5 no la admite»].",
        "alcance": "línea completa (eliminar)",
        "prioridad": "obligatoria",
    },
    {
        "archivo": "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
        "buscar": "Todos los modelos fueron configurados con temperatura 0 para maximizar la reproducibilidad de las respuestas.",
        "problema": "Atribuye a los tres modelos una configuración no aplicada y una garantía inexistente.",
        "propuesto": "Los tres modelos pertenecen a la familia GPT-5 y fueron invocados con los identificadores `gpt-5-nano`, `gpt-5-mini` y `gpt-5`. El código solicitó `temperature=0.0`, pero Pydantic AI 1.1.0 elimina ese parámetro para estos modelos antes de enviar la solicitud; por tanto, operaron con el muestreo predeterminado del proveedor. No se registró el esfuerzo de razonamiento. Se realizó una única ejecución por unidad y configuración, sin réplicas.",
        "alcance": "oración completa",
        "prioridad": "obligatoria",
    },
    {
        "archivo": "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
        "buscar": "+ Temperatura 0 para respuestas determinísticas (evita múltiples ejecuciones).",
        "problema": "Usa la temperatura para justificar la ausencia de réplicas.",
        "propuesto": "+ Una única ejecución por unidad y configuración, sin réplicas. La temperatura solicitada en el código no fue aplicada por los modelos GPT-5 y no se usa como garantía de determinismo.",
        "alcance": "línea completa",
        "prioridad": "obligatoria",
    },
    {
        "archivo": "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
        "buscar": "Los tres modelos fueron configurados con temperatura 0,0 y un límite de 5.000 tokens de salida.",
        "problema": "Mezcla la configuración de los jueces con la de los modelos generadores GPT-5.",
        "propuesto": "Los tres modelos jueces se configuraron en OpenRouter con `temperature=0.0` y un límite de 5.000 tokens de salida. Esa configuración corresponde a los jueces y no debe extrapolarse a los modelos generadores GPT-5, cuyo perfil elimina `temperature`. No se registró el esfuerzo de razonamiento de los jueces.",
        "alcance": "oración completa",
        "prioridad": "obligatoria",
    },
    {
        "archivo": "manuscrito/capitulos/07_capitulo_06_evaluacion.typ",
        "buscar": "El diseño experimental sigue un esquema factorial 3 × 3 detallado en el capítulo @cap:metodologia (@tabla-diseno-factorial): tres estrategias de recuperación (sin RAG, RAG básico, Agentic-RAG) × tres modelos de lenguaje (gpt-5-nano, gpt-5-mini, gpt-5), con temperatura 0 en todas las configuraciones para garantizar reproducibilidad.",
        "problema": "Convierte una solicitud del código en una garantía de reproducibilidad.",
        "propuesto": "El diseño experimental sigue un esquema factorial 3 × 3 detallado en el capítulo @cap:metodologia (@tabla-diseno-factorial): tres estrategias de recuperación (sin RAG, RAG básico, Agentic-RAG) × tres modelos de lenguaje (gpt-5-nano, gpt-5-mini, gpt-5), con una única ejecución por unidad y configuración. El código solicitó `temperature=0.0`, pero el perfil de Pydantic AI para los modelos GPT-5 no admite ese parámetro y la biblioteca lo elimina antes de la solicitud; por tanto, la configuración no garantiza determinismo ni reproducibilidad exacta.",
        "alcance": "oración completa",
        "prioridad": "obligatoria",
    },
    {
        "archivo": "codigo_experimentos/performed_tasks_summary.md",
        "buscar": "Uses Pydantic AI agents with temperature=0 for deterministic responses.",
        "problema": "Describe como deterministas unas respuestas que no tuvieron temperature aplicada.",
        "propuesto": "Uses Pydantic AI agents; the code requested `temperature=0`, but Pydantic AI 1.1.0 removes this setting for GPT-5 reasoning models. Responses are not assumed deterministic.",
        "alcance": "fragmento de la descripción de la tabla",
        "prioridad": "obligatoria",
    },
    {
        "archivo": "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
        "buscar": "La implementación se organizó en módulos independientes ejecutados como notebooks de Jupyter, lo que favorece la reproducibilidad y la iteración.",
        "problema": "Puede leerse como reproducibilidad exacta de las respuestas.",
        "propuesto": "La implementación se organizó en módulos independientes ejecutados como notebooks de Jupyter, lo que favorece la auditabilidad y la iteración sobre los artefactos; la reproducibilidad de las respuestas no está garantizada por la configuración de muestreo.",
        "alcance": "oración completa",
        "prioridad": "recomendada",
    },
    {
        "archivo": "manuscrito/capitulos/06_capitulo_05_metodologia.typ",
        "buscar": "La organización modular en notebooks independientes facilita la reproducibilidad y permite iterar sobre componentes específicos sin afectar al resto del sistema.",
        "problema": "Mismo riesgo: reproducibilidad del pipeline no equivale a determinismo de las respuestas.",
        "propuesto": "La organización modular en notebooks independientes facilita la reproducción del pipeline y la auditoría de los artefactos; no implica reproducibilidad exacta de las respuestas.",
        "alcance": "oración completa",
        "prioridad": "recomendada",
    },
]

README_ADDITION = (
    "> **Nota metodológica:** se realizó una única ejecución por unidad y configuración. "
    "El código solicitó `temperature=0.0`, pero Pydantic AI 1.1.0 elimina ese parámetro "
    "para los modelos GPT-5; por tanto, las respuestas no se consideran deterministas. "
    "Los análisis deben respetar el apareamiento por unidad y el anidamiento en casos."
)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def build_claim_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for claim in CLAIMS:
        path = REPO_ROOT / claim["archivo"]
        text = path.read_text(encoding="utf-8")
        offset = text.find(claim["buscar"])
        if offset < 0:
            raise ValueError(f"No se encontró el texto en {claim['archivo']}: {claim['buscar']!r}")
        line = _line_number(text, offset)
        current = text.splitlines()[line - 1].strip()
        rows.append(
            {
                "archivo": claim["archivo"],
                "linea": line,
                "alcance": claim["alcance"],
                "texto_actual": current,
                "texto_actual_coincidente": claim["buscar"],
                "problema": claim["problema"],
                "texto_propuesto": claim["propuesto"],
                "prioridad": claim["prioridad"],
                "nota": "No editar todavía: este CSV es una propuesta para revisión.",
            }
        )

    # Limitaciones: insertar un ítem nuevo después del ítem de ausencia de CoT.
    limitation_path = (
        REPO_ROOT
        / "manuscrito"
        / "capitulos"
        / "09_capitulo_08_conclusion_y_trabajos_futuros.typ"
    )
    limitation_text = limitation_path.read_text(encoding="utf-8")
    limitation_marker = (
        "+ *Ausencia de prompting de cadena de pensamiento (CoT) en los jueces LLM.*"
    )
    limitation_offset = limitation_text.find(limitation_marker)
    if limitation_offset < 0:
        raise ValueError("No se encontró el ítem de limitación sobre CoT")
    limitation_line = _line_number(limitation_text, limitation_offset)
    limitation_current = limitation_text.splitlines()[limitation_line - 1].strip()
    rows.append(
        {
            "archivo": "manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ",
            "linea": limitation_line,
            "alcance": "inserción después del ítem",
            "texto_actual": limitation_current,
            "texto_actual_coincidente": limitation_marker,
            "problema": "Falta declarar la ejecución única y la ausencia de un control efectivo de muestreo.",
            "texto_propuesto": "+ *Ejecución única y ausencia de control efectivo de muestreo.* Se realizó una única ejecución por unidad y configuración, sin réplicas. Aunque el código solicitó `temperature=0.0`, Pydantic AI 1.1.0 elimina ese parámetro para los modelos GPT-5 antes de construir la solicitud; por tanto, no puede afirmarse que las respuestas sean deterministas ni estimarse la variabilidad entre corridas. Tampoco se registró el esfuerzo de razonamiento, de modo que su valor histórico se desconoce. La estabilidad de las diferencias observadas debería verificarse con nuevas réplicas.",
            "prioridad": "obligatoria",
            "nota": "Insertar como nuevo ítem después de la limitación sobre CoT; no reemplazar el ítem existente.",
        }
    )
    rows.append(
        {
            "archivo": "README.md",
            "linea": 140,
            "alcance": "inserción después de la línea",
            "texto_actual": "[Insertar después de la línea de Análisis estadístico]",
            "texto_actual_coincidente": "[No existe; inserción nueva]",
            "problema": "El README no declara la ejecución única ni la diferencia entre reproducibilidad del pipeline y determinismo.",
            "texto_propuesto": README_ADDITION,
            "prioridad": "recomendada",
            "nota": "Inserción nueva; no reemplaza una línea existente.",
        }
    )
    return rows


# ---------------------------------------------------------------------------
# Figura
# ---------------------------------------------------------------------------


def build_figure(config_rows: list[dict[str, Any]], reasoning_rows: list[dict[str, Any]]) -> None:
    labels = {
        "sin_rag": "Sin RAG",
        "rag_basico": "RAG básico",
        "agentic_rag": "Agentic-RAG",
    }
    colors = {
        "gpt-5-nano": "#56B4E9",
        "gpt-5-mini": "#CC79A7",
        "gpt-5": "#D55E00",
    }
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), constrained_layout=True)

    for ax, role, title in [
        (axes[0], "especialista", "Modelo especialista"),
        (axes[1], "recuperador", "Agente de recuperación (gpt-5)"),
    ]:
        subset = [
            row
            for row in reasoning_rows
            if row["componente"] == role
            and (role == "especialista" or row["modelo_rol"] == "gpt-5")
        ]
        strategies = ["sin_rag", "rag_basico", "agentic_rag"] if role == "especialista" else ["agentic_rag"]
        x_base = np.arange(len(strategies))
        width = 0.24 if role == "especialista" else 0.5
        for idx, model in enumerate(MODELOS if role == "especialista" else ["gpt-5"]):
            vals = []
            for strategy in strategies:
                match = [
                    row
                    for row in subset
                    if row["estrategia"] == strategy and row["modelo_rol"] == model
                ]
                vals.append(match[0]["mediana"] if match else np.nan)
            positions = x_base + (idx - 1) * width if role == "especialista" else x_base
            ax.bar(
                positions,
                vals,
                width=width,
                label=model,
                color=colors[model],
                edgecolor="black",
                linewidth=0.5,
            )
        ax.set_xticks(x_base)
        ax.set_xticklabels([labels[s] for s in strategies])
        ax.set_ylabel("Tokens de razonamiento (mediana)")
        ax.set_title(title)
        ax.grid(axis="y", alpha=0.25)
        if role == "especialista":
            ax.legend(title="Modelo", fontsize=8)

    fig.suptitle(
        "Tokens de razonamiento registrados por celda\n"
        "No equivalen al esfuerzo de razonamiento solicitado ni al aplicado por el proveedor",
        fontsize=11,
    )
    for suffix in ["png", "pdf"]:
        fig.savefig(OUT_DIR / f"fig_tokens_razonamiento_por_celda.{suffix}", dpi=220)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Ejecución principal
# ---------------------------------------------------------------------------


def build_summary(
    manifest: dict[str, Any],
    config_rows: list[dict[str, Any]],
    reasoning_rows: list[dict[str, Any]],
    execution_rows: list[dict[str, Any]],
    judge_rows: list[dict[str, Any]],
    pydantic_evidence: dict[str, Any],
    reasoning_effort: dict[str, Any],
) -> dict[str, Any]:
    return {
        "fecha_ejecucion_utc": datetime.now(timezone.utc).isoformat(),
        "manifest": manifest,
        "pydantic_ai": {
            "version": pydantic_evidence["pydantic_ai_version"],
            "perfiles": pydantic_evidence["perfiles"],
            "captura_payload": pydantic_evidence["captura_payload"],
        },
        "reasoning_effort": {
            "ocurrencias": len(
                reasoning_effort[
                    "ocurrencias_de_reasoning_effort_o_reasoning_igual"
                ]
            ),
            "respuestas_primarias": reasoning_effort["n_respuestas_primarias"],
            "respuestas_con_reasoning_tokens": reasoning_effort[
                "n_respuestas_con_reasoning_tokens"
            ],
            "conclusion": reasoning_effort["conclusion"],
        },
        "tablas": {
            "configuracion": len(config_rows),
            "reasoning": len(reasoning_rows),
            "ejecuciones": len(execution_rows),
            "jueces": len(judge_rows),
            "ubicaciones_texto": len(build_claim_rows()),
        },
        "hallazgos_clave": [
            "Pydantic AI 1.1.0 declara temperature como setting no admitido para gpt-5-nano, gpt-5-mini y gpt-5.",
            "La captura local confirma que temperature no se incluye en el cuerpo Chat Completions.",
            "Los logs no son volcados HTTP: no-RAG/RAG registran temperature=0.0; Agentic-RAG registra {}.",
            "No hay reasoning_effort explícito en el código de generación ni en los logs revisados.",
            "Todas las respuestas primarias tienen reasoning_tokens, pero eso no identifica el esfuerzo aplicado.",
            "Cada celda tiene 79 registros para 79 unidades y no existe un campo de réplica.",
        ],
    }


def main() -> dict[str, Any]:
    print("1/8 Manifiesto de entradas...")
    manifest = build_manifest()

    print("2/8 Carga de respuestas primarias...")
    data = load_primary_data()
    records = list(primary_records(data))
    if len(records) != 711:
        raise AssertionError(f"Se esperaban 711 respuestas primarias, hay {len(records)}")

    print("3/8 Captura local de payloads (sin red)...")
    payloads = _run_coroutine(_capture_all_payloads())
    write_json(OUT_DIR / "evidencia_payloads_locales.json", payloads)

    print("4/8 Evidencia de Pydantic AI...")
    pydantic_evidence = build_pydantic_evidence(payloads)

    print("5/8 Evidencia de esfuerzo de razonamiento...")
    reasoning_effort = build_reasoning_effort_evidence(data)

    print("6/8 Tablas derivadas...")
    config_rows = build_config_table(
        data, payloads, pydantic_evidence["perfiles"]
    )
    reasoning_rows = build_reasoning_table(data)
    execution_rows = build_execution_table(data)
    judge_rows = build_judge_table()
    claim_rows = build_claim_rows()

    write_csv(OUT_DIR / "tabla_configuracion_solicitado_registrado_efectivo.csv", config_rows)
    write_csv(OUT_DIR / "tabla_reasoning_tokens_por_celda.csv", reasoning_rows)
    write_csv(OUT_DIR / "tabla_ejecuciones_unicas.csv", execution_rows)
    write_csv(OUT_DIR / "tabla_parametros_jueces.csv", judge_rows)
    write_csv(OUT_DIR / "tabla_ubicaciones_texto_a_modificar.csv", claim_rows)

    print("7/8 Figura...")
    build_figure(config_rows, reasoning_rows)

    print("8/8 Resumen...")
    summary = build_summary(
        manifest,
        config_rows,
        reasoning_rows,
        execution_rows,
        judge_rows,
        pydantic_evidence,
        reasoning_effort,
    )
    write_json(OUT_DIR / "resumen_evidencia.json", summary)
    print("Listo. Artefactos en:", OUT_DIR)
    return summary


if __name__ == "__main__":
    main()

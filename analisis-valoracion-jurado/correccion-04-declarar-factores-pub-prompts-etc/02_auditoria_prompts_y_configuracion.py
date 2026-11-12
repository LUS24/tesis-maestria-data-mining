#!/usr/bin/env python3
"""Auditoría read-only de prompts y configuración para IX.1.4.

Uso recomendado, desde `codigo_experimentos/` para disponer de pydantic-evals:
    uv run --no-sync --frozen python \
      ../analisis-valoracion-jurado/correccion-04-declarar-factores-pub-prompts-etc/02_auditoria_prompts_y_configuracion.py

El script NO modifica archivos del repositorio. Solo escribe dentro de esta
carpeta de corrección:
  - salidas/*.json, *.csv
  - propuestas/anexo_02_prompts_y_parametros.typ

Fuentes principales:
  - codigo_experimentos/part_g/01_generate_responses_using_agents.py
  - codigo_experimentos/part_g/01_generate_responses_using_agents.ipynb
  - codigo_experimentos/part_g/chat_data/*/*/law_specialist_agent.json
  - codigo_experimentos/part_g/chat_data/*/*/retrieval_agent.json
  - codigo_experimentos/part_e/02_query_llms_for_responses.ipynb
  - codigo_experimentos/part_f/01_rag_llm_responses.ipynb
  - codigo_experimentos/part_h_1/01_llm_as_a_judge*.ipynb
  - codigo_experimentos/part_h_1/reports/**/*.json
"""

from __future__ import annotations

import ast
import csv
import difflib
import hashlib
import importlib.metadata as importlib_metadata
import inspect
import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic_evals.evaluators import llm_as_a_judge as judge_module


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXP = ROOT / "codigo_experimentos"
CHAT = EXP / "part_g" / "chat_data"
OUT = HERE / "salidas"
PROP = HERE / "propuestas"
OUT.mkdir(parents=True, exist_ok=True)
PROP.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "agent_script": EXP / "part_g" / "01_generate_responses_using_agents.py",
    "agent_notebook": EXP / "part_g" / "01_generate_responses_using_agents.ipynb",
    "no_rag_notebook": EXP / "part_e" / "02_query_llms_for_responses.ipynb",
    "base_rag_notebook": EXP / "part_f" / "01_rag_llm_responses.ipynb",
    "judge_notebook": EXP / "part_h_1" / "01_llm_as_a_judge.ipynb",
    "judge_batch_2_notebook": EXP / "part_h_1" / "01_llm_as_a_judge_batch_2.ipynb",
}


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return ""


def notebook_source(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    return "\n\n".join(
        "".join(cell.get("source", []))
        for cell in data.get("cells", [])
        if cell.get("cell_type") == "code"
    )


def extract_assignment(source: str, name: str, env: dict[str, Any] | None = None) -> Any:
    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name
            for target in node.targets
        ):
            expression = ast.Expression(node.value)
            ast.fix_missing_locations(expression)
            return eval(compile(expression, "<prompt-source>", "eval"), env or {})
    raise KeyError(f"No se encontró la asignación {name!r}")


def extract_notebook_prompt(path: Path, name: str = "system_prompt") -> str:
    source = notebook_source(path)
    value = extract_assignment(source, name)
    if not isinstance(value, str):
        raise TypeError(f"{name!r} no es str en {path}")
    return value


def extract_agent_instructions(path: Path) -> dict[str, str]:
    source = path.read_text(encoding="utf-8")
    # El f-string del recuperador se evalúa con el valor histórico/canónico actual.
    env = {"VECTOR_SEARCH_LIMIT": "UsageLimits(tool_calls_limit=6)"}
    result = extract_assignment(source, "INSTRUCTIONS", env)
    if not isinstance(result, dict):
        raise TypeError("INSTRUCTIONS no es un dict")
    return result


def parse_limit(prompt: str) -> int | None:
    match = re.search(r"tool_calls_limit=(\d+)", prompt)
    return int(match.group(1)) if match else None


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def judge_rubrics_from_reports() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    """Devuelve rúbricas únicas y especificaciones de jueces desde los 27 reportes."""
    report_paths = sorted((EXP / "part_h_1" / "reports").glob("*/*.json"))
    if not report_paths:
        raise FileNotFoundError("No se encontraron reportes de jueces")

    rubric_by_name: dict[str, dict[str, Any]] = {}
    judge_specs: dict[str, dict[str, Any]] = {}
    for path in report_paths:
        report = load_json(path)
        for evaluator in report.get("evaluators", []):
            args = evaluator.get("arguments", {})
            rubric = args.get("rubric")
            if not isinstance(rubric, dict):
                continue
            name = rubric.get("nombre_evaluacion")
            if not name:
                continue
            rubric_by_name.setdefault(name, rubric)
            if compact_json(rubric_by_name[name]) != compact_json(rubric):
                raise ValueError(f"Rúbrica inconsistente para {name} en {path}")

            model = args.get("model")
            if model:
                spec = {
                    "model": model,
                    "include_input": args.get("include_input"),
                    "include_expected_output": args.get("include_expected_output"),
                    "model_settings": args.get("model_settings"),
                    "score": args.get("score"),
                    "assertion": args.get("assertion"),
                    "rubric_name": name,
                }
                key = compact_json(spec)
                judge_specs.setdefault(key, spec)

    wanted = ["respuesta_correcta", "precision_legal"]
    missing = [name for name in wanted if name not in rubric_by_name]
    if missing:
        raise KeyError(f"Faltan rúbricas: {missing}")
    specs = sorted(
        judge_specs.values(),
        key=lambda spec: (str(spec.get("model")), str(spec.get("rubric_name"))),
    )
    return [rubric_by_name[name] for name in wanted], specs, report_paths


def judge_templates(rubrics: list[dict[str, Any]]) -> tuple[str, dict[str, str], str]:
    """Reconstruye el prompt exacto de pydantic-evals 1.1.0.

    LLMJudge se configuró con include_input=True e include_expected_output=True,
    por lo que utiliza el agente `judge_input_output_expected`.
    """
    agent = judge_module._judge_input_output_expected_agent  # type: ignore[attr-defined]
    system_prompt = agent._system_prompts[0]  # type: ignore[attr-defined]
    templates = {}
    for rubric in rubrics:
        name = rubric["nombre_evaluacion"]
        templates[name] = judge_module._build_prompt(  # type: ignore[attr-defined]
            inputs="⟦PREGUNTA⟧",
            output="⟦RESPUESTA⟧",
            rubric=rubric,
            expected_output="⟦RESPUESTA_ESPERADA⟧",
        )
    source_file = Path(inspect.getsourcefile(judge_module) or "")
    return system_prompt, templates, str(source_file)


def main() -> None:
    instructions = extract_agent_instructions(SOURCES["agent_script"])
    notebook_instructions = extract_assignment(
        notebook_source(SOURCES["agent_notebook"]), "INSTRUCTIONS"
    )
    if not isinstance(notebook_instructions, dict):
        raise TypeError("INSTRUCTIONS del notebook no es un dict")

    no_rag_prompt = extract_notebook_prompt(SOURCES["no_rag_notebook"])
    base_rag_prompt = extract_notebook_prompt(SOURCES["base_rag_notebook"])

    law_logs = sorted(CHAT.glob("*/*/law_specialist_agent.json"))
    retrieval_logs = sorted(CHAT.glob("*/*/retrieval_agent.json"))
    if not law_logs or not retrieval_logs:
        raise FileNotFoundError("No se encontraron logs agénticos")

    law_instruction_variants: dict[str, str] = {}
    retrieval_instruction_variants: dict[str, str] = {}
    session_rows: list[dict[str, Any]] = []

    for law_path in law_logs:
        model_dir = law_path.parts[-3]
        case_dir = law_path.parent.name
        law_log = load_json(law_path)
        retrieval_path = law_path.parent / "retrieval_agent.json"
        retrieval_log = load_json(retrieval_path)

        law_instructions = [
            message.get("instructions")
            for message in law_log.get("messages", [])
            if message.get("kind") == "request" and message.get("instructions")
        ]
        retrieval_instructions = [
            message.get("instructions")
            for message in retrieval_log.get("messages", [])
            if message.get("kind") == "request" and message.get("instructions")
        ]
        if not law_instructions or not retrieval_instructions:
            raise ValueError(f"Faltan instrucciones en {law_path}")

        for text in law_instructions:
            law_instruction_variants.setdefault(sha256(text), text)
        for text in retrieval_instructions:
            retrieval_instruction_variants.setdefault(sha256(text), text)

        law_calls = [
            part
            for message in law_log.get("messages", [])
            if message.get("kind") == "response"
            for part in message.get("parts", [])
            if part.get("part_kind") == "tool-call"
            and part.get("tool_name") == "retrieve_relevant_documents"
        ]
        retrieval_calls = [
            part
            for message in retrieval_log.get("messages", [])
            if message.get("kind") == "response"
            for part in message.get("parts", [])
            if part.get("part_kind") == "tool-call"
            and part.get("tool_name") == "cosine_distance_vector_search"
        ]
        finish_reasons = [
            message.get("finish_reason") or "null"
            for message in retrieval_log.get("messages", [])
            if message.get("kind") == "response"
        ]

        retrieval_prompt = retrieval_instructions[-1]
        retrieval_hash = sha256(retrieval_prompt)
        session_rows.append(
            {
                "modelo_especialista": model_dir.removeprefix("openai_").replace("_", "-"),
                "caso": case_dir,
                "law_timestamp": law_log.get("metadata", {}).get("timestamp", ""),
                "retrieval_timestamp": retrieval_log.get("metadata", {}).get("timestamp", ""),
                "law_prompt_hash": sha256(law_instructions[-1]),
                "retrieval_prompt_hash": retrieval_hash,
                "retrieval_limit_declarado": parse_limit(retrieval_prompt),
                "law_tool_calls": len(law_calls),
                "retrieval_search_calls": len(retrieval_calls),
                "retrieval_finish_reasons": "|".join(finish_reasons),
                "quality_agent_logs": int((law_path.parent / "retrieval_quality_agent.json").exists()),
            }
        )

    if len(law_instruction_variants) != 1:
        raise ValueError("Se esperaba una sola variante del prompt del especialista")
    law_prompt_hash, law_prompt = next(iter(law_instruction_variants.items()))
    if law_prompt_hash != sha256(instructions["law_specialist_agent"]):
        raise ValueError("El prompt del especialista no coincide con el script final")

    # Dos variantes históricas del prompt del recuperador. La de 6 coincide con
    # el script actual; la de 7 fue usada por la corrida de gpt-5.
    if len(retrieval_instruction_variants) != 2:
        raise ValueError("Se esperaban dos variantes del prompt del recuperador")
    retrieval_by_limit = {
        parse_limit(text): (digest, text)
        for digest, text in retrieval_instruction_variants.items()
    }
    if set(retrieval_by_limit) != {6, 7}:
        raise ValueError(f"Límites inesperados: {sorted(retrieval_by_limit)}")
    ret6_hash, ret6 = retrieval_by_limit[6]
    ret7_hash, ret7 = retrieval_by_limit[7]
    if ret6_hash != sha256(instructions["retrieval_agent"]):
        raise ValueError("La variante de 6 no coincide con el script final")

    quality_prompt = instructions["retrieval_quality_agent"]
    quality_hash = sha256(quality_prompt)
    quality_logs = sorted(CHAT.glob("*/*/retrieval_quality_agent.json"))

    rubrics, judge_specs, report_paths = judge_rubrics_from_reports()
    judge_system_prompt, judge_template_by_rubric, judge_source_file = judge_templates(rubrics)

    # Agregados por modelo.
    by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in session_rows:
        by_model[row["modelo_especialista"]].append(row)

    model_summary: dict[str, Any] = {}
    for model, rows in sorted(by_model.items()):
        hashes = Counter(row["retrieval_prompt_hash"] for row in rows)
        model_summary[model] = {
            "sesiones": len(rows),
            "prompt_variants": {
                digest: {
                    "sesiones": count,
                    "limite_declarado": parse_limit(retrieval_instruction_variants[digest]),
                }
                for digest, count in hashes.items()
            },
            "retrieval_search_calls": dict(sorted(Counter(row["retrieval_search_calls"] for row in rows).items())),
            "law_tool_calls": dict(sorted(Counter(row["law_tool_calls"] for row in rows).items())),
            "fecha_min": min(row["retrieval_timestamp"] for row in rows),
            "fecha_max": max(row["retrieval_timestamp"] for row in rows),
        }

    anomalies = {
        "sesiones_con_mas_de_un_law_call": [
            row for row in session_rows if row["law_tool_calls"] > 1
        ],
        "sesiones_gpt5_con_7_busquedas": sum(
            1
            for row in session_rows
            if row["modelo_especialista"] == "gpt-5" and row["retrieval_search_calls"] > 6
        ),
        "sesiones_restantes_con_mas_de_6_busquedas": sum(
            1
            for row in session_rows
            if row["modelo_especialista"] != "gpt-5" and row["retrieval_search_calls"] > 6
        ),
    }

    prompt_entries = [
        {
            "id": "sin_rag_system",
            "kind": "system",
            "strategy": "sin_rag",
            "component": "generador",
            "source": "codigo_experimentos/part_e/02_query_llms_for_responses.ipynb",
            "source_lines": "67-71 (celda de código; valor de system_prompt)",
            "status": "fuente_sin_logs_de_entrada",
            "evidence": "Texto tomado del notebook que generó las respuestas; los JSON de salida no conservan el prompt de entrada.",
            "sha256": sha256(no_rag_prompt),
            "chars": len(no_rag_prompt),
            "text": no_rag_prompt,
        },
        {
            "id": "rag_basico_system_template",
            "kind": "system_template",
            "strategy": "rag_basico",
            "component": "generador",
            "source": "codigo_experimentos/part_f/01_rag_llm_responses.ipynb",
            "source_lines": "120-129 (celda de código; valor de system_prompt)",
            "status": "fuente_sin_logs_de_entrada",
            "evidence": "Plantilla del notebook; {retrieved_data} se sustituye por la representación Python de la lista de hasta diez documentos.",
            "sha256": sha256(base_rag_prompt),
            "chars": len(base_rag_prompt),
            "text": base_rag_prompt,
        },
        {
            "id": "especialista_legal_system",
            "kind": "system",
            "strategy": "agentic_rag",
            "component": "especialista_legal",
            "source": "codigo_experimentos/part_g/01_generate_responses_using_agents.py",
            "source_lines": "141-152",
            "status": "observado_en_logs",
            "evidence": "Una única variante en 237 sesiones y 476 solicitudes; coincide con INSTRUCTIONS['law_specialist_agent'] del script final.",
            "sha256": law_prompt_hash,
            "chars": len(law_prompt),
            "text": law_prompt,
        },
        {
            "id": "recuperador_system_6",
            "kind": "system",
            "strategy": "agentic_rag",
            "component": "agente_recuperacion",
            "source": "codigo_experimentos/part_g/chat_data/**/retrieval_agent.json",
            "source_lines": "Instrucción registrada; coincide con el script final, líneas 153-161",
            "status": "observado_en_logs",
            "evidence": "158 sesiones de gpt-5-mini y gpt-5-nano; 653 solicitudes; límite declarado 6.",
            "sha256": ret6_hash,
            "chars": len(ret6),
            "text": ret6,
        },
        {
            "id": "recuperador_system_7_gpt5",
            "kind": "system",
            "strategy": "agentic_rag",
            "component": "agente_recuperacion",
            "source": "codigo_experimentos/part_g/chat_data/openai_gpt-5/**/retrieval_agent.json",
            "source_lines": "Instrucción registrada en la corrida histórica de gpt-5",
            "status": "observado_en_logs",
            "evidence": "79 sesiones de gpt-5, 12 de noviembre de 2025; 345 solicitudes; límite declarado 7. No coincide con el script actual, que declara 6.",
            "sha256": ret7_hash,
            "chars": len(ret7),
            "text": ret7,
        },
        {
            "id": "calidad_recuperacion_system_no_ejecutado",
            "kind": "system",
            "strategy": "agentic_rag",
            "component": "agente_calidad",
            "source": "codigo_experimentos/part_g/01_generate_responses_using_agents.py",
            "source_lines": "162-168",
            "status": "definido_no_ejecutado",
            "evidence": "0 archivos retrieval_quality_agent.json y 0 llamadas a evaluate_retrieval en 237 sesiones. El agente se instancia sin herramientas; su prompt nunca se envió a un modelo.",
            "sha256": quality_hash,
            "chars": len(quality_prompt),
            "text": quality_prompt,
        },
        {
            "id": "juez_sistema",
            "kind": "judge_system",
            "strategy": "evaluacion",
            "component": "tres_jueces",
            "source": f"{Path(judge_source_file).relative_to(ROOT)} (pydantic-evals 1.1.0)",
            "source_lines": "Agente judge_input_output_expected",
            "status": "generado_por_libreria",
            "evidence": "Prompt de sistema constante para los tres jueces; include_input=True e include_expected_output=True.",
            "sha256": sha256(judge_system_prompt),
            "chars": len(judge_system_prompt),
            "text": judge_system_prompt,
        },
        {
            "id": "juez_respuesta_correcta_template",
            "kind": "judge_user_template",
            "strategy": "evaluacion",
            "component": "rubrica_respuesta_correcta",
            "source": "codigo_experimentos/part_h_1/01_llm_as_a_judge.ipynb y batch_2",
            "source_lines": "79-124 (definición de LLMJudge y rúbricas)",
            "status": "generado_por_libreria",
            "evidence": "Plantilla exacta construida con _build_prompt de pydantic-evals 1.1.0; los placeholders se sustituyen por pregunta, respuesta y respuesta esperada.",
            "sha256": sha256(judge_template_by_rubric["respuesta_correcta"]),
            "chars": len(judge_template_by_rubric["respuesta_correcta"]),
            "text": judge_template_by_rubric["respuesta_correcta"],
        },
        {
            "id": "juez_precision_legal_template",
            "kind": "judge_user_template",
            "strategy": "evaluacion",
            "component": "rubrica_precision_legal",
            "source": "codigo_experimentos/part_h_1/01_llm_as_a_judge.ipynb y batch_2",
            "source_lines": "79-124 (definición de LLMJudge y rúbricas)",
            "status": "generado_por_libreria",
            "evidence": "Plantilla exacta construida con _build_prompt de pydantic-evals 1.1.0; los placeholders se sustituyen por pregunta, respuesta y respuesta esperada.",
            "sha256": sha256(judge_template_by_rubric["precision_legal"]),
            "chars": len(judge_template_by_rubric["precision_legal"]),
            "text": judge_template_by_rubric["precision_legal"],
        },
    ]

    prompt_by_id = {entry["id"]: entry for entry in prompt_entries}
    assert prompt_by_id["recuperador_system_6"]["sha256"] == ret6_hash
    assert prompt_by_id["recuperador_system_7_gpt5"]["sha256"] == ret7_hash

    config_rows = [
        {
            "configuracion": "Sin RAG",
            "componente": "Generador",
            "modelo": "gpt-5-nano / gpt-5-mini / gpt-5",
            "prompt_id": "sin_rag_system",
            "limite_herramientas": "sin herramientas",
            "evidencia": "Notebook de part_e; no hay logs de mensajes de entrada",
        },
        {
            "configuracion": "RAG básico",
            "componente": "Generador",
            "modelo": "gpt-5-nano / gpt-5-mini / gpt-5",
            "prompt_id": "rag_basico_system_template",
            "limite_herramientas": "sin herramientas; top-10 en una búsqueda",
            "evidencia": "Notebook de part_f; no hay logs de mensajes de entrada",
        },
        {
            "configuracion": "Agentic-RAG + gpt-5",
            "componente": "Especialista Legal",
            "modelo": "gpt-5",
            "prompt_id": "especialista_legal_system",
            "limite_herramientas": "1 nominal; una sesión registra 3 llamadas",
            "evidencia": "237 logs; caso 16_01 es la excepción",
        },
        {
            "configuracion": "Agentic-RAG + gpt-5",
            "componente": "Agente de Recuperación",
            "modelo": "gpt-5",
            "prompt_id": "recuperador_system_7_gpt5",
            "limite_herramientas": "7; 33/79 sesiones usaron 7 búsquedas",
            "evidencia": "79 sesiones del 12-11-2025",
        },
        {
            "configuracion": "Agentic-RAG + gpt-5-mini",
            "componente": "Agente de Recuperación",
            "modelo": "gpt-5",
            "prompt_id": "recuperador_system_6",
            "limite_herramientas": "6",
            "evidencia": "79 sesiones del 13-11-2025",
        },
        {
            "configuracion": "Agentic-RAG + gpt-5-nano",
            "componente": "Agente de Recuperación",
            "modelo": "gpt-5",
            "prompt_id": "recuperador_system_6",
            "limite_herramientas": "6",
            "evidencia": "79 sesiones del 13-11-2025",
        },
        {
            "configuracion": "Agentic-RAG (todas)",
            "componente": "Agente de Calidad",
            "modelo": "gpt-5 (definido)",
            "prompt_id": "calidad_recuperacion_system_no_ejecutado",
            "limite_herramientas": "sin herramientas; no ejecutado",
            "evidencia": "0 logs y 0 llamadas; exclusión confirmada por el autor por costo y complejidad",
        },
    ]

    for row in config_rows:
        assert row["prompt_id"] in prompt_by_id

    diff_chunks = []
    for key in ["law_specialist_agent", "retrieval_agent", "retrieval_quality_agent"]:
        diff_chunks.extend(
            difflib.unified_diff(
                str(notebook_instructions[key]).splitlines(),
                str(instructions[key]).splitlines(),
                fromfile=f"notebook:{key}",
                tofile=f"script_final:{key}",
                lineterm="",
            )
        )
    (OUT / "diff_prompts_script_vs_notebook.diff").write_text(
        "\n".join(diff_chunks) + "\n", encoding="utf-8"
    )
    notebook_prompts_match_script = {
        key: notebook_instructions[key] == instructions[key]
        for key in ["law_specialist_agent", "retrieval_agent", "retrieval_quality_agent"]
    }

    generated_at = datetime.now(timezone.utc).isoformat()
    source_inventory = {
        name: {
            "path": str(path.relative_to(ROOT)),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for name, path in SOURCES.items()
    }
    source_inventory["judge_library_source"] = {
        "path": str(Path(judge_source_file).relative_to(ROOT)),
        "sha256": sha256_file(Path(judge_source_file)),
        "bytes": Path(judge_source_file).stat().st_size,
    }

    payload = {
        "metadata": {
            "generated_at_utc": generated_at,
            "repo_commit": git("rev-parse", "HEAD"),
            "repo_branch": git("branch", "--show-current"),
            "tracked_dirty_files": [
                path
                for path in git("diff", "--name-only").splitlines()
                if path
            ],
            "pydantic_ai_version": importlib_metadata.version("pydantic-ai-slim"),
            "pydantic_evals_version": importlib_metadata.version("pydantic-evals"),
            "python": os.sys.version.split()[0],
        },
        "prompts": prompt_entries,
        "observed_configuration": config_rows,
        "agent_log_summary": model_summary,
        "anomalies": anomalies,
        "judge_reports": {
            "count": len(report_paths),
            "by_judge": dict(sorted(Counter(path.parent.name for path in report_paths).items())),
            "evaluator_specs": judge_specs,
            "rubrics": rubrics,
        },
        "source_inventory": source_inventory,
    }
    (OUT / "prompts_canonicos.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    with (OUT / "inventario_prompts.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "id",
                "kind",
                "strategy",
                "component",
                "sha256",
                "chars",
                "source",
                "source_lines",
                "status",
                "evidence",
            ],
        )
        writer.writeheader()
        for entry in prompt_entries:
            writer.writerow({key: entry.get(key, "") for key in writer.fieldnames})

    with (OUT / "configuracion_observada.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(config_rows[0]))
        writer.writeheader()
        writer.writerows(config_rows)

    with (OUT / "sesiones_agentic.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(session_rows[0]))
        writer.writeheader()
        writer.writerows(session_rows)

    variant_rows = []
    for model, rows in sorted(by_model.items()):
        for digest, count in sorted(Counter(row["retrieval_prompt_hash"] for row in rows).items()):
            subset = [row for row in rows if row["retrieval_prompt_hash"] == digest]
            variant_rows.append(
                {
                    "modelo": model,
                    "prompt_id": "recuperador_system_" + str(parse_limit(retrieval_instruction_variants[digest])),
                    "sha256": digest,
                    "sesiones": count,
                    "limite_declarado": parse_limit(retrieval_instruction_variants[digest]),
                    "fecha_min": min(row["retrieval_timestamp"] for row in subset),
                    "fecha_max": max(row["retrieval_timestamp"] for row in subset),
                    "retrieval_calls_min": min(row["retrieval_search_calls"] for row in subset),
                    "retrieval_calls_max": max(row["retrieval_search_calls"] for row in subset),
                }
            )
    with (OUT / "variantes_prompts_agente.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(variant_rows[0]))
        writer.writeheader()
        writer.writerows(variant_rows)

    summary = {
        "metadata": payload["metadata"],
        "law_logs": len(law_logs),
        "retrieval_logs": len(retrieval_logs),
        "law_prompt_variants": len(law_instruction_variants),
        "retrieval_prompt_variants": len(retrieval_instruction_variants),
        "quality_agent_logs": len(quality_logs),
        "quality_agent_calls": 0,
        "judge_reports": len(report_paths),
        "notebook_prompts_match_script": notebook_prompts_match_script,
        "agent_log_summary": model_summary,
        "anomalies": anomalies,
    }
    (OUT / "resumen_auditoria.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT / "hashes_fuentes.json").write_text(
        json.dumps(source_inventory, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    build_appendix(prompt_by_id, model_summary, judge_specs, generated_at)
    print(f"OK: artefactos generados en {OUT}")
    print(f"OK: anexo generado en {PROP / 'anexo_02_prompts_y_parametros.typ'}")


def typst_string(text: str) -> str:
    """Serializa un string a un literal de Typst, preservando contenido."""
    return (
        '"'
        + text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r\n", "\\n")
        .replace("\r", "\\n")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
        + '"'
    )


def short_hash(value: str) -> str:
    return value[:16]


def build_appendix(
    prompts: dict[str, dict[str, Any]],
    model_summary: dict[str, Any],
    judge_specs: list[dict[str, Any]],
    generated_at: str,
) -> None:
    p_sin = prompts["sin_rag_system"]
    p_rag = prompts["rag_basico_system_template"]
    p_law = prompts["especialista_legal_system"]
    p_ret6 = prompts["recuperador_system_6"]
    p_ret7 = prompts["recuperador_system_7_gpt5"]
    p_quality = prompts["calidad_recuperacion_system_no_ejecutado"]
    p_judge_sys = prompts["juez_sistema"]
    p_judge_correct = prompts["juez_respuesta_correcta_template"]
    p_judge_legal = prompts["juez_precision_legal_template"]

    def meta(entry: dict[str, Any], status: str | None = None) -> str:
        return (
            f"Fuente: `{entry['source']}`. "
            f"SHA-256: `{entry['sha256']}`. "
            f"Estado: {status or entry['status'].replace('_', ' ')}."
        )

    def block(prompt_id: str, entry: dict[str, Any], status: str | None = None) -> str:
        return f"""#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_{prompt_id})
  ],
)
#text(size: 8pt)[{meta(entry, status)}]
"""

    judge_rows = "\n".join(
        f"      | `{spec['model']}` | `{spec['rubric_name']}` | {spec.get('model_settings', {}).get('temperature', '—')} | {spec.get('model_settings', {}).get('max_tokens', '—')} |"
        for spec in judge_specs
    )

    appendix = f"""// ARCHIVO GENERADO POR 02_auditoria_prompts_y_configuracion.py.
// Revisar antes de incorporarlo al manuscrito. No editar a mano sin actualizar
// el script y volver a ejecutarlo.
#import "@preview/tablem:0.3.0": three-line-table
#show table: set text(size: 8.5pt)

#let prompt_sin_rag_system = {typst_string(p_sin['text'])}
#let prompt_rag_basico_system_template = {typst_string(p_rag['text'])}
#let prompt_especialista_legal_system = {typst_string(p_law['text'])}
#let prompt_recuperador_system_6 = {typst_string(p_ret6['text'])}
#let prompt_recuperador_system_7_gpt5 = {typst_string(p_ret7['text'])}
#let prompt_calidad_recuperacion_system_no_ejecutado = {typst_string(p_quality['text'])}
#let prompt_juez_sistema = {typst_string(p_judge_sys['text'])}
#let prompt_juez_respuesta_correcta_template = {typst_string(p_judge_correct['text'])}
#let prompt_juez_precision_legal_template = {typst_string(p_judge_legal['text'])}

= Prompts y configuración experimental <anexo-prompts>

Este anexo documenta los prompts y la configuración observada en la versión evaluada. Su finalidad es hacer trazable qué instrucciones recibió cada componente y distinguir la configuración nominal del código de la configuración que efectivamente produjo las respuestas.

#block(
  width: 100%,
  inset: 8pt,
  stroke: 0.5pt + luma(180),
  radius: 3pt,
  [
    *Convención de transcripción.* Los textos se reproducen sin correcciones de estilo. Los saltos de línea que aparecen en la composición son ajustes de página; el contenido canónico y su SHA-256 están registrados en `salidas/prompts_canonicos.json`. Cuando un prompt contiene un marcador entre llaves, se indica en el texto.
  ],
)

== Configuración observada

La @tabla-configuracion-observada distingue los componentes activos, el modelo que los ejecutó y el límite de recuperación registrado. La configuración no fue simétrica entre modelos: la corrida de gpt-5 utilizó una variante del prompt del recuperador con límite 7 y las corridas de gpt-5-mini y gpt-5-nano utilizaron la variante con límite 6.

#figure(
  three-line-table(
    columns: (3.6cm, 3.0cm, 2.3cm, 1fr),
    [
      | *Configuración* | *Componente* | *Modelo* | *Prompt y límite observados* |
      | :--- | :--- | :--- | :--- |
      | Sin RAG | Generador | variable | `sin_rag_system`; sin herramientas ni recuperación. |
      | RAG básico | Generador | variable | `rag_basico_system_template`; top-10 en una búsqueda, sin herramientas. |
      | Agentic-RAG + gpt-5 | Especialista Legal | gpt-5 | `especialista_legal_system`; una invocación nominal de recuperación. |
      | Agentic-RAG + gpt-5 | Agente de Recuperación | gpt-5 | `recuperador_system_7_gpt5`; hasta 7 búsquedas. |
      | Agentic-RAG + gpt-5-mini | Agente de Recuperación | gpt-5 | `recuperador_system_6`; hasta 6 búsquedas. |
      | Agentic-RAG + gpt-5-nano | Agente de Recuperación | gpt-5 | `recuperador_system_6`; hasta 6 búsquedas. |
      | Agentic-RAG, todas | Agente de Calidad | gpt-5 definido | `calidad_recuperacion_system_no_ejecutado`; definido, sin herramientas y nunca ejecutado. |
    ],
  ),
  caption: [Configuración observada de prompts y modelos. El modelo consignado para el Agente de Recuperación es siempre gpt-5; el factor «modelo» identifica al generador de la respuesta.],
) <tabla-configuracion-observada>

== Prompts de generación

=== Sin RAG

{block('sin_rag_system', p_sin)}

=== RAG básico

El marcador `{{retrieved_data}}` se sustituye por la representación Python de la lista de hasta diez documentos recuperados, conservando los campos `codigo_norma`, `tipo_parte`, `numero_parte`, `ultimo_estado`, `contenido_texto`, `index` y `distance`.

{block('rag_basico_system_template', p_rag)}

=== Agente Especialista Legal

El texto siguiente coincide con la única variante registrada en las 237 sesiones agénticas.

{block('especialista_legal_system', p_law)}

=== Agente de Recuperación

El Agente de Recuperación tuvo dos variantes. La primera se usó en la corrida de gpt-5 del 12 de noviembre de 2025; la segunda, en las corridas de gpt-5-mini y gpt-5-nano del 13 de noviembre de 2025. El texto contiene la representación literal del objeto `UsageLimits` porque el prompt se construyó interpolando ese objeto en un f-string.

==== Variante usada con gpt-5: límite 7

{block('recuperador_system_7_gpt5', p_ret7)}

==== Variante usada con gpt-5-mini y gpt-5-nano: límite 6

{block('recuperador_system_6', p_ret6)}

=== Agente de Calidad de Recuperación (definido, no ejecutado)

El agente fue definido en el código con el prompt siguiente, pero no se registró su herramienta, no se invocó y no produjo ningún registro. Se excluyó por razones de costo y complejidad; no se realizó una comparación empírica de su contribución.

{block('calidad_recuperacion_system_no_ejecutado', p_quality, 'definido, nunca enviado a un modelo')}

== Prompts de evaluación

Los tres jueces utilizaron el mismo prompt de sistema y la misma plantilla de usuario; cambiaron el modelo y la rúbrica. Los prompts se generaron con `pydantic-evals` 1.1.0 mediante `LLMJudge` con `include_input=True` e `include_expected_output=True`.

=== Prompt de sistema del juez

{block('juez_sistema', p_judge_sys, 'generado por la librería; aplicado a los tres jueces')}

=== Plantilla de evaluación de respuesta correcta

Los marcadores `⟦PREGUNTA⟧`, `⟦RESPUESTA⟧` y `⟦RESPUESTA_ESPERADA⟧` identifican los puntos donde se insertan el caso evaluado; no forman parte del texto enviado.

{block('juez_respuesta_correcta_template', p_judge_correct, 'generado por la librería; aplicado a los tres jueces')}

=== Plantilla de evaluación de precisión legal

{block('juez_precision_legal_template', p_judge_legal, 'generado por la librería; aplicado a los tres jueces')}

== Modelos jueces y parámetros

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto),
    [
      | *Modelo* | *Rúbrica* | *Temperatura solicitada* | *Máx. tokens de salida* |
      | :--- | :--- | :---: | :---: |
{judge_rows}
    ],
  ),
  caption: [Configuración registrada de los jueces. La temperatura solicitada no se interpreta aquí como evidencia de determinismo; esa cuestión se documenta en la corrección IX.1.3.],
) <tabla-jueces-parametros>

== Procedencia y hashes

#figure(
  three-line-table(
    columns: (5.6cm, 2.9cm, 1fr),
    [
      | *Prompt* | *SHA-256 (prefijo)* | *Procedencia* |
      | :--- | :--- | :--- |
      | `sin_rag_system` | `{short_hash(p_sin['sha256'])}` | Notebook de `part_e`; sin logs de entrada. |
      | `rag_basico_system_template` | `{short_hash(p_rag['sha256'])}` | Notebook de `part_f`; sin logs de entrada. |
      | `especialista_legal_system` | `{short_hash(p_law['sha256'])}` | 237 logs; una variante. |
      | `recuperador_system_7_gpt5` | `{short_hash(p_ret7['sha256'])}` | 79 logs de gpt-5. |
      | `recuperador_system_6` | `{short_hash(p_ret6['sha256'])}` | 158 logs de mini/nano. |
      | `calidad_recuperacion_` #linebreak() `system_no_ejecutado` | `{short_hash(p_quality['sha256'])}` | Definición de código; 0 logs. |
      | `juez_sistema` | `{short_hash(p_judge_sys['sha256'])}` | pydantic-evals 1.1.0. |
      | `juez_respuesta_correcta_template` | `{short_hash(p_judge_correct['sha256'])}` | pydantic-evals 1.1.0. |
      | `juez_precision_legal_template` | `{short_hash(p_judge_legal['sha256'])}` | pydantic-evals 1.1.0. |
    ],
  ),
  caption: [Inventario de prompts y hashes. Los valores completos, la longitud y el texto canónico están en `salidas/prompts_canonicos.json`.],
) <tabla-prompts-hashes>

#text(size: 8pt)[Generado el {generated_at} por `02_auditoria_prompts_y_configuracion.py`.]
"""
    (PROP / "anexo_02_prompts_y_parametros.typ").write_text(appendix, encoding="utf-8")


if __name__ == "__main__":
    main()

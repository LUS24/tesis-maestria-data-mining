#!/usr/bin/env python3
"""Métricas de recuperación desde los registros de part_g (NV-02).

Calcula, por unidad y por modelo del Agente Especialista Legal:

- recall@k: proporción de artículos relevantes recuperados en el top-k;
- MRR: recíproco del primer artículo relevante;
- all@k / none@k: proporción de unidades con todos / ningún artículo relevante;
- hit@k: proporción de unidades con al menos un artículo relevante.

La lista de recuperación agéntica se construye con los documentos únicos en el
orden de las consultas registradas en ``retrieval_history``. No se consulta
Milvus ni se reconstruye la base vectorial.

Uso:
    cd codigo_experimentos
    uv run --frozen python ../analisis-valoracion-jurado/verificacion-analisis-estadistico/metricas_recuperacion/scripts/calcular_metricas.py
"""

from __future__ import annotations

import csv
import glob
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any

PACKAGE = Path(__file__).resolve().parent.parent
VERIF = PACKAGE.parent
ANALISIS = VERIF.parent
REPO = ANALISIS.parent
CHAT = REPO / "codigo_experimentos" / "part_g" / "chat_data"
PART_D = (
    REPO
    / "codigo_experimentos"
    / "part_d"
    / "20251012_retrieval_baseline_from_20250804_101435_generated_questions.json"
)
OUT = PACKAGE / "datos"
SALIDAS = PACKAGE / "salidas"
KS = (1, 5, 10, 20)
MODELS = {
    "openai_gpt-5": "Agentic-RAG · especialista gpt-5",
    "openai_gpt-5-mini": "Agentic-RAG · especialista gpt-5-mini",
    "openai_gpt-5-nano": "Agentic-RAG · especialista gpt-5-nano",
}


def canon_sub(value: Any) -> int:
    if value is None or str(value).strip() == "" or str(value).lower() == "none":
        return 0
    return int(float(value))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_gold() -> dict[tuple[int, int], dict[str, Any]]:
    questions = json.loads(PART_D.read_text(encoding="utf-8"))
    gold: dict[tuple[int, int], dict[str, Any]] = {}
    for question in questions:
        key = (int(question["numero_pregunta"]), canon_sub(question["numero_subpregunta"]))
        items = question.get("contexto_para_respuesta", [])
        gold[key] = {
            "ids": {item["id_parte"] for item in items if item.get("id_parte")},
            "numeros": {int(item["nro_articulo"]) for item in items if item.get("nro_articulo") is not None},
            "rankings": [item.get("search_ranking") for item in items],
        }
    if len(gold) != 79:
        raise ValueError(f"Se esperaban 79 unidades de referencia y hay {len(gold)}")
    return gold


def baseline_rows(gold: dict[tuple[int, int], dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (q, sub), data in sorted(gold.items()):
        ranks = [int(r) if r is not None else math.inf for r in data["rankings"]]
        row: dict[str, Any] = {
            "modelo": "rag_basico_part_d",
            "pregunta": q,
            "subpregunta": sub,
            "n_gold": len(ranks),
            "n_recuperados": None,
            "n_consultas": 1,
            "primer_rank": min(ranks) if ranks else None,
        }
        for k in KS:
            row[f"recall@{k}"] = sum(1 for r in ranks if r <= k) / len(ranks)
            row[f"hit@{k}"] = int(any(r <= k for r in ranks))
            row[f"all@{k}"] = int(row[f"recall@{k}"] == 1)
            row[f"none@{k}"] = int(row[f"recall@{k}"] == 0)
        row["mrr"] = (1 / min(ranks)) if ranks and math.isfinite(min(ranks)) else 0.0
        rows.append(row)
    return rows


def load_history(unit_dir: Path) -> tuple[list[str], list[str], int, list[str]]:
    """Devuelve ids en orden, ids por número, cantidad de consultas y queries."""
    ids: list[str] = []
    numeros: list[str] = []
    queries: list[str] = []
    seen_ids: set[str] = set()
    seen_nums: set[str] = set()
    for filename in sorted(glob.glob(str(unit_dir / "retrieval_history" / "*.json"))):
        try:
            data = json.loads(Path(filename).read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        query = data.get("query")
        if query:
            queries.append(str(query))
        for document in data.get("retrieved_documents", []):
            identifier = document.get("id_parte")
            number = document.get("numero_parte")
            if identifier and identifier not in seen_ids:
                seen_ids.add(identifier)
                ids.append(identifier)
            if number is not None and str(number) not in seen_nums:
                seen_nums.add(str(number))
                numeros.append(str(number))
    return ids, numeros, len(queries), queries


def metrics_for_ranked(
    ranked: list[str],
    gold_ids: set[str],
    *,
    model: str,
    q: int,
    sub: int,
    n_calls: int,
    n_gold: int,
    match_field: str,
) -> dict[str, Any]:
    gold = set(gold_ids)
    row: dict[str, Any] = {
        "modelo": model,
        "pregunta": q,
        "subpregunta": sub,
        "n_gold": n_gold,
        "n_recuperados": len(ranked),
        "n_consultas": n_calls,
        "match": match_field,
        "primer_rank": next((i for i, item in enumerate(ranked, 1) if item in gold), None),
    }
    for k in KS:
        hits = sum(1 for item in ranked[:k] if item in gold)
        row[f"recall@{k}"] = hits / n_gold
        row[f"hit@{k}"] = int(hits > 0)
        row[f"all@{k}"] = int(row[f"recall@{k}"] == 1)
        row[f"none@{k}"] = int(row[f"recall@{k}"] == 0)
    first = row["primer_rank"]
    row["mrr"] = (1 / first) if first else 0.0
    return row


def agentic_rows(gold: dict[tuple[int, int], dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    query_rows: list[dict[str, Any]] = []
    for model_dir, label in MODELS.items():
        for unit_dir in sorted((CHAT / model_dir).iterdir()):
            if not unit_dir.is_dir():
                continue
            q, sub = map(int, unit_dir.name.split("_"))
            key = (q, sub)
            if key not in gold:
                raise KeyError(f"Unidad sin gold: {unit_dir}")
            ids, numbers, n_calls, queries = load_history(unit_dir)
            n_gold = len(gold[key]["ids"])
            rows.append(
                metrics_for_ranked(
                    ids, gold[key]["ids"], model=label, q=q, sub=sub,
                    n_calls=n_calls, n_gold=n_gold, match_field="id_parte",
                )
            )
            # Sensibilidad: si algún registro no tuviera id, se compara por número.
            num_gold = {str(number) for number in gold[key]["numeros"]}
            rows.append(
                metrics_for_ranked(
                    numbers, num_gold, model=label + " (por número)", q=q, sub=sub,
                    n_calls=n_calls, n_gold=len(num_gold), match_field="numero_parte",
                )
            )
            query_rows.append(
                {
                    "modelo": label,
                    "pregunta": q,
                    "subpregunta": sub,
                    "n_consultas": n_calls,
                    "n_queries_unicas": len(set(queries)),
                    "n_documentos_unicos": len(ids),
                    "n_gold": n_gold,
                }
            )
    return rows, query_rows


def summarize(rows: list[dict[str, Any]], model: str) -> dict[str, Any]:
    subset = [row for row in rows if row["modelo"] == model]
    if not subset:
        raise ValueError(f"Sin filas para {model}")
    retrieved = [row["n_recuperados"] for row in subset if row["n_recuperados"] is not None]
    out: dict[str, Any] = {
        "modelo": model,
        "unidades": len(subset),
        "n_gold": sum(row["n_gold"] for row in subset),
        "n_recuperados_promedio": (sum(retrieved) / len(retrieved)) if retrieved else None,
        "n_consultas_promedio": sum(row["n_consultas"] for row in subset) / len(subset),
    }
    for k in KS:
        out[f"recall@{k}"] = sum(row[f"recall@{k}"] for row in subset) / len(subset)
        out[f"hit@{k}"] = sum(row[f"hit@{k}"] for row in subset) / len(subset)
        out[f"all@{k}"] = sum(row[f"all@{k}"] for row in subset) / len(subset)
        out[f"none@{k}"] = sum(row[f"none@{k}"] for row in subset) / len(subset)
    out["mrr"] = sum(row["mrr"] for row in subset) / len(subset)
    return out


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SALIDAS.mkdir(parents=True, exist_ok=True)
    gold = load_gold()
    base = baseline_rows(gold)
    agentic, queries = agentic_rows(gold)
    rows = base + agentic
    fields = [
        "modelo", "pregunta", "subpregunta", "n_gold", "n_recuperados",
        "n_consultas", "match", "primer_rank", "mrr",
        *[f"recall@{k}" for k in KS], *[f"hit@{k}" for k in KS],
        *[f"all@{k}" for k in KS], *[f"none@{k}" for k in KS],
    ]
    write_csv(OUT / "01_metricas_por_unidad.csv", rows, fields)
    write_csv(
        OUT / "02_consultas_por_unidad.csv",
        queries,
        ["modelo", "pregunta", "subpregunta", "n_consultas", "n_queries_unicas", "n_documentos_unicos", "n_gold"],
    )
    summary = [summarize(rows, "rag_basico_part_d")]
    summary.extend(summarize(rows, label) for label in MODELS.values())
    # La sensibilidad por número se conserva aparte; no se usa para el resultado principal.
    summary.extend(summarize(rows, label + " (por número)") for label in MODELS.values())
    write_csv(
        OUT / "03_resumen_modelos.csv",
        summary,
        ["modelo", "unidades", "n_gold", "n_recuperados_promedio", "n_consultas_promedio",
         "mrr", *[f"recall@{k}" for k in KS], *[f"hit@{k}" for k in KS],
         *[f"all@{k}" for k in KS], *[f"none@{k}" for k in KS]],
    )
    payload = {
        "fuente_gold": str(PART_D.relative_to(REPO)),
        "hash_gold": sha256(PART_D),
        "fuente_logs": "codigo_experimentos/part_g/chat_data",
        "n_logs_historial": len(glob.glob(str(CHAT / "*" / "*" / "retrieval_history" / "*.json"))),
        "n_unidades": len(gold),
        "resumen": summary,
        "definicion": {
            "ranking_agentico": "documentos únicos en orden de consultas registradas; deduplicación por id_parte",
            "baseline": "search_ranking de part_d; recall@k sobre los artículos de referencia",
            "mrr": "media de 1/rank del primer artículo relevante; 0 si no aparece",
            "all_none": "proporción de unidades con todos/ningún artículo relevante en el top-k",
        },
        "limite": "No se reconstruyó Milvus ni se comparó con BM25; la comparación es contra el baseline registrado en part_d.",
    }
    (SALIDAS / "resumen_metricas_recuperacion.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

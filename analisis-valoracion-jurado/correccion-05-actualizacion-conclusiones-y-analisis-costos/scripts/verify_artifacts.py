#!/usr/bin/env python3
"""Controles de consistencia de la corrección IX.1.5."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PACKAGE_DIR / "datos"
OUT_DIR = PACKAGE_DIR / "salidas"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def approx(value: float, expected: float, tol: float = 1e-6) -> bool:
    return abs(value - expected) <= tol


def main() -> None:
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"control": name, "ok": bool(condition), "detalle": detail})

    cells = read_csv(DATA_DIR / "costos_por_celda.csv")
    threshold_rows = read_csv(DATA_DIR / "costo_por_respuesta_aceptable_umbrales.csv")
    frontier = read_csv(DATA_DIR / "frontera_pareto.csv")
    table4 = read_csv(DATA_DIR / "tabla4_reformulada.csv")
    summary = json.loads((OUT_DIR / "resumen_costos.json").read_text(encoding="utf-8"))
    conclusion_summary = json.loads((OUT_DIR / "resumen_conclusiones.json").read_text(encoding="utf-8"))

    check("9 celdas", len(cells) == 9, f"encontradas={len(cells)}")
    check("79 observaciones por celda", all(int(row["n"]) == 79 for row in cells), "todas las celdas deben tener n=79")
    check("711 observaciones", sum(int(row["n"]) for row in cells) == 711, f"total={sum(int(row['n']) for row in cells)}")
    check("costo total 22,2939", approx(float(summary["costo_total_experimento_usd"]), 22.29387015, 1e-6), f"{summary['costo_total_experimento_usd']}")
    check("7 celdas en Pareto", len(frontier) == 7, f"encontradas={len(frontier)}")
    check("9 filas en Tabla 4", len(table4) == 9, f"encontradas={len(table4)}")
    check("estados normalizados suman 9", sum(conclusion_summary["estados_normalizados"].values()) == 9, str(conclusion_summary["estados_normalizados"]))

    lookup = {(row["estrategia_label"], row["modelo"]): row for row in cells}
    rag_nano = lookup[("RAG básico", "gpt-5-nano")]
    agentic_mini = lookup[("Agentic-RAG", "gpt-5-mini")]
    agentic_gpt5 = lookup[("Agentic-RAG", "gpt-5")]
    rag_gpt5 = lookup[("RAG básico", "gpt-5")]
    no_rag_gpt5 = lookup[("Sin RAG", "gpt-5")]
    agentic_nano = lookup[("Agentic-RAG", "gpt-5-nano")]

    check(
        "RAG básico + nano es el menor costo por aceptable",
        float(rag_nano["rank_costo_por_aceptable_075"]) == 1 and approx(float(rag_nano["costo_por_aceptable_075"]), 0.006094819696969697, 1e-9),
        f"rank={rag_nano['rank_costo_por_aceptable_075']} costo={rag_nano['costo_por_aceptable_075']}",
    )
    check(
        "Agentic mini no es más barato que RAG gpt-5",
        float(agentic_mini["costo_medio"]) > float(rag_gpt5["costo_medio"]),
        f"{agentic_mini['costo_medio']} > {rag_gpt5['costo_medio']}",
    )
    check(
        "Agentic mini no es más barato que Sin RAG gpt-5",
        float(agentic_mini["costo_medio"]) > float(no_rag_gpt5["costo_medio"]),
        f"{agentic_mini['costo_medio']} > {no_rag_gpt5['costo_medio']}",
    )
    check(
        "Agentic mini es más barato que Agentic gpt-5",
        float(agentic_mini["costo_medio"]) < float(agentic_gpt5["costo_medio"]),
        f"{agentic_mini['costo_medio']} < {agentic_gpt5['costo_medio']}",
    )
    check(
        "Agentic nano tiene 41 no sustantivas",
        int(agentic_nano["n_no_sustantiva"]) == 41,
        f"n_no_sustantiva={agentic_nano['n_no_sustantiva']}",
    )
    check(
        "Umbral 0,75 tiene 9 filas",
        sum(1 for row in threshold_rows if row["umbral"] == "0.75") == 9,
        "filas del umbral 0.75",
    )

    required_docs = {
        "README.md": ["LR = 293,28", "41/79", "USD 0,0061", "USD 0,0564"],
        "TABLA_4_REFORMULADA.md": ["T4-01", "T4-09", "−0,270", "+0,106"],
        "ANALISIS_COSTOS.md": ["USD 0,0061", "USD 0,0564", "USD 0,0392", "USD 0,0478"],
        "PROPUESTA_TEXTO_MANUSCRITO.md": ["LR = 293,28", "41/79", "no se atribuye"],
        "DECISIONES.md": ["D-01", "D-14"],
    }
    for filename, strings in required_docs.items():
        path = PACKAGE_DIR / filename
        text = path.read_text(encoding="utf-8") if path.exists() else ""
        for value in strings:
            check(f"{filename} contiene {value!r}", value in text, f"archivo existe={path.exists()}")

    # Coherencia interna: ningún costo por aceptable es negativo o NaN en el umbral principal.
    check(
        "costos por aceptable finitos y positivos",
        all(
            math.isfinite(float(row["costo_por_aceptable"])) and float(row["costo_por_aceptable"]) > 0
            for row in threshold_rows
            if row["umbral"] == "0.75"
        ),
        "umbral 0.75",
    )

    result = {
        "ok": all(item["ok"] for item in checks),
        "n_controles": len(checks),
        "n_fallos": sum(not item["ok"] for item in checks),
        "controles": checks,
    }
    (OUT_DIR / "verificacion_artefactos.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Controles: {result['n_controles']} | fallos: {result['n_fallos']}")
    if not result["ok"]:
        for item in checks:
            if not item["ok"]:
                print("FALLO:", item["control"], "-", item["detalle"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()

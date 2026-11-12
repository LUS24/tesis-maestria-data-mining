"""Genera tablas Typst de borrador para revisar el reanálisis IX.1.1.

No edita el manuscrito. Escribe en `propuestas/` y genera un `preview_tablas.typ`
que puede compilarse aparte.

Uso:
    uv run --project codigo_experimentos --no-sync --frozen \
      python analisis-valoracion-jurado/correccion-01-reanalisis-inferencial/src/make_typst_tables.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[3]
OUT = BASE / "analisis-valoracion-jurado" / "correccion-01-reanalisis-inferencial"
SALIDAS = OUT / "salidas"
PROPUESTAS = OUT / "propuestas"
PROPUESTAS.mkdir(parents=True, exist_ok=True)


def num(value: float, digits: int = 3) -> str:
    return f"{float(value):.{digits}f}".replace(".", ",")


def esc(text: object) -> str:
    return str(text).replace("#", "\\#").replace("[", "\\[").replace("]", "\\]")


def cell_table() -> str:
    df = pd.read_csv(SALIDAS / "30_tabla_celdas_principal.csv")
    lines = []
    lines.append('#import "@preview/tablem:0.3.0": three-line-table\n')
    lines.append("#figure(\n")
    lines.append("  three-line-table(\n")
    lines.append("    columns: (auto, auto, auto, auto, auto, auto, auto, auto),\n")
    lines.append("    [\n")
    lines.append("      | *Estrategia* | *Modelo* | *n* | *No sust.* | *Media* | *Mediana* | *P(≥ 0,75)* | *Media exclusión* |\n")
    lines.append("      | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |\n")
    for _, row in df.iterrows():
        lines.append(
            "      | "
            + " | ".join(
                [
                    esc(row["estrategia_label"]),
                    esc(row["modelo"]),
                    str(int(row["n"])),
                    str(int(row["n_no_sustantiva"])),
                    num(row["media_principal"]),
                    num(row["mediana_principal"]),
                    num(row["p_ge_075_principal"]),
                    num(row["media_exclusion"]),
                ]
            )
            + " |\n"
        )
    lines.append("    ],\n")
    lines.append("  ),\n")
    lines.append(
        "  caption: [Estadísticos descriptivos por configuración bajo el escenario principal "
        "(respuestas no sustantivas = 0). La columna de exclusión usa solo respuestas sustantivas "
        "y es una sensibilidad, no el escenario principal.],\n"
    )
    lines.append(") <tabla-reanalisis-celdas>\n")
    return "".join(lines)


def effects_table(family: str, filename: str, title: str) -> str:
    df = pd.read_csv(SALIDAS / "31_efectos_simples_orientados.csv")
    df = df[df["familia"] == family].copy()
    lines = []
    lines.append('#import "@preview/tablem:0.3.0": three-line-table\n')
    lines.append("#figure(\n")
    lines.append("  three-line-table(\n")
    lines.append("    columns: (auto, auto, auto, auto, auto, auto),\n")
    lines.append("    [\n")
    lines.append("      | *Bloque* | *Contraste* | *Δ media* | *IC 95%* | *Δ P(≥ 0,75)* | *IC 95%* |\n")
    lines.append("      | :--- | :--- | ---: | :--- | ---: | :--- |\n")
    for _, row in df.iterrows():
        lines.append(
            "      | "
            + " | ".join(
                [
                    esc(row["bloque"]),
                    esc(row["comparacion"]),
                    num(row["dif_esperada"]),
                    f"{num(row['dif_esperada_ic95_inf'])} a {num(row['dif_esperada_ic95_sup'])}",
                    num(row["dif_p_ge_075"]),
                    f"{num(row['dif_p_ge_075_ic95_inf'])} a {num(row['dif_p_ge_075_ic95_sup'])}",
                ]
            )
            + " |\n"
        )
    lines.append("    ],\n")
    lines.append("  ),\n")
    lines.append(f"  caption: [{title}],\n")
    lines.append(") <tabla-reanalisis-efectos>\n")
    (PROPUESTAS / filename).write_text("".join(lines), encoding="utf-8")
    return "".join(lines)


def main() -> None:
    (PROPUESTAS / "tabla_celdas_principal.typ").write_text(cell_table(), encoding="utf-8")
    effects_table(
        "estrategia_dentro_de_modelo",
        "tabla_efectos_estrategia.typ",
        "Efectos simples de estrategia dentro de cada modelo bajo el escenario principal. "
        "Diferencias orientadas como Agentic-RAG − RAG básico, Agentic-RAG − Sin RAG y RAG básico − Sin RAG. "
        "IC 95% por simulación del modelo ordinal; los p de Holm están en el informe.",
    )
    effects_table(
        "modelo_dentro_de_estrategia",
        "tabla_efectos_modelo.typ",
        "Efectos simples de modelo dentro de cada estrategia bajo el escenario principal. "
        "Diferencias orientadas como gpt-5-mini − gpt-5-nano, gpt-5 − gpt-5-nano y gpt-5 − gpt-5-mini. "
        "IC 95% por simulación del modelo ordinal; los p de Holm están en el informe.",
    )

    preview = """#set page(paper: "a4", margin: 1.2cm)
#set text(size: 8pt)
#set par(justify: true)

= Tablas de reanálisis IX.1.1 (borrador)

Este archivo es una previsualización independiente del manuscrito. No modifica la tesis.
Las cifras provienen del escenario principal con clasificación automática; deben regenerarse
si cambia la revisión manual de la corrección 02.

#include "tabla_celdas_principal.typ"

#pagebreak()
#include "tabla_efectos_estrategia.typ"

#pagebreak()
#include "tabla_efectos_modelo.typ"
"""
    (PROPUESTAS / "preview_tablas.typ").write_text(preview, encoding="utf-8")
    print(f"Propuestas Typst en: {PROPUESTAS}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Count how many benchmark questions the legal reviewer touched.

Reads only the derived tracked-changes table. The mapping from the 21
single-question title files to Q1-Q21 is positional. The final title file
contains Q22-Q25 in a single block; its changes are assigned by paragraph
and content, as documented below.

Outputs:
  salidas/conteo_preguntas_revisadas.csv
  salidas/resumen_conteo_preguntas.md
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "salidas"
CHANGES = OUT / "cambios_rastreados.csv"

# The 21 title files before título_final.md correspond, in order, to Q1-Q21.
TITLE_TO_Q = {
    "título_i.md": 1,
    "título_ii.md": 2,
    "título_iii.md": 3,
    "título_iv.md": 4,
    "título_v.md": 5,
    "título_vi.md": 6,
    "título_vii.md": 7,
    "título_viii.md": 8,
    "título_ix.md": 9,
    "título_x.md": 10,
    "título_xi.md": 11,
    "título_xii.md": 12,
    "título_xiii.md": 13,
    "título_xiv.md": 14,
    "título_xv.md": 15,
    "título_xvi.md": 16,
    "título_xvii.md": 17,
    "título_xviii.md": 18,
    "título_xix.md": 19,
    "título_xx.md": 20,
    "título_xxi.md": 21,
}

# The final title block contains Q22-Q25. These paragraph assignments are
# based on the reconstructed ODT/DOCX diff and were checked against the
# final JSON.
FINAL_BLOCK_TO_Q = {
    "368": [22],  # "Rodrigo Asís" (Q22); registered as a comment, applied in JSON
    "371": [23],  # "normativa aplicable" -> "Código de Minería" (Q23)
    "372": [24],  # "Ley 24.585": comment only; not applied in JSON
    "373": [25],  # "normativa actual" -> "Código de Minería vigente / 2025" (Q25)
    "376": [23],  # Q23 answer: YCRT comment / possible content change
}

# Changes at these blocks are general comments about the combined final case;
# they are not attributed to one question.
GENERAL_FINAL_BLOCKS = {"367"}
# Changes after the benchmark block belong to the excluded hydrocarbons case.
EXCLUDED_BLOCKS = {"380", "381", "382", "383", "384", "385", "386", "387"}

QUESTION_TEXT = {
    1: "Q1.1-Q1.3 (litio)",
    2: "Q2 (conflicto de interés)",
    3: "Q3 (permiso de exploración)",
    4: "Q4 (descubrimiento)",
    5: "Q5 (pertenencias)",
    6: "Q6 (servidumbres)",
    7: "Q7 (grupo minero)",
    8: "Q8 (servidumbres)",
    9: "Q9 (turba)",
    10: "Q10 (canteras)",
    11: "Q11 (sociedades)",
    12: "Q12 (caducidad)",
    13: "Q13 (infracciones)",
    14: "Q14 (avío)",
    15: "Q15 (sociedad minera)",
    16: "Q16 (matrimonio)",
    17: "Q17 (litio Catamarca)",
    18: "Q18 (Título XVIII)",
    19: "Q19 (Santa Cruz)",
    20: "Q20 (usufructo)",
    21: "Q21 (zona de interés especial)",
    22: "Q22 (manifestación de descubrimiento)",
    23: "Q23 (Río Turbio)",
    24: "Q24 (Ley 24.585)",
    25: "Q25 (litio 2025)",
}


def is_content(row: dict[str, str]) -> bool:
    return row["categoria"] != "comentario_o_instruccion_editorial"


def main() -> None:
    with CHANGES.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))

    counts = {
        q: {"total": 0, "content": 0, "comments": 0, "evidence": []}
        for q in range(1, 26)
    }
    general = 0
    excluded = 0
    prompt = 0
    unmapped = 0

    for row in rows:
        case = row["caso"].split("v1_")[-1] if row["caso"] else ""
        block = row["block_index"]
        targets = []

        if case in TITLE_TO_Q:
            targets = [TITLE_TO_Q[case]]
        elif case == "título_final.md":
            if block in EXCLUDED_BLOCKS:
                excluded += 1
                continue
            if block in FINAL_BLOCK_TO_Q:
                targets = FINAL_BLOCK_TO_Q[block]
            elif block in GENERAL_FINAL_BLOCKS:
                general += 1
                continue
            else:
                unmapped += 1
                continue
        elif case == "apéndice.md":
            excluded += 1
            continue
        elif not case:
            prompt += 1
            continue
        else:
            unmapped += 1
            continue

        for q in targets:
            counts[q]["total"] += 1
            if is_content(row):
                counts[q]["content"] += 1
            else:
                counts[q]["comments"] += 1
            if len(counts[q]["evidence"]) < 3:
                counts[q]["evidence"].append(
                    f"{row['seccion']}: {row['texto'][:60]}"
                )

    # Q22's name correction is registered as a comment but was applied in the JSON.
    if counts[22]["comments"] and not counts[22]["content"]:
        counts[22]["applied_comment"] = 1

    out_rows = []
    for q in range(1, 26):
        c = counts[q]
        if c["content"] > 0:
            status = "corregida"
        elif q == 22 and c.get("applied_comment"):
            status = "corregida (comentario aplicado)"
        elif c["comments"] > 0:
            status = "solo comentario / no aplicada"
        else:
            status = "sin intervención"
        out_rows.append({
            "numero_pregunta": q,
            "descripcion": QUESTION_TEXT[q],
            "intervenciones_total": c["total"],
            "cambios_contenido": c["content"],
            "comentarios_editoriales": c["comments"],
            "estado": status,
            "evidencia": " | ".join(c["evidence"]),
        })

    with (OUT / "conteo_preguntas_revisadas.csv").open(
        "w", encoding="utf-8", newline=""
    ) as fh:
        writer = csv.DictWriter(fh, fieldnames=list(out_rows[0]))
        writer.writeheader()
        writer.writerows(out_rows)

    total_q = len(out_rows)
    corrected = [r for r in out_rows if r["estado"].startswith("corregida")]
    comment_only = [r for r in out_rows if r["estado"].startswith("solo comentario")]
    untouched = [r for r in out_rows if r["estado"] == "sin intervención"]
    with_changes = [r for r in out_rows if r["intervenciones_total"] > 0]

    lines = [
        "# Conteo de preguntas revisadas por la profesional",
        "",
        "**Fuente:** `salidas/cambios_rastreados.csv` (cambios con texto del ODT).",
        "**Método:** los 21 archivos de título anteriores a `título_final.md` se asignan en orden a Q1-Q21; el bloque final se asigna a Q22-Q25 por párrafo y contenido.",
        "",
        "| Indicador | Valor |",
        "| --- | ---: |",
        f"| Preguntas del benchmark | {total_q} |",
        f"| Preguntas con alguna intervención | {len(with_changes)} |",
        f"| Preguntas con cambio de contenido | {len(corrected)} |",
        f"| Preguntas solo con comentario no aplicado | {len(comment_only)} |",
        f"| Preguntas sin intervención | {len(untouched)} |",
        f"| Cambios con texto (fragmentos) | {len(rows)} |",
        f"| Comentarios generales del bloque final | {general} |",
        f"| Cambios del caso de hidrocarburos excluido | {excluded} |",
        f"| Cambios de instrucción/prompt general | {prompt} |",
        f"| Cambios no asignados | {unmapped} |",
        "",
        "## Detalle",
        "",
        "| Q | Descripción | Intervenciones | Contenido | Comentarios | Estado |",
        "| ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for r in out_rows:
        lines.append(
            f"| {r['numero_pregunta']} | {r['descripcion']} | "
            f"{r['intervenciones_total']} | {r['cambios_contenido']} | "
            f"{r['comentarios_editoriales']} | {r['estado']} |"
        )
    lines += [
        "",
        "## Lectura",
        "",
        f"- {len(with_changes)} de 25 preguntas fueron objeto de alguna intervención.",
        f"- {len(corrected)} tienen un cambio de contenido identificable.",
        f"- {len(comment_only)} quedó solo con un comentario no aplicado (Q24).",
        f"- {len(untouched)} no fueron intervenidas: "
        + ", ".join(f"Q{r['numero_pregunta']}" for r in untouched)
        + ".",
        "",
        "El conteo es una cota inferior: el ODT registra comentarios y cambios, pero no un campo de “aceptado/rechazado” por pregunta. Las decisiones del autor se verifican contra el JSON final en `decisiones_revision.csv`.",
    ]
    (OUT / "resumen_conteo_preguntas.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Preguntas: {total_q}; intervenidas: {len(with_changes)}; corregidas: {len(corrected)}; solo comentario: {len(comment_only)}; sin intervención: {len(untouched)}")
    print("Generados:", OUT / "conteo_preguntas_revisadas.csv", OUT / "resumen_conteo_preguntas.md")


if __name__ == "__main__":
    main()

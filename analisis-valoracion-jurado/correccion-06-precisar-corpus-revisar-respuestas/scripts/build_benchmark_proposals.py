#!/usr/bin/env python3
"""Propose benchmark v2 changes without editing the source benchmark or manuscript."""
from __future__ import annotations
import csv
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "salidas"

rows = [
    {
        "id": "B01", "unidad": "Q1.1", "campo": "contexto_para_respuesta",
        "actual": "Artículo 2, inciso 1",
        "propuesto": "Artículo 2, categoría 1ª (numeral 1°)",
        "motivo": "El artículo 2 divide las minas en tres categorías; no contiene incisos. La etiqueta 'inciso' es incorrecta.",
        "prioridad": "alta",
    },
    {
        "id": "B02", "unidad": "Q1.1", "campo": "respuesta",
        "actual": "(art. 2° inc. 1)",
        "propuesto": "(art. 2°, categoría 1ª, numeral 1°)",
        "motivo": "Alinear la cita de la respuesta con la estructura real del artículo 2.",
        "prioridad": "alta",
    },
    {
        "id": "B03", "unidad": "Q1.2", "campo": "respuesta (anexo Typst)",
        "actual": "La propiedad minera constituye un derecho real separado de la propiedad del suelo (art. 8).",
        "propuesto": "La mina forma una propiedad distinta de la del terreno en que se encuentra (art. 11). El artículo 7 establece el dominio de la Nación o de las provincias y el artículo 10 la adquisición por concesión legal; el artículo 18 añade que las minas se conceden por tiempo ilimitado.",
        "motivo": "El artículo 8 se refiere a la facultad de buscar minas, no a la separación de la propiedad. El anexo Typst contradice la respuesta JSON, que cita 7, 10 y 11.",
        "prioridad": "alta",
    },
    {
        "id": "B04", "unidad": "Q1.3", "campo": "respuesta (anexo Typst y respuesta JSON)",
        "actual": "La propietaria solo puede oponerse por razones de seguridad o ambientales (art. 17).",
        "propuesto": "El artículo 17 dispone que los trabajos no pueden ser impedidos ni suspendidos sino cuando lo exija la seguridad pública, la conservación de las pertenencias y la salud o existencia de los trabajadores. La oposición debe encuadrarse en alguna de esas causales y ser resuelta por la autoridad competente.",
        "motivo": "La paráfrasis 'seguridad o ambientales' no reproduce el artículo 17 y omite 'conservación de las pertenencias' y 'salud o existencia de los trabajadores'. 'Solo' agrega un límite que el texto no formula de ese modo.",
        "prioridad": "alta",
    },
    {
        "id": "B05", "unidad": "Q5.1", "campo": "texto_subpregunta",
        "actual": "¿Cuál es la extensión de terreno que corresponde reconocer legalmente como pertenencia a Explora S.A. en este caso?",
        "propuesto": "¿Cuál es la extensión de terreno que corresponde reconocer legalmente como pertenencia a Explora S.A. en este caso y en base a qué disposiciones del Código de Minería?",
        "motivo": "La revisora pidió fundamento normativo; el JSON redujo la pregunta y perdió esa parte. La referencia 74/76 no se explicita en la pregunta.",
        "prioridad": "media",
    },
    {
        "id": "B06", "unidad": "Q13.2", "campo": "contexto_para_respuesta",
        "actual": "Artículo 243",
        "propuesto": "Artículos 235, 236, 237, 240, 241 y 243",
        "motivo": "La respuesta cita 235, 236, 237, 240 y 241 para las infracciones y 243 para las multas; la lista de referencias solo contiene 243.",
        "prioridad": "media",
    },
    {
        "id": "B07", "unidad": "Q13.3", "campo": "contexto_para_respuesta",
        "actual": "Artículo 245",
        "propuesto": "Artículos 245, 264 y 265 (si se mantiene la referencia a reincidencia y procedimiento)",
        "motivo": "La respuesta cita 264 y 265 además de 245; si se consideran parte de la respuesta esperada, deben figurar en las referencias.",
        "prioridad": "media",
    },
    {
        "id": "B08", "unidad": "Q22.1", "campo": "contexto_para_respuesta",
        "actual": "Artículo 45, Artículo 353",
        "propuesto": "Artículo 45; agregar el artículo 353 solo si la respuesta explica el plazo/abandono del trámite",
        "motivo": "La respuesta 22.1 cita solo el artículo 45; la referencia 353 no se usa. Verificar si la segunda subpregunta (Q22.2) es la que necesita 353.",
        "prioridad": "baja",
    },
    {
        "id": "B09", "unidad": "Q25.0", "campo": "contexto_para_respuesta",
        "actual": "Artículo 351",
        "propuesto": "Artículos 76 y 351",
        "motivo": "La respuesta cita el artículo 76 para caracterizar el litio como yacimiento diseminado de primera categoría y el 351 para el multiplicador; el 76 no está en las referencias.",
        "prioridad": "media",
    },
    {
        "id": "B10", "unidad": "Q23.0", "campo": "alcance del caso",
        "actual": "Caso incluido como unidad única dentro del benchmark del Código de Minería.",
        "propuesto": "Mantenerlo con una nota de alcance sobre el régimen de Río Turbio, rotularlo como caso de régimen especial o moverlo a un anexo; no atribuir la eliminación a la revisora.",
        "motivo": "La revisora no pidió eliminar Q23; pidió separar el caso final combinado. El caso que propuso eliminar es el de hidrocarburos (Ley 17.319). La revisión independiente detectó que Q23 no explicita si el régimen aplicable se agota en el Código.",
        "prioridad": "media",
    },
    {
        "id": "B11", "unidad": "Q24.0", "campo": "enunciado",
        "actual": "Un concesionario explota una mina desde antes de la vigencia de la Ley 24.585 y desea conocer su obligación ambiental transitoria.",
        "propuesto": "Un concesionario explota una mina desde antes de la vigencia de la Ley 24.585 (ley de protección ambiental para la actividad minera) y desea conocer su obligación transitoria de presentar el informe de impacto ambiental.",
        "motivo": "La revisora pidió aclarar genéricamente el tema de la ley citada. La pregunta actual presupone conocimiento de la Ley 24.585.",
        "prioridad": "media",
    },
    {
        "id": "B12", "unidad": "Q25.0", "campo": "enunciado",
        "actual": "Una empresa de explotación de litio consulta sobre el régimen de multiplicidad de pertenencias aplicable a yacimientos de litio en 2025.",
        "propuesto": "Una empresa de explotación de litio consulta sobre el régimen de multiplicidad de pertenencias aplicable a yacimientos de litio, según el Código de Minería vigente al año 2025.",
        "motivo": "La revisora pidió aclarar la temporalidad y la norma; el enunciado actual no identifica el Código ni la versión consultada.",
        "prioridad": "media",
    },
]

with (OUT / "propuestas_benchmark.csv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

lines = [
    "# Propuestas para una versión v2 del benchmark",
    "",
    "Estas propuestas no modifican `data/evaluation_questions_v20250804_101435.json`. Se ofrecen para que el autor y la abogada decidan qué cambios incorporar en una versión nueva y documentada.",
    "",
    "| ID | Unidad | Campo | Actual | Propuesto | Motivo | Prioridad |",
    "| --- | --- | --- | --- | --- | --- | --- |",
]
for r in rows:
    lines.append(f"| {r['id']} | {r['unidad']} | {r['campo']} | {r['actual']} | {r['propuesto']} | {r['motivo']} | {r['prioridad']} |")
lines += [
    "",
    "## Criterio de versionado",
    "",
    "Si se acepta cualquier cambio de B01–B12, crear `data/evaluation_questions_v20250804_101435_v2.json` (o un nombre con fecha) y dejar el archivo original intacto. Registrar en un changelog qué unidades cambiaron, quién los aprobó y con qué fuente. No recalcular las métricas históricas con el benchmark nuevo sin distinguir explícitamente la versión.",
]
(OUT / "propuestas_benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("proposals", len(rows))

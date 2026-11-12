#!/usr/bin/env python3
"""Build a curated table of review interventions and their state in the benchmark JSON."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
OUT = BASE / "salidas"
BENCH = json.loads((REPO / "data" / "evaluation_questions_v20250804_101435.json").read_text(encoding="utf-8"))
BENCH_TEXT = json.dumps(BENCH, ensure_ascii=False)


def has(s: str) -> bool:
    return s.lower() in BENCH_TEXT.lower()


def qtext(n: int) -> str:
    for q in BENCH["preguntas"]:
        if q["numero_pregunta"] == n:
            parts = [q.get("texto_enunciado", "")]
            for s in q.get("sub_preguntas", []) or []:
                parts += [s.get("texto_subpregunta", ""), s.get("respuesta", "")]
            parts += [q.get("texto_pregunta", ""), q.get("respuesta", "")]
            return " ".join(parts)
    return ""


rows = [
    # id, caso, comentario/cambio, evidencia ODT, estado en JSON, evidencia JSON, acción
    ("R01", "Instrucción general", "Reemplazar 'abogado experto en código minero' por 'experto/a en Derecho Minero', con mirada de género y especialización focalizada en el Código de Minería.", "Inserciones 2025-08-13 10:50–10:54", "no evaluable en benchmark; afecta el prompt de generación", "No hay prompt de generación en el JSON del benchmark", "Si se regenera el benchmark, actualizar el prompt; no cambiar el texto del benchmark actual."),
    ("R02", "Instrucción general", "Unificar 'Código de Minería' y 'Código Minero'.", "Inserción 12:00–12:02", "aplicado en el JSON", f"'Código Minero' aparece {BENCH_TEXT.lower().count('código minero')} veces; 'Código de Minería' aparece {BENCH_TEXT.lower().count('código de minería')} veces", "Mantener 'Código de Minería' en manuscrito, anexo y futuras regeneraciones."),
    ("R03", "Instrucción general", "Añadir 'ante situaciones concretas' para precisar el alcance de las preguntas.", "Inserción 12:01–12:02", "no verificable en el benchmark", "El JSON no conserva el prompt de generación", "Documentar la decisión si se publica el prompt; no afecta la redacción del benchmark actual."),
    ("R04", "Q1", "Corregir '1&' a '1' en la cita del art. 2.", "Eliminación 11:59", "aplicado (el JSON no contiene '1&')", "La respuesta usa '(art. 2° inc. 1)'", "Corregir además la etiqueta 'inciso' por 'categoría/numeral 1°'."),
    ("R05", "Q1", "Añadir 'Ing.' al nombre de Juan Pérez en la respuesta 1.2.", "Inserción 11:10", "aplicado", "La respuesta contiene 'Ing. Juan Pérez'", "Mantener."),
    ("R06", "Q2", "Nombrar a Laura Álvarez, Raúl Juárez y Oscar Castro.", "Inserciones 11:08–11:15", "aplicado con variantes de acentuación", "El JSON contiene 'Laura Álvarez', 'Raúl Juárez' y 'Oscar Castro'", "Mantener; unificar la tilde de Álvarez."),
    ("R07", "Q2", "Aclarar que la normativa aplicable es el Código de Minería Argentino.", "Inserciones 11:14–11:20 y eliminación 14:02", "aplicado en la introducción del caso", "La introducción termina '...basado en el Código de Minería Argentino:'", "Mantener; revisar que la subpregunta 2.3 no deje 'normativa mencionada' como referencia vaga."),
    ("R08", "Q2", "Reemplazar 'ningún derecho' por 'derecho alguno'.", "Eliminación/inserción 11:15–11:16", "aplicado", "La respuesta 2.3 dice 'no le otorga derecho alguno'", "Mantener."),
    ("R09", "Q3", "Reemplazar 'provincia X' por una provincia concreta (el autor usa San Juan).", "No hay cambio rastreado; el ODT final conserva 'provincia X'", "aplicado por el autor fuera del control de cambios", "El JSON dice 'provincia de San Juan'", "Confirmar que San Juan es la jurisdicción elegida y que no altera el caso."),
    ("R10", "Q4", "Nombrar al abogado Jorge Ramírez y corregir 'criaderode'.", "Inserciones 11:26–11:28", "aplicado", "El JSON contiene 'El abogado Jorge Ramírez' y 'criadero de mineral'", "Mantener; el comentario 'OJO cambiaste el estilo' es editorial."),
    ("R11", "Q5", "Sustituir 'normas' por 'disposiciones del Código Minero' y pedir fundamento normativo.", "Inserción/eliminación 12:04–12:05", "aplicado solo parcialmente; la pregunta del JSON quedó reducida a la extensión", "La subpregunta 5.1 del JSON no pide fundamento normativo", "Restaurar una fórmula como '¿Cuál es la extensión... y en base a qué disposiciones del Código de Minería?'."),
    ("R12", "Q6", "Localizar la provincia (el autor usa Chubut) y aceptar 'obligación/obligaciones'.", "Inserciones 12:11–12:12 y 12:40–12:41", "aplicado por el autor; Chubut no está en el ODT final", "El JSON dice 'provincia de Chubut' y 'obligación/obligaciones'", "Confirmar Chubut; mantener la alternativa gramatical."),
    ("R13", "Q9", "Localizar la provincia (el autor usa Tierra del Fuego).", "Inserción 13:08–13:09", "aplicado por el autor; el ODT final deja '…...'", "El JSON dice 'provincia de Tierra del Fuego'", "Confirmar la jurisdicción."),
    ("R14", "Q10", "Nombrar a Don Ricardo Ojeda.", "Inserciones 13:10–13:11", "aplicado", "El JSON contiene 'Don Ricardo Ojeda'", "Mantener."),
    ("R15", "Q14", "Localizar la provincia (el autor usa Jujuy).", "Inserción 13:28", "aplicado por el autor; el ODT final deja '…..'", "El JSON dice 'provincia de Jujuy'", "Confirmar la jurisdicción."),
    ("R16", "Q16", "Nombrar a Martina Truman y Jorge Speed.", "Inserciones 13:32–13:35", "aplicado", "El JSON contiene 'Martina Truman' y 'Jorge Speed'", "Mantener."),
    ("R17", "Q17", "Nombrar a Adrián López.", "Inserciones 13:35–13:37", "aplicado", "El JSON contiene 'Sr. Adrián López'", "Mantener; corregir el espacio doble en la respuesta 17.2 si se edita el benchmark."),
    ("R18", "Q18", "Nombrar a Joaquín Gómez y Ofelia Maldonado; aclarar el articulado del Título XVIII.", "Inserciones 13:37–13:41", "aplicado", "El JSON contiene 'Joaquín Gómez' y 'Ofelia Maldonado'", "Mantener; unificar 'Joaquín' y 'Joaquin'."),
    ("R19", "Q19", "Localizar la provincia de Santa Cruz.", "Inserción 13:42–13:43", "aplicado", "El JSON dice 'provincia de Santa Cruz'", "Mantener."),
    ("R20", "Q20", "Nombrar a Ana López.", "Inserciones 13:49–13:52", "aplicado", "El JSON contiene 'Ana López'", "Mantener."),
    ("R21", "Q21", "Aclarar 'empresa estatal provincial'.", "Inserción 13:53", "aplicado", "El JSON contiene 'empresa estatal provincial'", "Mantener."),
    ("R22", "Q22–Q25", "El caso final combinaba varios clientes; la profesional sugirió abrirlo en tres casos individuales. El autor generó cuatro unidades (Q22–Q25), no tres.", "Inserciones 13:58–14:01", "aplicado con una diferencia: 4 unidades en lugar de 3", "El JSON contiene Q22, Q23, Q24 y Q25 separadas", "Mantener y documentar la separación; explicar por qué se generaron cuatro y no tres."),
    ("R23", "Q22", "Nombrar a Rodrigo Asís.", "Inserción 13:58", "aplicado", "El JSON contiene 'Sr. Rodrigo Asís'", "Mantener."),
    ("R24", "Q23", "La profesional no recomendó eliminar Q23: pidió separar el caso final combinado. Q23 (Río Turbio) no explicita si el régimen aplicable se agota en el Código o requiere legislación especial.", "Inserciones 13:58–14:01; la recomendación de eliminar (14:09–14:12) corresponde al caso de hidrocarburos, no a Q23", "Q23 se mantiene en el JSON; su alcance no se reabre en esta tesis", "El JSON conserva Q23 y sus referencias 348/349", "No atribuir la eliminación a la revisora; decidir si Q23 se mantiene, se rotula como régimen especial o se mueve a anexo."),
    ("R25", "Q24", "Aclarar genéricamente el tema de la Ley 24.585.", "Inserción 14:02", "no aplicado; la pregunta se mantiene como fue revisada", "El JSON conserva 'Ley 24.585' sin aclaración", "Añadir 'ley de protección ambiental' o trasladar el caso a un anexo de legislación especial."),
    ("R26", "Q25", "Añadir temporalidad al régimen de litio.", "Inserción 14:03", "parcial; la pregunta se mantiene como fue revisada", "El JSON conserva 'al año 2025'", "Verificar que el artículo 351 citado sea el vigente en 2025 y documentar la fecha de consulta."),
    ("R27", "Caso adicional", "Omitir el caso de hidrocarburos añadido al final del ODT; la profesional lo consideró fuera del alcance.", "Inserciones 14:06–14:12", "aparente omisión; no se reabre en esta tesis", "No hay caso de hidrocarburos en las 25 preguntas del JSON", "Confirmar que la omisión es deliberada y documentarla; el ODT conserva el borrador y no debe tomarse como benchmark final."),
    ("R28", "Q1.2 (anexo)", "El anexo Typst atribuye a 'art. 8' la separación de la propiedad minera; la respuesta JSON y el corpus usan arts. 7, 10 y 11.", "No es un cambio de la profesional; detectado en la auditoría", "error solo en el anexo; la respuesta JSON es correcta", "La respuesta 1.2 cita 'artículos 7°, 10° y 11°' y 'art. 11'", "Reemplazar la referencia del anexo por art. 11 (y, si se explican dominio y concesión, arts. 7 y 10)."),
    ("R29", "Q1.3", "La respuesta parafrasea el art. 17 como 'seguridad pública, salud o conservación ambiental'.", "No es un cambio de la profesional; detectado en la auditoría", "error en JSON y anexo; el corpus es correcto", "El corpus dice 'seguridad pública, conservación de las pertenencias y salud o existencia de los trabajadores'", "Corregir la paráfrasis y revisar el alcance de 'solamente'."),
    ("R30", "Q1.1", "La referencia 'Artículo 2, inciso 1' no es técnicamente correcta: el artículo 2 divide en categorías, no en incisos.", "No es un cambio de la profesional; detectado en la auditoría", "etiqueta 'inciso' en el benchmark; fuera de alcance", "El artículo 2 del corpus usa '1&', '2&', '3&'", "Usar 'Artículo 2, categoría 1°' o 'numeral 1°' en el benchmark y en el anexo."),
]

with (OUT / "decisiones_revision.csv").open("w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "caso", "comentario_o_cambio", "evidencia_odt", "estado_en_json", "evidencia_json"])
    w.writerows([r[:6] for r in rows])

lines = [
    "# Intervenciones de la revisión y estado en el JSON",
    "",
    "Esta tabla separa lo que la profesional propuso, lo que el autor incorporó al JSON y lo que quedó sin aplicar. **No son decisiones de la tesis**: las decisiones locales están en `resumen_ejecutivo.md` y el registro global en `../DECISIONES_integradas.md`, Bloque D. No se modificó ningún archivo fuente.",
    "",
    "| ID | Caso | Propuesta / cambio | Estado en el JSON |",
    "| --- | --- | --- | --- |",
]
for r in rows:
    lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[4]} |")
lines += [
    "",
    "## Observaciones",
    "",
    "- Los cambios rastreados del ODT incluyen comentarios editoriales y fragmentos de edición; no todos son texto aprobado del benchmark. La tabla anterior es la lectura curada.",
    "- El autor aplicó varias elecciones que no quedaron registradas como cambios rastreados (por ejemplo, provincia de San Juan, Chubut, Tierra del Fuego y Jujuy). Esas elecciones deben confirmarse antes de tomarlas como parte de la revisión de la profesional.",
    "- La profesional pidió separar el caso final combinado y omitió el caso de hidrocarburos por la Ley 17.319. No recomendó eliminar Q23 (Río Turbio). El JSON conserva Q23 y Q24 y omite el caso de hidrocarburos; esta tabla no reabre esas preguntas (ver `resumen_ejecutivo.md` §5).",
]
(OUT / "decisiones_revision.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("decisiones", len(rows))

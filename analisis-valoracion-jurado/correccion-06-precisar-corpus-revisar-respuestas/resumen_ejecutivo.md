# Resumen ejecutivo — IX.1.6

> **Este documento concentra la síntesis y las decisiones locales de esta carpeta.** La evidencia está en `hallazgos_respuestas_referencia.md`; los textos propuestos, en `propuesta_edicion_manuscrito.md`; el registro global, en [`../DECISIONES_integradas.md`](../DECISIONES_integradas.md), Bloque D.

## 1. Qué pidió el jurado

El jurado pidió precisar la versión del corpus, aclarar las contradicciones sobre su origen y revisar las respuestas de referencia observadas en **V.7**: los ejemplos **1.2** (artículo 8) y **1.3** (artículo 17). También pidió documentar que el benchmark fue revisado por un único profesional y cuántas preguntas fueron corregidas.

## 2. Decisiones

| Tema | Decisión | Estado | Referencia |
| --- | --- | --- | --- |
| Procedencia del corpus | Describirlo como PDF de 1997 + actualización manual con Infoleg + OCR parcial como insumo histórico. Documentar el proceso en 8 pasos: PDF → imágenes → Markdown con o4 → división por títulos → revisión manual/Infoleg → GPT-4.1 → DOCX → revisión profesional → ODT → JSON. El parser HTML fue un prototipo descartado; la actualización fue manual | Resuelta (PI-12) | `propuesta_edicion_manuscrito.md` §1.1 |
| Conteos del corpus | Usar 398 nodos artículo (347 cuerpo + 15 disposiciones + 36 apéndice), 362 números únicos y 397 nodos con texto; el artículo 239 está derogado y vacío | Resuelta | `propuesta_edicion_manuscrito.md` §1.4 |
| Fechas y metadatos | Usar 1886-11-25 como sanción y 1997-05-30 como publicación del texto ordenado. Eliminar 1994-01-01/10/15 y 2024-12-09 si no se aporta fuente | Resuelta (PI-19) | `propuesta_edicion_manuscrito.md` §2.1 |
| Revisión profesional | Una sola profesional del derecho; no hubo segunda revisión independiente. Usar “revisión por una profesional”, no “validación final” | Resuelta (PI-18) | `propuesta_edicion_manuscrito.md` §2.2–2.3 |
| Conteo de preguntas | 25 preguntas: 18 con alguna intervención, 17 con cambio de contenido o corrección aplicada, 1 solo con comentario no aplicado (Q24) y 7 sin intervención | Resuelta (PI-32) | `salidas/conteo_preguntas_revisadas.csv`; `salidas/resumen_conteo_preguntas.md` |
| Q1.2 | El JSON, el corpus y `título_i.md` son correctos; el error está solo en el anexo Typst. Corregir únicamente el anexo | Resuelta (PI-16) | `propuesta_edicion_manuscrito.md` §3.1 |
| Q1.3 | El error está en el JSON y en el anexo Typst; el artículo 17 del corpus es correcto. No modificar el benchmark v1: corregir el anexo para citar el artículo 17 literalmente y declarar la discrepancia como limitación. Corregir el JSON y reevaluar es trabajo futuro | Resuelta (PI-15) | `propuesta_edicion_manuscrito.md` §3.2 |
| Q5.1, Q23/Q24 y hallazgos adicionales | Las preguntas ya revisadas por la profesional se mantienen. Q5.1, Q23, Q24, Q1.1, Q13.2/Q13.3, Q22.1 y Q25 no generan cambios ni una nueva revisión | Cancelada / fuera de alcance (PI-13, PI-14, PI-17) | `hallazgos_respuestas_referencia.md` §2.2; `resumen_ejecutivo.md` §5 |
| Benchmark v2 y nueva revisión profesional | No se crean en esta tesis; quedan como trabajo futuro | Cancelada / fuera de alcance (PI-20) | `resumen_ejecutivo.md` §5 |

## 3. Sustento mínimo

- **Corpus:** 482 nodos estructurales; 398 nodos artículo; 397 con texto; 362 números únicos. El detalle está en `hallazgos_respuestas_referencia.md` §1.1.
- **Linaje:** el corpus contiene texto posterior a 1997 (artículos 3, 31, 215, 221, 351 y 355) y coincide con el HTML actualizado de Infoleg. El detalle está en `hallazgos_respuestas_referencia.md` §1.2.
- **Revisión:** el ODT contiene 166 regiones de cambio, 130 con texto y 80 párrafos con diferencias. El detalle está en `hallazgos_respuestas_referencia.md` §2.1.
- **Conteo por pregunta:** 18/17/1/7, con el detalle y el método en `salidas/conteo_preguntas_revisadas.csv` y `scripts/count_reviewed_questions.py`.
- **Fechas:** sanción 1886-11-25; publicación original en Registro Nacional 1885/86, p. 578; texto ordenado en B.O. 1997-05-30. Las fechas 1994-01-10 y 2024-12-09 no están verificadas.

## 4. Q1.2 y Q1.3

**Q1.2.** La respuesta del JSON cita correctamente los artículos 7, 10 y 11; el artículo 11 establece que la mina es una propiedad distinta de la del terreno. El anexo Typst atribuye esa separación al artículo 8. El error está solo en el anexo.

**Q1.3.** La paráfrasis “seguridad pública, salud o conservación ambiental” está en el JSON y en el anexo Typst. El artículo 17 del corpus dice “seguridad pública, conservación de las pertenencias y salud o existencia de los trabajadores”. El benchmark v1 se mantiene porque ya fue usado para las 711 respuestas.

Los textos propuestos y la justificación están en `propuesta_edicion_manuscrito.md` §3.1 y §3.2; los textos del corpus y la comparación, en `hallazgos_respuestas_referencia.md` §3.1 y §3.2.

## 5. Fuera de alcance

La revisión dejó sin aplicar Q5.1 (fundamento normativo) y Q24 (aclaración de la Ley 24.585). La auditoría adicional detectó Q1.1 (etiqueta “inciso” en el artículo 2), Q13.2/Q13.3, Q22.1 y Q25 (referencias incompletas) y Q23 (alcance del régimen especial). **Ninguno de esos puntos forma parte de la respuesta al jurado**: las preguntas ya revisadas por la profesional se mantienen como tales. No se propone una nueva revisión, un benchmark v2 ni un cambio de las respuestas ya evaluadas.

## 6. Alcance y límites

- No se emite una opinión jurídica definitiva sobre la interpretación de los artículos; se verifica la fidelidad textual entre corpus, benchmark y anexo.
- No se recalculan métricas de jueces ni respuestas del sistema.
- No se modifican las fuentes, el benchmark ni el manuscrito.
- La “última actualización” del corpus no pudo verificarse; debe completarse con una fuente o eliminarse.
- Las decisiones de esta carpeta no reabren las preguntas ya revisadas ni crean una versión nueva del benchmark.

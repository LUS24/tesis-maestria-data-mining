# Resumen ejecutivo — IX.1.6

## Qué pidió el jurado

Precisar la versión del corpus, resolver las contradicciones sobre su origen y revisar las respuestas de referencia observadas en V.7: los ejemplos 1.2 (artículo 8) y 1.3 (artículo 17). También pidió documentar que el benchmark fue revisado por un único profesional y cuántas preguntas fueron corregidas.

## 1. Procedencia del corpus

El proceso efectivamente realizado fue:

1. Conversión del PDF del Boletín Oficial a imágenes y extracción a Markdown con o4.
2. División del Markdown en los archivos de `codigo_experimentos/data/law_data/titulos_codigo_mineria/`.
3. Revisión manual de cada archivo y actualización de los artículos con el texto de Infoleg.
4. Envío del Markdown a GPT-4.1 para generar preguntas y respuestas.
5. Exportación de las preguntas a DOCX.
6. Revisión por una profesional del derecho.
7. Devolución de un ODT con cambios y comentarios.
8. Generación de `data/evaluation_questions_v20250804_101435.json` a partir de esas correcciones.

El parser HTML se intentó, pero se descartó porque la revisión manual resultó más rápida y controlable. Por tanto, el corpus debe describirse como **PDF de 1997 + actualización manual con Infoleg + OCR parcial como insumo histórico**. No es una copia exclusiva del PDF de 1997 ni un producto automático del parser de Infoleg.

## 2. Conteos del corpus

| Dato | Valor verificado |
| --- | ---: |
| Nodos estructurales | 482 |
| Nodos artículo | 398 |
| Cuerpo principal | 347 (1–347) |
| Disposiciones generales y transitorias | 15 (348–362) |
| Apéndice | 36 (1–36) |
| Números únicos | 362 |
| Nodos artículo con texto | 397 |
| Artículo vacío | 239 (derogado) |

El manuscrito dice “399 artículos” en metodología y “245 artículos” en el capítulo 3. La tabla de 398 es correcta como nodos, pero debe explicar la duplicación del apéndice y el artículo 239.

## 3. Fechas del benchmark

- Sanción: **1886-11-25**, no 1994-01-01.
- Publicación original: Registro Nacional 1885/86, p. 578; texto ordenado: **B.O. 1997-05-30**.
- `1994-01-10` no está verificado.
- `2024-12-09` no está verificado; el HTML local contiene notas hasta 2023.

## 4. Revisión de la profesional

El ODT contiene **166 regiones de cambio**, **130 con texto** y **80 párrafos con diferencias**. La revisión fue realizada por **una única profesional del derecho argentino**; no hubo segunda revisión independiente.

| Indicador | Valor |
| --- | ---: |
| Preguntas del benchmark | 25 |
| Preguntas con alguna intervención | **18** |
| Preguntas con cambio de contenido o corrección aplicada | **17** |
| Preguntas solo con comentario no aplicado | **1** (Q24) |
| Preguntas sin intervención | **7** (Q7, Q8, Q9, Q12, Q13, Q15, Q20) |

El detalle está en `salidas/conteo_preguntas_revisadas.csv`; el método, en `scripts/count_reviewed_questions.py`.

La descripción correcta del manuscrito es **“revisión por una profesional”**, no “validación final” ni “segunda revisión”.

## 5. Respuestas de referencia observadas por el jurado

### Q1.2

- El JSON, el corpus y `título_i.md` citan correctamente los artículos 7, 10 y 11; el artículo 11 establece que la mina es una propiedad distinta.
- El error está **solo en el anexo Typst**, que atribuye al artículo 8 la separación de la propiedad.
- Acción: corregir únicamente el anexo. No modificar el benchmark.

### Q1.3

- La paráfrasis “seguridad pública, salud o conservación ambiental” está **en el JSON y en el anexo Typst**.
- El artículo 17 del corpus y de `título_i.md` dice: “seguridad pública, conservación de las pertenencias y salud o existencia de los trabajadores”.
- El benchmark v1 no se modifica porque ya fue usado para las 711 respuestas. Acción: corregir el anexo para citar el artículo 17 literalmente y declarar la discrepancia como limitación. Una corrección del benchmark y su reevaluación corresponden a trabajo futuro.

## 6. Fuera de alcance

La auditoría adicional detectó Q1.1 (etiqueta “inciso” en el artículo 2), Q13.2/Q13.3, Q22.1, Q25 (referencias incompletas) y Q23/Q24 (alcance de regímenes especiales). **No forman parte de la respuesta al jurado**: las preguntas ya fueron revisadas por la profesional y se mantienen como tales. No se propone una nueva revisión, un benchmark v2 ni un cambio de las respuestas ya evaluadas en esta tesis.

## 7. Qué se entrega

- `propuesta_edicion_manuscrito.md`: textos propuestos para corpus, revisión, 1.2 y 1.3.
- `hallazgos_respuestas_referencia.md`: auditoría detallada.
- `salidas/conteo_preguntas_revisadas.csv`: conteo por pregunta.
- `salidas/resumen_conteo_preguntas.md`: resumen del conteo.
- `salidas/parrafos_revisados.md`: los 80 párrafos antes/después.
- `salidas/corpus_vs_fuentes.csv`: comparación con HTML y OCR.
- `salidas/referencias_benchmark.csv` y `unidades_benchmark.csv`: evidencia adicional, fuera de las decisiones de esta tesis.

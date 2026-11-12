# Corrección IX.1.6 — Corpus, procedencia y respuestas de referencia

Esta carpeta reúne los artefactos para resolver el punto **IX.1.6** del plan de correcciones:

> Precisar la versión del corpus, resolver las contradicciones sobre su origen y revisar las respuestas de referencia observadas (V.7, V.9).

No se modificó ningún archivo existente del repositorio. Las fuentes, el manuscrito y los logs se leyeron en modo de solo lectura. Todo lo nuevo está en esta carpeta.

## 1. Qué revisar primero

1. **`resumen_ejecutivo.md`** — conclusiones y decisiones pendientes en dos páginas.
2. **`propuesta_edicion_manuscrito.md`** — texto actual y texto propuesto para los `.typ` y README, con la justificación de cada cambio.
3. **`hallazgos_respuestas_referencia.md`** — auditoría del corpus y de las respuestas 1.2 y 1.3; los demás hallazgos quedan fuera de alcance.
4. **`salidas/decisiones_revision.md`** — qué propuso la abogada, qué quedó en el JSON y qué sigue pendiente.
5. **`salidas/parrafos_revisados.md`** — comparación completa antes/después de los 80 párrafos con cambios.

## 2. Archivos de entrada y su rol

| Archivo | Rol según la aclaración del autor | Tratamiento |
| --- | --- | --- |
| `data/20250804_101435_generated_questions-SIN_REVISION.docx` | Casos generados por GPT-4.1, sin revisión de abogado | Se usa como línea base “antes”. No se modifica. |
| `data/20250804_101435_generated_questions - 130825-REVISADO.odt` | Casos revisados por una abogada, con control de cambios | Se reconstruyen texto original y final; se extraen cambios y comentarios. No se modifica. |
| `data/20250804_101435_generated_questions - 130825.json` | Casos separados en preguntas/subpreguntas por el autor a partir del archivo revisado | Se usa como benchmark final. No se modifica. |
| `data/codigo_de_mineria_actualizado_2025_08_02.json` | Corpus indexado | Se audita su estructura, metadatos y linaje. No se modifica. |
| `codigo_experimentos/data/inputs/html/codigo_minero_43797.html` | HTML actualizado de Infoleg, con notas de modificaciones | Se usa como contraste del corpus. No se modifica. |
| `codigo_experimentos/data/inputs/pdf/seccion_primera_19970530.pdf` | PDF del Boletín Oficial de 1997 | Se usa como fuente histórica declarada. No se modifica. |
| `codigo_experimentos/data/outputs/llm_img_to_md/*.md` | OCR/extracción del PDF | Se usa para mostrar que el OCR es parcial y previo a las modificaciones. No se modifica. |

## 3. Hallazgos principales

### 3.1. El corpus no es una copia del PDF de 1997

El corpus contiene texto posterior a 1997:

- artículo 3: incluye “wollastonita” (Ley 25.225/1999); el OCR de 1997 no la incluye;
- artículo 31: contiene la redacción de la Ley 27.111/2015;
- artículos 215 y 221: contienen las actualizaciones de la Resolución 90/2023 y la Ley 27.701/2022;
- artículos 351 y 355: contienen redacciones distintas de las que aparecen en el OCR largo.

El HTML de Infoleg conserva las notas de esas modificaciones y coincide con el corpus en los artículos verificados. Por tanto, la descripción defendible es: **PDF de 1997 como texto base + HTML actualizado de Infoleg para las modificaciones + OCR parcial como insumo histórico**. No es correcto afirmar que “Infoleg se descartó” sin explicar que su texto actualizado quedó incorporado.

### 3.2. Los conteos deben unificarse

- 482 nodos estructurales en total.
- 398 nodos de tipo artículo.
- 347 del cuerpo (1–347).
- 15 disposiciones generales y transitorias (348–362).
- 36 del apéndice (1–36).
- 362 números únicos, porque el apéndice repite 1–36.
- 397 nodos artículo con texto; el artículo 239 está derogado y vacío.

El manuscrito dice “399 artículos” en metodología y “245 artículos” en el capítulo 3. Ambas cifras deben corregirse. La tabla de 398 es correcta como nodos, pero debe explicar los duplicados del apéndice y el artículo 239.

### 3.3. Los metadatos de fecha son incorrectos o no están sustentados

- `fecha_sancion = 1994-01-01` → la Ley 1.919/1886 fue sancionada el **1886-11-25**.
- `fecha_publicacion = 1994-01-15` → la publicación original figura en el Registro Nacional 1885/86, p. 578; el texto ordenado se publicó en el **B.O. 1997-05-30**.
- `fecha_promulgacion = 1994-01-10` → no verificada; no usar sin fuente.
- `fecha_ultima_actualizacion = 2024-12-09` → no verificada; el HTML local contiene notas hasta 2023. No usar como dato verificado.

### 3.4. La revisión de la profesional: alcance y conteo

El ODT contiene **166 regiones de cambio**, **130 con texto** y **80 párrafos con diferencias** respecto del DOCX sin revisión. La revisión fue realizada por **una única profesional del derecho argentino**; no hay evidencia de una segunda revisión independiente.

El conteo por pregunta es reproducible con `scripts/count_reviewed_questions.py` y está en `salidas/conteo_preguntas_revisadas.csv`:

| Indicador | Valor |
| --- | ---: |
| Preguntas del benchmark | 25 |
| Preguntas con alguna intervención | **18** |
| Preguntas con cambio de contenido o corrección aplicada | **17** |
| Preguntas solo con comentario no aplicado | **1** (Q24) |
| Preguntas sin intervención | **7** (Q7, Q8, Q9, Q12, Q13, Q15, Q20) |
| Fragmentos de cambio con texto | 130 |
| Fragmentos de contenido (enunciado, respuesta, referencia) | 99 |
| Comentarios editoriales | 31 |

Q22 se contabiliza como corregida porque el nombre “Rodrigo Asís” fue incorporado al JSON, aunque el cambio esté registrado como comentario. Q24 quedó solo con un comentario de alcance que no se incorporó.

**No debe describirse el proceso como “validación final” ni como “segunda revisión”.** La descripción correcta es: revisión por una profesional, registrada en un ODT con control de cambios, con 18 preguntas intervenidas y 17 correcciones de contenido.

### 3.5. Respuestas de referencia: alcance del jurado

El jurado observó dos ejemplos concretos. La verificación distingue el dato del manuscrito:

| Unidad | Verificación | Acción |
| --- | --- | --- |
| Q1.2 | La respuesta del JSON cita correctamente 7, 10 y 11; los textos de los artículos 8 y 11 del corpus y de `título_i.md` son correctos. El error está **solo en el anexo Typst**, que atribuye al artículo 8 la separación de la propiedad. | Corregir únicamente el anexo Typst: art. 11 para propiedad distinta; 7 y 10 para dominio/concesión; 18 solo si se conserva “tiempo ilimitado”. No modificar el benchmark |
| Q1.3 | La paráfrasis “seguridad pública, salud o conservación ambiental” está **en el JSON y en el anexo Typst**. El artículo 17 del corpus y de `título_i.md` dice “seguridad pública, conservación de las pertenencias y salud o existencia de los trabajadores”. | El benchmark v1 no se modifica porque ya fue usado para generar y evaluar las 711 respuestas. Corregir el anexo del manuscrito para citar el artículo 17 literalmente y declarar la discrepancia como limitación. Una corrección del benchmark y una nueva evaluación corresponden a trabajo futuro |

### 3.6. Hallazgos fuera del alcance de esta respuesta

La auditoría adicional detectó Q1.1 (etiqueta “inciso” en el artículo 2), Q13.2/Q13.3, Q22.1, Q25 (referencias incompletas) y Q23/Q24 (alcance de regímenes especiales). **No forman parte de la respuesta al jurado**: las preguntas ya fueron revisadas por la profesional y se mantienen como tales. Quedan documentados en `hallazgos_respuestas_referencia.md` para trabajo futuro; no se propone una nueva revisión ni un benchmark v2 en esta tesis.

## 4. Archivos generados

### Informes

| Archivo | Contenido |
| --- | --- |
| `resumen_ejecutivo.md` | Síntesis para decidir antes de editar. |
| `propuesta_edicion_manuscrito.md` | Cambios concretos en `.typ` y README, con texto actual/propuesto. |
| `hallazgos_respuestas_referencia.md` | Auditoría del corpus y de las respuestas de referencia. |
| `README.md` | Este índice. |

### Tablas y datos derivados (`salidas/`)

| Archivo | Contenido |
| --- | --- |
| `comparacion_docx_odt.md` | Cambios rastreados con caso, sección y clasificación. |
| `comparacion_docx_odt.json` | Índice máquina-legible de la comparación. |
| `cambios_rastreados.csv` | 130 inserciones/eliminaciones con texto y contexto. |
| `conteo_preguntas_revisadas.csv` | Conteo por pregunta: intervenciones, contenido, comentarios y estado. |
| `resumen_conteo_preguntas.md` | Resumen legible: 18 intervenidas, 17 corregidas, 1 solo comentario, 7 sin intervención. |
| `cambios_por_caso.md` | Los mismos cambios agrupados por caso. |
| `parrafos_antes_despues.csv` | 80 párrafos con texto original y final. |
| `parrafos_revisados.md` | Los 80 párrafos en formato de revisión. |
| `decisiones_revision.csv` / `.md` | 30 decisiones curadas: propuesta, estado en JSON, acción. |
| `corpus_nodos.csv` | 482 nodos con tipo, número, estado, ruta y hash del texto. |
| `corpus_articulos.csv` | 398 nodos artículo con texto, estado y duplicados. |
| `corpus_metadatos.csv` | Metadatos del corpus y estado de verificación. |
| `corpus_vs_fuentes.csv` | Comparación de artículos clave contra HTML y OCR. |
| `referencias_benchmark.csv` | 166 referencias del benchmark y su resolución en el corpus. |
| `unidades_benchmark.csv` | 79 unidades, citas extraídas y alertas. |
| `citas_respuestas.csv` | Cada cita de artículo extraída de las respuestas. |
| `propuestas_benchmark.csv` / `.md` | 12 cambios detectados por la auditoría adicional; fuera de alcance, no se usan en esta tesis. |
| `auditoria_corpus_benchmark.md` | Informe automático de la auditoría. |

### Scripts reproducibles (`scripts/`)

| Archivo | Función |
| --- | --- |
| `extract_review_changes.py` | Reconstruye original/final del ODT, extrae cambios y los compara con el DOCX. |
| `count_reviewed_questions.py` | Mapea los cambios a Q1-Q25 y genera el conteo por pregunta. |
| `audit_corpus_benchmark.py` | Audita corpus, metadatos, referencias y citas. |
| `build_revision_decisions.py` | Construye la tabla curada de decisiones de revisión. |
| `build_benchmark_proposals.py` | Genera propuestas históricas de la auditoría adicional; fuera de alcance. |
| `build_manifest.py` | Genera el manifiesto SHA-256 de fuentes y artefactos. |
| `verificar_artefactos.py` | Verifica conteos y que los hashes de las fuentes no hayan cambiado. |

Para regenerar:

```bash
cd analisis-valoracion-jurado/correccion-06-precisar-corpus-revisar-respuestas
python3 scripts/extract_review_changes.py
python3 scripts/audit_corpus_benchmark.py
python3 scripts/build_revision_decisions.py
python3 scripts/build_benchmark_proposals.py
python3 scripts/build_manifest.py
python3 scripts/verificar_artefactos.py
```

Los scripts usan solo la biblioteca estándar de Python y rutas relativas al repositorio. No escriben fuera de `salidas/`. El manifiesto `manifiesto_sha256.csv` conserva los hashes de las fuentes y de los artefactos; `verificar_artefactos.py` comprueba que las fuentes no hayan cambiado.

## 5. Estado de las decisiones

1. **Corpus:** resuelto. El proceso fue: PDF → imágenes → Markdown con o4; división por títulos; revisión manual de cada archivo y actualización con Infoleg; envío a GPT-4.1; exportación a DOCX; revisión por una profesional; ODT con cambios; generación del JSON final. El parser HTML se intentó, pero se descartó porque la revisión manual fue más rápida. Documentar este proceso en metodología; no afirmar que Infoleg se descartó por completo.
2. **Q23 y Q24:** fuera de alcance. Las preguntas ya fueron revisadas por la profesional y se mantienen como tales. No se propone nueva revisión ni cambio de benchmark en esta tesis.
3. **Q1.3:** el error está en el JSON y en el anexo Typst; el artículo 17 del corpus es correcto. El benchmark v1 no se modifica porque ya fue usado para las 711 respuestas. Corregir el anexo para citar el artículo 17 literalmente y declarar la discrepancia como limitación; una nueva revisión/reevaluación es trabajo futuro.
4. **Q1.2:** el error está solo en el anexo Typst; el JSON y el corpus son correctos. Corregir el anexo y no crear una v2 por este punto.
5. **Revisión:** fue una sola profesional; no hubo segunda revisión independiente. Cambiar “validación” por “revisión por una profesional” y documentar el ODT.
6. **Conteo:** 18 preguntas intervenidas, 17 con corrección de contenido, Q24 solo con comentario, 7 sin intervención. Ver `salidas/conteo_preguntas_revisadas.csv`.

## 6. Límites

- No se pronunció una opinión jurídica definitiva sobre la interpretación de los artículos; se verificó la fidelidad textual entre corpus, benchmark y anexo.
- No se recalcularon métricas de jueces ni respuestas del sistema.
- No se modificaron los archivos fuente ni el manuscrito.
- Las fechas oficiales se verificaron en las fichas de Argentina.gob.ar/InfoLeg; la fecha de “última actualización” del corpus no pudo verificarse y debe completarse o eliminarse.

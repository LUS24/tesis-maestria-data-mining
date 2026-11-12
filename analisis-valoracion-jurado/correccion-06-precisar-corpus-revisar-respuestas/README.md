# Corrección IX.1.6 — Corpus, procedencia y respuestas de referencia

Esta carpeta reúne la evidencia y las propuestas para resolver el punto **IX.1.6** del plan de correcciones y la observación **V.7** del jurado: precisar la versión del corpus, aclarar su procedencia y revisar las respuestas de referencia 1.2 y 1.3.

No se modificó ningún archivo fuente del repositorio. Las fuentes, el manuscrito y los logs se leyeron en modo de solo lectura.

## 1. Documentos y responsabilidades

| Documento | Qué contiene | Qué no contiene |
| --- | --- | --- |
| `resumen_ejecutivo.md` | Síntesis, **decisiones locales** y estado de cada punto | Evidencia extensa ni textos completos de edición |
| `hallazgos_respuestas_referencia.md` | Evidencia: corpus, metadatos, revisión profesional y respuestas 1.2/1.3 | Decisiones ni propuestas de redacción |
| `propuesta_edicion_manuscrito.md` | Texto actual y texto propuesto para `.typ` y README | Decisiones ni evidencia completa |
| `salidas/` | Tablas, comparaciones y auditorías reproducibles | Decisiones de la tesis |
| `README.md` | Este índice y las instrucciones de reproducción | Hallazgos ni decisiones |

**Las decisiones locales están solo en `resumen_ejecutivo.md`.** El registro global de la tesis está en [`../DECISIONES_integradas.md`](../DECISIONES_integradas.md), Bloque D. Los demás documentos remiten allí en lugar de repetir estados o resoluciones.

## 2. Archivos de entrada y su rol

| Archivo | Rol | Tratamiento |
| --- | --- | --- |
| `data/20250804_101435_generated_questions-SIN_REVISION.docx` | Casos generados por GPT-4.1, sin revisión profesional | Línea base “antes”. No se modifica. |
| `data/20250804_101435_generated_questions - 130825-REVISADO.odt` | Casos revisados por una profesional, con control de cambios | Se reconstruyen texto original y final; se extraen cambios y comentarios. No se modifica. |
| `data/20250804_101435_generated_questions - 130825.json` | Casos separados en preguntas/subpreguntas por el autor a partir del archivo revisado | Benchmark final. No se modifica. |
| `data/codigo_de_mineria_actualizado_2025_08_02.json` | Corpus indexado | Se audita su estructura, metadatos y linaje. No se modifica. |
| `codigo_experimentos/data/inputs/html/codigo_minero_43797.html` | HTML actualizado de Infoleg, con notas de modificaciones | Contraste del corpus. No se modifica. |
| `codigo_experimentos/data/inputs/pdf/seccion_primera_19970530.pdf` | PDF del Boletín Oficial de 1997 | Fuente histórica declarada. No se modifica. |
| `codigo_experimentos/data/outputs/llm_img_to_md/*.md` | OCR/extracción del PDF | Se usa para mostrar que el OCR es parcial y previo a las modificaciones. No se modifica. |

## 3. Artefactos generados

### Tablas y datos derivados (`salidas/`)

| Archivo | Contenido |
| --- | --- |
| `comparacion_docx_odt.md` / `.json` | Cambios rastreados con caso, sección y clasificación; índice máquina-legible. |
| `cambios_rastreados.csv` | 130 inserciones/eliminaciones con texto y contexto. |
| `cambios_por_caso.md` | Los mismos cambios agrupados por caso. |
| `parrafos_antes_despues.csv` | 80 párrafos con texto original y final. |
| `parrafos_revisados.md` | Los 80 párrafos en formato de revisión. |
| `conteo_preguntas_revisadas.csv` | Conteo por pregunta: intervenciones, contenido, comentarios y estado. |
| `resumen_conteo_preguntas.md` | Resumen legible del conteo por pregunta. |
| `decisiones_revision.csv` / `.md` | 30 intervenciones curadas: propuesta, estado en el JSON y evidencia. No son decisiones de la tesis. |
| `corpus_nodos.csv` | 482 nodos con tipo, número, estado, ruta y hash del texto. |
| `corpus_articulos.csv` | 398 nodos artículo con texto, estado y duplicados. |
| `corpus_metadatos.csv` | Metadatos del corpus y estado de verificación. |
| `corpus_vs_fuentes.csv` | Comparación de artículos clave contra HTML y OCR. |
| `referencias_benchmark.csv` | 166 referencias del benchmark y su resolución en el corpus. |
| `unidades_benchmark.csv` | 79 unidades, citas extraídas y alertas. |
| `citas_respuestas.csv` | Cada cita de artículo extraída de las respuestas. |
| `propuestas_benchmark.csv` / `.md` | Registro histórico de la auditoría adicional; fuera de alcance y no usado en esta tesis. |
| `auditoria_corpus_benchmark.md` | Informe automático de la auditoría. |

### Scripts reproducibles (`scripts/`)

| Archivo | Función |
| --- | --- |
| `extract_review_changes.py` | Reconstruye original/final del ODT, extrae cambios y los compara con el DOCX. |
| `count_reviewed_questions.py` | Mapea los cambios a Q1–Q25 y genera el conteo por pregunta. |
| `audit_corpus_benchmark.py` | Audita corpus, metadatos, referencias y citas. |
| `build_revision_decisions.py` | Construye la tabla curada de intervenciones de la revisión. |
| `build_benchmark_proposals.py` | Genera el registro histórico de propuestas de la auditoría adicional; fuera de alcance. |
| `build_manifest.py` | Genera el manifiesto SHA-256 de fuentes y artefactos. |
| `verificar_artefactos.py` | Verifica conteos y que los hashes de las fuentes no hayan cambiado. |

## 4. Reproducción

```bash
cd analisis-valoracion-jurado/correccion-06-precisar-corpus-revisar-respuestas
python3 scripts/extract_review_changes.py
python3 scripts/count_reviewed_questions.py
python3 scripts/audit_corpus_benchmark.py
python3 scripts/build_revision_decisions.py
python3 scripts/build_benchmark_proposals.py
python3 scripts/build_manifest.py
python3 scripts/verificar_artefactos.py
```

Los scripts usan solo la biblioteca estándar de Python y rutas relativas al repositorio. Salvo `manifiesto_sha256.csv`, que se escribe en la raíz de esta carpeta, no escriben fuera de `salidas/`. El manifiesto conserva los hashes de las fuentes y de los artefactos; `verificar_artefactos.py` comprueba que las fuentes no hayan cambiado.

**Alcance y límites:** `resumen_ejecutivo.md` §6.

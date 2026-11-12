# Corrección IX.1.6 — Corpus, procedencia y respuestas de referencia

Esta carpeta reúne los artefactos para resolver el punto **IX.1.6** del plan de correcciones:

> Precisar la versión del corpus, resolver las contradicciones sobre su origen y revisar las respuestas de referencia observadas (V.7, V.9).

No se modificó ningún archivo existente del repositorio. Las fuentes, el manuscrito y los logs se leyeron en modo de solo lectura. Todo lo nuevo está en esta carpeta.

## 1. Qué revisar primero

1. **`resumen_ejecutivo.md`** — conclusiones y decisiones pendientes en dos páginas.
2. **`propuesta_edicion_manuscrito.md`** — texto actual y texto propuesto para los `.typ` y README, con la justificación de cada cambio.
3. **`hallazgos_respuestas_referencia.md`** — auditoría del corpus y de las respuestas 1.1, 1.2, 1.3, 13, 22, 23, 24 y 25.
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

### 3.4. La revisión de la abogada está registrada, pero no es una “validación” cerrada

El ODT contiene **166 regiones de cambio**, **130 con texto** y **80 párrafos con diferencias** respecto del DOCX sin revisión. Incluye:

- comentarios sobre el prompt y el perfil profesional;
- nombres y lugares para los casos;
- cambios de terminología (“Código Minero” → “Código de Minería”);
- correcciones de redacción;
- decisiones de alcance (separar el caso final, aclarar la Ley 24.585, omitir el caso de hidrocarburos).

No todos los comentarios están incorporados al JSON. El autor aplicó algunas decisiones que no quedaron registradas como cambios rastreados (por ejemplo, San Juan, Chubut, Tierra del Fuego y Jujuy). La tabla `salidas/decisiones_revision.csv` separa propuesta, estado en el JSON y acción pendiente.

**No debe describirse el proceso como “validación final” ni como “segunda revisión”** sin identificar al revisor, la fecha y el resultado. La evidencia disponible es una revisión con control de cambios.

### 3.5. Respuestas de referencia que requieren corrección

| Unidad | Problema | Corrección propuesta |
| --- | --- | --- |
| Q1.1 | “Artículo 2, inciso 1”: el artículo 2 usa categorías, no incisos. | “Artículo 2, categoría 1ª (numeral 1°)”. |
| Q1.2 | El anexo Typst atribuye al artículo 8 la separación de la propiedad; el artículo 8 se refiere a la facultad de buscar minas. | Usar artículo 11 para la propiedad distinta; artículos 7 y 10 para dominio/concesión; artículo 18 para “tiempo ilimitado”. |
| Q1.3 | La respuesta dice “seguridad pública, salud o conservación ambiental”; el artículo 17 dice “seguridad pública, conservación de las pertenencias y salud o existencia de los trabajadores”. | Reproducir el artículo 17 o reformular la pregunta. Revisión jurídica de la abogada. |
| Q13.2 | La respuesta cita 235, 236, 237, 240, 241 y 243; las referencias solo incluyen 243. | Agregar las referencias que la respuesta utiliza. |
| Q13.3 | La respuesta cita 264 y 265 además de 245; las referencias solo incluyen 245. | Agregar 264/265 o justificar por qué no son referencias. |
| Q22.1 | Declara el artículo 353, pero la respuesta solo cita el 45. | Verificar si 353 corresponde a Q22.2 o ampliar la respuesta. |
| Q23 | Río Turbio involucra un régimen especial que el caso no explicita. La revisora no pidió eliminar Q23; pidió separar el caso combinado. El caso que propuso eliminar es el de hidrocarburos. | Revisar el alcance de Q23 (mantener, rotular o mover a anexo); no atribuir su eliminación a la revisora. |
| Q24 | La Ley 24.585 se menciona sin explicar su tema. | Aclarar que es la ley de protección ambiental para la actividad minera o mover a anexo. |
| Q25 | La respuesta cita el artículo 76, pero las referencias solo incluyen el 351. | Agregar el 76 y verificar la versión vigente en 2025. |

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
| `propuestas_benchmark.csv` / `.md` | 12 cambios propuestos para una versión v2 del benchmark. |
| `auditoria_corpus_benchmark.md` | Informe automático de la auditoría. |

### Scripts reproducibles (`scripts/`)

| Archivo | Función |
| --- | --- |
| `extract_review_changes.py` | Reconstruye original/final del ODT, extrae cambios y los compara con el DOCX. |
| `audit_corpus_benchmark.py` | Audita corpus, metadatos, referencias y citas. |
| `build_revision_decisions.py` | Construye la tabla curada de decisiones de revisión. |
| `build_benchmark_proposals.py` | Construye las propuestas de benchmark v2. |
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

## 5. Decisiones que necesito de ti antes de editar el manuscrito

1. **Corpus:** ¿confirmas que el texto actualizado de Infoleg se incorporó manualmente al corpus? ¿O mediante un parser? Necesito la ruta exacta para describir la procedencia sin ambigüedad.
2. **Q23 (Río Turbio):** ¿se mantiene, se rotula como caso de régimen especial o se mueve a un anexo? La revisora no pidió eliminarlo; el caso que propuso eliminar es el de hidrocarburos.
3. **Q24 (Ley 24.585):** ¿se aclara en el enunciado o se mueve a un anexo?
4. **Q1.3 (art. 17):** ¿la abogada confirma la paráfrasis propuesta o prefiere reformular la pregunta?
5. **Q1.2 (art. 8 vs 11):** ¿se corrige solo el anexo Typst o también se crea una versión v2 del benchmark con la referencia 18?
6. **Revisión:** ¿hubo una segunda revisión independiente? Si no, el manuscrito debe decir “revisión por una profesional” y no “validación final”.

## 6. Límites

- No se pronunció una opinión jurídica definitiva sobre la interpretación de los artículos; se verificó la fidelidad textual entre corpus, benchmark y anexo.
- No se recalcularon métricas de jueces ni respuestas del sistema.
- No se modificaron los archivos fuente ni el manuscrito.
- Las fechas oficiales se verificaron en las fichas de Argentina.gob.ar/InfoLeg; la fecha de “última actualización” del corpus no pudo verificarse y debe completarse o eliminarse.

# Hallazgos sobre las respuestas de referencia

Este informe documenta los puntos de IX.1.6 que afectan la validez de la medición: procedencia del corpus, revisión del benchmark y respuestas esperadas. No modifica el benchmark ni el manuscrito.

## 1. Corpus: qué se puede afirmar y qué no

### 1.1. Estructura verificada

El archivo `data/codigo_de_mineria_actualizado_2025_08_02.json` contiene 482 nodos estructurales:

| Tipo | Cantidad |
| --- | ---: |
| Títulos | 22 |
| Secciones | 6 |
| Acápites | 55 |
| Nodos artículo | 398 |
| Apéndice | 1 |
| **Total** | **482** |

Los 398 nodos artículo se distribuyen así:

- 347 artículos del cuerpo principal (1–347);
- 15 disposiciones generales y transitorias (348–362);
- 36 artículos del apéndice (1–36).

Como el apéndice repite los números 1–36, hay **362 números únicos**. El artículo 239 está derogado y su texto está vacío; por eso hay **397 nodos artículo con texto**. El `398` del manuscrito es correcto como número de nodos, pero no como número de artículos numerados únicos. El `399` y el `245` son incompatibles con el corpus y con el propio HTML.

### 1.2. El corpus contiene texto posterior a 1997

La comparación de artículos concretos muestra que el corpus no es una copia literal del PDF/OCR de 1997. Los casos más claros:

| Artículo | Evidencia en el corpus | Evidencia en el OCR de 1997 | Consecuencia |
| --- | --- | --- | --- |
| 3 | Incluye “wollastonita” en el inciso c). | `texto_original_codigo_mineria.md` no incluye “wollastonita”; además, el OCR contiene “talio” donde el texto actual dice “tantalio”. | El corpus incorpora la sustitución de la Ley 25.225/1999. |
| 31 | Contiene 20.000/40.000 km² y 120 días. | El OCR corto termina en el artículo 24; el OCR largo no contiene el artículo 31 del cuerpo. | El corpus no puede provenir solo de ese OCR. |
| 215 | Contiene la escala de $1.900/$960. | El OCR largo contiene una versión incompatible, con porcentajes y remisiones distintas. | El corpus contiene una versión actualizada. |
| 221 | Contiene $960/$4.800 y la nota de la Ley 27.701/2022. | El OCR largo no contiene el artículo 221. | El corpus contiene texto que el OCR de 1997 no tiene. |
| 351 | Contiene el multiplicador 10/5/2 de la redacción actual. | El OCR largo contiene una redacción anterior (“duplicando... cánones suspendidos”). | El corpus fue actualizado después de 1997. |
| 355 | Contiene el informe de impacto ambiental de la Ley 24.585. | El OCR largo contiene una redacción anterior sobre cánones. | El corpus fue actualizado después de 1997. |

El HTML local `codigo_experimentos/data/inputs/html/codigo_minero_43797.html` contiene las notas de sustitución de la Ley 25.225/1999 (artículo 3), de la Ley 27.111/2015 (artículo 31), de la Ley 27.701/2022 (artículo 221) y de la Resolución 90/2023 (canon). El corpus coincide con ese HTML en los artículos verificados. Por tanto, la descripción más defendible es:

> El PDF del Boletín Oficial de 1997 aportó el texto base y el OCR histórico; el corpus final incorpora la versión actualizada de Infoleg para los artículos modificados. Las descargas automáticas se descartaron como pipeline principal, pero el texto actualizado de Infoleg sí quedó incorporado.

El autor debe confirmar si esa incorporación fue manual o mediante un parser y dejar registrada la ruta. La afirmación actual de que “ambas estrategias basadas en Infoleg se descartaron” es incompleta y contradice el contenido del corpus.

### 1.3. Metadatos incorrectos o no sustentados

| Campo | Valor en el JSON | Valor que surge de la fuente oficial | Acción |
| --- | --- | --- | --- |
| `fecha_sancion` | 1994-01-01 | 1886-11-25 (Ley 1.919/1886) | Corregir en el anexo y en toda tabla derivada. |
| `fecha_promulgacion` | 1994-01-10 | No verificada en la ficha consultada | No usar sin fuente; eliminar o completar. |
| `fecha_publicacion` | 1994-01-15 | Registro Nacional 1885/86, p. 578; texto ordenado: B.O. 1997-05-30 | Corregir. |
| `fecha_ultima_actualizacion` | 2024-12-09 | No verificada; el HTML contiene notas hasta 2023 | Reemplazar por fecha de consulta verificada o eliminar. |

Fuentes oficiales consultadas:

- Ley 1919/1886: `https://www.argentina.gob.ar/normativa/nacional/ley-1919-43797` (ficha con sanción 25-11-1886 y observación “PUBLICADA EN R.N. 1885/86, PAG.578”).
- Decreto 456/1997: `https://www.argentina.gob.ar/normativa/nacional/decreto-456-1997-43581` (texto ordenado; publicación 30-05-1997, B.O. 28658).

No se modificó el JSON fuente. Las tablas del manuscrito deben dejar de copiar esos metadatos sin verificación.

### 1.4. Calidad de extracción

El OCR disponible no permite afirmar que la extracción haya sido validada:

- `texto_original_codigo_mineria.md` contiene 24 marcadores de artículo (1–24), no el corpus completo.
- `output_codigo_mineria.md` contiene 265 marcadores, 247 números únicos, con omisiones como los artículos 34–41, 50–71, 97–100, 123, 136–145, 162–170, 195–196, 208–212, 218–232 y 239–242.
- El OCR largo contiene versiones antiguas de los artículos 215, 351 y 355, y no contiene los artículos 216, 221 ni 239 del cuerpo.
- El corpus contiene 397 nodos con texto y un nodo vacío (artículo 239).

El manuscrito dice que se hizo una “inspección manual de una muestra”. El proceso declarado fue una revisión manual por archivo, no un muestreo; no se conservó un conteo de discrepancias ni una tasa de error. Debe declararse que la extracción no fue validada cuantitativamente. La simple existencia de un OCR no demuestra fidelidad.

## 2. Revisión del benchmark: qué hizo la abogada

### 2.1. Archivos y relaciones

| Archivo | Rol | Evidencia |
| --- | --- | --- |
| `data/20250804_101435_generated_questions-SIN_REVISION.docx` | Casos generados por GPT-4.1, sin revisión | 389 párrafos; sin cambios registrados. |
| `data/20250804_101435_generated_questions - 130825-REVISADO.odt` | Casos revisados por la abogada | 389 párrafos; 166 regiones de cambio; 130 con texto; 80 párrafos con diferencias. |
| `data/20250804_101435_generated_questions - 130825.json` | Casos separados en preguntas/subpreguntas por el autor a partir del archivo revisado | 25 casos, 79 unidades, 166 referencias. |

El ODT conserva **comentarios y cambios** en el mismo documento. No es un archivo “limpio” de cambios aceptados. El JSON es la versión que el autor preparó después; no es una transcripción automática del ODT.

### 2.2. Tipos de intervención

La revisión incluye, al menos:

1. **Comentarios sobre el prompt de generación**: perfil “Derecho Minero”, mirada de género, unificación “Código de Minería/Código Minero”, “ante situaciones concretas”.
2. **Nombres y lugares**: Laura Álvarez, Raúl Juárez, Oscar Castro, Jorge Ramírez, Ricardo Ojeda, Martina Truman, Jorge Speed, Adrián López, Joaquín Gómez, Ofelia Maldonado, Ana López, Rodrigo Asís; San Juan, Chubut, Tierra del Fuego, Jujuy, Santa Cruz.
3. **Precisiones normativas**: “Código Minero” → “Código de Minería”; “normas” → “disposiciones del Código”; referencias al Título XVIII; artículos 2, 8, 10, 11, 17.
4. **Correcciones de redacción**: “1&” → “1”, “ningún” → “alguno”, “criaderode” → “criadero de”, “obligación/obligaciones”.
5. **Decisiones de alcance**: separar el caso final en casos individuales; aclarar la Ley 24.585; omitir el caso de hidrocarburos, que la revisora consideró fuera del alcance por la Ley 17.319.

No todas las intervenciones están incorporadas al JSON. Las más importantes que quedaron pendientes:

| Tema | Qué propuso la abogada | Estado en el JSON | Acción |
| --- | --- | --- | --- |
| Perfil profesional | “Derecho Minero”, mirada de género | No evaluable: el prompt de generación no está en el JSON | Actualizar el prompt solo si se regenera el benchmark. |
| Unificación terminológica | “Código de Minería” o “Código Minero”, no alternar | Aplicado: el JSON no contiene “Código Minero” | Mantener. |
| Nombres/lugares | Nombrar actores y localizar provincias | Aplicado en el JSON, aunque varias ubicaciones no están registradas como cambio rastreado (San Juan, Chubut, Tierra del Fuego, Jujuy) | Confirmar que fueron decisiones del autor y no inferencias. |
| Q5.1 | Pedir fundamento normativo | Parcial: la pregunta del JSON quedó reducida a la extensión | Restaurar la fórmula. |
| Q22–Q25 | Separar el caso combinado | Aplicado: el JSON tiene Q22–Q25 separadas | Mantener y documentar. |
| Q23 Río Turbio | No fue una recomendación de eliminación: la revisora pidió separar el caso combinado. Q23 no explicita el régimen especial. | Q23 sigue en el JSON | Revisar alcance: mantener, rotular o mover a anexo; no atribuir la eliminación a la revisora. |
| Q24 Ley 24.585 | Aclarar de qué trata la ley | No aplicado: sigue sin explicación | Aclarar o mover a anexo. |
| Q25 litio 2025 | Aclarar temporalidad | Parcial: dice “al año 2025”, sin versión normativa | Verificar artículo 351 y fecha de consulta. |
| Caso de hidrocarburos | Omitir por ser trabajo específico (Ley 17.319) | Aparente omisión: no está en el JSON, pero no puede probarse que la decisión se tomara después de la revisión; el ODT conserva el borrador | Confirmar la omisión y no usar el ODT como benchmark final. |

### 2.2.1. Conteo de preguntas intervenidas

| Indicador | Valor |
| --- | ---: |
| Preguntas del benchmark | 25 |
| Preguntas con alguna intervención | 18 |
| Preguntas con cambio de contenido o corrección aplicada | 17 |
| Preguntas solo con comentario no aplicado | 1 (Q24) |
| Preguntas sin intervención | 7 (Q7, Q8, Q9, Q12, Q13, Q15, Q20) |

El detalle está en `salidas/conteo_preguntas_revisadas.csv` y el método en `scripts/count_reviewed_questions.py`.

### 2.3. Consecuencia para el manuscrito

El manuscrito describe la revisión como “validación” por un profesional y, en metodología, como un proceso de cuatro etapas que incluye “validación final” y una segunda revisión. La evidencia disponible muestra **una revisión registrada en un ODT**, con comentarios y cambios, no una validación independiente ni una segunda revisión documentada. Propuesta:

- reemplazar “validación” por “revisión” cuando se describa el trabajo de la abogada;
- informar que la revisión quedó registrada en un ODT con control de cambios;
- no afirmar una segunda revisión salvo que se identifique revisor, fecha y resultado;
- distinguir “respuesta esperada revisada” de “respuesta esperada validada psicométricamente”.

## 3. Respuestas de referencia: hallazgos concretos

**Alcance:** los apartados 3.1 (Q1.2) y 3.2 (Q1.3) responden a la observación V.7 del jurado. El apartado 3.3 enumera hallazgos adicionales que no forman parte de las decisiones de esta tesis; las preguntas ya revisadas se mantienen como tales.


### 3.1. Q1.2: el artículo 8 no es la separación de la propiedad

**Texto del corpus:**

- Artículo 7: “Las minas son bienes privados de la Nación o de las Provincias, según el territorio en que se encuentren.”
- Artículo 8: “Concédese a los particulares la facultad de buscar minas, de aprovecharlas y disponer de ellas como dueños, con arreglo a las prescripciones de este Código.”
- Artículo 10: “Sin perjuicio del dominio originario del Estado reconocido por el Artículo 7, la propiedad particular de las minas se establece por la concesión legal.”
- Artículo 11: “Las minas forman una propiedad distinta de la del terreno en que se encuentran; pero se rigen por los mismos principios que la propiedad común, salvo las disposiciones especiales de este Código.”
- Artículo 18: “Las minas se conceden a los particulares por tiempo ilimitado.”

**Hallazgo:** el anexo Typst dice “La propiedad minera constituye un derecho real separado de la propiedad del suelo (art. 8)”. Es incorrecto: el artículo 8 no establece la separación; el artículo 11 sí. Además, el “tiempo ilimitado” está en el artículo 18, no en los artículos 10 y 11. Verificación: la respuesta del JSON y los artículos 8/11 del corpus y de `título_i.md` son correctos; el error está **solo en el anexo Typst**. **Corregir el anexo, no la respuesta JSON ni el benchmark.**

### 3.2. Q1.3: paráfrasis del artículo 17

**Texto del corpus:**

> Los trabajos de las minas no pueden ser impedidos ni suspendidos, sino cuando así lo exija la seguridad pública, la conservación de las pertenencias y la salud o existencia de los trabajadores.

**Texto de la respuesta esperada (JSON y anexo):**

> Solamente la autoridad competente puede establecer restricciones por motivos de seguridad pública, salud o conservación ambiental (artículo 17).

**Hallazgo:** la paráfrasis no es fiel:

- reemplaza “conservación de las pertenencias” por “conservación ambiental”;
- omite “salud o existencia de los trabajadores” y la reemplaza por “salud”;
- agrega “solamente”, que el texto no formula de ese modo.

No se afirma aquí cuál es la interpretación jurídica correcta; se afirma que la respuesta de referencia no reproduce el artículo que invoca. Verificación: el error está **en el JSON y en el anexo Typst**; el artículo 17 del corpus y de `título_i.md` es correcto. El benchmark v1 no se modifica porque ya fue usado para las 711 respuestas. Corregir el anexo del manuscrito para citar el artículo 17 literalmente y declarar la discrepancia como limitación; una nueva revisión o reevaluación corresponde a trabajo futuro.

### 3.3. Hallazgos adicionales fuera de alcance

La auditoría adicional detectó Q1.1 (etiqueta “inciso” en el artículo 2), Q13.2/Q13.3, Q22.1 y Q25 (referencias incompletas), y Q23/Q24 (alcance de regímenes especiales). **No forman parte de la respuesta al jurado**: las preguntas ya fueron revisadas por la profesional y se mantienen como tales. Quedan documentados en `salidas/unidades_benchmark.csv` y `salidas/decisiones_revision.csv` para trabajo futuro. No se propone una nueva revisión, un benchmark v2 ni un cambio de las respuestas ya evaluadas en esta tesis.

## 4. Resumen de decisiones

| Prioridad | Decisión | Estado |
| --- | --- | --- |
| Alta | Documentar el proceso de corpus en 8 pasos: PDF → o4 → Markdown → títulos → revisión manual/Infoleg → GPT-4.1 → DOCX → revisión profesional → ODT → JSON | Resuelta |
| Alta | Corregir 1.2 solo en el anexo Typst; el JSON y el corpus son correctos | Resuelta |
| Alta | No modificar el benchmark v1 por 1.3; corregir el anexo para citar el artículo 17 y declarar la discrepancia | Resuelta |
| Alta | Reemplazar “validación” por “revisión por una profesional”; no afirmar segunda revisión | Resuelta |
| Alta | Corregir fecha de sanción/publicación en anexo y tablas | Resuelta |
| Media | Documentar el conteo: 18 preguntas intervenidas, 17 corregidas, Q24 solo comentario, 7 sin intervención | Resuelta |
| — | Q23/Q24/Q13/Q22/Q25 y benchmark v2 | Fuera de alcance; no se incluyen en las decisiones |

## 5. Lo que queda fuera de este informe

- No se pronuncia sobre la interpretación jurídica definitiva de los artículos 17, 18 o 349; solo verifica la fidelidad textual de las respuestas de referencia.
- No modifica el benchmark ni el corpus.
- No recalcula las métricas de los jueces; el benchmark v1 se mantiene y cualquier cambio de respuestas requeriría una nueva versión y una reevaluación explícita, fuera del alcance de esta tesis.
- No se propone una nueva revisión profesional ni un benchmark v2; las preguntas ya revisadas se mantienen.

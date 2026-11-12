# Propuesta de edición del manuscrito (IX.1.6)

Este documento propone cambios concretos en los archivos `.typ` y en los README. **No modifica ningún archivo existente**: las citas “Actual” son el texto que hoy figura en el repositorio y las citas “Propuesto” son textos para que el autor revise antes de editar.

> **Este documento contiene textos de edición, no decisiones.** La evidencia está en `hallazgos_respuestas_referencia.md`; las decisiones locales, en `resumen_ejecutivo.md`; el registro global, en [`../DECISIONES_integradas.md`](../DECISIONES_integradas.md), Bloque D.

## 1. Procedencia y versión del corpus

### 1.1. `manuscrito/capitulos/06_capitulo_05_metodologia.typ`, líneas 51–58

**Actual**

> El texto del Código de Minería fue obtenido de la sección primera boletín oficial N°28.658 del día viernes 30 de mayo de 1997, descargado manualmente desde el sitio del Boletín Oficial de la República Argentina (...) en formato PDF. Este documento constituye la fuente primaria del corpus.
>
> Se exploraron dos estrategias adicionales de descarga desde el sistema Infoleg (...) Docling (...) Requests + BeautifulSoup (...). Ambas estrategias basadas en Infoleg resultaron en documentos incompletos o con errores de parsing, por lo que se descartaron en favor del procesamiento directo del PDF oficial.

**Propuesto**

> El texto base del Código de Minería se obtuvo de la sección primera del Boletín Oficial N.° 28.658, del 30 de mayo de 1997, que contiene el texto ordenado por el Decreto 456/1997. Ese PDF se procesó convirtiendo sus páginas a imagen y aplicando un modelo de visión; el OCR resultante se conservó como insumo histórico, pero fue parcial: por ejemplo, el Markdown corto de `texto_original_codigo_mineria.md` contiene solo los artículos 1 a 24.
>
> Para reflejar las modificaciones posteriores a 1997, el texto se contrastó con la versión actualizada publicada en Infoleg. El corpus final contiene texto de esa versión actualizada. La evidencia es verificable en los artículos que el PDF de 1997 no podía contener: el artículo 3 incluye “wollastonita” (Ley 25.225/1999), el artículo 31 contiene la redacción sustituida por la Ley 27.111/2015, y los artículos 215 y 221 contienen las actualizaciones de la Resolución 90/2023 y de la Ley 27.701/2022, respectivamente. Por lo tanto, el corpus no debe describirse como una copia exclusiva del PDF de 1997. El proceso efectivamente realizado fue: (1) conversión del PDF a imágenes y extracción a Markdown con o4; (2) división del Markdown en los archivos de `codigo_experimentos/data/law_data/titulos_codigo_mineria/`; (3) revisión manual de cada archivo y actualización de los artículos con el texto de Infoleg; (4) envío del Markdown a GPT-4.1 para generar las preguntas y respuestas; (5) exportación a DOCX; (6) revisión por una profesional del derecho; (7) devolución de un ODT con cambios y comentarios; (8) generación de `data/evaluation_questions_v20250804_101435.json`. El parser HTML se intentó, pero se descartó porque la revisión manual resultó más rápida y controlable.

**Por qué:** el repositorio contiene `codigo_experimentos/data/inputs/html/codigo_minero_43797.html` con las notas de las Leyes 25.225 y 27.111 y de la Resolución 90/2023. El corpus JSON coincide con ese HTML en los artículos 31, 215, 221, 351 y 355, y difiere del OCR de 1997. La afirmación “se descartaron” es cierta solo para el pipeline automático, no para el texto final.

### 1.2. `manuscrito/capitulos/02_capitulo_01_introduccion.typ`, líneas 21 y 45

**Actual (línea 21)**

> ... el Código de Minería Argentino extraído del archivo pdf descargado de la página del Boletín Oficial de la República Argentina y actualizado con los cambios publicados en el sitio Infoleg.

**Propuesto**

> ... el Código de Minería Argentino, cuyo texto base proviene del PDF del Boletín Oficial de 1997 y cuyo texto actualizado se contrastó con la versión publicada en Infoleg. El corpus final contiene la versión actualizada de los artículos modificados; el detalle de fuentes y fechas se presenta en el capítulo de metodología.

**Actual (línea 45)**

> Este módulo se encarga de la recopilación de los artículos del Código de Minería Argentino desde Infoleg, aplicando técnicas de web scraping...

**Propuesto**

> Este módulo reúne el texto base del PDF oficial de 1997, lo contrasta con la versión actualizada de Infoleg y normaliza los artículos en una estructura jerárquica. Las rutas de descarga automática se evaluaron, pero no fueron el pipeline principal.

**Por qué:** la introducción no debe sugerir que todo el corpus provino de un scraping exitoso de Infoleg ni que el PDF de 1997 fue la única fuente.

### 1.3. `manuscrito/capitulos/06_capitulo_05_metodologia.typ`, línea 74

**Actual**

> La calidad de la extracción se verificó mediante inspección manual de una muestra de artículos, comparando el texto extraído con el original en Infoleg.

**Propuesto**

> La extracción se revisó manualmente al actualizar cada archivo de título con el texto de Infoleg. No se conservó un registro cuantitativo de discrepancias ni una tasa de error; por tanto, no se afirma una validación estadística de la extracción. Se documenta como revisión manual por archivo y se declara la ausencia de una métrica de error.

**Por qué:** el repositorio no contiene un registro del tamaño de la muestra ni de la tasa de error. El OCR corto solo cubre 24 artículos y el OCR largo contiene 247 números únicos, con omisiones (por ejemplo, no contiene los artículos 216, 221 ni 239 del cuerpo). La frase actual no permite auditar la calidad.

### 1.4. Conteos del corpus

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`, línea 101.

**Actual**

> Los 399 artículos#footnote[362 en su cuerpo principal y 36 en su pie de apéndice.] constituyen las unidades normativas fundamentales...

**Propuesto**

> Los 398 nodos de tipo artículo —347 del cuerpo principal (1–347), 15 disposiciones generales y transitorias (348–362) y 36 del apéndice (1–36)— constituyen las unidades normativas fundamentales. El apéndice repite los números 1 a 36, por lo que el corpus contiene 362 números únicos. El artículo 239 está derogado y su texto está vacío, de modo que solo 397 nodos tienen contenido textual.

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`, línea 184.

**Actual**

> ... para los 398 artículos del corpus...

**Propuesto**

> ... para los 398 nodos de tipo artículo del corpus (397 con texto)...

**Archivo:** `manuscrito/capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ`, línea 111.

**Actual**

> ... citar el “artículo 1234 del Código de Minería” cuando el Código solo tiene 245 artículos.

**Propuesto**

> ... citar el “artículo 1234 del Código de Minería” cuando ese artículo no existe en el Código.

**Por qué:** el número 245 no coincide con ninguno de los conteos del propio corpus y no es necesario para el ejemplo. Si se quiere dar una cifra, usar “398 nodos artículo (362 números únicos)”.

## 2. Metadatos y revisión del benchmark

### 2.1. `manuscrito/capitulos/anexo_01.typ`, tabla de metadatos, líneas 249–259

**Actual**

| Campo | Valor |
| --- | --- |
| Fecha de sanción | 1994-01-01 |
| Última actualización | 2024-12-09 |
| Validación | Revisión por un profesional del derecho argentino |

**Propuesto**

| Campo | Valor |
| --- | --- |
| Fecha de sanción | 1886-11-25 |
| Texto ordenado | Decreto 456/1997 (B.O. 30/05/1997) |
| Fecha de consulta del texto actualizado | Consultar la fecha de la versión de Infoleg utilizada; no usar 2024-12-09 sin fuente |
| Validación | Revisión por una profesional del derecho argentino; cambios registrados en el ODT del 13/08/2025 |

**Por qué:** la ficha oficial de la Ley 1.919/1886 consigna sanción 25/11/1886 y publicación en el Registro Nacional 1885/86, p. 578. El Decreto 456/1997 aprobó el texto ordenado y se publicó el 30/05/1997. Las fechas 1994-01-01, 1994-01-10, 1994-01-15 y 2024-12-09 no surgen de las fuentes consultadas y no deben presentarse como datos verificados. La revisión fue realizada por una profesional; no hay evidencia en el repositorio de una segunda revisión independiente.

### 2.2. `manuscrito/capitulos/06_capitulo_05_metodologia.typ`, líneas 527–558

**Actual**

> Las preguntas del benchmark fueron generadas empleando GPT-4.1... compilación de las preguntas en un documento unificado para revisión.
>
> El benchmark contiene 25 preguntas... 79 subpreguntas que constituyen las unidades de evaluación independientes.
>
> Las preguntas generadas y sus respuestas esperadas fueron revisadas por un profesional... El proceso de validación se estructuró en... Revisión inicial... Verificación... Ajustes... Validación final... revisadas por segunda vez...

**Propuesto (resumen)**

> Las preguntas fueron generadas con GPT-4.1 y revisadas por una profesional del derecho argentino con experiencia en legislación minera. La revisión quedó registrada en un archivo ODT con control de cambios; el documento sin revisión se conserva por separado. La revisión produjo comentarios y ediciones sobre los enunciados, las respuestas y las referencias. El ODT contiene 166 regiones de cambio, 130 fragmentos con texto y 80 párrafos con diferencias. La revisión alcanzó 18 de las 25 preguntas: 17 tienen cambio de contenido o corrección aplicada y Q24 quedó solo con un comentario no incorporado; 7 no fueron intervenidas. No hubo una segunda revisión independiente.
>
> El benchmark final contiene 25 casos y 79 unidades de evaluación. Cada unidad incluye enunciado, respuesta esperada y referencias. La versión 1 del benchmark se generó a partir del documento revisado; no se crea una versión nueva en esta tesis.

**Por qué:** las 166 regiones de cambio incluyen comentarios editoriales y no todas son cambios aprobados. Por eso el texto propuesto no afirma “validación final” ni una segunda revisión; la decisión está en `resumen_ejecutivo.md` §2.

### 2.3. README raíz, línea 26

**Actual**

> ... un benchmark de 25 preguntas legales validadas por profesionales del derecho argentino...

**Propuesto**

> ... un benchmark de 25 preguntas legales revisado por una profesional del derecho argentino, con cambios registrados y criterios documentados...

**Por qué:** hay una sola profesional revisora y el proceso de revisión incluyó comentarios no resueltos; “validadas por profesionales” en plural no es exacto.

## 3. Respuestas de referencia del anexo

### 3.1. Subpregunta 1.2: artículo 8 y “tiempo ilimitado”

**Actual (anexo, línea 305)**

> El Estado puede otorgar la concesión sin consentimiento de la propietaria del terreno. El artículo 7 establece que las minas son bienes privados de la Nación o de las provincias según el territorio. Los artículos 10 y 11 determinan que sin perjuicio del dominio del Estado, las minas se conceden a los particulares por tiempo ilimitado. La propiedad minera constituye un derecho real separado de la propiedad del suelo (art. 8).

**Propuesto**

> El Estado puede otorgar la concesión sin el consentimiento de la propietaria del terreno. El artículo 7 establece que las minas son bienes privados de la Nación o de las provincias según el territorio. El artículo 10 dispone que, sin perjuicio del dominio originario del Estado, la propiedad particular de las minas se establece por concesión legal; el artículo 11 establece que las minas forman una propiedad distinta de la del terreno en que se encuentran; y el artículo 18 añade que las minas se conceden a los particulares por tiempo ilimitado. Por tanto, la propiedad minera es distinta de la propiedad del suelo y el consentimiento del superficiario no es el título de la concesión.

**Por qué:** el artículo 8 se refiere a la facultad de buscar minas, aprovecharlas y disponer de ellas, no a la separación de la propiedad. El “tiempo ilimitado” está en el artículo 18, no en los artículos 10 y 11. La respuesta JSON de 1.2 y los artículos 8/11 del corpus y de `título_i.md` son correctos; el error está solo en el anexo Typst. El artículo 18 se agrega solo si se conserva la frase sobre “tiempo ilimitado”. La decisión está en `resumen_ejecutivo.md` §2.

### 3.2. Subpregunta 1.3: paráfrasis del artículo 17

**Actual (anexo, línea 307, y respuesta JSON de 1.3)**

> La propietaria solo puede oponerse por razones de seguridad o ambientales (art. 17), pero no puede invocar la propiedad del suelo para impedirla.

**Propuesto**

> El artículo 17 dispone que los trabajos de las minas no pueden ser impedidos ni suspendidos sino cuando lo exija la seguridad pública, la conservación de las pertenencias y la salud o existencia de los trabajadores. Por tanto, la propietaria no puede invocar sin más su propiedad para impedir la explotación; cualquier oposición debe encuadrarse en alguna de esas causales y ser resuelta por la autoridad competente.

**Por qué:** el artículo 17 no dice “seguridad o ambientales” ni usa la palabra “solo”. La paráfrasis actual omite la conservación de las pertenencias y la salud o existencia de los trabajadores, y agrega una categoría ambiental que no está en el texto. El error está en el JSON y en el anexo Typst; el artículo 17 del corpus y de `título_i.md` es correcto. La decisión sobre el benchmark v1 está en `resumen_ejecutivo.md` §2.

## 4. Otras correcciones de consistencia

- `manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ`, línea 19: “revisadas por un profesional” es correcto en singular; no cambiar a “profesionales”. Si se conserva “validado”, aclarar que se refiere a revisión editorial, no a validación psicométrica.
- `README.md`, línea 170: “A los profesionales del derecho argentino que colaboraron en la validación del benchmark” → “A la profesional del derecho argentino que revisó el benchmark”.
- `manuscrito/capitulos/06_capitulo_05_metodologia.typ`, línea 70: el módulo `02_html_infoleg_parser` se presenta como parte del pipeline; aclarar que fue un prototipo y que la actualización final se hizo manualmente. No presentarlo como el pipeline principal.
- `manuscrito/capitulos/anexo_01.typ`, línea 236: “revisadas y validadas por un profesional” → “revisadas por una profesional”; “validado” implica un proceso que no está documentado.
- `manuscrito/capitulos/anexo_01.typ`, línea 238: el enlace al repositorio es correcto; verificar que la versión publicada incluya `data/20250804_101435_generated_questions-SIN_REVISION.docx` y el ODT revisado, o documentar que son evidencia interna y no forman parte del benchmark publicado.

## 5. Orden de aplicación

1. Corregir metadatos y conteos (`§1.4` y `§2.1`), que no dependen de decisiones jurídicas.
2. Reescribir la procedencia del corpus y la descripción de la revisión (`§1.1–1.3` y `§2.2–2.3`).
3. Corregir el anexo de 1.2 y 1.3 (`§3.1–3.2`).
4. Sincronizar README, anexo y conclusiones (`§4`).

Las decisiones que respaldan estos cambios están solo en `resumen_ejecutivo.md` §2.

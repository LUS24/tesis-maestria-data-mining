// Anexos
#import "@preview/tablem:0.3.0": three-line-table
#counter(heading).update(0)
#set heading(numbering: "A.1")

= Estructura del Repositorio de Código <anexo-repositorio>

== Organización de Carpetas

El repositorio se organiza en cuatro áreas: el manuscrito, el código de experimentación, los datos compartidos y los paquetes de corrección y verificación asociados a la revisión del tribunal. La carpeta `archivo/` contiene material auxiliar y no forma parte del núcleo reproducible; está excluida del control de versiones.

```
tesis/
├── manuscrito/                      # Manuscrito en Typst
│   ├── main.typ                     # Documento principal
│   ├── formato.typ                  # Estilos y página apaisada
│   ├── referencias.bib              # Bibliografía
│   ├── capitulos/                   # Capítulos y anexos
│   ├── media/                       # Figuras y diagramas
│   ├── codigo-helpers/              # Scripts de apoyo para figuras
│   └── salidas/                     # PDFs compilados (no versionados)
│
├── codigo_experimentos/             # Pipeline experimental (Python, uv)
│   ├── main.py                      # Punto de entrada
│   ├── pyproject.toml / uv.lock     # Entorno y dependencias
│   ├── performed_tasks_summary.md   # Resumen de tareas
│   ├── data/                        # Datos locales de experimentación
│   ├── part_0/                      # Extracción de texto de PDF (o4-mini)
│   ├── part_a/                      # Generación del benchmark (GPT-4.1)
│   ├── part_b/                      # Base relacional del benchmark (cancelada)
│   ├── part_c/                      # Creación de la base vectorial (Milvus)
│   ├── part_d/                      # Recuperación baseline
│   ├── part_e/                      # Respuestas sin RAG + métricas
│   ├── part_f/                      # Respuestas con RAG básico + métricas
│   ├── part_g/                      # Respuestas con Agentic-RAG + logs
│   ├── part_h/                      # Integración de resultados
│   ├── part_h_1/                    # Evaluación LLM-as-a-Judge
│   ├── part_i/                      # Preparación de datos para análisis
│   └── part_j/                      # Análisis exploratorio y de costos
│
├── data/                            # Datos compartidos
│   ├── codigo_de_mineria_*.json     # Corpus del Código de Minería
│   └── evaluation_questions_*.json  # Benchmark v1 (congelado)
│
├── analisis-valoracion-jurado/      # Correcciones y verificación posteriores
│   ├── correccion-01-analisis-estadistico/
│   ├── correccion-02-diagnostico-gpt-5-nano/
│   ├── correccion-03-documentar-api-eliminar-determinismo/
│   ├── correccion-04-declarar-factores-pub-prompts-etc/
│   ├── correccion-05-actualizacion-conclusiones-y-analisis-costos/
│   ├── correccion-06-precisar-corpus-revisar-respuestas/
│   ├── correccion-07-forma-y-bibliografia/
│   └── verificacion-analisis-estadistico/
│
└── archivo/                         # Material auxiliar (no versionado)
```

Los artefactos que el cuerpo cita viven en dos lugares. Los que sostienen los resultados —el modelo ordinal, los escenarios de sensibilidad, las figuras y las tablas canónicas— están en `analisis-valoracion-jurado/correccion-01-analisis-estadistico/`, con `run_all.sh` como punto de entrada y `salidas/` como destino. Los que auditan la corrida —la clasificación de las respuestas no sustantivas, los logs y las evaluaciones de los jueces— están en `analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/`, y la reconciliación de cifras y las métricas de recuperación, en `analisis-valoracion-jurado/verificacion-analisis-estadistico/`. Los prompts y la configuración de los agentes se documentan en el capítulo de metodología y en `analisis-valoracion-jurado/correccion-04-declarar-factores-pub-prompts-etc/`; no existe un anexo de prompts dentro del manuscrito.

== Descripción de Componentes Principales

=== Manuscrito (`manuscrito/`)

- *`main.typ`*: documento principal; incluye portada, capítulos, bibliografía y anexos, y toma la hora de compilación como entrada para la versión.

- *`media/`*: figuras vectoriales y diagramas referenciados por el texto. Las figuras canónicas del reanálisis se copiaron desde `correccion-01/figuras/` para que el manuscrito no dependa de rutas externas.

- *`codigo-helpers/`*: scripts de apoyo para generar diagramas y figuras del manuscrito.

=== Pipeline de Experimentación (`codigo_experimentos/`)

#figure(
  three-line-table(
    columns: (auto, auto),
    [
      | *Directorio* | *Función*                                                                                                                                                                                                                                                      |
      | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
      | `part_0/`    | Extracción de texto de los PDF del Código de Minería mediante modelos de visión (o4-mini) y OCR estructurado.                                                                                                                                                    |
      | `part_a/`    | Generación del benchmark: segmentación del Código de Minería por títulos y generación de preguntas tipo caso de estudio legal mediante GPT-4.1, con respuestas esperadas y artículos de referencia.                                                                |
      | `part_b/`    | Base relacional del benchmark: enfoque cancelado; el benchmark se conserva en archivos JSON.                                                                                                                                                                   |
      | `part_c/`    | Creación de la base de datos vectorial Milvus con embeddings de 768 dimensiones generados por el modelo `hiiamsid/sentence_similarity_spanish_es`. Población con artículos del Código de Minería.                                                                  |
      | `part_d/`    | Pruebas de recuperación baseline: evaluación de la precisión de búsqueda vectorial para las preguntas del benchmark.                                                                                                                                           |
      | `part_e/`    | Generación de respuestas sin RAG con tres modelos (gpt-5-nano, gpt-5-mini, gpt-5). Cálculo de más de 11 métricas de similitud textual y semántica.                                                                                                             |
      | `part_f/`    | Generación de respuestas con RAG básico: búsqueda vectorial top-10 inyectada como contexto en el prompt. Mismos modelos y métricas.                                                                                                                            |
      | `part_g/`    | Generación de respuestas con Agentic-RAG: arquitectura de dos agentes activos (Especialista Legal, Recuperación) implementada con Pydantic AI. Un tercer agente (Calidad) fue diseñado e implementado pero desactivado en la configuración experimental final. |
      | `part_h/`    | Integración de resultados de las tres estrategias en un archivo JSON unificado con todas las métricas.                                                                                                                                                         |
      | `part_h_1/`  | Evaluación LLM-as-a-Judge mediante `pydantic_evals` con tres jueces (DeepSeek, Grok, Kimi K2) y dos rúbricas de evaluación.                                                                                                                                    |
      | `part_i/`    | Transformación de datos JSON anidados a CSVs tabulares. Visualizaciones con Polars y plotnine (ggplot2).                                                                                                                                                       |
      | `part_j/`    | Análisis exploratorio en Python: exploración descriptiva y correlación, verificación de normalidad, Kruskal-Wallis con post-hoc de Dunn, Scheirer-Ray-Hare, análisis de costos y acuerdo inter-juez. La estimación definitiva —modelo ordinal acumulativo mixto con efectos aleatorios por caso y unidad, Friedman/Wilcoxon, bootstrap por casos y escenarios de sensibilidad— se realizó después, en R y Python, en `analisis-valoracion-jurado/correccion-01-analisis-estadistico/`. |
    ],
  ),
  caption: [Descripción de los directorios del pipeline de experimentación.],
) <tabla-pipeline-directorios>

=== Correcciones y Verificación (`analisis-valoracion-jurado/`)

Los directorios `correccion-01` a `correccion-07` se agregaron después de la primera versión del manuscrito para responder a la revisión del tribunal. No reemplazan al pipeline: lo auditan y, cuando corresponde, lo reestiman.

- *`correccion-01-analisis-estadistico/`*: modelo ordinal mixto, Friedman y Wilcoxon, bootstrap por casos, escenarios de sensibilidad, figuras y tablas canónicas. Es la fuente de las cifras del capítulo de evaluación.

- *`correccion-02-diagnostico-gpt-5-nano/`*: clasificación de las 711 respuestas, auditoría de los logs de los agentes y de las evaluaciones de los jueces, y revisión manual de las salidas no sustantivas.

- *`correccion-03-documentar-api-eliminar-determinismo/`*: payloads registrados, perfiles de Pydantic AI y tabla de parámetros solicitados, registrados y efectivos.

- *`correccion-04-declarar-factores-pub-prompts-etc/`*: auditoría de sesiones, prompts, factores confundidos y arquitectura efectiva.

- *`correccion-05-actualizacion-conclusiones-y-analisis-costos/`*: costos por celda, costo por respuesta correcta y frontera de Pareto.

- *`correccion-06-precisar-corpus-revisar-respuestas/`*: linaje del corpus, conteos de nodos y revisión de preguntas y respuestas de referencia.

- *`correccion-07-forma-y-bibliografia/`*: auditoría bibliográfica y correcciones de forma.

- *`verificacion-analisis-estadistico/`*: recálculo independiente de alpha, reconciliación de cifras del análisis previo y métricas de recuperación.

=== Principales Dependencias del Proyecto

#figure(
  three-line-table(
    columns: (auto, auto, auto),
    [
      | *Librería*              | *Versión* | *Función*                                    |
      | :---------------------- | :-------- | :------------------------------------------- |
      | `pydantic-ai`           | `1.1.0`   | Framework de agentes con herramientas        |
      | `pymilvus`              | `≥2.6.3`  | Cliente de la base de datos vectorial Milvus |
      | `sentence-transformers` | `≥5.1.1`  | Generación de embeddings                     |
      | `openai`                | `≥1.97.1` | Cliente del proveedor de LLM                 |
      | `polars`                | `≥1.35.2` | Transformación y análisis de datos           |
      | `bert-score`            | `≥0.3.13` | Métrica semántica BERTScore                  |
      | `rouge-score`           | `≥0.1.2`  | Métricas ROUGE                               |
      | `levenshtein`           | `≥0.27.1` | Distancia de edición                         |
      | `scikit-learn`          | `≥1.7.2`  | Utilidades de aprendizaje automático         |
      | `plotnine`              | `≥0.15.1` | Visualización estilo ggplot2                 |
      | `sqlmodel`              | `≥0.0.24` | ORM para bases de datos SQL                  |
      | `krippendorff`          | `≥0.8.2`  | Métricas de acuerdo inter-evaluador          |
    ],
  ),
  caption: [Principales dependencias del proyecto (Python ≥ 3.13).],
) <tabla-dependencias>

= Ejemplos de Consultas y Respuestas <anexo-ejemplos>

Este anexo presenta ejemplos representativos de consultas y respuestas del sistema para las tres estrategias evaluadas. Se seleccionó la primera subpregunta del benchmark (dominio del yacimiento de litio) para ilustrar las diferencias entre las configuraciones.

== Consulta de Ejemplo

*Escenario:* El ingeniero Juan Pérez ha descubierto un importante yacimiento de litio en una finca privada ubicada en territorio de la Provincia de Salta. La propietaria de la finca, la Sra. Marta Gómez, sostiene que, por ser dueña del suelo, es también dueña exclusiva del litio allí existente y que nadie puede explotarlo sin su consentimiento. Juan Pérez, por su parte, desea solicitar una concesión de explotación al Estado, argumentando que el litio es propiedad del Estado.

*Subpregunta 1:* Analice a quién corresponde el dominio del yacimiento de litio descubierto y determine a qué categoría de minas pertenece dicho yacimiento, fundamentando su respuesta en los artículos pertinentes del Código de Minería.

*Respuesta esperada:* El yacimiento de litio descubierto corresponde a la primera categoría de minas, según el artículo 3° inciso a) del Código de Minería Argentino. Esta categoría está compuesta por sustancias metalíferas, incluyendo expresamente el litio. Las minas de la primera categoría "pertenecen exclusivamente al Estado, y sólo pueden explotarse en virtud de concesión legal otorgada por autoridad competente" (art. 2° inc. 1). Por lo tanto, el dominio originario del yacimiento es estatal, aunque la mina se encuentre en una propiedad privada.

*Artículos de referencia:* Art. 2 (inciso 1), Art. 3 (inciso a).

== Consultas sin RAG

A continuación se presenta la respuesta generada por el modelo gpt-5-nano sin acceso a contexto adicional.

#figure(
  block(
    width: 100%,
    inset: 10pt,
    stroke: 0.5pt + luma(180),
    radius: 4pt,
    [
      *Modelo:* gpt-5-nano (sin RAG) \
      *Tokens de entrada:* 315 | *Tokens de salida:* 7818 | *Costo:* USD 0,003 \

      _Respuesta (extracto):_ "Dominio del yacimiento: correspondería a la Nación. La categoría es dominio de minas y yacimientos de minerales en el subsuelo (derecho minero)..." \

      La respuesta es extensa (ratio de longitud 4,62 respecto a la esperada) y carece de citaciones precisas a artículos específicos del Código de Minería. El modelo recurre a conocimiento general sobre derecho minero sin poder fundamentar en artículos concretos.
    ],
  ),
  caption: [Respuesta sin RAG (gpt-5-nano) para la subpregunta 1.1.],
) <ejemplo-sin-rag>

#figure(
  three-line-table(
    columns: (auto, auto),
    [
      | *Métrica*                  | *Valor* |
      | :------------------------- | ------: |
      | Exact Match                |   0,000 |
      | Token F1                   |   0,198 |
      | Jaccard                    |   0,110 |
      | Levenshtein                |   0,173 |
      | BLEU                       |   0,018 |
      | ROUGE-1                    |   0,208 |
      | ROUGE-2                    |   0,068 |
      | SBERT Similarity (español) |   0,797 |
      | BERTScore                  |   0,710 |
      | Ratio de longitud          |    4,62 |
    ],
  ),
  caption: [Métricas de la respuesta sin RAG (gpt-5-nano) para la subpregunta 1.1.],
) <metricas-sin-rag>

Se observa que las métricas léxicas (Token F1, Jaccard, BLEU) son bajas debido a la extensión excesiva y la ausencia de terminología legal específica. Las métricas semánticas (SBERT, BERTScore) capturan una similitud temática moderada, indicando que el modelo aborda el tema correcto sin la precisión requerida.

== Consultas con RAG Básico

En la configuración de RAG básico, el sistema realiza una búsqueda vectorial que retorna los 10 fragmentos más similares del Código de Minería. Estos fragmentos se inyectan en el prompt del sistema como contexto antes de la generación.

#figure(
  block(
    width: 100%,
    inset: 10pt,
    stroke: 0.5pt + luma(180),
    radius: 4pt,
    [
      *Modelo:* gpt-5-nano (RAG básico, top-10) \
      *Tokens de entrada:* 3.858 | *Tokens de salida:* 8.638 | *Costo:* USD 0,0036 | *Fragmentos recuperados:* 10 \

      _Respuesta (extracto):_ "Bajo el Código de Minería Argentino (CMA), la titularidad de un yacimiento mineral depende de a cuál de las tres categorías de minas reconoce el art. 2 del CMA... Si el yacimiento de litio encuadrara en la categoría 1, el dominio del yacimiento correspondería al Estado y la explotación requeriría concesión administrativa... En ausencia de una clasificación específica de la autoridad minera que sitúe el yacimiento de litio en la categoría 3, la posición más conservadora es que el litio del subsuelo de una finca privada pertenece al Estado (categoría 1) y su explotación debe hacerse mediante concesión administrativa." \

      Con los artículos recuperados como contexto, la respuesta reconoce la existencia del sistema de categorías y la primacía del dominio estatal, aunque no identifica con precisión el litio como sustancia de primera categoría: la clasificación queda condicionada a una decisión de la autoridad minera ("podría caer en cualquiera de estas categorías"). Las citas se concentran en los artículos 2, 25 y 99 recuperados, y no en el artículo 3 que resulta aplicable al caso.
    ],
  ),
  caption: [Respuesta con RAG básico (gpt-5-nano) para la subpregunta 1.1.],
) <ejemplo-rag-basico>

La mejora principal del RAG básico se manifiesta en las métricas léxicas, que reflejan una mayor coincidencia terminológica con la respuesta esperada, y en las métricas de evaluación por jueces, donde la precisión legal mejora por la capacidad de citar artículos específicos.

== Consultas con Agentic-RAG

En la configuración Agentic-RAG, el flujo de procesamiento activo involucra dos agentes:

+ *Agente Especialista Legal:* recibe la pregunta y determina que necesita información del Código de Minería. Invoca la herramienta `retrieve_relevant_documents`.

+ *Agente de Recuperación:* descompone la consulta en subconsultas semánticas (por ejemplo, "categorías de minas litio", "dominio estatal minas primera categoría"). Ejecuta múltiples búsquedas vectoriales (hasta 6) y consolida los resultados.

+ *Agente Especialista Legal:* con los fragmentos recuperados, genera la respuesta final citando los artículos pertinentes.

Nota: un tercer agente ---el Agente de Calidad--- fue diseñado e implementado para evaluar la pertinencia de los fragmentos recuperados y proveer retroalimentación, pero fue desactivado en la configuración experimental final.

#figure(
  block(
    width: 100%,
    inset: 10pt,
    stroke: 0.5pt + luma(180),
    radius: 4pt,
    [
      *Modelo:* gpt-5-nano (Agentic-RAG; Agente de Recuperación: gpt-5) \
      *Agente Especialista Legal:* 2.706 tokens de entrada, 7.395 de salida, USD 0,00285 \
      *Agente de Recuperación:* 16.787 tokens de entrada, 7.257 de salida, USD 0,05037 \
      *Costo total:* USD 0,05322 \

      _Respuesta (extracto):_ "- Categoría del litio: El litio es una sustancia de primera categoría conforme al Artículo 3, inciso a, del Código de Minería Argentino («Corresponden a la primera categoría: a) Las sustancias metalíferas... litio»)... - Dominio del yacimiento: Las minas son bienes privados de la Nación o de las Provincias, según el territorio en que se encuentren (Art. 7). El dominio originario de las minas es del Estado; sin perjuicio de ello, la propiedad particular de las minas se establece por concesión legal (Art. 10). Las minas forman una propiedad distinta de la del terreno en que se encuentran (Art. 11)... - Síntesis para el caso: En Salta, la Sra. Marta Gómez es dueña del suelo, pero no del litio; el yacimiento recae sobre dominio estatal y solo puede ser explotado por medio de una concesión otorgada por la autoridad competente." \

      La respuesta identifica correctamente el litio como sustancia de primera categoría (art. 3, inc. a) y funda el dominio estatal en los artículos 7, 10 y 11, con una extensión y una estructura de citación más próximas a la respuesta esperada que en el caso del RAG básico. El costo del Agente de Recuperación (USD 0,0504, con gpt-5) resulta más de diecisiete veces superior al del Agente Especialista Legal (USD 0,0029, con gpt-5-nano).
    ],
  ),
  caption: [Respuesta con Agentic-RAG (gpt-5-nano) para la subpregunta 1.1.],
) <ejemplo-agentic-rag>

La ventaja del enfoque agéntico se evidencia en la capacidad de descomponer consultas complejas en búsquedas más específicas, lo que mejora la precisión de la recuperación y, consecuentemente, la calidad de la respuesta generada.

= Benchmark Empleado <anexo-benchmark>

Este anexo presenta el benchmark utilizado para la evaluación del sistema. El conjunto de datos consta de 25 preguntas principales tipo caso de estudio legal, que se descomponen en 76 subpreguntas explícitas más 3 preguntas evaluadas como unidad única, totalizando 79 unidades de evaluación. Las preguntas fueron generadas a partir de los títulos del Código de Minería Argentino mediante GPT-4.1, y las respuestas esperadas fueron revisadas por una profesional del derecho argentino con experiencia en legislación minera; no hubo una segunda revisión independiente.

A continuación se describen los metadatos del conjunto de datos y se reproducen, a modo de ejemplo, dos de las 25 preguntas con sus respuestas esperadas. El benchmark completo —las 25 preguntas con sus subpreguntas, respuestas esperadas y artículos de referencia— se encuentra disponible en el repositorio de código del proyecto: #link("https://github.com/LUS24/tesis-maestria-data-mining")[https://github.com/LUS24/tesis-maestria-data-mining], en el directorio `data/`.

== Metadatos del Benchmark

#figure(
  three-line-table(
    columns: (auto, auto),
    [
      | *Campo*                         | *Valor*                                          |
      | :------------------------------ | :----------------------------------------------- |
      | Título                          | Evaluación derecho minero argentino              |
      | Norma evaluada                  | Código de Minería de la República Argentina      |
      | Jerarquía normativa             | Código                                           |
      | Fecha de sanción                | 1886-11-25                                       |
      | Texto ordenado                  | Decreto 456/1997 (B.O. 30/05/1997)               |
      | Estado                          | En vigencia                                      |
      | Autoridad de sanción            | Congreso de la Nación Argentina                  |
      | Total de preguntas principales  | 25                                               |
      | Total de unidades de evaluación | 79                                               |
      | Tipo de pregunta                | Caso de estudio legal con múltiples subpreguntas |
      | Generación                      | GPT-4.1 a partir de títulos del Código de Minería    |
      | Validación                      | Revisión por una profesional del derecho argentino |
    ],
  ),
  caption: [Metadatos del benchmark de evaluación.],
) <tabla-metadatos-benchmark>

== Estructura del Benchmark

Las 25 preguntas se distribuyen entre los títulos del Código de Minería Argentino, cubriendo temas como: dominio originario de las minas y clasificación (Título I), conflictos de interés de funcionarios judiciales (Título II), permisos de exploración y límites legales (Título III), derechos del descubridor y registro de minas (Título IV), dimensiones de pertenencias para sustancias de primera categoría (Título V), obligaciones ambientales y servidumbres mineras (Título VI), entre otros.

Cada pregunta se formula como un caso de estudio legal con un escenario narrativo, seguido de subpreguntas específicas que requieren la identificación y aplicación de artículos concretos del Código de Minería. Las respuestas esperadas incluyen la fundamentación legal con citación de los artículos pertinentes. El benchmark completo está disponible en el repositorio de código del proyecto (`data/`).

== Ejemplos de Preguntas

A continuación se presentan dos preguntas representativas del benchmark a modo de ejemplo.

=== Pregunta 1: Dominio de Yacimiento de Litio en Propiedad Privada

*Escenario:* El ingeniero Juan Pérez descubre un yacimiento de litio en una finca privada en Salta. La propietaria (Marta Gómez) reclama propiedad exclusiva por ser dueña del suelo. Juan Pérez desea solicitar concesión al Estado.

*Subpreguntas:*
+ Analice a quién corresponde el dominio del yacimiento de litio y determine a qué categoría de minas pertenece.
+ ¿Puede el Estado otorgar la concesión de explotación a Juan Pérez sin el consentimiento de la propietaria del terreno?
+ Explique si la Sra. Gómez puede impedir legítimamente la explotación minera en su propiedad.

*Artículos de referencia:* 2 (inc. 1), 3 (inc. a), 7, 8, 10, 11, 13, 17.

=== Pregunta 2: Conflictos de Interés de Funcionario Judicial con Actividad Minera

*Escenario:* El juez Raúl Juárez posee el 50% de participación en una mina adquirida antes de su designación. Posteriormente, su esposa hereda otra mina en el mismo distrito. Un ingeniero estatal intenta reclamar derechos sobre ambas minas.

*Subpreguntas:*
+ ¿Puede el juez Juárez mantener la participación minera adquirida antes de su nombramiento?
+ ¿Puede la esposa del juez adquirir legalmente una mina por herencia pese a la prohibición de conflicto de interés?
+ ¿Puede el ingeniero estatal reclamar derechos sobre las minas del juez invocando las restricciones legales?

*Artículos de referencia:* 22 (inc. 2, 3), 23, 24.

== Respuestas Esperadas (Ejemplos)

Las respuestas esperadas del benchmark se elaboraron a partir del texto vigente del Código de Minería Argentino. Cada respuesta incluye la fundamentación legal con citación de artículos específicos. A continuación se presentan las respuestas esperadas para las dos preguntas de ejemplo.

=== Respuestas a la Pregunta 1

*Subpregunta 1.1:* El yacimiento de litio corresponde a la primera categoría de minas, según el artículo 3° inciso a) del Código de Minería. Esta categoría comprende sustancias metalíferas, incluyendo expresamente el litio. Las minas de primera categoría "pertenecen exclusivamente al Estado, y sólo pueden explotarse en virtud de concesión legal otorgada por autoridad competente" (art. 2° inc. 1). El dominio originario del yacimiento es estatal, independientemente de la propiedad del suelo.

*Subpregunta 1.2:* El Estado puede otorgar la concesión sin consentimiento de la propietaria del terreno. El artículo 7 establece que las minas son bienes privados de la Nación o de las provincias según el territorio. Los artículos 10 y 11 determinan que sin perjuicio del dominio del Estado, las minas se conceden a los particulares por tiempo ilimitado. La propiedad minera constituye una propiedad distinta de la del terreno en que se encuentra (art. 11).

*Subpregunta 1.3:* La Sra. Gómez no puede impedir la explotación. La actividad minera es declarada de utilidad pública (art. 13), lo que prevalece sobre la propiedad superficiaria. La propietaria solo puede oponerse cuando lo exija la seguridad pública, la conservación de las pertenencias y la salud o existencia de los trabajadores (art. 17), pero no puede invocar la propiedad del suelo para impedirla.

=== Respuestas a la Pregunta 2

*Subpregunta 2.1:* El juez Juárez puede mantener la participación minera adquirida antes de su designación. El artículo 23 establece que las restricciones del artículo 22 no aplican a las minas adquiridas con anterioridad al nombramiento del funcionario.

*Subpregunta 2.2:* La esposa puede adquirir legalmente la mina por herencia. El artículo 22 inciso 3 prohíbe la adquisición de minas por ciertos funcionarios y sus familiares, pero el artículo 23 exceptúa las adquisiciones por sucesión hereditaria, que constituyen un modo de adquisición involuntario y protegido legalmente.

*Subpregunta 2.3:* El ingeniero estatal no puede reclamar derechos sobre las minas. El artículo 22 inciso 2 le prohíbe, como empleado del Estado vinculado a la actividad minera, adquirir minas o participar en sociedades mineras. El artículo 24 establece la nulidad de las adquisiciones realizadas en contravención del artículo 22, lo que afectaría cualquier intento del ingeniero por apropiarse de las minas.

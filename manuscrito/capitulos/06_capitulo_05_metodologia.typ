#import "@preview/mmdr:0.2.2": mermaid
#import "@preview/tablem:0.3.0": three-line-table

= Metodología e Implementación <cap:metodologia>

== Introducción

Este capítulo describe la metodología empleada para diseñar, implementar y evaluar el sistema Agentic-RAG para consulta de normativa argentina. Se detalla el enfoque metodológico adoptado, las fases del proyecto, las decisiones de diseño, los criterios de selección de herramientas y modelos, así como los detalles técnicos de la implementación. La implementación se organizó en módulos independientes ejecutados como notebooks de Jupyter, lo que favorece la reproducibilidad y la iteración.

== Enfoque Metodológico

=== Diseño de la Investigación

Los experimentos descritos en este capítulo fueron realizados durante el segundo semestre de 2025. Los modelos, versiones de librerías y servicios de API empleados corresponden a las versiones disponibles en dicho período. El campo de los grandes modelos de lenguaje se caracteriza por ciclos de lanzamiento cortos; los resultados deben interpretarse en ese contexto temporal.

La investigación sigue un enfoque experimental cuantitativo con diseño factorial en el que se comparan tres estrategias de generación de respuestas —sin recuperación (no RAG), RAG básico y Agentic-RAG— combinadas con tres modelos de lenguaje de la familia GPT-5 (nano, mini y estándar), lo que da lugar a nueve configuraciones experimentales. Este diseño permite evaluar tanto los efectos principales de cada factor como su interacción, tal como se resume en la @tabla-diseno-factorial.

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto),
    [
      | *Estrategia* | *gpt-5-nano* | *gpt-5-mini* | *gpt-5* |
      | :----------- | :----------: | :----------: | :-----: |
      | Sin RAG      |      ✓      |      ✓      |   ✓    |
      | RAG básico   |      ✓      |      ✓      |   ✓    |
      | Agentic-RAG  |      ✓      |      ✓      |   ✓    |
    ],
  ),
  caption: [Diseño factorial 3 × 3 del experimento. Cada celda marcada representa una configuración experimental evaluada.],
) <tabla-diseno-factorial>

=== Fases del Proyecto

El proyecto se estructura en las siguientes fases:

+ *Extracción de datos*: descarga de textos legales, conversión de texto original a texto estructurado y normalización del corpus.
+ *Generación de preguntas*: creación de un benchmark de preguntas con respuestas esperadas a partir de los títulos del Código de Minería.
+ *Base de datos vectorial*: diseño del esquema, generación de embeddings y almacenamiento en Milvus.
+ *Generación de respuestas*: consulta a los LLM bajo las tres estrategias de recuperación.
+ *Evaluación*: cálculo de métricas de similitud textual, semántica y evaluación por jueces LLM.
+ *Análisis estadístico*: aplicación de pruebas de normalidad, comparaciones no paramétricas (Kruskal-Wallis, Dunn), análisis factorial (Scheirer-Ray-Hare) y análisis de acuerdo inter-juez (Krippendorff's alpha).

== Selección y Extracción del Corpus

=== Características del Código de Minería Argentino

Se seleccionó el Código de Minería Argentino @codigo_mineria_1919 como corpus de prueba de concepto. Este cuerpo normativo presenta una estructura jerárquica definida (títulos, capítulos, secciones y artículos) que facilita la segmentación y vectorización. Además, su extensión es acotada (comparada con la totalidad de la legislación nacional), lo que permite iterar sobre el diseño del sistema sin incurrir en costos prohibitivos de procesamiento.

=== Obtención del Texto Legal

El texto del Código de Minería fue obtenido de la sección primera boletín oficial N°28.658 del día viernes 30 de mayo de 1997, descargado manualmente desde el sitio del Boletín Oficial de la República Argentina (#link("https://www.boletinoficial.gob.ar")[www.boletinoficial.gob.ar] #label("boletinoficial")) en formato PDF. Este documento constituye la fuente primaria del corpus.

Se exploraron dos estrategias adicionales de descarga desde el sistema Infoleg del Ministerio de Justicia de la Nación, que provee los textos legislativos en formato HTML:

+ *Docling*: librería especializada en descarga y conversión de documentos legales a formato Markdown.
+ *Requests + BeautifulSoup*: enfoque alternativo para descarga y parsing de HTML con extracción de metadatos estructurados (artículos individuales, fechas de sanción, anexos).

Ambas estrategias basadas en Infoleg resultaron en documentos incompletos o con errores de parsing, por lo que se descartaron en favor del procesamiento directo del PDF oficial. Ambos enfoques se implementaron como notebooks independientes, permitiendo contrastar y validar los resultados de extracción.

=== Extracción de Texto mediante Modelos de Visión

El texto del PDF fue extraído mediante un pipeline automatizado que convierte cada página del PDF a imagen y procesa las imágenes mediante el modelo de visión o4-mini de OpenAI. Este enfoque permite preservar la estructura jerárquica del documento legal (títulos, capítulos, artículos) y manejar documentos escaneados que carecen de una capa de texto digital.

El pipeline realiza las siguientes tareas:

+ Convierte cada página del PDF a formato PNG mediante la librería `pdf2image`.
+ Envía cada imagen al modelo o4-mini de OpenAI para extraer el texto estructurado.
+ Almacena los resultados en una base de datos SQLite para su posterior procesamiento y para evitar llamadas redundantes a la API.

Se desarrolló un módulo específico de parsing (`02_html_infoleg_parser`) que transforma el HTML original en texto estructurado, preservando los metadatos de cada artículo (número, título, capítulo, sección).

=== Validación de Calidad de Extracción

La calidad de la extracción se verificó mediante inspección manual de una muestra de artículos, comparando el texto extraído con el original en Infoleg. Se establecieron criterios de calidad basados en la completitud del texto, la preservación de la estructura jerárquica y la correcta identificación de los límites entre artículos.

=== Segmentación y Estructuración del Corpus

El Código de Minería fue segmentado en títulos individuales, y el texto completo fue dividido en 22 archivos Markdown correspondientes a cada título (Título I al Título XXII), más el apéndice y el título final. Esta segmentación por título constituye la base para la generación del benchmark de preguntas.

Posteriormente, para la indexación en la base de datos vectorial, el corpus fue dividido en unidades siguiendo su estructura jerárquica natural. Cada artículo se almacena como una unidad independiente, preservando metadatos como el título, capítulo y sección a los que pertenece, lo que permite tanto la recuperación granular como la contextualización de los fragmentos recuperados.

El corpus resultante está compuesto por un total de 482 partes distribuidas según su tipo en la @tabla-estadisticas-corpus.

#figure(
  three-line-table(
    columns: (auto, auto),
    [
      | *Tipo de parte* | *Cantidad* |
      | :-------------- | ---------: |
      | Títulos         |         22 |
      | Secciones       |          6 |
      | Acápites        |         55 |
      | Artículos       |        398 |
      | Apéndice        |          1 |
      | *Total*         |      *482* |
    ],
  ),
  caption: [Estadísticas del corpus del Código de Minería Argentino. Desglose por tipo de parte estructural.],
) <tabla-estadisticas-corpus>

El Código de Minería se organiza en 22 títulos que abarcan desde el dominio de las minas y su clasificación (Título I) hasta disposiciones sobre la caducidad de las concesiones (Título XXII). Los 399 artículos#footnote[362 en su cuerpo principal y 36 en su pie de apéndice.] constituyen las unidades normativas fundamentales, cada uno con contenido jurídico específico. Los 55 acápites agrupan artículos bajo subtemas dentro de cada título, mientras que las 6 secciones y el apéndice completan la estructura jerárquica del cuerpo legal. Esta organización jerárquica facilita la segmentación del corpus en fragmentos semánticamente coherentes para su indexación y recuperación en el sistema RAG.

== Base de Datos Vectorial

=== Selección de la Base de Datos Vectorial

Se seleccionó Milvus (versión 2.5.9) como base de datos vectorial por su capacidad de escalar a grandes volúmenes, soporte para múltiples tipos de índices y su disponibilidad como software de código abierto @wang2021milvus (véase el capítulo @cap:agentic-rag para los fundamentos de bases de datos vectoriales en sistemas RAG). La instancia se despliega mediante el script de instalación oficial de Milvus, que genera automáticamente la configuración de Docker Compose con los servicios de Milvus standalone y etcd como almacén de metadatos, lo que permite reproducir el entorno con un único comando.

=== Esquema de Datos

El esquema de la colección en Milvus contempla campos para:

+ Identificador único del fragmento.
+ Texto original del artículo o sección.
+ Metadatos estructurales (título, capítulo, sección, número de artículo).
+ Vector de embeddings (768 dimensiones).

La @tabla-esquema-milvus ilustra la estructura de la colección en Milvus.

#figure(
  three-line-table(
    columns: (auto, auto, auto),
    [
      | *Campo*                  | *Tipo*              |             *Descripción*              |
      | :----------------------- | :------------------ | :------------------------------------: |
      | `id`                     | `INT64`             |   Identificador único del fragmento    |
      | `contenido_texto`        | `STRING`            | Texto original del artículo o sección  |
      | `titulo`                 | `STRING`            |   Título del código al que pertenece   |
      | `capitulo`               | `STRING`            |       Capítulo dentro del título       |
      | `seccion`                | `STRING`            |      Sección dentro del capítulo       |
      | `numero_articulo`        | `INT64`             |          Número del artículo           |
      | `vector_contenido_texto` | `FLOAT_VECTOR[768]` | Embedding semántico de 768 dimensiones |
    ],
  ),
  caption: [Esquema de la colección en Milvus. Cada artículo se almacena con su texto, metadatos estructurales y vector de embeddings de 768 dimensiones.],
) <tabla-esquema-milvus>

=== Creación de Índices

Se creó un índice de tipo IVF_FLAT sobre el campo de embeddings, que ofrece un balance entre velocidad de búsqueda y precisión de los resultados. La métrica de distancia empleada fue la similitud coseno (COSINE), adecuada para comparar representaciones semánticas: al medir el coseno del ángulo entre dos vectores, es invariante a la magnitud de estos y captura su orientación relativa, propiedad que la torna la medida estándar para comparar embeddings de oraciones @reimers2019sentence @zhelezniak2019correlation.

=== Estrategia de Chunking

Se adoptó una estrategia de segmentación basada en la estructura natural del documento legal. Cada artículo constituye una unidad de chunking, lo que respeta los límites semánticos del texto jurídico y evita la fragmentación arbitraria que podría separar información contextualmente vinculada.

La @fig-esquema-milvus ilustra el proceso de generación de embeddings e inserción en la base de datos vectorial.

#figure(
  mermaid(
    "graph TD
    A[Documento legal] --> B[Segmentación por artículo]
    B --> C[SentenceTransformer]
    C --> D[Vector embedding 768d]
    D --> E[(Milvus)]
    F[Metadatos: título, capítulo, artículo] --> E",
  ),
  caption: [Diagrama del flujo de generación de embeddings e inserción en la base de datos vectorial Milvus.],
) <fig-esquema-milvus>

== Modelo de Embeddings

=== Criterios de Selección

La selección del modelo de embeddings se guió por cuatro criterios:

+ *Soporte para el idioma español*: el corpus y las consultas están íntegramente en español, con terminología del dominio jurídico. Un modelo entrenado específicamente en español evita la pérdida de matices que introduce la traducción implícita de los modelos multilingües de propósito general y evita depender de una etapa de traducción previa a la codificación.

+ *Desempeño en tareas de similitud semántica*: la recuperación se resuelve íntegramente por similitud entre la consulta y los artículos, de modo que la calidad del ranking depende directamente de la capacidad del modelo de ordenar pares de textos según su cercanía semántica. Los modelos de la familia _sentence-transformers_ entrenados para similitud textual ofrecen un desempeño sustancialmente superior al de los embeddings estáticos en esta tarea @reimers2019sentence.

+ *Dimensionalidad de los vectores resultantes*: una dimensionalidad moderada (768 dimensiones) mantiene el costo de almacenamiento y de búsqueda dentro de lo que permite una instancia de Milvus _standalone_, sin degradar la capacidad representativa. Dimensiones muy reducidas comprometen la separación entre artículos temáticamente próximos —riesgo relevante en un corpus con disposiciones que se repiten a lo largo de títulos distintos—, mientras que dimensiones muy altas encarecen la indexación sin beneficios proporcionales para un corpus de 482 partes.

+ *Disponibilidad como modelo de código abierto*: permite ejecutar la codificación en infraestructura propia (CPU), auditar el modelo, reproducir los experimentos y redistribuir el sistema, requisitos alineados con el carácter abierto del prototipo. Al no depender de una API externa, la generación de embeddings no introduce costo por token ni latencia de red, y el corpus completo permanece en la infraestructura local.

=== Modelo Seleccionado

Se seleccionó el modelo `hiiamsid/sentence_similarity_spanish_es` @hiiamsid2023sentence, un modelo de la familia sentence-transformers especializado en similitud semántica para textos en español @reimers2019sentence. Genera vectores de 768 dimensiones, ofreciendo un balance adecuado entre capacidad representativa y eficiencia computacional (véase el capítulo @cap:fundamentos-pln para los fundamentos de representaciones vectoriales y embeddings).

=== Generación e Inserción de Embeddings

Los embeddings se generaron procesando cada fragmento de texto mediante el modelo `SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')` cargado desde Hugging Face. La vectorización del corpus se realizó por lotes (batches) para optimizar el uso de memoria y CPU. Cada lote procesa un conjunto de artículos, genera los embeddings correspondientes y los prepara para la inserción en la base de datos.

Los vectores generados se insertaron en la colección de Milvus junto con sus metadatos textuales y estructurales. Se realizó una verificación post-inserción mediante consultas de prueba para confirmar la correcta indexación y recuperabilidad de los documentos. Los fragmentos sin contenido textual fueron representados con un vector nulo para mantener la consistencia del índice.

La generación de embeddings se realizó sobre una máquina con procesador x86_64 de 16 núcleos y 32 GB de RAM, ejecutando el modelo en CPU. El tiempo total de procesamiento para los 398 artículos del corpus fue del orden de minutos, dado el tamaño acotado del conjunto de datos.

== Sistema RAG Básico

El sistema RAG básico constituye una de las configuraciones de referencia del diseño experimental. A diferencia de la respuesta directa sin recuperación, incorpora una etapa de búsqueda vectorial para proveer contexto legal al modelo.

=== Módulo de Recuperación

El módulo de recuperación del RAG básico realiza una búsqueda vectorial por similitud coseno en Milvus, retornando los top-10 documentos más relevantes para cada consulta. Los documentos recuperados incluyen su texto completo y metadatos estructurales (título, capítulo, sección, número de artículo).

=== Módulo de Generación

Los fragmentos recuperados se inyectan en el prompt del sistema del LLM como contexto. El prompt instruye al modelo para responder basándose exclusivamente en la información proporcionada y citar los artículos relevantes. Se emplea la misma configuración de agente (Pydantic AI con temperatura 0) que en el baseline sin RAG, para mantener la comparabilidad.

=== Pipeline Completo

El pipeline completo del RAG básico sigue la secuencia: recepción de la pregunta → búsqueda vectorial → inyección de contexto en el prompt → generación de respuesta por el LLM. Se registran los metadatos completos de cada respuesta (tokens consumidos, costo, fragmentos recuperados, tiempos de ejecución).

== Sistema Agentic-RAG

=== Arquitectura General

El sistema Agentic-RAG implementa una arquitectura multi-agente compuesta por dos agentes especializados que coordinan las tareas de recuperación y generación de respuestas: el Agente Especialista Legal y el Agente de Recuperación. Durante el diseño se contempló un tercer agente —el Agente de Calidad de Recuperación— encargado de evaluar la pertinencia de los fragmentos recuperados, pero fue desactivado en la configuración experimental final debido a que su complejidad adicional no se tradujo en mejoras marginales significativas respecto al pipeline de dos agentes. Esta arquitectura se compara con dos configuraciones de referencia: respuesta directa sin recuperación (no RAG) y RAG básico con recuperación vectorial simple.

La @fig-arq-no-rag presenta el diagrama de secuencia de la configuración sin RAG.

#figure(
  image("../media/diag_no_rag.svg", width: 45%),
  caption: [Configuración _Sin RAG_: el modelo genera la respuesta directamente a partir de su conocimiento paramétrico, sin acceso a documentos externos.],
) <fig-arq-no-rag>

=== Framework de Orquestación (Pydantic AI)

La implementación de los agentes se realizó mediante el framework Pydantic AI @pydanticAI, cuya selección se fundamenta en los criterios presentados en el capítulo @cap:agentic-rag sobre frameworks de orquestación de agentes. Pydantic AI provee:

+ Definición declarativa de agentes con validación de tipos.
+ Gestión de herramientas (tools) con límites de invocación configurables.
+ Soporte para salidas estructuradas mediante modelos Pydantic.
+ Compatibilidad nativa con múltiples proveedores de LLM.
+ Ejecución asíncrona para optimizar las llamadas concurrentes a APIs.

Cada agente se define como una instancia con su propio prompt del sistema, conjunto de herramientas y restricciones de ejecución. Se habilitó la ejecución asíncrona para optimizar las llamadas concurrentes a las APIs de los modelos.

=== Agente Especialista Legal <sec:agente-especialista-legal>

El Agente Especialista Legal es el componente principal responsable de generar la respuesta final al usuario. Recibe la pregunta del usuario y, en la configuración Agentic-RAG, tiene acceso a herramientas que le permiten solicitar búsquedas al Agente de Recuperación. Su prompt del sistema está diseñado para orientar las respuestas hacia el dominio legal argentino:

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 10pt)
    _Eres un asistente legal experto en derecho Argentino. Respondes preguntas legales basadas en la Constitución Nacional Argentina, Códigos, Leyes y jurisprudencia. Analizas la pregunta del usuario, extraes los puntos importantes y utilizas la herramienta_ `retrieve_relevant_documents` _una vez para obtener información de la base de datos legislativa. Analizas los documentos para generar la respuesta final. Siempre citas las fuentes legales consultadas. Si no sabes la respuesta y los documentos legales no son suficientes para crear una respuesta, di que no cuentas con información para responderla. Las respuestas deben ser claras, concisas y directas al punto. Respondes en español al menos que el usuario solicite otro idioma._
  ],
)

El agente tiene límites configurables de invocaciones de herramientas para controlar costos y evitar ciclos infinitos.

La @fig-arq-base-rag presenta el diagrama de secuencia de la configuración RAG básico, donde la consulta se emplea directamente para recuperar fragmentos de la base vectorial.

#figure(
  image("../media/diag_base_rag.svg", width: 65%),
  caption: [Configuración _RAG Básico_: la consulta del usuario se emplea para recuperar los 10 fragmentos más similares de la base vectorial, que se inyectan como contexto en el prompt del modelo.],
) <fig-arq-base-rag>

=== Agente de Recuperación

El Agente de Recuperación se encarga de realizar búsquedas semánticas en la base de datos vectorial. Tiene la capacidad de descomponer consultas complejas en subconsultas más específicas, realizar múltiples búsquedas y consolidar los resultados. Retorna los fragmentos más relevantes junto con sus metadatos estructurales (artículo, capítulo, título). Su prompt del sistema es el siguiente:

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 10pt)
    _Eres un especialista en búsqueda de información legislativa que: recibes una consulta relacionada con cuestiones legales de derecho Argentino; la consulta puede dividirse en máximo 3 subconsultas para mejorar la recuperación; realizas una búsqueda por cada subconsulta en una base de datos de vectores empleando la herramienta_ `cosine_distance_vector_search` _como máximo 6 veces; seleccionas los documentos que mejor se ajustan a la consulta inicial y respondes con los resultados de la búsqueda._
  ],
)

Sus capacidades incluyen:

+ Descomposición de consultas complejas en subconsultas semánticamente más específicas.
+ Ejecución de múltiples búsquedas vectoriales en paralelo.
+ Consolidación y deduplicación de resultados.
+ Retorno de fragmentos con metadatos completos (artículo, capítulo, título, distancia de similitud).

La @fig-arq-agentic-rag presenta el diagrama de secuencia de la configuración Agentic-RAG, ilustrando la interacción entre ambos agentes.

#figure(
  image("../media/diag_agentic_rag.svg", width: 90%),
  caption: [Configuración _Agentic-RAG_: el Agente Especialista Legal delega la recuperación al Agente de Recuperación, que descompone la consulta en subconsultas y ejecuta múltiples búsquedas vectoriales (bucle). Los fragmentos recuperados se retornan directamente al Agente Especialista Legal para la generación de la respuesta.],
) <fig-arq-agentic-rag>

=== Agente de Calidad de Recuperación (Diseñado pero no Activado)

El Agente de Calidad de Recuperación fue diseñado para evaluar la pertinencia de los fragmentos recuperados antes de enviarlos al Agente Especialista Legal. Su función prevista era verificar que los documentos recuperados fueran relevantes para la consulta y solicitar búsquedas adicionales si la calidad de la recuperación inicial era insuficiente. Sin embargo, este agente fue desactivado en la configuración experimental final por dos motivos principales: (1) agregaba complejidad significativa en la gestión de llamadas a APIs, incrementando los costos operativos al requerir una capa adicional de invocación al LLM; y (2) requería la selección de un modelo adicional, introduciendo otra variable de configuración. En su lugar, se optó por actualizar los prompts del Agente Especialista Legal para que este pudiera solicitar búsquedas adicionales al Agente de Recuperación en caso de considerar que la información recuperada inicialmente era insuficiente, logrando un equilibrio entre calidad de recuperación y eficiencia. Su prompt del sistema era el siguiente:

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 10pt)
    _Eres un especialista en "retrieval augmented generation" encargado de evaluar la calidad de la recuperación. Comparas la consulta original con la información recuperada y decides si la información es suficiente para responder la consulta. Provees feedback conciso para mejorar la consulta._
  ],
)

En el código de orquestación, su herramienta (`evaluate_retrieval`) y su prompt del sistema fueron comentados, por lo que no participó en la generación de los resultados reportados.

=== Orquestación y Flujo de Comunicación

La orquestación se implementó como un flujo secuencial donde el Agente Especialista Legal invoca herramientas que internamente disparan la ejecución del Agente de Recuperación. Pydantic AI gestiona automáticamente el ciclo de herramientas (tool call → resultado → siguiente invocación) hasta que el agente principal produce la respuesta final o se alcanza el límite de herramientas. El flujo de comunicación sigue la siguiente secuencia:

+ El usuario formula una pregunta.
+ El Agente Especialista Legal recibe la consulta e invoca al Agente de Recuperación.
+ El Agente de Recuperación ejecuta búsquedas vectoriales, potencialmente descomponiendo la consulta en subconsultas.
+ Los fragmentos recuperados se retornan al Agente Especialista Legal.
+ El Agente Especialista Legal genera la respuesta final integrando el contexto recuperado.

Para las configuraciones sin RAG y RAG básico, se empleó un prompt simplificado que instruye al modelo como asistente legal experto en derecho argentino, con indicación de citar fuentes legales y responder de manera concisa. En la configuración RAG básico, el prompt incluye además una sección con los fragmentos recuperados de la base de datos vectorial inyectados como contexto.

=== Logging y Trazabilidad

Se implementó un sistema de logging que registra la conversación completa entre agentes, incluyendo:

+ Todas las invocaciones de herramientas con sus parámetros y resultados.
+ Los fragmentos recuperados en cada iteración de búsqueda.
+ Los metadatos de tokens consumidos y costos asociados a cada llamada a la API.

Los logs se almacenan en formato JSON (JavaScript Object Notation) para facilitar el análisis posterior del comportamiento del sistema. Nota: las decisiones del Agente de Calidad no aparecen en los logs de la configuración experimental final, dado que este agente fue desactivado.

=== Definición de Agentes y Herramientas

A continuación se presentan fragmentos representativos de la implementación de cada agente, incluyendo su instanciación, herramientas y mecanismos de control de ejecución. El código fuente completo se encuentra en el directorio `codigo_experimentos/part_g/`, y los logs detallados de cada interacción se almacenan en `codigo_experimentos/part_g/chat_data/`.

==== Agente Especialista Legal

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 9pt, font: "DejaVu Sans Mono")
    ```python
    law_specialist_agent = Agent(
        model=law_specialist_agent_model,
        instructions=INSTRUCTIONS["law_specialist_agent"],
        prepare_tools=cap_document_retrieval_tool_calls,
        tools=[retrieve_relevant_documents],
        model_settings=ModelSettings(temperature=0.0),
    )
    ```
  ],
)

El prompt del sistema (`INSTRUCTIONS["law_specialist_agent"]`) fue presentado en la sección @sec:agente-especialista-legal. La herramienta `retrieve_relevant_documents` actúa como fachada que internamente invoca al Agente de Recuperación:

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 9pt, font: "DejaVu Sans Mono")
    ```python
    def retrieve_relevant_documents(question: str) -> dict:
        """Recupera documentos para responder la pregunta."""
        retrieval_deps = RetrievalDependencies(
            vector_db_client=get_db_client(),
        )
        result = retrieval_agent.run_sync(
            f"Please retrieve documents for: {question}",
            usage_limits=VECTOR_SEARCH_LIMIT,
            deps=retrieval_deps,
        )
        return result.output
    ```
  ],
)

El límite de una única invocación se impone mediante la función `cap_document_retrieval_tool_calls`, que deshabilita todas las herramientas después de la primera llamada.

==== Agente de Recuperación

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 9pt, font: "DejaVu Sans Mono")
    ```python
    retrieval_agent = Agent(
        model=retrieval_agent_model,
        instructions=INSTRUCTIONS["retrieval_agent"],
        prepare_tools=cap_total_tool_calls,
        tools=[cosine_distance_vector_search],
        model_settings=ModelSettings(temperature=0.0),
        deps_type=RetrievalDependencies,
    )
    ```
  ],
)

La herramienta `cosine_distance_vector_search` ejecuta la búsqueda por similitud coseno contra Milvus:

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 9pt, font: "DejaVu Sans Mono")
    ```python
    def cosine_distance_vector_search(
        ctx: RunContext[RetrievalDependencies], query: str
    ) -> dict:
        """Busca documentos en la base vectorial
        por similitud coseno."""
        result = get_document_matches(
            ctx.deps.vector_db_client, query,
            max_documents=5
        )
        return {
            "usage_counts": vector_search_counter,
            "search_result": result
        }
    ```
  ],
)

La función `get_document_matches` codifica la consulta mediante `SentenceTransformer`, ejecuta `client.search()` sobre la colección con métrica `COSINE` y retorna los cinco documentos con mayor similitud junto con sus metadatos estructurales.

El límite global de 6 invocaciones se implementa mediante `cap_total_tool_calls`, que contabiliza todas las llamadas a herramientas en la sesión y deshabilita las herramientas al alcanzar el umbral. Esto permite que el agente descomponga la consulta en hasta 3 subconsultas con hasta 2 búsquedas cada una, o realice hasta 6 búsquedas con una única formulación.

Cabe precisar que el límite de seis búsquedas no depende únicamente de la indicación del prompt: está impuesto en el código de orquestación, en dos capas complementarias. En primer lugar, la ejecución del Agente de Recuperación se invoca con `usage_limits=VECTOR_SEARCH_LIMIT`, una instancia de `UsageLimits(tool_calls_limit=6)` que interrumpe la ejecución al alcanzar el tope de llamadas. En segundo lugar, `cap_total_tool_calls` actúa como función `prepare_tools` del agente: cuando contabiliza seis llamadas previas (`TOTAL_TOOL_CALL_LIMIT = 6`), devuelve una lista vacía de herramientas, de modo que el agente ya no dispone de ninguna herramienta para invocar. El mismo mecanismo acota la actuación del Agente Especialista Legal, cuyo límite es `DOCUMENT_RETRIEVAL_LIMIT = 1`.

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 9pt, font: "DejaVu Sans Mono")
    ```python
    TOTAL_TOOL_CALL_LIMIT = 6          # Agente de Recuperación
    DOCUMENT_RETRIEVAL_LIMIT = 1       # Agente Especialista Legal
    VECTOR_SEARCH_LIMIT = UsageLimits(tool_calls_limit=6)
    ```
  ],
)

Los dos mecanismos son redundantes de forma deliberada: el límite declarado en `UsageLimits` interrumpe la ejecución aun si el modelo intentara continuar, mientras que `cap_total_tool_calls` retira las herramientas antes de que el modelo pueda solicitarlas, lo que además evita llamadas fallidas y consumo innecesario de tokens.

=== Ejemplo de Interacción entre Agentes

Para ilustrar el flujo completo de comunicación, se presenta a continuación un ejemplo concreto extraído de los logs de ejecución correspondientes a la pregunta 1.1 del benchmark (modelo gpt-5-mini como Agente Especialista Legal, gpt-5 como Agente de Recuperación). Los logs completos de todas las interacciones se encuentran en `codigo_experimentos/part_g/chat_data/`.

*Pregunta del usuario*: "El ingeniero Juan Pérez ha descubierto un importante yacimiento de litio en una finca privada ubicada en territorio de la Provincia de Salta. El propietario de la finca, la Sra. Marta Gómez, sostiene que, por ser dueña del suelo, es también dueña exclusiva del litio allí existente y que nadie puede explotarlo sin su consentimiento. Juan Pérez pretende solicitar la concesión minera ante la autoridad competente y argumenta que el litio es de dominio estatal y que la propiedad del suelo es accesoria respecto de la mina."

*Paso 1 — Invocación del Agente de Recuperación*: El Agente Especialista Legal recibe la pregunta y estructura una consulta para la herramienta `retrieve_relevant_documents` con los términos clave: "Código de Minería Argentino dominio de los minerales litio propiedad del suelo acceso a minas categoría del litio normas aplicables explotación concesión minera artículos pertinentes régimen entre Estado y propietarios privados".

*Paso 2 — Descomposición en subconsultas*: El Agente de Recuperación recibe la consulta y la descompone en tres subconsultas más específicas: (a) clasificación del litio y sustancias mineras, (b) dominio originario de las minas y relación con la propiedad del suelo, y (c) régimen de concesiones y adquisición de minas. Para cada subconsulta, invoca `cosine_distance_vector_search`.

*Paso 3 — Búsqueda vectorial*: Cada subconsulta se codifica mediante el modelo de embeddings y se ejecuta una búsqueda por similitud coseno en Milvus, retornando los 5 documentos más similares por subconsulta. Los artículos recuperados incluyen: Art. 3 (clasificación del litio en primera categoría), Art. 7 (dominio originario del Estado), Art. 8 (facultad de buscar minas), Art. 10 (concesión legal), Art. 11 (propiedad distinta del terreno), Art. 44 (adquisición por concesión) y Art. 351 (multiplicador de pertenencias para litio).

*Paso 4 — Consolidación y respuesta*: El Agente de Recuperación selecciona los 10 documentos más pertinentes y los retorna al Agente Especialista Legal. Este integra el contexto recuperado y genera la respuesta final, citando los artículos 3, 7, 8, 10, 11, 44 y 351 del Código de Minería, y concluyendo que el dominio del litio corresponde a la Provincia de Salta, que el propietario del suelo no tiene derecho exclusivo sobre el mineral, y que Juan Pérez puede solicitar la concesión minera ante la autoridad competente.

Este ejemplo ilustra el flujo completo de delegación, descomposición de consultas, búsqueda vectorial múltiple e integración de contexto que caracteriza a la configuración Agentic-RAG. Los logs JSON de cada paso —incluyendo tokens consumidos, costo, documentos recuperados y sus distancias de similitud— están disponibles para su inspección en el directorio `codigo_experimentos/part_g/chat_data/`.

=== Hiperparámetros de Configuración

La temperatura controla la aleatoriedad de las respuestas del modelo (0,0 = determinista). El límite de llamadas a herramientas restringe cuántas veces cada agente puede invocar sus herramientas. La herramienta disponible especifica la función que cada agente puede ejecutar. El máximo de subconsultas indica cuántas preguntas derivadas puede generar el Agente de Recuperación a partir de una consulta original. El modelo por defecto define el LLM asignado a cada agente.

La @tabla-hiperparametros-agentes presenta los hiperparámetros de configuración de los agentes activos en la configuración Agentic-RAG experimental.

#figure(
  three-line-table(
    columns: (5cm, auto, auto),
    [
      | *Parámetro*                       |           *Agente Especialista Legal*            |              *Agente de Recuperación*              |
      | :-------------------------------- | :----------------------------------------------: | :------------------------------------------------: |
      | Temperatura                       |                       0,0                        |                        0,0                         |
      | Límite de llamadas a herramientas |                        1                         |                         6                          |
      | Herramienta disponible            | #text(size: 10pt)[`retrieve_relevant_documents`] | #text(size: 10pt)[`cosine_distance_vector_search`] |
      | Máx. subconsultas por consulta    |                        —                         |                         3                          |
      | Modelo por defecto                |                Variable#super[†]                 |                       gpt-5                        |
    ],
  ),
  caption: [Hiperparámetros de configuración de los agentes activos del sistema Agentic-RAG. #super[†]El modelo del Agente Especialista Legal varía según la configuración experimental (gpt-5-nano, gpt-5-mini o gpt-5).],
) <tabla-hiperparametros-agentes>

El límite total de llamadas a herramientas del sistema está fijado en 6 invocaciones, lo que permite al Agente de Recuperación descomponer la consulta en hasta 3 subconsultas y realizar hasta 2 búsquedas por subconsulta, o realizar hasta 6 búsquedas con una única formulación.

En la generación de respuestas no se configuró el parámetro `reasoning_effort`. La versión 1.1.0 de Pydantic AI no define un valor por defecto y envía `NOT_GIVEN`; OpenAI documenta `medium` como valor por defecto para GPT-5. El valor efectivo no quedó registrado y no se infiere de los tokens de razonamiento.

En cuanto al registro de costos, la ejecución del Agente de Recuperación se contabiliza de forma independiente de la del Agente Especialista Legal: los metadatos de cada respuesta de la configuración Agentic-RAG incluyen los campos `retrieval_input_tokens`, `retrieval_output_tokens` y `retrieval_total_price`, que registran el consumo del modelo de recuperación (`gpt-5`). El costo informado para cada consulta con Agentic-RAG es, por lo tanto, la suma del costo del Agente Especialista Legal (`total_price`, con el modelo que corresponda a la configuración) y del costo del Agente de Recuperación (`retrieval_total_price`); los 79 registros de la estrategia agéntica incluyen este segundo componente, mientras que las estrategias sin RAG y RAG básico no registran costo de recuperación por tokens (en el RAG básico la búsqueda vectorial se ejecuta localmente sobre Milvus y no consume tokens de API). Dado que el Agente de Recuperación emplea siempre `gpt-5`, este componente domina el costo de la estrategia agéntica, en particular cuando el Agente Especialista Legal es un modelo pequeño: en el ejemplo del anexo @anexo-ejemplos, el Agente de Recuperación representó USD 0,05037 frente a USD 0,00285 del Agente Especialista Legal.

== Selección de Modelos LLM

=== Criterios de Selección

La selección de los modelos de lenguaje consideró:

+ Disponibilidad mediante API pública.
+ Costo por token de entrada y salida.
+ Desempeño en benchmarks generales de lenguaje.
+ Capacidad de seguir instrucciones complejas (instruction following).
+ Soporte para generación con temperatura cero (respuestas determinísticas).

=== Modelos Evaluados

Se evaluaron tres modelos de la familia GPT-5 de OpenAI, lo que permite analizar el efecto del tamaño del modelo manteniendo constante la arquitectura:

+ *gpt-5-nano*: modelo de menor tamaño y costo, orientado a tareas simples.
+ *gpt-5-mini*: modelo intermedio que balancea capacidad y costo.
+ *gpt-5*: modelo de mayor capacidad, referencia de desempeño superior.

Todos los modelos fueron configurados con temperatura 0 para maximizar la reproducibilidad de las respuestas.

=== Costos por Token

La @tabla-costos-modelos presenta los costos por token de los tres modelos empleados, según la tarificación vigente de OpenAI al momento de la experimentación (agosto-noviembre 2025).

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto),
    [
      | *Modelo*   | *Entrada (USD/Mtok)* | *Salida (USD/Mtok)* | *Ratio vs. nano* |
      | :--------- | -------------------: | ------------------: | ---------------: |
      | gpt-5-nano |               \$0,05 |              \$0,40 |               1× |
      | gpt-5-mini |               \$0,25 |              \$2,00 |               5× |
      | gpt-5      |               \$1,25 |             \$10,00 |              25× |
    ],
  ),
  caption: [Costos por millón de tokens (Mtok) de los modelos GPT-5 empleados. El ratio indica el factor de costo relativo al modelo más económico (gpt-5-nano).],
) <tabla-costos-modelos>

La diferencia de costos entre modelos es significativa: gpt-5 es 25 veces más costoso que gpt-5-nano por token de entrada y salida. Esta variación permite analizar la relación costo-beneficio de cada configuración en el capítulo de evaluación. Cabe señalar que en la configuración Agentic-RAG, el Agente de Recuperación emplea gpt-5 independientemente del modelo del Agente Especialista Legal, lo que incrementa el costo base de esta estrategia.

== Diseño del Benchmark

=== Generación de Preguntas

Las preguntas del benchmark fueron generadas empleando GPT-4.1, a partir de cada título del Código de Minería. El proceso consistió en:

+ Segmentación del Código de Minería en títulos individuales (Título I, II, etc.).
+ Generación automatizada de preguntas tipo caso de estudio legal con respuestas esperadas para cada título.
+ Compilación de las preguntas en un documento unificado para revisión.

=== Estructura del Benchmark

El benchmark contiene 25 preguntas distribuidas entre los títulos del Código de Minería, que a su vez se descomponen en 79 subpreguntas que constituyen las unidades de evaluación independientes. Cada pregunta incluye:

+ Texto de la pregunta (formulada como caso de estudio legal).
+ Contexto relevante (artículos y secciones de referencia).
+ Respuesta esperada elaborada por el LLM generador.
+ Identificadores de los artículos fuente.

Las preguntas se normalizaron a un formato unificado donde cada subpregunta constituye una unidad de evaluación independiente, con su respectivo texto, contexto y respuesta esperada.

=== Colaboración con Profesionales del Derecho

Las preguntas generadas y sus respuestas esperadas fueron revisadas por un profesional del derecho con experiencia en legislación minera argentina, con el objetivo de validar la pertinencia, corrección y completitud de las respuestas de referencia. El proceso de validación se estructuró en las siguientes etapas:

+ *Revisión inicial*: el profesional examinó la totalidad de las preguntas generadas por GPT-4.1, verificando que los escenarios planteados fueran jurídicamente plausibles y que las subpreguntas abordaran aspectos relevantes de la normativa.

+ *Verificación de respuestas esperadas*: se contrastaron las respuestas de referencia con el texto vigente del Código de Minería, evaluando tres criterios: (a) correcta identificación de los artículos aplicables, (b) interpretación adecuada de las disposiciones normativas, y (c) coherencia entre la fundamentación y la conclusión jurídica.

+ *Ajustes y correcciones*: se realizaron correcciones en los casos donde la respuesta generada contenía imprecisiones en la citación de artículos, omisiones de disposiciones relevantes o interpretaciones ambiguas.

+ *Validación final*: las respuestas corregidas fueron revisadas por segunda vez para confirmar la consistencia del benchmark completo. Se verificó que las respuestas esperadas fueran autosuficientes y que los artículos de referencia citados correspondieran efectivamente a las disposiciones invocadas.

== Métricas y Sistema de Evaluación

La evaluación del sistema emplea tres familias de métricas complementarias que capturan diferentes aspectos de la calidad de las respuestas.

=== Métricas de Similitud Textual

Se implementaron métricas de solapamiento léxico y a nivel de n-gramas mediante un módulo reutilizable (`03_compare_texts.py`) que calcula más de 11 métricas de similitud textual entre la respuesta generada y la respuesta esperada:

+ *Token F1*: media armónica de precisión y recall a nivel de tokens @chinchor1992evaluating.
+ *Similitud de Jaccard*: proporción de tokens compartidos respecto al total de tokens únicos @jaccard1901distribution.
+ *Similitud de Levenshtein*: complemento normalizado de la distancia de edición @levenshtein1966binary.
+ *BLEU* (1-4): precisión de n-gramas con penalización por brevedad @papineni2002bleu.
+ *ROUGE* (1, 2, L): recall de n-gramas y subsecuencia común más larga @lin2004rouge.
+ *Tasa de error de caracteres (CER)*: proporción de operaciones de edición a nivel de caracteres.
+ *Exact Match*: coincidencia exacta entre respuestas.
+ *Ratios de longitud y conteo de palabras*: métricas complementarias de formato.

=== Métricas Semánticas

Se emplearon métricas basadas en modelos de lenguaje preentrenados:

+ *SBERT Similarity (Spanish)*: similitud coseno entre embeddings generados por un modelo sentence-transformers optimizado para español @reimers2019sentence.
+ *SBERT Similarity (Multilingual)*: variante multilingüe del mismo enfoque @reimers2020multilingual.
+ *BERTScore*: similitud contextualizada basada en alineamiento de tokens mediante embeddings BERT, reportando precisión, recall y F1 @zhang2019bertscore.

=== Evaluación LLM-as-a-Judge

Complementariamente a las métricas automatizadas, se implementó un esquema de evaluación LLM-as-a-Judge (véase el capítulo @cap:agentic-rag, sección @sec:llm-as-a-judge para los fundamentos teóricos de esta técnica de evaluación) empleando la librería `pydantic_evals`, que permite definir rúbricas estructuradas y ejecutar evaluaciones de forma automatizada. Se definieron dos rúbricas de evaluación:

+ *Respuesta correcta* (`score_respuesta_correcta`): evalúa el grado de alineamiento de la respuesta con la respuesta esperada, en una escala de 0.0 a 1.0 con valores discretos {0.0, 0.25, 0.5, 0.75, 1.0}.
+ *Precisión legal* (`score_precision_legal`): evalúa la correcta citación de artículos del Código de Minería argentino, en la misma escala.

Se emplearon tres modelos como jueces, seleccionados para diversificar las arquitecturas y proveedores, lo que permite evaluar la confiabilidad de las evaluaciones mediante métricas de acuerdo inter-juez:

+ *DeepSeek-V3* (`openrouter:deepseek/deepseek-chat-v3.1`): modelo de mezcla de expertos (MoE) con 671B parámetros totales y 37B activados por token @deepseek2024v3. No posee un modo de razonamiento nativo, pero puede seguir instrucciones de cadena de pensamiento mediante prompting estándar.
+ *Grok 4.1 Fast* (`openrouter:x-ai/grok-4.1-fast:free`): modelo con modo de razonamiento nativo que puede activarse mediante el parámetro `reasoning: enabled`, generando cadenas de pensamiento detalladas antes de producir la respuesta final @xai2025grok.
+ *Kimi K2 0905* (`openrouter:moonshotai/kimi-k2-0905`): modelo de mezcla de expertos con 1T parámetros totales y 32B activados, optimizado para uso agentivo @kimi2025k2. Es un modelo _reflex-grade_ sin modo de razonamiento nativo, aunque puede seguir instrucciones de cadena de pensamiento mediante prompting.

Los tres modelos fueron configurados con temperatura 0,0 y un límite de 5.000 tokens de salida. Los prompts de evaluación se construyeron a partir de las rúbricas definidas, solicitando al juez que asigne un puntaje y proporcione una justificación textual de la calificación mediante el parámetro `include_reason=True`. Cabe señalar que los prompts no incluyeron instrucciones explícitas de razonamiento paso a paso (cadena de pensamiento), lo que constituye una limitación discutida en @sec:limitaciones. Los resultados se almacenan como reportes JSON con scores y justificaciones por caso.

La @tabla-rubrica-correcta y la @tabla-rubrica-legal presentan los criterios detallados de cada rúbrica.

#figure(
  three-line-table(
    columns: (auto, auto),
    [
      | *Puntaje* | *Criterio*                                                                                    |
      | :-------: | :-------------------------------------------------------------------------------------------- |
      |   0,00    | La respuesta está en blanco o no coincide en absoluto con la respuesta esperada.              |
      |   0,25    | La respuesta tiene poca relación con la respuesta esperada y contiene errores significativos. |
      |   0,50    | La respuesta es parcialmente correcta, pero omite información clave o tiene errores menores.  |
      |   0,75    | La respuesta es mayormente correcta, con solo errores menores.                                |
      |   1,00    | La respuesta es completamente correcta y precisa.                                             |
    ],
  ),
  caption: [Rúbrica de evaluación `respuesta_correcta`: "La respuesta provista está alineada con la respuesta esperada."  Evaluada en español.],
) <tabla-rubrica-correcta>

#figure(
  three-line-table(
    columns: (auto, auto),
    [
      | *Puntaje* | *Criterio*                                                                              |
      | :-------: | :-------------------------------------------------------------------------------------- |
      |   0,00    | No cita ningún artículo relevante o cita artículos incorrectos.                         |
      |   0,25    | Cita algunos artículos relevantes, pero omite otros importantes.                        |
      |   0,50    | Cita la mayoría de los artículos relevantes y otros irrelevantes.                       |
      |   0,75    | Cita casi todos los artículos relevantes con precisión y pocos irrelevantes.            |
      |   1,00    | Cita todos los artículos relevantes y ninguno irrelevante de manera precisa y completa. |
    ],
  ),
  caption: [Rúbrica de evaluación `precision_legal`: "La respuesta cita correctamente los artículos relevantes del Código de Minería Argentino." Evaluada en español.],
) <tabla-rubrica-legal>

== Gestión de Costos y Tokens

=== Tracking de Uso

Cada llamada a la API de los proveedores de LLM registra los tokens de entrada y salida consumidos, así como el costo asociado. Esta información se almacena en los metadatos de cada respuesta y se consolida en un archivo CSV (`metadata_tokens_cost_cleaned.csv`) para el análisis agregado.

=== Optimización de Llamadas

Se implementaron las siguientes estrategias para optimizar el uso de la API y controlar costos:

+ Temperatura 0 para respuestas determinísticas (evita múltiples ejecuciones).
+ Límites de invocaciones de herramientas en los agentes.
+ Procesamiento secuencial con almacenamiento incremental de resultados para permitir la reanudación ante fallos.
+ Almacenamiento en caché de respuestas intermedias (embeddings, búsquedas vectoriales).

== Herramientas y Tecnologías

=== Lenguajes y Frameworks

+ *Python*: lenguaje principal de desarrollo @python2023.
+ *Pydantic AI*: framework para la implementación de agentes con validación de tipos @pydanticAI.
+ *pydantic_evals*: librería para evaluación LLM-as-a-Judge con rúbricas estructuradas @pydanticAI.
+ *Polars*: librería de procesamiento de datos tabulares de alto rendimiento @polars2024.
+ *sentence-transformers*: generación de embeddings semánticos @reimers2019sentence.
+ *scipy*: análisis estadístico @virtanen2020scipy.
+ *matplotlib*: visualización de resultados @hunter2007matplotlib.

Las versiones exactas de todas las librerías empleadas, incluyendo dependencias transitivas, pueden consultarse en el archivo `codigo_experimentos/uv.lock`, que registra el estado completo del entorno Python gestionado mediante uv.

=== Infraestructura

La infraestructura empleada combina un equipo local —donde se ejecutan íntegramente los notebooks de experimentación, el modelo de embeddings y la base de datos vectorial— con servicios externos accedidos por API para la generación de respuestas y la evaluación por jueces. Los componentes son los siguientes:

+ *Equipo local*: estación de trabajo con procesador x86_64 de 16 núcleos y 32 GB de RAM, sin GPU. Aloja los notebooks de experimentación (Python con `uv`), el modelo de embeddings —que se ejecuta en CPU— y la base de datos vectorial.
+ *Milvus*: base de datos vectorial desplegada mediante Docker Compose, junto con etcd como almacén de metadatos.
+ *OpenAI API*: acceso a los modelos GPT-5 (nano, mini, estándar), GPT-4.1 para generación de preguntas y o4-mini para extracción de contenido de archivos PDF.
+ *APIs de terceros*: DeepSeek, Grok y Kimi K2 como modelos jueces.

=== Análisis Estadístico

El análisis estadístico de los resultados se estructuró en varias etapas, cada una con un propósito específico y respaldada por métodos estadísticos establecidos en la literatura.

==== Verificación de Normalidad (Shapiro-Wilk)

Previo a la selección de pruebas de hipótesis, se verificó la normalidad de las distribuciones de las métricas mediante el test de Shapiro-Wilk @shapiro1965analysis. Este test evalúa la hipótesis nula de que la muestra proviene de una distribución normal. Si el valor p es inferior a 0,05, se rechaza la hipótesis de normalidad, lo que determina la necesidad de emplear métodos no paramétricos para los análisis subsiguientes.

==== Comparaciones No Paramétricas (Kruskal-Wallis y Dunn)

Para comparar las métricas entre los tres sistemas de recuperación (no RAG, RAG básico y Agentic-RAG) y entre los tres modelos (gpt-5-nano, gpt-5-mini, gpt-5), se empleó el test de Kruskal-Wallis @kruskal1952use, una alternativa no paramétrica al ANOVA de un factor que no requiere el supuesto de normalidad. Este test evalúa si al menos uno de los grupos difiere significativamente de los demás.

Ante resultados significativos en Kruskal-Wallis, se aplicó el test post-hoc de Dunn @dunn1964multiple con corrección de Bonferroni @bonferroni2010teoria para identificar qué pares de grupos presentan diferencias significativas, controlando la tasa de error familiar (family-wise error rate).

Para los análisis con más de cinco comparaciones —en particular, los efectos simples de estrategia dentro de cada modelo (9 comparaciones)— se aplicó adicionalmente la corrección de Holm-Bonferroni @holm1979simple, un procedimiento step-down secuencialmente rejectivo que ofrece mayor potencia estadística que Bonferroni manteniendo el control de la tasa de error familiar. El método de Holm ordena los p-values de menor a mayor y compara cada uno contra un umbral decreciente $alpha/(m - k + 1)$, donde $m$ es el número total de comparaciones y $k$ la posición en el ordenamiento. Ambas correcciones se implementaron mediante la función `multipletests` de la librería statsmodels @seabold2010statsmodels.

==== Análisis de Interacción Factorial (Scheirer-Ray-Hare)

Para evaluar la interacción entre los factores "sistema de recuperación" y "modelo" sobre las métricas de calidad, se empleó el test de Scheirer-Ray-Hare @scheirer1976analysis. Este test constituye la alternativa no paramétrica al ANOVA de dos factores y se basa en aplicar ANOVA sobre los rangos de los datos. Permite evaluar los efectos principales de cada factor y su interacción, siendo particularmente útil cuando no se cumplen los supuestos de normalidad y homocedasticidad del ANOVA paramétrico.

Como análisis de robustez se ajustó un modelo ordinal acumulativo con enlace logit, efectos fijos de estrategia, modelo del especialista y juez, y efectos aleatorios por caso y por unidad: `score_respuesta_correcta ~ estrategia * modelo_especialista + juez + (1 | caso) + (1 | unidad)`. Se utilizó `ordinal::clmm` con `nAGQ = 1`, es decir, la aproximación de Laplace. No se realizó una prueba formal del supuesto de odds proporcionales; los resultados de este modelo se interpretan como un análisis de sensibilidad y no como una estimación exacta de los efectos. Las cifras reconciliadas se documentan en `verificacion-analisis-estadistico/reconciliacion_v1/`.

==== Análisis de Acuerdo Inter-Juez (Krippendorff's Alpha)

Para evaluar la confiabilidad de las evaluaciones LLM-as-a-Judge, se calculó el coeficiente alpha de Krippendorff @krippendorff2019content @hayes2007answering entre los tres modelos jueces (DeepSeek-V3, Grok 4.1 Fast y Kimi K2 0905). Este coeficiente mide el acuerdo entre múltiples codificadores (en este caso, modelos LLM actuando como jueces) corrigiendo el acuerdo esperado por azar, y es aplicable a cualquier escala de medición (nominal, ordinal, intervalo o razón). Se complementó con el análisis de correlación de Spearman @spearman1904proof entre pares de jueces para identificar posibles sesgos sistemáticos.

== Desafíos Técnicos y Soluciones

=== Manejo de Errores y Reintentos

Se implementó un sistema de manejo de errores que registra las respuestas fallidas y permite su reprocesamiento selectivo. Los errores más frecuentes fueron timeouts de la API y límites de tasa (rate limits), que se gestionaron mediante reintentos con backoff exponencial.

En la etapa de evaluación LLM-as-a-Judge se detectaron, además, errores sistemáticos de formato en las salidas de los jueces: en algunos casos la respuesta del modelo juez no constituía un JSON válido —texto explicativo antes o después del objeto JSON, comillas sin escapar o bloques truncados—, lo que impedía el parseo del reporte de evaluación y dejaba el caso sin puntaje. Estos errores se concentraron en un único modelo juez, Grok 4.1 Fast, y fueron corregidos de forma manual: se revisó el reporte de cada caso afectado, se recuperó del texto devuelto por el juez el puntaje y la justificación correspondientes, y el registro corregido se incorporó al conjunto de resultados consolidado. Dado que la incidencia fue acotada y estuvo concentrada en un solo juez, no se instrumentó un reintento automático ni una reparación programática de las salidas malformadas. La consecuencia metodológica de esta decisión se discute en @sec:limitaciones.

=== Optimización de Rendimiento

Se empleó ejecución asíncrona para las llamadas a APIs externas, lo que permite solapar tiempos de espera. La generación de embeddings se paralelizó por lotes y los resultados intermedios se persistieron en disco para evitar pérdida de progreso ante interrupciones.

== Repositorio y Documentación

=== Estructura del Repositorio

El código se organizó en directorios temáticos que siguen el flujo del pipeline:

+ `notebooks/`: exploración y pruebas de tecnologías.
+ `part_a/`: generación de preguntas del benchmark.
+ `part_b/`: base de datos de preguntas del benchmark (enfoque cancelado; se optó por archivos JSON en su lugar).
+ `part_c/`: creación de la base de datos vectorial.
+ `part_d/`: pruebas de recuperación baseline.
+ `part_e/`: respuestas sin RAG y cálculo de métricas.
+ `part_f/`: respuestas con RAG básico.
+ `part_g/`: respuestas con Agentic-RAG.
+ `part_h/`: integración de datos.
+ `part_h_1/`: evaluación LLM-as-a-Judge.
+ `part_i/`: preparación de datos para análisis.
+ `part_j/`: análisis estadístico.

Los logs de interacción entre agentes correspondientes a la configuración Agentic-RAG se almacenan en `part_g/chat_data/`, organizados por modelo del Agente Especialista Legal y por número de pregunta. Cada sesión contiene archivos JSON independientes para el Agente Especialista Legal (`law_specialist_agent.json`) y el Agente de Recuperación (`retrieval_agent.json`), junto con el historial de búsquedas vectoriales (`retrieval_history/`). Los logs de las configuraciones sin RAG y RAG básico se encuentran en `part_e/` y `part_f/` respectivamente.

=== Documentación Técnica

Cada directorio contiene un archivo README con instrucciones de ejecución. Se mantiene un archivo de resumen de tareas (`performed_tasks_summary.md`) que documenta el propósito y resultado de cada notebook del proyecto.

== Conclusiones del Capítulo

Este capítulo presentó el diseño metodológico y la implementación del sistema Agentic-RAG, abarcando todo el pipeline desde la extracción de datos del Código de Minería hasta el análisis estadístico de los resultados. Se detallaron las decisiones de diseño fundamentales sobre la selección del corpus, la arquitectura multi-agente, la estrategia de evaluación y las herramientas empleadas, así como los detalles técnicos de implementación incluyendo la configuración de la base de datos vectorial, la orquestación de agentes mediante Pydantic AI y el sistema de logging y trazabilidad.

El diseño factorial de 3 estrategias × 3 modelos permite un análisis riguroso de los efectos de cada factor y su interacción, mientras que la combinación de métricas textuales, semánticas y evaluación por jueces LLM proporciona una visión multidimensional de la calidad de las respuestas. El análisis estadístico detallado —que comprende pruebas de normalidad (Shapiro-Wilk), comparaciones no paramétricas (Kruskal-Wallis con post-hoc de Dunn), análisis de interacción factorial (Scheirer-Ray-Hare) y acuerdo inter-juez (Krippendorff's alpha)— proporciona un marco riguroso para la interpretación de los resultados experimentales.

La organización modular en notebooks independientes facilita la reproducibilidad y permite iterar sobre componentes específicos sin afectar al resto del sistema. El uso de frameworks como Pydantic AI para la orquestación de agentes y `pydantic_evals` para la evaluación automatizada simplifica la gestión de la complejidad inherente a un sistema multi-agente.

El siguiente capítulo (@cap:evaluacion) presenta los resultados de la evaluación experimental, incluyendo el análisis comparativo de las nueve configuraciones mediante métricas de similitud textual y semántica, la evaluación por jueces LLM, el análisis de acuerdo inter-juez y el estudio de costos. Los resultados se presentan mediante tablas resumen, gráficos de caja (boxplots) y mapas de calor (heatmaps) que facilitan la interpretación de los efectos principales y las interacciones entre factores.



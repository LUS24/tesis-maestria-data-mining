// ARCHIVO GENERADO POR 02_auditoria_prompts_y_configuracion.py.
// Incorporado al manuscrito el 2026-11-12. Para actualizarlo, volver a ejecutar
// el script y reemplazar el archivo completo.
#import "@preview/tablem:0.3.0": three-line-table
#show table: set text(size: 8.5pt)
#set heading(numbering: "A.1")

#let prompt_sin_rag_system = "\nEres un asistente legal experto en derecho Argentino. Respondes preguntas legales basadas en la Constitución Nacional Argentina, Códigos, Leyes y jurisprudencia. Siempre que sea posible citas las fuentes legales en tu respuesta. Si no sabes la respuesta, dices que no lo sabes.\nDentro del texto de la respuesta debe mencionarse de donde provino la afirmación. Por ejemplo \"según el artículo... de la ...\". Las respuestas deben ser claras, concisas y directas al punto.\nSolo retorna la respuesta.\n"
#let prompt_rag_basico_system_template = "\nEres un asistente legal experto en derecho Argentino. Respondes preguntas legales basadas en la Constitución Nacional Argentina, Códigos, Leyes y jurisprudencia. Siempre que sea posible citas las fuentes legales en tu respuesta. Si no sabes la respuesta, dices que no lo sabes.\nDentro del texto de la respuesta debe mencionarse de donde provino la afirmación. Por ejemplo \"según el artículo... de la ...\". Las respuestas deben ser claras, concisas y directas al punto.\nSolo retorna la respuesta.\nTienes a tu disposición la siguiente información obtenida de un sistema RAG (Retrieval Augmented Generation). Utiliza esta información para responder la pregunta de la mejor manera posible.\n=========\n{retrieved_data}\n=========\n\n"
#let prompt_especialista_legal_system = "## Descripción:Eres un asistente legal experto en derecho Argentino. Respondes preguntas legales basadas en la Constitución Nacional Argentina, Códigos, Leyes y jurisprudencia.## Requisitos* Analizas la pregunta del usuario, extraes los puntos importantes y utilizas la herramienta `retrieve_relevant_documents` una vez para obtener información de la base de datos legislativa.* Analizas los documentos para generar la respuesta final.* Siempre citas las fuentes legales consultadas para la elaboración de tu respuesta. Por ejemplo: Código de Minería. Ley 1919 y sus modificatorias. Artículos 2, 3 inc. a, 5, 7, 8, 10 y 44. 25 de noviembre 1886 (Argentina)* Si no sabes la respuesta y los documentos legales no son suficientes para crear una respuesta, di que no cuentas con información para responderla.* Las respuestas deben ser claras, concisas y directas al punto.* Solo retorna la respuesta. No agregues texto irrelevante.* Respondes en español al menos que el usuario solicite otro idioma."
#let prompt_recuperador_system_6 = "Eres un especialista en búsqueda de información legislativa que:* Recibes una consulta relacionada con cuestiones legales de derecho Argentino.* La consulta puede dividirse en máximo 3 subconsultas para mejorar la recuperación.* Realizas una búsqueda por cada subconsulta en una base de datos de vectores empleando la herramienta `cosine_distance_vector_search` como máximo UsageLimits(tool_calls_limit=6) veces.Usa el valor para la clave 'usage_counts' del resultado para monitorear cuantas consultas has hecho* Seleccionas los documentos que mejor se ajustan a la consulta inicial y respondes con los resultados de la búsqueda. por ejemplo: {\"selected_documents\": [<document_1>, <document_2>, ...]}"
#let prompt_recuperador_system_7_gpt5 = "Eres un especialista en búsqueda de información legislativa que:* Recibes una consulta relacionada con cuestiones legales de derecho Argentino.* La consulta puede dividirse en máximo 3 subconsultas para mejorar la recuperación.* Realizas una búsqueda por cada subconsulta en una base de datos de vectores empleando la herramienta `cosine_distance_vector_search` como máximo UsageLimits(tool_calls_limit=7) veces.Usa el valor para la clave 'usage_counts' del resultado para monitorear cuantas consultas has hecho* Seleccionas los documentos que mejor se ajustan a la consulta inicial y respondes con los resultados de la búsqueda. por ejemplo: {\"selected_documents\": [<document_1>, <document_2>, ...]}"
#let prompt_calidad_recuperacion_system_no_ejecutado = "## Descripción:Eres un especialista en \"retrieval augmented generation\" encargado de evaluar la calidad de la recuperación.* Comparas la consulta original con la información recuperada y decides si la información es suficiente para responder la consulta.* Provees feedback para mejorar la consulta.* El feedback debe ser conciso."
#let prompt_juez_sistema = "\nYou are grading output according to a user-specified rubric. If the statement in the rubric is true for the provided input, expected output, and output, then the output passes the test. You respond with a JSON object with this structure: {reason: string, pass: boolean, score: number}\n\nExamples:\n\n<Input>What color is the sky?</Input>\n<ExpectedOutput>Blue</ExpectedOutput>\n<Output>Cerulean</Output>\n<Rubric>The output is consistent with the expected output but doesn't have to match exactly</Rubric>\n{\"reason\": \"'Cerulean' is a shade of blue\", \"pass\": true, \"score\": 1.0}\n\n<Input>How many legs does a spider have?</Input>\n<ExpectedOutput>8</ExpectedOutput>\n<Output>Six</Output>\n<Rubric>The output is factually consistent with the expected output</Rubric>\n{\"reason\": \"Spiders have 8 legs\", \"pass\": false, \"score\": 0.0}\n"
#let prompt_juez_respuesta_correcta_template = "<Input>\n⟦PREGUNTA⟧\n</Input>\n\n<Output>\n⟦RESPUESTA⟧\n</Output>\n\n<Rubric>\n{'nombre_evaluacion': 'respuesta_correcta', 'descripcion': 'La respuesta provista está alineada con la respuesta esperada. (Evalúa en español)', 'criterios': {'0.0': 'La respuesta está en blanco o no coincide en absoluto con la respuesta esperada.', '0.25': 'La respuesta tiene poca relación con la respuesta esperada y contiene errores significativos.', '0.5': 'La respuesta es parcialmente correcta, pero omite información clave o tiene errores menores.', '0.75': 'La respuesta es mayormente correcta, con solo errores menores.', '1.0': 'La respuesta es completamente correcta y precisa.'}}\n</Rubric>\n\n<ExpectedOutput>\n⟦RESPUESTA_ESPERADA⟧\n</ExpectedOutput>"
#let prompt_juez_precision_legal_template = "<Input>\n⟦PREGUNTA⟧\n</Input>\n\n<Output>\n⟦RESPUESTA⟧\n</Output>\n\n<Rubric>\n{'nombre_evaluacion': 'precision_legal', 'descripcion': 'La respuesta cita correctamente los artículos relevantes del Código de Minería Argentino. (Evalúa en español)', 'criterios': {'0.0': 'No cita ningún artículo relevante o cita artículos incorrectos.', '0.25': 'Cita algunos artículos relevantes, pero omite otros importantes.', '0.5': 'Cita la mayoría de los artículos relevantes y otros irrelevantes.', '0.75': 'Cita casi todos los artículos relevantes con precisión y pocos irrelevantes.', '1.0': 'Cita todos los artículos relevantes y ninguno irrelevante de manera precisa y completa.'}}\n</Rubric>\n\n<ExpectedOutput>\n⟦RESPUESTA_ESPERADA⟧\n</ExpectedOutput>"

= Prompts y configuración experimental <anexo-prompts>

Este anexo documenta los prompts y la configuración observada en la versión evaluada. Su finalidad es hacer trazable qué instrucciones recibió cada componente y distinguir la configuración nominal del código de la configuración que efectivamente produjo las respuestas.

#block(
  width: 100%,
  inset: 8pt,
  stroke: 0.5pt + luma(180),
  radius: 3pt,
  [
    *Convención de transcripción.* Los textos se reproducen sin correcciones de estilo. Los saltos de línea que aparecen en la composición son ajustes de página; el contenido canónico y su SHA-256 están registrados en `salidas/prompts_canonicos.json`. Cuando un prompt contiene un marcador entre llaves, se indica en el texto.
  ],
)

== Configuración observada

La @tabla-configuracion-observada distingue los componentes activos, el modelo que los ejecutó y el límite de recuperación registrado. La configuración no fue simétrica entre modelos: la corrida de gpt-5 utilizó una variante del prompt del recuperador con límite 7 y las corridas de gpt-5-mini y gpt-5-nano utilizaron la variante con límite 6.

#figure(
  three-line-table(
    columns: (3.6cm, 3.0cm, 2.3cm, 1fr),
    [
      | *Configuración* | *Componente* | *Modelo* | *Prompt y límite observados* |
      | :--- | :--- | :--- | :--- |
      | Sin RAG | Generador | variable | `sin_rag_system`; sin herramientas ni recuperación. |
      | RAG básico | Generador | variable | `rag_basico_system_template`; top-10 en una búsqueda, sin herramientas. |
      | Agentic-RAG + gpt-5 | Especialista Legal | gpt-5 | `especialista_legal_system`; una invocación nominal de recuperación. |
      | Agentic-RAG + gpt-5 | Agente de Recuperación | gpt-5 | `recuperador_system_7_gpt5`; hasta 7 búsquedas. |
      | Agentic-RAG + gpt-5-mini | Agente de Recuperación | gpt-5 | `recuperador_system_6`; hasta 6 búsquedas. |
      | Agentic-RAG + gpt-5-nano | Agente de Recuperación | gpt-5 | `recuperador_system_6`; hasta 6 búsquedas. |
      | Agentic-RAG, todas | Agente de Calidad | gpt-5 definido | `calidad_recuperacion_system_no_ejecutado`; definido, sin herramientas y nunca ejecutado. |
    ],
  ),
  caption: [Configuración observada de prompts y modelos. El modelo consignado para el Agente de Recuperación es siempre gpt-5; el factor «modelo» identifica al generador de la respuesta.],
) <tabla-configuracion-observada>

== Prompts de generación

=== Sin RAG

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_sin_rag_system)
  ],
)
#text(size: 8pt)[Fuente: `codigo_experimentos/part_e/02_query_llms_for_responses.ipynb`. SHA-256: `bdaa8c97c4889e773f8a4b84c865d57326b9cc83128d3e15a4f60839f0550755`. Estado: fuente sin logs de entrada.]


=== RAG básico

El marcador `{retrieved_data}` se sustituye por la representación Python de la lista de hasta diez documentos recuperados, conservando los campos `codigo_norma`, `tipo_parte`, `numero_parte`, `ultimo_estado`, `contenido_texto`, `index` y `distance`.

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_rag_basico_system_template)
  ],
)
#text(size: 8pt)[Fuente: `codigo_experimentos/part_f/01_rag_llm_responses.ipynb`. SHA-256: `c4bee157b0c7035d1d4a609ee0009037274c50beacf8d475eb25ca4de14161c6`. Estado: fuente sin logs de entrada.]


=== Agente Especialista Legal

El texto siguiente coincide con la única variante registrada en las 237 sesiones agénticas.

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_especialista_legal_system)
  ],
)
#text(size: 8pt)[Fuente: `codigo_experimentos/part_g/01_generate_responses_using_agents.py`. SHA-256: `cc3db2a1e375782ee5d40db517d6e3224e20c3d3ea6d8511da8fef12b295f322`. Estado: observado en logs.]


=== Agente de Recuperación

El Agente de Recuperación tuvo dos variantes. La primera se usó en la corrida de gpt-5 del 12 de noviembre de 2025; la segunda, en las corridas de gpt-5-mini y gpt-5-nano del 13 de noviembre de 2025. El texto contiene la representación literal del objeto `UsageLimits` porque el prompt se construyó interpolando ese objeto en un f-string.

==== Variante usada con gpt-5: límite 7

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_recuperador_system_7_gpt5)
  ],
)
#text(size: 8pt)[Fuente: `codigo_experimentos/part_g/chat_data/openai_gpt-5/**/retrieval_agent.json`. SHA-256: `4a77f607a7392ed186bc54a2014b8032a282c2e94b1e80fcd82890b02e645e2b`. Estado: observado en logs.]


==== Variante usada con gpt-5-mini y gpt-5-nano: límite 6

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_recuperador_system_6)
  ],
)
#text(size: 8pt)[Fuente: `codigo_experimentos/part_g/chat_data/**/retrieval_agent.json`. SHA-256: `27e1a20b08700a425b6e4b22220c9c6fdb397e7faa5b1b99d29b6c281f30cac2`. Estado: observado en logs.]


=== Agente de Calidad de Recuperación (definido, no ejecutado)

El agente fue definido en el código con el prompt siguiente, pero no se registró su herramienta, no se invocó y no produjo ningún registro. Se excluyó por razones de costo y complejidad; no se realizó una comparación empírica de su contribución.

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_calidad_recuperacion_system_no_ejecutado)
  ],
)
#text(size: 8pt)[Fuente: `codigo_experimentos/part_g/01_generate_responses_using_agents.py`. SHA-256: `f0cdae610e11215eb2879bfbfb2a911e631f434f6c2d08b5be7d35428beceb62`. Estado: definido, nunca enviado a un modelo.]


== Prompts de evaluación

Los tres jueces utilizaron el mismo prompt de sistema y la misma plantilla de usuario; cambiaron el modelo y la rúbrica. Los prompts se generaron con `pydantic-evals` 1.1.0 mediante `LLMJudge` con `include_input=True` e `include_expected_output=True`.

=== Prompt de sistema del juez

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_juez_sistema)
  ],
)
#text(size: 8pt)[Fuente: `codigo_experimentos/.venv/lib/python3.13/site-packages/pydantic_evals/evaluators/llm_as_a_judge.py (pydantic-evals 1.1.0)`. SHA-256: `2294a90c225a0d014a38fa4fbd31ed6cbdd46d964e67bb485a6a1548fbbc5d5b`. Estado: generado por la librería; aplicado a los tres jueces.]


=== Plantilla de evaluación de respuesta correcta

Los marcadores `⟦PREGUNTA⟧`, `⟦RESPUESTA⟧` y `⟦RESPUESTA_ESPERADA⟧` identifican los puntos donde se insertan el caso evaluado; no forman parte del texto enviado.

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_juez_respuesta_correcta_template)
  ],
)
#text(size: 8pt)[Fuente: `codigo_experimentos/part_h_1/01_llm_as_a_judge.ipynb y batch_2`. SHA-256: `e4216480d45fe72b18a2b31b27c3cc7c113948d63d845a1bc20309e151ba8e48`. Estado: generado por la librería; aplicado a los tres jueces.]


=== Plantilla de evaluación de precisión legal

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  breakable: true,
  [
    #set text(size: 8pt)
    #text(prompt_juez_precision_legal_template)
  ],
)
#text(size: 8pt)[Fuente: `codigo_experimentos/part_h_1/01_llm_as_a_judge.ipynb y batch_2`. SHA-256: `5807ee7e59eff27ddd2a108aac25eef90959125b65b18953d4a11c432575cde1`. Estado: generado por la librería; aplicado a los tres jueces.]


== Modelos jueces y parámetros

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto),
    [
      | *Modelo* | *Rúbrica* | *Temperatura solicitada* | *Máx. tokens de salida* |
      | :--- | :--- | :---: | :---: |
      | `openrouter:deepseek/deepseek-chat-v3.1` | `precision_legal` | 0.0 | 5000 |
      | `openrouter:deepseek/deepseek-chat-v3.1` | `respuesta_correcta` | 0.0 | 5000 |
      | `openrouter:moonshotai/kimi-k2-0905` | `precision_legal` | 0.0 | 5000 |
      | `openrouter:moonshotai/kimi-k2-0905` | `respuesta_correcta` | 0.0 | 5000 |
      | `openrouter:x-ai/grok-4.1-fast:free` | `precision_legal` | 0.0 | 5000 |
      | `openrouter:x-ai/grok-4.1-fast:free` | `respuesta_correcta` | 0.0 | 5000 |
    ],
  ),
  caption: [Configuración registrada de los jueces. La temperatura solicitada no se interpreta aquí como evidencia de determinismo; esa cuestión se documenta en la corrección IX.1.3.],
) <tabla-jueces-parametros>

== Procedencia y hashes

#figure(
  three-line-table(
    columns: (5.6cm, 2.9cm, 1fr),
    [
      | *Prompt* | *SHA-256 (prefijo)* | *Procedencia* |
      | :--- | :--- | :--- |
      | `sin_rag_system` | `bdaa8c97c4889e77` | Notebook de `part_e`; sin logs de entrada. |
      | `rag_basico_system_template` | `c4bee157b0c7035d` | Notebook de `part_f`; sin logs de entrada. |
      | `especialista_legal_system` | `cc3db2a1e375782e` | 237 logs; una variante. |
      | `recuperador_system_7_gpt5` | `4a77f607a7392ed1` | 79 logs de gpt-5. |
      | `recuperador_system_6` | `27e1a20b08700a42` | 158 logs de mini/nano. |
      | `calidad_recuperacion_` #linebreak() `system_no_ejecutado` | `f0cdae610e11215e` | Definición de código; 0 logs. |
      | `juez_sistema` | `2294a90c225a0d01` | pydantic-evals 1.1.0. |
      | `juez_respuesta_correcta_template` | `e4216480d45fe72b` | pydantic-evals 1.1.0. |
      | `juez_precision_legal_template` | `5807ee7e59eff27d` | pydantic-evals 1.1.0. |
    ],
  ),
  caption: [Inventario de prompts y hashes. Los valores completos, la longitud y el texto canónico están en `salidas/prompts_canonicos.json`.],
) <tabla-prompts-hashes>

#text(size: 8pt)[Generado el 2026-11-12T00:49:08.416484+00:00 por `02_auditoria_prompts_y_configuracion.py`.]

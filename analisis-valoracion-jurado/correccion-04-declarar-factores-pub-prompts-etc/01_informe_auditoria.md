# Informe de auditoría para IX.1.4

**Punto:** declarar factores confundidos, publicar prompts y resolver contradicciones.  
**Fecha de auditoría:** 2026-11-12.  
**Commit inspeccionado:** `b4a71aae754a13854fe938e55ab3d97debb0be10`.  
**Alcance:** `codigo_experimentos/part_g`, `part_e`, `part_f`, `part_h_1`, notebooks de prompts, logs agénticos y reportes de jueces.  
**Naturaleza:** auditoría read-only. No se modificaron fuentes, logs ni artefactos históricos.

## 1. Resultado principal

La configuración experimental **no fue simétrica entre los tres modelos de Agentic-RAG**. El análisis de los 237 logs muestra:

| Modelo especialista | Sesiones | Prompt del recuperador | Límite declarado | Fecha de la corrida |
| --- | ---: | --- | ---: | --- |
| gpt-5 | 79 | `recuperador_system_7_gpt5` | 7 | 2025-11-12, 11:15–19:27 UTC |
| gpt-5-mini | 79 | `recuperador_system_6` | 6 | 2025-11-13, 13:19–17:52 UTC |
| gpt-5-nano | 79 | `recuperador_system_6` | 6 | 2025-11-13, 08:05–12:26 UTC |

En gpt-5, **33 de 79 sesiones realizaron 7 búsquedas vectoriales**. En mini y nano, ninguna superó 6. El script final actual declara 6, pero no reproduce la corrida histórica de gpt-5.

Esto no invalida por sí solo los resultados, pero sí impide presentar el diseño como un factorial 3 × 3 perfectamente homogéneo. La diferencia de presupuesto de recuperación debe declararse como amenaza a la validez y no quedar oculta bajo la expresión “hasta seis búsquedas”.

## 2. Estado del Agente de Calidad de Recuperación

El autor confirmó que el agente se excluyó **por razones de costo y complejidad**. La auditoría es consistente con esa decisión y añade estos hechos:

- El agente está definido en `INSTRUCTIONS["retrieval_quality_agent"]`, con un prompt de 329 caracteres y SHA-256 `f0cdae610e11215eb2879bfbfb2a911e631f434f6c2d08b5be7d35428beceb62`.
- Se instancia en el script final, pero **sin herramientas**.
- La función `evaluate_retrieval` existe en el código, pero no está registrada como herramienta del recuperador.
- Hay **0 archivos** `retrieval_quality_agent.json` y **0 llamadas** a `evaluate_retrieval` en las 237 sesiones.
- Por tanto, el prompt del agente de calidad **nunca se envió a un modelo** y no existe evidencia empírica de que mejorara o empeorara el sistema.
- El notebook `part_g/01_generate_responses_using_agents.ipynb` conserva una versión anterior donde `evaluate_retrieval` sí aparece activo y el prompt del recuperador no tiene límite explícito. Ese notebook **no es la fuente canónica** de la corrida final; el script `.py` y los logs sí lo son.

## 3. Prompts y variantes

### 3.1 Sin RAG y RAG básico

Los prompts se tomaron de las celdas que generaron las respuestas:

- Sin RAG: `part_e/02_query_llms_for_responses.ipynb`, `system_prompt`, líneas 67–71; 497 caracteres; SHA-256 `bdaa8c97c4889e773f8a4b84c865d57326b9cc83128d3e15a4f60839f0550755`.
- RAG básico: `part_f/01_rag_llm_responses.ipynb`, `system_prompt`, líneas 120–129; 725 caracteres; SHA-256 `c4bee157b0c7035d1d4a609ee0009037274c50beacf8d475eb25ca4de14161c6`.
- La diferencia entre ambos es el bloque de contexto añadido al final del prompt de RAG básico. El marcador `{retrieved_data}` se reemplaza por la representación Python de una lista de hasta diez diccionarios.
- Los JSON de respuesta conservan metadatos de uso, pero **no conservan el prompt de entrada**. La procedencia de estos dos prompts es el notebook fuente, no un log de mensajes.

### 3.2 Agente Especialista Legal

- Una única variante en 237 sesiones y 476 solicitudes registradas.
- 995 caracteres; SHA-256 `cc3db2a1e375782ee5d40db517d6e3224e20c3d3ea6d8511da8fef12b295f322`.
- Coincide exactamente con `INSTRUCTIONS["law_specialist_agent"]` del script final.
- El texto real está concatenado sin saltos de línea ni espacios entre secciones: `## Descripción:Eres...`, `## Requisitos* Analizas...`, etc. El manuscrito actual lo presenta como un párrafo proseado; el anexo propuesto reproduce el texto canónico.

### 3.3 Agente de Recuperación

Hay dos variantes históricas de 700 caracteres:

| Variante | SHA-256 | Sesiones | Solicitudes | Modelos | Límite |
| --- | --- | ---: | ---: | --- | ---: |
| `recuperador_system_7_gpt5` | `4a77f607a7392ed186bc54a2014b8032a282c2e94b1e80fcd82890b02e645e2b` | 79 | 345 | gpt-5 | 7 |
| `recuperador_system_6` | `27e1a20b08700a425b6e4b22220c9c6fdb397e7faa5b1b99d29b6c281f30cac2` | 158 | 653 | gpt-5-mini, gpt-5-nano | 6 |

La variante de 6 coincide con el script final. La variante de 7 no. Ambas contienen el texto literal `UsageLimits(tool_calls_limit=7)` o `...=6`, porque el prompt se construyó interpolando un objeto `UsageLimits` en un f-string. Esa expresión debe conservarse en el anexo si se reproduce literalmente el prompt.

### 3.4 Jueces

- 27 reportes: 9 por cada juez (DeepSeek-V3, Grok 4.1 Fast, Kimi K2 0905).
- Las dos rúbricas son idénticas en los 27 reportes, salvo el modelo juez.
- `LLMJudge` se ejecutó con `include_input=True`, `include_expected_output=True`, `temperature=0.0` solicitada y `max_tokens=5000`.
- El prompt de sistema y las plantillas de usuario se reconstruyeron con `pydantic-evals` 1.1.0:
  - sistema del juez: 819 caracteres, SHA-256 `2294a90c225a0d014a38fa4fbd31ed6cbdd46d964e67bb485a6a1548fbbc5d5b`;
  - plantilla de respuesta correcta: 735 caracteres, SHA-256 `449777c32c7e0b3e61011adec7066803339234d0371a1a1fa3ec32bb2d0f0f4a`;
  - plantilla de precisión legal: 738 caracteres, SHA-256 `2d59bdf5e42f5e953e8b89d6066fba73f39e2d1e0f73f7ef03ad079197a20a5c`.

## 4. Contradicciones y anomalías detectadas

### 4.1 El Agente de Calidad no se excluyó por falta de mejoras

El texto actual de metodología y conclusión afirma que su complejidad “no se tradujo en mejoras marginales significativas”. No existe comparación registrada que sostenga esa afirmación. Debe reemplazarse por la razón confirmada: **costo y complejidad**. No se debe escribir que su exclusión fue innocua.

### 4.2 El especialista no “solicita búsquedas adicionales” en el sentido descrito

El prompt del especialista pide usar `retrieve_relevant_documents` **una vez**. El código fija `DOCUMENT_RETRIEVAL_LIMIT = 1`. La búsqueda múltiple ocurre dentro del Agente de Recuperación, no como una segunda ronda del especialista.

No obstante, la auditoría encontró **una excepción**: en la sesión `16_01` de gpt-5, el especialista registró **3 llamadas** a `retrieve_relevant_documents`. En las otras 236 sesiones registró una. La formulación correcta es “límite nominal de una invocación; 236/237 sesiones lo respetan, con una excepción documentada”. No conviene afirmar una garantía universal.

### 4.3 El límite de seis búsquedas no es uniforme

El código final y el prompt de mini/nano declaran 6. La corrida de gpt-5 utilizó 7 y 33 sesiones consumieron las 7. Cualquier tabla que diga “6 para todos” es incorrecta para los datos evaluados.

### 4.4 El notebook de agentes no coincide con el script final

El notebook de `part_g` contiene prompts antiguos con formato APA y una herramienta de calidad activa. El script `.py` contiene los prompts efectivamente registrados en los logs. Esta diferencia debe explicarse en el repositorio; en el manuscrito, la fuente canónica debe ser el script y los logs, no el notebook.

### 4.5 Few-shot y Chain-of-Thought no están implementados

El capítulo 3 afirma que el sistema combina few-shot prompting y Chain-of-Thought. Los prompts reproducidos no contienen ejemplos etiquetados ni una instrucción de razonamiento paso a paso. Lo que sí existe es prompting zero-shot con instrucciones estructuradas, una instrucción de citación y una herramienta de recuperación. La descomposición de la consulta se delega al Agente de Recuperación.

### 4.6 La etiqueta Agentic-RAG requiere una definición operativa

En esta tesis, “Agentic-RAG” designa una arquitectura acotada de dos agentes activos, una delegación nominal de recuperación y ninguna verificación automática de la respuesta. No debe usarse para sugerir un planificador autónomo, un ciclo iterativo del especialista ni un verificador activo.

### 4.7 El objetivo 2 no se cumplió completamente

Se implementaron dos agentes activos, pero el tercer agente no se ejecutó y no hay iteración del especialista ni verificación automática. Corresponde “cumplimiento parcial”, no “cumplimiento completo”.

## 5. Implicancias para la interpretación

Las estrategias no son variaciones de un único factor. En Agentic-RAG cambian simultáneamente:

1. el modelo que redacta y el modelo que recupera;
2. el prompt del generador;
3. la descomposición de la consulta;
4. el número de candidatos recuperados;
5. la selección de fragmentos por gpt-5;
6. el presupuesto de búsquedas;
7. la existencia o no de una etapa de verificación.

Sin ablaciones, el efecto atribuido a “Agentic-RAG” no puede descomponerse en esos componentes. La diferencia 7/6 entre gpt-5 y mini/nano agrega una amenaza específica al contraste entre modelos.

## 6. Artefactos de esta carpeta

- `02_auditoria_prompts_y_configuracion.py`: script reproducible, read-only, que reconstruye todos los conteos.
- `salidas/prompts_canonicos.json`: prompts exactos, hashes, procedencia y configuración observada.
- `salidas/sesiones_agentic.csv`: una fila por sesión, con modelo, prompt, límite, llamadas y timestamps.
- `salidas/variantes_prompts_agente.csv`: agregado de variantes por modelo.
- `salidas/inventario_prompts.csv`: inventario legible de prompts.
- `salidas/diff_prompts_script_vs_notebook.diff`: diferencia entre el notebook antiguo y el script final.
- `salidas/evidencia_codigo.md`: fragmentos de código que prueban la configuración descrita.
- `salidas/resumen_auditoria.json`: conteos y anomalías.
- `propuestas/anexo_02_prompts_y_parametros.typ`: anexo listo para revisar e insertar.
- `propuestas/cambios_manuscrito.md`: cambios propuestos, con texto anterior y texto nuevo.
- `propuestas/tabla_factores_confundidos.typ`: tabla de alcance y amenazas.
- `propuestas/diagrama_agentic_rag_operativo.mmd` y su SVG: diagrama coherente con los dos agentes y los límites observados.
- `04_checklist_aceptacion.md`: criterios de cierre.

Los valores completos y las rutas de procedencia están en `salidas/prompts_canonicos.json`; este informe usa solo prefijos de hash cuando la tabla debe seguir siendo legible.

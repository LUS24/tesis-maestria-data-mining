# Plan de correcciones y recomendaciones para la versión definitiva

**Documento de origen:** `analisis-valoracion-jurado/Valoracion_TF_Spairani_gp_v3.md`, sección IX, con trazabilidad a las observaciones V.1–V.11 y a las Tablas 2–4.  
**Repositorio inspeccionado:** `/mnt/d/OneDrive/ex_dropbox/tesis-maestria-data-mining`.  
**Fecha de inspección:** 2026-11-11.  
**Alcance de este documento:** plan de implementación; no contiene todavía resultados inferenciales corregidos ni sustituye la revisión de un profesional del derecho.

> **Ubicación adoptada (PI-01):** la implementación se organizó en `analisis-valoracion-jurado/correccion-01` a `correccion-07`, más `verificacion-analisis-estadistico/`. No se crea `codigo_experimentos/part_k_correcciones_jurado`; esa propuesta del plan queda reemplazada. Los artefactos históricos de `part_k` no se usan como fuente de las correcciones.


## 1. Resumen ejecutivo

La mayor parte de las correcciones requeridas puede resolverse **sin volver a generar respuestas**, porque el repositorio contiene las 711 respuestas, las evaluaciones de tres jueces, los metadatos de uso y los registros de los agentes. Las excepciones son la validación humana, las réplicas y la ablación, que dependen de personas, presupuesto y nuevas llamadas a APIs.

La inspección del repositorio también reveló dos problemas concretos que deben incorporarse al plan:

1. **Las 27 puntuaciones medias ausentes no corresponden a 27 fallos de generación.** Son las 27 combinaciones de las unidades 23, 24 y 25. En `part_i/combined_metrics_for_analysis.csv`, esas unidades tienen `nro_subpregunta` vacío; en `part_i/final_judge_results.csv`, tienen `numero_subpregunta = 0`. El join de `part_j/01_exploracion_descriptiva_correlacion.ipynb` no las enlaza. El archivo de jueces contiene 2.133 registros únicos, es decir, 711 configuraciones × 3 jueces. Por tanto, los 27 valores son recuperables mediante una normalización de identificadores **en una tabla derivada nueva**, sin tocar los archivos fuente.
2. **La celda Agentic-RAG + gpt-5-nano contiene 28 respuestas en blanco o compuestas solo por espacios** entre 79: 27 cadenas vacías y una cadena de espacios. Estas salidas deben analizarse separadamente de las 27 puntuaciones ausentes por el problema de join. Las demás 51 salidas de esa celda no están en blanco. Este diagnóstico preliminar es compatible con un modo de falla concentrado, pero no demuestra por sí solo su causa.

Otros hallazgos que condicionan el plan:

- `part_j/04_modelo_mixto_interaccion.ipynb` implementa Scheirer–Ray–Hare; **no estima un modelo mixto**. Se necesita un análisis nuevo, no solo trasladar sus resultados al manuscrito.
- El perfil de Pydantic AI 1.1.0 instalado y fijado en `uv.lock` declara `temperature` como parámetro no admitido para `gpt-5-nano`, `gpt-5-mini` y `gpt-5`. Los registros guardan configuración solicitada y tokens de razonamiento, pero no un volcado HTTP completo. En particular, el esfuerzo de razonamiento efectivo del servidor **no es recuperable si no fue registrado**; debe declararse como desconocido, no inferirse.
- El corpus JSON contiene 482 nodos estructurales: 22 títulos, 6 secciones, 55 acápites, 398 artículos y un apéndice. Hay 397 artículos con texto y uno vacío, el artículo 239, marcado como derogado. Esto permite corregir las cifras 245/399 por una descripción verificable de 398 nodos de tipo artículo.
- El código de creación de Milvus en `part_c/01_initial_vector_db_creation.ipynb` configura `AUTOINDEX`, aunque el manuscrito afirma `IVF_FLAT`. Debe verificarse el índice histórico o corregirse la descripción del código; no debe darse por cierta ninguna de las dos versiones sin una comprobación adicional.
- El acceso público ya cambió respecto de lo observado por el jurado: el 2026-11-11, `https://github.com/LUS24/tesis-maestria-data-mining` devolvió HTTP 200 y la API de GitHub informó `"private": false`. El árbol público incluye el benchmark, el corpus, 32 notebooks, 1.838 JSON de `chat_data` y 27 reportes de jueces. Queda pendiente una prueba de reproducción desde una clonación anónima de la versión final.

## 2. Reglas de implementación y organización propuesta

### 2.1 Inmutabilidad de fuentes y registros

1. No modificar, renombrar ni sobrescribir ningún JSON, CSV, SQLite, PDF, log o respuesta de jueces ya existente.
2. No ejecutar los notebooks originales que escriben sobre sus propias entradas. Varios notebooks de `part_e`, `part_f`, `part_g`, `part_i` y `part_j` tienen rutas de salida que podrían sobrescribir artefactos históricos.
3. Toda limpieza —incluida la equivalencia entre subpregunta vacía, `None` y `0`— se hará en memoria y se guardará como **artefacto derivado nuevo**, con una columna que conserve el identificador original.
4. Las nuevas ejecuciones, si se realizan, escribirán en directorios nuevos. Nunca se completarán ni corregirán los logs originales.
5. Cada notebook registrará rutas, tamaños y SHA-256 de sus entradas, versión de Python/R, paquetes, commit de Git y semilla aleatoria. Los resultados derivados incluirán una columna `fuente` o una tabla de procedencia.
6. Los valores observados preliminares mencionados en este plan deben recalcularse en los notebooks antes de incorporarse al manuscrito.

### 2.2 Nuevos notebooks propuestos

Crear, en la fase de implementación, el directorio `codigo_experimentos/part_k_correcciones_jurado/`:

| Notebook | Propósito | Nuevas llamadas a LLM |
| --- | --- | --- |
| `00_integridad_y_procedencia.ipynb` | Inventario, hashes, esquemas, unicidad, rejilla 25/79/9/3 y construcción de la tabla analítica derivada | No |
| `01_diagnostico_fallos_y_nano_agentic.ipynb` | Clasificación de respuestas, faltantes por celda, trazabilidad de logs y análisis de la celda anómala | No |
| `02_parametros_prompts_y_configuracion.ipynb` | Configuración solicitada/registrada/efectiva, tokens de razonamiento, prompts y límites de agentes | No; usar transporte simulado local |
| `03_inferencia_apareada_y_anidada.ipynb` | Modelo ordinal mixto, pruebas apareadas, efectos, IC y análisis de sensibilidad | No |
| `04_auditoria_corpus_y_benchmark.ipynb` | Linaje y versión del corpus, calidad de extracción, conteos y revisión de referencias | No |
| `05_evaluacion_aislada_recuperacion.ipynb` | Recall@k, MRR, nDCG, BM25, embeddings alternativos y recuperación agéntica desde logs | No |
| `06_evaluacion_determinista_citaciones.ipynb` | Extracción de citas, precisión, exhaustividad, inexistencia y validación del parser | No |
| `07_costos_pareto.ipynb` | Costos, frontera de Pareto y costo por respuesta aceptable, sin el piso arbitrario | No |
| `08_validacion_humana_jueces.ipynb` | Muestreo ciego, paquete de anotación y acuerdo humano–LLM | No; requiere nuevas calificaciones humanas |
| `09_replicas_y_ablacion.ipynb` | Protocolo y análisis de 3–5 réplicas y ablación con el mismo modelo en ambos agentes | Sí, solo si se aprueba el experimento |
| `10_auditoria_bibliografica.ipynb` | Consistencia de citas, DOI/URL, metadatos y versiones publicadas | No |

Las salidas se escribirán en `part_k_correcciones_jurado/salidas/` con nombres nuevos. Las figuras definitivas podrán copiarse posteriormente a `manuscrito/media/` con nombres específicos, sin sobrescribir las figuras históricas hasta haber actualizado sus referencias en Typst.

### 2.3 Fuente analítica y controles mínimos

Usar como insumos principales:

- Respuestas y referencias: `codigo_experimentos/part_h_1/llm_responses_all_results_with_metrics_judged_FINAL.json` y `part_i/responses_text_cleaned.csv`.
- Evaluaciones: los 27 reportes de `part_h_1/reports/` y `part_h_1/final_judge_results.csv`.
- Métricas y metadatos: `part_i/combined_metrics_for_analysis.csv` y `part_i/metadata_tokens_cost_cleaned.csv`.
- Logs agénticos: `part_g/chat_data/<modelo>/<caso>/{law_specialist_agent.json,retrieval_agent.json,retrieval_history/}`.
- Benchmark y corpus: `data/evaluation_questions_v20250804_101435.json` y `data/codigo_de_mineria_actualizado_2025_08_02.json`.
- Recuperación original: `part_d/20251012_retrieval_baseline_from_20250804_101435_generated_questions.json`.
- Corpus primario y extracción: `codigo_experimentos/data/inputs/pdf/seccion_primera_19970530.pdf`, `data/databases/responses.db` y `data/outputs/llm_img_to_md/`.

`00_integridad_y_procedencia.ipynb` debe construir `caso_id`, `unidad_id` y `observacion_id` canónicos. Para las preguntas de unidad única, una regla derivada explícita puede mapear `None`/vacío y `0` a un mismo sufijo `00`, conservando los campos originales. Controles de aceptación:

- 25 casos, 79 unidades y 711 pares unidad–configuración únicos.
- 2.133 filas juez–observación únicas, sin duplicados.
- Nueve celdas con 79 unidades antes de aplicar cualquier escenario de exclusión.
- Todas las puntuaciones de jueces enlazadas; cualquier ausencia restante debe tener una causa documentada.
- Tabla separada para valores fuera de rúbrica, sin llamar “imputación” a lo que sea simplemente una transformación de escala.
- Conciliación entre texto en blanco, puntuación ausente, error de generación y error del juez como cuatro estados distintos.

## 3. Correcciones requeridas de IX.1

### IX.1.1 — Rehacer el análisis inferencial respetando apareamiento y anidamiento

**Factibilidad:** alta, con datos existentes.  
**Notebooks:** `00`, `01` y `03`.  
**Archivos que luego deben modificarse:** `06_capitulo_05_metodologia.typ`, `07_capitulo_06_evaluacion.typ`, `01_texto_preliminar.typ`, `09_capitulo_08_conclusion_y_trabajos_futuros.typ` y ambos README.

#### A. Definir el estimando y la estructura antes de mirar los nuevos valores p

- Unidad repetida: las 79 subpreguntas/unidades evaluadas en las nueve configuraciones.
- Agrupamiento superior: 25 casos; las unidades de un mismo caso comparten escenario y no son independientes.
- Evaluaciones: tres jueces por respuesta.
- Variable ordinal original: `score_respuesta_correcta ∈ {0, 0.25, 0.5, 0.75, 1}`.
- Factores: estrategia y **modelo del especialista**. En Agentic-RAG debe quedar explícito que el recuperador es siempre gpt-5.
- Familia de comparaciones: definir antes del análisis las nueve comparaciones simples de estrategia dentro de modelo y, si se reportan, las nueve de modelo dentro de estrategia. Aplicar Holm dentro de familias declaradas, sin elegir la agrupación según el resultado.

#### B. Análisis principal: modelo ordinal mixto

En `03_inferencia_apareada_y_anidada.ipynb`, preferentemente con kernel R y el paquete `ordinal`, ajustar un modelo de enlaces acumulativos con:

```text
score_respuesta_correcta ~ estrategia * modelo_especialista
                           + juez
                           + (1 | caso_id)
                           + (1 | unidad_id)
```

- `unidad_id` debe ser globalmente único; así representa unidades anidadas en casos junto con el intercepto de caso.
- Incorporar `juez` como efecto fijo para controlar severidad sistemática; con solo tres jueces, un intercepto aleatorio sería difícil de estimar de forma estable.
- Probar la interacción mediante comparación de modelos con y sin `estrategia:modelo_especialista`, con una prueba de razón de verosimilitud. Esta prueba reemplaza el sustento inferencial principal de Scheirer–Ray–Hare.
- Reportar coeficientes como odds ratios con IC 95%, probabilidades predichas por celda y contrastes de efectos simples con IC. Para facilitar la interpretación, agregar diferencias de probabilidad de obtener una respuesta “mayormente correcta” (`score ≥ 0,75`) derivadas del modelo, dejando claro que son estimaciones modeladas.
- Documentar convergencia, singularidad, umbrales estimados y diagnóstico de odds proporcionales. Si el modelo no converge, aplicar una simplificación preespecificada o un modelo ordinal bayesiano; no recorrer modelos hasta obtener significación.
- Estimar también, como sensibilidad, un modelo por juez y un modelo sobre el promedio de jueces. El promedio tiene 13 valores posibles y no debe describirse como una observación ordinal individual de cinco niveles.

El repositorio ya utiliza R en `part_i/analisis_datos.qmd`, pero no fija actualmente los paquetes necesarios. Documentar nuevas versiones de `ordinal`, `emmeans` e `IRkernel` en un `renv.lock` nuevo o en la documentación del directorio; no instalar paquetes automáticamente dentro del notebook.

#### C. Análisis no paramétrico de sensibilidad

- Friedman para las tres estrategias dentro de cada modelo y para los tres modelos dentro de cada estrategia, usando la misma unidad como bloque.
- Wilcoxon de rangos con signo para contrastes por pares sobre pares realmente apareados, con corrección de Holm.
- Reportar W de Kendall para Friedman, correlación rango-biserial apareada y diferencias de medianas/medias.
- Estimar IC 95% mediante **bootstrap por casos** —remuestrear los 25 casos con todas sus unidades— con semilla fija y al menos 5.000 réplicas. Un bootstrap por filas invalidaría el anidamiento.
- Friedman/Wilcoxon no resuelven por sí solos el anidamiento; por eso quedan como sensibilidad y el modelo mixto es el análisis principal.
- No usar ART como sustituto automático sin demostrar que la implementación contempla repetición y anidamiento. Si se agrega ART como sensibilidad, documentar explícitamente esa parte del diseño.

#### D. Escenarios de fallos y referencias problemáticas

Repetir el análisis con un plan fijo:

1. **Escenario de sistema, fallo = 0:** toda salida vacía o fallo técnico confirmado recibe 0 en los tres jueces en el dataset derivado. Esto representa la utilidad del sistema para el usuario.
2. **Escenario de exclusión:** excluir esas salidas y usar pares completos por contraste. Informar el `n` real de cada celda y de cada comparación.
3. **Escenario de jueces observados:** conservar las puntuaciones originales para evaluar la sensibilidad a la evaluación de salidas vacías.
4. Si la auditoría jurídica confirma referencias inválidas, agregar un análisis que excluya las unidades afectadas. No cambiar retrospectivamente las respuestas esperadas fuente.

No elegir como “principal” el escenario que produzca el resultado más favorable. El escenario fallo = 0 debe ser el principal para evaluar el sistema completo; los demás son sensibilidad.

#### E. Cambios editoriales

- En metodología, sustituir la justificación basada únicamente en Shapiro–Wilk por la descripción del diseño repetido, ordinal y anidado.
- En evaluación, reemplazar Kruskal–Wallis, Dunn, Mann–Whitney y SRH como evidencia principal. Los resultados antiguos pueden omitirse o figurar como análisis exploratorio histórico, claramente subordinado.
- Actualizar todas las tablas, medianas, medias, IC, figuras de interacción y valores `n`; no conservar el texto `n = 79 observaciones por celda` en análisis con exclusiones sin desglosar el `n` efectivo.
- Sincronizar resumen, conclusiones y README solo después de cerrar los escenarios.

**Criterio de aceptación:** el notebook puede ejecutarse desde cero, produce todas las tablas/figuras con IC y efectos, y cada afirmación inferencial del manuscrito puede rastrearse a una fila de salida.

### IX.1.2 — Diagnosticar Agentic-RAG + gpt-5-nano y los datos faltantes

**Factibilidad:** alta para el diagnóstico descriptivo; la causa causal solo podrá afirmarse si los logs la demuestran.  
**Notebook:** `01`; sensibilidad estadística en `03`.

1. Clasificar las 79 salidas de esa celda y, para control, todas las demás celdas en categorías mutuamente excluyentes: `vacia`, `solo_espacios`, `abstencion_explicita`, `error_explicito`, `truncada`, `sustantiva` y `indeterminada`. Complementar la clasificación automática con revisión manual ciega de todas las no sustantivas y una muestra de sustantivas.
2. Enlazar cada salida con `law_specialist_agent.json`, `retrieval_agent.json`, todos los archivos de `retrieval_history/`, número de llamadas, consultas, documentos recuperados, tokens, motivo de finalización y excepciones disponibles. Si no hay log o excepción, marcar `indeterminada`; no reconstruir causas imaginarias.
3. Examinar `part_g/02_1_handle_missing_responses.ipynb`, cuya salida actual interpreta los faltantes como baja confiabilidad del modelo sin presentar un diagnóstico causal. Sustituir esa interpretación en el manuscrito por evidencia de logs.
4. Reportar por celda: respuestas esperadas, vacías, abstenciones, errores, truncamientos, respuestas sustantivas, evaluaciones ausentes y valores fuera de rúbrica. Incluir denominadores e IC para tasas de fallo.
5. Auditar separadamente:
   - las 28 salidas vacías/solo espacios de Agentic-RAG + nano;
   - las 27 medias ausentes por el join `vacío/None` frente a `0`;
   - las puntuaciones no nulas asignadas a algunas salidas vacías, que requieren revisión del reporte del juez.
6. Representar la distribución completa de puntuaciones por estado de salida. No inferir bimodalidad únicamente de la diferencia media–mediana.
7. Analizar descriptivamente por qué sin RAG nano supera a mini en la mediana, sin convertir el orden observado en una afirmación general sobre capacidad.
8. Repetir las comparaciones con fallo = 0 y exclusión en `03`.

**Reformulación requerida:** sustituir “identificación de la sobrecarga agéntica” por una descripción del patrón y de los modos de fallo observados. Solo si los logs muestran un mecanismo concreto —por ejemplo, agotamiento de tokens, llamadas mal formadas o truncamiento— se puede formular esa explicación como compatible con la evidencia. Incluso entonces, sin réplicas ni ablación no se debe afirmar que la “complejidad” sea la causa causal general.

**Criterio de aceptación:** cada una de las 79 unidades de la celda tiene categoría, fuente de evidencia y tratamiento en cada escenario; las sumas por celda coinciden con 79.

### IX.1.3 — Documentar parámetros de API y eliminar el determinismo

**Factibilidad:** completa para retirar el determinismo y declarar la ejecución única; parcial para reconstruir parámetros históricos no registrados.  
**Notebook:** `02_parametros_prompts_y_configuracion.ipynb`.

Crear una tabla por estrategia/componente/modelo con cuatro columnas conceptuales distintas:

1. **Solicitado en el código:** `ModelSettings(temperature=0.0)` en `part_e/02_query_llms_for_responses.ipynb`, `part_f/01_rag_llm_responses.ipynb` y `part_g/01_generate_responses_using_agents.py`/`.ipynb`.
2. **Registrado por el experimento:** `metadata.model_settings`, versión efectiva del modelo, tokens de entrada/salida y `reasoning_tokens`.
3. **Enviado tras el perfil de Pydantic AI:** verificar con el código instalado de la versión 1.1.0 y una prueba local con transporte HTTP simulado. La prueba debe capturar el cuerpo serializado sin llamar a OpenAI. El perfil instalado lista `temperature` como no admitido para los tres modelos GPT-5.
4. **Aplicado por el proveedor:** solo afirmar lo que los registros permitan. Si no existe `reasoning_effort` en la solicitud ni en la respuesta, escribir “no registrado; no recuperable retrospectivamente”. Los tokens de razonamiento demuestran consumo de razonamiento, no el nivel de esfuerzo seleccionado.

No confundir los metadatos `agent.model_settings` con una captura de la petición HTTP. Tampoco generalizar el comportamiento de los modelos generadores GPT-5 a DeepSeek, Grok o Kimi, cuya configuración debe documentarse por separado.

Cambios en Typst y README:

- Eliminar “0,0 = determinista”, “garantizar reproducibilidad”, “evita múltiples ejecuciones” y “soporte para temperatura cero” de metodología, evaluación y `performed_tasks_summary.md`.
- Sustituir la tabla de hiperparámetros por una tabla solicitado/registrado/enviado/no conocido.
- Declarar que hubo una ejecución por unidad y celda; por tanto, no puede separarse el efecto de los factores de la variabilidad entre corridas.
- Incorporar versiones snapshot observadas (`gpt-5*-2025-08-07`) y distribución de `reasoning_tokens`, sin identificar esos tokens con una configuración de esfuerzo concreta.
- Aclarar que reproducibilidad de código y datos no equivale a determinismo de las respuestas del proveedor.

**Criterio de aceptación:** ninguna afirmación de determinismo queda en manuscrito/README; el nivel de razonamiento figura como desconocido si no hay evidencia directa.


### IX.1.4 — Declarar factores confundidos, publicar prompts y resolver contradicciones

**Factibilidad:** alta; editorial y de auditoría de código/logs.  
**Notebook:** `02`.

1. Añadir en metodología una tabla de amenazas a la validez:
   - En Agentic-RAG, “modelo” identifica solo al especialista; el recuperador es siempre gpt-5.
   - Sin RAG/RAG básico y Agentic-RAG usan prompts diferentes.
   - RAG básico recupera 10 candidatos con la consulta original; el recuperador agéntico realiza hasta seis búsquedas de cinco y gpt-5 selecciona documentos.
   - Las estrategias difieren simultáneamente en descomposición, número de candidatos, selección y prompt. Sin ablación no puede atribuirse el efecto a uno de esos componentes.
2. Reproducir literalmente los prompts de sin RAG, RAG básico, especialista, recuperador, agente de calidad inactivo y ambos jueces/rúbricas. Extraerlos de notebooks y logs, calcular un hash por prompt y verificar si hubo variantes entre corridas. No reconstruirlos solo desde el manuscrito.
3. Crear preferentemente `manuscrito/capitulos/anexo_02_prompts_y_parametros.typ` e incluirlo desde `main.typ`. En el cuerpo de metodología conservar una descripción resumida y remitir al anexo para el texto completo.
4. Eliminar la afirmación de que el agente de calidad fue desactivado porque “no produjo mejoras significativas”: no hay una comparación que la sustente. Conservar únicamente las razones de costo/complejidad si el autor las confirma.
5. Sustituir “el especialista puede solicitar búsquedas adicionales” por la configuración real: una llamada del especialista a `retrieve_relevant_documents`; dentro de esa delegación, el recuperador puede realizar hasta seis búsquedas vectoriales.
6. Corregir `04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ`: el sistema no demuestra few-shot ni Chain-of-Thought explícito. Describir structured prompting, instrucción de citación y uso de herramienta; distinguir la discusión teórica de ReAct/verificación de lo efectivamente implementado.
7. Mantener `Agentic-RAG` como etiqueta si se desea, pero definirla operativamente como una implementación acotada de dos agentes, una delegación de recuperación y sin verificador activo. Evitar generalizaciones a arquitecturas iterativas o autónomas más amplias.
8. Cambiar el objetivo 2 a cumplimiento parcial respecto del diseño previsto, explicando qué componentes quedaron activos y cuáles no.

**Criterio de aceptación:** prompts, diagramas, código citado, límites y conclusiones describen la misma configuración.

### IX.1.5 — Reformular todas las conclusiones de la Tabla 4

**Factibilidad:** alta, pero debe hacerse después de los análisis que las sustentan.  
**Archivos:** `01_texto_preliminar.typ`, `02_capitulo_01_introduccion.typ`, `07_capitulo_06_evaluacion.typ`, `08_capitulo_07_trabajos_relacionados.typ`, `09_capitulo_08_conclusion_y_trabajos_futuros.typ`, `README.md` y `codigo_experimentos/README.md`.

| Conclusión observada | Acción requerida |
| --- | --- |
| “La recuperación mejora significativamente” | Formular por modelo, contraste y escenario de fallos; no usar efectos marginales para afirmar un beneficio uniforme. |
| Interacción estrategia × modelo | Mantener el patrón descriptivo y actualizar la inferencia con el modelo ordinal mixto. Interpretarla junto con la confusión de factores y el diagnóstico nano. |
| “Efecto igualador del RAG básico” | Eliminar. `p = 0,095` no demuestra equivalencia y las medianas conservan diferencias. Escribir “no se detectó evidencia suficiente de diferencias”, con IC. Si se desea equivalencia, definir antes un margen jurídicamente justificable y realizar una prueba específica; no elegir el margen después de ver los datos. |
| “Sobrecarga agéntica” | Sustituir por frecuencia y tipos de fallo observados; cualquier mecanismo causal queda condicionado a logs/réplicas. |
| “Validación de LLM-as-a-Judge” | Cambiar por “acuerdo entre jueces automáticos” o “confiabilidad inter-juez”. Sin criterio humano no hay validación de validez. |
| Objetivo 2 completamente cumplido | Cumplimiento parcial: dos agentes activos, una delegación, verificador inactivo. |
| Agentic-RAG + mini “costo-eficiente” | Reevaluar con costos absolutos, Pareto y costo por respuesta aceptable; no recomendarla por el índice con piso 0,01. |
| Resultado transferible a otros dominios | Sustituir por hipótesis de transferibilidad o potencial de adaptación que requiere validación externa. |
| Usuarios profesionales/no profesionales y repositorio | Aclarar que no hubo interfaz ni evaluación con usuarios. La accesibilidad pública ya está verificada; documentar commit y contenido de la versión final. |

Además:

- Proponer, sujeto a aprobación institucional, un título de alcance real: **“Desarrollo y evaluación de un prototipo Agentic-RAG para consulta del Código de Minería argentino”**. Actualizar `main.typ`, portada, README y bloque BibTeX. Si el título no puede cambiarse, mantener el aprobado e incorporar una declaración explícita de alcance en resumen, introducción y conclusiones.
- Reformular el objetivo general para referirse a evaluación con el benchmark, no a usuarios reales no evaluados.
- Eliminar la afirmación de “capacidad de razonamiento interna” como explicación comprobada de los resultados de gpt-5; presentarla solo como hipótesis si se conserva.
- No introducir en conclusiones resultados que no aparezcan antes en evaluación.

#### Análisis de costos asociado

Crear `07_costos_pareto.ipynb` y retirar el índice desempeño/costo normalizado con piso 0,01 como análisis principal:

1. Calcular costo total por consulta = especialista + recuperador, verificando el intercambio de `retrieval_timestamp` y `retrieval_provider_name` observado en `part_i/01_prepare_data.ipynb` antes de usar esas columnas.
2. Representar media, mediana y distribución de costos y desempeño por configuración.
3. Construir la frontera de Pareto minimizando costo y maximizando corrección, bajo los escenarios de fallos definidos.
4. Definir antes “respuesta aceptable” como `respuesta_correcta_avg ≥ 0,75`, coherente con “mayormente correcta”, y calcular costo total/número de respuestas aceptables. Reportar sensibilidad a otros umbrales sin presentar uno como universal.
5. Incluir los fallos como no aceptables en el escenario principal.
6. Crear una figura nueva `frontera_pareto_costo_calidad.pdf`; eliminar del cuerpo `eficiencia_costo.pdf` y su ranking, o trasladarlo a un apéndice de sensibilidad claramente rotulado.

### IX.1.6 — Precisar corpus/origen y revisar respuestas de referencia

**Factibilidad:** alta para linaje, conteos y extracción; revisión jurídica definitiva condicionada a un profesional.  
**Notebook:** `04_auditoria_corpus_y_benchmark.ipynb`.

#### A. Linaje y versión del corpus

1. Documentar la cadena real: PDF del Boletín Oficial de 1997 → imágenes → respuestas o4-mini en SQLite/Markdown → JSON estructurado → embeddings/Milvus. Identificar qué artefacto alimentó cada etapa mediante hashes y código.
2. Separar en el texto: fuente primaria del PDF, experimentos de Infoleg que fueron descartados y cualquier HTML usado para comparación/actualización. Corregir la introducción, que actualmente afirma que el corpus fue obtenido/actualizado desde Infoleg sin esa distinción.
3. Comparar los artículos 3 inc. c, 31, 215 y 221 con texto ordenado de 1997 y modificaciones de las Leyes 25.225 y 27.111. Extender la comparación a todo artículo marcado como modificado/derogado y a los artículos usados por el benchmark.
4. Producir una tabla derivada por artículo: versión detectada, fuente oficial, evidencia, fecha y discrepancia corpus/referencia. No modificar el corpus fuente. Si hay versiones mezcladas, declararlo y hacer sensibilidad excluyendo las unidades afectadas.
5. Unificar conteos: 482 nodos totales y 398 nodos artículo, distinguiendo cuerpo principal, apéndice, derogados y vacíos. Corregir “245 artículos” y “399 artículos”; no llamar “artículos” a los 482 fragmentos.
6. Corregir en `anexo_01.typ` la fecha de sanción tras contrastar la fuente oficial. Documentar que el metadato histórico `1994-01-01` del JSON es incompatible con la Ley 1.919 de 1886, sin alterar ese JSON.
7. Registrar el artículo 239 vacío/derogado y el uso de vectores nulos. La similitud coseno no está definida para un vector nulo; en análisis nuevos excluir documentos sin texto del universo derivado y documentar la diferencia respecto del sistema histórico.

#### B. Calidad de extracción

- Usar el PDF de 28 páginas, las respuestas almacenadas y el Markdown resultante para medir completitud y diferencias de texto, cifras, plazos, remisiones y límites de artículos.
- Preferiblemente revisar el censo de 398 artículos con comprobaciones automáticas y una revisión humana estratificada. Si solo es viable una muestra, calcular y justificar su tamaño, semilla y estratos por longitud/título; incluir todos los artículos modificados y todos los relevantes para el benchmark.
- Reportar número revisado, porcentaje del corpus, errores por tipo y tasa con IC. No escribir simplemente “inspección manual de una muestra”.

#### C. Benchmark y respuestas observadas

- Comparar los JSON por título de `part_a/data/generated_questions/` con el benchmark revisado para cuantificar cambios observables. No atribuir todas las diferencias al revisor humano si la procedencia no permite distinguirlas.
- Documentar modelo generador, fecha, revisor, criterios, número de preguntas/respuestas modificadas y segunda revisión solo si hay evidencia o confirmación del profesional.
- La fuente actual de la subpregunta 1.2 ya fundamenta la separación de propiedad en el artículo 11; el anexo Typst, en cambio, dice artículo 8. Corregir `anexo_01.typ` para eliminar esa inconsistencia.
- Someter 1.3 y cualquier otra referencia cuestionada a revisión jurídica. En particular, no reducir el artículo 17 a “seguridad o ambiente” ni usar “solo” sin sustento. Si no se obtiene revisión, marcar la unidad como controvertida en el análisis derivado, realizar sensibilidad con/sin ella y atenuar la afirmación de validación del benchmark.
- Aclarar que una única revisión profesional y el acuerdo entre jueces no demuestran validez de contenido.

**Criterio de aceptación:** origen, versión, número de artículos y referencia usada son coherentes en introducción, metodología, anexo y análisis; toda discrepancia no resuelta queda explícita y tiene análisis de sensibilidad.

### IX.1.7 — Corregir Tablas 2 y 3 y auditar toda la bibliografía

**Factibilidad:** alta; requiere verificación fuente por fuente. No se deben generar entradas BibTeX de memoria.  
**Notebook:** `10_auditoria_bibliografica.ipynb`.

#### A. Errores de la Tabla 2

| Ubicación actual | Corrección propuesta |
| --- | --- |
| `02_capitulo_01_introduccion.typ`, oración “Al combinar…” | Unirla a una proposición completa con la oración siguiente. |
| `03_capitulo_02_fundamentos_e_historia_pln.typ`, n-gramas | Definir n-gramas como secuencias de `n` unidades y especificar que el ejemplo usa palabras; distinguir n-gramas de caracteres. |
| mismo archivo, atención | Sustituir “similitud coseno escalada” por producto escalar escalado por `1/sqrt(d_k)`; la fórmula ya presente es la correcta. |
| mismo archivo, GPT-4/MoE | Eliminar la atribución arquitectónica si no existe fuente primaria que la confirme. |
| `04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ`, LEGAL-BERT | Separar Chalkidis et al. (2020), Zheng et al. (2021), Case Law Access Project y LegalBench (2023); eliminar la evaluación anacrónica en “todas las tareas de LegalBench”. Verificar cada afirmación en los artículos primarios. |
| mismo archivo, “245 artículos” | Sustituir por el conteo verificado o reformular como “un artículo inexistente en el corpus”. |
| `08_capitulo_07_trabajos_relacionados.typ`, desarrollos posteriores | Corregir DeepSeek-R1 a enero de 2025; verificar Llama 4 y Qwen3 en fuentes oficiales —la valoración indica abril de 2025—; unificar Gemini 3 Pro al 18 de noviembre si la fuente lo confirma. Reducir o retirar la sección según IX.2.5. |
| `anexo_01.typ`, fecha de sanción | Usar la fecha oficial de la Ley 1.919 y documentar la discrepancia del metadato fuente. |
| Referencias cruzadas | Eliminar sustantivos manuales redundantes antes de referencias a secciones (`capítulo @sec...`, `sección @sec...`) o remitir al capítulo correcto. La duplicación se genera al componer el texto manual con el suplemento automático de Typst. |
| Nota sobre sistemas expertos/Wikipedia | Reemplazar por una fuente académica/primaria verificada; si no se encuentra, eliminar el detalle histórico. |
| `01_texto_preliminar.typ`, dedicatoria | Completarla o eliminar “A mi familia …”. |
| declaración de IA | Ampliarla como se detalla en IX.1.8. |

#### B. Problemas de la Tabla 3

1. Reemplazar `bommasani2022gender` por la entrada verificada de Bozdag, Sevim y Koç para DOI `10.1145/3628602`, con autores, año y revista correctos. Actualizar las dos citas y releer el artículo: no atribuirle adapters si el método es ajuste fino ni afirmaciones no presentes.
2. En la afirmación sobre Westlaw/Lexis de `08_capitulo_07_trabajos_relacionados.typ`, citar el estudio correcto de Magesh et al. (2025), DOI `10.1111/jels.12413`. Conservar Dahl et al. (2024) únicamente para su propio artículo si se utiliza.
3. Verificar que las obras de Wei 2022 y Zhao 2026 se distingan también en la salida APA, no solo mediante claves BibTeX diferentes. Aplicar letras de año cuando corresponda según autoría y APA.
4. Eliminar la duplicación de DeepSeek-R1: usar la entrada 2025 existente y corregir la entrada/cita fechada en 2026.
5. Corregir la fecha de Llama 4 con la fuente oficial y eliminar la atribución 2026.
6. Unificar LEXTREME con el año de Findings of EMNLP 2023 y su DOI; si se renombra la clave, actualizar sus cinco usos.
7. Para Tribunal Fiscal de la Nación, citar el sitio oficial para el sistema o el autor real de la nota para el anuncio; no combinar autor institucional con URL de un estudio jurídico como si fuera la misma fuente.
8. Incorporar mediante metadatos verificados Lewis et al. (2020) para RAG y una referencia oficial al Código de Minería/Decreto 456/1997.
9. Preferir versiones revisadas por pares de BERT, LoRA, QLoRA y Self-RAG cuando existan, sin borrar arXiv si es la única versión pertinente.
10. Uniformar “y col.”, fechas de publicación frente a fechas de consulta y estilo APA. Revisar las reglas `show` de `main.typ`, que actualmente introducen variantes “y col.”/“y cols.”.

#### C. Auditoría completa

`10_auditoria_bibliografica.ipynb` debe:

- Parsear `referencias.bib`, enumerar sus 238 entradas y extraer todas las citas de los `.typ`.
- Detectar claves inexistentes, entradas no citadas, duplicados y pares autor–año ambiguos.
- Resolver DOI mediante Crossref/DOI y comprobar título, autores, año, venue y tipo; guardar fecha y respuesta de verificación.
- Comprobar URL y distinguir fuente primaria, preprint, blog comercial y versión revisada.
- Producir una tabla `clave, cita_en, identificador, estado, discrepancia, fuente_verificacion, accion` sin reescritura automática del `.bib`.
- Mantener una lista explícita de afirmaciones que requieren lectura del texto completo; una coincidencia de metadatos no valida la afirmación citada.

**Criterio de aceptación:** cada entrada citada tiene identificador/URL verificado o una limitación documentada, y cada corrección de fondo fue contrastada con la fuente primaria.

### IX.1.8 — Acceso público, reproducibilidad y declaración de IA

**Estado:** accesibilidad ya verificada; restan documentación y prueba final.  
**Archivos:** `README.md`, `codigo_experimentos/README.md`, `01_texto_preliminar.typ`, `anexo_01.typ` y `performed_tasks_summary.md`.

#### A. Repositorio y README

En el README raíz:

- Actualizar hallazgos solo después de `01`, `03` y `07`; eliminar mientras tanto las formulaciones de igualador, sobrecarga causal y “LLM-as-a-Judge validado”.
- Cambiar “validadas por profesionales” por la revisión efectivamente documentada —actualmente un profesional—.
- Corregir `part_h1/` a `part_h_1/`; el costo está en `part_j/05_analisis_costos.ipynb`, no en un `part_k` existente. Documentar el nuevo `part_k_correcciones_jurado` cuando se cree.
- Corregir el requisito de Python: el badge dice 3.12+, pero `codigo_experimentos/pyproject.toml` exige 3.13+.
- Sustituir la lista estadística antigua por el análisis ordinal mixto, pruebas apareadas, efectos e IC.
- Explicar que la interacción con APIs no es determinista y que los resultados originales tienen una ejecución por celda.
- Describir datos, logs, jueces, licencia, versión del corpus, limitaciones y alcance de un único Código.
- Añadir instrucciones de ejecución limpia, orden de notebooks, entradas/salidas y advertencia de que los notebooks históricos pueden sobrescribir archivos.

En `codigo_experimentos/README.md` y `performed_tasks_summary.md`:

- Documentar el pipeline real y las nuevas correcciones; eliminar “deterministic responses” e “iterative retrieval” si se refiere a iteración del especialista.
- Corregir la afirmación de metodología de que cada directorio tiene README: actualmente solo `part_b` lo tiene. Crear documentación por directorio o, preferiblemente, centralizar una tabla completa en el README de experimentos.
- Incluir rutas relativas portables; hay salidas de notebooks con rutas absolutas históricas que no deben usarse como documentación de ejecución.

En `anexo_01.typ`, sustituir el árbol obsoleto `examples/notebooks/` por la estructura actual `codigo_experimentos/`, `manuscrito/` y `data/`, y actualizar la descripción de componentes.

#### B. Verificación pública final

1. Publicar todos los cambios y registrar el commit/release definitivo en README y anexo.
2. Desde un entorno sin credenciales, clonar por HTTPS, comprobar presencia de benchmark, corpus, logs, salidas de jueces, `uv.lock` y notebooks nuevos.
3. Ejecutar `00_integridad_y_procedencia.ipynb` y compilar el manuscrito desde esa clonación.
4. Comprobar que no se publican `.env`, credenciales, tokens ni datos privados. `.env` está ignorado y no apareció como archivo rastreado en la inspección.
5. No afirmar que el objetivo de replicación está cumplido solo porque la página carga: exigir compilación y ejecución del análisis base.

#### C. Declaración ampliada de IA

En `01_texto_preliminar.typ`, describir de forma veraz y específica:

- extracción del PDF con o4-mini;
- generación de preguntas y respuestas de referencia con GPT-4.1 y revisión humana;
- generación de respuestas con la familia GPT-5;
- evaluación con DeepSeek, Grok y Kimi;
- asistencia de IA en redacción, traducción, programación o análisis estadístico, según lo efectivamente ocurrido;
- procedimientos de verificación humana y responsabilidad del autor sobre el resultado.

**Criterio de aceptación:** una clonación anónima del commit final permite compilar y reproducir el análisis descriptivo; la declaración cubre todas las etapas asistidas por IA.

## 4. Recomendaciones de IX.2

### IX.2.1 — Evaluar recuperación aislada y comparar recuperadores

**Factibilidad:** alta sin nuevas llamadas a LLM; requiere cómputo local y descarga de modelos.  
**Notebook:** `05_evaluacion_aislada_recuperacion.ipynb`.

1. Construir juicios de relevancia desde `contexto_para_respuesta`, pero no identificar documentos solo por número: el apéndice contiene números repetidos. Resolver `id_parte`, norma y jerarquía; revisar manualmente los casos ambiguos.
2. Auditar `part_d`: su código toma la primera coincidencia por `numero_parte` y busca con `limit=5000`. El hecho de que las 166 referencias tengan rango no implica recuperación útil a `k` pequeño.
3. Recalcular desde el resultado histórico, sin Milvus si es posible: Recall@k, Hit@k, Precision@k, MRR y nDCG@k para `k ∈ {1,3,5,10}`, con macro-promedio por unidad e IC bootstrap por casos.
4. Evaluar por separado:
   - RAG básico: ranking de la consulta original.
   - Agentic-RAG candidatos: unión de todos `retrieval_history`.
   - Agentic-RAG seleccionados: documentos efectivamente devueltos por el recuperador al especialista, extraídos del mensaje final.
   Reportar número de candidatos/seleccionados y no comparar como si todos tuvieran el mismo `k`.
5. Comparar sobre un corpus derivado idéntico y sin textos vacíos:
   - embedding actual `hiiamsid/sentence_similarity_spanish_es`;
   - al menos un modelo entrenado para recuperación multilingüe, por ejemplo `BAAI/bge-m3`, fijando revisión, instrucciones de consulta y longitud máxima según su tarjeta;
   - BM25 como línea léxica;
   - opcionalmente fusión BM25+densa con RRF.
6. Usar búsqueda exacta por fuerza bruta para las 482 unidades —o el subconjunto documentado— y separar ese resultado del sistema histórico aproximado. Consultar `describe_index` en modo lectura si Milvus está disponible para resolver AUTOINDEX/IVF_FLAT y sus parámetros; si no, informar lo que el código prueba y lo que no puede verificarse.
7. Medir truncamiento real por artículo y modelo. Eliminar del texto la afirmación no demostrada de que un modelo solo en español evita pérdidas de matices; sustituirla por una decisión empírica basada en esta comparación.
8. Auditar caracteres de control observados en algunas consultas de `retrieval_history`. Preferir las consultas originales de los tool calls cuando estén disponibles, marcar discrepancias y nunca corregir el log fuente.
9. Reportar resultados por caso, unidad y número de artículos relevantes; analizar fallos de recuperación junto con fallos de respuesta de `01`.

Actualizar metodología/evaluación con una subsección propia y las siglas MRR/NDCG, que actualmente figuran sin uso analítico. No afirmar que una mejor recuperación causa mejor respuesta sin un análisis que relacione ambos niveles.

### IX.2.2 — Medir citas de artículos de forma determinista

**Factibilidad:** alta con respuestas existentes.  
**Notebook:** `06_evaluacion_determinista_citaciones.ipynb`.

1. Extraer menciones `artículo`, `art.`, `arts.`, ordinales, incisos, rangos y expresiones como “y siguientes”, conservando span y texto original.
2. Distinguir Código de Minería, otras normas, artículo inexistente, artículo existente pero no relevante y mención ambigua/no parseable.
3. Expandir rangos solo con reglas explícitas. No expandir silenciosamente “y ss.” ni convertir números repetidos del apéndice en citas correctas.
4. Para cada respuesta calcular:
   - TP: artículos relevantes citados;
   - FP: artículos del Código citados no incluidos en la referencia;
   - FN: artículos relevantes omitidos;
   - precisión = TP/(TP+FP), exhaustividad = TP/(TP+FN) y F1, con convenciones para denominador cero;
   - cantidad/tasa de artículos inexistentes, citas externas y spans no parseados.
5. Validar el parser con una muestra manual estratificada que incluya rangos, incisos, múltiples normas, errores y respuestas vacías. Reportar precisión del extractor y casos no resueltos.
6. Comparar configuraciones con descriptivos e IC bootstrap por casos; integrar el análisis apareado si se hacen pruebas.
7. Presentar estas métricas como evaluación de citación, no como sustituto de la corrección jurídica de la interpretación.

Esto permite retirar `score_precision_legal` como única evidencia de citación y abordar directamente un riesgo central del dominio.

### IX.2.3 — Validar una submuestra con profesionales

**Factibilidad:** condicionada a disponibilidad de uno o dos profesionales. Si no se realiza, la limitación y la eliminación de “validado” permanecen.  
**Notebook:** `08_validacion_humana_jueces.ipynb`.

1. Seleccionar con semilla fija una muestra de aproximadamente 90 respuestas, 10 por celda, estratificada por configuración y nivel de puntuación. Si se enriquece con casos discordantes o con nano agéntico, mantener ese subconjunto separado o usar pesos para no sesgar la estimación.
2. Presentar respuestas en orden aleatorio, sin modelo, estrategia ni puntuación de jueces. Entregar pregunta, respuesta esperada y texto legal pertinente.
3. Usar la misma rúbrica ordinal de corrección para comparar con los jueces; una rúbrica separada de citas puede añadirse como análisis secundario.
4. Idealmente, dos profesionales evaluarán toda la muestra; con uno, declarar que no puede estimarse acuerdo humano–humano.
5. Medir alfa ordinal de Krippendorff, kappa ponderado, Spearman, MAE, matriz de confusión y diferencias de severidad por juez. Calcular IC bootstrap por caso.
6. Analizar si el acuerdo varía por estrategia, modelo, longitud y respuestas vacías; evitar concluir validez universal desde una submuestra.
7. Guardar las nuevas anotaciones como datos nuevos, nunca dentro de los reportes originales.

Actualizar la contribución solo si los resultados respaldan concordancia con criterio humano; en caso contrario, reportar la discrepancia como hallazgo de medición.

### IX.2.4 — Réplicas y ablación con el mismo modelo en ambos agentes

**Factibilidad:** condicionada a presupuesto, APIs y disponibilidad de snapshots.  
**Notebook:** `09_replicas_y_ablacion.ipynb`.

1. Antes de ejecutar, estimar costo por celda a partir de los metadatos existentes: `costo_medio_celda × 79 × réplicas`, más evaluación de jueces. Obtener aprobación explícita del presupuesto.
2. Priorizar tres réplicas; cinco si el presupuesto lo permite. Como mínimo incluir las celdas necesarias para las comparaciones marginales de gpt-5, el fallo de nano y el beneficio observado en mini. La opción metodológicamente más limpia es replicar las nueve celdas completas.
3. Fijar antes del experimento prompts, corpus, modelos snapshot, esfuerzo de razonamiento admitido, límites, semillas cuando existan y plan estadístico. Omitir temperatura si el modelo no la admite; no confundirla con esfuerzo de razonamiento.
4. Capturar el payload efectivamente enviado —sin claves—, respuesta, `finish_reason`, uso y errores en archivos nuevos. Repetir también la evaluación con jueces bajo un protocolo congelado.
5. Ablación mínima: para cada modelo del especialista, usar ese mismo modelo en el recuperador y comparar con la configuración original cuyo recuperador es gpt-5.
6. Declarar que esta ablación controla la mezcla de modelos, pero no elimina las diferencias de prompt, descomposición, candidatos o selección. No atribuir el efecto restante a “agencia” sin ablaciones adicionales.
7. Incorporar réplica como factor/efecto aleatorio según el diseño, estimar variabilidad entre corridas y actualizar los IC. No tratar réplicas como nuevas preguntas independientes.
8. Guardar todo en un directorio nuevo con un manifiesto; no completar ni sobrescribir `part_g/chat_data`.

Si no se ejecuta, el manuscrito debe conservar la ejecución única como limitación y evitar cualquier afirmación de estabilidad entre corridas.

### IX.2.5 — Reducir capítulo 2 y sección 7.7

**Factibilidad:** alta; tarea editorial.

- En `03_capitulo_02_fundamentos_e_historia_pln.typ`, conservar los conceptos usados después: n-gramas, embeddings, Transformer, LLM y limitaciones vinculadas al sistema. Reducir la cronología año por año y trasladar detalles de perceptrón/RNN/LSTM/GRU a un anexo solo si son necesarios.
- En `08_capitulo_07_trabajos_relacionados.typ`, retirar del cuerpo “Desarrollos Posteriores al Período Experimental” o reducirla a un párrafo de alcance temporal con fuentes primarias verificadas. Las afirmaciones comerciales de 2026 sobre modelos no son evidencia de los resultados de 2025.
- Eliminar de esa sección explicaciones especulativas de “sobrecarga agéntica” y cualquier afirmación de superioridad no verificada.
- No crear un anexo con material incorrecto: todo lo trasladado debe pasar la misma auditoría bibliográfica.
- Revisar después el índice, referencias cruzadas, siglas y estructura descrita en la introducción.

## 5. Secuencia de trabajo recomendada

### Fase 1 — Recuperar una base analítica válida

1. Crear `00` y congelar manifiesto/hashes.
2. Resolver en el dataset derivado el join vacío/None/0 y conciliar las 2.133 evaluaciones.
3. Ejecutar `01` para separar fallos de generación, evaluación y procesamiento.
4. Ejecutar `02` para cerrar parámetros, prompts y configuración.

**Bloqueo:** no reinterpretar resultados hasta terminar esta fase.

### Fase 2 — Rehacer evidencia central

1. Ejecutar `03` con escenarios predefinidos, efectos e IC.
2. Ejecutar `07` para Pareto/costo por respuesta aceptable.
3. Ejecutar `04` para corpus y referencias; incorporar unidades controvertidas a la sensibilidad de `03`.
4. Reescribir resultados, resumen, conclusiones y contribuciones con la evidencia nueva.

### Fase 3 — Correcciones editoriales y abiertas

1. Ejecutar `10` y corregir `referencias.bib` y citas con fuentes verificadas.
2. Corregir Tabla 2, prompts, arquitectura, título/alcance y estructura del anexo.
3. Actualizar READMEs y declaración de IA.
4. Publicar y probar clonación anónima.

### Fase 4 — Mejoras recomendadas, en orden de valor/costo

1. `06` citas deterministas: bajo costo y alto valor para el dominio.
2. `05` recuperación aislada: sin LLM, alto valor metodológico.
3. `08` validación humana: alto valor, depende de profesionales.
4. `09` réplicas/ablación: mayor costo; ejecutar solo con protocolo y presupuesto aprobados.

Si el tiempo es limitado, las correcciones requeridas tienen prioridad absoluta. Las recomendaciones no deben retrasar la corrección del análisis apareado, el diagnóstico de fallos y la moderación de conclusiones.

## 6. Matriz de trazabilidad y definición de terminado

| Punto | Estado de resolución posible | Evidencia/artefacto que debe existir |
| --- | --- | --- |
| IX.1.1 inferencia | Resoluble con datos existentes | `03`, tabla de efectos/IC, sensibilidad y capítulos actualizados |
| IX.1.2 celda anómala | Diagnóstico resoluble; causa condicionada a logs | `01`, clasificación completa y faltantes por celda |
| IX.1.3 parámetros | Parcialmente reconstruible; esfuerzo histórico puede quedar desconocido | `02`, payload simulado, tabla solicitado/registrado/enviado |
| IX.1.4 confusiones/prompts | Resoluble | Anexo de prompts, tabla de amenazas y contradicciones eliminadas |
| IX.1.5 conclusiones | Resoluble tras análisis | Tabla 4 reformulada en resumen/resultados/conclusiones/README |
| IX.1.6 corpus/referencias | Linaje resoluble; juicio jurídico requiere experto | `04`, versiones por artículo, calidad de extracción y sensibilidad |
| IX.1.7 forma/bibliografía | Resoluble con auditoría | `10`, inventario de 238 entradas y verificación documentada |
| IX.1.8 acceso/IA | Acceso ya verificado; reproducción final pendiente | Clonación anónima, README actualizado y declaración ampliada |
| IX.2.1 recuperación | Resoluble sin nuevos LLM | `05`, métricas por `k`, BM25 y alternativa densa |
| IX.2.2 citas | Resoluble sin nuevos LLM | `06`, métricas y validación del parser |
| IX.2.3 humanos | Condicionada a profesionales | `08`, anotaciones nuevas y acuerdo humano–LLM |
| IX.2.4 réplicas/ablación | Condicionada a API/presupuesto | `09`, nuevos logs y análisis por réplica |
| IX.2.5 reducción | Resoluble editorialmente | Capítulos revisados y bibliografía de lo retenido verificada |

### Comprobaciones finales obligatorias

1. Ejecutar todos los notebooks nuevos desde un entorno limpio, sin escrituras fuera de `part_k_correcciones_jurado/salidas/` ni de los directorios de nuevos experimentos.
2. Verificar que los hashes de todas las fuentes y logs son idénticos antes y después del análisis.
3. Regenerar figuras con una paleta apta para daltonismo y epígrafes autocontenidos; no conservar intervalos calculados como si las 711 filas fueran independientes.
4. Compilar con `make pdf` y revisar el PDF textual y visualmente.
5. Buscar en el PDF final restos de las afirmaciones antiguas: “efecto igualador”, “sobrecarga agéntica”, “validación de LLM-as-a-Judge”, “temperatura 0” asociada a determinismo, “transferible”, `n = 79` en análisis con exclusiones y fechas/controles incorrectos.
6. Comprobar referencias cruzadas duplicadas, citas no resueltas, tablas desbordadas y consistencia entre resumen, cuerpo, anexos y README.
7. Preparar posteriormente una `respuesta_al_jurado.md` que cite, para cada punto, la acción realizada, el notebook/artefacto y la página definitiva correspondiente.

## 7. Decisión práctica mínima para la versión definitiva

Si solo se dispone de tiempo para las correcciones obligatorias, el paquete mínimo coherente es:

- corregir el join y reconstruir la base de 711 observaciones;
- diagnosticar las 28 salidas vacías de nano agéntico sin confundirlas con los 27 valores ausentes;
- rehacer la inferencia con modelo ordinal mixto y análisis apareado/anidado, efectos e IC;
- documentar lo conocido y lo desconocido de los parámetros de API;
- publicar prompts y declarar confusión de factores;
- moderar todas las conclusiones y eliminar equivalencia/validación/causalidad no demostradas;
- auditar corpus, referencias, Tablas 2–3 y documentación;
- mantener explícitas las limitaciones de una ejecución, ausencia de validación humana y ausencia de ablación.

Las nuevas réplicas no son imprescindibles para reconocer esas limitaciones, pero **ninguna redacción debe convertir su ausencia en evidencia de determinismo, equivalencia, validez humana o causalidad**.

# Informe técnico — IX.1.3

**Punto:** documentar los parámetros de API y eliminar la afirmación de determinismo.  
**Fecha de generación:** 2026-11-12.  
**Alcance:** modelos generadores GPT-5 usados en las nueve configuraciones; los jueces se documentan por separado.  
**Regla:** no se modificó ningún archivo fuente, log, respuesta, reporte de juez ni capítulo del manuscrito.

## 1. Conclusión

La temperatura cero **fue solicitada en el código, pero no fue enviada a la API** de los modelos GPT-5. Pydantic AI 1.1.0, versión fijada en `codigo_experimentos/uv.lock`, declara `temperature` como parámetro no admitido para `gpt-5-nano`, `gpt-5-mini` y `gpt-5`; antes de construir la petición, elimina ese y otros parámetros de muestreo. La captura local del cuerpo Chat Completions confirma que `temperature` no aparece en ninguno de los 12 casos capturados.

En consecuencia:

- No corresponde afirmar que las respuestas son deterministas.
- No corresponde usar la temperatura como justificación de una única ejecución.
- No se registró un nivel de esfuerzo de razonamiento. Los `reasoning_tokens` existen en las 711 respuestas primarias, pero no permiten reconstruir el esfuerzo solicitado ni el aplicado por el proveedor.
- La ejecución única debe declararse como limitación.
- Los registros de los agentes **no son volcados HTTP**. Los de sin RAG y RAG básico conservan `temperature=0.0`; los de Agentic-RAG guardan `{}`. Esa diferencia impide tratar el campo `model_settings` del log como prueba de lo enviado.

## 2. Método y evidencia

### 2.1 Entradas y salvaguardas

Se calcularon hashes SHA-256 de 1.880 archivos de entrada antes de generar las tablas:

- 1.838 JSON de `codigo_experimentos/part_g/chat_data/`;
- 27 reportes de `codigo_experimentos/part_h_1/reports/`;
- 15 archivos de código, datos, manuscrito y documentación.

El manifiesto está en `salidas/manifiesto_entradas.csv`; el resumen y el hash del conjunto están en `salidas/manifiesto_resumen.json`. Los archivos fuente no se abren en modo escritura en ningún paso.

### 2.2 Configuración solicitada en el código

| Estrategia | Archivo | Configuración solicitada |
| --- | --- | --- |
| Sin RAG | `codigo_experimentos/part_e/02_query_llms_for_responses.ipynb` | `ModelSettings(temperature=0.0)` |
| RAG básico | `codigo_experimentos/part_f/01_rag_llm_responses.ipynb` | `ModelSettings(temperature=0.0)` |
| Agentic-RAG, especialista | `codigo_experimentos/part_g/01_generate_responses_using_agents.py` y `.ipynb` | `ModelSettings(temperature=0.0)` |
| Agentic-RAG, recuperador | mismo archivo | `ModelSettings(temperature=0.0)` |
| Jueces | `part_h_1/01_llm_as_a_judge.ipynb` y `..._batch_2.ipynb` | `temperature=0.0`, `max_tokens=5000` |

La solicitud no incluye `reasoning_effort`, `openai_reasoning_effort`, `seed`, `top_p` ni `max_tokens` para los generadores. Los jueces tienen un límite de salida explícito de 5.000 tokens; los generadores no.

### 2.3 Comportamiento de Pydantic AI 1.1.0

Los perfiles de los tres modelos contienen:

```text
temperature
top_p
presence_penalty
frequency_penalty
logit_bias
logprobs
top_logprobs
```

El código fuente de `OpenAIChatModel._completions_create` ejecuta:

```python
unsupported_model_settings = OpenAIModelProfile.from_profile(self.profile).openai_unsupported_model_settings
for setting in unsupported_model_settings:
    model_settings.pop(setting, None)
```

antes de llamar a `client.chat.completions.create(...)`. La evidencia completa está en `salidas/evidencia_perfil_pydantic.json` y `salidas/evidencia_pydantic_ai_excerpt.txt`.

### 2.4 Captura local del payload

Se usó `httpx.MockTransport` con una respuesta Chat Completions local. No hubo llamadas a OpenAI ni a ningún proveedor. Se usó la misma clase `OpenAIChatModel` y el mismo `openai_model_profile` que resuelve `pydantic_ai.infer_model("openai:gpt-5")` en la versión fijada.

Resultados de los 12 cuerpos capturados:

| Estrategia / componente | Claves del cuerpo | `temperature` | `reasoning_effort` | `max_completion_tokens` |
| --- | --- | --- | --- | --- |
| Sin RAG / especialista, 3 modelos | `messages`, `model`, `stream` | Ausente | Ausente | Ausente |
| RAG básico / especialista, 3 modelos | `messages`, `model`, `stream` | Ausente | Ausente | Ausente |
| Agentic-RAG / especialista, 3 modelos | `messages`, `model`, `stream`, `tool_choice`, `tools` | Ausente | Ausente | Ausente |
| Agentic-RAG / recuperador, gpt-5 | `messages`, `model`, `stream`, `tool_choice`, `tools` | Ausente | Ausente | Ausente |

El cuerpo capturado para sin RAG es, en lo que respecta a parámetros:

```json
{
  "messages": ["..."],
  "model": "gpt-5-nano",
  "stream": false
}
```

Los cuerpos completos, con los mensajes de prueba, están en `salidas/evidencia_payloads_locales.json`. La captura local conserva `temperature` en `agent.model_settings` después de `run`; los logs históricos Agentic-RAG lo muestran vacío. Esto refuerza que el log no debe interpretarse como el cuerpo HTTP: la diferencia de instrumentación no puede resolverse con los artefactos disponibles.

### 2.5 Lo registrado en los artefactos históricos

En `part_i/metadata_tokens_cost_cleaned.csv` y en `part_h/llm_responses_all_results_with_metrics_FINAL.json`:

- Sin RAG: 237 respuestas (3 modelos × 79), todas con `{"temperature": 0.0}` registrado.
- RAG básico: 237 respuestas, todas con `{"temperature": 0.0}` registrado.
- Agentic-RAG: 237 respuestas, todas con `{}` en el especialista y `{}` en el recuperador.
- Versiones efectivas observadas: `gpt-5-nano-2025-08-07`, `gpt-5-mini-2025-08-07` y `gpt-5-2025-08-07`; recuperador `gpt-5-2025-08-07`.
- Las 711 respuestas primarias tienen `reasoning_tokens` no nulo.
- Las 237 respuestas del recuperador también tienen `reasoning_tokens` no nulo.

La tabla `salidas/tabla_configuracion_solicitado_registrado_efectivo.csv` conserva las tres capas: solicitado, registrado y perfil de la biblioteca. No llama “enviado” a ninguno de los dos primeros.

### 2.6 Esfuerzo de razonamiento

La búsqueda de `reasoning_effort` y `openai_reasoning_effort` en 1.873 archivos —código de generación, respuestas primarias, reportes de jueces y todos los logs de `part_g/chat_data/`— devolvió **0 ocurrencias**. La búsqueda de `reasoning=` solo encontró una aparición en `part_a/part_A_3_generate_questions.ipynb`, correspondiente a la generación del benchmark con GPT-4.1, no a los modelos evaluados. El detalle está en `salidas/evidencia_reasoning_effort.json`.

Los tokens de razonamiento sí están registrados:

| Estrategia | Componente | Modelo | Mediana | Mín. | Máx. | Proporción mediana sobre tokens de salida |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Sin RAG | especialista | gpt-5-nano | 5.376 | 2.432 | 8.512 | 0,910 |
| Sin RAG | especialista | gpt-5-mini | 1.408 | 704 | 2.944 | 0,758 |
| Sin RAG | especialista | gpt-5 | 4.096 | 2.048 | 6.016 | 0,886 |
| RAG básico | especialista | gpt-5-nano | 4.864 | 1.344 | 10.816 | 0,898 |
| RAG básico | especialista | gpt-5-mini | 1.536 | 640 | 3.648 | 0,699 |
| RAG básico | especialista | gpt-5 | 3.072 | 768 | 5.888 | 0,882 |
| Agentic-RAG | especialista | gpt-5-nano | 3.456 | 512 | 8.448 | 0,914 |
| Agentic-RAG | especialista | gpt-5-mini | 1.344 | 448 | 3.392 | 0,609 |
| Agentic-RAG | especialista | gpt-5 | 3.072 | 960 | 5.696 | 0,841 |
| Agentic-RAG | recuperador | gpt-5 | 4.608 | 1.536 | 10.816 | 0,782 |
| Agentic-RAG | recuperador | gpt-5 | 4.800 | 2.304 | 9.600 | 0,737 |
| Agentic-RAG | recuperador | gpt-5 | 3.968 | 1.600 | 10.944 | 0,689 |

Las tres filas del recuperador corresponden a las tres configuraciones de especialista (nano, mini y gpt-5); el recuperador siempre es gpt-5. La tabla completa está en `salidas/tabla_reasoning_tokens_por_celda.csv`, y la figura en `salidas/fig_tokens_razonamiento_por_celda.png`/`.pdf`.

**Interpretación correcta:** estos valores muestran que los modelos consumieron tokens de razonamiento y que esa proporción es alta. No muestran qué nivel de esfuerzo se solicitó, porque el parámetro no aparece en el código ni en los logs. Tampoco permiten afirmar que el proveedor usó un nivel “alto” o “bajo” concreto.

### 2.7 Ejecución única

La tabla `salidas/tabla_ejecuciones_unicas.csv` muestra, para cada una de las 9 celdas:

- 79 registros;
- 79 unidades únicas;
- 25 casos únicos;
- 0 duplicados de unidad;
- 79 timestamps únicos del especialista;
- 79 timestamps únicos del recuperador en Agentic-RAG;
- ningún campo `run_id`, `replica` o equivalente;
- 28 respuestas en blanco únicamente en Agentic-RAG + gpt-5-nano (las demás celdas, 0).

Los timestamps prueban ejecuciones distintas por unidad, no repeticiones de la misma unidad. No hay evidencia de réplicas. Esta es una limitación que el análisis estadístico no puede resolver: solo nuevas ejecuciones podrían estimar la variabilidad entre corridas.

### 2.8 Jueces

Los reportes de `part_h_1/reports/` contienen 9 reportes por juez y 711 evaluaciones por juez:

| Juez | Reportes | Evaluaciones | Settings registrados |
| --- | ---: | ---: | --- |
| DeepSeek V3.1 | 9 | 711 | `temperature=0.0`, `max_tokens=5000` |
| Kimi K2 0905 | 9 | 711 | `temperature=0.0`, `max_tokens=5000` |
| Grok 4.1 Fast | 9 | 711 | `temperature=0.0`, `max_tokens=5000` |

Estos modelos se ejecutaron vía OpenRouter y no son los modelos generadores GPT-5. Su configuración no se usó para afirmar determinismo de las respuestas evaluadas. No se capturó su payload en este artefacto; por tanto, la tabla registra la configuración declarada, no una verificación HTTP.

## 3. Consecuencias para el manuscrito

### 3.1 Afirmaciones que deben retirarse o reemplazarse

| Archivo | Línea | Problema |
| --- | ---: | --- |
| `06_capitulo_05_metodologia.typ` | 196 | “Pydantic AI con temperatura 0” como configuración efectiva. |
| `06_capitulo_05_metodologia.typ` | 461 | “0,0 = determinista”. |
| `06_capitulo_05_metodologia.typ` | 471 | Tabla de hiperparámetros con temperatura 0,0. |
| `06_capitulo_05_metodologia.typ` | 495 | Criterio de selección “temperatura cero”. |
| `06_capitulo_05_metodologia.typ` | 505 | “Todos los modelos fueron configurados con temperatura 0”. |
| `06_capitulo_05_metodologia.typ` | 598 | Configuración de los jueces mezclada con la de los generadores. |
| `06_capitulo_05_metodologia.typ` | 644 | “Temperatura 0 ... evita múltiples ejecuciones”. |
| `07_capitulo_06_evaluacion.typ` | 16 | “Temperatura 0 ... para garantizar reproducibilidad”. |
| `09_capitulo_08_conclusion_y_trabajos_futuros.typ` | 87 | Falta declarar la ejecución única y la ausencia de control efectivo de muestreo. |
| `performed_tasks_summary.md` | 66 | “temperature=0 for deterministic responses”. |
| `06_capitulo_05_metodologia.typ` | 8 y 739 | “reproducibilidad” sin distinguir pipeline de respuestas (recomendado). |
| `README.md` | 140 | Falta una nota de ejecución única y no determinismo (inserción). |

### 3.2 Redacción mínima sugerida

En metodología:

> El código solicitó `temperature=0.0`, pero Pydantic AI 1.1.0 elimina ese parámetro para los modelos GPT-5 antes de construir la solicitud. Por tanto, la temperatura no fue un control efectivo y las respuestas no se consideran deterministas. No se registró el esfuerzo de razonamiento; su valor histórico debe considerarse desconocido. Se realizó una única ejecución por unidad y configuración, sin réplicas.

En evaluación:

> La configuración no garantiza determinismo ni reproducibilidad exacta: la temperatura solicitada no fue enviada a los modelos GPT-5 y no hubo réplicas. Las diferencias entre corridas no pueden estimarse con los datos disponibles.

En la tabla de hiperparámetros, reemplazar “Temperatura” por “Temperatura solicitada en el código” y aclarar “no aplicada por el perfil GPT-5”.

En las limitaciones, agregar un ítem específico sobre ejecución única y ausencia de control efectivo de muestreo, con la redacción propuesta en `propuestas_edicion.md`.

### 3.3 Lo que no debe afirmarse

- No afirmar que la temperatura cero “garantizó” reproducibilidad.
- No afirmar que la temperatura cero “evitó” múltiples ejecuciones; la causa fue el diseño de una ejecución por celda.
- No afirmar que el esfuerzo de razonamiento fue “alto”, “bajo” o “el predeterminado” sin registro.
- No afirmar que los logs demuestran la temperatura aplicada.
- No extrapolar la configuración de los jueces a los generadores GPT-5.
- No presentar los tokens de razonamiento como equivalente del esfuerzo.

## 4. Límites de esta reconstrucción

1. No existen volcados HTTP completos de 2025. La captura local prueba el comportamiento de la versión fijada, no reconstruye byte a byte la petición histórica.
2. La conclusión supone que la ejecución histórica usó Pydantic AI 1.1.0, como declara `uv.lock` y el anexo. Si se usó otra versión, no hay evidencia en los logs para confirmarlo; debe declararse la incertidumbre.
3. El esfuerzo de razonamiento no es recuperable si no fue registrado. No se infiere de los tokens.
4. La captura local no reproduce la mutación de `agent.model_settings` observada en los logs Agentic-RAG; por eso el log se trata como metadata de aplicación y no como payload.
5. La ejecución única no se corrige con análisis; se declara como limitación. Las réplicas pertenecen a IX.2.4 y requieren nuevas llamadas.

## 5. Artefactos y verificación

- `salidas/tabla_configuracion_solicitado_registrado_efectivo.csv`: 12 filas (3 estrategias × 3 modelos + 3 recuperadores).
- `salidas/tabla_reasoning_tokens_por_celda.csv`: 12 filas.
- `salidas/tabla_ejecuciones_unicas.csv`: 9 filas.
- `salidas/tabla_parametros_jueces.csv`: 3 filas.
- `salidas/tabla_ubicaciones_texto_a_modificar.csv`: 13 propuestas.
- `salidas/evidencia_payloads_locales.json`: 12 capturas.
- `salidas/evidencia_perfil_pydantic.json`: perfiles y resumen.
- `salidas/evidencia_pydantic_ai_excerpt.txt`: fuente de Pydantic AI.
- `salidas/evidencia_reasoning_effort.json`: búsqueda en 1.873 archivos.
- `salidas/manifiesto_entradas.csv`: 1.880 hashes.
- `salidas/fig_tokens_razonamiento_por_celda.png` y `.pdf`.
- `salidas/diccionario_tablas.md`: diccionario de columnas y advertencias de lectura.

Comprobaciones realizadas:

- 711 respuestas primarias contabilizadas.
- 12/12 payloads sin `temperature`.
- 12/12 payloads sin `reasoning_effort`.
- 711/711 respuestas primarias con `reasoning_tokens` no nulo.
- 0 ocurrencias de `reasoning_effort` en el alcance revisado.
- 9/9 celdas con 79 unidades y 0 duplicados.
- 1.880 archivos de entrada con hash.
- 3 jueces con 9 reportes y 711 evaluaciones cada uno.

## 6. Veredicto sobre IX.1.3

La parte documental y editorial queda resuelta con este paquete: se identifican los parámetros solicitados, se demuestra que la temperatura no se envía bajo la versión fijada, se distingue el log del payload, se documenta la ausencia de esfuerzo de razonamiento y se deja preparada la declaración de ejecución única.

No se puede “demostrar” el esfuerzo histórico ni la petición exacta de 2025 porque no fueron registrados. Esa imposibilidad debe quedar escrita como limitación, no cubierta con una inferencia.

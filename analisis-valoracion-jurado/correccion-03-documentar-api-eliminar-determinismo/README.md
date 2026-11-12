# Corrección IX.1.3 — Documentar parámetros de API y eliminar el determinismo

Esta carpeta contiene la evidencia y los borradores necesarios para resolver el punto **IX.1.3** del plan de correcciones. No modifica el manuscrito, los notebooks históricos, los JSON de respuestas, los logs de agentes ni los reportes de jueces.

## Qué se verificó

1. **Lo solicitado por el código:** `temperature=0.0` en los notebooks/script de generación sin RAG, RAG básico y Agentic-RAG.
2. **Lo registrado por los artefactos:** los registros de sin RAG y RAG básico conservan `{"temperature": 0.0}`; los registros Agentic-RAG guardan `{}`. Ninguno es un volcado de la petición HTTP.
3. **Lo enviado por la biblioteca:** Pydantic AI 1.1.0 declara `temperature` como parámetro no admitido para `gpt-5-nano`, `gpt-5-mini` y `gpt-5`, y lo elimina antes de construir la solicitud.
4. **La captura local:** con `httpx.MockTransport`, sin red, se capturó el cuerpo Chat Completions de las tres estrategias y del agente de recuperación. En los 12 casos, `temperature` está ausente; también están ausentes `reasoning_effort` y `max_completion_tokens`.
5. **Los tokens de razonamiento:** las 711 respuestas primarias tienen `reasoning_tokens` no nulo. Eso demuestra consumo de razonamiento, pero no identifica el esfuerzo solicitado ni el aplicado por el proveedor.
6. **La ejecución única:** cada una de las 9 celdas contiene 79 registros para 79 unidades, sin duplicados y sin campo `run_id`/réplica. Los timestamps son distintos por unidad.
7. **Los jueces:** los tres jueces se configuraron en OpenRouter con `temperature=0.0` y `max_tokens=5000`. Esa configuración es independiente de los modelos generadores GPT-5 y no se usa aquí para afirmar determinismo.

## Conclusión operativa

La afirmación de que la temperatura cero garantizaba reproducibilidad **no se sostiene**. El valor fue solicitado en el código, pero no llegó al payload de los modelos GPT-5. Además, no se registró el esfuerzo de razonamiento; por tanto, su valor histórico debe declararse **desconocido**, no inferirse de los tokens. La ejecución única debe declararse como limitación.

## Artefactos

| Archivo | Función |
| --- | --- |
| `02_parametros_prompts_y_configuracion.ipynb` | Notebook reproducible; ejecuta el análisis y muestra las tablas. |
| `scripts/generar_evidencia.py` | Script que genera todas las tablas, la captura local y la figura. |
| `scripts/ejecutar_notebook.py` | Ejecuta el notebook con el kernel del entorno de `codigo_experimentos`. |
| `informe_IX.1.3.md` | Informe técnico con hallazgos, evidencia, límites y consecuencias. |
| `propuestas_edicion.md` | Borrador de reemplazos para los `.typ` y el README, sin aplicarlos. |
| `borrador_respuesta_al_jurado.md` | Respuesta sintética al punto IX.1.3, lista para adaptar. |
| `salidas/manifiesto_entradas.csv` | SHA-256 y tamaño de las 1.880 entradas utilizadas. |
| `salidas/manifiesto_resumen.json` | Resumen y hash del conjunto de entradas. |
| `salidas/tabla_configuracion_solicitado_registrado_efectivo.csv` | Configuración solicitada, registrada, perfil no admitido y payload. |
| `salidas/tabla_reasoning_tokens_por_celda.csv` | Distribución de tokens de razonamiento por estrategia, componente y modelo. |
| `salidas/tabla_ejecuciones_unicas.csv` | Conteo de registros, unidades, duplicados y timestamps por celda. |
| `salidas/tabla_parametros_jueces.csv` | Configuración registrada de los jueces, separada de los generadores. |
| `salidas/tabla_ubicaciones_texto_a_modificar.csv` | Ubicaciones exactas y propuestas de edición. |
| `salidas/evidencia_payloads_locales.json` | Cuerpos de petición capturados localmente y settings antes/después. |
| `salidas/evidencia_perfil_pydantic.json` | Perfiles de los tres modelos y resumen de la captura. |
| `salidas/evidencia_pydantic_ai_excerpt.txt` | Extracto fuente de Pydantic AI 1.1.0 con el `pop` de settings no admitidos. |
| `salidas/evidencia_reasoning_effort.json` | Búsqueda de `reasoning_effort` en 1.873 archivos y conclusión. |
| `salidas/fig_tokens_razonamiento_por_celda.png` / `.pdf` | Figura de apoyo; no es una prueba del esfuerzo. |
| `salidas/diccionario_tablas.md` | Diccionario de columnas y advertencias de interpretación. |
| `salidas/resumen_evidencia.json` | Resumen legible por máquina. |

## Reproducción

Desde la raíz del repositorio:

```bash
cd codigo_experimentos
uv sync --frozen
uv run --no-sync --frozen python \
  ../analisis-valoracion-jurado/correccion-03-documentar-api-eliminar-determinismo/scripts/generar_evidencia.py
```

El script no usa credenciales ni llamadas de red. La captura HTTP se hace con `httpx.MockTransport` y el mismo `OpenAIChatModel`/`openai_model_profile` de Pydantic AI 1.1.0.

Para ejecutar el notebook con el kernel del entorno de experimentos:

```bash
cd codigo_experimentos
uv run --no-sync --frozen python \
  ../analisis-valoracion-jurado/correccion-03-documentar-api-eliminar-determinismo/scripts/ejecutar_notebook.py
```

## Lectura recomendada antes de editar

1. `informe_IX.1.3.md`
2. `propuestas_edicion.md`
3. `salidas/tabla_ubicaciones_texto_a_modificar.csv`
4. `salidas/evidencia_payloads_locales.json`
5. `salidas/evidencia_perfil_pydantic.json`

## Límites de la reconstrucción

- No existen volcados HTTP completos de las ejecuciones históricas de 2025. Los logs guardan metadatos de la aplicación, no la petición que recibió OpenAI.
- La conclusión sobre Pydantic AI se basa en la versión 1.1.0 fijada en `codigo_experimentos/uv.lock` y en el entorno declarado en el anexo. Si la ejecución histórica usó otra versión, no hay evidencia directa en los logs; la discrepancia debe declararse.
- El nivel de esfuerzo de razonamiento no es recuperable si no fue registrado. Los tokens de razonamiento no permiten reconstruirlo.
- La captura local demuestra el comportamiento del código con el perfil actual, no reproduce la respuesta del proveedor ni completa los logs históricos.
- La ejecución única no puede corregirse por análisis: solo puede declararse como limitación o resolverse con nuevas réplicas, que quedan fuera de este punto.

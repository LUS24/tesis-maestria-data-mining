# Diccionario de las tablas de evidencia

Este diccionario aclara qué prueba y qué no prueba cada columna. Es importante no leer los metadatos de la aplicación como si fueran el cuerpo HTTP enviado a OpenAI.

## `tabla_configuracion_solicitado_registrado_efectivo.csv`

| Columna | Significado |
| --- | --- |
| `estrategia` | `sin_rag`, `rag_basico` o `agentic_rag`. |
| `componente` | `especialista` o `recuperador`. |
| `modelo_rol` | Modelo que cumple ese componente. En el recuperador es siempre `gpt-5`. |
| `modelo_especialista` | Modelo que redacta la respuesta final; permite leer las tres filas del recuperador. |
| `n_observaciones` | Registros consolidados del componente. 79 por celda. |
| `modelo_efectivo_version` | Snapshot informado por la respuesta del proveedor; no es el alias solicitado. |
| `settings_solicitados_codigo` | Lo que el código pasa a `ModelSettings`. No implica que se haya enviado. |
| `settings_registrados_log` | Lo que quedó en `metadata.model_settings` del artefacto. No es el cuerpo HTTP. |
| `perfil_pydantic_unsupported` | Settings que el perfil de Pydantic AI declara no admitidos para ese modelo. |
| `temperatura_en_payload` | Resultado de la captura local del cuerpo Chat Completions. `False` = ausente. |
| `reasoning_effort_solicitado` | `False` = no aparece en el cuerpo capturado. No significa “esfuerzo predeterminado”. |
| `reasoning_effort_registrado` | `False` = no aparece en `metadata.model_settings`. |
| `max_tokens_solicitado` | Límite explícito en el código. Los generadores no lo fijaron; los jueces sí. |
| `reasoning_tokens_n` | Cantidad de respuestas con `usage.tokens.tokens_details.reasoning_tokens` no nulo. |
| `reasoning_tokens_*` | Distribución de tokens de razonamiento. No es el nivel de esfuerzo. |
| `output_tokens_mediana` | Mediana de tokens de salida. |
| `proporcion_razonamiento_mediana` | Mediana de `reasoning_tokens / output_tokens`. |
| `respuestas_blancas` | Respuestas vacías o solo con espacios. En el recuperador es `N/A`. |
| `unidades_unicas` | Unidades distintas en la celda. Debe ser 79. |
| `ejecuciones_por_unidad` | Registros consolidados por unidad en el artefacto. `1.0` significa una respuesta consolidada por unidad, **no** una única llamada HTTP en Agentic-RAG. |
| `fuente_codigo` | Notebook/script que solicitó la configuración. |
| `fuente_log` | Artefacto del que se extrajo el metadata. |
| `notas` | Aclaraciones específicas de instrumentación. |

## `tabla_reasoning_tokens_por_celda.csv`

| Columna | Significado |
| --- | --- |
| `n` | Respuestas con `reasoning_tokens` no nulo. |
| `min`, `p25`, `mediana`, `p75`, `max`, `media`, `total` | Estadísticos de tokens de razonamiento. |
| `output_tokens_mediana` | Mediana de tokens de salida. |
| `proporcion_razonamiento_mediana` | Mediana de la proporción de tokens de salida dedicada a razonamiento. |
| `respuestas_blancas` | Respuestas vacías o solo con espacios; `N/A` en recuperador. |

**No usar esta tabla para inferir el esfuerzo de razonamiento.** Solo describe el consumo observado.

## `tabla_ejecuciones_unicas.csv`

| Columna | Significado |
| --- | --- |
| `registros` | Filas consolidadas de la celda. |
| `unidades_unicas` | Unidades distintas. Debe ser 79. |
| `casos_unicos` | Casos distintos. Debe ser 25. |
| `duplicados_unidad` | Registros de la misma unidad repetidos en la celda. Debe ser 0. |
| `timestamps_unicos_especialista` | Timestamps distintos del especialista. |
| `timestamps_unicos_recuperador` | Timestamps distintos del recuperador en Agentic-RAG. |
| `replicas_identificadas` | Réplicas de la misma unidad detectables por duplicación de registros. 0 significa que no hay evidencia de réplicas en el artefacto. |
| `campo_run_id_replica` | Indica si existe un identificador de corrida/réplica. |
| `respuestas_blancas` | Respuestas vacías o solo con espacios. |
| `fecha_inicio_*`, `fecha_fin_*` | Rango temporal de los timestamps. |
| `modelo_version` | Snapshots observados. |
| `nota` | Aclaración de que una fila consolidada no equivale a una llamada HTTP. |

## `tabla_parametros_jueces.csv`

| Columna | Significado |
| --- | --- |
| `modelo_juez` | Identificador del modelo juez en OpenRouter. |
| `n_reportes` | Reportes JSON del juez. |
| `n_evaluaciones` | Casos evaluados por el juez; 711 por juez. |
| `settings_registrados` | Configuración declarada en los reportes de `pydantic_evals`. |
| `temperature_en_payload_verificada` | En este artefacto no se capturó el payload de los jueces; no se afirma su envío efectivo. |
| `reasoning_effort_registrado` | No se encontró un campo de esfuerzo. |
| `nota` | Separación entre jueces y modelos generadores GPT-5. |

## `tabla_ubicaciones_texto_a_modificar.csv`

| Columna | Significado |
| --- | --- |
| `archivo` | Archivo a revisar. |
| `linea` | Línea actual del texto coincidente. |
| `alcance` | Indica si se reemplaza una oración, una fila, una línea o se inserta un bloque. |
| `texto_actual` | Línea completa actual, para contexto. |
| `texto_actual_coincidente` | Fragmento exacto que se propone reemplazar. |
| `problema` | Motivo de la corrección. |
| `texto_propuesto` | Texto sugerido; no aplicado. |
| `prioridad` | `obligatoria` o `recomendada`. |
| `nota` | Aclaración de aplicación. |

En las inserciones (`README.md` y `09_capitulo_08...`), `texto_propuesto` **no reemplaza** el texto actual: se inserta después de la línea indicada.

## `evidencia_payloads_locales.json`

| Campo | Significado |
| --- | --- |
| `request_body_keys` | Claves del cuerpo Chat Completions capturado. |
| `temperature_presente` | Si `temperature` aparece en el cuerpo. |
| `reasoning_effort_presente` | Si `reasoning_effort` aparece en el cuerpo. |
| `max_completion_tokens_presente` | Si el límite de salida aparece en el cuerpo. |
| `model_settings_solicitados` | Settings del agente antes de la corrida. |
| `model_settings_agente_despues_de_run` | Settings del agente después de la corrida local. |
| `request_body` | Cuerpo completo de la petición simulada, con mensajes de prueba. |

La captura usa `httpx.MockTransport`; no sale a Internet. No prueba que la ejecución histórica haya sido idéntica, pero sí el comportamiento de la versión fijada.

## `evidencia_perfil_pydantic.json`

| Campo | Significado |
| --- | --- |
| `perfiles.*.openai_unsupported_model_settings` | Lista de settings que el perfil declara no admitidos. |
| `captura_payload.*` | Resumen por estrategia/componente/modelo. |
| `openai_chat_model_source_sha256` | Hash del archivo fuente de Pydantic AI usado. |

## `evidencia_reasoning_effort.json`

| Campo | Significado |
| --- | --- |
| `alcance` | Archivos revisados. |
| `ocurrencias_de_reasoning_effort_o_reasoning_igual` | Coincidencias encontradas. En la revisión actual: 0. |
| `n_respuestas_primarias` | 711. |
| `n_respuestas_con_reasoning_tokens` | 711. |
| `conclusion` | El esfuerzo histórico no es reconstruible con los artefactos. |

## `manifiesto_entradas.csv`

| Columna | Significado |
| --- | --- |
| `ruta_relativa` | Ruta respecto de la raíz del repositorio. |
| `bytes` | Tamaño del archivo. |
| `sha256` | Hash de la entrada usada. |
| `categoria` | `fuente_o_manuscrito`, `log_agente` o `reporte_juez`. |

El manifiesto se calcula antes de generar las tablas derivadas. No incluye los artefactos de esta carpeta, salvo el `README.md` raíz que forma parte de las fuentes revisadas.

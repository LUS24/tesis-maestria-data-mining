# Borrador de respuesta al jurado — IX.1.3

**Punto:** documentar los parámetros de API y eliminar la afirmación de determinismo.

## Respuesta propuesta

Se revisaron conjuntamente el código de generación, los metadatos de las 711 respuestas, los 1.838 logs de `part_g/chat_data/`, los reportes de los jueces y la versión de Pydantic AI fijada en `codigo_experimentos/uv.lock`.

El código solicitó `temperature=0.0` en los tres notebooks/scripts de generación. Sin embargo, Pydantic AI 1.1.0 declara `temperature` como parámetro no admitido para `gpt-5-nano`, `gpt-5-mini` y `gpt-5`, y lo elimina antes de construir la petición. La captura local del cuerpo Chat Completions —realizada con `httpx.MockTransport`, sin llamadas a OpenAI— confirma que `temperature` no aparece en ninguno de los 12 payloads de las estrategias y del agente de recuperación. También están ausentes `reasoning_effort` y `max_completion_tokens`.

Los logs no son volcados HTTP: sin RAG y RAG básico registran `{"temperature": 0.0}`, mientras que Agentic-RAG registra `{}`. Por eso no se usan como prueba de lo enviado. La versión definitiva del manuscrito debe distinguir “temperatura solicitada en el código” de “parámetro aplicado”.

No se registró el esfuerzo de razonamiento: la búsqueda de `reasoning_effort` en 1.873 archivos del alcance revisado —código de generación, respuestas primarias, reportes de jueces y logs— devolvió cero ocurrencias. Pydantic AI 1.1.0 no define un default y envía `NOT_GIVEN`; OpenAI documenta `medium` como default para GPT-5. Las 711 respuestas primarias tienen `reasoning_tokens` no nulo, pero esos tokens no identifican el valor efectivo local; se declara el default documentado, no un valor observado.

Finalmente, cada celda contiene 79 registros para 79 unidades, sin duplicados y sin campo de réplica. La ejecución única debe incorporarse como limitación explícita. No se afirma determinismo ni estabilidad entre corridas.

## Evidencia disponible para el jurado

- `salidas/tabla_configuracion_solicitado_registrado_efectivo.csv`
- `salidas/evidencia_payloads_locales.json`
- `salidas/evidencia_perfil_pydantic.json`
- `salidas/evidencia_pydantic_ai_excerpt.txt`
- `salidas/evidencia_reasoning_effort.json`
- `salidas/tabla_reasoning_tokens_por_celda.csv`
- `salidas/tabla_ejecuciones_unicas.csv`
- `salidas/manifiesto_entradas.csv` y `salidas/manifiesto_resumen.json`
- `propuestas_edicion.md` e `informe_IX.1.3.md`

## Redacción breve para el formulario

> Se documentó que la temperatura cero fue solicitada en el código pero no enviada a los modelos GPT-5, porque Pydantic AI 1.1.0 elimina ese parámetro antes de la solicitud. Se retiró la afirmación de determinismo, se declaró la ejecución única y se documentó que el esfuerzo de razonamiento no fue registrado. La evidencia incluye la captura local del payload, los perfiles de la biblioteca, las tablas por celda y los hashes de las fuentes.

# Informe de diagnóstico — IX.1.2

**Punto:** diagnosticar Agentic-RAG + gpt-5-nano, los faltantes y la interpretación de “sobrecarga agéntica”.  
**Fecha:** 2026-11-12.  
**Insumos:** respuestas, métricas, evaluaciones de jueces y logs históricos del repositorio.  
**Restricción respetada:** no se modificó ningún archivo fuente, log, JSON, CSV, PDF o base SQLite. Todos los artefactos son derivados y están en esta carpeta.

---

## 1. Resumen ejecutivo

1. **Las 27 medias ausentes no son 27 fallos de generación.** Son las 27 combinaciones de las unidades 23, 24 y 25 (3 unidades × 9 configuraciones). En el CSV de métricas la subpregunta está vacía; en el de jueces vale `0`. El join de `part_j/01_exploracion_descriptiva_correlacion.ipynb` no las encuentra. Las 27 tienen tres evaluaciones de jueces y respuestas sustantivas. Al normalizar la clave se recuperan **711 observaciones** y **2.133 evaluaciones de jueces**.
2. **La celda Agentic-RAG + gpt-5-nano contiene 41 salidas no sustantivas de 79** (51,9%; IC 95% Wilson 41,1–62,6%). El desglose es: 27 vacías, 1 solo espacios, 2 abstenciones explícitas, 1 truncada y 10 indeterminadas (mensajes de proceso, marcadores `TEST`/`placeholder`/`PENDING` y un mensaje interno). No hay errores técnicos explícitos.
3. **Los logs no muestran truncamiento por tokens ni falta de recuperación.** Los 79 logs de nano contienen una llamada a `retrieve_relevant_documents` y al menos una llamada a `final_result`; 77 tienen exactamente una y 2 tienen más de una. El `finish_reason` del especialista es `tool_call` en los 79 casos. Las 28 salidas vacías/solo espacios tienen entre 1 y 12 documentos seleccionados, entre 2 y 6 búsquedas y entre 575 y 7.015 tokens de salida. El problema está en el `response_text` del `final_result`: vacío, con espacios o con un marcador no respondido.
4. **Cuando nano responde, su calidad es alta.** Las 38 respuestas sustantivas tienen media 0,820 y mediana 0,958. Con fallo = 0, la celda completa tiene media 0,395 y mediana 0; con exclusión de no sustantivas, media 0,820 y mediana 0,958. La diferencia con RAG básico cambia de signo según el escenario: −0,205 con fallo = 0 y +0,182 con exclusión (38 pares). Esto describe un **modo de fallo de respuesta**, no una degradación uniforme de la calidad de las respuestas producidas.
5. **Los puntajes de los jueces sobre salidas no sustantivas no son una medición válida de calidad.** En las 57 observaciones no sustantivas hay 171 evaluaciones. Once filas de corrección (9 combinaciones celda-unidad; 8 unidades distintas) tienen puntaje mayor que cero y cinco filas de precisión legal tienen puntaje mayor que cero. Varias justificaciones citan artículos que no aparecen en la respuesta o describen contenido inexistente. Estos puntajes deben auditarse, no promediarse como calidad.
6. **La tabla de medianas del manuscrito se calculó sobre 76 observaciones por celda**, no sobre 79. Al recuperar el join cambian cinco de las nueve medianas. La celda nano pasa de 0,083 a 0,250 con los jueces originales, a 0,000 con fallo = 0 y a 0,958 con exclusión.
7. **La comparación sin RAG nano vs. mini también cambia.** gpt-5-mini tiene 14 abstenciones explícitas en sin RAG. Su mediana es 0,250 con las 79 unidades y 0,333 si se excluyen las abstenciones. La mediana de nano es 0,583 en ambos casos. El orden observado debe describirse, no explicarse causalmente por “capacidad” con estos datos.

---

## 2. Reconciliación de datos

| Control | Resultado |
|---|---:|
| Observaciones | 711 |
| Unidades de evaluación | 79 |
| Casos | 25 |
| Celdas estrategia × modelo | 9 |
| Filas de jueces | 2.133 |
| Medias ausentes por join | 27 |
| Observaciones no sustantivas | 57 |
| Evaluaciones de jueces sobre no sustantivas | 171 |

La tabla `salidas/04_auditoria_faltantes_join.csv` contiene las 27 filas recuperadas. Las 27 tienen `n_filas_juez = 3`; el valor de `respuesta_correcta_avg` del CSV original está vacío en las 27; el valor recalculado coincide con el promedio de los tres jueces. La tabla `salidas/08_comparacion_medianas_manuscrito.csv` compara la mediana publicada, la mediana calculada sobre las 76 filas originales, la mediana corregida sobre 79 y los escenarios de fallo.

**Implicación editorial:** la frase del manuscrito que atribuye las 27 ausencias a “fallos puntuales en la generación de respuestas” es incorrecta. Debe reemplazarse por la descripción del defecto de join y por la recuperación de las 711 observaciones.

---

## 3. Clasificación de las 711 respuestas

Categorías mutuamente excluyentes:

- **sustantiva:** contiene una respuesta al caso, aunque sea jurídicamente incorrecta.
- **vacía:** cadena vacía.
- **solo espacios:** únicamente espacios o saltos de línea.
- **abstención explícita:** el modelo declara que no puede responder o que no tiene información suficiente, sin una respuesta sustantiva.
- **error explícito:** error técnico, excepción, timeout, rate limit o respuesta HTTP de error.
- **truncada:** salida incompleta, por ejemplo un JSON que empieza con `{` y no continúa.
- **indeterminada:** marcador de prueba, mensaje de proceso, mensaje interno o texto no clasificable como respuesta.

| Estrategia | Modelo | Sustantivas | No sustantivas | Vacías | Solo espacios | Abstenciones | Truncadas | Indeterminadas | Tasa no sustantiva (IC 95%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sin RAG | gpt-5-nano | 78 | 1 | 0 | 0 | 1 | 0 | 0 | 1,3% (0,2–6,8) |
| Sin RAG | gpt-5-mini | 65 | 14 | 0 | 0 | 14 | 0 | 0 | 17,7% (10,9–27,6) |
| Sin RAG | gpt-5 | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |
| RAG básico | gpt-5-nano | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |
| RAG básico | gpt-5-mini | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |
| RAG básico | gpt-5 | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |
| Agentic-RAG | gpt-5-nano | 38 | 41 | 27 | 1 | 2 | 1 | 10 | 51,9% (41,1–62,6) |
| Agentic-RAG | gpt-5-mini | 78 | 1 | 0 | 0 | 0 | 0 | 1 | 1,3% (0,2–6,8) |
| Agentic-RAG | gpt-5 | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |

**Lectura:** el problema no es general a Agentic-RAG. Está concentrado en la combinación con gpt-5-nano; gpt-5-mini tiene un único mensaje de proceso y gpt-5 no tiene salidas no sustantivas. La tabla ancha está en `salidas/03b_tabla_categorias_ancha.csv`.

La clasificación automática es reproducible y conserva la evidencia textual. Las 27 vacías y la salida de solo espacios son inequívocas. Los 10 casos indeterminados y las 2 abstenciones requieren la revisión manual incluida en `revision_manual/`.

---

## 4. La celda Agentic-RAG + gpt-5-nano

### 4.1 Composición

| Categoría | n |
|---|---:|
| Sustantiva | 38 |
| Vacía | 27 |
| Solo espacios | 1 |
| Abstención explícita | 2 |
| Truncada | 1 |
| Indeterminada | 10 |
| **Total no sustantiva** | **41** |

Los 10 indeterminados son:

- `Q03_02`: “Por favor espera mientras analizo la normativa aplicable…”
- `Q03_03`: “I will consult the relevant legal sources… Retrieve.”
- `Q06_02`: `TEST`
- `Q07_01`: “[Se solicita al usuario esperar…]”
- `Q08_03`: “[Se procede a mayores explicando el procedimiento…]”
- `Q09_01`: `placeholder`
- `Q12_01`: `placeholder`
- `Q16_03`: `PENDING`
- `Q17_03`: “(Se ejecutó la búsqueda de documentos relevantes.)”
- `Q21_02`: “Esta es la preliminar que no debe aparecer al usuario”

Las dos abstenciones son `Q10_03` y `Q17_02`. La truncada es `Q05_04` (`{`). La salida de solo espacios es `Q07_03`.

### 4.2 Logs: el `final_result` contiene vacío o un marcador

Los logs de los 79 casos tienen la misma estructura básica:

1. el especialista recibe la pregunta;
2. llama a `retrieve_relevant_documents`;
3. recibe el `tool-return` con `selected_documents`;
4. llama a `final_result`;
5. se registra el `tool-return` de `final_result`.

En los 79 casos, el `finish_reason` del especialista es `tool_call`; no hay `length`, `error` ni una terminación anómala. La diferencia está en el argumento `response_text` del `final_result`. En los casos vacíos, ese argumento es `""`, `" "` o un marcador como `TEST`, `placeholder` o `PENDING`.

Dos logs (`Q09_01` y `Q21_02`) tienen más de una llamada a `final_result`; ambos son no sustantivos. El texto registrado coincide con el primer `final_result`. Esto es una anomalía adicional que debe mencionarse, pero no explica por sí sola los 41 casos.

### 4.3 No es falta de recuperación ni agotamiento de tokens

| Métrica | Salidas vacías/solo espacios (n=28) | Salidas sustantivas (n=38) |
|---|---:|---:|
| Documentos seleccionados, mediana (rango) | 5 (1–12) | 4 (1–11) |
| Búsquedas en el historial, mediana (rango) | 6 (2–6) | 6 (2–6) |
| Tokens de salida del especialista, mediana (rango) | 3.095 (575–7.015) | 4.491 (2.267–9.228) |
| Tokens de razonamiento, mediana (rango) | 2.976 (512–6.656) | 3.744 (1.984–8.448) |

Las salidas vacías tienen recuperación y tokens. No hay un patrón de “cero documentos” ni de “límite de tokens alcanzado”. La conclusión descriptiva correcta es: **el modelo devolvió un `final_result` vacío o no respondido en 41 casos, pese a disponer de contexto recuperado**. La causa de esa decisión de salida no puede establecerse con los logs disponibles.

### 4.4 Qué se puede y qué no se puede afirmar

Se puede afirmar:

- la celda tiene 41/79 salidas no sustantivas;
- las salidas no sustantivas no se deben a falta de llamadas, falta de recuperación ni truncamiento por longitud;
- las 38 respuestas sustantivas tienen un desempeño alto (media 0,820; mediana 0,958);
- el resultado a nivel sistema es inferior al de RAG básico cuando se asigna 0 a los fallos, pero superior cuando se comparan solo respuestas sustantivas;
- el patrón es heterogéneo y está concentrado en una celda.

No se puede afirmar:

- que la “complejidad agéntica” sea la causa;
- que el modelo pequeño tenga una “degradación general” de calidad;
- que el problema se resolvería con más recuperación;
- que los jueces midieron correctamente las salidas vacías;
- que el resultado sea estable entre réplicas, porque no hay réplicas.

---

## 5. Jueces sobre salidas no sustantivas

En las 57 observaciones no sustantivas hay 171 filas de jueces (3 por observación). Resultados:

- 11 filas de corrección con puntaje > 0, distribuidas en 9 combinaciones celda-unidad (8 unidades distintas);
- 5 filas de precisión legal con puntaje > 0, en 5 observaciones;
- 6 de las 11 filas de corrección corresponden a abstenciones de sin RAG + gpt-5-mini;
- las otras 5 corresponden a Agentic-RAG + gpt-5-nano: 3 salidas vacías y 2 mensajes de proceso;
- las 5 filas de precisión legal > 0 corresponden a Agentic-RAG + gpt-5-nano: 3 vacías y 2 indeterminadas.

Ejemplos verificables en `salidas/05_auditoria_jueces_salidas_no_sustantivas.csv`:

| Observación | Salida | Juez | Puntaje | Problema |
|---|---|---|---:|---|
| `Q05_01` | vacía | DeepSeek | corrección 1,00 | La justificación describe una respuesta completa; la salida está vacía. La misma fila asigna 0,00 en precisión legal y reconoce que el output está vacío. |
| `Q07_04` | vacía | DeepSeek | legal 1,00 | La justificación dice que se citan los artículos 138–145; la salida está vacía. |
| `Q08_01` | vacía | DeepSeek | corrección 0,85 | La justificación describe derechos y obligaciones que no están en la salida. |
| `Q08_03` | mensaje de proceso | DeepSeek y Kimi | corrección 1,00 | La salida solo dice “[Se procede a mayores explicando el procedimiento…]”; la justificación describe una respuesta completa. |
| `Q10_01` | vacía | DeepSeek | corrección 0,90 | La justificación cita el artículo 201; la salida está vacía. |
| `Q12_03` | vacía | DeepSeek | legal 1,00 | La justificación atribuye la cita del artículo 219; la salida está vacía. |
| `Q13_02` | vacía | DeepSeek | legal 1,00 | La justificación enumera los artículos 243, 236, 237, 235 y 241; la salida está vacía. |

**Implicación:** los promedios de jueces sobre salidas no sustantivas no son una medición válida de calidad. Para el análisis de sistema se debe usar fallo = 0 o exclusión, y para la validación de jueces se debe auditar explícitamente este subconjunto. La auditoría de jueces de IX.2.3 debería incluir estas salidas o justificar su exclusión.

---

## 6. Sensibilidad de las comparaciones

La inferencia principal corresponde a IX.1.1, con modelo ordinal mixto. Aquí se presenta una sensibilidad descriptiva y exploratoria para mostrar cuánto depende la lectura del tratamiento de las salidas no sustantivas.

| Comparación en gpt-5-nano | Original (jueces) | Fallo = 0 | Exclusión |
|---|---:|---:|---:|
| Agentic-RAG − RAG básico | −0,185 (n=79) | −0,205 (n=79) | +0,182 (n=38) |
| Agentic-RAG − Sin RAG | −0,151 (n=79) | −0,171 (n=79) | +0,213 (n=38) |
| RAG básico − Sin RAG | +0,034 (n=79) | +0,034 (n=79) | +0,021 (n=78) |

Medias de diferencias pareadas; los valores negativos indican que la primera estrategia tiene menor puntaje. La tabla completa con medianas y p exploratorios está en `salidas/09_sensibilidad_pares_estrategias.csv`. Los p no están corregidos y no reemplazan el análisis de IX.1.1.

La exclusión usa solo las 38 unidades en las que Agentic-RAG + nano produjo una respuesta sustantiva. Es una submuestra seleccionada: no es el efecto causal de Agentic-RAG, sino la calidad condicional a que el sistema haya respondido. La conclusión correcta es:

- **a nivel sistema**, la celda nano es peor que RAG básico porque falla en 41/79 unidades;
- **condicional a que responda**, la calidad de nano es alta y supera a RAG básico en la submuestra;
- ambas afirmaciones son compatibles y deben reportarse juntas;
- la etiqueta “sobrecarga agéntica” no describe adecuadamente este patrón.

---

## 7. Sin RAG: gpt-5-nano frente a gpt-5-mini

| Métrica | gpt-5-nano | gpt-5-mini |
|---|---:|---:|
| n | 79 | 79 |
| Sustantivas | 78 | 65 |
| Abstenciones explícitas | 1 | 14 |
| Media | 0,565 | 0,336 |
| Mediana | 0,583 | 0,250 |
| Q1–Q3 | 0,417–0,750 | 0,083–0,500 |
| Mediana solo sustantivas | 0,583 | 0,333 |
| % puntaje ≥ 0,75 | 32,9% | 13,9% |
| Mediana de longitud (caracteres) | 2.817 | 2.392 |
| Menciona algún artículo | 57,0% | 100,0% |
| Menciona limitación o falta de contexto | 20,3% | 77,2% |
| Mediana de tokens de razonamiento | 5.376 | 1.408 |

La diferencia persiste al excluir las abstenciones, pero el patrón no permite atribuirla a “capacidad”. gpt-5-mini se abstiene 14 veces, declara limitaciones con mucha frecuencia y sus respuestas son más cortas; nano responde casi siempre y con más tokens de razonamiento. Son diferencias de comportamiento que deben describirse y, si se quiere explicar, estudiarse con un diseño específico. La tabla está en `salidas/10_sin_rag_nano_vs_mini.csv`.

---

## 8. Qué cambia en las medianas del manuscrito

La Tabla 11 del manuscrito coincide con la mediana calculada sobre las 76 filas del CSV original. Al recuperar las 27 medias:

| Estrategia | Modelo | Manuscrito | CSV original (n=76) | Corregida 79 (jueces) | Fallo = 0 | Exclusión (n) |
|---|---:|---:|---:|---:|---:|---:|
| Sin RAG | gpt-5-nano | 0,583 | 0,583 | 0,583 | 0,583 | 0,583 (78) |
| Sin RAG | gpt-5-mini | 0,333 | 0,333 | 0,250 | 0,250 | 0,333 (65) |
| Sin RAG | gpt-5 | 0,833 | 0,833 | 0,833 | 0,833 | 0,833 (79) |
| RAG básico | gpt-5-nano | 0,583 | 0,583 | 0,583 | 0,583 | 0,583 (79) |
| RAG básico | gpt-5-mini | 0,625 | 0,625 | 0,667 | 0,667 | 0,667 (79) |
| RAG básico | gpt-5 | 0,833 | 0,833 | 0,833 | 0,833 | 0,833 (79) |
| Agentic-RAG | gpt-5-nano | 0,083 | 0,083 | 0,250 | 0,000 | 0,958 (38) |
| Agentic-RAG | gpt-5-mini | 0,917 | 0,917 | 1,000 | 1,000 | 1,000 (78) |
| Agentic-RAG | gpt-5 | 0,958 | 0,958 | 1,000 | 1,000 | 1,000 (79) |

Cinco de las nueve medianas cambian. La celda nano es la más sensible: 0,083 en el manuscrito, 0,250 al recuperar el join, 0,000 con fallo = 0 y 0,958 con exclusión. Por eso no debe presentarse una única mediana sin declarar el escenario.

---

## 9. Propuestas de redacción

El detalle está en `PROPUESTAS_MANUSCRITO.md`. En síntesis:

1. Reemplazar la afirmación de que 27 observaciones se eliminaron por fallos de generación por la explicación del join y la recuperación de las 711 observaciones.
2. Sustituir “sobrecarga agéntica” por “modo de fallo de respuesta” o “fallo de respuesta concentrado en la celda”, y reportar por separado el resultado a nivel sistema y la calidad condicional a respuesta sustantiva.
3. Actualizar la tabla de medianas y todas las referencias a `n = 79` o `n = 76` según el escenario.
4. Agregar una tabla de categorías por celda y una nota sobre los jueces que puntuaron salidas no sustantivas.
5. Añadir una limitación explícita: no hay réplicas ni ablación, por lo que no puede atribuirse el fallo a la “complejidad agéntica” ni a una causa única.
6. Ajustar el ejemplo del anexo: la respuesta correcta de nano Agentic-RAG es una de las 38 respuestas sustantivas y no representa las 41 no sustantivas.

---

## 10. Revisión manual pendiente

`revision_manual/paquete_revision_ciega.csv` contiene:

- las 57 observaciones no sustantivas;
- 30 respuestas sustantivas de control, estratificadas por celda;
- 87 filas en orden aleatorio, sin estrategia, modelo ni categoría automática.

El revisor debe completar `categoria_revisada` y `justificacion` en `revision_manual/plantilla_resultados.csv` usando las definiciones de `revision_manual/LEEME.md`. El mapa `salidas/mapa_revision_ciega.csv` no debe abrirse hasta terminar la revisión.

La revisión manual no es una evaluación de corrección jurídica. Solo decide si la salida es una respuesta sustantiva y, si no lo es, en qué categoría cae. La validación jurídica de las respuestas es otra tarea (IX.2.3).

---

## 11. Artefactos

| Archivo | Contenido |
|---|---|
| `diagnostico_gpt5_nano.ipynb` | Notebook ejecutado con el flujo completo. |
| `src/diagnostico.py` | Código reproducible; no modifica fuentes. |
| `salidas/01_dataset_derivado_711.csv` | 711 observaciones con categorías, jueces, escenarios y logs. |
| `salidas/02_resumen_por_celda.csv` | Resumen por celda con tasas e IC. |
| `salidas/03_conteo_categorias_por_celda.csv` | Conteo largo por categoría. |
| `salidas/03b_tabla_categorias_ancha.csv` | Tabla ancha para el manuscrito. |
| `salidas/04_auditoria_faltantes_join.csv` | Las 27 medias recuperadas. |
| `salidas/05_auditoria_jueces_salidas_no_sustantivas.csv` | 171 filas de jueces sobre no sustantivas. |
| `salidas/06_logs_agentes_237.csv` | Logs parseados de las 237 respuestas agénticas. |
| `salidas/07_resumen_logs_por_modelo.csv` | Resumen de logs por modelo. |
| `salidas/08_comparacion_medianas_manuscrito.csv` | Manuscrito vs. 76 vs. 79 vs. escenarios. |
| `salidas/09_sensibilidad_pares_estrategias.csv` | Comparaciones pareadas exploratorias. |
| `salidas/10_sin_rag_nano_vs_mini.csv` | Comparación descriptiva sin RAG. |
| `salidas/11_celda_nano_agentic_79.csv` | Las 79 filas de la celda, con evidencia. |
| `salidas/12_auditoria_27_medias_ausentes.csv` | Copia específica de la auditoría de join. |
| `salidas/13_salidas_no_sustantivas_con_evidencia.csv` | Las 57 no sustantivas con evidencia. |
| `salidas/lista_verificacion_no_sustantivas.csv` | Lista asistida para revisión. |
| `salidas/mapa_revision_ciega.csv` | Mapa review_id → observación; no abrir durante la revisión. |
| `salidas/resumen_ejecutivo.json` | Resumen numérico legible por máquina. |
| `figuras/01…07` | Figuras en PDF y PNG. |
| `revision_manual/LEEME.md` | Instrucciones de revisión ciega. |
| `revision_manual/paquete_revision_ciega.csv` | Paquete ciego de 87 respuestas. |
| `revision_manual/plantilla_resultados.csv` | Plantilla para completar. |
| `INFORME_DIAGNOSTICO.md` | Este informe. |
| `PROPUESTAS_MANUSCRITO.md` | Cambios de texto sugeridos. |

---

## 12. Limitaciones del diagnóstico

- La clasificación de las 57 no sustantivas es automática y debe confirmarse con la revisión ciega. Las 27 vacías y la salida de solo espacios son inequívocas; los 10 indeterminados y las 2 abstenciones requieren revisión.
- Los logs no registran el payload HTTP completo ni el esfuerzo de razonamiento efectivo. No se puede afirmar por qué el modelo devolvió un `final_result` vacío. IX.1.3 trata esa limitación.
- No hay réplicas ni ablación. No se puede saber si el fallo es estable entre corridas ni si depende del modelo del recuperador, del prompt o de otra diferencia entre estrategias.
- La comparación de respuestas sustantivas está condicionada a una submuestra seleccionada; no es el efecto causal de Agentic-RAG.
- La comparación sin RAG nano vs. mini es descriptiva. No demuestra una relación causal con la capacidad del modelo.
- La auditoría de jueces detecta inconsistencias claras, pero no cuantifica la validez de los jueces frente a criterio humano. Eso requiere IX.2.3.

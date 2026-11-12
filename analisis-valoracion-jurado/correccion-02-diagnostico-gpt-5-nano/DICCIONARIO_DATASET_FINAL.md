# Diccionario de la base final para IX.1.1

**Archivo:** `salidas/14_dataset_categoria_final.csv`  
**Filas:** 711 (79 unidades × 9 configuraciones).  
**Unidad de análisis:** una subpregunta/unidad de evaluación respondida por una configuración estrategia × modelo.  
**Clave:** `obs_id` + `estrategia` + `modelo`; `q` identifica el caso 1–25.

---

## 1. Columnas que debe usar IX.1.1

| Columna | Uso |
|---|---|
| `obs_id` | Identificador de unidad: `Q01_01`, `Q23_00`, etc. Es la unidad repetida entre estrategias y modelos. |
| `q` | Caso 1–25. Es el agrupamiento superior para el modelo mixto. |
| `sub` | Subpregunta canónica (0 para las unidades 23–25). |
| `estrategia` | `llm_responses_no_rag`, `llm_responses_base_rag`, `llm_responses_agentic_rag`. |
| `estrategia_corta` | `sin_rag`, `rag_basico`, `agentic_rag`. |
| `modelo` | Modelo del Agente Especialista Legal: `gpt-5-nano`, `gpt-5-mini`, `gpt-5`. En Agentic-RAG el recuperador es siempre gpt-5. |
| `categoria_final` | **Etiqueta final aceptada:** `sustantiva`, `vacia`, `solo_espacios`, `abstencion_explicita`, `error_explicito`, `truncada`, `indeterminada`. |
| `subcategoria_final` | Detalle de la categoría final. |
| `fuente_categoria` | `revision_manual` para las 87 filas revisadas; `clasificacion_automatica` para el resto. |
| `es_no_sustantiva_final` | `True` si `categoria_final != sustantiva`. |
| `es_fallo_tecnico_final` | `True` para vacía, solo espacios, error explícito, truncada e indeterminada. No incluye la abstención explícita. |
| `puntaje_final_original` | Promedio de los tres jueces, mapeado a la rúbrica, sin modificar por la categoría. |
| `puntaje_final_fallo_cero` | **Escenario principal de sistema:** 0 si la salida es no sustantiva; si es sustantiva, `puntaje_final_original`. |
| `puntaje_final_solo_fallos_tecnicos_cero` | 0 solo para fallos técnicos; conserva el puntaje de las abstenciones explícitas. |
| `puntaje_final_exclusion` | `puntaje_final_original` si es sustantiva; `NaN` si es no sustantiva. |
| `respuesta_correcta_scores_json` | Puntajes crudos de los tres jueces para esa observación. |
| `respuesta_correcta_rubric` | Promedio mapeado a la rúbrica (equivalente a `puntaje_final_original`). |
| `modelo_version`, `timestamp`, `provider_name` | Metadatos del modelo y la llamada. |
| `output_tokens`, `reasoning_tokens`, `costo_total` | Costos y uso; `costo_total` suma especialista + recuperador. |
| `law_*`, `retrieval_*` | Campos de logs del sistema agéntico; `NaN` en sin RAG y RAG básico. |

## 2. Columnas históricas que no deben usarse como etiqueta final

| Columna | Motivo |
|---|---|
| `categoria` / `subcategoria` | Clasificación automática original. Se conserva para auditoría. |
| `es_no_sustantiva` | Basada en la clasificación automática. |
| `puntaje_fallo_cero`, `puntaje_exclusion`, `puntaje_solo_fallos_tecnicos_cero` | Versiones automáticas de los escenarios. Usar las columnas `puntaje_final_*`. |
| `responses_text_cleaned.csv` / `01_dataset_derivado_711.csv` | No incorporan la revisión manual aceptada. |

## 3. Escenarios

- **`puntaje_final_fallo_cero`:** escenario principal para evaluar el sistema completo. Un sistema que no responde no recibe crédito.
- **`puntaje_final_exclusion`:** análisis condicional a que el sistema haya producido una respuesta sustantiva. La submuestra es seleccionada; no es un efecto causal.
- **`puntaje_final_solo_fallos_tecnicos_cero`:** separa la abstención explícita del fallo técnico. Sirve como sensibilidad, no como escenario principal.
- **`puntaje_final_original`:** refleja los puntajes de los jueces, incluidos los casos en que puntuaron salidas no sustantivas. Es útil para auditar a los jueces, no para la conclusión principal de calidad.

## 4. Advertencias para el modelo ordinal

1. La variable original es ordinal: 0, 0,25, 0,5, 0,75, 1. El promedio de tres jueces tiene 13 valores posibles; para el modelo ordinal principal usar los puntajes por juez o discretizar explícitamente.
2. `obs_id` es la unidad repetida; `q` es el caso que agrupa las subpreguntas.
3. En Agentic-RAG, `modelo` identifica solo al especialista; el recuperador es gpt-5 en todas las configuraciones.
4. La etiqueta `categoria_final` ya incorpora la revisión manual aceptada. No volver a aplicar la clasificación automática.
5. `R052` (`Q14_01`, sin RAG + gpt-5-mini) es `abstencion_explicita` en la base final, aunque el clasificador automático la haya marcado `sustantiva`.

## 5. Resumen de la base final

| Concepto | Valor |
|---|---:|
| Observaciones | 711 |
| Unidades | 79 |
| Casos | 25 |
| Celdas | 9 |
| Filas revisadas manualmente | 87 |
| Cambios de categoría por revisión | 1 (`R052`) |
| Salidas no sustantivas | 58 |
| Salidas sustantivas | 653 |
| Evaluaciones de jueces sobre no sustantivas | 174 |
| Puntajes de corrección > 0 sobre no sustantivas | 12 filas / 10 combinaciones / 9 unidades |
| Puntajes de precisión legal > 0 sobre no sustantivas | 5 filas |

Resumen completo: `salidas/resumen_ejecutivo_final.json`.

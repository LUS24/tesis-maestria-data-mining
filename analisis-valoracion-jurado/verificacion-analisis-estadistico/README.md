# Verificación independiente del acuerdo inter-juez — D-14

**Origen:** decisión `D-14` de `analisis-valoracion-jurado/correccion-05-actualizacion-conclusiones-y-analisis-costos/DECISIONES.md`.  
**Objetivo:** recalcular el alpha de Krippendorff desde los resultados originales de los jueces, sin editar ni leer como fuente la tabla derivada de la corrección 01 para el cálculo.  
**Fuente primaria:** `codigo_experimentos/part_i/final_judge_results.csv` (2.133 filas juez-observación).  
**Estado:** verificación ejecutada. **No se modificó ningún archivo fuente.**

## Reconciliación V.1/V.6 (NV-01)

El subdirectorio `reconciliacion_v1/` fija las cifras de V.1 y V.6 para Tabla 4. Usa los p Holm de `correccion-01` en V.1 y Wilcoxon de Pratt sobre las 38 respuestas sustantivas en V.6. Informe: `reconciliacion_v1/INFORME_RECONCILIACION.md`.

## Métricas de recuperación (NV-02)

El subdirectorio `metricas_recuperacion/` calcula recall@k, MRR y cobertura desde los 1.364 registros de `part_g`, con el baseline de `part_d`. Informe: `metricas_recuperacion/INFORME_METRICAS_RECUPERACION.md`.

## Resultado

| Rúbrica | Valores | Observaciones | Jueces | α ordinal |
| --- | --- | ---: | ---: | ---: |
| `score_respuesta_correcta` | originales | 711 | 3 | **0,807842** |
| `score_respuesta_correcta` | transformados a rúbrica | 711 | 3 | **0,799542** |
| `score_precision_legal` | originales | 711 | 3 | **0,784566** |
| `score_precision_legal` | transformados a rúbrica | 711 | 3 | **0,783985** |

Los valores de corrección coinciden con los publicados en la corrección 01: `0,807842` y `0,799542`. La verificación es independiente porque parte de `final_judge_results.csv`, no de la tabla larga `02_long_2133.csv`.

### Alpha por sistema

| Sistema | Observaciones | α corrección original | α corrección rúbrica | α precisión original |
| --- | ---: | ---: | ---: | ---: |
| Sin RAG | 237 | 0,6979 | 0,6922 | 0,6211 |
| RAG básico | 237 | 0,8219 | 0,8140 | 0,6389 |
| Agentic-RAG | 237 | 0,8693 | 0,8623 | 0,7550 |

### Correlaciones de Spearman

| Par | ρ | p |
| --- | ---: | ---: |
| Grok 4.1 Fast ↔ DeepSeek V3.1 | 0,8226 | 4,98 × 10⁻¹⁷⁶ |
| Grok 4.1 Fast ↔ Kimi K2 0905 | 0,8438 | 8,58 × 10⁻¹⁹⁴ |
| DeepSeek V3.1 ↔ Kimi K2 0905 | 0,7937 | 3,47 × 10⁻¹⁵⁵ |

### Controles de base

- 2.133 filas de jueces.
- 711 observaciones unidad × estrategia × modelo.
- 79 unidades únicas (preguntas/subpreguntas) anidadas en 25 casos.
- 3 jueces × 711 observaciones.
- 58 salidas no sustantivas; 41 en Agentic-RAG + gpt-5-nano.
- Costo total: USD 22,2939.

## Uso para D-01 y D-08

La decisión `D-01` indica que la corrección humana predomina sobre el juicio automático y que deben documentarse las discrepancias con el criterio humano. En los datos disponibles **no existen calificaciones humanas de las 711 respuestas del sistema**. La revisión humana documentada es la del benchmark (preguntas, respuestas esperadas y referencias), no una evaluación humana de las respuestas generadas. Por tanto:

- el alpha se reporta como **confiabilidad entre jueces**, no como acuerdo con criterio humano;
- no se puede afirmar que la “corrección humana” prevalga sobre los jueces en la medición de las respuestas;
- se entrega `datos/casos_discrepancia_para_revision_humana.csv` con **23 observaciones** donde los jueces difieren en al menos 0,75, para una eventual revisión humana;
- se entrega `datos/evaluaciones_positivas_salidas_no_sustantivas.csv` con **17 evaluaciones** positivas sobre salidas no sustantivas, para auditar el comportamiento de los jueces.

## Archivos

| Archivo | Contenido |
| --- | --- |
| `datos/alpha_global.csv` | Alpha global original y transformado |
| `datos/alpha_por_sistema.csv` | Alpha por sistema |
| `datos/spearman_pares.csv` | Correlaciones entre pares de jueces |
| `datos/resumen_conteos.csv` | Conteos de la base y costo total |
| `datos/casos_discrepancia_para_revision_humana.csv` | 23 casos con rango de jueces ≥ 0,75 |
| `datos/evaluaciones_positivas_salidas_no_sustantivas.csv` | Evaluaciones positivas sobre salidas no sustantivas |
| `datos/manifiesto_sha256.csv` | Hashes de las fuentes usadas |
| `salidas/resumen_verificacion.json` | Resumen completo de la verificación |
| `scripts/recalcular_acuerdo.py` | Script reproducible |
| `INFORME_VERIFICACION.md` | Informe metodológico y de resultados |

## Reproducción

Desde la raíz del repositorio:

```bash
cd analisis-valoracion-jurado/verificacion-analisis-estadistico
bash scripts/run_all.sh
```

El script no llama a APIs, no escribe fuera de este directorio y no modifica los archivos originales.

## Límites

- No se reajustó el modelo ordinal mixto; esta verificación cubre el acuerdo inter-juez y los insumos descriptivos que alimentan las conclusiones.
- No hay calificaciones humanas de las respuestas del sistema; la revisión humana del benchmark no sustituye esa validación.
- Los casos de discrepancia son una lista para revisión futura, no una calificación.
- El alpha no demuestra validez de contenido ni ausencia de sesgo compartido entre jueces.

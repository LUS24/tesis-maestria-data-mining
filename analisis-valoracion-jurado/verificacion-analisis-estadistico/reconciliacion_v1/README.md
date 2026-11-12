# Reconciliación V.1/V.6 — NV-01

Este directorio fija las cifras estadísticas que se usarán en Tabla 4 y en la discusión de resultados, después de comparar la valoración actualizada con `correccion-01`.

## Contenido

| Archivo | Contenido |
|---|---|
| `scripts/reconciliar_v1.py` | Recalcula Friedman, Wilcoxon/Holm por unidad y por caso, y las comparaciones de V.6. |
| `datos/01_comparaciones_v1_unidad.csv` | 18 comparaciones pareadas por unidad; las seis seleccionadas para V.1 están marcadas con `seleccionada=True`. |
| `datos/02_comparaciones_v1_caso.csv` | Las mismas comparaciones agregadas por caso (n = 25). |
| `datos/03_comparaciones_v6.csv` | Comparaciones de las 38 respuestas sustantivas de nano Agentic-RAG. |
| `datos/04_friedman.csv` | Friedman para RAG básico y para las estrategias en gpt-5. |
| `salidas/reconciliacion_v1.json` | Resultados, hashes y lectura metodológica. |
| `INFORME_RECONCILIACION.md` | Informe con tablas, discrepancias y cifras canónicas. |

## Reproducción

Desde la raíz del repositorio:

```bash
cd codigo_experimentos
uv run --frozen python ../analisis-valoracion-jurado/verificacion-analisis-estadistico/reconciliacion_v1/scripts/reconciliar_v1.py
```

El script no modifica fuentes ni artefactos de `correccion-01`; solo lee `01_wide_711.csv`, `02_long_2133.csv` y `33_friedman_principal.csv`.

## Decisión

- **V.1:** se usan los p Holm de `correccion-01` (Holm sobre las nueve comparaciones de cada familia).
- **V.6:** se usa Wilcoxon con `zero_method='pratt'` sobre las 38 respuestas sustantivas.
- Los p de la valoración se conservan como referencia ilustrativa y no reemplazan las cifras canónicas.

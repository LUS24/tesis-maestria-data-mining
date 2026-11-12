# Reconciliación de V.1 y V.6 — NV-01

**Estado:** ejecutada.  
**Fuente canónica:** `correccion-01-analisis-estadistico`.  
**Entrada:** `datos/01_wide_711.csv` (711 observaciones), contrastada con `datos/02_long_2133.csv` (2.133 filas juez-observación).  
**Script:** `scripts/reconciliar_v1.py`.  
**Salidas:** `datos/01_comparaciones_v1_unidad.csv`, `02_comparaciones_v1_caso.csv`, `03_comparaciones_v6.csv`, `04_friedman.csv` y `salidas/reconciliacion_v1.json`.

## 1. Qué se reconcilió

La valoración actualizada reporta cifras de V.1 y V.6 que no coinciden exactamente con los artefactos de `correccion-01`. La diferencia no está en la base —los conteos y las medias coinciden— sino en la prueba, la unidad de análisis, el manejo de empates/ceros y el universo de comparaciones corregidas.

Este informe fija cuatro reglas:

1. **V.1 se calcula sobre la unidad** (79 unidades) y usa **Holm sobre las nueve comparaciones de cada familia**, que es lo que hizo `correccion-01`.
2. **V.6 se calcula sobre las 38 respuestas sustantivas** de nano Agentic-RAG y compara las mismas unidades con gpt-5 Agentic-RAG y nano RAG básico.
3. Para V.6 se usa Wilcoxon de rangos con signo con `zero_method='pratt'`, porque es el método que reproduce los valores de la valoración.
4. Las cifras de la valoración son **ilustrativas**; para Tabla 4 se usan las cifras canónicas de `correccion-01` y, en V.6, los p de Pratt sobre las 38 unidades.

## 2. V.1 — pruebas pareadas por unidad

### 2.1. RAG básico: modelos

| Comparación | n | Diferencia media | p Wilcoxon | p Holm | p de la valoración |
|---|---:|---:|---:|---:|---:|
| nano − gpt-5 | 79 | −0,108 | 0,000887 | **0,003547** | 0,001 |
| nano − mini | 79 | −0,051 | 0,012942 | **0,038826** | 0,005 |
| mini − gpt-5 | 79 | −0,057 | 0,038412 | 0,076823 | — |

Friedman de los tres modelos: **χ² = 23,4273; gl = 2; p = 8,18 × 10⁻⁶**. Coincide con la valoración (χ² = 23,43; p < 0,001).

### 2.2. gpt-5: estrategias

| Comparación | n | Diferencia media | p Wilcoxon | p Holm | p de la valoración |
|---|---:|---:|---:|---:|---:|
| Agentic − RAG básico | 79 | +0,105 | 0,002904 | **0,011616** | 0,009 |
| Agentic − Sin RAG | 79 | +0,088 | 0,010213 | **0,030639** | 0,022 |
| RAG básico − Sin RAG | 79 | −0,018 | 0,726731 | 1,000000 | — |

Friedman de las tres estrategias en gpt-5: **χ² = 12,8824; gl = 2; p = 0,001595**.

### 2.3. Sensibilidad por caso (n = 25)

| Comparación | p Wilcoxon | p Holm |
|---|---:|---:|
| RAG básico: nano − gpt-5 | 0,023826 | 0,095302 |
| RAG básico: nano − mini | 0,025969 | 0,095302 |
| gpt-5: Agentic − RAG básico | 0,010513 | 0,052564 |
| gpt-5: Agentic − Sin RAG | 0,023992 | 0,095969 |

La agregación por caso **no reproduce** los `p = 0,008` y `p = 0,009` que menciona la valoración. Con la corrección de Holm sobre las nueve comparaciones, ninguna de esas diferencias queda por debajo de 0,05. Por eso la sensibilidad por caso no se usa como confirmación principal.

## 3. V.6 — las 38 respuestas sustantivas de nano Agentic-RAG

| Comparación en las mismas 38 unidades | Media 1 | Media 2 | Diferencia | p de Pratt | p de la valoración |
|---|---:|---:|---:|---:|---:|
| nano Agentic − gpt-5 Agentic | 0,8202 | 0,8421 | −0,0219 | **0,1894** | 0,19 |
| nano Agentic − nano RAG básico | 0,8202 | 0,6382 | +0,1820 | **0,002663** | 0,003 |

La media 0,82 de las 38 respuestas sustantivas coincide con la valoración. Los dos p se reproducen al redondear a dos y tres decimales, respectivamente.

## 4. Cifras canónicas para Tabla 4

| Bloque | Cifra canónica |
|---|---|
| RAG básico, Friedman | χ² = 23,4273; p = 8,18 × 10⁻⁶ |
| RAG básico, nano − gpt-5 | p Holm = 0,003547 |
| RAG básico, nano − mini | p Holm = 0,038826 |
| gpt-5, Friedman | χ² = 12,8824; p = 0,001595 |
| gpt-5, Agentic − RAG básico | p Holm = 0,011616 |
| gpt-5, Agentic − Sin RAG | p Holm = 0,030639 |
| V.6, nano Agentic − gpt-5 Agentic | p Pratt = 0,1894 |
| V.6, nano Agentic − nano RAG básico | p Pratt = 0,002663 |

**Regla:** no mezclar los p de la valoración con los p de `correccion-01`. Si se cita la valoración, decir que es un reanálisis ilustrativo; para la tesis, usar la tabla canónica anterior.

## 5. Por qué no coinciden exactamente

- La valoración no declara si usa la unidad, el caso o el promedio de jueces como estimando.
- No declara el tratamiento de empates ni de diferencias cero.
- No declara si Holm se aplica sobre tres comparaciones o sobre las nueve de la familia.
- Los p de V.1 de la valoración quedan entre los p sin corregir y los p Holm de `correccion-01`; no se pueden reproducir sin su código.
- En V.6, en cambio, el uso de Pratt sobre las 38 unidades reproduce los dos valores reportados.

## 6. Límites

- No se reajustó el modelo ordinal mixto; esta reconciliación cubre Friedman, Wilcoxon/Holm y la comparación condicional de V.6.
- No se modificaron fuentes, respuestas, evaluaciones ni artefactos históricos.
- La conclusión cualitativa no cambia: en RAG básico los modelos difieren; en gpt-5 Agentic-RAG supera a las dos alternativas; en nano Agentic-RAG la calidad condicional es alta pero solo en 38/79 unidades.

## 7. Reproducción

```bash
cd codigo_experimentos
uv run --frozen python ../analisis-valoracion-jurado/verificacion-analisis-estadistico/reconciliacion_v1/scripts/reconciliar_v1.py
```

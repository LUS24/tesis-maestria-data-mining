# Sensibilidad de D-02 a los umbrales — verificación

**Estado:** ejecutada.  
**Fuente:** `correccion-02-diagnostico-gpt-5-nano/salidas/14_dataset_categoria_final.csv` (711 observaciones).  
**Contraste:** `correccion-05-actualizacion-conclusiones-y-analisis-costos/datos/costo_por_respuesta_aceptable_umbrales.csv`.  
**Script:** `scripts/verificar_umbrales.py`.

## 1. Resultado

El recálculo independiente coincide exactamente con la tabla publicada por corrección 05:

- diferencia máxima en cantidad de respuestas correctas: **0**;
- diferencia máxima en costo por respuesta correcta: **0,0**.

Los tres umbrales ya estaban calculados en corrección 05. No hay una decisión nueva ni un cálculo faltante.

## 2. Mejor costo por respuesta correcta en cada umbral

| Umbral | Celda | Correctas | Costo total | Costo por correcta |
|---:|---|---:|---:|---:|
| ≥ 0,50 | Sin RAG + gpt-5-nano | 54/79 | USD 0,1981 | **USD 0,003668** |
| ≥ 0,75 | RAG básico + gpt-5-nano | 33/79 | USD 0,2011 | **USD 0,006095** |
| = 1,00 | RAG básico + gpt-5-nano | 16/79 | USD 0,2011 | **USD 0,012571** |

A umbral 0,50 el orden cambia: Sin RAG + nano es más barato por respuesta correcta porque las respuestas parciales cuentan. A 0,75 y 1,00, RAG básico + nano queda primero. En ningún umbral Agentic-RAG + nano es competitivo por respuesta correcta.

## 3. Lectura para D-02

- La definición principal sigue siendo **puntaje promedio ≥ 0,75**.
- Los umbrales 0,50 y 1,00 son **sensibilidad**, no definiciones alternativas.
- El orden de costo por respuesta correcta depende del umbral; por eso no se puede recomendar una celda sin declarar el umbral y el objetivo.
- El costo por respuesta correcta es una razón descriptiva; no es costo de producción ni una medida de calidad jurídica.

## 4. Archivos

| Archivo | Contenido |
|---|---|
| `datos/01_umbrales_recalculados.csv` | 27 filas: 9 celdas × 3 umbrales. |
| `datos/02_comparacion_correccion05.csv` | Contraste fila a fila con la tabla publicada. |
| `datos/03_top3_por_umbral.csv` | Tres menores costos por respuesta correcta en cada umbral. |
| `salidas/resumen_umbrales.json` | Hashes, deltas y mejor celda por umbral. |

## 5. Reproducción

```bash
cd codigo_experimentos
uv run --frozen python ../analisis-valoracion-jurado/verificacion-analisis-estadistico/sensibilidad_umbral/scripts/verificar_umbrales.py
```

No se modifican fuentes ni artefactos de corrección 05.

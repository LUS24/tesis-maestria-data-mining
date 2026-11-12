# Métricas de recuperación — NV-02

**Estado:** ejecutada.  
**Fuente de recuperaciones:** `codigo_experimentos/part_g/chat_data` (1.364 archivos `retrieval_history`).  
**Fuente de referencia:** `codigo_experimentos/part_d/20251012_retrieval_baseline_from_20250804_101435_generated_questions.json` (79 unidades; 166 artículos relevantes, 143 únicos).  
**Script:** `scripts/calcular_metricas.py`.

## Resultado principal

| Sistema | recall@10 | MRR | all@10 | none@10 | consultas promedio |
|---|---:|---:|---:|---:|---:|
| RAG básico (baseline `part_d`) | 0,3333 | 0,2143 | 27,85 % | 59,49 % | 1,00 |
| Agentic-RAG, especialista gpt-5 | 0,4148 | 0,2425 | 32,91 % | 45,57 % | 6,19 |
| Agentic-RAG, especialista gpt-5-mini | 0,3987 | 0,2635 | 32,91 % | 50,63 % | 5,66 |
| Agentic-RAG, especialista gpt-5-nano | 0,4464 | 0,2814 | 35,44 % | 44,30 % | 5,42 |

`recall@k` es la media por unidad de la proporción de artículos relevantes recuperados en el top-k. `all@10` y `none@10` son la proporción de unidades con todos o ningún artículo relevante en el top-10. `MRR` usa el primer artículo relevante.

El baseline reproduce las cifras previas del manuscrito: **recall@10 = 0,333; MRR = 0,214; 27,8 % con todos; 59,5 % sin ninguno**.

## Método

1. Se cargan las 79 unidades de referencia de `part_d` y sus `contexto_para_respuesta` (artículos relevantes).
2. Para el baseline se usan los `search_ranking` ya registrados por `part_d`; no se volvió a consultar Milvus.
3. Para Agentic-RAG se leen los `retrieval_history/*.json` de cada unidad y modelo. Los documentos se deduplican por `id_parte` y se ordenan por la secuencia de consultas registrada.
4. Se calculan `recall@1/5/10/20`, `hit@k`, `all@k`, `none@k` y `MRR`.
5. Se repite la comparación por `numero_parte` como control; el resultado principal usa `id_parte`.

## Archivos

| Archivo | Contenido |
|---|---|
| `datos/01_metricas_por_unidad.csv` | 79 unidades × 4 sistemas, más el control por número. |
| `datos/02_consultas_por_unidad.csv` | Consultas y documentos únicos por unidad y modelo. |
| `datos/03_resumen_modelos.csv` | Agregados por sistema. |
| `salidas/resumen_metricas_recuperacion.json` | Resumen, definiciones, hashes y límite. |

## Lectura

- Agentic-RAG mejora el recall@10 y el MRR respecto del baseline en los tres modelos del especialista.
- La mejora es moderada: el mejor recall@10 es 0,446 y el mejor MRR 0,281.
- gpt-5-nano obtiene el mejor recall@10 y MRR, pero también es el que menos consultas promedio realiza (5,42).
- La comparación **no es un experimento controlado de recuperadores**: el baseline usa una consulta y Agentic-RAG usa varias; el presupuesto de recuperación y el número de documentos únicos difieren. Sirve para describir el comportamiento registrado, no para atribuir causalmente la mejora a la arquitectura.
- No se comparó con BM25 ni con otro embedding porque el volumen de Milvus se perdió y no se recreó la base. Las cifras de `part_d` son el único baseline disponible.

## Reproducción

```bash
cd codigo_experimentos
uv run --frozen python ../analisis-valoracion-jurado/verificacion-analisis-estadistico/metricas_recuperacion/scripts/calcular_metricas.py
```

El script no modifica fuentes, logs, respuestas ni la base vectorial.

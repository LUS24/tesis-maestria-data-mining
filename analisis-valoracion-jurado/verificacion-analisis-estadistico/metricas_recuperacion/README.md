# Métricas de recuperación (NV-02)

Este directorio calcula las métricas de recuperación desde los registros de `part_g` y las compara con el baseline de `part_d`.

- Informe: [`INFORME_METRICAS_RECUPERACION.md`](INFORME_METRICAS_RECUPERACION.md)
- Script: [`scripts/calcular_metricas.py`](scripts/calcular_metricas.py)
- Resumen: [`salidas/resumen_metricas_recuperacion.json`](salidas/resumen_metricas_recuperacion.json)
- Tabla agregada: [`datos/03_resumen_modelos.csv`](datos/03_resumen_modelos.csv)

Reproducción:

```bash
cd codigo_experimentos
uv run --frozen python ../analisis-valoracion-jurado/verificacion-analisis-estadistico/metricas_recuperacion/scripts/calcular_metricas.py
```

No se consulta Milvus ni se modifican fuentes o logs.

# Sensibilidad de umbrales (D-02)

Verifica los umbrales 0,50/0,75/1,00 del costo por respuesta correcta.

- Informe: [`INFORME_SENSIBILIDAD_UMBRAL.md`](INFORME_SENSIBILIDAD_UMBRAL.md)
- Script: [`scripts/verificar_umbrales.py`](scripts/verificar_umbrales.py)
- Resumen: [`salidas/resumen_umbrales.json`](salidas/resumen_umbrales.json)
- Tabla completa: [`datos/01_umbrales_recalculados.csv`](datos/01_umbrales_recalculados.csv)

Reproducción:

```bash
cd codigo_experimentos
uv run --frozen python ../analisis-valoracion-jurado/verificacion-analisis-estadistico/sensibilidad_umbral/scripts/verificar_umbrales.py
```

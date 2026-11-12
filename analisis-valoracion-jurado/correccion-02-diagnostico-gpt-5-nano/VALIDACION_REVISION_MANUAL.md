# Acta de validación y decisión — revisión manual aceptada

**Punto:** IX.1.2.  
**Fecha de aceptación:** 2026-11-12.  
**Plantilla canónica:** `revision_manual/plantilla_resultados.csv`.  
**Versión previa preservada:** `revision_manual/plantilla_resultados_pre_aceptacion.csv`.  
**Base final para IX.1.1:** `salidas/14_dataset_categoria_final.csv`.

---

## 1. Decisión

Se acepta la revisión manual corregida. En particular:

- **`R002`** (`Q22_02`, sin RAG + gpt-5-mini) se acepta como **`abstencion_explicita`**. El modelo declara explícitamente que no puede afirmar las consecuencias sin consultar la norma; ofrecer buscar el texto no constituye una respuesta sustantiva.
- **`R052`** (`Q14_01`, sin RAG + gpt-5-mini) se acepta como **`abstencion_explicita`**. El clasificador automático la había marcado `sustantiva`; la etiqueta manual es la correcta.
- **`R017`** se acepta como `sustantiva`, con la justificación “Respuesta sustantiva que cita el artículo 324 del Código de Minería y describe las consecuencias de la conducta.”
- Las 27 justificaciones de salidas `vacia` se completaron con “Cadena vacía.”.

La plantilla previa a la aceptación se conserva para trazabilidad. La plantilla canónica ya contiene la versión aceptada.

---

## 2. Validación final

| Control | Resultado |
|---|---:|
| Filas esperadas | 87 |
| Filas presentes | 87 |
| `review_id` únicos | 87 |
| Categorías completas | 87 |
| Categorías inválidas | 0 |
| Justificaciones vacías | **0** |
| Revisores vacíos | 0 |
| Fechas vacías o con formato inválido | 0 |
| Acuerdo automático–manual | **98,9%** |
| Discrepancias | **1** |

La única discrepancia es `R052`: el clasificador automático la marcó `sustantiva` y la revisión manual la marcó `abstencion_explicita`. Se acepta la etiqueta manual. **No debe “corregirse” a `sustantiva`.**

---

## 3. Impacto en la base final

| Concepto | Clasificación automática | Base final aceptada |
|---|---:|---:|
| Salidas no sustantivas totales | 57 | **58** |
| Evaluaciones de jueces sobre no sustantivas | 171 | **174** |
| Puntajes de corrección > 0 | 11 filas / 9 combinaciones / 8 unidades | **12 filas / 10 combinaciones / 9 unidades** |
| Puntajes de precisión legal > 0 | 5 filas | **5 filas** |
| Sin RAG + gpt-5-mini: sustantivas | 65 | **64** |
| Sin RAG + gpt-5-mini: no sustantivas | 14 abstenciones | **15 abstenciones** |
| Sin RAG + gpt-5-mini: mediana condicional | 0,333 (n=65) | **0,375 (n=64)** |
| Agentic-RAG + gpt-5-nano: no sustantivas | 41 | **41** (sin cambios) |

La mediana completa de sin RAG + gpt-5-mini sigue siendo 0,250; la mediana condicional a respuestas sustantivas pasa a 0,375.

---

## 4. Historial de la revisión

La versión original de la plantilla tenía:

- 87 categorías completas;
- 28 justificaciones vacías;
- 97,7% de acuerdo automático–manual;
- 2 discrepancias: `R002` (`indeterminada`) y `R052` (`abstencion_explicita`).

La versión corregida sugerida y luego aceptada tiene:

- 87 categorías completas;
- 0 justificaciones vacías;
- 98,9% de acuerdo;
- 1 discrepancia: `R052`, que es un error del clasificador automático.

La decisión y los cambios están documentados en:

- `salidas/revision_manual_correcciones_sugeridas.csv`;
- `salidas/revision_manual_resumen_aceptada.csv`;
- `salidas/revision_manual_discrepancias_aceptada.csv`;
- `salidas/revision_manual_resumen_original.csv` (histórico);
- `salidas/revision_manual_discrepancias_original.csv` (histórico).

---

## 5. Revisor

`revisor = autor` en las 87 filas. El paquete no contenía estrategia, modelo ni categoría automática, pero **la revisión no es independiente**: el autor conoce el corpus y puede reconocer respuestas.

Para IX.1.1, la etiqueta manual es utilizable y debe documentarse como **revisión del autor**. No debe presentarse como validación humana independiente. Para la tesis, si se requiere independencia, otra persona debería repetir la revisión ciega o una submuestra.

---

## 6. Uso en IX.1.1

La base final es:

`salidas/14_dataset_categoria_final.csv`

Contiene 711 observaciones y estas columnas principales:

- `categoria_auto`, `subcategoria_auto`: clasificación automática original;
- `categoria_manual`, `justificacion_manual`, `revision_manual_id`: revisión aceptada;
- `categoria_final`, `subcategoria_final`, `fuente_categoria`: etiqueta que debe usarse;
- `puntaje_final_original`, `puntaje_final_fallo_cero`,
  `puntaje_final_solo_fallos_tecnicos_cero`, `puntaje_final_exclusion`: escenarios de puntuación.

**No usar `01_dataset_derivado_711.csv` como base final**: conserva la clasificación automática y mantiene `R052` como sustantiva. Esa tabla queda como histórico reproducible.

Resumen final:

`salidas/15_resumen_por_celda_final.csv`  
`salidas/17_auditoria_jueces_salidas_no_sustantivas_final.csv`  
`salidas/resumen_ejecutivo_final.json`

---

## 7. Comandos

Validar la plantilla canónica aceptada:

```bash
uv run --project codigo_experimentos --no-sync --frozen \
  python analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/src/validar_revision_manual.py
```

Reconsolidar la base final:

```bash
uv run --project codigo_experimentos --no-sync --frozen \
  python analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/src/consolidar_revision_manual.py
```

Regenerar todo:

```bash
bash analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/reproducir.sh
```

---

## 8. Veredicto

**La revisión manual está aceptada y la base final está lista para IX.1.1.** Las categorías son completas, las justificaciones están completas, el acuerdo automático–manual es 98,9% y la única discrepancia remanente es un error conocido del clasificador automático (`R052`). La revisión es del autor, no independiente; debe declararse así en el manuscrito.

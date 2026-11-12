# Corrección 02 — Diagnóstico de Agentic-RAG + gpt-5-nano

Esta carpeta contiene los artefactos para resolver el punto **IX.1.2** del plan de correcciones: diagnosticar la celda Agentic-RAG + gpt-5-nano, los datos faltantes y reformular la interpretación de “sobrecarga agéntica”.

**No se modificó ningún archivo fuente.** Las respuestas, logs, JSON, CSV, PDF y bases SQLite históricas se leyeron en modo de solo lectura. Todo lo nuevo está en esta carpeta.

---

## Resultado principal

- Las **27 medias ausentes** no son 27 fallos de generación: son las unidades 23, 24 y 25 en las 9 configuraciones, no enlazadas porque el CSV de métricas usa subpregunta vacía y el de jueces usa `0`. Al normalizar la clave se recuperan **711 observaciones** y **2.133 evaluaciones de jueces**.
- Agentic-RAG + gpt-5-nano tiene **41 salidas no sustantivas de 79** (51,9%; IC 95% Wilson 41,1–62,6%):
  - 27 vacías;
  - 1 solo espacios;
  - 2 abstenciones explícitas;
  - 1 truncada;
  - 10 indeterminadas (mensajes de proceso, `TEST`, `placeholder`, `PENDING`, mensaje interno).
- Los 79 logs tienen una llamada a `retrieve_relevant_documents` y al menos una a `final_result` (77 con una sola; 2 con más de una); el `finish_reason` del especialista es `tool_call` en los 79 casos. Las salidas vacías tienen recuperación (1–12 documentos seleccionados) y tokens (575–7.015 de salida). **No hay evidencia de falta de recuperación ni de truncamiento por tokens.**
- Cuando la celda produce una respuesta sustantiva (**38/79**), la calidad es alta: **media 0,820; mediana 0,958**.
- Con **fallo = 0**, la celda completa tiene media 0,395 y mediana 0,000. Con **exclusión**, media 0,820 y mediana 0,958.
- La diferencia Agentic-RAG − RAG básico en nano cambia de signo: **−0,205 con fallo = 0** y **+0,182 con exclusión** (38 pares). La exclusión es una submuestra seleccionada; no es un efecto causal.
- Los jueces asignaron **11 puntajes de corrección > 0** (9 combinaciones celda-unidad; 8 unidades distintas) y **5 puntajes de precisión legal > 0** a salidas no sustantivas. Varias justificaciones citan artículos que no están en la respuesta. Esos puntajes deben auditarse, no promediarse como calidad.
- La tabla de medianas del manuscrito se calculó sobre **76 observaciones por celda**, no 79. Al recuperar el join cambian 5 de las 9 medianas. La celda nano pasa de **0,083** a **0,250** con los jueces originales, a **0,000** con fallo = 0 y a **0,958** con exclusión.

---

## Archivos

```
.
├── README.md
├── RESUMEN_PARA_REVISION.md       # guía breve de revisión
├── INFORME_DIAGNOSTICO.md          # hallazgos, tablas e interpretación
├── PROPUESTAS_MANUSCRITO.md        # texto sugerido para los .typ y README
├── diagnostico_gpt5_nano.ipynb     # notebook ejecutado, sin errores
├── reproducir.sh                   # regenera tablas y figuras
├── src/
│   ├── diagnostico.py              # código reproducible
│   └── validar_revision_manual.py  # consolida la revisión ciega
├── salidas/                        # tablas, JSON y evidencia
├── figuras/                        # PDF y PNG
└── revision_manual/                # paquete ciego y plantilla
```

### Tablas principales

| Archivo | Contenido |
|---|---|
| `salidas/01_dataset_derivado_711.csv` | 711 observaciones con categorías, jueces, escenarios y logs. |
| `salidas/02_resumen_por_celda.csv` | Resumen por celda con tasas e IC 95%. |
| `salidas/03_conteo_categorias_por_celda.csv` | Conteo largo de las siete categorías. |
| `salidas/03b_tabla_categorias_ancha.csv` | Tabla ancha lista para el manuscrito. |
| `salidas/04_auditoria_faltantes_join.csv` | Las 27 medias recuperadas. |
| `salidas/05_auditoria_jueces_salidas_no_sustantivas.csv` | 171 evaluaciones sobre salidas no sustantivas. |
| `salidas/06_logs_agentes_237.csv` | Logs parseados de las 237 respuestas agénticas. |
| `salidas/07_resumen_logs_por_modelo.csv` | Resumen de logs por modelo. |
| `salidas/08_comparacion_medianas_manuscrito.csv` | Manuscrito vs. 76 vs. 79 vs. escenarios. |
| `salidas/09_sensibilidad_pares_estrategias.csv` | Comparaciones pareadas exploratorias. |
| `salidas/10_sin_rag_nano_vs_mini.csv` | Comparación descriptiva sin RAG. |
| `salidas/11_celda_nano_agentic_79.csv` | Las 79 filas de la celda, con evidencia textual y de log. |
| `salidas/12_auditoria_27_medias_ausentes.csv` | Copia específica de la auditoría de join. |
| `salidas/13_salidas_no_sustantivas_con_evidencia.csv` | Las 57 no sustantivas con evidencia. |
| `salidas/lista_verificacion_no_sustantivas.csv` | Lista asistida para revisión. |
| `salidas/mapa_revision_ciega.csv` | Mapa `review_id` → observación. **No abrir hasta terminar la revisión ciega.** |
| `salidas/resumen_ejecutivo.json` | Resumen numérico legible por máquina. |

### Figuras

| Archivo | Contenido |
|---|---|
| `figuras/01_composicion_respuestas_por_celda.*` | Composición de las 9 celdas por categoría. |
| `figuras/02_tasas_fallo_por_celda.*` | Tasa de salidas no sustantivas con IC 95%. |
| `figuras/03_estados_nano_agentic.*` | Desglose de las 79 salidas de nano. |
| `figuras/04_puntajes_jueces_salidas_no_sustantivas.*` | Puntajes de jueces sobre no sustantivas. |
| `figuras/05_logs_tokens_y_recuperacion_nano.*` | Tokens y recuperación por estado de salida. |
| `figuras/06_escenarios_nano.*` | Original vs. fallo = 0 vs. exclusión. |
| `figuras/07_sim_rag_nano_vs_mini.*` | Distribución sin RAG nano vs. mini. |

Las figuras están en PDF vectorial y PNG para revisión rápida.

---

## Reproducción

Desde la raíz del repositorio:

```bash
uv run --project codigo_experimentos --no-sync --frozen \
  python analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/src/diagnostico.py
```

O:

```bash
bash analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/reproducir.sh
```

El script:

- lee los archivos fuente sin modificarlos;
- escribe todas las salidas en `salidas/` y `figuras/`;
- valida 711 observaciones, 79 unidades, 9 celdas y 2.133 filas de jueces;
- no llama a APIs ni a modelos.

El notebook `diagnostico_gpt5_nano.ipynb` ya está ejecutado sin errores. Para volver a ejecutarlo se necesita `nbformat`/`nbclient`; el entorno de `codigo_experimentos` contiene las dependencias de análisis.

---

## Revisión manual

`revision_manual/paquete_revision_ciega.csv` contiene 87 filas:

- las 57 salidas no sustantivas;
- 30 respuestas sustantivas de control, estratificadas por celda;
- orden aleatorio y sin etiquetas de estrategia, modelo o categoría.

El revisor debe completar `categoria_revisada` y `justificacion` en `revision_manual/plantilla_resultados.csv`. Las definiciones están en `revision_manual/LEEME.md`.

Después de completar la plantilla:

```bash
uv run --project codigo_experimentos --no-sync --frozen \
  python analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/src/validar_revision_manual.py
```

Esto genera `salidas/revision_manual_resumen.csv` y `salidas/revision_manual_discrepancias.csv`. No modifica la plantilla ni el paquete ciego.

La revisión manual **no** evalúa corrección jurídica: solo decide si hay una respuesta sustantiva y, si no, en qué categoría cae. La validación jurídica con profesionales es IX.2.3.

---

## Límites de este diagnóstico

- La clasificación de las 57 no sustantivas es automática y debe confirmarse con la revisión ciega. Las 27 vacías y la salida de solo espacios son inequívocas; los 10 indeterminados y las 2 abstenciones requieren revisión.
- Los logs no registran el payload HTTP completo ni el esfuerzo de razonamiento efectivo. No se puede afirmar por qué el modelo devolvió un `final_result` vacío. IX.1.3 trata esa limitación.
- No hay réplicas ni ablación. No se puede saber si el fallo es estable entre corridas ni si depende del modelo del recuperador, del prompt o de otra diferencia entre estrategias.
- La comparación de respuestas sustantivas está condicionada a una submuestra seleccionada; no es el efecto causal de Agentic-RAG.
- La comparación sin RAG nano vs. mini es descriptiva. No demuestra una relación causal con la capacidad del modelo.
- La auditoría de jueces detecta inconsistencias claras, pero no cuantifica la validez de los jueces frente a criterio humano. Eso requiere IX.2.3.

---

## Estado

- [x] Dataset derivado de 711 observaciones.
- [x] Auditoría del join de 27 medias.
- [x] Clasificación de las 711 respuestas.
- [x] Diagnóstico de logs de la celda nano.
- [x] Auditoría de jueces sobre no sustantivas.
- [x] Sensibilidad fallo = 0 / exclusión.
- [x] Figuras y notebook ejecutado.
- [x] Informe y propuestas de redacción.
- [ ] Revisión manual ciega (a cargo del autor/revisor).
- [ ] Edición del manuscrito (no realizada en esta carpeta).

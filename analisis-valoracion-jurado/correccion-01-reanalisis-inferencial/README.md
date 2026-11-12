# Corrección IX.1.1 — Reanálisis inferencial

Esta carpeta resuelve el punto **IX.1.1** del plan: rehacer el análisis inferencial respetando el apareamiento por unidad y el anidamiento en casos, con tamaños de efecto e intervalos de confianza.

**No se modificó ningún archivo fuente, log, respuesta o evaluación histórica.** Todo lo nuevo está en esta carpeta. El análisis no llama a APIs.

---

## Qué revisar primero

1. **`INFORME_REANALISIS.md`** — resultados, interpretación y límites.
2. **`PROPUESTA_TEXTO_MANUSCRITO.md`** — reemplazos sugeridos para metodología, resultados y conclusiones.
3. **`PROTOCOLO_ANALISIS.md`** — decisiones preespecificadas y justificación de las pruebas.
4. **`salidas/30_tabla_celdas_principal.csv`** y **`salidas/31_efectos_simples_orientados.csv`** — tablas listas para revisar.
5. **`figuras/02_interaccion_prob_ge_075.png`** y **`figuras/04_sensibilidad_escenarios.png`** — patrón visual.

---

## Resultado principal

- La base tiene **711 observaciones**, **79 unidades**, **25 casos** y **2.133 evaluaciones juez-observación**. Las 27 medias que faltaban en el manuscrito se recuperan: eran un problema de join entre subpregunta vacía y `0`, no 27 fallos de generación.
- El modelo ordinal mixto principal (no sustantivas = 0) muestra una interacción muy fuerte: **LR = 293,00; gl = 4; p = 3,50 × 10⁻⁶²**.
- Bajo el escenario principal:
  - **gpt-5-nano + Agentic-RAG** es peor que RAG básico: diferencia modelada de **−0,270** (IC 95% −0,330 a −0,203).
  - **gpt-5-mini + Agentic-RAG** es mejor que RAG básico: **+0,150** (0,097 a 0,203).
  - **gpt-5 + Agentic-RAG** es mejor que RAG básico: **+0,106** (0,054 a 0,157). Esto cambia la conclusión anterior de “sin diferencias en gpt-5”.
- La celda nano Agentic-RAG concentra **41/79 respuestas no sustantivas**. Cuando responde, su calidad es alta (media 0,820; mediana 0,958; n = 38), pero como sistema completo falla en más de la mitad de las unidades.
- Por eso el contraste nano Agentic-RAG − RAG básico **cambia de signo** según el escenario: **−0,270** con fallo = 0 y **+0,215** con exclusión. No es una contradicción: mide dos preguntas distintas (utilidad del sistema vs. calidad condicional).
- **No se sostiene** “efecto igualador del RAG básico”, “sobrecarga agéntica” como causa, ni equivalencia por falta de significación. La interacción es robusta, pero la interpretación debe ser condicional y no causal.

---

## Estructura

```
correccion-01-reanalisis-inferencial/
├── README.md
├── INFORME_REANALISIS.md
├── PROPUESTA_TEXTO_MANUSCRITO.md
├── PROTOCOLO_ANALISIS.md
├── run_all.sh
├── instalar_dependencias_R.sh
├── src/
│   ├── build_dataset.py              # base 711 / 2.133
│   ├── run_nonparametric.py          # Friedman, Wilcoxon, bootstrap por casos
│   ├── run_ordinal_model.R           # clmm, efectos simples, sensibilidades
│   ├── make_figures.py
│   ├── summarize_results.py
│   ├── validate_artifacts.py
│   └── make_typst_tables.py          # tablas Typst de borrador
├── datos/                            # bases derivadas nuevas
├── salidas/                          # tablas, JSON y logs
├── figuras/                          # PDF y PNG
├── propuestas/                       # tablas Typst y preview PDF
└── modelos/                          # modelo principal .rds
```

### Tablas principales

| Archivo | Contenido |
|---|---|
| `datos/01_wide_711.csv` | Una fila por unidad × estrategia × modelo |
| `datos/02_long_2133.csv` | Una fila por juez × observación |
| `salidas/10_resumen_celdas_escenarios.csv` | Descriptivos y bootstrap por escenario |
| `salidas/11_friedman.csv` | Friedman y W de Kendall |
| `salidas/12_wilcoxon_posthoc.csv` | Wilcoxon, Holm, rango-biserial y bootstrap |
| `salidas/20_modelo_interaccion.csv` | Interacción y varianzas |
| `salidas/21_modelo_coeficientes.csv` | Coeficientes y odds ratios |
| `salidas/22_modelo_predicciones_celdas.csv` | Predicciones por celda |
| `salidas/23_efectos_simples_latentes.csv` | Contrastes latentes y Holm |
| `salidas/24_efectos_simples_probabilidad.csv` | Diferencias de media y P≥0,75 |
| `salidas/30_tabla_celdas_principal.csv` | Tabla principal |
| `salidas/31_efectos_simples_orientados.csv` | Efectos en orden intuitivo |
| `salidas/32_tabla_sensibilidad_nano.csv` | Sensibilidad de nano |
| `salidas/35_resultados_clave.json` | Números principales |
| `propuestas/preview_tablas.pdf` | Previsualización Typst de las tablas principales |

---

## Reproducción

Desde la raíz del repositorio:

```bash
bash analisis-valoracion-jurado/correccion-01-reanalisis-inferencial/run_all.sh
```

Si es la primera vez y faltan los paquetes de R:

```bash
bash analisis-valoracion-jurado/correccion-01-reanalisis-inferencial/instalar_dependencias_R.sh
```

El script:

- lee las fuentes en modo de solo lectura;
- escribe únicamente en esta carpeta;
- valida 711 observaciones, 79 unidades, 9 celdas y 2.133 filas de jueces;
- no llama a OpenAI, OpenRouter ni Milvus.

---

## Revisión manual pendiente

La clasificación de respuestas no sustantivas es la automática de la corrección 02 porque `revision_manual/plantilla_resultados.csv` todavía no está completa. `datos/00_estado_revision_manual.json` registra el estado. El paquete de revisión cubre las 57 no sustantivas automáticas y 30 controles; no es un censo de las 654 respuestas sustantivas.

Cuando la plantilla esté completa, ejecutar de nuevo `run_all.sh`. `build_dataset.py` usará las categorías revisadas y dejará constancia en `fuente_clasificacion`. No se mezclan filas manuales y automáticas: si la plantilla no está completa, se usa la clasificación automática para todas.

---

## Límites

- Una ejecución por celda: no hay réplicas; el modelo no estima variabilidad entre corridas.
- La imputación a 0 es una decisión normativa sobre la utilidad del sistema, no una medición de calidad jurídica.
- La exclusión es una submuestra seleccionada; no es un efecto causal.
- El recuperador agéntico es siempre gpt-5 y gpt-5 usó 7 búsquedas frente a 6 de mini/nano (corrección 04). El modelo no separa esos confundidos.
- No hay validación humana de los jueces ni de las respuestas esperadas en este paquete.

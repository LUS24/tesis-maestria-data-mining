# Corrección IX.1.5 — actualización de conclusiones y análisis de costos

**Punto:** reformular todas las conclusiones de la Tabla 4 de la valoración del jurado, actualizar las conclusiones del manuscrito/README y reemplazar el índice de eficiencia por un análisis de costos defendible.  
**Fecha:** 2026-11-12.  
**Estado:** artefactos listos para revisión; **no se editó ningún `.typ`, README, JSON, CSV, log o evaluación histórica**.

## Qué revisar primero

1. **`DECISIONES.md`** — decisiones que deben aceptarse antes de redactar. Si se aceptan las recomendaciones, las propuestas pueden aplicarse sin recalcular nada.
2. **`TABLA_4_REFORMULADA.md`** — las nueve conclusiones originales, su estado y la formulación propuesta, con evidencia y límites.
3. **`PROPUESTA_TEXTO_MANUSCRITO.md`** — reemplazos exactos para resumen, introducción, evaluación, conclusiones y anexo.
4. **`ANALISIS_COSTOS.md`** — costos, costo por respuesta aceptable, frontera de Pareto y verificación de la recomendación anterior.
5. **`PROPUESTA_TEXTO_README.md`** — cambios de hallazgos, métricas, análisis estadístico y agradecimientos.
6. **`INFORME_SINTESIS_CONCLUSIONES.md`** — qué se conserva, qué se reformula y qué se retira, con la evidencia de las correcciones 01–07.

## Resultado principal

- La interacción estrategia × modelo se mantiene: **LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²**. No se interpreta como efecto causal de un componente aislado.
- En el escenario principal (fallo = 0):
  - Agentic-RAG es **inferior** a RAG básico en gpt-5-nano: **−0,270** (IC 95% −0,330 a −0,202).
  - Agentic-RAG es **superior** en gpt-5-mini: **+0,150** (IC 95% 0,096 a 0,203).
  - Agentic-RAG es **superior** en gpt-5: **+0,106** (IC 95% 0,054 a 0,155). Esto corrige la conclusión anterior de “sin diferencias en gpt-5”.
- **No se sostiene el “efecto igualador”**: con RAG básico las diferencias observadas son menores, pero no desaparecen; los IC no establecen equivalencia.
- **No se sostiene la “sobrecarga agéntica” como causa**: Agentic-RAG + gpt-5-nano tiene 41/79 salidas no sustantivas; cuando responde, la calidad es alta (38/79; media 0,820; mediana 0,958).
- **No se sostiene “LLM-as-a-Judge validado”**: α = 0,808/0,800 mide acuerdo, no validez humana; además hay puntajes positivos sobre salidas no sustantivas.
- **No se sostiene “Agentic-RAG + mini es costo-eficiente”** en sentido absoluto: cuesta USD 0,0564/consulta, más que RAG básico + gpt-5 (USD 0,0392) y Sin RAG + gpt-5 (USD 0,0478). Es una opción no dominada, no la más barata.
- **RAG básico + gpt-5-nano** tiene el menor costo puntual por respuesta aceptable (≥ 0,75): USD 0,0061 (33/79; media 0,599); su IC bootstrap se solapa con Sin RAG + nano, por lo que no se establece una diferencia formal entre ambas. **Agentic-RAG + gpt-5** tiene la mayor media (0,812; USD 0,0792; 56/79).
- **El objetivo 2 es parcial**: dos agentes activos, una delegación, sin verificador; el Agente de Calidad nunca se ejecutó. **El repositorio es público**, pero la clonación limpia final sigue pendiente.

## Estructura

```text
correccion-05-actualizacion-conclusiones-y-analisis-costos/
├── README.md                         # este archivo
├── DECISIONES.md                     # D-01 a D-14
├── TABLA_4_REFORMULADA.md            # las 9 conclusiones del jurado
├── PROPUESTA_TEXTO_MANUSCRITO.md     # reemplazos para los .typ
├── PROPUESTA_TEXTO_README.md         # reemplazos para README.md
├── ANALISIS_COSTOS.md                # costos, Pareto, costo por aceptable
├── INFORME_SINTESIS_CONCLUSIONES.md  # integración de correcciones 01–07
├── scripts/
│   ├── build_cost_analysis.py        # análisis de costos y figuras
│   ├── build_conclusion_tables.py    # tablas de trazabilidad
│   ├── verify_artifacts.py           # controles de consistencia
│   └── run_all.sh                    # reproducción completa
├── datos/
│   ├── costos_por_celda.csv
│   ├── costos_por_estrategia.csv
│   ├── costo_por_respuesta_aceptable_umbrales.csv
│   ├── frontera_pareto.csv
│   ├── comparacion_recomendacion_anterior.csv
│   ├── tabla4_reformulada.csv
│   ├── matriz_evidencia.csv
│   ├── ubicaciones_texto.csv
│   ├── frases_a_eliminar.csv
│   └── manifiesto_entradas.csv
├── figuras/
│   ├── 01_costo_vs_desempenio_pareto.pdf/.png
│   └── 02_costo_por_aceptable.pdf/.png
├── salidas/
│   ├── resumen_costos.json
│   └── resumen_conclusiones.json
└── propuestas/
    └── vista_previa_tabla4_y_costos.pdf
```

## Cómo reproducir

Desde la raíz del repositorio:

```bash
cd analisis-valoracion-jurado/correccion-05-actualizacion-conclusiones-y-analisis-costos
bash scripts/run_all.sh
```

El script:

- lee las fuentes en modo de solo lectura;
- escribe únicamente en esta carpeta;
- no llama a APIs;
- valida 711 observaciones, 9 celdas, 79 unidades por celda y 2.133 evaluaciones;
- regenera las tablas y figuras;
- compila la vista previa Typst.

## Decisiones que bloquean la redacción

Las más importantes:

- **D-01:** escenario principal fallo = 0 (recomendado).
- **D-04:** reemplazar “costo-eficiente” por Pareto y objetivo explícito.
- **D-05:** reemplazar “sobrecarga agéntica” por “modo de fallo de respuesta”.
- **D-07:** congelar el benchmark v1 y documentar v2 como versión futura.
- **D-08:** declarar que no hay validación humana de los jueces.
- **D-09:** cambiar el título o declarar el alcance expreso.
- **D-10:** declarar el objetivo 2 como cumplimiento parcial.
- **D-11:** declarar acceso público verificado y reproducción final pendiente.

El resto está en `DECISIONES.md`, con opciones, recomendación, impacto y evidencia.

## Reglas respetadas

- No se modificó ningún archivo existente.
- No se alteraron respuestas, logs, evaluaciones ni metadatos.
- Los 27 valores ausentes del análisis original se tratan como un problema de join (`vacío`/`None` frente a `0`), no como 27 fallos de generación.
- Las 41 salidas no sustantivas de Agentic-RAG + nano se tratan como un fenómeno distinto de las 27 medias ausentes.
- Los costos son históricos y no se actualizaron a precios corrientes.
- La exclusión de no sustantivas es una sensibilidad, no un efecto causal.

## Estado de revisión

- [x] Costos por celda, estrategia y umbral.
- [x] Frontera de Pareto y costo por aceptable.
- [x] Tabla 4 reformulada (9 filas).
- [x] Propuestas para resumen, evaluación y conclusiones.
- [x] Propuestas para README.
- [x] Matriz de evidencia y frases a eliminar.
- [x] Decisiones separadas.
- [ ] Edición del manuscrito (fuera de esta carpeta).
- [ ] Validación humana de los jueces (IX.2.3).
- [ ] Réplicas y ablación (IX.2.4).
- [ ] Clonación anónima final y compilación.

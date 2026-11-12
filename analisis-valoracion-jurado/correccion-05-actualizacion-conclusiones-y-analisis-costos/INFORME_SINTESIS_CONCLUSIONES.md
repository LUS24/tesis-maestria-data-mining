# Síntesis de evidencia para actualizar las conclusiones

**Corrección:** IX.1.5.  
**Pregunta:** ¿qué conclusiones del manuscrito se sostienen, cuáles deben reformularse y cuáles deben retirarse a la luz de las correcciones IX.1.1–IX.1.8?  
**Respuesta breve:** se sostiene el patrón de interacción; se retiran la equivalencia por falta de significación, la “sobrecarga agéntica” como causa, la “validación” de los jueces, la recomendación costo-eficiente y la transferibilidad. Varias conclusiones deben volverse condicionales al modelo, al escenario de fallo y al benchmark v1.

---

## 1. Evidencia incorporada

Este paquete no reemplaza las correcciones anteriores: las integra. Las fuentes principales son:

| Corrección | Aporte para las conclusiones | Artefacto de referencia |
| --- | --- | --- |
| 01 — análisis estadístico | Modelo ordinal mixto, interacción, efectos simples, IC, escenarios, corrección del join, cambio en gpt-5 | `correccion-01.../INFORME_ANALISIS_ESTADISTICO.md`; `salidas/35_resultados_clave.json` |
| 02 — diagnóstico gpt-5-nano | 41/79 salidas no sustantivas; 38/79 sustantivas con calidad alta; jueces inconsistentes; no es falta de recuperación ni truncamiento | `correccion-02.../INFORME_DIAGNOSTICO.md`; `salidas/14_dataset_categoria_final.csv` |
| 03 — parámetros de API | No hay determinismo; la temperatura no se aplicó; el esfuerzo de razonamiento no se registró; una ejecución por celda | `correccion-03.../propuestas_edicion.md`; `salidas/resumen_evidencia.json` |
| 04 — factores confundidos y prompts | Recuperador fijo gpt-5; prompts distintos; límite 7 en gpt-5 y 6 en mini/nano; Agente de Calidad nunca ejecutado; objetivo 2 parcial | `correccion-04.../03_resolucion_contradicciones.md`; `propuestas/cambios_manuscrito.md` |
| 06 — corpus y benchmark | Corpus actualizado, no copia del PDF de 1997; 398 nodos artículo; revisión por una profesional; una revisión asistida por `ollama-cloud:deepseek-v4.1-flash:1017-cloud` detectó posibles errores que requieren revisión profesional | `correccion-06.../resumen_ejecutivo.md`; `salidas/auditoria_corpus_benchmark.md` |
| Verificación D-14 | α recalculado desde jueces originales; 23 discrepancias y 17 evaluaciones positivas no sustantivas | `verificacion-analisis-estadistico/salidas/resumen_verificacion.json` |
| 07 — bibliografía | Correcciones de citas y referencias; no altera la inferencia, pero impide sostener atribuciones erróneas | `correccion-07.../resumen_ejecutivo.md`; `propuesta_edicion_manuscrito.md` |
| 05 — este paquete | Costos, Pareto, costo por respuesta correcta, Tabla 4 reformulada y textos propuestos | `ANALISIS_COSTOS.md`; `TABLA_4_REFORMULADA.md` |

---

## 2. Qué cambia respecto del manuscrito y de la valoración del jurado

### 2.1. La inferencia ya no es la original

El manuscrito trataba 711 observaciones como independientes y usaba Kruskal–Wallis, Dunn, Mann–Whitney y Scheirer–Ray–Hare. La corrección 01 reemplaza ese sustento por un modelo ordinal mixto con interceptos por caso y unidad, 2.133 evaluaciones juez-observación y escenarios de fallo. La interacción es muy fuerte:

- LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²;
- AIC 5.525,0 frente a 5.810,3;
- varianza de caso 0,164 y de unidad 1,380;
- la interacción se mantiene en los cuatro escenarios (LR 82,52–293,28; p < 10⁻¹⁶) y en los tres jueces.

### 2.2. Cambia una premisa de la valoración del jurado: gpt-5 sí muestra un efecto positivo de Agentic-RAG

La valoración afirma que en gpt-5 “ninguna diferencia es significativa tras la corrección”. Con el modelo apareado:

- Agentic-RAG − RAG básico: +0,106; IC 95% 0,054–0,155; p Holm = 1,03 × 10⁻⁴.
- Agentic-RAG − Sin RAG: +0,095; IC 95% 0,046–0,146; p Holm = 4,82 × 10⁻⁴.
- RAG básico − Sin RAG: −0,011; IC −0,063 a 0,044; p Holm = 0,724.

La diferencia es menor que en gpt-5-mini, pero no nula. La respuesta al jurado debe reconocer que el análisis anterior no aprovechaba el apareamiento y que el nuevo resultado corrige esa premisa.

### 2.3. El “efecto igualador” no se sostiene

Con RAG básico, las diferencias observadas son menores que en otras estrategias, pero las estimaciones son positivas:

| Contraste | Diferencia media | IC 95% | p Holm en escala latente |
| --- | ---: | ---: | ---: |
| mini − nano | +0,063 | 0,005–0,120 | 0,068 |
| gpt-5 − nano | +0,128 | 0,071–0,186 | — |
| gpt-5 − mini | +0,065 | 0,011–0,124 | 0,064 |

No hay un margen de equivalencia definido y los intervalos no lo establecen. La frase correcta es “las diferencias observadas son menores, pero no desaparecen; no se demostró equivalencia”.

### 2.4. La celda nano no es una “degradación uniforme”

Agentic-RAG + gpt-5-nano:

- 41/79 salidas no sustantivas: 27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas.
- Con fallo = 0: media 0,395; mediana 0,000.
- Con exclusión: 38/79; media 0,820; mediana 0,958.
- Logs: recuperación y tokens de salida; sin evidencia de truncamiento por longitud.
- La diferencia Agentic − RAG básico cambia de signo: −0,270 (fallo = 0) y +0,216 (exclusión). No es una contradicción: mide utilidad del sistema frente a calidad condicional.

Por eso “sobrecarga agéntica” debe retirarse como explicación causal y reemplazarse por “modo de fallo de respuesta”.

### 2.5. Los jueces no están “validados”

- α ordinal global de corrección: 0,807842 con valores originales; 0,799542 con transformación a rúbrica, recalculado de forma independiente en `verificacion-analisis-estadistico/`.
- No se comparó con criterio humano ni existen calificaciones humanas de las respuestas; la revisión humana del benchmark no es validación de los jueces.
- La verificación identificó 23 discrepancias entre jueces para revisión humana y 17 evaluaciones positivas sobre salidas no sustantivas.
- La precisión legal tiene α = 0,784566 global, pero cae por debajo de 0,667 en RAG básico y Sin RAG.

La conclusión correcta es “acuerdo inter-juez bueno para corrección, con inconsistencias en salidas no sustantivas; confiabilidad, no validez”.

### 2.6. El objetivo 2 es parcial

- Dos agentes activos: Especialista Legal y Recuperación.
- Una delegación nominal del especialista; no hay segunda ronda ni verificación.
- El Agente de Calidad fue diseñado, pero no se ejecutó: no hay logs ni llamadas.
- 236/237 sesiones del especialista registran una llamada a `retrieve_relevant_documents`; `16_01` de gpt-5 registra tres.
- gpt-5 usó un prompt con límite 7; mini/nano, límite 6.

No se puede afirmar “cumplimiento completo” ni “ciclo multi-agente de verificación”.

### 2.7. El benchmark es v1, con revisión profesional y observaciones abiertas

- 25 casos, 79 unidades.
- Revisión por una profesional, registrada en ODT; no hay segunda revisión independiente.
- 12 propuestas de corrección (referencias, paráfrasis, alcance de Q23–Q25).
- Una revisión posterior asistida por `ollama-cloud:deepseek-v4.1-flash:1017-cloud` detectó posibles errores que requieren una nueva revisión por un profesional del derecho.
- Las conclusiones corresponden al instrumento v1. No se debe corregir el anexo y presentarlo como si fuera el usado.

### 2.8. Los costos no tienen un ganador único

- Costo total: USD 22,2939.
- Agentic-RAG + mini: USD 0,0564/consulta; RAG básico + gpt-5: USD 0,0392; Sin RAG + gpt-5: USD 0,0478. La recomendación “costo-eficiente” no se sostiene en sentido absoluto.
- Menor costo puntual por respuesta correcta (≥ 0,75, definición D-02): RAG básico + nano, USD 0,0061 (33/79; media 0,599); su IC bootstrap se solapa con Sin RAG + nano, por lo que no hay una diferencia formal establecida.
- Mayor media: Agentic-RAG + gpt-5, 0,812 (USD 0,0792; 56/79).
- Agentic-RAG + mini es no dominada: 0,788 a USD 0,0564, con diferencia no concluyente frente a Agentic-RAG + gpt-5.
- Agentic-RAG + nano tiene el peor costo por respuesta correcta: USD 0,1307 (27/79).

---

## 3. Clasificación de las conclusiones

### 3.1. Se conservan con matices

1. **Existe una interacción fuerte entre estrategia y modelo del especialista.** El patrón es robusto en escenarios y jueces. No se conserva la interpretación causal.
2. **La calidad de las respuestas sustantivas de Agentic-RAG + nano es alta.** 38/79; media 0,820; mediana 0,958. Se conserva solo como calidad condicional, no como resultado del sistema completo.
3. **El sistema es técnicamente viable como prototipo.** Se conserva con alcance de un corpus, sin interfaz y con una ejecución por celda.
4. **Agentic-RAG + mini es una alternativa de calidad alta con menor costo que Agentic-RAG + gpt-5.** Se conserva como opción no dominada, no como “la más costo-eficiente”.

### 3.2. Se reformulan

1. **“La recuperación mejora significativamente.”** → “El efecto depende de la estrategia y del modelo; no hay mejora uniforme”.
2. **“El objetivo 2 se cumplió completamente.”** → “Cumplimiento parcial: dos agentes activos, una delegación, sin verificador”.
3. **“El benchmark fue validado por un profesional.”** → “Revisado por una profesional; v1 congelado; correcciones v2; revisión LLM posterior detectó posibles errores que requieren revisión profesional”.
4. **“El repositorio es replicable.”** → “Acceso público verificado sin login; clonación y ejecución recomendadas como verificación de reproducibilidad”.
5. **“El sistema atiende a usuarios profesionales y no profesionales.”** → “Uso potencial; no se evaluó con usuarios ni se desarrolló interfaz”.

### 3.3. Se retiran

1. **“Efecto igualador del RAG básico.”** No hay equivalencia; las diferencias son positivas y algunas limítrofes.
2. **“Sobrecarga agéntica en modelos pequeños.”** No hay evidencia causal; hay un modo de fallo concentrado.
3. **“Validación de LLM-as-a-Judge.”** Hay acuerdo, no validez humana.
4. **“Combinación costo-eficiente: Agentic-RAG + gpt-5-mini.”** No es la más barata; se reemplaza por Pareto.
5. **“Resultado transferible a otros dominios.”** No se evaluó; es una hipótesis.
6. **“En gpt-5 no hay diferencias entre estrategias.”** El análisis apareado muestra diferencias positivas de Agentic-RAG.

---

## 4. Frases que deben buscarse y corregirse

| Frase o idea | Ubicación | Acción |
| --- | --- | --- |
| “efecto igualador” | `07...:131, 265, 414`; `09...:31` | Retirar o reformular como “diferencias reducidas, no equivalencia” |
| “sobrecarga agéntica” | `07...:419`; `09...:33, 83, 101` | Reemplazar por “modo de fallo de respuesta” |
| “validación de LLM-as-a-Judge” | `09...:37`; README | Cambiar por “acuerdo inter-juez” |
| “en gpt-5 no hay diferencias” | `07...:424, 435`; `09...:45, 138` | Corregir con +0,106 frente a RAG básico y +0,095 frente a Sin RAG |
| “resultado transferible” | `09...:138` | Retirar; hablar de hipótesis |
| “combinación costo-eficiente” | `07...:429`; `09...:57` | Reemplazar por Pareto/costo por respuesta correcta (≥ 0,75) |
| “objetivo 2 cumplido completamente” | `09...:17` | Cambiar a cumplimiento parcial |
| “temperatura 0” / “determinista” | `07...:16`; `06...:461, 644`; `09...:87` | Corregir según IX.1.3 |
| “n = 79 observaciones por celda” sin desglose | `07...:424` | Aclarar 79 unidades, 2.133 evaluaciones, 653 en exclusión |
| “245 artículos” / “399 artículos” | `04...:111`; `06...:101` | Usar 398 nodos artículo (397 con texto) o “artículo inexistente” |
| “IVF_FLAT” | `09...:15`; `06...:138` | Sustituir por “AUTOINDEX con similitud coseno” (D-12) |

La lista completa está en `FRASES_A_ELIMINAR.csv`.

---

## 5. Qué no se puede afirmar con los datos actuales

1. Que la estrategia óptima sea universal.
2. Que Agentic-RAG sea superior en todos los modelos.
3. Que RAG básico iguale a los modelos.
4. Que el fallo de nano se deba a la complejidad, al modelo, al prompt o al recuperador.
5. Que los jueces estén validados contra criterio humano.
6. Que el benchmark v1 esté jurídicamente cerrado.
7. Que los costos históricos sigan vigentes.
8. Que el sistema tenga impacto en usuarios o haya sido adoptado.
9. Que los resultados se transfieran a otros dominios.
10. Que una ejecución por celda permita estimar estabilidad entre corridas.

---

## 6. Qué se puede afirmar con los datos actuales

1. Hay una interacción fuerte y robusta entre estrategia y modelo del especialista.
2. En el escenario fallo = 0, Agentic-RAG es inferior a RAG básico en nano, superior en mini y moderadamente superior en gpt-5.
3. RAG básico presenta diferencias menores entre modelos, pero no las elimina ni demuestra equivalencia.
4. Agentic-RAG + nano tiene 41/79 salidas no sustantivas y una calidad condicional alta cuando responde.
5. Los jueces tienen acuerdo ordinal bueno para corrección, con inconsistencias en salidas no sustantivas.
6. El objetivo 2 es parcial: dos agentes, una delegación, sin verificador.
7. El benchmark es v1, revisado por una profesional, con correcciones pendientes para v2.
8. Los costos no tienen un ganador único; RAG básico + nano presenta el menor costo puntual por respuesta correcta (≥ 0,75; IC solapado con Sin RAG + nano) y Agentic-RAG + gpt-5 maximiza la media.
9. El repositorio es público y accesible sin login; la clonación y ejecución se recomiendan como verificación de reproducibilidad.
10. El sistema es un prototipo de investigación, no una interfaz evaluada con usuarios.

---

## 7. Orden de edición

1. Aceptar `DECISIONES.md`.
2. Aplicar `PROPUESTA_TEXTO_MANUSCRITO.md` en metodología/evaluación.
3. Aplicar resumen y conclusiones.
4. Aplicar introducción, anexo y README.
5. Recompilar y buscar las frases de `FRASES_A_ELIMINAR.csv`.
6. Verificar cifras contra `datos/tabla4_reformulada.csv` y `datos/costos_por_celda.csv`.
7. Actualizar la respuesta al jurado con la Tabla 4 reformulada.

---

## 8. Limitaciones de esta síntesis

- No reemplaza la revisión jurídica de las respuestas de referencia (IX.1.6); el benchmark v1 se conserva como instrumento usado.
- No reemplaza la validación humana de los jueces (IX.2.3); declara su ausencia y deja 23 discrepancias para revisión futura.
- No reemplaza las réplicas ni la ablación (IX.2.4); solo declara que no existen.
- No actualiza precios ni costos de producción; usa los costos registrados.
- No decide el título ni el alcance institucional; eso queda en D-09.
- No edita el manuscrito: las propuestas deben revisarse antes de aplicarse.

---
title: "Verificación del manuscrito frente a las exigencias del tribunal — ollama-cloud-mimo-v2-6-flash"
model: "ollama-cloud-mimo-v2-6-flash"
created: 2026-11-12T21:47:00Z
---

# Verificación del manuscrito frente a la valoración del tribunal
## Reporte generado por el modelo `ollama-cloud-mimo-v2-6-flash`

| Campo | Valor |
|---|---|
| Documento de referencia | `analisis-valoracion-jurado/Valoracion_TF_Spairani_gp_actualizada.md` (Mg. Gastón Pezzuchi, nov. 2026) |
| Objeto verificado | `manuscrito/main.typ`, `manuscrito/capitulos/*.typ` (12 archivos, 3.326 líneas) y `manuscrito/referencias.bib` |
| Commit verificado | `6208cac` — *docs(readme): alinear el estado del repositorio con las revisiones* (12/11/2026 22:22) |
| Compilación | `typst compile main.typ` → **sin errores, 167 páginas** (la versión valorada tenía 165) |
| Método | Compilación + `pdftotext` (verificación sobre lo **impreso**, no solo el fuente) + búsquedas sistemáticas punto por punto contra IX.1.1–IX.1.9, IX.2.1–IX.2.5, Tablas 2/3/4 y V.1–V.11 |
| Fecha | 12/11/2026 |

> Este informe contrasta lo que el manuscrito **dice** con lo que el tribunal **exige**. No recalcula resultados estadísticos: las cifras se contrastaron contra los artefactos de `analisis-valoracion-jurado/correccion-01..07` y `verificacion-analisis-estadistico/`.
>
> Convenciones: ✅ Cumplido · 🟡 Parcial · ❌ Pendiente · ⛔ Contradicción interna (crítica para la defensa).

---

## 1. Veredicto ejecutivo

**El manuscrito ya contiene la sustancia de las correcciones del tribunal en el resumen, en las conclusiones y en las debilidades, pero el cuerpo del capítulo 6 y varias secciones de metodología y del capítulo 8 siguen exponiendo el análisis anterior.** El resultado es un documento internamente inconsistente: el mismo análisis aparece con dos bases de cálculo (684 y 711 observaciones) y dos marcos inferenciales (pruebas para muestras independientes vs. modelo ordinal mixto).

| Bloque | Estado | Comentario |
|---|---|---|
| Declaración de uso de IA (IX.1.8) | ✅ | Ampliada por etapas, con modelos, verificación y referencia fabricada (`01_texto_preliminar.typ:19-28`). |
| Medidas de recuperación (IX.1.9, V.8) | ✅ | recall@10, MRR, % unidades con todos/sin ningún artículo de referencia (`07…:314-331`), con advertencia de no causalidad. |
| No equivalencia inferida (V.3) | ✅ | Retirada en resumen, capítulo 6 y contribuciones (`07…:435, 456`; `09…:35`). |
| Factores confundidos y arquitectura acotada (V.5) | ✅ | Sección dedicada (`06…:284-290`), Agente de Calidad y límites 6/7 búsquedas declarados. **Falta**: prompts de líneas base y jueces. |
| Bibliografía (Tab. 3, IX.1.7) | ✅ | 8 de 9 ítems corregidos; quedan detalles de forma (preprints, 2 comas colgantes). |
| Forma (Tab. 2, IX.1.7) | 🟡 | 7 de 12 ítems corregidos; persisten n-gramas, "similitud coseno escalada", GPT-4/MoE, dedicatoria y **14 referencias cruzadas duplicadas en el PDF**. |
| Diagnóstico celda nano (IX.1.2, V.6) | 🟡 | 41/79 salidas no sustantivas informadas y "sobrecarga agéntica" reformulada a "modo de fallo de respuesta". **Falta** el diagnóstico por celda con evidencia de logs y la mención de los casos 23–25. |
| Corrección de los 27 faltantes (IX.1.2) | ⛔ | `07…:73` sigue atribuyéndolos a "fallos puntuales en la generación" y declara **684 observaciones**, mientras que `07…:18` declara **711**. |
| Inferencia del cuerpo (IX.1.1, V.1–V.2) | ⛔ | El modelo ordinal mixto está en resumen/conclusiones, pero el capítulo 6 sigue exponiendo Kruskal-Wallis, Dunn, Mann-Whitney y Scheirer-Ray-Hare como secciones principales, con texto y tabla que se contradicen entre sí. |
| Determinismo / temperatura (IX.1.3, V.4) | ⛔ | **6 frases residuales** afirman temperatura 0 y determinismo, pese a la corrección ya incorporada en `01…:28` y `06…:497`. |
| Ejecución única como limitación (IX.1.3) | ❌ | No figura entre las 12 limitaciones del capítulo 8. |
| Conclusiones (Tab. 4, IX.1.5) | 🟡 | 5 de 9 filas reformuladas; 4 persisten con cifras del análisis viejo (`09…:55, 57, 63, 75`). |
| Corpus (IX.1.6, V.9) | 🟡 | Procedencia, conteos y respuestas de referencia corregidos; la calidad de la extracción sigue sin cuantificar (`06…:67`). |
| Costos (V.10) | 🟡 | Costo por respuesta correcta incorporado; el **índice con piso 0,01 objetado sigue en el cuerpo** (`07…:289-306`). |
| Alcance (V.11) | 🟡 | Objetivo general y contribuciones de la introducción siguen prometiendo "usuarios profesionales y no profesionales". |
| Recomendaciones (IX.2.1–2.5) | ❌/🟡 | Ninguna ejecutada; 3 declaradas como limitación/trabajo futuro, 2 sin declarar. |

**Bloqueantes para la defensa (⛔):**

1. **`07_capitulo_06_evaluacion.typ:73`** — los 27 faltantes siguen explicados como "fallos en la generación" y la base sigue en 684 observaciones; el resumen y las conclusiones corren sobre 711 (79 × 9). El manuscrito describe un análisis que no es el que sustenta sus conclusiones.
2. **`07…:135` vs `07…:140-158`** — el texto dice "los efectos simples se estimaron con ese modelo [ordinal]" pero la tabla que sigue se titula "Efectos simples … (Mann-Whitney U)" con medianas y p de la base vieja. Contradicción texto–tabla en la misma sección.
3. **`06…:708` vs `07…:135` y `01…:4`** — metodología llama al modelo ordinal "análisis de robustez/sensibilidad"; el resumen y el capítulo 6 lo llaman "análisis principal". Además `09…:71` afirma que "la inferencia principal se apoya en las pruebas pareadas", pero **no existe ningún Friedman, Wilcoxon ni bootstrap en el manuscrito**.
4. **6 afirmaciones de determinismo** (`06…:191, 511, 521, 614, 660`; `07…:16`) que contradicen la corrección ya declarada en `01…:28` y `06…:475, 497`.
5. **`anexo_01.typ:86`** — la Tabla 17 sigue diciendo "modelos mixtos" para `part_j/`, cuando el tribunal confirmó que no fueron estimados.

---

## 2. Correcciones requeridas (IX.1.1 – IX.1.9)

| # | Exigencia | Estado | Evidencia en el manuscrito | Pendiente |
|---|---|---|---|---|
| **1** | Rehacer la inferencia con apareamiento y anidamiento, efectos con IC, corregir "modelos mixtos" | 🟡 | Modelo ordinal mixto con LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶² e efectos con IC 95 % en resumen (`01…:4`), capítulo 6 (`07…:135, 456`) y conclusiones (`09…:31`); especificación `clmm`/`nAGQ = 1` en `06…:708`. | Cuerpo del cap. 6 sigue con KW/Dunn/MW/SRH como secciones principales (`07…:93-226`); tabla de efectos es Mann-Whitney (`07…:140-158`); tabla de medianas con base vieja sin `n` ni no sustantivas (`07…:169-190`); sin Friedman/Wilcoxon/bootstrap; `anexo_01.typ:86` aún dice "modelos mixtos"; contradicción robustez vs. principal. |
| **2** | Informar 41 salidas, reincorporar casos 23–25, corregir faltantes, reformular "sobrecarga agéntica" | 🟡 | "41 de 79 salidas no fueron sustantivas (27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada, 10 indeterminadas)" en resumen (`01…:4`), debilidades (`07…:440`) y contribuciones (`09…:33`); reformulado como "modo de fallo de respuesta", sin atribución causal. | ⛔ `07…:73` conserva la explicación errónea y las "684 observaciones"; **cero menciones** a los casos 23–25 o al defecto de join; sin subsección de diagnóstico por celda (tasa, `finish_reason`, tokens); tabla de medianas sin actualización. |
| **3** | Retirar determinismo, informar esfuerzo de razonamiento, declarar ejecución única | ❌ | `reasoning_effort` declarado correctamente en `01…:28` y `06…:497` (Pydantic AI 1.1.0 → `NOT_GIVEN`, default `medium`). | **6 frases residuales**: `06…:191` ("temperatura 0"), `06…:511` ("temperatura cero (respuestas determinísticas)"), `06…:521` ("temperatura 0 para maximizar la reproducibilidad"), `06…:614` (jueces), `06…:660` ("evita múltiples ejecuciones"), `07…:16` ("temperatura 0 … para garantizar reproducibilidad"). La ejecución única **no** figura como limitación en el cap. 8. |
| **4** | Declarar factores confundidos, reproducir prompts, resolver contradicciones | 🟡 | "Alcance operativo y factores confundidos" (`06…:284-290`); Agente de Calidad excluido sin promesa de mejora (`06…:201, 292-294`); límite 6/7 búsquedas y recuperador siempre gpt-5 documentados (`06…:281, 497`); zero-shot sin CoT declarado (`04…:89`). | Solo 3 prompts reproducidos (Especialista, Recuperación, Calidad: `06…:270-330`). **No** se reproducen el de sin RAG / RAG básico (siguen como "prompt simplificado", `06…:321`) ni los de los jueces; no existe `anexo_02_prompts_y_parametros.typ` y `04…:89` remite a "el anexo de prompts del repositorio" (fuera del manuscrito). |
| **5** | Reformular las conclusiones de la Tabla 4 | 🟡 | Reformuladas: interacción como hallazgo principal (`01…:4`, `09…:31`); "efecto igualador" retirado (`09…:35`); LLM-as-a-Judge → "confiabilidad, no validación" (`09…:37`); objetivo 2 → "cumplimiento parcial" (`09…:17`); costo-eficiente → "alternativa no dominada" (`07…:450`); transferencia acotada (`09…:45, 142`). | `09…:55` "Mejora significativa con recuperación" con los p viejos (p < 0,001; p = 0,0066); `09…:57` "Configuración costo-eficiente viable … 0,78 vs. 0,80"; `09…:63` "Análisis estadístico riguroso (Shapiro-Wilk, Kruskal-Wallis, Dunn, Scheirer-Ray-Hare, Mann-Whitney)"; `09…:73` "diferencia marginal (p = 0,383)"; `09…:75` "Degradación con modelos pequeños (p_corr = 0,017)"; `09…:136` "validación mediante LLM-as-a-Judge". |
| **6** | Precisar versión del corpus, resolver contradicciones, revisar respuestas de referencia | 🟡 | Procedencia resuelta: PDF del BO 30/05/1997 + contraste con Infoleg, evidenciada en arts. 3 (Ley 25.225), 31/215/221 (Ley 27.111); el parser HTML se intentó y descartó (`06…:51-56`). Conteos unificados: 482 partes; 398 artículos = 347 + 15 + 36; 362 números únicos; art. 239 derogado (`06…:77-96`). Fecha de sanción 1886-11-25 (`anexo_01.typ:251`). Respuestas 1.2 y 1.3 corregidas a art. 11 y art. 17 con las tres causales (`anexo_01.typ:305, 307`). | `06…:67` "Validación de Calidad de Extracción": sigue sin tamaño de muestra, sin tasa de error y sin declarar que no existe métrica de error. |
| **7** | Corregir Tablas 2 y 3 y auditar la bibliografía | 🟡 | Tabla 3: ✅ (ver §4). Tabla 2: corregidos oración trunca (`02…:11`), LEGAL-BERT (`04…:29, 65`), "245 artículos" (ausente), fechas de DeepSeek-R1/Llama 4/Qwen3/Gemini 3 Pro (`08…:253, 257, 259, 156`), fecha 1994 → 1886 (`anexo…:251`), Wikipedia en nota 13 (ya no remite), "y col(s)." (0 en PDF). | 5 ítems: n-gramas "secuencias de caracteres" (`03…:101`), "similitud coseno escalada" (`03…:333`), GPT-4/MoE (`03…:371, 409`), dedicatoria "A mi familia …" (`01…:13`), y **14 referencias cruzadas duplicadas** ("capítulo Sección 4"…) en 12 páginas del PDF. Auditoría completa de la lista: no verificable desde aquí, pero las entradas erróneas ya no están. |
| **8** | Ampliar la declaración de uso de IA | ✅ | `01…:19-28`: cinco etapas (extracción `o4-mini`, benchmark `GPT-4.1`, respuestas GPT-5, jueces, asistencia), con alcance de la verificación, referencia fabricada eliminada y nota sobre `reasoning_effort`. | — |
| **9** | Informar medidas de recuperación | ✅ | `07…:314-331`: recall top-10, MRR, % con todos y % sin ningún artículo de referencia, para baseline (0,333 / 0,214 / 27,9 % / 59,5 %) y estrategia agéntica; comparación declarada no causal; BM25/no-embedding declarado imposible por pérdida del volumen de Milvus. | Sin nDCG ni Hit@k; `NDCG` y `HNSW` siguen en `acronimos_o_siglas.typ:16, 26` sin usarse (el tribunal ya había señalado la sigla MRR, que hoy sí se usa). |

---

## 3. Recomendaciones (IX.2.1 – IX.2.5)

| # | Recomendación | Estado | Detalle |
|---|---|---|---|
| **1** | Comparar el embedding con un recuperador entrenado y una línea base léxica | ❌ | No ejecutado. Declarado en `07…:331` (volumen de Milvus perdido) y previsto como trabajo futuro (BM25 en `09…:107`). |
| **2** | Métricas deterministas de citas (precisión, exhaustividad, artículos inexistentes) | ❌ | No ejecutado (NV-03, cancelado por tiempo) y **no anunciado como trabajo futuro** en el manuscrito, pese a que el marco teórico presenta la citación como riesgo central. |
| **3** | Validar una submuestra de calificaciones con profesionales | ❌ | No ejecutado; declarado como limitación (`09…:87, 89`). |
| **4** | Réplicas de celdas críticas y ablación con el mismo modelo en ambos agentes | ❌ | No ejecutado. `07…:452` advierte "no se recomienda sin réplicas ni ablaciones", pero **no se declara como limitación de las estimaciones** en el capítulo 8. |
| **5** | Reducir el capítulo 2 y la sección 7.7 | ❌ | Cap. 2: PDF pp. 24–42 (~19 páginas), sin cambios. Sección 7.7: PDF pp. 123–128 (~6 páginas con 4 líneas de tiempo), sin cambios. |

---

## 4. Errores de forma (Tabla 2) y bibliografía (Tabla 3)

### Tabla 2 — 12 ítems

| Ítem del tribunal | Estado | Ubicación actual |
|---|---|---|
| Oración trunca "Al combinar grandes modelos de lenguaje…" | ✅ | `02_capitulo_01_introduccion.typ:13` — "La combinación de grandes modelos de lenguaje (LLM) con mecanismos de recuperación de información **permite fundamentar las respuestas**…" |
| n-gramas como "secuencias de caracteres" con ejemplo de palabras | ❌ | `03_capitulo_02…:101` (definición y ejemplo siguen sin coincidir) |
| "similitud coseno escalada" | ❌ | `03…:333` (la fórmula de debajo es correcta: producto escalado / √d_k; solo el texto la llama coseno) |
| GPT-4 "introduce arquitectura MoE" | ❌ | `03…:371` y `03…:409` |
| LEGAL-BERT / Case Law Access / LegalBench | ✅ | `04…:29, 65` separan las tres fuentes y niegan la evaluación anacrónica |
| "El Código solo tiene 245 artículos" | ✅ | Ausente del PDF; `06…:84-96` reporta 398 artículos |
| Fechas DeepSeek-R1, Llama 4, Qwen3, Gemini 3 Pro | ✅ | `08…:253` (R1 ene-2025), `:259` (Llama 4 abr-2025), `:257` (Qwen3 abr-2025), `:156/191` (Gemini 3 Pro 18-nov) |
| Fecha de sanción 1994-01-01 | ✅ | `anexo_01.typ:251` → 1886-11-25 |
| "capítulo Sección 4" / "sección Sección 4.7" | ❌ | **14 ocurrencias en 12 páginas del PDF** (págs. 43, 49, 50, 53 ×2, 74, 76, 78, 82, 89 ×2, 96, 111, 133). El texto manual dice "capítulo"/"sección" y `@cap:`/`@sec:` se imprime como "Sección N". Defecto más visible del PDF. |
| Nota 13 con remisión a Wikipedia | ✅ | Sin remisiones a Wikipedia para datos históricos. (Quedan 2 entradas de bibliografía que son **créditos de imagen** de Wikimedia Commons, práctica aceptable para figuras.) |
| Dedicatoria "A mi familia …" | ❌ | `01_texto_preliminar.typ:13` — sigue con apariencia de texto provisorio |
| Declaración de IA de una sola oración | ✅ | `01…:19-28` |

### Tabla 3 — 9 ítems

| Ítem | Estado | Nota |
|---|---|---|
| Bommasani et al. (2023) → Bozdag, Sevim y Koç (2024) | ✅ | `bozdag2024gender` (DOI 10.1145/3628602); sin "adapters" atribuidos; no queda entrada `bommasani` en el `.bib` |
| Estudio de Stanford (Dahl) → Magesh et al. (2025) | ✅ | `magesh2025hallucinationfree` (DOI 10.1111/jels.12413); sin entrada `dahl` |
| Wei 2022a/2022b y Zhao 2026 sin distinguir | ✅ | Claves separadas (`wei2022cot`, `wei2022emergent`; `zhao2026surveySpringer`, `zhao2026reportlogic`); el PDF imprime "Wei et al. (2022a)" ×3 y "(2022b)" ×1 |
| DeepSeek (2026b) / Meta (2026) duplicados y mal fechados | ✅ | `deepseek2025r1` (ene-2025), `llama4` (abr-2025) |
| LEXTREME: año 2024 vs. Findings EMNLP 2023 | ✅ | `niklaus2023lextreme` con DOI de Findings 2023 |
| Tribunal Fiscal de la Nación con URL de un estudio | ✅ | `tribunalfiscal2024buscador` → página institucional (`argentina.gob.ar/tribunalfiscal`) |
| Faltan Lewis et al. (2020) y el Código de Minería | ✅ | `lewis2020rag` citado en `02…:11`; `codigo_mineria_1919` como fuente legal |
| Preprints con versión con arbitraje | 🟡 | Parcial; persisten `@misc` de material de proveedor (aceptable para modelos, conviene revisar) |
| "y col(s)." y fecha de consulta como fecha de publicación | ✅ | 0 apariciones de "y col(s)." en el PDF; estilo APA automático uniforme |

**Menor:** 2 entradas imprimen el año con coma colgante — "(2024, )" y "(2022, )" — por no tener `month` en el `.bib`.

---

## 5. Estado de la Tabla 4 del tribunal (conclusiones)

| Conclusión cuestionada | Estado | Evidencia / pendiente |
|---|---|---|
| "La recuperación mejora significativamente la calidad" | 🟡 | Reformulada como condicional al modelo (`07…:433, 456`; `01…:4`), pero `09…:55` la mantiene con los p del análisis viejo. |
| Interacción como hallazgo principal | 🟡 | Afirmada con el modelo ordinal (`09…:31`), pero su sustento inferencial en el cuerpo sigue siendo SRH + Mann-Whitney (V.1/V.2). |
| "Efecto igualador del RAG básico" | ✅ | Retirada; explícitamente: "la conclusión anterior basada en un p de Kruskal–Wallis no significativo debe retirarse" (`09…:35`). |
| "Sobrecarga agéntica en modelos pequeños" | 🟡 | Reformulada a "modo de fallo de respuesta" en `01…:4`, `07…:440`, `09…:33`; sobrevive la atribución causal en `07…:164` ("la complejidad agéntica es excesiva"). |
| "Validación de LLM-as-a-Judge" | 🟡 | `09…:37` la corrige; pero `09…:136` (trabajos futuros) aún dice "validación mediante LLM-as-a-Judge" y `09…:63` la presenta como base sólida. |
| Objetivo 2 "se cumplió completamente" | ✅ | `09…:17` → "cumplimiento parcial", con detalle de agentes activos e inactivos. |
| "Combinación costo-eficiente: Agentic-RAG + gpt-5-mini" | 🟡 | `07…:449-450` y `09…:57` la matizan ("alternativa no dominada, no la más barata"), pero `09…:57` conserva la fórmula "Configuración costo-eficiente viable" y medias desactualizadas (0,78 vs. 0,80; las canónicas son 0,788 y 0,812). |
| "Transferible a otros dominios" | ✅ | Acotada en `09…:45` y `09…:142` (un corpus, 25 casos, una ejecución por celda, un recuperador fijo). |
| "Usuarios profesionales y no profesionales" (p. 6) | ❌ | El objetivo general sigue prometiéndolo (`02…:105`); las "Contribuciones principales" de la introducción (`02…:131-145`) no reflejan el alcance acotado. |

---

## 6. Observaciones sustantivas V.1 – V.11

| Obs. | Exigencia | Estado | Evidencia / pendiente |
|---|---|---|---|
| **V.1** | Inferencia apareada/anidada, efectos con IC, corregir modelos mixtos | 🟡 | Modelo ordinal con efectos e IC: ✅ en resumen/cap.6/cap.8. Pendiente: cuerpo del cap. 6 (`07…:93-226`), tablas viejas, `anexo…:86` "modelos mixtos", sin sensibilidad Friedman/Wilcoxon. |
| **V.2** | Sustituir el sustento de la interacción (SRH) | 🟡 | SRH rotulado "antecedente exploratorio" (`07…:135, 222`), pero la sección completa con fórmula y tabla H sigue en el cuerpo (`07…:195-226`) en vez de anexo. |
| **V.3** | No inferir equivalencia de la falta de significación | ✅ | `07…:435, 456`; `09…:35`; sin frases "elimina las diferencias" ni "efecto igualador" en todo el manuscrito. |
| **V.4** | Retirar determinismo, informar esfuerzo de razonamiento, declarar ejecución única | ❌ | 6 frases residuales (ver IX.1.3); `reasoning_effort` ✅; ejecución única no declarada como limitación. |
| **V.5** | Factores confundidos, prompts, contradicciones | 🟡 | Factores confundidos, Arquitectura acotada, Agente de Calidad y límites 6/7: ✅. Prompts de líneas base y jueces: ❌. |
| **V.6** | Informar 41 salidas, casos 23–25, faltantes, reformular sobrecarga | 🟡 | 41/79 con desglose y reformulación: ✅. Faltantes y casos 23–25: ⛔ ❌. Diagnóstico por celda con logs: ❌. |
| **V.7** | Validez de la medición (benchmark, respuestas, jueces) | 🟡 | Respuestas 1.2/1.3 corregidas ✅; revisión por una sola profesional declarada (`09…:19, 87`) ✅; confiabilidad ≠ validez declarada (`09…:37`) ✅; 23 discrepancias y 17 puntajes positivos sobre salidas no sustantivas reportados ✅. Sin validación humana de jueces (limitación declarada) y sin métricas deterministas de citas (❌). |
| **V.8** | Informar medidas de recuperación | ✅ | `07…:314-331` (ver IX.1.9). Pendiente menor: `NDCG`/`HNSW` sin uso en siglas. |
| **V.9** | Versión y calidad del corpus, unificar conteos, revisar respuestas | 🟡 | Procedencia, conteos, fecha 1886 y respuestas: ✅. Calidad de la extracción sin cuantificar: ❌ (`06…:67`). |
| **V.10** | Costos: retirar el índice con piso 0,01; Pareto o costo por respuesta correcta | 🟡 | Costo por respuesta correcta (USD 0,0061; 33/79) y "no dominada": ✅ (`07…:449-450`). **Índice de Eficiencia con piso 0,01 sigue en el cuerpo** (`07…:289-306`, con su figura `eficiencia_costo.pdf`); sin frontera de Pareto. |
| **V.11** | Título, objetivos, alcance, repositorio, IA | 🟡 | Título acotado ✅; declaración de IA ✅; repositorio verificado ✅ (`09…:21`). Objetivo general y contribuciones de la introducción sin acotar ❌ (`02…:105, 133-145`). |

---

## 7. Pendientes priorizados (con archivo:línea)

### ⛔ Críticos (contradicciones internas)

1. **`07_capitulo_06_evaluacion.typ:73`** — reescribir el bloque de faltantes: defecto de join en los casos 23–25, normalización a **711 observaciones / 2.133 evaluaciones**, y actualizar las tablas de medianas (`07…:169-190`) y de efectos (`07…:140-158`) a la base de 79 por celda.
2. **`07…:135` vs `07…:140-158`** — la tabla de efectos simples debe ser la del modelo ordinal (Δ media, IC 95 %, Δ P(≥ 0,75), p Holm) o el texto debe dejar de afirmar que los efectos se estimaron con ese modelo.
3. **`06…:708` / `09…:71` vs `01…:4` / `07…:135`** — unificar el estatus del modelo ordinal (¿principal o de robustez?) y eliminar/reformular la frase "la inferencia principal se apoya en las pruebas pareadas", que no existen en el manuscrito.
4. **Determinismo (6 frases)** — `06…:191, 511, 521, 614, 660` y `07…:16`.
5. **`anexo_01.typ:86`** — "modelos mixtos" en la Tabla 17 → describir lo que realmente se corrió.

### 🟡 Altos (cuerpo del capítulo 6 y conclusiones)

6. Trasladar KW/Dunn (`07…:93-131`) y SRH (`07…:195-226`) a un anexo "análisis exploratorio histórico"; incorporar la tabla de celdas con `n`, no sustantivas, media, mediana, media modelada y P(≥ 0,75), y las figuras canónicas del análisis (hoy no están en `manuscrito/media/`).
7. Reformular `09…:55, 57, 63, 73, 75` y `09…:136` con las cifras del análisis nuevo.
8. Declarar como limitación del capítulo 8: **ejecución única sin réplicas**, factores confundidos sin ablaciones y costos de producción.
9. `07…:164` — retirar "la complejidad agéntica es excesiva para modelos de capacidad reducida".

### 🟡 Medios (alcance, forma y costos)

10. `02…:105, 111, 131-145` — acotar objetivo general, objetivo específico 2 y contribuciones de la introducción.
11. `07…:289-306` — sacar el Índice de Eficiencia (piso 0,01) del cuerpo; añadir frontera de Pareto.
12. Referencias cruzadas duplicadas (14 en 12 páginas): usar `#ref(<etiqueta>, supplement: [Capítulo])` o reescribir el texto manual.
13. `03…:101, 333, 371, 409` y `01…:13` — los 5 ítems de forma restantes de la Tabla 2.
14. `06…:67` — honestidad sobre la validación de la extracción (sin muestra ni tasa de error).
15. Reproducir los prompts de sin RAG / RAG básico y de los jueces (idealmente en un `anexo_02_prompts_y_parametros.typ`); `04…:89` hoy remite fuera del manuscrito.

### 🟡 Menores

16. `acronimos_o_siglas.typ:16, 26` — quitar `HNSW`/`NDCG` o usarlas (nDCG@10 está disponible en `verificacion-analisis-estadistico/metricas_recuperacion/`).
17. Anunciar las métricas deterministas de citas (IX.2.2) como trabajo futuro.
18. `.bib`: añadir `month` a Self-RAG y LoRA (coma colgante "(2024, )"/"(2022, )").

---

## Anexo A — Comprobaciones ejecutadas

```bash
# Compilación y texto plano
cd manuscrito && typst compile main.typ /tmp/verif_mimo.pdf   # → 167 páginas, sin errores
pdftotext /tmp/verif_mimo.pdf /tmp/verif_mimo.txt

# Determinismo / temperatura (6 hits)
grep -n "temperatura 0\|temperatura cero\|Temperatura 0\|respuestas determinísticas\
\|para garantizar reproducibilidad\|maximizar la reproducibilidad" capitulos/*.typ
# → 06:191, 06:511, 06:521, 06:614, 06:660, 07:16

# Faltantes y base de cálculo (1 hit, contradice resumen)
grep -n "684\|27 observaciones\|fallos puntuales\|711 observaciones" capitulos/*.typ
# → 07:73 (684) vs 07:18 (711)

# Casos 23-25 / join: 0 hits
grep -n "casos 23\|23, 24 y 25\|clave de subpregunta" capitulos/*.typ   # → vacío

# Pruebas viejas en el capítulo 6
grep -c "Kruskal"   07_capitulo_06_evaluacion.typ   # 5
grep -c "Dunn"      07_capitulo_06_evaluacion.typ   # 2
grep -c "Mann-Whitney" 07_capitulo_06_evaluacion.typ # 1
grep -c "Scheirer"  07_capitulo_06_evaluacion.typ   # 5
grep -in "friedman\|wilcoxon\|bootstrap" capitulos/*.typ   # 0 hits (solo "pareadas": 09:31,71,142)

# Referencias cruzadas duplicadas en el PDF
python3 - <<'EOF'
import re
raw = open('/tmp/verif_mimo.txt', encoding='utf-8').read()
pat = re.compile(r'(cap[ií]tulo|secci[oó]n)\s+Secci[oó]n\s+[0-9.]+', re.I)
hits = [(i, m.group(0)) for i, pg in enumerate(raw.split('\f'), 1)
        for m in pat.finditer(re.sub(r'\s+',' ', pg))]
print(len(hits), "coincidencias")   # → 14 en 12 páginas
EOF

# Índice de eficiencia con piso 0,01
grep -n "max(frac(c - c_min, c_max - c_min), 0.01)" capitulos/07_capitulo_06_evaluacion.typ  # → 07:297

# Bibliografía: entradas erróneas ausentes y correctas presentes
grep -n "bommasani\|dahl" manuscrito/referencias.bib            # → vacío
grep -n "bozdag2024\|magesh2025\|lewis2020\|niklaus2023\|codigo_mineria" manuscrito/referencias.bib
# → 5 entradas correctas

# Siglas sin uso
grep -n "NDCG\|HNSW" capitulos/acronimos_o_siglas.typ   # → 16, 26 (sin uso en el texto)
```

## Anexo B — Artefactos con el contenido ya calculado para cerrar pendientes

| Pendiente | Artefacto |
|---|---|
| §7.1–7.3 (tablas y cifras del análisis nuevo) | `correccion-01-analisis-estadistico/INFORME_ANALISIS_ESTADISTICO.md`, `salidas/30_tabla_celdas_principal.csv`, `salidas/31_efectos_simples_orientados.csv`, `figuras/02..04` |
| §7.1 (faltantes 23–25) | `correccion-02-diagnostico-gpt-5-nano/PROPUESTAS_MANUSCRITO.md` §1 |
| §7.4 (determinismo) | `correccion-03-documentar-api-eliminar-determinismo/propuestas_edicion.md` §3.1–3.8 |
| §7.7 (conclusiones) | `correccion-05-actualizacion-conclusiones-y-analisis-costos/PROPUESTA_TEXTO_MANUSCRITO.md` §2–§4, `ANALISIS_COSTOS.md` (Pareto) |
| §7.14 (extracción) | `correccion-06-precisar-corpus-revisar-respuestas/propuesta_edicion_manuscrito.md` §1.3 |
| §7.12 (refs cruzadas) | `correccion-07-forma-y-bibliografia/propuesta_edicion_manuscrito.md` |
| §7.16 (nDCG) | `verificacion-analisis-estadistico/metricas_recuperacion/` |

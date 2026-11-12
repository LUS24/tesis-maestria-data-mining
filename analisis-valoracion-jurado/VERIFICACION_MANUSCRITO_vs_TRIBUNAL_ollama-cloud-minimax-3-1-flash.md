---
title: "Verificación del manuscrito frente a la valoración del tribunal"
creator: "Revisión asistida por IA sobre los archivos .typ del repositorio"
created: "2026-11-12T22:45:00Z"
modified: "2026-11-12T22:45:00Z"
---

# Verificación del manuscrito frente a la valoración del tribunal

**Documento de referencia:** `analisis-valoracion-jurado/Valoracion_TF_Spairani_gp_actualizada.md` (Gastón Pezzuchi, noviembre de 2026).
**Objeto verificado:** archivos `manuscrito/capitulos/*.typ`, `manuscrito/main.typ` y `manuscrito/referencias.bib`.
**Commit verificado:** `6208cac` — *docs(readme): alinear el estado del repositorio con las revisiones* (12/11/2026 22:22).
**Fecha de la verificación:** 12/11/2026.
**Estado de compilación:** `typst compile main.typ` compila sin errores → **167 páginas** (la versión valorada tenía 165).

> Esta verificación es **editorial y documental**: contrasta lo que el manuscrito dice contra lo que la valoración exige. No recalcula resultados estadísticos ni revalida el benchmark; las cifras se contrastaron contra los artefactos ya producidos en `analisis-valoracion-jurado/correccion-01..07` y `verificacion-analisis-estadistico/`.

---

## 1. Alcance y método

1. Lectura íntegra de los 12 archivos `.typ` del manuscrito y de `main.typ`.
2. Compilación del manuscrito con Typst 0.14.2 y extracción del texto del PDF resultante para verificar lo que realmente se imprime (no sólo lo que dice el código fuente).
3. Contraste literal, punto por punto, contra las cuatro fuentes normativas de la valoración:
   - **V.1–V.11**: observaciones sustantivas.
   - **Tabla 2**: errores de forma del manuscrito.
   - **Tabla 3**: errores de citas y referencias.
   - **Tabla 4**: validación de las conclusiones.
   - **IX.1.1–IX.1.9**: correcciones requeridas (obligatorias).
   - **IX.2.1–IX.2.5**: recomendaciones (no bloquean la aprobación).
4. Contraste contra los textos propuestos en los paquetes de corrección ya producidos (`correccion-01` a `correccion-07`) para identificar qué ediciones se aplicaron y cuáles no.
5. Búsqueda de frases clave en el PDF compilado para detectar afirmaciones residuales.

**Convenciones de estado:** ✅ Cumplido · 🟡 Parcial · ❌ Pendiente · ⛔ Bloqueante para la defensa.

---

## 2. Veredicto ejecutivo

**El manuscrito absorbe la sustancia de la corrección metodológica, pero conserva el cuerpo viejo del capítulo de resultados.** Los tres cambios que el jurado declaró indispensables ("las correcciones 1 a 3") están escritos en el resumen y en las conclusiones, pero **el cuerpo del capítulo de evaluación sigue exponiendo el análisis anterior**. El resultado es un manuscrito internamente inconsistente: el mismo hallazgo aparece con dos bases de cálculo (684 y 711 observaciones) y dos valores (medianas 0,625 / 0,667; 0,958 / 1,000).

| Bloque | Estado | Comentario |
|---|---|---|
| Título, portada y alcance | ✅ | Título actualizado a "prototipo Agentic-RAG… Código de Minería argentino" en `main.typ` y portada. |
| Resumen | ✅ | Reescrito con el modelo ordinal mixto y los tres efectos con IC 95 %. |
| Declaraciones de IA | ✅ | Declaración por etapas (extracción, benchmark, respuestas, jueces, asistencia) + antecedente de la referencia fabricada. |
| Diagnóstico celda nano (41/79) | 🟡 | Las cifras están en el resumen, en las debilidades del capítulo 6 y en las contribuciones; falta la subsección de diagnóstico con evidencia de logs y la tabla de tasas por celda. |
| Corrección de los 27 faltantes | ❌ | El texto sigue atribuyéndolos a "fallos puntuales en la generación" y sigue declarando 684 observaciones. |
| Análisis inferencial del cuerpo | ❌ | Kruskal–Wallis, Dunn, Mann–Whitney y SRH siguen siendo el cuerpo del capítulo 6; el modelo ordinal aparece como "análisis de robustez" en metodología pero como "análisis principal" en el resumen. |
| Determinismo / temperatura | ❌ | 6 frases residuales (5 en metodología, 1 en evaluación) que afirman determinismo y reproducibilidad por temperatura 0. |
| Tabla 4 (conclusiones) | 🟡 | 8 de 9 filas reformuladas; quedan dos formulaciones que contradicen el texto nuevo ("mejora significativa con recuperación", "degradación con modelos pequeños"). |
| Tabla 2 (forma) | 🟡 | 7 de 12 ítems corregidos; persisten n-gramas, "similitud coseno escalada", GPT-4/MoE, dedicatoria y las referencias cruzadas duplicadas. |
| Tabla 3 (bibliografía) | ✅ (1 salvedad) | Corregidos Bommasani→Bozdag, Dahl→Magesh, Wei 2022a/b, duplicación DeepSeek/Meta, LEXTREME, Tribunal Fiscal, y añadidos Lewis et al. (2020) y el Código de Minería. |
| IX.2 (recomendaciones) | ❌/🟡 | Métricas de recuperación aplicadas (🟡); auditorías de citas, validación humana, réplicas, ablación y reducción editorial no ejecutadas (❌), pero las tres últimas están declaradas como limitación. |

**Bloqueantes para la defensa (⛔):**

1. La sección "Imputación de Valores Fuera de Rúbrica" (`07_capitulo_06_evaluacion.typ:73`) afirma que 27 observaciones se perdieron por fallos de generación y que el análisis corrió sobre 684 observaciones. El análisis canónico corre sobre **711** (79 unidades × 9 configuraciones), con los casos 23–25 reincorporados. El manuscrito, tal como está, describe un análisis que no es el que sustenta sus propias conclusiones.
2. Las tablas 11 y 13 del capítulo 6 (`07_capitulo_06_evaluacion.typ:158` y `:190`) reproducen medianas calculadas sobre 76 observaciones por celda; cinco de las nueve medianas cambian al usar las 79 (documentado en `correccion-01/INFORME_ANALISIS_ESTADISTICO.md` §6).
3. El marco metodológico y el capítulo de resultados no coinciden: `06_capitulo_05_metodologia.typ:708` describe el modelo ordinal como "análisis de robustez", mientras que el resumen lo llama "el análisis". Ningún Friedman, Wilcoxon ni bootstrap por casos aparece en el manuscrito, aunque la limitación de `09_capitulo_08…:71` afirma que "la inferencia principal se apoya en las pruebas pareadas y en los intervalos de confianza".
4. Las afirmaciones de determinismo y de reproducibilidad por temperatura 0 (6 ocurrencias) contradicen la declaración de IA y la nota sobre parámetros de API ya corregidas.

---

## 3. Cobertura de las observaciones sustantivas (V.1–V.11)

| Obs. | Exigencia del jurado | Estado | Evidencia en el manuscrito | Pendiente |
|---|---|---|---|---|
| **V.1** | Rehacer la inferencia respetando apareamiento y anidamiento; efectos e IC; corregir la mención a modelos mixtos | 🟡 | `01_texto_preliminar.typ:4` y `09_capitulo_08…:31` reportan el modelo ordinal mixto (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²) con efectos e IC. `06_capitulo_05_metodologia.typ:708` documenta la especificación (`clmm`, `nAGQ = 1`). | El capítulo 6 mantiene el análisis para muestras independientes como cuerpo del texto (`07…:93-230`) y la tabla de efectos simples sigue siendo Mann-Whitney (`07…:158`). Faltan las tablas canónicas de celdas y de efectos (propuestas en `correccion-01/PROPUESTA_TEXTO_MANUSCRITO.md` §3.4-3.5) y la sensibilidad Friedman/Wilcoxon/bootstrap por casos. |
| **V.2** | Sustituir el sustento de la interacción (SRH) | 🟡 | `07…:135` y `07…:222` declaran SRH como "antecedente exploratorio" y remiten al modelo ordinal. | La sección "Test de Scheirer-Ray-Hare" (`07…:195-226`) sigue íntegra, con la fórmula y la tabla H completa; debe pasar a anexo. |
| **V.3** | No inferir equivalencia de la falta de significación | ✅ | `07…:131` ("no se afirma equivalencia"), `07…:446`, `09…:35` ("Límites de la hipótesis de igualación por RAG básico"). | — |
| **V.4** | Retirar el determinismo; informar el esfuerzo de razonamiento; declarar la ejecución única | ❌ | `06…:497` y `06…:475` explican que `temperature=0.0` fue solicitado pero no aplicado y que `reasoning_effort` no quedó registrado (`01_texto_preliminar.typ:28`). | 5 frases residuales (ver §8, P-01) y falta la limitación de ejecución única en el capítulo 8. |
| **V.5** | Factores confundidos, prompts, contradicciones sobre el Agente de Calidad y el límite de búsquedas | ✅ | `06…:284` ("Alcance operativo y factores confundidos"), `06…:292-318` (Agente de Calidad: excluido por costo y complejidad, sin comparación empírica), `06…:284-290` y `06…:435-455` (límites 6/7 y excepción `16_01`), `04_capitulo_03…:89` (zero-shot, sin CoT). | Falta reproducir literalmente el prompt de sin RAG / RAG básico y los de los jueces (P-09). |
| **V.6** | Informar las 41 salidas no sustantivas; reincorporar casos 23–25; corregir los faltantes; reformular la "sobrecarga agéntica" | 🟡 | `07…:440` y `09…:33` describen 41/79 no sustantivas y la calidad condicional (38/79; media 0,820; mediana 0,958) como "modo de fallo de respuesta". | `07…:73` conserva la explicación errónea de los 27 faltantes y las 684 observaciones (⛔). Falta la subsección de diagnóstico con evidencia de logs (tasa con IC de Wilson, `finish_reason`, tokens) y la tabla por celda. `07…:164` y `07…:256` conservan las atribuciones causales (P-03). |
| **V.7** | Validez de la medición: benchmark, respuestas de referencia, jueces | 🟡 | `06…:564-576` (revisión por una profesional, sin segunda), `09…:37` ("Confiabilidad inter-juez, no validación"), `09…:87` (23 discrepancias, 17 puntajes positivos sobre salidas no sustantivas), `anexo_01.typ:305` (respuesta 1.2 corregida al art. 11) y `:307` (art. 17 con las tres causales). | Sin validación humana de las respuestas generadas (limitación declarada, `09…:89`). Sin métricas deterministas de citas (IX.2.2, cancelada por tiempo: NV-03). |
| **V.8** | Informar medidas de recuperación | ✅ (parcial) | `07…:312-330`: tabla con recall en top-10, MRR, % de unidades con todos / sin ningún artículo de referencia, para el baseline y las tres células agénticas; se declara que la comparación no es causal. | No hay nDCG ni Hit@k; las siglas `NDCG` y `HNSW` siguen listadas sin uso (`acronimos_o_siglas.typ`). No hay comparación con BM25 u otro embedding (declarado como no posible por pérdida del volumen de Milvus, `07…:330`). |
| **V.9** | Versión y calidad del corpus; unificar conteos; revisar respuestas de referencia | 🟡 | `06…:51` (procedencia: PDF 1997 + contraste con Infoleg, con los artículos 3, 31, 215 y 221 como evidencia), `06…:77-96` (482 partes; 398 artículos = 347 + 15 + 36; 362 números únicos; art. 239 derogado y vacío), `anexo_01.typ:251` (sanción 1886-11-25), `02_capitulo_01…:19` (procedencia corregida). | `06…:67` ("Validación de Calidad de Extracción") sigue diciendo "inspección manual de una muestra" sin tamaño, sin tasa de error y sin declarar que no existe métrica de error (P-08). |
| **V.10** | Costos: retirar el índice con piso arbitrario; Pareto o costo por respuesta correcta | 🟡 | `07…:444-452` reporta el costo por respuesta correcta (RAG básico + nano: USD 0,0061; 33/79) yAgentic-RAG + mini como alternativa no dominada; `09…:57` matiza la recomendación. | La sección "Índice de Eficiencia" (`07…:289-306`) **sigue en el cuerpo** con el piso 0,01 que el jurado}}}$ objetó. No hay frontera de Pareto (P-05). |
| **V.11** | Título, objetivos, alcance, repositorio y declaración de IA | 🟡 | Título en `main.typ:4` y portada; `01_texto_preliminar.typ:18-28` (declaración ampliada); `09…:21` (repositorio publicado y auditable). | El objetivo general sigue prometiendo "usuarios profesionales y no profesionales" (`02_capitulo_01_introduccion.typ:105`) y el objetivo específico 2 sigue siendo genérico (`:111`); las "Contribuciones principales" de la introducción (`:133-143`) no reflejan el alcance acotado (P-06). |

---

## 4. Cobertura de las correcciones requeridas (IX.1)

| Punto | Estado | Detalle |
|---|---|---|
| **IX.1.1** Rehacer la inferencia con apareamiento y anidamiento; efectos e IC; corregir la mención a modelos mixtos | 🟡 | El modelo ordinal sí está (metodología y resumen/conclusiones) y la mención a "modelos mixtos" ya no es engañosa: `06…:708` lo describe como "modelo ordinal acumulativo" y `09…:71` declara la aproximación de Laplace. **Pero el cuerpo del capítulo 6 no lo contiene.** Faltan las tablas canónicas y la sensibilidad no paramétrica. |
| **IX.1.2** Informar las 41 salidas; reincorporar 23–25; corregir los faltantes; reformular la "sobrecarga agéntica" | 🟡 | Lo reformulado está en resumen, debilidades y conclusiones. **Lo no reformulado:** `07…:73` (faltantes), `07…:164` y `09…:75` ("Degradación con modelos pequeños"). |
| **IX.1.3** Retirar el determinismo; informar el esfuerzo de razonamiento; declarar la ejecución única | ❌ | 5 frases con afirmaciones de determinismo/reproducibilidad (P-01). La limitación de ejecución única **no existe** en el capítulo 8. |
| **IX.1.4** Declarar factores confundidos, publicar prompts y resolver contradicciones | 🟡 | Los factores confundidos, la arquitectura acotada, la desactivación del Agente de Calidad y los límites 6/7 están resueltos. Falta la reproducción literal de los prompts de las líneas base y de los jueces y no existe `anexo_02_prompts_y_parametros.typ` (P-09). |
| **IX.1.5** Reformular las conclusiones de la Tabla 4 | 🟡 | 7 de 9 filas reformuladas (ver §6). Restan "Mejora significativa con recuperación" (`09…:55`), "Configuración costo-eficiente viable" (`09…:57`) y "Degradación con modelos pequeños" (`09…:75`). |
| **IX.1.6** Precisar corpus, origen y respuestas de referencia | 🟡 | Procedencia, conteos, fecha de sanción y respuestas 1.2/1.3 corregidos. Falta el tratamiento de la calidad de extracción (`06…:88`, P-08). |
| **IX.1.7** Corregir las Tablas 2 y 3 y auditar la bibliografía | 🟡 | Tabla 3: ✅. Tabla 2: 4 ítems pendientes (P-07). |
| **IX.1.8** Ampliar la declaración de uso de IA | ✅ | `01_texto_preliminar.typ:18-28`: por etapas, con modelos nombrados y con el antecedente de la referencia fabricada y su eliminación. |
| **IX.1.9** Informar las medidas de recuperación | ✅ | `07…:312-330`, con la advertencia metodológica correspondiente. |

---

## 5. Cobertura de las recomendaciones (IX.2)

| Punto | Estado | Detalle |
|---|---|---|
| **IX.2.1** Comparar el embedding con un recuperador entrenado y con BM25 | ❌ | No ejecutado: el volumen de Milvus se perdió. El manuscrito lo declara (`07…:330`). |
| **IX.2.2** Métricas deterministas de citas (precisión, exhaustividad, artículos inexistentes) | ❌ | No ejecutado (NV-03, cancelado por tiempo). No aparece como trabajo futuro en el manuscrito. |
| **IX.2.3** Validar una submuestra con profesionales | ❌ | No ejecutado; declarado como limitación (`09…:89`). |
| **IX.2.4** Réplicas y ablación | ❌ | No ejecutado; el manuscrito advierte que no se recomienda sin réplicas (`07…:452`) pero **no lo declara como limitación de las estimaciones**. |
| **IX.2.5** Reducir el capítulo 2 y la sección 7.7 | ❌ | No ejecutado: el capítulo 2 sigue ocupando ~18 páginas (pp. 30-47) y la sección 7.7 "Desarrollos Posteriores al Período Experimental" conserva 4 subsecciones y ~4 páginas (pp. 108-111). |

---

## 6. Estado de las conclusiones (Tabla 4 del jurado)

| Conclusión del jurado | Estado en el manuscrito | Nota |
|---|---|---|
| "La recuperación mejora significativamente la calidad" | 🟡 Parcial | `07…:433` la reformula por modelo ("no produce una mejora uniforme"); pero `09…:55` la mantiene en las fortalezas con los p del análisis viejo. |
| Interacción estrategia × modelo como hallazgo principal | ✅ | `01…:4`, `07…:445`, `09…:31` con el modelo ordinal y la advertencia de que no identifica un componente causal. |
| "Efecto igualador del RAG básico" | ✅ | Retirada (`07…:131`, `09…:35`). |
| "Sobrecarga agéntica" | 🟡 Parcial | Reformulada a "modo de fallo de respuesta" en resumen y conclusiones; sobrevive en `07…:164` y `09…:75`. |
| "Validación de LLM-as-a-Judge" | ✅ | `09…:37` la reformula como "confiabilidad inter-juez, no validación"; `09…:89` declara la ausencia de validación humana. |
| Objetivo 2 "se cumplió completamente" | ✅ | `09…:17` lo declara "cumplimiento parcial" con el detalle de los componentes activos e inactivos. |
| "Combinación costo-eficiente: Agentic-RAG + gpt-5-mini" | ✅ | `07…:434` y `07…:450`: alternativa no dominada, no la más barata; `09…:57` matizado. |
| "Transferible a otros dominios" | ✅ | `09…:45` y `09…:142` lo acotan al corpus, los 25 casos, la ejecución única y el recuperador fijo. |
| Atención a "usuarios profesionales y no profesionales" | 🟡 Parcial | Declarado como limitación (`09…:83`) pero el objetivo general de la introducción sigue prometiéndolo (`02…:105`). |

---

## 7. Errores de forma (Tabla 2) y bibliografía (Tabla 3)

### Tabla 2 — 12 ítems

| Ítem del jurado | Estado | Ubicación actual |
|---|---|---|
| p. 1: oración trunca "Al combinar grandes modelos de lenguaje…" | ✅ | `02_capitulo_01_introduccion.typ:9` |
| p. 12: n-gramas como "secuencias de caracteres" con ejemplo de palabras | ❌ | `03_capitulo_02_fundamentos_e_historia_pln.typ:101` |
| p. 23: "similitud coseno escalada" | ❌ | `03…:333` |
| pp. 25-26: GPT-4 "introduce arquitectura MoE" | ❌ | `03…:371` y `03…:409` |
| pp. 30, 32: LEGAL-BERT / Case Law Access Project / LegalBench | ✅ | `04_capitulo_03…:29` y `:65` separan las tres fuentes y niegan la evaluación anacrónica |
| p. 36: "el Código solo tiene 245 artículos" | ✅ | Ausente; `06…:84` reporta 398 nodos de tipo artículo |
| pp. 106-110: fechas de DeepSeek-R1, Llama 4, Qwen3, Gemini 3 Pro | ✅ | `08_capitulo_07…:253` (R1, enero de 2025), `:259` (Llama 4, abril de 2025), `:257` (Qwen3, abril de 2025), `:156` y `:191` (Gemini 3 Pro, 18 de noviembre) |
| p. 147: fecha de sanción 1994-01-01 | ✅ | `anexo_01.typ:251` → 1886-11-25 |
| pp. 34, 38, 73: "capítulo Sección 4", "sección Sección 4.7" | ❌ | **14 ocurrencias en 12 páginas del PDF**: el texto manual dice "capítulo"/"sección" y `@cap:…`/`@sec:…` se renderiza como "Sección N" (`04…:3, 83, 89, 125, 135`; `06…:102, 171, 212, 358, 603`; `07…:16, 337`; `09…:89`) |
| p. 29: nota 13 con remisión a Wikipedia | ✅ | La nota fue reemplazada por una fuente académica o eliminada; no queda ninguna remisión a Wikipedia |
| p. iii: dedicatoria "A mi familia …" | ❌ | `01_texto_preliminar.typ:15` |
| p. iv: declaración de IA de una sola oración | ✅ | `01_texto_preliminar.typ:18-28` |

### Tabla 3 — 9 ítems

| Ítem | Estado | Nota |
|---|---|---|
| Bommasani et al. (2023) → Bozdag, Sevim y Koç (2024) | ✅ | `referencias.bib` clave `bozdag2024gender`, DOI 10.1145/3628602; el texto ya no le atribuye adapters (`04…:69`, `:95`) |
| Estudio de alucinaciones atribuido a Dahl et al. (2024) | ✅ | `magesh2025hallucinationfree`, DOI 10.1111/jels.12413, citado en `08…:29` |
| Wei et al. (2022) y Zhao et al. (2026) sin distinguir | ✅ | El PDF muestra "Wei et al. (2022a)" y "(2022b)" |
| DeepSeek (2026b) y Meta (2026) duplicados y mal fechados | ✅ | `deepseek2025r1` (20/01/2025) y `llama4` (05/04/2025) |
| Niklaus et al. (2024) LEXTREME vs. Findings EMNLP 2023 | ✅ | `niklaus2023lextreme` con DOI 10.18653/v1/2023.findings-emnlp.200 |
| Tribunal Fiscal de la Nación (2026) con URL de un estudio | ✅ | `tribunalfiscal2024buscador` con la página institucional |
| Falta Lewis et al. (2020) y el Código de Minería | ✅ | `lewis2020rag` citada en `02…:11`; `codigo_mineria_1919` con fecha de sanción correcta |
| Preprints con versión con arbitraje | 🟡 | Parcial: Self-RAG, BERT, QLoRA y Self-RAG tienen versión publicada; persisten entradas `@misc` de notas de lanzamiento de proveedores (aceptable para material de modelo, pero conviene revisarlo) |
| "y col." / "y cols." y fecha de consulta como fecha de publicación | ✅ | El estilo APA automático de Typst produce "et al." de forma uniforme; 0 apariciones de "y col(s)." en el PDF |

**Observación menor de maquetación de la bibliografía:** 2 entradas imprimen el año con una coma colgante — "(2024, )" (Self-RAG) y "(2022, )" (LoRA) — por no tener `month` en el `.bib`.

---

## 8. Pendientes detallados

Ordenados por criticidad para la defensa. Cada ítem indica el archivo y la línea exacta.

### ⛔ P-01 — Afirmaciones de determinismo y de reproducibilidad (V.4, IX.1.3)

| Archivo:línea | Texto actual | Corrección propuesta en `correccion-03/propuestas_edicion.md` |
|---|---|---|
| `06_capitulo_05_metodologia.typ:191` | "Se emplea la misma configuración de agente (Pydantic AI con temperatura 0) que en el baseline sin RAG" | §3.1: separar la configuración del agente de la temperatura, no aplicada |
| `06_capitulo_05_metodologia.typ:511` | "+ Soporte para generación con temperatura cero (respuestas determinísticas)." | §3.4: eliminar el ítem de los criterios de selección |
| `06_capitulo_05_metodologia.typ:521` | "Todos los modelos fueron configurados con temperatura 0 para maximizar la reproducibilidad de las respuestas." | §3.5: describir lo solicitado, lo aplicado y la ejecución única |
| `06_capitulo_05_metodologia.typ:614` | "Los tres modelos fueron configurados con temperatura 0,0 y un límite de 5.000 tokens de salida." | §3.6: aclarar que corresponde a los jueces y no a los generadores GPT-5 |
| `06_capitulo_05_metodologia.typ:660` | "+ Temperatura 0 para respuestas determinísticas (evita múltiples ejecuciones)." | §3.7: "Una única ejecución por unidad y configuración, sin réplicas" |
| `07_capitulo_06_evaluacion.typ:16` | "…con temperatura 0 en todas las configuraciones para garantizar reproducibilidad." | §3.8: una única ejecución; la configuración no garantiza determinismo |

### ⛔ P-02 — Faltantes: explicación errónea y base de cálculo (V.6, IX.1.2)

`07_capitulo_06_evaluacion.typ:73`:

> "Adicionalmente, se identificaron 27 observaciones (3.8% del total) con valores ausentes en las métricas de evaluación por jueces, **atribuibles a fallos puntuales en la generación de respuestas** para ciertas combinaciones subpregunta-configuración. Estos valores fueron excluidos de las pruebas de hipótesis mediante eliminación por lista (listwise deletion), **reduciendo el conjunto efectivo a 684 observaciones**…"

Debe reemplazarse por el texto de `correccion-02/PROPUESTAS_MANUSCRITO.md` §1: las 27 ausencias eran un **defecto de join** (subpregunta vacía en el archivo de métricas y `0` en el de jueces) de los casos 23, 24 y 25; normalizada la clave se recuperaron **711 observaciones y 2.133 evaluaciones**. En coherencia, deben actualizarse la Tabla de medianas (`07…:190`), la Tabla de efectos simples (`07…:158`) y todas las cifras derivadas (5 de las 9 medianas cambian; ver `correccion-01/INFORME_ANALISIS_ESTADISTICO.md` §6).

### ⛔ P-03 — Cuerpo del capítulo de evaluación: análisis viejo y atribuciones causales (V.1, V.5, V.6, IX.1.1, IX.1.5)

- `07…:93-133` — Kruskal–Wallis y Dunn como sección principal (sólo deben quedar como antecedente exploratorio).
- `07…:135-167` — tabla de efectos simples con **Mann-Whitney U** y p de la base de 684; debe ser la tabla canónica de efectos del modelo ordinal (Δ media, IC 95 %, Δ P(≥ 0,75), p Holm), según `correccion-01/PROPUESTA_TEXTO_MANUSCRITO.md` §3.5.
- `07…:169-190` — Tabla de medianas con los valores de 76 observaciones por celda; debe incorporar `n`, nº de no sustantivas, media, mediana, media modelada y P(≥ 0,75) por celda (§3.4).
- `07…:195-226` — sección SRH completa (procedimiento, fórmula, tabla H); a anexo.
- `07…:164` — "Esto sugiere que la **complejidad agéntica es excesiva** para modelos de capacidad reducida."
- `07…:256` — "gpt-5 es robusto … **mediante su capacidad de razonamiento interna**."
- `07…:262-266` — "La interacción significativa **matiza las conclusiones del análisis de Kruskal-Wallis**".
- `06_capitulo_05_metodologia.typ:41` — la fase de análisis estadístico no menciona el modelo ordinal.
- `06_capitulo_05_metodologia.typ:562` — "cada subpregunta constituye una **unidad de evaluación independiente**".
- `06_capitulo_05_metodologia.typ:692-710` — la subsección de análisis estadístico mantiene Shapiro–Wilk/KW/Dunn/SRH como marco y relega el modelo ordinal a "análisis de robustez"; el resumen lo llama "el análisis".
- `06_capitulo_05_metodologia.typ:757` — "El análisis estadístico detallado —que comprende pruebas de normalidad (Shapiro-Wilk), comparaciones no paramétricas (Kruskal-Wallis con post-hoc de Dunn), análisis de interacción factorial (Scheirer-Ray-Hare)…— proporciona un marco riguroso".
- `02_capitulo_01_introduccion.typ` (estructura del trabajo, cap. 6) — "el análisis estadístico (Kruskal-Wallis, Dunn, Scheirer-Ray-Hare, Krippendorff's alpha)".

### 🟡 P-04 — Fortalezas y limitaciones del capítulo 8 con las cifras del análisis viejo (IX.1.5)

- `09…:55` — "**Mejora significativa con recuperación.** Tanto el RAG básico como el Agentic-RAG superan significativamente al baseline sin RAG ($p < 0.001$ …; $p = 0.0066$ …)" → sustituir por la versión con efectos e IC de `correccion-05/PROPUESTA_TEXTO_MANUSCRITO.md` §4.4.
- `09…:57` — "Configuración costo-eficiente viable … comparable al 0.80 de gpt-5" → contrastar con las medias canónicas (0,788 y 0,812) y con la ausencia de Pareto.
- `09…:63` — "Análisis estadístico riguroso (Shapiro-Wilk, Kruskal-Wallis, Dunn con Bonferroni, Scheirer-Ray-Hare) … (Mann-Whitney U con corrección de Holm-Bonferroni…)" → sustituir por la descripción del modelo ordinal.
- `09…:73` — "Ausencia de diferencia marginal entre Agentic-RAG y RAG básico ($p = 0.383$)" → "No se demostró una superioridad global de Agentic-RAG".
- `09…:75` — "**Degradación con modelos pequeños.** El sistema Agentic-RAG perjudica el desempeño de gpt-5-nano… ($p_corr = 0.017$…)" → "Modo de fallo de respuesta en Agentic-RAG + gpt-5-nano", coherente con `09…:33`.
- `09…:85` — "Alcance temporal" sin la configuración 7/6 búsquedas.

### 🟡 P-05 — Costos: índice con piso arbitrario y ausencia de Pareto (V.10, IX.1.5)

- `07…:289-306` — sección "Índice de Eficiencia" con `max(…, 0.01)`: el índice fue precisamente el objeto de la crítica V.10. Debe salir del cuerpo (anexo rotulado como sensibilidad) o eliminarse.
- `07…:304` — la figura `eficiencia_costo.pdf` debe salir del cuerpo con ella.
- `07…:447-452` — falta la frontera de Pareto (siete de las nueve configuraciones son no dominadas) y la tabla de costo por respuesta correcta (≥ 0,75) con IC bootstrap, ya disponible en `correccion-05/ANALISIS_COSTOS.md`.

### 🟡 P-06 — Alcance, objetivo general y contribuciones de la introducción (V.11, IX.1.5)

- `02_capitulo_01_introduccion.typ:105` — "…para responder consultas de **usuarios profesionales y no profesionales** en el derecho." → reemplazado propuesto en `correccion-05/PROPUESTA_TEXTO_MANUSCRITO.md` §2.1.
- `02…:111` — objetivo específico 2 sin acotar (la versión definitiva debe decir dos agentes activos, una delegación, sin verificador).
- `02…:131-145` — "Contribuciones principales" sin el alcance acotado, sin el modo de fallo y sin el modelo ordinal (propuesta en §2.3 del mismo documento).
- `09…:136` — queda la fórmula "validación mediante LLM-as-a-Judge" en Trabajos futuros.

### 🟡 P-07 — Tabla 2 pendiente (forma)

- `03_capitulo_02_fundamentos_e_historia_pln.typ:101` — n-gramas: definir como secuencias de *n* unidades y aclarar que el ejemplo usa palabras.
- `03…:333` — sustituir "similitud coseno escalada" por producto escalar escalado por `1/sqrt(d_k)` (la fórmula ya presente es la correcta).
- `03…:371` y `03…:409` — retirar la atribución de arquitectura MoE a GPT-4 o respaldarla con fuente primaria.
- `01_texto_preliminar.typ:15` — completar o eliminar la dedicatoria.
- **Referencias cruzadas duplicadas** (14 ocurrencias en 12 páginas del PDF): el texto dice "capítulo"/"sección" y la referencia `@cap:…`/`@sec:…` se imprime como "Sección N". Ubicaciones: `04_capitulo_03…:3, 83, 89, 125, 135`; `06_capitulo_05…:102, 171, 212, 358, 603`; `07_capitulo_06…:16, 337`; `09_capitulo_08…:89`. Solución: usar `#ref(<etiqueta>, supplement: [Capítulo])` / `[Sección]` según corresponda, o reescribir el texto manual ("…del capítulo de metodología"). Es el defecto más visible en el PDF.

### 🟡 P-08 — Calidad de la extracción del corpus (V.9, IX.1.6)

`06_capitulo_05_metodologia.typ:67`:

> "La calidad de la extracción se verificó mediante **inspección manual de una muestra de artículos**, comparando el texto extraído con el original en Infoleg. Se establecieron criterios de calidad basados en la completitud del texto…"

No informa tamaño de la muestra, ni tasa de error, ni estratificación. El texto propuesto en `correccion-06/propuesta_edicion_manuscrito.md` §1.3 es más honesto: la revisión fue manual por archivo y **no se conserva un registro cuantitativo de discrepancias ni una tasa de error**; por tanto, no se afirma una validación estadística de la extracción.

### 🟡 P-09 — Prompts no reproducidos (IX.1.4)

Se reproducen literalmente tres prompts (Especialista `06…:235`, Recuperación `06…:266`, Agente de Calidad `06…:305`). **No se reproducen**: el prompt de sin RAG, el de RAG básico (`06…:321` los describe sólo como "prompt simplificado") ni los prompts de los jueces con sus rúbricas. El plan prevé `manuscrito/capitulos/anexo_02_prompts_y_parametros.typ`, que **no existe**; hoy el texto remite al "anexo de prompts del repositorio", es decir, fuera del manuscrito.

### 🟡 P-10 — Limitaciones que faltan en el capítulo 8 (V.4, IX.1.3, IX.2.4)

Deberían incorporarse, según `correccion-01/PROPUESTA_TEXTO_MANUSCRITO.md` §4.5 y `correccion-03/propuestas_edicion.md` §2:

1. **Ejecución única y ausencia de control efectivo de muestreo** — es la limitación que sostiene el resto (no se puede separar el efecto de los factores de la variabilidad entre corridas). Hoy sólo aparece implícita en el resumen y en "Reflexiones finales".
2. **Tratamiento de las respuestas no sustantivas** (escenario fallo = 0 vs. exclusión) y su carácter normativo, no mediacional.
3. **Factores confundidos y ausencia de ablaciones**.
4. **Costos históricos y ausencia de costos de producción** (infraestructura, latencia, mantenimiento, interfaz, costos humanos).
5. Revisar `09…:71`: afirma que "la inferencia principal se apoya en las pruebas pareadas y en los intervalos de confianza", pero **las pruebas pareadas no están en el manuscrito** (o se las incorpora, o se reescribe la frase).

### 🟡 P-11 — Recuperación y siglas (V.8, IX.1.9, IX.2.1)

- `acronimos_o_siglas.typ` mantiene `NDCG` y `HNSW`, que no se usan en ningún punto del texto (el jurado ya había señalado las siglas sin uso). `BM25` sí aparece, pero sólo como línea de trabajo futura.
- `07…:312-330` informa recall@10 y MRR; no hay Hit@k ni nDCG@k (las cifras están disponibles en `verificacion-analisis-estadistico/metricas_recuperacion/`).
- No hay comparación con BM25 ni con un embedding de recuperación; el motivo se declara en el texto, pero conviene dejar constancia de que es una limitación y no sólo una nota metodológica.

### 🟡 P-12 — Citas deterministas e IX.2.2 (V.7)

No se calculó precisión/exhaustividad de citas ni la tasa de artículos inexistentes sobre las 711 respuestas (NV-03, cancelada por tiempo). El manuscrito no lo anuncia como trabajo futuro: conviene agregarlo a "Ampliación del Benchmark" o a "Trabajos Futuros", porque el jurado lo presenta, en el marco teórico, como el riesgo central del dominio.

### ❌ P-13 — Reducción editorial (IX.2.5)

- Capítulo 2: pp. 30-47 (~18 páginas), de los cuales la cronología año por año y las arquitecturas recurrentes (perceptrón, RNN, LSTM, GRU) ocupan una parte desproporcionada respecto de su uso posterior. Puede recortarse o trasladarse a un anexo.
- Sección 7.7 "Desarrollos Posteriores al Período Experimental": pp. 108-111, con 4 subsecciones y afirmaciones comerciales de 2026 sobre modelos que no participaron en el experimento. El texto de `08…:321` ya evita el tono causal, pero la sección conserva extensión y peso.

### ❌ P-14 — Figuras nuevas no incorporadas

Las figuras del análisis canónico (`correccion-01/figuras/02_interaccion_prob_ge_075.pdf`, `03_efectos_simples_probabilidad.pdf`, `04_sensibilidad_escenarios.pdf`) y las del diagnóstico (`correccion-02/figuras/01..03`) **no están en `manuscrito/media/`** ni referenciadas en el manuscrito. Sin ellas, el capítulo 6 sigue apoyándose en las figuras del análisis histórico (`interaccion_modelo_estrategia.pdf`, `boxplots_por_estrategia.pdf`).

---

## 9. Checklist previo a la defensa

Orden sugerido, por dependencia entre tareas.

- [ ] **A.** Corregir `07…:73` (faltantes 23–25 y base de 711) y regenerar las tablas 11 y 13 sobre 79 unidades por celda.
- [ ] **B.** Sustituir el cuerpo inferencial del capítulo 6 por el bloque canónico (especificación del modelo, interacción, efectos simples con IC, sensibilidad a los escenarios, comparación con las pruebas pareadas) y trasladar KW/Dunn/MW/SRH a un anexo "análisis exploratorio histórico".
- [ ] **C.** Añadir al capítulo 6 las tablas de celdas y de efectos con `n`, no sustantivas, media, mediana, media modelada y P(≥ 0,75); incorporar las figuras canónicas.
- [ ] **D.** Eliminar las 6 afirmaciones de determinismo/temperatura (P-01).
- [ ] **E.** Retirar el índice de eficiencia con piso 0,01 e incorporar Pareto + costo por respuesta correcta (P-05).
- [ ] **F.** Rehacer las fortalezas y limitaciones del capítulo 8 y añadir las 5 limitaciones faltantes (P-04, P-10).
- [ ] **G.** Corregir el objetivo general, el objetivo específico 2 y las contribuciones de la introducción (P-06).
- [ ] **H.** Corregir los 5 ítems de forma pendientes, empezando por las 14 referencias cruzadas duplicadas (P-07).
- [ ] **I.** Corregir la sección de validación de la extracción (P-08) y completar la reproducción de prompts (P-09).
- [ ] **J.** Limpiar las siglas sin uso, añadir nDCG/Hit@k si están disponibles y dejar constancia de la comparación pendiente con BM25 (P-11).
- [ ] **K.** Anunciar las citas deterministas como trabajo futuro (P-12).
- [ ] **L.** Recortar el capítulo 2 y la sección 7.7, o dejarlos expresamente como trabajo futuro del jurado (P-13).
- [ ] **M.** Compilar, releer el resumen y las conclusiones contra el capítulo 6 (una sola pasada de coherencia numérica) y verificar la bibliografía.

---

## Anexo A — Comprobaciones automáticas ejecutadas

```bash
# Compilación y texto plano del PDF final
cd manuscrito && typst compile main.typ /tmp/verificacion_jurado.pdf
pdftotext /tmp/verificacion_jurado.pdf /tmp/verificacion_jurado.txt

# 1. Determinismo y temperatura
grep -rn "determin\|temperatura 0\|temperatura cero\|evita múltiples ejecuciones" manuscrito/capitulos/*.typ
# → 06…:191, 06…:511, 06…:521, 06…:614, 06…:660, 07…:16

# 2. Faltantes y base de cálculo
grep -rn "684\|27 observaciones\|atribuibles a fallos puntuales" manuscrito/capitulos/*.typ
# → 07…:73

# 3. Referencias cruzadas duplicadas en el PDF compilado
python3 - <<'EOF'
import re
raw = open('/tmp/verificacion_jurado.txt', encoding='utf-8').read()
pat = re.compile(r'(capítulo|sección)\s+Sección\s+[0-9.]+', re.I)
for i, pg in enumerate(raw.split('\f'), 1):
    for m in pat.finditer(re.sub(r'\s+', ' ', pg).replace('­', '')):
        print(f"pág. PDF {i}: {m.group(0)}")
EOF
# → 14 coincidencias en 12 páginas

# 4. Afirmaciones causales residuales
grep -rn "complejidad agéntica es excesiva\|capacidad de razonamiento interna\|p = 0.383" manuscrito/capitulos/*.typ
# → 07…:164, 07…:256, 09…:73

# 5. Objetivo general y deducciones
grep -n "Objetivo general" -A 4 manuscrito/capitulos/02_capitulo_01_introduccion.typ

# 6. Estado del índice de eficiencia
grep -n "Índice de Eficiencia" -A 20 manuscrito/capitulos/07_capitulo_06_evaluacion.typ

# 7. Bibliografía: entradas con año y coma colgante en la salida APA
grep -o "([0-9]\{4\}, )" /tmp/verificacion_jurado.txt | sort | uniq -c
# → 2 (Self-RAG 2024, LoRA 2022)
```

## Anexo B — Artefactos de referencia para cerrar los pendientes

| Pendiente | Artefacto con el contenido ya calculado |
|---|---|
| P-02, P-03 (tablas y cifras) | `analisis-valoracion-jurado/correccion-01-analisis-estadistico/INFORME_ANALISIS_ESTADISTICO.md` (§6 y §8.3), `salidas/30_tabla_celdas_principal.csv`, `salidas/31_efectos_simples_orientados.csv`, `figuras/02..04` |
| P-02 (diagnóstico nano) | `analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/PROPUESTAS_MANUSCRITO.md` (§1-§3), `salidas/14_dataset_categoria_final.csv`, `salidas/03_conteo_categorias_por_celda.csv` |
| P-01 (determinismo) | `analisis-valoracion-jurado/correccion-03-documentar-api-eliminar-determinismo/propuestas_edicion.md` (§3.1-§3.8) |
| P-04, P-06 (conclusiones y alcance) | `analisis-valoracion-jurado/correccion-05-actualizacion-conclusiones-y-analisis-costos/PROPUESTA_TEXTO_MANUSCRITO.md` (§2, §3, §4) y `ANALISIS_COSTOS.md` |
| P-08 (corpus) | `analisis-valoracion-jurado/correccion-06-precisar-corpus-revisar-respuestas/propuesta_edicion_manuscrito.md` (§1.3) |
| P-07 (forma y bibliografía) | `analisis-valoracion-jurado/correccion-07-forma-y-bibliografia/propuesta_edicion_manuscrito.md` y `auditoria_bibliografia.md` |
| Reconciliación V.1/V.6 | `analisis-valoracion-jurado/verificacion-analisis-estadistico/reconciliacion_v1/INFORME_RECONCILIACION.md` |
| Métricas de recuperación | `analisis-valoracion-jurado/verificacion-analisis-estadistico/metricas_recuperacion/INFORME_METRICAS_RECUPERACION.md` |
| Estado de cobertura previo | `analisis-valoracion-jurado/COBERTURA_valoracion_actualizada.md` (12/11/2026, anterior a la última tanda de edición del manuscrito) |

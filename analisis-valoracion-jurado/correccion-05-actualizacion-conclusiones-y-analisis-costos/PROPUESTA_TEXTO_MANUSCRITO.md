# Propuesta de texto para el manuscrito — IX.1.5

**Uso:** documento de revisión. No se editó ningún `.typ`. Las citas “Actual” corresponden al estado del repositorio al 2026-11-12; las citas “Propuesto” son textos listos para revisar y, si se aceptan, trasladar a los archivos indicados.  
**Dependencias:** las decisiones `D-01` a `D-14` están en `DECISIONES.md`. Salvo indicación contraria, el texto siguiente asume las opciones recomendadas.

**Escenario base:** respuestas no sustantivas = 0. Cuando corresponde, se reporta la exclusión como sensibilidad; nunca como efecto causal.  
**Fuente de cifras:** `correccion-01.../salidas/35_resultados_clave.json`, `correccion-01.../salidas/31_efectos_simples_orientados.csv`, `correccion-02.../salidas/14_dataset_categoria_final.csv` y `ANALISIS_COSTOS.md`.

---

## 1. Resumen (`manuscrito/capitulos/01_texto_preliminar.typ`, línea 4)

### 1.1. Texto actual

El párrafo comienza “Presentamos el diseño, implementación y evaluación…” y contiene la interacción con $H = 56.62$, el “efecto igualador”, la mediana 0.92 frente a 0.33, la celda 0.08 vs. 0.58 y la afirmación de que en gpt-5 no hay diferencias.

### 1.2. Reemplazo propuesto

```typst
Presentamos el diseño, implementación y evaluación de un prototipo Agentic-RAG de código abierto para la consulta del Código de Minería Argentino. El acceso a la normativa legal argentina está limitado por sistemas de búsqueda basados en coincidencias léxicas que no capturan la semántica del lenguaje jurídico, mientras que las herramientas avanzadas existentes son predominantemente comerciales y de acceso restringido. El prototipo integra una base de datos vectorial con embeddings semánticos, una arquitectura de dos agentes activos —Especialista Legal y Recuperación— y un pipeline de evaluación con métricas textuales, semánticas y tres jueces LLM. La evaluación emplea un diseño factorial 3 × 3 sobre 25 casos y 79 unidades, revisadas por una profesional del derecho. El análisis respeta el apareamiento por unidad y el anidamiento en casos mediante un modelo ordinal mixto. Se observó una interacción entre estrategia y modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). En el escenario principal, que asigna cero a las respuestas no sustantivas, Agentic-RAG fue inferior a RAG básico en gpt-5-nano (−0,270; IC 95% −0,330 a −0,202), superior en gpt-5-mini (+0,150; IC 95% 0,096 a 0,203) y superior en gpt-5 (+0,106; IC 95% 0,054 a 0,155). RAG básico no eliminó las diferencias entre modelos. En Agentic-RAG con gpt-5-nano, 41 de 79 salidas no fueron sustantivas; cuando respondió, la calidad fue alta (n = 38; media 0,820). Los resultados corresponden a un corpus, 25 casos, una ejecución por celda y un recuperador fijo, por lo que constituyen evidencia de viabilidad y no una validación externa.
```

### 1.3. Notas

- Cambiar “tres jueces independientes” por “tres jueces” si se quiere evitar la ambigüedad de independencia; el texto propuesto no lo afirma.
- El resumen no menciona costos para no convertirlo en un artículo de eficiencia; el resultado de costos se desarrolla en el capítulo de evaluación.
- Si se acepta D-09 A, el título del resumen y de la portada debe cambiar; ver §2.2.

---

## 2. Introducción (`manuscrito/capitulos/02_capitulo_01_introduccion.typ`)

### 2.1. Objetivo general (línea 105)

**Actual**

```typst
Desarrollar un sistema Agentic-RAG de código abierto como prueba de concepto, utilizando el Código de Minería Argentino, para responder consultas de usuarios profesionales y no profesionales en el derecho.
```

**Propuesto**

```typst
Desarrollar y evaluar un prototipo Agentic-RAG de código abierto, utilizando el Código de Minería Argentino como prueba de concepto, para responder consultas en lenguaje natural sobre esa normativa. La evaluación se realiza con un benchmark específico; no se evalúa una interfaz ni la experiencia de usuarios finales.
```

**Motivo:** el objetivo actual promete usuarios profesionales y no profesionales, pero no hubo interfaz ni pruebas de usuarios. Si se prefiere conservar la ambición, agregar “potencialmente” y una frase de alcance; no presentarlo como resultado.

### 2.2. Título (D-09)

**Actual**

```typst
Desarrollo y evaluación de un prototipo de sistema inteligente para consulta de normativa nacional argentina mediante recuperación agéntica
```

**Propuesto (opción A, recomendada si la institución lo permite)**

```typst
Desarrollo y evaluación de un prototipo Agentic-RAG para consulta del Código de Minería argentino
```

Actualizar en `main.typ` (documento y portada), README y bloque BibTeX. Si no se autoriza el cambio, mantener el título y agregar en el resumen y en la introducción: “El alcance empírico se limita al Código de Minería Argentino; no se evaluó una interfaz ni una muestra de usuarios”.

### 2.3. Contribuciones principales (líneas 133–143)

**Actual (ideas):** sistema completo, base vectorial, benchmark “validado”, metodología replicable, contribución a la transparencia.

**Reemplazo propuesto**

```typst
Las principales contribuciones del presente trabajo final son:

+ *Sistema Agentic-RAG de código abierto, con alcance acotado.* Desarrollo de un prototipo que integra recuperación semántica, base de datos vectorial y dos agentes activos: el Agente Especialista Legal y el Agente de Recuperación. El especialista realiza una delegación nominal de recuperación y no itera sobre los resultados; el Agente de Calidad fue diseñado pero no se ejecutó. No se implementó un ciclo completo de verificación multi-agente.

+ *Base de datos vectorial del Código de Minería.* Creación de una base especializada con embeddings semánticos de 398 nodos de tipo artículo (397 con texto; el artículo 239 está derogado y vacío), con similitud coseno. [Si no se verifica el índice en Milvus, no afirmar “IVF_FLAT”.]

+ *Benchmark para el Código de Minería Argentino.* Desarrollo de un benchmark de 25 casos y 79 unidades, generado con asistencia de LLM y revisado por una profesional del derecho. La versión experimental se conserva congelada; las correcciones detectadas en la auditoría se documentan como una versión v2 para evaluaciones futuras.

+ *Evidencia empírica sobre la interacción estrategia × modelo.* El análisis apareado muestra que el efecto de la estrategia depende del modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²), con patrones distintos en gpt-5-nano, gpt-5-mini y gpt-5. La interacción no identifica por sí sola qué componente de la estrategia la produce.

+ *Caracterización de un modo de fallo de respuesta.* En Agentic-RAG con gpt-5-nano, 41 de 79 salidas no fueron sustantivas; cuando el sistema respondió, la calidad fue alta (38/79; media 0,820; mediana 0,958). El patrón se describe sin atribuirlo causalmente a la “complejidad agéntica”.

+ *Metodología de evaluación y artefactos abiertos.* Modelo ordinal mixto con interceptos por caso y unidad, escenarios de fallo, efectos simples con IC, análisis de costos por respuesta aceptable y publicación de código, benchmark, logs y evaluaciones para auditoría.
```

**No conservar** “primer sistema” sin la salvedad “no se identificaron antecedentes públicos comparables en la búsqueda realizada” (D-13).

---

## 3. Capítulo de evaluación (`manuscrito/capitulos/07_capitulo_06_evaluacion.typ`)

### 3.1. Fortalezas del sistema (líneas 412–415)

**Actual (ideas):** ambos sistemas con recuperación superan al baseline; Agentic-RAG + mini comparable a gpt-5; RAG básico iguala; acuerdo inter-juez “valida” la confiabilidad.

**Reemplazo propuesto**

```typst
+ *Mejora condicionada al modelo y a la estrategia.* En gpt-5-mini, RAG básico y Agentic-RAG superaron a Sin RAG (+0,363; IC 95% 0,304–0,417 y +0,513; IC 95% 0,454–0,562). En gpt-5, Agentic-RAG superó a RAG básico y a Sin RAG (+0,106; IC 95% 0,054–0,155 y +0,095; IC 95% 0,046–0,146). En gpt-5-nano, en cambio, Agentic-RAG fue inferior a ambas referencias. No hay una mejora uniforme de “la recuperación”.

+ *Alternativas no dominadas en costo-calidad.* Agentic-RAG + gpt-5-mini alcanza una media de 0,788 y cuesta USD 0,0564 por consulta; Agentic-RAG + gpt-5 alcanza 0,812 y cuesta USD 0,0792. La diferencia de calidad entre ambas no es concluyente, de modo que la primera es una alternativa no dominada cuando se busca calidad alta con menor costo que gpt-5. No es la opción más barata del estudio.

+ *Evaluación multidimensional con límites explícitos.* La combinación de métricas textuales, semánticas y jueces LLM permite examinar dimensiones distintas de la respuesta. El acuerdo entre jueces se reporta como confiabilidad; no se confunde con validez frente a criterio humano.

+ *Trazabilidad de las interacciones.* Los logs de los agentes registran llamadas, documentos recuperados, selección y uso de tokens, lo que permite auditar el comportamiento y reproducir el análisis. Los registros no contienen el payload HTTP completo ni el esfuerzo de razonamiento efectivo.

+ *Análisis inferencial adecuado al diseño.* El modelo ordinal mixto con interceptos por caso y unidad, las pruebas pareadas de Friedman/Wilcoxon como sensibilidad, el bootstrap por casos y la corrección de Holm dentro de familias predefinidas respetan el apareamiento y el anidamiento del diseño.
```

### 3.2. Debilidades y limitaciones (líneas 419–422)

**Actual (ideas):** Agentic-RAG degrada nano por “complejidad agéntica”; precisión legal poco confiable; no hay diferencia marginal Agentic vs. RAG; benchmark limitado.

**Reemplazo propuesto**

```typst
+ *Modo de fallo de respuesta en Agentic-RAG + gpt-5-nano.* La celda produjo 41/79 salidas no sustantivas: 27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas. La media con fallo = 0 fue 0,395 y la mediana 0,000; cuando respondió (38/79), la media fue 0,820 y la mediana 0,958. Los logs muestran recuperación y tokens de salida, sin evidencia de truncamiento por longitud. El patrón no se atribuye a una causa única.

+ *La precisión legal no alcanzó confiabilidad suficiente en todos los sistemas.* La rúbrica `score_precision_legal` tuvo un α global de 0,785, pero cayó por debajo de 0,667 en RAG básico y Sin RAG. No se usó como variable principal de comparación.

+ *No se demostró equivalencia entre modelos con RAG básico.* Las diferencias fueron menores que en otras estrategias, pero las estimaciones fueron positivas: mini−nano +0,063 (IC 0,005–0,120), gpt-5−nano +0,128 (IC 0,071–0,186), gpt-5−mini +0,065 (IC 0,011–0,124). Los dos últimos contrastes fueron limítrofes tras Holm. La ausencia de significación no demuestra equivalencia.

+ *Factores confundidos entre estrategias.* El recuperador agéntico fue siempre gpt-5; los prompts, la descomposición, el número de candidatos, la selección y el presupuesto de búsquedas difirieron. Además, gpt-5 usó un límite de 7 búsquedas y mini/nano de 6. Sin ablaciones, el efecto no puede atribuirse a un componente aislado.

+ *Una ejecución por celda y ausencia de control efectivo de muestreo.* El código solicitó `temperature=0.0`, pero Pydantic AI 1.1.0 elimina ese parámetro para los modelos GPT-5; no se registró el esfuerzo de razonamiento. No puede afirmarse determinismo ni estimarse la variabilidad entre corridas.

+ *Benchmark v1 con observaciones abiertas.* La revisión fue realizada por una profesional y produjo cambios registrados; no hubo una segunda revisión independiente. La auditoría identificó referencias y paráfrasis que requieren corrección en una versión v2. Las conclusiones corresponden al instrumento v1 efectivamente usado.
```

### 3.3. Párrafo especulativo sobre gpt-5 (línea 424)

**Actual (ideas):** atribuye la ausencia de diferencias a conocimiento paramétrico, techo de rúbrica, potencia o capacidad de los jueces.

**Reemplazo propuesto**

```typst
El patrón de gpt-5 no debe interpretarse como ausencia de efecto: Agentic-RAG superó a RAG básico y a Sin RAG, aunque con diferencias menores que en gpt-5-mini. No se atribuye ese patrón al conocimiento paramétrico del modelo, a un techo de la rúbrica ni a su “capacidad de razonamiento”: son hipótesis no contrastadas. La comparación está además confundida por el límite de siete búsquedas en gpt-5 frente a seis en mini/nano y por el recuperador fijo. La validación con expertos humanos y las réplicas quedan pendientes.
```

### 3.4. Implicaciones prácticas (líneas 428–431)

**Reemplazo propuesto**

```typst
+ *No hay una combinación óptima única.* La frontera de Pareto contiene siete de las nueve configuraciones; la elección depende de si se prioriza calidad media, costo por consulta o costo por respuesta aceptable.

+ *Si se prioriza el menor costo puntual por respuesta aceptable (≥ 0,75):* RAG básico + gpt-5-nano (USD 0,0061 por aceptable; IC bootstrap 0,0043–0,0091; 33/79 aceptables; media 0,599). Su IC se solapa con Sin RAG + gpt-5-nano (0,0058–0,0107), de modo que el orden es descriptivo y no una diferencia formal. No es la opción de mayor calidad.

+ *Si se prioriza la calidad media:* Agentic-RAG + gpt-5 (media 0,812; USD 0,0792) seguido por Agentic-RAG + gpt-5-mini (0,788; USD 0,0564). La diferencia de calidad entre ambos no es concluyente; la segunda es una alternativa no dominada de menor costo.

+ *Agentic-RAG + gpt-5-nano no se recomienda como sistema completo.* Solo 27/79 respuestas alcanzan el umbral de aceptabilidad y su costo por aceptable es USD 0,1307, el peor de las nueve celdas. La calidad condicional cuando responde es alta, pero la tasa de no respuesta domina el resultado del sistema.

+ *El índice anterior no se usa.* El piso 0,01 del costo normalizado determinaba por sí solo el valor de la configuración más barata. Se reemplaza por costo absoluto, costo por aceptable y frontera de Pareto.
```

### 3.5. Conclusión del capítulo (línea 435)

**Reemplazo propuesto**

```typst
El análisis apareado confirma una interacción fuerte entre estrategia y modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). Bajo el escenario principal, Agentic-RAG presenta una diferencia negativa en gpt-5-nano frente a RAG básico (−0,270; IC 95% −0,330 a −0,202), una diferencia positiva en gpt-5-mini (+0,150; IC 95% 0,096 a 0,203) y también en gpt-5 (+0,106; IC 95% 0,054 a 0,155). RAG básico no se distingue de Sin RAG en gpt-5 ni en nano; en mini, RAG básico supera a Sin RAG. La afirmación de que “el RAG básico iguala a los modelos” no se sostiene: las diferencias observadas son menores, pero no desaparecen y no se demostró equivalencia. La afirmación de que “en gpt-5 no hay diferencias” también debe corregirse: Agentic-RAG presenta una diferencia positiva y significativa frente a RAG básico, aunque menor que en mini. En Agentic-RAG + gpt-5-nano, 41/79 salidas no son sustantivas; cuando responde, la calidad es alta. El patrón es un problema de fiabilidad del sistema completo, no una degradación uniforme de la calidad jurídica. Los costos no identifican un ganador único: RAG básico + nano presenta el menor costo puntual por aceptable (IC solapado con Sin RAG + nano) y Agentic-RAG + gpt-5 maximiza la media, con Agentic-RAG + mini como alternativa no dominada. El acuerdo entre jueces es confiabilidad, no validación humana.
```

---

## 4. Capítulo de conclusiones (`manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ`)

### 4.1. Cumplimiento de objetivos (líneas 15–21)

**Reemplazo propuesto**

```typst
+ *Desarrollar una base de datos vectorial del Código de Minería Argentino diseñada específicamente para trabajar con sistemas RAG.* Este objetivo se cumplió en lo funcional. Se implementó una base vectorial en Milvus con embeddings de 768 dimensiones generados por `hiiamsid/sentence_similarity_spanish_es`, con segmentación por artículo y similitud coseno. El corpus contiene 398 nodos de tipo artículo: 347 del cuerpo principal, 15 disposiciones generales y transitorias y 36 del apéndice; 397 tienen texto y el artículo 239 está derogado y vacío. [Si D-12 A: no se afirma “IVF_FLAT”; si D-12 B: reemplazar por el tipo verificado en Milvus.]

+ *Desarrollar un sistema de agentes de inteligencia artificial para que trabajen de manera conjunta con el sistema RAG.* Este objetivo se cumplió parcialmente. Se implementó una arquitectura de dos agentes activos mediante Pydantic AI: el Agente Especialista Legal (generación) y el Agente de Recuperación (descomposición y búsqueda). El especialista realiza una delegación nominal de recuperación; no itera sobre los resultados ni verifica la respuesta con un agente adicional. El Agente de Calidad fue diseñado, pero se excluyó por costo y complejidad y no participó en ninguna de las respuestas evaluadas. En 236 de 237 sesiones el especialista hizo una llamada a `retrieve_relevant_documents`; la sesión `16_01` de gpt-5 registró tres. El objetivo se cumple respecto de la coordinación recuperación–generación, pero no de un ciclo completo de verificación multi-agente.

+ *Desarrollar un benchmark específico para el Código de Minería Argentino para evaluar el desempeño del sistema.* Este objetivo se cumplió con alcance limitado. Se generó un benchmark de 25 casos y 79 unidades, con respuestas esperadas generadas por GPT-4.1 y revisadas por una profesional del derecho. La revisión quedó registrada en un ODT con cambios y comentarios; no hay evidencia de una segunda revisión independiente. La auditoría identificó referencias y paráfrasis que requieren corrección en una versión v2. Las conclusiones de este trabajo corresponden al benchmark v1 efectivamente usado.

+ *Cargar el código y una descripción de la metodología a un repositorio abierto para que cualquier organización, empresa o individuo pueda replicar y adaptar el sistema a otras normativas.* El acceso público está verificado: el repositorio contiene código, benchmark, corpus, logs y evaluaciones. La reproducción funcional desde una clonación anónima del commit final queda como verificación pendiente. El sistema no incluye una interfaz de usuario ni fue evaluado con usuarios finales.
```

### 4.2. Contribuciones del trabajo (líneas 27–39)

**Reemplazo propuesto**

```typst
+ *Sistema Agentic-RAG de código abierto, con alcance acotado.* Se desarrolló un prototipo que integra recuperación semántica, base vectorial y dos agentes activos. No es un planificador autónomo ni un ciclo iterativo de verificación: el especialista delega una recuperación y redacta con los documentos devueltos. El Agente de Calidad no se ejecutó. Hasta donde se tiene conocimiento, no se identificaron antecedentes públicos comparables para normativa argentina en la búsqueda realizada.

+ *Benchmark para el Código de Minería Argentino.* Se creó un benchmark de 25 casos y 79 unidades, con revisión profesional registrada. La versión experimental se conserva congelada; las correcciones detectadas se documentan como v2 para futuras evaluaciones. El benchmark es un instrumento de investigación, no una validación psicométrica ni jurídica definitiva.

+ *Evidencia empírica sobre la interacción estrategia × modelo.* El análisis apareado muestra que el efecto de la estrategia depende del modelo del especialista (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). En el escenario principal, Agentic-RAG es inferior a RAG básico en gpt-5-nano, superior en gpt-5-mini y moderadamente superior en gpt-5. La interacción es robusta a los escenarios de sensibilidad y a los tres jueces, pero no identifica un componente causal único.

+ *Caracterización de un modo de fallo de respuesta.* En Agentic-RAG con gpt-5-nano, 41/79 salidas no fueron sustantivas; cuando respondió, la calidad fue alta (38/79; media 0,820; mediana 0,958). Los logs muestran recuperación y tokens, sin truncamiento por longitud. El hallazgo es descriptivo; no se atribuye a la “complejidad agéntica” sin réplicas ni ablaciones.

+ *Límites de la hipótesis de igualación por RAG básico.* Con RAG básico, las diferencias observadas entre modelos son menores, pero no desaparecen: las estimaciones son positivas y los intervalos no definen equivalencia. La conclusión anterior basada en un p de Kruskal–Wallis no significativo debe retirarse.

+ *Confiabilidad inter-juez, no validación.* Los tres jueces alcanzaron un acuerdo ordinal global bueno para corrección (α = 0,808 con valores originales; 0,800 con transformación a rúbrica), pero no se compararon con criterio humano. La auditoría detectó evaluaciones positivas sobre salidas no sustantivas. La rúbrica de precisión legal no alcanzó confiabilidad suficiente en todos los sistemas.

+ *Metodología de evaluación y artefactos abiertos.* El modelo ordinal mixto con interceptos por caso y unidad, los escenarios de fallo, los efectos simples con IC, el análisis de costos por respuesta aceptable y la publicación de código, logs y evaluaciones permiten auditar y replicar el análisis. La replicación funcional desde una clonación limpia queda pendiente.
```

### 4.3. Impacto de la propuesta (línea 45)

**Reemplazo propuesto**

```typst
El trabajo muestra la viabilidad técnica de un prototipo Agentic-RAG de código abierto para consultar el Código de Minería Argentino, pero no demuestra una superioridad general de la recuperación agéntica. En gpt-5-mini, RAG básico y Agentic-RAG presentaron diferencias positivas frente a Sin RAG; en gpt-5, Agentic-RAG presentó una diferencia positiva frente a ambas referencias; en gpt-5-nano, Agentic-RAG presentó una diferencia negativa en la utilidad del sistema porque 41/79 salidas no fueron sustantivas. No hay una recomendación universal: la elección de estrategia y modelo debe hacerse conjuntamente y con un objetivo explícito de calidad y costo. La disponibilidad del código y la metodología habilita su adaptación, pero no demuestra adopción, impacto social ni transferencia a otros dominios.
```

### 4.4. Fortalezas del sistema (líneas 55–63)

**Reemplazo propuesto**

```typst
+ *Diseño factorial y benchmark propio.* El estudio compara tres estrategias y tres modelos sobre las mismas 79 unidades, con un benchmark específico para el Código de Minería. El diseño permite examinar la interacción y no solo efectos marginales.

+ *Mejora condicionada al modelo.* En gpt-5-mini, ambas estrategias de recuperación presentaron diferencias positivas frente a Sin RAG; en gpt-5, Agentic-RAG presentó una diferencia positiva frente a RAG básico y Sin RAG; en gpt-5-nano, Agentic-RAG presentó un modo de fallo de respuesta.

+ *Alternativa no dominada de costo-calidad.* Agentic-RAG + gpt-5-mini ofrece una media de 0,788 a USD 0,0564 por consulta, con una diferencia de calidad no concluyente frente a Agentic-RAG + gpt-5 (0,812; USD 0,0792). No es la opción más barata, pero es una alternativa razonable cuando se prioriza calidad alta con menor costo que gpt-5.

+ *Trazabilidad y auditabilidad.* Los logs de los agentes, las respuestas, las métricas y las evaluaciones de los jueces están disponibles para auditoría. Los registros no incluyen el payload HTTP completo ni el esfuerzo de razonamiento efectivo.

+ *Análisis inferencial adecuado al diseño.* El modelo ordinal mixto, las pruebas pareadas y el bootstrap por casos respetan el apareamiento y el anidamiento. Los efectos se reportan con IC y las comparaciones múltiples se corrigen dentro de familias predefinidas.
```

### 4.5. Debilidades y limitaciones (líneas 69–87)

**Conservar** las limitaciones de alcance del corpus (69), precisión legal (75), escala del benchmark (77), dependencia de APIs (79) y ausencia de evaluación con usuarios (81), con los ajustes indicados en §3.2.

**Reemplazar la limitación de “ausencia de diferencia marginal” (71)** por:

```typst
+ *No se demostró una superioridad global de Agentic-RAG.* El efecto depende del modelo: es negativo en gpt-5-nano, positivo en gpt-5-mini y moderado en gpt-5. No corresponde reportar un efecto marginal único ni usar la falta de significación como prueba de equivalencia.
```

**Reemplazar “Degradación con modelos pequeños” (73)** por:

```typst
+ *Modo de fallo de respuesta en Agentic-RAG + gpt-5-nano.* La celda produjo 41/79 salidas no sustantivas, con una media de 0,395 y mediana 0,000 en el escenario fallo = 0. Cuando respondió (38/79), la media fue 0,820 y la mediana 0,958. Los logs no muestran falta de recuperación ni truncamiento por tokens. No se atribuye el fallo a la “complejidad agéntica” sin réplicas ni ablaciones.
```

**Reemplazar “Alcance temporal de los modelos” (83)** por:

```typst
+ *Alcance temporal y de configuración.* Los modelos GPT-5 evaluados corresponden al período experimental (segundo semestre de 2025). El recuperador fue siempre gpt-5; gpt-5 usó siete búsquedas y mini/nano seis. El modo de fallo de gpt-5-nano podría cambiar con otros modelos o configuraciones, pero no se atribuye a una propiedad estable de “los modelos pequeños”.
```

**Reemplazar “Ausencia de validación manual” (85)** por:

```typst
+ *Ausencia de validación humana de los jueces.* No se comparó una submuestra con calificaciones de profesionales. El acuerdo inter-juez mide confiabilidad, no validez. Además, la auditoría detectó 12 evaluaciones de corrección con puntaje > 0 sobre salidas no sustantivas (9 unidades distintas) y 5 evaluaciones de precisión legal > 0; varias justificaciones describen contenido que no aparece en la respuesta. Estos puntajes no deben promediarse como calidad.
```

**Agregar después de la limitación anterior:**

```typst
+ *Ejecución única y ausencia de control efectivo de muestreo.* Se realizó una única ejecución por unidad y configuración, sin réplicas. El código solicitó `temperature=0.0`, pero Pydantic AI 1.1.0 elimina ese parámetro para los modelos GPT-5 antes de construir la solicitud; no se registró el esfuerzo de razonamiento. No puede afirmarse determinismo ni estimarse la variabilidad entre corridas.

+ *Factores confundidos y ausencia de ablaciones.* En Agentic-RAG cambian simultáneamente el prompt, la descomposición, el número de candidatos, la selección, el modelo recuperador y el presupuesto de búsquedas. Sin ablaciones no puede atribuirse el efecto a uno de esos componentes. La diferencia 7/6 entre gpt-5 y mini/nano agrega una amenaza específica al contraste por modelo.

+ *Benchmark v1 con observaciones abiertas.* La revisión fue realizada por una profesional y no hay evidencia de una segunda revisión independiente. La auditoría identificó referencias y paráfrasis que requieren corrección en una versión v2. Las conclusiones corresponden al instrumento v1; no se aplicaron correcciones retroactivas.

+ *Costos históricos y ausencia de costos de producción.* Los costos son los registrados en el experimento (precios de API del período) y no incluyen infraestructura, latencia, mantenimiento, interfaz ni costos humanos. No se extrapolan a precios actuales.
```

### 4.6. Trabajos futuros

**Reemplazar la viñeta de políticas adaptativas (101)** por:

```typst
- *Políticas adaptativas de complejidad.* Un agente clasificador podría decidir dinámicamente si emplear RAG básico o Agentic-RAG según la consulta y el modelo, con el objetivo de reducir la tasa de respuestas no sustantivas y evitar configuraciones con mal costo por respuesta aceptable. La política debería evaluarse con réplicas y una métrica de fallo, no solo con la media de corrección.
```

**Agregar en Mejoras en la Arquitectura:**

```typst
- *Réplicas y ablaciones.* Repetir las celdas críticas entre tres y cinco veces y ejecutar una ablación con el mismo modelo en el especialista y el recuperador. Sin réplicas no puede separarse el efecto de la estrategia de la variabilidad entre corridas; sin ablación no puede atribuirse el efecto a la descomposición, la selección o el prompt.
```

**Agregar en Ampliación del Benchmark:**

```typst
- *Versión v2 del benchmark.* Incorporar las correcciones de referencias y paráfrasis detectadas en la auditoría, documentar las decisiones jurídicas y volver a evaluar una submuestra con profesionales. La v2 no debe presentarse como el instrumento usado en esta tesis.
- *Validación humana de los jueces.* Seleccionar una submuestra ciega, obtener calificaciones de uno o dos profesionales y medir acuerdo humano–juez. Sin esa comparación, el acuerdo inter-juez no es validación.
```

**Reemplazar la sección de re-evaluación (132)** por:

```typst
La velocidad de iteración en el desarrollo de LLMs hace deseable repetir el diseño experimental sobre modelos lanzados después del período de estudio, especialmente modelos que integran cadenas de pensamiento explícitas. La comparación debería verificar si el modo de fallo observado en Agentic-RAG con gpt-5-nano se reproduce, si la interacción cambia y si la diferencia 7/6 se elimina con un presupuesto homogéneo. La metodología de evaluación propuesta —diseño factorial, benchmark específico, modelo ordinal mixto y análisis de costos por respuesta aceptable— es aplicable a futuras generaciones, pero la validación con jueces humanos sigue siendo necesaria.
```

### 4.7. Reflexiones finales (líneas 136–140)

**Reemplazo propuesto para los dos primeros párrafos**

```typst
El presente trabajo muestra que un prototipo Agentic-RAG de código abierto es técnicamente viable para consultar el Código de Minería Argentino, pero no demuestra que la recuperación agéntica sea uniformemente superior. En gpt-5-mini, ambas estrategias de recuperación presentaron diferencias positivas frente a Sin RAG; en gpt-5, Agentic-RAG presentó una diferencia positiva moderada; en gpt-5-nano, se observó un modo de fallo de respuesta en 41/79 unidades. La calidad condicional cuando el sistema responde es alta, pero la tasa de no respuesta domina la utilidad del sistema completo.

El hallazgo de interacción entre estrategia y modelo del especialista exige una selección conjunta y un objetivo explícito de calidad y costo. No autoriza una recomendación universal, una explicación causal única ni una afirmación de transferencia a otros dominios. Los resultados corresponden a un corpus, 25 casos, una ejecución por celda, un recuperador fijo y un benchmark v1 con observaciones abiertas.
```

**Reemplazo propuesto para el párrafo final (140)**

```typst
La publicación del código, la metodología y el benchmark como recursos abiertos busca facilitar que otros investigadores e instituciones auditen, adapten y mejoren el sistema. La disponibilidad de una alternativa abierta es un paso hacia la democratización del acceso a la información legal, pero no demuestra por sí sola adopción, impacto social ni utilidad para usuarios finales.
```

---

## 5. Anexo de ejemplo (`manuscrito/capitulos/anexo_01.typ`, línea 232)

**Actual**

```typst
La ventaja del enfoque agéntico se evidencia en la capacidad de descomponer consultas complejas en búsquedas más específicas, lo que mejora la precisión de la recuperación y, consecuentemente, la calidad de la respuesta generada.
```

**Propuesto**

```typst
Este caso ilustra cómo el enfoque agéntico puede descomponer una consulta compleja en búsquedas más específicas. Corresponde a una de las 38 respuestas sustantivas de Agentic-RAG con gpt-5-nano y no representa las 41 salidas no sustantivas de esa celda. La ventaja cualitativa del ejemplo no debe generalizarse al conjunto de las 79 unidades ni interpretarse como evidencia de superioridad uniforme.
```

---

## 6. Tabla de reemplazos rápidos

| Archivo:línea | Texto actual o idea | Reemplazo | Decisión |
| --- | --- | --- | --- |
| `01_texto_preliminar.typ:4` | Resumen con H = 56.62, igualador, 0.92/0.33, 0.08/0.58, “sin diferencias en gpt-5” | §1.2 | D-01, D-05, D-09 |
| `02_capitulo_01_introduccion.typ:105` | Usuarios profesionales y no profesionales | §2.1 | D-09 |
| `02_capitulo_01_introduccion.typ:133–143` | Contribuciones con “validado”, “completo”, “primer” | §2.3 | D-05, D-07, D-13 |
| `07_capitulo_06_evaluacion.typ:412–415` | RAG iguala; LLM-as-a-Judge validado | §3.1 | D-04, D-08 |
| `07_capitulo_06_evaluacion.typ:419–422` | Degradación por complejidad; no diferencia marginal | §3.2 | D-05, D-06 |
| `07_capitulo_06_evaluacion.typ:424` | Conocimiento paramétrico/techo/potencia | §3.3 | D-01, D-06 |
| `07_capitulo_06_evaluacion.typ:428–431` | Agentic mini costo-eficiente; Agentic gpt-5 óptimo | §3.4 | D-02, D-04 |
| `07_capitulo_06_evaluacion.typ:435` | Kruskal/Mann-Whitney; igualador; gpt-5 sin diferencias | §3.5 | D-01, D-05 |
| `09...:15–21` | Objetivos 1–2 “completamente”; 3–4 con alcance | §4.1 | D-07, D-10, D-11, D-12 |
| `09...:27–39` | Contribuciones con sobrecarga, validación, igualador | §4.2 | D-04, D-05, D-08 |
| `09...:45` | Medianas globales 0.58–0.83; igualador | §4.3 | D-01, D-03 |
| `09...:55–63` | Fortalezas con sobrecarga y pruebas no pareadas | §4.4 | D-05, D-06 |
| `09...:71` | “Ausencia de diferencia marginal” | §4.5 | D-01 |
| `09...:73` | “Degradación con modelos pequeños” | §4.5 | D-05 |
| `09...:83` | “Sobrecarga agéntica” | §4.5 | D-05, D-06 |
| `09...:85` | Validación manual ausente | §4.5 | D-08 |
| `09...:101` | “Evitando la sobrecarga agéntica” | §4.6 | D-05 |
| `09...:132` | “Degradación observada”; “validación LLM-as-a-Judge” | §4.6 | D-05, D-08 |
| `09...:136–140` | Resultado transferible; impacto | §4.7 | D-08, D-09 |
| `anexo_01.typ:232` | “La ventaja del enfoque agéntico se evidencia…” | §5 | D-05 |

---

## 7. Qué no editar todavía

1. No reemplazar cifras del cuerpo hasta que se acepte D-01; el escenario cambia el signo de la comparación nano.
2. No eliminar `score_precision_legal` del capítulo de evaluación solo por este paquete; su tratamiento corresponde a la corrección específica de medición.
3. No afirmar que los jueces son inválidos en general: la auditoría muestra inconsistencias en salidas no sustantivas, no una invalidación global.
4. No afirmar que el fallo de nano se debe al modelo, al prompt, al recuperador o a la “agencia” sin réplicas/ablación.
5. No publicar una recomendación de costo sin declarar el umbral de aceptabilidad y la base histórica de precios.
6. No cambiar el título sin actualizar portada, `main.typ`, README y BibTeX; si no se cambia, agregar la declaración de alcance.

## 8. Orden de edición recomendado

1. Aceptar o rechazar las decisiones de `DECISIONES.md`.
2. Editar primero metodología y evaluación (modelo, efectos, fallo nano, costos).
3. Editar resumen y conclusiones.
4. Editar introducción, anexo y README.
5. Compilar con `make pdf`.
6. Buscar las frases de `FRASES_A_ELIMINAR.csv` en el PDF final.
7. Verificar que las cifras del PDF coincidan con `datos/tabla4_reformulada.csv` y `datos/costos_por_celda.csv`.

# Reporte de verificación del manuscrito contra la valoración del tribunal

**Documento de referencia:** `analisis-valoracion-jurado/Valoracion_TF_Spairani_gp_actualizada.md` (informe ampliado del miembro del tribunal, Mg. Lic. Prof. Gastón Pezzuchi, MSc., noviembre de 2026).
**Objetos verificados:** los 11 archivos `.typ` de `manuscrito/` (más `main.typ` y `manuscrito/referencias.bib`) tal como están en el árbol de trabajo al día de la verificación.
**Fecha de verificación:** 2026-11-12.
**Modelo verificador:** `ollama-cloud-glm-5-3-flash` (Ollama Cloud, GLM 5.3-flash).
**Método:** lectura completa de los archivos `.typ`; búsquedas dirigidas (`grep`) sobre los puntos señalados por el tribunal (Tabla 2, Tabla 3, Tabla 4, IX.1 y IX.2); contraste de la bibliografía contra `referencias.bib`; verificación del render de citas en el PDF compilado (`pdftotext`); compilación del manuscrito con `make pdf` (exitosa, 167 páginas). **No se ejecutaron ni re-verificaron los análisis estadísticos**: este reporte evalúa solo la conformidad del *texto* del manuscrito con lo requerido.

**Estados:** ✅ CUMPLE · ⚠️ CUMPLE PARCIAL · ❌ PENDIENTE.

---

## 1. Conclusión ejecutiva

El manuscrito incorpora **la mayor parte** de las correcciones del tribunal: título y portada, resumen, declaración de IA, diagnóstico de la celda anómala, factores confundidos y prompts, corpus y benchmark, bibliografía (Tabla 3 completa y casi toda la Tabla 2), métricas de recuperación y conclusiones reformuladas. **Compila sin errores.**

Sin embargo, **no todas las correcciones requeridas por el tribunal están reflejadas en el texto**, y en particular subsisten elementos que la propia valoración declara **indispensables para la versión definitiva** (sección X: "las correcciones 1 a 3 … su incorporación a la versión definitiva es indispensable"):

| # | Corrección requerida (IX.1) | Estado | Pendiente esencial |
|---|---|:---:|---|
| IX.1.1 | Rehacer análisis inferencial, tamaños de efecto e IC, corregir "modelos mixtos" | ⚠️ | Modelo ordinal presente (LR = 293,28 + IC), pero Friedman/Wilcoxon no se describen ni reportan; la tabla de efectos simples sigue siendo Mann-Whitney U; el anexo aún menciona "modelos mixtos"; contradicción "análisis principal" vs. "robustez" |
| IX.1.2 | Informar 41 salidas, reincorporar casos 23–25, corregir faltantes, reformular "sobrecarga" | ⚠️ | 41/79 y modo de fallo informados ✅, pero los 27 faltantes siguen atribuidos a "fallos puntuales en la generación" y los análisis siguen sobre 684 observaciones (casos 23–25 no reincorporados); restan formulaciones causales ("la complejidad agéntica es excesiva") |
| IX.1.3 | Retirar determinismo, informar esfuerzo, declarar ejecución única | ⚠️ | `reasoning_effort` correctamente documentado ✅, pero **subsisten 4 afirmaciones de determinismo** ("temperatura 0 … determinísticas", "garantizar reproducibilidad", "evita múltiples ejecuciones") y 2 referencias rotas a una "sección de parámetros de API" inexistente |
| IX.1.4 | Declarar factores confundidos, reproducir prompts, resolver contradicciones | ✅ | Cobertura completa; salvedad menor: los prompts de sin-RAG y RAG básico se describen ("prompt simplificado") pero no se reproducen literalmente |
| IX.1.5 | Reformular conclusiones (Tabla 4) | ⚠️ | Resumen, evaluación y conclusiones reformuladas ✅, pero el capítulo 8 conserva residuos: "Mejora significativa con recuperación", "Configuración costo-eficiente viable" y la lista estadística antigua en fortalezas |
| IX.1.6 | Precisar corpus, origen y respuestas de referencia | ✅ | Corpus, linaje Infoleg, conteos, fecha 1886 y respuestas 1.2/1.3 corregidos; salvedad: tasa de error de extracción sin cuantificar |
| IX.1.7 | Corregir Tabla 2 y Tabla 3, auditoría de referencias | ⚠️ | Tabla 3 íntegra y casi toda la Tabla 2 corregidas; **quedan sin corregir**: n-gramas "caracteres" vs. ejemplo de palabras, atención como "similitud coseno escalada", GPT-4 "arquitectura MoE", y la dedicatoria "A mi familia …" |
| IX.1.8 | Ampliar declaración de IA | ⚠️/✅ | Declaración por etapas, verificación y referencia eliminada ✅; pendiente: el anexo de estructura del repositorio sigue mostrando un árbol obsoleto (`examples/notebooks/`, `archivo/`) incompatible con el repositorio actual |
| IX.1.9 | Informar métricas de recuperación | ✅ | Tabla con recall@10, MRR, todos/ninguno por sistema y caveat de no comparabilidad ✅; sin comparación BM25/otro embedding (IX.2.1, recomendación no obligatoria) |

Recomendaciones IX.2 (no condicionan aprobación): **ninguna está implementada en el manuscrito**, y la mayoría está declarada como limitación o trabajo futuro, lo que resulta aceptable.

---

## 2. Correcciones requeridas IX.1 — detalle

### IX.1.1 — Rehacer el análisis inferencial y corregir "modelos mixtos" (V.1, V.2) · ⚠️ PARCIAL

**Cumple:**
- El manuscrito adopta el modelo ordinal mixto como herramienta inferencial central y reporta la interacción con el estadístico de razón de verosimilitud: "LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²" (`07_capitulo_06_evaluacion.typ` líneas 135 y 222, resumen en `01_texto_preliminar.typ`, conclusiones de capítulo 6 y 8).
- Reporta diferencias del escenario principal con **IC 95%**: Agentic-RAG −0,270 [−0,330; −0,202] en gpt-5-nano; +0,150 [0,096; 0,203] en gpt-5-mini; +0,106 [0,054; 0,155] en gpt-5 (evaluación, "Conclusiones del Capítulo"; resumen; capítulo 8). Satisface el pedido de "tamaños del efecto con sus intervalos de confianza".
- La especificación del modelo está descrita (`06_capitulo_05_metodologia.typ` ~708): efectos fijos + juez + (1 | caso) + (1 | unidad), `ordinal::clmm`, `nAGQ = 1` (Laplace), sin prueba de odds proporcionales — coincide con la decisión PI-29.
- La mención "n = 79 observaciones por celda" fue eliminada (sin coincidencias en `grep`).
- SRH queda degradado a "antecedente exploratorio" (evaluación, líneas 135 y 222), en línea con V.2.

**Pendiente:**
- **Friedman y Wilcoxon no aparecen en ninguna parte del manuscrito** (0 coincidencias). El tribunal solicitó explícitamente el reanálisis con pruebas pareadas; las decisiones internas (NV-01: `correccion-01` canónica, con Friedman/Wilcoxon) no se tradujeron al texto.
- **La tabla de efectos simples sigue siendo Mann-Whitney U** (`tabla-efectos-simples`, con U y p Holm de corridas independientes), aunque el texto afirma: "Los efectos simples se estimaron con ese modelo [el ordinal] y se corrigen con Holm" (evaluación, ~135). El texto y la tabla se contradicen.
- **`anexo_01.typ` línea 86 aún describe `part_j/` con "modelos mixtos y análisis de costos"** — la mención exacta que el tribunal pidió corregir junto con IX.1.1, dado que esa denominación no corresponde a un modelo mixto estimado.
- **Contradicción de encuadre entre capítulos**: la metodología y la limitación "Aproximación de Laplace" (cap. 8, ~71) llaman al modelo ordinal "análisis de robustez"/"sensibilidad" y afirman que "la inferencia principal se apoya en las pruebas pareadas"; la evaluación afirma que "El análisis principal es el modelo ordinal mixto". Debe homogeneizarse (el diseño adoptado según el registro de decisiones es: modelo ordinal = análisis de sensibilidad y Friedman/Wilcoxon = pareado principal, o unificar el encuadre elegido).
- Los **efectos del modelo dentro de cada estrategia** (p. ej., dentro de RAG básico — donde el reanálisis del tribunal encuentra diferencias significativas) no se reportan.
- Los **escenarios de fallo** (no sustantivas = 0 como principal, exclusión y jueces observados como sensibilidad) aparecen en evaluación ("fallo = 0", "escenario principal") **sin definirse previamente en metodología**.

### IX.1.2 — Celda gpt-5-nano con Agentic-RAG y datos faltantes (V.6) · ⚠️ PARCIAL

**Cumple:**
- Se informa la clasificación de salidas: "41/79 salidas no fueron sustantivas (27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas); la media con fallo = 0 fue 0,395 y la mediana 0,000. Cuando respondió (38/79), la media fue 0,820 y la mediana 0,958" (evaluación, "Debilidades y Limitaciones").
- El hallazgo se reformula como **"modo de fallo de respuesta"** y se rechaza la atribución causal: "no se atribuye a la 'complejidad agéntica' sin réplicas ni ablaciones" (cap. 8 — la contribución "sobrecarga agéntica" ya no existe; `grep` sin coincidencias).
- Se reporta la revisión manual de las 87 filas no sustantivas como del autor, sin estatus de validación (cap. 8, ~87) y las 23 discrepancias / 17 evaluaciones positivas sobre salidas no sustantivas (cap. 8, ~37 y ~87).

**Pendiente:**
- **Los 27 faltantes siguen mal explicados**: evaluación (~73) conserva la frase exacta objectionada: "atribuibles a fallos puntuales en la generación de respuestas", y el análisis sigue sobre **684 observaciones** (página i del Tribunal). Los **casos 23–25 no fueron reincorporados** ni se explica el problema del join (`nro_subpregunta` vacío vs. 0). La reincorporación hecha en el análisis derivado no aparece en el manuscrito.
- Restan **formulaciones causales contradictorias** en evaluación: "Esto sugiere que la complejidad agéntica es excesiva para modelos de capacidad reducida" (efectos simples) y "sugiere que el sistema agéntico genera instrucciones y contextos de complejidad excesiva" (patrón de interacción) — incompatibles con la reformulación adoptada en cap. 8 y con V.6.
- El análisis de sensibilidad "fallo = 0 vs. exclusión" no se presenta como plan formal (solo cifras sueltas).

### IX.1.3 — Documentar parámetros de API y eliminar determinismo (V.4) · ⚠️ PARCIAL (núcleo pendiente)

**Cumple:**
- `reasoning_effort` correctamente explicado en dos lugares: declaración preliminar (línea 28) e hiperparámetros (metodología ~497): "Pydantic AI 1.1.0 … envía `NOT_GIVEN`; OpenAI documenta `medium` como valor por defecto… El valor efectivo no quedó registrado y no se infiere de los tokens de razonamiento" — coincide con NV-05 y V.4.
- La tabla de hiperparámetros marca la temperatura como "valor solicitado" con nota sobre su "tratamiento efectivo" (metodología ~475, ~492).
- La ejecución única se declara en resumen y reflexiones finales ("una ejecución por celda") y se recomienda no usar la celda nano "sin réplicas ni ablaciones".

**Pendiente — afirmaciones de determinismo aún vigentes (pedido central de V.4):**
- `06_capitulo_05_metodologia.typ`:511 — "+ Soporte para generación con temperatura cero (respuestas determinísticas)." (criterios de selección de modelos).
- `06_capitulo_05_metodologia.typ`:521 — "Todos los modelos fueron configurados con temperatura 0 para maximizar la reproducibilidad de las respuestas."
- `06_capitulo_05_metodologia.typ`:660 — "+ Temperatura 0 para respuestas determinísticas (evita múltiples ejecuciones)." (Optimización de Llamadas; es la frase textual objectionada en V.4).
- `07_capitulo_06_evaluacion.typ`:16 — "con temperatura 0 en todas las configuraciones para garantizar reproducibilidad."
- También: metodología ~191 "(Pydantic AI con temperatura 0) … para mantener la comparabilidad" y ~495 "Temperatura 0,0" como "valor solicitado" sin aclarar en línea que el parámetro no llega a la API.
- **Referencias rotas**: metodología ~475 ("se discute en la sección de parámetros de API") y ~492 ("se discute en la corrección sobre parámetros de API") apuntan a una sección que **no existe** en el manuscrito; "la corrección sobre parámetros de API" es además un residuo de la nomenclatura de los paquetes de corrección (`correccion-03`), ajeno al lector del PDF.
- La ejecución única **no figura como ítem explícito** en la lista de limitaciones (`sec:limitaciones`, cap. 8).

### IX.1.4 — Factores confundidos, prompts y contradicciones (V.5) · ✅ CUMPLE

- Sección "Alcance operativo y factores confundidos" (metodología): recuperador siempre gpt-5, diferencias simultáneas de prompt/descomposición/candidatos/selección/presupuesto, límites 7 (gpt-5) vs. 6 (mini/nano) declarados como amenaza, imposibilidad de atribución sin ablaciones, etiqueta acotada ("dos agentes activos, una delegación nominal … ninguna verificación automática").
- Prompts del especialista, del recuperador y del Agente de Calidad reproducidos literalmente en bloques; se declara la excepción `16_01` (3 llamadas) y las dos variantes del prompt del recuperador.
- El capítulo 3 ya no atribuye few-shot/CoT al sistema: "El sistema de este trabajo no incorpora ejemplos etiquetados en el prompt ni una instrucción explícita de cadena de pensamiento. Su diseño se apoya en prompting zero-shot…" ✅ (pedido explícito en V.5).
- Contradicciones del Agente de Calidad resueltas: única razón (costo y complejidad), "no se realizó una comparación empírica de su contribución", "el prompt nunca se envió a un modelo".
- Salvedad ⚠️: los prompts de sin-RAG y RAG básico se describen ("prompt simplificado que instruye al modelo como asistente legal experto…") pero no se reproducen literalmente en el manuscrito; el texto los remite al "anexo de prompts del repositorio" (el anexo del manuscrito no los contiene — ver IX.1.8).

### IX.1.5 — Reformular conclusiones (Tabla 4) · ⚠️ PARCIAL

**Cumple (versión reformulada presente):**
- "La recuperación mejora…": ahora condicional — "La recuperación no produce una mejora uniforme: el efecto depende del modelo" (evaluación, Fortalezas) + IC del escenario principal ✅.
- Interacción: mantenida como patrón y sustentada por el ordinal; "no identifica un componente causal único" ✅.
- "Efecto igualador": retirado — "Con RAG básico las diferencias entre modelos son menores, pero no se demostró equivalencia"; contribución con redacción "Límites de la hipótesis de igualación… debe retirarse" ✅ (`grep` "igualador": 0).
- "Sobrecarga agéntica" → "modos de fallo observados" ✅ (`grep` "sobrecarga": 0).
- "Validación de LLM-as-a-Judge" → "Confiabilidad inter-juez, no validación" (α como confiabilidad; "no se compararon con criterio humano") ✅.
- Objetivo 2 → "se cumplió parcialmente" con explicación (dos agentes activos, verificador inactivo, delegación nominal) ✅.
- Recomendación costo-eficiente → "alternativa no dominada", "no la más barata", con costo por respuesta correcta (evaluación, Implicaciones Prácticas) ✅ — V.10 satisfecha en evaluación.
- Transferibilidad → "no se demostró transferencia a otros dominios"; "evidencia de viabilidad y no una validación externa" (resumen, reflexiones) ✅.

**Residuos a corregir (cap. 8, sección "Fortalezas del Sistema"):**
- "*Mejora significativa con recuperación.* Tanto el RAG básico como el Agentic-RAG superan significativamente al baseline sin RAG (p < 0.001 …; p = 0.0066 …)" — efecto marginal incondicional, exactamente la formulación que la Tabla 4 pide condicionar al modelo y a la estrategia (y usa los p de las pruebas independientes).
- "*Configuración costo-eficiente viable.* La combinación Agentic-RAG con gpt-5-mini… ofreciendo una alternativa práctica para escenarios con restricciones presupuestarias." — contradice la corrección adoptada en evaluación y la fila de Tabla 4 (la configuración no es la más barata ni lidera el índice).
- "*Análisis estadístico riguroso.* … (Shapiro-Wilk, Kruskal-Wallis, Dunn con Bonferroni, Scheirer-Ray-Hare), complementadas con análisis de efectos simples (Mann-Whitney U…" — lista antigua sin el modelo ordinal ni las pruebas pareadas; contradictoria con lo que el propio capítulo declara como inferencia principal.
- En evaluación resta la explicación "capacidad de razonamiento interna" para gpt-5 ("compensando parcialmente la ausencia de contexto mediante su capacidad de razonamiento interna"), señalada en el plan (IX.1.5) para presentarla solo como hipótesis.
- Coherencia menor: el índice de eficiencia con piso 0,01 sigue presentándose sin la crítica de V.10 (piso arbitrario), aunque se agregaron costo por respuesta correcta y lectura de no-dominancia.

### IX.1.6 — Corpus, origen y respuestas de referencia (V.9, V.7) · ✅ CUMPLE (con salvedades)

- **Origen resuelto**: "texto base proviene del PDF del Boletín Oficial de 1997 y cuyo texto actualizado se contrastó con la versión publicada en Infoleg… Las rutas de descarga automática se evaluaron, pero no fueron el pipeline principal" (intro) + cadena de proceso documentada en 8 pasos (metodología) + "El parser HTML se intentó, pero se descartó…" — desaparece la contradicción "se descartaron (Infoleg)" vs. "actualizado con Infoleg".
- **Conteos unificados**: 482 partes (22 títulos, 6 secciones, 55 acápites, 398 artículos, 1 apéndice), 362 números únicos (el apéndice repite 1–36), artículo 239 derogado/vacío, 397 con texto — elimina las cifras 245/399.
- **Fecha de sanción** en metadatos del benchmark: "1886-11-25" ✅ (corregida desde 1994-01-01).
- **Respuestas de referencia corregidas en el anexo**: 1.2 ahora funda la propiedad distinta del terreno en el art. 11 (antes art. 8/"derecho real separado"), y 1.3 reproduce los criterios completos del art. 17 ("seguridad pública, la conservación de las pertenencias y la salud o existencia de los trabajadores") ✅.
- Validación del benchmark documentada con sus etapas y el matiz "No existió una segunda revisión independiente" ✅ (V.7).
- Salvedad ⚠️ (V.9): la calidad de la extracción sigue siendo "inspección manual de una muestra de artículos, comparando el texto extraído con el original en Infoleg" **sin tamaño de muestra ni tasa de error** — no cuantificada (coincide con lo documentado en el registro de cobertura).
- Salvedad: las unidades con referencia controvertida (Q23–Q25) quedan fuera de alcance según decisiones; el cap. 8 declara que "una revisión posterior asistida por IA detectó posibles errores que requieren una nueva revisión profesional; … no se aplicaron retroactivamente" (correcto y transparente).

### IX.1.7 — Tablas 2 y 3 y auditoría bibliográfica · ⚠️ PARCIAL

**Tabla 3 (problemas de citas y referencias) — ✅ CUMPLE, verificada en `.bib` y en el PDF renderizado:**
- `bommasani…` eliminada; `bozdag2024gender` con autores/año/DOI correctos y usada en cap. 3 con atribución ajustada ("basado en fine-tuning… sin atribuir el método a variantes de adapters") ✅.
- Estudio de alucinaciones → `magesh2025hallucinationfree` (Magesh et al., 2025) citado y listado; no queda cita errónea a Dahl/AI Legal Analysis ✅.
- Desambiguación de mismo autor-año: `wei2022cot`/`wei2022emergent` y `zhao2026surveySpringer`/`zhao2026reportlogic` — el PDF muestra "(2022a)"/"(2022b)" (4 y 2 apariciones), es decir, Typst resuelve la distinción ✅.
- `deepseek2025r1` con nota de fecha oficial de lanzamiento (20-01-2025); sin entradas "DeepSeek (2026b)" duplicadas ✅; "Meta (2026)" corregido → "(DeepSeek-AI, 2025)" y "Meta, 2025" en el PDF ✅; Llama 4 = "abril de 2025" con nota "5 de abril de 2025" ✅.
- `niklaus2023lextreme`: year = 2023 con DOI de Findings of EMNLP 2023 ✅.
- `tribunalfiscal2024buscador` apunta a la página oficial (`argentina.gob.ar/tribunalfiscal/jurisprudencia`) con nota aclaratoria ✅.
- **Ausencias incorporadas**: `lewis2020rag` (citado en intro `@lewis2020rag` y listado) y `codigo_mineria_1919` ("Honorable Congreso de la Nación Argentina. (1886, noviembre). Ley 1.919. Código de Minería…", citado en metodología) ✅.
- **Versiones con revisión de pares preferidas**: BERT (NAACL-HLT 2019), LoRA (ICLR 2022), QLoRA (NeurIPS 2023), Self-RAG (ICLR 2024) ✅.
- Forma: citas y referencias renderizan con "et al." uniforme (estilo `apa` de Typst; `grep` "y col" solo encuentra la prosa "y colaboradores"); fechas de sitios web con nota de acceso y año ✅. La auditoría completa entrada por entrada (IX.1.7.C) excede el alcance de esta verificación textual (fue realizada en `correccion-07` según el registro de decisiones).

**Tabla 2 (errores verificados en el texto) — estado por ítem:**

| Ítem (Tabla 2) | Estado | Evidencia |
|---|:---:|---|
| p. 1 — oración trunca "Al combinar…" | ✅ | Cap. 1: "La combinación de grandes modelos de lenguaje (LLM) con mecanismos de recuperación de información permite fundamentar las respuestas en documentos externos." |
| p. 12 — n-gramas "caracteres" vs. ejemplo con palabras | ❌ | `03_capitulo_02…typ`:101 sigue diciendo "los cuales consisten en secuencias de caracteres de longitud $n$" con tablas de palabras ("Palabra") |
| p. 23 — atención como "similitud coseno escalada" | ❌ | `03_capitulo_02…typ`:333: "La atención entre una query y todas las keys se calcula como la similitud coseno escalada" (la fórmula correcta ya está debajo; falta corregir la prosa) |
| pp. 25-26 — GPT-4 "arquitectura MoE" | ❌ | `03_capitulo_02…typ`:371 (cronología) y :409 ("modelo multimodal con arquitectura *Mixture of Experts* (MoE)") — la fuente (informe técnico) no describe la arquitectura |
| pp. 30, 32 — LEGAL-BERT/Case Law/LegalBench | ✅ | Cap. 3: corpus correcto de LEGAL-BERT; Case Law como recurso distinto de Zheng et al.; "no corresponde afirmar que LEGAL-BERT superó a BERT en 'todas las tareas de LegalBench'" |
| p. 36 — "el Código solo tiene 245 artículos" | ✅ | Cap. 3 usa "artículo 1234 … no existe en el corpus"; metodología da conteos unificados |
| pp. 106-110 — fechas DeepSeek-R1/Llama 4/Qwen3/Gemini 3 Pro | ✅ | Cap. 7: "DeepSeek-R1 (enero de 2025)", "Llama 4 en abril de 2025", "Qwen3 (abril de 2025)", "Gemini 3 Pro (18 de noviembre)" (texto y línea de tiempo unificados) |
| p. 147 — Tabla 20 fecha de sanción | ✅ | Anexo: "Fecha de sanción 1886-11-25" |
| Referencias cruzadas "capítulo Sección 4" | ✅ | `grep` "Sección 4 / sección Sección / capítulo Sección": 0 coincidencias |
| p. 29 — nota con Wikipedia | ✅ | `grep` "Wikipedia": 0 coincidencias en los `.typ` |
| p. iii — dedicatoria "A mi familia …" | ❌ | `01_texto_preliminar.typ`: sigue literal "A mi familia ..." (apariencia provisoria, señalada por el tribunal) |

### IX.1.8 — Declaración de IA, título y repositorio (V.11) · ⚠️/✅

**Cumple:**
- **Título y portada actualizados** en `main.typ`: "Desarrollo y evaluación de un prototipo Agentic-RAG para consulta del Código de Minería argentino" — refleja el alcance real (un solo código) ✅.
- **Declaración de IA ampliada** (`01_texto_preliminar.typ`): cinco etapas (corpus con `o4-mini`, benchmark con GPT-4.1 + profesional, generación con GPT-5, jueces DeepSeek/Grok/Kimi, asistencia en investigación y edición), verificación del autor, límites de la verificación ("no incluyó una validación humana de la calidad de las 711 respuestas"), antecedente de la referencia fabricada detectada y eliminada, y nota sobre `reasoning_effort` ✅ — responde IX.1.8/V.11.
- Objetivo 4 con matiz ("El acceso público está verificado; la clonación y ejecución se recomiendan como verificación de reproducibilidad") — no reclama reproducibilidad demostrada ✅.
- Sin interfaz/usuarios reconocidos (limitación explícita "Ausencia de evaluación con usuarios reales") ✅.
- Compila sin errores (`make pdf`, 167 páginas) ✅.

**Pendiente:**
- **Anexo "Estructura del Repositorio de Código" obsoleto** (`anexo_01.typ`): el árbol sigue mostrando `archivo/`, `examples/notebooks/`, `00_escritura/` y el módulo `04_vector_database_creation/` con pgvector, incompatible con la estructura real del repositorio publicada (y descrita en metodología: `codigo_experimentos/` con `part_a`…`part_j`). V.11/IX.1.8 exigen consistencia entre el anexo, el README y el repositorio; el plan de correcciones ya identificaba este punto ("sustituir el árbol obsoleto").
- **Objetivo general** (cap. 1, ~105) mantiene "para responder consultas de usuarios profesionales y no profesionales en el derecho" sin ajustar el alcance (el acotamiento está hecho en resumen, limitaciones y conclusiones, pero el objetivo general no fue tocado — V.11/Tabla 4, última fila).
- El cuerpo remite varias veces a "el anexo de prompts del repositorio" y a rutas `verificacion-analisis-estadistico/` (metodología ~708, evaluación ~314, cap. 8 ~37) — ubicaciones que el anexo del manuscrito no describe y cuya existencias el lector del PDF no puede asumir; conviene aclarar dónde viven esos artefactos (repositorio público) o integrarlos al anexo.

### IX.1.9 — Métricas de recuperación (V.8) · ✅ CUMPLE

- Sección "Métricas de recuperación" en evaluación (~314): tabla con **recall@10, MRR, % de unidades con todos/ningún artículo de referencia en el top-10** para RAG básico (0,333 / 0,214 / 27,9 % / 59,5 %) y Agentic-RAG por especialista (0,399–0,446 / 0,242–0,281 / 32,9–35,4 % / 44,3–50,6 %).
- Caveat metodológico incluido: comparación descriptiva, presupuesto no igualado, "No se comparó con BM25 ni con otro embedding porque el volumen de Milvus se perdió" ✅ (y esa comparación queda como recomendación IX.2.1, no obligatoria).
- MRR ahora se usa en el texto ✅; el índice `AUTOINDEX` (no IVF_FLAT) es coherente en metodología y cap. 8 ✅ (NV-06).
- Salvedad ⚠️ (V.8): la afirmación "Un modelo entrenado específicamente en español **evita la pérdida de matices** que introduce la traducción implícita de los modelos multilingües" (metodología, criterios de selección del embedding) sigue sin respaldo empírico — el tribunal la marcó explícitamente como no sustentada y no fue atenuada ni probada.

---

## 3. Cobertura cruzada por observación del tribunal (V.1–V.11)

| Observación | Estado en el manuscrito | Comentario |
|---|:---:|---|
| V.1 apareamiento/modelos mixtos | ⚠️ | Ordinal + IC presentes; Friedman/Wilcoxon ausentes; "modelos mixtos" en anexo; tabla MWU |
| V.2 Scheirer-Ray-Hare | ✅ | Degrado a exploratorio con sustento ordinal |
| V.3 equivalencia inferida | ✅ | "no se demostró equivalencia" en evaluación, resumen y cap. 8 |
| V.4 temperatura/esfuerzo/réplicas | ⚠️ | Esfuerzo documentado ✅; determinismo aún afirmado en 4 lugares ❌; ejecución única sin ítem de limitación |
| V.5 factores confundidos | ✅ | Sección dedicada + prompts + contradicciones resueltas |
| V.6 celda nano y faltantes | ⚠️ | 41/79 y modo de fallo ✅; casos 23–25 no reincorporados; explicación faltantes sin corregir; restos causales |
| V.7 validez de la medición | ⚠️ | Benchmark/jueces con matices correctos ✅; Grok corregido sin cantidad; imputación sin conteo de casos; citas deterministas no ejecutadas (NV-03, trabajo futuro) |
| V.8 recuperación | ✅ | Métricas informadas; embedding sin comparación (recomendación) |
| V.9 corpus | ✅ | Versión, linaje, conteos y fecha unificados; tasa de error de extracción sin cuantificar |
| V.10 costos | ⚠️/✅ | Costo por respuesta correcta y no-dominancia incorporados; índice con piso 0,01 persiste sin crítica |
| V.11 título/alcance/repo/IA | ⚠️ | Título, declaración y moderación ✅; anexo de repositorio obsoleto ❌; objetivo general sin ajustar |

---

## 4. Recomendaciones IX.2 (no condicionan la aprobación)

| # | Recomendación | Estado | Nota |
|---|---|:---:|---|
| IX.2.1 | Comparar embedding con recuperador entrenado / BM25 | ❌ | Declarado explícitamente: "No se comparó con BM25 ni con otro embedding porque el volumen de Milvus se perdió" |
| IX.2.2 | Citas deterministas (precisión/exhaustividad/inexistentes) | ❌ | No ejecutado (NV-03 cancelada por tiempo; trabajo futuro); la rúbrica de precisión legal sigue excluida por baja confiabilidad |
| IX.2.3 | Validación humana de jueces (submuestra) | ❌ | No realizada; declarada como limitación (`lim:sin-validacion-manual`) ✅ en forma |
| IX.2.4 | Réplicas (3–5) y ablación con mismo modelo en ambos agentes | ❌ | No ejecutadas; mencionadas como requisito para recomendaciones ("no se recomienda sin réplicas ni ablaciones") |
| IX.2.5 | Reducir capítulo 2 y sección 7.7 | ❌ | Sin reducción; se agregó nota de alcance temporal y la sección "Desarrollos Posteriores" se mantiene completa (4 líneas de tiempo, incluida 2026) |

Estos ítems están, en general, **transparencia-declarada** (limitaciones o trabajo futuro), lo cual es defendible ante el tribunal, aunque la reducción editorial de IX.2.5 es solo material pendiente.

---

## 5. Priorización de pendientes concretos para la versión definitiva

Los tres primeros corresponden a las correcciones que el tribunal califica de **indispensables** (sección X) y sobre las que la defensa será interrogada.

1. **IX.1.1/IX.1.2 — Inconsistencias estadísticas** (alta):
   - Reemplazar o renombrar la tabla de efectos simples por efectos del modelo ordinal (o etiquetarla explícitamente como análisis exploratorio histórico) y describir Friedman/Wilcoxon en metodología (aunque sea como sensibilidad, con sus resultados).
   - Unificar el encuadre "principal": metodología + limitación del cap. 8 dicen "robustez/pareadas"; evaluación dice "ordinal como principal".
   - Corregir `anexo_01.typ:86` ("modelos mixtos" → descripción real del análisis).
   - Definir los escenarios de fallo en metodología antes de usarlos en evaluación.
2. **IX.1.2 — Faltantes** (alta):
   - Corregir la explicación de los 27 faltantes (join de los casos 23–25) y el "684" → reincorporar o, al menos, reportar el análisis con 23–25 incluidos como escenario.
   - Eliminar las frases causales residuales en evaluación ("complejidad agéntica es excesiva…", "contextos de complejidad excesiva").
3. **IX.1.3 — Determinismo** (alta, edición simple):
   - Eliminar/reescribir las 4 afirmaciones de determinismo (`metodologia.typ` 511, 521, 660; `evaluacion.typ` 16) conforme a lo ya documentado en la declaración y en la tabla de hiperparámetros.
   - Reparar las 2 referencias rotas ("sección/corrección sobre parámetros de API") apuntando a la sección real del manuscrito.
   - Agregar "ejecución única por celda" como ítem de `sec:limitaciones`.
4. **IX.1.5 — Residuos de conclusiones** (media):
   - Reformular en cap. 8 "Fortalezas del Sistema" los ítems "Mejora significativa con recuperación", "Configuración costo-eficiente viable" y "Análisis estadístico riguroso" (lista antigua sin ordinal/pareado).
   - Presentar "capacidad de razonamiento interna" de gpt-5 como hipótesis.
5. **IX.1.7 — Errores de la Tabla 2 restantes** (media):
   - n-gramas: "secuencias de $n$ unidades (caracteres o palabras)" y aclarar que el ejemplo usa palabras (`03…typ`:101).
   - Atención: sustituir "similitud coseno escalada" por "producto escalar escalado por $\sqrt{d_k}$" (`03…typ`:333).
   - GPT-4/MoE: eliminar la atribución arquitectónica o marcarla como no documentada (`03…typ`:371 y 409).
   - Completar o retirar la dedicatoria "A mi familia ...".
6. **IX.1.8 — Coherencia de anexo y alcance** (media):
   - Actualizar el árbol del repositorio del anexo (`examples/notebooks/` → estructura actual; incluir `codigo_experimentos/` y los artefactos de verificación citados en el cuerpo).
   - Evaluar ajuste del objetivo general o añadir la declaración de alcance allí (hoy solo en resumen/limitaciones/conclusiones).
7. **Salvedades menores** (baja):
   - Cuantificar Grok corregido a mano y los casos alcanzados por la imputación (V.7).
   - Tamaño de muestra / tasa de error de la extracción del corpus (V.9).
   - Atenuar "evita la pérdida de matices…" del criterio de selección del embedding (V.8).
   - Criticar el piso 0,01 del índice de eficiencia donde se presenta (V.10).
   - MRR/siglas: quitar HNSW de siglas si no se usa.

---

## 6. Verificación técnica

- Compilación: `make pdf` → exitosa, 0 errores; PDF de 167 páginas.
- Sin referencias cruzadas duplicadas ("capítulo Sección 4"), sin menciones a Wikipedia, sin "n = 79 observaciones por celda", sin "sobrecarga agéntica" ni "efecto igualador" (grep: 0 en todos los casos).
- Citas desambiguadas en el PDF: "(2022a)/(2022b)" presentes; "DeepSeek-AI (2025)", "Meta (2025)", "Magesh et al. (2025)", "Bozdag et al. (2024)", Lewis et al. (2020) y la entrada de la Ley 1.919 (1886) verificados en el texto renderizado.
- Estilo de citas uniforme "et al."; sin restos de "y col."/"y cols.".
- El PDF compilado (`manuscrito_latest.pdf`) refleja el estado de los `.typ` verificados en esta sesión.

## 7. Veredicto

El manuscrito está **sustancialmente actualizado frente a la valoración y en condiciones de defensa**, pero **aún no refleja íntegramente los requerimientos del tribunal**: los puntos con mayor riesgo para la versión definitiva son las **inconsistencias internas del reanálisis estadístico** (IX.1.1/IX.1.2: tabla Mann-Whitney vs. "se estimaron con ese modelo", "robustez" vs. "principal", "modelos mixtos" en el anexo, explicación de los 27 faltantes y las 684 observaciones), las **afirmaciones de determinismo todavía vigentes** (IX.1.3, edición trivial pero central según la sección X del tribunal), los **tres errores conceptuales restantes del capítulo 2** (n-gramas, atención, MoE) y el **anexo de repositorio obsoleto**. Con esas ediciones — todas localizadas y enumeradas en la §5 — el manuscrito quedaría alineado con la totalidad de las correcciones requeridas; las recomendaciones IX.2 permanecen correctamente declaradas como limitaciones o trabajo futuro.

---
*Reporte generado por `ollama-cloud-glm-5-3-flash` (pi coding agent). Fuente de los requierimientos: `Valoracion_TF_Spairani_gp_actualizada.md`. Verificación limitada al texto del manuscrito y su render; no se re-ejecutaron experimentos.*

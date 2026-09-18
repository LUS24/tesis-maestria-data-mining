#import "@preview/diatypst:0.9.3": *

// ─── Portada personalizada ───────────────────────────────────────────
#set page(
  footer: none, header: none, margin: 0cm,
  height: 10.5cm,
  width: 16/9 * 10.5cm,
)

#align(center + horizon)[
  // #v(0.5cm)
  #image("../../manuscrito/media/logo_universidad_austral_ingenieria.png", height: 30%)

  #text(size: 20pt, weight: "bold")[Desarrollo y evaluación de un prototipo de sistema inteligente para consulta de normativa nacional argentina mediante recuperación agéntica]

  #text(size: 16pt)[Leonardo Ulises Spairani]

  #text(size: 14pt)[Tesis de Maestría en Data Mining]

  #text(size: 12pt)[Universidad Austral — 2026]
]

// ─── Configuración de slides ─────────────────────────────────────────
#show: slides.with(
  title: "Sistema Agentic-RAG para consulta de normativa argentina",
  subtitle: "Tesis de Maestría — Universidad Austral",
  date: "2026",
  authors: ("Leonardo Ulises Spairani"),
  ratio: 16/9,
  layout: "medium",
  title-color: blue.darken(60%),
  toc: false,
  first-slide: false,
  bg-color: white,
  count: "number",
  theme: "full",
)

// ═══════════════════════════════════════════════════════════════════════
// 1. AGENDA
// ═══════════════════════════════════════════════════════════════════════
= Agenda

#v(0.5cm)

1. Motivación y problema
2. Objetivos
3. Contexto: PLN y dominio legal
4. Marco teórico: Agentic-RAG
5. Metodología e implementación
6. Diseño experimental
7. Resultados
8. Discusión
9. Contribuciones y limitaciones
10. Conclusiones y trabajo futuro

// ═══════════════════════════════════════════════════════════════════════
// 2. MOTIVACIÓN
// ═══════════════════════════════════════════════════════════════════════
= Motivación

== El problema del acceso a la normativa argentina

- La legislación argentina está dispersa en múltiples fuentes: Infoleg, SAIJ, Boletín Oficial.
- Los sistemas tradicionales de búsqueda legal se basan en *coincidencia de palabras clave*.
- No capturan la semántica del lenguaje jurídico ni las relaciones contextuales entre conceptos.
- Resultados irrelevantes o incompletos, especialmente para *usuarios no especializados*.

#v(0.5cm)

#align(center)[
  #text(size: 14pt, weight: "bold")[¿Cómo podemos mejorar el acceso a la normativa legal argentina usando inteligencia artificial?]
]

== Desafíos específicos del dominio legal

- *Lenguaje técnico y formulista*: vocabulario especializado, estructuras rituales, red densa de remisiones internas.
- *Documentos extensos y jerárquicos*: códigos con miles de artículos, múltiples niveles (título, capítulo, sección, artículo, inciso).
- *Alto costo del error*: una respuesta incorrecta puede afectar derechos fundamentales.
- *Dependencia jurisdiccional*: el derecho es local — los modelos entrenados en inglés tienen utilidad limitada en Argentina.
- *Sistema continental (civil law)*: la ley escrita es la fuente principal, a diferencia del _common law_ anglosajón.

// ═══════════════════════════════════════════════════════════════════════
// 3. OBJETIVOS
// ═══════════════════════════════════════════════════════════════════════
= Objetivos

== Objetivo general

Desarrollar un sistema *Agentic-RAG de código abierto* como prueba de concepto, utilizando el Código de Minería Argentino, para responder consultas de usuarios profesionales y no profesionales en el derecho.

== Objetivos específicos

1. *Base de datos vectorial* del Código de Minería Argentino para sistemas RAG.
2. *Sistema de agentes de IA* que trabajen de manera conjunta con RAG.
3. *Benchmark específico* para evaluar el desempeño del sistema.
4. *Código abierto*: repositorio público para replicación y adaptación a otras normativas.

// ═══════════════════════════════════════════════════════════════════════
// 4. CONTEXTO: PLN + DOMINIO LEGAL
// ═══════════════════════════════════════════════════════════════════════
= Contexto

== Evolución del PLN: de n-gramas a Transformers

- *1913–1990s*: Modelos estadísticos (Markov, Shannon), n-gramas, sistemas basados en reglas (ELIZA).
- *2003–2017*: Redes neuronales (Bengio), word embeddings (Word2Vec, GloVe), LSTM, GRU.
- *2017*: Arquitectura *Transformer* @vaswani2017 — atención multi-cabezal, procesamiento paralelo.
- *2018–2022*: BERT, GPT-3, ChatGPT — modelos fundacionales y capacidades emergentes.
- *2023–2025*: GPT-4, Claude, DeepSeek — razonamiento, agentes, modelos de código abierto.

== PLN aplicado al derecho

- *Tareas principales*: recuperación de información legal, respuesta a preguntas legales (LegalQA), verificación de afirmaciones.
- *Adaptación de LLMs al dominio*: pre-entrenamiento de dominio, fine-tuning, PEFT (LoRA), in-context learning.
- *Riesgos críticos*: alucinaciones y citas falsas — el caso _Mata v. Avianca_ (2023).
- *Solución estructural*: RAG ancla cada respuesta en documentos reales y verificables.

// ═══════════════════════════════════════════════════════════════════════
// 5. MARCO TEÓRICO: AGENTIC-RAG
// ═══════════════════════════════════════════════════════════════════════
= Marco Teórico: Agentic-RAG

== De RAG clásico a Agentic-RAG

#figure(
  align(center, image("../../manuscrito/media/diag_base_rag.svg", width: 70%)),
  caption: [RAG clásico: pipeline estático _retrieve-then-read_.],
)

#v(0.3cm)

*Agentic-RAG* extiende RAG con un *planificador autónomo* que decide:
- Cuándo y cómo buscar información.
- Qué herramientas utilizar (búsqueda vectorial, web, grafos, SQL).
- Cuándo iterar y cuándo detenerse.

== Arquitectura Agentic-RAG

#figure(
  align(center, image("../../manuscrito/media/diag_agentic_rag.svg", width: 80%)),
  caption: [Arquitectura Agentic-RAG con componentes agénticos.],
)

== Patrones de flujo de trabajo agéntico

- *Encadenamiento*: secuencia de pasos (reformular → recuperar → agrupar → generar).
- *Enrutamiento*: clasificador deriva la consulta a sub-flujos especializados.
- *Paralelización*: múltiples recuperadores sobre variantes de la consulta.
- *Orquestador–Trabajadores*: un orquestador descompone la tarea y asigna a agentes especializados.
- *Evaluador–Optimizador*: un evaluador juzga la calidad y un optimizador ajusta.

== LLM-as-a-Judge

- Paradigma donde un LLM actúa como *evaluador* de las respuestas generadas.
- *Ventajas*: escalable, captura dimensiones que métricas léxicas (BLEU, ROUGE) no miden.
- *Atributos evaluables*: utilidad, seguridad, confiabilidad, relevancia, lógica, calidad general.
- *Sesgos conocidos*: posición, verbosidad, egocéntrico, autoridad.
- *En esta tesis*: 3 jueces independientes (DeepSeek-V3, Grok 4.1, Kimi K2) con rúbricas estructuradas.

// ═══════════════════════════════════════════════════════════════════════
// 6. METODOLOGÍA E IMPLEMENTACIÓN
// ═══════════════════════════════════════════════════════════════════════
= Metodología e Implementación

== Corpus y extracción de datos

- *Código de Minería Argentino* (Ley 1.919): 22 títulos, 398 artículos, 482 partes estructurales.
- *Extracción*: PDF oficial → imágenes → modelo de visión o4-mini → texto estructurado.
- *Segmentación*: un artículo por fragmento, preservando metadatos (título, capítulo, sección).

== Base de datos vectorial

- *Milvus 2.5.9*: base de datos vectorial de código abierto.
- *Embeddings*: `hiiamsid/sentence_similarity_spanish_es` — 768 dimensiones, optimizado para español.
- *Índice*: IVF_FLAT con similitud coseno.
- *Esquema*: id, contenido, título, capítulo, sección, número de artículo, vector.

== Arquitectura del sistema Agentic-RAG

*Dos agentes especializados* (Pydantic AI):

1. *Agente Especialista Legal*: recibe la consulta, invoca al agente de recuperación, genera la respuesta final citando fuentes.
2. *Agente de Recuperación*: descompone consultas complejas (máx. 3 subconsultas), ejecuta búsquedas vectoriales (máx. 6), consolida resultados.

#v(0.3cm)

*Flujo*: Consulta → Agente Legal → Agente Recuperación → Búsqueda vectorial → Consolidación → Respuesta final

== Configuraciones evaluadas

#figure(
  align(center, image("../../manuscrito/media/diag_no_rag.svg", width: 30%)),
  caption: [Sin RAG: el modelo responde desde su conocimiento paramétrico.],
)

#figure(
  align(center, image("../../manuscrito/media/diag_base_rag.svg", width: 50%)),
  caption: [RAG básico: búsqueda vectorial simple + inyección de contexto.],
)

#figure(
  align(center, image("../../manuscrito/media/diag_agentic_rag.svg", width: 70%)),
  caption: [Agentic-RAG: dos agentes coordinados con descomposición de consultas.],
)

// ═══════════════════════════════════════════════════════════════════════
// 7. DISEÑO EXPERIMENTAL
// ═══════════════════════════════════════════════════════════════════════
= Diseño Experimental

== Diseño factorial 3 × 3

#align(center)[
  #table(
    columns: 4,
    stroke: 0.5pt,
    [*Estrategia*], [*gpt-5-nano*], [*gpt-5-mini*], [*gpt-5*],
    [Sin RAG], [✓], [✓], [✓],
    [RAG básico], [✓], [✓], [✓],
    [Agentic-RAG], [✓], [✓], [✓],
  )
]

- *9 configuraciones* × 79 unidades de evaluación = 711 observaciones.
- Temperatura 0 en todos los modelos (determinista).
- Modelos: GPT-5 nano (\$0.05/Mtok), mini (\$0.25/Mtok), estándar (\$1.25/Mtok).

== Benchmark y métricas

*Benchmark*: 25 preguntas tipo caso de estudio legal (79 subpreguntas), generadas con GPT-4.1 y validadas por profesionales del derecho argentino.

*Tres familias de métricas*:
- *Textuales*: Token F1, Jaccard, Levenshtein, BLEU, ROUGE, CER.
- *Semánticas*: SBERT Similarity (español y multilingüe), BERTScore.
- *LLM-as-a-Judge*: `respuesta_correcta` y `precision_legal` (3 jueces, escala 0–1).

*Variable de respuesta principal*: `respuesta_correcta_avg` (α de Krippendorff = 0.81).

// ═══════════════════════════════════════════════════════════════════════
// 8. RESULTADOS
// ═══════════════════════════════════════════════════════════════════════
= Resultados

== Comparación global entre estrategias

#align(center)[
  #table(
    columns: 3,
    stroke: 0.5pt,
    [*Estrategia*], [*Mediana*], [*Media*],
    [Sin RAG], [0.583], [0.55],
    [RAG básico], [0.708], [0.64],
    [*Agentic-RAG*], [*0.833*], [*0.66*],
  )
]

- Kruskal-Wallis: $H = 21.83$, $p < 0.001$ — diferencias significativas entre estrategias.
- Agentic-RAG vs. sin RAG: $p = 0.000014$ (significativo).
- RAG básico vs. sin RAG: $p = 0.0066$ (significativo).
- Agentic-RAG vs. RAG básico: $p = 0.383$ (no significativo a nivel global).

== Interacción estrategia × modelo

#figure(
  align(center, image("../../manuscrito/media/interaccion_modelo_estrategia.pdf", width: 90%)),
  caption: [Interacción disordinal: el efecto de la estrategia depende del modelo.],
)

- Scheirer-Ray-Hare: $H = 56.62$, $p < 10^{-11}$ — *interacción significativa*.
- La interacción supera a ambos efectos principales.

== Resultados por configuración

#align(center)[
  #table(
    columns: 4,
    stroke: 0.5pt,
    [*Estrategia*], [*Modelo*], [*Mediana*], [*Media*],
    [Sin RAG], [gpt-5-nano], [0.583], [0.58],
    [Sin RAG], [gpt-5-mini], [0.333], [0.35],
    [Sin RAG], [gpt-5], [0.833], [0.73],
    [RAG básico], [gpt-5-nano], [0.583], [0.59],
    [RAG básico], [gpt-5-mini], [0.625], [0.64],
    [RAG básico], [gpt-5], [0.833], [0.70],
    [Agentic-RAG], [gpt-5-nano], [0.083], [0.40],
    [Agentic-RAG], [*gpt-5-mini*], [*0.917*], [*0.78*],
    [Agentic-RAG], [*gpt-5*], [*0.958*], [*0.80*],
  )
]

== Hallazgos principales

*Efecto del modelo dentro de cada estrategia*:
- *Agentic-RAG*: los modelos difieren significativamente ($p < 0.0001$).
- *Sin RAG*: los modelos difieren significativamente ($p < 0.0001$).
- *RAG básico*: los modelos *no* difieren ($p = 0.095$) → *efecto igualador*.

*Efectos simples de estrategia (corrección Holm-Bonferroni)*:
- *gpt-5-mini*: Agentic-RAG supera a RAG básico ($p_"corr" = 0.018$) y a sin RAG ($p_"corr" < 0.0001$).
- *gpt-5-nano*: Agentic-RAG *degrada* respecto a RAG básico ($p_"corr" = 0.017$).
- *gpt-5*: sin diferencias significativas entre estrategias tras corrección.

== Análisis de costos

#figure(
  align(center, image("../../manuscrito/media/costos_por_configuracion.pdf", width: 80%)),
  caption: [Costo medio por consulta (USD). Agentic-RAG es más costoso por las llamadas adicionales al Agente de Recuperación (gpt-5).],
)

- *Costo total del experimento*: USD 22.29.
- *Combinación más costo-eficiente*: Agentic-RAG + gpt-5-mini (media 0.78, costo intermedio).

== Evaluación LLM-as-a-Judge

#figure(
  align(center, image("../../manuscrito/media/krippendorff_alpha_por_sistema.pdf", width: 80%)),
  caption: [Alpha de Krippendorff por sistema y rúbrica. `respuesta_correcta` supera el umbral aceptable en todos los sistemas.],
)

- `respuesta_correcta`: α = 0.81 (bueno) — *métrica confiable*.
- `precision_legal`: α = 0.78 global, pero < 0.67 en RAG básico y sin RAG — *no confiable*.

// ═══════════════════════════════════════════════════════════════════════
// 9. DISCUSIÓN
// ═══════════════════════════════════════════════════════════════════════
= Discusión

== Fortalezas

- *Mejora significativa con recuperación*: RAG básico y Agentic-RAG superan al baseline sin RAG.
- *Configuración costo-eficiente*: Agentic-RAG + gpt-5-mini (0.78) comparable a gpt-5 (0.80).
- *Efecto igualador del RAG básico*: elimina diferencias entre modelos, permitiendo usar modelos más económicos.
- *Evaluación robusta*: métricas textuales, semánticas y LLM-as-a-Judge con acuerdo inter-juez validado.
- *Trazabilidad completa*: logging de todas las interacciones entre agentes.

== Debilidades

- *Sobrecarga agéntica*: Agentic-RAG degrada a gpt-5-nano (0.40 vs. 0.59 con RAG básico).
- *Sin diferencia marginal global*: Agentic-RAG vs. RAG básico no significativo a nivel agregado.
- *Métrica de precisión legal no confiable*: α < 0.67 en dos de tres sistemas.
- *Alcance limitado*: solo Código de Minería, sin evaluación con usuarios reales.
- *Dependencia de APIs comerciales*: costos recurrentes y dependencia externa.

// ═══════════════════════════════════════════════════════════════════════
// 10. TRABAJOS RELACIONADOS
// ═══════════════════════════════════════════════════════════════════════
= Trabajos Relacionados

== Comparación con sistemas existentes

#align(center)[
  #table(
    columns: 6,
    stroke: 0.5pt,
    [*Sistema*], [*Cód. abierto*], [*RAG*], [*Agentes*], [*Norm. arg.*], [*Benchmark*],
    [Infoleg / SAIJ], [N/A], [No], [No], [Sí], [No],
    [Westlaw CoCounsel], [No], [Sí], [Sí], [No], [No],
    [Lexis+ Protégé], [No], [Sí], [Sí], [No], [No],
    [Lexius / Juztina], [No], [Sí], [Sí], [Sí], [No],
    [*Este trabajo*], [*Sí*], [*Sí*], [*Sí*], [*Sí*], [*Sí*],
  )
]

*Vacíos identificados*:
- Ausencia de sistemas de código abierto para normativa argentina.
- Falta de benchmarks específicos para evaluación reproducible.
- Subrepresentación del español y del derecho civil en la investigación.

// ═══════════════════════════════════════════════════════════════════════
// 11. CONTRIBUCIONES
// ═══════════════════════════════════════════════════════════════════════
= Contribuciones

== Contribuciones principales

1. *Sistema Agentic-RAG de código abierto* para normativa argentina (prueba de concepto sobre Código de Minería).

2. *Evidencia empírica sobre interacción estrategia × modelo*: la efectividad de una estrategia de recuperación depende del modelo con el que se combine ($H = 56.62$, $p < 10^{-11}$).

3. *Efecto igualador del RAG básico*: elimina diferencias de desempeño entre modelos de distinta capacidad.

4. *Identificación de sobrecarga agéntica*: Agentic-RAG perjudica a modelos de capacidad reducida.

5. *Benchmark para el Código de Minería Argentino*: 25 preguntas validadas por profesionales del derecho.

6. *Validación de LLM-as-a-Judge*: acuerdo inter-juez bueno (α = 0.81) para evaluación de corrección.

7. *Metodología replicable*: documentación completa para adaptación a otras normativas.

// ═══════════════════════════════════════════════════════════════════════
// 12. LIMITACIONES
// ═══════════════════════════════════════════════════════════════════════
= Limitaciones

- *Alcance del corpus*: solo Código de Minería Argentino.
- *Benchmark de escala limitada*: 79 unidades de evaluación.
- *Dependencia de APIs comerciales*: costos recurrentes.
- *Sin evaluación con usuarios reales*: no hay evidencia directa de utilidad percibida.
- *Métrica de precisión legal no confiable*: α < 0.67 en dos sistemas.
- *Alcance temporal*: modelos evaluados corresponden al segundo semestre de 2025.
- *Sin validación manual de evaluaciones LLM-as-a-Judge*: la concordancia con criterio de expertos legales no fue cuantificada.
- *Sin prompting de cadena de pensamiento en jueces*: posible incremento de sesgos de evaluación.

// ═══════════════════════════════════════════════════════════════════════
// 13. CONCLUSIONES
// ═══════════════════════════════════════════════════════════════════════
= Conclusiones

== Conclusiones principales

1. Los sistemas con recuperación de información *mejoran significativamente* la calidad de las respuestas de LLMs en el dominio legal argentino.

2. La *interacción estrategia × modelo* es el hallazgo más relevante: no existe una recomendación universal — la selección debe hacerse de manera conjunta.

3. *Agentic-RAG + gpt-5-mini* es la combinación más costo-eficiente (media 0.78, comparable a gpt-5).

4. El *RAG básico iguala* el desempeño entre modelos, permitiendo usar modelos más económicos.

5. *Agentic-RAG no es adecuado para modelos pequeños*: degrada el desempeño de gpt-5-nano.

6. La metodología, el benchmark y el código abierto permiten la *replicación y adaptación* a otras normativas y jurisdicciones.

// ═══════════════════════════════════════════════════════════════════════
// 14. TRABAJO FUTURO
// ═══════════════════════════════════════════════════════════════════════
= Trabajo Futuro

== Líneas de investigación

- *Extensión del corpus*: incluir toda la normativa nacional de Infoleg, normativa provincial y municipal, y jurisprudencia.

- *Políticas adaptativas*: agente clasificador que decida dinámicamente entre RAG básico y Agentic-RAG según la complejidad de la consulta.

- *Recuperación híbrida*: combinar búsqueda vectorial + BM25 + grafos de conocimiento.

- *Modelos de código abierto*: evaluar familias Llama, Mistral, Qwen, DeepSeek para eliminar dependencia de APIs comerciales.

- *Ampliación del benchmark*: más preguntas, mayor diversidad, rúbricas refinadas para precisión legal.

- *Evaluación con usuarios reales*: estudios de usabilidad con abogados, funcionarios y ciudadanos.

- *Re-evaluación con modelos de nueva generación*: la metodología es directamente aplicable a modelos futuros.

// ═══════════════════════════════════════════════════════════════════════
// 15. CIERRE
// ═══════════════════════════════════════════════════════════════════════
= ¡Gracias!

#v(1cm)

#align(center)[
  #text(size: 18pt, weight: "bold")[¿Preguntas?]
]

#v(1.5cm)

#align(center)[
  #text(size: 14pt)[Código y benchmark disponibles en GitHub]
  #v(0.3cm)
  #text(size: 12pt)[Repositorio público — Metodología replicable]
]

#v(1cm)

#align(center)[
  #text(size: 12pt, style: "italic")[Leonardo Ulises Spairani]
  #v(0.2cm)
  #text(size: 11pt)[Tesis de Maestría en Data Mining — Universidad Austral — 2026]
]

#bibliography("../../manuscrito/referencias.bib", title: [Referencias], style: "apa")

= Conclusiones y Trabajos Futuros

== Introducción

El presente trabajo se propuso diseñar, implementar y evaluar un sistema de Generación Aumentada por Recuperación Agéntica (Agentic-RAG) de código abierto para la consulta de normativa argentina, utilizando el Código de Minería Argentino como prueba de concepto. A lo largo de los capítulos precedentes se presentaron los fundamentos teóricos de modelos de lenguaje, sistemas RAG, arquitecturas agénticas y Agentic-RAG; se describió la metodología y el diseño del sistema multi-agente; se detalló la implementación del prototipo completo ---desde la extracción de datos hasta el pipeline de evaluación---; y se analizaron los resultados experimentales mediante un diseño factorial de 3 estrategias de recuperación × 3 modelos de lenguaje, evaluados con métricas textuales, semánticas y evaluación LLM-as-a-Judge.

Este capítulo sintetiza los hallazgos principales, revisa el cumplimiento de los objetivos planteados, discute las fortalezas y limitaciones del trabajo y propone líneas de investigación futuras.

== Conclusiones

=== Cumplimiento de Objetivos

El trabajo planteó cuatro objetivos específicos, cuyo grado de cumplimiento se detalla a continuación:

+ *Desarrollar una base de datos vectorial del Código de Minería Argentino diseñada específicamente para trabajar con sistemas RAG.* Este objetivo se cumplió completamente. Se implementó una base de datos vectorial en Milvus con embeddings de 768 dimensiones generados por el modelo `hiiamsid/sentence_similarity_spanish_es`, empleando una estrategia de segmentación basada en la estructura natural del documento legal (un artículo por fragmento). El índice IVF\_FLAT con similitud coseno permite búsquedas semánticas eficientes sobre el corpus del Código de Minería.

+ *Desarrollar un sistema de agentes de inteligencia artificial para que trabajen de manera conjunta con el sistema RAG.* Este objetivo se cumplió parcialmente. Se implementó una arquitectura multi-agente acotada mediante Pydantic AI, con dos agentes activos: el Agente Especialista Legal (generación de respuestas) y el Agente de Recuperación (descomposición de consultas y búsqueda vectorial). El Agente de Calidad de Recuperación fue diseñado, pero se excluyó por razones de costo y complejidad y no participó en la configuración experimental. El especialista realiza una delegación nominal de recuperación; no hay iteración del especialista ni verificación automática de la respuesta. En consecuencia, el objetivo se cumple respecto de la coordinación entre recuperación y generación, pero no respecto de un ciclo completo de verificación multi-agente.

+ *Desarrollar un benchmark específico para el Código de Minería Argentino para evaluar el desempeño del sistema.* Este objetivo se cumplió. Se generó un benchmark de 25 preguntas tipo caso de estudio legal (76 subpreguntas explícitas más 3 preguntas evaluadas como unidad única, totalizando 79 unidades de evaluación), distribuidas entre los títulos del Código de Minería, con respuestas esperadas generadas por GPT-4.1 y revisadas por una profesional del derecho argentino. El benchmark fue empleado como instrumento de evaluación en las nueve configuraciones experimentales; no hubo una segunda revisión independiente.

+ *Cargar el código y una descripción de la metodología a un repositorio abierto para que cualquier organización, empresa o individuo pueda replicar y adaptar el sistema a otras normativas.* Este objetivo se cumplió. El código fue organizado en módulos independientes (notebooks) con documentación técnica en cada directorio, siguiendo el flujo del pipeline experimental, y se publicó en un repositorio público de GitHub.

=== Contribuciones del Trabajo

Las principales contribuciones del presente trabajo son:

+ *Sistema Agentic-RAG de código abierto para normativa argentina.* Se desarrolló un sistema completo que integra recuperación semántica, base de datos vectorial y agentes inteligentes, constituyendo, hasta donde se tiene conocimiento, el primer sistema de este tipo aplicado al Código de Minería Argentino con código disponible públicamente.

+ *Evidencia empírica sobre la interacción estrategia × modelo.* El hallazgo más relevante del trabajo es la interacción significativa entre la estrategia de recuperación y el modelo de lenguaje ($H = 56.62$, $p < 10^(-11)$), que demuestra que la efectividad de una estrategia depende del modelo con el que se combine. Este resultado tiene implicaciones prácticas directas: no existe una recomendación universal, y la selección de modelo y estrategia debe hacerse de manera conjunta.

+ *Efecto igualador del RAG básico.* Se demostró que el RAG básico elimina las diferencias significativas de desempeño entre modelos ($p = 0.095$), permitiendo que modelos más pequeños y económicos alcancen un desempeño comparable al de modelos superiores cuando se les provee de contexto relevante.

+ *Identificación de la sobrecarga agéntica en modelos pequeños.* Se documentó que el sistema Agentic-RAG degrada el desempeño de modelos de capacidad reducida. El análisis de efectos simples con corrección de Holm-Bonferroni confirma que gpt-5-nano sufre una degradación significativa con Agentic-RAG frente a RAG básico (media de 0.40 vs. 0.59, $p_"corr" = 0.017$), aunque la diferencia frente a sin RAG no alcanza significación estadística tras la corrección ($p_"corr" = 0.064$). Esto sugiere que la complejidad de las instrucciones y contextos generados por el sistema agéntico excede la capacidad de procesamiento de estos modelos.

+ *Benchmark para el Código de Minería Argentino.* Se creó un benchmark específico con 25 preguntas (79 unidades de evaluación), elaborado con asistencia de LLM y revisado por una profesional del derecho, que puede emplearse como referencia para futuras evaluaciones de sistemas de consulta legal sobre esta normativa.

+ *Validación de LLM-as-a-Judge para evaluación legal.* Se demostró que la evaluación mediante tres jueces LLM (DeepSeek, Grok, Kimi K2) alcanza un acuerdo inter-juez bueno ($alpha = 0.81$) para la métrica de "respuesta correcta", validando su uso como herramienta de evaluación en este dominio.

+ *Metodología replicable y documentada.* La documentación completa de la metodología, las decisiones de diseño y los resultados permite la replicación del sistema para otros cuerpos normativos y jurisdicciones.

Cabe destacar que la contribución principal del trabajo no reside en los valores de desempeño absolutos de los modelos evaluados ---que reflejan el estado de los sistemas disponibles durante el período experimental--- sino en la metodología de evaluación, el benchmark creado y el sistema replicable, que pueden aplicarse sobre cualquier generación futura de modelos.

=== Impacto de la Propuesta

El presente trabajo demuestra la viabilidad técnica de aplicar sistemas Agentic-RAG de código abierto a la consulta de normativa legal argentina. Los resultados confirman que la incorporación de mecanismos de recuperación de información mejora significativamente la calidad de las respuestas de los modelos de lenguaje en el dominio legal, con mejoras que van desde una mediana global de 0.58 (sin RAG) hasta 0.83 (Agentic-RAG) en la evaluación de "respuesta correcta". Cabe precisar que este beneficio es dependiente del modelo y no uniforme. El análisis de efectos simples con corrección de Holm-Bonferroni revela que Agentic-RAG beneficia significativamente a gpt-5-mini (0.92 frente a 0.33 sin RAG, $p_"corr" < 0.0001$) pero degrada a gpt-5-nano frente a RAG básico (0.08 vs. 0.58, $p_"corr" = 0.017$). Para gpt-5, las diferencias entre estrategias no alcanzan significación estadística tras la corrección por comparaciones múltiples ($p_"corr" > 0.05$ en todos los pares). El RAG básico, aunque con una mejora más modesta (mediana global de 0.71), ofrece el beneficio adicional de igualar el desempeño entre modelos de distinta capacidad.

La disponibilidad del código y la metodología como recurso abierto habilita su adaptación por instituciones públicas, organizaciones de la sociedad civil y desarrolladores independientes que busquen mejorar el acceso ciudadano a la información legal. En un contexto donde las herramientas avanzadas de consulta legal son predominantemente comerciales y de acceso restringido, esta contribución tiene el potencial de reducir las barreras de acceso a la normativa para usuarios no especializados.

== Discusión de Resultados

=== Fortalezas del Sistema

El sistema desarrollado presenta las siguientes fortalezas:

+ *Mejora significativa con recuperación.* Tanto el RAG básico como el Agentic-RAG superan significativamente al baseline sin RAG ($p < 0.001$ para Agentic-RAG vs. sin RAG; $p = 0.0066$ para RAG básico vs. sin RAG), confirmando el valor de anclar las respuestas en evidencia documental.

+ *Configuración costo-eficiente viable.* La combinación Agentic-RAG con gpt-5-mini alcanza una media de 0.78 en corrección, comparable al 0.80 de gpt-5, ofreciendo una alternativa práctica para escenarios con restricciones presupuestarias.

+ *Evaluación multidimensional robusta.* La combinación de métricas textuales, semánticas y evaluación por jueces LLM proporciona una visión multidimensional de la calidad, mitigando los sesgos de cada familia de métricas por separado.

+ *Trazabilidad completa.* El sistema de logging registra todas las interacciones entre agentes, herramientas invocadas, fragmentos recuperados y decisiones intermedias, lo que facilita la auditoría y la depuración del sistema.

+ *Análisis estadístico riguroso.* El uso de pruebas no paramétricas justificadas por la verificación de supuestos (Shapiro-Wilk, Kruskal-Wallis, Dunn con Bonferroni, Scheirer-Ray-Hare), complementadas con análisis de efectos simples (Mann-Whitney U con corrección de Holm-Bonferroni y el análisis de acuerdo inter-juez (Krippendorff's alpha), proporcionan una base estadística sólida para las conclusiones.

=== Debilidades y Limitaciones <sec:limitaciones>

El trabajo presenta las siguientes limitaciones que deben considerarse al interpretar los resultados:

+ *Alcance del corpus.* El sistema se limita al Código de Minería Argentino como prueba de concepto, sin incluir otras normativas nacionales, provinciales o municipales. La generalización de los resultados a otros cuerpos normativos requiere validación adicional.

+ *Aproximación de Laplace en el modelo ordinal.* El modelo acumulativo se estimó con `nAGQ = 1` (Laplace) porque `ordinal::clmm` no admite cuadratura adaptativa con más de un término de efectos aleatorios. No se realizó una prueba formal de odds proporcionales. Por ello, el modelo se reporta como análisis de robustez y sus coeficientes no deben interpretarse como estimaciones exactas; la inferencia principal se apoya en las pruebas pareadas y en los intervalos de confianza.

+ *Ausencia de diferencia marginal entre Agentic-RAG y RAG básico.* A nivel global, no se encontró diferencia significativa entre ambas estrategias ($p = 0.383$), aunque el análisis de interacción muestra que esta conclusión enmascara diferencias condicionales al modelo. Este resultado sugiere que, para ciertos modelos, la complejidad adicional del sistema agéntico no se traduce en mejora marginal respecto a un RAG más simple.

+ *Degradación con modelos pequeños.* El sistema Agentic-RAG perjudica el desempeño de gpt-5-nano, lo que constituye una limitación para despliegues con restricciones de costo o en entornos con acceso limitado a modelos de mayor capacidad. El análisis de efectos simples confirma que esta degradación es significativa frente a RAG básico ($p_"corr" = 0.017$, Holm-Bonferroni) pero marginal frente a sin RAG ($p_"corr" = 0.064$).

+ *Confiabilidad insuficiente de la métrica de precisión legal.* La rúbrica `score_precision_legal` no alcanzó niveles aceptables de acuerdo inter-juez en todos los subgrupos ($alpha < 0.667$ en base\_rag y no\_rag), lo que impidió su uso como variable de comparación y limitó la evaluación de la precisión en la citación de artículos.

+ *Benchmark de escala limitada.* Aunque las 79 unidades de evaluación proporcionan una base razonable para la evaluación, un benchmark de mayor escala, con mayor diversidad de tipos de preguntas y grados de dificultad, fortalecería la validez externa de los resultados.

+ *Dependencia de APIs comerciales.* El empleo de modelos GPT-5 a través de APIs de pago introduce una dependencia externa y costos recurrentes que podrían limitar la accesibilidad del sistema en el largo plazo.

+ *Ausencia de evaluación con usuarios reales.* No se realizaron pruebas de usabilidad con usuarios finales (abogados, funcionarios, ciudadanos), por lo que no se cuenta con evidencia directa sobre la utilidad percibida y la experiencia de usuario del sistema.

+ *Alcance temporal de los modelos evaluados.* Los modelos de la familia GPT-5 evaluados corresponden al estado de las APIs disponibles durante el período experimental (segundo semestre de 2025). Modelos posteriores ---en particular modelos de razonamiento (_reasoning models_) lanzados entre fines de 2025 y 2026--- podrían mostrar patrones de comportamiento distintos, especialmente respecto a la sobrecarga agéntica observada en modelos de menor capacidad (gpt-5-nano). La validez de los resultados se circunscribe al conjunto de modelos evaluados.

+ *Revisión humana limitada a la sustantividad y al benchmark.* La revisión de las 87 filas no sustantivas fue realizada por el autor y no constituye una validación humana independiente de la calidad de las respuestas. La única revisión profesional documentada corresponde al benchmark (preguntas y respuestas esperadas) y fue realizada por una sola profesional, sin segunda revisión. Se identificaron 23 discrepancias entre jueces y 17 evaluaciones positivas sobre salidas no sustantivas; se reportan como insumos para una auditoría futura, no como una validación de los jueces.

+ *Ausencia de validación manual de las evaluaciones LLM-as-a-Judge.* Si bien la sección sobre LLM-as-a-judge del marco teórico (capítulo @cap:agentic-rag) plantea la validación manual de una muestra de evaluaciones como estrategia para mitigar sesgos del juez LLM, esta validación no pudo realizarse en la práctica. La cantidad de contenido generado por las nueve configuraciones experimentales (tres estrategias de recuperación $times$ tres modelos de lenguaje) y la falta de disponibilidad de profesionales del derecho con el tiempo necesario para revisar y puntuar manualmente las respuestas impidieron llevar a cabo esta verificación. Como consecuencia, la concordancia entre las evaluaciones automáticas del juez LLM y el criterio de expertos legales no ha sido cuantificada directamente, lo que constituye una limitación importante para la interpretación de los resultados de la evaluación automática. <lim:sin-validacion-manual>

+ *Ausencia de prompting de cadena de pensamiento (CoT) en los jueces LLM.* Aunque el marco teórico menciona el uso de cadenas de pensamiento como estrategia para reducir sesgos superficiales en la evaluación, los prompts empleados en la implementación práctica no incluyen instrucciones explícitas de razonamiento paso a paso. El análisis del código de evaluación (archivo `01_llm_as_a_judge.ipynb`) revela que los prompts se limitan a presentar la rúbrica con criterios y puntajes, solicitando una justificación textual del puntaje asignado mediante el parámetro `include_reason=True`, pero sin requerir una cadena de razonamiento estructurada antes de emitir la calificación. Esta omisión podría incrementar la susceptibilidad de los jueces a sesgos como el de posición o verbosidad, particularmente en los modelos DeepSeek-V3 y Kimi K2 0905 que no poseen capacidad de razonamiento nativa. Solo Grok 4.1 Fast cuenta con un modo de razonamiento nativo que podría haberse activado explícitamente. <lim:sin-cot>

== Trabajos Futuros

A partir de las limitaciones identificadas y los resultados obtenidos, se proponen las siguientes líneas de investigación futuras:

=== Extensión del Corpus Legal

La extensión natural del trabajo consiste en ampliar el corpus más allá del Código de Minería para incluir la totalidad de la normativa nacional disponible en Infoleg. Esto implicaría abordar desafíos adicionales como la heterogeneidad de formatos, la mayor profundidad de las estructuras jerárquicas y el volumen significativamente mayor de documentos. En una etapa posterior, podría incorporarse normativa provincial y municipal, así como jurisprudencia, doctrina y dictámenes.

=== Mejoras en la Arquitectura

Se identifican varias oportunidades de mejora en la arquitectura del sistema:

- *Políticas adaptativas de complejidad agéntica.* Un agente clasificador que determine la complejidad de la consulta podría decidir dinámicamente si emplear RAG básico o Agentic-RAG, evitando la sobrecarga agéntica para consultas simples y modelos de menor capacidad.

- *Recuperación híbrida.* La combinación de búsqueda vectorial con búsqueda léxica (BM25) y búsqueda sobre grafos de conocimiento podría mejorar la cobertura de la recuperación, especialmente para consultas que requieren coincidencias exactas de términos legales o razonamiento sobre relaciones entre normas.

- *Modelos de embeddings especializados.* El entrenamiento o ajuste fino de modelos de embeddings sobre texto jurídico argentino podría mejorar la calidad de la recuperación semántica, dado que los modelos de propósito general pueden no capturar adecuadamente los matices del lenguaje legal.

- *Modelos de lenguaje de código abierto.* La evaluación de modelos de lenguaje de código abierto (por ejemplo, de las familias Llama, Mistral o Qwen) permitiría reducir la dependencia de APIs comerciales y facilitar el despliegue local, relevante para entornos donde la confidencialidad de las consultas sea un requisito.

=== Ampliación del Benchmark

El benchmark podría ampliarse en varias direcciones:

- Incrementar el número de preguntas y la diversidad de tipos (factoides, multi-salto, comparativas, hipotéticas).
- Incluir preguntas de mayor dificultad que requieran razonamiento sobre múltiples artículos o cuerpos normativos.
- Desarrollar rúbricas más específicas para la evaluación de precisión legal, incorporando anclas de dominio que mejoren el acuerdo inter-juez.
- Incorporar la evaluación de la capacidad de abstención del sistema (es decir, su habilidad para reconocer cuando no tiene información suficiente para responder).

=== Integración con Sistemas Existentes

La integración del sistema con plataformas como Infoleg o SAIJ permitiría acceder a información actualizada de manera automática y ofrecer una interfaz de consulta más completa. Asimismo, la integración con grafos de conocimiento que modelen las relaciones entre normas (derogaciones, modificaciones, referencias cruzadas) habilitaría un razonamiento más profundo sobre la estructura del ordenamiento jurídico.

=== Evaluación con Usuarios Reales

Una línea de trabajo complementaria consiste en la realización de estudios de usabilidad con usuarios finales, incluyendo profesionales del derecho, funcionarios públicos y ciudadanos sin formación jurídica. Estos estudios permitirían evaluar la utilidad percibida del sistema, identificar patrones de uso y necesidades no cubiertas, y ajustar la interfaz y las respuestas del sistema a las expectativas de los distintos perfiles de usuario.

=== Optimización del Entrenamiento con Aprendizaje por Refuerzo

Los avances recientes en optimización de políticas Agentic-RAG mediante aprendizaje por refuerzo con supervisión de proceso (como RAG-Gym, ReasonRAG y TreePS-RAG) abren la posibilidad de entrenar agentes que aprendan a seleccionar estrategias de recuperación óptimas para cada tipo de consulta, superando las políticas manuales basadas en prompts empleadas en este trabajo.

=== Re-evaluación sobre Modelos de Nueva Generación

La velocidad de iteración en el desarrollo de LLMs hace deseable repetir el diseño experimental sobre modelos lanzados después del período de estudio, especialmente modelos de razonamiento que integran cadenas de pensamiento explícitas (_chain-of-thought_). Estos modelos podrían alterar la dinámica de interacción estrategia × modelo documentada en este trabajo, en particular reduciendo o eliminando la degradación observada en el modo Agentic-RAG con modelos de menor capacidad. La metodología de evaluación propuesta ---diseño factorial, benchmark específico y validación mediante LLM-as-a-Judge--- es directamente aplicable a futuras generaciones de modelos sin modificaciones sustanciales.

== Reflexiones Finales

El presente trabajo demuestra que los sistemas de Generación Aumentada por Recuperación Agéntica constituyen una herramienta viable para mejorar el acceso a la normativa legal argentina. La combinación de modelos de lenguaje con mecanismos de recuperación semántica y agentes especializados permite generar respuestas más precisas y contextualizadas que las obtenidas por modelos sin acceso a información externa.

El hallazgo de la interacción significativa entre la estrategia de recuperación y el modelo de lenguaje subraya la importancia de un enfoque integral en el diseño de estos sistemas: la selección de una estrategia de recuperación no puede realizarse de manera independiente del modelo que la utilizará. El análisis de efectos simples con corrección de Holm-Bonferroni confirma que Agentic-RAG beneficia significativamente a gpt-5-mini pero degrada a gpt-5-nano frente a RAG básico, mientras que para gpt-5 no se detectan diferencias significativas entre estrategias. Este resultado es transferible a otros dominios y aplicaciones de RAG, y constituye un aporte al entendimiento de cómo interactúan los componentes de estos sistemas.

La publicación del código, la metodología y el benchmark como recursos abiertos busca facilitar que otros investigadores, instituciones y desarrolladores puedan replicar, adaptar y mejorar el sistema para otras normativas y jurisdicciones. En un país donde el acceso a herramientas avanzadas de consulta legal permanece en gran medida restringido a plataformas comerciales, la disponibilidad de una alternativa abierta y documentada representa un paso concreto hacia la democratización del acceso a la información legal.

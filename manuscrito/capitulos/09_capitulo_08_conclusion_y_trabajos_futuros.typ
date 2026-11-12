= Conclusiones y Trabajos Futuros

== Introducción

El presente trabajo se propuso diseñar, implementar y evaluar un sistema de Generación Aumentada por Recuperación Agéntica (Agentic-RAG) de código abierto para la consulta de normativa argentina, utilizando el Código de Minería Argentino como prueba de concepto. A lo largo de los capítulos precedentes se presentaron los fundamentos teóricos de modelos de lenguaje, sistemas RAG, arquitecturas agénticas y Agentic-RAG; se describió la metodología y el diseño del sistema multi-agente; se detalló la implementación del prototipo completo ---desde la extracción de datos hasta el pipeline de evaluación---; y se analizaron los resultados experimentales mediante un diseño factorial de 3 estrategias de recuperación × 3 modelos de lenguaje, evaluados con métricas textuales, semánticas y evaluación LLM-as-a-Judge.

Este capítulo sintetiza los hallazgos principales, revisa el cumplimiento de los objetivos planteados, discute las fortalezas y limitaciones del trabajo y propone líneas de investigación futuras.

== Conclusiones

=== Cumplimiento de Objetivos

El trabajo planteó cuatro objetivos específicos, cuyo grado de cumplimiento se detalla a continuación:

+ *Desarrollar una base de datos vectorial del Código de Minería Argentino diseñada específicamente para trabajar con sistemas RAG.* Este objetivo se cumplió en lo funcional. Se implementó una base de datos vectorial en Milvus con embeddings de 768 dimensiones generados por el modelo `hiiamsid/sentence_similarity_spanish_es`, empleando una estrategia de segmentación basada en la estructura natural del documento legal (un artículo por fragmento). El índice `AUTOINDEX` con similitud coseno permite búsquedas semánticas eficientes sobre el corpus del Código de Minería.

+ *Desarrollar un sistema de agentes de inteligencia artificial para que trabajen de manera conjunta con el sistema RAG.* Este objetivo se cumplió parcialmente. Se implementó una arquitectura multi-agente acotada mediante Pydantic AI, con dos agentes activos: el Agente Especialista Legal (generación de respuestas) y el Agente de Recuperación (descomposición de consultas y búsqueda vectorial). El Agente de Calidad de Recuperación fue diseñado, pero se excluyó por razones de costo y complejidad y no participó en la configuración experimental. El especialista realiza una delegación nominal de recuperación; no hay iteración del especialista ni verificación automática de la respuesta. En consecuencia, el objetivo se cumple respecto de la coordinación entre recuperación y generación, pero no respecto de un ciclo completo de verificación multi-agente.

+ *Desarrollar un benchmark específico para el Código de Minería Argentino para evaluar el desempeño del sistema.* Este objetivo se cumplió. Se generó un benchmark de 25 preguntas tipo caso de estudio legal (76 subpreguntas explícitas más 3 preguntas evaluadas como unidad única, totalizando 79 unidades de evaluación), distribuidas entre los títulos del Código de Minería, con respuestas esperadas generadas por GPT-4.1 y revisadas por una profesional del derecho argentino. El benchmark fue empleado como instrumento de evaluación en las nueve configuraciones experimentales; no hubo una segunda revisión independiente.

+ *Cargar el código y una descripción de la metodología a un repositorio abierto para que cualquier organización, empresa o individuo pueda replicar y adaptar el sistema a otras normativas.* Este objetivo se cumplió. El código fue organizado en módulos independientes (notebooks) con documentación técnica en cada directorio, siguiendo el flujo del pipeline experimental, y se publicó en un repositorio público de GitHub.

=== Contribuciones del Trabajo

Las principales contribuciones del presente trabajo son:

+ *Sistema Agentic-RAG de código abierto, con alcance acotado.* Se desarrolló un prototipo que integra recuperación semántica, base vectorial y dos agentes activos. No es un planificador autónomo ni un ciclo iterativo de verificación: el especialista delega una recuperación y redacta con los documentos devueltos. El Agente de Calidad no se ejecutó. No se identificaron antecedentes públicos comparables para normativa argentina en la búsqueda realizada.

+ *Benchmark para el Código de Minería Argentino.* Se creó un benchmark de 25 casos y 79 unidades, con revisión por una profesional. La versión experimental v1 se conserva congelada. Una revisión posterior asistida por IA detectó posibles errores que requieren una nueva revisión profesional; las correcciones se documentan como v2 y no se aplicaron retroactivamente. El benchmark es un instrumento de investigación, no una validación psicométrica ni jurídica definitiva.

+ *Evidencia empírica sobre la interacción estrategia × modelo.* El análisis apareado muestra que el efecto de la estrategia depende del modelo del especialista (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). En el escenario principal, Agentic-RAG es inferior a RAG básico en gpt-5-nano, superior en gpt-5-mini y moderadamente superior en gpt-5. La interacción es robusta a los escenarios de sensibilidad y a los tres jueces, pero no identifica un componente causal único.

+ *Caracterización de un modo de fallo de respuesta.* En Agentic-RAG con gpt-5-nano, 41/79 salidas no fueron sustantivas; cuando respondió, la calidad fue alta (38/79; media 0,820; mediana 0,958). Los logs muestran recuperación y tokens, sin truncamiento por longitud. El hallazgo es descriptivo; no se atribuye a la “complejidad agéntica” sin réplicas ni ablaciones.

+ *Límites de la hipótesis de igualación por RAG básico.* Con RAG básico, las diferencias observadas entre modelos son menores, pero no desaparecen: las estimaciones son positivas y los intervalos no definen equivalencia. La conclusión anterior basada en un p de Kruskal–Wallis no significativo debe retirarse.

+ *Confiabilidad inter-juez, no validación.* Los tres jueces alcanzaron un acuerdo ordinal global bueno para corrección (α = 0,807842 con valores originales; 0,799542 con transformación a rúbrica), verificado de forma independiente en `verificacion-analisis-estadistico/`. No se compararon con criterio humano ni existen calificaciones humanas de las respuestas; la revisión humana del benchmark es la referencia del instrumento, no una validación de los jueces. Se identificaron 23 discrepancias entre jueces y 17 evaluaciones positivas sobre salidas no sustantivas. La rúbrica de precisión legal no alcanzó confiabilidad suficiente en todos los sistemas.

+ *Metodología de evaluación y artefactos abiertos.* El modelo ordinal mixto con interceptos por caso y unidad, los escenarios de fallo, los efectos simples con IC, el análisis de costos por respuesta correcta (≥ 0,75) y la publicación de código, logs y evaluaciones permiten auditar el análisis. El acceso público está verificado; la clonación y ejecución se recomiendan como verificación de reproducibilidad.

Cabe destacar que la contribución principal del trabajo no reside en los valores de desempeño absolutos de los modelos evaluados ---que reflejan el estado de los sistemas disponibles durante el período experimental--- sino en la metodología de evaluación, el benchmark creado y el sistema replicable, que pueden aplicarse sobre cualquier generación futura de modelos.

=== Impacto de la Propuesta

El trabajo muestra la viabilidad técnica de un prototipo Agentic-RAG de código abierto para consultar el Código de Minería Argentino, pero no demuestra una superioridad general de la recuperación agéntica. En gpt-5-mini, RAG básico y Agentic-RAG presentaron diferencias positivas frente a Sin RAG; en gpt-5, Agentic-RAG presentó una diferencia positiva frente a ambas referencias; en gpt-5-nano, Agentic-RAG presentó una diferencia negativa en la utilidad del sistema porque 41/79 salidas no fueron sustantivas. No hay una recomendación universal: la elección de estrategia y modelo debe hacerse conjuntamente y con un objetivo explícito de calidad y costo. La disponibilidad del código y la metodología habilita su adaptación, pero no demuestra adopción, impacto social ni transferencia a otros dominios.

La disponibilidad del código y la metodología como recurso abierto habilita su adaptación por instituciones públicas, organizaciones de la sociedad civil y desarrolladores independientes que busquen mejorar el acceso ciudadano a la información legal. En un contexto donde las herramientas avanzadas de consulta legal son predominantemente comerciales y de acceso restringido, esta contribución tiene el potencial de reducir las barreras de acceso a la normativa para usuarios no especializados.

== Discusión de Resultados

=== Fortalezas del Sistema

El sistema desarrollado presenta las siguientes fortalezas:

+ *Diseño factorial y benchmark propio.* El estudio compara tres estrategias de recuperación y tres modelos sobre las mismas 79 unidades, con un benchmark específico para el Código de Minería. El diseño permite examinar la interacción entre estrategia y modelo y no solo efectos marginales.

+ *Mejora condicionada al modelo.* En gpt-5-mini, ambas estrategias de recuperación presentaron diferencias positivas frente a Sin RAG (+0,363 para RAG básico; +0,513 para Agentic-RAG). En gpt-5, Agentic-RAG presentó una diferencia positiva moderada frente a RAG básico (+0,106; IC 95 % 0,054 a 0,155) y frente a Sin RAG (+0,095). En gpt-5-nano, Agentic-RAG presentó un modo de fallo de respuesta. No se sostiene la afirmación de que la recuperación mejore el desempeño con independencia del modelo.

+ *Alternativa no dominada de costo-calidad.* Agentic-RAG con gpt-5-mini ofrece una media de 0,788 a USD 0,0564 por consulta, frente a 0,812 y USD 0,0792 de Agentic-RAG con gpt-5. La diferencia de calidad entre ambas no es concluyente; la de gpt-5-mini es una alternativa razonable cuando se prioriza calidad alta con menor costo, no la opción más barata.

+ *Trazabilidad y auditabilidad.* Los logs de los agentes, las respuestas, las métricas y las evaluaciones de los jueces están disponibles para auditoría. Los registros no incluyen el payload HTTP completo ni el esfuerzo de razonamiento efectivo.

+ *Análisis inferencial adecuado al diseño.* El modelo ordinal mixto con interceptos por caso y unidad, la prueba de razón de verosimilitud para la interacción, las pruebas pareadas de Friedman y Wilcoxon y el bootstrap por casos respetan el apareamiento y el anidamiento. Los efectos se reportan con intervalos de confianza y las comparaciones múltiples se corrigen con Holm dentro de familias predefinidas. El acuerdo inter-juez se mide con el alpha de Krippendorff, que cuantifica confiabilidad y no validez.

=== Debilidades y Limitaciones <sec:limitaciones>

El trabajo presenta las siguientes limitaciones que deben considerarse al interpretar los resultados:

+ *Alcance del corpus.* El sistema se limita al Código de Minería Argentino como prueba de concepto, sin incluir otras normativas nacionales, provinciales o municipales. La generalización de los resultados a otros cuerpos normativos requiere validación adicional.

+ *Aproximación de Laplace en el modelo ordinal.* El modelo acumulativo es el análisis principal y se estimó con `nAGQ = 1` (Laplace) porque `ordinal::clmm` no admite cuadratura adaptativa con más de un término de efectos aleatorios. No se realizó una prueba formal del supuesto de odds proporcionales. La aproximación se declara como limitación de la estimación, no se corrige con otra especificación y no convierte al modelo en un análisis secundario. Las pruebas de Friedman, Wilcoxon y el bootstrap por casos se reportan como sensibilidad no paramétrica del modelo principal, no como la inferencia de referencia.

+ *No se demostró una superioridad global de Agentic-RAG.* El efecto depende del modelo: es negativo en gpt-5-nano, positivo en gpt-5-mini y moderado en gpt-5. No corresponde reportar un efecto marginal único ni usar la falta de significación de una comparación marginal como prueba de equivalencia: el promedio entre modelos con efectos de signo opuesto no tiene interpretación sustantiva.

+ *Modo de fallo de respuesta en Agentic-RAG con gpt-5-nano.* La celda produjo 41/79 salidas no sustantivas (27 vacías, 1 con solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas), pese a que los logs registran recuperación y tokens de salida. Cuando respondió, la calidad fue alta (38/79; media 0,820; mediana 0,958). Bajo el escenario principal, la diferencia frente a RAG básico es −0,270 (IC 95 % −0,330 a −0,202; $p_"Holm" = 3,25 times 10^(-14)$) y frente a Sin RAG es −0,242 (IC 95 % −0,307 a −0,176). El resultado es una limitación para despliegues con restricciones de costo, pero no hay evidencia para atribuir el fallo a la “complejidad agéntica”: no se realizaron réplicas ni ablaciones.

+ *Confiabilidad insuficiente de la métrica de precisión legal.* La rúbrica `score_precision_legal` no alcanzó niveles aceptables de acuerdo inter-juez en todos los subgrupos ($alpha < 0.667$ en base\_rag y no\_rag), lo que impidió su uso como variable de comparación y limitó la evaluación de la precisión en la citación de artículos.

+ *Benchmark de escala limitada.* Aunque las 79 unidades de evaluación proporcionan una base razonable para la evaluación, un benchmark de mayor escala, con mayor diversidad de tipos de preguntas y grados de dificultad, fortalecería la validez externa de los resultados.

+ *Dependencia de APIs comerciales.* El empleo de modelos GPT-5 a través de APIs de pago introduce una dependencia externa y costos recurrentes que podrían limitar la accesibilidad del sistema en el largo plazo.

+ *Ausencia de evaluación con usuarios reales.* No se realizaron pruebas de usabilidad con usuarios finales (abogados, funcionarios, ciudadanos), por lo que no se cuenta con evidencia directa sobre la utilidad percibida y la experiencia de usuario del sistema.

+ *Alcance temporal y de configuración.* Los modelos de la familia GPT-5 evaluados corresponden al estado de las APIs disponibles durante el período experimental (segundo semestre de 2025). El recuperador fue siempre gpt-5; la corrida de gpt-5 usó siete búsquedas y las de mini y nano seis. El modo de fallo de gpt-5-nano podría cambiar con otros modelos o configuraciones, pero no se atribuye a una propiedad estable de “los modelos pequeños”. La validez de los resultados se circunscribe al conjunto de modelos y configuraciones evaluados.

+ *Revisión humana limitada a la sustantividad y al benchmark.* La revisión de las 87 filas no sustantivas fue realizada por el autor y no constituye una validación humana independiente de la calidad de las respuestas. La única revisión profesional documentada corresponde al benchmark (preguntas y respuestas esperadas) y fue realizada por una sola profesional, sin segunda revisión. Se identificaron 23 discrepancias entre jueces y 17 evaluaciones positivas sobre salidas no sustantivas; se reportan como insumos para una auditoría futura, no como una validación de los jueces.

+ *Ausencia de validación manual de las evaluaciones LLM-as-a-Judge.* Si bien la sección sobre LLM-as-a-judge del marco teórico (#ref(<cap:agentic-rag>, supplement: [Capítulo])) plantea la validación manual de una muestra de evaluaciones como estrategia para mitigar sesgos del juez LLM, esta validación no pudo realizarse en la práctica. La cantidad de contenido generado por las nueve configuraciones experimentales (tres estrategias de recuperación $times$ tres modelos de lenguaje) y la falta de disponibilidad de profesionales del derecho con el tiempo necesario para revisar y puntuar manualmente las respuestas impidieron llevar a cabo esta verificación. Como consecuencia, la concordancia entre las evaluaciones automáticas del juez LLM y el criterio de expertos legales no ha sido cuantificada directamente, lo que constituye una limitación importante para la interpretación de los resultados de la evaluación automática. <lim:sin-validacion-manual>

+ *Ausencia de prompting de cadena de pensamiento (CoT) en los jueces LLM.* Aunque el marco teórico menciona el uso de cadenas de pensamiento como estrategia para reducir sesgos superficiales en la evaluación, los prompts empleados en la implementación práctica no incluyen instrucciones explícitas de razonamiento paso a paso. El análisis del código de evaluación (archivo `01_llm_as_a_judge.ipynb`) revela que los prompts se limitan a presentar la rúbrica con criterios y puntajes, solicitando una justificación textual del puntaje asignado mediante el parámetro `include_reason=True`, pero sin requerir una cadena de razonamiento estructurada antes de emitir la calificación. Esta omisión podría incrementar la susceptibilidad de los jueces a sesgos como el de posición o verbosidad, particularmente en los modelos DeepSeek-V3 y Kimi K2 0905 que no poseen capacidad de razonamiento nativa. Solo Grok 4.1 Fast cuenta con un modo de razonamiento nativo que podría haberse activado explícitamente. <lim:sin-cot>

+ *Ejecución única y ausencia de control efectivo de muestreo.* Se realizó una única ejecución por unidad y configuración, sin réplicas. El código solicitó `temperature=0.0`, pero Pydantic AI 1.1.0 elimina ese parámetro para los modelos GPT-5 antes de construir la solicitud, y no se registró el esfuerzo de razonamiento. No puede afirmarse determinismo ni estimarse la variabilidad entre corridas, de modo que los efectos estimados describen esta ejecución y no una distribución de resultados posibles.

+ *Tratamiento de las respuestas no sustantivas como decisión normativa.* El escenario principal imputa cero a las salidas no sustantivas porque mide la utilidad del sistema completo; la exclusión mide la calidad condicional a que el sistema responda y la sensibilidad con puntajes observados audita a los jueces. Ninguna de las tres es “la” medición de calidad jurídica: la elección del escenario es una decisión sobre qué se quiere evaluar y se reporta completa para que el lector pueda adoptar otra.

+ *Factores confundidos y ausencia de ablaciones.* En Agentic-RAG cambian simultáneamente el prompt, la descomposición de la consulta, el número de candidatos recuperados, la selección de fragmentos, el modelo recuperador y el presupuesto de búsquedas. Sin ablaciones no puede atribuirse el efecto a uno de esos componentes. La asimetría de presupuesto de búsqueda (siete en gpt-5, seis en mini y nano) agrega una amenaza específica al contraste entre modelos.

+ *Costos históricos y ausencia de costos de producción.* Los costos reportados son los registrados durante el experimento con los precios de API del período (USD 22,2939 en total) y corresponden al consumo de tokens. No incluyen latencia, infraestructura, mantenimiento, interfaz ni costos humanos, y no se extrapolan a precios actuales ni a un despliegue en producción.

+ *Réplicas y ablaciones como límite de las estimaciones.* El modelo ordinal mixto separa la variabilidad entre unidades y casos, pero no la variabilidad entre ejecuciones del mismo modelo. Las estimaciones de esta tesis no permiten afirmar estabilidad entre corridas ni separar el efecto de la estrategia de la variabilidad del proveedor; las réplicas y la sustitución controlada del recuperador quedan como trabajo futuro.

== Trabajos Futuros

A partir de las limitaciones identificadas y los resultados obtenidos, se proponen las siguientes líneas de investigación futuras:

=== Extensión del Corpus Legal

La extensión natural del trabajo consiste en ampliar el corpus más allá del Código de Minería para incluir la totalidad de la normativa nacional disponible en Infoleg. Esto implicaría abordar desafíos adicionales como la heterogeneidad de formatos, la mayor profundidad de las estructuras jerárquicas y el volumen significativamente mayor de documentos. En una etapa posterior, podría incorporarse normativa provincial y municipal, así como jurisprudencia, doctrina y dictámenes.

=== Mejoras en la Arquitectura

Se identifican varias oportunidades de mejora en la arquitectura del sistema:

- *Políticas adaptativas de complejidad.* Un agente clasificador podría decidir dinámicamente si emplear RAG básico o Agentic-RAG según la consulta y el modelo, con el objetivo de reducir la tasa de respuestas no sustantivas y evitar configuraciones con mal costo por respuesta correcta. La política debería evaluarse con réplicas y una métrica de fallo.

- *Recuperación híbrida.* La combinación de búsqueda vectorial con búsqueda léxica (BM25) y búsqueda sobre grafos de conocimiento podría mejorar la cobertura de la recuperación, especialmente para consultas que requieren coincidencias exactas de términos legales o razonamiento sobre relaciones entre normas.

- *Modelos de embeddings especializados.* El entrenamiento o ajuste fino de modelos de embeddings sobre texto jurídico argentino podría mejorar la calidad de la recuperación semántica, dado que los modelos de propósito general pueden no capturar adecuadamente los matices del lenguaje legal.

- *Modelos de lenguaje de código abierto.* La evaluación de modelos de lenguaje de código abierto (por ejemplo, de las familias Llama, Mistral o Qwen) permitiría reducir la dependencia de APIs comerciales y facilitar el despliegue local, relevante para entornos donde la confidencialidad de las consultas sea un requisito.

=== Ampliación del Benchmark

El benchmark podría ampliarse en varias direcciones:

- Incrementar el número de preguntas y la diversidad de tipos (factoides, multi-salto, comparativas, hipotéticas).
- Incluir preguntas de mayor dificultad que requieran razonamiento sobre múltiples artículos o cuerpos normativos.
- Desarrollar rúbricas más específicas para la evaluación de precisión legal, incorporando anclas de dominio que mejoren el acuerdo inter-juez.
- Incorporar la evaluación de la capacidad de abstención del sistema (es decir, su habilidad para reconocer cuando no tiene información suficiente para responder).

=== Evaluación Determinista de Citas

El marco teórico identifica la citación incorrecta o inexistente como el riesgo central de los sistemas de consulta legal. Esta tesis no midió ese riesgo de forma determinista: no se calculó la precisión ni la exhaustividad de las citas de las 711 respuestas, ni la tasa de artículos citados que no existen en el corpus. La evaluación de citas quedó limitada a la rúbrica `score_precision_legal` de los jueces, que además no alcanzó confiabilidad suficiente. Una línea de trabajo inmediata consiste en extraer automáticamente las citas de cada respuesta, contrastarlas contra los 398 nodos de artículo del corpus y reportar precisión, exhaustividad, F1 y tasa de citas inexistentes, de forma independiente de los jueces. Ese cálculo no requiere nuevas corridas: puede ejecutarse sobre las respuestas ya registradas.

=== Integración con Sistemas Existentes

La integración del sistema con plataformas como Infoleg o SAIJ permitiría acceder a información actualizada de manera automática y ofrecer una interfaz de consulta más completa. Asimismo, la integración con grafos de conocimiento que modelen las relaciones entre normas (derogaciones, modificaciones, referencias cruzadas) habilitaría un razonamiento más profundo sobre la estructura del ordenamiento jurídico.

=== Evaluación con Usuarios Reales

Una línea de trabajo complementaria consiste en la realización de estudios de usabilidad con usuarios finales, incluyendo profesionales del derecho, funcionarios públicos y ciudadanos sin formación jurídica. Estos estudios permitirían evaluar la utilidad percibida del sistema, identificar patrones de uso y necesidades no cubiertas, y ajustar la interfaz y las respuestas del sistema a las expectativas de los distintos perfiles de usuario.

=== Optimización del Entrenamiento con Aprendizaje por Refuerzo

Los avances recientes en optimización de políticas Agentic-RAG mediante aprendizaje por refuerzo con supervisión de proceso (como RAG-Gym, ReasonRAG y TreePS-RAG) abren la posibilidad de entrenar agentes que aprendan a seleccionar estrategias de recuperación óptimas para cada tipo de consulta, superando las políticas manuales basadas en prompts empleadas en este trabajo.

=== Re-evaluación sobre Modelos de Nueva Generación

La velocidad de iteración en el desarrollo de LLMs hace deseable repetir el diseño experimental sobre modelos lanzados después del período de estudio, especialmente modelos de razonamiento que integran cadenas de pensamiento explícitas (_chain-of-thought_). Estos modelos podrían alterar la dinámica de interacción estrategia × modelo documentada en este trabajo, en particular reduciendo o eliminando el modo de fallo de respuesta observado en Agentic-RAG con gpt-5-nano. La metodología de evaluación propuesta ---diseño factorial, benchmark específico, modelo ordinal mixto, análisis de costos por respuesta correcta y acuerdo inter-juez como medida de confiabilidad--- es aplicable a futuras generaciones de modelos, pero no sustituye la validación con jueces humanos.

== Reflexiones Finales

El presente trabajo demuestra que los sistemas de Generación Aumentada por Recuperación Agéntica constituyen una herramienta viable para mejorar el acceso a la normativa legal argentina. La combinación de modelos de lenguaje con mecanismos de recuperación semántica y agentes especializados permite generar respuestas más precisas y contextualizadas que las obtenidas por modelos sin acceso a información externa.

El hallazgo de la interacción entre la estrategia de recuperación y el modelo del especialista subraya la importancia de un enfoque integral: la selección de una estrategia no puede realizarse de manera independiente del modelo que la utilizará. El análisis apareado confirma que Agentic-RAG es inferior a RAG básico en gpt-5-nano, superior en gpt-5-mini y moderadamente superior en gpt-5. El resultado corresponde a un corpus, 25 casos, una ejecución por celda y un recuperador fijo; no se demostró transferencia a otros dominios ni una propiedad general de Agentic-RAG.

La publicación del código, la metodología y el benchmark como recursos abiertos busca facilitar que otros investigadores, instituciones y desarrolladores puedan replicar, adaptar y mejorar el sistema para otras normativas y jurisdicciones. En un país donde el acceso a herramientas avanzadas de consulta legal permanece en gran medida restringido a plataformas comerciales, la disponibilidad de una alternativa abierta y documentada representa un paso concreto hacia la democratización del acceso a la información legal.

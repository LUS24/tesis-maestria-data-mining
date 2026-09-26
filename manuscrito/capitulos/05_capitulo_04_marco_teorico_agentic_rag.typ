= Agentic-RAG: Generación Aumentada por Recuperación Agéntica <cap:agentic-rag>

#import "@preview/tablem:0.3.0": three-line-table
#import "../formato.typ": pagina-apaisada

Este capítulo presenta el marco teórico de Agentic-RAG, describiendo sus conceptos fundamentales, arquitecturas, patrones de flujo de trabajo, agentes especializados, casos de uso prácticos y consideraciones de ingeniería.

== Concepto de Agentic-RAG

La Generación Aumentada por Recuperación (RAG) es una técnica que combina un sistema de búsqueda (recuperador) con un modelo de lenguaje grande (LLM) para generar respuestas fundamentadas en información externa, en lugar de depender únicamente del conocimiento que el modelo aprendió durante su entrenamiento. El recuperador busca documentos relevantes en una base de conocimiento y el modelo los utiliza como contexto para responder. Agentic-RAG extiende esta idea al dotar al sistema de un planificador que decide de manera autónoma cuándo y cómo buscar información, permitiendo una recuperación iterativa y un razonamiento en múltiples pasos @mishra2026sok.

Frente a RAG tradicional, donde la recuperación es un preprocesamiento estático _retrieve-then-read_, Agentic-RAG convierte al LLM en un agente que decide qué acciones realizar (por ejemplo, buscar, reformular la consulta, consultar otra base, usar un grafo, etc.), cuándo iterar y cuándo detenerse. Esta autonomía permite adaptar la estrategia de recuperación a la complejidad de la tarea y del entorno, reduciendo ruido, mejorando la cobertura y habilitando flujos de trabajo complejos @ferrazzi2026worth @shorten2024weaviate.

== Arquitecturas de Agentic-RAG

=== De RAG clásico a Agentic-RAG

En RAG clásico, la arquitectura se suele modelar como dos módulos: _Retriever_ (vector search, BM25, etc.) y _Generator_ (LLM) unidos en un pipeline estático de una sola pasada. Varios trabajos muestran que esta arquitectura sufre cuando las consultas son multi-hop, requieren desambiguación, o necesitan combinar múltiples fuentes heterogéneas @singh2025agentic @xiong2025raggym @mishra2026sok.

Agentic-RAG introduce un tercer componente central: un _Planner/Controller_ que convierte el pipeline en un proceso de decisión secuencial, donde cada paso puede desencadenar nuevas acciones de búsqueda, filtrado, verificación o reformulación. Este bucle de planificación-acción-observación se formaliza como un proceso de decisión parcialmente observable de horizonte finito (POMDP, por sus siglas en inglés _Partially Observable Markov Decision Process_) en el estudio de conocimiento (del inglés _Systematization of Knowledge_, SoK) "Agentic Retrieval-Augmented Generation" @mishra2026sok.

#figure(
  align(center, image("../media/diag_base_rag.svg", width: 80%)),
  caption: [Arquitectura básica de RAG clásico.],
) <fig:rag-base>

=== Descomposición modular típica

La literatura reciente propone una descomposición modular de Agentic-RAG en al menos cuatro subsistemas @singh2025agentic @mishra2026sok:

- *Planner / Policy Controller:* decide la siguiente acción (por ejemplo, llamar a una herramienta de búsqueda, leer un fragmento, cambiar de base de conocimiento, pedir verificación, etc.).

- *Motor de Recuperación (Retrieval Engine):* deja de ser un simple filtro pasivo y pasa a actuar como coprocesador lógico, combinando índices densos, dispersos, bases SQL y grafos de conocimiento mediante interfaces programables @mishra2026sok.

- *Memoria / Estado:* almacena trayectoria de acciones, evidencias recuperadas, hipótesis intermedias y feedback del usuario o de otros agentes @bandara2025practical @singh2025agentic.

- *Ejecutor de Herramientas / Entorno:* encapsula APIs externas (web search, bases vectoriales, bases relacionales, calculadoras, simuladores, etc.) y devuelve observaciones al agente @achanta2025ieee @shorten2024weaviate.

=== Patrones de flujo de trabajo agéntico aplicados a RAG

La revisión bibliográfica de Agentic-RAG identifica varios patrones de flujos de trabajo agénticos reutilizados dentro de arquitecturas RAG @singh2025agentic:

- *Encadenamiento de instrucciones (_prompt chaining_):* secuencia de pasos donde salidas intermedias se convierten en entradas del siguiente (por ejemplo, reformular consulta $arrow$ recuperar $arrow$ agrupar $arrow$ generar respuesta).

- *Enrutamiento (_routing_):* un agente clasificador deriva la consulta a distintos sub-flujos especializados (por ejemplo, factual simple vs. multi-salto vs. cálculo numérico) @singh2025agentic.

- *Paralelización (_parallelization_):* ejecución concurrente de múltiples recuperadores o agentes sobre variantes de la consulta, seguida de agregación @singh2025agentic.

- *Orquestador--Trabajadores (_orchestrator--workers_):* un orquestador central descompone la tarea en subtareas y asigna a agentes trabajadores especializados (por ejemplo, agente de búsqueda web, de grafo, de base SQL) @salve2024multiagent @singh2025agentic.

- *Evaluador--Optimizador (_evaluator--optimizer_):* un evaluador (a menudo otro LLM) juzga la calidad de la evidencia y la respuesta, y un optimizador ajusta instrucciones, rutas o políticas @xiong2025raggym @singh2025agentic.

Estos patrones se implementan en marcos de trabajo como LangGraph, AutoGen o Hugging Face Agents, que proporcionan nodos y aristas para describir estados y transiciones del flujo de trabajo @achanta2025ieee @singh2025agentic.

#figure(
  align(center, image("../media/diag_agentic_rag.svg", width: 80%)),
  caption: [Arquitectura de Agentic-RAG con componentes agénticos.],
) <fig:rag-agentic>

=== Arquitecturas jerárquicas y multi-herramienta

#cite(<du2026arag>, form: "prose") propone una arquitectura de Agentic-RAG basada en *interfaces de recuperación jerárquicas* expuestas directamente al modelo. Define tres herramientas de recuperación: _keyword search_, _semantic search_ y _chunk read_, que el agente aprende a combinar de forma adaptativa según la tarea, escalando en tamaño de modelo y cómputo de inferencia.

Esta idea generaliza al concepto de *múltiples herramientas de recuperación*: el agente puede elegir entre distintos índices (vectorial, BM25, grafos, SQL) y granularidades (documento, sección, párrafo, frase), lo que le permite navegar un espacio de búsqueda mucho más expresivo que el de un único vector store @shorten2024weaviate @mishra2026sok.

=== Arquitecturas multi-agente

Varios trabajos implementan Agentic-RAG mediante colaboración de múltiples agentes especializados que comparten memoria y se coordinan mediante un orquestador @maragheh2025arag @salve2024multiagent @singh2025agentic:

- ARAG (Personalized Recommendation) define cuatro agentes: _Agente de Comprensión del Usuario_ (_User Understanding Agent_), _Agente de NLI_ (_NLI Agent_)#footnote[NLI: _Natural Language Inference_ (Inferencia de Lenguaje Natural). Este agente evalúa, mediante un LLM, el grado de alineación semántica entre cada ítem candidato recuperado y la intención inferida del usuario, produciendo un puntaje que permite filtrar aquellos ítems que realmente respaldan la consulta o preferencia expresada @maragheh2025arag.], _Agente de Resumen de Contexto_ (_Context Summary Agent_) y _Agente de Ranking de Ítems_ (_Item Ranker Agent_); cada uno procesa una parte distinta de la información (preferencias de usuario, alineación semántica, resumen contextual y ranking final) @maragheh2025arag.

- Sistemas de RAG multi-fuente asignan un agente por tipo de fuente (relacional, NoSQL, documentos, grafos), que generan subconsultas y devuelven vistas parciales al orquestador @salve2024multiagent.

Este diseño mejora escalabilidad y permite extensibilidad incremental: añadir un nuevo tipo de fuente implica definir un nuevo agente y su herramienta.

=== Comparativa de arquitecturas

La @tab:comparativa-arq sintetiza las diferencias entre las principales variantes arquitectónicas de RAG @singh2025agentic @du2026arag @mishra2026sok @maragheh2025arag @salve2024multiagent.

#pagina-apaisada[
  #figure(
    three-line-table(
      columns: (1.2fr, 1.2fr, 1.6fr, 1.6fr),
      [
        | *Dimensión*             | *RAG clásico*             | *Agentic-RAG monolítico*                      | *Agentic-RAG multi-agente*                            |
        | ----------------------- | ------------------------- | --------------------------------------------- | ----------------------------------------------------- |
        | Control del flujo       | Pipeline fijo 1--2 pasos  | LLM decide secuencia de acciones              | Orquestador + múltiples agentes coordinados           |
        | Recuperación            | Una llamada a un índice   | Múltiples llamadas iterativas y adaptativas   | Recuperadores especializados por agente/fuente        |
        | Herramientas            | Normalmente solo búsqueda | Búsqueda + otras herramientas (cálculo, APIs) | Conjunto amplio de herramientas heterogéneas          |
        | Escalabilidad semántica | Limitada por el embedding | Mejora vía planificación y re-consulta        | Mejora adicional vía especialización y paralelización |
        | Complejidad de impl.    | Baja                      | Media (diseño de policy y herramientas)       | Alta (orquestación, memoria compartida, concurrencia) |
      ],
    ),
    caption: [Comparativa de arquitecturas RAG.],
  ) <tab:comparativa-arq>
]

== Agentes especializados en Agentic-RAG

=== Tipos de agentes por rol en el pipeline

La literatura y la práctica industrial convergen en una tipología de agentes especializados relativamente estable @shorten2024weaviate @singh2025agentic @achanta2025ieee:

- *Agente Planner / Orquestador:* recibe la consulta del usuario, la analiza, define subtareas y planea la secuencia de acciones (por ejemplo, "reformule la consulta", "busque en el grafo", "combine resultados").

- *Agentes de Recuperación (Retrieval Agents):* encapsulan estrategias de búsqueda concretas, como vector search, BM25, web search, bases SQL, grafos, APIs de dominio @mishra2026sok @shorten2024weaviate.

- *Agentes de Razonamiento y Fusión:* combinan evidencias, realizan razonamiento multi-hop, verifican consistencia y sintetizan una respuesta intermedia o final @mishra2026sok.

- *Agentes Evaluadores / Críticos:* revisan respuestas y cadenas de pensamiento, detectan alucinaciones, miden relevancia de pasajes y pueden gatillar re-búsquedas @xiong2025raggym @singh2025agentic.

- *Agentes de Dominio Específico:* especializados en un dominio (sanidad, finanzas, testing software, religión, etc.), con acceso a herramientas y conocimiento específicos @hariharan2025testing @zheng2025deepdx @zeggai2025vaxguide @bhatia2026islamic @maragheh2025arag.

=== Ejemplos concretos de agentes especializados

- *ARAG (recomendación personalizada)* @maragheh2025arag:
  - _User Understanding Agent_: resume preferencias del usuario combinando contexto a largo plazo y de sesión.
  - _NLI Agent_: evalúa la alineación semántica entre ítems candidatos y la intención inferida.
  - _Context Summary Agent_: condensa las evidencias del NLI para reducir longitud de contexto.
  - _Item Ranker Agent_: genera el ranking final de recomendaciones.

- *AI-VaxGuide (decisiones de vacunación):* utiliza un marco Agentic-RAG para convertir guías de vacunación extensas en un sistema interactivo de preguntas y respuestas, donde agentes razonadores buscan y combinan recomendaciones nacionales y de la OMS @zeggai2025vaxguide.

- *Deep-DxSearch (diagnóstico médico):* entrena un sistema Agentic-RAG end-to-end mediante RL, donde el LLM actúa como investigador activo sobre perfiles de enfermedad, historiales clínicos y literatura biomédica; el agente formula queries, evalúa evidencia y refina hipótesis diagnósticas @zheng2025deepdx.

- *IslamicFaithQA:* construye un marco Agentic-RAG para fundamentación coránica, utilizando llamadas estructuradas a herramientas de búsqueda sobre un corpus de versículos y recursos islámicos; el agente itera entre recuperar evidencias y revisar la respuesta para minimizar alucinaciones y abstenerse cuando no hay evidencia @bhatia2026islamic.

- *Agentic-RAG para testing de software:* combina agentes que trabajan sobre un sistema híbrido vector-grafo para automatizar generación de planes y casos de prueba, logrando importantes mejoras de precisión y eficiencia @hariharan2025testing.

=== Agentes de recuperación avanzados

Trabajos de Agentic-RAG como los de #cite(<du2026arag>, form: "prose") y #cite(<mishra2026sok>, form: "prose") enfatizan que el agente de recuperación evoluciona de simple indexador a *motor de búsqueda semántico-lógico* que integra múltiples índices y estrategias:

- Soporta *interfaces jerárquicas* (buscar documentos, luego secciones, luego chunks) con herramientas diferenciadas @du2026arag.

- Combina *vector search* con recuperación dispersa, queries estructuradas y grafos de conocimiento para superar las limitaciones de separabilidad lineal de embeddings densos en consultas lógicas complejas @mishra2026sok.

En la práctica industrial, proveedores como Weaviate, IBM y Azure hablan de _agentic retrieval_ como un pipeline especializado donde el LLM descompone la consulta en subconsultas, las ejecuta en paralelo sobre distintos recursos y luego reensambla las respuestas @microsoft2026ragazure @belcic2025ibm @shorten2024weaviate.

=== Evaluadores, jueces y supervisores

Con el auge de RL para Agentic-RAG, emergen agentes especializados que actúan como *jueces de proceso* (process reward models) evaluando la calidad de cada paso de la trayectoria en lugar de solo el resultado final @zhang2025process @zhang2026treeps @xiong2025raggym:

- ReasonRAG y TreePS-RAG utilizan recompensas de proceso para supervisar generación de queries, extracción de evidencias y síntesis de respuesta, mejorando estabilidad de entrenamiento y asignación de crédito @zhang2026treeps @zhang2025process.

- En RAG-Gym se explora el uso de LLMs avanzados como jueces de proceso para evaluar la calidad de trayectorias de agentes, cuya señal se usa luego para entrenar políticas de búsqueda más eficientes @xiong2025raggym.

== Flujo de trabajo en Agentic-RAG

=== Comparación de flujos: RAG estático vs. Agentic-RAG

En RAG estático, el flujo típico es: (1) indexación fuera de línea, (2) embedding y recuperación de top-$k$ pasajes, (3) concatenación al prompt, (4) generación de respuesta. Este flujo no se adapta durante la inferencia: no hay verificación dinámica de si la evidencia es suficiente, ni reformulación de la consulta @shorten2024weaviate @mishra2026sok.

En Agentic-RAG, el flujo se convierte en un bucle plan-act-observe-reflect donde el LLM (o conjunto de agentes) puede decidir: cuándo recuperar, cómo reformular, qué fuentes consultar, cuándo detener la búsqueda, y cómo fusionar evidencia @ferrazzi2026worth @shorten2024weaviate @mishra2026sok.

=== Flujo de trabajo genérico de Agentic-RAG

Un flujo de trabajo genérico, extraído de los surveys y de guías industriales de IBM, Weaviate, Google y Microsoft, se puede describir así @kolesnikov2026google @belcic2025ibm @microsoft2026ragazure @singh2025agentic @shorten2024weaviate:

+ *Comprensión y clasificación de la consulta.* Un agente planner analiza la consulta, detecta su tipo (factual simple, multi-salto, pregunta de dominio, tarea de síntesis, etc.) y decide si necesita recuperación externa. En algunos sistemas, un clasificador ligero estima la complejidad y escoge entre cero ejemplos (sin RAG), RAG simple o Agentic-RAG multi-paso @singh2025agentic.

+ *Planificación inicial.* El planner decide un plan de alto nivel: qué fuentes consultar (vector DB, web, grafo, SQL), qué herramientas usar y en qué orden (por ejemplo, primero ampliar contexto, luego focalizar) @achanta2025ieee @shorten2024weaviate @singh2025agentic.

+ *Ciclo iterativo de recuperación y razonamiento.* El agente ejecuta un bucle estilo ReAct: _Thought_ (razona sobre el siguiente paso), _Action_ (invoca una herramienta: búsqueda, cálculo, ejecución de código, llamada API, etc.) y _Observation_ (recibe resultados y actualiza su estado) @patronusai2025tutorial @shorten2024weaviate. Este ciclo se repite hasta cumplir criterios de parada (confianza suficiente, límite de pasos/tokens, retroalimentación del usuario) @xiong2025raggym @mishra2026sok.

+ *Fusión, verificación y corrección.* Un agente de fusión integra evidencias heterogéneas, aplica validaciones cruzadas (por ejemplo, comparar varias fuentes para detectar inconsistencias) y descarta ruido @achanta2025ieee @mishra2026sok. Un evaluador puede puntuar la respuesta candidata y, si la calidad es baja, pedir más evidencia o reformular la consulta @zhang2025process @zhang2026treeps @singh2025agentic.

+ *Síntesis y generación final.* El agente genera una respuesta final, potencialmente acompañada de citas, explicaciones de trazabilidad y advertencias cuando la evidencia es insuficiente @zheng2025deepdx @bhatia2026islamic @mishra2026sok.

+ *Actualización de memoria y aprendizaje.* El sistema puede actualizar memorias largas (por ejemplo, perfil de usuario en recomendación) y registros de trayectoria usados después para ajuste fino supervisado o aprendizaje por refuerzo (por ejemplo, ReasonRAG, TreePS-RAG) @zhang2026treeps @zhang2025process @xiong2025raggym @maragheh2025arag.

=== Patrones de flujos de trabajo específicos

Las revisiones bibliográficas de Agentic-RAG y de flujos de trabajo agéntico identifican patrones recurrentes que se concretan en implementaciones prácticas @kirkovska2025vellum @bandara2025practical @singh2025agentic:

- *Multi-query / Multi-HyDE:* generar múltiples reformulaciones de una misma consulta para cubrir aspectos complementarios, ejecutar recuperaciones en paralelo y fusionar resultados (por ejemplo, en Financial RAG con Multi-HyDE) @srinivasan2025financial.

- *Finite State Machine (FSM):* representar el flujo de trabajo agéntico como una máquina de estados finitos donde cada estado es una fase (reformulación, búsqueda, verificación, síntesis) y las transiciones se controlan con reglas o políticas aprendidas @srinivasan2025financial.

- *Grafos de flujo de trabajo (LangGraph, StateFlow):* modelar cada nodo como un agente o herramienta y usar edges condicionales basadas en resultados intermedios @kirkovska2025vellum @achanta2025ieee @singh2025agentic.

- *Orchestrator-Workers:* un agente orquestador divide la tarea en subtareas (por ejemplo, "extraer requisitos", "buscar casos similares", "proponer plan"), que se asignan a workers especializados; luego recoge y combina las salidas @jeong2024graph @salve2024multiagent @singh2025agentic.

=== Entrenamiento y optimización del flujo

Una tendencia clara es el uso de *RL y supervisión de proceso* para optimizar políticas Agentic-RAG, más allá de simple ingeniería de instrucciones @xiong2025raggym @zhang2025process @zhang2026treeps:

- RAG-Gym proporciona un entorno unificado para entrenar agentes de búsqueda y razonamiento con supervisión de proceso, destacando la eficacia de LLMs como jueces de trayectoria @xiong2025raggym.

- ReasonRAG (Process vs. Outcome Reward) muestra que recompensas de proceso para generación de queries, extracción de evidencias y respuesta final mejoran estabilidad y eficiencia frente a RL solo con recompensa final @zhang2025process.

- TreePS-RAG modela el razonamiento agentic como un árbol de rollouts, estimando la utilidad de cada paso a partir de resultados de sus descendientes, lo que permite crédito fino sin anotaciones intermedias @zhang2026treeps.

Estos enfoques apuntan a flujos de trabajo de Agentic-RAG cada vez más aprendidos y menos manuales.

== Casos de uso de Agentic-RAG

=== Dominios donde Agentic-RAG aporta ventajas claras

Las revisiones bibliográficas y estudios experimentales señalan que Agentic-RAG es especialmente útil cuando @singh2025agentic @ferrazzi2026worth @mishra2026sok:

- Las consultas requieren *razonamiento multi-hop* (por ejemplo, combinar múltiples documentos para llegar a una conclusión).
- Se necesitan *fuentes heterogéneas* (documentos, bases estructuradas, grafos, web en tiempo real).
- Hay *requisitos fuertes de trazabilidad y verificación*, como en salud, derecho o finanzas.
- La *complejidad de la tarea es variable*, por lo que conviene adaptar el grado de búsqueda y razonamiento.

El paper "Is Agentic RAG Worth It?" realiza una comparación experimental rigurosa entre RAG mejorado (Enhanced RAG) y Agentic-RAG, concluyendo que Agentic-RAG tiende a ofrecer mayores mejoras en escenarios complejos, aunque con mayor coste computacional @ferrazzi2026worth.

=== Salud y diagnóstico clínico

- *Deep-DxSearch:* un sistema de diagnóstico basado en Agentic-RAG que entrena end-to-end con RL sobre perfiles de enfermedad, historiales y 27M de documentos biomédicos @zheng2025deepdx. El agente aprende a formular consultas, evaluar evidencias y refinar búsquedas para cerrar brechas diagnósticas, superando ampliamente marcos RAG de ingeniería de prompts. En validación con 150 casos reales, mejora la precisión diagnóstica de médicos de 45.6% a 69.1% @zheng2025deepdx.

- *AI-VaxGuide:* sistema de preguntas y respuestas agéntico para decisiones de vacunación que transforma guías extensas en un sistema interactivo multilingüe. Agentic-RAG resulta especialmente superior frente a métodos tradicionales en preguntas multi-paso o ambiguas @zeggai2025vaxguide.

=== Recomendadores y personalización

ARAG demuestra un marco Agentic-RAG multi-agente para recomendación personalizada, donde agentes dedicados entienden al usuario, validan alineación semántica y ordenan ítems @maragheh2025arag. En tres conjuntos de datos de recomendación, ARAG supera RAG estándar y baselines por recencia, con mejoras de hasta 42.1% en NDCG\@5 y 35.5% en Hit\@5. El diseño agentic permite capturar comportamientos de sesión y largo plazo de forma más rica que heurísticas estáticas @maragheh2025arag.

=== Pruebas de software y entornos empresariales

- *Agentic-RAG para pruebas de software:* un enfoque que combina agentes autónomos con un sistema híbrido vector-grafo para automatizar generación de planes de prueba, casos y métricas de QE, usando modelos como Gemini y Mistral @hariharan2025testing. Reporta mejoras de precisión de 65% a 94.8%, reducción del 85% del cronograma de pruebas y ahorros de coste del 35% en proyectos de migración SAP y sistemas corporativos @hariharan2025testing.

- *Resolución de problemas empresarial:* trabajos sobre RAG agéntico ponderado para soporte técnico describen agentes que priorizan dinámicamente fuentes como manuales, bases de conocimiento internas y guías de resolución de problemas según el contexto, mejorando tiempo de resolución @khanda2024enterprise.

=== Dominios regulados y de alto riesgo

El marco agéntico para preguntas y respuestas islámicas (IslamicFaithQA) muestra cómo Agentic-RAG puede reducir alucinaciones y mejorar la capacidad de abstención en dominios donde respuestas incorrectas tienen consecuencias graves @bhatia2026islamic. El sistema incluye 25.000 pares de razonamiento SFT#footnote[SFT: _Supervised Fine-Tuning_ (Ajuste Fino Supervisado), técnica de entrenamiento donde un modelo pre-entrenado se ajusta con pares de entrada-salida etiquetados, empleada en la primera etapa del pipeline de InstructGPT @ouyang2022instructgpt.], 5.000 muestras de preferencia y un corpus de versículos; el agente llama herramientas estructuradas para buscar evidencia y revisa iterativamente las respuestas. Los resultados muestran que Agentic-RAG supera RAG estándar en corrección y robustez árabe-inglés @bhatia2026islamic.

De forma análoga, IBM y otros proveedores destacan Agentic-RAG como patrón recomendado para dominios donde se requieran respuestas explicables, auditables y actualizables sobre bases de conocimiento en constante cambio @belcic2025ibm @microsoft2026ragazure @achanta2025ieee.

=== Investigación académica y análisis político

Trabajos sobre LLMs como asistentes de investigación política describen Agentic-RAG como mecanismo central para dotar a los modelos de capacidades de acción sobre funciones y herramientas, desde recopilación automatizada de datos hasta codificación de transcripciones y modelado estadístico @loffredo2025political. El agente no solo recupera documentos, sino que también invoca herramientas para resumir, clasificar y cuantificar información, operando sobre flujos de trabajo multi-paso típicos de investigación en ciencias sociales @loffredo2025political.

=== Benchmarks y plataformas de evaluación

Para medir de forma sistemática Agentic-RAG, se han propuesto:

- *RAG-Gym:* entorno para optimizar agentes de búsqueda y razonamiento con supervisión de proceso, evaluando costes y calidad de forma uniforme @xiong2025raggym.

- *ARC (Agentic RAG Capabilities):* métrica fina que descompone capacidades agentic en razonamiento, coordinación de búsqueda y síntesis de respuesta, usada para estudiar cómo modelos compactos preservan comportamientos agentic mediante RL con distillation-guided policy optimization @kotoge2025compact.

Estos recursos son clave para comparar arquitecturas y políticas de Agentic-RAG de forma rigurosa más allá de casos de uso ad hoc.

== Consideraciones prácticas para ingeniería

=== Diseño de arquitecturas en producción

Las guías de IBM, Weaviate, Microsoft y Google Cloud coinciden en varias recomendaciones prácticas @kolesnikov2026google @microsoft2026ragazure @belcic2025ibm @shorten2024weaviate @achanta2025ieee:

- Empezar por un RAG bien instrumentado y evolucionar a Agentic-RAG donde haya puntos críticos evidentes (multi-hop, heterogeneidad de fuentes, requisitos de auditoría).

- Modelar explícitamente el flujo de trabajo como grafo o FSM (por ejemplo, LangGraph, StateFlow, orquestadores propios) para controlar costes y trazabilidad.

- Limitar el espacio de herramientas y definir contratos claros (inputs/outputs tipados) para reducir errores de invocación de herramientas.

- Introducir agentes evaluadores (LLM como juez, reglas, métricas) que puedan rechazar respuestas de baja calidad y gatillar bucles de corrección. 

=== Compromisos clave

Los estudios comparativos resaltan varios trade-offs @kotoge2025compact @mishra2026sok @ferrazzi2026worth @xiong2025raggym:

- *Calidad vs. coste:* más pasos agentic implican más tokens y latencia; conviene adoptar políticas adaptativas que escalen el esfuerzo con la dificultad de la consulta.

- *Autonomía vs. control:* dar demasiada libertad al agente puede aumentar riesgos de alucinación compuesta, _uso indebido de herramientas_ y comportamiento impredecible; por ello se recomiendan políticas con límites de profundidad y herramientas, además de supervisores @mishra2026sok.

- *Complejidad de ingeniería:* multi-agente y multi-herramienta simplifican extensibilidad pero aumentan coste de observabilidad, testing y debugging.

=== Direcciones abiertas de investigación

#cite(<mishra2026sok>, form: "prose") y trabajos recientes identifican varias líneas abiertas @chen2026jade @tian2025queryperf @kotoge2025compact @zhang2026treeps:

- *Retrieval adaptativo y estable:* políticas que ajusten dinámicamente intensidad y tipo de búsqueda según señales de calidad de query y de resultados @tian2025queryperf.

- *Orquestación consciente de costos:* optimizar políticas de Agentic-RAG bajo restricciones de coste/latencia, quizá con RL multi-objetivo.

- *Evaluación de trayectorias:* métricas y benchmarks que evalúen no solo la respuesta final, sino la calidad del camino seguido (relevancia de evidencias, robustez a ruido, etc.) @mishra2026sok @xiong2025raggym.

- *Seguridad y robustez:* mitigación de riesgos como contaminación de memoria, propagación de alucinaciones, vulnerabilidades en ejecución de herramientas y ataques adversarios sobre el pipeline @mishra2026sok.

Estas líneas son altamente relevantes para trabajos de tesis que busquen unir aportes teóricos (por ejemplo, formulación POMDP#footnote[POMDP: _Partially Observable Markov Decision Process_ (Proceso de Decisión de Markov Parcialmente Observable). Modelo matemático para problemas de decisión secuencial donde el agente no observa completamente el estado del entorno, sino que recibe observaciones parciales y debe mantener una creencia (distribución de probabilidad) sobre el estado real. En Agentic-RAG, se usa para formalizar el bucle de planificación-acción-observación donde el agente decide qué buscar basándose en evidencias parciales @mishra2026sok.], garantías de convergencia) con ingeniería de sistemas (por ejemplo, frameworks de orquestación, métricas operativas).


== LLM-as-a-judge <sec:llm-as-a-judge>

La evaluación automática de sistemas de lenguaje natural ha sido históricamente un desafío. Las métricas tradicionales como BLEU @papineni2002bleu y ROUGE @lin2004rouge miden calidad mediante solapamiento léxico entre la salida y un texto de referencia, pero fallan en escenarios abiertos y dinámicos donde múltiples respuestas pueden ser igualmente válidas @liu2016not. Con el auge de los modelos de lenguaje grandes (LLMs), surgió el paradigma _LLM-as-a-judge_, donde un LLM actúa como evaluador, asignando puntuaciones, produciendo rankings o seleccionando la mejor opción entre candidatos @zheng2023judging @li2024generation2judgment.

=== Definición y fundamentos

Formalmente, el proceso de evaluación con LLM-as-a-judge se puede definir como $R = J(C_1, ..., C_n)$, donde $J$ es el LLM juez, $C_i$ son los candidatos a evaluar y $R$ es el resultado del juicio @li2024generation2judgment. Las modalidades de entrada se clasifican en:

- *Point-wise* ($n=1$): el juez evalúa un único candidato de forma absoluta, asignando una puntuación numérica o categórica.
- *Pair-wise* ($n=2$): el juez compara dos candidatos y determina cuál es superior.
- *List-wise* ($n>2$): el juez ordena o selecciona entre múltiples candidatos.

En cuanto a la salida, el juez puede producir: (a) una *puntuación* numérica (continua o discreta), (b) un *ranking* de los candidatos, o (c) una *selección* del mejor candidato @li2024generation2judgment.

=== Taxonomía de atributos evaluables

La literatura identifica al menos seis atributos que LLM-as-a-judge puede evaluar de forma diferenciada @li2024generation2judgment:

- *Utilidad (Helpfulness)*: mide la utilidad e informatividad de una respuesta generada. Es el criterio más empleado en evaluación de asistentes conversacionales y alineamiento @zheng2023judging.
- *Seguridad (Safety \& Security)*: evalúa si el modelo evita generar contenido dañino, tóxico o sesgado. Se ha validado que LLMs pueden actuar como moderadores de contenido siguiendo guías de políticas @bai2022constitutional.
- *Confiabilidad (Reliability)*: mide la fidelidad de la respuesta a fuentes verificables y la calibración de la incertidumbre expresada. Incluye la detección de alucinaciones @min2023factscore.
- *Relevancia (Relevance)*: evalúa qué tan bien se alinea la respuesta con la consulta o tarea original. Es particularmente importante en sistemas RAG @es2023ragas.
- *Lógica (Logic)*: evalúa la coherencia interna y corrección del razonamiento, independientemente de la precisión factual @yao2023tree.
- *Calidad general (Overall Quality)*: evaluación holística que integra múltiples dimensiones en una puntuación compuesta @lin2023unlocking.

=== Metodologías de prompting

El diseño de las instrucciones (_prompts_) para el LLM juez es crítico para la calidad de la evaluación. Las principales estrategias incluyen @li2024generation2judgment @gu2024survey:

- *Aumento con reglas (Rule Augmentation)*: incorporar principios, rúbricas y criterios de evaluación directamente en el prompt. Por ejemplo, en Constitutional AI @bai2022constitutional se introduce una lista de principios (utilidad, inocuidad, honestidad) para guiar la comparación.
- *Operación de intercambio (Swapping Operation)*: para mitigar el sesgo de posición —donde el LLM favorece la primera o última opción presentada— se invoca al juez dos veces intercambiando el orden de los candidatos. Si los resultados son inconsistentes, se declara un empate @zheng2023judging.
- *Demostraciones (In-Context Learning)*: proporcionar ejemplos concretos de evaluaciones correctas para que el LLM aprenda los estándares de evaluación @jain2023multi.
- *Cadena de pensamiento (Chain-of-Thought)*: descomponer la evaluación en pasos intermedios, como en G-Eval @liu2023geval, donde el LLM primero genera una explicación y luego asigna una puntuación.
- *Colaboración multi-agente*: utilizar múltiples LLMs como jueces y agregar sus decisiones mediante votación, debate o ranking entre pares para reducir sesgos individuales @li2023prd @chanchateval.
- *Interacción multi-turno*: el juez interactúa dinámicamente con el candidato, formulando preguntas de seguimiento para una evaluación más profunda @bai2023benchmarking.

=== Métodos de ajuste fino

Más allá del prompting, se han desarrollado LLMs especializados como jueces mediante ajuste fino supervisado (SFT) y aprendizaje por preferencias @li2024generation2judgment:

- *JudgeLM* @zhu2023judgelm: ajusta modelos Vicuna con 100K pares de juicios generados por GPT-4, abordando sesgos mediante aumento de datos con intercambio.
- *Prometheus* @kim2023prometheus y *Prometheus 2* @kim2024prometheus2: modelos open-source especializados en evaluación fine-grained, capaces de evaluar según rúbricas personalizadas y soportar tanto evaluación directa como comparación por pares.
- *AUTO-J* @li2024generative: entrenado con datos sintéticos de GPT-4 para generar evaluaciones tanto point-wise como pair-wise con explicaciones detalladas.
- *FLAMe* @vu2024foundational: modelo entrenado con más de 5 millones de juicios humanos en 100+ tareas, demostrando capacidad de generalización a tareas no vistas.
- *Self-Taught Evaluator* @wang2024self: utiliza aprendizaje iterativo con datos sintéticos para mejorar sin depender de anotaciones humanas.

=== Sesgos y vulnerabilidades

A pesar de su efectividad, LLM-as-a-judge presenta sesgos significativos que deben ser considerados @li2024generation2judgment @gu2024survey:

- *Sesgo de posición (Position Bias)*: el LLM tiende a favorecer respuestas según su orden de presentación @zheng2023judging @wang2023large.
- *Sesgo de verbosidad (Verbosity Bias)*: favorece respuestas más largas, equiparando extensión con calidad @koo2023benchmarking.
- *Sesgo egoísta (Egocentric Bias)*: el LLM juez favorece respuestas generadas por sí mismo @liu2023geval.
- *Sesgo de autoridad (Authority Bias)*: favorece afirmaciones que citan fuentes que parecen autoritarias @chen2024humans.
- *Vulnerabilidad adversarial*: secuencias adversariales cuidadosamente diseñadas pueden manipular las puntuaciones del juez @shi2024judgedeceiver @raina2024llm.

Para mitigar estos sesgos, se han propuesto técnicas como calibración mediante intercambio de posición @zheng2023judging, uso de múltiples jueces @li2023prd, y entrenamiento con datos debiased como OFFSETBIAS @park2024offsetbias.

=== LLM-as-a-judge en sistemas RAG

En el contexto de RAG, LLM-as-a-judge se ha convertido en el método de evaluación predominante, ya que permite evaluar dimensiones que las métricas tradicionales no capturan @gu2024survey @li2024llmsasjudges:

- *RAGAS* @es2023ragas: framework que utiliza LLMs para evaluar sistemas RAG en tres dimensiones: relevancia del contexto, fidelidad de la respuesta y relevancia de la respuesta.
- *ARES* @saad2023ares: combina LLMs con clasificadores entrenados para evaluar RAG en las mismas tres dimensiones, utilizando PPI (_Prediction-Powered Inference_) para intervalos de confianza estadística.
- *Self-RAG* @asai2023selfrag: el propio LLM genera _tokens reflectantes_ que indican si necesita recuperación y evalúa la calidad de sus propias salidas, integrando el juez dentro del pipeline de generación.
- *RAG-Gym* @xiong2025raggym: entorno unificado para entrenar agentes de búsqueda y razonamiento con supervisión de proceso, donde LLMs avanzados actúan como jueces de trayectoria.
- *ConsJudge* @liu2025consjudge: método que mejora la consistencia del juez LLM en RAG utilizando consistencia entre juicios (_judge-consistency_) para seleccionar pares de preferencia y entrenar con DPO.

=== Meta-evaluación de LLM-as-a-judge

La evaluación de los propios LLM jueces —meta-evaluación— es un área activa de investigación. Los benchmarks más relevantes incluyen @li2024generation2judgment:

- *MT-Bench y Chatbot Arena* @zheng2023judging: el primero es un conjunto de preguntas multi-turno para evaluar la capacidad de los LLMs de seguir instrucciones; el segundo es una plataforma crowdsourced donde usuarios votan anónimamente entre respuestas de distintos modelos, generando rankings mediante puntuaciones Elo.
- *JudgeBench* @tan2024judgebench: benchmark que evalúa LLM jueces en pares de respuestas desafiantes en dominios como conocimiento, razonamiento, matemáticas y código, con etiquetas de preferencia que reflejan corrección objetiva.
- *RewardBench* @lambert2024rewardbench: benchmark para evaluar modelos de recompensa en áreas como chat, razonamiento y seguridad.
- *LLM-as-a-Judge Meta-Evaluation* @bavaresco2024llms: estudio a gran escala que evalúa la correlación entre LLM jueces y evaluadores humanos en 20 tareas de NLP, encontrando que la concordancia varía significativamente según la tarea y el modelo.

Las métricas de meta-evaluación más utilizadas son la correlación de Pearson, Spearman, Kendall's $tau$ y el coeficiente Kappa de Cohen, que miden el grado de acuerdo entre el LLM juez y los evaluadores humanos @li2024generation2judgment. Soft Pairwise Accuracy (SPA) @thompson2024spa ha surgido como una métrica más robusta que asigna crédito parcial por rankings casi correctos.

=== Implicaciones para esta tesis

En esta tesis, LLM-as-a-judge se emplea como método principal de evaluación del sistema Agentic-RAG para consulta de normativa argentina. La elección responde a varias consideraciones:

1. Las respuestas del sistema son inherentemente abiertas y no existe una única respuesta correcta, lo que hace que métricas basadas en solapamiento léxico (BLEU, ROUGE) sean inadecuadas.
2. El dominio legal requiere evaluación de dimensiones como precisión factual, completitud y relevancia, que LLM-as-a-judge puede capturar mediante rúbricas personalizadas.
3. La escalabilidad del método permite evaluar sistemáticamente múltiples configuraciones del sistema sin el costo prohibitivo de anotadores humanos expertos.

Para mitigar los sesgos inherentes, se adoptan las siguientes estrategias: (a) uso de múltiples LLM jueces y agregación de resultados, y (b) prompts con rúbricas detalladas específicas del dominio legal que definan explícitamente los criterios de puntuación.

== Síntesis del capítulo

Este capítulo presentó el marco teórico de Agentic-RAG, partiendo del concepto de RAG clásico y evolucionando hacia arquitecturas agénticas donde un planificador autónomo decide cuándo y cómo recuperar información. Se describieron las principales arquitecturas —monolítica, multi-agente y jerárquica—, los patrones de flujo de trabajo reutilizables (encadenamiento, enrutamiento, paralelización, orquestador-trabajadores, evaluador-optimizador) y los agentes especializados que componen estos sistemas: planificadores, recuperadores, razonadores, evaluadores y agentes de dominio específico.

Se dedicó una sección al paradigma LLM-as-a-judge, que constituye el método de evaluación principal empleado en esta tesis. Se presentaron sus fundamentos formales, la taxonomía de atributos evaluables (utilidad, seguridad, confiabilidad, relevancia, lógica y calidad general), las metodologías de prompting y ajuste fino para construir jueces LLM, los sesgos y vulnerabilidades que afectan a estos evaluadores, y su aplicación específica en sistemas RAG mediante frameworks como RAGAS, ARES, Self-RAG y ConsJudge. Se discutieron también los benchmarks y métricas de meta-evaluación para validar la calidad de los propios jueces LLM.

Se analizaron casos de uso concretos en salud, recomendación, pruebas de software, dominios regulados e investigación académica, así como las consideraciones prácticas de ingeniería para llevar estos sistemas a producción. Finalmente, se identificaron direcciones abiertas de investigación, entre las que se destacan la orquestación consciente de costos, la evaluación de trayectorias y la seguridad y robustez de los pipelines agénticos.

El siguiente capítulo (@cap:metodologia) describe la metodología empleada para diseñar, implementar y evaluar el sistema Agentic-RAG para consulta de normativa argentina, detallando el diseño experimental, las fases del proyecto y los criterios de selección de herramientas y métricas.

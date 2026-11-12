= Trabajos Relacionados

#import "@preview/tablem:0.3.0": three-line-table

== Introducción

El presente capítulo revisa los trabajos previos y las plataformas existentes que guardan relación con el sistema Agentic-RAG propuesto en este trabajo final. La revisión se organiza en cuatro ejes: sistemas de búsqueda legal (tanto tradicionales como asistidos por inteligencia artificial), aplicaciones de RAG en dominios especializados con énfasis en el ámbito jurídico, sistemas agénticos y su integración con RAG, y benchmarks para la evaluación de sistemas de procesamiento de lenguaje natural en el dominio legal. Finalmente, se presenta una comparación del presente trabajo con la literatura analizada, identificando las contribuciones originales.

== Sistemas de Búsqueda Legal

=== Sistemas Tradicionales Basados en Palabras Clave

Los sistemas de consulta legal más establecidos en Argentina operan mediante búsquedas basadas en coincidencia de palabras clave, filtros por tipo de norma, jurisdicción y fecha.

*Infoleg* @infoleg2025 es una base de datos legislativa nacional de acceso libre y gratuito, administrada por la Dirección Nacional del Sistema Argentino de Información Jurídica del Ministerio de Justicia de la Nación. Contiene leyes, decretos, decisiones administrativas, resoluciones, disposiciones y todo acto cuya publicación sea obligatoria en la primera sección del Boletín Oficial de la República Argentina. Sus contenidos están licenciados bajo Creative Commons Reconocimiento 2.5 Argentina.

*SAIJ* (Sistema Argentino de Información Jurídica) @saij2025 es un servicio de la Dirección Nacional del SAIJ, dependiente del Ministerio de Justicia de la Nación. Fundado en 1981 con apoyo de la UNESCO, incluye todas las leyes nacionales sancionadas desde 1853, tratados internacionales, decretos nacionales y provinciales, jurisprudencia de tribunales federales, nacionales y provinciales, proyectos legislativos, dictámenes de la Procuración del Tesoro de la Nación, artículos de doctrina y publicaciones de Ediciones SAIJ. Su motor de búsqueda permite filtrar por tipo de contenido (legislación, fallos, sumarios, doctrina), tipo de norma (ley, decreto, resolución, disposición), jurisdicción y fecha.

A nivel internacional, plataformas como *Westlaw* @westlaw2025 y *LexisNexis* @lexisplus2025 han sido durante décadas los referentes en investigación legal, operando inicialmente con motores de búsqueda por palabras clave sobre extensas bases de datos de jurisprudencia y legislación, principalmente de Estados Unidos y otros países anglosajones.

Si bien estos sistemas cumplen una función esencial al garantizar el acceso a la información jurídica, su dependencia de la coincidencia exacta de términos limita su capacidad para comprender la semántica de las consultas, lo que frecuentemente produce resultados irrelevantes o incompletos cuando el usuario no emplea los términos técnicos precisos.

=== Sistemas Comerciales con IA

En los últimos años, múltiples plataformas comerciales han integrado inteligencia artificial para mejorar la búsqueda y el análisis jurídico. A continuación se describen las más relevantes.

*Lexis+ con Protégé* @lexisplus2025 es la evolución de la plataforma de LexisNexis que integra un asistente de IA agéntico denominado Protégé. Este sistema es capaz de completar tareas de forma autónoma, revisar su propio trabajo y sugerir mejoras. Entre sus capacidades se incluyen la redacción de documentos legales (mociones, demandas, memorandos), la investigación legal con validación de citas mediante Shepard's, el análisis de documentos de hasta 300 páginas y la generación de cronologías a partir de materiales cargados. En agosto de 2025, LexisNexis incorporó Protégé General AI, que provee acceso seguro a múltiples modelos de IA de propósito general (GPT-5, Claude Sonnet 4, GPT-4o) junto con herramientas de IA específicas para el dominio legal. La plataforma emplea una arquitectura RAG con integración del grafo de conocimiento Shepard's (GraphRAG) para generar respuestas fundamentadas en fuentes verificables.

*Westlaw con CoCounsel* @westlaw2025 es la plataforma de Thomson Reuters que lanzó CoCounsel Legal en agosto de 2025, representando su oferta más avanzada de IA. Integrada con Westlaw Advantage, incluye la funcionalidad Deep Research, que en lugar de devolver simplemente resultados de búsqueda, razona a través de preguntas legales, genera planes de investigación de múltiples pasos, explica su lógica y entrega informes completos fundamentados en el contenido de Westlaw y Practical Law. La tecnología se basa en los desarrollos de CoCounsel, construidos sobre GPT-4. Un estudio publicado en el Journal of Empirical Legal Studies encontró que Westlaw AI-Assisted Research presentaba alucinaciones en el 33\% de las consultas, Lexis+ AI en el 17\% y GPT-4 sin RAG en el 43\% @magesh2025hallucinationfree.

*vLex con Vincent AI* @vlex2025 es una plataforma de inteligencia legal generativa que combina una de las mayores bases de datos legales a nivel global —con más de mil millones de documentos de más de 100 países— con IA avanzada. Vincent AI interpreta consultas en lenguaje natural para producir respuestas legales con citas completas, generar argumentos legales, comparar leyes entre jurisdicciones y automatizar flujos de trabajo complejos. En ensayos controlados aleatorizados, Vincent mostró 3,67 veces más fiabilidad que los LLM de propósito general. La plataforma emplea búsqueda vectorial (machine learning) para organizar documentos mediante búsqueda conceptual en lugar de coincidencia de palabras clave. Su alcance internacional, que incluye cobertura de Estados Unidos, Reino Unido, España, la Unión Europea, Singapur, México, Chile, Nueva Zelanda y Colombia, lo diferencia de sus competidores.

*Lexius* @lexius2025 es un sistema jurídico con IA de origen latinoamericano que opera en 18 países. En Argentina cuenta con acceso a más de 32.500 textos legales y 52.500 sentencias. Su motor de búsqueda inteligente identifica la intención de la consulta del usuario y ofrece funcionalidades como chat y llamadas con IA para resolver dudas legales, generación de video podcasts legales narrados por IA, mapas mentales interactivos y exportación de documentos en múltiples formatos.

*Juztina* @juztina2025 es una legaltech peruana que utiliza inteligencia artificial para democratizar el acceso a información jurídica en América Latina. Su plataforma ofrece un chat de IA con acceso a más de 3 millones de documentos legales, permitiendo a abogados y usuarios realizar búsquedas especializadas de jurisprudencia, normativa y doctrina. Con presencia en Perú, Colombia y México, Juztina ha expandido su operación a Argentina. La búsqueda de información empleando la plataforma toma de diez segundos a un minuto, reduciendo significativamente los tiempos de investigación legal.

*Veredicta* @veredicta2025 es una plataforma argentina que integra gestión de expedientes con IA. Su motor de búsqueda semántica analiza más de 500.000 fuentes judiciales argentinas, permite buscar describiendo el caso en lenguaje natural, genera resúmenes automáticos de fallos y está integrado con el Poder Judicial de la Nación (PJN), expedientes y WhatsApp. A diferencia de herramientas como Lexius o Juztina, Veredicta permite encontrar jurisprudencia y vincularla directamente al expediente en curso.

*Lexium* @lexium2025 es una plataforma de IA de gestión jurídica especializada en derecho argentino. Ofrece búsqueda inteligente en SAIJ, Infoleg y jurisprudencia, automatización de escritos y gestión de vencimientos procesales. La propia plataforma reconoce las limitaciones inherentes a los modelos de IA generativa, incluyendo la posibilidad de generar información incompleta, imprecisa o no actualizada con la legislación vigente, recomendando verificar siempre las fuentes oficiales.

En Argentina también se destaca el sistema de *Búsqueda de Jurisprudencia Asistida por IA* del Tribunal Fiscal de la Nación @tribunalfiscal2024buscador, que incorpora inteligencia artificial a la búsqueda de documentos legales, aunque limitado a documentos emitidos por dicho tribunal.

== Sistemas RAG en Dominios Especializados

=== RAG para el Dominio Legal

La aplicación de RAG al dominio legal ha sido objeto de creciente investigación. Hindi et al. @hindi2025legalrag presentaron una revisión exhaustiva sobre la precisión e interpretabilidad de los sistemas RAG en tecnología legal, identificando que la combinación de recuperación semántica con generación de texto permite anclar las respuestas en documentos reales, reduciendo significativamente las alucinaciones en comparación con el uso de LLMs sin RAG. La revisión cataloga diversos métodos y aplicaciones de RAG legal, incluyendo análisis de contratos, protección de privacidad y evaluación de sistemas mediante LegalBench-RAG @pipitone2024legalbench.

Siino et al. @siino2025legal realizaron una revisión de la literatura sobre aplicaciones de LLMs en el ámbito legal, cubriendo tareas como clasificación de textos legales, reconocimiento de entidades nombradas, resumidización de documentos y respuesta a preguntas legales. Los autores identifican que si bien los avances son significativos, la mayoría de los trabajos se concentran en el idioma inglés y en los sistemas jurídicos del common law, dejando subrepresentados los sistemas de derecho civil como el argentino.

LexisNexis incorporó a su plataforma Lexis+ AI mejoras en su pipeline de RAG, incluyendo la integración del grafo de conocimiento Shepard's (GraphRAG), que utiliza información de relaciones entre casos para generar respuestas más completas y autoritativas.

A nivel académico, se han desarrollado sistemas como JusBuild, que emplea un modelo de campos aleatorios condicionales (CRF) para la segmentación supervisada de documentos legales en secciones funcionales, una base de datos vectorial para almacenar representaciones semánticas y RAG con LLMs para sugerir secciones relevantes durante la redacción de documentos legales.

=== RAG para Documentación Técnica y Otros Dominios

Los sistemas RAG han encontrado aplicaciones significativas en múltiples dominios especializados más allá del legal. En el ámbito médico, una revisión narrativa publicada en PubMed Central @gargari2025medicalai exploró la aplicación de RAG en contextos médicos, identificando su utilidad para soporte en decisiones clínicas, asistencia diagnóstica, interpretación de guías médicas y evaluación de elegibilidad para ensayos clínicos. Un estudio publicado en npj Digital Medicine evaluó modelos LLM-RAG para determinar la aptitud quirúrgica utilizando 35 guías locales y 23 internacionales, demostrando que RAG permite personalizar LLMs integrando conocimiento especializado con mayor precisión y consistencia que los modelos base.

En el ámbito financiero, se han explorado aplicaciones de RAG para la recuperación y consulta de documentación regulatoria, reportes financieros y normativa contable @srinivasan2025financial. En contextos de gobernanza electrónica, se ha evaluado la fidelidad de sistemas Agentic-RAG utilizando frameworks de evaluación basados en LLM-as-a-Judge con múltiples modelos evaluadores.

Estos trabajos demuestran que la arquitectura RAG es transferible entre dominios especializados, y que las técnicas de fragmentación de texto, embeddings semánticos y recuperación por similitud desarrolladas en un dominio pueden informar el diseño de sistemas en otros.

== Sistemas Agénticos

=== Agentes para Tareas Legales

La aplicación de agentes basados en LLM al dominio legal ha sido revisada de forma comprehensiva por #cite(<yang2025legalagents>, form: "prose"), quienes trazan la evolución desde sistemas de agente único hacia arquitecturas multi-agente. Los autores identifican que los agentes legales pueden clasificarse según sus capacidades: consulta legal, análisis de documentos, asistencia en litigios y simulación judicial.

He et al. @he2024agentscourt propusieron *AgentsCourt*, un sistema que construye agentes de toma de decisiones judiciales mediante simulación de debates judiciales y aumentación de conocimiento legal. El sistema simula el proceso judicial completo, con agentes que representan diferentes roles (juez, fiscal, defensor), demostrando que la interacción multi-agente puede mejorar la calidad del razonamiento legal.

En una dirección complementaria, se ha propuesto una *arquitectura multi-agente para IA legal confiable* @springer2025trustworthy que emplea tres componentes principales: enrutamiento de consultas a agentes especializados para actos legales específicos, recuperación de regulaciones y razonamiento para generar respuestas fundamentadas. El sistema fue evaluado utilizando un examen de ingreso a la abogacía de 2024 con 150 preguntas, demostrando que la combinación de agentes especializados con RAG mejora significativamente la precisión respecto a modelos de propósito general.

=== Agentic-RAG en la Literatura

El concepto de Agentic-RAG ha sido formalizado por Singh et al. @singh2025agentic, quienes presentaron una revisión comprensiva que distingue este paradigma del RAG tradicional. Mientras que el RAG convencional sigue flujos de trabajo estáticos (consulta → recuperación → generación), Agentic-RAG incorpora agentes autónomos de IA en el pipeline que son capaces de planificar, razonar, usar herramientas y adaptarse al contexto de la consulta. Los autores identifican que Agentic-RAG trasciende las limitaciones del RAG estático al permitir razonamiento de múltiples pasos y gestión de tareas complejas.

La tendencia hacia sistemas Agentic-RAG se ve reforzada por avances recientes en modelos de razonamiento de gran escala (Large Reasoning Models), como los modelos basados en aprendizaje por refuerzo (DeepSeek-R1, modelos análogos a OpenAI o1), que poseen capacidades inherentes de razonamiento complejo y de múltiples pasos, integrándose naturalmente en flujos de trabajo agénticos.

LexisNexis ha adoptado este paradigma con su asistente Protégé, descrito explícitamente como un "sistema de IA agéntico" capaz de completar tareas de forma autónoma, revisar su propio trabajo y sugerir mejoras @lexisplus2025. De manera similar, Westlaw con CoCounsel implementa capacidades agénticas a través de Deep Research, que genera planes de investigación de múltiples pasos y explica su lógica.

== Benchmarks para Evaluación Legal

=== LegalBench, LexGLUE y Otros Benchmarks en Inglés

La evaluación del desempeño de modelos de lenguaje en tareas legales se ha beneficiado del desarrollo de múltiples benchmarks, aunque la gran mayoría se concentran en el idioma inglés y en sistemas jurídicos anglosajones.

*LexGLUE* @chalkidis2021lexglue es un benchmark inspirado en GLUE que comprende siete datasets para evaluar la comprensión del lenguaje legal en inglés, cubriendo legislación de la Unión Europea y Estados Unidos. Incluye tareas de clasificación multi-etiqueta y multi-clase sobre documentos legales del Parlamento Europeo, la Corte Suprema de Estados Unidos y contratos.

*LegalBench* @guha2023legalbench es un esfuerzo colaborativo de código abierto que agrupa tareas para evaluar el razonamiento legal en LLMs. Contiene tareas diversas que cubren múltiples tipos textuales, estructuras de tareas, dominios legales y niveles de dificultad, centradas principalmente en el derecho estadounidense. LegalBench es notable por su enfoque interdisciplinario, combinando la experiencia de científicos de la computación y abogados.

*LegalBench-RAG* @pipitone2024legalbench adapta el benchmark LegalBench para evaluar específicamente sistemas de generación aumentada por recuperación en el dominio legal, permitiendo medir no solo la calidad de la generación sino también la efectividad de la recuperación de documentos relevantes.

*LEXTREME* @niklaus2023lextreme es el primer benchmark multilingüe y multi-tarea para el dominio legal, cubriendo 24 idiomas indoeuropeos y urálicos a través de 11 datasets. Sus resultados muestran que incluso los mejores modelos de referencia alcanzan resultados modestos, y que ChatGPT enfrenta dificultades con muchas tareas, evidenciando la brecha entre los modelos de propósito general y las necesidades del dominio legal especializado.

*LawBench* @fei2024lawbench se enfoca en el sistema legal chino, y *LEXam* @niklaus2025lexam evalúa el razonamiento legal sobre 340 exámenes de derecho de múltiples jurisdicciones.

=== Benchmarks en Español y Modelos para el Dominio Legal Hispanohablante

El estado del arte en evaluación de NLP legal en español es considerablemente más limitado que en inglés. Si bien LEXTREME incluye algunos idiomas europeos, el español está subrepresentado en los corpus de entrenamiento de los grandes modelos de lenguaje, lo que genera un desafío adicional para el desarrollo de herramientas de NLP para textos legales en español.

*MEL* (Modelo de Español Legal) @betancur2025mel es un modelo de lenguaje basado en XLM-RoBERTa-large, entrenado específicamente para la comprensión de textos legales en español. Sus evaluaciones muestran una mejora significativa sobre los modelos base en tareas como clasificación legal y reconocimiento de entidades nombradas en español. Este trabajo es especialmente relevante al demostrar que la adaptación al dominio legal en español requiere modelos especializados.

El corpus *Legal-ES* @samy2020legales constituye un meta-corpus que reúne múltiples fuentes del dominio legal en lengua española, incluyendo textos legislativos, jurisprudenciales (sentencias) y administrativos. Además, presenta resultados preliminares sobre embeddings del español jurídico y un modelo de tópicos entrenado sobre legislación española.

En Argentina, no se han identificado a la fecha benchmarks específicos para evaluar sistemas de consulta sobre normativa argentina, lo que constituye una de las motivaciones del presente trabajo.

== Comparación con el Presente Trabajo

La @tab:comparacion_trabajos presenta una comparación del presente trabajo con los sistemas y plataformas revisados en este capítulo.

#figure(
  three-line-table(
    columns: (1.3fr, 0.7fr, 0.55fr, 0.65fr, 0.9fr, 0.9fr),
    [
      | *Sistema/Trabajo*  | *Código abierto* | *RAG* | *Agentes* | *Normativa argentina* | *Benchmark abierto* |
      | :----------------- | :--------------: | :---: | :-------: | :-------------------: | :-----------------: |
      | Infoleg / SAIJ     |       N/A        |  No   |    No     |          Sí           |         No          |
      | Westlaw CoCounsel  |        No        |  Sí   |    Sí     |          No           |         No          |
      | Lexis+ Protégé     |        No        |  Sí   |    Sí     |          No           |         No          |
      | vLex Vincent AI    |        No        |  Sí   |    Sí     |        Parcial        |         No          |
      | Lexius             |        No        |  Sí   |    Sí     |          Sí           |         No          |
      | Juztina            |        No        |  Sí   |    Sí     |          Sí           |         No          |
      | Veredicta          |        No        |  Sí   |    No     |          Sí           |         No          |
      | Lexium             |        No        |  Sí   |    No     |          Sí           |         No          |
      | AgentsCourt        |        Sí        |  No   |    Sí     |          No           |         No          |
      | *Presente trabajo* |       *Sí*       | *Sí*  |   *Sí*    |         *Sí*          |        *Sí*         |
    ],
  ),
  caption: [Comparación del presente trabajo con sistemas y trabajos relacionados],
) <tab:comparacion_trabajos>

La columna *RAG* indica si el sistema declara emplear recuperación aumentada como parte de su arquitectura; *Agentes*, si declara componentes agénticos (planificación, uso autónomo de herramientas o coordinación entre agentes); y *Benchmark abierto*, si publica el conjunto de evaluación con el que mide su desempeño de modo que un tercero pueda reproducir la medición. Para las plataformas comerciales (Westlaw CoCounsel, Lexis+ Protégé, vLex Vincent AI, Lexius, Juztina, Veredicta y Lexium) la clasificación se basa en la documentación pública, las notas de producto y el material de difusión disponibles al momento de la revisión (segundo semestre de 2025), dado que ninguna de ellas publica su arquitectura ni sus artefactos de evaluación: en consecuencia, las categorías reflejan lo que cada proveedor declara o describe públicamente y no una verificación independiente del sistema, limitación que se extiende a plataformas cuya implementación puede haber cambiado con posterioridad. Para los sistemas de código abierto (AgentsCourt y el presente trabajo) la clasificación se basa en el código y la documentación publicados. Infoleg/SAIJ se incluye como referencia del estado previo —búsqueda léxica sobre normativa argentina, sin componentes de IA— y por ello no aplica la categoría de código abierto (N/A).

=== Diferencias Metodológicas y Contribuciones Originales

El presente trabajo se diferencia de los trabajos y sistemas revisados en los siguientes aspectos:

+ *Código abierto*: A diferencia de las plataformas comerciales (Lexius, Juztina, Veredicta, Lexium, Westlaw, Lexis+, vLex), el sistema propuesto es de código abierto, con toda la documentación y el código disponible en un repositorio público, permitiendo su replicación y adaptación por cualquier organización.

+ *Enfoque integral Agentic-RAG sobre normativa argentina*: Si bien existen plataformas comerciales que ofrecen funcionalidades de IA sobre normativa argentina, ninguna de las identificadas publica su arquitectura ni permite evaluar independientemente su desempeño. El presente trabajo documenta de manera completa y trasparente la arquitectura Agentic-RAG empleada.

+ *Benchmark específico*: No se han identificado benchmarks públicos para evaluar sistemas de consulta sobre normativa argentina. El desarrollo de un benchmark para el Código de Minería Argentino, elaborado con asistencia de LLM y revisado por una profesional del derecho, constituye una contribución original que permite la evaluación reproducible del sistema.

+ *Dominio del derecho civil en español*: La mayoría de los benchmarks y trabajos académicos revisados se concentran en el common law anglosajón. El presente trabajo contribuye al subrepresentado dominio del derecho civil argentino en idioma español, complementando los esfuerzos de modelos como MEL @betancur2025mel y recursos como Legal-ES @samy2020legales.

+ *Evaluación comparativa de estrategias*: El trabajo evalúa y compara tres estrategias (sin RAG, RAG básico y Agentic-RAG) sobre el mismo corpus y benchmark, permitiendo cuantificar el valor agregado de cada componente de la arquitectura.

== Desarrollos Posteriores al Período Experimental

El ritmo de evolución del campo de la inteligencia artificial implicó que, entre la finalización de los experimentos (segundo semestre de 2025) y la redacción final de este manuscrito, se produjeran avances significativos. Esta sección documenta los desarrollos más relevantes organizados en tres ejes: modelos de lenguaje propietarios, modelos de código abierto y _frameworks_ agénticos. Las @fig:timeline_desarrollos_1, @fig:timeline_desarrollos_2, @fig:timeline_desarrollos_3 y @fig:timeline_desarrollos_4 presentan líneas de tiempo con los principales hitos.

#import "@preview/zeitline:0.1.1": timeline

#let eventos_propietarios_2025 = (
  (date: "2025-11-12", desc: [OpenAI lanza GPT-5.1 (Instant y Thinking), con razonamiento adaptativo y tono más cálido @openai_gpt5_1.]),
  (date: "2025-11-18", desc: [Google lanza Gemini 3 Pro, su modelo más inteligente hasta la fecha, con razonamiento de nivel de doctorado y ventana de 1M de tokens @google_gemini3.]),
  (date: "2025-11-24", desc: [Anthropic presenta Claude Opus 4.5, con el nuevo parámetro _effort_ y reducción del 67\% en precio @anthropic_opus4_5.]),
  (date: "2025-12-11", desc: [OpenAI lanza GPT-5.2, enfocado en trabajo profesional de conocimiento @openai_gpt5_2.]),
)

#let eventos_propietarios_2026 = (
  (date: "2026-02-05", desc: [Anthropic lanza Claude Opus 4.6, con ventana de contexto de 1M de tokens y _Agent Teams_ en Claude Code @anthropic_opus4_6.]),
  (date: "2026-02-17", desc: [Anthropic presenta Claude Sonnet 4.6, con rendimiento cercano a Opus a un costo significativamente menor @anthropic_sonnet4_6.]),
  (date: "2026-02-19", desc: [Google lanza Gemini 3.1 Pro, líder en 13 de 16 benchmarks principales @google_gemini3_1.]),
  (date: "2026-03-05", desc: [OpenAI lanza GPT-5.4, primer modelo general con capacidades nativas de _computer use_ y 1M de tokens de contexto @openai_gpt5_4.]),
  (date: "2026-04-16", desc: [Anthropic lanza Claude Opus 4.7, con visión de alta resolución y nivel de esfuerzo _xhigh_ @anthropic_opus4_7.]),
  (date: "2026-04-23", desc: [OpenAI lanza GPT-5.5, modelo frontera con rendimiento líder en codificación y razonamiento @openai_gpt5_5.]),
  (date: "2026-05-28", desc: [Anthropic presenta Claude Opus 4.8, con _Dynamic Workflows_ y 4 veces menos probabilidad de pasar errores de código @anthropic_opus4_8.]),
  (date: "2026-06-09", desc: [Anthropic lanza Claude Fable 5 y Mythos 5, primera generación Claude 5 con la nueva clase Mythos por encima de Opus @anthropic_fable5.]),
)

#let eventos_abiertos_frameworks_1 = (
  (date: "2025-12", desc: [DeepSeek lanza DeepSeek-V3.2, modelo MoE de 671B parámetros con rendimiento comparable a GPT-5 a una fracción del costo @deepseek_v3_2.]),
  (date: "2026-01", desc: [Microsoft fusiona AutoGen y Semantic Kernel en el _Microsoft Agent Framework_ unificado @microsoft_agent_framework.]),
  (date: "2026-01", desc: [Mastra, _framework_ agéntico TypeScript, alcanza versión 1.0 con más de 1.77M de descargas mensuales @mastra_1_0.]),
  (date: "2026-02-16", desc: [Alibaba lanza Qwen 3.5, modelo de 397B parámetros (17B activos) bajo licencia Apache 2.0 @qwen3_5.]),
  (date: "2025-04-05", desc: [Meta publica Llama 4 (Scout y Maverick), con arquitectura MoE y capacidades multimodales @llama4.]),
  (date: "2026-03", desc: [Google contribuye con Gemma 4, modelos compactos (hasta 26B) bajo licencia Apache 2.0 @gemma4.]),
  (date: "2026-04-20", desc: [Moonshot AI lanza Kimi K2.6, modelo MoE de 1T parámetros (32B activos) con _Agent Swarm_ de hasta 300 subagentes @kimi_k2_6.]),
  (date: "2026-04-24", desc: [DeepSeek lanza V4-Pro y V4-Flash, modelos MoE con atención híbrida (CSA+HCA), 1M de contexto y licencia MIT @deepseek_v4.]),
)

#let eventos_abiertos_frameworks_2 = (
  (date: "2026-06-01", desc: [MiniMax lanza M3, modelo MoE con atención dispersa (MSA), 1M de contexto y capacidades multimodales nativas @minimax_m3.]),
  (date: "2026-06-12", desc: [Moonshot AI lanza Kimi K2.7-Code, con 30\% menos _tokens_ de razonamiento y mejoras en tareas de codificación @kimi_k2_7_code.]),
  (date: "2026-06-13", desc: [Zhipu AI (Z.ai) lanza GLM-5.2, modelo MoE de 744B parámetros con 1M de contexto y licencia MIT @glm_5_2.]),
)

=== Modelos Propietarios de Nueva Generación

En un lapso de apenas doce días en noviembre de 2025, los tres principales laboratorios de IA lanzaron nuevos modelos insignia: OpenAI publicó GPT-5.1 (12 de noviembre), que introdujo razonamiento adaptativo donde el modelo decide autónomamente cuánto tiempo de "pensamiento" asignar a cada consulta @openai_gpt5_1; Google lanzó Gemini 3 Pro (18 de noviembre), que alcanzó el primer puesto en múltiples _benchmarks_ académicos con una ventana de contexto de un millón de _tokens_ @google_gemini3; y Anthropic presentó Claude Opus 4.5 (24 de noviembre), con el nuevo parámetro _effort_ para balancear capacidad y costo @anthropic_opus4_5.

La cadencia se aceleró en los meses siguientes. OpenAI iteró rápidamente con GPT-5.2 (diciembre de 2025) @openai_gpt5_2, GPT-5.4 estándar (5 de marzo de 2026) @openai_gpt5_4 y las variantes GPT-5.4 mini y nano (17 de marzo de 2026). Anthropic respondió con Claude Opus 4.6 (5 de febrero de 2026) @anthropic_opus4_6 y Sonnet 4.6 (17 de febrero de 2026) @anthropic_sonnet4_6, donde Sonnet 4.6 alcanzó rendimiento cercano a Opus a un costo significativamente menor. Google presentó Gemini 3.1 Pro (19 de febrero de 2026) @google_gemini3_1, que lideró 13 de 16 _benchmarks_ principales y empató con GPT-5.4 Pro en el índice de inteligencia de Artificial Analysis a aproximadamente un tercio del costo de API. xAI lanzó Grok 4.20 (febrero--marzo de 2026), notable por introducir una arquitectura multi-agente novedosa.

La competencia se intensificó en el segundo trimestre de 2026. Anthropic lanzó Claude Opus 4.7 (16 de abril) @anthropic_opus4_7, con visión de alta resolución y un nuevo nivel de esfuerzo _xhigh_. OpenAI contraatacó con GPT-5.5 (23 de abril) @openai_gpt5_5, estableciendo un nuevo estado del arte en codificación y razonamiento. Anthropic continuó con Claude Opus 4.8 (28 de mayo) @anthropic_opus4_8, que introdujo _Dynamic Workflows_ con cientos de subagentes paralelos y redujo cuatro veces la probabilidad de pasar errores de código inadvertidos. Finalmente, Anthropic lanzó Claude Fable 5 y Mythos 5 (9 de junio) @anthropic_fable5, la primera generación Claude 5 con la nueva clase Mythos por encima de Opus, aunque el acceso a estos modelos fue suspendido días después por una directiva de control de exportaciones del gobierno de Estados Unidos.

El dato más revelador del período es la densidad de lanzamientos: solo en el primer trimestre de 2026 se registraron más de 255 lanzamientos de modelos por parte de organizaciones relevantes, con siete modelos de frontera publicados únicamente en febrero de 2026.

#figure(
  placement: top,
  timeline(
    eventos_propietarios_2025,
    theme: (
      colors: (
        accent: rgb("#0050b3"),
        muted: rgb("#555555"),
        line:  rgb("#aaaaaa"),
      ),
      sizes: (
        date: 10pt,
        body: 8.5pt,
        dot: 5pt,
        line-width: 2.5pt,
      ),
      spacing: (
        row: 1.2em,
        arm:  2.4em,
      ),
    ),
  ),
  caption: [Línea de tiempo de los principales desarrollos en modelos de lenguaje propietarios durante 2025.],
) <fig:timeline_desarrollos_1>

#figure(
  placement: top,
  timeline(
    eventos_propietarios_2026,
    theme: (
      colors: (
        accent: rgb("#0050b3"),
        muted: rgb("#555555"),
        line:  rgb("#aaaaaa"),
      ),
      sizes: (
        date: 10pt,
        body: 8.5pt,
        dot: 5pt,
        line-width: 2.5pt,
      ),
      spacing: (
        row: 1.2em,
        arm:  2.4em,
      ),
    ),
  ),
  caption: [Línea de tiempo de los principales desarrollos en modelos de lenguaje propietarios durante 2026.],
) <fig:timeline_desarrollos_2>

=== Modelos de Código Abierto y Razonamiento

Uno de los desarrollos más disruptivos del período fue la irrupción de modelos de código abierto con capacidades competitivas frente a los modelos propietarios, lo que alteró fundamentalmente la dinámica del mercado de IA.

*DeepSeek* captó la atención global con dos lanzamientos clave: DeepSeek-V3.2 (diciembre de 2025), un modelo de 671B parámetros con arquitectura _Mixture-of-Experts_ (MoE, 37B activos) que alcanzó rendimiento comparable a GPT-5 en razonamiento a una fracción del costo de entrenamiento (aproximadamente \$6 millones frente a más de \$100 millones estimados para modelos propietarios equivalentes); y DeepSeek-R1 (enero de 2025), un modelo de razonamiento entrenado con aprendizaje por refuerzo a gran escala que demostró capacidades a nivel de GPT-4 en tareas de razonamiento complejo. DeepSeek-R1 introdujo además una familia de modelos destilados (_DeepSeek-R1-Distill_) basados en arquitecturas Qwen y Llama, diseñados para entornos de producción con restricciones de cómputo.

*DeepSeek* continuó su avance con DeepSeek-V4 (abril de 2026) @deepseek_v4, presentado en dos variantes: V4-Pro (1.6T parámetros totales, 49B activos) y V4-Flash (284B totales, 13B activos), ambos con ventana de contexto de 1M de _tokens_ y licencia MIT. V4 incorpora una arquitectura de atención híbrida que combina _Compressed Sparse Attention_ (CSA) y _Heavily Compressed Attention_ (HCA), reduciendo los FLOPs de inferencia al 27\% y la _KV cache_ al 10\% respecto a V3.2 en contexto de 1M de _tokens_. En _benchmarks_ de codificación, V4-Pro alcanzó 80.6\% en SWE-Bench Verified y 93.5\% en LiveCodeBench, posicionándose como el modelo de código abierto más fuerte en tareas de ingeniería de _software_.

*Qwen* (Alibaba) avanzó desde Qwen3 (abril de 2025) @qwen2025qwen3 hasta Qwen 3.5 (16 de febrero de 2026), un modelo de 397B parámetros totales con 17B activos por paso de inferencia, licenciado bajo Apache 2.0 @qwen3_5. Qwen 3.5 se posicionó como líder en tareas de visión, seguimiento de instrucciones y comprensión multimodal, áreas directamente relevantes para aplicaciones de producción.

*Meta* publicó Llama 4 en abril de 2025 con las variantes Scout (109B totales/17B activos) y Maverick (400B totales/17B activos), ambas con arquitectura MoE, capacidades multimodales y contexto extendido @llama4. *Google* contribuyó con Gemma 4, una familia de modelos compactos (hasta 26B parámetros) con licencia Apache 2.0, donde el modelo de 9B parámetros alcanzó un 81.7\% en GPQA Diamond, superando a modelos de código abierto hasta 13 veces más grandes @gemma4.

*Moonshot AI* emergió como un competidor relevante con Kimi K2.6 (abril de 2026) @kimi_k2_6, un modelo MoE de 1 billón de parámetros totales (32B activos) con ventana de contexto de 256K _tokens_ y un sistema _Agent Swarm_ capaz de orquestar hasta 300 subagentes ejecutando 4.000 pasos coordinados simultáneamente. K2.6 alcanzó 58.6\% en SWE-Bench Pro, superando a GPT-5.4 en esta métrica de referencia para tareas de ingeniería de _software_. Poco después, Moonshot lanzó Kimi K2.7-Code (junio de 2026) @kimi_k2_7_code, una versión optimizada que reduce en aproximadamente un 30\% los _tokens_ de razonamiento necesarios por tarea, manteniendo la misma arquitectura de 1T parámetros.

*MiniMax* presentó M3 (junio de 2026) @minimax_m3, un modelo que combina por primera vez en un peso abierto tres capacidades de frontera: codificación de nivel competitivo (59.0\% en SWE-Bench Pro, superando a GPT-5.5), una ventana de contexto de 1M de _tokens_ gracias a su novedosa arquitectura de atención dispersa (MSA), y capacidades multimodales nativas (imagen y video). Su precio de API (\$0.30 por millón de _tokens_ de entrada) representa una fracción del costo de los modelos propietarios equivalentes.

*Zhipu AI* (Z.ai) lanzó GLM-5.2 (junio de 2026) @glm_5_2, un modelo MoE de 744B parámetros totales (~40B activos) con ventana de contexto de 1M de _tokens_, licencia MIT y dos modos de razonamiento seleccionables (High y Max). GLM-5.2 se posicionó como el modelo de código abierto más fuerte en codificación, alcanzando 81.0 en Terminal-Bench 2.1 y 62.1 en SWE-Bench Pro, con un rendimiento cercano a Claude Opus 4.8 en tareas de horizonte largo.

El resultado neto es que, para mediados de 2026, la brecha de rendimiento entre modelos de código abierto y propietarios se ha reducido sustancialmente. Análisis independientes sugieren que para aproximadamente el 80\% de tareas empresariales comunes (clasificación, extracción, resumen, traducción), los modelos abiertos ofrecen rendimiento comparable a un costo significativamente menor.

#figure(
  placement: top,
  timeline(
    eventos_abiertos_frameworks_1,
    theme: (
      colors: (
        accent: rgb("#0050b3"),
        muted: rgb("#555555"),
        line:  rgb("#aaaaaa"),
      ),
      sizes: (
        date: 10pt,
        body: 8.5pt,
        dot: 5pt,
        line-width: 2.5pt,
      ),
      spacing: (
        row: 1.2em,
        arm:  2.4em,
      ),
    ),
  ),
  caption: [Línea de tiempo de los principales desarrollos en modelos de código abierto y _frameworks_ agénticos (diciembre de 2025 a abril de 2026).],
) <fig:timeline_desarrollos_3>

#figure(
  placement: top,
  timeline(
    eventos_abiertos_frameworks_2,
    theme: (
      colors: (
        accent: rgb("#0050b3"),
        muted: rgb("#555555"),
        line:  rgb("#aaaaaa"),
      ),
      sizes: (
        date: 10pt,
        body: 8.5pt,
        dot: 5pt,
        line-width: 2.5pt,
      ),
      spacing: (
        row: 1.2em,
        arm:  2.4em,
      ),
    ),
  ),
  caption: [Línea de tiempo de los principales desarrollos en modelos de código abierto y _frameworks_ agénticos durante junio de 2026 (continuación).],
) <fig:timeline_desarrollos_4>

=== Implicaciones para el Presente Trabajo

Estos desarrollos tienen implicaciones directas para la interpretación de los resultados de esta tesis. En primer lugar, el hallazgo de la sobrecarga agéntica observada en modelos de menor capacidad (gpt-5-nano) podría no reproducirse con los modelos de razonamiento de nueva generación (DeepSeek-R1, Gemini 3.1 Pro, Claude Opus 4.8), que integran cadenas de pensamiento explícitas capaces de gestionar instrucciones complejas de manera más efectiva. En segundo lugar, la disponibilidad de modelos de código abierto competitivos con las APIs propietarias (Kimi K2.7-Code, MiniMax M3, GLM-5.2) abre la posibilidad de eliminar la dependencia de APIs comerciales identificada como limitación del sistema, habilitando despliegues locales relevantes para entornos donde la confidencialidad de las consultas legales sea un requisito. Por último, la maduración de los _frameworks_ agénticos (Microsoft Agent Framework, Mastra) simplificaría una futura reimplementación del sistema multi-agente, potencialmente mejorando la eficiencia y modularidad de la arquitectura.

La inclusión de estos desarrollos en el análisis comparativo requeriría experimentación adicional fuera del alcance del presente trabajo; no obstante, la metodología propuesta ---diseño factorial, _benchmark_ específico y evaluación LLM-as-a-Judge--- es directamente aplicable a futuras generaciones de modelos sin modificaciones sustanciales.

== Conclusiones del Capítulo

La revisión de la literatura y de las plataformas existentes evidencia un crecimiento acelerado en la integración de IA al dominio legal, tanto en el ámbito comercial como académico. Las grandes plataformas internacionales (Westlaw, LexisNexis, vLex) han evolucionado desde buscadores por palabras clave hacia sistemas agénticos con RAG, mientras que en Latinoamérica plataformas como Lexius, Juztina, Veredicta y Lexium están adoptando tecnologías similares adaptadas al contexto regional.

Sin embargo, se identifican vacíos significativos: (1) la ausencia de sistemas de código abierto que permitan la evaluación independiente y la replicación de resultados en el ámbito legal argentino; (2) la falta de benchmarks específicos para normativa argentina; y (3) la subrepresentación del español y del derecho civil en la investigación académica sobre NLP legal. El presente trabajo se posiciona en la intersección de estos vacíos, proponiendo un sistema Agentic-RAG de código abierto para el Código de Minería Argentino, acompañado de un benchmark específico que permite su evaluación reproducible.

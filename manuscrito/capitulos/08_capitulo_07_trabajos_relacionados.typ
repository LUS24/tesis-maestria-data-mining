= Trabajos Relacionados

#import "@preview/tablem:0.3.0": three-line-table

== Introducción

El presente capítulo revisa los trabajos previos y las plataformas existentes que guardan relación con el sistema Agentic-RAG propuesto en este trabajo final. La revisión se organiza en cuatro ejes: sistemas de búsqueda legal (tanto tradicionales como asistidos por inteligencia artificial), aplicaciones de RAG en dominios especializados con énfasis en el ámbito jurídico, sistemas agénticos y su integración con RAG, y benchmarks para la evaluación de sistemas de procesamiento de lenguaje natural en el dominio legal. Finalmente, se presenta una comparación del presente trabajo con la literatura analizada, identificando las contribuciones originales.

== Sistemas de Búsqueda Legal

=== Sistemas Tradicionales Basados en Palabras Clave

Los sistemas de consulta legal más establecidos en Argentina operan mediante búsquedas basadas en coincidencia de palabras clave, filtros por tipo de norma, jurisdicción y fecha.

*Infoleg* @infoleg2025 es una base de datos legislativa nacional de acceso libre y gratuito, administrada por la Dirección Nacional del Sistema Argentino de Información Jurídica del Ministerio de Justicia de la Nación. Contiene leyes, decretos, decisiones administrativas, resoluciones, disposiciones y todo acto cuya publicación sea obligatoria en la primera sección del Boletín Oficial de la República Argentina. Sus contenidos están licenciados bajo Creative Commons Reconocimiento 2.5 Argentina.

*SAIJ* (Sistema Argentino de Información Jurídica) @saij2025 es un servicio de la Dirección Nacional del SAIJ, dependiente del Ministerio de Justicia y Derechos Humanos de la Nación. Fundado en 1981 con apoyo de la UNESCO, incluye todas las leyes nacionales sancionadas desde 1853, tratados internacionales, decretos nacionales y provinciales, jurisprudencia de tribunales federales, nacionales y provinciales, proyectos legislativos, dictámenes de la Procuración del Tesoro de la Nación, artículos de doctrina y publicaciones de Ediciones SAIJ. Su motor de búsqueda permite filtrar por tipo de contenido (legislación, fallos, sumarios, doctrina), tipo de norma (ley, decreto, resolución, disposición), jurisdicción y fecha.

A nivel internacional, plataformas como *Westlaw* @westlaw2025 y *LexisNexis* @lexisplus2025 han sido durante décadas los referentes en investigación legal, operando inicialmente con motores de búsqueda por palabras clave sobre extensas bases de datos de jurisprudencia y legislación, principalmente de Estados Unidos y otros países anglosajones.

Si bien estos sistemas cumplen una función esencial al garantizar el acceso a la información jurídica, su dependencia de la coincidencia exacta de términos limita su capacidad para comprender la semántica de las consultas, lo que frecuentemente produce resultados irrelevantes o incompletos cuando el usuario no emplea los términos técnicos precisos.

=== Sistemas Comerciales con IA

En los últimos años, múltiples plataformas comerciales han integrado inteligencia artificial para mejorar la búsqueda y el análisis jurídico. A continuación se describen las más relevantes.

*Lexis+ con Protégé* @lexisplus2025 es la evolución de la plataforma de LexisNexis que integra un asistente de IA agéntico denominado Protégé. Este sistema es capaz de completar tareas de forma autónoma, revisar su propio trabajo y sugerir mejoras. Entre sus capacidades se incluyen la redacción de documentos legales (mociones, demandas, memorandos), la investigación legal con validación de citas mediante Shepard's, el análisis de documentos de hasta 300 páginas y la generación de cronologías a partir de materiales cargados. En agosto de 2025, LexisNexis incorporó Protégé General AI, que provee acceso seguro a múltiples modelos de IA de propósito general (GPT-5, Claude Sonnet 4, GPT-4o) junto con herramientas de IA específicas para el dominio legal. La plataforma emplea una arquitectura RAG con integración del grafo de conocimiento Shepard's (GraphRAG) para generar respuestas fundamentadas en fuentes verificables.

*Westlaw con CoCounsel* @westlaw2025 es la plataforma de Thomson Reuters que lanzó CoCounsel Legal en agosto de 2025, representando su oferta más avanzada de IA. Integrada con Westlaw Advantage, incluye la funcionalidad Deep Research, que en lugar de devolver simplemente resultados de búsqueda, razona a través de preguntas legales, genera planes de investigación de múltiples pasos, explica su lógica y entrega informes completos fundamentados en el contenido de Westlaw y Practical Law. La tecnología se basa en los desarrollos de CoCounsel, construidos sobre GPT-4. Un estudio de la Universidad de Stanford publicado en el Journal of Empirical Legal Studies en 2025 encontró que Westlaw AI presentaba alucinaciones en el 33\% de las consultas, mientras que Lexis+ AI lo hacía en el 17\%, en comparación con el 43\% de GPT-4 sin RAG @dahan2024stanford.

*vLex con Vincent AI* @vlex2025 es una plataforma de inteligencia legal generativa que combina una de las mayores bases de datos legales a nivel global —con más de mil millones de documentos de más de 100 países— con IA avanzada. Vincent AI interpreta consultas en lenguaje natural para producir respuestas legales con citas completas, generar argumentos legales, comparar leyes entre jurisdicciones y automatizar flujos de trabajo complejos. En ensayos controlados aleatorizados, Vincent mostró 3,67 veces más fiabilidad que los LLM de propósito general. La plataforma emplea búsqueda vectorial (machine learning) para organizar documentos mediante búsqueda conceptual en lugar de coincidencia de palabras clave. Su alcance internacional, que incluye cobertura de Estados Unidos, Reino Unido, España, la Unión Europea, Singapur, México, Chile, Nueva Zelanda y Colombia, lo diferencia de sus competidores.

*Lexius* @lexius2025 es un sistema jurídico con IA de origen latinoamericano que opera en 18 países. En Argentina cuenta con acceso a más de 32.500 textos legales y 52.500 sentencias. Su motor de búsqueda inteligente identifica la intención de la consulta del usuario y ofrece funcionalidades como chat y llamadas con IA para resolver dudas legales, generación de video podcasts legales narrados por IA, mapas mentales interactivos y exportación de documentos en múltiples formatos.

*Juztina* @juztina2025 es una legaltech peruana que utiliza inteligencia artificial para democratizar el acceso a información jurídica en América Latina. Su plataforma ofrece un chat de IA con acceso a más de 3 millones de documentos legales, permitiendo a abogados y usuarios realizar búsquedas especializadas de jurisprudencia, normativa y doctrina. Con presencia en Perú, Colombia y México, Juztina ha expandido su operación a Argentina. La búsqueda de información empleando la plataforma toma de diez segundos a un minuto, reduciendo significativamente los tiempos de investigación legal.

*Veredicta* @veredicta2025 es una plataforma argentina que integra gestión de expedientes con IA. Su motor de búsqueda semántica analiza más de 500.000 fuentes judiciales argentinas, permite buscar describiendo el caso en lenguaje natural, genera resúmenes automáticos de fallos y está integrado con el Poder Judicial de la Nación (PJN), expedientes y WhatsApp. A diferencia de herramientas como Lexius o Juztina, Veredicta permite encontrar jurisprudencia y vincularla directamente al expediente en curso.

*Lexium* @lexium2025 es una plataforma de IA de gestión jurídica especializada en derecho argentino. Ofrece búsqueda inteligente en SAIJ, Infoleg y jurisprudencia, automatización de escritos y gestión de vencimientos procesales. La propia plataforma reconoce las limitaciones inherentes a los modelos de IA generativa, incluyendo la posibilidad de generar información incompleta, imprecisa o no actualizada con la legislación vigente, recomendando verificar siempre las fuentes oficiales.

En Argentina también se destaca el sistema de *Búsqueda de Jurisprudencia Asistida por IA* del Tribunal Fiscal de la Nación @tribunalfiscal2025 @worldlawgroup2025, que constituye una de las primeras iniciativas gubernamentales en el país en incorporar inteligencia artificial a la búsqueda de documentos legales, aunque limitado a documentos emitidos por dicho tribunal.

== Sistemas RAG en Dominios Especializados

=== RAG para el Dominio Legal

La aplicación de RAG al dominio legal ha sido objeto de creciente investigación. Hindi et al. @hindi2025legalrag presentaron una revisión exhaustiva sobre la precisión e interpretabilidad de los sistemas RAG en tecnología legal, identificando que la combinación de recuperación semántica con generación de texto permite anclar las respuestas en documentos reales, reduciendo significativamente las alucinaciones en comparación con el uso de LLMs sin RAG. La revisión cataloga diversos métodos y aplicaciones de RAG legal, incluyendo análisis de contratos, protección de privacidad y evaluación de sistemas mediante LegalBench-RAG @pipitone2024legalbench.

Siino et al. @siino2025legal realizaron una revisión de la literatura sobre aplicaciones de LLMs en el ámbito legal, cubriendo tareas como clasificación de textos legales, reconocimiento de entidades nombradas, resumidización de documentos y respuesta a preguntas legales. Los autores identifican que si bien los avances son significativos, la mayoría de los trabajos se concentran en el idioma inglés y en los sistemas jurídicos del common law, dejando subrepresentados los sistemas de derecho civil como el argentino.

LexisNexis incorporó a su plataforma Lexis+ AI mejoras en su pipeline de RAG, incluyendo la integración del grafo de conocimiento Shepard's (GraphRAG), que utiliza información de relaciones entre casos para generar respuestas más completas y autoritativas.

A nivel académico, se han desarrollado sistemas como JusBuild, que emplea un modelo de campos aleatorios condicionales (CRF) para la segmentación supervisada de documentos legales en secciones funcionales, una base de datos vectorial para almacenar representaciones semánticas y RAG con LLMs para sugerir secciones relevantes durante la redacción de documentos legales.

=== RAG para Documentación Técnica y Otros Dominios

Los sistemas RAG han encontrado aplicaciones significativas en múltiples dominios especializados más allá del legal. En el ámbito médico, una revisión narrativa publicada en PubMed Central @gao2023retrieval exploró la aplicación de RAG en contextos médicos, identificando su utilidad para soporte en decisiones clínicas, asistencia diagnóstica, interpretación de guías médicas y evaluación de elegibilidad para ensayos clínicos. Un estudio publicado en npj Digital Medicine evaluó modelos LLM-RAG para determinar la aptitud quirúrgica utilizando 35 guías locales y 23 internacionales, demostrando que RAG permite personalizar LLMs integrando conocimiento especializado con mayor precisión y consistencia que los modelos base.

En el ámbito financiero, se han explorado aplicaciones de RAG para la recuperación y consulta de documentación regulatoria, reportes financieros y normativa contable @srinivasan2025financial. En contextos de gobernanza electrónica, se ha evaluado la fidelidad de sistemas Agentic-RAG utilizando frameworks de evaluación basados en LLM-as-a-Judge con múltiples modelos evaluadores.

Estos trabajos demuestran que la arquitectura RAG es transferible entre dominios especializados, y que las técnicas de fragmentación de texto, embeddings semánticos y recuperación por similitud desarrolladas en un dominio pueden informar el diseño de sistemas en otros.

== Sistemas Agénticos

=== Agentes para Tareas Legales

La aplicación de agentes basados en LLM al dominio legal ha sido revisada de forma comprehensiva por Wan et al. @wan2025legalagents, quienes trazan la evolución desde sistemas de agente único hacia arquitecturas multi-agente. Los autores identifican que los agentes legales pueden clasificarse según sus capacidades: consulta legal, análisis de documentos, asistencia en litigios y simulación judicial.

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

*LEXTREME* @niklaus2024lextreme es el primer benchmark multilingüe y multi-tarea para el dominio legal, cubriendo 24 idiomas indoeuropeos y urálicos a través de 11 datasets. Sus resultados muestran que incluso los mejores modelos de referencia alcanzan resultados modestos, y que ChatGPT enfrenta dificultades con muchas tareas, evidenciando la brecha entre los modelos de propósito general y las necesidades del dominio legal especializado.

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
    columns: (1.2fr, 0.7fr, 0.7fr, 0.7fr, 0.7fr, 0.7fr),
    [
      | *Sistema/Trabajo*  | *Código abierto* | *RAG* | *Agentes* | *Normativa argentina* | *Benchmark propio* |
      | :----------------- | :--------------: | :---: | :-------: | :-------------------: | :----------------: |
      | Infoleg / SAIJ     |       N/A        |  No   |    No     |          Sí           |         No         |
      | Westlaw CoCounsel  |        No        |  Sí   |    Sí     |          No           |         No         |
      | Lexis+ Protégé     |        No        |  Sí   |    Sí     |          No           |         No         |
      | vLex Vincent AI    |        No        |  Sí   |    Sí     |        Parcial        |         No         |
      | Lexius             |        No        |  Sí   |    Sí     |          Sí           |         No         |
      | Juztina            |        No        |  Sí   |    Sí     |          Sí           |         No         |
      | Veredicta          |        No        |  Sí   |    No     |          Sí           |         No         |
      | Lexium             |        No        |  Sí   |    No     |          Sí           |         No         |
      | AgentsCourt        |        Sí        |  No   |    Sí     |          No           |         No         |
      | *Presente trabajo* |       *Sí*       | *Sí*  |   *Sí*    |         *Sí*          |        *Sí*        |
    ],
  ),
  caption: [Comparación del presente trabajo con sistemas y trabajos relacionados],
) <tab:comparacion_trabajos>

=== Diferencias Metodológicas y Contribuciones Originales

El presente trabajo se diferencia de los trabajos y sistemas revisados en los siguientes aspectos:

+ *Código abierto*: A diferencia de las plataformas comerciales (Lexius, Juztina, Veredicta, Lexium, Westlaw, Lexis+, vLex), el sistema propuesto es de código abierto, con toda la documentación y el código disponible en un repositorio público, permitiendo su replicación y adaptación por cualquier organización.

+ *Enfoque integral Agentic-RAG sobre normativa argentina*: Si bien existen plataformas comerciales que ofrecen funcionalidades de IA sobre normativa argentina, ninguna de las identificadas publica su arquitectura ni permite evaluar independientemente su desempeño. El presente trabajo documenta de manera completa y trasparente la arquitectura Agentic-RAG empleada.

+ *Benchmark específico*: No se han identificado benchmarks públicos para evaluar sistemas de consulta sobre normativa argentina. El desarrollo de un benchmark para el Código de Minería Argentino, elaborado con profesionales del derecho, constituye una contribución original que permite la evaluación reproducible del sistema.

+ *Dominio del derecho civil en español*: La mayoría de los benchmarks y trabajos académicos revisados se concentran en el common law anglosajón. El presente trabajo contribuye al subrepresentado dominio del derecho civil argentino en idioma español, complementando los esfuerzos de modelos como MEL @betancur2025mel y recursos como Legal-ES @samy2020legales.

+ *Evaluación comparativa de estrategias*: El trabajo evalúa y compara tres estrategias (sin RAG, RAG básico y Agentic-RAG) sobre el mismo corpus y benchmark, permitiendo cuantificar el valor agregado de cada componente de la arquitectura.

== Desarrollos Posteriores al Período Experimental

El ritmo de evolución del campo de la inteligencia artificial implicó que, entre la finalización de los experimentos (segundo semestre de 2025) y la redacción final de este manuscrito, se produjeran avances significativos. Esta sección documenta los desarrollos más relevantes organizados en tres ejes: modelos de lenguaje propietarios, modelos de código abierto y _frameworks_ agénticos. La @fig:timeline_desarrollos presenta una línea de tiempo con los principales hitos.

#figure(
  image("../media/timeline_desarrollos_posteriores.svg", width: 85%),
  caption: [Línea de tiempo de los principales desarrollos en LLMs y Agentic-RAG entre noviembre de 2025 y abril de 2026, período posterior a la finalización de los experimentos de este trabajo.],
) <fig:timeline_desarrollos>

=== Modelos Propietarios de Nueva Generación

En un lapso de apenas doce días en noviembre de 2025, los tres principales laboratorios de IA lanzaron nuevos modelos insignia: OpenAI publicó GPT-5.1 (12 de noviembre), que introdujo razonamiento adaptativo donde el modelo decide autónomamente cuánto tiempo de "pensamiento" asignar a cada consulta; Google lanzó Gemini 3 Pro (20 de noviembre), que alcanzó el primer puesto en múltiples _benchmarks_ académicos con una ventana de contexto de un millón de _tokens_; y Anthropic presentó Claude Opus 4.5 (24 de noviembre), con mejoras sustanciales en razonamiento avanzado.

La cadencia se aceleró en los meses siguientes. OpenAI iteró rápidamente con GPT-5.2 (diciembre de 2025), GPT-5.4 estándar (5 de marzo de 2026) y las variantes GPT-5.4 mini y nano (17 de marzo de 2026). Anthropic respondió con Claude Opus 4.6 y Sonnet 4.6 (febrero de 2026), donde Sonnet 4.6 alcanzó rendimiento cercano a Opus a un costo significativamente menor. Google presentó Gemini 3.1 Pro (19 de febrero de 2026), que lideró 13 de 16 _benchmarks_ principales y empató con GPT-5.4 Pro en el índice de inteligencia de Artificial Analysis a aproximadamente un tercio del costo de API. xAI lanzó Grok 4.20 (febrero--marzo de 2026), notable por introducir una arquitectura multi-agente novedosa.

El dato más revelador del período es la densidad de lanzamientos: solo en el primer trimestre de 2026 se registraron más de 255 lanzamientos de modelos por parte de organizaciones relevantes, con siete modelos de frontera publicados únicamente en febrero de 2026.

=== Modelos de Código Abierto y Razonamiento

Uno de los desarrollos más disruptivos del período fue la irrupción de modelos de código abierto con capacidades competitivas frente a los modelos propietarios, lo que alteró fundamentalmente la dinámica del mercado de IA.

*DeepSeek* captó la atención global con dos lanzamientos clave: DeepSeek-V3.2 (diciembre de 2025), un modelo de 671B parámetros con arquitectura _Mixture-of-Experts_ (MoE, 37B activos) que alcanzó rendimiento comparable a GPT-5 en razonamiento a una fracción del costo de entrenamiento (aproximadamente \$6 millones frente a más de \$100 millones estimados para modelos propietarios equivalentes); y DeepSeek-R1 (enero de 2026), un modelo de razonamiento entrenado con aprendizaje por refuerzo a gran escala que demostró capacidades a nivel de GPT-4 en tareas de razonamiento complejo. DeepSeek-R1 introdujo además una familia de modelos destilados (_DeepSeek-R1-Distill_) basados en arquitecturas Qwen y Llama, diseñados para entornos de producción con restricciones de cómputo.

*Qwen* (Alibaba) avanzó desde Qwen3 (diciembre de 2025) hasta Qwen 3.5 (16 de febrero de 2026), un modelo de 397B parámetros totales con 17B activos por paso de inferencia, licenciado bajo Apache 2.0. Qwen 3.5 se posicionó como líder en tareas de visión, seguimiento de instrucciones y comprensión multimodal, áreas directamente relevantes para aplicaciones de producción.

*Meta* publicó Llama 4 con las variantes Scout (109B totales/17B activos) y Maverick (400B totales/17B activos), ambas con arquitectura MoE, capacidades multimodales y contexto extendido, manteniendo la línea de modelos abiertos que ha catalizado el ecosistema de código abierto desde 2023. *Google* contribuyó con Gemma 4, una familia de modelos compactos (hasta 26B parámetros) con licencia Apache 2.0, donde el modelo de 9B parámetros alcanzó un 81.7\% en GPQA Diamond, superando a modelos de código abierto hasta 13 veces más grandes.

El resultado neto es que, para abril de 2026, la brecha de rendimiento entre modelos de código abierto y propietarios se ha reducido sustancialmente. Análisis independientes sugieren que para aproximadamente el 80\% de tareas empresariales comunes (clasificación, extracción, resumen, traducción), los modelos abiertos ofrecen rendimiento comparable a un costo significativamente menor.

=== _Frameworks_ Agénticos y Agentic-RAG

El ecosistema de _frameworks_ para construir sistemas agénticos y Agentic-RAG maduró considerablemente durante el período. Microsoft fusionó AutoGen y Semantic Kernel en el unificado Microsoft Agent Framework (enero de 2026), con disponibilidad general prevista para fines del primer trimestre de 2026. Mastra, un _framework_ agéntico basado en TypeScript, alcanzó la versión 1.0 (enero de 2026) y superó 1.77 millones de descargas mensuales en NPM. LangGraph consolidó su posición como herramienta de referencia para orquestación de flujos agénticos multi-paso, mientras que LlamaIndex se especializó en pipelines RAG de producción con soporte nativo para flujos agénticos.

En el ámbito de herramientas especializadas para RAG, RAGFlow evolucionó como motor de RAG de código abierto con soporte para GraphRAG y razonamiento agéntico. RAGAS se estableció como el estándar _de facto_ para evaluación de pipelines RAG, proporcionando métricas de relevancia, fidelidad y calidad de respuesta. AutoRAG introdujo la automatización de la optimización de pipelines RAG mediante experimentación sistemática.

Según proyecciones de Gartner, se espera que el 40\% de las aplicaciones empresariales incluyan agentes de IA específicos para tareas a fines de 2026, frente a menos del 5\% en 2025. El mercado global de agentes de IA pasó de \$5.4 mil millones en 2024 a \$7.6 mil millones en 2025, con proyecciones de alcanzar \$50 mil millones para 2030.

=== Implicaciones para el Presente Trabajo

Estos desarrollos tienen implicaciones directas para la interpretación de los resultados de esta tesis. En primer lugar, el hallazgo de la sobrecarga agéntica observada en modelos de menor capacidad (gpt-5-nano) podría no reproducirse con los modelos de razonamiento de nueva generación (DeepSeek-R1, Gemini 3.1 Pro), que integran cadenas de pensamiento explícitas capaces de gestionar instrucciones complejas de manera más efectiva. En segundo lugar, la disponibilidad de modelos de código abierto competitivos con las APIs propietarias abre la posibilidad de eliminar la dependencia de APIs comerciales identificada como limitación del sistema, habilitando despliegues locales relevantes para entornos donde la confidencialidad de las consultas legales sea un requisito. Por último, la maduración de los _frameworks_ agénticos simplificaría una futura reimplementación del sistema multi-agente, potencialmente mejorando la eficiencia y modularidad de la arquitectura.

La inclusión de estos desarrollos en el análisis comparativo requeriría experimentación adicional fuera del alcance del presente trabajo; no obstante, la metodología propuesta ---diseño factorial, _benchmark_ específico y evaluación LLM-as-a-Judge--- es directamente aplicable a futuras generaciones de modelos sin modificaciones sustanciales.

== Conclusiones del Capítulo

La revisión de la literatura y de las plataformas existentes evidencia un crecimiento acelerado en la integración de IA al dominio legal, tanto en el ámbito comercial como académico. Las grandes plataformas internacionales (Westlaw, LexisNexis, vLex) han evolucionado desde buscadores por palabras clave hacia sistemas agénticos con RAG, mientras que en Latinoamérica plataformas como Lexius, Juztina, Veredicta y Lexium están adoptando tecnologías similares adaptadas al contexto regional.

Sin embargo, se identifican vacíos significativos: (1) la ausencia de sistemas de código abierto que permitan la evaluación independiente y la replicación de resultados en el ámbito legal argentino; (2) la falta de benchmarks específicos para normativa argentina; y (3) la subrepresentación del español y del derecho civil en la investigación académica sobre NLP legal. El presente trabajo se posiciona en la intersección de estos vacíos, proponiendo un sistema Agentic-RAG de código abierto para el Código de Minería Argentino, acompañado de un benchmark específico que permite su evaluación reproducible.

// Resumen
#heading(outlined: false, numbering: none)[Resumen]

Presentamos el diseño, implementación y evaluación de un sistema de generación aumentada por recuperación agéntica (Agentic Retrieval-Augmented Generation, Agentic-RAG) de código abierto para la consulta del Código de Minería Argentino. El acceso a la normativa legal argentina está limitado por sistemas de búsqueda basados en coincidencias léxicas que no capturan la semántica del lenguaje jurídico, mientras que las herramientas avanzadas existentes son predominantemente comerciales y de acceso restringido. El sistema integra una base de datos vectorial con embeddings semánticos, una arquitectura multi-agente con agentes especializados en recuperación y generación de respuestas, y un pipeline de evaluación basado en modelos de lenguaje que actúan como jueces (LLM-as-a-Judge, por su sigla en inglés _Large Language Model as a Judge_) con tres jueces independientes. La evaluación emplea un diseño factorial 3 × 3 —respuesta directa sin recuperación (sin RAG), recuperación aumentada básica (RAG básico) y recuperación agéntica (Agentic-RAG), combinadas con tres modelos de lenguaje— sobre un benchmark de 25 preguntas legales (79 unidades de evaluación) validadas por un profesional del derecho argentino. Los resultados revelan una interacción significativa entre estrategia de recuperación y modelo de lenguaje ($H = 56.62$, $p < 10^(-11)$). El análisis de efectos simples con corrección de Holm-Bonferroni muestra que el RAG básico elimina las diferencias de desempeño entre modelos de distinta capacidad, mientras que Agentic-RAG beneficia significativamente a gpt-5-mini (mediana de 0.92 frente a 0.33 sin RAG, $p_"corr" < 0.0001$) pero degrada a gpt-5-nano frente a RAG básico (0.08 vs. 0.58, $p_"corr" = 0.017$). Para gpt-5, Agentic-RAG no produce diferencias significativas respecto a las otras estrategias tras la corrección por comparaciones múltiples.

*Palabras claves*

_Agentic-RAG, Generación Aumentada por Recuperación, Código de Minería Argentino, Procesamiento de lenguaje natural jurídico, LLM-as-a-Judge, benchmark legal, base de datos vectorial, agentes inteligentes_

// Dedicatoria
#heading(outlined: false, numbering: none)[Dedicatoria]

A mi familia ...

// Declaraciones
#heading(outlined: false, numbering: none)[Declaraciones]

Se han empleado productos basados en inteligencia artificial para asistir en la elaboración de este trabajo.

#outline(title: [Índice], indent: auto)

#outline(title: [Índice de Figuras], target: figure.where(kind: image))

#outline(title: [Índice de Tablas], target: figure.where(kind: table))

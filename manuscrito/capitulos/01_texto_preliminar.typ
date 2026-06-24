// Resumen
#heading(outlined: false, numbering: none)[Resumen]

Presentamos el diseño, implementación y evaluación de un sistema Agentic-RAG de código abierto para la consulta del Código de Minería Argentino. El acceso a la normativa legal argentina está limitado por sistemas de búsqueda basados en coincidencias léxicas que no capturan la semántica del lenguaje jurídico, mientras que las herramientas avanzadas existentes son predominantemente comerciales y de acceso restringido. El sistema integra una base de datos vectorial con embeddings semánticos, una arquitectura multi-agente con agentes especializados en recuperación y generación de respuestas, y un pipeline de evaluación LLM-as-a-Judge con tres jueces independientes. La evaluación emplea un diseño factorial 3 × 3 —sin RAG, RAG básico y Agentic-RAG combinados con tres modelos de lenguaje— sobre un benchmark de 25 preguntas legales (79 unidades de evaluación) validadas por profesionales del derecho argentino. Los resultados revelan una interacción significativa entre estrategia de recuperación y modelo de lenguaje ($H = 56.62$, $p < 10^(-11)$): el RAG básico elimina las diferencias de desempeño entre modelos de distinta capacidad, mientras que Agentic-RAG potencia a los modelos de mayor capacidad (gpt-5 alcanza una mediana de 0.96 en "respuesta correcta") pero degrada sustancialmente el desempeño del modelo más pequeño (gpt-5-nano: 0.08 frente a 0.58 sin RAG).

*Palabras claves*

_Agentic-RAG, Generación Aumentada por Recuperación, Código de Minería Argentino, PLN jurídico, LLM-as-a-Judge, benchmark legal, base de datos vectorial, agentes inteligentes_

// Dedicatoria
#heading(outlined: false, numbering: none)[Dedicatoria]

A mi familia ...

// Declaraciones
#heading(outlined: false, numbering: none)[Declaraciones]

Se han empleado productos basados en inteligencia artificial para asistir en la elaboración de este trabajo.

#outline(title: [Índice], indent: auto)

#outline(title: [Índice de Figuras], target: figure.where(kind: image))

#outline(title: [Índice de Tablas], target: figure.where(kind: table))

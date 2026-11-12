// Resumen
#heading(outlined: false, numbering: none)[Resumen]

Presentamos el diseño, implementación y evaluación de un prototipo Agentic-RAG de código abierto para la consulta del Código de Minería Argentino. El acceso a la normativa legal argentina está limitado por sistemas de búsqueda basados en coincidencias léxicas que no capturan la semántica del lenguaje jurídico, mientras que las herramientas avanzadas existentes son predominantemente comerciales y de acceso restringido. El prototipo integra una base de datos vectorial con embeddings semánticos, una arquitectura de dos agentes activos —Especialista Legal y Recuperación— y un pipeline de evaluación con métricas textuales, semánticas y tres jueces LLM. La evaluación emplea un diseño factorial 3 × 3 sobre 25 casos y 79 unidades, revisadas por una profesional del derecho. El análisis respeta el apareamiento por unidad y el anidamiento en casos mediante un modelo ordinal mixto. Se observó una interacción entre estrategia y modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). En el escenario principal, que asigna cero a las respuestas no sustantivas, Agentic-RAG fue inferior a RAG básico en gpt-5-nano (−0,270; IC 95% −0,330 a −0,202), superior en gpt-5-mini (+0,150; IC 95% 0,096 a 0,203) y superior en gpt-5 (+0,106; IC 95% 0,054 a 0,155). RAG básico no eliminó las diferencias entre modelos. En Agentic-RAG con gpt-5-nano, 41 de 79 salidas no fueron sustantivas; cuando respondió, la calidad fue alta (n = 38; media 0,820). Los resultados corresponden a un corpus, 25 casos, una ejecución por celda y un recuperador fijo, por lo que constituyen evidencia de viabilidad y no una validación externa.

*Palabras claves*

_Agentic-RAG, Generación Aumentada por Recuperación, Código de Minería Argentino, Procesamiento de lenguaje natural jurídico, LLM-as-a-Judge, benchmark legal, base de datos vectorial, agentes inteligentes_

// Dedicatoria
#heading(outlined: false, numbering: none)[Dedicatoria]

A mi familia, por el sostén de todos los días; a los docentes y compañeros de la maestría, por las preguntas que mejoraron este trabajo; y a quienes trabajan por un acceso más igualitario a la información pública.

// Declaraciones
#heading(outlined: false, numbering: none)[Declaraciones]

Se utilizaron herramientas de inteligencia artificial en distintas etapas de la investigación. La declaración siguiente distingue la etapa, el modelo empleado y el alcance de la verificación aplicada.

- *Extracción y estructuración del corpus*: se empleó `o4-mini` para transcribir y estructurar el texto del Código de Minería a partir de imágenes y documentos, con revisión y corrección manual posterior.
- *Generación del benchmark*: las preguntas y las respuestas esperadas se generaron con `GPT-4.1` y fueron revisadas por una profesional del derecho.
- *Generación de las respuestas evaluadas*: se utilizaron `gpt-5-nano`, `gpt-5-mini` y `gpt-5` de OpenAI.
- *Evaluación automática*: actuaron como jueces `DeepSeek V3.1`, `Grok 4.1 Fast` y `Kimi K2 0905`, con rúbricas explícitas.
- *Asistencia en la investigación*: se emplearon asistentes de IA para búsqueda bibliográfica, revisión y validación de citas, edición del manuscrito, programación, análisis de datos y preparación de figuras y tablas.

La verificación de los artefactos, las cifras, las citas y el código estuvo a cargo del autor. Esa verificación no incluyó una validación humana de la calidad de las 711 respuestas generadas: la revisión humana documentada corresponde al benchmark y fue realizada por una profesional del derecho. Durante la redacción se detectó y eliminó una referencia generada que no correspondía a una fuente verificable; la lista final de referencias fue auditada y contrastada con sus identificadores.

En la generación de respuestas no se configuró el parámetro `reasoning_effort`. Pydantic AI 1.1.0 no define un valor por defecto y envía `NOT_GIVEN`; OpenAI documenta `medium` como valor por defecto para GPT-5. El valor efectivo no quedó registrado y no se infiere de los tokens de razonamiento.

#outline(title: [Índice], indent: auto)

#outline(title: [Índice de Figuras], target: figure.where(kind: image))

#outline(title: [Índice de Tablas], target: figure.where(kind: table))

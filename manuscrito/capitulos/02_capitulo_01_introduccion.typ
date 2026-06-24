= Introducción

#import "@preview/tablem:0.3.0": three-line-table

== Motivación e importancia del tema de estudio

El acceso a la normativa legal es esencial para el funcionamiento del Estado de derecho, la transparencia institucional y la participación ciudadana. En Argentina, la legislación nacional se encuentra dispersa en diversas fuentes, como Infoleg (Sistema de Información Legislativa y Documental)#footnote[#link("https://www.infoleg.gob.ar/"): mantenido por el Ministerio de Justicia de la Nación.], el Sistema Argentino de Información Jurídica (SAIJ)#footnote[#link("https://www.saij.gob.ar/"): mantenido por la Dirección Nacional del Sistema Argentino de Información Jurídica (SAIJ) dependiente del Ministerio de Justicia de la Nación.] y boletines oficiales#footnote[#link("https://www.boletinoficial.gob.ar"): mantenido por la Secretaría Legal y Técnica de la Presidencia de la Nación, a través de la Dirección Nacional del Registro Oficial.], siendo las dos primeras fuentes secundarias, que en parte se nutren de los boletines oficiales nacionales. Esta distribución de la información dificulta su consulta y comprensión, especialmente para usuarios no especializados.

Esta dificultad de consulta se ve agravada por los sistemas tradicionales de búsqueda legal, basados en coincidencias de palabras clave, que fallan en capturar la semántica del lenguaje jurídico y las relaciones contextuales entre conceptos legales, lo que conlleva a resultados irrelevantes o incompletos. Además, la estructura compleja y jerárquica de los documentos legales requiere herramientas que comprendan y puedan navegar estas relaciones.

La Generación Aumentada por Recuperación (RAG) ha emergido como una solución prometedora para mejorar la consulta de información en dominios especializados, información confidencial, documentación interna, etc. Esta estrategia consiste en crear representaciones del texto de interés en forma de vectores (secuencias de números), almacenarlos en una base de datos para luego emplear algoritmos matemáticos para calcular similitudes entre cadenas de texto y enviar los resultados de la búsqueda al usuario @gao2023retrieval.

Al combinar grandes modelos de lenguaje (LLM) con mecanismos de recuperación de información. La incorporación de agentes inteligentes en este proceso, conocida como Agentic-RAG, añade capacidades de planificación, razonamiento y adaptación @singh2025agentic.

Implementar un sistema Agentic-RAG para la consulta de normativa argentina tiene el potencial de transformar la manera en que se accede y utiliza la legislación. Facilitaría la búsqueda de información legal, reduciría las barreras de acceso para usuarios no especializados y mejoraría la eficiencia de profesionales del derecho y funcionarios públicos. Además, contribuiría a la transparencia institucional y al fortalecimiento del Estado de derecho, al hacer la normativa más accesible y comprensible para todos los ciudadanos. Como prueba de concepto, el presente trabajo se enfoca en el Código de Minería Argentino, un cuerpo normativo estructurado que permite validar la arquitectura propuesta antes de escalar a la totalidad de la legislación nacional.

Este proyecto se alinea con las tendencias actuales en inteligencia artificial y procesamiento de  (PLN), aplicándolas a un dominio crítico como el legal.

== Requerimientos y desafíos

El desarrollo de un sistema Agentic-RAG para la consulta de normativa argentina implica abordar diversos requerimientos técnicos y desafíos específicos del dominio legal. El primer requisito es contar con una fuente de datos; en este caso particular, se empleará el Código de Minería Argentino extraído del archivo pdf descargado de la página del Boletín Oficial de la República Argentina y actualizado con los cambios publicados en el sitio Infoleg. El siguiente requisito es un sistema para extraer el texto de los artículos del código y almacenarlo en archivos de texto plano o en una base de datos para luego ser transformado en "embeddings" por un modelo de vectorización semántica y almacenarlo en una base de datos vectorial. Otros requisitos incluyen la integración de modelos de lenguaje preentrenados capaces de generar respuestas coherentes y contextualizadas a partir de la información recuperada, y el desarrollo de agentes inteligentes que coordinen las tareas de recuperación y generación, adaptándose a las necesidades y contextos específicos de las consultas.

Entre los desafíos del proyecto está en primer lugar, la complejidad del lenguaje jurídico, lo que presenta un obstáculo significativo, ya que el lenguaje legal es altamente técnico y especializado lo que necesita métodos más avanzados y complejos de evaluación de la calidad de recuperación. Una vez extraído el texto, se presenta la necesidad de seleccionar una estructura adecuada de representación de los datos, ya que depende de ello la calidad de los "embeddings" a ser almacenados en forma de vectores @tsitsulin2023unsupervised. Asimismo, la calidad de los "embeddings" también depende la correcta selección del tipo de "embedding" a emplear, por ejemplo, de documentos o tópicos @isbarov2024enhanced y del tamaño de fragmentación de texto, también conocido como "chunking" @zhong2024mix.

Además, la estructura jerárquica de los documentos legales, que suelen tener múltiples niveles de jerarquía como títulos, capítulos, artículos e incisos, complica su representación y recuperación efectiva. Por otro lado, la legislación está en constante cambio, lo que exige que el sistema sea capaz de actualizarse regularmente para reflejar las modificaciones y nuevas normativas. Asimismo, es fundamental emplear métricas como la precisión, relevancia y coherencia y desarrollar un sistema punto de referencia (benchmark) para evaluar las respuestas generadas por el sistema. Finalmente, el sistema debe ser accesible y fácil de usar para usuarios con distintos niveles de conocimiento legal, incluyendo interfaces intuitivas y explicaciones claras de las respuestas proporcionadas. Abordar estos requerimientos y desafíos es esencial para el éxito del proyecto, garantizando que el sistema desarrollado sea efectivo, confiable y útil para una amplia gama de usuarios interesados en la normativa legal argentina.

== Problemas y soluciones

=== Problemas no resueltos

A pesar de los avances en tecnologías de recuperación de información y procesamiento de lenguaje natural, persisten desafíos significativos en la consulta de normativa legal. En primer lugar, los sistemas tradicionales de búsqueda legal en Argentina, como Infoleg y SAIJ, se basan principalmente en coincidencias de palabras clave limitando su capacidad para comprender la semántica y contexto de las consultas, llevando a resultados que pueden ser irrelevantes o incompletos. Al día de la fecha, se ha encontrado un sistema de búsqueda asistido por IA, el sistema de "Búsqueda de Jurisprudencia Asistida por IA" del Tribunal Fiscal de la Nación#footnote[#link("https://jurisprudenciatfn.mecon.gob.ar/")], limitado a documentos emitidos por dicho tribunal. Fuera de esa excepción, no se han identificado bases de datos o sistemas de búsqueda más avanzados de uso libre en Argentina, aunque sí se han encontrado plataformas pagas como Lexius#footnote[#link("https://lexius.io/")] o Juztina#footnote[#link("https://www.juztina.ai/ar/es")] que permiten realizar búsquedas y análisis avanzados con asistencia de inteligencia artificial empleando sus bases de datos privadas.

Uno de los principales problemas en los sistemas basados en grandes modelos de lenguaje o Large Language Models (LLM) son las alucinaciones. Este término se puede definir como "generación de información que no está basada en datos reales o verificables", es decir, el sistema "inventa" información. Esto es una ocurrencia normal en los grandes modelos de lenguaje @islam2025hallucinate que puede atenuarse en gran medida empleando RAG @shuster2021retrieval y potencialmente mediante el diseño de un sistema de agentes que empleen un método estandarizado de comunicación @gosmar2025hallucination.

En esta línea, surge el concepto de generación aumentada por recuperación agéntica o Agentic-RAG, el cual combina la versatilidad de los Agentes y la RAG para crear un sistema capaz de tener memoria a corto y largo plazo, capacidad de planificar, así como también seleccionar herramientas a emplear dependiendo del rol y tarea a realizar @singh2025agentic.

Otro desafío es la evaluación del desempeño de los modelos de lenguaje natural en un área específica. Para realizar esta tarea se suelen emplear "benchmarks" o puntos de referencia, que contienen preguntas y respuestas esperadas para varios tópicos legales, principalmente en idioma inglés. Dependiendo de la cantidad de preguntas que el sistema responde de manera correcta, se le asigna un puntaje lo que permite comparar varios sistemas entre sí. Algunos de los benchmarks empleados para evaluar el desempeño de los sistemas en el ámbito legal son: LexGLUE @chalkidis2021lexglue, LegalBench @guha2023legalbench, LEXTREME @niklaus2024lextreme y LegalBench-RAG que consiste en la adaptación de LegalBench a sistemas de Generación Aumentada por Recuperación @pipitone2024legalbench. Actualmente, la creación de benchmarks es una tarea que requiere de la intervención de humanos competentes en el área a ser evaluada, lo que conlleva a una gran inversión de tiempo y dinero, aunque este paradigma está cambiando hacia una mayor automatización @cao2025toward. Al día de la fecha no se han encontrado benchmarks para normativa argentina.

Por último, la mayor barrera al día de la fecha para el desarrollo de este tipo de sistemas y evaluar de manera fiable su desempeño, es el costo económico del uso de los modelos LLM ya que la estimación no es trivial y puede rápidamente escalar a grandes sumas. Asimismo, existe un número elevado de modelos y proveedores por lo que la selección puede llegar a requerir una aproximación sistemática @shekhar2024towards.

=== Solución propuesta

La solución propuesta consiste en el desarrollo de un sistema de Generación Aumentada por Recuperación con agentes (Agentic-RAG) que será estructurado en tres módulos principales:

+ *Extracción y estandarización de datos normativos*: Este módulo se encarga de la recopilación de los artículos del Código de Minería Argentino desde Infoleg, aplicando técnicas de web scraping y procesamiento de lenguaje natural para extraer y estructurar la información legal. La normalización de los datos incluye la estandarización de formatos, corrección de inconsistencias y eliminación de duplicados, asegurando la calidad y coherencia de la información recopilada.

+ *Base de datos vectorial*: Los artículos del Código de Minería normalizados se transforman en vectores semánticos utilizando modelos de generación de embeddings. Estos vectores se almacenan en una base de datos vectorial que permite realizar búsquedas basadas en la similitud semántica, facilitando la recuperación de información relevante incluso cuando las consultas no coincidan exactamente con los términos utilizados en los artículos @jing2024large.

+ *Sistema Agentic-RAG*: Este componente integra modelos de lenguaje preentrenados con capacidades de recuperación de información, coordinados por agentes inteligentes (LLMs o Small Language Models, SLM) que gestionan el flujo de trabajo. Los agentes son responsables de tareas como la interpretación de consultas, planificación de acciones, recuperación de artículos relevantes y generación de respuestas @ehtesham2025survey.

El sistema tiene dos funcionalidades principales. La primera consiste en la *extracción y estandarización de datos* donde se recopilan los artículos del Código de Minería y se colocan en la base de datos vectorial.

La segunda funcionalidad será atender las consultas de los usuarios, lo que desencadena un conjunto de subtareas:

+ *Recepción de la consulta:* El usuario introduce su consulta en lenguaje natural.

+ *Interpretación de la consulta:* Un agente especializado analiza la consulta para identificar la intención del usuario y los elementos clave de la búsqueda.

+ *Planificación de la recuperación:* Basándose en la interpretación de la consulta, el agente planifica las acciones necesarias para recuperar la información relevante, determinando qué fuentes consultar y qué estrategias de búsqueda emplear.

+ *Recuperación de documentos:* El sistema realiza búsquedas en la base de datos vectorial para identificar los documentos legales más relevantes según la similitud semántica con la consulta.

+ *Generación de la respuesta:* Utilizando los documentos recuperados de la base de datos vectorial, un modelo de lenguaje preentrenado genera una respuesta coherente y contextualizada que responde a la consulta del usuario.

+ *Presentación de la respuesta:* La respuesta final se presenta al usuario junto con enlaces a los documentos legales relevantes y opciones para profundizar en la información.

Para evaluar la efectividad del sistema propuesto, se llevarán a cabo pruebas utilizando un conjunto de consultas representativas del dominio legal argentino. Se medirán métricas como la precisión, exhaustividad, relevancia y coherencia de las respuestas generadas, comparando el rendimiento del sistema Agentic-RAG con soluciones existentes.

Además, se realizarán pruebas utilizando un *benchmark a pequeña escala, generado con asistencia de LLM y validado por profesionales del derecho argentino*. Este benchmark, al ser revisado por expertos en el campo, garantizará que las evaluaciones se basen en casos de uso reales y desafiantes, proporcionando una medida fidedigna de la capacidad del sistema para asistir en la práctica jurídica diaria.

=== Limitaciones de la solución propuesta

La solución propuesta presenta algunas limitaciones que deben considerarse:

- El sistema se limita al Código de Minería Argentino como prueba de concepto, sin incluir otras normativas nacionales, provinciales o municipales.
- La calidad de las respuestas depende de la calidad de la extracción de texto y de los modelos de embeddings seleccionados.
- El costo computacional y económico del uso de modelos LLM puede limitar la escalabilidad del sistema.
- El benchmark desarrollado es de pequeña escala, enfocado específicamente en el Código de Minería.
- El sistema se implementa como un pipeline experimental en notebooks de Jupyter, sin una interfaz de usuario final desplegada. La interacción con el sistema requiere conocimientos técnicos para ejecutar los scripts y notebooks correspondientes.

Como trabajo futuro, se podría ampliar el sistema para incluir la totalidad de la normativa nacional disponible en Infoleg, así como normativa provincial y municipal, expandir el benchmark con la colaboración de más profesionales del derecho, y desarrollar una interfaz de usuario accesible para usuarios no técnicos.

== Resumen de problemas y soluciones

A continuación, se detallan los principales problemas identificados, con un breve resumen de cada uno de ellos y las soluciones propuestas:

#figure(
  three-line-table(
    columns: (1fr, 1.3fr),
    [
      | *Problema*                                                                              | *Solución*                                                                                                           |
      | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
      | Sistemas de búsqueda legal basados en palabras clave con limitada comprensión semántica | Implementación de búsqueda semántica mediante base de datos vectorial con embeddings                                 |
      | Alucinaciones en modelos de lenguaje que generan información no verificable             | Uso de RAG para anclar respuestas en documentos reales y verificables                                                |
      | Ausencia de benchmarks para normativa argentina                                         | Desarrollo de benchmark específico generado con asistencia de LLM y validado por profesionales del derecho argentino |
    ],
  ),
  caption: [Resumen de problemas identificados y soluciones propuestas],
) <tab:problemas_soluciones>

== Objetivo del trabajo

=== Objetivo general

Desarrollar un sistema Agentic-RAG de código abierto como prueba de concepto, utilizando el Código de Minería Argentino, para responder consultas de usuarios profesionales y no profesionales en el derecho.

=== Objetivos específicos

+ Desarrollar una base de datos vectorial del Código de Minería Argentino diseñada específicamente para trabajar con sistemas RAG.

+ Desarrollar un sistema de agentes de inteligencia artificial para que trabajen de manera conjunta con el sistema RAG.

+ Desarrollar un benchmark específico para el Código de Minería Argentino para evaluar el desempeño del sistema.

+ Cargar el código y una descripción de la metodología a un repositorio abierto para que cualquier organización, empresa o individuo pueda replicar y adaptar el sistema a otras normativas.

== Transferencia de los resultados obtenidos

El código y la documentación generada durante el proyecto se cargarán a un repositorio del sistema de control de versiones "Git"#footnote[#link("https://git-scm.com/")] y luego se subirá la información a la plataforma "GitHub"#footnote[#link("https://github.com/")] en un repositorio público para que cualquier individuo pueda descargarlo.

La solución propuesta tiene aplicaciones prácticas que trascienden el ámbito específico de la normativa argentina:

- *Adaptación a otras jurisdicciones*: La metodología y arquitectura del sistema pueden ser replicadas para crear sistemas similares en otros países de habla hispana o con sistemas legales comparables.

- *Extensión a otros dominios*: Los principios de Agentic-RAG pueden aplicarse a otros dominios especializados como medicina, ingeniería o finanzas, donde se requiere consulta de documentación técnica extensa.

- *Contribución al software libre*: Al ser de código abierto, el proyecto contribuye al ecosistema de herramientas legales accesibles, permitiendo que organizaciones sin recursos para adquirir soluciones comerciales puedan implementar sistemas de consulta avanzados.

- *Modelo para instituciones públicas*: El sistema puede servir como referencia para que organismos gubernamentales implementen herramientas similares para mejorar el acceso ciudadano a la información legal.

== Contribuciones principales

Las principales contribuciones del presente trabajo final son:

+ *Sistema Agentic-RAG de código abierto*: Desarrollo de un sistema completo que integra recuperación semántica, base de datos vectorial y agentes inteligentes para la consulta del Código de Minería Argentino como prueba de concepto.

+ *Base de datos vectorial del Código de Minería*: Creación de una base de datos especializada con embeddings semánticos de los artículos del Código de Minería Argentino, optimizada para búsquedas por similitud.

+ *Benchmark para el Código de Minería Argentino*: Desarrollo de un benchmark específico para evaluar sistemas de consulta legal sobre el Código de Minería, generado con asistencia de LLM y validado por profesionales del derecho.

+ *Metodología replicable*: Documentación detallada de la metodología empleada, permitiendo la replicación del sistema para otras normativas y jurisdicciones.

+ *Contribución a la transparencia institucional*: Demostración del potencial para mejorar el acceso ciudadano a la información legal, fortaleciendo el Estado de derecho y la participación ciudadana.

== Trabajos presentados vinculados con el trabajo final

Al momento de la escritura de este documento, no se han presentado trabajos de investigación en congresos o revistas científicas vinculados directamente con el presente trabajo final.

== Estructura general del trabajo final

El presente trabajo final se estructura de la siguiente manera:

- *Capítulo 2 - Fundamentos e Historia del Procesamiento de Lenguaje Natural*: Se presentan los conceptos fundamentales sobre la evolución de los modelos de lenguaje, desde modelos estadísticos hasta los grandes modelos de lenguaje (LLM), incluyendo embeddings semánticos, tokenización, mecanismos de atención y las limitaciones como las alucinaciones.

- *Capítulo 3 - Aplicación de PLN al Dominio Legal*: Se analizan las particularidades del lenguaje jurídico, las tareas típicas del procesamiento de lenguaje natural legal, las técnicas de adaptación de LLMs al dominio legal y los riesgos asociados (alucinaciones, sesgos), fundamentando la complementariedad entre LLMs y RAG.

- *Capítulo 4 - Agentic-RAG: Generación Aumentada por Recuperación Agéntica*: Se presenta el marco teórico unificado de RAG y sistemas agénticos, describiendo arquitecturas, patrones de flujo de trabajo, agentes especializados, la técnica de evaluación LLM-as-a-Judge y los desafíos y limitaciones asociados.

- *Capítulo 5 - Metodología e Implementación*: Se describe la metodología empleada y la implementación técnica del sistema, incluyendo la selección del corpus legal, extracción y preprocesamiento de datos, diseño de la base de datos vectorial, arquitectura del sistema Agentic-RAG, diseño del benchmark y el sistema de evaluación.

- *Capítulo 6 - Evaluación y Resultados*: Se presenta el diseño experimental factorial 3 × 3, las métricas utilizadas (textuales, semánticas y LLM-as-a-Judge), los resultados obtenidos para las nueve configuraciones, el análisis estadístico (Kruskal-Wallis, Dunn, Scheirer-Ray-Hare, Krippendorff's alpha) y el análisis de costos.

- *Capítulo 7 - Trabajos Relacionados*: Se presenta una revisión de los trabajos previos y plataformas existentes, organizada en cuatro ejes: sistemas de búsqueda legal, RAG en dominios especializados, sistemas agénticos y benchmarks para evaluación legal, posicionando el presente trabajo en el contexto de la literatura.

- *Capítulo 8 - Conclusiones y Trabajos Futuros*: Se sintetizan las conclusiones del trabajo, se revisa el cumplimiento de los objetivos, se discuten las fortalezas y limitaciones identificadas, y se proponen líneas de investigación futuras.

Adicionalmente, el trabajo incluye anexos con la estructura del repositorio de código, ejemplos de consultas y respuestas, y el benchmark completo utilizado para la evaluación, así como un listado de acrónimos y siglas empleados en el documento.

---
title: "Valoración del Trabajo Final de Maestría"
creator: "Gastón Pezzuchi"
created: "2026-11-11T19:27:00Z"
modified: "2026-11-11T19:27:00Z"
---

VALORACIÓN DEL TRABAJO FINAL DE MAESTRÍA

Informe ampliado del miembro del tribunal

| Autor | Leonardo Ulises Spairani |
| --- | --- |
| Título | Desarrollo y evaluación de un prototipo de sistema inteligente para consulta de normativa nacional argentina mediante recuperación agéntica |
| Directores | Dra. Laura Lucía Bélfer y Dr. Rafael Crescenzi |
| Institución | Universidad Austral, Facultad de Ingeniería |
| Versión evaluada | Manuscrito de octubre de 2026 (versión 2026.10.07.16.40.28), 165 páginas |
| Miembro del tribunal | Mg. Lic. Prof. Gastón Pezzuchi, MSc. |
| Fecha | Noviembre de 2026 |

# I. OBJETIVO TÉCNICO

Este informe amplía y fundamenta la evaluación sintética consignada en el formulario institucional. Se basa en la lectura completa del manuscrito, en el control de su consistencia interna y en la verificación, contra fuentes primarias, de sus referencias y de las afirmaciones técnicas que sostienen el diseño experimental. Las páginas citadas corresponden a la numeración impresa del manuscrito (Spairani, 2026), no a la numeración interna del archivo.

La valoración se concentra en los aspectos propios de la minería de datos y el aprendizaje automático: diseño experimental, medición, análisis estadístico y sustento de las conclusiones. Las cuestiones estrictamente jurídicas se señalan solo cuando entendemos que afectan la validez del instrumento de evaluación.

# II. SÍNTESIS DEL TRABAJO

El trabajo presenta el diseño, la implementación y la evaluación de un prototipo de consulta en lenguaje natural sobre el Código de Minería argentino. El sistema combina una base vectorial (Milvus) con representaciones de 768 dimensiones, un esquema de recuperación simple y un esquema de dos agentes implementado con Pydantic AI. La evaluación sigue un diseño factorial de tres estrategias (sin recuperación, RAG básico y Agentic-RAG) por tres modelos (gpt-5-nano, gpt-5-mini y gpt-5), sobre 25 casos que se descomponen en 79 unidades de evaluación, con un total de 711 observaciones (Spairani, 2026, pp. 56, 79).

La variable de respuesta principal es el promedio de las calificaciones de tres jueces automáticos sobre una rúbrica de cinco niveles. El hallazgo que el autor destaca es la interacción entre estrategia y modelo: el esquema agéntico favorece a gpt-5-mini, no produce diferencias significativas en gpt-5 y degrada a gpt-5-nano (Spairani, 2026, pp. 85-90).

# III. DICTAMEN Y CALIFICACIÓN POR CRITERIO

Se propone aceptar el trabajo para su defensa oral. Las observaciones que siguen son subsanables y, en su mayoría, pueden resolverse con nuevos análisis sobre los datos y los registros que el autor ya posee. La Tabla 1 resume la calificación asignada a cada criterio del formulario.

Tabla 1

Calificación por criterio

| Criterio | Calificación | Fundamento |
| --- | --- | --- |
| Aporte del trabajo presentado | Muy Buena | Tema pertinente y poco explorado en español y en derecho continental. Prototipo, banco de preguntas y comparación empírica propios. |
| Profundidad de la investigación y el desarrollo | Muy Buena | Canal completo, desde la extracción del corpus hasta el análisis de costos. Revisión bibliográfica extensa. |
| Metodología de trabajo adoptada y aplicada | Buena | Diseño factorial, líneas de base y corrección por comparaciones múltiples bien planteados. Factores confundidos y pruebas que no corresponden a la estructura de los datos. |
| Calidad del trabajo experimental | Regular | Una ejecución por celda, parámetros de muestreo y de razonamiento sin control efectivo, celda anómala sin diagnóstico y recuperación no evaluada. |
| Claridad y precisión de la redacción | Buena | Texto ordenado y legible. Contradicciones internas y errores conceptuales puntuales. |
| Fuentes de información y bibliografía | Buena | Bibliografía amplia y actual. Atribuciones erróneas y una referencia con autoría que no corresponde al artículo citado. |
| Validez de las conclusiones alcanzadas | Regular | Varias conclusiones exceden lo que los datos y los análisis permiten sostener. |

# IV. FORTALEZAS

1. Pertinencia y originalidad local. El trabajo se ocupa de normativa argentina, en español y dentro de la tradición del derecho continental, un terreno poco cubierto por una literatura que se concentra en el inglés y en el derecho anglosajón. El autor no identificó bancos de evaluación públicos para normativa argentina (Spairani, 2026, p. 105) y construyó uno.

2. Sistema completo y trazable. El prototipo cubre la extracción del corpus, la indexación vectorial, dos esquemas de recuperación, la generación y la evaluación. Cada interacción entre agentes queda registrada en archivos JSON (pp. 66, 77-78), lo que permite auditar el comportamiento del sistema y rehacer análisis sin nuevas ejecuciones.

3. Diseño comparativo con dos líneas de base. La inclusión de la respuesta sin recuperación y del RAG básico permite distinguir el aporte de la recuperación del aporte de la orquestación con agentes.

4. Evaluación con jueces heterogéneos. Los tres jueces provienen de proveedores distintos del que desarrolla los modelos evaluados (p. 73), lo que reduce el riesgo de que un juez favorezca respuestas de su misma familia. El acuerdo se cuantificó con el alfa de Krippendorff y la rúbrica de precisión legal se descartó cuando su confiabilidad resultó insuficiente (pp. 95-96). Es una decisión metodológicamente correcta.

5. Cuidado en las comparaciones múltiples. Tras detectar la interacción, el autor analizó efectos simples y aplicó la corrección de Holm (pp. 84-85), sin apoyarse en los valores p sin corregir.

6. Análisis de costos. El registro de tokens y costos por configuración (pp. 90-93) agrega una dimensión de decisión que muchos trabajos de este tipo omiten.

7. Franqueza sobre las limitaciones. El capítulo final declara diez limitaciones, entre ellas la falta de validación humana de los jueces y la ausencia de razonamiento explícito en sus instrucciones (pp. 116-118).

# V. OBSERVACIONES SUSTANTIVAS

Las observaciones se ordenan según su efecto sobre la validez de las conclusiones. Cada una indica la evidencia en el manuscrito y lo que se solicita al autor.

## V.1 Estructura de dependencia de los datos y pruebas estadísticas

Las mismas 79 unidades de evaluación se responden en las nueve configuraciones: “79 unidades de evaluación × 9 configuraciones = 711 observaciones” (Spairani, 2026, p. 79). Las observaciones están, por lo tanto, apareadas por unidad. Además, las unidades son subpreguntas anidadas en 25 casos, aunque el texto las presenta como “unidades de evaluación independientes” (p. 71). El análisis emplea Kruskal-Wallis, Dunn, Mann-Whitney y Scheirer-Ray-Hare (pp. 76, 83-88), procedimientos formulados para muestras independientes. El último fue propuesto de manera expresa para diseños factoriales completamente aleatorizados (Scheirer et al., 1976).

Ignorar el apareamiento tiene, en principio, dos consecuencias principales. La variabilidad entre unidades, que refleja la dificultad de cada pregunta, queda dentro del término de error y reduce la potencia. Además, los valores p dejan de ser válidos, porque las observaciones no son independientes. Para comparar sistemas sobre un mismo conjunto de ítems, la literatura de aprendizaje automático y de procesamiento del lenguaje recomienda pruebas para muestras relacionadas, como Wilcoxon de rangos con signo y Friedman (Demšar, 2006; Dror et al., 2018). Una alternativa más completa es un modelo ordinal con efectos aleatorios por caso y por subpregunta. El anexo indica que el directorio de análisis contiene “modelos mixtos” (Tabla 17, p. 141), pero el cuerpo del trabajo no los informa.

Esta observación no es solo formal. En gpt-5, las diferencias de Agentic-RAG frente a las otras dos estrategias tienen valores p sin corregir de 0,013 y 0,025, que pasan a 0,064 y 0,074 tras la corrección (Tabla 10, p. 85). La conclusión de que en gpt-5 no hay diferencias significativas (p. ii) descansa en una prueba que desaprovecha el apareamiento y podría modificarse con el análisis estadístico adecuado. Tampoco se informan tamaños de efecto ni intervalos de confianza, y el texto menciona “n = 79 observaciones por celda” (p. 97) aunque 27 observaciones fueron eliminadas (pp. 82-83).

Se solicita rehacer el análisis inferencial con procedimientos que respeten el apareamiento y el anidamiento, informar tamaños de efecto con sus intervalos de confianza e incluir los resultados de los modelos mixtos si fueron estimados.

## V.2 Prueba de interacción

El hallazgo que el autor considera más relevante es la interacción entre estrategia y modelo, sostenida en la prueba de Scheirer-Ray-Hare (H = 56,62; Tabla 12, p. 88). Esta prueba aplica un análisis de varianza sobre los rangos globales. La literatura estadística advierte desde hace décadas que la transformación a rangos no es adecuada para contrastar interacciones cuando existen efectos principales, porque el estadístico puede resultar poco robusto (Blair et al., 1987; Seaman et al., 1994). La transformación a rangos alineados es la alternativa habitual (Wobbrock et al., 2011).

El patrón descriptivo de la Figura 21 y de la Tabla 13 (pp. 89-90) es lo bastante marcado como para que la interacción sea plausible. Lo que requiere corrección es su sustento inferencial y, sobre todo, su interpretación, que depende de las observaciones V.5 y V.6.

## V.3 Equivalencia inferida de la falta de significación

El trabajo afirma que “el RAG básico elimina las diferencias de desempeño entre modelos de distinta capacidad” (p. ii) y lo presenta como una contribución demostrada (p. 114). El sustento es una prueba de Kruskal-Wallis no significativa (H = 4,71; p = 0,095; p. 84). Ahora bien, la ausencia de significación no demuestra equivalencia. Con RAG básico las medianas son 0,583 para gpt-5-nano, 0,625 para gpt-5-mini y 0,833 para gpt-5 (Tabla 11, p. 87), y la distancia entre los extremos equivale a un nivel completo de la rúbrica. Una afirmación de equivalencia exige una prueba de equivalencia con un margen definido de antemano o, al menos, intervalos de confianza para las diferencias. Se solicita reformular la conclusión.

## V.4 Control experimental: temperatura, razonamiento y réplicas

El manuscrito declara temperatura cero en todas las configuraciones “para garantizar reproducibilidad” (p. 79), la incluye entre los criterios de selección de modelos (p. 70) y la fija en el código de ambos agentes mediante el ajuste “temperature=0.0” (pp. 66-67). Los modelos gpt-5, gpt-5-mini y gpt-5-nano son modelos de razonamiento y no admiten los parámetros de muestreo, entre ellos la temperatura (Microsoft, 2026). La API de OpenAI rechaza las solicitudes que fijan temperatura cero en estos modelos, con un error que indica que solo se admite el valor predeterminado (Droniu, s.f.).

El destino del parámetro pudo verificarse en el código de la biblioteca. El anexo declara la versión 1.1.0 de Pydantic AI (p. 142), publicada el 15 de octubre de 2025. En esa versión, el perfil de los modelos de OpenAI clasifica como modelo de razonamiento a todo identificador que comience con “gpt-5” e incluye la temperatura entre los ajustes no admitidos; antes de construir la solicitud, la clase del modelo elimina esos ajustes sin emitir advertencia ni error (Pydantic, 2025). La documentación de la biblioteca describe el mismo mecanismo (Pydantic, s.f.). El tratamiento está presente, con otra implementación, desde la versión 0.7.0, del 12 de agosto de 2025, por lo que cubre el período de experimentación informado: “agosto-noviembre 2025” (p. 71). En las versiones previas el parámetro se enviaba y la API lo habría rechazado. En ningún caso, por lo tanto, la temperatura cero llegó a tener efecto. Los tres modelos operaron con el muestreo predeterminado, lo que explica que las ejecuciones se completaran sin fallos y que el problema pasara inadvertido.

La comprobación se hizo sobre la biblioteca declarada, dado que el código y los registros del experimento no pudieron consultarse (V.11); corresponde al autor confirmarla con los parámetros efectivamente enviados. El propio anexo es coherente con esta lectura: una respuesta breve de gpt-5-nano consumió 315 tokens de entrada y 7.818 de salida (p. 143), proporción que solo se explica por tokens de razonamiento interno. El trabajo no menciona el nivel de esfuerzo de razonamiento utilizado.

Esto genera dos consecuencias. Las respuestas no son deterministas y existe un parámetro que incide en la calidad y en el costo sin control ni registro. Además, la temperatura cero se invoca para justificar una única ejecución por celda: “evita múltiples ejecuciones” (p. 74). Con una sola ejecución no es posible separar el efecto de los factores de la variabilidad entre corridas. Las diferencias marginales señaladas en V.1 para gpt-5 pueden quedar dentro de esa variabilidad. El costo total informado, USD 22,29 (p. 93), muestra que repetir el experimento varias veces era viable.

Se solicita mostrar, a partir de los registros, los parámetros efectivamente enviados a la API, informar el esfuerzo de razonamiento, retirar la afirmación de determinismo salvo que esos registros la respalden y, de ser posible, agregar réplicas de las celdas críticas.

## V.5 Factores confundidos y alcance del término Agentic-RAG

En la estrategia agéntica el Agente de Recuperación utiliza siempre gpt-5, cualquiera sea el modelo del Agente Especialista Legal (Tabla 6, p. 70). El factor modelo tiene entonces un significado distinto en cada nivel del factor estrategia: en las dos primeras estrategias designa el único modelo que interviene y en la tercera, solo el que redacta la respuesta. La configuración denominada Agentic-RAG con gpt-5-nano es, en rigor, un sistema mixto.

Las estrategias difieren además en otros aspectos que no se controlan. El prompt de las configuraciones sin RAG y con RAG básico es un “prompt simplificado” (p. 66) que el manuscrito no reproduce, por lo que no puede establecerse si contiene la instrucción de abstención presente en el prompt agéntico (p. 63). El RAG básico recupera diez fragmentos con la consulta original (p. 62), mientras que el esquema agéntico ejecuta hasta seis búsquedas de cinco fragmentos y luego gpt-5 selecciona los que entrega (pp. 67-69). Sin ablaciones, la diferencia entre estrategias no puede atribuirse a la descomposición de consultas, a la mayor cantidad de candidatos, a la selección realizada por gpt-5 o al cambio de instrucciones.

Por último, el sistema evaluado es más limitado que el descrito en el marco teórico. El Agente Especialista Legal puede invocar la recuperación una sola vez: su prompt indica “utilizas la herramienta retrieve_relevant_documents una vez” (p. 63) y el código fija DOCUMENT_RETRIEVAL_LIMIT = 1 (p. 68). El Agente de Calidad, encargado de verificar la pertinencia de lo recuperado, fue desactivado (p. 65). El manuscrito sostiene, sin embargo, que “se optó por actualizar los prompts del Agente Especialista Legal para que este pudiera solicitar búsquedas adicionales” (p. 65), lo que contradice el límite anterior. Ofrece además dos motivos distintos para la desactivación: que no produjo mejoras (p. 62) y que agregaba costo y una variable más (p. 65), sin datos de esa comparación.

El capítulo 3 afirma que el sistema combina “few-shot prompting para fijar el formato de respuesta, Chain-of-Thought para inducir razonamiento explícito” (p. 35), pero los prompts reproducidos no contienen ejemplos ni instrucciones de razonamiento (pp. 63-64). Lo evaluado se aproxima a un RAG con descomposición de consultas delegada en gpt-5, sin iteración ni verificación.

Se solicita declarar estas confusiones como amenazas a la validez, reproducir todos los prompts utilizados, resolver las contradicciones señaladas y ajustar la denominación de la estrategia o el alcance de lo que se afirma sobre ella.

## V.6 La celda gpt-5-nano con Agentic-RAG y los datos faltantes

La configuración de gpt-5-nano con Agentic-RAG tiene mediana 0,083 (Tabla 11, p. 87) y media 0,40 (Tabla 13, p. 90). Una distancia semejante entre mediana y media indica una distribución bimodal: muchas respuestas con puntaje casi nulo y otras con puntaje alto. Las métricas textuales apuntan en la misma dirección. La mediana de similitud SBERT cae a 0,389, cuando en las demás celdas de ese modelo no baja de 0,74 (Tabla 11). La Figura 20 muestra, solo en el grupo agéntico, valores de BERTScore iguales a cero y un conjunto de valores de SBERT por debajo de 0,3 (p. 82). En la Figura 21, la media de BERTScore de gpt-5-nano desciende de alrededor de 0,71 a 0,45 únicamente en esa celda (p. 89).

Un BERTScore nulo o una similitud semántica cercana a cero no describen una respuesta jurídicamente peor, sino un texto vacío o ajeno a la referencia: una abstención, un mensaje de error o una salida truncada. El ejemplo del anexo muestra que, cuando responde, gpt-5-nano con Agentic-RAG produce una respuesta correcta y bien fundada (p. 145). Los datos son compatibles con un modo de falla que afecta a una parte de los ítems y no con una degradación general. El manuscrito lo atribuye a que “la complejidad agéntica es excesiva para modelos de capacidad reducida” (p. 86) y lo presenta como contribución (p. 114), sin examinar los registros de ejecución, que están disponibles (pp. 77-78).

A esto se suma el tratamiento de los faltantes. Se eliminaron 27 observaciones sin calificación de los jueces, “atribuibles a fallos puntuales en la generación de respuestas” (p. 82), sin informar su distribución por celda. Si los fallos se concentran en una configuración, excluirlos sesga la comparación. En un sistema de consulta, no responder es un resultado y no un dato ausente.

Tampoco se discute que, sin recuperación, gpt-5-nano obtenga una mediana superior a la de gpt-5-mini (0,583 frente a 0,333; Tabla 11, p. 87), resultado contrario al orden de capacidad de los modelos.

Se solicita clasificar las respuestas de la celda anómala (vacías, abstenciones, errores y respuestas sustantivas), informar los faltantes por celda, repetir el análisis tratando los fallos como puntaje cero y como exclusión, y reformular la contribución relativa a la “sobrecarga agéntica” según lo que surja.

## V.7 Validez de la medición

La variable de respuesta mide la alineación con una respuesta esperada (Tabla 8, p. 74). Esas respuestas fueron generadas por GPT-4.1 (p. 71), un modelo del mismo proveedor que los evaluados, y revisadas por un único profesional (p. 72). No se informa cuántas fueron corregidas ni existe un segundo revisor. La validez de toda la medición depende, entonces, de un instrumento cuya calidad no está documentada.

Los dos ejemplos publicados en el anexo justifican la preocupación. La respuesta esperada 1.2 afirma: “La propiedad minera constituye un derecho real separado de la propiedad del suelo (art. 8)” (p. 149). El capítulo 5, en cambio, describe el artículo 8 como “facultad de buscar minas” y el artículo 11 como “propiedad distinta del terreno” (p. 69), en línea con el texto del artículo 11 del Código (Decreto 456/1997). La respuesta esperada 1.3 sostiene que la propietaria “solo puede oponerse por razones de seguridad o ambientales (art. 17)” (p. 149). El artículo 17 dispone que los trabajos no pueden ser impedidos ni suspendidos sino cuando lo exija la seguridad pública, la conservación de las pertenencias y la salud o existencia de los trabajadores (Decreto 456/1997). Corresponde que el tesista y el profesional que validó el banco aclaren estos puntos. Para la evaluación importa su efecto: un sistema que cite el artículo correcto puede ser penalizado por apartarse de la referencia.

Los jueces automáticos no fueron contrastados con criterio humano, como el propio autor reconoce al señalar que se trata de jueces “cuya alineación con criterios humanos no ha sido validada” (p. 97). El acuerdo entre jueces mide confiabilidad, no validez: tres modelos pueden coincidir y compartir un mismo sesgo, por ejemplo hacia respuestas extensas o de estilo similar al de la referencia. Por eso la contribución 6, que da el método por validado, “validando su uso como herramienta de evaluación en este dominio” (p. 115), contradice la limitación 9 (p. 117). Tampoco se cuantifican las salidas del juez Grok corregidas a mano (p. 77) ni los casos alcanzados por la imputación de valores fuera de rúbrica (p. 82).

La rúbrica de precisión legal combina en una sola escala la exhaustividad y la exactitud de las citas, y su nivel intermedio casi no se utilizó: 3 %, 1 % y 1 % de las calificaciones de cada juez (Figura 25, p. 94). La baja confiabilidad era previsible. Dado que el banco registra los artículos de referencia de cada pregunta (p. 72), la calidad de las citas puede medirse sin jueces: basta extraer los artículos citados en cada respuesta y calcular precisión, exhaustividad y citas a artículos inexistentes. Así se recuperaría la dimensión que el marco teórico presenta como el riesgo central del dominio (pp. 36-37) y que quedó fuera del análisis (p. 96).

Se solicita documentar el proceso de validación del banco, revisar las respuestas de referencia, atenuar la afirmación sobre la validación de los jueces e incorporar, si es posible, una submuestra calificada por profesionales.

## V.8 Recuperación no evaluada

El manuscrito reconoce que “la calidad de la respuesta final está acotada por la calidad de la recuperación” (p. 32), pero no informa ninguna medida de recuperación. No hay exhaustividad a k, rango recíproco medio ni nDCG, aunque el banco contiene los artículos de referencia y el anexo describe un directorio dedicado a la “evaluación de la precisión de búsqueda vectorial para las preguntas del benchmark” (Tabla 17, p. 141). La lista de siglas incluye MRR y HNSW (p. 150), que no se utilizan en el texto.

El modelo de representaciones elegido, hiiamsid/sentence_similarity_spanish_es (p. 61), es un BERT en español ajustado para similitud semántica textual entre pares de oraciones, con una longitud máxima de 512 tokens (hiiamsid, s.f.). La similitud entre oraciones es una tarea simétrica y la recuperación de artículos a partir de una consulta es asimétrica. El desempeño en una no garantiza el desempeño en la otra (Muennighoff et al., 2023). No se lo comparó con modelos entrenados para recuperación ni con una línea de base léxica, y los artículos que exceden la longitud máxima se representan truncados. La afirmación de que un modelo exclusivamente en español “evita la pérdida de matices que introduce la traducción implícita de los modelos multilingües” (p. 60) no tiene respaldo empírico en el trabajo.

Asimismo, hay dos decisiones de implementación que merecen una aclaración. El índice IVF_FLAT (p. 59) es aproximado y no se informan sus parámetros; con 482 vectores, la búsqueda exacta elimina una fuente de pérdida sin costo apreciable. Además, los fragmentos sin texto se representaron “con un vector nulo” (p. 61), para el cual la similitud coseno no está definida.

## V.9 Versión y calidad del corpus

El corpus proviene del Boletín Oficial del 30 de mayo de 1997 (p. 57), es decir, del texto ordenado de ese año. El Código fue modificado con posterioridad: la Ley 25.225 sustituyó el inciso c) del artículo 3 y la Ley 27.111 sustituyó los artículos 31, 215 y 221. El manuscrito se contradice sobre este punto. Afirma que el texto fue “actualizado con los cambios publicados en el sitio Infoleg” (p. 2) y obtenido “desde Infoleg, aplicando técnicas de web scraping” (p. 4). Luego indica que las estrategias basadas en Infoleg “se descartaron” (p. 57) y, en la página siguiente, menciona un módulo que “transforma el HTML original en texto estructurado” (p. 58). Las respuestas esperadas, en cambio, “se elaboraron a partir del texto vigente” (p. 148). Si el corpus y la referencia corresponden a versiones distintas de la norma, las estrategias con recuperación pueden ser penalizadas por ser fieles a su fuente.

La extracción se realizó con un modelo generativo de visión y se validó por “inspección manual de una muestra de artículos” (p. 58), sin informar el tamaño de la muestra ni la tasa de error. Un modelo generativo puede alterar cifras, plazos o remisiones sin dejar rastro, lo que en un texto legal es crítico. El número de artículos tampoco es consistente: 245 (p. 36), 398 (Tabla 4, p. 58), 399 y 362 más 36 (p. 58). La Tabla 20 consigna como fecha de sanción el 1 de enero de 1994 (p. 147), mientras que la nota 18 indica el 25 de noviembre de 1886 (p. 57).

Se solicita precisar qué versión de cada artículo contiene la base, cuantificar la calidad de la extracción y unificar los datos descriptivos del corpus.

## V.10 Análisis de costos

El índice de eficiencia divide el desempeño por el costo normalizado con un piso de 0,01 (p. 93). Ese piso es arbitrario y determina por sí solo el valor de la configuración más barata, de modo que el ordenamiento refleja la constante elegida más que una propiedad de los sistemas. Una frontera de Pareto o el costo por respuesta correcta son alternativas sin ese problema.

Por otra parte, la recomendación de Agentic-RAG con gpt-5-mini como “Combinación costo-eficiente” (p. 97) no coincide con el propio análisis. Esa configuración cuesta USD 0,0564 por consulta, más que gpt-5 con RAG básico (USD 0,0392) o sin recuperación (USD 0,0478), según la Figura 22 (p. 91), y ocupa el séptimo lugar entre nueve en el índice de la Figura 24 (p. 93). El costo de gpt-5 sin recuperación, mayor que con RAG básico pese a recibir menos texto, confirma además el peso de los tokens de razonamiento señalado en V.4.

## V.11 Título, objetivos, alcance y reproducibilidad

El título alude a la “normativa nacional argentina” y el objetivo general a responder consultas de “usuarios profesionales y no profesionales en el derecho” (p. 6). El trabajo evalúa un único código, no incluye una interfaz (p. 5) y no realizó pruebas con usuarios (p. 117). El autor lo reconoce como limitación, pero el título y el objetivo deberían reflejar el alcance real o declararlo de manera expresa.

En cuanto al cuarto objetivo, el manuscrito indica que el código “se publicó en un repositorio público de GitHub” (p. 114). En la fecha de esta revisión, la dirección consignada (p. 147) devuelve un error 404, la respuesta que GitHub entrega cuando un repositorio no existe o es privado. El código, el banco de preguntas completo y los registros de ejecución no pudieron, por lo tanto, ser examinados, y el objetivo no puede darse por cumplido en estas condiciones. Se solicita habilitar el acceso público antes de la defensa y verificar que el repositorio incluye el banco de preguntas, los registros de ejecución y las salidas de los jueces.

# VI. MARCO TEÓRICO Y ASPECTOS FORMALES

El marco teórico es amplio y, en general, correcto. Su extensión, sin embargo, no guarda proporción con el uso que el resto del trabajo hace de él: los capítulos 2 a 4 ocupan 47 páginas. Contiene además errores que deben corregirse. La Tabla 2 reúne los verificados (en este caso se solicitó asistencia de modelos de IA para verificar las observaciones encontradas en la lectura de la tesis al igual que de las referencias que luego se volvieron a controlar manualmente).

Tabla 2

Errores e inconsistencias verificados en el texto

| Página | Texto del manuscrito | Observación |
| --- | --- | --- |
| p. 1 | “Al combinar grandes modelos de lenguaje (LLM) con mecanismos de recuperación de información.” | Oración trunca: falta la proposición principal. |
| p. 12 | Los n-gramas “consisten en secuencias de caracteres de longitud n”. | El ejemplo que sigue opera sobre palabras. La definición y el ejemplo no coinciden. |
| p. 23 | “La atención entre una query y todas las keys se calcula como la similitud coseno escalada”. | La operación es un producto escalar dividido por la raíz de la dimensión de las claves. No se normaliza por la norma de los vectores, por lo que no es una similitud coseno. |
| pp. 25-26 | GPT-4 “introduce arquitectura MoE”. | La fuente citada, el informe técnico de OpenAI, no describe la arquitectura del modelo. La afirmación carece de sustento documental. |
| pp. 30, 32 | Legal-BERT: modelos “preentrenados sobre el corpus Case Law Access Project (Harvard, 3.4 millones de casos federales y estatales de EE.UU.) que superó a BERT general en todas las tareas de LegalBench”. | LEGAL-BERT se preentrenó con unos 12 GB de legislación de la Unión Europea y del Reino Unido, fallos europeos, casos estadounidenses y contratos (Chalkidis et al., 2020). El corpus de Harvard con 3,4 millones de decisiones pertenece a otro trabajo (Zheng et al., 2021). LegalBench es de 2023 y no pudo emplearse para evaluar un modelo de 2020. |
| p. 36 | “el Código solo tiene 245 artículos”. | Contradice la Tabla 4 (398), el texto que la acompaña (399) y la nota 19 (362 más 36), todos en p. 58. |
| pp. 106-110 | DeepSeek-R1 fechado en enero de 2026, Llama 4 en marzo de 2026 y Qwen3 en diciembre de 2025. Gemini 3 Pro, el 20 de noviembre en el texto y el 18 en la Figura 27. | DeepSeek-R1 es de enero de 2025, como indica el propio manuscrito (p. 26) y su lista de referencias. Los lanzamientos de Llama 4 y Qwen3 son de abril de 2025 y deben verificarse. La sección 7.7 es periférica al objeto del trabajo y se apoya en anuncios comerciales: se sugiere reducirla o trasladarla a un anexo. |
| p. 147 | Tabla 20: “Fecha de sanción 1994-01-01”. | La nota 18 (p. 57) indica que la Ley 1.919 fue sancionada el 25 de noviembre de 1886. |
| pp. 34, 38, 73 y otras | “capítulo Sección 4”, “sección Sección 4.7”. | Referencias cruzadas duplicadas por la plantilla de edición. |
| p. 29 | Nota 13: remisión a Wikipedia. | Fuente no académica para un dato histórico. |
| p. iii | Dedicatoria: “A mi familia …”. | Tiene apariencia de texto provisorio. |
| p. iv | “Se han empleado productos basados en inteligencia artificial para asistir en la elaboración de este trabajo.” | Dado que el banco de preguntas, la extracción del corpus y la evaluación dependen de modelos de lenguaje, se solicita precisar en qué etapas de la redacción y del análisis se usaron estas herramientas y cómo se verificó lo producido. |

La redacción es clara y ordenada. Se sugiere una revisión final para eliminar las referencias cruzadas duplicadas, unificar el registro, que alterna la primera persona del plural con la forma impersonal, y reducir los anglicismos que tienen equivalente asentado.

# VII. FUENTES Y BIBLIOGRAFÍA

La lista supera las doscientas entradas y cubre de manera adecuada la literatura reciente sobre generación aumentada por recuperación, agentes y evaluación con jueces automáticos. Se verificó una muestra contra las fuentes primarias. La Tabla 3 presenta los problemas confirmados (ver comentario en el apartado VI).

Tabla 3

Problemas verificados en citas y referencias

| Entrada o cita | Problema verificado | Corrección |
| --- | --- | --- |
| Bommasani, Davis y Cardon (2023), citado en pp. 33 y 35; entrada en p. 122 | El título y el DOI corresponden a un artículo de Bozdag, Sevim y Koç publicado en ACM Transactions on Knowledge Discovery from Data (Bozdag et al., 2024). Los autores y la revista consignados no corresponden. El texto le atribuye además el uso de “variantes de adapters” (p. 33), mientras que el resumen del artículo describe un método basado en ajuste fino. | Reemplazar la entrada y contrastar con el artículo lo que se le atribuye. |
| Estudio de Stanford sobre alucinaciones en herramientas legales, atribuido a Dahl y col. (2024), p. 100 | El estudio publicado en el Journal of Empirical Legal Studies es de Magesh et al. (2025). La entrada de Dahl y col. (2024) corresponde a otro artículo, del Journal of Legal Analysis (p. 124). | Incorporar la referencia correcta y corregir la cita. |
| Wei y col. (2022); Zhao y col. (2026) | En cada caso hay dos obras distintas del mismo año (pp. 137, 138) citadas sin distinción (pp. 25, 34; pp. 24, 52). | Diferenciar con letras (2022a, 2022b). |
| DeepSeek (2026b), p. 124; Meta (2026), p. 130 | Entradas fechadas en 2026 para lanzamientos anteriores. DeepSeek-R1 ya figura como DeepSeek-AI (2025). | Corregir fechas y eliminar la duplicación. |
| Niklaus y col. (2024), LEXTREME, p. 131 | La entrada indica 2024 y, a la vez, Findings of EMNLP 2023. | Unificar el año. |
| Tribunal Fiscal de la Nación (2026), p. 136 | La dirección remite a una nota publicada por un estudio jurídico, no al organismo. | Citar la fuente oficial o al autor real de la nota. |
| Ausencias | No se cita el trabajo que introdujo la generación aumentada por recuperación (Lewis et al., 2020). Tampoco hay una entrada para el Código de Minería como fuente legal. | Incorporar ambas. |
| Preprints y material de proveedores | Numerosas entradas remiten a arXiv aunque existe versión con revisión de pares (por ejemplo, BERT, LoRA, QLoRA y Self-RAG) y a blogs comerciales. | Preferir las versiones publicadas. |
| Forma | Alternan “y col.” y “y cols.”. En sitios web se usa la fecha de consulta como fecha de publicación. | Uniformar según APA, séptima edición. |

La primera fila describe una entrada cuyos autores no corresponden a la publicación. Por esa razón se solicita una auditoría completa de la lista: cada entrada debe poder rastrearse hasta su DOI o su dirección, y cada afirmación atribuida debe haberse contrastado con la fuente.

# VIII. VALIDEZ DE LAS CONCLUSIONES

La Tabla 4 contrasta las conclusiones principales del manuscrito con la evidencia que las sostiene.

Tabla 4

Conclusiones del manuscrito y valoración de su sustento

| Conclusión | Valoración |
| --- | --- |
| La recuperación “mejora significativamente la calidad de las respuestas” (p. 97). | Se sostiene para gpt-5-mini, con un efecto grande. No para gpt-5, donde ninguna diferencia es significativa tras la corrección, ni para gpt-5-nano, cuya mediana con RAG básico es igual a la obtenida sin recuperación (0,583; Tabla 11, p. 87). Debe formularse como resultado condicional al modelo. |
| La interacción entre estrategia y modelo como hallazgo principal (p. 114). | El patrón descriptivo es claro. El sustento inferencial debe rehacerse (V.1, V.2) y la interpretación depende del diagnóstico de la celda anómala (V.6) y de la confusión de factores (V.5). |
| “Efecto igualador del RAG básico” (p. 114). | No se sostiene con la evidencia presentada (V.3). |
| “Identificación de la sobrecarga agéntica en modelos pequeños” (p. 114). | No se sostiene como explicación causal sin análisis de los registros (V.6). |
| “Validación de LLM-as-a-Judge para evaluación legal” (p. 115). | No se sostiene. Se mostró acuerdo entre jueces, no validez frente a criterio humano (V.7). |
| El objetivo 2 “se cumplió completamente” (p. 113). | Cumplimiento parcial. El agente de verificación fue desactivado y el agente principal realiza una única recuperación (V.5). |
| “Combinación costo-eficiente: Agentic-RAG + gpt-5-mini” (p. 97). | No coincide con las Figuras 22 y 24 (V.10). |
| “Este resultado es transferible a otros dominios y aplicaciones de RAG” (p. 120). | No se sostiene. Un corpus, un banco de 25 casos, una familia de modelos y una ejecución por celda no permiten generalizar. |
| Atención a “usuarios profesionales y no profesionales” (p. 6) y publicación en repositorio abierto (p. 114). | Sin evaluación con usuarios ni interfaz. La dirección del repositorio devuelve un error 404, por lo que el código no es accesible (V.11). |

# IX. CORRECCIONES REQUERIDAS Y RECOMENDACIONES

## IX.1 Correcciones requeridas para la versión definitiva

1. Rehacer el análisis inferencial con procedimientos que respeten el apareamiento por unidad y el anidamiento en casos, con tamaños de efecto e intervalos de confianza (V.1, V.2).

2. Diagnosticar la celda gpt-5-nano con Agentic-RAG a partir de los registros, informar los faltantes por celda y reformular la contribución relativa a la “sobrecarga agéntica” (V.6).

3. Documentar los parámetros efectivamente enviados a la API, incluido el esfuerzo de razonamiento, y retirar la afirmación de determinismo, salvo que los registros demuestren que la temperatura cero fue aplicada. Declarar como limitación la ejecución única (V.4).

4. Declarar la confusión de factores, reproducir todos los prompts y resolver las contradicciones sobre el Agente de Calidad y el límite de búsquedas (V.5).

5. Reformular las conclusiones señaladas en la Tabla 4.

6. Precisar la versión del corpus, resolver las contradicciones sobre su origen y revisar las respuestas de referencia observadas (V.7, V.9).

7. Corregir los errores de la Tabla 2 y de la Tabla 3, con una auditoría completa de las referencias.

8. Habilitar el acceso público al repositorio, cuya dirección devuelve un error 404 en la fecha de esta revisión, y ampliar la declaración sobre el uso de herramientas de inteligencia artificial.

## IX.2 Recomendaciones

Las siguientes acciones no condicionan la aprobación, pero mejorarían de manera sustancial el trabajo o una eventual publicación derivada.

1. Evaluar la recuperación de forma aislada con los artículos de referencia del banco, y comparar el modelo de representaciones con al menos una alternativa entrenada para recuperación y con una línea de base léxica o híbrida.

2. Calcular de manera determinista la precisión y la exhaustividad de las citas de artículos, y contar las citas a artículos inexistentes.

3. Validar una submuestra de calificaciones con uno o dos profesionales del derecho y medir el acuerdo entre personas y jueces automáticos.

4. Ejecutar entre tres y cinco réplicas de las celdas críticas y una ablación con el mismo modelo en ambos agentes.

5. Reducir el capítulo 2 y la sección 7.7 para concentrar el texto en el aporte propio.

# X. DICTAMEN

Por lo expuesto, este miembro del tribunal considera que el trabajo reúne las condiciones para ser defendido oralmente y propone su aceptación para esa instancia. La calificación final quedará sujeta al desempeño del tesista en la defensa, en particular a su capacidad para responder las observaciones sobre el diseño experimental, la celda anómala y el alcance de las conclusiones.

Mg. Lic. Prof. Gastón Pezzuchi, MSc.

Miembro del tribunal

# REFERENCIAS

Blair, R. C., Sawilowsky, S. S., & Higgins, J. J. (1987). Limitations of the rank transform statistic in tests for interactions. Communications in Statistics - Simulation and Computation, 16(4), 1133-1145.

Bozdag, M., Sevim, N., & Koç, A. (2024). Measuring and mitigating gender bias in legal contextualized language models. ACM Transactions on Knowledge Discovery from Data, 18(4), 1-26. https://doi.org/10.1145/3628602

Chalkidis, I., Fergadiotis, M., Malakasiotis, P., Aletras, N., & Androutsopoulos, I. (2020). LEGAL-BERT: The Muppets straight out of law school. En Findings of the Association for Computational Linguistics: EMNLP 2020 (pp. 2898-2904). Association for Computational Linguistics. https://aclanthology.org/2020.findings-emnlp.261

Decreto 456/1997. Código de Minería. Texto ordenado. Boletín Oficial de la República Argentina, 28.658, 30 de mayo de 1997.

Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. Journal of Machine Learning Research, 7, 1-30. https://www.jmlr.org/papers/v7/demsar06a.html

Droniu. (s.f.). [Bug] Off Topic Prompts guardrail fails with GPT-5 models due to hardcoded temperature: 0.0 (Incidencia n.º 29) [Informe de error en el repositorio openai/openai-guardrails-js]. GitHub. Recuperado el 11 de noviembre de 2026, de https://github.com/openai/openai-guardrails-js/issues/29

Dror, R., Baumer, G., Shlomov, S., & Reichart, R. (2018). The hitchhiker’s guide to testing statistical significance in natural language processing. En Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (pp. 1383-1392). Association for Computational Linguistics. https://doi.org/10.18653/v1/P18-1128

hiiamsid. (s.f.). hiiamsid/sentence_similarity_spanish_es [Modelo de representaciones de oraciones]. Hugging Face. Recuperado el 11 de noviembre de 2026, de https://huggingface.co/hiiamsid/sentence_similarity_spanish_es

Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Küttler, H., Lewis, M., Yih, W., Rocktäschel, T., Riedel, S., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33, 9459-9474. https://papers.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html

Ley 25.225. Código de Minería. Sustitución del inciso c) del artículo 3. Boletín Oficial de la República Argentina, 29 de diciembre de 1999. https://www.argentina.gob.ar/normativa/nacional/ley-25225-61722/texto

Ley 27.111. Código de Minería. Decreto 456/1997. Modificación. Sancionada el 17 de diciembre de 2014 y promulgada de hecho el 20 de enero de 2015. Boletín Oficial de la República Argentina. https://www.boletinoficial.gob.ar/pdf/linkQR/MUJtOTlvaEFlbUZycmZ0RFhoUThyQT09

Magesh, V., Surani, F., Dahl, M., Suzgun, M., Manning, C. D., & Ho, D. E. (2025). Hallucination-free? Assessing the reliability of leading AI legal research tools. Journal of Empirical Legal Studies, 22(2), 216-242. https://doi.org/10.1111/jels.12413

Microsoft. (2026, 23 de octubre). Azure OpenAI reasoning models. Microsoft Learn. https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reasoning

Muennighoff, N., Tazi, N., Magne, L., & Reimers, N. (2023). MTEB: Massive text embedding benchmark. En Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics (pp. 2014-2037). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.eacl-main.148

Pydantic. (s.f.). pydantic_ai.profiles [Documentación de la API de Pydantic AI]. Recuperado el 11 de noviembre de 2026, de https://pydantic.dev/docs/ai/api/pydantic-ai/profiles/

Pydantic. (2025). pydantic-ai-slim (Versión 1.1.0) [Software]. Python Package Index. https://pypi.org/project/pydantic-ai-slim/1.1.0/

Scheirer, C. J., Ray, W. S., & Hare, N. (1976). The analysis of ranked data derived from completely randomized factorial designs. Biometrics, 32(2), 429-434. https://doi.org/10.2307/2529511

Seaman, J. W., Walls, S. C., Wise, S. E., & Jaeger, R. G. (1994). Caveat emptor: Rank transform methods and interaction. Trends in Ecology & Evolution, 9(7), 261-263.

Spairani, L. U. (2026). Desarrollo y evaluación de un prototipo de sistema inteligente para consulta de normativa nacional argentina mediante recuperación agéntica [Tesis de maestría, Universidad Austral].

Wobbrock, J. O., Findlater, L., Gergle, D., & Higgins, J. J. (2011). The aligned rank transform for nonparametric factorial analyses using only ANOVA procedures. En Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 143-146). Association for Computing Machinery. https://doi.org/10.1145/1978942.1978963

Zheng, L., Guha, N., Anderson, B. R., Henderson, P., & Ho, D. E. (2021). When does pretraining help? Assessing self-supervised learning for law and the CaseHOLD dataset. En Proceedings of the 18th International Conference on Artificial Intelligence and Law. Association for Computing Machinery. https://arxiv.org/abs/2104.08671

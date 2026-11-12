---
title: "Valoraci\u00f3n del Trabajo Final de Maestr\u00eda"
creator: "Gast\u00f3n Pezzuchi"
created: "2026-11-11T19:27:00Z"
modified: "2026-11-12T13:10:00Z"
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

Este informe amplía y fundamenta la evaluación sintética consignada en el formulario institucional. Se basa en la lectura completa del manuscrito, en el control de su consistencia interna y en la verificación, contra fuentes primarias, de sus referencias y de las afirmaciones técnicas que sustentan el diseño experimental. Las páginas citadas corresponden a la numeración impresa del manuscrito (Spairani, 2026a), no a la numeración interna del archivo.

La valoración se centra en los aspectos propios de la minería de datos y del aprendizaje automático: diseño experimental, medición, análisis estadístico y el sustento de las conclusiones. Las cuestiones estrictamente jurídicas se señalan únicamente cuando se entiende que afectan la validez del instrumento de evaluación.

Este documento es una actualización de nuestra versión anterior. Por lo tanto, el informe tuvo dos etapas. La primera versión se elaboró sin acceso al repositorio de código, cuya URL devolvía un error 404. El 11 de noviembre de 2026, el repositorio quedó accesible y las observaciones se contrastaron con el código, los registros de ejecución y los datos allí publicados (Spairani, 2026b). Los apartados de la sección V incorporan ese contraste, y el Anexo detalla qué se sostenía antes del acceso y qué se confirmó, se corrigió o se agregó, para resumir la información colocada en ese anexo, se utilizó asistencia de IA.

# II. SÍNTESIS DEL TRABAJO

El trabajo presenta el diseño, la implementación y la evaluación de un prototipo de consulta en lenguaje natural sobre el Código de Minería argentino. El sistema combina una base vectorial (Milvus) con representaciones de 768 dimensiones, un esquema de recuperación simple y un esquema de dos agentes implementado con Pydantic AI. La evaluación sigue un diseño factorial con tres estrategias (sin recuperación, RAG básico y Agentic-RAG) y tres modelos (gpt-5-nano, gpt-5-mini y gpt-5), sobre 25 casos que se descomponen en 79 unidades de evaluación, con un total de 711 observaciones (Spairani, 2026a, pp. 56, 79).

La variable de respuesta principal es el promedio de las calificaciones de tres jueces automáticos en una rúbrica de cinco niveles. El hallazgo que el autor destaca es la interacción entre estrategia y modelo: el esquema agéntico favorece a gpt-5-mini, no produce diferencias significativas en gpt-5 y degrada a gpt-5-nano (Spairani, 2026a, pp. 85-90).

# III. DICTAMEN Y CALIFICACIÓN POR CRITERIO[^1]

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

1. Pertinencia y originalidad local. El trabajo se ocupa de normativa argentina, en español y dentro de la tradición del derecho continental, un terreno poco cubierto por una literatura que se concentra en el inglés y en el derecho anglosajón. El autor no identificó bancos de evaluación públicos para normativa argentina (Spairani, 2026a, p. 105) y construyó uno.

2. Sistema completo y trazable. El prototipo cubre la extracción del corpus, la indexación vectorial, dos esquemas de recuperación, la generación y la evaluación. Cada interacción entre agentes queda registrada en archivos JSON (pp. 66, 77-78), lo que permite auditar el comportamiento del sistema y rehacer análisis sin nuevas ejecuciones. El repositorio publicado lo confirma: reúne el código, el banco de preguntas, los registros y las calificaciones de los jueces, y permitió verificar las observaciones de este informe (Spairani, 2026b).

3. Diseño comparativo con dos líneas de base. La inclusión de la respuesta sin recuperación y del RAG básico permite distinguir el aporte de la recuperación del aporte de la orquestación con agentes.

4. Evaluación con jueces heterogéneos. Los tres jueces provienen de proveedores distintos del que desarrolla los modelos evaluados (p. 73), lo que reduce el riesgo de que un juez favorezca respuestas de su misma familia. El acuerdo se cuantificó con el alfa de Krippendorff y la rúbrica de precisión legal se descartó cuando su confiabilidad resultó insuficiente (pp. 95-96). Es una decisión metodológicamente correcta.

5. Cuidado en las comparaciones múltiples. Tras detectar la interacción, el autor analizó efectos simples y aplicó la corrección de Holm (pp. 84-85), sin apoyarse en los valores p sin corregir.

6. Análisis de costos. El registro de tokens y costos por configuración (pp. 90-93) agrega una dimensión de decisión que muchos trabajos de este tipo omiten.

7. Franqueza sobre las limitaciones. El capítulo final declara diez limitaciones, entre ellas la falta de validación humana de los jueces y la ausencia de razonamiento explícito en sus instrucciones (pp. 116-118).

# V. OBSERVACIONES SUSTANTIVAS

Las observaciones se ordenan según su efecto sobre la validez de las conclusiones. Cada una indica la evidencia en el manuscrito y lo que se solicita al autor.

## V.1 Estructura de dependencia de los datos y pruebas estadísticas

Las mismas 79 unidades de evaluación se responden en las nueve configuraciones: “79 unidades de evaluación × 9 configuraciones = 711 observaciones” (Spairani, 2026a, p. 79). Las observaciones están, por lo tanto, apareadas por unidad. Además, las unidades son subpreguntas anidadas en 25 casos, aunque el texto las presenta como “unidades de evaluación independientes” (p. 71). El análisis emplea Kruskal-Wallis, Dunn, Mann-Whitney y Scheirer-Ray-Hare (pp. 76, 83-88), procedimientos diseñados para muestras independientes. El último fue propuesto específicamente para diseños factoriales completamente aleatorizados (Scheirer et al., 1976).

Ignorar el apareamiento tiene, en principio, dos consecuencias principales. La variabilidad entre unidades, que refleja la dificultad de cada pregunta, queda dentro del término de error y reduce la potencia. Además, los valores p dejan de ser válidos, porque las observaciones no son independientes. Para comparar sistemas sobre un mismo conjunto de ítems, la literatura de aprendizaje automático y de procesamiento del lenguaje recomienda pruebas para muestras relacionadas, como Wilcoxon de rangos con signo y Friedman (Demšar, 2006; Dror et al., 2018). Una alternativa más completa es un modelo ordinal con efectos aleatorios por caso y por subpregunta. El anexo indica que el directorio de análisis contiene “modelos mixtos” (Tabla 17, p. 141). El repositorio muestra que no fueron estimados: el cuaderno 04_modelo_mixto_interaccion solo ejecuta la prueba de Scheirer-Ray-Hare (Spairani, 2026b).

Esta observación no es solo formal. En gpt-5, las diferencias de Agentic-RAG frente a las otras dos estrategias tienen valores p sin corregir de 0,013 y 0,025, que pasan a 0,064 y 0,074 tras la corrección (Tabla 10, p. 85). La conclusión de que en gpt-5 no hay diferencias significativas (p. ii) descansa en una prueba que desaprovecha el apareamiento y podría modificarse con el análisis estadístico adecuado. Tampoco se informan tamaños de efecto ni intervalos de confianza, y el texto menciona “n = 79 observaciones por celda” (p. 97) aunque 27 observaciones fueron eliminadas (pp. 82-83).

Los datos del repositorio permitieron comprobarlo (Spairani, 2026b). Se reconstruyó, con asistencia de IA, la variable de respuesta a partir de las calificaciones de los jueces, obteniendo un resultado idéntico al del autor en las 684 observaciones que él analiza, y se repitieron las comparaciones sobre las 79 unidades con pruebas para muestras relacionadas: Friedman y Wilcoxon de rangos con signo, con corrección de Holm. Dos conclusiones cambian. Dentro del RAG básico, los modelos difieren (Friedman, χ² = 23,43; p < 0,001): gpt-5-nano queda por debajo de gpt-5 (p = 0,001) y de gpt-5-mini (p = 0,005). En gpt-5, Agentic-RAG supera al RAG básico (p = 0,009) y a la respuesta sin recuperación (p = 0,022). Ambos resultados se mantienen cuando las calificaciones se promedian por caso (n = 25; p = 0,008 y p = 0,009). Este reanálisis es meramente ilustrativo y no sustituye al que corresponde al autor.

Se solicita rehacer el análisis inferencial utilizando procedimientos que respeten el apareamiento y el anidamiento, informar los tamaños del efecto con sus intervalos de confianza y corregir la mención a los modelos mixtos.

## V.2 Prueba de interacción

El hallazgo que el autor considera más relevante es la interacción entre la estrategia y el modelo, respaldada por la prueba de Scheirer-Ray-Hare (H = 56,62; Tabla 12, p. 88). Esta prueba aplica un análisis de varianza a los rangos globales. Ahora bien, la literatura estadística advierte desde hace décadas que la transformación a rangos no es adecuada para contrastar interacciones cuando existen efectos principales, porque el estadístico puede resultar poco robusto (Blair et al., 1987; Seaman et al., 1994). La transformación a rangos alineados es la alternativa habitual (Wobbrock et al., 2011).

El patrón descriptivo de la Figura 21 y de la Tabla 13 (pp. 89-90) es lo bastante marcado como para que la interacción sea plausible. Por lo tanto, requiere corrección el  sustento inferencial y, sobre todo, su interpretación, que depende de las observaciones V.5 y V.6 (ver más abajo).

## V.3 Equivalencia inferida de la falta de significación

El trabajo afirma que “el RAG básico elimina las diferencias de desempeño entre modelos de distinta capacidad” (p. ii) y lo presenta como una contribución demostrada (p. 114). El sustento es una prueba de Kruskal-Wallis no significativa (H = 4,71; p = 0,095; p. 84). Ahora bien, la ausencia de significación no demuestra equivalencia. Con RAG básico las medianas son 0,583 para gpt-5-nano, 0,625 para gpt-5-mini y 0,833 para gpt-5 (Tabla 11, p. 87), y la distancia entre los extremos equivale a un nivel completo de la rúbrica. Una afirmación de equivalencia exige una prueba de equivalencia con un margen definido de antemano o, al menos, intervalos de confianza para las diferencias. El reanálisis con pruebas apareadas descrito en V.1 muestra, además, que esas diferencias son significativas. Se solicita reformular la conclusión.

## V.4 Control experimental: temperatura, razonamiento y réplicas

El manuscrito declara temperatura cero en todas las configuraciones “para garantizar reproducibilidad” (p. 79), la incluye entre los criterios de selección de modelos (p. 70) y la fija en el código de ambos agentes mediante el ajuste “temperature=0.0” (pp. 66-67). Ahora bien, los modelos gpt-5, gpt-5-mini y gpt-5-nano son modelos de razonamiento y no admiten los parámetros de muestreo, entre ellos la temperatura (Microsoft, 2026). La API de OpenAI rechaza las solicitudes que fijan la temperatura en cero en estos modelos, con un error que indica que solo se admite el valor predeterminado (Droniu, s.f.).

El destino del parámetro se pudo verificar en el código de la biblioteca. El anexo declara la versión 1.1.0 de Pydantic AI (p. 142), publicada el 15 de octubre de 2025. En esa versión, el perfil de los modelos de OpenAI clasifica como modelo de razonamiento a todo identificador que comience con “gpt-5” e incluye la temperatura entre los ajustes no admitidos; antes de construir la solicitud, la clase del modelo elimina esos ajustes sin emitir advertencia ni error (Pydantic, 2025). La documentación de la biblioteca describe el mismo mecanismo (Pydantic, s.f.). El tratamiento está presente, con otra implementación, desde la versión 0.7.0, del 12 de agosto de 2025, por lo que cubre el período de experimentación informado: “agosto-noviembre 2025” (p. 71). En las versiones previas, el parámetro se enviaba y la API lo habría rechazado. En ningún caso, por lo tanto, la temperatura cero tuvo efecto. Los tres modelos operaron con el muestreo predeterminado, lo que explica que las ejecuciones se completaran sin fallos y que el problema pasara inadvertido.

El repositorio confirma esta conclusión (Spairani, 2026b). La versión 1.1.0 está fijada en el archivo de dependencias y los modelos se invocan a través del proveedor de OpenAI con los nombres gpt-5-nano, gpt-5-mini y gpt-5. Las corridas registradas son del 19 de octubre, del 2 de noviembre y del 12 y 13 de noviembre de 2025, todas posteriores a la publicación de esa versión. Los 474 registros de conversación de la estrategia agéntica guardan vacíos los ajustes del modelo, porque la biblioteca quita la temperatura del propio objeto de configuración. En las otras dos estrategias el registro conserva el valor 0,0, pero lo que allí se guarda es la configuración del agente y no la solicitud enviada. En todas las celdas, entre el 59 % y el 91 % de los tokens de salida son de razonamiento, y el código no fija el esfuerzo de razonamiento, que quedó en su valor predeterminado. El anexo del manuscrito ya lo dejaba ver: una respuesta breve de gpt-5-nano consumió 315 tokens de entrada y 7.818 de salida (p. 143).

Esto genera dos consecuencias. Las respuestas no son deterministas y existe un parámetro que incide en la calidad y en el costo sin control ni registro. Además, la temperatura cero se invoca para justificar una única ejecución por celda: “evita múltiples ejecuciones” (p. 74). Con una sola ejecución no es posible separar el efecto de los factores de la variabilidad entre corridas. Las diferencias marginales señaladas en V.1 para gpt-5 pueden quedar dentro de esa variabilidad. El costo total informado, USD 22,29 (p. 93), muestra que repetir el experimento varias veces era viable.

Se solicita retirar la afirmación de determinismo, informar que el esfuerzo de razonamiento quedó en su valor predeterminado, declarar como limitación la ejecución única y, de ser posible, agregar réplicas de las celdas críticas.

## V.5 Factores confundidos y alcance del término Agentic-RAG

En la estrategia agéntica el Agente de Recuperación utiliza siempre gpt-5, cualquiera sea el modelo del Agente Especialista Legal (Tabla 6, p. 70). El factor modelo tiene entonces un significado distinto en cada nivel del factor estrategia: en las dos primeras estrategias designa el único modelo que interviene y en la tercera, solo el que redacta la respuesta. La configuración denominada Agentic-RAG con gpt-5-nano es, en rigor, un sistema mixto. Los costos lo reflejan: en esa celda, USD 3,41 de los 3,53 gastados corresponden al agente de recuperación (Spairani, 2026b).

Las estrategias difieren además en otros aspectos que no se controlan. El prompt de las configuraciones sin RAG y con RAG básico es un “prompt simplificado” (p. 66) que el manuscrito no reproduce. El repositorio muestra que también contiene una instrucción de abstención, con otra redacción, y que solo la estrategia agéntica exige una salida estructurada (Spairani, 2026b). El RAG básico recupera diez fragmentos con la consulta original (p. 62), mientras que el esquema agéntico ejecuta hasta seis búsquedas de cinco fragmentos y luego gpt-5 selecciona los que entrega (pp. 67-69). Los registros indican que la corrida de gpt-5 admitió siete búsquedas y las de los otros dos modelos, seis, y que la instrucción del agente de recuperación incluye, en lugar del número máximo de búsquedas, la representación textual de un objeto de programación. Sin ablaciones, la diferencia entre estrategias no puede atribuirse a la descomposición de consultas, a la mayor cantidad de candidatos, a la selección realizada por gpt-5 o al cambio de instrucciones.

Por último, el sistema evaluado es más limitado que el descrito en el marco teórico. El Agente Especialista Legal puede invocar la recuperación una sola vez: su prompt indica “utilizas la herramienta retrieve_relevant_documents una vez” (p. 63) y el código fija DOCUMENT_RETRIEVAL_LIMIT = 1 (p. 68). El Agente de Calidad, encargado de verificar la pertinencia de lo recuperado, fue desactivado (p. 65). El manuscrito sostiene, sin embargo, que “se optó por actualizar los prompts del Agente Especialista Legal para que este pudiera solicitar búsquedas adicionales” (p. 65), lo que contradice el límite anterior. Ofrece además dos motivos distintos para la desactivación: que no produjo mejoras (p. 62) y que agregaba costo y una variable más (p. 65), sin datos de esa comparación.

El capítulo 3 afirma que el sistema combina “few-shot prompting para fijar el formato de respuesta, Chain-of-Thought para inducir razonamiento explícito” (p. 35), pero los prompts reproducidos no contienen ejemplos ni instrucciones de razonamiento (pp. 63-64). Lo evaluado se aproxima a un RAG con descomposición de consultas delegada en gpt-5, sin iteración ni verificación.

Se solicita declarar estas confusiones como amenazas a la validez, reproducir todos los prompts utilizados, resolver las contradicciones señaladas y ajustar la denominación de la estrategia o el alcance de lo que se afirma sobre ella.

## V.6 La celda gpt-5-nano con Agentic-RAG y los datos faltantes

La configuración de gpt-5-nano con Agentic-RAG tiene mediana 0,083 (Tabla 11, p. 87) y media 0,40 (Tabla 13, p. 90). Una distancia semejante entre mediana y media indica una distribución bimodal: muchas respuestas con puntaje casi nulo y otras con puntaje alto. Las métricas textuales apuntan en la misma dirección. La mediana de similitud SBERT cae a 0,389, cuando en las demás celdas de ese modelo no baja de 0,74 (Tabla 11). La Figura 20 muestra, solo en el grupo agéntico, valores de BERTScore iguales a cero y un conjunto de valores de SBERT por debajo de 0,3 (p. 82). En la Figura 21, la media de BERTScore de gpt-5-nano desciende de alrededor de 0,71 a 0,45 únicamente en esa celda (p. 89).

Un BERTScore nulo o una similitud semántica cercana a cero no describen una respuesta jurídicamente peor, sino un texto vacío o ajeno a la referencia: una abstención, un mensaje de error o una salida truncada. El ejemplo del anexo muestra que, cuando responde, gpt-5-nano con Agentic-RAG produce una respuesta correcta y bien fundada (p. 145). Los datos son compatibles con un modo de falla que afecta a una parte de los ítems y no con una degradación general. El manuscrito lo atribuye a que “la complejidad agéntica es excesiva para modelos de capacidad reducida” (p. 86) y lo presenta como contribución (p. 114), sin examinar los registros de ejecución, que están disponibles (pp. 77-78).

El repositorio confirma esta lectura (Spairani, 2026b). De las 79 salidas de esa celda, 28 están vacías y 13 son marcadores o mensajes que no responden la pregunta, como “TEST”, “placeholder” o “PENDING”. El modelo invoca la salida estructurada, que solo esta estrategia exige, y la entrega sin contenido después de consumir miles de tokens de razonamiento. Las 38 respuestas sustantivas tienen una media de 0,82, que no difiere de la de gpt-5 en las mismas unidades (0,84; p = 0,19) y supera a la del propio gpt-5-nano con RAG básico (0,64; p = 0,003). La caída de la celda no expresa una pérdida de calidad jurídica, sino una falla del canal de salida en algo más de la mitad de los ítems. Un cuaderno del repositorio muestra que el autor detectó las respuestas vacías y decidió conservarlas; el manuscrito no las menciona.

A esto se suma el tratamiento de los faltantes. El manuscrito informa que se eliminaron 27 observaciones sin calificación de los jueces, “atribuibles a fallos puntuales en la generación de respuestas” (p. 82). Los datos del repositorio muestran otra cosa: las 27 corresponden a los casos 23, 24 y 25 en las nueve configuraciones. Son los tres casos sin subpreguntas, tienen respuesta en todas las celdas y fueron calificados por los tres jueces. La clave de subpregunta está vacía en una tabla y vale cero en la otra, lo que explica que no se hayan combinado. Las respuestas vacías de gpt-5-nano, en cambio, no se excluyeron: se calificaron con cero y permanecen en el análisis. El análisis inferencial se hizo, entonces, sobre 76 unidades de 22 casos, y la explicación del manuscrito no corresponde a lo ocurrido (Spairani, 2026b).

Tampoco se discute que, sin recuperación, gpt-5-nano obtenga una mediana superior a la de gpt-5-mini (0,583 frente a 0,333; Tabla 11, p. 87), resultado contrario al orden de capacidad de los modelos. Las respuestas publicadas sugieren la causa: gpt-5-mini declara con frecuencia que no dispone del texto legal, como le indica la instrucción del sistema, y la rúbrica penaliza esa reserva (Spairani, 2026b).

Se solicita informar las salidas vacías y los marcadores de esa celda, reincorporar los casos 23 a 25, corregir la explicación de los faltantes, repetir el análisis tratando los fallos como puntaje cero y como exclusión, y reformular la contribución relativa a la “sobrecarga agéntica” como un problema de confiabilidad de la salida estructurada.

## V.7 Validez de la medición

La variable de respuesta mide la alineación con una respuesta esperada (Tabla 8, p. 74). Esas respuestas fueron generadas por GPT-4.1 (p. 71), un modelo del mismo proveedor que los evaluados, y revisadas por un único profesional (p. 72). No se informa cuántas fueron corregidas ni existe un segundo revisor. La validez de toda la medición depende, entonces, de un instrumento cuya calidad no está documentada.

Los dos ejemplos publicados en el anexo justifican la preocupación. La respuesta esperada 1.2 afirma: “La propiedad minera constituye un derecho real separado de la propiedad del suelo (art. 8)” (p. 149). El capítulo 5, en cambio, describe el artículo 8 como “facultad de buscar minas” y el artículo 11 como “propiedad distinta del terreno” (p. 69), en línea con el texto del artículo 11 del Código (Decreto 456/1997). La respuesta esperada 1.3 sostiene que la propietaria “solo puede oponerse por razones de seguridad o ambientales (art. 17)” (p. 149). El artículo 17 dispone que los trabajos no pueden ser impedidos ni suspendidos sino cuando lo exija la seguridad pública, la conservación de las pertenencias y la salud o existencia de los trabajadores (Decreto 456/1997). Corresponde que el tesista y el profesional que validó el banco aclaren estos puntos. Para la evaluación importa su efecto: un sistema que cite el artículo correcto puede ser penalizado por apartarse de la referencia.

Los jueces automáticos no fueron contrastados con criterio humano, como el propio autor reconoce al señalar que se trata de jueces “cuya alineación con criterios humanos no ha sido validada” (p. 97). El acuerdo entre jueces mide confiabilidad, no validez: tres modelos pueden coincidir y compartir un mismo sesgo, por ejemplo hacia respuestas extensas o de estilo similar al de la referencia. Por eso la contribución 6, que da el método por validado, “validando su uso como herramienta de evaluación en este dominio” (p. 115), contradice la limitación 9 (p. 117). Tampoco se cuantifican las salidas del juez Grok corregidas a mano (p. 77) ni los casos alcanzados por la imputación de valores fuera de rúbrica (p. 82). El repositorio aporta un indicio concreto sobre la validez: el juez DeepSeek calificó con 1,0, 0,85 y 0,9 tres respuestas vacías de gpt-5-nano, con fundamentos que describen un contenido inexistente (Spairani, 2026b).

La rúbrica de precisión legal combina en una sola escala la exhaustividad y la exactitud de las citas, y su nivel intermedio casi no se utilizó: 3 %, 1 % y 1 % de las calificaciones de cada juez (Figura 25, p. 94). La baja confiabilidad era previsible. Dado que el banco registra los artículos de referencia de cada pregunta (p. 72), la calidad de las citas puede medirse sin jueces: basta extraer los artículos citados en cada respuesta y calcular precisión, exhaustividad y citas a artículos inexistentes. Así se recuperaría la dimensión que el marco teórico presenta como el riesgo central del dominio (pp. 36-37) y que quedó fuera del análisis (p. 96).

Se solicita documentar el proceso de validación del banco, revisar las respuestas de referencia, atenuar la afirmación sobre la validación de los jueces e incorporar, si es posible, una submuestra calificada por profesionales.

## V.8 Recuperación no evaluada

El manuscrito reconoce que “la calidad de la respuesta final está acotada por la calidad de la recuperación” (p. 32), pero no informa ninguna medida de recuperación. No hay exhaustividad a k, rango recíproco medio ni nDCG, aunque el banco contiene los artículos de referencia y el anexo describe un directorio dedicado a la “evaluación de la precisión de búsqueda vectorial para las preguntas del benchmark” (Tabla 17, p. 141). La lista de siglas incluye MRR y HNSW (p. 150), que no se utilizan en el texto.

Los datos del repositorio permiten calcular esas medidas (Spairani, 2026b). El directorio de recuperación registra la posición de cada artículo de referencia en la búsqueda vectorial, y las respuestas guardan los fragmentos utilizados. En el RAG básico, los diez fragmentos contienen todos los artículos de referencia en el 27,8 % de las unidades y ninguno en el 59,5 %; la exhaustividad media es 0,33 y el rango recíproco medio, 0,21. En la estrategia agéntica, los fragmentos entregados al especialista alcanzan una exhaustividad de entre 0,54 y 0,58. La ventaja del esquema agéntico es, en buena medida, una ventaja de recuperación, y en ambos casos la recuperación es el eslabón débil del sistema.

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

En cuanto al cuarto objetivo, el manuscrito indica que el código “se publicó en un repositorio público de GitHub” (p. 114). Durante la primera revisión, la dirección consignada (p. 147) devolvía un error 404. El repositorio quedó accesible el 11 de noviembre de 2026 y contiene el código, el banco de preguntas, los registros de ejecución y las calificaciones de los jueces (Spairani, 2026b). Esa disponibilidad es un mérito del trabajo, porque permitió verificar las observaciones de este informe. Su historial comienza en junio de 2026, de modo que no documenta la evolución del código durante los experimentos.

El repositorio permite además dimensionar el uso de inteligencia artificial. La declaración del manuscrito se limita a una oración: “Se han empleado productos basados en inteligencia artificial para asistir en la elaboración de este trabajo” (p. iv). El repositorio contiene instrucciones para agentes que redactan borradores de secciones y gestionan la bibliografía, y su historial registra la eliminación de una referencia que el propio autor califica de fabricada (Spairani, 2026b). El uso de estas herramientas no es objetable en sí mismo, pero la declaración debería precisar su alcance.

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
| La recuperación “mejora significativamente la calidad de las respuestas” (p. 97). | Se sostiene para gpt-5-mini, con un efecto grande. En gpt-5, las pruebas del manuscrito no detectan diferencias y el reanálisis apareado indica una mejora solo con Agentic-RAG (V.1). En gpt-5-nano, el RAG básico no mejora lo obtenido sin recuperación (mediana de 0,583 en ambos casos; Tabla 11, p. 87). Debe formularse como resultado condicional al modelo y a la estrategia. |
| La interacción entre estrategia y modelo como hallazgo principal (p. 114). | El patrón descriptivo es claro, pero su componente principal, la caída de gpt-5-nano con Agentic-RAG, es una falla de salida y no un efecto de la estrategia (V.6). El sustento inferencial debe rehacerse (V.1, V.2) y persiste la confusión de factores (V.5). |
| “Efecto igualador del RAG básico” (p. 114). | No se sostiene. La ausencia de significación no demuestra equivalencia (V.3) y, con pruebas apareadas, los modelos difieren dentro del RAG básico (V.1). |
| “Identificación de la sobrecarga agéntica en modelos pequeños” (p. 114). | No se sostiene. De las 79 salidas, 41 están vacías o son marcadores, y las 38 respuestas sustantivas igualan a las de gpt-5 (V.6). |
| “Validación de LLM-as-a-Judge para evaluación legal” (p. 115). | No se sostiene. Se mostró acuerdo entre jueces, no validez frente a criterio humano. Un juez asignó puntajes altos a tres respuestas vacías (V.7). |
| El objetivo 2 “se cumplió completamente” (p. 113). | Cumplimiento parcial. El agente de verificación fue desactivado y el agente principal realiza una única recuperación (V.5). |
| “Combinación costo-eficiente: Agentic-RAG + gpt-5-mini” (p. 97). | No coincide con las Figuras 22 y 24 (V.10). |
| “Este resultado es transferible a otros dominios y aplicaciones de RAG” (p. 120). | No se sostiene. Un corpus, un banco de 25 casos, una familia de modelos y una ejecución por celda no permiten generalizar. |
| Atención a “usuarios profesionales y no profesionales” (p. 6) y publicación en repositorio abierto (p. 114). | Sin evaluación con usuarios ni interfaz. El repositorio, inaccesible durante la primera revisión, quedó disponible el 11 de noviembre de 2026 y contiene el material necesario para auditar el trabajo (V.11). |

# IX. CORRECCIONES REQUERIDAS Y RECOMENDACIONES

## IX.1 Correcciones requeridas para la versión definitiva

1. Rehacer el análisis inferencial con procedimientos que respeten el apareamiento por unidad y el anidamiento en casos, con tamaños de efecto e intervalos de confianza, y corregir la mención a modelos mixtos, que no fueron estimados (V.1, V.2).

2. Informar las 41 salidas vacías o sin contenido de la celda gpt-5-nano con Agentic-RAG, reincorporar los casos 23 a 25, corregir la explicación de los faltantes y reformular la contribución relativa a la “sobrecarga agéntica” (V.6).

3. Retirar la afirmación de determinismo, informar que el esfuerzo de razonamiento quedó en su valor predeterminado y declarar como limitación la ejecución única (V.4).

4. Declarar la confusión de factores, reproducir todos los prompts y resolver las contradicciones sobre el Agente de Calidad y el límite de búsquedas (V.5).

5. Reformular las conclusiones señaladas en la Tabla 4.

6. Precisar la versión del corpus, resolver las contradicciones sobre su origen y revisar las respuestas de referencia observadas (V.7, V.9).

7. Corregir los errores de la Tabla 2 y de la Tabla 3, con una auditoría completa de las referencias.

8. Ampliar la declaración sobre el uso de herramientas de inteligencia artificial, que hoy se limita a una oración (p. iv), con el alcance que surge del repositorio (V.11).

9. Informar las medidas de recuperación que surgen de los datos ya disponibles (V.8).

## IX.2 Recomendaciones

Las siguientes acciones no condicionan la aprobación, pero mejorarían de manera sustancial el trabajo o una eventual publicación derivada.

1. Comparar el modelo de representaciones con al menos una alternativa entrenada para recuperación y con una línea de base léxica o híbrida.

2. Calcular de manera determinista la precisión y la exhaustividad de las citas de artículos, y contar las citas a artículos inexistentes.

3. Validar una submuestra de calificaciones con uno o dos profesionales del derecho y medir el acuerdo entre personas y jueces automáticos.

4. Ejecutar entre tres y cinco réplicas de las celdas críticas y una ablación con el mismo modelo en ambos agentes.

5. Reducir el capítulo 2 y la sección 7.7 para concentrar el texto en el aporte propio.

# X. DICTAMEN

Por lo expuesto, este miembro del tribunal considera que el trabajo reúne las condiciones para ser defendido oralmente y propone su aceptación para esa instancia. La calificación final quedará sujeta al desempeño del tesista en la defensa, en particular a su capacidad para responder las observaciones sobre el diseño experimental, la celda anómala y el alcance de las conclusiones. La verificación realizada en el repositorio no modifica esta propuesta. Confirma, sin embargo, que las correcciones 1 a 3 alcanzan a los hallazgos centrales del trabajo, por lo que su incorporación a la versión definitiva es indispensable.

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

Spairani, L. U. (2026a). Desarrollo y evaluación de un prototipo de sistema inteligente para consulta de normativa nacional argentina mediante recuperación agéntica [Tesis de maestría, Universidad Austral].

Spairani, L. U. (2026b). tesis-maestria-data-mining (commit c96f82c) [Repositorio de código]. GitHub. https://github.com/LUS24/tesis-maestria-data-mining

Wobbrock, J. O., Findlater, L., Gergle, D., & Higgins, J. J. (2011). The aligned rank transform for nonparametric factorial analyses using only ANOVA procedures. En Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 143-146). Association for Computing Machinery. https://doi.org/10.1145/1978942.1978963

Zheng, L., Guha, N., Anderson, B. R., Henderson, P., & Ho, D. E. (2021). When does pretraining help? Assessing self-supervised learning for law and the CaseHOLD dataset. En Proceedings of the 18th International Conference on Artificial Intelligence and Law. Association for Computing Machinery. https://arxiv.org/abs/2104.08671

# ANEXO. CONTRASTE CON EL REPOSITORIO DE CÓDIGO

La Tabla A1 resume, para cada aspecto, lo que este informe sostenía antes de acceder al repositorio y lo que resultó de contrastarlo con el código, los registros y los datos (Spairani, 2026b). No se volvieron a ejecutar los experimentos. Los cálculos propios son meramente ilustrativos y no sustituyen el reanálisis que corresponde al autor.

Tabla A1

Observaciones formuladas sin acceso al repositorio y resultado de su verificación

| Aspecto | Versión previa al acceso | Resultado de la verificación |
| --- | --- | --- |
| Repositorio (V.11) | La dirección consignada devolvía un error 404. El código y los registros no podían examinarse y el cuarto objetivo no podía darse por cumplido. | Corregido. Accesible desde el 11 de noviembre de 2026. Contiene el código, el banco de preguntas, los registros y las calificaciones. |
| Temperatura (V.4) | Se infería, a partir de la versión declarada de la biblioteca, que el parámetro no llegaba a la API. Se pedía confirmarlo con los registros. | Confirmado. Versión 1.1.0 fijada y 474 registros agénticos con ajustes vacíos. Entre el 59 % y el 91 % de los tokens de salida son de razonamiento. |
| Celda gpt-5-nano con Agentic-RAG (V.6) | Se planteaba como hipótesis que la caída respondía a salidas vacías, abstenciones o errores, y no a una pérdida de calidad. | Confirmado y cuantificado. De 79 salidas, 28 vacías y 13 marcadores. Las 38 respuestas sustantivas promedian 0,82. El autor había detectado las vacías. |
| Observaciones excluidas (V.6) | Se tomaba la explicación del manuscrito, fallos de generación, y se pedía su distribución por celda. | Corregido. Son los casos 23, 24 y 25 en las nueve configuraciones. Tenían respuesta y calificación y no se combinaron por la clave de subpregunta. |
| Modelos mixtos (V.1) | Se señalaba que el anexo los menciona y el cuerpo no los informa. Se pedía incluirlos. | Corregido. No fueron estimados. El cuaderno así denominado solo ejecuta Scheirer-Ray-Hare. |
| Pruebas para muestras independientes (V.1, V.3) | Objeción metodológica. Se advertía que las conclusiones podían cambiar. | Comprobado con los datos. Con pruebas apareadas, los modelos difieren dentro del RAG básico y gpt-5 mejora con Agentic-RAG. |
| Prompts y presupuesto de búsqueda (V.5) | No podía establecerse si las líneas de base contenían la instrucción de abstención. | Establecido. La contienen, con otra redacción. Solo la estrategia agéntica exige salida estructurada. La corrida de gpt-5 admitió siete búsquedas y las demás, seis. |
| Recuperación (V.8) | Se señalaba la ausencia de medidas de recuperación. | Calculadas. Exhaustividad de 0,33 en el RAG básico y de 0,54 a 0,58 en el agéntico. En el 59,5 % de las unidades el RAG básico no recupera ningún artículo de referencia. |
| Jueces automáticos (V.7) | Se objetaba la falta de contraste con criterio humano. | Se mantiene, con un indicio adicional: un juez asignó puntajes altos a tres respuestas vacías. |
| Costos (V.5, V.10) | Se tomaban las cifras del manuscrito. | El total de USD 22,29 coincide con los registros. En gpt-5-nano con Agentic-RAG, USD 3,41 de 3,53 corresponden al agente gpt-5. |

## Footnotes

[^1]: Nuestra valoración inicial se realizó sin acceso al código; con ese acceso, algunos elementos se han modificado. Aun así, sostenemos el formulario oportunamente enviado, pero aquí fundamentamos detalles en relación con él.

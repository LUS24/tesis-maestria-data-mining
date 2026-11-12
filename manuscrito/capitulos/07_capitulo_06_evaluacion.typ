#import "@preview/oxdraw:0.1.0": *
#import "@preview/tablem:0.3.0": three-line-table
#import "../formato.typ": pagina-apaisada

= Evaluación y Resultados <cap:evaluacion>

// Este capítulo presenta los experimentos realizados, las métricas obtenidas
// y el análisis de los resultados del sistema Agentic-RAG.

== Introducción

Este capítulo presenta la evaluación sistemática del sistema Agentic-RAG y los resultados obtenidos. Se describen el diseño experimental, las métricas empleadas, los resultados de cada configuración y el análisis estadístico que fundamenta las conclusiones. El análisis sigue una progresión desde la exploración descriptiva hasta la especificación de un modelo ordinal mixto que respeta el apareamiento y el anidamiento del diseño, el contraste de la interacción estrategia × modelo y el análisis de sensibilidad a escenarios de fallo.

== Diseño Experimental

El diseño experimental sigue un esquema factorial 3 × 3 detallado en el capítulo @cap:metodologia (@tabla-diseno-factorial): tres estrategias de recuperación (sin RAG, RAG básico, Agentic-RAG) × tres modelos de lenguaje (gpt-5-nano, gpt-5-mini, gpt-5), con temperatura 0 en todas las configuraciones para garantizar reproducibilidad.

El benchmark de evaluación —descrito en @cap:metodologia— está compuesto por 25 preguntas (76 subpreguntas explícitas más 3 preguntas evaluadas como unidad única, totalizando 79 unidades de evaluación × 9 configuraciones = 711 observaciones). Las métricas empleadas abarcan tres familias complementarias presentadas en dicho capítulo: solapamiento léxico (Token F1, Jaccard, Levenshtein, BLEU, ROUGE, CER), similitud semántica (SBERT Similarity, BERTScore) y evaluación LLM-as-a-Judge (`score_respuesta_correcta`, `score_precision_legal`) mediante tres jueces independientes (DeepSeek, Grok, Kimi K2).

== Exploración Descriptiva y Selección de Variables de Respuesta

=== Análisis de Correlación entre Métricas

Se calcularon correlaciones de Spearman entre las 13 métricas textuales y las 2 métricas de evaluación por jueces. El análisis reveló cuatro clústeres de métricas:

+ *Clúster de volumen*: `word_count_ratio`, `length_ratio`, `character_error_rate` — métricas ortogonales a la calidad del contenido.
+ *Clúster de embeddings neuronales*: `bertscore`, `sbert_similarity_spanish`, `sbert_similarity_multilingual` — similitud semántica vía modelos de lenguaje.
+ *Clúster léxico/n-gramas*: `token_f1`, `jaccard_similarity`, `levenshtein_similarity`, `bleu`, `rouge_*` — solapamiento a nivel de tokens y n-gramas.
+ *Clúster agéntico*: `respuesta_correcta_avg` (alineada con el clúster semántico) y `precision_legal_avg` (alineada con el clúster léxico).

La @fig-spearman-correlacion presenta la matriz de correlación completa, donde los bloques de alta correlación intra-clúster (rojo) y las líneas divisorias confirman visualmente la estructura de agrupamiento.

#figure(
  image("../media/spearman_correlacion_completa.pdf", width: 100%),
  caption: [Matriz de correlación de Spearman entre las 13 métricas textuales y las 2 métricas de evaluación agéntica. Los bloques de correlación alta (rojo intenso) delimitan los cuatro clústeres: léxico/n-gramas (recuadro superior-izquierdo), embeddings neuronales (recuadro central), volumen (recuadro inferior-derecho) y agéntico (últimas dos filas/columnas). Las líneas punteadas separan los clústeres identificados.],
) <fig-spearman-correlacion>

=== Selección de Variables de Respuesta

Empleando un umbral de |ρ| > 0.85 para identificar redundancias, se identificaron seis candidatas a variables de respuesta (VR) representativas de los clústeres:

+ `token_f1`: representante del clúster léxico.
+ `rouge_l`: representante de métricas de subsecuencia.
+ `sbert_similarity_spanish`: representante del clúster semántico.
+ `bertscore`: similitud contextualizada.
+ `respuesta_correcta_avg`: evaluación global de qué tan correcta es una respuesta de acuerdo al método LLM-as-a-judge.
+ `precision_legal_avg`: evaluación de precisión en citación legal.

El análisis de componentes principales (PCA) con biplot confirmó la estructura de clústeres, ubicando `respuesta_correcta_avg` con correlación moderada con PC1 ($r = +0.488$) y PC2 ($r = +0.429$), y `precision_legal_avg` con correlación predominante con PC1 ($r = +0.545$). La @fig-biplot-pca presenta el biplot con las 13 métricas textuales como variables activas (azul) y las 2 métricas agénticas como variables suplementarias (rojo).

#figure(
  image("../media/biplot_pca_suplementarias.pdf", width: 90%),
  caption: [Biplot del análisis de componentes principales (PCA) sobre las 13 métricas textuales estandarizadas. Las flechas azules representan las métricas activas; las flechas rojas representan las variables agénticas proyectadas como suplementarias. PC1 (61,0%) captura principalmente el contraste entre métricas de similitud (derecha) y métricas de error/volumen (izquierda). PC2 (25,8%) separa las métricas de volumen del resto. `respuesta_correcta_avg` se ubica en una posición intermedia entre los clústeres semántico y léxico, mientras que `precision_legal_avg` se alinea más estrechamente con el clúster léxico. El círculo punteado indica el umbral de correlación $r = 0.6$ con las componentes principales.],
) <fig-biplot-pca>

Para las pruebas de hipótesis subsiguientes se retuvo exclusivamente `respuesta_correcta_avg` como variable de respuesta principal. Esta decisión se fundamenta en tres consideraciones: (1) es la métrica más directamente alineada con el objetivo de evaluar la calidad de las respuestas legales; (2) el análisis de acuerdo inter-juez (@sec:acuerdo-inter-juez) reveló que `precision_legal_avg` no alcanza confiabilidad suficiente; y (3) las métricas textuales y semánticas, aunque informativas, presentan alta redundancia interna y correlación moderada con la evaluación de corrección. Las cinco métricas restantes se emplearon con fines descriptivos y complementarios, en particular en el análisis de costos.

La @fig-boxplots-estrategia presenta la distribución de `respuesta_correcta_avg` agrupada por estrategia de recuperación.

#figure(
  image("../media/boxplots_por_estrategia.pdf", width: 100%),
  caption: [Distribución de las métricas de respuesta por estrategia de recuperación. La figura presenta seis paneles —`respuesta_correcta_avg`, Token F1, ROUGE-L, SBERT Similarity (español), BERTScore y `precision_legal_avg`—; en cada panel las cajas representan el rango intercuartílico (IQR), la línea central indica la mediana y los diamantes rojos señalan la media. En `respuesta_correcta_avg` se observa una tendencia general de mejora desde la configuración sin RAG hacia Agentic-RAG, con mayor variabilidad en esta última debido a la interacción con el modelo; las métricas textuales y semánticas muestran diferencias más atenuadas entre estrategias.],
) <fig-boxplots-estrategia>

=== Imputación de Valores Fuera de Rúbrica

Se detectaron valores de evaluación por jueces fuera del conjunto válido {0.0, 0.25, 0.5, 0.75, 1.0} (11 combinaciones únicas juez-métrica-valor). Se aplicó una estrategia de imputación al valor de rúbrica más cercano, resolviendo empates en favor del valor mayor (sesgo conservador hacia el reconocimiento parcial):

$ r^* = arg min_(r in cal(R)) |x - r| $

donde $cal(R) = {0.0, 0.25, 0.5, 0.75, 1.0}$.

Adicionalmente, un análisis inicial reportó 27 observaciones ausentes en las métricas de evaluación por jueces. La auditoría de las claves de identificación mostró que no se trataba de fallos de generación: las 27 medias ausentes correspondían a las unidades 23, 24 y 25 en las nueve configuraciones, porque en el archivo de métricas la subpregunta figuraba vacía y en el archivo de evaluaciones figuraba como `0`, de modo que la unión de ambas tablas no las encontraba. Las 27 respuestas y sus tres evaluaciones de jueces existen. Al normalizar la clave se recuperaron las 711 observaciones y las 2.133 evaluaciones (711 observaciones × 3 jueces), de manera que la base de análisis contiene 79 unidades por celda y no 76. No se aplicó eliminación por lista ni ninguna otra imputación de observaciones completas; la única transformación es la corrección de los valores fuera de rúbrica descrita arriba.

== Especificación del Análisis Inferencial

=== Unidades Apareadas, Anidamiento y Modelo Ordinal

El diseño no es de grupos independientes. Las 79 unidades de evaluación se responden en las nueve configuraciones, de modo que las observaciones están apareadas por unidad; además, las unidades están anidadas en 25 casos y cada respuesta recibe tres evaluaciones de jueces. Ignorar esas dependencias infla los grados de libertad, deja la dificultad de cada unidad dentro del error y vuelve inválidos los valores p de las pruebas para muestras independientes.

La variable de respuesta principal es el puntaje ordinal de `score_respuesta_correcta` en la escala {0; 0,25; 0,50; 0,75; 1}. El análisis principal es el modelo ordinal mixto de enlaces acumulativos descrito en el capítulo de metodología: `score_respuesta_correcta ~ estrategia * modelo_especialista + juez + (1 | caso) + (1 | unidad)`, estimado con `ordinal::clmm` (Laplace, `nAGQ = 1`). La interacción se contrastó con una prueba de razón de verosimilitud de 4 grados de libertad y los efectos simples se corrigen con Holm dentro de cada una de las dos familias de nueve contrastes.

=== Comparación con el Análisis Exploratorio

La primera versión del análisis se apoyó en pruebas que tratan las observaciones como independientes: Shapiro-Wilk, Kruskal-Wallis con post-hoc de Dunn, análisis estratificado por estrategia y Scheirer-Ray-Hare. Esos resultados se conservan en el @anexo-analisis-exploratorio y no sostienen las conclusiones de este capítulo. La diferencia no es de grado: Kruskal-Wallis, Dunn y Scheirer-Ray-Hare asignan rangos globales a observaciones que pertenecen a la misma unidad y al mismo caso, de modo que sus valores p no tienen la interpretación habitual. En particular, el $p = 0.383$ de Agentic-RAG frente a RAG básico y el $p = 0.095$ de RAG básico no deben leerse como evidencia de equivalencia.

=== Efectos Simples del Modelo Ordinal

Los efectos simples que se reportan a continuación provienen del modelo ordinal mixto, cuya interacción se contrasta en la @sec-interaccion-modelo. Se definieron dos familias de nueve comparaciones —estrategia dentro de cada modelo y modelo dentro de cada estrategia— y el p de Holm se aplicó dentro de cada familia @holm1979simple. Las diferencias de media esperada y de $P("score" >= 0,75)$ se acompañan con IC 95 % obtenidos por simulación de 4.000 extracciones de la distribución asintótica de los coeficientes y umbrales.

La @tabla-efectos-simples presenta los contrastes de estrategia dentro de cada modelo, orientados como Agentic-RAG − RAG básico, Agentic-RAG − Sin RAG y RAG básico − Sin RAG.

#pagina-apaisada[
  #figure(
    three-line-table(
      columns: (auto, auto, auto, auto, auto, auto, auto),
      [
        | *Modelo* | *Contraste* | *Δ media* | *IC 95 %* | *Δ P(≥ 0,75)* | *IC 95 %* | *p de Holm* |
        | :--- | :--- | ---: | :---: | ---: | :---: | ---: |
        | gpt-5-nano | Agentic − RAG | *−0,270* | −0,330 a −0,202 | *−0,308* | −0,382 a −0,225 | 3,25 × 10⁻¹⁴ |
        | gpt-5-nano | Agentic − Sin RAG | *−0,242* | −0,307 a −0,176 | *−0,270* | −0,349 a −0,192 | 1,18 × 10⁻¹¹ |
        | gpt-5-nano | RAG − Sin RAG | 0,028 | −0,032 a 0,085 | 0,037 | −0,043 a 0,114 | 0,724 |
        | gpt-5-mini | Agentic − RAG | *0,150* | 0,096 a 0,203 | *0,210* | 0,134 a 0,283 | 1,72 × 10⁻⁷ |
        | gpt-5-mini | Agentic − Sin RAG | *0,513* | 0,455 a 0,562 | *0,630* | 0,564 a 0,680 | 9,42 × 10⁻⁵⁴ |
        | gpt-5-mini | RAG − Sin RAG | *0,363* | 0,304 a 0,417 | *0,420* | 0,343 a 0,488 | 7,83 × 10⁻²⁹ |
        | gpt-5 | Agentic − RAG | *0,106* | 0,054 a 0,155 | *0,146* | 0,074 a 0,216 | 1,03 × 10⁻⁴ |
        | gpt-5 | Agentic − Sin RAG | *0,095* | 0,046 a 0,146 | *0,130* | 0,063 a 0,202 | 4,82 × 10⁻⁴ |
        | gpt-5 | RAG − Sin RAG | −0,011 | −0,063 a 0,044 | −0,016 | −0,089 a 0,062 | 0,724 |
      ],
    ),
    caption: [Efectos simples de estrategia dentro de cada modelo bajo el escenario principal (respuestas no sustantivas = 0), estimados con el modelo ordinal mixto. `Δ media` y `Δ P(≥ 0,75)` son diferencias de predicciones poblacionales con efectos aleatorios en cero y promedio sobre los tres jueces; los IC 95 % provienen de simulación de la distribución asintótica. El p de Holm corresponde a la familia de nueve contrastes de estrategia. En negrita, los contrastes significativos con Holm.],
  ) <tabla-efectos-simples>
]

La @tabla-efectos-modelo presenta la familia complementaria: modelo dentro de cada estrategia, orientada del modelo de menor a mayor capacidad.

#pagina-apaisada[
  #figure(
    three-line-table(
      columns: (auto, auto, auto, auto, auto, auto, auto),
      [
        | *Estrategia* | *Contraste* | *Δ media* | *IC 95 %* | *Δ P(≥ 0,75)* | *IC 95 %* | *p de Holm* |
        | :--- | :--- | ---: | :---: | ---: | :---: | ---: |
        | Sin RAG | mini − nano | *−0,273* | −0,328 a −0,212 | *−0,295* | −0,366 a −0,223 | 4,36 × 10⁻¹⁷ |
        | Sin RAG | gpt-5 − nano | *0,167* | 0,110 a 0,225 | *0,233* | 0,153 a 0,309 | 1,15 × 10⁻⁷ |
        | Sin RAG | gpt-5 − mini | *0,440* | 0,380 a 0,493 | *0,528* | 0,452 a 0,589 | 2,99 × 10⁻³⁹ |
        | RAG básico | mini − nano | *0,063* | 0,005 a 0,120 | *0,087* | 0,007 a 0,166 | 0,068 |
        | RAG básico | gpt-5 − nano | *0,128* | 0,071 a 0,186 | *0,180* | 0,100 a 0,260 | 4,93 × 10⁻⁵ |
        | RAG básico | gpt-5 − mini | *0,065* | 0,011 a 0,124 | *0,093* | 0,015 a 0,174 | 0,064 |
        | Agentic-RAG | mini − nano | *0,483* | 0,419 a 0,539 | *0,605* | 0,534 a 0,660 | 8,92 × 10⁻⁴³ |
        | Agentic-RAG | gpt-5 − nano | *0,504* | 0,439 a 0,561 | *0,634* | 0,567 a 0,686 | 2,82 × 10⁻⁴⁷ |
        | Agentic-RAG | gpt-5 − mini | 0,021 | −0,023 a 0,066 | 0,029 | −0,031 a 0,089 | 0,349 |
      ],
    ),
    caption: [Efectos simples de modelo dentro de cada estrategia bajo el escenario principal, estimados con el modelo ordinal mixto. Las diferencias están orientadas del primer al segundo modelo indicado (por ejemplo, `mini − nano` = gpt-5-mini menos gpt-5-nano). El p de Holm corresponde a la familia de nueve contrastes de modelo. En negrita, los contrastes significativos con Holm.],
  ) <tabla-efectos-modelo>
]

Los resultados revelan patrones diferenciados por modelo:

+ *gpt-5-mini* es el modelo más sensible a la estrategia: los tres contrastes son significativos con corrección de Holm. Agentic-RAG supera a RAG básico en 0,150 de media (IC 95 % 0,096 a 0,203) y a Sin RAG en 0,513, lo que evidencia una dependencia crítica del contexto externo.
+ *gpt-5-nano* presenta el patrón inverso: Agentic-RAG reduce la media en 0,270 frente a RAG básico (IC 95 % −0,330 a −0,202) y en 0,242 frente a Sin RAG. RAG básico no se distingue de Sin RAG (0,028; IC 95 % −0,032 a 0,085). La magnitud y la dirección del contraste se interpretan como un modo de fallo de respuesta; la atribución causal se discute más adelante.
+ *gpt-5* se beneficia de Agentic-RAG en 0,106 de media (IC 95 % 0,054 a 0,155) frente a RAG básico y en 0,095 frente a Sin RAG; RAG básico no se distingue de Sin RAG (−0,011). El efecto es positivo y significativo, aunque menor que en gpt-5-mini.

En la familia de modelo dentro de estrategia, las tres comparaciones de Sin RAG y de Agentic-RAG son significativas con Holm. En RAG básico, gpt-5 supera a gpt-5-nano, mientras que mini − nano y gpt-5 − mini no sobreviven a la corrección ($p_"Holm"$ = 0,068 y 0,064); esos dos contrastes no permiten afirmar equivalencia, solo ausencia de evidencia suficiente con este tamaño muestral.

Estos resultados refuerzan el hallazgo de interacción: el signo del efecto de Agentic-RAG difiere entre modelos y su magnitud es máxima en los extremos de la escala evaluada.

La @tabla-celdas-principal presenta la descripción y la predicción de la variable de respuesta principal para las nueve configuraciones sobre la base completa de 79 unidades por celda. A diferencia de la versión anterior de esta tabla, todas las celdas tienen $n = 79$; las diferencias respecto de los valores previos se deben a la recuperación de las 27 observaciones descrita antes y no a un cambio de los datos de origen.

#pagina-apaisada[
  #figure(
    three-line-table(
      columns: (1.2fr, 1.1fr, auto, auto, auto, auto, auto, auto),
      [
        | *Estrategia* | *Modelo* | *n* | *No sust.* | *Media* | *Mediana* | *Media modelo* | *P(≥ 0,75)* |
        | :----------- | :------- | --: | --------: | ------: | -------: | -------------: | ----------: |
        | Sin RAG      | gpt-5-nano | 79 | 1 | 0,565 | 0,583 | 0,588 | 0,453 |
        | Sin RAG      | gpt-5-mini | 79 | 15 | 0,325 | 0,250 | 0,315 | 0,157 |
        | Sin RAG      | gpt-5      | 79 | 0 | 0,725 | 0,833 | 0,755 | 0,686 |
        | RAG básico   | gpt-5-nano | 79 | 0 | 0,599 | 0,583 | 0,616 | 0,490 |
        | RAG básico   | gpt-5-mini | 79 | 0 | 0,650 | 0,667 | 0,678 | 0,577 |
        | RAG básico   | gpt-5      | 79 | 0 | 0,707 | 0,833 | 0,744 | 0,670 |
        | Agentic-RAG  | gpt-5-nano | 79 | 41 | 0,395 | 0,000 | 0,346 | 0,182 |
        | Agentic-RAG  | gpt-5-mini | 79 | 1 | *0,788* | *1,000* | *0,828* | *0,787* |
        | Agentic-RAG  | gpt-5      | 79 | 0 | *0,812* | *1,000* | *0,850* | *0,816* |
      ],
    ),
    caption: [Estadísticos descriptivos y predicciones por configuración bajo el escenario principal (respuestas no sustantivas = 0), con 79 unidades por celda. `Media` y `Mediana` describen la puntuación imputada; `Media modelo` y `P(≥ 0,75)` son predicciones poblacionales del modelo ordinal, con efectos aleatorios en cero y promedio sobre los tres jueces. En negrita, los tres valores más altos de cada columna de predicción.],
  ) <tabla-celdas-principal>
]

La @tabla-resumen-medianas conserva, con fines exclusivamente descriptivos, las medianas de las cinco métricas complementarias calculadas sobre la misma base de 79 unidades. Esas métricas no se usaron en las pruebas de hipótesis, que se realizaron exclusivamente sobre `respuesta_correcta_avg`.

#pagina-apaisada[
  #figure(
    three-line-table(
      columns: (1.2fr, 1.2fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      [
        | *Estrategia* | *Modelo*   | *Token F1* | *ROUGE-L* | *SBERT (es)* | *BERTScore* | *Prec. legal* |
        | :----------- | :--------- | :--------: | :-------: | :----------: | :---------: | :-----------: |
        | Sin RAG      | gpt-5-nano |   0,201    |   0,123   |    0,740     |    0,688    |     0,000     |
        | Sin RAG      | gpt-5-mini |   0,176    |   0,123   |    0,629     |    0,674    |     0,000     |
        | Sin RAG      | gpt-5      |   0,243    |   0,141   |    0,760     |    0,694    |     0,333     |
        | RAG básico   | gpt-5-nano |   0,253    |   0,150   |    0,769     |    0,703    |     0,333     |
        | RAG básico   | gpt-5-mini |   0,213    |   0,135   |    0,760     |    0,700    |     0,417     |
        | RAG básico   | gpt-5      |   0,257    |   0,174   |    0,794     |    0,706    |     0,667     |
        | Agentic-RAG  | gpt-5-nano |   0,125    |   0,083   |    0,389     |    0,648    |     0,125     |
        | Agentic-RAG  | gpt-5-mini |   0,215    |   0,130   |   *0,795*    |    0,706    |     0,833     |
        | Agentic-RAG  | gpt-5      |  *0,277*   |  *0,190*  |    0,791     |   *0,708*   |    *0,875*    |
      ],
    ),
    caption: [Medianas de las cinco métricas complementarias por configuración (estrategia × modelo), calculadas sobre 79 unidades por celda. `Prec. legal` corresponde a `precision_legal_avg`, que no alcanzó confiabilidad inter-juez suficiente y se reporta solo con fines descriptivos. El máximo de cada columna se destaca en negrita.],
  ) <tabla-resumen-medianas>
]

== Interacción Estrategia × Modelo <sec-interaccion-modelo>

=== Prueba de Razón de Verosimilitud

La interacción entre estrategia de recuperación y modelo del Agente Especialista Legal se contrastó con una prueba de razón de verosimilitud entre el modelo completo y el modelo sin el término `estrategia:modelo_especialista` (4 grados de libertad). El estadístico fue LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶². El modelo completo reduce el AIC de 5.810,3 a 5.525,0. Las varianzas de los efectos aleatorios son 0,164 para caso y 1,380 para unidad, lo que confirma que una parte sustancial de la variabilidad se explica por la dificultad de las unidades y de los casos.

La interacción se mantiene en los cuatro escenarios definidos en el capítulo de metodología (LR entre 82,52 y 293,28; p < 10⁻¹⁶), aunque la dirección de algunos efectos simples depende del tratamiento de las respuestas no sustantivas. El contraste por juez reproduce la interacción en los tres evaluadores (LR = 82,04 para DeepSeek-V3; 92,66 para Kimi K2 0905; 100,46 para Grok 4.1 Fast).

=== Patrón de Interacción

La @fig-interaccion presenta el gráfico de interacción que visualiza cómo las líneas de los modelos se cruzan entre estrategias, evidenciando la interacción disordinal.

#pagina-apaisada[
  #figure(
    image("../media/interaccion_modelo_estrategia.pdf", width: 96%),
    caption: [Gráficos de interacción modelo × estrategia de recuperación para las seis métricas de respuesta. Las líneas representan la media de cada modelo con intervalos de confianza del 95%; cada panel corresponde a una métrica. El cruce de las líneas en `respuesta_correcta_avg` confirma la interacción disordinal: el modelo óptimo depende de la estrategia empleada.],
  ) <fig-interaccion>
]

El análisis de las medias por combinación —cuyas estimaciones modeladas figuran en la @tabla-celdas-principal— revela un patrón de interacción disordinal, con líneas que se cruzan.

Las principales observaciones son:

+ *gpt-5 es robusto*: mantiene un desempeño alto (0.70–0.80) en todas las condiciones, compensando parcialmente la ausencia de contexto mediante su capacidad de razonamiento interna.
+ *gpt-5-mini es sensible al RAG*: con Agentic-RAG alcanza 0.78 (comparable a gpt-5), pero sin RAG cae a 0.35, evidenciando una dependencia crítica del contexto externo.
+ *gpt-5-nano muestra un comportamiento contraintuitivo*: su desempeño es *peor* con Agentic-RAG (0.40) que con RAG básico (0.59), lo que sugiere que el sistema agéntico genera instrucciones y contextos de complejidad excesiva para un modelo de capacidad reducida.

=== Lectura del Patrón

+ La ausencia de diferencia marginal entre Agentic-RAG y RAG básico enmascara diferencias condicionales al modelo: en gpt-5-mini la diferencia es positiva y sustancial, mientras que en gpt-5-nano se invierte.
+ Con RAG básico las diferencias entre modelos son menores, pero no se demostró equivalencia; el sistema agéntico no las elimina.
+ El cruce de las líneas es disordinal, de modo que no existe un orden único de las estrategias ni de los modelos: la comparación debe hacerse célula por célula y con intervalos, no a partir del efecto marginal.

== Sensibilidad No Paramétrica Pareada

El modelo ordinal mixto descrito en el capítulo de metodología es el análisis principal. Para verificar que la interacción y la dirección de los efectos no dependen de la especificación paramétrica ni del tratamiento de los efectos aleatorios, se repitió el análisis con pruebas pareadas que usan la unidad de evaluación como bloque: Friedman para el efecto global de cada factor dentro del nivel del otro y Wilcoxon de rangos con signo para los pares, con corrección de Holm dentro de cada familia de nueve contrastes. Los intervalos de confianza provienen de un bootstrap por casos (25 casos remuestreados con todas sus unidades, 5.000 réplicas), no de un remuestreo de filas.

La @tabla-friedman-sensibilidad presenta los resultados globales de Friedman. Los seis bloques rechazan la hipótesis de igualdad de distribuciones, incluido RAG básico, donde el test de Kruskal-Wallis para muestras independientes no había alcanzado significación.

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto, auto, auto),
    [
      | *Familia* | *Bloque* | *χ²* | *gl* | *p* | *W de Kendall* |
      | :--- | :--- | ---: | :---: | ---: | ---: |
      | Estrategia dentro del modelo | gpt-5-nano | 12,05 | 2 | 0,0024 | 0,076 |
      | Estrategia dentro del modelo | gpt-5-mini | 54,81 | 2 | < 0,0001 | 0,347 |
      | Estrategia dentro del modelo | gpt-5 | 12,88 | 2 | 0,0016 | 0,082 |
      | Modelo dentro de la estrategia | Sin RAG | 61,24 | 2 | < 0,0001 | 0,388 |
      | Modelo dentro de la estrategia | RAG básico | 23,43 | 2 | 8,2 × 10⁻⁶ | 0,148 |
      | Modelo dentro de la estrategia | Agentic-RAG | 61,19 | 2 | < 0,0001 | 0,387 |
    ],
  ),
  caption: [Pruebas de Friedman por bloque, escenario principal (respuestas no sustantivas = 0). `W de Kendall` es el tamaño de efecto global del bloque; los seis contrastes usan 79 unidades como bloques.],
) <tabla-friedman-sensibilidad>

La @tabla-wilcoxon-sensibilidad presenta los contrastes pareados de estrategia orientados como Agentic-RAG − RAG básico, Agentic-RAG − Sin RAG y RAG básico − Sin RAG.

#pagina-apaisada[
  #figure(
    three-line-table(
      columns: (auto, auto, auto, auto, auto, auto),
      [
        | *Modelo* | *Contraste* | *Δ media* | *IC 95 % (bootstrap por casos)* | *p de Wilcoxon* | *p de Holm* |
        | :--- | :--- | ---: | :---: | ---: | ---: |
        | gpt-5-nano | Agentic − RAG | −0,205 | −0,333 a −0,073 | 0,0008 | 0,0048 |
        | gpt-5-nano | Agentic − Sin RAG | −0,171 | −0,300 a −0,031 | 0,0021 | 0,0106 |
        | gpt-5-nano | RAG − Sin RAG | 0,034 | −0,075 a 0,160 | 0,9895 | 1,000 |
        | gpt-5-mini | Agentic − RAG | 0,138 | 0,081 a 0,201 | 0,0001 | 0,0008 |
        | gpt-5-mini | Agentic − Sin RAG | 0,463 | 0,368 a 0,560 | < 0,0001 | < 0,0001 |
        | gpt-5-mini | RAG − Sin RAG | 0,325 | 0,227 a 0,431 | < 0,0001 | < 0,0001 |
        | gpt-5 | Agentic − RAG | 0,106 | 0,046 a 0,160 | 0,0029 | 0,0116 |
        | gpt-5 | Agentic − Sin RAG | 0,088 | 0,025 a 0,160 | 0,0102 | 0,0306 |
        | gpt-5 | RAG − Sin RAG | −0,018 | −0,100 a 0,077 | 0,7267 | 1,000 |
      ],
    ),
    caption: [Contrastes pareados de Wilcoxon con corrección de Holm dentro de la familia de nueve comparaciones; escenario principal (respuestas no sustantivas = 0). `Δ media` es la diferencia de medias de la puntuación imputada, orientada según el contraste indicado. Los intervalos provienen de un bootstrap por casos (25 casos, 5.000 réplicas).],
  ) <tabla-wilcoxon-sensibilidad>
]

Los nueve signos coinciden con los del modelo ordinal y con los de la @tabla-efectos-simples; las magnitudes difieren porque Wilcoxon no modela el anidamiento ni la severidad del juez. La lectura sustantiva es la misma: Agentic-RAG reduce la utilidad del sistema en gpt-5-nano y la aumenta en gpt-5-mini y en gpt-5. La diferencia de RAG básico frente a Sin RAG no se distingue de cero en gpt-5-nano ni en gpt-5, y es positiva y significativa en gpt-5-mini. En RAG básico, las diferencias entre modelos siguen siendo significativas salvo gpt-5 − gpt-5-mini, que no sobrevive a la corrección de Holm ($p_"Holm" = 0,077$); un p no significativo no demuestra equivalencia.

== Sensibilidad al Tratamiento de Respuestas No Sustantivas

Los cuatro escenarios definidos en el capítulo de metodología se estimaron con el mismo modelo ordinal. La @tabla-sensibilidad-escenarios presenta la diferencia modelada Agentic-RAG − RAG básico por modelo en cada escenario.

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto),
    [
      | *Escenario* | *gpt-5-nano* | *gpt-5-mini* | *gpt-5* |
      | :--- | ---: | ---: | ---: |
      | Principal (fallo = 0) | *−0,270* | *0,150* | *0,106* |
      | Puntajes observados | *−0,243* | *0,150* | *0,106* |
      | Solo fallos técnicos = 0 | *−0,270* | *0,150* | *0,106* |
      | Exclusión de no sustantivas | *0,216* | *0,160* | *0,111* |
    ],
  ),
  caption: [Diferencia de media esperada Agentic-RAG − RAG básico por modelo y escenario, estimada con el modelo ordinal mixto. En negrita, los contrastes cuyo signo se mantiene en los cuatro escenarios; el único cambio de signo corresponde a gpt-5-nano bajo exclusión, donde la estimación condiciona a que el sistema responda.],
) <tabla-sensibilidad-escenarios>

La celda Agentic-RAG + gpt-5-nano concentra 41 de las 79 respuestas no sustantivas, de modo que es la única cuyo resultado depende del escenario. Bajo el escenario principal su media es 0,395 y su mediana 0,000; bajo exclusión la media asciende a 0,820 y la mediana a 0,958, pero sobre 38 unidades. Bajo puntajes observados la media es 0,415 y la mediana 0,250; bajo solo fallos técnicos = 0 los valores coinciden con el escenario principal, porque las abstenciones y los mensajes indeterminados de esa celda no recibieron puntajes positivos de los jueces.

No se trata de estimaciones contradictorias. La primera mide la utilidad del sistema completo, la segunda la calidad condicional a que el sistema responda y la tercera la forma en que los jueces califican salidas que no contienen respuesta. El manuscrito reporta las tres y no elige una sola como “el efecto” de Agentic-RAG. En gpt-5-mini y en gpt-5 la diferencia es positiva en los cuatro escenarios, con variación de centésimas.

== Análisis de Costos

=== Costos Descriptivos por Modelo y Sistema

Se calculó el costo total de cada consulta sumando el costo de generación de la respuesta y el costo de recuperación (cuando aplica). Los costos se analizaron por modelo, por sistema y por combinación modelo × sistema. La @fig-costos-configuracion presenta el costo medio por configuración.

#figure(
  image("../media/costos_por_configuracion.pdf", width: 100%),
  caption: [Costo medio por consulta (USD) para cada combinación modelo × estrategia de recuperación. El costo del sistema Agentic-RAG incluye las llamadas al Agente de Recuperación, que emplea gpt-5 independientemente del modelo del Agente Especialista Legal.],
) <fig-costos-configuracion>

=== Relación Costo-Desempeño

Para cada combinación se graficó el costo medio versus el desempeño medio en `respuesta_correcta_avg` y, complementariamente, en las cinco métricas textuales y semánticas (@fig-costo-desempenio). Este análisis permite identificar las configuraciones con mejor balance de eficiencia.

#pagina-apaisada[
  #figure(
    image("../media/costo_desempenio.pdf", width: 100%),
    caption: [Relación costo-desempeño para `respuesta_correcta_avg` y las cinco métricas complementarias. Cada punto representa una combinación modelo × estrategia; el color indica la estrategia y la forma, el modelo. El cuadrante superior-izquierdo (alto desempeño, bajo costo) contiene las configuraciones más eficientes.],
  ) <fig-costo-desempenio>
]

=== Índice de Eficiencia

Se definió un índice de eficiencia como el cociente entre el desempeño y el costo normalizado (normalización min-max):

$ "Eficiencia" = frac("Desempeño", "Costo normalizado") $

donde el costo normalizado se calcula como:

$ c_"norm" = max(frac(c - c_min, c_max - c_min), 0.01) $

El piso de 0.01 evita la división por cero para la configuración de menor costo. Este índice permite comparar qué combinaciones ofrecen mayor desempeño por unidad de costo.

La @fig-eficiencia presenta el índice de eficiencia para las nueve configuraciones, ordenadas de menor a mayor.

#figure(
  image("../media/eficiencia_costo.pdf", width: 100%),
  caption: [Índice de eficiencia (desempeño / costo normalizado) para la métrica `respuesta_correcta_avg`. Las barras se colorean según el modelo y se texturizan según la estrategia. Las configuraciones más eficientes combinan alto desempeño con bajo costo relativo.],
) <fig-eficiencia>

=== Resumen de Tokens y Costos del Experimento

Se reportaron los tokens totales consumidos y el costo acumulado por modelo y por estrategia. El costo total del experimento fue de USD 22.29, distribuido en Agentic-RAG (USD 14.24), RAG básico (USD 3.75) y sin RAG (USD 4.31). El mayor costo de Agentic-RAG refleja las llamadas adicionales al Agente de Recuperación, que emplea gpt-5 independientemente del modelo del Agente Especialista Legal.

=== Métricas de recuperación

Se calcularon métricas de recuperación desde los registros de búsqueda y desde el baseline de `part_d`; el detalle y la reproducción están en `verificacion-analisis-estadistico/metricas_recuperacion/`. La comparación usa `recall en top-10` (proporción media de artículos de referencia recuperados en el top-10), el rango recíproco medio (MRR) y la proporción de unidades con todos o ningún artículo de referencia en el top-10.

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto, auto),
    [
      | *Sistema* | *recall en top-10* | *MRR* | *unidades con todos en top-10* | *unidades sin ninguno en top-10* |
      | :--- | ---: | ---: | ---: | ---: |
      | RAG básico (baseline `part_d`) | 0,333 | 0,214 | 27,9 % | 59,5 % |
      | Agentic-RAG, especialista gpt-5 | 0,415 | 0,242 | 32,9 % | 45,6 % |
      | Agentic-RAG, especialista gpt-5-mini | 0,399 | 0,263 | 32,9 % | 50,6 % |
      | Agentic-RAG, especialista gpt-5-nano | 0,446 | 0,281 | 35,4 % | 44,3 % |
    ],
  ),
  caption: [Métricas de recuperación del baseline y de Agentic-RAG. El baseline usa una consulta; Agentic-RAG usa varias y el número de documentos únicos difiere. La comparación es descriptiva, no un experimento controlado de recuperadores.],
) <tabla-metricas-recuperacion>

Agentic-RAG mejora el recall en top-10 y el MRR respecto del baseline, pero la comparación no es causal: el baseline emplea una consulta y el sistema agéntico varias, y el presupuesto de recuperación no está igualado. No se comparó con BM25 ni con otro embedding porque el volumen de Milvus se perdió y no se recreó la base. El baseline de `part_d` reproduce los valores previos del manuscrito (recall en top-10 = 0,333; MRR = 0,214; 27,9 % con todos; 59,5 % sin ninguno).

== Evaluación LLM-as-a-Judge

=== Modelos de Juez

Se emplearon tres modelos como jueces independientes, cuyas características y configuración se detallan en el capítulo @cap:metodologia: DeepSeek-V3, Grok 4.1 Fast y Kimi K2 0905. Cada juez evaluó las 9 configuraciones usando las dos rúbricas definidas en dicho capítulo (`score_respuesta_correcta`, @tabla-rubrica-correcta; `score_precision_legal`, @tabla-rubrica-legal).

=== Resultados de "respuesta_correcta"

Los scores de `respuesta_correcta` muestran una distribución concentrada en los valores {0.5, 0.75, 1.0} para los sistemas con RAG, mientras que el sistema sin RAG presenta mayor dispersión hacia valores bajos, consistente con la menor calidad de las respuestas sin contexto externo.

=== Resultados de Precisión Legal

Los scores de `precision_legal` presentan mayor variabilidad entre jueces que los de corrección, reflejando la mayor subjetividad inherente en evaluar la precisión de citación legal.

La @fig-heatmap-jueces presenta la distribución de los puntajes asignados por cada juez para ambas rúbricas.

#figure(
  image("../media/heatmap_jueces.pdf", width: 100%),
  caption: [Distribución proporcional de puntajes por juez y rúbrica. Cada celda indica la proporción de evaluaciones que recibieron cada puntaje. Se observan diferencias en los patrones de distribución: algunos jueces tienden a concentrar sus evaluaciones en valores centrales (0,50–0,75), mientras que otros exhiben distribuciones más polarizadas.],
) <fig-heatmap-jueces>

== Acuerdo Inter-Juez <sec:acuerdo-inter-juez>

El análisis de acuerdo inter-juez evalúa la confiabilidad de las evaluaciones LLM-as-a-Judge.

=== Correlación de Spearman entre Jueces

Las correlaciones de Spearman entre pares de jueces resultaron altas y significativas:

+ Para `score_respuesta_correcta`: $rho = 0.79 – 0.84$ entre todos los pares.
+ Para `score_precision_legal`: $rho = 0.77 – 0.82$ entre todos los pares.

Esto indica un ordenamiento relativo consistente de las respuestas entre los tres jueces.

=== Alpha de Krippendorff

El Alpha de Krippendorff ($alpha$) es un coeficiente de acuerdo inter-anotadores que corrige el acuerdo esperado por azar, soporta múltiples anotadores y datos faltantes, y admite escala ordinal @krippendorff2019content. Los umbrales de interpretación según Krippendorff (2019) son: $alpha >= 0.800$ (bueno), $0.667 <= alpha < 0.800$ (aceptable), $alpha < 0.667$ (insuficiente).

Los resultados globales fueron:

#figure(
  three-line-table(
    columns: (auto, auto, auto),
    [
      | *Rúbrica*                  | *α ordinal* | *Interpretación* |
      | :------------------------- | :---------: | :--------------: |
      | `score_respuesta_correcta` |   *0.8078*    |      Bueno       |
      | `score_precision_legal`    |   0.7846    |    Aceptable     |
    ],
  ),
  caption: [Alpha de Krippendorff global por rúbrica. En negrita, el coeficiente de mayor valor.],
)

==== Alpha por Sistema de Recuperación

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto),
    [
      | *Rúbrica*                  | *agentic_rag* | *base_rag* | *no_rag* |
      | :------------------------- | :-----------: | :--------: | :------: |
      | `score_respuesta_correcta` |    *0.8693*     |   0.8219   |  0.6979  |
      | `score_precision_legal`    |    *0.7550*     |   0.6389   |  0.6211  |
    ],
  ),
  caption: [Alpha de Krippendorff ordinal por sistema de recuperación. En negrita, el coeficiente de mayor valor de cada sistema.],
)

La @fig-krippendorff-alpha visualiza estos resultados, permitiendo comparar de un vistazo la consistencia entre sistemas y rúbricas con respecto al umbral de aceptabilidad.

#figure(
  image("../media/krippendorff_alpha_por_sistema.pdf", width: 100%),
  caption: [Acuerdo inter-juez (Alpha de Krippendorff) por sistema de recuperación y rúbrica. Las líneas punteadas indican los umbrales de acuerdo aceptable ($alpha = 0.667$) y bueno ($alpha = 0.8$). Se observa que `score_respuesta_correcta` supera el umbral aceptable en todos los sistemas, mientras que `score_precision_legal` cae por debajo en _base_rag_ y _no_rag_.],
) <fig-krippendorff-alpha>

Para `score_respuesta_correcta`, el acuerdo es bueno o cercano al umbral en los tres sistemas. Para `score_precision_legal`, dos de los tres sistemas caen por debajo del umbral aceptable ($alpha < 0.667$), lo que indica que los jueces no miden de forma consistente la precisión legal en esas condiciones.

=== Test Chi-Cuadrado de Homogeneidad

Se aplicó el test chi-cuadrado de homogeneidad sobre la tabla de contingencia jueces × valores de score para evaluar si los jueces distribuyen los scores de la misma manera. El test rechazó la hipótesis nula para ambas rúbricas ($p < 0.001$), confirmando diferencias en los patrones de distribución de scores entre jueces.

No obstante, este resultado es complementario al $alpha$ de Krippendorff: el chi-cuadrado detecta diferencias estadísticamente significativas (sensible al tamaño muestral), mientras que el $alpha$ cuantifica la magnitud del acuerdo y es el estadístico de decisión sobre la confiabilidad.

=== Decisión sobre `score_precision_legal`

Basándose en los resultados del acuerdo inter-juez, se decidió emplear exclusivamente `score_respuesta_correcta` para las comparaciones entre sistemas. Las razones principales son:

+ $alpha$ ordinal de `score_precision_legal` cae por debajo de 0.667 en base_rag y no_rag.
+ Su coeficiente de variación inter-juez (95–105%) duplica al de `score_respuesta_correcta` (58–62%).
+ La ambigüedad conceptual inherente a la "precisión legal" no es resoluble sin una reformulación de la rúbrica con anclas específicas del dominio.
+ `score_respuesta_correcta` es suficiente para el objetivo de comparar estrategias, con $alpha >= 0.82$ en los sistemas RAG.

=== Análisis de Sesgo Sistemático

Se analizó el sesgo de cada juez mediante la media, mediana, desviación estándar y coeficiente de variación de sus scores. Se identificaron patrones de lenidad/severidad leves pero consistentes. El sesgo se analizó también de forma estratificada por sistema de recuperación, confirmando que las diferencias entre jueces son uniformes a través de los sistemas (sesgo no diferencial).

== Discusión de Resultados

=== Fortalezas del Sistema

+ La recuperación no produce una mejora uniforme: el efecto depende del modelo. En gpt-5-mini, RAG básico y Agentic-RAG superan a Sin RAG; en gpt-5, Agentic-RAG supera a ambas referencias; en gpt-5-nano, Agentic-RAG presenta un modo de fallo de respuesta.
+ Agentic-RAG + gpt-5-mini presenta una media de 0,788 y un costo de USD 0,0564 por consulta; es una alternativa no dominada frente a Agentic-RAG + gpt-5 (0,812; USD 0,0792), no una equivalencia demostrada.
+ Con RAG básico las diferencias entre modelos son menores, pero no desaparecen; no se demostró equivalencia.
+ El acuerdo inter-juez para `score_respuesta_correcta` es bueno ($alpha = 0.81$); mide confiabilidad, no validez frente a criterio humano.

=== Debilidades y Limitaciones

+ En Agentic-RAG con gpt-5-nano, 41/79 salidas no fueron sustantivas (27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas); la media con fallo = 0 fue 0,395 y la mediana 0,000. Cuando respondió (38/79), la media fue 0,820 y la mediana 0,958. El patrón se describe como un modo de fallo de respuesta, no como una degradación uniforme ni como efecto causal de la “complejidad agéntica”.
+ La métrica `score_precision_legal` no alcanza confiabilidad inter-juez suficiente para ser empleada en comparaciones, lo que limita la evaluación de la precisión de citación.
+ No se demostró una superioridad global de Agentic-RAG: el efecto es negativo en gpt-5-nano, positivo en gpt-5-mini y moderado en gpt-5. No corresponde reportar un efecto marginal único ni usar la falta de significación como prueba de equivalencia.
+ El benchmark se limita al Código de Minería Argentino, por lo que la generalización a otros cuerpos normativos requiere validación adicional.

La comparación pareada cambia la lectura de los resultados originales: Agentic-RAG no es equivalente a las otras estrategias en gpt-5, sino que presenta diferencias positivas moderadas. La interpretación debe basarse en las estimaciones e intervalos del modelo ordinal, no en la falta de significación de pruebas para muestras independientes.

=== Implicaciones Prácticas

+ *Mayor calidad media*: Agentic-RAG + gpt-5 (media 0,812), con costo superior.
+ *Alternativa no dominada*: Agentic-RAG + gpt-5-mini (media 0,788; USD 0,0564 por consulta) es una opción de calidad alta, no la más barata. El menor costo puntual por respuesta correcta corresponde a RAG básico + gpt-5-nano (USD 0,0061; 33/79), con IC solapado con Sin RAG + nano.
+ *No existe una recomendación universal*: la interacción significativa entre factores implica que la selección de modelo y estrategia debe hacerse conjuntamente, no de forma independiente.
+ *Advertencia*: Agentic-RAG + gpt-5-nano presentó 41/79 salidas no sustantivas y el peor costo por respuesta correcta; no se recomienda sin réplicas ni ablaciones.

== Conclusiones del Capítulo

Los resultados muestran una interacción entre la estrategia de recuperación y el modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). En el escenario principal, Agentic-RAG fue inferior a RAG básico en gpt-5-nano (−0,270; IC 95% −0,330 a −0,202), superior en gpt-5-mini (+0,150; IC 95% 0,096 a 0,203) y superior en gpt-5 (+0,106; IC 95% 0,054 a 0,155). RAG básico no eliminó las diferencias entre modelos: las estimaciones fueron positivas y los intervalos no definen equivalencia. En Agentic-RAG con gpt-5-nano, 41 de 79 salidas no fueron sustantivas; cuando respondió, la calidad fue alta (38/79; media 0,820; mediana 0,958). El alpha de Krippendorff (0,807842 original; 0,799542 rúbrica) mide confiabilidad entre jueces, no validez frente a criterio humano. Las pruebas para muestras independientes del análisis original se conservan solo como antecedente exploratorio.

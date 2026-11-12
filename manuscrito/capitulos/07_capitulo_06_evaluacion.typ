#import "@preview/oxdraw:0.1.0": *
#import "@preview/tablem:0.3.0": three-line-table
#import "../formato.typ": pagina-apaisada

= Evaluación y Resultados <cap:evaluacion>

// Este capítulo presenta los experimentos realizados, las métricas obtenidas
// y el análisis de los resultados del sistema Agentic-RAG.

== Introducción

Este capítulo presenta la evaluación sistemática del sistema Agentic-RAG y los resultados obtenidos. Se describen el diseño experimental, las métricas empleadas, los resultados de cada configuración y el análisis estadístico que fundamenta las conclusiones. El análisis sigue una progresión desde la exploración descriptiva hasta la especificación de un modelo ordinal mixto que respeta el apareamiento y el anidamiento del diseño, el contraste de la interacción estrategia × modelo y el análisis de sensibilidad a escenarios de fallo.

== Diseño Experimental

El diseño experimental sigue un esquema factorial 3 × 3 detallado en el #ref(<cap:metodologia>, supplement: [Capítulo]) (@tabla-diseno-factorial): tres estrategias de recuperación (sin RAG, RAG básico, Agentic-RAG) × tres modelos de lenguaje (gpt-5-nano, gpt-5-mini, gpt-5), con una única ejecución por unidad y configuración. El código solicitó `temperature=0.0`, pero el perfil de Pydantic AI para los modelos GPT-5 no admite ese parámetro y la biblioteca lo elimina antes de la solicitud; por tanto, la configuración no garantiza determinismo ni reproducibilidad exacta.

El benchmark de evaluación —descrito en el #ref(<cap:metodologia>, supplement: [Capítulo])— está compuesto por 25 preguntas (76 subpreguntas explícitas más 3 preguntas evaluadas como unidad única, totalizando 79 unidades de evaluación × 9 configuraciones = 711 observaciones). Las métricas empleadas abarcan tres familias complementarias presentadas en dicho capítulo: solapamiento léxico (Token F1, Jaccard, Levenshtein, BLEU, ROUGE, CER), similitud semántica (SBERT Similarity, BERTScore) y evaluación LLM-as-a-Judge (`score_respuesta_correcta`, `score_precision_legal`) mediante tres jueces independientes (DeepSeek, Grok, Kimi K2).

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

Se detectaron valores de evaluación por jueces fuera del conjunto válido {0.0, 0.25, 0.5, 0.75, 1.0}: 50 evaluaciones sobre las 2.133, distribuidas en 11 combinaciones únicas de juez, métrica y valor. La imputación alcanzó 37 evaluaciones de corrección y 13 de precisión legal; por juez, 47 corresponden a DeepSeek-V3, 2 a Kimi K2 0905 y 1 a Grok 4.1 Fast. Se aplicó una estrategia de imputación al valor de rúbrica más cercano, resolviendo empates en favor del valor mayor (sesgo conservador hacia el reconocimiento parcial):

$ r^* = arg min_(r in cal(R)) |x - r| $

donde $cal(R) = {0.0, 0.25, 0.5, 0.75, 1.0}$.

Adicionalmente, un análisis inicial reportó 27 observaciones ausentes en las métricas de evaluación por jueces. La auditoría de las claves de identificación mostró que no se trataba de fallos de generación: las 27 medias ausentes correspondían a las unidades 23, 24 y 25 en las nueve configuraciones, porque en el archivo de métricas la subpregunta figuraba vacía y en el archivo de evaluaciones figuraba como `0`, de modo que la unión de ambas tablas no las encontraba. Las 27 respuestas y sus tres evaluaciones de jueces existen. Al normalizar la clave se recuperaron las 711 observaciones y las 2.133 evaluaciones (711 observaciones × 3 jueces), de manera que la base de análisis contiene 79 unidades por celda y no 76. No se aplicó eliminación por lista ni ninguna otra imputación de observaciones completas; la única transformación es la corrección de los valores fuera de rúbrica descrita arriba.

== Especificación del Análisis Inferencial

=== Unidades Apareadas, Anidamiento y Modelo Ordinal

El diseño no es de grupos independientes. Las 79 unidades de evaluación se responden en las nueve configuraciones, de modo que las observaciones están apareadas por unidad; además, las unidades están anidadas en 25 casos y cada respuesta recibe tres evaluaciones de jueces. Ignorar esas dependencias infla los grados de libertad, deja la dificultad de cada unidad dentro del error y vuelve inválidos los valores p de las pruebas para muestras independientes.

La variable de respuesta principal es el puntaje ordinal de `score_respuesta_correcta` en la escala {0; 0,25; 0,50; 0,75; 1}. El análisis principal es el modelo ordinal mixto de enlaces acumulativos descrito en el capítulo de metodología: `score_respuesta_correcta ~ estrategia * modelo_especialista + juez + (1 | caso) + (1 | unidad)`, estimado con `ordinal::clmm` (Laplace, `nAGQ = 1`). La interacción se contrastó con una prueba de razón de verosimilitud de 4 grados de libertad y los efectos simples se corrigen con Holm dentro de cada una de las dos familias de nueve contrastes.

=== Comparación con el Análisis Exploratorio

La primera versión del análisis se apoyó en pruebas que tratan las observaciones como independientes: Shapiro-Wilk, Kruskal-Wallis con post-hoc de Dunn, análisis estratificado por estrategia y Scheirer-Ray-Hare. Esos resultados se conservan en el #ref(<anexo-analisis-exploratorio>, supplement: [Anexo]) y no sostienen las conclusiones de este capítulo. La diferencia no es de grado: Kruskal-Wallis, Dunn y Scheirer-Ray-Hare asignan rangos globales a observaciones que pertenecen a la misma unidad y al mismo caso, de modo que sus valores p no tienen la interpretación habitual. En particular, el $p = 0.383$ de Agentic-RAG frente a RAG básico y el $p = 0.095$ de RAG básico no deben leerse como evidencia de equivalencia.

=== Efectos Simples del Modelo Ordinal

Los efectos simples que se reportan a continuación provienen del modelo ordinal mixto, cuya interacción se contrasta en la @sec-interaccion-modelo. Se definieron dos familias de nueve comparaciones —estrategia dentro de cada modelo y modelo dentro de cada estrategia— y el p de Holm se aplicó dentro de cada familia @holm1979simple. Las diferencias de media esperada y de $P("score" >= 0,75)$ se acompañan con IC 95 % obtenidos por simulación de 4.000 extracciones de la distribución asintótica de los coeficientes y umbrales.

La @tabla-efectos-simples presenta los contrastes de estrategia dentro de cada modelo y la @tabla-efectos-modelo, la familia complementaria de modelo dentro de cada estrategia, orientada del modelo de menor a mayor capacidad.

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

#v(1.2em)


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

#pagina-apaisada[
  La @tabla-celdas-principal presenta la descripción y la predicción de la variable de respuesta principal para las nueve configuraciones sobre la base completa de 79 unidades por celda. A diferencia de la versión anterior de esta tabla, todas las celdas tienen $n = 79$; las diferencias respecto de los valores previos se deben a la recuperación de las 27 observaciones descrita antes y no a un cambio de los datos de origen.

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


  #v(1.2em)

  La @tabla-resumen-medianas conserva, con fines exclusivamente descriptivos, las medianas de las cinco métricas complementarias calculadas sobre la misma base de 79 unidades. Esas métricas no se usaron en las pruebas de hipótesis, que se realizaron exclusivamente sobre `respuesta_correcta_avg`.

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
    caption: [Medianas de las cinco métricas complementarias por configuración (estrategia × modelo), calculadas sobre 79 unidades por celda. `Prec. legal` corresponde a la métrica de precisión legal, que no alcanzó confiabilidad inter-juez suficiente y se reporta solo con fines descriptivos. El máximo de cada columna se destaca en negrita.],
  ) <tabla-resumen-medianas>

]

#pagina-apaisada[
  La @fig-analisis-celdas presenta la media de corrección por configuración bajo el escenario principal, con intervalo de confianza del 95 %, sobre la misma base de 79 unidades por celda.

  #figure(
    image("../media/analisis_celdas_principal.pdf", width: 96%),
    caption: [Media de `respuesta_correcta_avg` por configuración bajo el escenario principal, con intervalo de confianza del 95 %. La línea punteada marca el umbral de 0,75 usado para definir una respuesta correcta.],
  ) <fig-analisis-celdas>
]

#pagina-apaisada[
  La @fig-analisis-efectos presenta las dos familias de contrastes como gráfico de bosque, ordenadas por familia y por magnitud del efecto.

  #figure(
    image("../media/analisis_efectos_simples.pdf", width: 96%),
    caption: [Efectos simples del modelo ordinal bajo el escenario principal. Panel izquierdo: estrategia dentro de cada modelo; panel derecho: modelo dentro de cada estrategia. Los puntos son diferencias de media esperada y las barras, intervalos de confianza del 95 % obtenidos por simulación de la distribución asintótica. La línea vertical en cero marca la ausencia de diferencia.],
  ) <fig-analisis-efectos>

]

== Interacción Estrategia × Modelo <sec-interaccion-modelo>

=== Prueba de Razón de Verosimilitud

La interacción entre estrategia de recuperación y modelo del Agente Especialista Legal se contrastó con una prueba de razón de verosimilitud entre el modelo completo y el modelo sin el término `estrategia:modelo_especialista` (4 grados de libertad). El estadístico fue LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶². El modelo completo reduce el AIC de 5.810,3 a 5.525,0. Las varianzas de los efectos aleatorios son 0,164 para caso y 1,380 para unidad, lo que confirma que una parte sustancial de la variabilidad se explica por la dificultad de las unidades y de los casos.

La interacción se mantiene en los cuatro escenarios definidos en el capítulo de metodología (LR entre 82,52 y 293,28; p < 10⁻¹⁶), aunque la dirección de algunos efectos simples depende del tratamiento de las respuestas no sustantivas. El contraste por juez reproduce la interacción en los tres evaluadores (LR = 82,04 para DeepSeek-V3; 92,66 para Kimi K2 0905; 100,46 para Grok 4.1 Fast).

=== Patrón de Interacción

La @fig-interaccion presenta la predicción del modelo ordinal para la probabilidad de obtener un puntaje de corrección de al menos 0,75 en cada combinación, con bandas de confianza del 95 %.

#figure(
  image("../media/analisis_interaccion_prob.pdf", width: 88%),
  caption: [Interacción estrategia × modelo bajo el escenario principal: probabilidad predicha de obtener un puntaje de corrección de al menos 0,75, con bandas de confianza del 95 %. Las líneas se cruzan entre RAG básico y Agentic-RAG: gpt-5-nano desciende y gpt-5-mini asciende, mientras gpt-5 se mantiene por encima de 0,65 en las tres estrategias.],
) <fig-interaccion>

El análisis de las medias por combinación —cuyas estimaciones modeladas figuran en la @tabla-celdas-principal— revela un patrón de interacción disordinal, con líneas que se cruzan.

Las principales observaciones son:

+ *gpt-5 mantiene el desempeño más alto en las tres estrategias*: su probabilidad predicha de obtener al menos 0,75 se mantiene por encima de 0,65 en todas las condiciones. No se atribuye esa estabilidad a un mecanismo interno de razonamiento del modelo: el diseño no permite separar el tamaño del modelo de otras diferencias entre proveedores y versiones.
+ *gpt-5-mini depende del contexto externo*: con Agentic-RAG alcanza una probabilidad predicha de 0,79 frente a 0,16 sin RAG, y la diferencia Agentic − Sin RAG es la mayor de la matriz (+0,513 de media).
+ *gpt-5-nano presenta un modo de fallo de respuesta*: 41 de las 79 salidas no son sustantivas, frente a 0 en RAG básico y 1 en Sin RAG. Cuando produce una respuesta sustantiva (38/79), su calidad es alta (media 0,820; mediana 0,958). La diferencia negativa a nivel sistema se explica por las salidas no sustantivas y no por una degradación uniforme de las respuestas efectivamente producidas.

=== Lectura del Patrón

+ La ausencia de diferencia marginal entre Agentic-RAG y RAG básico enmascara diferencias condicionales al modelo: en gpt-5-mini la diferencia es positiva y sustancial, mientras que en gpt-5-nano se invierte.
+ Con RAG básico las diferencias entre modelos son menores, pero no se demostró equivalencia; el sistema agéntico no las elimina.
+ El cruce de las líneas es disordinal, de modo que no existe un orden único de las estrategias ni de los modelos: la comparación debe hacerse célula por célula y con intervalos, no a partir del efecto marginal.

=== Diagnóstico de Agentic-RAG con gpt-5-nano

La celda Agentic-RAG con gpt-5-nano requiere una lectura separada. De las 79 unidades, 41 no contienen una respuesta sustantiva: 27 vacías, una con solo espacios, dos abstenciones explícitas, una truncada y diez indeterminadas. La @fig-diagnostico-estados desglosa esas 79 salidas y la @fig-diagnostico-tasas compara la tasa de salidas no sustantivas con la de las otras ocho celdas, donde es 0 % o 1,3 %.

#figure(
  image("../media/diagnostico_estados_nano_agentic.pdf", width: 80%),
  caption: [Estados de las 79 salidas de Agentic-RAG con gpt-5-nano. `Indeterminada` agrupa mensajes de proceso, marcadores de prueba y un mensaje interno; `Truncada` corresponde a una salida cortada.],
) <fig-diagnostico-estados>

#figure(
  image("../media/diagnostico_tasas_fallo.pdf", width: 88%),
  caption: [Tasa de salidas no sustantivas por celda, con intervalo de confianza del 95 % de Wilson sobre 79 unidades. El fenómeno está concentrado en Agentic-RAG con gpt-5-nano (51,9 %; IC 95 % 41,1–62,6) y, en menor medida, en Sin RAG con gpt-5-mini (19,0 %).],
) <fig-diagnostico-tasas>

La @fig-diagnostico-composicion muestra la composición completa de las nueve celdas. Los registros de los agentes permiten descartar varias explicaciones simples: los 79 logs contienen una llamada a `retrieve_relevant_documents` y al menos una a `final_result`, el `finish_reason` del especialista es `tool_call` en los 79 casos, y las salidas vacías o con solo espacios registran entre 1 y 12 documentos seleccionados, entre 2 y 6 búsquedas y entre 575 y 7.015 tokens de salida. No hay evidencia de falta de recuperación ni de truncamiento por límite de tokens; el texto final es vacío, contiene solo espacios o contiene un marcador no respondido. La causa de esa decisión de salida no puede determinarse con los logs disponibles.

#pagina-apaisada[
  #figure(
    image("../media/diagnostico_composicion_respuestas.pdf", width: 96%),
    caption: [Composición de las respuestas por estrategia y modelo, con 79 unidades por celda. La categoría `Sustantiva` reúne las salidas con contenido utilizable; las restantes corresponden a los tipos de salida no sustantiva definidos en el capítulo de metodología.],
  ) <fig-diagnostico-composicion>
]

La celda es heterogénea. Cuando el sistema produjo una respuesta sustantiva (38 de 79 unidades), la media de `respuesta_correcta_avg` fue 0,820 y la mediana 0,958. Cuando se asigna 0 a las salidas no sustantivas, la media de la celda es 0,395 y la mediana 0,000; cuando se excluyen esas salidas, la media es 0,820 y la mediana 0,958. Por lo tanto, el resultado a nivel sistema es inferior al de RAG básico, pero la calidad condicional a que el sistema responda es alta. La segunda comparación usa una submuestra seleccionada y no debe interpretarse como el efecto causal de la estrategia.

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

#pagina-apaisada[
  La @fig-analisis-sensibilidad muestra la media de corrección de las nueve celdas en cada escenario de tratamiento de las respuestas no sustantivas.

  #figure(
    image("../media/analisis_sensibilidad_escenarios.pdf", width: 96%),
    caption: [Media de la puntuación de corrección por celda en los cuatro escenarios de tratamiento de respuestas no sustantivas. Las curvas se superponen en las celdas sin salidas no sustantivas y se separan en Agentic-RAG con gpt-5-nano y en Sin RAG con gpt-5-mini.],
  ) <fig-analisis-sensibilidad>
]

La celda Agentic-RAG + gpt-5-nano concentra 41 de las 79 respuestas no sustantivas, de modo que es la única cuyo resultado depende del escenario. Bajo el escenario principal su media es 0,395 y su mediana 0,000; bajo exclusión la media asciende a 0,820 y la mediana a 0,958, pero sobre 38 unidades. Bajo puntajes observados la media es 0,415 y la mediana 0,250; bajo solo fallos técnicos = 0 los valores coinciden con el escenario principal, porque las abstenciones y los mensajes indeterminados de esa celda no recibieron puntajes positivos de los jueces.

No se trata de estimaciones contradictorias. La primera mide la utilidad del sistema completo, la segunda la calidad condicional a que el sistema responda y la tercera la forma en que los jueces califican salidas que no contienen respuesta. El manuscrito reporta las tres y no elige una sola como “el efecto” de Agentic-RAG. En gpt-5-mini y en gpt-5 la diferencia es positiva en los cuatro escenarios, con variación de centésimas.

== Análisis de Costos

=== Costos Descriptivos por Modelo y Sistema

Se calculó el costo total de cada consulta sumando el costo de generación de la respuesta y el costo de recuperación (cuando aplica). Los costos se analizaron por modelo, por sistema y por combinación modelo × sistema. La @fig-costos-configuracion presenta el costo medio por configuración.

#figure(
  image("../media/costos_por_configuracion.pdf", width: 100%),
  caption: [Costo medio por consulta (USD) para cada combinación modelo × estrategia de recuperación. El costo del sistema Agentic-RAG incluye las llamadas al Agente de Recuperación, que emplea gpt-5 independientemente del modelo del Agente Especialista Legal.],
) <fig-costos-configuracion>

#pagina-apaisada[
  === Relación Costo-Desempeño

  Para cada combinación se graficó el costo medio versus el desempeño medio en `respuesta_correcta_avg` y, complementariamente, en las cinco métricas textuales y semánticas (@fig-costo-desempenio). Este análisis permite identificar las configuraciones con mejor balance de eficiencia.

  #figure(
    image("../media/costo_desempenio.pdf", width: 82%),
    caption: [Relación costo-desempeño para `respuesta_correcta_avg` y las cinco métricas complementarias. Cada punto representa una combinación modelo × estrategia; el color indica la estrategia y la forma, el modelo. El cuadrante superior-izquierdo (alto desempeño, bajo costo) contiene las configuraciones más eficientes.],
  ) <fig-costo-desempenio>
]

=== Costo por Respuesta Correcta

El índice de eficiencia con costo normalizado min-max y piso de 0,01 se retiró: el piso determina por sí solo el valor de la configuración más barata y el ranking depende de una constante elegida. En su lugar se reporta el costo por respuesta correcta, definido como el costo total de la celda dividido por la cantidad de observaciones con puntaje promedio ≥ 0,75 (@tabla-costo-respuesta-correcta). La definición es una operacionalización de la rúbrica y no una categoría jurídica objetiva; el umbral 0,75 es el principal y la sensibilidad a 0,50 y 1,00 se documenta en el capítulo de metodología.

#pagina-apaisada[
  #figure(
    three-line-table(
      columns: (auto, auto, auto, auto, auto, auto, auto),
      [
        | *Estrategia* | *Modelo* | *Costo medio (USD)* | *Costo total (USD)* | *Correctas ≥ 0,75* | *Costo por correcta (USD)* | *IC 95 % bootstrap* |
        | :--- | :--- | ---: | ---: | :---: | ---: | :---: |
        | Sin RAG | gpt-5-nano | 0,0025 | 0,1981 | 26/79 | 0,0076 | 0,0058 a 0,0107 |
        | Sin RAG | gpt-5-mini | 0,0043 | 0,3395 | 11/79 | 0,0309 | 0,0183 a 0,0665 |
        | Sin RAG | gpt-5 | 0,0478 | 3,7731 | 49/79 | 0,0770 | 0,0652 a 0,0932 |
        | RAG básico | gpt-5-nano | 0,0025 | 0,2011 | 33/79 | *0,0061* | 0,0043 a 0,0091 |
        | RAG básico | gpt-5-mini | 0,0057 | 0,4465 | 38/79 | 0,0117 | 0,0088 a 0,0163 |
        | RAG básico | gpt-5 | 0,0392 | 3,0997 | 52/79 | 0,0596 | 0,0494 a 0,0721 |
        | Agentic-RAG | gpt-5-nano | 0,0447 | 3,5299 | 27/79 | 0,1307 | 0,0931 a 0,2036 |
        | Agentic-RAG | gpt-5-mini | 0,0564 | 4,4530 | 55/79 | 0,0810 | 0,0675 a 0,0988 |
        | Agentic-RAG | gpt-5 | 0,0792 | 6,2530 | 56/79 | 0,1117 | 0,0928 a 0,1370 |
      ],
    ),
    caption: [Costo medio, costo total y costo por respuesta correcta por celda, con 79 observaciones por celda. `Correctas ≥ 0,75` cuenta las observaciones cuyo puntaje promedio de los tres jueces alcanza el umbral bajo el escenario principal. Los intervalos provienen de un bootstrap por casos (25 casos, 5.000 réplicas). En negrita, el menor costo puntual por respuesta correcta.],
  ) <tabla-costo-respuesta-correcta>
]

El menor costo puntual por respuesta correcta corresponde a RAG básico con gpt-5-nano (USD 0,0061), seguido por Sin RAG con gpt-5-nano (USD 0,0076); los intervalos de ambas se solapan, de modo que el orden es descriptivo y no una diferencia formal. El mayor costo por respuesta correcta corresponde a Agentic-RAG con gpt-5-nano (USD 0,1307), porque solo 27 de 79 observaciones alcanzan el umbral. Agentic-RAG con gpt-5-mini cuesta USD 0,0564 por consulta y USD 0,0810 por respuesta correcta, frente a USD 0,0792 y USD 0,1117 de Agentic-RAG con gpt-5.

#figure(
  image("../media/costos_por_respuesta_correcta.pdf", width: 96%),
  caption: [Costo por respuesta correcta (puntaje ≥ 0,75) por configuración. Las barras ordenan las celdas por costo; el costo bajo por consulta de las configuraciones con gpt-5-nano no se traduce en un costo bajo por respuesta correcta cuando la tasa de respuestas correctas es reducida.],
) <fig-costo-respuesta-correcta>

=== Frontera de Pareto

La comparación entre costo medio y desempeño medio no admite un ganador único. Una configuración domina a otra si cuesta igual o menos y obtiene un desempeño igual o mayor, con al menos una desigualdad estricta. Siete de las nueve configuraciones son no dominadas y la frontera es escalonada (@fig-costos-pareto): Sin RAG con gpt-5-nano y RAG básico con gpt-5-nano ocupan el extremo de menor costo; RAG básico con gpt-5-mini y RAG básico con gpt-5 son las posiciones más estables bajo bootstrap (95,0 % y 94,3 % de las réplicas); Agentic-RAG con gpt-5-mini y con gpt-5 ocupan el extremo de mayor calidad y mayor costo.

#figure(
  image("../media/costos_pareto.pdf", width: 92%),
  caption: [Costo medio por consulta y media de corrección por configuración, con la frontera de Pareto (línea punteada) y escala logarítmica en el eje de costo. Quedan fuera de la frontera Sin RAG con gpt-5-mini y Agentic-RAG con gpt-5-nano, dominadas por alternativas más baratas y con mejor media.],
) <fig-costos-pareto>

Quedan fuera de la frontera Sin RAG con gpt-5-mini, dominada por alternativas más baratas y mejores, y Agentic-RAG con gpt-5-nano, dominada por RAG básico con gpt-5-nano y por otras celdas. No existe una recomendación universal: la elección depende del objetivo declarado —menor costo por respuesta correcta, menor costo por consulta o mayor calidad media— y de si el sistema se evalúa por su utilidad completa o por la calidad condicional a que responda.

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

Agentic-RAG mejora el recall en top-10 y el MRR respecto del baseline, pero la comparación no es causal: el baseline emplea una consulta y el sistema agéntico varias, y el presupuesto de recuperación no está igualado. No se comparó con BM25 ni con otro modelo de embeddings: la base vectorial no pudo recrearse porque el volumen de Milvus se perdió, de modo que la comparación de recuperadores no forma parte de esta tesis. La consecuencia es una limitación de la inferencia y no solo una nota de método: las métricas de la @tabla-metricas-recuperacion describen la recuperación observada con el embedding `hiiamsid/sentence_similarity_spanish_es`, pero no permiten atribuir el recall ni el MRR al embedding ni afirmar que sea superior a una búsqueda léxica. El baseline de `part_d` reproduce los valores previos del manuscrito (recall en top-10 = 0,333; MRR = 0,214; 27,9 % con todos; 59,5 % sin ninguno), y también se calculó con el mismo índice. La comparación controlada con BM25 y con un segundo embedding queda como trabajo futuro.

== Evaluación LLM-as-a-Judge

=== Modelos de Juez

Se emplearon tres modelos como jueces independientes, cuyas características y configuración se detallan en el #ref(<cap:metodologia>, supplement: [Capítulo]): DeepSeek-V3, Grok 4.1 Fast y Kimi K2 0905. Cada juez evaluó las 9 configuraciones usando las dos rúbricas definidas en dicho capítulo (`score_respuesta_correcta`, @tabla-rubrica-correcta; `score_precision_legal`, @tabla-rubrica-legal).

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
+ *Advertencia*: Agentic-RAG + gpt-5-nano presentó 41/79 salidas no sustantivas y el peor costo por respuesta correcta; no se recomienda sin réplicas ni ablaciones. La advertencia no es solo operativa: las estimaciones de todas las celdas provienen de una única ejecución por unidad y configuración, de modo que no permiten afirmar estabilidad entre corridas (véase la limitación correspondiente en el capítulo de conclusiones).

== Conclusiones del Capítulo

Los resultados muestran una interacción entre la estrategia de recuperación y el modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). En el escenario principal, Agentic-RAG fue inferior a RAG básico en gpt-5-nano (−0,270; IC 95% −0,330 a −0,202), superior en gpt-5-mini (+0,150; IC 95% 0,096 a 0,203) y superior en gpt-5 (+0,106; IC 95% 0,054 a 0,155). RAG básico no eliminó las diferencias entre modelos: las estimaciones fueron positivas y los intervalos no definen equivalencia. En Agentic-RAG con gpt-5-nano, 41 de 79 salidas no fueron sustantivas; cuando respondió, la calidad fue alta (38/79; media 0,820; mediana 0,958). El alpha de Krippendorff (0,807842 original; 0,799542 rúbrica) mide confiabilidad entre jueces, no validez frente a criterio humano. Las pruebas para muestras independientes del análisis original se conservan solo como antecedente exploratorio.

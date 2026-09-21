#import "@preview/oxdraw:0.1.0": *
#import "@preview/tablem:0.3.0": three-line-table
#import "../formato.typ": pagina-apaisada

= Evaluación y Resultados <cap:evaluacion>

// Este capítulo presenta los experimentos realizados, las métricas obtenidas
// y el análisis de los resultados del sistema Agentic-RAG.

== Introducción

Este capítulo presenta la evaluación sistemática del sistema Agentic-RAG y los resultados obtenidos. Se describen el diseño experimental, las métricas empleadas, los resultados de cada configuración y el análisis estadístico que fundamenta las conclusiones. El análisis sigue una progresión desde la exploración descriptiva hasta pruebas de hipótesis y análisis de interacción factorial.

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

Adicionalmente, se identificaron 27 observaciones (3.8% del total) con valores ausentes en las métricas de evaluación por jueces, atribuibles a fallos puntuales en la generación de respuestas para ciertas combinaciones subpregunta-configuración. Estos valores fueron excluidos de las pruebas de hipótesis mediante eliminación por lista (listwise deletion), reduciendo el conjunto efectivo a 684 observaciones para los análisis que involucran `respuesta_correcta_avg`.

== Verificación de Normalidad

=== Test de Shapiro-Wilk y Resultados

Se aplicó el test de Shapiro-Wilk ($H_0$: los datos siguen una distribución normal, $alpha = 0.05$) a nivel global (todas las observaciones por métrica) y a nivel de grupos (dentro de cada combinación estrategia × modelo).

La mayoría de las métricas rechazan la hipótesis nula de normalidad tanto a nivel global como por grupos. El caso de los scores de evaluación por jueces requiere una aclaración: al tratarse de mediciones ordinales en una escala discreta {0.0, 0.25, 0.5, 0.75, 1.0}, la normalidad no es un supuesto plausible _por construcción_ —una variable con cinco valores posibles y masa de probabilidad concentrada en ellos no puede seguir una distribución normal—, de modo que el test de Shapiro-Wilk no aporta evidencia adicional en este caso: se incluye por uniformidad del diagnóstico y solo confirma, como era esperable, el rechazo de $H_0$. El test resulta informativo para las 13 métricas textuales y semánticas, que son continuas y para las cuales la normalidad no puede descartarse _a priori_; allí los resultados también conducen al rechazo, lo que motiva el uso de pruebas no paramétricas para todas las métricas por igual. Se reportan, en consecuencia, los resultados del test para las 15 métricas.

=== Implicación Metodológica

Los resultados justifican el uso de pruebas no paramétricas para las comparaciones posteriores:

+ *Kruskal-Wallis* en lugar de ANOVA unilateral.
+ *Dunn con corrección de Bonferroni* como prueba post-hoc.
+ *Scheirer-Ray-Hare* en lugar de ANOVA factorial para evaluar interacciones.

== Comparaciones entre Estrategias y Modelos

=== Test de Kruskal-Wallis

Se aplicó el test de Kruskal-Wallis como alternativa no paramétrica al ANOVA para comparar las distribuciones de cada VR entre los niveles de cada factor.

En cuanto al *efecto de la estrategia de recuperación*, para la métrica `respuesta_correcta_avg` el test arrojó $H = 21.83$, $p < 0.001$, indicando diferencias significativas entre las tres estrategias de recuperación. Las medianas observadas fueron:

+ Agentic-RAG: 0.8333
+ RAG básico: 0.7083
+ Sin RAG: 0.5833

Respecto del *efecto del modelo*, para la misma métrica se obtuvo $H = 49.01$, $p < 0.001$, lo que confirma diferencias significativas entre modelos. Las medianas fueron:

+ gpt-5: 0.8333
+ gpt-5-mini: 0.5417
+ gpt-5-nano: 0.5833

=== Prueba Post-Hoc de Dunn

Las comparaciones por pares con corrección de Bonferroni revelaron los siguientes patrones para `respuesta_correcta_avg`:

*Entre estrategias:*
+ Agentic-RAG vs. sin RAG: $p = 0.000014$ — diferencia significativa.
+ RAG básico vs. sin RAG: $p = 0.0066$ — diferencia significativa.
+ Agentic-RAG vs. RAG básico: $p = 0.383$ — sin diferencia significativa.

*Entre modelos:*
+ gpt-5 vs. gpt-5-nano: $p < 0.0001$ — diferencia significativa.
+ gpt-5 vs. gpt-5-mini: $p = 0.000007$ — diferencia significativa.
+ gpt-5-mini vs. gpt-5-nano: $p = 0.101$ — sin diferencia significativa.

=== Análisis Estratificado: Efecto del Modelo dentro de cada Sistema

Se realizaron tests de Kruskal-Wallis estratificados por sistema de recuperación, con nivel de significación ajustado por Bonferroni ($alpha = 0.05 / 3 = 0.0167$):

+ *Agentic-RAG*: $H = 40.64$, $p < 0.0001$ — los modelos difieren significativamente.
+ *Sin RAG*: $H = 59.67$, $p < 0.0001$ — los modelos difieren significativamente.
+ *RAG básico*: $H = 4.71$, $p = 0.095$ — los modelos *no* difieren significativamente.

Este último resultado sugiere un *efecto igualador* del RAG básico: al proveer contexto relevante, las diferencias de capacidad entre modelos se atenúan, permitiendo que modelos más pequeños y económicos alcancen un desempeño comparable al del modelo de mayor tamaño.

=== Efectos Simples: Estrategia dentro de cada Modelo

El test de Scheirer-Ray-Hare reveló una interacción significativa entre estrategia y modelo ($H = 56.62$, $p < 10^(-11)$). Cuando existe interacción, los efectos principales no son interpretables de forma aislada: el efecto de la estrategia depende del modelo empleado. El análisis estratificado anterior evaluó el efecto del modelo dentro de cada estrategia; como complemento necesario, se evaluó el efecto de la estrategia dentro de cada modelo mediante tests de Mann-Whitney U (efectos simples de estrategia).

Dado que se realizan 9 comparaciones (3 modelos × 3 pares de estrategias), se aplicaron correcciones de Bonferroni y Holm-Bonferroni @holm1979simple mediante `statsmodels.stats.multitest.multipletests` @seabold2010statsmodels. La @tabla-efectos-simples presenta los resultados completos.

#pagina-apaisada[
  #figure(
    three-line-table(
      columns: (1.1fr, 1.1fr, 1.1fr, 1fr, 1fr, 1fr, 1.1fr, 1.2fr, 1fr),
      [
        | *Modelo*   | *Estrategia 1* | *Estrategia 2* | *Med. 1* | *Med. 2* |  *U*   |    *p*    | *p corr. Holm* | *Sig. Holm* |
        | :--------- | :------------- | :------------- | :------: | :------: | :----: | :-------: | :------------: | :---------: |
        | gpt-5      | agentic_rag    | base_rag       | *0.9583* |  0.8333  | 3475.5 | 0.024606  |    0.073819    |             |
        | gpt-5      | agentic_rag    | no_rag         | *0.9583* |  0.8333  | 3545.5 | 0.012841  |    0.063887    |             |
        | gpt-5      | base_rag       | no_rag         |  0.8333  |  0.8333  | 2850.5 | 0.889993  |    1.000000    |             |
        | gpt-5-mini | agentic_rag    | base_rag       | *0.9167* |  0.6250  | 3666.0 | 0.003055  |    0.018331    |     ✓      |
        | gpt-5-mini | agentic_rag    | no_rag         | *0.9167* |  0.3333  | 4964.0 | $<0.0001$ |   $<0.0001$    |     ✓      |
        | gpt-5-mini | base_rag       | no_rag         | *0.6250* |  0.3333  | 4349.0 | $<0.0001$ |   $<0.0001$    |     ✓      |
        | gpt-5-nano | agentic_rag    | base_rag       |  0.0833  | *0.5833* | 2076.0 | 0.002382  |    0.016676    |     ✓      |
        | gpt-5-nano | agentic_rag    | no_rag         |  0.0833  | *0.5833* | 2221.5 | 0.012777  |    0.063887    |             |
        | gpt-5-nano | base_rag       | no_rag         |  0.5833  |  0.5833  | 2923.5 | 0.896927  |    1.000000    |             |
      ],
    ),
    caption: [Efectos simples de estrategia dentro de cada modelo (Mann-Whitney U). `Med. 1` y `Med. 2` son las medianas de `respuesta_correcta_avg` para cada estrategia; en negrita, la mediana mayor de cada comparación. `p corr. Holm` es el p-value corregido por Holm-Bonferroni; ✓ indica significativo con corrección de Holm ($p_"corr" < 0.05$). $m = 9$ comparaciones.],
  ) <tabla-efectos-simples>
]

Los resultados revelan patrones diferenciados por modelo:

+ *gpt-5-mini* es el modelo más sensible a la estrategia: las tres comparaciones son significativas incluso con corrección de Holm-Bonferroni. Agentic-RAG (mediana 0.92) supera ampliamente a RAG básico (0.63) y a sin RAG (0.33), evidenciando una dependencia crítica del contexto externo.
+ *gpt-5-nano* muestra un comportamiento contraintuitivo: Agentic-RAG (0.08) degrada significativamente el desempeño respecto a RAG básico (0.58, $p_"corr" = 0.017$), pero la degradación frente a sin RAG (0.58, $p_"corr" = 0.064$) no alcanza significación con corrección de Holm. Esto sugiere que la complejidad agéntica es excesiva para modelos de capacidad reducida.
+ *gpt-5* se beneficia de Agentic-RAG (0.96 vs. 0.83 sin RAG, $p = 0.013$), aunque esta mejora no sobrevive a la corrección por comparaciones múltiples ($p_"corr" = 0.064$), indicando un efecto positivo pero moderado.

Estos resultados refuerzan el hallazgo de interacción: el efecto de Agentic-RAG es marcadamente beneficioso para modelos de capacidad media-alta pero perjudicial para el modelo más pequeño.

La @tabla-resumen-medianas presenta las medianas de `respuesta_correcta_avg` y, con fines descriptivos, de las cinco métricas complementarias para las nueve configuraciones evaluadas. Los valores de las métricas textuales y semánticas se incluyen como referencia, pero las pruebas de hipótesis se realizaron exclusivamente sobre `respuesta_correcta_avg`.

#pagina-apaisada[
  #figure(
    three-line-table(
      columns: (1.2fr, 1.2fr, 1.2fr, 1fr, 1fr, 1fr, 1fr, 1fr),
      [
        | *Estrategia* | *Modelo*   | *Resp. correcta* | *Token F1* | *ROUGE-L* | *SBERT (es)* | *BERTScore* | *Prec. legal* |
        | :----------- | :--------- | :--------------: | :--------: | :-------: | :----------: | :---------: | :-----------: |
        | Sin RAG      | gpt-5-nano |      0,583       |   0,200    |   0,123   |    0,740     |    0,688    |     0,000     |
        | Sin RAG      | gpt-5-mini |      0,333       |   0,176    |   0,123   |    0,629     |    0,674    |     0,000     |
        | Sin RAG      | gpt-5      |      0,833       |   0,243    |   0,141   |    0,760     |    0,694    |     0,333     |
        | RAG básico   | gpt-5-nano |      0,583       |   0,253    |   0,150   |    0,770     |    0,703    |     0,333     |
        | RAG básico   | gpt-5-mini |      0,625       |   0,213    |   0,135   |    0,760     |    0,700    |     0,417     |
        | RAG básico   | gpt-5      |      0,833       |   0,257    |   0,174   |    0,794     |    0,706    |     0,667     |
        | Agentic-RAG  | gpt-5-nano |      0,083       |   0,125    |   0,083   |    0,389     |    0,648    |     0,125     |
        | Agentic-RAG  | gpt-5-mini |      0,917       |   0,215    |   0,130   |   *0,795*    |    0,706    |     0,833     |
        | Agentic-RAG  | gpt-5      |     *0,958*      |  *0,277*   |  *0,190*  |    0,791     |   *0,708*   |    *0,875*    |
      ],
    ),
    caption: [Medianas por configuración (estrategia × modelo). `Resp. correcta` es la variable de respuesta principal utilizada en las pruebas de hipótesis; las columnas restantes (`Token F1`, `ROUGE-L`, `SBERT (es)`, `BERTScore`, `Prec. legal`) se incluyen con fines descriptivos. Los valores más altos indican mejor desempeño y se destacan en negrita (el máximo de cada columna). Destaca la mediana de 0,958 de Agentic-RAG + gpt-5 en respuesta correcta, y el valor anómalamente bajo de 0,083 para Agentic-RAG + gpt-5-nano.],
  ) <tabla-resumen-medianas>
]

== Análisis Factorial: Interacción Estrategia × Modelo

=== Test de Scheirer-Ray-Hare

Para evaluar si los efectos de la estrategia de recuperación y del modelo operan de forma independiente o interactúan, se aplicó el test de Scheirer-Ray-Hare (SRH), análogo no paramétrico al ANOVA factorial de dos vías. El procedimiento consiste en:

+ Asignar rangos globales a todas las observaciones.
+ Aplicar ANOVA de dos vías sobre los rangos.
+ Calcular el estadístico $H$ para cada efecto:

$ H = frac(S S_"efecto", M S_"total rangos") $

donde $H$ sigue una distribución $chi^2$ con los grados de libertad correspondientes.

=== Resultados de la Interacción

Los resultados para `respuesta_correcta_avg` fueron:

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto, auto),
    [
      | *Efecto*         |  *H*   | *gl* |           *p*           | *Sig.* |
      | :--------------- | :----: | :--: | :---------------------: | :----: |
      | Sistema          | 21.83  |  2   |        0.000018         |   Sí   |
      | Modelo           | 49.01  |  2   |        < 0.0001         |   Sí   |
      | Sistema × Modelo | *56.62* |  4   | *$1.48 times 10^(-11)$* |   Sí   |
    ],
  ),
  caption: [Resultados del test de Scheirer-Ray-Hare para `respuesta_correcta_avg`. En negrita, el efecto de interacción, que reúne el mayor estadístico $H$ y el menor p-value del análisis y constituye el hallazgo principal del capítulo.],
)

La interacción significativa ($H = 56.62$, $p < 10^(-11)$) indica que el efecto de la estrategia de recuperación *depende* del modelo empleado, y viceversa. El estadístico de interacción supera a ambos efectos principales, lo que implica que las combinaciones explican más varianza que los factores individuales.

=== Patrón de Interacción

La @fig-interaccion presenta el gráfico de interacción que visualiza cómo las líneas de los modelos se cruzan entre estrategias, evidenciando la interacción disordinal.

#pagina-apaisada[
  #figure(
    image("../media/interaccion_modelo_estrategia.pdf", width: 96%),
    caption: [Gráficos de interacción modelo × estrategia de recuperación para las seis métricas de respuesta. Las líneas representan la media de cada modelo con intervalos de confianza del 95%; cada panel corresponde a una métrica. El cruce de las líneas en `respuesta_correcta_avg` confirma la interacción disordinal: el modelo óptimo depende de la estrategia empleada.],
  ) <fig-interaccion>
]

El análisis de las medias por combinación revela un patrón de interacción disordinal (líneas cruzadas):

#figure(
  three-line-table(
    columns: (auto, auto, auto, auto),
    [
      | *Modelo*   | *agentic_rag* | *base_rag* | *no_rag* |
      | :--------- | :-----------: | :--------: | :------: |
      | gpt-5      |    *0.80*     |    0.70    |   0.73   |
      | gpt-5-mini |    *0.78*     |    0.64    |   0.35   |
      | gpt-5-nano |     0.40      |   *0.59*   |   0.58   |
    ],
  ),
  caption: [Medias de `respuesta_correcta_avg` por combinación modelo × sistema. En negrita, la estrategia con mejor desempeño dentro de cada modelo.],
)

Las principales observaciones son:

+ *gpt-5 es robusto*: mantiene un desempeño alto (0.70–0.80) en todas las condiciones, compensando parcialmente la ausencia de contexto mediante su capacidad de razonamiento interna.
+ *gpt-5-mini es sensible al RAG*: con Agentic-RAG alcanza 0.78 (comparable a gpt-5), pero sin RAG cae a 0.35, evidenciando una dependencia crítica del contexto externo.
+ *gpt-5-nano muestra un comportamiento contraintuitivo*: su desempeño es *peor* con Agentic-RAG (0.40) que con RAG básico (0.59), lo que sugiere que el sistema agéntico genera instrucciones y contextos de complejidad excesiva para un modelo de capacidad reducida.

=== Implicaciones para Resultados Previos

La interacción significativa matiza las conclusiones del análisis de Kruskal-Wallis:

+ La no-diferencia marginal entre Agentic-RAG y RAG básico enmascara diferencias condicionales al modelo: para gpt-5-mini la diferencia es sustancial (0.78 vs. 0.64), mientras que para gpt-5-nano la relación se invierte (0.40 vs. 0.59).
+ El efecto igualador del RAG básico se confirma, pero no aplica al sistema agéntico, que amplifica las diferencias entre modelos.

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

El Alpha de Krippendorff ($alpha$) es un coeficiente de acuerdo inter-anotadores que corrige el acuerdo esperado por azar, soporta múltiples anotadores y datos faltantes, y admite escala ordinal @krippendorff2004content. Los umbrales de interpretación según Krippendorff (2004) son: $alpha >= 0.800$ (bueno), $0.667 <= alpha < 0.800$ (aceptable), $alpha < 0.667$ (insuficiente).

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

+ Los sistemas con recuperación (RAG básico y Agentic-RAG) superan significativamente al baseline sin RAG en la métrica de corrección.
+ El sistema Agentic-RAG combinado con gpt-5-mini alcanza un desempeño comparable al de gpt-5 (0.78 vs. 0.80), ofreciendo una alternativa de menor costo.
+ El RAG básico presenta un efecto igualador sobre los modelos, eliminando las diferencias significativas de desempeño entre gpt-5, gpt-5-mini y gpt-5-nano.
+ El acuerdo inter-juez para `score_respuesta_correcta` es bueno ($alpha = 0.81$), validando la confiabilidad de las evaluaciones.

=== Debilidades y Limitaciones

+ El sistema Agentic-RAG degrada el desempeño de gpt-5-nano frente a RAG básico (0.40 vs. 0.59, $p_"corr" = 0.017$, Holm-Bonferroni), indicando que la complejidad agéntica es excesiva para modelos de capacidad reducida. La diferencia frente a sin RAG no es significativa tras la corrección ($p_"corr" = 0.064$).
+ La métrica `score_precision_legal` no alcanza confiabilidad inter-juez suficiente para ser empleada en comparaciones, lo que limita la evaluación de la precisión de citación.
+ No se encontró diferencia marginal significativa entre Agentic-RAG y RAG básico, aunque el análisis de interacción revela que esta conclusión global enmascara patrones condicionales al modelo.
+ El benchmark se limita al Código de Minería Argentino, por lo que la generalización a otros cuerpos normativos requiere validación adicional.

La ausencia de diferencias significativas para gpt-5 entre estrategias tras la corrección de Holm-Bonferroni admite múltiples interpretaciones no mutuamente excluyentes. En primer lugar, el modelo podría poseer conocimiento paramétrico suficiente del Código de Minería —cuya última modificación data de 2024 y cuyos textos son de acceso público— para responder correctamente sin necesidad de recuperación externa, lo que explicaría su elevada mediana sin RAG (0.83). En segundo lugar, la escala discreta de cinco niveles de la rúbrica de evaluación podría generar un efecto de techo: si las respuestas de gpt-5 se concentran en los valores superiores (0.75–1.00), la resolución de la rúbrica resulta insuficiente para discriminar mejoras marginales que el RAG podría aportar. En tercer lugar, la potencia estadística disponible (n = 79 observaciones por celda, 9 comparaciones) podría ser insuficiente para detectar efectos moderados tras una corrección exigente como Holm-Bonferroni; la diferencia cruda entre Agentic-RAG y sin RAG ($p = 0.013$) es significativa sin corregir, pero no sobrevive a la corrección. Finalmente, la capacidad discriminatoria de los jueces LLM —que no fueron configurados con cadenas de razonamiento explícitas y cuya alineación con criterios humanos no ha sido validada— podría ser limitada para distinguir matices de corrección jurídica entre respuestas de alta calidad. La validación con expertos legales humanos constituye el único camino para dirimir entre estas hipótesis.

=== Implicaciones Prácticas

+ *Combinación óptima*: Agentic-RAG + gpt-5 (media 0.80), pero con costo superior.
+ *Combinación costo-eficiente*: Agentic-RAG + gpt-5-mini (media 0.78) para escenarios con restricciones presupuestarias, siempre que el sistema RAG esté activo.
+ *No existe una recomendación universal*: la interacción significativa entre factores implica que la selección de modelo y estrategia debe hacerse conjuntamente, no de forma independiente.
+ *Advertencia para modelos pequeños*: evitar la combinación Agentic-RAG + gpt-5-nano, que constituye la peor configuración evaluada.

== Conclusiones del Capítulo

Los resultados confirman que la incorporación de un sistema de recuperación de información mejora significativamente la calidad de las respuestas de los LLM en el dominio legal argentino. La interacción significativa entre la estrategia de recuperación y el modelo ($H = 56.62$, $p < 10^(-11)$) es el hallazgo más relevante: demuestra que la efectividad de una estrategia depende del modelo con el que se combine, y viceversa. El análisis de efectos simples mediante Mann-Whitney U con corrección de Holm-Bonferroni revela que Agentic-RAG beneficia significativamente a gpt-5-mini (las tres comparaciones entre estrategias son significativas, $p_"corr" < 0.05$) pero degrada a gpt-5-nano frente a RAG básico ($p_"corr" = 0.017$). Para gpt-5, no se detectan diferencias significativas entre estrategias tras la corrección por comparaciones múltiples. El RAG básico actúa como igualador de capacidades entre modelos, mientras que el sistema agéntico amplifica las diferencias. La evaluación LLM-as-a-Judge con tres jueces es confiable para la métrica de corrección ($alpha = 0.81$) pero no para la de precisión legal ($alpha = 0.78$ global, con valores insuficientes por sistema).

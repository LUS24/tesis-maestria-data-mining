// Anexo de análisis exploratorio histórico
#import "@preview/tablem:0.3.0": three-line-table
#import "../formato.typ": pagina-apaisada

#set heading(numbering: "A.1")

= Análisis Exploratorio Histórico <anexo-analisis-exploratorio>

Este anexo conserva, como antecedente exploratorio, el primer conjunto de pruebas con el que se analizaron los resultados. Todas las pruebas que se describen aquí tratan las observaciones como independientes: ignoran que las 79 unidades se responden en las nueve configuraciones y que están anidadas en 25 casos. Por esa razón no sostienen las conclusiones del capítulo de evaluación y se reproducen únicamente para dejar constancia del recorrido analítico y de las cifras que aparecían en versiones anteriores del manuscrito.

El análisis se apoyó en pruebas de Shapiro-Wilk para la normalidad, de Kruskal-Wallis con post-hoc de Dunn para las comparaciones entre niveles de cada factor, y de Scheirer-Ray-Hare para la interacción. Los efectos simples por par de estrategias se estimaron con Mann-Whitney U; esa tabla no se reproduce porque se calculó sobre la base de 76 observaciones por celda, que quedó reemplazada por la base de 79 descrita en el capítulo de evaluación.

== Verificación de Normalidad

=== Test de Shapiro-Wilk y Resultados

Se aplicó el test de Shapiro-Wilk ($H_0$: los datos siguen una distribución normal, $alpha = 0.05$) a nivel global (todas las observaciones por métrica) y a nivel de grupos (dentro de cada combinación estrategia × modelo) @shapiro1965analysis.

La mayoría de las métricas rechazan la hipótesis nula de normalidad tanto a nivel global como por grupos. El caso de los puntajes de evaluación por jueces requiere una aclaración: al tratarse de mediciones ordinales en una escala discreta {0.0, 0.25, 0.5, 0.75, 1.0}, la normalidad no es un supuesto plausible _por construcción_ —una variable con cinco valores posibles y masa de probabilidad concentrada en ellos no puede seguir una distribución normal—, de modo que el test de Shapiro-Wilk no aporta evidencia adicional en este caso: se incluyó por uniformidad del diagnóstico y solo confirmó, como era esperable, el rechazo de $H_0$. El test resulta informativo para las 13 métricas textuales y semánticas, que son continuas y para las cuales la normalidad no puede descartarse _a priori_; allí los resultados también condujeron al rechazo.

=== Implicación Metodológica del Análisis Exploratorio

Los resultados motivaron el uso de pruebas no paramétricas para las comparaciones exploratorias:

+ *Kruskal-Wallis* en lugar de ANOVA unilateral.
+ *Dunn con corrección de Bonferroni* como prueba post-hoc.
+ *Scheirer-Ray-Hare* en lugar de ANOVA factorial para evaluar interacciones.

Esa decisión se adoptó sobre la distribución marginal de cada métrica y no sobre la estructura del diseño. La revisión posterior mostró que la razón principal para apartarse de las pruebas para muestras independientes es el apareamiento de las observaciones, no el rechazo de la normalidad: la ordinalidad del puntaje y la dependencia entre unidades invalidan los valores p de Kruskal-Wallis, Dunn y Scheirer-Ray-Hare aunque las distribuciones fueran normales.

== Comparaciones entre Estrategias y Modelos

=== Test de Kruskal-Wallis

Se aplicó el test de Kruskal-Wallis como alternativa no paramétrica al ANOVA para comparar las distribuciones de cada variable de respuesta entre los niveles de cada factor @kruskal1952use.

En cuanto al *efecto de la estrategia de recuperación*, para la métrica `respuesta_correcta_avg` el test arrojó $H = 21.83$, $p < 0.001$. Las medianas observadas fueron 0.8333 para Agentic-RAG, 0.7083 para RAG básico y 0.5833 para Sin RAG.

Respecto del *efecto del modelo*, para la misma métrica se obtuvo $H = 49.01$, $p < 0.001$. Las medianas fueron 0.8333 para gpt-5, 0.5417 para gpt-5-mini y 0.5833 para gpt-5-nano.

=== Prueba Post-Hoc de Dunn

Las comparaciones por pares con corrección de Bonferroni @dunn1964multiple @bonferroni2010teoria arrojaron los siguientes resultados para `respuesta_correcta_avg`:

*Entre estrategias:*
+ Agentic-RAG vs. Sin RAG: $p = 0.000014$.
+ RAG básico vs. Sin RAG: $p = 0.0066$.
+ Agentic-RAG vs. RAG básico: $p = 0.383$.

*Entre modelos:*
+ gpt-5 vs. gpt-5-nano: $p < 0.0001$.
+ gpt-5 vs. gpt-5-mini: $p = 0.000007$.
+ gpt-5-mini vs. gpt-5-nano: $p = 0.101$.

El valor $p = 0.383$ para Agentic-RAG frente a RAG básico se leyó en su momento como ausencia de diferencia entre estrategias. Esa lectura no se sostiene: el contraste marginal promedia modelos con efectos de signo opuesto y la falta de significación no demuestra equivalencia.

=== Análisis Estratificado: Efecto del Modelo dentro de cada Sistema

Se realizaron tests de Kruskal-Wallis estratificados por sistema de recuperación, con nivel de significación ajustado por Bonferroni ($alpha = 0.05 / 3 = 0.0167$):

+ *Agentic-RAG*: $H = 40.64$, $p < 0.0001$.
+ *Sin RAG*: $H = 59.67$, $p < 0.0001$.
+ *RAG básico*: $H = 4.71$, $p = 0.095$.

El valor $p = 0.095$ de RAG básico se interpretó como ausencia de diferencias entre modelos. Tampoco esa lectura se sostiene: el análisis pareado del capítulo de evaluación encuentra diferencias significativas entre gpt-5 y gpt-5-nano dentro de RAG básico y estimaciones positivas para los otros dos pares.

== Análisis Factorial: Interacción Estrategia × Modelo

=== Test de Scheirer-Ray-Hare

Para evaluar si los efectos de la estrategia de recuperación y del modelo operan de forma independiente o interactúan, se aplicó el test de Scheirer-Ray-Hare (SRH), análogo no paramétrico al ANOVA factorial de dos vías @scheirer1976analysis. El procedimiento consiste en:

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
  caption: [Resultados del test de Scheirer-Ray-Hare para `respuesta_correcta_avg`, cálculo exploratorio sobre observaciones tratadas como independientes. La interacción se confirmó después con la prueba de razón de verosimilitud del modelo ordinal mixto (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²).],
)

=== Implicaciones para los Resultados Previos

La interacción detectada por el test exploratorio anticipó el patrón que el modelo ordinal confirmó: el efecto de la estrategia depende del modelo del especialista. La @fig-interaccion-historica conserva el gráfico de medias con el que se describió ese patrón en la primera versión; las medias no coinciden con las del capítulo de evaluación porque provienen de la base de 76 observaciones por celda y del escenario de puntajes observados.

#pagina-apaisada[
  #figure(
    image("../media/interaccion_modelo_estrategia.pdf", width: 96%),
    caption: [Gráficos de interacción modelo × estrategia para las seis métricas de respuesta, cálculo exploratorio histórico. Las líneas representan la media de cada modelo con intervalos de confianza del 95 %. La figura se conserva como antecedente; las estimaciones vigentes son las del modelo ordinal (@fig-interaccion).],
  ) <fig-interaccion-historica>
]

La comparación entre Agentic-RAG y RAG básico, que en el análisis marginal aparecía como no significativa, se resuelve en diferencias de signo opuesto por modelo. El test de Scheirer-Ray-Hare no identifica cuál componente de la estrategia produce esa dependencia y no permite estimar magnitudes ni intervalos; por eso se conserva solo como antecedente.

== Nota sobre los Efectos Simples Históricos

La tabla de efectos simples de la primera versión se calculó con U de Mann-Whitney sobre la base de 76 observaciones por celda y con corrección de Holm-Bonferroni @holm1979simple @seabold2010statsmodels. Sus valores no son comparables con los del capítulo de evaluación: además del cambio de base, la prueba trata las observaciones como independientes y no incorpora el anidamiento por caso ni la severidad del juez. La tabla se retiró del manuscrito y sus conclusiones se reemplazaron por las dos familias de contrastes del modelo ordinal.

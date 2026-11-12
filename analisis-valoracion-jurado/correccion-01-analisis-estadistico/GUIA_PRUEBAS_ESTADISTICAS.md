# Guía de pruebas estadísticas empleadas — IX.1.1

**Corrección:** IX.1.1 — análisis estadístico inferencial con apareamiento por unidad y anidamiento en casos.  
**Fecha:** 2026-11-12.  
**Código:** `src/run_ordinal_model.R`, `src/run_nonparametric.py`, `src/make_figures.py`.  
**Citas:** `citas_estadisticas/citas_estadisticas.bib`, validadas con el método de la corrección 07.

Esta guía explica **cuándo se usa cada prueba, cómo se calcula, cómo se interpretan sus estadísticos, qué figura la representa y qué cita conviene agregar al manuscrito**. No reemplaza el informe de resultados; lo complementa.

---

## 1. Estructura de los datos y notación

| Símbolo | Significado |
|---|---|
| `c = 1, …, 25` | Caso del benchmark |
| `u = 1, …, 79` | Unidad de evaluación; `u` está anidada en `c` |
| `s ∈ {Sin RAG, RAG básico, Agentic-RAG}` | Estrategia de recuperación |
| `m ∈ {gpt-5-nano, gpt-5-mini, gpt-5}` | Modelo del Agente Especialista Legal |
| `j ∈ {Grok, DeepSeek, Kimi}` | Juez automático |
| `Y_{u,c,s,m,j}` | Puntaje ordinal de corrección, `{0; 0,25; 0,50; 0,75; 1}` |

Hay 711 observaciones `(u, s, m)` y 2.133 evaluaciones `(u, s, m, j)`. La unidad `u` se repite en las nueve configuraciones; por eso las observaciones no son independientes. Además, las unidades comparten el escenario del caso `c`.

La variable `Y` es **ordinal**: los valores están ordenados, pero la distancia entre 0 y 0,25 no tiene por qué ser la misma que entre 0,75 y 1. Por eso el análisis principal no es una regresión lineal ni un ANOVA de medias.

---

## 2. Mapa rápido: qué prueba responde qué pregunta

| Pregunta | Prueba principal | Unidad | Estadístico | Figura | Cita |
|---|---|---|---|---|---|
| ¿La estrategia y el modelo interactúan? | Modelo ordinal mixto + razón de verosimilitud | Evaluación juez-observación | Coeficientes, OR, LR χ² | `02_interaccion_prob_ge_075` | `@mccullagh1980`, `@agresti2010`, `@laird1982`, `@wilks1938` |
| ¿Qué diferencia hay entre celdas? | Medias marginales y contrastes | Evaluación / celda | Diferencia de media, diferencia de P(≥ 0,75) | `03_efectos_simples_probabilidad` | `@searle1980`, `@lenth2026emmeans` |
| ¿Se controla el error familiar? | Holm | Familia de 9 contrastes | p ajustado | tablas | `@holm1979` |
| ¿Hay diferencias globales entre estrategias/modelos? | Friedman | Unidad (79 bloques) | χ², W de Kendall | tablas | `@friedman1937`, `@kendall1939` |
| ¿Qué pares difieren? | Wilcoxon de rangos con signo | Unidad apareada | W, p, r rango-biserial | tablas | `@wilcoxon1945`, `@cureton1956` |
| ¿Cuánta incertidumbre hay? | Bootstrap por casos | Caso (25 bloques) | IC percentil | barras/forest | `@efron1979`, `@field2007` |
| ¿Qué modelo tiene mejor ajuste? | AIC | Modelo | −2 logL + 2k | tablas | `@akaike1974` |

---

## 3. Modelo ordinal mixto de enlaces acumulativos

### 3.1 Cuándo se usa

Se usa cuando:

- la respuesta es ordinal con pocos niveles;
- las mismas unidades se repiten en varias condiciones;
- hay agrupamiento jerárquico (unidades dentro de casos);
- se quiere estimar el efecto de estrategia, modelo y su interacción controlando la severidad del juez.

Es el **análisis principal** de IX.1.1. No se usa para reemplazar el análisis descriptivo ni para afirmar causalidad.

### 3.2 Cómo se calcula

Para una evaluación con estrategia `s`, modelo `m`, juez `j`, caso `c` y unidad `u`, el modelo acumulativo logit se escribe:

```text
logit[P(Y ≤ k)] = θ_k − (β0 + βS·S + βM·M + βSM·(S×M) + βJ·J + b_c + b_u)
```

para `k = 0, 1, 2, 3` (los cuatro umbrales que separan las cinco categorías). `F(z) = 1/(1+e^(−z))` es la función logística. Los umbrales `θ_k` son parámetros del modelo; `b_c ~ N(0, σ_c²)` y `b_u ~ N(0, σ_u²)` son interceptos aleatorios de caso y unidad.

El modelo se ajusta por máxima verosimilitud con aproximación de Laplace (`ordinal::clmm`, `nAGQ = 1`, `Hess = TRUE`). La implementación concreta es la de `@christensen2026ordinal`; la formulación estadística es la de `@mccullagh1980` y `@agresti2010`; los interceptos aleatorios siguen el marco de `@laird1982`.

### 3.3 Cómo se interpretan los estadísticos

#### Coeficientes `β` y odds ratios

Un coeficiente `β` positivo indica que, manteniendo constantes los demás términos, un aumento de esa variable se asocia con **mayor probabilidad de estar en categorías superiores** de la rúbrica. El odds ratio acumulativo es:

```text
OR = exp(β)
```

- `OR = 1`: sin asociación.
- `OR > 1`: mayor odds de una categoría superior.
- `OR < 1`: menor odds de una categoría superior.

El OR **no es una probabilidad ni un riesgo relativo**. En un modelo acumulativo, el OR se interpreta como el cambio en la odds de superar un umbral, bajo el supuesto de que el efecto es el mismo para todos los umbrales (odds proporcionales). Ese supuesto se declara; el modelo usa umbrales flexibles, pero no se estima un modelo nominal no proporcional.

#### Umbrales `θ_k`

Son los puntos de corte en la escala latente. No tienen una interpretación sustantiva directa; se usan para calcular probabilidades predichas. Un umbral más alto desplaza la distribución hacia categorías superiores.

#### Varianzas de efectos aleatorios

`σ_c²` y `σ_u²` describen cuánto varía el nivel medio de corrección entre casos y entre unidades después de controlar estrategia, modelo y juez.

- `σ_u²` grande: las unidades difieren mucho en dificultad.
- `σ_c²` grande: los casos difieren en dificultad media.
- Si ambas son cercanas a cero, el agrupamiento aporta poca heterogeneidad; el modelo igualmente respeta el diseño.

En el modelo principal: `σ_c² = 0,164` y `σ_u² = 1,383`. La unidad explica mucha más heterogeneidad que el caso.

#### Probabilidades predichas

Con los umbrales y los coeficientes se calcula:

```text
P(Y = k) = F(θ_k − η) − F(θ_(k−1) − η)
```

donde `η` es la parte fija y `F` es la logística, con `θ_(−1) = −∞` y `θ_4 = +∞`. Las probabilidades de las cinco categorías suman 1. A partir de ellas:

```text
P(Y ≥ 0,75) = P(Y = 0,75) + P(Y = 1)
E[Y] = 0·P(0) + 0,25·P(0,25) + 0,50·P(0,50) + 0,75·P(0,75) + 1·P(1)
```

`P(Y ≥ 0,75)` se usa como proporción modelada de respuestas “mayormente correctas”. **No es la proporción observada** de la muestra; es una predicción del modelo con efectos aleatorios en cero y promedio sobre los jueces.

#### AIC

```text
AIC = −2·logL + 2·p
```

donde `p` es el número de parámetros. Menor AIC indica mejor equilibrio entre ajuste y complejidad **para comparar modelos sobre los mismos datos** (`@akaike1974`). No es una prueba de hipótesis ni una medida absoluta de calidad.

### 3.4 Gráficos del modelo

- **`02_interaccion_prob_ge_075.png`**: líneas de `P(Y ≥ 0,75)` por estrategia, una línea por modelo, con bandas de IC 95% por simulación. Si las líneas no son paralelas, hay interacción. El cruce o cambio de orden indica que el modelo óptimo depende de la estrategia. No leer la figura como prueba de significación: la prueba es el LR y los contrastes.
- **`01_medias_por_celda_principal.png`**: barras de la media observada bajo el escenario principal, con IC bootstrap por casos. Sirve para describir el nivel y la incertidumbre; no controla el anidamiento por sí sola.
- **`03_efectos_simples_probabilidad.png`**: forest plot de diferencias entre celdas. Cada punto es una diferencia de media esperada (o de P≥0,75); la barra es el IC 95%; la línea vertical en 0 es “sin diferencia”. Si el IC cruza 0, la diferencia es compatible con ausencia de efecto; si no lo cruza, hay evidencia de diferencia en la dirección del signo.

### 3.5 Citas para el manuscrito

En metodología, al presentar el modelo:

> “Se ajustó un modelo ordinal mixto de enlaces acumulativos con función logit y umbrales flexibles @mccullagh1980 @agresti2010, con interceptos aleatorios por caso y por unidad @laird1982, implementado con `ordinal::clmm` @christensen2026ordinal.”

En resultados, al interpretar OR:

> “Los coeficientes se reportan como odds ratios acumulativos; un OR mayor que 1 indica mayor odds de una categoría superior de la rúbrica, no una diferencia de medias ni una probabilidad.”

---

## 4. Prueba de razón de verosimilitud para la interacción

### 4.1 Cuándo se usa

Se usa para comparar dos modelos anidados: el modelo completo con `estrategia × modelo` y el modelo reducido que elimina solo esa interacción. Es la prueba principal de la interacción.

### 4.2 Cómo se calcula

```text
LR = −2·(logL_reducido − logL_completo)
gl = p_completo − p_reducido
p = P(χ²_gl ≥ LR)
```

En este análisis, `LR = 293,00`, `gl = 4`, `p = 3,50 × 10⁻⁶²`. Los 4 grados de libertad corresponden a los cuatro términos de interacción del diseño 3 × 3 (2 × 2).

### 4.3 Cómo se interpreta

- `p < α`: la interacción aporta información; el efecto de la estrategia depende del modelo (y viceversa).
- `p ≥ α`: no hay evidencia suficiente de interacción; no se concluye equivalencia.
- Un LR grande con 4 gl indica que la mejora de ajuste del modelo completo es grande.
- La prueba supone modelos anidados y verosimilitud calculada sobre los mismos datos. No es una comparación de AIC.

### 4.4 Cita

`@wilks1938` para la distribución asintótica del LR. En el manuscrito:

> “La interacción se contrastó con una prueba de razón de verosimilitud @wilks1938.”

---

## 5. Medias marginales y efectos simples

### 5.1 Cuándo se usa

Cuando la interacción es significativa, los efectos principales no se interpretan aisladamente. Se calculan **efectos simples**: estrategia dentro de cada modelo y modelo dentro de cada estrategia.

### 5.2 Cómo se calcula

Se usan las medias marginales poblacionales del modelo (`emmeans`), que promedian sobre los niveles de los demás factores con pesos iguales. Para cada contraste:

```text
Δ = media_marginal(celda A) − media_marginal(celda B)
```

En escala latente, el contraste es una combinación lineal de coeficientes; en escala de probabilidad, se calcula a partir de las probabilidades predichas. Los IC 95% se obtienen por simulación de 4.000 draws de la distribución asintótica de los coeficientes y umbrales.

### 5.3 Cómo se interpreta

- La diferencia de media esperada está en la escala 0–1 de la rúbrica; es más intuitiva que el coeficiente logit.
- La diferencia de `P(≥ 0,75)` está en puntos de probabilidad; `+0,15` significa 15 puntos porcentuales más de probabilidad modelada de una respuesta mayormente correcta.
- Un IC que excluye 0 indica dirección consistente; un IC que lo cruza no permite afirmar una diferencia.
- No comparar magnitudes de `P(≥ 0,75)` entre modelos con distinta calibración sin mirar también la media esperada y la tasa de fallo.

### 5.4 Citas

`@searle1980` para medias marginales poblacionales; `@lenth2026emmeans` para la implementación. En el manuscrito:

> “Los efectos simples se calcularon como medias marginales poblacionales @searle1980 con `emmeans` @lenth2026emmeans.”

---

## 6. Corrección de Holm

### 6.1 Cuándo se usa

Cuando se hacen varias comparaciones dentro de una familia y se quiere controlar la tasa de error familiar sin ser tan conservador como Bonferroni. En este análisis se aplica a:

- 9 contrastes de estrategia dentro de modelo;
- 9 contrastes de modelo dentro de estrategia.

### 6.2 Cómo se calcula

Se ordenan los `m` p-values de menor a mayor: `p_(1) ≤ … ≤ p_(m)`. Se compara cada uno con:

```text
α / (m − i + 1)
```

y se aplica el procedimiento step-down: se rechaza hasta la primera comparación que no cumple el umbral. El p ajustado de Holm se calcula de forma equivalente y se reporta como `p_holm`.

### 6.3 Cómo se interpreta

- `p_holm < 0,05`: diferencia significativa controlando la familia.
- `p_holm ≥ 0,05`: no se rechaza; no implica equivalencia.
- Holm controla la probabilidad de al menos un falso positivo bajo la hipótesis nula global, con más potencia que Bonferroni.
- La familia debe estar definida antes de mirar los resultados. No se agrupan contrastes según conveniencia.

### 6.4 Cita

`@holm1979`. En el manuscrito:

> “Los p-values de los efectos simples se ajustaron con el procedimiento step-down de Holm @holm1979 dentro de cada familia de nueve comparaciones.”

---

## 7. Prueba de Friedman y W de Kendall

### 7.1 Cuándo se usa

Cuando se comparan `k ≥ 3` condiciones medidas en los mismos bloques (las mismas unidades) y no se quiere imponer normalidad. En este análisis:

- tres estrategias dentro de cada modelo;
- tres modelos dentro de cada estrategia.

Es una **sensibilidad no paramétrica** del modelo ordinal, no su reemplazo.

### 7.2 Cómo se calcula

Para `n` bloques y `k` tratamientos, se asignan rangos dentro de cada bloque y se suman por tratamiento (`R_j`):

```text
χ² = [12 / (n·k·(k+1))] · Σ_j R_j² − 3·n·(k+1)
gl = k − 1
```

Con empates se aplica la corrección correspondiente. El coeficiente de concordancia de Kendall es:

```text
W = χ² / [n·(k−1)]
```

`W` va de 0 a 1: 0 indica ausencia de concordancia en el ordenamiento; 1, concordancia perfecta.

### 7.3 Cómo se interpreta

- `p` de Friedman: al menos una condición difiere en rangos.
- `W`: magnitud de la concordancia global. No hay un umbral universal; reportar el valor y el contexto. En este análisis, `W` es bajo para estrategia en nano (0,076) y gpt-5 (0,082), y moderado en mini (0,347); es alto para modelo dentro de estrategia (0,148–0,388).
- Friedman no identifica qué pares difieren; para eso se usa Wilcoxon.
- Friedman no modela covariables ni efectos aleatorios; por eso no reemplaza al `clmm`.
- Si hay datos faltantes, Friedman usa solo bloques completos; el `n` de bloques debe informarse.

### 7.4 Citas

`@friedman1937` para la prueba; `@kendall1939` para `W`. En el manuscrito:

> “Como sensibilidad no paramétrica se aplicó la prueba de Friedman @friedman1937, con W de Kendall @kendall1939 como tamaño de efecto de concordancia.”

---

## 8. Wilcoxon de rangos con signo y correlación rango-biserial

### 8.1 Cuándo se usa

Para comparar **dos** condiciones medidas en las mismas unidades, sin supuesto de normalidad. Se usa como post-hoc de Friedman y como sensibilidad del modelo ordinal. No se usa Mann–Whitney porque las muestras no son independientes.

### 8.2 Cómo se calcula

Para cada par apareado `(x_i, y_i)`:

```text
d_i = x_i − y_i
```

Se descartan los `d_i = 0` (según la convención `zero_method = "wilcox"`), se ordenan los valores absolutos y se suman los rangos positivos (`W+`) y negativos (`W−`). El estadístico es `W = min(W+, W−)`. El p-value se obtiene de la distribución exacta o asintótica según el tamaño y los empates.

La correlación rango-biserial apareada es:

```text
r = (W+ − W−) / (W+ + W−)
```

### 8.3 Cómo se interpreta

- `W` no tiene una escala intuitiva; el signo y el p son más informativos.
- `r` va de −1 a +1. El signo indica dirección de la diferencia; la magnitud, tamaño del efecto. Convenciones descriptivas habituales: `|r| ≈ 0,1` pequeño, `0,3` mediano, `0,5` grande; no son puntos de corte universales.
- `p < 0,05`: diferencia consistente; `p ≥ 0,05`: no se rechaza, no equivalencia.
- Los ceros y empates reducen el número efectivo de pares; reportar `n` y `n_no_cero`.

### 8.4 Citas

`@wilcoxon1945` para la prueba; `@cureton1956` para la correlación rango-biserial. En el manuscrito:

> “Los contrastes pareados se realizaron con Wilcoxon de rangos con signo @wilcoxon1945 y se reportó la correlación rango-biserial @cureton1956.”

---

## 9. Bootstrap por casos

### 9.1 Cuándo se usa

Para estimar IC de medias, medianas y diferencias sin depender de normalidad, respetando la dependencia entre unidades de un mismo caso. Se usa en:

- IC de medias por celda;
- IC de diferencias apareadas;
- IC de diferencias de `P(≥ 0,75)` (cuando se calculan desde el modelo, se usa simulación paramétrica; el bootstrap se usa para los estadísticos observados).

### 9.2 Cómo se calcula

1. Se identifican los 25 casos.
2. En cada réplica `b = 1, …, B`, se muestrean 25 casos **con reposición**.
3. Se incluyen todas las unidades de cada caso seleccionado.
4. Se calcula el estadístico (media, mediana o diferencia apareada).
5. Los IC percentiles son los cuantiles 2,5% y 97,5% de las `B` réplicas.

En este análisis `B = 5.000` y la semilla es `20261112`. El bootstrap **no remuestrea filas**: hacerlo rompería el anidamiento y produciría IC demasiado estrechos.

### 9.3 Cómo se interpreta

- El IC percentil indica el rango de valores plausibles del estadístico bajo el mecanismo de remuestreo.
- Si el IC de una diferencia excluye 0, hay evidencia de dirección consistente; si lo cruza, no se puede afirmar la dirección.
- El bootstrap captura la variabilidad de muestreo de casos y unidades, **no** la variabilidad entre ejecuciones del mismo modelo. Para eso harían falta réplicas.
- El IC no es una prueba de hipótesis; no convertir “IC cruza 0” en “efecto nulo” sin discutir potencia.

### 9.4 Citas

`@efron1979` para el bootstrap; `@field2007` para bootstrap de datos agrupados. En el manuscrito:

> “Los intervalos de confianza se estimaron por bootstrap percentil con remuestreo de casos completos @efron1979 @field2007.”

---

## 10. AIC

### 10.1 Cuándo se usa

Para comparar el modelo con y sin interacción, y para describir el equilibrio ajuste–complejidad. No se usa como prueba de hipótesis.

### 10.2 Cómo se calcula

```text
AIC = −2·logL + 2·p
```

### 10.3 Cómo se interpreta

- Menor AIC es mejor **entre modelos ajustados a los mismos datos**.
- La diferencia de AIC no tiene un p-value; se reporta como diferencia descriptiva.
- Un AIC menor no implica que el modelo sea “verdadero” ni causalmente correcto.
- No comparar AIC de modelos con distintas muestras (por ejemplo, principal vs exclusión).

### 10.4 Cita

`@akaike1974`. En el manuscrito:

> “Se reportó el AIC @akaike1974 como medida descriptiva de ajuste y complejidad.”

---

## 11. Estadísticos descriptivos y elección de pruebas

### 11.1 Media, mediana, IQR y proporción ≥ 0,75

Se reportan media, mediana, Q1–Q3 y proporción de puntajes ≥ 0,75 por celda. La mediana es más robusta a la masa de ceros; la media conserva la escala 0–1 y es comparable con la diferencia media del modelo.

La proporción observada `P(≥ 0,75)` se calcula sobre las evaluaciones juez-observación después de la imputación principal. La predicción `P(≥ 0,75)` del modelo es otra cantidad: se calcula con los umbrales y coeficientes, no con un conteo directo.

### 11.2 Por qué no se usa Shapiro–Wilk para elegir la prueba

Shapiro–Wilk evalúa normalidad, pero la variable es ordinal por construcción y las observaciones están apareadas. La decisión del modelo se basa en la naturaleza ordinal y en la estructura de dependencia, no en un test de normalidad. Además, un p de Shapiro–Wilk no decide entre un modelo ordinal y uno lineal.

### 11.3 Por qué no se usa Kruskal–Wallis, Dunn ni Mann–Whitney como análisis principal

Esas pruebas suponen muestras independientes. Aquí las mismas unidades se repiten en las nueve configuraciones y están anidadas en casos. Usarlas como análisis principal desaprovecha el apareamiento e invalida los p-values. Se conservan solo como antecedente histórico o se eliminan.

### 11.4 Citas de software

- `ordinal` y `clmm`: `@christensen2026ordinal`.
- `emmeans`: `@lenth2026emmeans`.
- `MASS` para `mvrnorm`: `@venables2002`.
- SciPy para Friedman, Wilcoxon y bootstrap: `@virtanen2020scipy`.
- statsmodels para Holm: `@seabold2010statsmodels`.
- R: `@rcore2026`.

No es necesario citar todas las librerías en el cuerpo; se pueden agrupar en una nota de implementación o en el anexo de reproducibilidad.

---

## 12. Qué muestra cada figura y cómo leerla

| Figura | Qué representa | Cómo leerla | Qué no concluir |
|---|---|---|---|
| `01_medias_por_celda_principal` | Media observada por celda bajo fallo = 0, con IC bootstrap | Altura = media; barra = incertidumbre; comparar celdas y el umbral 0,75 | No controla el anidamiento por sí sola; no es una prueba de interacción |
| `02_interaccion_prob_ge_075` | `P(≥ 0,75)` predicha por el modelo, por estrategia y modelo | Líneas no paralelas = interacción; bandas = IC de simulación | No usar cruces como p-value; la prueba es el LR |
| `03_efectos_simples_probabilidad` | Diferencias de media esperada (o P≥0,75) entre celdas | Punto = diferencia; barra = IC; línea 0 = sin diferencia | Un IC que cruza 0 no prueba equivalencia |
| `04_sensibilidad_escenarios` | Media por celda en cuatro escenarios | Separación vertical = sensibilidad al tratamiento de no sustantivas | No es una prueba entre escenarios; es descriptiva |
| `05_distribucion_puntajes_principal` | Proporción de evaluaciones en cada nivel, tras imputar 0 | Masa en 0 = fallos o abstenciones; masa en 1 = respuestas correctas | No mide calidad jurídica de la respuesta |

---

## 13. Citas validadas y entradas BibTeX

El archivo `citas_estadisticas/citas_estadisticas.bib` contiene 19 entradas propuestas (3 ya existen en `referencias.bib`). La validación siguió el método de la corrección 07:

- 15 entradas con DOI: metadatos consultados en Crossref, comparación de título, año y primer autor;
- 4 entradas con URL: CRAN, R Project y JSTOR;
- todas las DOI respondieron 200 y coincidieron en título, año y primer autor;
- las URL respondieron 200/206;
- JSTOR devuelve “Client Challenge” para el artículo de Holm: la URL es válida, pero el título no es automatizable. Se conserva la entrada existente de Holm y se deja la observación.

| Clave | Referencia | Identificador | Estado | Uso |
|---|---|---|---|---|
| `mccullagh1980` | McCullagh (1980) | `10.1111/j.2517-6161.1980.tb01109.x` | verificado | Modelo ordinal |
| `agresti2010` | Agresti (2010) | `10.1002/9780470594001` | verificado | Modelo ordinal |
| `laird1982` | Laird y Ware (1982) | `10.2307/2529876` | verificado | Efectos aleatorios |
| `wilks1938` | Wilks (1938) | `10.1214/aoms/1177732360` | verificado | LR |
| `akaike1974` | Akaike (1974) | `10.1109/TAC.1974.1100705` | verificado | AIC |
| `friedman1937` | Friedman (1937) | `10.1080/01621459.1937.10503522` | verificado | Friedman |
| `kendall1939` | Kendall y Babington Smith (1939) | `10.1214/aoms/1177732186` | verificado | W de Kendall |
| `wilcoxon1945` | Wilcoxon (1945) | `10.2307/3001968` | verificado | Wilcoxon |
| `cureton1956` | Cureton (1956) | `10.1007/BF02289138` | verificado | rango-biserial |
| `efron1979` | Efron (1979) | `10.1214/aos/1176344552` | verificado | Bootstrap |
| `field2007` | Field y Welsh (2007) | `10.1111/j.1467-9868.2007.00593.x` | verificado | Bootstrap agrupado |
| `searle1980` | Searle et al. (1980) | `10.1080/00031305.1980.10483031` | verificado | Medias marginales |
| `holm1979` | Holm (1979) | `https://www.jstor.org/stable/4615733` | URL responde; JSTOR bloquea título | Holm |
| `christensen2026ordinal` | Christensen (2026) | `https://CRAN.R-project.org/package=ordinal` | URL responde | `clmm` |
| `lenth2026emmeans` | Lenth y Piaskowski (2026) | `https://CRAN.R-project.org/package=emmeans` | URL responde | `emmeans` |
| `venables2002` | Venables y Ripley (2002) | `10.1007/978-0-387-21706-2` | verificado | MASS |
| `virtanen2020scipy` | Virtanen et al. (2020) | `10.1038/s41592-019-0686-2` | verificado | SciPy |
| `seabold2010statsmodels` | Seabold y Perktold (2010) | `10.25080/majora-92bf1922-011` | verificado | statsmodels |
| `rcore2026` | R Core Team (2026) | `https://www.R-project.org/` | URL responde | R |

La tabla completa, con título y autores devueltos por la fuente, está en `citas_estadisticas/verificacion_citas_estadisticas.csv`. El resumen está en `resumen_validacion_citas.json`.

### 13.1 Cómo agregarlas al manuscrito

1. Copiar las entradas aprobadas de `citas_estadisticas.bib` a `manuscrito/referencias.bib`.
2. Verificar que no exista una clave previa con el mismo nombre. Ya existen en `referencias.bib`: `holm1979`, `virtanen2020scipy` y `seabold2010statsmodels`; no deben duplicarse. Las demás claves son nuevas.
3. Usar las claves en el texto, por ejemplo:
   - `@mccullagh1980`, `@agresti2010`, `@laird1982`, `@christensen2026ordinal` en metodología;
   - `@wilks1938` en la prueba de interacción;
   - `@akaike1974` si se reporta AIC;
   - `@friedman1937`, `@kendall1939`, `@wilcoxon1945`, `@cureton1956` en sensibilidad no paramétrica;
   - `@efron1979`, `@field2007` en bootstrap;
   - `@searle1980`, `@lenth2026emmeans` en medias marginales;
   - `@holm1979` en corrección de comparaciones.
4. No citar `@virtanen2020scipy` o `@seabold2010statsmodels` en el cuerpo si no se describe la implementación; pueden ir en una nota de software.
5. Compilar y revisar la lista de referencias; las entradas de software usan `@manual` y se renderizan sin DOI, lo cual es correcto.

### 13.2 Reproducir la validación

```bash
python3 analisis-valoracion-jurado/correccion-01-analisis-estadistico/citas_estadisticas/validar_citas.py
```

Esto consulta Crossref/URL con caché en `citas_estadisticas/cache/` y regenera:

- `verificacion_citas_estadisticas.csv`;
- `resumen_validacion_citas.json`.

La compilación de prueba está en `citas_estadisticas/prueba_citas.typ` y `prueba_citas.pdf`.

---

## 14. Errores de interpretación que deben evitarse

| Error | Por qué es incorrecto | Forma correcta |
|---|---|---|
| “p > 0,05 demuestra equivalencia” | La ausencia de evidencia no es evidencia de ausencia; depende de potencia y del margen de equivalencia | Reportar IC y no afirmar equivalencia sin prueba específica |
| “OR = 2 significa el doble de probabilidad” | El OR es una razón de odds, no de probabilidades | “El doble de odds de una categoría superior” |
| “La media predicha es la media observada” | La predicción poblacional usa efectos aleatorios en cero y promedio sobre jueces | Distinguir descriptivo de modelo |
| “Friedman prueba la interacción” | Friedman solo compara `k` condiciones en bloques; no modela interacción | Usar el modelo ordinal y el LR |
| “Wilcoxon es post-hoc de Friedman sin más” | Es una prueba pareada; requiere corrección y no modela anidamiento | Holm dentro de la familia y reportar `n` |
| “Bootstrap de filas” | Rompe la dependencia de unidades dentro de casos | Remuestrear casos completos |
| “AIC más bajo prueba causalidad” | AIC es descriptivo y relativo a los modelos comparados | Reportar ΔAIC y no inferir causalidad |
| “Shapiro–Wilk decide el modelo” | La variable es ordinal por construcción y hay dependencia | Elegir el modelo por diseño y escala |
| “Kruskal–Wallis/Dunn/Mann–Whitney son válidos aquí” | Suponen independencia; las unidades están apareadas | Modelo ordinal mixto y pruebas pareadas |

---

## 15. Resumen de una frase por prueba

- **Modelo ordinal mixto:** modela la probabilidad acumulada de una categoría superior, con efectos fijos de estrategia/modelo/juez y efectos aleatorios de caso/unidad.
- **LR:** compara el ajuste con y sin interacción; `p` pequeño indica que la interacción mejora el ajuste.
- **Medias marginales:** traducen el modelo a diferencias de media o de P(≥ 0,75) entre celdas.
- **Holm:** controla falsos positivos dentro de una familia de comparaciones.
- **Friedman:** detecta diferencias globales entre `k` condiciones medidas en los mismos bloques.
- **Kendall W:** mide la concordancia global de los rankings; 0 = ninguna, 1 = perfecta.
- **Wilcoxon:** compara dos condiciones apareadas; `W` y `p` indican diferencia, `r` indica tamaño y dirección.
- **Bootstrap por casos:** cuantifica incertidumbre remuestreando casos completos, no filas.
- **AIC:** compara ajuste y complejidad entre modelos con los mismos datos.

---

## 16. Referencias internas

- `INFORME_ANALISIS_ESTADISTICO.md` — resultados y decisiones.
- `PROTOCOLO_ANALISIS.md` — protocolo preespecificado.
- `PROPUESTA_TEXTO_MANUSCRITO.md` — texto sugerido para los `.typ`.
- `salidas/20_modelo_interaccion.csv` — LR y varianzas.
- `salidas/21_modelo_coeficientes.csv` — coeficientes y OR.
- `salidas/22_modelo_predicciones_celdas.csv` — probabilidades predichas.
- `salidas/23_efectos_simples_latentes.csv` — contrastes latentes y Holm.
- `salidas/24_efectos_simples_probabilidad.csv` — diferencias de media y P≥0,75.
- `salidas/33_friedman_principal.csv` — Friedman y W.
- `salidas/34_wilcoxon_principal.csv` — Wilcoxon, Holm, rango-biserial y bootstrap.
- `citas_estadisticas/citas_estadisticas.bib` — entradas BibTeX.
- `citas_estadisticas/verificacion_citas_estadisticas.csv` — validación.

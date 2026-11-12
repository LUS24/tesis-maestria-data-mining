# Propuesta de texto para el manuscrito — IX.1.1

**Uso:** documento de revisión. No se editó ningún `.typ`. Las cifras provienen del escenario principal con clasificación automática; si la revisión manual de la corrección 02 cambia alguna categoría, deben regenerarse con `run_all.sh` antes de insertarlas.

Los números entre corchetes `[...]` indican decisiones editoriales que el autor debe confirmar.

También se incluye `propuestas/preview_tablas.pdf`, una previsualización Typst independiente de las tablas principales. Es un borrador de revisión; no forma parte del manuscrito.

---

## 1. Resumen

### 1.1 Reemplazo sugerido para el párrafo de resultados del resumen

**Texto actual (idea):** “el RAG básico elimina las diferencias de desempeño entre modelos… Agentic-RAG no produce diferencias significativas en gpt-5”.

**Reemplazo propuesto:**

> Los resultados muestran una interacción entre estrategia de recuperación y modelo del Agente Especialista Legal. En el escenario principal, que asigna cero a las respuestas no sustantivas, Agentic-RAG reduce el desempeño de gpt-5-nano frente a RAG básico (diferencia modelada de −0,270; IC 95% −0,330 a −0,202), mientras que lo aumenta en gpt-5-mini (+0,150; IC 95% 0,096 a 0,203) y en gpt-5 (+0,106; IC 95% 0,054 a 0,155). La interacción es robusta (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²), pero no permite afirmar que el RAG básico “iguale” a los modelos ni que Agentic-RAG sea uniformemente superior. En gpt-5-nano, 41 de 79 unidades no reciben una respuesta sustantiva; cuando responde, la calidad es alta (media 0,820; mediana 0,958; n = 38). El patrón debe interpretarse como un problema de fiabilidad del sistema completo, no como una degradación uniforme de la calidad jurídica.

### 1.2 Palabras clave

Sin cambios. Si se quiere explicitar el enfoque, agregar “modelos ordinales mixtos” o “evaluación apareada”.

---

## 2. Metodología (`06_capitulo_05_metodologia.typ`)

### 2.1 Reemplazo de la sección “Análisis Estadístico” (líneas 672–695)

Sustituir las subsecciones `Verificación de Normalidad (Shapiro-Wilk)`, `Comparaciones No Paramétricas (Kruskal-Wallis y Dunn)` y `Análisis de Interacción Factorial (Scheirer-Ray-Hare)` por el texto siguiente. La subsección de Krippendorff puede conservarse después.

> **Diseño de medidas repetidas y modelo ordinal mixto**
>
> El diseño no es de grupos independientes. Las 79 unidades de evaluación se responden en las nueve configuraciones (tres estrategias × tres modelos), de modo que las observaciones están apareadas por unidad. Además, las unidades están anidadas en 25 casos, y cada respuesta recibe tres evaluaciones de jueces. Ignorar esas dependencias infla los grados de libertad, deja la dificultad de cada unidad dentro del error y vuelve inválidos los valores p de las pruebas para muestras independientes.
>
> La variable de respuesta principal es el puntaje ordinal de `score_respuesta_correcta` asignado por cada juez en la escala {0; 0,25; 0,50; 0,75; 1}. Los valores fuera de rúbrica se transformaron al valor más cercano, resolviendo los empates hacia el valor mayor, y se conservó el valor original para auditoría. Para el análisis principal, toda respuesta clasificada como no sustantiva —vacía, solo espacios, abstención, error, truncada o indeterminada— recibe puntaje 0 en las tres evaluaciones; las respuestas sustantivas conservan el puntaje de rúbrica de cada juez. Este escenario representa la utilidad del sistema completo y se denomina “fallo = 0”. Se reportan además tres escenarios de sensibilidad: puntajes observados, exclusión de respuestas no sustantivas y cero solo para fallos técnicos.
>
> El modelo principal es un modelo de enlaces acumulativos con función logit y umbrales flexibles:
>
> ```text
> score_respuesta_correcta ~ estrategia * modelo_especialista
>                            + juez
>                            + (1 | caso)
>                            + (1 | unidad)
> ```
>
> `unidad` es globalmente única; junto con `caso` representa el anidamiento. `juez` se incluye como efecto fijo para controlar la severidad sistemática de los tres evaluadores. La interacción se contrasta mediante una prueba de razón de verosimilitud entre el modelo completo y el modelo sin `estrategia:modelo_especialista` (4 grados de libertad). Los modelos se ajustaron con `ordinal::clmm` (`nAGQ = 1`, aproximación de Laplace, `Hess = TRUE`); se reportan convergencia e iteraciones.
>
> Se reportan odds ratios con IC 95%, probabilidades predichas por celda, media esperada y `P(score ≥ 0,75)`. Para los efectos simples se definieron dos familias de nueve comparaciones: estrategia dentro de cada modelo y modelo dentro de cada estrategia. La corrección de Holm se aplicó dentro de cada familia. Las diferencias de media esperada y de `P(score ≥ 0,75)` se acompañan con IC 95% obtenidos por simulación de 4.000 draws de la distribución asintótica de los coeficientes y umbrales.
>
> Como análisis de sensibilidad no paramétrico se usaron pruebas de Friedman para las tres estrategias dentro de cada modelo y para los tres modelos dentro de cada estrategia, con la unidad como bloque, W de Kendall como tamaño de efecto global y Wilcoxon de rangos con signo para los pares, con corrección de Holm dentro de cada familia. Los IC de las diferencias pareadas se estimaron por bootstrap por casos —remuestreando los 25 casos con todas sus unidades, 5.000 réplicas, semilla fija—, no por filas. Friedman y Wilcoxon no incorporan los efectos aleatorios; se interpretan como sensibilidad del modelo ordinal.

### 2.2 Otras correcciones en metodología

- En la descripción del diseño experimental, reemplazar “79 unidades × 9 configuraciones = 711 observaciones” por la misma cifra, pero aclarar que **no son independientes**: 79 unidades apareadas y anidadas en 25 casos, con tres jueces por respuesta. Ver `07_capitulo_06_evaluacion.typ`, línea 16.
- Eliminar la justificación de las pruebas no paramétricas basada únicamente en Shapiro–Wilk. La ordinalidad y la dependencia son la razón principal; Shapiro–Wilk no decide el método.
- En la sección de benchmark, reemplazar “unidades de evaluación independientes” (línea 539) por “unidades de evaluación” o “unidades apareadas”. Las unidades no son independientes.
- Agregar una frase: “El recuperador del sistema agéntico es siempre gpt-5; el factor ‘modelo’ designa al Agente Especialista Legal”. La corrección 04 desarrolla esta limitación.
- Si se conserva la tabla de hiperparámetros, no asociar temperatura 0 con determinismo; eso corresponde a IX.1.3.

---

## 3. Evaluación y resultados (`07_capitulo_06_evaluacion.typ`)

### 3.1 Reestructuración propuesta

Reemplazar el bloque de secciones desde `== Verificación de Normalidad` (línea 75) hasta el final de `=== Implicaciones para Resultados Previos` (línea 265) por una sección nueva:

```text
== Análisis inferencial del diseño apareado
=== Especificación del modelo
=== Interacción estrategia × modelo
=== Efectos simples
=== Sensibilidad al tratamiento de respuestas no sustantivas
=== Comparación con el análisis no paramétrico
=== Síntesis de la inferencia
```

Las secciones antiguas de Kruskal–Wallis, Dunn, Mann–Whitney y Scheirer–Ray–Hare pueden eliminarse o trasladarse a un anexo como “análisis exploratorio histórico”, claramente subordinado. No deben quedar como sustento principal.

### 3.2 Texto propuesto para “Especificación del modelo”

> El análisis inferencial se realizó con un modelo ordinal mixto de enlaces acumulativos (logit) sobre las 2.133 evaluaciones juez-observación. La variable de respuesta es el puntaje ordinal de corrección; los efectos fijos son estrategia, modelo del Agente Especialista Legal y juez; los efectos aleatorios son interceptos por caso y por unidad. La inclusión de ambos interceptos reconoce que las 79 unidades se repiten en las nueve configuraciones y que están anidadas en 25 casos. El modelo se ajustó con `ordinal::clmm` (aproximación de Laplace, `nAGQ = 1`, `Hess = TRUE`). La interacción se evaluó con una prueba de razón de verosimilitud de 4 grados de libertad.

### 3.3 Texto propuesto para “Interacción”

> La interacción entre estrategia y modelo del especialista es estadísticamente significativa (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). El modelo completo reduce el AIC de 5.810,3 a 5.525,0. Las varianzas de los efectos aleatorios son 0,164 para caso y 1,380 para unidad, lo que confirma que una parte sustancial de la variabilidad se explica por la dificultad de las unidades y de los casos. La interacción se mantiene en los escenarios de sensibilidad (LR entre 82,52 y 293,28; p < 10⁻¹⁶), aunque la dirección de algunos efectos simples depende del tratamiento de las respuestas no sustantivas.

### 3.4 Tabla propuesta para celdas

**Caption:** “Estadísticos descriptivos y predicciones por configuración bajo el escenario principal (respuestas no sustantivas = 0). `Media` y `Mediana` son descriptivos de la puntuación imputada; `Media modelo` y `P(≥ 0,75)` son predicciones poblacionales del modelo ordinal, con efectos aleatorios en cero y promedio sobre los tres jueces.”

| Estrategia | Modelo | n | No sust. | Media | Mediana | Media modelo | P(≥ 0,75) |
|---|---|---:|---:|---:|---:|---:|---:|
| Sin RAG | gpt-5-nano | 79 | 1 | 0,565 | 0,583 | 0,588 | 0,453 |
| Sin RAG | gpt-5-mini | 79 | 15 | 0,325 | 0,250 | 0,315 | 0,157 |
| Sin RAG | gpt-5 | 79 | 0 | 0,725 | 0,833 | 0,755 | 0,686 |
| RAG básico | gpt-5-nano | 79 | 0 | 0,599 | 0,583 | 0,616 | 0,490 |
| RAG básico | gpt-5-mini | 79 | 0 | 0,650 | 0,667 | 0,678 | 0,577 |
| RAG básico | gpt-5 | 79 | 0 | 0,707 | 0,833 | 0,744 | 0,670 |
| Agentic-RAG | gpt-5-nano | 79 | 41 | 0,395 | 0,000 | 0,346 | 0,182 |
| Agentic-RAG | gpt-5-mini | 79 | 1 | 0,788 | 1,000 | 0,828 | 0,787 |
| Agentic-RAG | gpt-5 | 79 | 0 | 0,812 | 1,000 | 0,850 | 0,816 |

No usar esta tabla para reemplazar la Tabla 11 sin actualizar también la tabla de sensibilidad. La Tabla 11 anterior se calculó sobre 76 observaciones por celda; la nueva base tiene 79.

### 3.5 Tabla propuesta para efectos simples de estrategia

**Caption:** “Efectos simples de estrategia dentro de cada modelo bajo el escenario principal. Diferencias orientadas como Agentic-RAG − RAG básico, Agentic-RAG − Sin RAG y RAG básico − Sin RAG. IC 95% por simulación del modelo ordinal. p de Holm corresponde a la familia de nueve contrastes en escala latente.”

| Modelo | Contraste | Δ media | IC 95% | Δ P(≥ 0,75) | IC 95% | p Holm |
|---|---|---:|---:|---:|---:|---:|
| gpt-5-nano | Agentic − RAG | **−0,270** | −0,330 a −0,202 | **−0,308** | −0,382 a −0,225 | 3,25 × 10⁻¹⁴ |
| gpt-5-nano | Agentic − Sin RAG | **−0,242** | −0,307 a −0,176 | **−0,270** | −0,349 a −0,192 | 1,18 × 10⁻¹¹ |
| gpt-5-nano | RAG − Sin RAG | 0,028 | −0,032 a 0,085 | 0,037 | −0,043 a 0,114 | 0,724 |
| gpt-5-mini | Agentic − RAG | **+0,150** | 0,096 a 0,203 | **+0,210** | 0,134 a 0,283 | 1,72 × 10⁻⁷ |
| gpt-5-mini | Agentic − Sin RAG | **+0,513** | 0,455 a 0,562 | **+0,630** | 0,564 a 0,680 | 9,42 × 10⁻⁵⁴ |
| gpt-5-mini | RAG − Sin RAG | **+0,363** | 0,304 a 0,417 | **+0,420** | 0,343 a 0,488 | 7,83 × 10⁻²⁹ |
| gpt-5 | Agentic − RAG | **+0,106** | 0,054 a 0,155 | **+0,146** | 0,074 a 0,216 | 1,03 × 10⁻⁴ |
| gpt-5 | Agentic − Sin RAG | **+0,095** | 0,046 a 0,146 | **+0,130** | 0,063 a 0,202 | 4,82 × 10⁻⁴ |
| gpt-5 | RAG − Sin RAG | −0,011 | −0,063 a 0,044 | −0,016 | −0,089 a 0,062 | 0,724 |

### 3.6 Texto propuesto para “Sensibilidad”

> La celda Agentic-RAG + gpt-5-nano concentra 41 de las 79 respuestas no sustantivas. Bajo el escenario principal, su media es 0,395 y su mediana 0,000; bajo exclusión, la media asciende a 0,820 y la mediana a 0,958, pero solo sobre 38 unidades. La diferencia Agentic-RAG − RAG básico pasa de −0,270 (IC 95% −0,330 a −0,202) con fallo = 0 a +0,216 (IC 95% 0,146 a 0,279) con exclusión. No se trata de dos estimaciones contradictorias: la primera mide la utilidad del sistema completo y la segunda la calidad condicional a que el sistema responda. El manuscrito debe reportar ambas y no elegir una sola como “el efecto” de Agentic-RAG.

### 3.7 Reemplazo de “Fortalezas” y “Debilidades”

**Fortalezas (línea 410 y siguientes):** reemplazar “El RAG básico presenta un efecto igualador…” por:

> El análisis apareado muestra que el efecto de la estrategia depende del modelo del especialista y que la interacción es robusta al tratamiento de las respuestas no sustantivas. La combinación Agentic-RAG + gpt-5-mini mejora frente a RAG básico, mientras que gpt-5-nano presenta un aumento de la tasa de fallos. La calidad de las respuestas sustantivas de nano Agentic-RAG es alta, lo que separa el problema de fiabilidad del de calidad condicional.

**Debilidades (línea 417 y siguientes):** agregar:

> La principal limitación del análisis es que existe una sola ejecución por unidad y configuración. El modelo ordinal mixto separa la variabilidad entre unidades y casos, pero no puede estimar la variabilidad entre corridas ni separar el efecto de la estrategia de la variabilidad del proveedor. Además, la imputación a cero de las respuestas no sustantivas es una decisión normativa sobre la utilidad del sistema, no una medición de calidad jurídica; por eso se reportan escenarios alternativos.

### 3.8 Reemplazo de la conclusión del capítulo (línea 435)

> El análisis apareado confirma una interacción fuerte entre estrategia y modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). Bajo el escenario principal, Agentic-RAG reduce el desempeño de gpt-5-nano frente a RAG básico (−0,270; IC 95% −0,330 a −0,202), lo aumenta en gpt-5-mini (+0,150; 0,096 a 0,203) y en gpt-5 (+0,106; 0,054 a 0,155). RAG básico no se distingue de Sin RAG en gpt-5 ni en nano; en mini, RAG básico supera a Sin RAG. La afirmación de que “el RAG básico iguala a los modelos” no se sostiene: hay diferencias pequeñas y algunas comparaciones limítrofes, pero no una equivalencia demostrada. La afirmación de que “en gpt-5 no hay diferencias” también debe corregirse: la diferencia Agentic-RAG − RAG básico es positiva y significativa, aunque menor que en mini.

---

## 4. Conclusiones (`09_capitulo_08_conclusion_y_trabajos_futuros.typ`)

### 4.1 Reemplazo del bullet “Efecto igualador del RAG básico” (línea 31)

> **Ausencia de un efecto igualador demostrado.** Con RAG básico, las diferencias entre modelos se reducen en algunas comparaciones, pero no desaparecen. En el escenario principal, gpt-5-mini supera a gpt-5-nano (+0,063; IC 95% 0,005 a 0,119) y gpt-5 supera a ambos; la comparación gpt-5 − gpt-5-mini es limítrofe y no permite afirmar equivalencia. La conclusión anterior basada en un p de Kruskal–Wallis no significativo (p = 0,095) debe retirarse: la ausencia de significación no demuestra equivalencia.

### 4.2 Reemplazo del bullet “Sobrecarga agéntica” (línea 33)

> **Aumento de fallos en Agentic-RAG con gpt-5-nano.** En el escenario principal, Agentic-RAG + gpt-5-nano obtiene una media de 0,395 y una mediana de 0,000; 41 de 79 unidades no reciben una respuesta sustantiva. La diferencia frente a RAG básico es −0,270 (IC 95% −0,330 a −0,202). Cuando produce una respuesta sustantiva, la calidad es alta (media 0,820; mediana 0,958; n = 38), de modo que el patrón debe describirse como un problema de fiabilidad del sistema completo. No se atribuye a la “complejidad agéntica” como causa: no hay réplicas ni ablación, y el recuperador está fijo en gpt-5.

### 4.3 Reemplazo del bullet “Análisis estadístico riguroso” (línea 63)

> **Análisis inferencial adecuado al diseño.** El uso de un modelo ordinal mixto con interceptos aleatorios por caso y unidad, junto con pruebas pareadas de Friedman/Wilcoxon y bootstrap por casos, respeta el apareamiento y el anidamiento del diseño. Los efectos simples se corrigen con Holm dentro de familias predefinidas y se reportan con IC. Esta especificación reemplaza el uso de pruebas para muestras independientes (Kruskal–Wallis, Dunn, Mann–Whitney, Scheirer–Ray–Hare) como sustento principal.

### 4.4 Reemplazo del párrafo de “Reflexiones finales” (línea 138)

> El hallazgo de interacción entre estrategia y modelo del especialista se mantiene, pero su interpretación es condicional. Bajo el escenario principal, Agentic-RAG perjudica a gpt-5-nano, beneficia a gpt-5-mini y beneficia moderadamente a gpt-5. La diferencia en gpt-5 es positiva y significativa, aunque menor que en mini; la conclusión anterior de “sin diferencias en gpt-5” no se sostiene con el análisis apareado. El patrón de nano se explica por una alta tasa de respuestas no sustantivas, no por una degradación uniforme de la calidad. Estos resultados son específicos de la configuración evaluada —recuperador gpt-5, una ejecución por celda, un corpus y 25 casos— y no deben presentarse como transferibles sin validación externa.

### 4.5 Limitaciones a agregar

Agregar a la lista de limitaciones (después de la limitación de validación manual o junto a ella):

> **Análisis inferencial y variabilidad entre corridas.** El modelo ordinal mixto permite separar la variabilidad entre unidades y casos, pero no la variabilidad entre ejecuciones del mismo modelo. Como se realizó una sola ejecución por unidad y configuración, los efectos estimados no permiten afirmar estabilidad entre corridas ni separar el efecto de la estrategia de la variabilidad del proveedor. Las réplicas y la sustitución controlada del recuperador quedan como trabajo futuro (IX.2.4).

> **Tratamiento de las respuestas no sustantivas.** El escenario principal imputa cero a las respuestas no sustantivas porque miden la utilidad del sistema completo; la exclusión mide la calidad condicional a que el sistema responda. Ambas métricas son informativas y no deben confundirse. La clasificación automática debe confirmarse con la revisión manual ciega antes de la versión definitiva.

---

## 5. Tablas y figuras: nombres propuestos

| Elemento | Nombre propuesto | Fuente |
|---|---|---|
| Tabla de celdas | `tabla-analisis-celdas` | `salidas/30_tabla_celdas_principal.csv` |
| Tabla de efectos de estrategia | `tabla-analisis-efectos-estrategia` | `salidas/31_efectos_simples_orientados.csv` |
| Tabla de efectos de modelo | `tabla-analisis-efectos-modelo` | `salidas/31_efectos_simples_orientados.csv` |
| Figura de interacción | `fig-analisis-interaccion` | `figuras/02_interaccion_prob_ge_075.pdf` |
| Figura de sensibilidad | `fig-analisis-sensibilidad` | `figuras/04_sensibilidad_escenarios.pdf` |
| Figura de efectos simples | `fig-analisis-forest` | `figuras/03_efectos_simples_probabilidad.pdf` |

Al copiar las figuras a `manuscrito/media/`, usar nombres nuevos y no sobrescribir las figuras históricas hasta actualizar sus referencias.

---

## 6. Frases que deben buscarse y corregirse

| Frase o idea | Ubicación | Acción |
|---|---|---|
| “unidades de evaluación independientes” | `06_capitulo_05_metodologia.typ:539` | Reemplazar por “unidades de evaluación” o “unidades apareadas” |
| “temperatura 0 para garantizar reproducibilidad” | `07_capitulo_06_evaluacion.typ:16` | Corregir según IX.1.3; no atribuir determinismo |
| “Kruskal-Wallis”, “Dunn”, “Mann-Whitney”, “Scheirer-Ray-Hare” como análisis principal | `07...:75-265`; `09...:63` | Reemplazar por modelo ordinal mixto y análisis pareado; mover lo anterior a anexo si se conserva |
| “efecto igualador del RAG básico” | `07...:131, 265, 414`; `09...:31` | Eliminar o reformular como “diferencias reducidas, no equivalencia” |
| “sobrecarga agéntica” como causa | `09...:33, 83, 101`; `07...` | Reformular como tasa de fallo observada y calidad condicional; no causal |
| “para gpt-5 no se detectan diferencias significativas” | `07...:424, 435`; `09...:138` | Corregir: hay diferencia positiva Agentic-RAG − RAG básico |
| “n = 79 observaciones por celda” sin desglose | `07...:424` | Aclarar 79 unidades, 2.133 evaluaciones, 653 en exclusión |
| “resultado transferible a otros dominios” | `09...:138` | Sustituir por hipótesis de transferibilidad |
| “LLM-as-a-Judge validado” | `09...` y README | Cambiar por “acuerdo entre jueces”; la validez humana es otra corrección |

---

## 7. Nota sobre el orden de edición

1. Cerrar la revisión manual de la corrección 02.
2. Ejecutar `run_all.sh` y confirmar que las cifras de este documento siguen vigentes.
3. Editar metodología y evaluación.
4. Editar resumen y conclusiones.
5. Actualizar tablas, figuras y referencias cruzadas.
6. Compilar y buscar las frases de la sección 6.

No editar primero las conclusiones: dependen de que el análisis y la clasificación estén cerrados.

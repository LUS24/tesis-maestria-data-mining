# Informe de análisis estadístico inferencial — IX.1.1

**Corrección:** IX.1.1 — corregir el análisis inferencial para respetar el apareamiento por unidad y el anidamiento en casos.  
**Fecha:** 2026-11-12.  
**Insumos:** 711 observaciones, 79 unidades, 25 casos y 2.133 evaluaciones juez-observación.  
**Estado:** análisis ejecutado con la clasificación final de la revisión manual completa (87/87). No hubo cambios de categoría respecto de la clasificación automática en las 711 observaciones.

---

## 1. Qué cambia respecto del análisis anterior

El manuscrito trataba las 711 observaciones como muestras independientes y aplicaba Kruskal–Wallis, Dunn, Mann–Whitney y Scheirer–Ray–Hare. Esos procedimientos no respetan que:

1. las mismas 79 unidades se responden en las nueve configuraciones;
2. las unidades están anidadas en 25 casos;
3. cada respuesta tiene tres evaluaciones de jueces.

El análisis estadístico usa un **modelo ordinal mixto** con interceptos aleatorios por caso y por unidad, y complementa con pruebas pareadas de Friedman/Wilcoxon y bootstrap por casos. La variable ordinal es el puntaje de rúbrica de cada juez.

Además, se corrigió el problema de join documentado en la corrección 02: las unidades 23, 24 y 25 tienen subpregunta vacía en la tabla de métricas y `0` en la de jueces. Eso producía 27 medias ausentes; no eran 27 fallos de generación. La base nueva recupera las 711 observaciones y las 2.133 evaluaciones.

---

## 2. Base analítica y escenarios

| Elemento | Valor |
|---|---:|
| Observaciones unidad × estrategia × modelo | 711 |
| Unidades | 79 |
| Casos | 25 |
| Evaluaciones juez-observación | 2.133 |
| Respuestas no sustantivas (clasificación final) | 57 |
| Respuestas sustantivas | 654 |
| Celdas | 9 |

La clasificación final de la corrección 02 identifica 57 respuestas no sustantivas. La celda Agentic-RAG + gpt-5-nano concentra 41: 27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas. Las otras 16 se distribuyen principalmente en Sin RAG + gpt-5-mini (14 abstenciones).

La revisión manual ciega está **completa** (87/87) y `datos/00_estado_revision_manual.json` lo registra. `build_dataset.py` usó las categorías revisadas; no hubo cambios de categoría respecto de la clasificación automática en las 711 observaciones. No se editan tablas a mano: cualquier cambio futuro en la plantilla exige volver a ejecutar el pipeline.

### 2.1 Escenario principal

El escenario principal asigna **0 en las tres evaluaciones** a toda respuesta no sustantiva. Las respuestas sustantivas conservan el puntaje de rúbrica de cada juez.

Esta no es una decisión “neutra”: representa la utilidad del sistema completo. Un usuario que recibe una cadena vacía, un mensaje de proceso o una abstención no obtiene una respuesta utilizable, aunque un juez haya puntuado el texto con un valor distinto de cero. Por eso el escenario principal es el de fallo = 0, y los demás son sensibilidad.

### 2.2 Escenarios de sensibilidad

| Escenario | Definición | Pregunta que responde |
|---|---|---|
| Principal | No sustantivas = 0 | ¿Qué utilidad tiene el sistema completo? |
| Observado | Puntajes originales de los jueces | ¿Qué cambia si se conservan los puntajes asignados a textos no sustantivos? |
| Exclusión | Solo respuestas sustantivas | ¿Qué calidad tienen las respuestas cuando el sistema responde? |
| Solo fallos técnicos = 0 | Vacías/espacios/errores/truncadas/indeterminadas = 0; abstenciones observadas | ¿Cuánto depende del tratamiento de las abstenciones? |

La exclusión es una submuestra seleccionada y no debe interpretarse como el efecto causal de Agentic-RAG. El escenario principal y la exclusión responden preguntas distintas.

---

## 3. Modelo ordinal mixto

### 3.1 Especificación

```text
score_respuesta_correcta ~ estrategia * modelo_especialista
                           + juez
                           + (1 | caso)
                           + (1 | unidad)
```

- Enlace logit, umbrales flexibles.
- `unidad` es globalmente única; junto con `caso` representa el anidamiento.
- `juez` es efecto fijo.
- La interacción se contrasta con una prueba de razón de verosimilitud entre el modelo completo y el modelo sin la interacción (4 grados de libertad).
- `ordinal::clmm`, `nAGQ = 1`, `Hess = TRUE`. El modelo principal converge (convergencia 0, 71 iteraciones).

### 3.2 Interacción

| Escenario | LR | gl | p | AIC completo | AIC reducido | Var(caso) | Var(unidad) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Principal: no sustantivas = 0 | 293,00 | 4 | 3,50 × 10⁻⁶² | 5525,3 | 5810,3 | 0,164 | 1,383 |
| Observado | 266,68 | 4 | 1,66 × 10⁻⁵⁶ | 5543,3 | 5802,0 | 0,158 | 1,373 |
| Exclusión | 86,82 | 4 | 6,24 × 10⁻¹⁸ | 4959,0 | 5037,9 | 0,216 | 1,394 |
| Solo fallos técnicos = 0 | 286,12 | 4 | 1,07 × 10⁻⁶⁰ | 5532,0 | 5810,1 | 0,166 | 1,383 |

La interacción es muy fuerte en todos los escenarios. Pero la dirección de algunos efectos simples **no es estable**: depende de si las respuestas no sustantivas se imputan a 0 o se excluyen. Esa es la razón por la que el manuscrito no debe presentar una única conclusión causal sobre “Agentic-RAG”.

### 3.3 Predicciones por celda

Las predicciones son poblacionales: efectos aleatorios en cero y promedio sobre los tres jueces. No son los promedios observados de la tabla descriptiva.

| Estrategia | Modelo | Media esperada | IC 95% | P(≥ 0,75) | IC 95% |
|---|---|---:|---:|---:|---:|
| Sin RAG | gpt-5-nano | 0,588 | 0,518–0,660 | 0,452 | 0,362–0,551 |
| Sin RAG | gpt-5-mini | 0,316 | 0,254–0,384 | 0,158 | 0,112–0,219 |
| Sin RAG | gpt-5 | 0,755 | 0,690–0,812 | 0,685 | 0,592–0,766 |
| RAG básico | gpt-5-nano | 0,616 | 0,544–0,685 | 0,490 | 0,393–0,588 |
| RAG básico | gpt-5-mini | 0,678 | 0,610–0,742 | 0,577 | 0,479–0,670 |
| RAG básico | gpt-5 | 0,744 | 0,678–0,803 | 0,670 | 0,576–0,753 |
| Agentic-RAG | gpt-5-nano | 0,345 | 0,277–0,422 | 0,182 | 0,127–0,254 |
| Agentic-RAG | gpt-5-mini | 0,828 | 0,771–0,873 | 0,787 | 0,707–0,847 |
| Agentic-RAG | gpt-5 | 0,850 | 0,798–0,891 | 0,816 | 0,743–0,870 |

La predicción de Agentic-RAG + nano (0,345) es menor que la descriptiva observada (0,395) porque el modelo poblacional no incorpora los efectos aleatorios de las unidades concretas. La conclusión cualitativa es la misma: la celda tiene una masa importante de puntajes cero.

### 3.4 Efectos simples de estrategia dentro de modelo

Diferencias orientadas como `Agentic-RAG − RAG básico`, `Agentic-RAG − Sin RAG` y `RAG básico − Sin RAG`. IC 95% por simulación de los coeficientes y umbrales.

| Modelo | Contraste | Diferencia media | IC 95% | Diferencia P(≥ 0,75) | IC 95% |
|---|---|---:|---:|---:|---:|
| gpt-5-nano | Agentic-RAG − RAG básico | **−0,270** | −0,330 a −0,203 | **−0,308** | −0,382 a −0,224 |
| gpt-5-nano | Agentic-RAG − Sin RAG | **−0,243** | −0,307 a −0,177 | **−0,271** | −0,348 a −0,193 |
| gpt-5-nano | RAG básico − Sin RAG | 0,027 | −0,032 a 0,086 | 0,037 | −0,042 a 0,116 |
| gpt-5-mini | Agentic-RAG − RAG básico | **+0,150** | 0,097 a 0,203 | **+0,210** | 0,135 a 0,283 |
| gpt-5-mini | Agentic-RAG − Sin RAG | **+0,512** | 0,453 a 0,562 | **+0,629** | 0,563 a 0,680 |
| gpt-5-mini | RAG básico − Sin RAG | **+0,362** | 0,302 a 0,417 | **+0,419** | 0,341 a 0,487 |
| gpt-5 | Agentic-RAG − RAG básico | **+0,106** | 0,054 a 0,157 | **+0,146** | 0,075 a 0,218 |
| gpt-5 | Agentic-RAG − Sin RAG | **+0,095** | 0,045 a 0,145 | **+0,130** | 0,062 a 0,201 |
| gpt-5 | RAG básico − Sin RAG | −0,011 | −0,063 a 0,043 | −0,016 | −0,089 a 0,060 |

En escala latente, los contrastes equivalentes tienen p de Holm:

| Contraste | p Holm |
|---|---:|
| nano: Agentic-RAG − RAG básico | 3,07 × 10⁻¹⁴ |
| nano: Agentic-RAG − Sin RAG | 1,11 × 10⁻¹¹ |
| nano: RAG básico − Sin RAG | 0,726 |
| mini: Agentic-RAG − RAG básico | 1,70 × 10⁻⁷ |
| mini: Agentic-RAG − Sin RAG | 1,16 × 10⁻⁵³ |
| mini: RAG básico − Sin RAG | 9,74 × 10⁻²⁹ |
| gpt-5: Agentic-RAG − RAG básico | 1,02 × 10⁻⁴ |
| gpt-5: Agentic-RAG − Sin RAG | 4,78 × 10⁻⁴ |
| gpt-5: RAG básico − Sin RAG | 0,726 |

**Cambio importante:** con el modelo apareado, gpt-5 **sí** muestra una diferencia Agentic-RAG − RAG básico (p Holm = 0,0001; diferencia media +0,106). El manuscrito anterior concluía que en gpt-5 no había diferencias tras Holm. Esa conclusión debe corregirse: la diferencia es menor que en mini, pero no nula.

### 3.5 Efectos simples de modelo dentro de estrategia

Diferencias orientadas como `gpt-5-mini − nano`, `gpt-5 − nano` y `gpt-5 − mini`.

| Estrategia | Contraste | Diferencia media | IC 95% | Diferencia P(≥ 0,75) | IC 95% |
|---|---|---:|---:|---:|---:|
| Sin RAG | mini − nano | **−0,272** | −0,325 a −0,212 | **−0,294** | −0,366 a −0,221 |
| Sin RAG | gpt-5 − nano | **+0,167** | 0,108 a 0,224 | **+0,233** | 0,150 a 0,309 |
| Sin RAG | gpt-5 − mini | **+0,438** | 0,379 a 0,491 | **+0,527** | 0,451 a 0,589 |
| RAG básico | mini − nano | **+0,063** | 0,005 a 0,119 | **+0,088** | 0,008 a 0,165 |
| RAG básico | gpt-5 − nano | **+0,128** | 0,071 a 0,186 | **+0,180** | 0,100 a 0,259 |
| RAG básico | gpt-5 − mini | **+0,065** | 0,011 a 0,124 | **+0,093** | 0,016 a 0,174 |
| Agentic-RAG | mini − nano | **+0,483** | 0,419 a 0,539 | **+0,605** | 0,533 a 0,662 |
| Agentic-RAG | gpt-5 − nano | **+0,504** | 0,440 a 0,560 | **+0,634** | 0,566 a 0,687 |
| Agentic-RAG | gpt-5 − mini | +0,021 | −0,023 a 0,067 | +0,029 | −0,031 a 0,091 |

Los contrastes de RAG básico mini − nano y gpt-5 − mini son **limítrofes**: sus IC de diferencia de media excluyen 0 por poco, pero el p de Holm en escala latente es 0,067 y 0,064, respectivamente. En Wilcoxon, mini − nano es significativo (p Holm = 0,0388) y gpt-5 − mini no lo es (0,0768). La evidencia es limítrofe y no debe presentarse como equivalencia ni como diferencia fuerte. En Agentic-RAG, gpt-5 y mini son indistinguibles; nano está muy por debajo.

---

## 4. Análisis no paramétrico apareado

### 4.1 Friedman

| Familia | Bloque | χ² | gl | p | W de Kendall |
|---|---|---:|---:|---:|---:|
| Estrategia dentro de modelo | gpt-5-nano | 12,05 | 2 | 0,00242 | 0,076 |
| Estrategia dentro de modelo | gpt-5-mini | 54,81 | 2 | 1,25 × 10⁻¹² | 0,347 |
| Estrategia dentro de modelo | gpt-5 | 12,88 | 2 | 0,00159 | 0,082 |
| Modelo dentro de estrategia | Sin RAG | 61,24 | 2 | 5,02 × 10⁻¹⁴ | 0,388 |
| Modelo dentro de estrategia | RAG básico | 23,43 | 2 | 8,18 × 10⁻⁶ | 0,148 |
| Modelo dentro de estrategia | Agentic-RAG | 61,19 | 2 | 5,15 × 10⁻¹⁴ | 0,387 |

El acuerdo de ranking es fuerte en mini y en la comparación de modelos; es más débil en nano y gpt-5, donde el efecto de la estrategia es menor en términos de rangos.

### 4.2 Wilcoxon con Holm

Los contrastes principales, orientados de forma intuitiva:

| Modelo | Contraste | n pares | Diferencia media | p Holm | r rango-biserial |
|---|---|---:|---:|---:|---:|
| gpt-5-nano | Agentic-RAG − RAG básico | 79 | −0,205 | 0,00477 | −0,471 |
| gpt-5-nano | Agentic-RAG − Sin RAG | 79 | −0,171 | 0,01055 | −0,423 |
| gpt-5-nano | RAG básico − Sin RAG | 79 | 0,034 | 1,000 | 0,002 |
| gpt-5-mini | Agentic-RAG − RAG básico | 79 | +0,138 | 0,000829 | +0,607 |
| gpt-5-mini | Agentic-RAG − Sin RAG | 79 | +0,462 | 8,60 × 10⁻¹¹ | +0,887 |
| gpt-5-mini | RAG básico − Sin RAG | 79 | +0,324 | 6,65 × 10⁻⁸ | +0,770 |
| gpt-5 | Agentic-RAG − RAG básico | 79 | +0,105 | 0,0116 | +0,493 |
| gpt-5 | Agentic-RAG − Sin RAG | 79 | +0,088 | 0,0306 | +0,381 |
| gpt-5 | RAG básico − Sin RAG | 79 | −0,018 | 1,000 | −0,051 |

Los signos y la significación coinciden cualitativamente con el modelo ordinal: Agentic-RAG perjudica a nano, beneficia a mini y beneficia moderadamente a gpt-5; RAG básico no se distingue de Sin RAG en gpt-5 ni en nano.

En la comparación de modelos dentro de estrategia, los resultados principales son:

- Sin RAG: las tres comparaciones son significativas; gpt-5 > nano > mini en media, y mini es el peor.
- RAG básico: mini > nano (p Holm = 0,0388), gpt-5 > nano (0,00355), gpt-5 − mini no significativo (0,0768).
- Agentic-RAG: mini > nano (4,19 × 10⁻⁸), gpt-5 > nano (6,89 × 10⁻⁸), gpt-5 − mini no significativo (0,314).

La tabla completa está en `salidas/34_wilcoxon_principal.csv`; incluye IC bootstrap por casos.

---

## 5. Sensibilidad al tratamiento de respuestas no sustantivas

### 5.1 La celda nano Agentic-RAG

| Escenario | n | Media | Mediana | P(≥ 0,75) | IC 95% media |
|---|---:|---:|---:|---:|---:|
| Principal: no sustantivas = 0 | 79 | 0,395 | 0,000 | 0,342 | 0,278–0,517 |
| Observado (rúbrica) | 79 | 0,415 | 0,250 | 0,342 | 0,308–0,530 |
| Exclusión | 38 | 0,820 | 0,958 | 0,711 | 0,720–0,898 |
| Solo fallos técnicos = 0 | 79 | 0,395 | 0,000 | 0,342 | 0,281–0,518 |

La media del escenario principal (0,395) y la observada (0,415) son parecidas porque los jueces ya habían puntuado bajo la mayoría de las salidas no sustantivas. La **mediana** sí cambia: 0,000 versus 0,250. La exclusión muestra que, cuando nano Agentic-RAG produce una respuesta sustantiva, la calidad es alta (media 0,820; mediana 0,958), pero solo lo hace en 38/79 unidades.

### 5.2 Reversión del contraste nano Agentic-RAG − RAG básico

| Escenario | Diferencia media | IC 95% | Diferencia P(≥ 0,75) | IC 95% |
|---|---:|---:|---:|---:|
| Principal: no sustantivas = 0 | **−0,270** | −0,330 a −0,203 | **−0,308** | −0,382 a −0,224 |
| Exclusión | **+0,215** | 0,146 a 0,279 | **+0,319** | 0,217 a 0,410 |

Este cambio de signo es el resultado más importante para la redacción. No significa que Agentic-RAG sea “bueno” o “malo” para nano en abstracto. Significa que:

- como **sistema completo**, nano Agentic-RAG falla en 41/79 unidades y queda por debajo de RAG básico;
- entre las unidades en las que **sí responde**, la calidad es alta y supera a RAG básico.

La afirmación “sobrecarga agéntica” debe reemplazarse por una descripción de **tasa de fallo y calidad condicional**. Sin réplicas y sin ablación no se puede atribuir el fallo a la “complejidad” de la arquitectura.

### 5.3 Interacción en los escenarios

La interacción sigue siendo significativa en todos los escenarios (LR 86,8 a 293,0; p < 10⁻¹⁷). Lo que cambia es la interpretación de los efectos simples. El manuscrito debe reportar el escenario principal y, junto a él, la exclusión como sensibilidad; no elegir el escenario que produzca la conclusión más favorable.

---

## 6. Comparación con la Tabla 11 del manuscrito

La Tabla 11 se calculó sobre 76 observaciones por celda (684 en total), no sobre 79, por el join de las unidades 23–25. Al recuperar las 27 medias, cambian cinco de las nueve medianas.

| Estrategia | Modelo | Mediana manuscrito | Mediana 79 observada | Mediana principal (0) | Mediana exclusión | n exclusión |
|---|---|---:|---:|---:|---:|---:|
| Sin RAG | gpt-5-nano | 0,583 | 0,583 | 0,583 | 0,583 | 78 |
| Sin RAG | gpt-5-mini | 0,333 | 0,250 | 0,250 | 0,333 | 65 |
| Sin RAG | gpt-5 | 0,833 | 0,833 | 0,833 | 0,833 | 79 |
| RAG básico | gpt-5-nano | 0,583 | 0,583 | 0,583 | 0,583 | 79 |
| RAG básico | gpt-5-mini | 0,625 | 0,667 | 0,667 | 0,667 | 79 |
| RAG básico | gpt-5 | 0,833 | 0,833 | 0,833 | 0,833 | 79 |
| Agentic-RAG | gpt-5-nano | 0,083 | 0,250 | 0,000 | 0,958 | 38 |
| Agentic-RAG | gpt-5-mini | 0,917 | 1,000 | 1,000 | 1,000 | 78 |
| Agentic-RAG | gpt-5 | 0,958 | 1,000 | 1,000 | 1,000 | 79 |

La tabla completa, con media y P(≥ 0,75), está en `salidas/30_tabla_celdas_principal.csv`. Cualquier tabla del manuscrito que use 76 observaciones por celda debe actualizarse o justificar explícitamente por qué excluye las unidades 23–25.

---

## 7. Sensibilidad por juez

| Juez | n | LR interacción | p | Convergencia |
|---|---:|---:|---:|---:|
| Grok 4.1 Fast | 711 | 100,46 | 7,84 × 10⁻²¹ | 0 |
| DeepSeek V3.1 | 711 | 81,80 | 7,25 × 10⁻¹⁷ | 0 |
| Kimi K2 0905 | 711 | 92,66 | 3,58 × 10⁻¹⁹ | 0 |

La interacción no depende de un solo juez. Las predicciones por juez están en `salidas/25_modelo_por_juez.csv`; las diferencias de severidad se controlan en el modelo principal con `juez` como efecto fijo.

---

## 8. Interpretación para el manuscrito

### 8.1 Lo que sí se puede afirmar

1. Hay una interacción fuerte entre estrategia y modelo del especialista, robusta al tratamiento de respuestas no sustantivas y a los tres jueces.
2. Con el escenario principal:
   - Agentic-RAG perjudica a gpt-5-nano frente a RAG básico y frente a Sin RAG;
   - Agentic-RAG beneficia a gpt-5-mini;
   - Agentic-RAG beneficia moderadamente a gpt-5, y la diferencia con RAG básico es significativa (a diferencia de la conclusión anterior).
3. RAG básico no se distingue de Sin RAG en gpt-5 ni en nano; en mini, RAG básico supera a Sin RAG.
4. En Agentic-RAG, gpt-5 y mini no se distinguen; nano queda muy por debajo en el escenario principal.
5. La calidad condicional de nano Agentic-RAG, cuando responde, es alta; su problema principal es la tasa de respuestas no sustantivas.

### 8.2 Lo que no se puede afirmar

- “El RAG básico elimina las diferencias entre modelos.” No hay equivalencia; hay diferencias pequeñas y algunas comparaciones limítrofes. La afirmación debe reformularse como “no se detectaron diferencias sustanciales en algunas comparaciones, con IC que no permiten afirmar equivalencia”.
- “Agentic-RAG produce sobrecarga agéntica en modelos pequeños” como propiedad causal de la arquitectura. Lo observado es un aumento de fallos en esta configuración, con recuperador gpt-5 y una asimetría de búsquedas 7/6. Sin réplicas ni ablación no se identifica la causa.
- “En gpt-5 no hay diferencias entre estrategias.” El modelo apareado y el Wilcoxon muestran una diferencia positiva de Agentic-RAG frente a RAG básico.
- “Los resultados son transferibles a otros dominios.” El diseño tiene un corpus, 25 casos y una ejecución por celda.
- “LLM-as-a-Judge está validado.” El acuerdo entre jueces no es validez frente a criterio humano.

### 8.3 Redacción sugerida para la conclusión principal

> “Con el Agente de Recuperación fijado en gpt-5, el efecto de la estrategia depende del modelo del Agente Especialista Legal. En el escenario principal —que asigna cero a las respuestas no sustantivas— Agentic-RAG reduce el desempeño de gpt-5-nano frente a RAG básico (diferencia media −0,270; IC 95% −0,330 a −0,203), mientras que lo aumenta en gpt-5-mini (+0,150; IC 95% 0,097 a 0,203) y, en menor medida, en gpt-5 (+0,106; IC 95% 0,054 a 0,157). La interacción es robusta a los escenarios de sensibilidad (LR = 293,0; gl = 4; p = 3,5 × 10⁻⁶²). En gpt-5-nano, la calidad de las respuestas sustantivas es alta (media 0,820; mediana 0,958), pero solo 38 de 79 unidades reciben una respuesta sustantiva; el patrón debe describirse como un problema de fiabilidad y no como una degradación uniforme de la calidad.”

---

## 9. Limitaciones

1. **Una ejecución por celda.** El modelo separa variabilidad entre unidades y casos, pero no variabilidad entre corridas. No se puede afirmar estabilidad de los efectos.
2. **Alcance de la revisión manual.** La revisión manual de la corrección 02 está completa (87/87) y no cambió ninguna categoría respecto de la clasificación automática en las 711 observaciones. El paquete cubre las 57 no sustantivas automáticas y 30 controles, no las 654 respuestas sustantivas; por tanto, corrige falsos positivos y algunos falsos negativos, pero no es un censo de todas las respuestas.
3. **Imputación normativa.** Asignar 0 a una abstención es una decisión sobre la utilidad del sistema, no una medición de calidad jurídica.
4. **Exclusión seleccionada.** Los 38 pares de nano Agentic-RAG no son una muestra aleatoria; la comparación condicional no es causal.
5. **Confundidos de la configuración agéntica.** El recuperador es siempre gpt-5; gpt-5 usó un prompt de recuperación con 7 búsquedas y mini/nano con 6 (corrección 04). El modelo no puede separar capacidad del especialista, capacidad del recuperador y presupuesto de búsqueda.
6. **Escala ordinal.** Cinco niveles y valores fuera de rúbrica transformados al más cercano. El modelo no recupera matices por debajo de ese nivel.
7. **Sin validación humana de los jueces.** El acuerdo inter-juez es confiabilidad, no validez.
8. **Sin prueba formal de odds proporcionales.** Se usa un modelo acumulativo estándar y análisis no paramétrico como sensibilidad; el supuesto se declara.
9. **Pocos casos.** 25 casos y 79 unidades; los IC reflejan esa información. Los efectos grandes son precisos; los moderados no.

---

## 10. Artefactos

| Archivo | Contenido |
|---|---|
| `datos/01_wide_711.csv` | Base ancha con escenarios y categorías |
| `datos/02_long_2133.csv` | Base larga juez-observación |
| `datos/03_resumen_celdas.csv` | Descriptivos por celda |
| `datos/04_comparacion_medianas_manuscrito.csv` | Comparación 76 vs 79 vs escenarios |
| `datos/05_auditoria_join_23_25.csv` | Verificación de las 27 medias recuperadas |
| `salidas/10_resumen_celdas_escenarios.csv` | Descriptivos y bootstrap por escenario |
| `salidas/11_friedman.csv` | Friedman y W de Kendall |
| `salidas/12_wilcoxon_posthoc.csv` | Wilcoxon, Holm, rango-biserial y bootstrap |
| `salidas/20_modelo_interaccion.csv` | Interacción y varianzas |
| `salidas/21_modelo_coeficientes.csv` | Coeficientes y odds ratios |
| `salidas/22_modelo_predicciones_celdas.csv` | Predicciones por celda |
| `salidas/23_efectos_simples_latentes.csv` | Contrastes latentes y Holm |
| `salidas/24_efectos_simples_probabilidad.csv` | Diferencias de media y P≥0,75 |
| `salidas/25_modelo_por_juez.csv` | Sensibilidad por juez |
| `salidas/30_tabla_celdas_principal.csv` | Tabla principal lista para revisión |
| `salidas/31_efectos_simples_orientados.csv` | Efectos en orden intuitivo |
| `salidas/32_tabla_sensibilidad_nano.csv` | Sensibilidad de la celda nano |
| `salidas/35_resultados_clave.json` | Números principales |
| `figuras/01_medias_por_celda_principal.*` | Medias por celda, escenario principal |
| `figuras/02_interaccion_prob_ge_075.*` | Interacción en P(≥ 0,75) |
| `figuras/03_efectos_simples_probabilidad.*` | Forest plot de efectos simples |
| `figuras/04_sensibilidad_escenarios.*` | Sensibilidad a los escenarios |
| `figuras/05_distribucion_puntajes_principal.*` | Distribución de puntajes |
| `propuestas/preview_tablas.pdf` | Previsualización Typst de las tablas principales |
| `GUIA_PRUEBAS_ESTADISTICAS.md` | Guía de pruebas, fórmulas, interpretación, figuras y citas |
| `citas_estadisticas/citas_estadisticas.bib` | Citas estadísticas validadas |

---

## 11. Reproducción

Desde la raíz del repositorio:

```bash
bash analisis-valoracion-jurado/correccion-01-analisis-estadistico/run_all.sh
```

El script reconstruye la base, ejecuta el análisis no paramétrico, ajusta los modelos ordinales y regenera las figuras. No llama a APIs ni modifica archivos fuente.

La revisión manual de la corrección 02 ya está completa. Si se modifica la plantilla, basta con volver a ejecutar `run_all.sh`; `build_dataset.py` detectará el estado y usará las categorías revisadas.

---

## 12. Estado

- [x] Base de 711 observaciones y 2.133 evaluaciones.
- [x] Corrección del join de las 27 medias.
- [x] Modelo ordinal mixto principal.
- [x] Friedman/Wilcoxon y bootstrap por casos.
- [x] Escenarios de sensibilidad.
- [x] Figuras y tablas.
- [x] Revisión manual ciega (corrección 02, 87/87, sin cambios de categoría).
- [ ] Edición del manuscrito (no realizada en esta carpeta).

La decisión editorial principal es **cómo tratar las respuestas no sustantivas**: el escenario principal de este paquete las imputa a 0, porque miden la utilidad del sistema. La exclusión se reporta como análisis condicional. Esa distinción debe quedar explícita en metodología, resultados y limitaciones; no debe presentarse una sola cifra como “el efecto de Agentic-RAG”.

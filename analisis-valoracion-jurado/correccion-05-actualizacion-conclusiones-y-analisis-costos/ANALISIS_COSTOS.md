# Análisis de costos — reemplazo del índice de eficiencia y de la recomendación “costo-eficiente”

**Corrección:** IX.1.5, con evidencia de IX.1.1, IX.1.2 y IX.1.4.  
**Insumo principal:** `correccion-02-diagnostico-gpt-5-nano/salidas/14_dataset_categoria_final.csv` (711 observaciones, 79 unidades por celda, costos registrados).  
**Salida:** tablas y figuras en `datos/`, `salidas/` y `figuras/`.  
**Restricción:** no se modificó ningún archivo fuente ni se actualizaron precios.

## 1. Qué se corrige

El manuscrito define un índice de eficiencia como desempeño dividido por costo normalizado min-max, con un piso artificial de 0,01. Ese piso determina por sí solo el valor de la configuración más barata y hace que el ranking dependa de una constante elegida. Además, la recomendación “Agentic-RAG + gpt-5-mini es la combinación costo-eficiente” no coincide con los costos registrados: esa celda cuesta más por consulta que RAG básico + gpt-5 y que Sin RAG + gpt-5.

Este informe reemplaza el índice por tres análisis directos:

1. costo medio y costo total por celda;
2. costo por respuesta correcta, con umbral principal `puntaje ≥ 0,75` y sensibilidad a 0,50 y 1,00;
3. frontera de Pareto entre costo medio y desempeño medio.

## 2. Método

- **Unidad:** 79 observaciones por celda; 711 en total.
- **Costo:** `costo_total` registrado por observación, suma de generación y recuperación. Son precios históricos del período experimental, no una estimación a precios corrientes.
- **Desempeño principal:** `puntaje_final_fallo_cero`, promedio de los tres jueces después de asignar 0 a las respuestas no sustantivas.
- **Respuesta correcta (definición D-02):** puntaje promedio de los tres jueces ≥ 0,75. Es el nivel “mayormente correcta” de la rúbrica y coincide con el umbral usado en la corrección 01 para `P(≥ 0,75)`. Se reportan también 0,50 y 1,00.
- **Costo por respuesta correcta:** costo total de la celda dividido por la cantidad de observaciones con puntaje ≥ 0,75. Es una razón descriptiva, no una proyección de producción.

> **Definición operativa adoptada (D-02).** “Respuesta correcta” no es una categoría jurídica objetiva: es una operacionalización de la rúbrica. El umbral principal es ≥ 0,75; 0,50 y 1,00 se reportan como sensibilidad. Los nombres internos de columnas (`aceptables_075`, `costo_por_aceptable_075`) y el archivo `costo_por_respuesta_aceptable_umbrales.csv` se conservan por compatibilidad, pero en el texto significan “respuestas correctas” y “costo por respuesta correcta”.
- **Incertidumbre:** IC 95% por bootstrap de casos (25 casos remuestreados con todas sus unidades; 5.000 réplicas; semilla 20261112). Para la tasa de respuestas correctas se reporta además Wilson.
- **Pareto:** una celda domina a otra si cuesta menos o igual y tiene desempeño mayor o igual, con al menos una desigualdad estricta. Se reporta la frecuencia de pertenencia a la frontera bajo bootstrap.

## 3. Costos por celda

| Estrategia | Modelo | Costo medio/consulta (USD) | Costo total (USD) | Media de corrección | Correctas ≥ 0,75 | Tasa de correctas | Costo por respuesta correcta (USD) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Sin RAG | gpt-5-nano | 0,0025 | 0,1981 | 0,565 | 26/79 | 32,9% | 0,0076 |
| Sin RAG | gpt-5-mini | 0,0043 | 0,3395 | 0,325 | 11/79 | 13,9% | 0,0309 |
| Sin RAG | gpt-5 | 0,0478 | 3,7731 | 0,725 | 49/79 | 62,0% | 0,0770 |
| RAG básico | gpt-5-nano | 0,0025 | 0,2011 | 0,599 | 33/79 | 41,8% | **0,0061** |
| RAG básico | gpt-5-mini | 0,0057 | 0,4465 | 0,650 | 38/79 | 48,1% | 0,0117 |
| RAG básico | gpt-5 | 0,0392 | 3,0997 | 0,707 | 52/79 | 65,8% | 0,0596 |
| Agentic-RAG | gpt-5-nano | 0,0447 | 3,5299 | 0,395 | 27/79 | 34,2% | 0,1307 |
| Agentic-RAG | gpt-5-mini | 0,0564 | 4,4530 | 0,788 | 55/79 | 69,6% | 0,0810 |
| Agentic-RAG | gpt-5 | 0,0792 | 6,2530 | 0,812 | 56/79 | 70,9% | 0,1117 |

**Total del experimento:** USD 22,2939.  
**Por estrategia:** Sin RAG USD 4,3107; RAG básico USD 3,7473; Agentic-RAG USD 14,2359.

### Lectura

- El menor costo puntual por respuesta correcta es **RAG básico + gpt-5-nano** (USD 0,0061; IC bootstrap 0,0043–0,0091), seguido por **Sin RAG + gpt-5-nano** (USD 0,0076; IC 0,0058–0,0107) y **RAG básico + gpt-5-mini** (USD 0,0117; IC 0,0088–0,0163). Los IC de las dos primeras se solapan: el orden es descriptivo y no una diferencia formal.
- La media de corrección más alta es **Agentic-RAG + gpt-5** (0,812), pero su costo por respuesta correcta es USD 0,1117, casi 18 veces el de RAG básico + nano.
- **Agentic-RAG + gpt-5-mini** tiene una media de 0,788, no distinguible de Agentic-RAG + gpt-5 (diferencia +0,021; IC 95% −0,023 a 0,066), y cuesta USD 0,0564 frente a USD 0,0792. Es una opción no dominada, pero **no es la más barata**.
- **Agentic-RAG + gpt-5-nano** tiene el peor costo por respuesta correcta (USD 0,1307) porque solo 27/79 observaciones alcanzan el umbral, pese a que su costo medio no es el más alto. El bajo costo por consulta oculta el costo de los fallos.

## 4. Frontera de Pareto

Siete de las nueve configuraciones son no dominadas. La frontera es escalonada: no hay un ganador único.

| Celda | Costo medio (USD) | Media de corrección | Costo por respuesta correcta (USD) | Frecuencia en frontera bootstrap |
| --- | ---: | ---: | ---: | ---: |
| Sin RAG + gpt-5-nano | 0,0025 | 0,565 | 0,0076 | 67,7% |
| RAG básico + gpt-5-nano | 0,0025 | 0,599 | 0,0061 | 76,0% |
| RAG básico + gpt-5-mini | 0,0057 | 0,650 | 0,0117 | 95,0% |
| RAG básico + gpt-5 | 0,0392 | 0,707 | 0,0596 | 94,3% |
| Sin RAG + gpt-5 | 0,0478 | 0,725 | 0,0770 | 65,7% |
| Agentic-RAG + gpt-5-mini | 0,0564 | 0,788 | 0,0810 | 91,9% |
| Agentic-RAG + gpt-5 | 0,0792 | 0,812 | 0,1117 | 69,4% |

**Fuera de la frontera:** Sin RAG + gpt-5-mini (dominada por alternativas más baratas y mejores) y Agentic-RAG + gpt-5-nano (dominada por RAG básico + gpt-5-nano y otras). La frecuencia bootstrap indica que RAG básico + mini y RAG básico + gpt-5 son las posiciones más estables de la frontera; Agentic-RAG + gpt-5 es menos estable, pero sigue siendo no dominada en la estimación puntual.

## 5. Sensibilidad al umbral de “respuesta correcta”

El orden cambia según el umbral, lo que refuerza que no hay una recomendación única sin declarar el objetivo.

| Umbral | Celda más barata por respuesta correcta | Costo por respuesta correcta | Correctas |
| --- | --- | ---: | ---: |
| ≥ 0,50 | Sin RAG + gpt-5-nano | USD 0,0037 | 54/79 |
| ≥ 0,75 | RAG básico + gpt-5-nano (puntual; IC solapado con Sin RAG + nano) | USD 0,0061 | 33/79 |
| = 1,00 | RAG básico + gpt-5-nano | USD 0,0126 | 16/79 |

A umbral 0,50, Sin RAG + nano es más barato por respuesta correcta porque muchas respuestas parciales cuentan. A umbral 0,75 y 1,00, RAG básico + nano pasa al primer lugar. En ningún umbral Agentic-RAG + nano es competitivo por respuesta correcta.

## 6. Verificación de la recomendación anterior

| Comparación | Resultado |
| --- | --- |
| Agentic-RAG + mini vs. RAG básico + gpt-5 | Agentic mini cuesta USD 0,0564; RAG gpt-5 cuesta USD 0,0392. **No es más barato**. |
| Agentic-RAG + mini vs. Sin RAG + gpt-5 | Agentic mini cuesta USD 0,0564; Sin RAG gpt-5 cuesta USD 0,0478. **No es más barato**. |
| Agentic-RAG + mini vs. Agentic-RAG + gpt-5 | Agentic mini cuesta 28,8% menos (USD 0,0564 vs. 0,0792), con media 0,788 vs. 0,812 y diferencia no significativa. **Es una alternativa no dominada**, no una ganga absoluta. |
| Agentic-RAG + nano | Costo por respuesta correcta USD 0,1307, el peor de las nueve celdas. **No recomendable como sistema completo**. |

**Conclusión editorial:** eliminar “Combinación costo-eficiente: Agentic-RAG + gpt-5-mini” y reemplazarla por una recomendación condicional al objetivo. Si se conserva una frase: “Agentic-RAG + gpt-5-mini es una alternativa no dominada para priorizar calidad alta con menor costo que Agentic-RAG + gpt-5; no es la opción más barata por consulta ni por respuesta correcta”.

## 7. Qué no se puede concluir

- No se puede extrapolar a precios actuales ni a otros proveedores: los costos son históricos y corresponden a las tarifas registradas.
- No se puede interpretar el costo por respuesta correcta como costo de producción: no incluye infraestructura, latencia, mantenimiento, interfaz ni costos humanos.
- No se puede afirmar una relación causal entre costo y calidad: la estrategia, el modelo, el recuperador fijo y los prompts están confundidos.
- No se puede usar el umbral 0,75 como “calidad jurídica” universal: es una convención de la rúbrica.
- No se puede afirmar estabilidad entre corridas: hay una ejecución por celda.

## 8. Archivos

| Archivo | Contenido |
| --- | --- |
| `datos/costos_por_celda.csv` | Costos, medias, respuestas correctas, IC y Pareto por celda |
| `datos/costos_por_estrategia.csv` | Agregado por estrategia |
| `datos/costo_por_respuesta_aceptable_umbrales.csv` | Sensibilidad a 0,50 / 0,75 / 1,00 (nombre interno conservado; contenido = respuesta correcta) |
| `datos/frontera_pareto.csv` | Celdas no dominadas |
| `datos/comparacion_recomendacion_anterior.csv` | Celdas implicadas en la recomendación anterior |
| `salidas/resumen_costos.json` | Totales, rankings y verificación de la recomendación |
| `figuras/01_costo_vs_desempenio_pareto.pdf` | Costo vs. desempeño y frontera |
| `figuras/02_costo_por_aceptable.pdf` | Costo por respuesta correcta (nombre interno conservado); no incluye rayas ni frontera de Pareto |
| `scripts/build_cost_analysis.py` | Reproducción del análisis |

La frontera de Pareto se muestra únicamente en `figuras/01_costo_vs_desempenio_pareto.pdf`; la figura 02 es un gráfico de barras de costo por respuesta correcta sin marcas de Pareto.

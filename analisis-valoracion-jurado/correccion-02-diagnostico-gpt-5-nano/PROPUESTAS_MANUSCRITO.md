# Propuestas de cambios en el manuscrito — IX.1.2

Este archivo contiene texto sugerido para revisar antes de editar el manuscrito. No se modificó ningún `.typ`, README ni notebook existente. Las propuestas usan los resultados de `INFORME_DIAGNOSTICO.md` y los artefactos de `salidas/`.

---

## 1. Reemplazo del párrafo sobre las 27 observaciones ausentes

**Archivo:** `manuscrito/capitulos/07_capitulo_06_evaluacion.typ`  
**Sección actual:** “Imputación de Valores Fuera de Rúbrica”  
**Problema:** el texto atribuye las 27 medias ausentes a fallos de generación. La auditoría muestra que son un defecto de join.

### Texto propuesto

```typst
No se eliminaron 27 observaciones por fallos de generación. La auditoría de las claves
de identificación mostró que las 27 medias ausentes correspondían a las unidades 23,
24 y 25 en las nueve configuraciones: en el archivo de métricas la subpregunta figuraba
vacía y en el archivo de evaluaciones figuraba como 0, de modo que el join no las
encontraba. Las 27 respuestas y sus tres evaluaciones de jueces existen. Al normalizar
la clave se recuperaron las 711 observaciones y las 2.133 evaluaciones de jueces
(711 observaciones × 3 jueces). Por lo tanto, la base de análisis contiene 79 unidades
por celda y no 76. Las medianas y los tamaños muestrales de este capítulo deben
recalcularse sobre esa base.
```

### Consecuencia

Reemplazar toda mención a “27 observaciones eliminadas”, “3,8% del total” y “684 observaciones” por la explicación anterior y por los valores recalculados. La tabla `salidas/08_comparacion_medianas_manuscrito.csv` documenta el cambio celda por celda.

---

## 2. Nueva subsección de diagnóstico de la celda nano

**Archivo:** `manuscrito/capitulos/07_capitulo_06_evaluacion.typ`  
**Ubicación sugerida:** después de “Patrón de Interacción” y antes de “Implicaciones para Resultados Previos”.

### Texto propuesto

```typst
=== Diagnóstico de Agentic-RAG con gpt-5-nano

La celda Agentic-RAG con gpt-5-nano requiere una lectura separada. De las 79 unidades,
41 no contienen una respuesta sustantiva: 27 están vacías, una contiene solo espacios,
dos son abstenciones explícitas, una está truncada y diez son indeterminadas (mensajes
de proceso, marcadores de prueba o un mensaje interno). La tasa de salidas no
sustantivas es 51,9% (IC 95% Wilson: 41,1–62,6%). En las otras ocho celdas la tasa es
0% o 1,3%; el fenómeno está concentrado en esta combinación.

Los registros de los agentes permiten descartar varias explicaciones simples. Los 79
logs contienen una llamada a `retrieve_relevant_documents` y al menos una llamada a
`final_result` (77 con una sola y 2 con más de una); el `finish_reason` del Agente
Especialista Legal es `tool_call` en los 79 casos. Las 28 salidas vacías o con solo espacios tienen entre 1 y 12 documentos
seleccionados, entre 2 y 6 búsquedas en el historial y entre 575 y 7.015 tokens de
salida. No hay evidencia de falta de recuperación ni de truncamiento por límite de
tokens. El texto final del `final_result` es vacío, contiene solo espacios o contiene
un marcador no respondido. La causa de esa decisión de salida no puede determinarse
con los logs disponibles.

La celda es heterogénea. Cuando el sistema produjo una respuesta sustantiva (38 de 79
unidades), la media de `respuesta_correcta_avg` fue 0,820 y la mediana 0,958. Cuando se
asigna 0 a las salidas no sustantivas, la media de la celda es 0,395 y la mediana 0,000;
cuando se excluyen esas salidas, la media es 0,820 y la mediana 0,958. Por lo tanto, el
resultado a nivel sistema es inferior al de RAG básico (diferencia media de −0,205 con
fallo = 0), pero la calidad condicional a que el sistema responda es alta (diferencia
media de +0,182 en las 38 unidades con respuesta sustantiva en ambas estrategias). La
segunda comparación usa una submuestra seleccionada y no debe interpretarse como el
efecto causal de la estrategia.

La etiqueta “sobrecarga agéntica” no describe adecuadamente este patrón. No hay
evidencia de que la complejidad del sistema agéntico sea la causa: no se realizaron
ablaciones ni réplicas. La descripción empírica defendible es un *modo de fallo de
respuesta* concentrado en Agentic-RAG con gpt-5-nano, con resultados de calidad alta
cuando el sistema efectivamente responde. La atribución causal a la “complejidad
agéntica” debe retirarse o presentarse como hipótesis no contrastada.
```

### Tabla sugerida

Se puede agregar una tabla como la siguiente, generada desde `salidas/03b_tabla_categorias_ancha.csv`:

```typst
#figure(
  three-line-table(
    columns: (auto, auto, auto, auto, auto, auto, auto, auto),
    [
      | *Estrategia* | *Modelo* | *Sustantivas* | *No sustantivas* | *Vacías / espacios* | *Abstenciones* | *Otras no sust.* | *Tasa no sust. (IC 95%)* |
      | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
      | Sin RAG | gpt-5-nano | 78 | 1 | 0 | 1 | 0 | 1,3% (0,2–6,8) |
      | Sin RAG | gpt-5-mini | 65 | 14 | 0 | 14 | 0 | 17,7% (10,9–27,6) |
      | Sin RAG | gpt-5 | 79 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |
      | RAG básico | gpt-5-nano | 79 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |
      | RAG básico | gpt-5-mini | 79 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |
      | RAG básico | gpt-5 | 79 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |
      | Agentic-RAG | gpt-5-nano | 38 | 41 | 28 | 2 | 11 | 51,9% (41,1–62,6) |
      | Agentic-RAG | gpt-5-mini | 78 | 1 | 0 | 0 | 1 | 1,3% (0,2–6,8) |
      | Agentic-RAG | gpt-5 | 79 | 0 | 0 | 0 | 0 | 0,0% (0,0–4,6) |
    ],
  ),
  caption: [Categorías de respuesta por estrategia y modelo. “Vacías / espacios” incluye cadenas vacías y salidas con solo espacios. “Otras no sust.” incluye truncadas e indeterminadas. La tasa y su IC 95% se calcularon con el método de Wilson sobre 79 unidades por celda.],
) <tabla-diagnostico-respuestas>
```

La tabla completa con las siete categorías está en `salidas/03_conteo_categorias_por_celda.csv`.

### Figura sugerida

`figuras/03_estados_nano_agentic.pdf` muestra el desglose de las 79 salidas de la celda. `figuras/01_composicion_respuestas_por_celda.pdf` muestra la composición de las nueve celdas. `figuras/02_tasas_fallo_por_celda.pdf` muestra las tasas con IC 95%.

---

## 3. Reemplazo de la interpretación de “sobrecarga agéntica”

**Archivo:** `manuscrito/capitulos/07_capitulo_06_evaluacion.typ`  
**Sección actual:** “Patrón de Interacción”, viñeta sobre gpt-5-nano.

### Texto actual (problemático)

> “gpt-5-nano muestra un comportamiento contraintuitivo: su desempeño es peor con Agentic-RAG (0.40) que con RAG básico (0.59), lo que sugiere que el sistema agéntico genera instrucciones y contextos de complejidad excesiva para un modelo de capacidad reducida.”

### Texto propuesto

```typst
+ *gpt-5-nano presenta un modo de fallo de respuesta*: 41 de las 79 salidas no son
  sustantivas, frente a 0 en RAG básico y 1 en sin RAG. Cuando produce una respuesta
  sustantiva (38/79), su calidad es alta (media 0,820; mediana 0,958). La diferencia
  negativa a nivel sistema se explica por las salidas no sustantivas, no por una
  degradación uniforme de las respuestas efectivamente producidas. No corresponde
  atribuir el patrón a una “complejidad excesiva” sin ablaciones ni réplicas.
```

### Texto para la sección de debilidades

Reemplazar:

> “El sistema Agentic-RAG degrada el desempeño de gpt-5-nano frente a RAG básico (0.40 vs. 0.59, p corr. = 0.017), indicando que la complejidad agéntica es excesiva para modelos de capacidad reducida.”

por:

```typst
+ *Modo de fallo en Agentic-RAG con gpt-5-nano.* La celda produjo 41/79 salidas no
  sustantivas (28 vacías o con solo espacios, 10 indeterminadas, 2 abstenciones y 1
  truncada), pese a que los logs registran recuperación y tokens de salida. Cuando
  respondió, la calidad fue alta (38/79; media 0,820; mediana 0,958). El resultado a
  nivel sistema es inferior al de RAG básico bajo el escenario fallo = 0, pero no hay
  evidencia para atribuir el fallo a la “complejidad agéntica”. No se realizaron
  réplicas ni ablaciones.
```

---

## 4. Reemplazo de la contribución “sobrecarga agéntica”

**Archivo:** `manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ`  
**Sección:** “Contribuciones del Trabajo”.

### Texto actual (problemático)

> “Identificación de la sobrecarga agéntica en modelos pequeños. Se documentó que el sistema Agentic-RAG degrada el desempeño de modelos de capacidad reducida…”

### Texto propuesto

```typst
+ *Identificación de un modo de fallo de respuesta en Agentic-RAG con gpt-5-nano.*
  Se documentó que 41 de las 79 salidas de esa celda no fueron sustantivas: 28 vacías
  o con solo espacios, 10 indeterminadas, 2 abstenciones explícitas y 1 truncada. Los
  logs muestran que el Agente Especialista Legal invocó la recuperación y devolvió un
  `final_result` vacío o no respondido, sin evidencia de truncamiento por tokens. La
  interpretación se limita a un modo de fallo observado; no se atribuye a una causa
  única ni se generaliza a otros modelos. Cuando la celda produjo una respuesta
  sustantiva (38/79), su calidad fue alta (media 0,820; mediana 0,958).
```

---

## 5. Reemplazo del resumen

**Archivo:** `manuscrito/capitulos/01_texto_preliminar.typ`

### Texto actual (problemático)

> “El análisis de efectos simples con corrección de Holm-Bonferroni muestra que el RAG básico elimina las diferencias de desempeño entre modelos de distinta capacidad, mientras que Agentic-RAG beneficia significativamente a gpt-5-mini … pero degrada a gpt-5-nano frente a RAG básico (0.08 vs. 0.58, p corr. = 0.017).”

### Texto propuesto

```typst
El análisis de efectos simples con corrección de Holm-Bonferroni muestra que el RAG
básico reduce las diferencias de desempeño entre modelos, mientras que Agentic-RAG
beneficia a gpt-5-mini. En Agentic-RAG con gpt-5-nano se observó un modo de fallo de
respuesta: 41 de las 79 salidas no fueron sustantivas (28 vacías o con solo espacios,
10 indeterminadas, 2 abstenciones y 1 truncada). Cuando esa celda produjo una respuesta
sustantiva (38/79), su calidad fue alta (mediana 0,958). El resultado a nivel sistema
debe reportarse con un escenario de fallo = 0 y no como una degradación uniforme de la
calidad de las respuestas. La atribución causal a la “complejidad agéntica” no se
sostiene con el diseño actual.
```

**Nota:** no conservar los valores `0,08 vs. 0,58` ni `p corr. = 0,017` hasta que el análisis de IX.1.1 se rehaga sobre las 711 observaciones. La mediana 0,083 del manuscrito se calculó sobre 76 filas y no sobre 79.

---

## 6. Ajuste del ejemplo del anexo

**Archivo:** `manuscrito/capitulos/anexo_01.typ`  
**Sección:** “Consultas con Agentic-RAG”.

Agregar después del ejemplo de gpt-5-nano:

```typst
Este ejemplo corresponde a una de las 38 respuestas sustantivas de la celda
Agentic-RAG con gpt-5-nano. No representa las 41 salidas no sustantivas de esa celda
documentadas en el capítulo de evaluación. La ventaja cualitativa que ilustra este
ejemplo no debe generalizarse al conjunto de las 79 unidades.
```

También conviene suavizar la frase “La ventaja del enfoque agéntico se evidencia…” por “Este caso ilustra cómo el enfoque agéntico puede…”, para no convertir un ejemplo seleccionado en una conclusión general.

---

## 7. Actualización de la tabla de medianas

**Archivo:** `manuscrito/capitulos/07_capitulo_06_evaluacion.typ`  
**Tabla:** `<tabla-resumen-medianas>`.

No reutilizar los valores actuales: fueron calculados sobre 76 filas por celda. Opciones:

1. Recalcular la tabla completa desde `salidas/01_dataset_derivado_711.csv` después de definir el escenario principal en IX.1.1.
2. Si se mantiene `respuesta_correcta_avg` con los jueces originales, usar la columna `mediana_corregida_79_jueces_original` de `salidas/08_comparacion_medianas_manuscrito.csv`.
3. Si se adopta fallo = 0 como escenario principal, usar `mediana_fallo_cero`; para Agentic-RAG + nano será `0,000`.
4. Agregar una nota al pie o una fila separada con la mediana condicional a respuestas sustantivas de esa celda: `0,958` con `n = 38`.

Propuesta de nota:

```typst
Las medianas se calcularon sobre 79 unidades por celda. En Agentic-RAG con gpt-5-nano,
41 salidas no son sustantivas; la mediana de 0,000 corresponde al escenario fallo = 0.
La mediana condicional a las 38 respuestas sustantivas es 0,958 y se reporta como
análisis descriptivo, no como efecto causal de la estrategia.
```

---

## 8. Actualización del README

**Archivo:** `README.md`.

Reemplazar la fila:

> “Sobrecarga agéntica en modelos pequeños: Agentic-RAG puede degradar el desempeño de modelos de capacidad reducida.”

por:

> “Modo de fallo en Agentic-RAG + gpt-5-nano: 41/79 salidas no sustantivas (28 vacías o con solo espacios, 10 indeterminadas, 2 abstenciones y 1 truncada). Cuando responde, la calidad es alta (media 0,82; mediana 0,96).”

También conviene aclarar en el README que las cifras de la tabla de hallazgos deben actualizarse después del análisis de IX.1.1 y que las 27 medias ausentes del análisis original eran un problema de join, no 27 fallos de generación.

---

## 9. Actualización de la documentación de `part_g`

**Archivo:** `codigo_experimentos/performed_tasks_summary.md` o el README que corresponda.

El notebook `part_g/02_1_handle_missing_responses.ipynb` concluye que los faltantes son “del mismo modelo” y que el modelo “no es muy confiable” sin diagnóstico causal. La auditoría muestra dos fenómenos distintos:

- 27 medias ausentes por join `vacío` vs. `0` en las unidades 23–25;
- 28 salidas vacías/solo espacios en Agentic-RAG + gpt-5-nano.

Propuesta de nota:

```markdown
Nota de auditoría (IX.1.2): los 27 valores ausentes de `respuesta_correcta_avg` no son
fallos de generación. Corresponden a las unidades 23–25 en las nueve configuraciones y
se producen por la diferencia entre subpregunta vacía y `0` en los archivos de métricas
y jueces. Las 28 salidas vacías/solo espacios de Agentic-RAG + gpt-5-nano son un
fenómeno distinto: el `final_result` del Agente Especialista Legal contiene un texto
vacío o un marcador no respondido, pese a que existen recuperación y tokens de salida.
No debe concluirse que el modelo sea “poco confiable” sin analizar los logs.
```

---

## 10. Respuesta sintética para el jurado

```text
Sobre V.6/IX.1.2: se auditó la celda Agentic-RAG + gpt-5-nano y los faltantes. Las 27
medias ausentes no eran 27 fallos de generación, sino 3 unidades (23, 24 y 25) por 9
configuraciones, no enlazadas por una diferencia entre subpregunta vacía y 0. Al
normalizar la clave se recuperaron 711 observaciones y 2.133 evaluaciones de jueces.
La celda nano contiene 41/79 salidas no sustantivas: 27 vacías, 1 solo espacios, 2
abstenciones, 1 truncada y 10 indeterminadas. Los logs muestran que el agente recuperó
documentos e invocó `final_result`; el texto final fue vacío o un marcador, sin
evidencia de truncamiento por tokens. Cuando produjo una respuesta sustantiva (38/79),
la calidad fue alta (media 0,820; mediana 0,958). El resultado a nivel sistema es
inferior a RAG básico con fallo = 0, pero no hay evidencia para atribuirlo a la
“complejidad agéntica”. Se retiró esa atribución causal y se reportan ambos escenarios.
```

---

## 11. Qué no cambiar todavía

- No editar la tabla de medianas ni las conclusiones hasta que IX.1.1 fije el modelo ordinal mixto y el escenario principal.
- No eliminar `score_precision_legal` del manuscrito solo por este diagnóstico; su tratamiento corresponde a IX.1.1/IX.2.2.
- No afirmar que los jueces son inválidos en general. La auditoría muestra inconsistencias en salidas no sustantivas; la validez global requiere IX.2.3.
- No afirmar que el fallo se debe al modelo, al prompt, al recuperador o a la “agencia” sin réplicas/ablación.
- No usar el ejemplo del anexo como prueba de que Agentic-RAG funciona en todos los casos.

# Protocolo de reanálisis inferencial — IX.1.1

**Estado:** versión ejecutada el 2026-11-12.  
**Objetivo:** reemplazar el análisis que trataba las 711 observaciones como independientes por un análisis que respete (i) el apareamiento de las 79 unidades en las nueve configuraciones, (ii) el anidamiento de las unidades en 25 casos y (iii) las tres evaluaciones por respuesta.

Este documento fija las decisiones **antes** de interpretar los nuevos valores p. Los resultados se reportan en `INFORME_REANALISIS.md`.

## 1. Unidad de análisis y estructura

| Elemento | Definición |
|---|---|
| Caso | 25 escenarios del benchmark (`q = 1..25`) |
| Unidad | 79 subpreguntas/unidades; las preguntas 23–25 son de unidad única |
| Observación | unidad × estrategia × modelo; 711 en total |
| Evaluación | observación × juez; 3 jueces; 2.133 filas |
| Estrategia | sin RAG, RAG básico, Agentic-RAG |
| Modelo | gpt-5-nano, gpt-5-mini, gpt-5; en Agentic-RAG identifica solo al Agente Especialista Legal |

La unidad 23–25 tiene `nro_subpregunta` vacío en la tabla de métricas y `0` en la tabla de jueces. La corrección 02 documentó que esto producía 27 medias ausentes por el join, no 27 fallos de generación. En la base nueva se normaliza a `Q23_00`, `Q24_00`, `Q25_00`, conservando los identificadores originales.

## 2. Variable de respuesta

La variable principal es el puntaje ordinal de `score_respuesta_correcta` de cada juez, con valores `{0, 0.25, 0.5, 0.75, 1}`.

Los valores fuera de rúbrica observados en los registros (por ejemplo, 0.9, 0.85, 0.375) se transforman al valor de rúbrica más cercano; los empates se resuelven hacia el valor mayor, siguiendo la regla ya usada en la corrección 02. La transformación se aplica **por juez** y se conserva el valor original en la tabla larga.

## 3. Escenarios de tratamiento

### 3.1 Principal: respuestas no sustantivas = 0

Toda respuesta clasificada como no sustantiva (`vacia`, `solo_espacios`, `abstencion_explicita`, `error_explicito`, `truncada`, `indeterminada`) recibe puntaje 0 en las tres evaluaciones. Las respuestas sustantivas conservan el puntaje de rúbrica de cada juez.

Este escenario representa la **utilidad del sistema completo**: un usuario que no recibe una respuesta sustantiva no obtiene el servicio, con independencia de que un juez haya puntuado el texto vacío.

### 3.2 Sensibilidad: puntajes observados

Se conservan los puntajes que asignaron los jueces a todas las respuestas, incluidas las no sustantivas. Este escenario permite comparar con la práctica del manuscrito anterior, pero no debe usarse para afirmar calidad cuando el texto está vacío.

### 3.3 Sensibilidad: exclusión

Se excluyen las 57 respuestas no sustantivas y se analizan solo las 654 respuestas sustantivas (1.962 evaluaciones juez-observación). Es una submuestra seleccionada: responde “¿qué calidad tienen las respuestas cuando el sistema responde?”, no “¿qué tan útil es el sistema?”. No se interpreta como efecto causal.

### 3.4 Sensibilidad: solo fallos técnicos = 0

Se asigna 0 a vacías, solo espacios, errores, truncadas e indeterminadas, pero se conservan los puntajes observados de las abstenciones explícitas. Permite separar el efecto de considerar una abstención como fallo del de considerar un fallo técnico.

### 3.5 Revisión manual

La clasificación automática se reemplaza por la clasificación manual cuando la plantilla de la corrección 02 está completa. El programa `build_dataset.py` verifica que las 87 filas tengan categoría válida y justificación; si no, usa la clasificación automática y lo registra en `datos/00_estado_revision_manual.json`. No se mezclan filas manuales y automáticas de manera parcial. El paquete de revisión contiene las 57 respuestas no sustantivas automáticas y 30 controles sustantivos; no es un censo de las 654 respuestas sustantivas, de modo que la revisión manual corrige falsos positivos y algunos falsos negativos, pero no valida por completo la clasificación.

## 4. Modelo principal

Modelo de enlaces acumulativos (cumulative link) con función logit y umbrales flexibles:

```text
score_respuesta_correcta ~ estrategia * modelo_especialista
                           + juez
                           + (1 | caso)
                           + (1 | unidad)
```

- `unidad` es globalmente única; junto con `caso` representa el anidamiento.
- `juez` entra como efecto fijo para controlar la severidad sistemática de los tres evaluadores.
- La interacción se contrasta mediante la comparación de verosimilitud entre el modelo completo y el modelo sin `estrategia:modelo_especialista` (4 grados de libertad).
- Se usa `ordinal::clmm` con `nAGQ = 1` (aproximación de Laplace) y `Hess = TRUE`. Se registran convergencia, iteraciones y varianzas de los efectos aleatorios.
- No se selecciona el modelo según el resultado. Si no converge, el protocolo prevé una simplificación declarada o un modelo bayesiano; no se probaron variantes hasta obtener significación.

### 4.1 Medidas reportadas

1. Coeficientes, errores estándar, z, p y odds ratios con IC 95% (Wald).
2. Predicciones poblacionales por celda: probabilidades de cada nivel, media esperada y `P(score ≥ 0,75)`, con efectos aleatorios en cero y promedio sobre los tres jueces.
3. Efectos simples en escala latente mediante `emmeans`, con IC 95%.
4. Diferencias de media esperada y de `P(score ≥ 0,75)` entre celdas, con IC 95% obtenidos por simulación de 4.000 draws de la distribución asintótica de los coeficientes y umbrales.
5. Modelos separados por juez como sensibilidad.

## 5. Familias de contrastes y corrección

Se definen dos familias de nueve comparaciones simples:

| Familia | Comparaciones |
|---|---|
| Estrategia dentro de modelo | Agentic-RAG − RAG básico; Agentic-RAG − Sin RAG; RAG básico − Sin RAG, para cada uno de los tres modelos |
| Modelo dentro de estrategia | gpt-5-mini − gpt-5-nano; gpt-5 − gpt-5-nano; gpt-5 − gpt-5-mini, para cada una de las tres estrategias |

La corrección de Holm se aplica **dentro de cada familia de nueve**, no sobre todos los 18 contrastes ni sobre un subconjunto elegido después de ver los resultados. Los p de la escala latente y los IC de las diferencias de probabilidad se reportan por separado; no se convierten IC en pruebas de significación.

## 6. Análisis no paramétrico de sensibilidad

Para cada escenario:

- Friedman para las tres estrategias dentro de cada modelo y para los tres modelos dentro de cada estrategia, usando la misma unidad como bloque.
- W de Kendall como tamaño de efecto global.
- Wilcoxon de rangos con signo para los pares, con corrección de Holm dentro de cada familia de nueve.
- Correlación rango-biserial apareada.
- Bootstrap por **casos**: se remuestrean los 25 casos con todas sus unidades, 5.000 réplicas, semilla 20261112. No se remuestrean filas, porque rompería el anidamiento.

Friedman y Wilcoxon no incorporan los efectos aleatorios ni el anidamiento completo; son sensibilidad y se interpretan junto con el modelo ordinal, no como sustituto.

## 7. Reglas de decisión e interpretación

1. El escenario principal es el de no sustantivas = 0.
2. La exclusión y los puntajes observados son sensibilidad, no escenarios intercambiables.
3. No se afirma equivalencia por falta de significación. Se reportan IC y, si se desea equivalencia, se fija un margen antes de la prueba.
4. No se afirma causalidad: hay una ejecución por celda, no réplicas, y el recuperador agéntico está fijo en gpt-5.
5. La asimetría de búsquedas 7/6 entre gpt-5 y mini/nano (corrección 04) se declara como confundido; el modelo no puede separarla de la capacidad del especialista.
6. La validación jurídica de las respuestas esperadas y la validación humana de los jueces pertenecen a otras correcciones y no se infieren de este análisis.
7. Si la revisión manual cambia la categoría de alguna respuesta, se vuelve a ejecutar todo el pipeline; no se editan a mano las tablas de resultados.

## 8. Limitaciones del diseño inferencial

- Una sola ejecución por unidad y celda: el modelo separa variabilidad entre unidades y casos, pero no variabilidad entre corridas.
- 25 casos y 79 unidades: los IC reflejan esa cantidad de información; los efectos grandes pueden ser precisos y los moderados, no.
- La asignación de 0 a las respuestas no sustantivas es una decisión normativa explícita, no una medición.
- Los jueces son automáticos y su acuerdo no demuestra validez frente a criterio humano.
- La rúbrica tiene cinco niveles; el modelo ordinal es adecuado, pero no recupera matices por debajo de esa escala.
- El modelo supone una estructura de umbrales acumulativos; no se realizó una prueba formal de odds proporcionales en el modelo mixto. Se declara como supuesto y se acompaña con análisis no paramétrico.

## 9. Artefactos y trazabilidad

| Archivo | Contenido |
|---|---|
| `datos/01_wide_711.csv` | 711 observaciones con escenarios y categorías |
| `datos/02_long_2133.csv` | 2.133 evaluaciones juez-observación |
| `salidas/10_resumen_celdas_escenarios.csv` | Descriptivos por celda y escenario |
| `salidas/11_friedman.csv` | Friedman y W de Kendall |
| `salidas/12_wilcoxon_posthoc.csv` | Wilcoxon, Holm, rango-biserial y bootstrap |
| `salidas/20_modelo_interaccion.csv` | Interacción y varianzas por escenario |
| `salidas/21_modelo_coeficientes.csv` | Coeficientes y odds ratios |
| `salidas/22_modelo_predicciones_celdas.csv` | Predicciones por celda |
| `salidas/23_efectos_simples_latentes.csv` | Contrastes latentes y Holm |
| `salidas/24_efectos_simples_probabilidad.csv` | Diferencias de media y P≥0,75 |
| `salidas/25_modelo_por_juez.csv` | Sensibilidad por juez |
| `salidas/30_tabla_celdas_principal.csv` | Tabla lista para revisión |
| `salidas/31_efectos_simples_orientados.csv` | Contrastes en orden intuitivo |
| `salidas/35_resultados_clave.json` | Números principales legibles por máquina |

## 10. Reproducción

```bash
bash analisis-valoracion-jurado/correccion-01-reanalisis-inferencial/run_all.sh
```

La instalación de R se documenta en `instalar_dependencias_R.sh`. El entorno Python es el de `codigo_experimentos`; no se requieren llamadas a APIs.

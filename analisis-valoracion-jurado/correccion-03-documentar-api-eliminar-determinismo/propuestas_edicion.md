# Propuestas de edición para IX.1.3

Este archivo es un **borrador de revisión**. No se aplicó ningún cambio al manuscrito ni al README. Las ubicaciones y el texto exacto también están en `salidas/tabla_ubicaciones_texto_a_modificar.csv`.

## 1. Criterio de redacción

La formulación debe distinguir cuatro cosas:

1. lo que el código **solicitó** (`temperature=0.0`);
2. lo que el artefacto **registró** (`{"temperature": 0.0}` o `{}` según la estrategia);
3. lo que la biblioteca **construyó y envió** (sin `temperature`, sin `reasoning_effort`, sin `max_completion_tokens`);
4. lo que el proveedor **aplicó**, que no está documentado en los logs; para el esfuerzo de razonamiento, el default documentado de OpenAI para GPT-5 es `medium`, pero el valor efectivo local no se registró.

No conviene escribir “temperatura 0” como si fuera un control efectivo. Tampoco conviene afirmar un nivel de esfuerzo distinto de `medium`: no se registró el valor efectivo, pero OpenAI documenta `medium` como default para GPT-5.

## 2. Resumen de cambios

| Archivo | Línea | Prioridad | Acción |
| --- | ---: | --- | --- |
| `manuscrito/capitulos/06_capitulo_05_metodologia.typ` | 196 | Obligatoria | Reemplazar la oración sobre “Pydantic AI con temperatura 0”. |
| `manuscrito/capitulos/06_capitulo_05_metodologia.typ` | 461 | Obligatoria | Reemplazar “0,0 = determinista”. |
| `manuscrito/capitulos/06_capitulo_05_metodologia.typ` | 471 | Obligatoria | Rotular la temperatura como solicitada y no aplicada. |
| `manuscrito/capitulos/06_capitulo_05_metodologia.typ` | 495 | Obligatoria | Eliminar “temperatura cero” como criterio de selección. |
| `manuscrito/capitulos/06_capitulo_05_metodologia.typ` | 505 | Obligatoria | Reemplazar “todos configurados con temperatura 0”. |
| `manuscrito/capitulos/06_capitulo_05_metodologia.typ` | 598 | Obligatoria | Separar la configuración de jueces de la de generadores. |
| `manuscrito/capitulos/06_capitulo_05_metodologia.typ` | 644 | Obligatoria | Reemplazar “temperatura 0 evita múltiples ejecuciones”. |
| `manuscrito/capitulos/07_capitulo_06_evaluacion.typ` | 16 | Obligatoria | Reemplazar “garantizar reproducibilidad”. |
| `manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ` | 87 | Obligatoria | Insertar limitación de ejecución única y ausencia de control de muestreo. |
| `codigo_experimentos/performed_tasks_summary.md` | 66 | Obligatoria | Quitar “deterministic responses”. |
| `manuscrito/capitulos/06_capitulo_05_metodologia.typ` | 8 | Recomendada | Distinguir reproducibilidad del pipeline de determinismo. |
| `manuscrito/capitulos/06_capitulo_05_metodologia.typ` | 739 | Recomendada | Misma distinción. |
| `README.md` | 140 | Recomendada | Insertar nota de ejecución única y no determinismo. |

## 3. Reemplazos propuestos

### 3.1 Metodología, línea 196

**Actual**

```typst
Se emplea la misma configuración de agente (Pydantic AI con temperatura 0) que en el baseline sin RAG, para mantener la comparabilidad.
```

**Propuesto**

```typst
Se emplea la misma configuración de agente (Pydantic AI) que en el baseline sin RAG para mantener la comparabilidad. En el código se solicitó `temperature=0.0`, pero la versión 1.1.0 de Pydantic AI elimina ese parámetro para los modelos GPT-5 antes de construir la solicitud; por tanto, no se la presenta como un control efectivo de reproducibilidad.
```

**Motivo:** evita afirmar que la temperatura fue aplicada y conserva la comparabilidad del agente.

### 3.2 Metodología, línea 461

**Actual**

```typst
La temperatura controla la aleatoriedad de las respuestas del modelo (0,0 = determinista).
```

**Propuesto**

```typst
La temperatura es un parámetro de muestreo. En los modelos GPT-5 evaluados, el perfil de Pydantic AI 1.1.0 declara `temperature` como parámetro no admitido y la biblioteca lo elimina antes de construir la solicitud; el valor `0.0` figura en el código y en algunos registros, pero no fue aplicado. El esfuerzo de razonamiento no se registró; Pydantic AI 1.1.0 no define default y OpenAI documenta `medium` para GPT-5.
```

**Motivo:** distingue el valor solicitado del enviado y no presenta el cero como determinismo.

### 3.3 Metodología, tabla de hiperparámetros, línea 471

**Actual**

```typst
| Temperatura                       |                       0,0                        |                        0,0                         |
```

**Propuesto**

```typst
| Temperatura solicitada en el código | 0,0#super[†] | 0,0#super[†] |
```

Agregar al pie de la tabla, después de la nota del modelo del especialista:

```typst
#super[†] El valor fue solicitado en el código, pero Pydantic AI 1.1.0 elimina `temperature` para los modelos GPT-5 antes de construir la solicitud; no fue aplicado.
```

**Motivo:** la tabla deja de atribuir a los agentes un parámetro que no llegó al payload. Si se prefiere una tabla más corta, puede usarse `0,0 (solicitada, no aplicada)` en la celda, pero la nota al pie es más legible.

### 3.4 Metodología, línea 495

**Actual**

```typst
+ Soporte para generación con temperatura cero (respuestas determinísticas).
```

**Propuesto**

Eliminar el ítem. Si se quiere conservar una aclaración, agregar fuera de la lista:

```typst
No se utilizó la temperatura como criterio de selección porque el perfil de Pydantic AI para los modelos GPT-5 no la admite.
```

**Motivo:** no se puede seleccionar un modelo por una capacidad que el perfil de la biblioteca elimina.

### 3.5 Metodología, línea 505

**Actual**

```typst
Todos los modelos fueron configurados con temperatura 0 para maximizar la reproducibilidad de las respuestas.
```

**Propuesto**

```typst
Los tres modelos pertenecen a la familia GPT-5 y fueron invocados con los identificadores `gpt-5-nano`, `gpt-5-mini` y `gpt-5`. El código solicitó `temperature=0.0`, pero Pydantic AI 1.1.0 elimina ese parámetro para estos modelos antes de enviar la solicitud; por tanto, operaron con el comportamiento de muestreo predeterminado del proveedor. No se registró el esfuerzo de razonamiento; el default documentado del proveedor es `medium`. Se realizó una única ejecución por unidad y configuración, sin réplicas.
```

**Motivo:** reemplaza una garantía inexistente por una descripción verificable y agrega la limitación de ejecución única.

### 3.6 Metodología, línea 598 (jueces)

**Actual**

```typst
Los tres modelos fueron configurados con temperatura 0,0 y un límite de 5.000 tokens de salida.
```

**Propuesto**

```typst
Los tres modelos jueces se configuraron en OpenRouter con `temperature=0.0` y un límite de 5.000 tokens de salida. Esa configuración corresponde a los jueces y no debe extrapolarse a los modelos generadores GPT-5, cuyo perfil elimina `temperature`. No se registró el esfuerzo de razonamiento de los jueces.
```

**Motivo:** evita confundir la configuración de los jueces con la de los generadores. El resto del párrafo puede conservarse.

### 3.7 Metodología, línea 644

**Actual**

```typst
+ Temperatura 0 para respuestas determinísticas (evita múltiples ejecuciones).
```

**Propuesto**

```typst
+ Una única ejecución por unidad y configuración, sin réplicas. La temperatura solicitada en el código no fue aplicada por los modelos GPT-5 y no se usa como garantía de determinismo.
```

**Motivo:** la ausencia de réplicas es una decisión de diseño y una limitación, no una consecuencia de la temperatura.

### 3.8 Evaluación, línea 16

**Actual**

```typst
El diseño experimental sigue un esquema factorial 3 × 3 detallado en el capítulo @cap:metodologia (@tabla-diseno-factorial): tres estrategias de recuperación (sin RAG, RAG básico, Agentic-RAG) × tres modelos de lenguaje (gpt-5-nano, gpt-5-mini, gpt-5), con temperatura 0 en todas las configuraciones para garantizar reproducibilidad.
```

**Propuesto**

```typst
El diseño experimental sigue un esquema factorial 3 × 3 detallado en el capítulo @cap:metodologia (@tabla-diseno-factorial): tres estrategias de recuperación (sin RAG, RAG básico, Agentic-RAG) × tres modelos de lenguaje (gpt-5-nano, gpt-5-mini, gpt-5), con una única ejecución por unidad y configuración. El código solicitó `temperature=0.0`, pero el perfil de Pydantic AI para los modelos GPT-5 no admite ese parámetro y la biblioteca lo elimina antes de la solicitud; por tanto, la configuración no garantiza determinismo ni reproducibilidad exacta.
```

**Motivo:** alinea evaluación con metodología y elimina la garantía de reproducibilidad.

### 3.9 `performed_tasks_summary.md`, línea 66

**Actual**

```text
Uses Pydantic AI agents with temperature=0 for deterministic responses.
```

**Propuesto**

```text
Uses Pydantic AI agents; the code requested `temperature=0`, but Pydantic AI 1.1.0 removes this setting for GPT-5 reasoning models. Responses are not assumed deterministic.
```

**Motivo:** la documentación de experimentos no debe afirmar determinismo.

### 3.10 Metodología, línea 8 (recomendada)

**Actual**

```typst
La implementación se organizó en módulos independientes ejecutados como notebooks de Jupyter, lo que favorece la reproducibilidad y la iteración.
```

**Propuesto**

```typst
La implementación se organizó en módulos independientes ejecutados como notebooks de Jupyter, lo que favorece la auditabilidad y la iteración sobre los artefactos; la reproducibilidad de las respuestas no está garantizada por la configuración de muestreo.
```

**Motivo:** “reproducibilidad” puede leerse como reproducibilidad exacta de las respuestas.

### 3.11 Metodología, línea 739 (recomendada)

**Actual**

```typst
La organización modular en notebooks independientes facilita la reproducibilidad y permite iterar sobre componentes específicos sin afectar al resto del sistema.
```

**Propuesto**

```typst
La organización modular en notebooks independientes facilita la reproducción del pipeline y la auditoría de los artefactos; no implica reproducibilidad exacta de las respuestas.
```

**Motivo:** igual que el anterior.

### 3.12 README, después de la línea 140 (recomendada)

**Insertar**

```markdown
> **Nota metodológica:** se realizó una única ejecución por unidad y configuración. El código solicitó `temperature=0.0`, pero Pydantic AI 1.1.0 elimina ese parámetro para los modelos GPT-5; por tanto, las respuestas no se consideran deterministas. Los análisis deben respetar el apareamiento por unidad y el anidamiento en casos.
```

**Motivo:** el README describe el diseño experimental sin advertir la ejecución única.

## 4. Tabla de hiperparámetros propuesta

Una versión completa de la tabla, coherente con el texto:

```typst
#figure(
  three-line-table(
    columns: (5cm, auto, auto),
    [
      | *Parámetro*                       |           *Agente Especialista Legal*            |              *Agente de Recuperación*              |
      | :-------------------------------- | :----------------------------------------------: | :------------------------------------------------: |
      | Temperatura solicitada en el código | 0,0#super[†] | 0,0#super[†] |
      | Límite de llamadas a herramientas |                        1                         |                         6                          |
      | Herramienta disponible            | #text(size: 10pt)[`retrieve_relevant_documents`] | #text(size: 10pt)[`cosine_distance_vector_search`] |
      | Máx. subconsultas por consulta    |                        —                         |                         3                          |
      | Modelo por defecto                |                Variable#super[‡]                 |                       gpt-5                        |
    ],
  ),
  caption: [Hiperparámetros de configuración de los agentes activos del sistema Agentic-RAG. #super[†]El valor fue solicitado en el código, pero Pydantic AI 1.1.0 elimina `temperature` para los modelos GPT-5 antes de construir la solicitud; no fue aplicado. #super[‡]El modelo del Agente Especialista Legal varía según la configuración experimental (gpt-5-nano, gpt-5-mini o gpt-5).],
) <tabla-hiperparametros-agentes>
```

**Nota:** la tabla actual usa `#super[†]` para el modelo variable. Si se introduce un segundo símbolo, hay que revisar que no colisione con otras notas del capítulo. También puede usarse una nota textual debajo de la tabla en lugar de dos superíndices.

## 5. Párrafo de limitación sugerido

Agregar en `09_capitulo_08_conclusion_y_trabajos_futuros.typ`, dentro de las limitaciones:

```typst
+ *Ejecución única y ausencia de control efectivo de muestreo.* Se realizó una única ejecución por unidad y configuración, sin réplicas. Aunque el código solicitó `temperature=0.0`, Pydantic AI 1.1.0 elimina ese parámetro para los modelos GPT-5 antes de construir la solicitud; por tanto, no puede afirmarse que las respuestas sean deterministas ni estimarse la variabilidad entre corridas. Tampoco se registró el esfuerzo de razonamiento; el default documentado del proveedor es `medium`, pero no hay prueba local del valor efectivo. La estabilidad de las diferencias observadas debería verificarse con nuevas réplicas.
```

**Motivo:** convierte la limitación en una declaración explícita y evita que la temperatura se use como coartada metodológica.

## 6. Qué no cambiar

- No cambiar la descripción del agente de recuperación que siempre usa gpt-5: es correcta y ayuda a interpretar la confusión de factores.
- No afirmar que los jueces son GPT-5: son DeepSeek, Kimi y Grok vía OpenRouter.
- No eliminar la mención a `temperature=0.0` del código: debe quedar documentada como solicitud, no como parámetro aplicado.
- No reemplazar “reproducibilidad” en todos los contextos: es válida para el pipeline, los hashes, los notebooks y los artefactos. Solo debe precisarse cuando se refiere a las respuestas del modelo.

## 7. Verificación posterior a la edición

1. Buscar en el PDF final `temperatura 0`, `determinista`, `determinísticas`, `garantizar reproducibilidad` y `evita múltiples ejecuciones`.
2. Verificar que la tabla de hiperparámetros distingue “solicitada” de “aplicada”.
3. Verificar que la limitación de ejecución única aparece en conclusiones y en el README.
4. Verificar que el texto sobre jueces no se mezcla con los generadores GPT-5.
5. Revisar que no se haya introducido una afirmación sobre el esfuerzo de razonamiento sin evidencia.

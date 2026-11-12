# Cambios propuestos para el manuscrito

Este documento no modifica el manuscrito. Contiene textos listos para revisar y trasladar a los archivos `.typ`. Las líneas indicadas corresponden a la versión inspeccionada el 2026-11-11.

## 1. Arquitectura general

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`  
**Reemplazar:** párrafo de líneas 204–206.

### Texto anterior

```typst
El sistema Agentic-RAG implementa una arquitectura multi-agente compuesta por dos agentes especializados que coordinan las tareas de recuperación y generación de respuestas: el Agente Especialista Legal y el Agente de Recuperación. Durante el diseño se contempló un tercer agente —el Agente de Calidad de Recuperación— encargado de evaluar la pertinencia de los fragmentos recuperados, pero fue desactivado en la configuración experimental final debido a que su complejidad adicional no se tradujo en mejoras marginales significativas respecto al pipeline de dos agentes. Esta arquitectura se compara con dos configuraciones de referencia: respuesta directa sin recuperación (no RAG) y RAG básico con recuperación vectorial simple.
```

### Texto propuesto

```typst
El sistema Agentic-RAG implementa una arquitectura multi-agente acotada, compuesta por dos agentes activos: el Agente Especialista Legal, que interpreta la consulta y redacta la respuesta final, y el Agente de Recuperación, que descompone la consulta, ejecuta búsquedas vectoriales y selecciona los fragmentos que devuelve al especialista. El Agente Especialista Legal realiza una delegación nominal de recuperación por consulta; no itera sobre los resultados ni verifica la respuesta mediante un agente adicional. Se diseñó un tercer agente —el Agente de Calidad de Recuperación—, pero se excluyó de la configuración experimental por razones de costo y complejidad: añadía una llamada adicional a un LLM y requería seleccionar y justificar un modelo adicional. El agente de calidad no participó en ninguna de las respuestas evaluadas. Esta arquitectura se compara con dos referencias: respuesta directa sin recuperación y RAG básico con una búsqueda vectorial y contexto inyectado.
```

## 2. Agente Especialista Legal

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`  
**Reemplazar:** bloque de líneas 229–242.

### Texto anterior

```typst
El Agente Especialista Legal es el componente principal responsable de generar la respuesta final al usuario. Recibe la pregunta del usuario y, en la configuración Agentic-RAG, tiene acceso a herramientas que le permiten solicitar búsquedas al Agente de Recuperación. Su prompt del sistema está diseñado para orientar las respuestas hacia el dominio legal argentino:

#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 10pt)
    _Eres un asistente legal experto en derecho Argentino. [...]_
  ],
)

El agente tiene límites configurables de invocaciones de herramientas para controlar costos y evitar ciclos infinitos.
```

### Texto propuesto

```typst
El Agente Especialista Legal es el componente principal responsable de generar la respuesta final al usuario. Recibe la pregunta y, en la configuración Agentic-RAG, tiene acceso a la herramienta `retrieve_relevant_documents` para delegar una recuperación en el Agente de Recuperación. Su instrucción solicita utilizar esa herramienta una vez, analizar los documentos devueltos y citar las fuentes legales consultadas. El texto canónico completo se reproduce en @anexo-prompts.

El agente no recibe ejemplos etiquetados en el prompt ni una instrucción explícita de razonamiento paso a paso. Su diseño corresponde a prompting zero-shot con instrucciones estructuradas, una instrucción de citación y una herramienta de recuperación. La descomposición de la consulta y la selección de fragmentos se delegan al Agente de Recuperación. El límite nominal de invocaciones es una llamada; como se documenta en la sección de amenazas a la validez, una sesión histórica registró tres llamadas.
```

## 3. Agente de Recuperación

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`  
**Reemplazar:** líneas 253–271.

### Texto anterior

```typst
El Agente de Recuperación se encarga de realizar búsquedas semánticas en la base de datos vectorial. Tiene la capacidad de descomponer consultas complejas en subconsultas más específicas, realizar múltiples búsquedas y consolidar los resultados. Retorna los fragmentos más relevantes junto con sus metadatos estructurales (artículo, capítulo, título). Su prompt del sistema es el siguiente:

#block(
  [...]
    _Eres un especialista en búsqueda de información legislativa que: [...] como máximo 6 veces; [...]_
  [...]
)

Sus capacidades incluyen:

+ Descomposición de consultas complejas en subconsultas semánticamente más específicas.
+ Ejecución de múltiples búsquedas vectoriales en paralelo.
+ Consolidación y deduplicación de resultados.
+ Retorno de fragmentos con metadatos completos (artículo, capítulo, título, distancia de similitud).
```

### Texto propuesto

```typst
El Agente de Recuperación recibe una consulta del Agente Especialista Legal y puede dividirla en hasta tres subconsultas. Cada búsqueda vectorial devuelve hasta cinco documentos, y el recuperador selecciona los fragmentos que devuelve al especialista. Sus capacidades operativas son:

+ Descomposición de la consulta en hasta tres subconsultas semánticamente más específicas.
+ Ejecución de una o más búsquedas vectoriales en una misma ejecución, sujetas al límite configurado.
+ Selección de documentos y retorno de fragmentos con metadatos estructurales (artículo, capítulo, título y distancia).
+ Retorno de los documentos seleccionados al Agente Especialista Legal.

El prompt completo tuvo dos variantes observadas: la usada por gpt-5 declaró un límite de siete búsquedas y la usada por gpt-5-mini y gpt-5-nano, un límite de seis. Ambas se reproducen literalmente en @anexo-prompts. Esta diferencia se declara como amenaza a la validez en la subsección siguiente.
```

## 4. Agente de Calidad de Recuperación

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`  
**Reemplazar:** líneas 280–295.

### Texto anterior

```typst
El Agente de Calidad de Recuperación fue diseñado para evaluar la pertinencia de los fragmentos recuperados antes de enviarlos al Agente Especialista Legal. [...] Sin embargo, este agente fue desactivado en la configuración experimental final por dos motivos principales: (1) agregaba complejidad significativa en la gestión de llamadas a APIs, incrementando los costos operativos al requerir una capa adicional de invocación al LLM; y (2) requería la selección de un modelo adicional, introduciendo otra variable de configuración. En su lugar, se optó por actualizar los prompts del Agente Especialista Legal para que este pudiera solicitar búsquedas adicionales al Agente de Recuperación en caso de considerar que la información recuperada inicialmente era insuficiente, logrando un equilibrio entre calidad de recuperación y eficiencia. Su prompt del sistema era el siguiente: [...]

En el código de orquestación, su herramienta (`evaluate_retrieval`) y su prompt del sistema fueron comentados, por lo que no participó en la generación de los resultados reportados.
```

### Texto propuesto

```typst
El Agente de Calidad de Recuperación fue diseñado para evaluar la pertinencia de los fragmentos recuperados antes de enviarlos al Agente Especialista Legal. Su función prevista era comprobar si la recuperación inicial era suficiente y, en caso contrario, generar retroalimentación para reformular la consulta. Se excluyó de la configuración experimental por razones de costo y complejidad: añadía una llamada adicional a un LLM y exigía seleccionar y justificar un modelo adicional. No se realizó una comparación empírica de su contribución, de modo que no se afirma que su exclusión haya producido una mejora o un deterioro en el desempeño.

Su prompt se reproduce en @anexo-prompts. En el código final, el agente se instancia sin herramientas, la función `evaluate_retrieval` no está registrada como herramienta y no se encontró ningún registro de ejecución del agente de calidad. Por lo tanto, el prompt nunca se envió a un modelo y el agente no participó en las respuestas evaluadas.
```

> **Confirmación del autor:** la exclusión se debió a costo y complejidad. No debe conservarse la frase “no se tradujo en mejoras marginales significativas”, porque no existe una comparación que la respalde.

## 5. Orquestación y flujo de comunicación

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`  
**Reemplazar:** líneas 299–307.

### Texto anterior

```typst
La orquestación se implementó como un flujo secuencial donde el Agente Especialista Legal invoca herramientas que internamente disparan la ejecución del Agente de Recuperación. Pydantic AI gestiona automáticamente el ciclo de herramientas (tool call → resultado → siguiente invocación) hasta que el agente principal produce la respuesta final o se alcanza el límite de herramientas. [...]

+ El usuario formula una pregunta.
+ El Agente Especialista Legal recibe la consulta e invoca al Agente de Recuperación.
+ El Agente de Recuperación ejecuta búsquedas vectoriales, potencialmente descomponiendo la consulta en subconsultas.
+ Los fragmentos recuperados se retornan al Agente Especialista Legal.
+ El Agente Especialista Legal genera la respuesta final integrando el contexto recuperado.

Para las configuraciones sin RAG y RAG básico, se empleó un prompt simplificado [...]
```

### Texto propuesto

```typst
La orquestación implementada es una delegación de una sola ronda desde el Agente Especialista Legal hacia el Agente de Recuperación. El flujo es el siguiente:

+ El usuario formula una pregunta.
+ El Agente Especialista Legal recibe la consulta e invoca `retrieve_relevant_documents`.
+ La herramienta ejecuta internamente `retrieval_agent.run_sync(...)`.
+ El Agente de Recuperación puede dividir la consulta en hasta tres subconsultas y realizar búsquedas vectoriales dentro de su propio límite.
+ El recuperador devuelve los documentos seleccionados como resultado de la herramienta.
+ El Agente Especialista Legal redacta la respuesta final con ese contexto.

El Agente Especialista Legal no recibe el control para una segunda ronda de recuperación ni verifica la respuesta con el Agente de Calidad. El bucle de búsquedas ocurre dentro del Agente de Recuperación, no entre el especialista y el recuperador.

Los prompts de las configuraciones sin RAG y RAG básico no son una versión simplificada del prompt agéntico: son textos distintos. En RAG básico se añade además el bloque de documentos recuperados al prompt. Los tres textos se reproducen en @anexo-prompts.
```

## 6. Límites de herramientas y variante histórica

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`  
**Reemplazar:** párrafos y bloque de líneas 422–441.

### Texto propuesto

```typst
El código final fija un límite nominal de seis búsquedas para el Agente de Recuperación (`TOTAL_TOOL_CALL_LIMIT = 6`) y de una invocación para el Agente Especialista Legal (`DOCUMENT_RETRIEVAL_LIMIT = 1`). Ambas capas se implementan mediante `UsageLimits` y `prepare_tools`.

Sin embargo, la corrida evaluada no fue uniforme. Los logs muestran que la variante usada por gpt-5 declaró y aplicó un límite de siete búsquedas: 33 de sus 79 sesiones realizaron siete búsquedas. Las variantes usadas por gpt-5-mini y gpt-5-nano declararon un límite de seis y ninguna sesión superó ese valor. Además, 236 de las 237 sesiones del especialista registraron una llamada a `retrieve_relevant_documents`; la sesión `16_01` de gpt-5 registró tres.

En consecuencia, el límite de seis no debe presentarse como una propiedad homogénea de las nueve configuraciones. La diferencia se conserva en la tabla de configuración observada y se declara como amenaza a la validez.
```

Si se conserva el bloque de código, debe acompañarse de una nota inmediata:

```typst
#block(
  width: 100%,
  inset: 10pt,
  stroke: 0.5pt + luma(180),
  radius: 4pt,
  [
    #set text(size: 9pt, font: "DejaVu Sans Mono")
    ```python
    TOTAL_TOOL_CALL_LIMIT = 6          # valor del código final
    DOCUMENT_RETRIEVAL_LIMIT = 1       # nominal
    VECTOR_SEARCH_LIMIT = UsageLimits(tool_calls_limit=6)
    # La corrida histórica de gpt-5 usó tool_calls_limit=7.
    ```
  ],
)
```

## 7. Hiperparámetros: cambios mínimos

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`  
**Reemplazar:** tabla de líneas 465–477 y párrafo de línea 481.

### Texto anterior

```typst
| Temperatura                       | 0,0 | 0,0 |
| Límite de llamadas a herramientas |  1  |  6  |
...
El límite total de llamadas a herramientas del sistema está fijado en 6 invocaciones [...]
```

### Texto propuesto

```typst
| Temperatura solicitada             | 0,0#super[†] | 0,0#super[†] |
| Límite de llamadas a herramientas | 1 nominal; una sesión registró 3 | 6 en mini/nano; 7 en gpt-5 |
| Herramienta disponible            | `retrieve_relevant_documents` | `cosine_distance_vector_search` |
| Máx. subconsultas por consulta    | — | 3 |
| Modelo por defecto                | Variable#super[‡] | gpt-5 |
```

Caption:

```typst
caption: [Configuración nominal y observada de los agentes activos. #super[†]La temperatura se conserva como valor solicitado; su tratamiento efectivo se discute en la corrección metodológica sobre parámetros de API. #super[‡]El modelo del Agente Especialista Legal varía según la configuración experimental (gpt-5-nano, gpt-5-mini o gpt-5). La corrida de gpt-5 usó un límite de 7 búsquedas; las de mini y nano usaron 6.],
```

Párrafo que debe seguir a la tabla:

```typst
El límite nominal del código final es de seis búsquedas para el recuperador y una invocación para el especialista. La corrida histórica de gpt-5 utilizó siete búsquedas y una sesión del especialista registró tres invocaciones. Por tanto, los valores de la tabla describen la configuración nominal y las variantes observadas, no una regla uniforme aplicada a todas las configuraciones.
```

No conservar “La temperatura controla ... (0,0 = determinista)” en este punto. Esa frase pertenece a la corrección IX.1.3 y no debe introducirse en la tabla de esta corrección.

## 8. Nueva subsección de alcance y factores confundidos

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ`  
**Insertar después de:** `@fig-arq-agentic-rag` (después de la línea 278), antes de la sección del Agente de Calidad.

```typst
=== Alcance operativo y factores confundidos

La etiqueta Agentic-RAG se usa en este trabajo para designar una implementación acotada: dos agentes activos, una delegación nominal de recuperación y ninguna verificación automática de la respuesta. No debe interpretarse como un planificador autónomo ni como un ciclo iterativo del Agente Especialista Legal.

Las tres estrategias no son variaciones de un único factor. En Agentic-RAG cambian simultáneamente el prompt del generador, la descomposición de la consulta, el número de candidatos recuperados, la selección de fragmentos, el modelo que recupera y el presupuesto de búsquedas. La @tabla-factores-confundidos resume las diferencias y sus consecuencias para la interpretación. Si se inserta el archivo `propuestas/tabla_factores_confundidos.typ`, usar esa tabla y no duplicar el bloque de esta sección.

#figure(
  three-line-table(
    columns: (2.3cm, 3.2cm, 3.2cm, 1fr),
    [
      | *Dimensión* | *Sin RAG* | *RAG básico* | *Agentic-RAG observado* |
      | :--- | :--- | :--- | :--- |
      | Modelo que redacta | variable | variable | variable: gpt-5-nano, mini o gpt-5 |
      | Modelo que recupera | — | — | gpt-5 en las tres configuraciones |
      | Prompt | `sin_rag_system` | `rag_basico_system_template` | `especialista_legal_system` |
      | Consulta de recuperación | — | consulta original, una búsqueda | delegada; hasta 3 subconsultas |
      | Candidatos | — | top-10 | hasta 5 por búsqueda; 6 búsquedas en mini/nano y 7 en gpt-5 |
      | Selección | — | top-10 por similitud | gpt-5 selecciona los documentos devueltos |
      | Iteración del especialista | — | — | una delegación nominal; sin segunda ronda |
      | Verificación | — | — | Agente de Calidad definido, nunca ejecutado |
      | Ablación | — | — | no realizada |
    ],
  ),
  caption: [Diferencias simultáneas entre las estrategias. No constituyen un factorial de un único factor y, sin ablaciones, no permiten atribuir el efecto observado a la descomposición, al número de candidatos, a la selección o al cambio de prompt.],
) <tabla-factores-confundidos>

La diferencia de límite entre gpt-5 y los otros dos modelos agrega una amenaza específica al contraste entre modelos: gpt-5 dispuso de hasta siete búsquedas, mientras que mini y nano dispusieron de seis. Esta asimetría debe mencionarse al interpretar la interacción estrategia × modelo y no puede resolverse sin una nueva corrida homogénea o una ablación específica.

#figure(
  image("../media/diag_agentic_rag_operativo.svg", width: 88%),
  caption: [Configuración Agentic-RAG observada: el Agente Especialista Legal realiza una delegación nominal al Agente de Recuperación; el recuperador ejecuta hasta 6 búsquedas en mini/nano y hasta 7 en gpt-5; el Agente de Calidad no participa.],
) <fig-arq-agentic-rag-operativo>
```

Si no se incorpora el SVG nuevo, conservar el diagrama actual y cambiar solamente su epígrafe por el texto anterior, corrigiendo “Hasta 6 búsquedas” en la figura si es posible.

## 9. Capítulo 3: few-shot y Chain-of-Thought

**Archivo:** `manuscrito/capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ`

### Reemplazar línea 89

```typst
El sistema de este trabajo combina varias de estas técnicas: few-shot prompting para fijar el formato de respuesta, Chain-of-Thought para inducir razonamiento explícito, y structured prompting para organizar la entrada con contexto recuperado + consulta + restricciones. La descripción detallada del prompt concreto se presenta en el capítulo @cap:metodologia.
```

por:

```typst
El sistema de este trabajo no incorpora ejemplos etiquetados en el prompt ni una instrucción explícita de cadena de pensamiento. Su diseño se apoya en prompting zero-shot con instrucciones estructuradas, una instrucción explícita de citar fuentes y el uso de una herramienta de recuperación. La descomposición de la consulta y la selección de fragmentos se delegan al Agente de Recuperación. La descripción completa de los prompts se presenta en el capítulo @cap:metodologia y se reproduce en @anexo-prompts.
```

### Reemplazar el cierre de línea 135

```typst
En síntesis, el LLM aporta versatilidad cognitiva, la base documental aporta factualidad y trazabilidad, y el agente aporta planificación y verificación.
```

por:

```typst
En el sistema implementado, el LLM aporta generación, la base documental aporta factualidad y trazabilidad, y el Agente de Recuperación aporta descomposición y selección de evidencia. No se implementó un verificador autónomo ni una cadena de verificación de la respuesta.
```

## 10. Conclusiones: objetivo 2

**Archivo:** `manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ`  
**Reemplazar:** línea 17.

```typst
+ *Desarrollar un sistema de agentes de inteligencia artificial para que trabajen de manera conjunta con el sistema RAG.* Este objetivo se cumplió parcialmente. Se implementó una arquitectura multi-agente acotada mediante Pydantic AI, con dos agentes activos: el Agente Especialista Legal (generación de respuestas) y el Agente de Recuperación (descomposición de consultas y búsqueda vectorial). El Agente de Calidad de Recuperación fue diseñado, pero se excluyó por razones de costo y complejidad y no participó en la configuración experimental. El especialista realiza una delegación nominal de recuperación; no hay iteración del especialista ni verificación automática de la respuesta. En consecuencia, el objetivo se cumple respecto de la coordinación entre recuperación y generación, pero no respecto de un ciclo completo de verificación multi-agente.
```

## 11. Diagrama

**Archivo nuevo propuesto:** `manuscrito/media/diag_agentic_rag_operativo.svg`.  
**Origen revisable:** `propuestas/diagrama_agentic_rag_operativo.mmd`.

El diagrama actual (`diag_agentic_rag.svg`) muestra “Hasta 6 busquedas”. Es correcto para mini y nano, pero no para gpt-5. El diagrama nuevo debe mostrar la delegación, el límite variable y la ausencia del Agente de Calidad. Si no se cambia el SVG, al menos debe cambiarse el epígrafe y no afirmar que el límite de seis es universal.

## 12. README, resumen de tareas y notebook

### `codigo_experimentos/performed_tasks_summary.md`

La fila de `part_g` describe “three-agent architecture” y presenta al Agente de Calidad como parte del sistema. Cambiar por:

```markdown
| `01_generate_responses_using_agents.py` | Define dos agentes activos (Law Specialist y Retrieval) y un tercer agente de calidad que fue diseñado pero no ejecutado. El script final es la fuente canónica de los prompts registrados en los logs. |
```

### `codigo_experimentos/part_g/01_generate_responses_using_agents.ipynb`

El notebook conserva una versión anterior: prompt del especialista con formato APA, prompt del recuperador sin límite explícito y `evaluate_retrieval` activo. No es la fuente de la corrida final. Antes de publicar la versión definitiva:

1. reemplazar sus celdas de instrucciones por los prompts canónicos del anexo; o
2. marcarlo explícitamente como exploratorio y remitir al script `.py` como fuente canónica.

No se debe presentar simultáneamente el notebook viejo y el anexo nuevo como si describieran la misma configuración.

### `README.md`

Actualizar la descripción del sistema multi-agente para indicar “dos agentes activos y un Agente de Calidad diseñado pero no ejecutado”. Si se cambia el título, actualizar también el bloque BibTeX y la portada.

## 13. Inclusión del anexo

**Archivo:** `manuscrito/main.typ`

Agregar después de `#include "capitulos/anexo_01.typ"`:

```typst
#include "capitulos/anexo_02_prompts_y_parametros.typ"
```

El archivo propuesto debe copiarse como `manuscrito/capitulos/anexo_02_prompts_y_parametros.typ`. Revisar la numeración de anexos y las referencias `@anexo-prompts`. El archivo generado no modifica `main.typ` ni el anexo existente.

## 14. Orden de revisión sugerido

1. Confirmar que se acepta declarar la diferencia 7/6 entre gpt-5 y mini/nano.
2. Confirmar si se desea corregir el diagrama o solo el epígrafe.
3. Revisar el anexo generado y los hashes.
4. Aplicar los cambios de metodología.
5. Aplicar capítulo 3 y conclusiones.
6. Actualizar README y notebook.
7. Compilar y comprobar las referencias cruzadas.

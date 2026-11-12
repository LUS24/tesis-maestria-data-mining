# Reflexión: ablación, modelo recuperador y alcance del factor "modelo"

**Corrección asociada:** IX.1.4 — *Declarar la confusión de factores, reproducir todos los prompts y resolver las contradicciones sobre el Agente de Calidad y el límite de búsquedas.*
**Observación de origen:** V.5 (factores confundidos y alcance del término Agentic-RAG).
**Estado:** nota de trabajo. **No** es texto para insertar en el manuscrito; es insumo para decidir qué se cambia y cómo se redacta.
**Fecha:** 2026-11-11.
**Motivo:** el autor objetó —con razón— la formulación del plan que presentaba como "necesario" igualar el modelo recuperador. Esta nota corrige esa formulación y fija el criterio para el manuscrito.

**Relación con el resto del paquete:** esta nota se suma al material ya producido en esta carpeta (`README.md`, `01_informe_auditoria.md`, `03_resolucion_contradicciones.md`, `propuestas/`). No lo reemplaza: aporta el criterio metodológico para decidir *qué* se afirma sobre el factor "modelo" y si hace falta un experimento adicional. Los hallazgos de la auditoría de prompts se citan aquí solo en lo que afecta esa decisión.

---

## 1. Punto de partida: la objeción

> "¿Por qué es incorrecto dejar constante al modelo recuperador?"

**No lo es.** Fijar el recuperador en gpt-5 es una decisión de diseño legítima, y de hecho es la que corresponde al sistema que se despliega. Lo incorrecto no es el diseño, sino tres cosas distintas:

1. no declararlo como parte de la definición del tratamiento;
2. usar la etiqueta "modelo" para un factor que designa constructos diferentes en cada estrategia;
3. interpretar el resultado como una propiedad de la arquitectura en general, y no de la arquitectura *con recuperador gpt-5*.

La distinción importa porque cambia el trabajo requerido: el punto 1, 2 y 3 se resuelven **editando el manuscrito**, sin nuevas corridas.

---

## 2. Precisión terminológica: ablación ≠ sustitución

En el plan se usó "ablación" en el sentido amplio de la práctica de ML (cambiar una pieza y ver qué pasa). Conviene precisarlo, porque el manuscrito va a tener que nombrar el experimento:

| Término | Qué hace | Ejemplo en esta tesis |
|---|---|---|
| **Ablación** (estricta) | Elimina un componente para medir su aporte | Quitar la descomposición de consultas; quitar el paso de selección de documentos |
| **Sustitución controlada** | Reemplaza un componente por otro, manteniendo el resto fijo | Cambiar el recuperador gpt-5 por el modelo del especialista |
| **Factorial** | Cruza dos factores y estima su interacción | Especialista ∈ {nano, mini, gpt-5} × recuperador ∈ {nano, mini, gpt-5} |

La propuesta de la "diagonal" es una **sustitución**, no una ablación. Si se ejecuta, el manuscrito debe llamarla así. Llamarla "ablación" invita a una objeción del jurado en la defensa.

---

## 3. Qué queda confundido —y qué no— con el recuperador fijo

Sea **S** la capacidad del Agente Especialista Legal y **R** la del Agente de Recuperación. En la configuración experimental, **R = gpt-5 constante**:

| Especialista | Recuperador | Presupuesto de búsqueda | Composición del sistema | Ventaja del ayudante (R − S) |
|---|---|---|---|---|
| gpt-5-nano | gpt-5 | 6 búsquedas | **mixta** | grande |
| gpt-5-mini | gpt-5 | 6 búsquedas | **mixta** | media |
| gpt-5 | gpt-5 | **7 búsquedas** | homogénea | nula |

Lo que varía al movernos por el factor "modelo" **no es una sola cosa**: cambia la capacidad del redactor y, con ella, la distancia entre redactor y recuperador. La *intensidad del tratamiento* depende del nivel del factor.

La auditoría de este mismo paquete (`03_resolucion_contradicciones.md`) agrega una **segunda asimetría sobre el mismo eje**: la configuración de gpt-5 se ejecutó con un prompt de recuperador que permite **siete** búsquedas, mientras que mini y nano usaron uno de **seis**; en gpt-5, 33 de 79 sesiones agotaron las siete. El modelo de mayor capacidad recibió además el mayor presupuesto de recuperación. Son dos confundidos que apuntan en la misma dirección, y el segundo **no se corrige con la diagonal**: hay que declararlo o repetir la corrida de gpt-5 con el prompt de seis búsquedas.

En las otras dos estrategias no existe un recuperador-LLM, de modo que "modelo" designa allí al único modelo del sistema. El mismo nombre cubre entonces tres constructos:

- sin RAG → el modelo que responde;
- RAG básico → el modelo que responde, con contexto fijo de 10 fragmentos;
- Agentic-RAG → **solo** el modelo que redacta; la recuperación y la selección las hace gpt-5.

**Precisión importante:** el recuperador constante **no fabrica** una interacción espuria si los efectos fueran aditivos. Si el desempeño fuera `P = f(S) + g(R)`, fijar R agrega una constante y no altera la interacción. El problema es de **validez de constructo y externa**, no de aritmética: la interacción observada es real *en esta configuración*, pero no es generalizable sin más.

---

## 4. Qué inferencias siguen siendo válidas

### Válidas con R = gpt-5 fijo

- "Dado un recuperador gpt-5, ¿qué modelo conviene usar como redactor?" — pregunta operativa y plenamente respondible con los datos actuales.
- "Con recuperador gpt-5, el efecto de la estrategia depende del modelo redactor" — afirmación acotada y correcta.
- Comparaciones **dentro** de la estrategia agéntica entre redactores: son válidas en cuanto a la composición de modelos, porque R no varía; **no** son del todo limpias, porque gpt-5 corrió con presupuesto de siete búsquedas y mini y nano con seis (véase §3).

### No válidas con R = gpt-5 fijo

- "Agentic-RAG sobrecarga a los modelos pequeños" **como propiedad de la arquitectura**. Solo está establecido para la arquitectura con recuperador gpt-5. Con recuperador nano el patrón podría invertirse o desaparecer.
- "La capacidad del modelo afecta el desempeño de tal manera" comparando **entre** estrategias: en la celda agéntica el contraste incluye incorporar un modelo fuerte; en las otras no.
- Cualquier partición del efecto entre "capacidad del redactor" y "capacidad del recuperador": con R fijo ambas fuentes son **inidentificables por separado**.

---

## 5. Los diseños posibles

| Diseño | Manipula | Pregunta que responde | Celdas nuevas | Costo aprox. |
|---|---|---|---|---|
| **A. R fijo = gpt-5** (actual) | Solo el redactor | ¿Qué redactor usar si el recuperador es gpt-5? | 0 | ya ejecutado |
| **A′. R fijo, presupuesto igualado** | Solo el redactor, con 6 búsquedas en las tres celdas | La misma pregunta, sin la asimetría 7/6 | 1 (repetir gpt-5) | ≈ USD 5 |
| **B. Diagonal** (R = S) | Redactor y recuperador juntos | ¿Importa la capacidad del sistema cuando ambos agentes son el mismo modelo? | 2 | ≈ USD 9,5 |
| **C. Factorial 3×3** | Ambos por separado | ¿Cuánto aporta cada agente y cómo interactúan? | 8 | ≈ USD 38 |

A′ merece atención porque es la intervención **más barata** que elimina un confundido real: deja las tres configuraciones agénticas con el mismo prompt de recuperador, sin tocar la composición de modelos. No sustituye a B ni a C —no responde cómo interactúan redactor y recuperador—, pero sí elimina una objeción concreta y verificable que hoy está en el manuscrito sin declarar.

Las cifras son de orden de magnitud, derivadas del agregado histórico (Agentic-RAG: USD 14,24 / 237 observaciones ≈ USD 0,060 por consulta × 79). El costo exacto debe recalcularse antes de aprobar el gasto.

### Comentario sobre el costo, a favor del diseño A

El propio análisis de costos de la tesis muestra que el recuperador domina la factura. En el ejemplo del anexo, con gpt-5-nano como especialista:

- Agente de Recuperación (gpt-5): **USD 0,05037**
- Agente Especialista Legal (gpt-5-nano): **USD 0,00285**

Es decir, ~95 % del costo de la celda está en la pieza que se mantiene fija. Un sistema realista **siempre** usará un recuperador fuerte. Bajo ese supuesto, el diseño A no es un defecto: es la configuración desplegable, y la diagonal sería una configuración que nadie elegiría en producción.

Esto sugiere una defensa sólida en la instancia oral: *"fijé el recuperador porque es la decisión de ingeniería que un despliegue adoptaría; lo que varía es el modelo que redacta"*. Es una respuesta mejor que la actual, que no declara la decisión.

---

## 6. La diagonal tampoco es gratis

Al pasar de `nano + gpt-5` a `nano + nano` cambian **dos** cosas respecto de la celda original: el redactor y el recuperador. Por lo tanto:

- **`nano + gpt-5` vs `nano + nano`** → aísla el efecto del **recuperador** con redactor fijo. Contraste limpio de una sola pieza. ✔
- **La columna diagonal entre modelos** → mantiene la regla de composición (R = S) y varía la capacidad del sistema; pero cualquier diferencia es **compuesta**: no permite afirmar "gpt-5 redacta mejor", porque también recupera mejor.

En síntesis: la diagonal arregla la **homogeneidad del factor**, no la **separación de componentes**. Solo el diseño C separa redactor, recuperador y su interacción.

---

## 7. Camino recomendado: resolverlo sin nuevas corridas

Propuesta principal para la corrección 04. Cuatro cambios, todos editoriales:

1. **Renombrar el factor en todo el manuscrito.** Donde hoy dice "modelo", escribir "modelo del Agente Especialista Legal". En tablas y figuras, la etiqueta de la celda agéntica debe incluir el recuperador: `Agentic-RAG (recuperador gpt-5) + gpt-5-nano`. La etiqueta actual, "Agentic-RAG + gpt-5-nano", describe mal un sistema mixto.
2. **Declarar la composición como parte de la definición del tratamiento.** El "Agentic-RAG" evaluado es: especialista variable + recuperador gpt-5 + una delegación + sin verificador activo. No es "Agentic-RAG" en abstracto.
3. **Reformular la conclusión** de "sobrecarga agéntica" a un enunciado condicionado a la configuración (véase §9).
4. **No reclamar** partición de efectos entre agentes ni superioridad de un modelo "como redactor".

Con esto, cada afirmación queda acotada a lo que los datos sostienen, y la confusión de V.5 deja de ser un defecto de diseño para convertirse en una **limitación declarada**.

---

## 8. Cuándo la sustitución pasa a ser necesaria

La diagonal (diseño B) deja de ser opcional **solo** en tres escenarios:

1. **Se quiere mantener la explicación causal** "la complejidad agéntica es excesiva para modelos de capacidad reducida". Sostenerla exige mostrar que el patrón no depende de que el recuperador sea fuerte.
2. **Se aspira a publicar el hallazgo** como propiedad de la arquitectura Agentic-RAG, y no de esta implementación.
3. **El jurado lo pide expresamente** en la defensa.

En cualquiera de los tres casos hay una **restricción de calendario dura**: los tres modelos se apagan el **2026-12-11** (verificado contra `GET /v1/models` el 2026-11-11; `shutdown_date` presente en alias y snapshots). Después de esa fecha la sustitución con los modelos originales ya no es posible, y solo quedaría rehacer el marco experimental con la familia `gpt-5.6-*`, que no sería comparable con las 711 observaciones existentes.

**Decisión pendiente del autor.** Si no se persigue la afirmación causal, no hace falta correr nada.

---

## 9. Implicancias para el resto de la corrección 04

Estas reflexiones no viven aisladas: comparten causa con las otras contradicciones de V.5. Al revisar el manuscrito, tratarlas como un mismo bloque.

### 9.1 Afirmación no sustentada sobre el Agente de Calidad

Aparece en **dos** lugares, y en ninguno hay comparación que la respalde:

- `06_capitulo_05_metodologia.typ:206` — "fue desactivado […] debido a que su complejidad adicional **no se tradujo en mejoras marginales significativas** respecto al pipeline de dos agentes".
- `09_capitulo_08_conclusion_y_trabajos_futuros.typ:17` — misma afirmación, dentro de un objetivo declarado "cumplido completamente".

Contradice la justificación de `06_capitulo_05_metodologia.typ:282`, que da **dos motivos distintos**: (1) complejidad y costo de llamadas, y (2) necesidad de elegir un modelo adicional. Ninguno menciona una comparación de desempeño.

**Acción:** conservar únicamente las razones de costo y complejidad —el autor ya las confirmó, según el `README.md` de este paquete—. Eliminar "no se tradujo en mejoras" de ambos lugares. La auditoría verificó además que el Agente de Calidad tiene **0 logs y 0 llamadas**: nunca se ejecutó, de modo que ninguna afirmación sobre su efecto es sostenible, ni en un sentido ni en el otro.

### 9.2 Contradicción "búsquedas adicionales" vs límite de una invocación

Todo ocurre en `06_capitulo_05_metodologia.typ`:

- **:282** afirma que se actualizaron los prompts "para que este pudiera **solicitar búsquedas adicionales** al Agente de Recuperación".
- **:238** reproduce el prompt del especialista: "utilizas la herramienta `retrieve_relevant_documents` **una vez**".
- **:424** explica que `DOCUMENT_RETRIEVAL_LIMIT = 1` retira las herramientas tras la primera llamada.
- **:435** muestra el código: `DOCUMENT_RETRIEVAL_LIMIT = 1`.

**Acción:** distinguir tres niveles, que es lo que realmente ocurre:

1. **Delegación del especialista:** límite nominal de **una** invocación a `retrieve_relevant_documents`; 236 de 237 sesiones lo respetan, con una excepción registrada (`16_01` de gpt-5, con tres llamadas).
2. **Búsquedas del recuperador:** hasta **seis** por delegación en mini y nano; hasta **siete** en gpt-5.
3. **Iteración:** ninguna. El especialista no vuelve a solicitar documentos en función de lo recibido.

La frase de :282 debe reescribirse en esos términos. No puede decir que el especialista itera, ni presentar "seis búsquedas" como propiedad uniforme sin resolver antes la asimetría 7/6.

### 9.3 Few-shot y Chain-of-Thought

`04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:89` afirma que el sistema combina "few-shot prompting para fijar el formato de respuesta" y "Chain-of-Thought para inducir razonamiento explícito".

Los prompts reproducidos en metodología y los registrados en `part_g/chat_data/` **no contienen ejemplos** ni instrucciones de razonamiento paso a paso. Los jueces tampoco recibieron CoT (`09_capitulo_08…:85`, limitación ya declarada).

**Acción:** reformular como discusión teórica de técnicas disponibles y describir lo efectivamente implementado: *structured prompting*, instrucción de citación obligatoria, instrucción de abstención y uso de herramienta. Si se quiere conservar la mención a CoT, debe referirse al razonamiento interno de los modelos GPT-5 (tokens de razonamiento), no a una técnica de prompting aplicada.

### 9.4 Confusión entre "no significativo" y "equivalente"

Con R fijo, la celda de gpt-5 muestra diferencias no significativas tras Holm. Eso **no** habilita hablar de equivalencia, ni entre estrategias ni entre modelos. Aplica lo mismo que la corrección IX.1.5: reportar IC y, si se desea equivalencia, fijar un margen *a priori*.

---

## 10. Checklist para la revisión del manuscrito

| # | Verificación | Archivo(s) |
|---|---|---|
| 1 | "modelo" siempre calificado como "modelo del Agente Especialista Legal" | todos los capítulos, tablas y figuras |
| 2 | Etiquetas de celda agéntica indican `recuperador gpt-5` | `07_capitulo_06_evaluacion.typ`, figuras en `media/` |
| 3 | Composición del tratamiento declarada en metodología y en amenazas a la validez | `06_capitulo_05_metodologia.typ` |
| 4 | Eliminada "no se tradujo en mejoras marginales significativas" | `06…:206`, `09…:17` |
| 5 | Razones de desactivación del Agente de Calidad: solo costo/complejidad | `06…:282` |
| 6 | "Búsquedas adicionales" reformulado a tres niveles (delegación / búsquedas / sin iteración) | `06…:282`, `06…:424` |
| 6 bis | Asimetría 7/6 declarada o corrida de gpt-5 repetida con límite 6 | `03_resolucion_contradicciones.md` |
| 7 | Few-shot/CoT reclasificados como marco teórico, no como implementación | `04…:89` |
| 8 | Conclusión de "sobrecarga agéntica" condicionada a la configuración | `07…`, `09…`, `01_texto_preliminar.typ`, `README.md` |
| 9 | Objetivo 2 declarado como cumplimiento parcial | `09…:17` |
| 10 | Sin afirmaciones de equivalencia por falta de significación | `07…`, `09…` |
| 11 | Prompts completos reproducidos y verificados contra los logs | `propuestas/anexo_02_prompts_y_parametros.typ` (ya existe) |
| 12 | Si se ejecuta la sustitución: llamarla "sustitución controlada", no "ablación" | capítulo de evaluación |
| 13 | Excepción `16_01` (tres llamadas del especialista) declarada | `06…`, anexo de prompts |

---

## 11. Redacciones propuestas

### 11.1 Conclusión sobre modelos pequeños

**Actual** (`09_capitulo_08…:33`):

> "Se documentó que el sistema Agentic-RAG degrada el desempeño de modelos de capacidad reducida […] Esto sugiere que la complejidad de las instrucciones y contextos generados por el sistema agéntico excede la capacidad de procesamiento de estos modelos."

**Propuesta:**

> "Con el Agente de Recuperación fijado en gpt-5, la configuración agéntica degradó el desempeño de gpt-5-nano respecto de RAG básico (p corregido = 0,017). El patrón es consistente con una dificultad de los modelos pequeños para operar el flujo de dos agentes, pero no permite atribuir la degradación a la complejidad de la arquitectura en general ni descartar que dependa de la composición específica del sistema evaluado, en el que la recuperación y la selección de documentos las realiza un modelo de mayor capacidad."

### 11.2 Definición del tratamiento

**Propuesta de párrafo para metodología:**

> "La estrategia Agentic-RAG evaluada se define por cinco rasgos: (i) un Agente Especialista Legal cuyo modelo varía entre configuraciones; (ii) un Agente de Recuperación fijado en gpt-5 para las tres configuraciones, que descompone la consulta y ejecuta búsquedas vectoriales —hasta seis en mini y nano, hasta siete en gpt-5—; (iii) un límite nominal de una delegación de recuperación por consulta, respetado en 236 de 237 sesiones, con una excepción registrada; (iv) ausencia de iteración: el especialista no vuelve a solicitar documentos en función de lo recibido; y (v) un Agente de Calidad de Recuperación diseñado pero nunca ejecutado. En consecuencia, el factor 'modelo' designa en esta estrategia únicamente al modelo del Agente Especialista Legal, y las configuraciones agénticas con modelos pequeños son sistemas mixtos."

### 11.3 Tabla de amenazas a la validez (fila nueva)

| Amenaza | Descripción | Mitigación / estado |
|---|---|---|
| Composición heterogénea en Agentic-RAG | El recuperador es siempre gpt-5; el factor "modelo" designa solo al redactor | Declarado; conclusión acotada a esta configuración. Sustitución controlada (R = S) solo si se persigue la afirmación causal |
| Prompts no equivalentes entre estrategias | Sin RAG y RAG básico usan un prompt simplificado distinto del agéntico | Prompts completos en anexo; diferencia declarada como parte del tratamiento |
| Componentes no separados | Descomposición, número de candidatos, selección por gpt-5 y prompt cambian juntos | Sin ablaciones; no se atribuye el efecto a un componente específico |

---

## 12. Preguntas abiertas para el autor

1. ¿El sistema que se querría desplegar usaría siempre un recuperador fuerte? Si la respuesta es sí, el diseño A es defendible tal cual y conviene decirlo explícitamente en metodología.
2. ¿Se quiere sostener la afirmación causal "sobrecarga agéntica"? De la respuesta depende si hay que ejecutar la sustitución antes del **2026-12-11**.
3. ¿Existe algún registro, aunque sea informal, de la comparación con el Agente de Calidad activo? Si no existe, hay que eliminar la afirmación de `06…:206` y `09…:17`.
4. ¿Se dispone de presupuesto y tiempo para 2 celdas (≈ USD 9,5) o para 8 (≈ USD 38), considerando además la evaluación con jueces?
5. ¿Se declara la asimetría 7/6 o se repite Agentic-RAG + gpt-5 con el prompt de seis búsquedas? Esta segunda opción también vence el 2026-12-11 y compite por el mismo presupuesto que la sustitución.

---

## 13. Registro de decisión

| Fecha | Decisión | Responsable |
|---|---|---|
| | Camino sin nuevas corridas (declarar + acotar) / Sustitución B / Factorial C | |
| | Si se ejecuta: fecha límite de corrida (≤ 2026-12-11) | |
| | Denominación adoptada en el manuscrito para el experimento adicional | |

---

## Referencias internas

- `analisis-valoracion-jurado/plan_correcciones_y_recomendaciones.md` — §IX.1.4 y §IX.2.4.
- `analisis-valoracion-jurado/Valoracion_TF_Spairani_gp_v3.md` — V.5 e IX.1.4.
- `README.md` y `03_resolucion_contradicciones.md` de esta carpeta — auditoría de prompts, asimetría 7/6 y excepción `16_01`.
- `propuestas/anexo_02_prompts_y_parametros.typ` y `propuestas/tabla_factores_confundidos.typ` — artefactos ya redactados a los que esta nota remite.
- Verificación de vigencia de modelos: `GET /v1/models`, 2026-11-11; `shutdown_date = 2026-12-11` para alias y snapshots.
- Estado de parámetros de muestreo: ver la nota de la corrección 03 (temperatura rechazada por la API y descartada por pydantic-ai 1.1.0).

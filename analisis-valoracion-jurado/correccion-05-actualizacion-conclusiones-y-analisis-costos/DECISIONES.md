# Decisiones necesarias antes de editar las conclusiones

**Corrección:** IX.1.5 — reformulación de la Tabla 4 y actualización de conclusiones.  
**Uso:** este archivo separa las decisiones editoriales/metodológicas de los hallazgos verificados. Ninguna decisión se aplicó al manuscrito. Las opciones recomendadas permiten redactar una versión coherente sin cambiar los datos fuente.

## Cómo leer este archivo

- **Bloquea redacción:** indica si la decisión cambia cifras, signos o afirmaciones centrales.
- **Recomendación:** opción que mejor se ajusta a la evidencia disponible y al principio de no sobreafirmar.
- **Impacto:** lugares del manuscrito/README que dependen de la decisión.
- Las decisiones pueden aceptarse todas con la recomendación por defecto; las alternativas quedan documentadas para revisión.

---

## D-01 — Escenario principal para las conclusiones

**Pregunta:** ¿qué tratamiento de las respuestas no sustantivas se reporta como escenario principal?

| Opción | Definición | Consecuencia |
| --- | --- | --- |
| **A (recomendada)** | Fallo = 0: toda salida vacía, solo espacios, abstención, error, truncada o indeterminada recibe 0 en las tres evaluaciones. | Mide la utilidad del sistema completo. Es el escenario usado por el modelo ordinal de la corrección 01. |
| B | Puntajes observados de los jueces. | Conserva puntajes asignados a textos no sustantivos; algunos jueces puntuaron salidas vacías con valores > 0. No mide calidad jurídica. |
| C | Exclusión de no sustantivas. | Mide calidad condicional a que el sistema responda; es una submuestra seleccionada, no el efecto causal de la estrategia. |

**Recomendación:** A como principal; B y C como sensibilidad. Reportar siempre A y C juntos para la celda Agentic-RAG + gpt-5-nano, porque el signo del contraste cambia.

**Bloquea redacción:** sí.  
**Impacto:** resumen, Tabla 4, resultados, fortalezas/debilidades, conclusiones, README.  
**Evidencia:** `correccion-01.../INFORME_ANALISIS_ESTADISTICO.md` §2 y §5; `correccion-02.../INFORME_DIAGNOSTICO.md` §6.

---

## D-02 — Definición de “respuesta correcta” para el análisis de costos

**Pregunta:** ¿qué umbral se usa para calcular costo por respuesta correcta?

| Opción | Umbral | Ventaja | Riesgo |
| --- | --- | --- | --- |
| **A (recomendada)** | `puntaje_final_fallo_cero ≥ 0,75` | Coincide con “mayormente correcta” en la rúbrica y con el umbral usado en el análisis de probabilidad de la corrección 01. | Es una decisión normativa; no agota la calidad jurídica. |
| B | `≥ 0,50` | Incluye respuestas parcialmente correctas. | Puede contar como aceptable una respuesta con omisiones clave. |
| C | `= 1,00` | Exigencia máxima. | Reduce mucho el denominador y aumenta la sensibilidad al ruido de los jueces. |

**Recomendación:** A como principal; B y C en tabla de sensibilidad. No usar un único umbral sin declararlo. **Decisión aplicada:** A; “respuesta correcta” se define como puntaje promedio ≥ 0,75 y se documenta en `ANALISIS_COSTOS.md`.

**Bloquea redacción:** solo para la recomendación de costos; no para la inferencia principal.  
**Impacto:** `ANALISIS_COSTOS.md`, implicaciones prácticas, conclusión sobre “combinación costo-eficiente”.  
**Evidencia:** `datos/costo_por_respuesta_aceptable_umbrales.csv`.

---

## D-03 — Base de costos que se reporta

**Pregunta:** ¿se usan los costos registrados durante el experimento o se actualizan a precios corrientes?

| Opción | Definición | Consecuencia |
| --- | --- | --- |
| **A (recomendada)** | Costos registrados en los metadatos del experimento (precios de API del período, segundo semestre de 2025). | Permite reproducir exactamente el total de USD 22,29 y comparar las celdas bajo una misma tarifa histórica. |
| B | Precios actuales de los mismos modelos. | Puede cambiar el orden de eficiencia y no corresponde a lo ejecutado. Requiere nueva tabla y fecha de consulta. |

**Recomendación:** A. Aclarar que los valores son históricos y no una estimación de precios futuros.  
**Bloquea redacción:** sí, si se publican cifras en USD.  
**Impacto:** sección de costos, Tabla 4, README, conclusiones.  
**Evidencia:** `datos/costos_por_celda.csv`; `salidas/resumen_costos.json`; metadatos de `correccion-01`/`correccion-02`.

---

## D-04 — Cómo reformular la recomendación “costo-eficiente”

**Pregunta:** ¿se conserva una recomendación única o se reemplaza por una frontera de Pareto?

| Opción | Formulación | Evaluación |
| --- | --- | --- |
| **A (recomendada)** | No hay una combinación costo-eficiente única. Reportar frontera de Pareto y elegir según objetivo: menor costo puntual por respuesta correcta (RAG básico + nano; los IC bootstrap se solapan con Sin RAG + nano) o mayor calidad media (Agentic-RAG + gpt-5), con Agentic-RAG + mini como opción no dominada de calidad alta y costo intermedio. | Coherente con los datos: siete configuraciones son no dominadas; el costo por respuesta correcta y la calidad media no ordenan igual. |
| B | Mantener “Agentic-RAG + mini es la combinación costo-eficiente”. | Falso en sentido absoluto: cuesta USD 0,0564/consulta, más que RAG básico + gpt-5 (USD 0,0392) y Sin RAG + gpt-5 (USD 0,0478). Solo es más barata que Agentic-RAG + gpt-5 (USD 0,0792), con calidad media no distinguible. |
| C | Declarar “RAG básico + nano es la mejor combinación” por tener el menor costo puntual por respuesta correcta. | Es el menor costo puntual por respuesta correcta (USD 0,0061; IC bootstrap 0,0043–0,0091, solapado con Sin RAG + nano 0,0058–0,0107), pero su media es 0,599 y solo 33/79 respuestas alcanzan ≥ 0,75. No es “la mejor” en calidad. |

**Recomendación:** A. Si se necesita una frase prescriptiva: “Para minimizar el costo puntual por respuesta correcta, RAG básico + gpt-5-nano (sin diferencia formal con Sin RAG + nano); para maximizar calidad media, Agentic-RAG + gpt-5; Agentic-RAG + gpt-5-mini es una alternativa no dominada cuando se busca calidad alta con menor costo que gpt-5”.  
**Bloquea redacción:** sí, para la conclusión de costos y las implicaciones prácticas.  
**Impacto:** Tabla 4, sección de costos, conclusiones, README.  
**Evidencia:** `ANALISIS_COSTOS.md`; `datos/frontera_pareto.csv`; `datos/comparacion_recomendacion_anterior.csv`.

---

## D-05 — Etiqueta y estatus causal del fallo de Agentic-RAG + gpt-5-nano

**Pregunta:** ¿cómo se nombra el patrón de 41/79 salidas no sustantivas?

| Opción | Formulación | Evaluación |
| --- | --- | --- |
| **A (recomendada)** | “Modo de fallo de respuesta” o “fallo de respuesta no sustantiva”, con descripción de frecuencia y calidad condicional. | Describe lo observado sin atribuir causalidad. Es compatible con los logs: hay recuperación y tokens, pero el `final_result` es vacío o un marcador. |
| B | “Degradación del desempeño” o “baja calidad de gpt-5-nano”. | Confunde tasa de fallo con calidad de las respuestas producidas: cuando responde, la media es 0,820. |
| C | Conservar “sobrecarga agéntica” como hipótesis explícita. | Solo es aceptable si se rotula como hipótesis no contrastada y se elimina de contribuciones/conclusiones. No se recomienda porque sugiere una causa que no se midió. |

**Recomendación:** A. No usar “sobrecarga agéntica” como hallazgo ni como contribución.  
**Bloquea redacción:** sí.  
**Impacto:** resumen, Tabla 4, contribución 4, debilidades, conclusión, trabajos futuros, README.  
**Evidencia:** `correccion-02.../INFORME_DIAGNOSTICO.md` §3–§4; `datos/costos_por_celda.csv` (41 no sustantivas, 38 sustantivas, media condicional 0,820).

---

## D-06 — Asimetría de búsquedas 7/6 entre gpt-5 y mini/nano

**Pregunta:** ¿cómo se trata la diferencia de presupuesto de recuperación?

| Opción | Acción | Consecuencia |
| --- | --- | --- |
| **A (recomendada)** | Declarar la asimetría: gpt-5 usó un prompt con límite 7 y 33/79 sesiones agotaron 7 búsquedas; mini/nano usaron límite 6. No atribuir el efecto de modelo a capacidad sin esa salvedad. | No requiere nuevas llamadas; mantiene la trazabilidad histórica. |
| B | Repetir solo Agentic-RAG + gpt-5 con el prompt de 6 búsquedas en un directorio nuevo y actualizar el análisis. | Permite una comparación homogénea, pero requiere presupuesto, nuevas llamadas y rehacer la inferencia. |
| C | Omitir la diferencia y describir “6 búsquedas” como regla uniforme. | No es correcto: el log histórico muestra 7 en gpt-5. |

**Recomendación:** A para la versión definitiva, salvo que se apruebe B. Si se elige B, no sobrescribir `part_g/chat_data` ni los JSON históricos.  
**Bloquea redacción:** sí, para las afirmaciones sobre el efecto de modelo en Agentic-RAG.  
**Impacto:** Tabla 4 (interacción), interpretación de gpt-5, limitaciones, trabajos futuros.  
**Evidencia:** `correccion-04.../03_resolucion_contradicciones.md`; `correccion-04.../propuestas/cambios_manuscrito.md` §6–§8.

---

## D-07 — Versión del benchmark que se usa en las conclusiones

**Pregunta:** ¿se congela el benchmark experimental v1 o se aplican las correcciones detectadas por la corrección 06?

| Opción | Acción | Consecuencia |
| --- | --- | --- |
| **A (recomendada)** | Congelar v1 como instrumento efectivamente usado; publicar las correcciones como “benchmark v2 / versión revisada para futuras evaluaciones”. No volver a puntuar las respuestas existentes. | Las conclusiones describen el experimento realmente ejecutado. Las correcciones jurídicas quedan documentadas sin mezclar instrumentos. |
| B | Corregir el benchmark y volver a evaluar las respuestas con los jueces. | Permite una medición más válida, pero cambia el instrumento y requiere nuevas evaluaciones; no es comparable sin declararlo. |
| C | Corregir el benchmark en el anexo y presentarlo como si fuera el usado. | No es correcto: oculta que las respuestas fueron generadas y evaluadas con v1. |

**Recomendación:** A. En el texto: “las conclusiones corresponden al benchmark v1; las correcciones detectadas se documentan como v2 y no se aplicaron retroactivamente”.  
**Bloquea redacción:** sí, para el objetivo 3 y la contribución del benchmark.  
**Impacto:** objetivo 3, contribución benchmark, limitaciones, anexo, README.  
**Evidencia:** `correccion-06.../resumen_ejecutivo.md`; `correccion-06.../salidas/propuestas_benchmark.csv`.

---

## D-08 — Validación humana de los jueces

**Pregunta:** ¿se declara la ausencia de validación humana o se realiza una nueva submuestra?

| Opción | Acción | Consecuencia |
| --- | --- | --- |
| **A (recomendada)** | Declarar que no hubo validación humana; reportar acuerdo inter-juez como confiabilidad, no validez. | Es lo que permiten los datos actuales. No bloquea la defensa si se explicita. |
| B | Realizar una submuestra ciega con uno o dos profesionales y actualizar la conclusión. | Agrega evidencia de validez, pero requiere tiempo, acuerdo y nuevo análisis; no debe presentarse como validación completa si la muestra es pequeña. |

**Recomendación:** A para la versión definitiva; B como trabajo futuro o refuerzo si hay disponibilidad.  
**Bloquea redacción:** sí, para cualquier frase que use “validado”.  
**Impacto:** contribución LLM-as-a-Judge, limitaciones, conclusión, README.  
**Evidencia:** `correccion-02.../INFORME_DIAGNOSTICO.md` §5; `correccion-01.../INFORME_ANALISIS_ESTADISTICO.md` §9.

---

## D-09 — Título y alcance del sistema

**Pregunta:** ¿se cambia el título para reflejar que se evalúa un solo Código y un prototipo sin interfaz?

| Opción | Acción | Consecuencia |
| --- | --- | --- |
| **A (recomendada, si la institución lo permite)** | “Desarrollo y evaluación de un prototipo Agentic-RAG para consulta del Código de Minería argentino”. | Alinea título, objetivo y alcance; requiere actualizar portada, `main.typ`, README y BibTeX. |
| B | Mantener el título aprobado y agregar una declaración de alcance en resumen, introducción y conclusiones. | No requiere trámite institucional, pero el título sigue siendo más amplio que la evidencia. |
| C | Mantener el título y afirmar que el sistema se evaluó para “normativa nacional” en general. | No se sostiene: solo se evaluó un código. |

**Recomendación:** A si es viable; B en caso contrario. Nunca C.  
**Bloquea redacción:** sí, para el alcance del resumen y la conclusión sobre usuarios.  
**Impacto:** título, resumen, objetivo general, conclusión, README, BibTeX.  
**Evidencia:** valoración del jurado §V.11; `manuscrito/main.typ`; `02_capitulo_01_introduccion.typ` líneas 103–105.

---

## D-10 — Estatus del objetivo 2 (sistema de agentes)

**Pregunta:** ¿cómo se declara el cumplimiento del objetivo 2?

| Opción | Formulación | Evaluación |
| --- | --- | --- |
| **A (recomendada)** | “Cumplimiento parcial: dos agentes activos y una delegación nominal; el Agente de Calidad no se ejecutó y no hay verificación iterativa.” | Refleja la implementación observada. |
| B | “Cumplido con alcance reducido: se implementó la coordinación recuperación–generación, sin verificador.” | Es admisible si se explicita que no se cumplió el ciclo multi-agente completo. |
| C | “Cumplido completamente.” | No se sostiene: el tercer agente no participó y el especialista no itera. |

**Recomendación:** A o B; nunca C.  
**Bloquea redacción:** sí.  
**Impacto:** objetivo 2, contribución del sistema, conclusión.  
**Evidencia:** `correccion-04.../03_resolucion_contradicciones.md`; `correccion-04.../propuestas/cambios_manuscrito.md` §10.

---

## D-11 — Acceso público y reproducibilidad

**Pregunta:** ¿se considera cumplido el objetivo de acceso público?

| Opción | Formulación | Evaluación |
| --- | --- | --- |
| **A (recomendada)** | “Acceso público verificado sin login; la clonación y ejecución se recomiendan como verificación de reproducibilidad.” | Coincide con la decisión del autor: el acceso desde el navegador está resuelto; la reproducibilidad exacta no se presume. |
| B | “Cumplido completamente: código y metodología publicados.” | Solo si se ejecuta la clonación anónima, se compila el manuscrito y se corre el análisis base antes de la entrega. |
| C | “Repositorio privado / no disponible.” | Ya no corresponde: la URL pública respondió 200 y la API de GitHub informó `private: false` el 2026-11-11. |

**Recomendación:** A. El acceso público se considera cumplido; la clonación se recomienda para reproducibilidad, no como bloqueo.  
**Bloquea redacción:** sí, para el objetivo 4 y la frase “replicable”.  
**Impacto:** objetivo 4, contribución de metodología, reflexiones finales, README, anexo.  
**Evidencia:** verificación pública del 2026-11-11; `plan_correcciones_y_recomendaciones.md` IX.1.8.

---

## D-12 — Tipo de índice vectorial

**Pregunta:** ¿se conserva “IVF_FLAT” en la conclusión del objetivo 1?

| Opción | Acción | Consecuencia |
| --- | --- | --- |
| **A (recomendada)** | Eliminar “IVF_FLAT” y describir “índice `AUTOINDEX` con similitud coseno”. | Coincide con el código de creación de la base y con la decisión del autor. |
| B | Verificar en Milvus el índice efectivo (`describe_index`) y reportar el tipo real. | Es la única forma de conservar “IVF_FLAT” con respaldo. |
| C | Mantener “IVF_FLAT” porque el manuscrito lo afirma. | No hay evidencia suficiente en el repositorio; no se recomienda. |

**Recomendación:** A. Se documenta `AUTOINDEX`; no se afirma un parámetro de índice no verificado.  
**Bloquea redacción:** no bloquea la conclusión principal, pero afecta el objetivo 1.  
**Impacto:** objetivo 1, metodología, anexo.  
**Evidencia:** `part_c/01_initial_vector_db_creation.ipynb` usa `AUTOINDEX`; plan IX.1.6/IX.2.1.

---

## D-13 — Afirmación de “primer sistema”

**Pregunta:** ¿se conserva la prioridad “primer sistema de este tipo”?

| Opción | Formulación | Evaluación |
| --- | --- | --- |
| **A (recomendada)** | “No se identificaron antecedentes públicos comparables en la búsqueda realizada.” | Es una afirmación acotada y verificable; no exige un censo exhaustivo. |
| B | “Primer sistema Agentic-RAG de código abierto aplicado a normativa argentina.” | Es una afirmación fuerte; requiere una búsqueda sistemática y una fecha de corte. |

**Recomendación:** A.  
**Bloquea redacción:** no; es una decisión de prudencia.  
**Impacto:** contribución del sistema, introducción, README.  
**Evidencia:** búsqueda bibliográfica del manuscrito; no se dispone de un censo exhaustivo en este paquete.

---

## D-14 — Alpha de Krippendorff que se reporta

**Pregunta:** ¿qué valor de alpha se cita para la rúbrica de corrección?

| Opción | Valor | Observación |
| --- | --- | --- |
| **A (recomendada)** | Reportar ambos: 0,808 con puntajes originales y 0,800 después de transformar los valores fuera de rúbrica al valor más cercano. | Es transparente y evita que la transformación parezca inocua. |
| B | 0,808 (valores originales). | Coincide con el manuscrito actual; no refleja la transformación usada en el análisis ordinal. |
| C | 0,800 (rúbrica transformada). | Coincide con la base del modelo; difiere del valor actual del manuscrito. |

**Recomendación:** A. La conclusión no debe depender de la diferencia 0,808/0,800: en ambos casos el acuerdo es bueno, pero no es validación humana. **Decisión aplicada:** A, con recálculo independiente en `verificacion-analisis-estadistico/`.  
**Bloquea redacción:** no para la conclusión cualitativa; sí para la cifra exacta.  
**Impacto:** sección de acuerdo inter-juez, conclusión, README.  
**Evidencia:** cálculo reproducido sobre `correccion-01.../datos/02_long_2133.csv` (`score_raw` = 0,807842; `score_rubric` = 0,799542).

---

## Resumen de decisiones recomendadas

| ID | Decisión | Recomendación | Decisión autor |
| --- | --- | --- | --- |
| D-01 | Escenario principal | Fallo = 0, con sensibilidad de exclusión; sin calificaciones humanas de respuestas |  Fallo = 0, con sensibilidad de exclusión para la realización de las pruebas estadísticas que evalúan al sistema. La corrección humana predomina sobre la del LLM-as-a-Judge. Se debe documentar la discrepancias de los jueves con el criterio humano|
| D-02 | Umbral de respuesta correcta | ≥ 0,75, con sensibilidad 0,5 y 1,0 | "Opción A" documentando la decisión de lo que se considera "respuesta correcta" |
| D-03 | Base de costos | Costos registrados del experimento | "Opción A" |
| D-04 | Recomendación de costos | Sin ganador único; Pareto y objetivo explícito | "Opción A" |
| D-05 | Etiqueta del fallo nano | “Modo de fallo de respuesta”, sin causalidad | "Opción A" |
| D-06 | Asimetría 7/6 | Declararla; no atribuir a capacidad sin salvedad | "Opción A" |
| D-07 | Benchmark | Congelar v1; revisión LLM detectó posibles errores que requieren revisión profesional | "Opción A": Congelar el benchmark y aclarar que luego de una nueva revisión por un modelo LLM (ollama-cloud:deepseek-v4.1-flash:1017-cloud) se detectaron posibles errores que requieren una nueva revisión por un profesional del derecho |
| D-08 | Validación humana | Declarar ausencia; documentar 23 discrepancias y 17 evaluaciones positivas no sustantivas | "Opción A": vincular conclusiones con lo observado en D-01 |
| D-09 | Título/alcance | Título actualizado al alcance real | "Opción A": actualizar el título para subsanar los comentarios en "V.11 Título, objetivos, alcance y reproducibilidad" del archivo de valoración |
| D-10 | Objetivo 2 | Cumplimiento parcial; objetivo específico actualizado | "Opción A": actualizar el objetivo para subsanar los comentarios en "V.11 Título, objetivos, alcance y reproducibilidad" del archivo de valoración |
| D-11 | Repositorio | Acceso público verificado sin login; clonación recomendada para reproducibilidad | Considerar resuelto ya que se puede acceder desde el explorador web sin necesidad de login en github |
| D-12 | Índice | AUTOINDEX con similitud coseno; quitar “IVF_FLAT” | Quitar “IVF_FLAT” y mencionar que se empleó AUTOINDEX como se respalda en el código de generación de la base de datos |
| D-13 | “Primer sistema” | “No se identificaron antecedentes” | "Opción A" |
| D-14 | Alpha | Verificado en `verificacion-analisis-estadistico/`: 0,807842 y 0,799542 | "Opción A": antes de usar ese valor se debe recalcular con los resultados originales de los jueces, sin editar los archivos originales. Replicar los análisis en un nuevo directorio `analisis-valoracion-jurado/verificacion-analisis-estadistico` |

Si se aceptan las recomendaciones, las propuestas de `PROPUESTA_TEXTO_MANUSCRITO.md` y `PROPUESTA_TEXTO_README.md` pueden aplicarse sin cambiar ningún dato fuente. Si se elige una alternativa, deben ajustarse las frases marcadas con el ID correspondiente.

---

## Implementación de las decisiones aceptadas

Esta sección registra cómo se aplicaron las decisiones del autor en los artefactos de `correccion-05-actualizacion-conclusiones-y-analisis-costos`. No modifica las decisiones originales ni el manuscrito.

| ID | Decisión aplicada | Implementación en el paquete | Observación |
| --- | --- | --- | --- |
| D-01 | Fallo = 0, con sensibilidad de exclusión; criterio humano como referencia | Se mantiene el escenario principal y la sensibilidad. Se agrega la aclaración de que no existen calificaciones humanas de las 711 respuestas; la revisión humana del benchmark es la referencia del instrumento. Se documentan 23 discrepancias entre jueces para revisión humana. | No se afirma que la “corrección humana” prevalezca sobre los jueces en la medición de respuestas, porque esa medición humana no existe. |
| D-02 | Opción A: ≥ 0,75, con sensibilidad 0,5 y 1,0; documentar qué se considera “respuesta correcta” | Se define “respuesta correcta” como puntaje promedio de los tres jueces ≥ 0,75, equivalente a “mayormente correcta” en la rúbrica. Se mantiene la sensibilidad a 0,50 y 1,00. | Es una operacionalización normativa; no una verdad jurídica. Los nombres internos `aceptables_075` se conservan por compatibilidad. |
| D-03 | Opción A: costos registrados | Se mantienen los costos históricos del experimento y se advierte que no son precios corrientes. | Total: USD 22,2939. |
| D-04 | Opción A: sin ganador único; Pareto y objetivo explícito | Se reemplaza la recomendación única por Pareto, costo por respuesta correcta y elección según objetivo. | RAG básico + nano es el menor costo puntual por respuesta correcta, con IC solapado con Sin RAG + nano. |
| D-05 | Opción A: “modo de fallo de respuesta”, sin causalidad | Se elimina “sobrecarga agéntica” como hallazgo y se describe 41/79 no sustantivas y la calidad condicional. | No se atribuye a la complejidad agéntica. |
| D-06 | Opción A: declarar asimetría 7/6 | Se declara que gpt-5 usó 7 búsquedas y mini/nano 6; se advierte que el efecto de modelo no se atribuye a capacidad sin esa salvedad. | No se reejecutó la corrida. |
| D-07 | Congelar v1; nueva revisión LLM detectó posibles errores que requieren revisión profesional | Se actualizan objetivo 3, contribución del benchmark y limitaciones para decir “benchmark v1 congelado” y mencionar la revisión con `ollama-cloud:deepseek-v4.1-flash:1017-cloud`. | No se aplicaron correcciones retroactivas ni se volvió a puntuar. |
| D-08 | Opción A: declarar ausencia de validación humana; vincular con D-01 | Se reporta α como confiabilidad y se aclara que no hay validación humana de respuestas; se documentan 23 discrepancias y 17 evaluaciones positivas sobre salidas no sustantivas. | La revisión humana del benchmark no es validación de los jueces. |
| D-09 | Opción A: actualizar el título | Se propone “Desarrollo y evaluación de un prototipo Agentic-RAG para consulta del Código de Minería argentino” y se actualizan portada, `main.typ`, README y BibTeX. | Requiere aprobación institucional si el título ya está registrado. |
| D-10 | Opción A: objetivo 2 parcial | Se propone un objetivo específico 2 acotado a dos agentes activos, sin ciclo iterativo de verificación; la conclusión declara cumplimiento parcial. | El Agente de Calidad no se ejecutó. |
| D-11 | Acceso público resuelto sin login | Se declara el repositorio público accesible desde el navegador sin autenticación. La clonación y ejecución se recomiendan como verificación de reproducibilidad, no como bloqueo del objetivo de acceso. | El acceso se verificó el 2026-11-11. |
| D-12 | Quitar “IVF_FLAT” y mencionar AUTOINDEX | Se reemplaza “IVF_FLAT” por “índice AUTOINDEX con similitud coseno”, respaldado en `part_c/01_initial_vector_db_creation.ipynb`. | No se afirma un parámetro de índice no verificado. |
| D-13 | Opción A: “no se identificaron antecedentes” | Se reemplaza “primer sistema” por “no se identificaron antecedentes públicos comparables en la búsqueda realizada”. | Se mantiene la cautela. |
| D-14 | Recalcular alpha desde jueces originales en un directorio nuevo | Se creó `analisis-valoracion-jurado/verificacion-analisis-estadistico/`. α = 0,807842 (corrección original) y 0,799542 (rúbrica); α = 0,784566 para precisión legal original. Coinciden con la corrección 01. Se documentan 23 discrepancias y 17 evaluaciones positivas no sustantivas. | No se modificaron archivos originales. |

### Nota de implementación sobre D-01 y D-08

La decisión del autor indica que “la corrección humana predomina sobre la del LLM-as-a-Judge” y que deben documentarse las discrepancias con el criterio humano. En los datos disponibles:

- existe una revisión humana del benchmark (preguntas, respuestas esperadas y referencias);
- **no existen calificaciones humanas de las 711 respuestas generadas**;
- por lo tanto, no es posible afirmar que la corrección humana prevalezca sobre los jueces en la medición de las respuestas, ni calcular acuerdo humano–juez.

La implementación adoptada es: usar la revisión humana del benchmark como referencia principal del instrumento, reportar el α como confiabilidad entre jueces, no como validación, y dejar los 23 casos de discrepancia como insumo para una revisión humana futura. Si se obtiene una submuestra humana, este texto deberá actualizarse.

### Nota de implementación sobre D-14

La verificación independiente está en:

`analisis-valoracion-jurado/verificacion-analisis-estadistico/`

Allí se recalcula el alpha desde `codigo_experimentos/part_i/final_judge_results.csv`, sin usar como insumo la tabla derivada de la corrección 01. Los resultados y los casos para revisión humana están en `datos/` y `salidas/resumen_verificacion.json`.

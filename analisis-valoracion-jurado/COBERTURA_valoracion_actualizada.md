# Cobertura de la valoración actualizada y efecto sobre las decisiones

**Fecha:** 2026-11-12.  
**Documento comparado:** `Valoracion_TF_Spairani_gp_actualizada.docx` / `.md`.  
**Paquetes existentes:** `correccion-01` a `correccion-07` y `verificacion-analisis-estadistico`.  
**Registro de decisiones:** `DECISIONES_integradas.md` (D-01–D-14, PI-01–PI-32 y NV-01–NV-07).

## 1. Conclusión ejecutiva

**La cobertura es alta, pero no completa.**

Los paquetes existentes cubren el núcleo analítico que la nueva valoración considera indispensable:

- análisis apareado y anidado;
- diagnóstico de la celda gpt-5-nano;
- corrección del join de los casos 23–25;
- temperatura, determinismo y ejecución única;
- factores confundidos y prompts;
- reformulación de la Tabla 4;
- corpus, benchmark y bibliografía.

Sin embargo, la nueva valoración **agrega o eleva a requerimiento** cuatro materias que los paquetes actuales no cierran:

1. **Métricas de recuperación** (IX.1.9 y V.8).
2. **Evaluación aislada del embedding y comparación con BM25/recuperador alternativo** (IX.2.1).
3. **Métricas deterministas de citas sobre las respuestas generadas** (IX.2.2).
4. **Declaración ampliada de uso de IA** (IX.1.8 y V.11).

Además, siguen abiertas las recomendaciones de validación humana, réplicas/ablación y reducción de capítulos, que ya estaban identificadas como pendientes y no forman parte de los paquetes cerrados.

**Ninguna decisión D-01–D-14 queda invalidada.** D-01 quedó aclarada por el autor: la “corrección humana” es la revisión manual de categorías, no una calificación humana de calidad. **D-12 quedó resuelta con NV-06:** se usa AUTOINDEX del código y no se afirma IVF_FLAT. Las decisiones PI-04, PI-06, PI-07, PI-08, PI-29 y PI-31 fueron resueltas o ampliadas; el detalle está en `DECISIONES_integradas.md` §6.

---

## 2. Cobertura de las observaciones V.1–V.11

| Sección nueva | Qué exige | Paquete que la cubre | Estado | Observación |
|---|---|---|---|---|
| V.1 | Reanálisis apareado/anidado, efectos e IC; corregir “modelos mixtos” | `correccion-01` | **Cubierto con salvedad** | El modelo ordinal mixto, Friedman/Wilcoxon y bootstrap existen. Las cifras nuevas de la valoración no coinciden exactamente con las de `correccion-01`; hay que reconciliar prueba, escenario y corrección (NV-01) |
| V.2 | Crítica a Scheirer-Ray-Hare | `correccion-01` | **Cubierto** | Se reemplaza por el modelo ordinal y análisis no paramétrico de sensibilidad |
| V.3 | No inferir equivalencia de la falta de significación | `correccion-01`; `correccion-05` | **Cubierto** | Se reportan IC y se retira el “efecto igualador” |
| V.4 | Temperatura no aplicada, no determinismo, esfuerzo y ejecución única | `correccion-03` | **Cubierto con salvedad** | La temperatura no se envía y la ejecución es única; se usó el valor por defecto de la API: Pydantic AI 1.1.0 no fija `reasoning_effort` y OpenAI documenta `medium` para GPT-5 (NV-05) |
| V.5 | Factores confundidos, prompts, Agente de Calidad, límite de búsquedas | `correccion-04`; `correccion-05` | **Cubierto** | Quedan decisiones de redacción: 7/6, `16_01` y notebook canónico (PI-10, PI-11) |
| V.6 | 41 salidas no sustantivas, reincorporar casos 23–25, corregir faltantes, reformular sobrecarga | `correccion-02`; `correccion-01`; `correccion-05` | **Cubierto** | La base final tiene 58 no sustantivas y 41 en nano agéntico; el join 23–25 está resuelto. Las medias 0,82/0,84/0,64 se reproducen; los valores `p = 0,19` y `p = 0,003` no coinciden exactamente con las pruebas pareadas locales y deben documentarse (método, unidad y corrección). Falta editar el manuscrito |
| V.7 | Validez del benchmark, respuestas de referencia y jueces; citas deterministas; submuestra humana | `correccion-06`; `verificacion-analisis-estadistico`; `correccion-05` | **Parcial** | Hay auditoría de referencias y evidencia de jueces; no hay métricas de citas sobre respuestas generadas ni validación humana (NV-03) |
| V.8 | Evaluar recuperación; comparar embedding/BM25 | `part_d` y datos de `correccion-06`; no hay notebook en los paquetes | **Parcial** | Las métricas de RAG básico se reproducen desde `part_d`: recall@10 0,333; MRR 0,214; 27,8 % con todos los artículos; 59,5 % sin ninguno. Falta el artefacto reproducible y la comparación con BM25/otro embedding (NV-02) |
| V.9 | Versión y calidad del corpus | `correccion-06` | **Cubierto con salvedad** | Versión, conteos y linaje están auditados; la calidad de extracción no se cuantificó con tasa de error, solo con comparación de artículos clave |
| V.10 | Costos, Pareto y recomendación | `correccion-05` | **Cubierto** | Costos históricos, frontera de Pareto y costo por respuesta ≥ 0,75 |
| V.11 | Título, alcance, repositorio y declaración de IA | `correccion-05`; verificación pública | **Parcial** | Título/objetivo están propuestos; el repositorio es público; la declaración de IA sigue pendiente (NV-04) |

---

## 3. Cobertura de las correcciones requeridas IX.1

| Punto | Estado | Evidencia / faltante |
|---|---|---|
| IX.1.1 Rehacer inferencia y corregir modelos mixtos | **Cubierto** | `correccion-01`; modelo ordinal, Friedman/Wilcoxon, efectos e IC |
| IX.1.2 Informar 41 salidas, reincorporar 23–25, corregir faltantes | **Cubierto** | `correccion-02` y `correccion-01`; falta trasladarlo al manuscrito |
| IX.1.3 Retirar determinismo, informar esfuerzo y ejecución única | **Cubierto con salvedad** | `correccion-03` demuestra que la temperatura no se envía. `reasoning_effort` no se envió; el default efectivo del proveedor es `medium`, aunque no quedó registrado localmente |
| IX.1.4 Declarar confundidos, prompts y contradicciones | **Cubierto** | `correccion-04`; quedan decisiones editoriales menores (7/6, `16_01`, notebook) |
| IX.1.5 Reformular Tabla 4 y conclusiones | **Cubierto como propuesta** | `correccion-05`; no se editó el manuscrito |
| IX.1.6 Corpus, origen y respuestas de referencia | **Cubierto en análisis** | `correccion-06`; 1.2/1.3 verificados; Q23–Q25 fuera de alcance |
| IX.1.7 Tablas 2 y 3, auditoría bibliográfica | **Cubierto** | `correccion-07`; quedan decisiones manuales de autoría/DOI/fuente |
| IX.1.8 Ampliar declaración de IA | **No cubierto** | Solo existe la propuesta general de `correccion-05`; falta una declaración por etapas y revisar el antecedente de la “referencia fabricada” que menciona la nueva valoración |
| IX.1.9 Informar métricas de recuperación | **Parcial** | Los datos están en `part_d` y los logs; las cifras de RAG básico se reproducen, pero no hay notebook/CSV de resultados en los paquetes. Falta un artefacto propio (NV-02) |

---

## 4. Cobertura de las recomendaciones IX.2

| Punto | Estado | Evidencia / faltante |
|---|---|---|
| IX.2.1 Comparar embedding con recuperador entrenado y BM25/híbrido | **No cubierto** | Solo existe la propuesta en el plan; no hay notebook ni resultados |
| IX.2.2 Precisión/exhaustividad de citas y citas inexistentes | **Parcial** | `correccion-06` extrae citas de las respuestas esperadas del benchmark (`unidades_benchmark.csv`, `citas_respuestas.csv`), no de las respuestas generadas por el sistema. No hay precisión/recall/F1 ni tasa de citas inexistentes sobre las 711 respuestas |
| IX.2.3 Validación humana de jueces | **No cubierto** | Sigue pendiente; la revisión de 87 filas es del autor y la del benchmark es de una profesional, no de las respuestas generadas |
| IX.2.4 Réplicas y ablación | **No cubierto** | `correccion-04` analiza el diseño, pero no se ejecutaron réplicas ni sustitución controlada |
| IX.2.5 Reducir capítulo 2 y sección 7.7 | **No cubierto** | Tarea editorial; no hay edición del manuscrito |

---

## 5. Efecto sobre las decisiones tomadas D-01–D-14

| Decisión | Efecto de la nueva valoración | Acción |
|---|---|---|
| D-01 Fallo = 0 y exclusión como sensibilidad | **Aclarada; dos planos** | La nueva V.6 confirma que las salidas vacías se calificaron con cero. Para el sistema se usa fallo = 0; para la auditoría de jueces se conservan los valores originales y se critican los puntajes > 0 sobre no sustantivas. Mantener |
| D-02 “Respuesta correcta” ≥ 0,75 | **Sin cambio** | No es objeto de la nueva valoración |
| D-03 Costos históricos | **Sin cambio; confirmada** | El Anexo A1 dice que el total USD 22,29 coincide con los registros |
| D-04 Pareto y costo por respuesta correcta | **Sin cambio** | V.10 no se modifica |
| D-05 “Modo de fallo”, no “sobrecarga agéntica” | **Sin cambio; refinada** | La nueva V.6 habla de falla del canal de salida estructurada; puede precisarse la etiqueta, pero no se revierte |
| D-06 Declarar asimetría 7/6 | **Sin cambio; confirmada** | La nueva V.5 repite 7 para gpt-5 y 6 para mini/nano |
| D-07 Congelar benchmark v1 y revisar con profesional | **Sin cambio** | La nueva valoración no modifica el alcance del benchmark; la revisión profesional sigue pendiente |
| D-08 Sin validación humana; alpha como confiabilidad | **Sin cambio; reforzada** | V.7 agrega un indicio de puntajes altos a respuestas vacías |
| D-09 Actualizar título y alcance | **Sin cambio; reforzada** | V.11 mantiene la crítica al título/objetivo amplio |
| D-10 Objetivo 2 parcial | **Sin cambio; confirmado** | V.5 y Tabla 4 describen dos agentes y ausencia de verificador |
| D-11 Acceso público resuelto | **Sin cambio en lo sustantivo; añadir matiz** | La nueva V.11 confirma el acceso, pero señala que el historial empieza en junio de 2026 y no documenta la evolución experimental. Mantener “acceso público sí; reproducibilidad exacta no demostrada” |
| D-12 AUTOINDEX, quitar IVF_FLAT | **Resuelta con NV-06** | Se adopta AUTOINDEX, el valor del código; no se afirma IVF_FLAT |
| D-13 “No se identificaron antecedentes” | **Sin cambio** | No es objeto de la nueva valoración |
| D-14 Alpha 0,807842/0,799542 | **Sin cambio** | La nueva valoración no discute el alpha; la verificación independiente sigue vigente |

---

## 6. Efecto sobre las decisiones pendientes PI-01–PI-32

| Grupo | Efecto | Prioridad |
|---|---|---|
| PI-01 Ubicación de paquetes | Sin cambio | Media |
| PI-02 Título/alcance | Reforzada por V.11 | Alta |
| PI-03 Paquete 04 (textos, diagrama, anexo) | Reforzada por V.5 | Alta |
| PI-04 Declaración de IA | **Resuelta: opción B**; declaración por etapas y antecedente de la referencia fabricada | Alta |
| PI-05 Terminología “modelo del especialista” | Reforzada por V.5 | Media |
| PI-06 Validación humana de jueces | D-01 ya no depende de esto; V.7 agrega evidencia de puntajes altos a respuestas vacías | Alta |
| PI-07 Independencia de la revisión de categorías | Reforzada: V.7 dice una sola profesional | Media |
| PI-08 23 discrepancias/17 positivas | Reforzada por V.7 (tres respuestas vacías) | Media |
| PI-09 Nuevas corridas | Sin cambio; la nueva valoración no las exige para aceptar, pero siguen siendo necesarias para causalidad/réplicas | Media |
| PI-10 Excepción `16_01` | Sin cambio | Baja |
| PI-11 Notebook `part_g` | Sin cambio; V.11 valora el repositorio, no la discrepancia notebook/script | Media |
| PI-12 Procedencia Infoleg | **Resuelta**; V.9 no se actualizó; sin acción pendiente | — |
| PI-13–PI-20 Benchmark/corpus | **Reclasificadas:** PI-16 y PI-18 resueltas; PI-13, PI-14, PI-17 y PI-20 canceladas por estar fuera de alcance; PI-15 y PI-19 resueltas con implementación editorial pendiente. PI-12 se registra en la fila anterior | Alta/Media |
| PI-21–PI-28 Bibliografía | **Resueltas:** PI-21, PI-22, PI-23, PI-26, PI-27 y PI-28 con opción A; PI-24 con opción A usando la página institucional verificada (el endpoint directo del buscador no responde desde este entorno); PI-25 con las cinco entradas y claves actualizadas | Alta/Media |
| PI-29 `nAGQ`/odds proporcionales | **Resuelta: opción A**; mantener `nAGQ = 1` (Laplace) y declarar la limitación. `nAGQ > 1` no está disponible con dos efectos aleatorios | Media |
| PI-30 Versionar verificación | **Resuelta: opción A**; publicar después de revisar el manuscrito y ordenar el directorio | Alta |
| PI-31 Sincronización final | **Resuelta: opción A**; aplicar todo y generar una nueva versión del archivo | Alta |
| PI-32 Conteo de preguntas corregidas | **Resuelta**; V.7 confirma 18/17/1/7 | — |

---

## 7. Nuevas decisiones incorporadas (NV-01–NV-07)

El estado actualizado está en `DECISIONES_integradas.md` §6: todas las NV están resueltas salvo NV-03, que queda pendiente y no prioritaria.

| ID | Decisión | Opciones | Recomendación | Bloquea |
|---|---|---|---|---|
| NV-01 | ¿Qué reanálisis se usa como fuente canónica: el de `correccion-01` o el de la nueva valoración? | A) `correccion-01` (modelo ordinal + Friedman/Wilcoxon); B) reanálisis de la valoración; C) reportar ambos y reconciliar | **A adoptada:** `correccion-01` es la fuente canónica; no usar el reanálisis de la valoración | Sí, para Tabla 4 y resultados |
| NV-02 | Métricas de recuperación y comparación de recuperadores | A) Calcular desde `part_d` y logs en un notebook nuevo; B) adoptar las cifras de la nueva valoración; C) ambas | **A adaptada:** Milvus no está disponible; calcular recall@k/MRR desde las recuperaciones `.json` y guardar en `verificacion-analisis-estadistico/metricas_recuperacion/`. No comparar BM25 desde la base | Sí, para IX.1.9/IX.2.1 |
| NV-03 | Métricas deterministas de citas sobre las 711 respuestas | A) Extender `correccion-06` para extraer citas de las respuestas generadas y calcular precisión/recall/F1/inexistentes; B) usar solo las citas de las respuestas esperadas; C) dejar la rúbrica de jueces | **No prioritaria por tiempo:** posponer; no bloquea la entrega | No para la entrega |
| NV-04 | Declaración de IA y antecedente de “referencia fabricada” | A) Declaración por etapas + revisión del historial; B) mantener la frase genérica; C) declaración mínima sin explicar el antecedente | **A adoptada:** extender la declaración a búsqueda bibliográfica, escritura, validación de citas, implementación y otras tareas; revisar el antecedente al redactar | Sí, para IX.1.8 |
| NV-05 | “Esfuerzo predeterminado” vs. “desconocido” | A) Mantener “desconocido” (lo que prueban los logs); B) afirmar “predeterminado” porque el código no lo fija; C) documentar ambos | **Resuelta:** se usó el valor por defecto de la API. Pydantic AI 1.1.0 no fija `reasoning_effort` y envía `NOT_GIVEN`; el default efectivo de OpenAI para GPT-5 es `medium`; declarar “default del proveedor = medium”, no un default de Pydantic AI | No para aceptar; sí para precisión |
| NV-06 | Índice vectorial: IVF_FLAT vs. AUTOINDEX | A) Mantener D-12 y describir AUTOINDEX; B) verificar en Milvus el índice efectivo; C) aceptar IVF_FLAT de la nueva valoración | **A adoptada:** usar AUTOINDEX del código; no afirmar IVF_FLAT | Sí, para coherencia de V.8/metodología |
| NV-07 | Actualización de Tabla 4/IX con los nuevos hallazgos | A) Incorporar recuperación, IA y cifras reconciliadas; B) dejar Tabla 4 como está y agregar anexo; C) solo cambios de forma | **A.** La nueva valoración cambia el sustento de V.1/V.6/V.8/V.11; Tabla 4 debe reflejarlo | Sí, para la versión final |

---

## 8. Estado tras las decisiones

| Punto | Estado |
|---|---|
| NV-01 Reanálisis canónico | **Decidida (A):** `correccion-01`; falta implementar la reconciliación |
| Edición del manuscrito | **Pendiente:** aplicar las correcciones 01–07 |
| NV-04 Declaración de IA | **Decidida (A):** extender la declaración; falta redactarla y revisar el antecedente |
| PI-02 / PI-06 / PI-08 | **Decididas:** título aprobado, sin validación humana adicional, casos adjudicados; falta implementarlas |
| NV-06 Índice vectorial | **Resuelta (A):** AUTOINDEX del código; no usar IVF_FLAT |
| NV-02 Recuperación | **Decidida (A adaptada):** sin Milvus; usar recuperaciones `.json` en `verificacion-analisis-estadistico/metricas_recuperacion/` |
| NV-03 Citas deterministas | **No prioritaria:** posponer por tiempo |
| PI-25 DOIs de edición | **Resuelta:** cinco entradas adoptadas y claves/citas actualizadas; PDF compilado |
| NV-05 Esfuerzo de razonamiento | **Resuelta:** valor por defecto de la API; Pydantic AI 1.1.0 no fija `reasoning_effort` y OpenAI GPT-5 usa `medium` por defecto. No se registró localmente |
| PI-31 Sincronización final | **Decidida (A):** aplicar todo y generar una nueva versión |

## 9. Veredicto de cobertura

- **Núcleo metodológico:** cubierto.
- **Diagnóstico de la celda anómala y faltantes:** cubierto.
- **Corpus, benchmark y bibliografía:** cubierto en análisis, con revisiones jurídicas pendientes.
- **Recuperación:** datos verificables; decisión NV-02 adaptada a los `.json`, falta el artefacto propio y no hay comparación BM25 por pérdida de Milvus.
- **Citas deterministas:** parcial; solo respuestas esperadas, no respuestas generadas. NV-03 queda no prioritaria.
- **Validación humana, réplicas y reducción editorial:** no cubierto.
- **Declaración de IA:** decidida (PI-04/NV-04), pendiente de implementación.

Por tanto, **el trabajo existente permite responder la mayor parte de la nueva valoración, pero no alcanza para declarar cobertura total**. La nueva valoración no invalida las decisiones tomadas; refuerza varias y agrega las decisiones NV-01 a NV-07.

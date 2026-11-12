# Decisiones integradas pendientes

**Fecha de verificación:** 2026-11-12.  
**Alcance:** directorios `correccion-01` a `correccion-07` y `verificacion-analisis-estadistico` de `analisis-valoracion-jurado/`.  
**Objetivo:** reunir en un solo registro las decisiones que todavía requieren una elección, sin reabrir las decisiones ya aceptadas ni convertir tareas de edición en falsas alternativas.

**Regla de trabajo:** las fuentes, respuestas, logs, evaluaciones y archivos históricos no se modifican. Toda decisión se implementa en artefactos nuevos y, cuando corresponda, en el manuscrito/README mediante una edición explícita y trazable.

---

## 1. Verificación de los directorios

### 1.1 Inventario y estado

| Directorio | Qué contiene | Verificación realizada | Estado | Pendiente principal |
|---|---|---|---|---|
| `correccion-01-analisis-estadistico` | Modelo ordinal mixto, Friedman/Wilcoxon, bootstrap por casos, escenarios, figuras y tablas | `37_validacion_artefactos.json` sin errores; conteos releídos: 711 observaciones, 2.133 evaluaciones, 58 no sustantivas, 9 celdas | **OK** | Insertar el análisis en el manuscrito; decidir sensibilidad del modelo (PI-28) |
| `correccion-02-diagnostico-gpt-5-nano` | Clasificación de las 711 respuestas, auditoría de logs, jueces y faltantes | Acta de revisión 87/87; resumen final: 58 no sustantivas, 41 en nano agéntico; notebook válido sin errores | **OK** | Revisión independiente y tratamiento de jueces (PI-06, PI-07, PI-08) |
| `correccion-03-documentar-api-eliminar-determinismo` | 12 payloads locales, perfiles de Pydantic AI, tokens de razonamiento, tabla solicitado/registrado/efectivo | Resumen de evidencia y notebook válido; 12/12 payloads sin temperatura ni `reasoning_effort` | **OK** | Aceptar la redacción y declarar el esfuerzo histórico como desconocido |
| `correccion-04-declarar-factores-pub-prompts-etc` | Auditoría de 237 sesiones, 27 reportes de jueces, prompts, anexo y diagrama | 237 logs, 27 reportes, 0 logs del Agente de Calidad; 236/237 sesiones con una llamada; scripts válidos | **OK con alerta** | Seis decisiones del checklist; el notebook de `part_g` no coincide con el script final |
| `correccion-05-actualizacion-conclusiones-y-analisis-costos` | Tabla 4 reformulada, costos, Pareto, propuestas de texto y README | `verificacion_artefactos.json`: 46 controles, 0 fallos; 9 celdas, 711 observaciones, costo USD 22,2939 | **OK** | Aprobación institucional del título (PI-02) y validación humana de jueces (PI-06); D-01 aclarada por el autor |
| `correccion-06-precisar-corpus-revisar-respuestas` | Linaje del corpus, conteos, revisión por una profesional y conteo de preguntas | Verificador: 130 cambios, 80 párrafos, 482 nodos, 398 artículos, 79 unidades, 166 referencias y 12 propuestas (fuera de alcance); hashes fuente sin cambios | **OK** | 1.2/1.3 y conteo de preguntas; Q23/Q24 y v2 fuera de alcance |
| `correccion-07-forma-y-bibliografia` | Auditoría de 238 referencias, Tablas 2 y 3, propuestas BibTeX | Verificador: 412 archivos del manifiesto coinciden; 238 entradas, 0 claves huérfanas; 45 decisiones manuales | **OK** | Seis decisiones editoriales y paquete de correcciones factuales (PI-20 a PI-27) |
| `verificacion-analisis-estadistico` | Recálculo independiente de alpha, Spearman, 23 discrepancias y 17 evaluaciones positivas | Alpha recalculado en memoria desde `final_judge_results.csv`: 0,807842 original y 0,799542 rúbrica; coincide con el informe | **OK** | El directorio no está versionado; revisión humana de los 23 casos (PI-08, PI-29) |

### 1.2 Comprobaciones técnicas realizadas

- Los 32 archivos Python de los paquetes compilan en memoria; no se ejecutaron notebooks que pudieran sobrescribir salidas.
- Los dos notebooks de corrección (`diagnostico_gpt5_nano.ipynb` y `02_parametros_prompts_y_configuracion.ipynb`) son JSON válidos y no contienen celdas con salida de error.
- Los verificadores de `correccion-06` y `correccion-07` se ejecutaron en modo de solo lectura y pasaron.
- El alpha se recalculó desde la fuente original, no desde la tabla derivada de la corrección 01.
- No hay cambios en archivos fuente rastreados (`git diff` vacío). Los paquetes de corrección están versionados; solo `verificacion-analisis-estadistico/` aparece como directorio no rastreado.
- No existe `codigo_experimentos/part_k_correcciones_jurado`: la implementación se organizó finalmente en `analisis-valoracion-jurado/correccion-*`. Es una desviación del plan original que debe documentarse (PI-01).

### 1.3 Hallazgos que condicionan las decisiones

1. **No hay contradicción entre “28 vacías” y “41 no sustantivas”.** Las 28 son las salidas vacías o solo con espacios de Agentic-RAG + gpt-5-nano; las 41 incluyen además 2 abstenciones, 1 truncada y 10 indeterminadas. En el texto deben usarse etiquetas distintas: “salidas vacías/solo espacios” y “respuestas no sustantivas”.
2. **La revisión manual de 87 filas es del autor, no independiente.** La base final es válida para el análisis, pero no debe presentarse como validación humana independiente.
3. **El notebook de `part_g` conserva una versión anterior** con `evaluate_retrieval` activo y prompts distintos. El script `.py` y los logs son la fuente canónica de la corrida final.
4. **La asimetría 7/6 es real:** gpt-5 usó un prompt de recuperación con límite 7 y 33/79 sesiones agotaron las siete búsquedas; mini y nano usaron límite 6. Además, `16_01` registró tres llamadas del especialista, frente a una en las otras 236 sesiones.
5. **El Agente de Calidad nunca se ejecutó:** 0 logs y 0 llamadas. No se puede afirmar que mejorara ni empeorara el sistema.
6. **El esfuerzo de razonamiento histórico es desconocido:** los `reasoning_tokens` existen en las 711 respuestas, pero no se registró el nivel de esfuerzo. No debe inferirse “alto” o “bajo” a partir de los tokens.
7. **D-01 quedó aclarada por el autor:** la “corrección humana” no es una calificación humana de la calidad de las respuestas, sino la revisión manual de categorías de `correccion-02-diagnostico-gpt-5-nano/revision_manual`. Esa revisión decide qué salidas son sustantivas y, por tanto, qué recibe fallo = 0 en el análisis del sistema. La crítica a los jueces que puntuaron por encima de cero esas salidas se conserva como un análisis separado de medición. Sigue sin existir una validación humana de las calificaciones de los jueces; eso permanece en PI-06.
8. **El modelo ordinal usa `nAGQ = 1`** y no incluye una prueba formal de odds proporcionales. Es aceptable como análisis principal, pero conviene declararlo y añadir una sensibilidad si el costo computacional lo permite.
9. **El benchmark v1 está congelado**, pero la revisión asistida por LLM detectó posibles errores que requieren revisión profesional. No debe llamarse “validación” a esa revisión automática.
10. **La bibliografía tiene 45 decisiones manuales:** 2 críticas, 11 altas, 12 medias y 20 bajas. Las dos críticas son Bozdag/Bommasani y Magesh/Dahl; no son opcionales.

---

## 2. Decisiones ya cerradas que no deben reabrirse

Estas decisiones fueron aceptadas por el autor en `correccion-05-actualizacion-conclusiones-y-analisis-costos/DECISIONES.md`. Se listan para evitar duplicados; solo se reabren si el autor cambia explícitamente de posición.

| ID | Decisión aceptada | Estado de implementación | Observación |
|---|---|---|---|
| D-01 | Escenario principal: respuestas no sustantivas = 0, definido por la revisión manual de categorías, con exclusión como sensibilidad | **Aceptada; interpretación operativa aclarada** | La “corrección humana” es la clasificación manual de sustantividad, no una calificación humana de calidad. Para el análisis del sistema se usa fallo = 0; para la auditoría de jueces se conservan los valores originales y se critican los puntajes > 0 sobre no sustantivas. Ver “D-01 — implementación en dos planos” |
| D-02 | “Respuesta correcta” = puntaje promedio ≥ 0,75, con sensibilidad 0,50 y 1,00 | Aceptada | Documentar que es una operacionalización normativa |
| D-03 | Costos históricos registrados, no precios corrientes | Aceptada | Total USD 22,2939 |
| D-04 | Sin ganador único: Pareto, costo por respuesta correcta y objetivo explícito | Aceptada | RAG básico + nano es el menor costo puntual; no es “la mejor” en calidad |
| D-05 | “Modo de fallo de respuesta”, sin causalidad ni “sobrecarga agéntica” | Aceptada | 41/79 no sustantivas; 38/79 sustantivas con media 0,820 |
| D-06 | Declarar la asimetría 7/6 y no atribuir el efecto de modelo a capacidad sin salvedad | Aceptada | Queda por decidir si se repite la corrida (PI-09) |
| D-07 | Congelar benchmark v1; la revisión LLM detectó posibles errores que requieren revisión profesional | Aceptada | La revisión profesional sigue pendiente como trabajo futuro; no se reabre el benchmark v1 en esta tesis |
| D-08 | Declarar ausencia de validación humana; alpha como confiabilidad, no validez | Aceptada | Documentar 23 discrepancias y 17 evaluaciones positivas (PI-08) |
| D-09 | Actualizar el título al alcance real | Aceptada | Requiere aprobación institucional (PI-02) |
| D-10 | Objetivo 2 como cumplimiento parcial; dos agentes activos, sin verificador | Aceptada | Solo falta insertarlo en el manuscrito |
| D-11 | Acceso público resuelto sin login; clonación recomendada para reproducibilidad | Aceptada | No bloquea el objetivo de acceso |
| D-12 | Quitar “IVF_FLAT” y describir `AUTOINDEX` con similitud coseno | Aceptada | Respaldado por `part_c` |
| D-13 | “No se identificaron antecedentes públicos comparables” en lugar de “primer sistema” | Aceptada | Mantener la cautela |
| D-14 | Recalcular alpha desde los jueces originales en un directorio independiente | Aceptada y verificada | Valores: 0,807842 y 0,799542; precisión legal 0,784566 |

### D-01 — implementación en dos planos

La aclaración del autor permite separar dos estimandos que no deben mezclarse:

1. **Análisis del sistema (estimando principal):** toda salida no sustantiva recibe 0 en las tres evaluaciones. La categoría se toma de la revisión manual de `correccion-02.../revision_manual`. Responde: ¿qué utilidad tiene el sistema completo? Sensibilidad: exclusión de no sustantivas y “solo fallos técnicos = 0”.
2. **Auditoría de jueces (estimando separado):** se conservan los puntajes originales de los jueces, incluidas las 17 evaluaciones positivas sobre las 58 salidas no sustantivas (12 de corrección y 5 de precisión legal). Se reportan por juez y categoría, se contrastan con las justificaciones y se critican como fallas de medición. Responde: ¿miden bien los jueces?

Reglas de implementación:

- **No usar** los puntajes originales de los jueces para afirmar la calidad del sistema; pueden recompensar salidas vacías.
- **No usar** el fallo = 0 para afirmar la validez de los jueces; son preguntas distintas.
- Reportar el alpha original (0,807842) y un alpha condicionado a respuestas sustantivas, además de la tasa de puntajes > 0 sobre no sustantivas.
- La revisión de categorías es del autor, no independiente. D-01 no la convierte en validación humana de los jueces.
- Sensibilidad recomendada: modelo de dos partes (probabilidad de respuesta sustantiva + calidad ordinal condicional) para separar fallo de calidad. No es obligatorio, pero es más limpio que una única imputación a 0.

---

## 3. Decisiones pendientes

### Cómo leer las tablas

- **Bloquea:** indica si la decisión impide redactar o publicar una afirmación central.
- **Responsable:** quién debe decidir; no implica que esa persona deba ejecutar toda la edición.
- Las opciones no son necesariamente excluyentes; cuando se recomienda una combinación, se indica.
- Los identificadores `PI-*` son de este registro; `D-*` remiten a las decisiones ya cerradas y `R*`/`B*` a los paquetes de origen.

### Bloque A — Estructura, alcance y edición

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-01 | Ubicación oficial de los paquetes de corrección | A) Mantener `analisis-valoracion-jurado/correccion-*`; B) mover todo a `codigo_experimentos/part_k_correcciones_jurado`; C) duplicar | **A.** Es la organización ya construida y versionada. Actualizar el plan y el README para explicar que reemplaza a `part_k`; no duplicar archivos | Autor | No, pero afecta la trazabilidad y el README |
| PI-02 | Título definitivo y alcance institucional (D-09) | A) “Desarrollo y evaluación de un prototipo Agentic-RAG para consulta del Código de Minería argentino”; B) mantener el título aprobado y agregar una declaración de alcance; C) mantener el título sin aclaración | **A si la institución lo aprueba; B como respaldo.** Nunca C. Actualizar portada, `main.typ`, README y BibTeX de forma consistente | Autor + Universidad | **Sí** para el título, resumen y conclusión |
| PI-03 | Adopción del paquete 04: textos, diagrama y anexo | A) Aplicar textos, anexo y SVG operativo; B) solo textos y anexo, conservando el diagrama antiguo; C) mínima corrección de epígrafes | **A.** El diagrama antiguo no representa los dos agentes activos ni los límites 6/7. Si no hay tiempo, al menos reemplazar el diagrama. El notebook se decide en PI-11 | Autor | **Sí** para arquitectura y reproducibilidad |
| PI-04 | Declaración de uso de IA | A) Mantener la frase genérica actual; B) declarar por etapas: extracción con o4-mini, preguntas con GPT-4.1, respuestas con GPT-5, jueces con DeepSeek/Grok/Kimi, asistencia de escritura/código y verificación humana | **B.** Es la única forma de que la declaración sea verificable y consistente con el resto del trabajo | Autor | No, pero es integridad académica |
| PI-05 | Terminología del factor “modelo” | A) Renombrar en todo el manuscrito a “modelo del Agente Especialista Legal” y etiquetar las celdas agénticas como “recuperador gpt-5”; B) mantener “modelo” con una nota al pie | **A.** Evita que el mismo término designe tres constructos distintos | Autor | No, pero afecta la interpretación de V.5 |

### Bloque B — Medición humana y jueces

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-06 | Validación humana de las calificaciones de los jueces (D-01 ya no depende de esto) | A) No realizar; declarar que no hay calificaciones humanas de las 711 respuestas y que la revisión de categorías es del autor; reportar alpha como confiabilidad; B) realizar una submuestra ciega de ~90 respuestas (10 por celda) con 1–2 profesionales; C) realizar las 711 (no viable) | **B si hay disponibilidad; A en caso contrario.** D-01 se resuelve con la revisión de categorías; no confundirla con validación de jueces | Autor + directores + profesionales | **Sí** para cualquier afirmación sobre validez humana de los jueces |
| PI-07 | Independencia de la revisión manual de categorías de las 87 respuestas no sustantivas | A) Aceptar la revisión del autor y declararla como tal; B) pedir una segunda revisión ciega de las 87; C) presentarla como validación independiente sin evidencia | **A para la defensa; B si se busca robustez.** Nunca C. La revisión actual tiene 98,9% de acuerdo automático–manual y una discrepancia conocida (`R052`) | Autor | No para el análisis principal; **sí** para la palabra “independiente” |
| PI-08 | Tratamiento de las 23 discrepancias entre jueces y las 17 evaluaciones positivas sobre salidas no sustantivas | A) Incluirlas como anexo/material suplementario y no recalcular; B) adjudicar humanamente los 23 casos; C) omitirlas | **A + B si hay tiempo.** No promediar las 17 evaluaciones positivas como calidad. Si se adjudican, conservar el análisis principal y reportar la sensibilidad | Autor + profesionales | No para el resultado principal; **sí** para la validez de los jueces |

### Bloque C — Diseño experimental y reproducibilidad

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-09 | ¿Se ejecutan nuevas corridas para eliminar confundidos? | A) No ejecutar; declarar 7/6, recuperador fijo y ejecución única; A′) repetir solo Agentic-RAG + gpt-5 con límite 6; B) diagonal R = S (2 celdas nuevas); C) factorial 3×3 de recuperador (8 celdas nuevas) | **A para la versión definitiva.** Si se quiere sostener una afirmación causal o el jurado lo exige, hacer **A′** antes que B/C: es la intervención más barata que elimina un confundido real. A′/B/C vencen el **2026-12-11** y requieren presupuesto y evaluación con jueces | Autor + directores | **Sí** para cualquier afirmación causal o de estabilidad entre corridas |
| PI-10 | Excepción `16_01` (tres llamadas del especialista) | A) Declararla como excepción documentada; B) repetir la sesión; C) omitirla | **A.** El log es público y 236/237 sesiones respetan el límite nominal. Si se ejecuta A′, repetir también `16_01` y conservar el registro histórico | Autor | No, pero afecta la afirmación “una sola delegación” |
| PI-11 | Notebook de `part_g` frente al script final | A) Actualizar el notebook para que coincida con el script/logs; B) marcarlo como exploratorio y declarar el script como fuente canónica; C) dejarlo sin aclaración | **B inmediato; A si hay tiempo.** La reproducibilidad debe apoyarse en el script `.py` y en los logs, no en un notebook desactualizado | Autor | No para el análisis; **sí** para la reproducibilidad |

### Bloque D — Corpus, benchmark y respuestas de referencia

**No quedan decisiones pendientes en este bloque.** Las observaciones del jurado V.7 y IX.1.6 se resolvieron o se acotaron; las preguntas ya revisadas por la profesional se mantienen como tales.

| ID | Tema | Estado | Resolución | Evidencia |
|---|---|---|---|---|
| PI-12 | Procedencia del corpus | **Resuelta** | Proceso en 8 pasos: PDF → imágenes → Markdown con o4 → división por títulos → revisión manual y actualización con Infoleg → GPT-4.1 → DOCX → revisión por una profesional → ODT → JSON final. El parser HTML se intentó y se descartó por complejidad; la actualización fue manual | Declaración del autor; `correccion-06/README.md` §5; `propuesta_edicion_manuscrito.md` §1.1 |
| PI-13 | Q23 (Río Turbio) | **Cancelada / fuera de alcance** | La pregunta se mantiene como fue revisada; no se propone nueva revisión ni cambio de benchmark. No atribuir a la revisora una eliminación que no pidió | `correccion-06/README.md` §3.6; `decisiones_revision.csv` R24 |
| PI-14 | Q24 (Ley 24.585) | **Cancelada / fuera de alcance** | La pregunta se mantiene como fue revisada; el comentario no aplicado se documenta, no genera una nueva decisión | `salidas/conteo_preguntas_revisadas.csv` |
| PI-15 | Q1.3: artículo 17 | **Resuelta; implementación editorial pendiente** | El error está en el JSON y en el anexo Typst; el corpus es correcto. No se modifica el benchmark v1. Se corrige el anexo para citar el artículo 17 literalmente y se declara la discrepancia; corregir el JSON y reevaluar es trabajo futuro | `correccion-06/README.md` §3.5; `propuesta_edicion_manuscrito.md` §3.2 |
| PI-16 | Q1.2: artículo 8 vs 11 | **Resuelta; implementación editorial pendiente** | El JSON, el corpus y `título_i.md` son correctos; el error está solo en el anexo Typst. Corregir únicamente el anexo; no crear v2 | `correccion-06/README.md` §3.5; `propuesta_edicion_manuscrito.md` §3.1 |
| PI-17 | Referencias Q13/Q22/Q25 | **Cancelada / fuera de alcance** | Son hallazgos de auditoría adicional, no observaciones del jurado; las preguntas revisadas se mantienen y no se propone v2 | `correccion-06/README.md` §3.6 |
| PI-18 | Segunda revisión independiente | **Resuelta** | Hubo una sola profesional revisora; no existe segunda revisión independiente. Usar “revisión por una profesional” | `correccion-06/README.md` §3.4; `resumen_conteo_preguntas.md` |
| PI-19 | Fechas y metadatos | **Resuelta; implementación editorial pendiente** | Usar 1886-11-25 y 1997-05-30; eliminar 1994-01-01/10/15 y 2024-12-09 no verificados | `propuesta_edicion_manuscrito.md` §2.1 |
| PI-20 | Benchmark v2 | **Cancelada / fuera de alcance** | No se crea ni publica benchmark v2 en esta tesis; nueva revisión = trabajo futuro | `correccion-06/README.md` §3.6 |
| PI-32 | Conteo de preguntas corregidas | **Resuelta** | 25 preguntas: 18 con alguna intervención, 17 con cambio de contenido o corrección aplicada, 1 solo comentario no aplicado (Q24), 7 sin intervención (Q7, Q8, Q9, Q12, Q13, Q15, Q20) | `salidas/conteo_preguntas_revisadas.csv`; `salidas/resumen_conteo_preguntas.md` |

### Bloque E — Bibliografía y citas

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-21 | Bommasani/Davis/Cardon → Bozdag, Sevim y Koç | A) Reemplazar la entrada y reescribir las dos afirmaciones; B) conservar la entrada y corregir solo el DOI; C) dejar como está | **A.** El DOI 10.1145/3628602 corresponde a Bozdag et al. (2024), y el método es ajuste fino, no “adapters”. Revisar el texto completo antes de atribuir resultados | Autor + bibliografía | **Sí** para la Tabla 3 |
| PI-22 | Dahl et al. (2024) frente a Magesh et al. (2025) | A) Usar Magesh et al. para la frase sobre Westlaw/Lexis y conservar Dahl solo para su propio contenido; B) conservar Dahl para la frase; C) eliminar ambas | **A.** El estudio de Westlaw/Lexis es Magesh et al. (2025), JELS 22(2), 216–242. Dahl no sustenta esa afirmación | Autor | **Sí** para la Tabla 3 |
| PI-23 | Wei 2022 y Zhao 2026: APA frente a letras a/b | A) APA: “Wei, Wang, y cols.” / “Wei, Tay, y cols.” y “W. X. Zhao y cols.” / “J. Zhao y cols.”; B) letras (2022a/2022b, 2026a/2026b) como pedía literalmente el jurado | **A.** Es la regla APA 7 para coautores distintos e iniciales distintas; Typst ya maneja bien `form: "year"`. Probar en `pruebas/citas_ambiguas.typ` | Autor + bibliografía | No, pero afecta la Tabla 3 |
| PI-24 | Tribunal Fiscal de la Nación | A) Entrada institucional con el sitio oficial; B) nota de AUNO con autora Milagros Denise Tallarico; C) mantener la mezcla actual | **A.** Si se conserva la nota, usar B y no atribuirla al organismo. No mezclar autor institucional con URL de un estudio jurídico | Autor + bibliografía | No, pero afecta la fuente |
| PI-25 | DOI de edición en Hebb, Minsky, Bonferroni, Jordan y Krippendorff | A) Citar la edición efectivamente consultada y retirar el DOI si no corresponde; B) conservar el DOI y cambiar la edición; C) dejar el DOI actual | **A.** No atribuir a 1949/1969/1936/1986 un DOI de 2005/2017/2010/1997. Documentar la edición consultada | Autor + bibliografía | No, pero afecta la trazabilidad |
| PI-26 | Forma de autoría: “y cols.” frente a “et al.” | A) “y cols.” uniforme en español; B) “et al.” estricto APA; C) mantener la mezcla actual | **A.** El PDF tiene 309 “y col.” y 11 “y cols.”; usar “y cols.” en ambas reglas de `main.typ` y corregir el singular | Autor | No, pero es corrección editorial obligatoria |
| PI-27 | Paquete de correcciones factuales de alta prioridad | A) Aplicar todas las correcciones verificadas: Niklaus 2023, DeepSeek-R1 2025, Llama 4 abril 2025, Qwen3 abril 2025, Yang en lugar de Wan, Pydantic 1.1.0, Springer 2025, Zhao survey, Raeini, etc.; B) aplicar solo las críticas; C) posponerlas | **A.** Son correcciones de metadatos y autoría respaldadas por Crossref/arXiv/sitios oficiales; no requieren nueva evidencia. Revisar las afirmaciones que dependen de ellas | Autor + bibliografía | **Sí** para la auditoría completa |
| PI-28 | Referencias faltantes | A) Agregar Lewis et al. (2020), Código de Minería/Ley 1.919, Zheng et al. (2021), Bench-Capon et al. (2012), Tribunal Fiscal y Qwen3; B) agregar solo Lewis y Código; C) no agregar | **A.** Lewis es fundacional para RAG; el Código es la fuente legal del corpus; Zheng separa CaseHOLD del corpus de Legal-BERT; Bench-Capon reemplaza la nota a Wikipedia | Autor + bibliografía | **Sí** para la completitud de fuentes |

### Bloque F — Análisis, release y cierre

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-29 | Sensibilidad del modelo ordinal (`nAGQ = 1`) y odds proporcionales | A) Mantener `nAGQ = 1` y declarar el supuesto; B) agregar una sensibilidad con `nAGQ = 7` o un modelo bayesiano; C) cambiar el modelo principal | **B si el cómputo lo permite; A como mínimo.** No cambiar el modelo principal después de ver los resultados. Reportar la limitación de odds proporcionales | Autor + estadística | No para el resultado principal; **sí** para la robustez |
| PI-30 | Versionado y publicación del directorio de verificación | A) Agregar `verificacion-analisis-estadistico/` al repositorio y hacer una clonación anónima de prueba; B) dejarlo fuera del repositorio; C) publicarlo sin verificar | **A.** Es el único directorio de corrección no rastreado. Incluirlo, ejecutar `run_all.sh`, compilar el manuscrito desde una clonación limpia y registrar el commit | Autor | **Sí** para la afirmación de reproducibilidad |
| PI-31 | Sincronización final de manuscrito, README y presentación | A) Aplicar todas las propuestas de las correcciones 01–07 y recompilar; B) aplicar solo las críticas; C) dejar el manuscrito como está y entregar los paquetes como anexos | **A.** Es la única opción coherente con las decisiones D-01–D-14. Verificar con `make pdf`, búsquedas de frases prohibidas y revisión visual | Autor | **Sí** para la entrega |

---

## 4. Decisiones que no requieren elección: aplicar por evidencia

Estas no son alternativas abiertas; ya están respaldadas por los datos o por decisiones aceptadas. Se incluyen para evitar que se confundan con “pendientes”.

| Tema | Acción definida | Evidencia |
|---|---|---|
| Join de las 27 medias | Normalizar subpregunta vacía/`None`/`0` en la tabla derivada; no editar los CSV fuente | 711 observaciones, 2.133 evaluaciones, 27 filas recuperadas |
| Universo de respuestas | Reportar 58 no sustantivas y 653 sustantivas; 41 no sustantivas en nano agéntico | Base final `14_dataset_categoria_final.csv` |
| Taxonomía de fallos | Distinguir 27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas; no llamar “27 fallos” a todas | Corrección 02 |
| Auditoría de jueces | Conservar los valores originales solo para auditar a los jueces; no usarlos para el ranking del sistema | D-01; 12 filas de corrección + 5 de precisión legal > 0 sobre no sustantivas |
| “Sobrecarga agéntica” | Retirar como hallazgo/contribución; usar “modo de fallo de respuesta” | D-05; 41/79 con 38 respuestas sustantivas de calidad alta |
| Determinismo | Retirar “temperatura 0 = determinista”; la temperatura no se envía a GPT-5 bajo Pydantic AI 1.1.0 | Corrección 03; 12/12 payloads sin temperatura |
| Esfuerzo de razonamiento | Declararlo desconocido; no inferirlo de los tokens | 0 ocurrencias de `reasoning_effort`; 711 respuestas con tokens de razonamiento |
| Agente de Calidad | Eliminar “no se tradujo en mejoras”; conservar solo costo/complejidad | 0 logs y 0 llamadas |
| 7/6 | Declarar la asimetría; no afirmar que todas las configuraciones usaron seis búsquedas | 33/79 sesiones de gpt-5 agotaron 7; mini/nano usaron 6 |
| `16_01` | Declarar la excepción de tres llamadas | 236/237 sesiones con una llamada |
| Índice vectorial | Describir `AUTOINDEX` con similitud coseno; quitar “IVF_FLAT” | `part_c/01_initial_vector_db_creation.ipynb`; D-12 |
| Corpus | 482 nodos, 398 nodos artículo, 397 con texto y 1 vacío (art. 239); no decir “399 artículos” ni “245 artículos” | Auditoría 06; verificación de hashes |
| Fechas | Sanción 1886-11-25; texto ordenado B.O. 1997-05-30; no usar 1994-01-01 ni 2024-12-09 sin fuente | Auditoría 06 |
| Alpha | Reportar 0,807842 (original) y 0,799542 (rúbrica); no llamarlo validación | D-14; recálculo independiente |
| Costos | Usar costos históricos; reportar Pareto y costo por respuesta ≥ 0,75, sin el piso 0,01 | D-02, D-03, D-04 |
| “Primer sistema” | “No se identificaron antecedentes públicos comparables” | D-13 |
| Acceso público | Declarar acceso sin login; no afirmar reproducibilidad exacta sin clonación | D-11; verificación 2026-11-11 |
| Bibliografía factual | Aplicar las correcciones de Niklaus, DeepSeek, Llama 4, Qwen3, Yang/Wan, Pydantic, Springer, Zhao survey y Raeini | Corrección 07; 238 entradas, 45 decisiones manuales |

---

## 5. Ruta crítica recomendada

### Antes de editar el manuscrito

1. **PI-02:** resolver el título con la institución; si no hay aprobación, adoptar la opción B y declarar el alcance.
2. **PI-06 y PI-07:** D-01 ya está resuelta con la revisión manual de categorías. Decidir si se agrega una submuestra humana para validar las calificaciones de los jueces; si no, declarar la ausencia y no llamar “validación” al acuerdo entre jueces.
3. **PI-09:** decidir si se ejecuta A′/B/C antes del **2026-12-11**; si no, declarar la ejecución única y la asimetría 7/6.
4. **Bloque D:** no quedan decisiones pendientes. Aplicar la implementación editorial de PI-15 y PI-19; mantener PI-13, PI-14, PI-17 y PI-20 fuera de alcance.
5. **PI-21 a PI-28:** aprobar el paquete bibliográfico; primero las dos críticas, luego las altas y finalmente las bajas.

### Antes de compilar la versión final

1. **PI-03, PI-05, PI-10, PI-11:** aplicar los textos de arquitectura, prompts, límites y notebook canónico.
2. **PI-29:** agregar la sensibilidad del modelo o declarar la limitación.
3. **PI-31:** sincronizar resumen, introducción, metodología, evaluación, conclusiones, anexos y README.
4. **PI-30:** agregar la verificación al repositorio, ejecutar los verificadores y hacer la clonación anónima.
5. **PI-04:** completar la declaración de IA con las etapas efectivamente asistidas.

### Verificación final

- `make pdf` compila sin errores.
- Búsquedas en el PDF: “sobrecarga agéntica”, “efecto igualador”, “LLM-as-a-Judge validado”, “temperatura 0” asociada a determinismo, “transferible”, “IVF_FLAT”, “245 artículos”, “399 artículos”, “n = 79” sin aclarar exclusiones.
- El PDF final no contiene “Bommasani y col., 2023” para el DOI de Bozdag, ni “Dahl y col., 2024” para Westlaw/Lexis, ni “DeepSeek 2026b”, ni “Meta 2026” para Llama 4.
- Las tablas de la corrección 01, la Tabla 4 de la corrección 05 y los textos del manuscrito usan las mismas cifras.
- Los 412 archivos del manifiesto de corrección 07 y los hashes de corrección 06 siguen coincidiendo.
- La clonación anónima incluye `verificacion-analisis-estadistico/` y permite ejecutar el análisis descriptivo y compilar el manuscrito.

---

## 6. Registro de decisión

Completar una fila por cada `PI-*` antes de editar el manuscrito. Si se elige una opción distinta de la recomendada, actualizar también los artefactos que dependen de ella y dejar la justificación.

| ID | Fecha | Decisión adoptada | Responsable | Artefacto/evidencia actualizado |
|---|---|---|---|---|
| PI-01 | 2026-11-12 | Opción A: adicionalmente, hay que marcar como "deprecados" los análisis previos que ya no se utilizan | autor | |
| PI-02 | 2026-11-12 | Opción A: Ya fue aprobado vía correo electrónico por el director de la maestría | autor | |
| PI-03 | 2026-11-12 | Opción A: Ya fue aprobado vía correo electrónico por el director de la maestría | autor | |
| PI-04 | 2026-11-12 | Opción A: requiere actualizar el diagrama propuesto para que respete los colores previos. Asegurarse que el texto no se salga de los "text box" o límites de los contenedores | autor | |
| PI-05 | 2026-11-12 | Opción A: Renombrar en todo el manuscrito a “modelo del Agente Especialista Legal” y etiquetar las celdas agénticas como “recuperador gpt-5” | autor | |
| PI-06 | 2026-11-12 | Opción A: No realizar validaciones humanas adicionales, no se cuenta con tiempo ni disponibilidad de profesionales | autor | |
| PI-07 | 2026-11-12 | Opción A: Aceptar la revisión del autor y declararla como tal | autor | |
| PI-08 | 2026-11-12 | Opción A y B. Ya están adjudicados los casos, y se encuentran incluidos en `analisis-valoracion-jurado/correccion-02-diagnostico-gpt-5-nano/salidas/14_dataset_categoria_final.csv` para su uso en la estadística. El análisis dentro de `analisis-valoracion-jurado/correccion-01-analisis-estadistico` ya lo incorpora. | autor | |
| PI-09 | 2026-11-12 | A) No ejecutar; declarar 7/6, recuperador fijo y ejecución única. Aceptar y documentar limitación en el texto| autor | |
| PI-10 | 2026-11-12 | A) Declararla como excepción documentada | autor | |
| PI-11 | 2026-11-12 | B) marcarlo como exploratorio y declarar el script como fuente canónica. | autor | |
| PI-12 | 2026-11-12 | **Resuelta.** Proceso documentado: PDF → imágenes → Markdown con o4; división por títulos; revisión manual y actualización con Infoleg; GPT-4.1; DOCX; revisión por una profesional; ODT; JSON final. El parser HTML se intentó y se descartó por complejidad; la actualización fue manual | autor | `correccion-06/README.md` §5; `propuesta_edicion_manuscrito.md` §1.1 |
| PI-13 | 2026-11-12 | **Cancelada / fuera de alcance.** Q23 se mantiene como fue revisada; no se propone nueva revisión ni cambio de benchmark | autor | `correccion-06/README.md` §3.6; `decisiones_revision.csv` R24 |
| PI-14 | 2026-11-12 | **Cancelada / fuera de alcance.** Q24 se mantiene como fue revisada; el comentario no aplicado se documenta, no genera una nueva decisión | autor | `salidas/conteo_preguntas_revisadas.csv` |
| PI-15 | 2026-11-12 | **Resuelta.** No se modifica el benchmark v1. Se corrige el anexo para citar el artículo 17 literalmente y se declara la discrepancia. Corregir el JSON y reevaluar es trabajo futuro | autor | `correccion-06/README.md` §3.5; `propuesta_edicion_manuscrito.md` §3 |
| PI-16 | 2026-11-12 | **Resuelta.** El error de 1.2 está solo en el anexo Typst; el JSON y el corpus son correctos. Corregir el anexo; no crear v2 | autor | `correccion-06/README.md` §3.5 |
| PI-17 | 2026-11-12 | **Cancelada / fuera de alcance.** Q13.2/Q13.3/Q22.1/Q25 son hallazgos adicionales, no observaciones del jurado; no se propone nueva revisión ni v2 | autor | `correccion-06/README.md` §3.6 |
| PI-18 | 2026-11-12 | **Resuelta.** Una sola profesional revisora; no hubo segunda revisión independiente. Usar “revisión por una profesional”, no “validación” | autor | `correccion-06/README.md` §3.4; `resumen_conteo_preguntas.md` |
| PI-19 | 2026-11-12 | **Resuelta.** Usar 1886-11-25 y 1997-05-30; eliminar 1994-01-01/10/15 y 2024-12-09 no verificados | autor | `propuesta_edicion_manuscrito.md` §2.1 |
| PI-20 | 2026-11-12 | **Cancelada / fuera de alcance.** No se crea ni publica benchmark v2 en esta tesis; nueva revisión = trabajo futuro | autor | `correccion-06/README.md` §3.6 |
| PI-21 | | | | |
| PI-22 | | | | |
| PI-23 | | | | |
| PI-24 | | | | |
| PI-25 | | | | |
| PI-26 | | | | |
| PI-27 | | | | |
| PI-28 | | | | |
| PI-29 | | | | |
| PI-30 | | | | |
| PI-31 | | | | |
| PI-32 | 2026-11-12 | **Resuelta.** 25 preguntas: 18 con alguna intervención; 17 con cambio de contenido o corrección aplicada; 1 solo comentario no aplicado (Q24); 7 sin intervención (Q7, Q8, Q9, Q12, Q13, Q15, Q20) | autor | `salidas/conteo_preguntas_revisadas.csv`; `salidas/resumen_conteo_preguntas.md` |

---

## 7. Criterio de cierre

Se considera cerrado este registro cuando:

1. cada `PI-*` tiene una decisión escrita, incluso si la decisión es “se declara como limitación”;
2. ninguna decisión contradice D-01–D-14 sin una actualización explícita de esas decisiones;
3. el manuscrito, el README y la presentación usan las mismas cifras, etiquetas y fuentes;
4. los paquetes de corrección y la verificación están versionados y una clonación anónima reproduce el análisis;
5. el PDF final no contiene afirmaciones de causalidad, equivalencia, determinismo o validación humana que los datos no sostengan.

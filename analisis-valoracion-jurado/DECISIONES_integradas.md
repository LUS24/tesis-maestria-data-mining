# Decisiones integradas pendientes

**Fecha de verificación:** 2026-11-12.  
**Alcance:** directorios `correccion-01` a `correccion-07` y `verificacion-analisis-estadistico` de `analisis-valoracion-jurado/`; incluye las decisiones NV-01–NV-07 de la valoración actualizada.  
**Objetivo:** reunir en un solo registro las decisiones que todavía requieren una elección, sin reabrir las decisiones ya aceptadas ni convertir tareas de edición en falsas alternativas.

**Regla de trabajo:** las fuentes, respuestas, logs, evaluaciones y archivos históricos no se modifican. Toda decisión se implementa en artefactos nuevos y, cuando corresponda, en el manuscrito/README mediante una edición explícita y trazable.

---

## 1. Verificación de los directorios

### 1.1 Inventario y estado

| Directorio | Qué contiene | Verificación realizada | Estado | Pendiente principal |
|---|---|---|---|---|
| `correccion-01-analisis-estadistico` | Modelo ordinal mixto, Friedman/Wilcoxon, bootstrap por casos, escenarios, figuras y tablas | `37_validacion_artefactos.json` sin errores; conteos releídos: 711 observaciones, 2.133 evaluaciones, 58 no sustantivas, 9 celdas | **OK** | Insertar el análisis en el manuscrito; reconciliar cifras de V.1 (NV-01) y declarar Laplace (PI-29) |
| `correccion-02-diagnostico-gpt-5-nano` | Clasificación de las 711 respuestas, auditoría de logs, jueces y faltantes | Acta de revisión 87/87; resumen final: 58 no sustantivas, 41 en nano agéntico; notebook válido sin errores | **OK** | Revisión independiente y tratamiento de jueces (PI-06, PI-07, PI-08) |
| `correccion-03-documentar-api-eliminar-determinismo` | 12 payloads locales, perfiles de Pydantic AI, tokens de razonamiento, tabla solicitado/registrado/efectivo | Resumen de evidencia y notebook válido; 12/12 payloads sin temperatura ni `reasoning_effort` | **OK** | Declarar el valor por defecto de la API: Pydantic AI 1.1.0 no fija `reasoning_effort`; OpenAI documenta `medium` para GPT-5 (NV-05) |
| `correccion-04-declarar-factores-pub-prompts-etc` | Auditoría de 237 sesiones, 27 reportes de jueces, prompts, anexo y diagrama | 237 logs, 27 reportes, 0 logs del Agente de Calidad; 236/237 sesiones con una llamada; scripts válidos | **OK con alerta** | Seis decisiones del checklist; el notebook de `part_g` no coincide con el script final |
| `correccion-05-actualizacion-conclusiones-y-analisis-costos` | Tabla 4 reformulada, costos, Pareto, propuestas de texto y README | `verificacion_artefactos.json`: 46 controles, 0 fallos; 9 celdas, 711 observaciones, costo USD 22,2939 | **OK** | Aprobación institucional del título (PI-02), validación humana de jueces (PI-06) y declaración de IA (PI-04/NV-04); D-01 aclarada por el autor |
| `correccion-06-precisar-corpus-revisar-respuestas` | Linaje del corpus, conteos, revisión por una profesional y conteo de preguntas | Verificador: 130 cambios, 80 párrafos, 482 nodos, 398 artículos, 79 unidades, 166 referencias y 12 propuestas (fuera de alcance); hashes fuente sin cambios | **OK** | 1.2/1.3 y conteo de preguntas; NV-03 (citas sobre respuestas generadas); Q23/Q24 y v2 fuera de alcance |
| `correccion-07-forma-y-bibliografia` | Auditoría de 238 referencias, Tablas 2 y 3, propuestas BibTeX | Verificador: 412 archivos del manifiesto coinciden; 238 entradas, 0 claves huérfanas; 45 decisiones manuales | **OK** | Seis decisiones editoriales y paquete de correcciones factuales (PI-21 a PI-28) |
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
6. **El esfuerzo de razonamiento no se registró localmente:** no se envió `reasoning_effort`. Pydantic AI 1.1.0 no define un default; OpenAI documenta `medium` como default para GPT-5 cuando se omite. Los `reasoning_tokens` no permiten reconstruir el esfuerzo; no debe inferirse “alto” o “bajo” a partir de ellos.
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
| D-12 | Quitar “IVF_FLAT” y describir `AUTOINDEX` con similitud coseno | Aceptada; NV-06 resuelta con AUTOINDEX | Respaldado por `part_c`; la nueva valoración repite “IVF_FLAT” sin evidencia nueva |
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

## 3. Catálogo de opciones y recomendaciones

> **El estado vigente de cada ID está solo en `§6`.** Este catálogo conserva las opciones y recomendaciones de todas las decisiones, incluidas las ya cerradas o canceladas, para trazabilidad. No debe leerse como una lista de pendientes.

### Cómo leer las tablas

- **Bloquea:** indica si la decisión impide redactar o publicar una afirmación central.
- **Responsable:** quién debe decidir; no implica que esa persona deba ejecutar toda la edición.
- Las opciones no son necesariamente excluyentes; cuando se recomienda una combinación, se indica.
- Los identificadores `PI-*` y `NV-*` son de este registro; `D-*` remiten a las decisiones ya cerradas y `R*`/`B*` a los paquetes de origen.

### Bloque A — Estructura, alcance y edición

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-01 | Ubicación oficial de los paquetes de corrección | A) Mantener `analisis-valoracion-jurado/correccion-*`; B) mover todo a `codigo_experimentos/part_k_correcciones_jurado`; C) duplicar | **A.** Es la organización ya construida y versionada. Actualizar el plan y el README para explicar que reemplaza a `part_k`; no duplicar archivos | Autor | No, pero afecta la trazabilidad y el README |
| PI-02 | Título definitivo y alcance institucional (D-09) | A) “Desarrollo y evaluación de un prototipo Agentic-RAG para consulta del Código de Minería argentino”; B) mantener el título aprobado y agregar una declaración de alcance; C) mantener el título sin aclaración | **A si la institución lo aprueba; B como respaldo.** Nunca C. Actualizar portada, `main.typ`, README y BibTeX de forma consistente | Autor + Universidad | **Sí** para el título, resumen y conclusión |
| PI-03 | Adopción del paquete 04: textos, diagrama y anexo | A) Aplicar textos, anexo y SVG operativo; B) solo textos y anexo, conservando el diagrama antiguo; C) mínima corrección de epígrafes | **A.** El diagrama antiguo no representa los dos agentes activos ni los límites 6/7. Si no hay tiempo, al menos reemplazar el diagrama. El notebook se decide en PI-11 | Autor | **Sí** para arquitectura y reproducibilidad |
| PI-04 | Declaración de uso de IA (ampliada por IX.1.8/V.11) | A) Mantener la frase genérica actual; B) declarar por etapas: extracción con o4-mini, preguntas con GPT-4.1, respuestas con GPT-5, jueces con DeepSeek/Grok/Kimi, asistencia de escritura/código y verificación humana de artefactos (no de la calidad de las respuestas); revisar el antecedente de la “referencia fabricada” que menciona V.11 | **B.** Es la única forma de que la declaración sea verificable y consistente con el resto del trabajo. Coordinar con NV-04 | Autor | **Sí** para IX.1.8 |
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
| PI-12 | Procedencia del corpus | **Resuelta** | Proceso en 8 pasos: PDF → imágenes → Markdown con o4 → división por títulos → revisión manual y actualización con Infoleg → GPT-4.1 → DOCX → revisión por una profesional → ODT → JSON final. El parser HTML se intentó y se descartó por complejidad; la actualización fue manual | `correccion-06/propuesta_edicion_manuscrito.md` §1.1; `correccion-06/resumen_ejecutivo.md` §2 |
| PI-13 | Q23 (Río Turbio) | **Cancelada / fuera de alcance** | La pregunta se mantiene como fue revisada; no se propone nueva revisión ni cambio de benchmark. No atribuir a la revisora una eliminación que no pidió | `correccion-06/resumen_ejecutivo.md` §5; `correccion-06/hallazgos_respuestas_referencia.md` §2.2 |
| PI-14 | Q24 (Ley 24.585) | **Cancelada / fuera de alcance** | La pregunta se mantiene como fue revisada; el comentario no aplicado se documenta, no genera una nueva decisión | `correccion-06/resumen_ejecutivo.md` §5; `correccion-06/salidas/conteo_preguntas_revisadas.csv` |
| PI-15 | Q1.3: artículo 17 | **Resuelta; implementación editorial pendiente** | El error está en el JSON y en el anexo Typst; el corpus es correcto. No se modifica el benchmark v1. Se corrige el anexo para citar el artículo 17 literalmente y se declara la discrepancia; corregir el JSON y reevaluar es trabajo futuro | `correccion-06/propuesta_edicion_manuscrito.md` §3.2; `correccion-06/resumen_ejecutivo.md` §2 |
| PI-16 | Q1.2: artículo 8 vs 11 | **Resuelta; implementación editorial pendiente** | El JSON, el corpus y `título_i.md` son correctos; el error está solo en el anexo Typst. Corregir únicamente el anexo; no crear v2 | `correccion-06/propuesta_edicion_manuscrito.md` §3.1; `correccion-06/resumen_ejecutivo.md` §2 |
| PI-17 | Referencias Q13/Q22/Q25 | **Cancelada / fuera de alcance** | Son hallazgos de auditoría adicional, no observaciones del jurado; las preguntas revisadas se mantienen y no se propone v2 | `correccion-06/resumen_ejecutivo.md` §5 |
| PI-18 | Segunda revisión independiente | **Resuelta** | Hubo una sola profesional revisora; no existe segunda revisión independiente. Usar “revisión por una profesional” | `correccion-06/hallazgos_respuestas_referencia.md` §2.1; `correccion-06/resumen_ejecutivo.md` §2 |
| PI-19 | Fechas y metadatos | **Resuelta; implementación editorial pendiente** | Usar 1886-11-25 y 1997-05-30; eliminar 1994-01-01/10/15 y 2024-12-09 no verificados | `correccion-06/propuesta_edicion_manuscrito.md` §2.1; `correccion-06/resumen_ejecutivo.md` §2 |
| PI-20 | Benchmark v2 | **Cancelada / fuera de alcance** | No se crea ni publica benchmark v2 en esta tesis; nueva revisión = trabajo futuro | `correccion-06/resumen_ejecutivo.md` §5 |
| PI-32 | Conteo de preguntas corregidas | **Resuelta** | 25 preguntas: 18 con alguna intervención, 17 con cambio de contenido o corrección aplicada, 1 solo comentario no aplicado (Q24), 7 sin intervención (Q7, Q8, Q9, Q12, Q13, Q15, Q20) | `salidas/conteo_preguntas_revisadas.csv`; `salidas/resumen_conteo_preguntas.md` |

### Bloque E — Bibliografía y citas

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-21 | Bommasani/Davis/Cardon → Bozdag, Sevim y Koç | A) Reemplazar la entrada y reescribir las dos afirmaciones; B) conservar la entrada y corregir solo el DOI; C) dejar como está | **A.** El DOI 10.1145/3628602 corresponde a Bozdag et al. (2024), y el método es ajuste fino, no “adapters”. Revisar el texto completo antes de atribuir resultados | Autor + bibliografía | **Sí** para la Tabla 3 |
| PI-22 | Dahl et al. (2024) frente a Magesh et al. (2025) | A) Usar Magesh et al. para la frase sobre Westlaw/Lexis y conservar Dahl solo para su propio contenido; B) conservar Dahl para la frase; C) eliminar ambas | **A.** El estudio de Westlaw/Lexis es Magesh et al. (2025), JELS 22(2), 216–242. Dahl no sustenta esa afirmación | Autor | **Sí** para la Tabla 3 |
| PI-23 | Wei 2022 y Zhao 2026: APA frente a letras a/b | A) APA: “Wei, Wang, y cols.” / “Wei, Tay, y cols.” y “W. X. Zhao y cols.” / “J. Zhao y cols.”; B) letras (2022a/2022b, 2026a/2026b) como pedía literalmente el jurado | **A.** Es la regla APA 7 para coautores distintos e iniciales distintas; Typst ya maneja bien `form: "year"`. Probar en `pruebas/citas_ambiguas.typ` | Autor + bibliografía | No, pero afecta la Tabla 3 |
| PI-24 | Tribunal Fiscal de la Nación | A) Entrada institucional con el sitio oficial; B) nota de AUNO con autora Milagros Denise Tallarico; C) mantener la mezcla actual | **A adoptada con la página institucional:** `https://www.argentina.gob.ar/tribunalfiscal/jurisprudencia` responde 200 y enlaza al “Buscador de Jurisprudencia Asistido por IA”. El endpoint directo `https://jurisprudenciatfn.mecon.gob.ar/` no respondió desde este entorno (timeout). Usar `tribunalfiscal2024buscador`; no mezclar autor institucional con la nota de AUNO | Autor + bibliografía | No, pero afecta la fuente |
| PI-25 | DOI de edición en Hebb, Minsky, Bonferroni, Jordan y Krippendorff | A) Citar la edición efectivamente consultada y retirar el DOI si no corresponde; B) conservar el DOI y cambiar la edición; C) dejar el DOI actual | **Resuelta:** se adoptan las ediciones y entradas de `§6.4`; las cinco claves y todas sus citas se actualizaron en el manuscrito | Autor + bibliografía | No, pero afecta la trazabilidad |
| PI-26 | Forma de autoría: “y cols.” frente a “et al.” | A) “y cols.” uniforme en español; B) “et al.” estricto APA; C) mantener la mezcla actual | **B adoptada:** `et al.` estricto APA 7, como solicita el tribunal. Revisar las dos reglas de `main.typ` y las citas renderizadas | Autor | No, pero es corrección editorial obligatoria |
| PI-27 | Paquete de correcciones factuales de alta prioridad | A) Aplicar todas las correcciones verificadas: Niklaus 2023, DeepSeek-R1 2025, Llama 4 abril 2025, Qwen3 abril 2025, Yang en lugar de Wan, Pydantic 1.1.0, Springer 2025, Zhao survey, Raeini, etc.; B) aplicar solo las críticas; C) posponerlas | **A.** Son correcciones de metadatos y autoría respaldadas por Crossref/arXiv/sitios oficiales; no requieren nueva evidencia. Revisar las afirmaciones que dependen de ellas | Autor + bibliografía | **Sí** para la auditoría completa |
| PI-28 | Referencias faltantes | A) Agregar Lewis et al. (2020), Código de Minería/Ley 1.919, Zheng et al. (2021), Bench-Capon et al. (2012), Tribunal Fiscal y Qwen3; B) agregar solo Lewis y Código; C) no agregar | **A.** Lewis es fundacional para RAG; el Código es la fuente legal del corpus; Zheng separa CaseHOLD del corpus de Legal-BERT; Bench-Capon reemplaza la nota a Wikipedia | Autor + bibliografía | **Sí** para la completitud de fuentes |

### Bloque F — Análisis, release y cierre

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-29 | Sensibilidad del modelo ordinal (`nAGQ = 1`), odds proporcionales y reconciliación con V.1 | A) Mantener `nAGQ = 1` y declarar el supuesto; B) agregar una sensibilidad con `nAGQ = 7` o un modelo bayesiano; C) cambiar el modelo principal. En todos los casos, reconciliar las cifras nuevas de V.1 con `correccion-01` (NV-01) | **A adoptada:** mantener `nAGQ = 1` (Laplace) y declarar la limitación. `nAGQ > 1` no está disponible en `ordinal::clmm` con dos términos de efectos aleatorios (`(1|caso) + (1|unidad)`); la opción `nAGQ = 7` no es ejecutable con esta fórmula. Reconciliar con NV-01 | Autor + estadística | No para el resultado principal; **sí** para la robustez |
| PI-30 | Versionado y publicación del directorio de verificación | A) Agregar `verificacion-analisis-estadistico/` al repositorio y hacer una clonación anónima de prueba; B) dejarlo fuera del repositorio; C) publicarlo sin verificar | **A:** publicar después de revisar el manuscrito y ordenar el directorio; luego ejecutar `run_all.sh`, compilar desde una clonación limpia y registrar el commit | Autor | **Sí** para la afirmación de reproducibilidad |
| PI-31 | Sincronización final de manuscrito, README y presentación | A) Aplicar todas las propuestas de las correcciones 01–07 y recompilar, incorporando métricas de recuperación (NV-02), citas deterministas (NV-03), declaración de IA (NV-04) y cifras reconciliadas de V.1/V.6 (NV-01/NV-07); B) aplicar solo las críticas; C) dejar el manuscrito como está y entregar los paquetes como anexos | **A adoptada:** aplicar todo y generar una nueva versión del archivo. Verificar con `make pdf`, búsquedas de frases prohibidas y revisión visual | Autor | **Sí** para la entrega |

### Bloque G — Decisiones de la valoración actualizada (NV-01–NV-07)

Estas decisiones provienen de `COBERTURA_valoracion_actualizada.md` §7. El estado actualizado de cada una está en `§6`.

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| NV-01 | ¿Qué reanálisis se usa como fuente canónica: `correccion-01` o el de la nueva valoración? | A) `correccion-01` (modelo ordinal + Friedman/Wilcoxon); B) reanálisis de la valoración; C) reportar ambos y reconciliar | **A adoptada:** `correccion-01` es la fuente canónica; no usar el reanálisis de la valoración como sensibilidad | Autor + estadística | **Sí** para Tabla 4 y resultados |
| NV-02 | Métricas de recuperación y comparación de recuperadores | A) Calcular desde `part_d` y logs en un notebook nuevo; B) adoptar las cifras de la nueva valoración; C) ambas | **A adaptada:** Milvus no está disponible (se perdió el volumen Docker); calcular recall@k/MRR desde las recuperaciones ya registradas en los `.json` y guardar los resultados en `verificacion-analisis-estadistico/metricas_recuperacion/`. No comparar contra BM25 desde la base | Autor | **Sí** para IX.1.9/IX.2.1 |
| NV-03 | Métricas deterministas de citas sobre las 711 respuestas | A) Extender `correccion-06` para extraer citas de las respuestas generadas y calcular precisión/recall/F1/inexistentes; B) usar solo las citas de las respuestas esperadas; C) dejar la rúbrica de jueces | **No prioritaria por tiempo:** posponer. Si se retoma, opción A. No bloquea la entrega | Autor | No para la entrega |
| NV-04 | Declaración de IA y antecedente de “referencia fabricada” | A) Declaración por etapas + revisión del historial; B) mantener la frase genérica; C) declaración mínima sin explicar el antecedente | **A adoptada:** extender la declaración a búsqueda bibliográfica, escritura, validación de citas, implementación y otras tareas. Revisar el antecedente de la “referencia fabricada” al redactar. Coordinar con PI-04 | Autor | **Sí** para IX.1.8 |
| NV-05 | “Esfuerzo predeterminado” vs. “desconocido” | A) Mantener “desconocido” (lo que prueban los logs); B) afirmar “predeterminado” porque el código no lo fija; C) documentar ambos | **Resuelta:** se usó el valor por defecto de la API. Pydantic AI 1.1.0 no fija `reasoning_effort`; `OpenAIChatModel` envía `NOT_GIVEN` (`models/openai.py:500`). El default efectivo es del proveedor: OpenAI documenta `medium` para GPT-5. Declarar “default del proveedor = medium”, no un default de Pydantic AI | Autor | No para aceptar; **sí** para precisión |
| NV-06 | Índice vectorial: IVF_FLAT vs. AUTOINDEX | A) Mantener D-12 y describir AUTOINDEX; B) verificar en Milvus el índice efectivo; C) aceptar IVF_FLAT de la nueva valoración | **A adoptada:** usar el valor del código (`AUTOINDEX`), que es el que se usaría si se recrea la base. No afirmar IVF_FLAT | Autor | **Sí** para coherencia de V.8/metodología |
| NV-07 | Actualización de Tabla 4/IX con los nuevos hallazgos | A) Incorporar recuperación, IA y cifras reconciliadas; B) dejar Tabla 4 como está y agregar anexo; C) solo cambios de forma | **A.** La nueva valoración cambia el sustento de V.1/V.6/V.8/V.11; Tabla 4 debe reflejarlo. Coordinar con PI-31 | Autor | **Sí** para la versión final |

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
| Agente de Calidad | Eliminar “no se tradujo en mejoras”; conservar solo costo/complejidad | 0 logs y 0 llamadas |
| 7/6 | Declarar la asimetría; no afirmar que todas las configuraciones usaron seis búsquedas | 33/79 sesiones de gpt-5 agotaron 7; mini/nano usaron 6 |
| `16_01` | Declarar la excepción de tres llamadas | 236/237 sesiones con una llamada |
| Índice vectorial | Describir `AUTOINDEX` con similitud coseno y quitar “IVF_FLAT”; no usar IVF_FLAT | `part_c/01_initial_vector_db_creation.ipynb`; D-12; NV-06 resuelta |
| Corpus | 482 nodos, 398 nodos artículo, 397 con texto y 1 vacío (art. 239); no decir “399 artículos” ni “245 artículos” | Auditoría 06; verificación de hashes |
| Fechas | Sanción 1886-11-25; texto ordenado B.O. 1997-05-30; no usar 1994-01-01 ni 2024-12-09 sin fuente | Auditoría 06 |
| Alpha | Reportar 0,807842 (original) y 0,799542 (rúbrica); no llamarlo validación | D-14; recálculo independiente |
| Costos | Usar costos históricos; reportar Pareto y costo por respuesta ≥ 0,75, sin el piso 0,01 | D-02, D-03, D-04 |
| “Primer sistema” | “No se identificaron antecedentes públicos comparables” | D-13 |
| Acceso público | Declarar acceso sin login; no afirmar reproducibilidad exacta sin clonación | D-11; verificación 2026-11-11 |
| Bibliografía factual | Aplicar las correcciones de Niklaus, DeepSeek, Llama 4, Qwen3, Yang/Wan, Pydantic, Springer, Zhao survey y Raeini | Corrección 07; 238 entradas, 45 decisiones manuales |

---

## 5. Ruta crítica recomendada

### 5.1 Decisiones que requieren cálculos (prioridad)

Estas decisiones no se resuelven solo redactando: su resultado numérico condiciona qué se puede afirmar en el manuscrito. Se ordenan por dependencia editorial, no por dificultad.

| Prioridad | Decisión | Cálculo requerido | Salida | Condiciona |
|---|---|---|---|---|
| **P0** | **NV-01** (V.1/V.6) | Reconciliar las cifras de la valoración con `correccion-01`: reproducir los p-valores 0,19 y 0,003 declarando prueba (Wilcoxon/t pareada), unidad (respuesta, caso o unidad), escenario y corrección (Holm/Bonferroni); verificar LR = 293,28, gl = 4, p = 3,05 × 10⁻⁶², efectos e IC. No reemplazar el modelo canónico | `verificacion-analisis-estadistico/reconciliacion_v1/` (tabla comparativa, JSON y notas de método) | Tabla 4; resultados V.1/V.6; redacción de PI-29 |
| **P0** | **NV-02** | Calcular recall@k, MRR y cobertura (todos/ninguno) desde las recuperaciones `.json` de `part_g`; reportar por estrategia y modelo. No requiere Milvus | `verificacion-analisis-estadistico/metricas_recuperacion/` (CSV, notebook y resumen) | IX.1.9, IX.2.1, V.8 y Tabla 4 |
| **P1** | **D-02** | Recalcular la proporción de respuestas correctas y el costo por respuesta correcta con umbrales 0,50, 0,75 y 1,00. El recálculo coincide exactamente con la tabla de corrección 05 | `verificacion-analisis-estadistico/sensibilidad_umbral/` | Tabla 4, análisis de costos y enunciado de D-02 |
| **P2** | **NV-03** | Extraer citas de las 711 respuestas generadas y calcular precisión, recall, F1 y tasa de citas inexistentes contra el corpus. Diferida: no bloquea la entrega | `verificacion-analisis-estadistico/citas_generadas/` o un anexo de `correccion-06` | IX.2.2 y V.7, solo si se retoma |

**Cálculos condicionales:** PI-08 no requiere un cálculo nuevo en esta entrega porque los 23 casos ya están identificados en la base final; solo un cambio de adjudicación obligaría a recalcular alpha. D-01 solo requiere el modelo de dos partes si se adopta esa sensibilidad opcional. **No requieren cálculo nuevo:** PI-29 (opción A: declarar Laplace; `nAGQ > 1` no es ejecutable con dos efectos aleatorios), PI-06/PI-07 (juicio humano), PI-09 (nuevas corridas) y NV-07/PI-31 (dependen de los resultados P0/P1).

### 5.2 Pendiente de decisión o verificación

1. **NV-03:** no prioritaria por tiempo; no bloquea la entrega.

### 5.3 Implementación

1. **P0 — NV-01:** reconciliar V.1/V.6 y fijar las cifras que se usarán en Tabla 4. No editar resultados antes de este paso.
2. **P0 — NV-02:** calcular recuperación desde los `.json` y dejar el artefacto reproducible en `verificacion-analisis-estadistico/metricas_recuperacion/`.
3. **P1 — D-02:** sensibilidad 0,50/0,75/1,00 y costo por respuesta correcta verificados en `verificacion-analisis-estadistico/sensibilidad_umbral/`; coinciden con corrección 05.
4. **PI-04 / NV-04:** redactar la declaración de IA por etapas y revisar el antecedente de la “referencia fabricada”. **NV-05:** declarar que se usó el valor por defecto de la API: Pydantic AI 1.1.0 no fija `reasoning_effort` y envía `NOT_GIVEN`; OpenAI documenta `medium` para GPT-5, pero no hay registro local del valor efectivo.
5. **PI-21, PI-22, PI-23, PI-24, PI-26, PI-27 y PI-28:** aplicar las correcciones bibliográficas decididas. **PI-24:** usar `tribunalfiscal2024buscador` con la página institucional verificada; no usar la nota de AUNO como fuente institucional. **PI-25:** verificar en el PDF las cinco claves de `§6.4`; ya están aplicadas.
6. **PI-29:** mantener `nAGQ = 1`, declarar la limitación de Laplace y usar las cifras reconciliadas de NV-01.
7. **PI-03, PI-05, PI-10 y PI-11:** aplicar textos de arquitectura, terminología, excepción `16_01` y notebook canónico.
8. **PI-06, PI-07, PI-08, PI-12, PI-15, PI-16, PI-18, PI-19 y PI-32:** declarar la revisión humana y sus límites, fijar el proceso del corpus, corregir 1.2/1.3 y fechas, y usar el conteo de preguntas revisadas.
9. **PI-01, PI-02 y PI-31 / NV-07:** actualizar plan/README y título/portada; sincronizar manuscrito, anexos y presentación con recuperación y cifras reconciliadas; generar una nueva versión.
10. **PI-30:** publicar la verificación después de revisar el manuscrito y ordenar el directorio; ejecutar `run_all.sh` y la clonación de prueba.
11. **P2 — NV-03:** retomar solo si el tiempo alcanza; no condiciona la entrega.

### 5.4 Verificación final

- `make pdf` compila sin errores.
- Búsquedas en el PDF: “sobrecarga agéntica”, “efecto igualador”, “LLM-as-a-Judge validado”, “temperatura 0” asociada a determinismo, “transferible”, “IVF_FLAT”, “245 artículos”, “399 artículos”, “n = 79” sin aclarar exclusiones.
- El PDF final no contiene “Bommasani y col., 2023” para el DOI de Bozdag, ni “Dahl y col., 2024” para Westlaw/Lexis, ni “DeepSeek 2026b”, ni “Meta 2026” para Llama 4.
- Las tablas de la corrección 01, la Tabla 4 de la corrección 05 y los textos del manuscrito usan las mismas cifras.
- Los 412 archivos del manifiesto de corrección 07 y los hashes de corrección 06 siguen coincidiendo.
- La clonación anónima incluye `verificacion-analisis-estadistico/` y permite ejecutar el análisis descriptivo y compilar el manuscrito.

---

## 6. Registro de decisión

**Estados:** `Cerrada` = decisión adoptada; `Cancelada` = explícitamente fuera de alcance; `Pendiente` = falta una elección o una verificación. Las opciones y recomendaciones están en `§3` para PI/NV y en `§2` para D; este registro contiene la decisión vigente. Decisiones registradas el **2026-11-12**.

### 6.1 Resumen

| Estado | IDs | Total |
|---|---|---:|
| Cerrada | D-01–D-14; PI-01–PI-12, PI-15, PI-16, PI-18, PI-19, PI-21–PI-32; NV-01, NV-02, NV-04, NV-05, NV-06, NV-07 | 48 |
| Cancelada | PI-13, PI-14, PI-17, PI-20 | 4 |
| Pendiente | NV-03 | 1 |
| **Total** | **D-01–D-14, PI-01–PI-32, NV-01–NV-07** | **53** |

### 6.2 Decisiones cerradas y canceladas

| ID | Estado | Decisión adoptada | Implementación / evidencia |
|---|---|---|---|
| D-01 | Cerrada | Fallo = 0 para el sistema; auditoría de jueces en un plano separado | `§2`; `D-01 — implementación en dos planos` |
| D-02 | Cerrada | “Respuesta correcta” = promedio ≥ 0,75; sensibilidad 0,50 y 1,00 | `§2`; verificado en `verificacion-analisis-estadistico/sensibilidad_umbral/` |
| D-03 | Cerrada | Costos históricos, no precios corrientes (USD 22,2939) | `§2`; mantener en manuscrito |
| D-04 | Cerrada | Sin ganador único: Pareto, costo por respuesta correcta y objetivo explícito | `§2`; aplicar en conclusiones |
| D-05 | Cerrada | “Modo de fallo de respuesta”, sin “sobrecarga agéntica” | `§2`; retirar causalidad |
| D-06 | Cerrada | Declarar asimetría 7/6; no atribuir el efecto de modelo a capacidad sin salvedad | `§2`; documentar |
| D-07 | Cerrada | Congelar benchmark v1; revisión profesional pendiente como trabajo futuro | `§2`; no crear v2 |
| D-08 | Cerrada | Declarar ausencia de validación humana; alpha como confiabilidad | `§2`; coordinar con PI-06/PI-08 |
| D-09 | Cerrada | Actualizar título al alcance real | `§2`; PI-02 |
| D-10 | Cerrada | Objetivo 2 como cumplimiento parcial; dos agentes activos, sin verificador | `§2`; insertar en manuscrito |
| D-11 | Cerrada | Acceso público sin login; clonación recomendada para reproducibilidad | `§2`; no afirmar reproducibilidad exacta |
| D-12 | Cerrada | Quitar “IVF_FLAT” y describir AUTOINDEX con similitud coseno | `§2`; NV-06 resuelta con AUTOINDEX |
| D-13 | Cerrada | “No se identificaron antecedentes públicos comparables” | `§2`; mantener cautela |
| D-14 | Cerrada | Alpha 0,807842 original y 0,799542 rúbrica | `§2`; recálculo independiente |
| PI-01 | Cerrada | Opción A: mantener `correccion-*` y marcar como deprecados los análisis previos que ya no se usan | Nota de ubicación incorporada en el plan; no se crea `part_k` |
| PI-02 | Cerrada | Opción A: título aprobado por correo por el director de la maestría | Título, portada, README y BibTeX actualizados |
| PI-03 | Cerrada | Opción A: aplicar textos, anexo y SVG operativo; actualizar el diagrama para respetar colores y límites | Arquitectura, agentes y SVG operativo actualizados en el manuscrito |
| PI-04 | Cerrada | Opción B: declaración de IA por etapas; incluye extracción, benchmark, respuestas, jueces, asistencia y verificación; antecedente de la referencia eliminada | Declaración incorporada en `01_texto_preliminar.typ`; PDF compilado |
| PI-05 | Cerrada | Opción A: “modelo del Agente Especialista Legal”; celdas agénticas como “recuperador gpt-5” | Terminología y etiquetas aplicadas en arquitectura y tablas |
| PI-06 | Cerrada | Opción A: no realizar validaciones humanas adicionales; declarar la ausencia | Ausencia declarada en limitaciones; PDF compilado |
| PI-07 | Cerrada | Opción A: aceptar la revisión del autor y declararla como tal | Declarada como revisión del autor, no independiente |
| PI-08 | Cerrada | Opciones A+B: los 23 casos ya están adjudicados en la base final; incluir el análisis | 23 discrepancias y 17 evaluaciones positivas documentadas en limitaciones |
| PI-09 | Cerrada | Opción A: no ejecutar nuevas corridas; declarar 7/6, recuperador fijo y ejecución única | Documentar la limitación |
| PI-10 | Cerrada | Opción A: declarar la excepción `16_01` de tres llamadas | Excepción incorporada en metodología y amenazas |
| PI-11 | Cerrada | Opción B: notebook de `part_g` exploratorio; script `.py` como fuente canónica | Nota incorporada en metodología; PDF compilado |
| PI-12 | Cerrada | Corpus: PDF 1997 + actualización manual con Infoleg + OCR histórico; proceso en 8 pasos | Ver `correccion-06/resumen_ejecutivo.md` §2 |
| PI-13 | Cancelada | Q23 se mantiene como fue revisada; no se reabre | Sin acción |
| PI-14 | Cancelada | Q24 se mantiene; el comentario no aplicado se documenta | Sin acción |
| PI-15 | Cerrada | No modificar benchmark v1; corregir el anexo de 1.3 y declarar la discrepancia | Anexo corregido con el texto del artículo 17; PDF compilado |
| PI-16 | Cerrada | Corregir solo el anexo de 1.2; el JSON y el corpus son correctos | Anexo corregido con el artículo 11; PDF compilado |
| PI-17 | Cancelada | Q13/Q22/Q25 fuera de alcance; no se reabren | Sin acción |
| PI-18 | Cerrada | Una sola profesional revisora; no existe segunda revisión independiente | “Revisión por una profesional” aplicada en todo el texto |
| PI-19 | Cerrada | Fechas: 1886-11-25 y 1997-05-30; eliminar las no verificadas | Fechas aplicadas en anexo y metodología; PDF compilado |
| PI-20 | Cancelada | No se crea benchmark v2 en esta tesis | Sin acción |
| PI-21 | Cerrada | Opción A: reemplazar Bommasani/Davis/Cardon por Bozdag, Sevim y Koç; reescribir las dos afirmaciones | Aplicada en `.bib` y texto; PDF compilado |
| PI-22 | Cerrada | Opción A: usar Magesh et al. (2025) para Westlaw/Lexis; conservar Dahl para su propio contenido | Aplicada en `.bib` y texto; PDF compilado |
| PI-23 | Cerrada | Opción A: APA con nombres/iniciales para Wei/Zhao, sin letras a/b | Aplicada en citas y texto; PDF compilado |
| PI-24 | Cerrada | Opción A con la página institucional verificada (`https://www.argentina.gob.ar/tribunalfiscal/jurisprudencia`), que enlaza al buscador asistido por IA. El endpoint directo no respondió desde este entorno (timeout) | Entrada y cita actualizadas; PDF compilado |
| PI-25 | Cerrada | Se adoptan las cinco entradas de `§6.4`: Hebb 2005, Minsky 2017, Miceli 2010 (Bonferroni), Jordan 1997 y Krippendorff 2019; claves actualizadas | Citas y `.bib` actualizados; PDF compilado |
| PI-26 | Cerrada | Opción B: `et al.` estricto APA 7, como solicita el tribunal | Reglas de traducción eliminadas; PDF usa `et al.` |
| PI-27 | Cerrada | Opción A: aplicar el paquete de correcciones factuales verificadas | Aplicada en `.bib` y texto; PDF compilado |
| PI-28 | Cerrada | Opción A: agregar Lewis, Código de Minería, Zheng, Bench-Capon, Tribunal Fiscal y Qwen3 | Referencias incorporadas y citadas; PDF compilado |
| PI-29 | Cerrada | Opción A: mantener `nAGQ = 1` (Laplace) y declarar la limitación; reconciliar con NV-01 | Limitación y método incorporados en capítulos 5 y 8; `nAGQ > 1` no está disponible en `clmm` con dos efectos aleatorios |
| PI-30 | Cerrada | Opción A: publicar después de revisar el manuscrito y ordenar el directorio | Ejecutar `run_all.sh`, clonación y registro al final |
| PI-31 | Cerrada | Opción A: aplicar todo y generar una nueva versión del archivo | Sincronización principal aplicada; PDF recompilado |
| PI-32 | Cerrada | 25 preguntas: 18 intervenidas, 17 corregidas, Q24 solo comentario, 7 sin intervención | Conteo incorporado en metodología; `correccion-06/salidas/conteo_preguntas_revisadas.csv` |
| NV-01 | Cerrada | Opción A: `correccion-01` como fuente canónica; no usar el reanálisis de la valoración | Reconciliado en `verificacion-analisis-estadistico/reconciliacion_v1/`; usar p Holm en V.1 y Pratt en V.6 |
| NV-02 | Cerrada | Opción A adaptada: sin Milvus; recall@k/MRR desde las recuperaciones `.json` | Calculado en `verificacion-analisis-estadistico/metricas_recuperacion/`; sin comparación BM25 |
| NV-04 | Cerrada | Opción A: extender la declaración a búsqueda bibliográfica, escritura, validación de citas, implementación y otras tareas; revisar el antecedente de la “referencia fabricada” | Declaración incorporada en `01_texto_preliminar.typ`; PDF compilado |
| NV-05 | Cerrada | Se usó el valor por defecto de la API: Pydantic AI 1.1.0 no fija `reasoning_effort` y envía `NOT_GIVEN`; el default efectivo de OpenAI para GPT-5 es `medium` | Nota incorporada en método y declaración; PDF compilado |
| NV-06 | Cerrada | Opción A: usar AUTOINDEX, valor del código; no afirmar IVF_FLAT | Aplicar en V.8/metodología |
| NV-07 | Cerrada | Opción A: incorporar recuperación, IA y cifras reconciliadas a Tabla 4/IX | Cifras, recuperación y conclusiones incorporadas en evaluación y conclusiones |

### 6.3 Decisiones pendientes

| ID | Tema | Qué falta decidir / verificar | Recomendación / bloqueo | Responsable |
|---|---|---|---|---|
| NV-03 | Citas deterministas | Métricas de citas sobre las 711 respuestas | **No prioritaria por tiempo**: posponer; cálculo P2 en `§5.1`; no bloquea la entrega | Autor |

### 6.4 PI-25 — Entradas adoptadas

| Clave nueva | Entrada | DOI | Cambio |
|---|---|---|---|
| `hebb2005organization` | Hebb, 2005, Routledge; nota “Originally published in 1949” | `10.4324/9781410612403` | Reemplaza `hebb1949organization` |
| `minsky2017perceptrons` | Minsky y Papert, 2017, MIT Press; reissue de la edición ampliada de 1988 | `10.7551/mitpress/11301.001.0001` | Reemplaza `minsky1969perceptrons` |
| `bonferroni2010teoria` | Miceli, 2010, en *Encyclopedia of Research Design*, ed. Salkind | `10.4135/9781412961288.n455` | Reemplaza `bonferroni1936teoria` |
| `jordan1997` | Jordan, 1997, *Neural-Network Models of Cognition*, pp. 471–495 | `10.1016/S0166-4115(97)80111-2` | Reemplaza `jordan1986` |
| `krippendorff2019content` | Krippendorff, 2019, 4.ª ed., SAGE | `10.4135/9781071878781` | Reemplaza `krippendorff2018content` |

PI-25 se cerró cuando el autor aportó estas cinco entradas; los DOIs de la tabla son los verificados. Las entradas se incorporaron a `manuscrito/referencias.bib`; las citas de `manuscrito/capitulos/03_capitulo_02...typ`, `06_capitulo_05...typ` y `07_capitulo_06...typ` se actualizaron con las claves nuevas. `make pdf` compiló sin errores.

---

## 7. Criterio de cierre

Se considera cerrado este registro cuando:

1. cada `PI-*` y `NV-*` tiene una decisión escrita, incluso si la decisión es “se declara como limitación”;
2. ninguna decisión contradice D-01–D-14 sin una actualización explícita de esas decisiones;
3. el manuscrito, el README y la presentación usan las mismas cifras, etiquetas y fuentes;
4. los paquetes de corrección y la verificación están versionados y una clonación anónima reproduce el análisis;
5. el PDF final no contiene afirmaciones de causalidad, equivalencia, determinismo o validación humana que los datos no sostengan.

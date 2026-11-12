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
| `correccion-05-actualizacion-conclusiones-y-analisis-costos` | Tabla 4 reformulada, costos, Pareto, propuestas de texto y README | `verificacion_artefactos.json`: 46 controles, 0 fallos; 9 celdas, 711 observaciones, costo USD 22,2939 | **OK** | Aprobación institucional del título (PI-02) y conflicto D-01/D-08 (PI-06) |
| `correccion-06-precisar-corpus-revisar-respuestas` | Linaje del corpus, conteos, revisión de la abogada y benchmark v2 | Verificador: 130 cambios, 80 párrafos, 482 nodos, 398 artículos, 79 unidades, 166 referencias y 12 propuestas; hashes fuente sin cambios | **OK** | Procedencia Infoleg y decisiones Q23–Q25/art. 17 (PI-11 a PI-17) |
| `correccion-07-forma-y-bibliografia` | Auditoría de 238 referencias, Tablas 2 y 3, propuestas BibTeX | Verificador: 412 archivos del manifiesto coinciden; 238 entradas, 0 claves huérfanas; 45 decisiones manuales | **OK** | Seis decisiones editoriales y paquete de correcciones factuales (PI-20 a PI-27) |
| `verificacion-analisis-estadistico` | Recálculo independiente de alpha, Spearman, 23 discrepancias y 17 evaluaciones positivas | Alpha recalculado en memoria desde `final_judge_results.csv`: 0,807842 original y 0,799542 rúbrica; coincide con el informe | **OK** | El directorio no está versionado; revisión humana de los 23 casos (PI-08, PI-29) |

### 1.2 Comprobaciones técnicas realizadas

- Los 31 archivos Python de los paquetes compilan en memoria; no se ejecutaron notebooks que pudieran sobrescribir salidas.
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
7. **La decisión D-01 del autor dice que “la corrección humana predomina”**, pero no existen calificaciones humanas de las 711 respuestas. La única revisión humana documentada es la del benchmark. Esta es la principal contradicción pendiente.
8. **El modelo ordinal usa `nAGQ = 1`** y no incluye una prueba formal de odds proporcionales. Es aceptable como análisis principal, pero conviene declararlo y añadir una sensibilidad si el costo computacional lo permite.
9. **El benchmark v1 está congelado**, pero la revisión asistida por LLM detectó posibles errores que requieren revisión profesional. No debe llamarse “validación” a esa revisión automática.
10. **La bibliografía tiene 45 decisiones manuales:** 2 críticas, 11 altas, 12 medias y 20 bajas. Las dos críticas son Bozdag/Bommasani y Magesh/Dahl; no son opcionales.

---

## 2. Decisiones ya cerradas que no deben reabrirse

Estas decisiones fueron aceptadas por el autor en `correccion-05-actualizacion-conclusiones-y-analisis-costos/DECISIONES.md`. Se listan para evitar duplicados; solo se reabren si el autor cambia explícitamente de posición.

| ID | Decisión aceptada | Estado de implementación | Observación |
|---|---|---|---|
| D-01 | Escenario principal: respuestas no sustantivas = 0, con exclusión como sensibilidad | Aceptada | El autor añadió que “la corrección humana predomina”; eso no es posible con los datos actuales (ver PI-06) |
| D-02 | “Respuesta correcta” = puntaje promedio ≥ 0,75, con sensibilidad 0,50 y 1,00 | Aceptada | Documentar que es una operacionalización normativa |
| D-03 | Costos históricos registrados, no precios corrientes | Aceptada | Total USD 22,2939 |
| D-04 | Sin ganador único: Pareto, costo por respuesta correcta y objetivo explícito | Aceptada | RAG básico + nano es el menor costo puntual; no es “la mejor” en calidad |
| D-05 | “Modo de fallo de respuesta”, sin causalidad ni “sobrecarga agéntica” | Aceptada | 41/79 no sustantivas; 38/79 sustantivas con media 0,820 |
| D-06 | Declarar la asimetría 7/6 y no atribuir el efecto de modelo a capacidad sin salvedad | Aceptada | Queda por decidir si se repite la corrida (PI-09) |
| D-07 | Congelar benchmark v1; la revisión LLM detectó posibles errores que requieren revisión profesional | Aceptada | La revisión profesional sigue pendiente (PI-19) |
| D-08 | Declarar ausencia de validación humana; alpha como confiabilidad, no validez | Aceptada | Documentar 23 discrepancias y 17 evaluaciones positivas (PI-08) |
| D-09 | Actualizar el título al alcance real | Aceptada | Requiere aprobación institucional (PI-02) |
| D-10 | Objetivo 2 como cumplimiento parcial; dos agentes activos, sin verificador | Aceptada | Solo falta insertarlo en el manuscrito |
| D-11 | Acceso público resuelto sin login; clonación recomendada para reproducibilidad | Aceptada | No bloquea el objetivo de acceso |
| D-12 | Quitar “IVF_FLAT” y describir `AUTOINDEX` con similitud coseno | Aceptada | Respaldado por `part_c` |
| D-13 | “No se identificaron antecedentes públicos comparables” en lugar de “primer sistema” | Aceptada | Mantener la cautela |
| D-14 | Recalcular alpha desde los jueces originales en un directorio independiente | Aceptada y verificada | Valores: 0,807842 y 0,799542; precisión legal 0,784566 |

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
| PI-06 | Cómo conciliar D-01/D-08 con la ausencia de calificaciones humanas de las respuestas | A) Declarar que no hay medición humana de las 711 respuestas y retirar “la corrección humana predomina”; B) realizar una submuestra ciega de ~90 respuestas (10 por celda) con 1–2 profesionales; C) realizar las 711 (no viable) | **B si hay disponibilidad; A en caso contrario.** Si se elige B, actualizar D-01 y la conclusión; si se elige A, no afirmar superioridad del criterio humano | Autor + directores + profesionales | **Sí** para cualquier afirmación sobre validez humana |
| PI-07 | Independencia de la revisión de las 87 respuestas no sustantivas | A) Aceptar la revisión del autor y declararla como tal; B) pedir una segunda revisión ciega de las 87; C) presentarla como validación independiente sin evidencia | **A para la defensa; B si se busca robustez.** Nunca C. La revisión actual tiene 98,9% de acuerdo automático–manual y una discrepancia conocida (`R052`) | Autor | No para el análisis principal; **sí** para la palabra “independiente” |
| PI-08 | Tratamiento de las 23 discrepancias entre jueces y las 17 evaluaciones positivas sobre salidas no sustantivas | A) Incluirlas como anexo/material suplementario y no recalcular; B) adjudicar humanamente los 23 casos; C) omitirlas | **A + B si hay tiempo.** No promediar las 17 evaluaciones positivas como calidad. Si se adjudican, conservar el análisis principal y reportar la sensibilidad | Autor + profesionales | No para el resultado principal; **sí** para la validez de los jueces |

### Bloque C — Diseño experimental y reproducibilidad

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-09 | ¿Se ejecutan nuevas corridas para eliminar confundidos? | A) No ejecutar; declarar 7/6, recuperador fijo y ejecución única; A′) repetir solo Agentic-RAG + gpt-5 con límite 6; B) diagonal R = S (2 celdas nuevas); C) factorial 3×3 de recuperador (8 celdas nuevas) | **A para la versión definitiva.** Si se quiere sostener una afirmación causal o el jurado lo exige, hacer **A′** antes que B/C: es la intervención más barata que elimina un confundido real. A′/B/C vencen el **2026-12-11** y requieren presupuesto y evaluación con jueces | Autor + directores | **Sí** para cualquier afirmación causal o de estabilidad entre corridas |
| PI-10 | Excepción `16_01` (tres llamadas del especialista) | A) Declararla como excepción documentada; B) repetir la sesión; C) omitirla | **A.** El log es público y 236/237 sesiones respetan el límite nominal. Si se ejecuta A′, repetir también `16_01` y conservar el registro histórico | Autor | No, pero afecta la afirmación “una sola delegación” |
| PI-11 | Notebook de `part_g` frente al script final | A) Actualizar el notebook para que coincida con el script/logs; B) marcarlo como exploratorio y declarar el script como fuente canónica; C) dejarlo sin aclaración | **B inmediato; A si hay tiempo.** La reproducibilidad debe apoyarse en el script `.py` y en los logs, no en un notebook desactualizado | Autor | No para el análisis; **sí** para la reproducibilidad |

### Bloque D — Corpus, benchmark y respuestas de referencia

| ID | Decisión pendiente | Opciones | Recomendación | Responsable | Bloquea |
|---|---|---|---|---|---|
| PI-12 | Procedencia del texto actualizado de Infoleg | A) Incorporación manual documentada; B) incorporación mediante parser, indicando ruta y versión; C) no se puede reconstruir | **A o B con evidencia.** Si no se recuerda, describir “incorporación controlada del texto actualizado” solo si es cierto y dejar la ruta/versión como limitación. No afirmar que Infoleg “se descartó por completo” | Autor | **Sí** para la sección de corpus |
| PI-13 | Q23 (Río Turbio) | A) Mantener con nota de alcance; B) rotular como régimen especial y agregar normas; C) mover a anexo | **A para v1; B/C para v2.** La revisora no pidió eliminar Q23; el caso que propuso eliminar es el de hidrocarburos. No atribuirle una decisión que no tomó | Autor + abogada | No para v1; **sí** para v2 |
| PI-14 | Q24 (Ley 24.585) | A) Aclarar que es la ley de protección ambiental minera; B) mover a anexo; C) dejarla como está | **A para v2; nota de alcance en v1.** La pregunta actual presupone conocimiento de la ley | Autor + abogada | No para v1; **sí** para v2 |
| PI-15 | Q1.3 y paráfrasis del artículo 17 | A) Reproducir literalmente el artículo 17; B) paráfrasis aprobada por la abogada; C) reformular la pregunta | **A + revisión de la abogada.** No usar “solo” ni “seguridad o ambiental”: el artículo 17 incluye seguridad pública, conservación de las pertenencias y salud o existencia de los trabajadores | Abogada | **Sí** para la exactitud jurídica |
| PI-16 | Q1.2: artículo 8 frente a artículo 11 | A) Corregir solo el anexo Typst; B) crear v2 con artículo 18 si se conserva “tiempo ilimitado”; C) ambas | **C.** Corregir el anexo ahora (art. 11 para propiedad distinta; 7 y 10 para dominio/concesión) y decidir el art. 18 en v2 | Autor + abogada | No para v1; **sí** para v2 |
| PI-17 | Referencias de Q13.2, Q13.3, Q22.1 y Q25 | A) Agregar las referencias que las respuestas usan, previa revisión jurídica; B) anotar la discrepancia en v1 y corregir en v2; C) dejar solo las referencias actuales | **B para v1; A para v2.** En v1 no cambiar las respuestas ni volver a puntuar; documentar la diferencia | Autor + abogada | No para v1; **sí** para v2 |
| PI-18 | Segunda revisión independiente del benchmark | A) Confirmar que existe y documentarla; B) declarar que hubo una sola revisión profesional; C) mantener “validado por profesionales” sin evidencia | **B.** La evidencia disponible es una revisión con control de cambios, no una segunda revisión. Cambiar “validado” por “revisado por una profesional” | Autor | **Sí** para la afirmación de validación |
| PI-19 | Fechas y metadatos del benchmark | A) Usar 1886-11-25 (sanción), 1997-05-30 (texto ordenado) y eliminar 1994-01-01/10/15 y 2024-12-09 no verificados; B) conservar los metadatos fuente y explicar que son erróneos; C) usar una fecha de “última actualización” solo si se identifica la versión | **A.** Si se conserva una fecha de actualización, que sea la de la versión efectivamente consultada y con fuente. No presentar 2024-12-09 como verificado | Autor | **Sí** para el anexo y la metodología |
| PI-20 | Alcance y publicación del benchmark v2 | A) Congelar v1 para la tesis y publicar v2 como anexo/trabajo futuro; B) publicar v2 ahora con revisión profesional; C) publicar v2 solo con la revisión LLM | **A para la tesis; B si hay revisión profesional antes de la entrega.** La revisión LLM es un tamiz, no una validación jurídica | Autor + abogada | No para la defensa; **sí** para la contribución del benchmark |

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
2. **PI-06 y PI-07:** decidir si habrá una submuestra humana o si se declara la ausencia; no escribir “la corrección humana predomina” sin datos.
3. **PI-09:** decidir si se ejecuta A′/B/C antes del **2026-12-11**; si no, declarar la ejecución única y la asimetría 7/6.
4. **PI-12 a PI-20:** cerrar procedencia del corpus, Q23–Q25, art. 17, fechas y alcance de v2 con la abogada.
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
| PI-01 | | | | |
| PI-02 | | | | |
| PI-03 | | | | |
| PI-04 | | | | |
| PI-05 | | | | |
| PI-06 | | | | |
| PI-07 | | | | |
| PI-08 | | | | |
| PI-09 | | | | |
| PI-10 | | | | |
| PI-11 | | | | |
| PI-12 | | | | |
| PI-13 | | | | |
| PI-14 | | | | |
| PI-15 | | | | |
| PI-16 | | | | |
| PI-17 | | | | |
| PI-18 | | | | |
| PI-19 | | | | |
| PI-20 | | | | |
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

---

## 7. Criterio de cierre

Se considera cerrado este registro cuando:

1. cada `PI-*` tiene una decisión escrita, incluso si la decisión es “se declara como limitación”;
2. ninguna decisión contradice D-01–D-14 sin una actualización explícita de esas decisiones;
3. el manuscrito, el README y la presentación usan las mismas cifras, etiquetas y fuentes;
4. los paquetes de corrección y la verificación están versionados y una clonación anónima reproduce el análisis;
5. el PDF final no contiene afirmaciones de causalidad, equivalencia, determinismo o validación humana que los datos no sostengan.

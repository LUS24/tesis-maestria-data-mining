# Resumen ejecutivo — IX.1.7

**Alcance:** artefactos para corregir las Tablas 2 y 3 y auditar la bibliografía. **No se modificó ningún archivo existente** del manuscrito, del `.bib`, de los datos ni de los logs. Todo lo nuevo está en `analisis-valoracion-jurado/correccion-07-forma-y-bibliografia/`.

## 1. Qué se hizo

1. Se parsearon las **238 entradas** de `manuscrito/referencias.bib` y se extrajeron las citas de los 11 archivos `.typ`.
2. Se identificaron **238 entradas citadas** y **0 no citadas**; no hay claves citadas sin entrada. La primera extracción tuvo un falso negativo porque el regex incluía los dos puntos finales de algunas citas; se corrigió.
3. Se consultaron **79 DOI** en Crossref/DataCite, **87 identificadores arXiv** en el API de arXiv y **172 URL**.
4. Se compiló el manuscrito actual y se extrajo la lista de referencias renderizada para comprobar cómo resuelve Typst/APA los casos dudosos.
5. Se cotejaron los ítems de las Tablas 2 y 3 con el texto, el `.bib`, los datos y las fuentes primarias.
6. Se prepararon propuestas de reemplazo, renombres, adiciones y edición, sin aplicarlas.

## 2. Cifras de la auditoría

| Indicador | Resultado |
| --- | ---: |
| Entradas en `referencias.bib` | 238 |
| Entradas citadas | 238 |
| Entradas no citadas | 0 |
| Claves citadas sin entrada | 0 |
| DOI consultados | 79 |
| DOI con respuesta 200 | 78 |
| DOI sin respuesta en Crossref (Jeong) | 1, verificado en KCI/arXiv |
| DOI con metadatos que coinciden plenamente | 61 |
| DOI con alguna discrepancia de autor, año o título | 18 |
| arXiv consultados | 87 |
| arXiv con coincidencia plena | 79 |
| arXiv con diferencia de año/título | 8, en su mayoría preprint vs. actas |
| URL consultadas | 172 |
| URL con respuesta 200/206/202 | 156 |
| URL con 403/401/405/429 | 15, bloqueo de bots o paywall |
| URL sin resolución DNS | 1, Lexium |
| Entradas sin DOI ni URL | 4 |

Los 18 DOI con discrepancia no son 18 errores fatales; la mayoría son diferencias de edición o de versión. Varios son diferencias esperables entre preprint y actas (BERTScore, ReAct, LawBench, Ariai, Wang), o metadatos de Crossref para actas (BLEU). La clasificación caso por caso está en `auditoria_bibliografia.md` y en `estado_por_entrada.csv`.

## 3. Hallazgos críticos de la Tabla 3

| Punto | Hallazgo | Acción propuesta |
| --- | --- | --- |
| Bommasani/Davis/Cardon | El DOI `10.1145/3628602` pertenece a **Bozdag, Sevim y Koç (2024)**, ACM TKDD 18(4). El método es **fine-tuning**, no “variantes de adapters”. | Reemplazar por `bozdag2024gender` y reescribir las dos afirmaciones de `04_capitulo_03...typ`. |
| Dahl et al. (2024) | La frase sobre Westlaw/Lexis corresponde a **Magesh et al. (2025)**, JELS 22(2), 216-242. El texto completo confirma 33% Westlaw, 17% Lexis/PL y 43% GPT-4. | Usar `magesh2025hallucinationfree` en `08_capitulo_07...typ:29`. |
| Wei 2022 / Zhao 2026 | El PDF renderiza “Wei y col., 2022” para dos obras distintas y “Zhao y col., 2026” para dos autores distintos. **Las letras a/b no son la regla APA en estos casos.** | Wei: agregar el segundo autor (`Wei, Wang` / `Wei, Tay`) y “y cols.”. Zhao: agregar iniciales (`W. X.` / `J.`). Ver §4. |
| DeepSeek-R1 | Hay dos entradas; una fechada en enero de 2026. El lanzamiento oficial fue el **20 de enero de 2025**. | Eliminar `deepseek_r1`; usar `deepseek2025r1`; corregir las dos fechas del capítulo 7. |
| Llama 4 | Fechado en marzo de 2026; Meta lo publicó el **5 de abril de 2025**. | Corregir `llama4` y las dos menciones del capítulo 7. |
| Qwen3 | El texto lo fecha en diciembre de 2025; Qwen3 se publicó el **29 de abril de 2025**. `qwen3_5` es Qwen 3.5 (2026). | Agregar `qwen2025qwen3` y corregir la frase de la línea 258. |
| LEXTREME | El año es **2023**, no 2024, y falta **Chalkidis** como sexto autor. | Usar `niklaus2023lextreme`; actualizar cinco citas. |
| Tribunal Fiscal | El autor institucional no corresponde a la URL: la URL es una nota de **AUNO Abogados**, autora **Milagros Denise Tallarico**. El sitio oficial es `https://jurisprudenciatfn.mecon.gob.ar/`. | Usar `tribunalfiscal2024buscador` o `tallarico_tfn`; no mezclar ambos. |
| Lewis et al. (2020) | No está citado. | Agregar `lewis2020rag` y citarlo al presentar RAG. |
| Código de Minería | No hay entrada legal. | Agregar `codigo_mineria_1919`. |

## 4. Corrección importante al pedido del jurado sobre APA

El informe del jurado pide “letras (2022a, 2022b)” para Wei 2022 y Zhao 2026. La regla APA 7 es más específica:

- **Wei 2022:** los dos trabajos tienen el mismo primer autor y año, pero **listas de coautores distintas**. APA 8.18 indica escribir tantos nombres como sean necesarios para distinguirlos, no asignar letras: `Wei, Wang, y cols. (2022)` y `Wei, Tay, y cols. (2022)`.
- **Zhao 2026:** los primeros autores tienen el mismo apellido pero **iniciales distintas**. APA 8.20 indica incluir las iniciales: `W. X. Zhao y cols. (2026)` y `J. Zhao y cols. (2026)`.

Typst ya asigna a/b a los autores institucionales del mismo año (OpenAI, Anthropic, Google, DeepSeek, etc.) y no asigna letras a Wei/Zhao, lo cual es coherente. La intervención debe ser manual solo en esos dos casos. Se probó la forma tipográfica en `pruebas/citas_ambiguas.typ`: `#cite(<clave>, form: "year")` permite escribir el autor desambiguado sin duplicar el año.

## 5. Hallazgos adicionales de la auditoría completa

- `raeini2025evolution`: el autor correcto es **Ghaseminejad Raeini, Mohammad**.
- `wan2025legalagents`: el primer autor es **Se Yang**, no Hao Wan; el texto debe decir “Yang et al.”.
- `springer2025trustworthy`: año **2025**, no 2026.
- `zhao2026surveySpringer`: la entrada usa `others` y una revista incorrecta; Crossref da **23 autores** y **Frontiers of Computer Science 20(12)**.
- `pydanticAI`: declara versión **2.0.0** y 2024; el proyecto usa **1.1.0**.
- `jeong2024graph`: el DOI no está indexado en Crossref, pero existe en KCI y arXiv; no es inventado.
- `hebb`, `minsky`, `bonferroni`, `jordan` y `krippendorff` tienen DOI de **otra edición**; conviene retirar el DOI o cambiar la edición citada.
- `markov1913` y `markov2006` no son un duplicado accidental: son original y traducción.
- `tunstall2022`, `rogers1951` y `levenshtein1966` no tienen DOI/URL; se documentan como excepciones, no se inventan identificadores.
- **No hay entradas no citadas**: las 12 que una primera extracción marcó como tales eran citas seguidas de dos puntos (`@clave:`), que el regex inicial no reconocía. La extracción corregida encuentra las 238 entradas citadas.

## 6. Decisiones que requieren revisión humana

1. **Bozdag:** confirmar la reescritura de las dos afirmaciones; el artículo no demuestra por sí solo una relación con decisiones judiciales reales.
2. **Magesh:** confirmar que se elimina `dahan2024stanford` o se conserva solo si se cita para su propio contenido.
3. **Wei/Zhao:** elegir entre la solución APA (nombres/iniciales) y la solución literal del jurado (a/b). La recomendación técnica es APA.
4. **Tribunal Fiscal:** elegir sitio oficial o nota de AUNO; no se pudo acceder al sitio oficial desde este entorno, aunque la búsqueda lo confirma.
5. **DOI de edición:** decidir si se retira el DOI o se cambia la edición citada en Hebb, Minsky, Bonferroni, Jordan y Krippendorff.
6. **Forma de autoría:** elegir “y cols.” (recomendado en español) o “et al.” (estricto APA). No dejar “y col.” singular.

## 7. Qué revisar primero

1. `propuesta_edicion_manuscrito.md`: texto actual y propuesto, archivo por archivo.
2. `cotejo_tablas_2_3.csv`: los 39 ítems con estado, acción, evidencia y prioridad.
3. `auditoria_bibliografia.md`: panorama completo y casos límite.
4. `propuestas_bibtex.bib`: 28 entradas propuestas, con comentarios de reemplazo/renombre.
5. `mapa_renombres.csv`: claves que cambian y ubicaciones de sus citas.
6. `estado_por_entrada.csv`: estado de las 238 entradas actuales.

## 8. Criterio de aceptación

- Las 238 entradas tienen estado de identificador o excepción documentada.
- Las 238 entradas tienen una cita y una ubicación verificable.
- No hay entradas no citadas ni claves huérfanas.
- Las correcciones de la Tabla 3 están aplicadas en el `.bib` y en el texto, no solo en este informe.
- El PDF final no contiene “Bommasani y col., 2023” para el DOI de Bozdag, ni “Dahl y col., 2024” para el estudio de Westlaw/Lexis, ni “DeepSeek 2026b”, ni “Meta 2026” para Llama 4.
- Las referencias cruzadas duplicadas desaparecen del PDF.
- La lista de referencias y las citas en el texto coinciden en autor, año y clave.

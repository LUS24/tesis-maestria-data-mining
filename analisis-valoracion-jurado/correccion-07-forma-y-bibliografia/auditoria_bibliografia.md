# Auditoría de la bibliografía y de las Tablas 2 y 3

Este informe documenta el estado de `manuscrito/referencias.bib` y de las citas del manuscrito. No modifica archivos existentes. Los datos completos están en los CSV de esta carpeta; aquí se explican los hallazgos y las decisiones propuestas.

## 1. Método

1. **Parseo del `.bib`:** se extrajeron tipo, clave, línea, autores, año, título, DOI, URL, `eprint`, `urldate` y `note` de las 238 entradas.
2. **Extracción de citas:** se recorrieron los 11 archivos `.typ` de `manuscrito/capitulos` y se capturaron tanto `#cite(<clave>)` como `@clave`. Se descartaron los `@preview` de importaciones y las etiquetas de figuras/secciones.
3. **Verificación de DOI:** consulta a Crossref; si no hay registro, a DataCite. Se comparó título, autores, año, venue y tipo.
4. **Verificación de arXiv:** consulta por lotes al API de arXiv para 87 identificadores; se comparó título, año y autores.
5. **Verificación de URL:** solicitud HTTP con rango de bytes; se registró estado, URL final, tipo de contenido y título de página. Un 401/403/405/429 se marca como **bloqueo de automatización**, no como recurso inexistente.
6. **Render:** se compiló el manuscrito actual con Typst 0.14.2 y se extrajo la lista de referencias para comprobar el resultado APA.
7. **Cotejo:** cada ítem de las Tablas 2 y 3 se contrastó con el texto, el `.bib`, el corpus cuando correspondía y las fuentes primarias.

**Límite explícito:** esta auditoría verifica identificadores y metadatos, no sustituye la lectura completa de las 238 obras citadas. Las afirmaciones que requieren lectura se listan en `cola_lectura_afirmaciones.csv`.

## 2. Estructura del archivo

| Indicador | Valor |
| --- | ---: |
| Entradas | 238 |
| Claves únicas | 238 |
| Entradas citadas | 238 |
| Entradas no citadas | 0 |
| Claves citadas sin entrada | 0 |
| DOI declarados | 79 |
| URL declaradas | 172 |
| Entradas sin DOI ni URL | 4 |
| Entradas con URL de arXiv | 87 |
| Entradas con fecha de consulta o “Accedido” | 43 |
| Grupos de autor–año potencialmente ambiguos | 16 |
| Grupos de DOI duplicado | 0 |
| Pares de títulos con similitud ≥ 0.90 | 7 |

Los siete pares de títulos similares son:

- `markov1913anexampleof` y `markov2006anexampleof`: **no es un duplicado accidental**; son el original ruso y su traducción inglesa.
- `anthropic_opus4_5`, `anthropic_opus4_6`, `anthropic_opus4_7`, `anthropic_opus4_8`: títulos de versiones distintas del mismo producto; no son duplicados.
- No se detectaron DOI duplicados.

## 3. Cobertura de identificadores

| Estado | Entradas |
| --- | ---: |
| DOI verificado y metadatos coincidentes | 61 |
| DOI responde pero metadatos a revisar | 17 |
| DOI no indexado; arXiv verificado | 1 |
| arXiv verificado (sin DOI) | 75 |
| URL responde (sin DOI/arXiv) | 68 |
| URL bloquea automatización | 11 |
| Sin identificador | 4 |
| URL no resuelve | 1 |
| Total | 238 |

La suma no coincide con 238 porque un mismo registro puede tener DOI y URL; `estado_por_entrada.csv` asigna un estado principal por entrada.

## 4. Discrepancias de DOI

De los 79 DOI, 78 respondieron con HTTP 200 y uno con 404 (Jeong). Las 18 discrepancias se clasifican así:

| Clave | DOI | Año registro → fuente | Discrepancia | Acción |
| --- | --- | --- | --- | --- |
| `raeini2025evolution` | 10.1016/j.nlp.2025.100168 | 2025 → 2025 | Autor: `Raeini` vs. `Ghaseminejad Raeini` | Corregir autor. |
| `niklaus2024lextreme` | 10.18653/v1/2023.findings-emnlp.200 | 2024 → 2023 | Año y sexto autor | Corregir; renombrar a 2023. |
| `papineni2002bleu` | 10.3115/1073083.1073135 | 2002 → 2001 | Crossref data 2001; ACL es 2002 | Conservar 2002; no es error real. |
| `zhang2019bertscore` | 10.48550/arXiv.1904.09675 | 2020 → 2019 | DOI del preprint; entrada ICLR 2020 | Conservar 2020. |
| `jeong2024graph` | 10.15813/kmr.2024.25.3.005 | 2024 → sin Crossref | DOI no indexado; KCI y arXiv lo confirman | Conservar con nota. |
| `wan2025legalagents` | 10.20517/aiagent.2025.06 | 2025 → 2025 | Primer autor: Wan vs. Yang | Reemplazar por Yang et al. |
| `springer2025trustworthy` | 10.1007/978-3-032-09318-9_1 | 2026 → 2025 | Año | Cambiar a 2025. |
| `jordan1986` | 10.1016/S0166-4115(97)80111-2 | 1986 → 1997 | DOI de capítulo de 1997 | Quitar DOI o cambiar edición. |
| `pascanu2013` | 10.48550/arXiv.1211.5063 | 2013 → 2012 | DOI del preprint; ICML 2013 | Conservar 2013. |
| `hebb1949organization` | 10.4324/9781410612403 | 1949 → 2005 | DOI de edición Routledge 2005 | Quitar DOI. |
| `minsky1969perceptrons` | 10.7551/mitpress/11301.001.0001 | 1969 → 2017 | DOI de edición 2017 | Quitar DOI. |
| `rumelhart1986parallel` | 10.7551/mitpress/5236.001.0001 | 1986 → 1986 | Título truncado en Crossref | Conservar; no es error real. |
| `press2022train` | 10.48550/arXiv.2108.12409 | 2022 → 2021 | DOI del preprint; ICLR 2022 | Conservar 2022. |
| `bommasani2022gender` | 10.1145/3628602 | 2023 → 2024 | Autores, año y revista equivocados | Reemplazar por Bozdag et al. |
| `wang2021milvus` | 10.1145/3448016.3457550 | 2021 → 2021 | Título truncado en Crossref (“Milvus”) | Conservar. |
| `kim2023prometheus` | 10.48550/arXiv.2310.08491 | 2024 → 2023 | DOI del preprint; ICLR 2024 | Conservar 2024. |
| `bonferroni1936teoria` | 10.4135/9781412961288.n455 | 1936 → 2010 | DOI de entrada de enciclopedia 2010 | Quitar DOI. |
| `krippendorff2018content` | 10.4135/9781071878781 | 2018 → 2019 | DOI online 2019; libro 2018 | Revisar y optar por una edición. |

**Errores reales de autor/año/venue:** `bommasani2022gender`, `niklaus2024lextreme`, `raeini2025evolution`, `wan2025legalagents`, `springer2025trustworthy`. Los demás son diferencias de edición, preprint o metadatos de Crossref.

## 5. Discrepancias de arXiv

De 87 identificadores arXiv, 79 coinciden plenamente. Los ocho restantes:

| Clave | Diferencia | Acción |
| --- | --- | --- |
| `islam2025hallucinate` | Título registrado vs. título actual de arXiv (“On Realistic Multilingual Estimation…”) | Actualizar solo si se cita la versión arXiv vigente. |
| `niklaus2024lextreme` | 2024 vs. 2023 | Corregir a 2023. |
| `yao2023react` | 2023 vs. 2022 | Conservar 2023 (ICLR 2023; arXiv 2022). |
| `xiong2025raggym` | Título ligeramente distinto | Revisar versión publicada; no es error de identificador. |
| `betancur2025mel` | Apellido del primer autor | Corregir contra la ficha de arXiv. |
| `fei2024lawbench` | 2024 vs. 2023 | Conservar 2024 si se cita la versión ACL/EMNLP; verificar. |
| `ariai2025nlp` | 2025 vs. 2024 | Conservar 2025 si se cita ACM CSUR; arXiv es 2024. |
| `wang2023large` | 2024 vs. 2023 | Conservar 2024 si se cita la versión publicada; verificar. |

## 6. URL

| Estado HTTP | Entradas |
| --- | ---: |
| 206 (contenido parcial) | 112 |
| 200 | 42 |
| 202 | 2 |
| 403 | 15 |
| Sin resolución DNS | 1 |
| Total | 172 |

Los 403 son, en su mayoría, **bloqueos de automatización o paywall**, no prueba de que el recurso no exista:

- OpenAI (varias entradas), ACM DL, ScienceDirect, ScholarWorks, DOI de Oxford.
- En esos casos el DOI o la búsqueda primaria confirma el recurso.
- `lexium2025` no resolvió por DNS desde este entorno, aunque la búsqueda web reporta el sitio activo. No se declara caída.

## 7. Entradas no citadas

**No hay entradas no citadas.** La primera extracción marcó 12 como no citadas porque el regex de `@clave` incluía los dos puntos finales de citas como `@asai2023selfrag:`. Al corregir el regex, las 238 entradas tienen al menos una cita. Este falso negativo muestra por qué el conteo de citas debe validarse contra el PDF y no solo contra un script.

## 8. Entradas sin DOI ni URL

| Clave | Obra | Tratamiento |
| --- | --- | --- |
| `markov1913anexampleof` | Markov, 1913, original ruso | Excepción documentada; existe traducción 2006 con DOI. |
| `tunstall2022natural` | Libro sobre Transformers | Agregar ISBN/URL editorial si se dispone; no inventar DOI. |
| `rogers1951clientcentered` | Libro clásico | Agregar ISBN de la edición consultada o documentar la excepción. |
| `levenshtein1966binary` | Artículo clásico | Excepción documentada; no inventar DOI. |

## 9. Ambigüedades autor–año

Se detectaron 16 grupos:

| Grupo | Entradas | Tratamiento |
| --- | --- | --- |
| Anthropic 2025 | 3 | Typst asigna a/b automáticamente; verificado en PDF. |
| Anthropic 2026 | 5 | Idem. |
| DeepSeek 2026 | 2 | Idem; además se elimina la duplicación de R1. |
| `fdeloche` 2017 | 2 | Dos imágenes del mismo autor; a/b automático. |
| Google 2026 | 2 | Idem. |
| Microsoft 2026 | 2 | Idem. |
| Moonshot AI 2026 | 2 | Idem. |
| OpenAI 2025 | 5 | Idem; PDF muestra 2025a–e. |
| OpenAI 2026 | 2 | Idem. |
| Rumelhart 1986 | 2 | Listas de autores distintas; APA pide nombres adicionales, no letras. |
| **Wei 2022** | 2 | **Requiere intervención manual:** `Wei, Wang, y cols.` / `Wei, Tay, y cols.` |
| **Zhao 2026** | 2 | **Requiere intervención manual:** `W. X. Zhao y cols.` / `J. Zhao y cols.` |
| Kim 2024 | 2 | Listas de autores distintas; APA pide nombres adicionales. |
| Li 2023 | 2 | Iniciales distintas; APA pide iniciales. |
| Li 2024 | 2 | Iniciales distintas; APA pide iniciales. |
| Wang 2024 | 2 | Iniciales distintas; APA pide iniciales. |

Typst ya resuelve los grupos institucionales con letras a/b. No se deben cambiar los años del `.bib` para forzar letras: eso produciría un resultado APA incorrecto en Wei/Zhao.

## 10. Preprints y versiones publicadas

| Entrada actual | Versión propuesta | Evidencia |
| --- | --- | --- |
| `devlin2018bert` (arXiv 2018) | `devlin2019bert`, NAACL 2019, DOI 10.18653/v1/N19-1423 | Crossref / ACL Anthology |
| `hu2021lora` (arXiv 2021) | `hu2022lora`, ICLR 2022, OpenReview nZeVKeeFYf9 | OpenReview / Microsoft |
| `dettmers2023qlora` (arXiv) | NeurIPS 36, 2023, DOI 10.52202/075280-0441 | Crossref / NeurIPS |
| `asai2023selfrag` (arXiv 2023) | `asai2024selfrag`, ICLR 2024, OpenReview hSyW5go0v8 | ICLR / OpenReview |
| `chalkidis2020legalbert` (arXiv) | Findings EMNLP 2020, DOI 10.18653/v1/2020.findings-emnlp.261 | Crossref / ACL Anthology |

No se propone cambiar el año de `press2022train` ni de `zhang2019bertscore`: el DOI es del preprint, pero la entrada cita correctamente ICLR 2022/2020.

## 11. DOI de edición o de otra obra

| Clave | Problema | Acción |
| --- | --- | --- |
| `hebb1949organization` | DOI de edición Routledge 2005 | Quitar DOI o citar 2005. |
| `minsky1969perceptrons` | DOI de edición MIT 2017 | Quitar DOI o citar 2017. |
| `bonferroni1936teoria` | DOI de entrada de enciclopedia 2010 | Quitar DOI. |
| `jordan1986` | DOI de capítulo 1997 | Quitar DOI o citar 1997. |
| `krippendorff2018content` | DOI online 2019 vs. libro 2018 | Elegir edición; quitar DOI si se conserva 2018. |

## 12. Correcciones adicionales de metadatos

| Clave | Problema | Corrección |
| --- | --- | --- |
| `raeini2025evolution` | Autor | `Ghaseminejad Raeini, Mohammad` |
| `wan2025legalagents` | Primer autor | `Yang, Se; Yang, Zhe; Liu, Yutong; Wang, Hongtao` |
| `springer2025trustworthy` | Año | 2025 |
| `zhao2026surveySpringer` | 23 autores y venue | Lista completa; Frontiers of Computer Science 20(12) |
| `pydanticAI` | Versión/año | 1.1.0, 2025 |
| `jeong2024graph` | DOI no Crossref | Conservar, nota KCI/arXiv |
| `zhao2026reportlogic` | Sin DOI | Correcto: arXiv 2602.18446 verificado |

## 13. Tabla 2: correcciones editoriales

El cotejo completo está en `cotejo_tablas_2_3.csv`. Los cambios de mayor impacto:

1. **Oración trunca** en `02_capitulo_01_introduccion.typ:13`.
2. **Definición de n-gramas** en `03_capitulo_02_fundamentos_e_historia_pln.typ:101`.
3. **“Similitud coseno escalada”** en `03_capitulo_02...typ:333`; es producto escalar.
4. **GPT-4/MoE** en `03_capitulo_02...typ:371`; la fuente no lo respalda.
5. **Legal-BERT** en `04_capitulo_03...typ:29` y `:65`; separar Chalkidis, Zheng y LegalBench.
6. **“245 artículos”** en `04_capitulo_03...typ:111`; evitar el número.
7. **Fechas de modelos** en `08_capitulo_07...typ:174,178,192,254,258,260`.
8. **Fecha de sanción** en `anexo_01.typ:251`.
9. **Referencias cruzadas duplicadas** en nueve lugares; lista exacta en la §14.
10. **Nota a Wikipedia** en `04_capitulo_03...typ:23`; reemplazar por Bench-Capon et al. (2012).
11. **Dedicatoria** y **declaración de IA** en `01_texto_preliminar.typ:13,18`.

### 13.1. Referencias cruzadas duplicadas

El PDF actual contiene, entre otras:

- “en el capítulo Sección 4” (`04:83`);
- “capítulo Sección 6” (`04:125`);
- “capítulo Sección 4” (`04:135`);
- “capítulo Sección 4” (`06:107`);
- “capítulo Sección 2” (`06:176`);
- “sección Sección 5.7.3” (`06:344`);
- “capítulo Sección 4, sección Sección 4.7” (`06:587`);
- “capítulo Sección 5” (`07:316`);
- “capítulo Sección 4” (`09:85`).

La causa es el sustantivo manual (“capítulo”/“sección”) sumado al suplemento automático de Typst. La solución es eliminar el sustantivo y dejar `@cap:...`/`@sec:...`, o usar `#ref(<...>, supplement: [sección])` si se necesita minúscula.

## 14. Tabla 3: problemas verificados y propuestas

### 14.1. Bommasani → Bozdag

- **Ubicación:** `04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:69,95`.
- **Problema:** el DOI `10.1145/3628602` corresponde a Bozdag, Sevim y Koç (2024), ACM TKDD 18(4), 1-26. El título es el mismo, pero los autores, el año y la revista son otros.
- **Método:** el resumen describe un método de **debiasing mediante fine-tuning** sobre el corpus del Tribunal Europeo de Derechos Humanos y una evaluación en LexGLUE; no “variantes de adapters”.
- **Propuesta:** reemplazar por `bozdag2024gender` y reescribir las dos afirmaciones. No atribuirle una correlación con decisiones judiciales reales si no está en el artículo.

### 14.2. Dahl → Magesh

- **Ubicación:** `08_capitulo_07_trabajos_relacionados.typ:29`.
- **Problema:** el estudio de Westlaw/Lexis es Magesh et al. (2025), JELS 22(2), 216-242, DOI `10.1111/jels.12413`. Dahl et al. (2024) es “Large Legal Fictions”, otro artículo.
- **Verificación:** el texto completo (apéndice B1) reporta 33% Westlaw, 17% Lexis+ AI, 17% Ask Practical Law AI y 43% GPT-4.
- **Propuesta:** citar `magesh2025hallucinationfree`; conservar `dahan2024stanford` solo si se usa para su propio contenido, que hoy no ocurre.

### 14.3. Wei y Zhao

- **Wei:** `wei2022cot` y `wei2022emergent` tienen el mismo primer autor y año, pero coautores distintos. APA 8.18 exige agregar nombres, no letras: `Wei, Wang, y cols. (2022)` y `Wei, Tay, y cols. (2022)`.
- **Zhao:** `zhao2026surveySpringer` (Wayne Xin Zhao) y `zhao2026reportlogic` (Jujia Zhao) comparten apellido pero no iniciales. APA 8.20 exige iniciales: `W. X. Zhao y cols. (2026)` y `J. Zhao y cols. (2026)`.
- **Implementación:** usar `Wei, Wang, y cols. (#cite(<wei2022cot>, form: "year"))`, etc. La prueba `pruebas/citas_ambiguas.typ` confirma que `form: "year"` evita duplicar el año.

### 14.4. DeepSeek

- **Ubicación:** `08:174,254`.
- **Problema:** `deepseek_r1` fecha DeepSeek-R1 en enero de 2026 y duplica `deepseek2025r1`.
- **Solución:** eliminar `deepseek_r1`; usar `deepseek2025r1`; cambiar “enero de 2026” por “enero de 2025”. La página oficial confirma el 20 de enero de 2025.

### 14.5. Llama 4 y Qwen3

- **Llama 4:** `08:178,260`; Meta publicó el 5 de abril de 2025, no marzo de 2026. Corregir entrada y texto.
- **Qwen3:** `08:258`; Qwen3 es del 29 de abril de 2025. `qwen3_5` es Qwen 3.5 (2026). Agregar `qwen2025qwen3` y corregir la frase.
- **Gemini 3 Pro:** `08:192`; el timeline y la fuente oficial usan 18 de noviembre de 2025; el texto dice 20. Corregir solo el texto.

### 14.6. LEXTREME

- **Ubicación:** cinco citas (`02:37`, `04:11,15,99`, `08:93`).
- **Problema:** año 2024 en lugar de 2023; falta Chalkidis.
- **Solución:** `niklaus2023lextreme`, seis autores, Findings EMNLP 2023, pp. 3016-3054, DOI `10.18653/v1/2023.findings-emnlp.200`.

### 14.7. Tribunal Fiscal

- **Ubicación:** `08_capitulo_07_trabajos_relacionados.typ:41`.
- **Problema:** la entrada usa autor institucional “Tribunal Fiscal de la Nación” pero la URL es una nota de AUNO Abogados, cuya autora es Milagros Denise Tallarico. El sitio oficial es `https://jurisprudenciatfn.mecon.gob.ar/`.
- **Solución:** elegir una:
  - `tribunalfiscal2024buscador`, autor institucional y sitio oficial; o
  - `tallarico_tfn`, autora real y URL de la nota.
- No mezclar autor institucional con URL de un estudio jurídico.

### 14.8. Lewis y Código de Minería

- **Lewis et al. (2020):** falta; agregar `lewis2020rag` y citarlo al presentar RAG en `02:11`.
- **Código de Minería:** falta; agregar `codigo_mineria_1919` y citarlo en `06:47`.

### 14.9. Forma de autoría

El PDF contiene **309 “y col.”** y **11 “y cols.”**. `main.typ:27-39` traduce `et al.` a “y col.” y `& others` a “y cols.”. Hay dos opciones coherentes:

- **Recomendada en español:** usar “y cols.” en ambas reglas; es plural y concuerda con “y colaboradores”.
- **Estricta APA:** dejar “et al.” y eliminar las reglas de traducción.

No dejar “y col.” singular y “y cols.” plural mezclados.

## 15. Cola de lectura de afirmaciones

La auditoría de metadatos no valida por sí sola las afirmaciones. Las siguientes requieren lectura o revisión jurídica:

1. Bozdag et al. (2024): qué mide exactamente y qué no demuestra sobre sesgos en decisiones judiciales.
2. Chalkidis et al. (2020): corpus real de Legal-BERT y alcance de sus resultados.
3. Zheng et al. (2021): relación con Case Law Access Project y CaseHOLD.
4. Guha et al. (2023): número de tareas y fecha; no usar para evaluar un modelo de 2020.
5. Magesh et al. (2025): ya se verificaron los porcentajes 17/33/43 en el apéndice B1.
6. Raeini/Ghaseminejad Raeini (2025): autoría; no afecta la afirmación sustantiva.
7. Yang et al. (2025): revisión de agentes legales; el texto debe dejar de atribuirla a Wan.
8. Código de Minería: fuente oficial y fecha de sanción.
9. Tribunal Fiscal: cuál es la fuente que se quiere citar (sistema oficial o nota).
10. Cualquier afirmación sobre “adapters” en Bozdag: el artículo usa fine-tuning.

El detalle está en `cola_lectura_afirmaciones.csv`.

## 16. Conclusión

La bibliografía es amplia y, en general, trazable: las 238 entradas se usan, no hay claves huérfanas y la mayoría de los DOI responde. Los problemas graves están concentrados en pocas entradas: Bozdag/Bommasani, Magesh/Dahl, DeepSeek, Llama/Qwen, LEXTREME y Tribunal Fiscal. La auditoría completa añade correcciones de autoría y año que no estaban en la Tabla 3, y separa las discrepancias reales de las diferencias esperables entre preprint, acta y edición.

La decisión más importante antes de editar es **no aplicar letras a/b a Wei/Zhao**: la solución APA correcta es agregar nombres o iniciales. El resto de las propuestas están en `propuesta_edicion_manuscrito.md` y `propuestas_bibtex.bib`.

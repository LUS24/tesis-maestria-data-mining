# Propuesta de edición del manuscrito (IX.1.7)

Este documento propone cambios concretos para los archivos `.typ` y el `.bib`. **No modifica ningún archivo existente**: las citas “Actual” son el texto que hoy figura en el repositorio y las “Propuesto” son textos para revisar antes de editar. Los números de línea corresponden al estado auditado el 2026-11-12.

## 0. Convenciones

- Se recomienda usar **“y cols.”** de forma uniforme (plural de “y colaboradores”). Si se prefiere APA estricto, usar **“et al.”** en todo el texto y eliminar las reglas de traducción de `main.typ`.
- Las claves nuevas están en `propuestas_bibtex.bib`; los renombres y sus citas están en `mapa_renombres.csv`.
- No se deben pegar las 28 entradas de `propuestas_bibtex.bib` al final del `.bib` sin reemplazar las existentes: hay claves repetidas a propósito para indicar reemplazo.

## 1. Tabla 2 — correcciones editoriales

### 1.1. Oración trunca

**Archivo:** `manuscrito/capitulos/02_capitulo_01_introduccion.typ:13`

**Actual**

> Al combinar grandes modelos de lenguaje (LLM) con mecanismos de recuperación de información. La incorporación de agentes inteligentes en este proceso, conocida como Agentic-RAG, añade capacidades de planificación, razonamiento y adaptación @singh2025agentic.

**Propuesto**

> La combinación de grandes modelos de lenguaje (LLM) con mecanismos de recuperación de información permite fundamentar las respuestas en documentos externos. La incorporación de agentes inteligentes en este proceso, conocida como Agentic-RAG, añade capacidades de planificación, razonamiento y adaptación @singh2025agentic.

### 1.2. Definición de n-gramas

**Archivo:** `manuscrito/capitulos/03_capitulo_02_fundamentos_e_historia_pln.typ:101`

**Actual**

> Esta estrategia se basa en el uso de n-gramas, los cuales consisten en secuencias de caracteres de longitud $n$. Por ejemplo, para la frase ...

**Propuesto**

> Esta estrategia se basa en el uso de n-gramas, es decir, secuencias de $n$ unidades contiguas (palabras, caracteres o tokens). En el ejemplo siguiente las unidades son palabras, por lo que un bigrama es una secuencia de dos palabras y un trigrama, de tres.

**Por qué:** la definición y el ejemplo deben usar la misma unidad. Si se quiere hablar de n-gramas de caracteres, debe cambiarse el ejemplo y la ecuación.

### 1.3. Atención escalada

**Archivo:** `manuscrito/capitulos/03_capitulo_02_fundamentos_e_historia_pln.typ:333`

**Actual**

> La atención entre una query y todas las keys se calcula como la similitud coseno escalada:

**Propuesto**

> La atención entre una query y todas las keys se calcula como el producto escalar escalado por $1\/sqrt(d_k)$:

**Por qué:** la fórmula `softmax((Q K^T) / sqrt(d_k)) V` no normaliza por las normas de los vectores; por tanto, no es una similitud coseno.

### 1.4. GPT-4 y MoE

**Archivo:** `manuscrito/capitulos/03_capitulo_02_fundamentos_e_historia_pln.typ:371`

**Actual**

> *GPT-4* @openai2023gpt4 introduce arquitectura MoE; *Claude* @anthropic2023claude enfatiza seguridad; *Toolformer* @schick2023toolformer y *Function Calling* incorporan herramientas externas.

**Propuesto**

> *GPT-4* @openai2023gpt4 amplía las capacidades de razonamiento y generalización; *Claude* @anthropic2023claude enfatiza seguridad; *Toolformer* @schick2023toolformer y *Function Calling* incorporan herramientas externas.

**Por qué:** el informe técnico de GPT-4 citado no describe una arquitectura MoE. Si se quiere mencionar MoE, hace falta una fuente primaria que lo demuestre; no debe inferirse por el nombre del modelo.

### 1.5. Legal-BERT, Case Law Access Project y LegalBench

**Archivo:** `manuscrito/capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:29`

**Actual**

> El hito más importante de esta etapa es _Legal-BERT_ @chalkidis2020legalbert, una familia de modelos BERT preentrenados sobre el corpus _Case Law Access Project_ (Harvard, ~3.4 millones de casos federales y estatales de EE.UU.) que superó a BERT general en todas las tareas de LegalBench.

**Propuesto**

> El hito más importante de esta etapa es _LEGAL-BERT_ (Chalkidis y cols., 2020), una familia de modelos BERT preentrenada con un corpus legal en inglés que incluye legislación de la Unión Europea y del Reino Unido, decisiones judiciales europeas, casos estadounidenses y contratos. El corpus _Case Law Access Project_ (Zheng y cols., 2021) es un recurso distinto, con alrededor de 3,4 millones de decisiones, y _LegalBench_ (Guha y cols., 2023) es un benchmark posterior. Por eso no corresponde afirmar que LEGAL-BERT superó a BERT en “todas las tareas de LegalBench”.

**Por qué:** separa tres obras y elimina una evaluación anacrónica. Requiere agregar `zheng2021casehold` y `guha2023legalbench` ya existe.

**Archivo:** `manuscrito/capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:65`

**Actual**

> _Legal-BERT_ @chalkidis2020legalbert es el ejemplo paradigmático: un BERT preentrenado desde cero sobre el _Case Law Access Project_ supera a BERT base en todas las tareas de LegalBench.

**Propuesto**

> _LEGAL-BERT_ @chalkidis2020legalbert es el ejemplo paradigmático del preentrenamiento de dominio. Su corpus no es el _Case Law Access Project_ de Zheng y cols. @zheng2021casehold, y sus resultados no deben presentarse como una evaluación sobre LegalBench, que es posterior.

### 1.6. “245 artículos”

**Archivo:** `manuscrito/capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:111`

**Actual**

> Por ejemplo, citar el “artículo 1234 del Código de Minería” cuando el Código solo tiene 245 artículos.

**Propuesto**

> Por ejemplo, citar el “artículo 1234 del Código de Minería” cuando ese artículo no existe en el corpus.

**Por qué:** 245 no coincide con el corpus (398 nodos artículo, 397 con texto) ni con las otras cifras del manuscrito. Es más robusto hablar de inexistencia que fijar un número que depende de cómo se cuenten cuerpo y apéndice.

### 1.7. Fechas de modelos

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:174`

**Actual**

> (date: “2026-01”, desc: [DeepSeek-R1, ... @deepseek_r1.])

**Propuesto**

> (date: “2025-01-20”, desc: [DeepSeek-R1, ... @deepseek2025r1.])

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:178`

**Actual**

> (date: “2026-03”, desc: [Meta publica Llama 4 ... @llama4.])

**Propuesto**

> (date: “2025-04-05”, desc: [Meta publica Llama 4 ... @llama4.])

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:254`

**Actual**

> ... y DeepSeek-R1 (enero de 2026), un modelo de razonamiento ...

**Propuesto**

> ... y DeepSeek-R1 (enero de 2025), un modelo de razonamiento ...

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:258`

**Actual**

> *Qwen* (Alibaba) avanzó desde Qwen3 (diciembre de 2025) hasta Qwen 3.5 (16 de febrero de 2026), ... @qwen3_5.

**Propuesto**

> *Qwen* (Alibaba) avanzó desde Qwen3 (abril de 2025) @qwen2025qwen3 hasta Qwen 3.5 (16 de febrero de 2026), ... @qwen3_5.

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:260`

**Actual**

> *Meta* publicó Llama 4 con las variantes Scout ... @llama4.

**Propuesto**

> *Meta* publicó Llama 4 en abril de 2025 con las variantes Scout ... @llama4.

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:192`

**Actual**

> Google lanzó Gemini 3 Pro (20 de noviembre), ...

**Propuesto**

> Google lanzó Gemini 3 Pro (18 de noviembre), ...

**Por qué:** la fuente oficial de Google fecha Gemini 3 el 18 de noviembre de 2025; el timeline ya usaba esa fecha.

### 1.8. Fecha de sanción del Código

**Archivo:** `manuscrito/capitulos/anexo_01.typ:251`

**Actual**

> | Fecha de sanción | 1994-01-01 |

**Propuesto**

> | Fecha de sanción | 1886-11-25 |

**Por qué:** la Ley 1.919 fue sancionada el 25 de noviembre de 1886. El metadato `1994-01-01` del JSON fuente es incompatible con la fuente oficial y no debe trasladarse al anexo. Si se conserva el JSON sin cambios, documentar la discrepancia en una nota.

### 1.9. Referencias cruzadas duplicadas

**Archivo:** `manuscrito/main.typ` y capítulos. La causa es el sustantivo manual sumado al suplemento automático de Typst.

| Archivo:línea | Actual | Propuesto |
| --- | --- | --- |
| `04:83` | `en el capítulo @cap:agentic-rag` | `en @cap:agentic-rag` |
| `04:125` | `(capítulo @cap:evaluacion)` | `(@cap:evaluacion)` |
| `04:135` | `en el capítulo @cap:agentic-rag` | `en @cap:agentic-rag` |
| `06:107` | `(véase el capítulo @cap:agentic-rag para ...)` | `(véase @cap:agentic-rag para ...)` |
| `06:176` | `(véase el capítulo @cap:fundamentos-pln para ...)` | `(véase @cap:fundamentos-pln para ...)` |
| `06:344` | `en la sección @sec:agente-especialista-legal` | `en @sec:agente-especialista-legal` |
| `06:587` | `(véase el capítulo @cap:agentic-rag, sección @sec:llm-as-a-judge ...)` | `(véase @cap:agentic-rag y @sec:llm-as-a-judge ...)` |
| `07:316` | `en el capítulo @cap:metodologia` | `en @cap:metodologia` |
| `09:85` | `(capítulo @cap:agentic-rag)` | `(@cap:agentic-rag)` |

Si se necesita minúscula (“en la sección 4”), usar `#ref(<cap:agentic-rag>, supplement: [sección])` en lugar de escribir “sección” antes de la referencia.

### 1.10. Nota sobre sistemas expertos

**Archivo:** `manuscrito/capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:23`

**Actual**

> ... razonamiento basado en casos (_case-based reasoning_) para emular el razonamiento de un abogado#footnote[https://en.wikipedia.org/wiki/Legal_expert_system].

**Propuesto**

> ... razonamiento basado en casos (_case-based reasoning_) para emular el razonamiento de un abogado @bench-capon2012history.

**Por qué:** reemplaza una nota a Wikipedia por una revisión académica verificada. Agregar `bench-capon2012history` al `.bib`.

### 1.11. Dedicatoria

**Archivo:** `manuscrito/capitulos/01_texto_preliminar.typ:13`

**Actual**

> A mi familia ...

**Propuesto**

> Completar con el texto definitivo o eliminar la sección si no se desea incluir dedicatoria.

### 1.12. Declaración de uso de IA

**Archivo:** `manuscrito/capitulos/01_texto_preliminar.typ:18`

**Actual**

> Se han empleado productos basados en inteligencia artificial para asistir en la elaboración de este trabajo.

**Propuesto (base; ajustar a lo efectivamente realizado)**

> Se utilizaron herramientas de inteligencia artificial generativa en las siguientes etapas: (a) extracción del texto del PDF del Boletín Oficial mediante el modelo de visión o4-mini; (b) generación de preguntas y respuestas de referencia con GPT-4.1, revisadas por un profesional del derecho; (c) generación de respuestas evaluadas con los modelos GPT-5 nano, mini y estándar; (d) evaluación comparativa con los modelos jueces DeepSeek, Grok y Kimi K2; y (e) asistencia en redacción, edición y programación. El autor verificó las fuentes, revisó el contenido y asume la responsabilidad por el texto y por las decisiones metodológicas.

**Por qué:** la declaración actual no permite saber en qué etapas se usó IA ni cómo se verificó. Coordinar con IX.1.8; si alguna etapa no corresponde, eliminarla.

## 2. Tabla 3 — correcciones de citas y afirmaciones

### 2.1. Bommasani → Bozdag

**Archivo:** `manuscrito/capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:69`

**Actual**

> En el dominio legal, @bommasani2022gender aplican técnicas de mitigation de sesgos sobre _Legal-BERT_ usando variantes de adapters, mostrando que se puede especializar preservando propiedades de fairness.

**Propuesto**

> En el dominio legal, Bozdag y cols. (2024) proponen un método de mitigación de sesgos de género basado en fine-tuning sobre el corpus del Tribunal Europeo de Derechos Humanos y evalúan su efecto en LexGLUE, sin atribuir el método a variantes de adapters.

**Archivo:** `manuscrito/capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:95`

**Actual**

> El estudio más sistemático sobre este problema es el de #cite(<bommasani2022gender>, form: “prose”), quienes demostraron que _Legal-BERT_ y otros modelos preentrenados sobre jurisprudencia estadounidense reproducen y amplifican sesgos de género presentes en los datos históricos. En particular, los embeddings asocian sistemáticamente profesiones y roles según estereotipos de género ... y estas asociaciones correlacionan con decisiones judiciales reales que pueden estar sesgadas.

**Propuesto**

> Uno de los estudios sistemáticos sobre sesgo de género en modelos BERT legales es el de Bozdag y cols. (2024). Los autores proponen una métrica basada en plantillas y un corpus de evaluación construido con términos de delitos, y un método de debiasing mediante fine-tuning sobre el corpus del TEDH; evalúan el efecto en LexGLUE y proponen una penalización por sesgo. El trabajo no demuestra por sí solo que esos sesgos se traduzcan en decisiones judiciales reales; esa relación requiere evidencia adicional.

**Por qué:** el artículo de Bozdag no usa adapters y no debe cargarse con afirmaciones sobre decisiones judiciales que no se verificaron en su texto. Si se conserva la frase sobre roles y profesiones, debe citarse la sección exacta del artículo o una fuente adicional.

**Cambio de clave:** `bommasani2022gender` → `bozdag2024gender` en las dos citas. La entrada nueva está en `propuestas_bibtex.bib`.

### 2.2. Dahl → Magesh

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:29`

**Actual**

> Un estudio de la Universidad de Stanford publicado en el Journal of Empirical Legal Studies en 2025 encontró que Westlaw AI presentaba alucinaciones en el 33\% de las consultas, mientras que Lexis+ AI lo hacía en el 17\%, en comparación con el 43\% de GPT-4 sin RAG @dahan2024stanford.

**Propuesto**

> Un estudio publicado en el Journal of Empirical Legal Studies (Magesh y cols., 2025) encontró que Westlaw AI-Assisted Research presentaba alucinaciones en el 33\% de las consultas, Lexis+ AI en el 17\% y GPT-4 sin RAG en el 43\%.

**Por qué:** el estudio correcto es Magesh et al. (2025), DOI `10.1111/jels.12413`. Los porcentajes 33/17/43 están verificados en el apéndice B1 del texto completo. `dahan2024stanford` es “Large Legal Fictions” y no debe usarse para esta frase. Si no se cita en otro lugar, eliminar la entrada.

**Cambio de clave:** `dahan2024stanford` → `magesh2025hallucinationfree` en esa frase.

### 2.3. Wei 2022 y Zhao 2026

**Archivo:** `manuscrito/capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:81`

**Actual**

> Introducido por #cite(<wei2022cot>, form: “prose”), el _Chain-of-Thought_ ...

**Propuesto**

> Introducido por Wei, Wang, y cols. (#cite(<wei2022cot>, form: “year”)), el _Chain-of-Thought_ ...

**Archivo:** `manuscrito/capitulos/03_capitulo_02_fundamentos_e_historia_pln.typ:370`

**Actual**

> Wei y colaboradores documentan las *capacidades emergentes* @wei2022emergent; ...

**Propuesto**

> Wei, Tay, y cols. (#cite(<wei2022emergent>, form: “year”)) documentan las *capacidades emergentes*; ...

**Archivo:** `manuscrito/capitulos/03_capitulo_02_fundamentos_e_historia_pln.typ:402`

**Actual**

> *Emergent Abilities of Large Language Models* @wei2022emergent: Wei y colaboradores documentaron ...

**Propuesto**

> *Emergent Abilities of Large Language Models* @wei2022emergent: Wei, Tay, y cols. (#cite(<wei2022emergent>, form: “year”)) documentaron ...

**Archivo:** `manuscrito/capitulos/03_capitulo_02_fundamentos_e_historia_pln.typ:405`

**Actual**

> ... las capacidades emergentes descritas por @wei2022emergent ...

**Propuesto**

> ... las capacidades emergentes descritas por Wei, Tay, y cols. (#cite(<wei2022emergent>, form: “year”)) ...

**Archivo:** `manuscrito/capitulos/03_capitulo_02_fundamentos_e_historia_pln.typ:355`

**Actual**

> ... consultar #cite(<zhao2026surveySpringer>, form: “prose”).

**Propuesto**

> ... consultar W. X. Zhao y cols. (#cite(<zhao2026surveySpringer>, form: “year”)).

**Archivo:** `manuscrito/capitulos/05_capitulo_04_marco_teorico_agentic_rag.typ:306`

**Actual**

> ... independientemente de la precisión factual @zhao2026reportlogic.

**Propuesto**

> ... independientemente de la precisión factual (J. Zhao y cols., #cite(<zhao2026reportlogic>, form: “year”)).

**Por qué:** APA 8.18 (Wei: coautores distintos) pide nombres adicionales, no letras a/b. APA 8.20 (Zhao: iniciales distintas) pide iniciales. La prueba `pruebas/citas_ambiguas.typ` confirma que `form: “year”` evita repetir el año.

### 2.4. DeepSeek

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:174`

**Actual**

> ... DeepSeek-R1 ... @deepseek_r1.

**Propuesto**

> ... DeepSeek-R1 ... @deepseek2025r1.

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:254`

**Actual**

> ... DeepSeek-R1 (enero de 2026), ...

**Propuesto**

> ... DeepSeek-R1 (enero de 2025), ...

**Bibliografía:** eliminar `deepseek_r1`; conservar y completar `deepseek2025r1` con la fecha oficial 2025-01-20. La página oficial es `https://api-docs.deepseek.com/news/news250120/`.

### 2.5. Llama 4 y Qwen3

**Llama 4:** `08:178` → fecha `2025-04-05`; `08:260` → “en abril de 2025”; `.bib` `llama4` → año 2025, mes abril, día 5. Fuente: `https://ai.meta.com/blog/llama-4-multimodal-intelligence/`.

**Qwen3:** `08:258` → “Qwen3 (abril de 2025) @qwen2025qwen3”; agregar `qwen2025qwen3`. No cambiar `qwen3_5`, que es Qwen 3.5 (2026). Fuente: `https://qwenlm.github.io/blog/qwen3/`.

**Gemini 3 Pro:** `08:192` → “18 de noviembre”. Fuente: `https://blog.google/products-and-platforms/products/gemini/gemini-3/`.

### 2.6. LEXTREME

**Cambio global:** `niklaus2024lextreme` → `niklaus2023lextreme` en las cinco citas:

- `02:37`
- `04:11`
- `04:15`
- `04:99`
- `08:93`

La entrada nueva tiene año 2023 y seis autores (se agrega Chalkidis). No cambiar el texto sustantivo.

### 2.7. Tribunal Fiscal

**Archivo:** `manuscrito/capitulos/08_capitulo_07_trabajos_relacionados.typ:41`

**Actual**

> En Argentina también se destaca el sistema de *Búsqueda de Jurisprudencia Asistida por IA* del Tribunal Fiscal de la Nación @tribunalfiscal2025, que incorpora inteligencia artificial a la búsqueda de documentos legales, aunque limitado a documentos emitidos por dicho tribunal.

**Propuesto (opción oficial)**

> En Argentina también se destaca el sistema de *Búsqueda de Jurisprudencia Asistida por IA* del Tribunal Fiscal de la Nación @tribunalfiscal2024buscador, que incorpora inteligencia artificial a la búsqueda de documentos legales, aunque limitado a documentos emitidos por dicho tribunal.

**Alternativa:** si se prefiere citar la nota periodística, usar `@tallarico_tfn` y aclarar “según una nota de AUNO Abogados”. No mezclar autor institucional con URL de un estudio jurídico.

### 2.8. Lewis et al. (2020)

**Archivo:** `manuscrito/capitulos/02_capitulo_01_introduccion.typ:11`

**Actual**

> La Generación Aumentada por Recuperación (RAG) ha emergido como una solución prometedora ... y enviar los resultados de la búsqueda al usuario @gao2023retrieval.

**Propuesto**

> La Generación Aumentada por Recuperación (RAG), introducida por Lewis y cols. @lewis2020rag, ha emergido como una solución prometedora ... y enviar los resultados de la búsqueda al usuario @gao2023retrieval.

**Por qué:** Lewis et al. (2020) es el trabajo fundacional; Gao et al. (2023) es una revisión posterior. Agregar `lewis2020rag` al `.bib`.

### 2.9. Código de Minería

**Archivo:** `manuscrito/capitulos/06_capitulo_05_metodologia.typ:47`

**Actual**

> Se seleccionó el Código de Minería Argentino#footnote[...] como corpus de prueba de concepto.

**Propuesto**

> Se seleccionó el Código de Minería Argentino @codigo_mineria_1919#footnote[...] como corpus de prueba de concepto.

**Por qué:** falta la fuente legal. La entrada `codigo_mineria_1919` apunta a la ficha oficial de la Ley 1.919 y consigna la sanción del 25-11-1886 y el texto ordenado por Decreto 456/1997.

### 2.10. Preprints → versiones publicadas

No hay cambios de texto; solo de entradas:

| Clave actual | Clave/entrada propuesta |
| --- | --- |
| `devlin2018bert` | `devlin2019bert`, NAACL 2019 |
| `hu2021lora` | `hu2022lora`, ICLR 2022 |
| `dettmers2023qlora` | misma clave, NeurIPS 2023 con DOI |
| `asai2023selfrag` | `asai2024selfrag`, ICLR 2024 |
| `chalkidis2020legalbert` | misma clave, Findings EMNLP 2020 |

### 2.11. Forma “y col.” / “y cols.”

**Archivo:** `manuscrito/main.typ:27-39`

**Actual**

```typst
#show cite: it => {
  show regex("et\s+al\.?"): [y col.]
  show regex("\s*&\s*others"): [ y cols.]
  it
}
#show bibliography: it => {
  show regex("et\s+al\.?"): [y col.]
  show regex(",\s*&\s*others\.?"): [, y col.]
  it
}
```

**Propuesto (opción “y cols.” uniforme)**

```typst
#show cite: it => {
  show regex("et\s+al\.?"): [y cols.]
  show regex("\s*&\s*others"): [ y cols.]
  it
}
#show bibliography: it => {
  show regex("et\s+al\.?"): [y cols.]
  show regex(",\s*&\s*others\.?"): [, y cols.]
  it
}
```

**Alternativa estricta APA:** eliminar ambos `show` y dejar que el estilo APA produzca “et al.”. En ese caso, reemplazar también los “y colaboradores” manuales si se busca uniformidad total.

## 3. Cambios globales de claves

| Actual | Propuesta | Nº de citas | Ubicaciones |
| --- | --- | ---: | --- |
| `bommasani2022gender` | `bozdag2024gender` | 2 | `04:69,95` |
| `dahan2024stanford` | `magesh2025hallucinationfree` | 1 | `08:29` |
| `deepseek_r1` | `deepseek2025r1` | 1 | `08:174` |
| `niklaus2024lextreme` | `niklaus2023lextreme` | 5 | `02:37`; `04:11,15,99`; `08:93` |
| `tribunalfiscal2025` | `tribunalfiscal2024buscador` | 1 | `08:41` |
| `wan2025legalagents` | `yang2025legalagents` | 1 | `08:67` |
| `devlin2018bert` | `devlin2019bert` | 3 | `03:33,352`; `04:29` |
| `hu2021lora` | `hu2022lora` | 1 | `04:69` |
| `asai2023selfrag` | `asai2024selfrag` | 1 | `05:348` |

No renombrar `llama4`, `qwen3_5`, `pydanticAI`, `jeong2024graph`, `zhao2026surveySpringer` ni `zhao2026reportlogic`; sus correcciones son de contenido, no de clave.

## 4. Orden de edición recomendado

1. **Congelar una copia** de `referencias.bib` y del manuscrito.
2. Reemplazar las entradas críticas en `referencias.bib` con `propuestas_bibtex.bib`:
   - Bozdag, Magesh, Niklaus, DeepSeek, Llama, Qwen, Lewis, Código, Bench-Capon, Zheng.
3. Corregir los metadatos adicionales (Raeini, Yang, Springer, Zhao survey, Pydantic, Jeong).
4. Aplicar los renombres de claves y actualizar las citas con `mapa_renombres.csv`.
5. Editar el texto de la Tabla 2 y de la Tabla 3 con las secciones 1 y 2 de este documento.
6. Corregir las referencias cruzadas y la forma “y cols.”.
7. Compilar y revisar el PDF; buscar las cadenas de la §5.
8. Actualizar la declaración de IA y la dedicatoria.

## 5. Verificación posterior

Buscar en el PDF final:

- `Bommasani y cols., 2023` → no debe existir para el DOI de Bozdag.
- `Dahl y cols., 2024` en la frase de Westlaw/Lexis → no debe existir.
- `DeepSeek, 2026b` o `DeepSeek-R1 (enero de 2026)` → no debe existir.
- `Meta. (2026` o `Llama 4` fechado en 2026 → no debe existir.
- `Qwen3 (diciembre de 2025)` → no debe existir.
- `Niklaus y cols., 2024` en LEXTREME → no debe existir.
- `capítulo Sección` y `sección Sección` → no deben existir.
- `y col.` singular → no debe quedar si se eligió “y cols.”.
- `1994-01-01` en el anexo → no debe existir.
- `A mi familia ...` → no debe quedar.
- `Zhao y col., 2026` para ambas obras → no debe quedar; deben verse las iniciales o nombres adicionales.

## 6. Criterio de aceptación

- Las 238 entradas actuales tienen estado en `estado_por_entrada.csv`.
- Las 28 entradas propuestas se revisaron y se incorporaron solo las aprobadas.
- Las 9 claves renombradas se actualizaron en todas sus citas.
- Las citas del PDF coinciden con el `.bib` en autor, año y clave.
- No quedan referencias cruzadas duplicadas ni “y col.”/“y cols.” mezclados.
- Las afirmaciones sobre Bozdag, Magesh, Legal-BERT, DeepSeek, Llama y Qwen coinciden con las fuentes primarias.

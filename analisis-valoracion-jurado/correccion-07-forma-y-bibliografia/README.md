# Corrección IX.1.7 — Tablas 2 y 3 y auditoría bibliográfica

Esta carpeta reúne los artefactos para resolver el punto **IX.1.7** del plan:

> Corregir los errores de las Tablas 2 y 3, con una auditoría completa de las referencias.

**No se modificó ningún archivo existente** del manuscrito, del `.bib`, de los datos, de los notebooks ni de los logs. Las fuentes se leyeron en modo de solo lectura. Todo lo nuevo está en esta carpeta.

## 1. Qué revisar primero

1. **`resumen_ejecutivo.md`** — cifras, hallazgos y decisiones pendientes en dos páginas.
2. **`propuesta_edicion_manuscrito.md`** — texto actual y propuesto, archivo por archivo, con la justificación.
3. **`cotejo_tablas_2_3.csv`** — los 39 ítems de las Tablas 2 y 3 y de la auditoría adicional, con estado, acción, evidencia y prioridad.
4. **`auditoria_bibliografia.md`** — auditoría completa: 238 entradas, DOI, arXiv, URL, preprints, ediciones y ambigüedades.
5. **`propuestas_bibtex.bib`** — 28 entradas propuestas, con comentarios de reemplazo, renombre o adición.
6. **`mapa_renombres.csv`** — las 9 claves que cambian y todas las ubicaciones de sus citas.
7. **`estado_por_entrada.csv`** — estado de las 238 entradas actuales.

## 2. Resultado en cifras

| Indicador | Resultado |
| --- | ---: |
| Entradas en `referencias.bib` | 238 |
| Entradas citadas | 238 |
| Entradas no citadas | 0 |
| Claves citadas sin entrada | 0 |
| DOI consultados | 79 |
| DOI con respuesta 200 | 78 |
| DOI no indexado en Crossref (Jeong) | 1, verificado en KCI/arXiv |
| DOI con metadatos coincidentes | 61 |
| DOI con alguna discrepancia | 18, clasificadas en el informe |
| arXiv consultados | 87 |
| arXiv con coincidencia plena | 79 |
| URL consultadas | 172 |
| URL con 200/206/202 | 156 |
| URL con 401/403/405/429 | 15, bloqueo de automatización |
| URL sin resolución DNS | 1, Lexium |
| Entradas sin DOI ni URL | 4, documentadas |

La primera extracción de citas marcó 12 entradas como no citadas. Era un **falso negativo**: el regex de `@clave` incluía los dos puntos finales de citas como `@asai2023selfrag:`. La extracción corregida encuentra las 238 entradas citadas. Este incidente quedó documentado para que no se repita.

## 3. Hallazgos principales

### 3.1. Correcciones críticas de la Tabla 3

- **Bommasani → Bozdag:** el DOI `10.1145/3628602` pertenece a Bozdag, Sevim y Koç (2024), ACM TKDD. El método es **fine-tuning**, no adapters.
- **Dahl → Magesh:** el estudio de Westlaw/Lexis es Magesh et al. (2025), JELS 22(2), 216-242. Los porcentajes 33/17/43 están verificados en el apéndice B1.
- **DeepSeek-R1:** hay dos entradas y una fechada en 2026; el lanzamiento fue el **20 de enero de 2025**.
- **Llama 4:** Meta lo publicó el **5 de abril de 2025**, no en marzo de 2026.
- **Qwen3:** se publicó el **29 de abril de 2025**; `qwen3_5` es Qwen 3.5 (2026).
- **LEXTREME:** es de **2023**, no 2024, y falta Chalkidis como sexto autor.
- **Tribunal Fiscal:** el autor institucional no corresponde a la URL de la nota de AUNO; el sitio oficial es `https://jurisprudenciatfn.mecon.gob.ar/`.
- **Lewis et al. (2020)** y el **Código de Minería** no estaban citados; se agregan.

### 3.2. Corrección al pedido de letras a/b

El jurado pide “letras (2022a, 2022b)” para Wei y Zhao. La regla APA 7 es distinta:

- **Wei 2022:** mismo primer autor y año, pero **coautores distintos** → APA 8.18 pide agregar nombres, no letras: `Wei, Wang, y cols.` / `Wei, Tay, y cols.`
- **Zhao 2026:** mismo apellido y año, pero **iniciales distintas** → APA 8.20 pide iniciales: `W. X. Zhao y cols.` / `J. Zhao y cols.`

Typst ya asigna a/b a los autores institucionales del mismo año (OpenAI, Anthropic, Google, etc.) y no asigna letras a Wei/Zhao, lo cual es coherente. La intervención debe ser manual solo en esos dos casos. La prueba está en `pruebas/citas_ambiguas.typ` y `salidas/prueba_citas.pdf`.

### 3.3. Hallazgos adicionales

- `raeini2025evolution`: autor correcto **Ghaseminejad Raeini, Mohammad**.
- `wan2025legalagents`: primer autor **Se Yang**, no Hao Wan; el texto debe decir “Yang et al.”.
- `springer2025trustworthy`: año **2025**, no 2026.
- `zhao2026surveySpringer`: 23 autores y **Frontiers of Computer Science 20(12)**, no la revista consignada.
- `pydanticAI`: versión **1.1.0**, no 2.0.0.
- `jeong2024graph`: DOI no indexado en Crossref, pero existe en KCI y arXiv.
- `hebb`, `minsky`, `bonferroni`, `jordan` y `krippendorff`: DOI de **otra edición**; conviene retirarlo o cambiar la edición citada.

## 4. Estructura de la carpeta

### 4.1. Informes y propuestas

| Archivo | Contenido |
| --- | --- |
| `resumen_ejecutivo.md` | Síntesis y decisiones pendientes |
| `auditoria_bibliografia.md` | Auditoría completa y clasificación de discrepancias |
| `propuesta_edicion_manuscrito.md` | Cambios concretos en `.typ`, con texto actual/propuesto |
| `propuestas_bibtex.bib` | 28 entradas BibTeX propuestas |
| `cotejo_tablas_2_3.csv` | Cotejo de 39 ítems de las Tablas 2/3 y auditoría adicional |
| `mapa_renombres.csv` | 9 claves que cambian y sus citas |
| `cola_lectura_afirmaciones.csv` | Afirmaciones que requieren lectura completa o revisión jurídica |

### 4.2. Inventarios y verificaciones

| Archivo | Contenido |
| --- | --- |
| `inventario_bibliografia.csv` | 238 entradas con tipo, línea, autores, DOI, URL y uso |
| `citas_por_archivo.csv` | 503 ocurrencias de cita con archivo, línea y contexto |
| `citas_sin_entrada.csv` | Claves citadas sin entrada (0 filas) |
| `autor_anio_ambiguos.csv` | 16 grupos de autor–año y regla APA sugerida |
| `doi_duplicados.csv` | DOI repetidos (0 grupos) |
| `titulos_similares.csv` | 7 pares de títulos similares, revisados |
| `preprints.csv` | 66 entradas con arXiv/preprint |
| `fechas_de_consulta.csv` | 43 entradas con fecha de consulta o “Accedido” |
| `sin_identificador.csv` | 4 entradas sin DOI ni URL |
| `verificacion_doi.csv` | 79 DOI con título, autores, año y estado |
| `verificacion_arxiv.csv` | 87 arXiv con título, autores y año |
| `verificacion_url.csv` | 172 URL con estado, URL final y título |
| `estado_por_entrada.csv` | Estado consolidado de las 238 entradas actuales |
| `propuestas_nuevas.csv` | 7 entradas nuevas propuestas |
| `decisiones_manuales.csv` | 45 decisiones por entrada |
| `resumen_auditoria_local.json` | Resumen del parseo local |
| `resumen_verificacion_online.json` | Resumen de DOI/arXiv/URL |
| `resumen_consolidado.json` | Resumen del cruce final |

### 4.3. Scripts reproducibles

| Archivo | Función |
| --- | --- |
| `auditar_bibliografia.py` | Parsea el `.bib` y extrae citas |
| `verificar_fuentes.py` | Verifica DOI/DataCite/arXiv/URL con caché |
| `verificar_arxiv_lotes.py` | Verifica arXiv por lotes para evitar 429 |
| `consolidar_auditoria.py` | Cruza inventario, verificaciones y decisiones |
| `generar_manifiesto.py` | Genera `manifiesto_sha256.csv` |
| `verificar_artefactos.py` | Comprueba que los artefactos no cambiaron |
| `manifiesto_sha256.csv` | Hashes de fuentes y artefactos |

### 4.4. Salidas

| Archivo | Contenido |
| --- | --- |
| `salidas/manuscrito_actual.pdf` | Compilación del manuscrito al 2026-11-12 |
| `salidas/manuscrito_actual.txt` | Texto extraído del PDF |
| `salidas/referencias_renderizadas.txt` | Lista de referencias renderizada |
| `salidas/prueba_citas.pdf` | Prueba de desambiguación Wei/Zhao |
| `salidas/bibliografia_propuesta.pdf` | Compilación de las 28 entradas propuestas |
| `pruebas/citas_ambiguas.typ` | Documento Typst de prueba de Wei/Zhao |
| `pruebas/bibliografia_propuesta.typ` | Documento Typst que compila el `.bib` propuesto |
| `salidas/*.log` | Logs de compilación y verificación |

### 4.5. Caché

`cache/` contiene las respuestas crudas de Crossref, DataCite, arXiv y URL. Permite reproducir la auditoría sin volver a consultar los servicios. No contiene credenciales.

## 5. Cómo reproducir

Desde la raíz del repositorio:

```bash
python3 analisis-valoracion-jurado/correccion-07-forma-y-bibliografia/auditar_bibliografia.py --repo .
python3 analisis-valoracion-jurado/correccion-07-forma-y-bibliografia/verificar_fuentes.py --solo-doi
python3 analisis-valoracion-jurado/correccion-07-forma-y-bibliografia/verificar_arxiv_lotes.py
python3 analisis-valoracion-jurado/correccion-07-forma-y-bibliografia/verificar_fuentes.py --solo-url
python3 analisis-valoracion-jurado/correccion-07-forma-y-bibliografia/consolidar_auditoria.py
python3 analisis-valoracion-jurado/correccion-07-forma-y-bibliografia/generar_manifiesto.py
```

**Advertencia:** `verificar_fuentes.py --solo-doi` también reescribe `verificacion_arxiv.csv` si se ejecuta después de `verificar_arxiv_lotes.py`; por eso el orden recomendado es DOI, luego arXiv por lotes, luego URL. Si se vuelve a ejecutar, repetir el lote de arXiv al final.

Para compilar la prueba de citas:

```bash
cd analisis-valoracion-jurado/correccion-07-forma-y-bibliografia/pruebas
typst compile citas_ambiguas.typ ../salidas/prueba_citas.pdf --root ../../..
```

## 6. Decisiones pendientes

1. **Bozdag:** confirmar la reescritura; el artículo no demuestra por sí solo una relación con decisiones judiciales reales.
2. **Magesh:** confirmar que se elimina `dahan2024stanford` o se conserva solo para su propio contenido.
3. **Wei/Zhao:** elegir APA (nombres/iniciales) o la solución literal del jurado (a/b). Se recomienda APA.
4. **Tribunal Fiscal:** elegir sitio oficial o nota de AUNO.
5. **DOI de edición:** decidir si se retira el DOI o se cambia la edición en Hebb, Minsky, Bonferroni, Jordan y Krippendorff.
6. **Forma de autoría:** “y cols.” uniforme o “et al.” estricto APA.

## 7. Límites

- La verificación de DOI/URL es de **metadatos y localizadores**, no de lectura completa de las 238 obras.
- Los 403 de OpenAI, ACM, ScienceDirect, ScholarWorks y Oxford son bloqueos de automatización; no prueban que el recurso no exista.
- El sitio oficial del Tribunal Fiscal no respondió por timeout desde este entorno; la búsqueda web lo confirma, pero conviene verificarlo desde otra red antes de la entrega.
- No se generaron citas de memoria: las entradas propuestas se obtuvieron de Crossref, DataCite, arXiv, OpenReview, ACL Anthology o sitios oficiales.
- La decisión jurídica sobre las respuestas de referencia corresponde al profesional del derecho, no a esta auditoría.

## 8. Criterio de aceptación

- Las 238 entradas tienen estado en `estado_por_entrada.csv`.
- Las 238 están citadas y no hay claves huérfanas.
- Las 28 entradas de `propuestas_bibtex.bib` se revisaron y se incorporaron solo las aprobadas.
- Las 9 claves renombradas se actualizaron en todas sus citas.
- El PDF final no contiene las cadenas listadas en `propuesta_edicion_manuscrito.md` §5.
- Las referencias cruzadas duplicadas desaparecen.
- La forma “y col.”/“y cols.” queda unificada.

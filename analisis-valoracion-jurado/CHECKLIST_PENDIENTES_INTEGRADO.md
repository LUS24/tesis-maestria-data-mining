# Checklist integrado de pendientes del manuscrito

**Fecha de integración:** 2026-11-12.
**Informes integrados:**

| Abrev. | Archivo | Modelo |
|:---:|---|---|
| **[G]** | `VERIFICACION_MANUSCRITO_vs_TRIBUNAL_ollama-cloud-glm-5-3-flash.md` | GLM 5.3-flash |
| **[M]** | `VERIFICACION_MANUSCRITO_vs_TRIBUNAL_ollama-cloud-mimo-v2-6-flash.md` | MiMo v2.6-flash |
| **[m]** | `VERIFICACION_MANUSCRITO_vs_TRIBUNAL_ollama-cloud-minimax-3-1-flash.md` | MiniMax 3.1-flash |

**Documento normativo:** `Valoracion_TF_Spairani_gp_actualizada.md` (V.1–V.11, Tablas 2–4, IX.1.1–IX.1.9, IX.2.1–IX.2.5).

**Método de integración:** se unificaron los tres reportes por *pendiente concreto* (no por sección del tribunal), se deduplicaron las coincidencias y se **re-verificó cada ítem que los informes reportaban de forma divergente** contra `manuscrito/capitulos/*.typ` y contra el PDF compilado en esta sesión (`typst compile` → 167 páginas, sin errores). La columna `Fuente` indica cuántos informes lo señalan; `✓` significa verificado directamente en el repositorio durante la integración.

**Total: 27 pendientes** (9 bloqueantes · 10 altos · 8 medios/menores).

**Estado: los 27 pendientes fueron resueltos** el 2026-11-12/13. Cada ítem se implementó en un commit propio para conservar la trazabilidad; el hash correspondiente figura en la columna `Commit` de §0.1. El manuscrito compila sin errores (195 páginas) y las verificaciones de §6 dan el resultado esperado.

## 0.1. Registro de ejecución

| Ítem | Commit | Qué se hizo |
|---|---|---|
| A-01 | `e6db99b` | Base 684 → 711 con el diagnóstico del join |
| A-02 | `9a82ac7` | Tabla de efectos simples del modelo ordinal con IC y Holm |
| A-03 | `0d8aadd` | Tabla por celda reconstruida sobre 79 unidades |
| A-04 | `640b746` | Modelo ordinal como análisis principal + Friedman/Wilcoxon/bootstrap |
| A-05 | `a5faf94` | KW/Dunn/SRH al anexo D; escenarios definidos en metodología |
| A-06 | `47809f6` | Retiro del determinismo por temperatura 0 y subsección de parámetros de API |
| A-07 | `0f5e6c6` | Retiro de atribuciones causales sobre la celda nano |
| A-08 | `a4b4987` | Descripción real de `part_j/` en el anexo |
| A-09 | `5edef8e` | Referencias cruzadas con `supplement` (0 duplicadas en el PDF) |
| B-01 | `2f25558` | Fortalezas y limitaciones con cifras canónicas |
| B-02 | `95d251c` | Limitaciones faltantes (ejecución única, escenarios, confundidos, costos) |
| B-03 | `6e211a1` | Índice de eficiencia fuera del cuerpo; costo por respuesta correcta y Pareto |
| B-04 | `ab78699` | Objetivo general, específico 2 y contribuciones acotados |
| B-05 | `0aaa0f1` | Árbol real del repositorio en el anexo A |
| B-06 | `93827c7` | Anexo E de prompts y parámetros con hashes |
| B-07 | `7ef05f2` | N-gramas, atención escalada, MoE de GPT-4 y dedicatoria |
| B-08 | `5dd50fb` | Extracción del corpus sin afirmación de validación estadística |
| B-09 | `e21254b` | Figuras canónicas del reanálisis y diagnóstico de la celda nano |
| B-10 | `b005491` | Coherencia de la tabla de hiperparámetros con parámetros de API |
| C-01 | `a4f50b0` | Retiro de HNSW (NDCG se conserva: aparece en el cap. 4) |
| C-02 | `9195bba` | Evaluación determinista de citas como trabajo futuro |
| C-03 | `15cf0ef` | Réplicas y ablación como límite y como trabajo futuro |
| C-04 | `3332d1a` | Extensión de los capítulos 2 y 7 como decisión de alcance |
| C-05 | `c496036` | Ausencia de comparación con BM25 como limitación |
| C-06 | `4f6e498` | Embedding en español como decisión a priori, sin ventaja afirmada |
| C-07 | `fdfeccd` | Mes de ICLR en LoRA y Self-RAG (sin coma colgante) |
| C-08 | `4e6b562` | Imputación: 50 evaluaciones en 11 combinaciones, por juez |
| — | `a2da467` | Pasada final: transferencia al repositorio publicado |
| — | `3b96a76` | Pasada final: remisiones y «unidad de evaluación» |
| — | `20469cc` | Pasada final: agrupación de tablas anchas (199 → 195 páginas) |

---

## 0. Discrepancias entre los tres informes y resolución

Antes de usar el checklist conviene saber dónde los informes se contradicen, porque un ítem que un informe da por cerrado otro lo da por bloqueante.

| Punto | [G] | [M] | [m] | Resolución verificada |
|---|:---:|:---:|:---:|---|
| Frases de determinismo/temperatura | 4 | 6 | 5–6 | **6** — `06:191, 511, 521, 614, 660` + `07:16` ✓ (las 6 confirmadas con `grep`) |
| Referencias cruzadas "capítulo Sección N" | 0 ❌ | 14 | 14 | **14 ocurrencias en 12 páginas**, verificado en el PDF: pp. 43, 49, 50, 53×2, 74, 76, 78, 82, 89×2, 96, 111, 133 ✓ — [G] buscó en el `.typ` en lugar del PDF |
| "modelos mixtos" en `anexo_01.typ:86` | pendiente | pendiente | "ya no es engañosa" | **Pendiente** ✓ — la línea sigue literal |
| Árbol del repositorio en el anexo | obsoleto | no lo evalúa | no lo evalúa | **Obsoleto** ✓ — `anexo_01.typ:10, 20, 26, 32` mencionan `archivo/`, `examples/notebooks/`, `04_vector_database_creation/` (pgvector) |
| Base 684 observaciones | pendiente | bloqueante | bloqueante | **Pendiente y bloqueante** ✓ — `07:73` (684) vs `07:18` (711) |
| Índice de eficiencia piso 0,01 | ⚠️ salvedad | debe salir del cuerpo | debe salir del cuerpo | **Sigue en el cuerpo** ✓ — `07:289-306` + figura `eficiencia_costo.pdf` |

---

## 1. Bloqueantes (⛔) — contradicciones internas que el tribunal puede señalar en la defensa

- [x] **A-01 · Base de cálculo 684 → 711 y explicación de los 27 faltantes** ⛔
  - Ubicación: `07_capitulo_06_evaluacion.typ:73` (contradice `:18`, que ya declara 711).
  - Fuente: 3/3 · ✓
  - Acción: reemplazar "atribuibles a fallos puntuales en la generación" y la "reducción a 684 observaciones" por el diagnóstico real: defecto de *join* (subpregunta vacía vs. `0`) en los casos 23, 24 y 25; clave normalizada ⇒ 711 observaciones y 2.133 evaluaciones.
  - Texto listo: `correccion-02-diagnostico-gpt-5-nano/PROPUESTAS_MANUSCRITO.md` §1.
  - Efecto derivado: recalcular toda cifra que dependa de 684 (ver A-02, A-03, B-01).

- [x] **A-02 · La tabla de efectos simples es Mann-Whitney aunque el texto diga que salió del modelo ordinal** ⛔
  - Ubicación: `07:135` ("Los efectos simples se estimaron con ese modelo y se corrigen con Holm") vs. tabla `07:140-158` (U de Mann-Whitney, medias de la base vieja).
  - Fuente: 3/3 · ✓
  - Acción: sustituir por la tabla canónica del modelo ordinal (Δ media, IC 95 %, Δ P(≥ 0,75), p Holm) **o** eliminar la afirmación del texto y etiquetar la tabla como análisis exploratorio histórico.
  - Texto/CSV listo: `correccion-01-analisis-estadistico/PROPUESTA_TEXTO_MANUSCRITO.md` §3.5 + `salidas/31_efectos_simples_orientados.csv`.

- [x] **A-03 · Tablas de medianas calculadas sobre 76 observaciones por celda** ⛔
  - Ubicación: `07:169-190` (5 de las 9 medianas cambian con 79).
  - Fuente: [M][m] · ✓
  - Acción: reconstruir la tabla por celda con `n`, nº de no sustantivas, media, mediana, media modelada y P(≥ 0,75).
  - Insumos: `correccion-01/salidas/30_tabla_celdas_principal.csv`, `INFORME_ANALISIS_ESTADISTICO.md` §6.

- [x] **A-04 · Estatus contradictorio del modelo ordinal ("principal" vs. "robustez") y "pruebas pareadas" que no existen** ⛔
  - Ubicaciones: `06:708` y `09:71` lo llaman "análisis de robustez/sensibilidad" y afirman que "la inferencia principal se apoya en las pruebas pareadas"; `01:4` y `07:135` lo presentan como el análisis principal.
  - Hecho verificado: `grep -i "friedman\|wilcoxon\|bootstrap"` sobre `capitulos/*.typ` ⇒ **0 coincidencias** ✓.
  - Fuente: 3/3 · ✓
  - **Requiere decisión del autor** (no es edición mecánica): (a) incorporar Friedman/Wilcoxon/bootstrap por casos con sus resultados y mantener el ordinal como robustez —opción alineada con NV-01 y con `correccion-01`—, o (b) declarar el ordinal como análisis principal y reescribir `06:708` y `09:71` en consecuencia.
  - Registro: `DECISIONES_integradas.md` (NV-01, PI-29).

- [x] **A-05 · El cuerpo del capítulo 6 sigue exponiendo el análisis viejo como secciones principales** ⛔
  - Ubicaciones: Kruskal–Wallis y Dunn `07:93-131`; Scheirer-Ray-Hare completo con fórmula y tabla H `07:195-226`; referencias a la "interacción que matiza las conclusiones de KW" `07:262-266`.
  - Fuente: [M][m] (y [G] parcial) · ✓
  - Acción: trasladar KW/Dunn/SRH a un anexo rotulado "análisis exploratorio histórico"; dejar en el cuerpo el bloque canónico (especificación, interacción, efectos con IC, sensibilidad a escenarios de fallo).
  - Coherencia adicional: definir los escenarios de fallo en metodología antes de usarlos en evaluación (`07` los usa sin definirlos) y actualizar la descripción del cap. 6 en la estructura del trabajo (`02_capitulo_01_introduccion.typ`), que aún lista "Kruskal-Wallis, Dunn, Scheirer-Ray-Hare" como el análisis del capítulo.

- [x] **A-06 · Seis afirmaciones de determinismo/reproducibilidad por temperatura 0** ⛔
  - Ubicaciones verificadas ✓: `06:191` ("Pydantic AI con temperatura 0"), `06:511` ("respuestas determinísticas"), `06:521` ("temperatura 0 para maximizar la reproducibilidad"), `06:614` (jueces, "temperatura 0,0"), `06:660` ("Temperatura 0 para respuestas determinísticas (evita múltiples ejecuciones)"), `07:16` ("garantizar reproducibilidad").
  - Fuente: 3/3 · ✓ — contradice la corrección ya incorporada en `01:28` y `06:475, 497`.
  - Texto listo: `correccion-03-documentar-api-eliminar-determinismo/propuestas_edicion.md` §3.1–3.8.
  - Efecto colateral a reparar: las dos referencias rotas que remiten a una "sección/corrección sobre parámetros de API" inexistente (`06:475`, `06:492`).

- [x] **A-07 · Atribuciones causales residuales sobre la celda gpt-5-nano** ⛔
  - Ubicaciones verificadas ✓: `07:164` ("la complejidad agéntica es excesiva para modelos de capacidad reducida"), `07:256` ("compensando… mediante su capacidad de razonamiento interna" — debe quedar como hipótesis), `09:75` ("Degradación con modelos pequeños", con p de la base vieja).
  - Fuente: 3/3 · ✓
  - Nota: "sobrecarga agéntica" y "efecto igualador" ya están en 0 ocurrencias en el PDF ✓; estas tres frases son los últimos restos.

- [x] **A-08 · `anexo_01.typ:86` sigue diciendo "modelos mixtos"** ⛔
  - Ubicación verificada ✓: fila de la Tabla 17 sobre `part_j/`.
  - Fuente: [G][M] · ✓ ([m] lo da por resuelto: incorrecto).
  - Acción: reemplazar por la descripción real (modelo ordinal acumulativo + análisis de costos, o lo que efectivamente se ejecutó).

- [x] **A-09 · 14 referencias cruzadas duplicadas ("capítulo Sección N") en el PDF** ⛔ (defecto más visible)
  - Causa: texto manual "capítulo"/"sección" + `@cap:…`/`@sec:…` que imprime "Sección N". Líneas fuente: `04:3, 83, 89, 125, 135`; `06:102, 171, 212, 358, 603`; `07:16, 337`; `09:89`.
  - Fuente: [M][m] · ✓ (14 ocurrencias confirmadas en el PDF; [G] las dio por ausentes por error de método).
  - Acción: `#ref(<etiqueta>, supplement: [Capítulo])` / `[Sección]`, o reescribir el texto ("…del capítulo de metodología").
  - Propuesta: `correccion-07-forma-y-bibliografia/propuesta_edicion_manuscrito.md`.

---

## 2. Altos (🟡) — coherencia editorial y de alcance

- [x] **B-01 · Fortalezas y limitaciones del capítulo 8 con las cifras del análisis viejo**
  - Ubicaciones verificadas ✓: `09:55` ("Mejora significativa con recuperación", p < 0,001 / p = 0,0066), `09:57` ("Configuración costo-eficiente viable", 0,78 vs. 0,80; las canónicas son 0,788 y 0,812), `09:63` ("Análisis estadístico riguroso" con la lista Shapiro–Wilk/KW/Dunn/SRH/MWU), `09:73` ("p = 0.383" → reformular como "no se demostró superioridad global"), `09:75` (ver A-07), `09:136` ("validación mediante LLM-as-a-Judge" en trabajos futuros → "confiabilidad inter-juez").
  - Fuente: 3/3 · ✓
  - Texto listo: `correccion-05-actualizacion-conclusiones-y-analisis-costos/PROPUESTA_TEXTO_MANUSCRITO.md` §4.4.

- [x] **B-02 · Limitaciones faltantes en `sec:limitaciones` (cap. 8)**
  - Faltan: (i) **ejecución única sin réplicas** y ausencia de control efectivo de muestreo; (ii) tratamiento de respuestas no sustantivas (escenario fallo = 0 vs. exclusión) como decisión normativa; (iii) factores confundidos sin ablaciones; (iv) costos de producción no estimados (latencia, infraestructura, mantenimiento, interfaz, costos humanos); (v) réplicas/ablación como límite de las estimaciones (IX.2.4).
  - Fuente: 3/3 · ✓
  - Texto listo: `correccion-01/PROPUESTA_TEXTO_MANUSCRITO.md` §4.5 y `correccion-03/propuestas_edicion.md` §2.

- [x] **B-03 · El índice de eficiencia con piso 0,01 sigue en el cuerpo (objeto directo de V.10)**
  - Ubicaciones verificadas ✓: `07:289-306` (fórmula `max(…, 0.01)` y justificación "evita la división por cero") + figura `media/eficiencia_costo.pdf`.
  - Fuente: [M][m] (+ salvedad de [G]) · ✓
  - Acción: sacarlo del cuerpo (anexo como sensibilidad) o eliminarlo; incorporar frontera de Pareto y tabla de costo por respuesta correcta (≥ 0,75) con IC bootstrap.
  - Insumo: `correccion-05/ANALISIS_COSTOS.md`.

- [x] **B-04 · Objetivo general, objetivo específico 2 y contribuciones de la introducción sin acotar**
  - Ubicaciones verificadas ✓: `02:105` sigue prometiendo "usuarios profesionales y no profesionales"; `02:111` (objetivo específico 2 genérico); `02:131-145` (contribuciones sin el alcance acotado, sin modo de fallo ni modelo ordinal).
  - Fuente: 3/3 · ✓
  - Texto listo: `correccion-05/PROPUESTA_TEXTO_MANUSCRITO.md` §2.1 y §2.3.

- [x] **B-05 · Árbol del repositorio obsoleto en el anexo**
  - Ubicaciones verificadas ✓: `anexo_01.typ:10, 20, 26, 32` (`archivo/`, `examples/notebooks/`, `04_vector_database_creation/` con pgvector) y las secciones descriptivas `:54-68`.
  - Fuente: [G] (los otros dos no lo revisaron) · ✓
  - Acción: sustituir por la estructura real (`codigo_experimentos/part_a…part_j`, `manuscrito/`, `data/`) y añadir dónde viven los artefactos citados en el cuerpo (`verificacion-analisis-estadistico/`, anexo de prompts).

- [x] **B-06 · Prompts de las líneas base y de los jueces no reproducidos; `anexo_02_prompts_y_parametros.typ` no existe**
  - Ubicaciones verificadas ✓: `06:321` describe "un prompt simplificado" para sin RAG / RAG básico; `04:89`, `06:224`, `06:257`, `06:296` remiten al "anexo de prompts del repositorio" (fuera del manuscrito); no hay prompts de los jueces con sus rúbricas.
  - Fuente: [G] (salvedad) [M][m] (pendiente) · ✓
  - Insumos: `correccion-04-declarar-factores-pub-prompts-etc/propuestas/`.

- [x] **B-07 · Tabla 2: 4 ítems de forma pendientes**
  - `03:101` — n-gramas definidos como "secuencias de caracteres" con ejemplo de palabras.
  - `03:333` — "similitud coseno escalada" (la fórmula ya es producto escalado por `1/√d_k`).
  - `03:371` y `03:409` — GPT-4 "introduce arquitectura MoE" / "modelo multimodal con arquitectura MoE" (el informe técnico no lo describe).
  - `01:13` — dedicatoria "A mi familia ..." incompleta.
  - Fuente: 3/3 · ✓
  - Nota: los otros 8 ítems de la Tabla 2 ya están corregidos ✓; `grep "245 artículos"` y `grep "Wikipedia"` ⇒ 0.

- [x] **B-08 · La validación de la extracción del corpus sigue sin cuantificar**
  - Ubicación verificada ✓: `06:67` ("inspección manual de una muestra de artículos", sin tamaño de muestra, sin tasa de error, sin estratificación).
  - Fuente: 3/3 · ✓
  - Texto listo: `correccion-06-precisar-corpus-revisar-respuestas/propuesta_edicion_manuscrito.md` §1.3 (declarar que no existe métrica de error y no afirmar validación estadística).

- [x] **B-09 · Figuras canónicas del reanálisis no incorporadas**
  - Faltan en `manuscrito/media/`: `correccion-01/figuras/02_interaccion_prob_ge_075.pdf`, `03_efectos_simples_probabilidad.pdf`, `04_sensibilidad_escenarios.pdf`; `correccion-02/figuras/01..03`.
  - Fuente: [m] · ✓ (el cap. 6 se apoya todavía en las figuras del análisis histórico).
  - Dependencia: ejecutar junto con A-02, A-03 y A-05.

- [x] **B-10 · Tabla de hiperparámetros: coherencia con la nota sobre `reasoning_effort`**
  - Verificar que `06:475` y `06:492` (temperatura como "valor solicitado", remisión a una sección inexistente) no contradigan la aclaración de `06:497` una vez aplicado A-06.

---

## 3. Medios y menores (🟡/🟢)

- [x] **C-01 · Siglas sin uso** — `acronimos_o_siglas.typ:16` (`HNSW`) y `:26` (`NDCG`) no aparecen en el texto ✓. O se eliminan, o se agrega nDCG@10/Hit@k con las cifras disponibles en `verificacion-analisis-estadistico/metricas_recuperacion/`.

- [x] **C-02 · Citas deterministas (IX.2.2) no anunciadas como trabajo futuro** — no se calculó precisión/exhaustividad de citas ni tasa de artículos inexistentes sobre las 711 respuestas (NV-03 cancelada). Declararlo en "Trabajos Futuros", dado que el marco teórico presenta la citación como riesgo central.

- [x] **C-03 · Réplicas y ablación (IX.2.4)** — el texto advierte que no se recomienda la celda nano "sin réplicas ni ablaciones" (`07:452`) pero no lo declara como límite de *las estimaciones* en cap. 8 (se cierra con B-02).

- [x] **C-04 · Reducción editorial (IX.2.5)** — capítulo 2 (~18–19 páginas, con cronología año por año y RNN/LSTM/GRU con poco uso posterior) y sección 7.7 "Desarrollos Posteriores" (4 subsecciones, ~4–6 páginas). Decidir: recortar o declarar explícitamente como decisión de alcance.

- [x] **C-05 · Comparación con BM25 / otro embedding (IX.2.1)** — no ejecutada por pérdida del volumen de Milvus; ya está declarada en `07:330`. Añadir la lectura de "limitación" y no solo de nota metodológica.

- [x] **C-06 · Afirmación no sustentada sobre el embedding en español** — "un modelo entrenado específicamente en español evita la pérdida de matices" (`06:~171`) sin respaldo empírico; el tribunal la marcó explícitamente. Atenuar o condicionar.

- [x] **C-07 · Bibliografía: coma colgante** — 2 entradas imprimen "(2024, )" y "(2022, )" (Self-RAG y LoRA) por falta de `month` en `referencias.bib`.

- [x] **C-08 · V.7 pendientes menores de conteo** — cuantificar cuántas evaluaciones de Grok se corrigieron a mano y cuántos casos alcanzó la imputación.

---

## 4. Ya cumplido — no re-trabajar

Verificado en esta sesión; los tres informes coinciden en darlo por cerrado:

| Materia | Evidencia |
|---|---|
| Título y portada acotados | `main.typ` — "prototipo Agentic-RAG … Código de Minería argentino" |
| Resumen reescrito con modelo ordinal, 3 efectos e IC | `01:4` ✓ |
| V.3 — no se infiere equivalencia | `07:435, 456`; `09:35`; "efecto igualador" = 0 ocurrencias en el PDF ✓ |
| V.5 — factores confundidos y arquitectura acotada | sección dedicada en `06`; Agente de Calidad resuelto |
| IX.1.6 — corpus, origen, conteos, fecha 1886, respuestas 1.2/1.3 | `06:51-96`; `anexo_01:251, 305, 307` ✓ (salvo B-08) |
| IX.1.8 — declaración de IA ampliada | `01:19-28` ✓ |
| IX.1.9 / V.8 — métricas de recuperación con caveat | `07:312-330` ✓ |
| Tabla 3 — bibliografía | 8/9 ítems; `bommasani` y `dahl` ausentes del `.bib` ✓ |
| "sobrecarga agéntica", "n = 79 por celda", "y col(s).", "245 artículos" | 0 ocurrencias en el PDF ✓ |
| Compilación | `typst compile` → 167 páginas, sin errores ✓ |

---

## 5. Orden de ejecución sugerido

La numeración respeta dependencias: las cifras primero, porque A-02, A-03 y B-01 dependen de A-01.

- [x] **Fase 1 — Decidir y fijar la base numérica:** A-04 (decisión de encuadre) → A-01 → A-03 → A-02 → A-05 → B-09.
- [x] **Fase 2 — Quitar afirmaciones falsas (edición acotada, alto impacto):** A-06 → A-07 → A-08 → A-09.
- [x] **Fase 3 — Coherencia editorial:** B-01 → B-02 → B-03 → B-04 → B-05.
- [x] **Fase 4 — Completitud documental:** B-06 → B-07 → B-08 → B-10 → bloque C.
- [x] **Fase 5 — Pasada final de coherencia** (ver §6) y actualización de `COBERTURA_valoracion_actualizada.md` y `DECISIONES_integradas.md`.

---

## 6. Verificación después de editar

```bash
cd manuscrito && typst compile main.typ /tmp/final.pdf && pdftotext /tmp/final.pdf /tmp/final.txt

# A-06 · determinismo (debe dar 0)
grep -rn "temperatura 0\|temperatura cero\|Temperatura 0\|respuestas determinísticas" capitulos/*.typ

# A-01 · base de cálculo (no debe aparecer 684)
grep -rn "684 observaciones\|fallos puntuales en la generación" capitulos/*.typ

# A-04 · pruebas pareadas efectivamente presentes si se las declara
grep -rin "friedman\|wilcoxon\|bootstrap" capitulos/*.typ

# A-08 · "modelos mixtos" (debe dar 0)
grep -rn "modelos mixtos" capitulos/*.typ

# A-07 · atribuciones causales (debe dar 0)
grep -rn "complejidad agéntica es excesiva\|capacidad de razonamiento interna" capitulos/*.typ

# A-09 · referencias cruzadas duplicadas en el PDF (debe dar 0)
python3 - <<'EOF'
import re
raw = open('/tmp/final.txt', encoding='utf-8').read()
pat = re.compile(r'(cap[ií]tulo|secci[oó]n)\s+Secci[oó]n\s+[0-9.]+', re.I)
print(sum(1 for pg in raw.split('\f') for _ in pat.finditer(re.sub(r'\s+',' ',pg))))
EOF

# Coherencia de cifras resumen ↔ capítulo 6 ↔ conclusiones
grep -rn "293,28\|0,788\|0,812\|41 de 79" capitulos/*.typ
```

---

### 6.1. Resultado de la verificación final

Verificado sobre el PDF recompilado (195 páginas):

| Control | Esperado | Obtenido |
|---|---|---|
| `temperatura 0` / `respuestas determinísticas` | 0 | 0 |
| `684 observaciones` / `fallos puntuales en la generación` | 0 | 0 |
| `friedman` / `wilcoxon` / `bootstrap` en `capitulos/*.typ` | > 0 | 18 |
| `modelos mixtos` | 0 | 0 |
| `complejidad agéntica es excesiva` / `capacidad de razonamiento interna` | 0 | 0 |
| Referencias «capítulo Sección N» en el PDF | 0 | 0 |
| Entradas con coma colgante `(2024, )` / `(2022, )` | 0 | 0 |
| Cifras 293,28 / 0,788 / 0,812 / 41 de 79 presentes | > 0 | 8 / 4 / 4 / 3 |

*Checklist integrado a partir de los tres reportes de verificación del 2026-11-12. Los ítems marcados con ✓ fueron re-verificados contra `manuscrito/capitulos/*.typ` y el PDF compilado durante la integración; las discrepancias entre informes están resueltas en §0.*

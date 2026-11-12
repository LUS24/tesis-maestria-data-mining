# Propuesta de texto para el README — IX.1.5

**Uso:** revisión antes de editar. No se modificó `README.md`. Las propuestas suponen las decisiones recomendadas de `DECISIONES.md` (D-01, D-04, D-05, D-07, D-08, D-09, D-11, D-13).

---

## 1. Descripción del sistema (línea 25)

**Actual**

> Sistema multi-agente (Pydantic AI) con agentes especializados en interpretación de consultas, recuperación de artículos y generación de respuestas.

**Propuesto**

> Sistema de dos agentes activos (Pydantic AI): el Agente Especialista Legal, que interpreta la consulta y redacta la respuesta, y el Agente de Recuperación, que descompone la consulta y busca artículos. El Agente de Calidad fue diseñado pero no se ejecutó; el especialista no itera sobre los resultados ni verifica la respuesta con un agente adicional.

---

## 2. Benchmark (línea 26)

**Actual**

> Pipeline de evaluación con un benchmark de 25 preguntas legales validadas por profesionales del derecho argentino...

**Propuesto**

> Pipeline de evaluación con un benchmark de 25 casos y 79 unidades, revisado por una profesional del derecho argentino. La versión experimental (v1) se conserva congelada; las correcciones detectadas en la auditoría se documentan como v2 para futuras evaluaciones.

---

## 3. Hallazgos principales (líneas 28–36)

**Actual**

| Hallazgo | Descripción |
| --- | --- |
| RAG mejora significativamente la calidad | Tanto RAG básico como Agentic-RAG superan al baseline sin recuperación (p < 0.001) |
| Efecto igualador del RAG | Con RAG básico, modelos pequeños alcanzan desempeño comparable al de modelos superiores |
| Interacción estrategia × modelo | La efectividad de cada estrategia depende del modelo con el que se combine (p < 10⁻¹¹) |
| Sobrecarga agéntica en modelos pequeños | Agentic-RAG puede degradar el desempeño de modelos de capacidad reducida |
| LLM-as-a-Judge validado | Acuerdo inter-juez bueno (α = 0.81) para evaluación de la variable “respuesta correcta” en dominio legal |

**Propuesto**

| Hallazgo | Descripción |
| --- | --- |
| **Interacción estrategia × modelo** | El efecto de la estrategia depende del modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). La interacción es robusta a los escenarios de fallo y a los tres jueces, pero no identifica un componente causal único. |
| **Efecto condicionado al modelo** | En el escenario principal (fallo = 0), Agentic-RAG es inferior a RAG básico en gpt-5-nano (−0,270; IC 95% −0,330 a −0,202), superior en gpt-5-mini (+0,150; IC 95% 0,096 a 0,203) y superior en gpt-5 (+0,106; IC 95% 0,054 a 0,155). |
| **Modo de fallo en Agentic-RAG + gpt-5-nano** | 41/79 salidas no sustantivas (27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas). Cuando responde, la calidad es alta (38/79; media 0,820; mediana 0,958). No se atribuye a la “complejidad agéntica” sin réplicas ni ablaciones. |
| **RAG básico no iguala a los modelos** | Las diferencias observadas son menores, pero no desaparecen: mini−nano +0,063 (IC 95% 0,005–0,120), gpt-5−nano +0,128 (IC 95% 0,071–0,186), gpt-5−mini +0,065 (IC 95% 0,011–0,124). No se demostró equivalencia. |
| **Jueces: acuerdo, no validación** | α ordinal global de 0,808 con valores originales (0,800 tras transformar valores fuera de rúbrica). Mide confiabilidad entre jueces, no validez frente a criterio humano. La auditoría detectó puntajes positivos sobre salidas no sustantivas. |
| **Costos: no hay ganador único** | RAG básico + gpt-5-nano presenta el menor costo puntual por respuesta aceptable (USD 0,0061; IC bootstrap 0,0043–0,0091; 33/79; media 0,599), con IC solapado con Sin RAG + nano; no se establece una diferencia formal. Agentic-RAG + gpt-5 maximiza la media (0,812; USD 0,0792). Agentic-RAG + gpt-5-mini (0,788; USD 0,0564) es una alternativa no dominada, no la más barata. |
| **Alcance** | Un corpus (Código de Minería), 25 casos, 79 unidades, una ejecución por celda y un recuperador fijo en gpt-5. Los resultados son evidencia de viabilidad, no una validación externa ni una recomendación universal. |

**No conservar** las filas “RAG mejora significativamente”, “Efecto igualador”, “Sobrecarga agéntica” y “LLM-as-a-Judge validado” en su forma actual.

---

## 4. ¿Por qué es relevante? (líneas 40–43)

**Actual (ideas):** acceso a la justicia, código abierto, metodología replicable, primer sistema.

**Propuesto**

```markdown
- **Acceso a la justicia**: explora una alternativa abierta para consultar normativa; no se evaluó su impacto ni su uso por ciudadanos o profesionales.
- **Código abierto**: el código, el benchmark y los logs permiten auditar y adaptar el prototipo a otras normativas, sujeto a validación externa.
- **Metodología auditable**: el diseño apareado, el análisis de fallos y el costo por respuesta aceptable pueden reutilizarse en otras evaluaciones.
- **Antecedentes**: no se identificaron sistemas públicos comparables para normativa argentina en la búsqueda realizada; no se afirma que sea el “primer sistema” en sentido absoluto.
```

---

## 5. Análisis estadístico (línea 140)

**Actual**

> Kruskal-Wallis, Dunn con corrección Bonferroni, Scheirer-Ray-Hare (interacción), Krippendorff's alpha (acuerdo inter-juez).

**Propuesto**

> Modelo ordinal mixto con interceptos aleatorios por caso y unidad (interacción estrategia × modelo), pruebas pareadas de Friedman/Wilcoxon como sensibilidad, bootstrap por casos, corrección de Holm dentro de familias y Krippendorff's alpha para el acuerdo inter-juez. Las pruebas para muestras independientes del análisis original se conservan solo como antecedente exploratorio.

---

## 6. Métricas (líneas 135–138)

**Actual**

> Textuales: BLEU, ROUGE-1, ROUGE-L, METEOR, exactitud de tokens...

**Propuesto**

> Textuales y léxicas: Token F1, Jaccard, Levenshtein, BLEU, ROUGE-1/2/L, CER y ratios de longitud. Semánticas: SBERT Similarity (español y multilingüe) y BERTScore. Evaluación por jueces: corrección y precisión legal con tres modelos (DeepSeek, Grok y Kimi K2).

**Motivo:** el manuscrito no usa METEOR ni “exactitud de tokens” como métrica principal; la lista del README debe coincidir con el código.

---

## 7. Agradecimientos (línea 170)

**Actual**

> A los profesionales del derecho argentino que colaboraron en la validación del benchmark.

**Propuesto**

> A la profesional del derecho argentino que revisó el benchmark y registró sus observaciones.

**Motivo:** la evidencia disponible corresponde a una revisora; “profesionales” y “validación” sobreestiman el proceso.

---

## 8. Nota metodológica que conviene agregar después del diseño experimental

```markdown
> **Nota metodológica:** se realizó una única ejecución por unidad y configuración. El código solicitó `temperature=0.0`, pero Pydantic AI 1.1.0 elimina ese parámetro para los modelos GPT-5; las respuestas no se consideran deterministas y el esfuerzo de razonamiento no se registró. El recuperador agéntico fue siempre gpt-5; gpt-5 usó un límite de 7 búsquedas y mini/nano de 6. Los análisis respetan el apareamiento por unidad y el anidamiento en 25 casos.
```

---

## 9. Qué no cambiar en el README sin evidencia

- No volver a afirmar que el repositorio “reproduce” el experimento sin una prueba de clonación anónima.
- No afirmar que los jueces están “validados”.
- No presentar Agentic-RAG + mini como “costo-eficiente” sin aclarar que no es la opción más barata.
- No usar medianas globales (0,58 → 0,83) como resumen del efecto: ocultan la interacción y los fallos.
- No afirmar que el sistema atiende usuarios profesionales y no profesionales: no hubo interfaz ni estudio de usuarios.

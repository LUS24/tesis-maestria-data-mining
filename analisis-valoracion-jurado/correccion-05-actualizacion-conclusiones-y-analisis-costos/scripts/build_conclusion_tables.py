#!/usr/bin/env python3
"""Genera las tablas de trazabilidad de la corrección IX.1.5.

No modifica el manuscrito ni los datos fuente. Las filas son una síntesis
editorial de la evidencia ya producida por las correcciones 01–07.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PACKAGE_DIR / "datos"
OUT_DIR = PACKAGE_DIR / "salidas"
for directory in (DATA_DIR, OUT_DIR):
    directory.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


TABLA4 = [
    {
        "id": "T4-01",
        "conclusion_original": "La recuperación ‘mejora significativamente la calidad de las respuestas’ (p. 97).",
        "estado": "Se reformula",
        "formulacion_propuesta": "No se observó una mejora uniforme de ‘la recuperación’. En gpt-5-mini, RAG básico y Agentic-RAG superaron a Sin RAG (+0,363; IC 0,304–0,417 y +0,513; IC 0,454–0,562). En gpt-5, Agentic-RAG superó a RAG básico y Sin RAG (+0,106; IC 0,054–0,155 y +0,095; IC 0,046–0,146), mientras RAG básico no se diferenció de Sin RAG (−0,011; IC −0,063 a 0,044). En gpt-5-nano, Agentic-RAG fue inferior a RAG básico y Sin RAG (−0,270; IC −0,330 a −0,202 y −0,242; IC −0,307 a −0,176), y RAG básico no se diferenció de Sin RAG (+0,028; IC −0,032 a 0,085).",
        "evidencia": "Corrección 01: modelo ordinal mixto principal; salidas/31_efectos_simples_orientados.csv; salidas/23_efectos_simples_latentes.csv; salidas/35_resultados_clave.json.",
        "no_afirmar": "Que ‘la recuperación’ sea un factor único; que el efecto sea uniforme; que RAG básico mejore en gpt-5 o nano; que Agentic-RAG sea siempre superior.",
        "ubicaciones": "01_texto_preliminar.typ:4; 07_capitulo_06_evaluacion.typ:435; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:45,136",
        "decisiones": "D-01, D-09",
    },
    {
        "id": "T4-02",
        "conclusion_original": "La interacción entre estrategia y modelo como hallazgo principal (p. 114).",
        "estado": "Se conserva con matices",
        "formulacion_propuesta": "Se observó una interacción fuerte entre estrategia y modelo del Agente Especialista Legal (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²; AIC 5.525,0 vs. 5.810,3). El patrón se mantiene en los escenarios de sensibilidad (LR 82,52–293,28; p < 10⁻¹⁶) y en los tres jueces. Es un hallazgo sobre el efecto conjunto, no sobre un componente aislado de la estrategia.",
        "evidencia": "Corrección 01: salidas/20_modelo_interaccion.csv; salidas/25_modelo_por_juez.csv. Corrección 04: confundidos y límites 7/6.",
        "no_afirmar": "Que la interacción demuestre que la descomposición, la selección, el prompt o el número de candidatos sean la causa. El recuperador fue siempre gpt-5; gpt-5 usó 7 búsquedas y mini/nano 6.",
        "ubicaciones": "01_texto_preliminar.typ:4; 07_capitulo_06_evaluacion.typ:222,435; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:29",
        "decisiones": "D-06",
    },
    {
        "id": "T4-03",
        "conclusion_original": "‘Efecto igualador del RAG básico’ (p. 114).",
        "estado": "Se retira",
        "formulacion_propuesta": "No se demostró equivalencia. Con RAG básico, las diferencias entre modelos fueron menores, pero las estimaciones fueron positivas: mini−nano +0,063 (IC 0,005–0,120), gpt-5−nano +0,128 (IC 0,071–0,186), gpt-5−mini +0,065 (IC 0,011–0,124). Los dos últimos contrastes fueron limítrofes en escala latente tras Holm (p = 0,068 y 0,064). Los intervalos no definen un margen de equivalencia.",
        "evidencia": "Corrección 01: salidas/31_efectos_simples_orientados.csv; salidas/23_efectos_simples_latentes.csv; salidas/34_wilcoxon_principal.csv.",
        "no_afirmar": "Que el RAG básico elimine o iguale las diferencias; que un p no significativo demuestre equivalencia; que los modelos pequeños alcancen a los superiores.",
        "ubicaciones": "01_texto_preliminar.typ:4; 07_capitulo_06_evaluacion.typ:131,265,414; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:31,45,138",
        "decisiones": "D-01",
    },
    {
        "id": "T4-04",
        "conclusion_original": "‘Identificación de la sobrecarga agéntica en modelos pequeños’ (p. 114).",
        "estado": "Se retira como explicación causal; se conserva el hallazgo descriptivo",
        "formulacion_propuesta": "En Agentic-RAG + gpt-5-nano, 41 de 79 salidas no fueron sustantivas: 27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada y 10 indeterminadas (51,9%; IC Wilson 41,1–62,6%). La media de la celda con fallo = 0 fue 0,395 y la mediana 0,000. Cuando produjo una respuesta sustantiva (38/79), la media fue 0,820 y la mediana 0,958. Los logs muestran recuperación y tokens de salida; no hay evidencia de truncamiento por longitud. El patrón se describe como un modo de fallo de respuesta, no como una degradación uniforme ni como efecto causal de la ‘complejidad agéntica’.",
        "evidencia": "Corrección 02: INFORME_DIAGNOSTICO.md §3–§4; salidas/14_dataset_categoria_final.csv; salidas/11_celda_nano_agentic_79.csv; salidas/06_logs_agentes_237.csv. Corrección 01: salidas/32_tabla_sensibilidad_nano.csv.",
        "no_afirmar": "Que la causa sea la complejidad de la arquitectura; que el modelo pequeño tenga una degradación general; que más recuperación lo resolvería; que el resultado sea estable entre réplicas.",
        "ubicaciones": "01_texto_preliminar.typ:4; 07_capitulo_06_evaluacion.typ:164,419; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:33,73,83,101,132",
        "decisiones": "D-05, D-06",
    },
    {
        "id": "T4-05",
        "conclusion_original": "‘Validación de LLM-as-a-Judge para evaluación legal’ (p. 115).",
        "estado": "Se retira la palabra ‘validación’; se conserva la confiabilidad",
        "formulacion_propuesta": "Los tres jueces mostraron un acuerdo ordinal global bueno para corrección: α = 0,807842 con puntajes originales y α = 0,799542 después de transformar los valores fuera de rúbrica al valor más cercano; el cálculo fue verificado de forma independiente en verificacion-analisis-estadistico/. Eso mide confiabilidad entre jueces, no validez frente a criterio humano. No existen calificaciones humanas de las 711 respuestas; la revisión humana del benchmark es la referencia del instrumento, no una validación de los jueces. Se identificaron 23 discrepancias entre jueces para revisión humana y 17 evaluaciones positivas sobre salidas no sustantivas.",
        "evidencia": "verificacion-analisis-estadistico/salidas/resumen_verificacion.json; corrección 02: salidas/17_auditoria_jueces_salidas_no_sustantivas_final.csv.",
        "no_afirmar": "Que los jueces estén validados; que el acuerdo demuestre validez; que α = 0,81 autorice a usar los puntajes sin auditoría; que la precisión legal sea confiable en todos los sistemas.",
        "ubicaciones": "README.md:36; 07_capitulo_06_evaluacion.typ:415; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:37,85",
        "decisiones": "D-08, D-14",
    },
    {
        "id": "T4-06",
        "conclusion_original": "‘El objetivo 2 se cumplió completamente’ (p. 113).",
        "estado": "Se reformula a cumplimiento parcial",
        "formulacion_propuesta": "El objetivo 2 se cumple parcialmente y el objetivo específico debe actualizarse en la introducción. Se implementaron dos agentes activos: Especialista Legal y Recuperación. El especialista realiza una delegación nominal de recuperación; no itera sobre los resultados ni verifica la respuesta con un agente adicional. El Agente de Calidad fue diseñado, pero nunca se ejecutó. En 236 de 237 sesiones el especialista hizo una llamada a retrieve_relevant_documents; la sesión 16_01 de gpt-5 registró tres. No se cumplió un ciclo completo de verificación multi-agente.",
        "evidencia": "Corrección 04: 03_resolucion_contradicciones.md; propuestas/cambios_manuscrito.md §10; salidas/sesiones_agentic.csv.",
        "no_afirmar": "Que el sistema sea un planificador autónomo; que el Agente de Calidad haya mejorado o empeorado el sistema; que el especialista itere; que todas las configuraciones usen seis búsquedas.",
        "ubicaciones": "09_capitulo_08_conclusion_y_trabajos_futuros.typ:17",
        "decisiones": "D-10",
    },
    {
        "id": "T4-07",
        "conclusion_original": "‘Combinación costo-eficiente: Agentic-RAG + gpt-5-mini’ (p. 97).",
        "estado": "Se retira la recomendación única; se reemplaza por Pareto",
        "formulacion_propuesta": "No hay una combinación costo-eficiente única. Agentic-RAG + gpt-5-mini cuesta USD 0,0564 por consulta, más que RAG básico + gpt-5 (USD 0,0392) y Sin RAG + gpt-5 (USD 0,0478); su media es 0,788. Es una opción no dominada de calidad alta, no la más barata. La definición D-02 operacionaliza “respuesta correcta” como puntaje promedio ≥ 0,75. El menor costo puntual por respuesta correcta corresponde a RAG básico + gpt-5-nano (USD 0,0061; IC bootstrap 0,0043–0,0091; 33/79; media 0,599); su IC se solapa con Sin RAG + nano (0,0058–0,0107), de modo que no se establece una diferencia formal entre ambas. La mayor media corresponde a Agentic-RAG + gpt-5 (0,812; USD 0,0792; 56/79). La elección depende del objetivo y debe reportarse la frontera de Pareto, sin el piso 0,01.",
        "evidencia": "ANALISIS_COSTOS.md; datos/costos_por_celda.csv; datos/frontera_pareto.csv; datos/comparacion_recomendacion_anterior.csv; salidas/resumen_costos.json.",
        "no_afirmar": "Que Agentic-RAG + mini sea más barato que RAG básico + gpt-5 o Sin RAG + gpt-5; que el índice con piso 0,01 ordene las configuraciones; que el costo por respuesta correcta sea una medida de producción; que los precios históricos sigan vigentes.",
        "ubicaciones": "07_capitulo_06_evaluacion.typ:291,310,429; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:57",
        "decisiones": "D-02, D-03, D-04",
    },
    {
        "id": "T4-08",
        "conclusion_original": "‘Este resultado es transferible a otros dominios y aplicaciones de RAG’ (p. 120).",
        "estado": "Se retira",
        "formulacion_propuesta": "No se demostró transferibilidad. Los resultados corresponden a un corpus (Código de Minería), 25 casos, 79 unidades, una ejecución por celda, un recuperador fijo en gpt-5 y prompts/límites diferentes entre estrategias. La interacción observada es una hipótesis a evaluar en otros corpus y configuraciones, no una propiedad general de Agentic-RAG.",
        "evidencia": "Corrección 01: limitaciones §9; corrección 04: confundidos; corrección 06: alcance del corpus; ANALISIS_COSTOS.md §7.",
        "no_afirmar": "Que el patrón se repita en medicina, ingeniería o finanzas; que el sistema sea replicable sin validación externa; que el corpus equivalga a ‘normativa nacional’.",
        "ubicaciones": "09_capitulo_08_conclusion_y_trabajos_futuros.typ:138",
        "decisiones": "D-06, D-09, D-11",
    },
    {
        "id": "T4-09",
        "conclusion_original": "‘Atención a usuarios profesionales y no profesionales’ (p. 6) y publicación en repositorio abierto (p. 114).",
        "estado": "Se reformula en dos partes",
        "formulacion_propuesta": "No se evaluó con usuarios ni se desarrolló una interfaz; el sistema es un prototipo de investigación ejecutado como pipeline/notebooks. La atención a profesionales y ciudadanos es un uso potencial, no un resultado medido. El repositorio es público y accesible desde el navegador sin login; contiene código, benchmark, corpus, logs y evaluaciones. Se considera cumplido el acceso público. La clonación y ejecución se recomiendan como verificación de reproducibilidad, no como bloqueo del objetivo de acceso.",
        "evidencia": "Verificación pública del 2026-11-11; decisión D-11; corrección 07; README del proyecto.",
        "no_afirmar": "Que el sistema haya sido usado o validado por profesionales o ciudadanos; que la disponibilidad del código equivalga a una interfaz desplegada; que el acceso público equivalga a reproducibilidad exacta.",
        "ubicaciones": "02_capitulo_01_introduccion.typ:105; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:21,47,81; README.md:40",
        "decisiones": "D-09, D-11",
    },
]

MATRIZ = [
    {
        "id": "E-01",
        "afirmacion": "Interacción estrategia × modelo del especialista",
        "estado": "Robusta; no causal",
        "evidencia": "Modelo ordinal mixto, LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²; escenarios LR 82,52–293,28; tres jueces",
        "fuente": "Corrección 01: salidas/20_modelo_interaccion.csv; salidas/25_modelo_por_juez.csv",
        "cifra": "LR 293,28; p 3,05e-62",
        "limitacion": "Recuperador fijo gpt-5; prompts y límites 7/6; sin ablación",
        "decision": "D-06",
    },
    {
        "id": "E-02",
        "afirmacion": "Agentic-RAG vs. RAG básico en gpt-5-nano",
        "estado": "Negativo con fallo = 0; positivo con exclusión",
        "evidencia": "Diferencia modelada −0,270 (IC −0,330 a −0,202); exclusión +0,216 (IC 0,146–0,279)",
        "fuente": "Corrección 01: salidas/31_efectos_simples_orientados.csv; salidas/32_tabla_sensibilidad_nano.csv",
        "cifra": "−0,270 / +0,216",
        "limitacion": "La exclusión es submuestra seleccionada; 41/79 no sustantivas",
        "decision": "D-01, D-05",
    },
    {
        "id": "E-03",
        "afirmacion": "Agentic-RAG vs. RAG básico en gpt-5-mini",
        "estado": "Positivo",
        "evidencia": "Diferencia modelada +0,150 (IC 0,096–0,203); Agentic vs. Sin RAG +0,513 (IC 0,454–0,562); p Holm 1,72e-7 y 9,42e-54",
        "fuente": "Corrección 01: salidas/31_efectos_simples_orientados.csv; salidas/23_efectos_simples_latentes.csv",
        "cifra": "+0,150; +0,513",
        "limitacion": "Una ejecución por celda; recuperador fijo",
        "decision": "D-01",
    },
    {
        "id": "E-04",
        "afirmacion": "Agentic-RAG vs. RAG básico en gpt-5",
        "estado": "Positivo, menor que en mini",
        "evidencia": "Diferencia modelada +0,106 (IC 0,054–0,155); vs. Sin RAG +0,095 (IC 0,046–0,146); p Holm 1,03e-4 y 4,82e-4",
        "fuente": "Corrección 01: salidas/31_efectos_simples_orientados.csv; salidas/23_efectos_simples_latentes.csv",
        "cifra": "+0,106; +0,095",
        "limitacion": "gpt-5 usó 7 búsquedas; mini/nano 6",
        "decision": "D-01, D-06",
    },
    {
        "id": "E-05",
        "afirmacion": "RAG básico iguala a los modelos",
        "estado": "No sostenido",
        "evidencia": "mini−nano +0,063 (0,005–0,120); gpt-5−nano +0,128 (0,071–0,186); gpt-5−mini +0,065 (0,011–0,124); p latentes 0,068 y 0,064",
        "fuente": "Corrección 01: salidas/31_efectos_simples_orientados.csv; salidas/23_efectos_simples_latentes.csv",
        "cifra": "+0,063; +0,128; +0,065",
        "limitacion": "No hay margen de equivalencia; IC no lo establecen",
        "decision": "D-01",
    },
    {
        "id": "E-06",
        "afirmacion": "Salidas no sustantivas de Agentic-RAG + gpt-5-nano",
        "estado": "41/79; modo de fallo",
        "evidencia": "27 vacías, 1 solo espacios, 2 abstenciones, 1 truncada, 10 indeterminadas; 38/79 sustantivas con media 0,820",
        "fuente": "Corrección 02: INFORME_DIAGNOSTICO.md §3–§4; salidas/14_dataset_categoria_final.csv",
        "cifra": "41/79 = 51,9%",
        "limitacion": "No hay causa identificada; una ejecución; logs sin payload",
        "decision": "D-05",
    },
    {
        "id": "E-07",
        "afirmacion": "Jueces validados",
        "estado": "No sostenido; confiabilidad solamente",
        "evidencia": "α 0,807842 raw / 0,799542 rúbrica, verificado en verificacion-analisis-estadistico; 23 discrepancias; 17 evaluaciones positivas no sustantivas",
        "fuente": "verificacion-analisis-estadistico/salidas/resumen_verificacion.json; corrección 02: salidas/17_auditoria_jueces_salidas_no_sustantivas_final.csv",
        "cifra": "α 0,807842 / 0,799542",
        "limitacion": "Sin validación humana; inconsistencias en salidas no sustantivas",
        "decision": "D-08, D-14",
    },
    {
        "id": "E-08",
        "afirmacion": "Objetivo 2 completo",
        "estado": "Parcial",
        "evidencia": "Dos agentes activos; una delegación; Agente de Calidad no ejecutado; 236/237 sesiones con una llamada; 16_01 con tres",
        "fuente": "Corrección 04: 03_resolucion_contradicciones.md; salidas/sesiones_agentic.csv",
        "cifra": "236/237; 0 ejecuciones de calidad",
        "limitacion": "No hay iteración ni verificación",
        "decision": "D-10",
    },
    {
        "id": "E-09",
        "afirmacion": "Agentic-RAG + mini es costo-eficiente",
        "estado": "No sostenido en sentido absoluto",
        "evidencia": "USD 0,0564 vs. RAG gpt-5 USD 0,0392 y Sin RAG gpt-5 USD 0,0478; no dominada; 0,788",
        "fuente": "ANALISIS_COSTOS.md; datos/comparacion_recomendacion_anterior.csv",
        "cifra": "USD 0,0564; 55/79 respuestas correctas; USD 0,0810 por respuesta correcta",
        "limitacion": "Precios históricos; umbral 0,75; una ejecución",
        "decision": "D-02, D-03, D-04",
    },
    {
        "id": "E-10",
        "afirmacion": "Menor costo por respuesta correcta",
        "estado": "RAG básico + nano",
        "evidencia": "USD 0,0061 por respuesta correcta (≥ 0,75); 33/79; media 0,599",
        "fuente": "ANALISIS_COSTOS.md; datos/costos_por_celda.csv",
        "cifra": "USD 0,0061",
        "limitacion": "Umbral 0,75; no mide producción; no es la mayor calidad",
        "decision": "D-02, D-04",
    },
    {
        "id": "E-11",
        "afirmacion": "Benchmark v1 revisado",
        "estado": "Revisado, no validado",
        "evidencia": "25 casos/79 unidades; revisión por una profesional; 12 propuestas v2; revisión LLM posterior detectó posibles errores que requieren revisión profesional",
        "fuente": "Corrección 06; decisión D-07; revisión con ollama-cloud:deepseek-v4.1-flash:1017-cloud",
        "cifra": "25/79; 12 propuestas",
        "limitacion": "Sin segunda revisión profesional; v1 con observaciones abiertas",
        "decision": "D-07",
    },
    {
        "id": "E-12",
        "afirmacion": "Acceso público verificado sin login",
        "estado": "Acceso público sin login verificado; clonación recomendada para reproducibilidad",
        "evidencia": "HTTP 200 y API GitHub private=false el 2026-11-11; 32 notebooks, 1.838 logs, 27 reportes",
        "fuente": "Verificación pública; decisión D-11; plan IX.1.8",
        "cifra": "32 notebooks; 1.838 logs; 27 reportes",
        "limitacion": "Clonación recomendada, no bloqueante; sin interfaz",
        "decision": "D-11",
    },
]


UBICACIONES = [
    ("manuscrito/capitulos/01_texto_preliminar.typ", 4, "Resumen", "Reemplazar párrafo de resultados", "PROPUESTA_TEXTO_MANUSCRITO.md §1.2", "D-01, D-05, D-09"),
    ("manuscrito/capitulos/02_capitulo_01_introduccion.typ", 105, "Objetivo general", "Limitar a evaluación con benchmark, sin usuarios", "PROPUESTA_TEXTO_MANUSCRITO.md §2.1", "D-09"),
    ("manuscrito/capitulos/02_capitulo_01_introduccion.typ", 111, "Objetivo específico 2", "Dos agentes activos; sin ciclo de verificación", "PROPUESTA_TEXTO_MANUSCRITO.md §2.1.1", "D-10"),
    ("manuscrito/capitulos/02_capitulo_01_introduccion.typ", 115, "Objetivo específico 4", "Acceso público sin login; clonación recomendada", "PROPUESTA_TEXTO_MANUSCRITO.md §2.1.2", "D-11"),
    ("manuscrito/main.typ", 4, "Título", "Título al alcance real", "PROPUESTA_TEXTO_MANUSCRITO.md §2.2", "D-09"),
    ("manuscrito/capitulos/02_capitulo_01_introduccion.typ", 135, "Contribuciones", "Reemplazar lista completa", "PROPUESTA_TEXTO_MANUSCRITO.md §2.3", "D-05, D-07, D-13"),
    ("manuscrito/capitulos/07_capitulo_06_evaluacion.typ", 412, "Fortalezas", "Reemplazar viñetas", "PROPUESTA_TEXTO_MANUSCRITO.md §3.1", "D-04, D-08"),
    ("manuscrito/capitulos/07_capitulo_06_evaluacion.typ", 419, "Debilidades", "Reemplazar viñetas", "PROPUESTA_TEXTO_MANUSCRITO.md §3.2", "D-05, D-06"),
    ("manuscrito/capitulos/07_capitulo_06_evaluacion.typ", 424, "Párrafo gpt-5", "Eliminar especulación; corregir efecto positivo", "PROPUESTA_TEXTO_MANUSCRITO.md §3.3", "D-01, D-06"),
    ("manuscrito/capitulos/07_capitulo_06_evaluacion.typ", 428, "Implicaciones prácticas", "Reemplazar por Pareto y objetivo", "PROPUESTA_TEXTO_MANUSCRITO.md §3.4", "D-02, D-04"),
    ("manuscrito/capitulos/07_capitulo_06_evaluacion.typ", 435, "Conclusión del capítulo", "Reemplazar por análisis apareado", "PROPUESTA_TEXTO_MANUSCRITO.md §3.5", "D-01, D-05"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 15, "Objetivos", "Reemplazar 4 viñetas", "PROPUESTA_TEXTO_MANUSCRITO.md §4.1", "D-07, D-10, D-11, D-12"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 27, "Contribuciones", "Reemplazar lista", "PROPUESTA_TEXTO_MANUSCRITO.md §4.2", "D-04, D-05, D-08"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 45, "Impacto", "Reemplazar párrafo", "PROPUESTA_TEXTO_MANUSCRITO.md §4.3", "D-01, D-03"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 55, "Fortalezas", "Reemplazar viñetas", "PROPUESTA_TEXTO_MANUSCRITO.md §4.4", "D-04, D-05, D-06"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 71, "Limitaciones", "Reemplazar diferencia marginal", "PROPUESTA_TEXTO_MANUSCRITO.md §4.5", "D-01"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 73, "Limitaciones", "Reemplazar degradación", "PROPUESTA_TEXTO_MANUSCRITO.md §4.5", "D-05"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 83, "Limitaciones", "Reemplazar sobrecarga temporal", "PROPUESTA_TEXTO_MANUSCRITO.md §4.5", "D-05, D-06"),
    ("manuscrito/capitulos/07_capitulo_06_evaluacion.typ", 346, "Alpha de Krippendorff", "Reemplazar 0,808/0,800 por valores verificados", "PROPUESTA_TEXTO_MANUSCRITO.md §3.1", "D-14"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 37, "Contribución LLM-as-a-Judge", "Cambiar a confiabilidad inter-juez; no validación", "PROPUESTA_TEXTO_MANUSCRITO.md §4.2", "D-08, D-14"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 85, "Limitaciones", "Corregir validación humana y documentar discrepancias", "PROPUESTA_TEXTO_MANUSCRITO.md §4.5", "D-01, D-08, D-14"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 101, "Trabajos futuros", "Reemplazar sobrecarga", "PROPUESTA_TEXTO_MANUSCRITO.md §4.6", "D-05"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 132, "Trabajos futuros", "Reemplazar degradación/validación", "PROPUESTA_TEXTO_MANUSCRITO.md §4.6", "D-05, D-08"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 136, "Reflexiones finales", "Reemplazar dos párrafos", "PROPUESTA_TEXTO_MANUSCRITO.md §4.7", "D-08, D-09"),
    ("manuscrito/capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ", 140, "Reflexiones finales", "Reemplazar párrafo final", "PROPUESTA_TEXTO_MANUSCRITO.md §4.7", "D-09, D-11"),
    ("manuscrito/capitulos/anexo_01.typ", 232, "Ejemplo Agentic-RAG", "Reemplazar generalización", "PROPUESTA_TEXTO_MANUSCRITO.md §5", "D-05"),
    ("README.md", 25, "Descripción del sistema", "Dos agentes activos; calidad no ejecutada", "PROPUESTA_TEXTO_README.md §1", "D-10"),
    ("README.md", 26, "Benchmark", "Revisión por una profesional; v1/v2", "PROPUESTA_TEXTO_README.md §2", "D-07"),
    ("README.md", 28, "Hallazgos", "Reemplazar tabla", "PROPUESTA_TEXTO_README.md §3", "D-01, D-04, D-05, D-08"),
    ("README.md", 40, "Relevancia", "Potencial, no impacto demostrado", "PROPUESTA_TEXTO_README.md §4", "D-09"),
    ("README.md", 135, "Métricas", "Alinear con código", "PROPUESTA_TEXTO_README.md §6", "—"),
    ("README.md", 140, "Análisis estadístico", "Modelo ordinal mixto y alpha verificado", "PROPUESTA_TEXTO_README.md §5", "D-01, D-14"),
    ("README.md", 170, "Agradecimientos", "Una profesional", "PROPUESTA_TEXTO_README.md §7", "D-07"),
    ("README.md", 30, "Título y BibTeX", "Título al alcance real", "PROPUESTA_TEXTO_README.md §9", "D-09"),
]

FRASES = [
    ("efecto igualador", "07_capitulo_06_evaluacion.typ:131,265,414; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:31,45", "diferencias reducidas, no equivalencia", "El p no significativo de Kruskal-Wallis no demuestra equivalencia; el modelo apareado muestra diferencias positivas."),
    ("sobrecarga agéntica", "07_capitulo_06_evaluacion.typ:419; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:33,83,101", "modo de fallo de respuesta", "No hay evidencia causal; 41/79 no sustantivas, 38/79 sustantivas con calidad alta."),
    ("validación de LLM-as-a-Judge", "09_capitulo_08_conclusion_y_trabajos_futuros.typ:37; README.md:36", "acuerdo inter-juez; confiabilidad, no validez", "No se comparó con criterio humano; se detectaron puntajes positivos en salidas no sustantivas."),
    ("En gpt-5 no hay diferencias significativas entre estrategias", "07_capitulo_06_evaluacion.typ:424,435; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:45,138", "Agentic-RAG +0,106 frente a RAG básico y +0,095 frente a Sin RAG", "El análisis apareado detecta diferencias positivas; la conclusión anterior usaba pruebas no apareadas."),
    ("resultado transferible a otros dominios", "09_capitulo_08_conclusion_y_trabajos_futuros.typ:138", "hipótesis a evaluar; no transferibilidad demostrada", "Un corpus, 25 casos, una ejecución y un recuperador fijo."),
    ("Combinación costo-eficiente: Agentic-RAG + gpt-5-mini", "07_capitulo_06_evaluacion.typ:429; 09_capitulo_08_conclusion_y_trabajos_futuros.typ:57", "opción no dominada; Pareto; costo por respuesta correcta (≥ 0,75)", "Agentic mini cuesta más que RAG gpt-5 y Sin RAG gpt-5; no es la más barata. D-02 define respuesta correcta."),
    ("objetivo 2 se cumplió completamente", "09_capitulo_08_conclusion_y_trabajos_futuros.typ:17", "cumplimiento parcial", "Dos agentes activos, una delegación, sin verificador; el Agente de Calidad no se ejecutó. D-10 actualiza el objetivo específico 2."),
    ("temperatura 0 / determinista", "06_capitulo_05_metodologia.typ:461,644; 07_capitulo_06_evaluacion.typ:16; 09...:87", "configuración solicitada, no aplicada; sin determinismo", "Pydantic AI 1.1.0 elimina temperature para GPT-5; el esfuerzo de razonamiento no se registró."),
    ("n = 79 observaciones por celda", "07_capitulo_06_evaluacion.typ:424", "79 unidades y 2.133 evaluaciones; 653 en exclusión", "Las 27 medias ausentes eran un join, no 27 fallos; el n efectivo cambia por escenario."),
    ("245 artículos / 399 artículos", "04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ:111; 06_capitulo_05_metodologia.typ:101", "398 nodos artículo (397 con texto) o ‘artículo inexistente’", "El corpus tiene 482 nodos; 398 son artículos; el 239 está vacío/derogado."),
    ("IVF_FLAT", "09_capitulo_08_conclusion_y_trabajos_futuros.typ:15; 06_capitulo_05_metodologia.typ:138", "AUTOINDEX con similitud coseno", "El código de creación de la base usa AUTOINDEX; D-12 adopta esa descripción."),
    ("validado por un profesional / profesionales", "README.md:26,170; 09...:19; anexo_01.typ:236", "revisado por una profesional; v1 congelado", "Una revisión registrada; revisión LLM posterior detectó posibles errores que requieren revisión profesional."),
    ("primer sistema de este tipo", "09_capitulo_08_conclusion_y_trabajos_futuros.typ:27", "no se identificaron antecedentes públicos comparables", "Evita una prioridad absoluta no censada."),
    ("mediana global 0.58 a 0.83", "09_capitulo_08_conclusion_y_trabajos_futuros.typ:45", "efectos condicionales por modelo y escenario", "La mediana global oculta la interacción y los fallos."),
    ("0.08 vs. 0.58 / 0.92 frente a 0.33", "01_texto_preliminar.typ:4; 09...:45", "cifras del modelo ordinal con IC", "Las medianas antiguas se calcularon sobre 76 filas y sin escenario de fallo."),
]


def main() -> None:
    categorias = {
        "T4-01": "Se reformula",
        "T4-02": "Se conserva",
        "T4-03": "Se retira",
        "T4-04": "Se reformula",
        "T4-05": "Se reformula",
        "T4-06": "Se reformula",
        "T4-07": "Se reformula",
        "T4-08": "Se retira",
        "T4-09": "Se reformula",
    }
    for row in TABLA4:
        row["categoria"] = categorias[row["id"]]
    fields4 = ["id", "categoria", "conclusion_original", "estado", "formulacion_propuesta", "evidencia", "no_afirmar", "ubicaciones", "decisiones"]
    write_csv(DATA_DIR / "tabla4_reformulada.csv", TABLA4, fields4)

    fields_matrix = ["id", "afirmacion", "estado", "evidencia", "fuente", "cifra", "limitacion", "decision"]
    write_csv(DATA_DIR / "matriz_evidencia.csv", MATRIZ, fields_matrix)

    fields_locations = ["archivo", "linea", "seccion", "cambio", "propuesta", "decisiones"]
    write_csv(
        DATA_DIR / "ubicaciones_texto.csv",
        [
            {
                "archivo": archivo,
                "linea": linea,
                "seccion": seccion,
                "cambio": cambio,
                "propuesta": propuesta,
                "decisiones": decisiones,
            }
            for archivo, linea, seccion, cambio, propuesta, decisiones in UBICACIONES
        ],
        fields_locations,
    )

    fields_phrases = ["frase", "ubicacion", "reemplazo", "motivo"]
    write_csv(
        DATA_DIR / "frases_a_eliminar.csv",
        [{"frase": frase, "ubicacion": ubicacion, "reemplazo": reemplazo, "motivo": motivo} for frase, ubicacion, reemplazo, motivo in FRASES],
        fields_phrases,
    )

    status_counts: dict[str, int] = {}
    for row in TABLA4:
        status_counts[row["estado"]] = status_counts.get(row["estado"], 0) + 1
    summary = {
        "n_filas_tabla4": len(TABLA4),
        "estados": status_counts,
        "estados_normalizados": {
            "se_conserva": sum(row["categoria"] == "Se conserva" for row in TABLA4),
            "se_reformula": sum(row["categoria"] == "Se reformula" for row in TABLA4),
            "se_retira": sum(row["categoria"] == "Se retira" for row in TABLA4),
        },
        "n_evidencias": len(MATRIZ),
        "n_ubicaciones": len(UBICACIONES),
        "n_frases": len(FRASES),
        "decisiones": [f"D-{i:02d}" for i in range(1, 15)],
    }
    (OUT_DIR / "resumen_conclusiones.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Tablas de conclusiones generadas en", DATA_DIR)


if __name__ == "__main__":
    main()

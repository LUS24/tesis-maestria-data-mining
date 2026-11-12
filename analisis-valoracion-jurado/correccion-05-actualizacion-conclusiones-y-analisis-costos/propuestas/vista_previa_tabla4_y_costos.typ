#set page(paper: "a4", flipped: true, margin: 1.1cm)
#set text(font: "New Computer Modern", size: 7pt, lang: "es")
#set par(justify: true, leading: 0.55em)
#set table(stroke: 0.3pt, inset: 3pt)

#align(center)[
  #text(size: 15pt, weight: "bold")[Corrección IX.1.5 — vista previa para revisión]
  #v(0.2em)
  #text(size: 8pt)[Tabla 4 reformulada y costos. No es parte del manuscrito.]
]

#v(0.8em)

= Tabla 4 — síntesis

#table(
  columns: (1.05cm, 4.2cm, 2.7cm, 13.7cm),
  [*ID*], [*Conclusión original*], [*Estado*], [*Formulación propuesta (síntesis)*],
  [T4-01], [La recuperación mejora significativamente.], [Se reformula], [No hay mejora uniforme: depende de estrategia y modelo. En gpt-5-mini mejoran RAG básico y Agentic; en gpt-5 solo Agentic; en nano Agentic es inferior.],
  [T4-02], [La interacción es el hallazgo principal.], [Se conserva con matices], [Interacción fuerte (LR = 293,28; gl = 4; p = 3,05 × 10⁻⁶²). No identifica un componente causal único: recuperador fijo gpt-5 y límites 7/6.],
  [T4-03], [Efecto igualador del RAG básico.], [Se retira], [Las diferencias se reducen, pero no desaparecen: mini−nano +0,063; gpt-5−nano +0,128; gpt-5−mini +0,065. No se demostró equivalencia.],
  [T4-04], [Sobrecarga agéntica en modelos pequeños.], [Se retira como causa], [41/79 salidas no sustantivas en Agentic + nano; 38/79 sustantivas con media 0,820. Modo de fallo, no degradación uniforme ni causa “agéntica”.],
  [T4-05], [Validación de LLM-as-a-Judge.], [Se retira “validación”], [α = 0,808/0,800: acuerdo, no validez humana. 12 evaluaciones de corrección > 0 sobre salidas no sustantivas.],
  [T4-06], [Objetivo 2 cumplido completamente.], [Se reformula], [Cumplimiento parcial: dos agentes activos, una delegación, sin verificador. El Agente de Calidad nunca se ejecutó.],
  [T4-07], [Agentic-RAG + mini es costo-eficiente.], [Se retira y se reemplaza por Pareto], [Cuesta USD 0,0564, más que RAG gpt-5 (0,0392) y Sin RAG gpt-5 (0,0478). Es no dominada, no la más barata. RAG nano: USD 0,0061 por aceptable.],
  [T4-08], [Resultado transferible a otros dominios.], [Se retira], [Un corpus, 25 casos, una ejecución y recuperador fijo. Es una hipótesis, no transferibilidad demostrada.],
  [T4-09], [Usuarios profesionales y repositorio abierto.], [Se reformula], [Sin interfaz ni evaluación con usuarios. Repositorio público verificado; clonación limpia final pendiente.],
)

#v(0.8em)

= Costos por celda y frontera de Pareto

#table(
  columns: (3.1cm, 1.8cm, 2.3cm, 2.3cm, 2.0cm, 2.2cm, 2.2cm, 2.5cm),
  [*Celda*], [*Costo medio*], [*Costo total*], [*Media corrección*], [*Aceptables ≥ 0,75*], [*Costo por aceptable*], [*Pareto*], [*Frec. bootstrap*],
  [Sin RAG + nano], [0,0025], [0,1981], [0,565], [26/79], [0,0076], [Sí], [67,7%],
  [Sin RAG + mini], [0,0043], [0,3395], [0,325], [11/79], [0,0309], [No], [0,0%],
  [Sin RAG + gpt-5], [0,0478], [3,7731], [0,725], [49/79], [0,0770], [Sí], [65,7%],
  [RAG + nano], [0,0025], [0,2011], [0,599], [33/79], [*0,0061*], [Sí], [76,0%],
  [RAG + mini], [0,0057], [0,4465], [0,650], [38/79], [0,0117], [Sí], [95,0%],
  [RAG + gpt-5], [0,0392], [3,0997], [0,707], [52/79], [0,0596], [Sí], [94,3%],
  [Agentic + nano], [0,0447], [3,5299], [0,395], [27/79], [0,1307], [No], [0,0%],
  [Agentic + mini], [0,0564], [4,4530], [0,788], [55/79], [0,0810], [Sí], [91,9%],
  [Agentic + gpt-5], [0,0792], [6,2530], [0,812], [56/79], [0,1117], [Sí], [69,4%],
)

#v(0.6em)
#text(size: 6.5pt)[
  Costos en USD, precios históricos registrados. “Aceptables” usa el escenario fallo = 0 y umbral ≥ 0,75. La frecuencia bootstrap indica la proporción de 5.000 remuestreos por casos en que la celda permanece en la frontera. El total del experimento es USD 22,2939. La configuración con menor costo puntual por aceptable es RAG básico + gpt-5-nano, con IC solapado con Sin RAG + nano; la de mayor media es Agentic-RAG + gpt-5; Agentic-RAG + gpt-5-mini es una alternativa no dominada.
]

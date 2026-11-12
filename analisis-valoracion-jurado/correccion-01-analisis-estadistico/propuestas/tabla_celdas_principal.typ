#import "@preview/tablem:0.3.0": three-line-table
#figure(
  three-line-table(
    columns: (auto, auto, auto, auto, auto, auto, auto, auto),
    [
      | *Estrategia* | *Modelo* | *n* | *No sust.* | *Media* | *Mediana* | *P(≥ 0,75)* | *Media exclusión* |
      | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
      | Sin RAG | gpt-5-nano | 79 | 1 | 0,565 | 0,583 | 0,329 | 0,573 |
      | Sin RAG | gpt-5-mini | 79 | 15 | 0,325 | 0,250 | 0,139 | 0,401 |
      | Sin RAG | gpt-5 | 79 | 0 | 0,725 | 0,833 | 0,620 | 0,725 |
      | RAG basico | gpt-5-nano | 79 | 0 | 0,599 | 0,583 | 0,418 | 0,599 |
      | RAG basico | gpt-5-mini | 79 | 0 | 0,650 | 0,667 | 0,481 | 0,650 |
      | RAG basico | gpt-5 | 79 | 0 | 0,707 | 0,833 | 0,658 | 0,707 |
      | Agentic-RAG | gpt-5-nano | 79 | 41 | 0,395 | 0,000 | 0,342 | 0,820 |
      | Agentic-RAG | gpt-5-mini | 79 | 1 | 0,788 | 1,000 | 0,696 | 0,798 |
      | Agentic-RAG | gpt-5 | 79 | 0 | 0,812 | 1,000 | 0,709 | 0,812 |
    ],
  ),
  caption: [Estadísticos descriptivos por configuración bajo el escenario principal (respuestas no sustantivas = 0). La columna de exclusión usa solo respuestas sustantivas y es una sensibilidad, no el escenario principal.],
) <tabla-analisis-celdas>

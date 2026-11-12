#import "@preview/tablem:0.3.0": three-line-table
#figure(
  three-line-table(
    columns: (auto, auto, auto, auto, auto, auto),
    [
      | *Bloque* | *Contraste* | *Δ media* | *IC 95%* | *Δ P(≥ 0,75)* | *IC 95%* |
      | :--- | :--- | ---: | :--- | ---: | :--- |
      | gpt-5-nano | Agentic-RAG - RAG basico | -0,270 | -0,330 a -0,202 | -0,308 | -0,382 a -0,225 |
      | gpt-5-nano | Agentic-RAG - Sin RAG | -0,242 | -0,307 a -0,176 | -0,270 | -0,349 a -0,192 |
      | gpt-5-nano | RAG basico - Sin RAG | 0,028 | -0,032 a 0,085 | 0,037 | -0,043 a 0,114 |
      | gpt-5-mini | Agentic-RAG - RAG basico | 0,150 | 0,096 a 0,203 | 0,210 | 0,134 a 0,283 |
      | gpt-5-mini | Agentic-RAG - Sin RAG | 0,513 | 0,455 a 0,562 | 0,630 | 0,564 a 0,680 |
      | gpt-5-mini | RAG basico - Sin RAG | 0,363 | 0,304 a 0,417 | 0,420 | 0,343 a 0,488 |
      | gpt-5 | Agentic-RAG - RAG basico | 0,106 | 0,054 a 0,155 | 0,146 | 0,074 a 0,216 |
      | gpt-5 | Agentic-RAG - Sin RAG | 0,095 | 0,046 a 0,146 | 0,130 | 0,063 a 0,202 |
      | gpt-5 | RAG basico - Sin RAG | -0,011 | -0,063 a 0,044 | -0,016 | -0,089 a 0,062 |
    ],
  ),
  caption: [Efectos simples de estrategia dentro de cada modelo bajo el escenario principal. Diferencias orientadas como Agentic-RAG − RAG básico, Agentic-RAG − Sin RAG y RAG básico − Sin RAG. IC 95% por simulación del modelo ordinal; los p de Holm están en el informe.],
) <tabla-analisis-efectos>

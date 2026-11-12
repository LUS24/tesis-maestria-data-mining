#import "@preview/tablem:0.3.0": three-line-table
#figure(
  three-line-table(
    columns: (auto, auto, auto, auto, auto, auto),
    [
      | *Bloque* | *Contraste* | *Δ media* | *IC 95%* | *Δ P(≥ 0,75)* | *IC 95%* |
      | :--- | :--- | ---: | :--- | ---: | :--- |
      | Sin RAG | gpt-5-mini - gpt-5-nano | -0,272 | -0,325 a -0,212 | -0,294 | -0,366 a -0,221 |
      | Sin RAG | gpt-5 - gpt-5-nano | 0,167 | 0,108 a 0,224 | 0,233 | 0,150 a 0,309 |
      | Sin RAG | gpt-5 - gpt-5-mini | 0,438 | 0,379 a 0,491 | 0,527 | 0,451 a 0,589 |
      | RAG basico | gpt-5-mini - gpt-5-nano | 0,063 | 0,005 a 0,119 | 0,088 | 0,008 a 0,165 |
      | RAG basico | gpt-5 - gpt-5-nano | 0,128 | 0,071 a 0,186 | 0,180 | 0,100 a 0,259 |
      | RAG basico | gpt-5 - gpt-5-mini | 0,065 | 0,011 a 0,124 | 0,093 | 0,016 a 0,174 |
      | Agentic-RAG | gpt-5-mini - gpt-5-nano | 0,483 | 0,419 a 0,539 | 0,605 | 0,533 a 0,662 |
      | Agentic-RAG | gpt-5 - gpt-5-nano | 0,504 | 0,440 a 0,560 | 0,634 | 0,566 a 0,687 |
      | Agentic-RAG | gpt-5 - gpt-5-mini | 0,021 | -0,023 a 0,067 | 0,029 | -0,031 a 0,091 |
    ],
  ),
  caption: [Efectos simples de modelo dentro de cada estrategia bajo el escenario principal. Diferencias orientadas como gpt-5-mini − gpt-5-nano, gpt-5 − gpt-5-nano y gpt-5 − gpt-5-mini. IC 95% por simulación del modelo ordinal; los p de Holm están en el informe.],
) <tabla-reanalisis-efectos>

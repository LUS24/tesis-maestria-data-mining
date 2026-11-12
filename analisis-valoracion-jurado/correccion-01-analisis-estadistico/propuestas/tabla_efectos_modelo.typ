#import "@preview/tablem:0.3.0": three-line-table
#figure(
  three-line-table(
    columns: (auto, auto, auto, auto, auto, auto),
    [
      | *Bloque* | *Contraste* | *Δ media* | *IC 95%* | *Δ P(≥ 0,75)* | *IC 95%* |
      | :--- | :--- | ---: | :--- | ---: | :--- |
      | Sin RAG | gpt-5-mini - gpt-5-nano | -0,273 | -0,328 a -0,212 | -0,295 | -0,366 a -0,223 |
      | Sin RAG | gpt-5 - gpt-5-nano | 0,167 | 0,110 a 0,225 | 0,233 | 0,153 a 0,309 |
      | Sin RAG | gpt-5 - gpt-5-mini | 0,440 | 0,380 a 0,493 | 0,528 | 0,452 a 0,589 |
      | RAG basico | gpt-5-mini - gpt-5-nano | 0,063 | 0,005 a 0,120 | 0,087 | 0,007 a 0,166 |
      | RAG basico | gpt-5 - gpt-5-nano | 0,128 | 0,071 a 0,186 | 0,180 | 0,100 a 0,260 |
      | RAG basico | gpt-5 - gpt-5-mini | 0,065 | 0,011 a 0,124 | 0,093 | 0,015 a 0,174 |
      | Agentic-RAG | gpt-5-mini - gpt-5-nano | 0,483 | 0,419 a 0,539 | 0,605 | 0,534 a 0,660 |
      | Agentic-RAG | gpt-5 - gpt-5-nano | 0,504 | 0,439 a 0,561 | 0,634 | 0,567 a 0,686 |
      | Agentic-RAG | gpt-5 - gpt-5-mini | 0,021 | -0,023 a 0,066 | 0,029 | -0,031 a 0,089 |
    ],
  ),
  caption: [Efectos simples de modelo dentro de cada estrategia bajo el escenario principal. Diferencias orientadas como gpt-5-mini − gpt-5-nano, gpt-5 − gpt-5-nano y gpt-5 − gpt-5-mini. IC 95% por simulación del modelo ordinal; los p de Holm están en el informe.],
) <tabla-analisis-efectos>

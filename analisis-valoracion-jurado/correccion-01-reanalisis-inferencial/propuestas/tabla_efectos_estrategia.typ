#import "@preview/tablem:0.3.0": three-line-table
#figure(
  three-line-table(
    columns: (auto, auto, auto, auto, auto, auto),
    [
      | *Bloque* | *Contraste* | *Δ media* | *IC 95%* | *Δ P(≥ 0,75)* | *IC 95%* |
      | :--- | :--- | ---: | :--- | ---: | :--- |
      | gpt-5-nano | Agentic-RAG - RAG basico | -0,270 | -0,330 a -0,203 | -0,308 | -0,382 a -0,224 |
      | gpt-5-nano | Agentic-RAG - Sin RAG | -0,243 | -0,307 a -0,177 | -0,271 | -0,348 a -0,193 |
      | gpt-5-nano | RAG basico - Sin RAG | 0,027 | -0,032 a 0,086 | 0,037 | -0,042 a 0,116 |
      | gpt-5-mini | Agentic-RAG - RAG basico | 0,150 | 0,097 a 0,203 | 0,210 | 0,135 a 0,283 |
      | gpt-5-mini | Agentic-RAG - Sin RAG | 0,512 | 0,453 a 0,562 | 0,629 | 0,563 a 0,680 |
      | gpt-5-mini | RAG basico - Sin RAG | 0,362 | 0,302 a 0,417 | 0,419 | 0,341 a 0,487 |
      | gpt-5 | Agentic-RAG - RAG basico | 0,106 | 0,054 a 0,157 | 0,146 | 0,075 a 0,218 |
      | gpt-5 | Agentic-RAG - Sin RAG | 0,095 | 0,045 a 0,145 | 0,130 | 0,062 a 0,201 |
      | gpt-5 | RAG basico - Sin RAG | -0,011 | -0,063 a 0,043 | -0,016 | -0,089 a 0,060 |
    ],
  ),
  caption: [Efectos simples de estrategia dentro de cada modelo bajo el escenario principal. Diferencias orientadas como Agentic-RAG − RAG básico, Agentic-RAG − Sin RAG y RAG básico − Sin RAG. IC 95% por simulación del modelo ordinal; los p de Holm están en el informe.],
) <tabla-reanalisis-efectos>

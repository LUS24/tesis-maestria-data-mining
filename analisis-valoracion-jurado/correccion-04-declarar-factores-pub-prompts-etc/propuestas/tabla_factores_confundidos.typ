// Alternativa standalone a la tabla de la sección 8 de cambios_manuscrito.md.
// Insertar una sola de las dos versiones para no duplicar la etiqueta.
#import "@preview/tablem:0.3.0": three-line-table
#figure(
  text(size: 9pt)[
    #three-line-table(
      columns: (2.4cm, 3.0cm, 3.0cm, 1fr),
      [
        | *Dimensión* | *Sin RAG* | *RAG básico* | *Agentic-RAG observado* |
        | :--- | :--- | :--- | :--- |
        | Modelo que redacta | variable | variable | variable: gpt-5-nano, mini o gpt-5 |
        | Modelo que recupera | — | — | gpt-5 en las tres configuraciones |
        | Prompt | `sin_rag_system` | `rag_basico_system_template` | `especialista_legal_system` |
        | Consulta de recuperación | — | consulta original, una búsqueda | delegada; hasta 3 subconsultas |
        | Candidatos | — | top-10 | hasta 5 por búsqueda; 6 búsquedas en mini/nano y 7 en gpt-5 |
        | Selección | — | top-10 por similitud | gpt-5 selecciona los documentos devueltos |
        | Iteración del especialista | — | — | una delegación nominal; sin segunda ronda |
        | Verificación | — | — | Agente de Calidad definido, nunca ejecutado |
        | Ablación | — | — | no realizada |
      ],
    )
  ],
  caption: [Diferencias simultáneas entre las estrategias. No constituyen un factorial de un único factor y, sin ablaciones, no permiten atribuir el efecto observado a la descomposición, al número de candidatos, a la selección o al cambio de prompt.],
) <tabla-factores-confundidos>

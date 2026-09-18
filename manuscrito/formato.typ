// Utilidades de formato compartidas por los capítulos del manuscrito.
//
// Uso desde un capítulo:
//   #import "../formato.typ": pagina-apaisada
//
// Nota: los archivos incluidos con `#include` no comparten el ámbito de
// variables de main.typ (solo heredan sus reglas `show`/`set`), por lo que
// estas utilidades deben importarse explícitamente en cada capítulo que las use.

// Página apaisada (horizontal) con el contenido centrado horizontal y
// verticalmente respecto de la hoja. Se emplea para figuras y tablas anchas
// que requieren toda la hoja para visualizarse correctamente.
#let pagina-apaisada(body) = {
  pagebreak(weak: true)
  page(flipped: true, margin: 2cm)[
    #place(center + horizon, body)
  ]
  pagebreak(weak: true)
}

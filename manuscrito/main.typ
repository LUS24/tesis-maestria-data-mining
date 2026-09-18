#import "@preview/mmdr:0.2.2"

#set document(
  title: "Desarrollo y evaluación de un prototipo de sistema inteligente para consulta de normativa nacional argentina mediante recuperación agéntica",
  author: "Leonardo Ulises Spairani",
)
#set page(paper: "a4", margin: 2.5cm, numbering: "i")
#set text(font: "New Computer Modern", size: 12pt, lang: "es")
#set par(justify: true, leading: 0.65em)
#set par.line(numbering: "1") // TODO: quitar cuando se prepare la versión final.
#set heading(numbering: "1.1")
#show outline.entry: set par(justify: true)

// Todos los enlaces del documento se muestran en azul (#0000FF), tanto en el
// cuerpo del texto como en las URLs de la lista de referencias.
#show link: set text(fill: rgb("#0000FF"))

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  text(18pt, weight: "bold", it)
  v(0.5em)
}

// Estilo de captions: texto más pequeño para diferenciar del cuerpo
#show figure.caption: set text(size: 10pt)

// Corrección para las citas dentro del texto
#show cite: it => {
  // Cambia "et al." por "y col."
  show regex("et\s+al\.?"): [y col.]
  // Cambia "& others" por "y cols." dentro de los paréntesis
  show regex("\s*&\s*others"): [ y cols.]
  it
}

// Corrección para la lista de referencias
#show bibliography: it => {
  show regex("et\s+al\.?"): [y col.]
  show regex(",\s*&\s*others\.?"): [, y col.]
  it
}

// ───────────────────────────────────────────
// Portada
// ───────────────────────────────────────────

#page(numbering: none)[
  #align(center)[
    #image("media/logo_universidad_austral_ingenieria.png", width: 100%)

    #v(2cm)

    #text(16pt, weight: "bold")[
      Desarrollo y evaluación de un prototipo de sistema inteligente para consulta de normativa nacional argentina mediante recuperación agéntica
    ]

    #v(1cm)

    #text(14pt)[Tesis de Maestría]

    #v(1cm)

    #text(16pt)[Leonardo Ulises Spairani]

    #v(1.5cm)

    #text(14pt)[Tutores]
    #linebreak()
    #text(14pt)[Dra. Laura Lucía Bélfer y Dr. Rafael Crescenzi]

    #v(1fr)

    #{
      let meses = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                   "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
      let d = datetime.today()
      meses.at(d.month() - 1) + ", " + str(d.year())
    }

    #v(0.5cm)

    Versión: #{
      let h = int(sys.inputs.at("hour", default: "0"))
      let m = int(sys.inputs.at("minute", default: "0"))
      let s = int(sys.inputs.at("second", default: "0"))
      let pad = n => if n < 10 { "0" + str(n) } else { str(n) }
      datetime(year: datetime.today().year(), month: datetime.today().month(), day: datetime.today().day(), hour: h, minute: m, second: s).display("[year].[month].[day].[hour].[minute].[second]")
    }
  ]
]

// ───────────────────────────────────────────
// Capítulos preliminares
// ───────────────────────────────────────────

#include "capitulos/01_texto_preliminar.typ"

// Reiniciar numeración arábiga desde el Capítulo 1
#set page(numbering: "1")
#counter(page).update(1)

#include "capitulos/02_capitulo_01_introduccion.typ"

// ───────────────────────────────────────────
// Capítulos principales - Marco Teórico
// ───────────────────────────────────────────

#include "capitulos/03_capitulo_02_fundamentos_e_historia_pln.typ"

#include "capitulos/04_capitulo_03_aplicacion_de_pln_a_dominio_legal.typ"

// ───────────────────────────────────────────
// Capítulos principales - Desarrollo y Evaluación
// ───────────────────────────────────────────

#include "capitulos/05_capitulo_04_marco_teorico_agentic_rag.typ"

#include "capitulos/06_capitulo_05_metodologia.typ"

#include "capitulos/07_capitulo_06_evaluacion.typ"

// ───────────────────────────────────────────
// Capítulos finales
// ───────────────────────────────────────────

#include "capitulos/08_capitulo_07_trabajos_relacionados.typ"

#include "capitulos/09_capitulo_08_conclusion_y_trabajos_futuros.typ"

// ───────────────────────────────────────────
// Bibliografía
// ───────────────────────────────────────────

#bibliography("referencias.bib", title: [Referencias], style: "apa")

// ───────────────────────────────────────────
// Anexos
// ───────────────────────────────────────────

#include "capitulos/anexo_01.typ"

// ───────────────────────────────────────────
// Acrónimos y Siglas
// ───────────────────────────────────────────

#include "capitulos/acronimos_o_siglas.typ"

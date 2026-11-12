#set page(paper: "a4", margin: 2cm)
#set text(font: "New Computer Modern", size: 10pt, lang: "es")

#show cite: it => {
  show regex("et\s+al\.?"): [y cols.]
  show regex("\s*&\s*others"): [ y cols.]
  it
}

#bibliography("../propuestas_bibtex.bib", style: "apa", title: [Bibliografía propuesta])

= Comprobación de compilación

Entradas de prueba: @bozdag2024gender, @magesh2025hallucinationfree, @lewis2020rag,
@codigo_mineria_1919, @niklaus2023lextreme, @devlin2019bert, @hu2022lora,
@dettmers2023qlora, @asai2024selfrag, @zhao2026surveySpringer.

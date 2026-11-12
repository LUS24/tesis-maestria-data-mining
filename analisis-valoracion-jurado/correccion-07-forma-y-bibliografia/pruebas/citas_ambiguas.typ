#set page(paper: "a4", margin: 2cm)
#set text(font: "New Computer Modern", size: 11pt, lang: "es")

#show cite: it => {
  show regex("et\s+al\.?"): [y col.]
  show regex("\s*&\s*others"): [ y cols.]
  it
}

#bibliography("../../../manuscrito/referencias.bib", style: "apa", title: [Referencias])

= Prueba de desambiguación

Forma normal CoT: #cite(<wei2022cot>).

Forma normal emergent: #cite(<wei2022emergent>).

Forma año CoT: Wei, Wang, et al. #cite(<wei2022cot>, form: "year").

Forma año emergent: Wei, Tay, et al. #cite(<wei2022emergent>, form: "year").

Forma autor CoT: #cite(<wei2022cot>, form: "author") (2022).

Forma autor emergent: #cite(<wei2022emergent>, form: "author") (2022).

Forma normal Zhao survey: #cite(<zhao2026surveySpringer>).

Forma normal Zhao logic: #cite(<zhao2026reportlogic>).

Forma año Zhao survey: W. X. Zhao et al. #cite(<zhao2026surveySpringer>, form: "year").

Forma año Zhao logic: J. Zhao et al. #cite(<zhao2026reportlogic>, form: "year").

Forma autor Zhao survey: #cite(<zhao2026surveySpringer>, form: "author") (2026).

Forma autor Zhao logic: #cite(<zhao2026reportlogic>, form: "author") (2026).
